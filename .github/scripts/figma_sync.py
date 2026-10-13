#!/usr/bin/env python3
"""figma_sync.py — pull a course's Figma figures into its repo (D3 sync against the D4 contract).

Reads `figma-assets.json`, exports every selected `illustration` as SVG through the Figma REST
Images endpoint, writes it to `out.path` only when the bytes changed, and records
`provenance.synced` + `status`. An `animation` is exported as the built scene frame (SVG with
`data-node-id`) and rendered to animated SVG when `--renderer` and a `tracks.json` next to the
spec exist; otherwise it is skipped with a reason. The whole file is never fetched: nodes are
addressed by id, and a page is read (depth 2) only to repair a lost node through the
`⟨<id>⟩` layer-name stamp (contract §3).

Exit codes: 0 ok · 2 some entries ended `broken` (manifest and artifacts still written) ·
1 usage / auth / transport error. Stdlib only. Token: env `FIGMA_TOKEN` — a read-only PAT
(File content: Read, File metadata: Read). The token is sent only to api.figma.com, never to the
S3 download hosts, and never printed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.figma.com"
UA = "learn-figma-sync/1"
BATCH = 20


class SyncError(Exception):
    pass


# ---------------------------------------------------------------- transport

def api(path: str, token: str, params: dict | None = None, tries: int = 5) -> dict:
    """GET api.figma.com with the PAT header; retries 429/5xx with backoff."""
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    for i in range(tries):
        req = urllib.request.Request(url, headers={"X-Figma-Token": token, "User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                wait = int(e.headers.get("Retry-After") or 0) or 5 * 2 ** i
                print(f"  {e.code} on {path} — retry in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise SyncError(f"HTTP {e.code} on {path}: {e.read()[:200]!r}") from None
        except urllib.error.URLError as e:
            if i < tries - 1:
                time.sleep(5 * 2 ** i)
                continue
            raise SyncError(f"network error on {path}: {e.reason}") from None
    raise SyncError(f"gave up on {path}")


def download(url: str, tries: int = 3) -> bytes:
    """GET a render URL (pre-signed storage link) — no token header."""
    for i in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            if i < tries - 1:
                time.sleep(3 * 2 ** i)
                continue
            raise SyncError(f"download failed: {e}") from None
    raise SyncError("download failed")


def export_svg(token: str, file_key: str, node_ids: list[str], include_node_id: bool = False) -> dict[str, str | None]:
    """Images endpoint: returns {nodeId: url|None} (None = Figma could not render / node gone)."""
    out: dict[str, str | None] = {}
    for i in range(0, len(node_ids), BATCH):
        chunk = node_ids[i:i + BATCH]
        params = {"ids": ",".join(chunk), "format": "svg", "svg_outline_text": "true"}
        if include_node_id:
            params["svg_include_node_id"] = "true"
        res = api(f"/v1/images/{file_key}", token, params)
        if res.get("err"):
            raise SyncError(f"images endpoint error: {res['err']}")
        imgs = res.get("images", {})
        for nid in chunk:
            out[nid] = imgs.get(nid)
    return out


def file_version(token: str, file_key: str, probe_node: str) -> str:
    """The file's version id, read through the nodes endpoint (no whole-file fetch)."""
    res = api(f"/v1/files/{file_key}/nodes", token, {"ids": probe_node, "depth": 0})
    return str(res.get("version", ""))


# ---------------------------------------------------------------- repair via ⟨id⟩ stamp

def course_pages(token: str, file_key: str, prefix: str) -> list[tuple[str, str]]:
    """Page ids + names of this course (depth-1 read: the page list only)."""
    doc = api(f"/v1/files/{file_key}", token, {"depth": 1})
    return [(p["id"], p["name"]) for p in doc["document"]["children"] if p["name"].startswith(prefix)]


def search_stamp(token: str, file_key: str, page_id: str, stamp: str) -> str | None:
    """Walk one page two levels deep (sections → frames) for a layer name containing the stamp."""
    res = api(f"/v1/files/{file_key}/nodes", token, {"ids": page_id, "depth": 2})
    page = res["nodes"].get(page_id, {}).get("document", {})
    for sec in page.get("children", []):
        if sec.get("name", "").startswith("⏱"):
            continue
        for fr in sec.get("children", []):
            if stamp in fr.get("name", ""):
                return fr["id"]
    return None


def repair(token: str, file_key: str, asset: dict, pages: list[tuple[str, str]]) -> str | None:
    stamp = f"⟨{asset['id']}⟩"
    hint = asset.get("figma", {}).get("page")
    ordered = sorted(pages, key=lambda p: 0 if p[1] == hint else 1)
    for pid, _name in ordered:
        found = search_stamp(token, file_key, pid, stamp)
        if found:
            return found
    return None


# ---------------------------------------------------------------- manifest + files

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_manifest(path: Path) -> tuple[dict, int]:
    text = path.read_text(encoding="utf-8")
    indent = 1
    for line in text.splitlines()[1:3]:
        if line.strip():
            indent = len(line) - len(line.lstrip(" ")) or 1
            break
    return json.loads(text), indent


def save_manifest(path: Path, data: dict, indent: int) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")


def write_if_changed(root: Path, rel: str, data: bytes) -> bool:
    p = root / rel
    if p.exists() and p.read_bytes() == data:
        return False
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    return True


EXT_FOR_FORMAT = {"svg": ".svg", "animated-svg": ".svg", "apng": ".png"}


def path_matches_format(a: dict) -> bool:
    """Refuse to write bytes of one format into a file named for another (a seed defect did that once)."""
    ext = EXT_FOR_FORMAT.get(a["out"].get("format", ""))
    return bool(ext) and a["out"]["path"].lower().endswith(ext)


def select(assets: list[dict], scope: str, keys: set[str], ids: set[str]) -> list[dict]:
    picked = []
    for a in assets:
        if a["kind"] == "native":
            continue
        if keys or ids:
            if a["id"] in ids or a["display"]["key"] in keys:
                picked.append(a)
            continue
        if a["status"] == "orphan":
            continue  # unreferenced figures are exported only on explicit request
        if scope == "pending" and a["status"] not in ("pending", "broken"):
            continue
        picked.append(a)
    return picked


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------- main

def run(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    mpath = root / args.manifest
    manifest, indent = load_manifest(mpath)
    file_key = manifest["figma"]["fileKey"]
    course = manifest["course"]
    prefix = args.page_prefix or f"{course.upper()} ·"
    keys = {k.strip() for k in args.keys.split(",") if k.strip()}
    ids = {k.strip() for k in args.ids.split(",") if k.strip()}
    todo = select(manifest["assets"], args.scope, keys, ids)

    report = {"written": [], "unchanged": [], "repaired": [], "broken": [], "skipped": []}
    for a in [a for a in todo if not path_matches_format(a)]:
        report["skipped"].append((a, f"out.path extension does not match out.format {a['out'].get('format')!r} — not written"))
    todo = [a for a in todo if path_matches_format(a)]
    if args.dry_run:
        for a in todo:
            report["skipped"].append((a, "dry run"))
        return finish(args, manifest, report, version="", wrote_manifest=False)

    token = os.environ.get("FIGMA_TOKEN", "").strip()
    if not token:
        print("FIGMA_TOKEN is not set", file=sys.stderr)
        return 1
    if not todo:
        return finish(args, manifest, report, version="", wrote_manifest=False)

    version = file_version(token, file_key, todo[0]["figma"]["nodeId"])
    stamp = now_iso()
    pages: list[tuple[str, str]] | None = None

    # ---- illustrations: one batched export, then per-entry write
    ills = [a for a in todo if a["kind"] == "illustration"]
    urls = export_svg(token, file_key, [a["figma"]["nodeId"] for a in ills]) if ills else {}
    for a in ills:
        url = urls.get(a["figma"]["nodeId"])
        if url is None:
            if pages is None:
                pages = course_pages(token, file_key, prefix)
            new_id = repair(token, file_key, a, pages)
            if new_id:
                a["figma"]["nodeId"] = new_id
                url = export_svg(token, file_key, [new_id]).get(new_id)
                if url:
                    report["repaired"].append(a)
            if url is None:
                a["status"] = "broken"
                report["broken"].append(a)
                continue
        data = download(url)
        record(a, data, version, stamp, report, root)

    # ---- animations: base export of the built scene frame + renderer
    for a in [a for a in todo if a["kind"] == "animation"]:
        anim_id = a.get("figma", {}).get("motion", {}).get("animId")
        spec = root / a["spec"] if a.get("spec") else None
        tracks = root / a["tracks"] if a.get("tracks") else (spec.with_name("tracks.json") if spec else None)
        if not args.renderer:
            report["skipped"].append((a, "no --renderer (animation pilot pending)"))
            continue
        if not anim_id or not spec or not spec.exists() or not tracks.exists():
            report["skipped"].append((a, "needs figma.motion.animId, spec and tracks.json"))
            continue
        url = export_svg(token, file_key, [anim_id], include_node_id=True).get(anim_id)
        if url is None:
            a["status"] = "broken"
            report["broken"].append(a)
            continue
        base = download(url)
        with tempfile.TemporaryDirectory() as td:
            bp, op = Path(td) / "base.svg", Path(td) / "out.svg"
            bp.write_bytes(base)
            r = subprocess.run([sys.executable, args.renderer, str(bp), str(tracks), str(op)],
                               capture_output=True, text=True)
            if r.returncode != 0 or not op.exists():
                report["skipped"].append((a, f"renderer failed: {r.stderr.strip()[:200]}"))
                continue
            data = op.read_bytes()
        record(a, data, version, stamp, report, root,
               spec_sha=sha256(spec.read_bytes()), tracks_sha=sha256(tracks.read_bytes()))

    save_manifest(mpath, manifest, indent)
    return finish(args, manifest, report, version, wrote_manifest=True)


def record(a: dict, data: bytes, version: str, stamp: str, report: dict, root: Path,
           spec_sha: str | None = None, tracks_sha: str | None = None) -> None:
    changed = write_if_changed(root, a["out"]["path"], data)
    prov = a.setdefault("provenance", {})
    synced = prov.get("synced", {})
    if changed or synced.get("sha256") != sha256(data):
        synced = {"figmaVersion": version, "at": stamp, "sha256": sha256(data)}
        if spec_sha:
            synced["specSha256"] = spec_sha
        if tracks_sha:
            synced["tracksSha256"] = tracks_sha
        prov["synced"] = synced
    if a["status"] in ("pending", "broken"):
        a["status"] = "synced"
    report["written" if changed else "unchanged"].append(a)


def finish(args: argparse.Namespace, manifest: dict, report: dict, version: str, wrote_manifest: bool) -> int:
    lines = [f"## figma-sync · {manifest['course']}", ""]
    lines.append(f"Figma file `{manifest['figma']['fileKey']}`" + (f" · version `{version}`" if version else "") +
                 f" · scope `{args.scope}`" + (f" · keys `{args.keys}`" if args.keys else "") + (f" · ids `{args.ids}`" if args.ids else ""))
    lines.append("")
    lines.append("| result | count |")
    lines.append("|---|---|")
    for k in ("written", "unchanged", "repaired", "broken", "skipped"):
        lines.append(f"| {k} | {len(report[k])} |")
    lines.append("")
    if report["written"]:
        lines += ["### Written", "", "| key | id | file |", "|---|---|---|"]
        lines += [f"| {a['display']['key']} | `{a['id']}` | `{a['out']['path']}` |" for a in report["written"]]
        lines.append("")
    if report["repaired"]:
        lines += ["### Repaired via ⟨id⟩ stamp (nodeId updated in the manifest)", ""]
        lines += [f"- {a['display']['key']} `{a['id']}` → `{a['figma']['nodeId']}`" for a in report["repaired"]]
        lines.append("")
    if report["broken"]:
        lines += ["### ⚠ Broken — node gone and no ⟨id⟩ stamp found", ""]
        lines += [f"- {a['display']['key']} `{a['id']}` (was `{a['figma']['nodeId']}`)" for a in report["broken"]]
        lines.append("")
    if report["skipped"]:
        lines += ["### Skipped", ""]
        lines += [f"- {a['display']['key']} `{a['id']}` — {why}" for a, why in report["skipped"]]
        lines.append("")
    if not wrote_manifest:
        lines.append("_Manifest not modified._")
    text = "\n".join(lines) + "\n"
    print(text)
    if args.summary:
        Path(args.summary).write_text(text, encoding="utf-8")
    return 2 if report["broken"] else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=".", help="course repo root (default: cwd)")
    ap.add_argument("--manifest", default="figma-assets.json", help="manifest path relative to root")
    ap.add_argument("--scope", choices=["pending", "all"], default="pending",
                    help="pending = status pending|broken; all = also re-export synced entries")
    ap.add_argument("--keys", default="", help="comma-separated display keys to sync (overrides scope; includes orphans)")
    ap.add_argument("--ids", default="", help="comma-separated stable ids to sync (overrides scope)")
    ap.add_argument("--renderer", default="", help="path to render.py; animations are skipped without it")
    ap.add_argument("--page-prefix", default="", help="page-name prefix of this course (default '<COURSE> ·')")
    ap.add_argument("--summary", default="", help="write the markdown report here (e.g. $GITHUB_STEP_SUMMARY)")
    ap.add_argument("--dry-run", action="store_true", help="select only; no network, no writes")
    args = ap.parse_args(argv)
    try:
        return run(args)
    except SyncError as e:
        print(f"figma-sync: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
