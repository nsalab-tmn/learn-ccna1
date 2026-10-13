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


CSS_BLEND = {"MULTIPLY": "multiply", "SCREEN": "screen", "OVERLAY": "overlay", "DARKEN": "darken", "LIGHTEN": "lighten",
             "COLOR_DODGE": "color-dodge", "COLOR_BURN": "color-burn", "HARD_LIGHT": "hard-light", "SOFT_LIGHT": "soft-light",
             "DIFFERENCE": "difference", "EXCLUSION": "exclusion", "HUE": "hue", "SATURATION": "saturation", "COLOR": "color",
             "LUMINOSITY": "luminosity", "LINEAR_BURN": "multiply", "LINEAR_DODGE": "screen"}


def blend_map(node: dict) -> dict[str, str]:
    """{nodeId: css blend} for every node in the subtree whose layer blend mode is not normal."""
    out: dict[str, str] = {}
    stack = [node]
    while stack:
        n = stack.pop()
        css = CSS_BLEND.get(n.get("blendMode", "NORMAL"))
        if css:
            out[n["id"]] = css
        stack.extend(n.get("children", []))
    return out


def reinject_blend_modes(svg: str, blends: dict[str, str]) -> tuple[str, int]:
    """Figma's REST SVG export drops `mix-blend-mode` on plain shapes (ellipses, vectors) while the
    desktop export keeps it; the elements are still addressable via data-node-id (svg_include_node_id=true),
    so put the layer's blend mode back as an inline style where it is missing."""
    import re
    added = 0
    for nid, css in blends.items():
        pat = re.compile(r'<([a-zA-Z]+)([^>]*\sdata-node-id="' + re.escape(nid) + r'")([^>]*?)(/?)>')
        def fix(m: "re.Match[str]") -> str:
            nonlocal added
            head, mid, rest, close = m.group(1), m.group(2), m.group(3), m.group(4)
            if "mix-blend-mode" in rest or "mix-blend-mode" in mid:
                return m.group(0)
            added += 1
            sm = re.search(r'\sstyle="([^"]*)"', rest)
            if sm:
                rest = rest[:sm.start()] + f' style="{sm.group(1).rstrip(";")};mix-blend-mode:{css}"' + rest[sm.end():]
            else:
                rest = rest + f' style="mix-blend-mode:{css}"'
            return f"<{head}{mid}{rest}{close}>"
        svg = pat.sub(fix, svg, count=1)
    return svg, added


def paint_blend_map(node: dict) -> dict[str, list[tuple[int, str]]]:
    """{nodeId: [(index among visible fills, css blend)]} for fills that carry their own blend mode
    (e.g. a grey noise texture multiplied over a device face). The exporter emits one element per visible
    fill, bottom first, inside the node's <g data-node-id>, and drops the paint's blend when the paint
    has an opacity < 1 — that is what turns switch faces grey."""
    out: dict[str, list[tuple[int, str]]] = {}
    stack = [node]
    while stack:
        n = stack.pop()
        fills = [f for f in (n.get("fills") or []) if f.get("visible", True)]
        items = [(k, CSS_BLEND[f["blendMode"]]) for k, f in enumerate(fills) if CSS_BLEND.get(f.get("blendMode", "NORMAL"))]
        if items:
            out[n["id"]] = items
        stack.extend(n.get("children", []))
    return out


def _element_span(svg: str, start: int) -> tuple[int, int]:
    """[start, end) of the element whose '<' is at `start` (self-closing or with matching close tag)."""
    import re
    tag = re.match(r"<([a-zA-Z]+)", svg[start:]).group(1)
    gt = svg.index(">", start)
    if svg[gt - 1] == "/":
        return start, gt + 1
    pat = re.compile(r"<(/?)" + re.escape(tag) + r"\b[^>]*?(/?)>")
    depth, pos = 1, gt + 1
    while depth:
        mm = pat.search(svg, pos)
        if not mm:
            return start, len(svg)
        if mm.group(1):
            depth -= 1
        elif not mm.group(2):
            depth += 1
        pos = mm.end()
    return start, pos


def reinject_paint_blends(svg: str, pmap: dict[str, list[tuple[int, str]]]) -> tuple[str, int]:
    """Wrap the k-th fill element of a node in <g style="mix-blend-mode:…"> when the paint's blend was
    dropped — the same form the desktop export uses."""
    import re
    added = 0
    for nid, items in pmap.items():
        m = re.search(r'<([a-zA-Z]+)[^>]*\sdata-node-id="' + re.escape(nid) + r'"', svg)
        if not m:
            continue
        s, e = _element_span(svg, m.start())
        block = svg[s:e]
        if m.group(1) == "g":
            inner_start, inner_end = block.index(">") + 1, block.rfind("</g>")
            kids, pos = [], inner_start
            while True:
                k = block.find("<", pos, inner_end)
                if k < 0:
                    break
                ks, ke = _element_span(block, k)
                kids.append((ks, ke))
                pos = ke
        else:
            kids = [(0, len(block))]
        new_block = block
        for k, css in sorted(items, reverse=True):
            if k >= len(kids):
                continue
            ks, ke = kids[k]
            child = block[ks:ke]
            if "mix-blend-mode" in child[: child.find(">") + 1]:
                continue
            new_block = new_block[:ks] + f'<g style="mix-blend-mode:{css}">' + child + "</g>" + new_block[ke:]
            added += 1
        svg = svg[:s] + new_block + svg[e:]
    return svg, added


def node_docs(token: str, file_key: str, node_ids: list[str]) -> dict[str, dict]:
    """Subtrees for the given nodes (one call per batch) — used for blend-mode re-injection."""
    out: dict[str, dict] = {}
    for i in range(0, len(node_ids), BATCH):
        chunk = node_ids[i:i + BATCH]
        res = api(f"/v1/files/{file_key}/nodes", token, {"ids": ",".join(chunk)})
        for nid, v in (res.get("nodes") or {}).items():
            if v and v.get("document"):
                out[nid] = v["document"]
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


def image_paint_nodes(node: dict, visible: bool = True):
    """Yield (node, n) for every visible node carrying n visible IMAGE paints (fills + strokes)."""
    visible = visible and node.get("visible", True)
    if visible:
        n = sum(1 for p in node.get("fills", []) + node.get("strokes", [])
                if p.get("type") == "IMAGE" and p.get("visible", True))
        if n:
            yield node, n
    for c in node.get("children", []):
        yield from image_paint_nodes(c, visible)


def degraded(svg: bytes, doc: dict) -> tuple[int, int] | None:
    """The REST exporter intermittently drops every image fill of a node — the element is there, its
    `fill="url(#pattern…)"` and the <defs> image are not (11 of 325 figures in one run, 2026-10-13).
    Checks each image-painted node that the export emitted (`data-node-id` present; nodes the
    exporter leaves out altogether — clipped, empty — are not a fill loss): its own element and the
    fill elements before the next node must reference a pattern per image paint. Returns
    (got, expected) when short, else None."""
    if not doc:
        return None
    text = svg.decode("utf-8", "replace")
    expected = got = 0
    for node, n in image_paint_nodes(doc):
        i = text.find(f'data-node-id="{node["id"]}"')
        if i < 0:
            # Absent from the export. Figma's own verdict decides: a node it renders (absoluteRenderBounds
            # set) must be there; one it does not (null — no geometry, clipped away) is not a loss.
            if node.get("absoluteRenderBounds"):
                expected += n
            continue
        j = text.find("data-node-id=", i + 14)
        expected += n
        got += min(n, text.count("url(#pattern", i, j if j > 0 else len(text)))
    return (got, expected) if got < expected else None


def fetch_svg(token: str, file_key: str, url: str, node_id: str, doc: dict) -> tuple[bytes, str | None, int]:
    """Download one export; re-export once if its image fills are missing; re-inject the blend modes the
    exporter dropped. Returns (data, skip_reason, blends_reinjected) — a skip means the committed file
    is kept, so a flaky export can never replace a faithful one."""
    data = download(url)
    short = degraded(data, doc)
    if short:
        retry = export_svg(token, file_key, [node_id], include_node_id=True).get(node_id)
        if retry:
            data = download(retry)
            short = degraded(data, doc)
    if short:
        return data, f"degraded export — {short[0]} of {short[1]} image fills came back, twice; committed file kept", 0
    n = 0
    blends, pblends = blend_map(doc), paint_blend_map(doc)
    if blends or pblends:
        text = data.decode("utf-8")
        text, n1 = reinject_blend_modes(text, blends)
        text, n2 = reinject_paint_blends(text, pblends)
        n = n1 + n2
        if n:
            data = text.encode("utf-8")
    return data, None, n


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

    # ---- illustrations: one batched export, then per-entry write.
    # Always with svg_include_node_id=true: besides making every layer addressable, it makes the exporter
    # keep layer blend modes (mix-blend-mode wrappers) that it drops from a plain export — the desktop
    # export keeps them, so this is what matches the hand-made renders. The re-injection below is the
    # safety net for any blend the exporter still loses.
    ills = [a for a in todo if a["kind"] == "illustration"]
    urls = export_svg(token, file_key, [a["figma"]["nodeId"] for a in ills], include_node_id=True) if ills else {}
    docs = node_docs(token, file_key, [a["figma"]["nodeId"] for a in ills]) if ills else {}
    for a in ills:
        url = urls.get(a["figma"]["nodeId"])
        if url is None:
            if pages is None:
                pages = course_pages(token, file_key, prefix)
            new_id = repair(token, file_key, a, pages)
            if new_id:
                a["figma"]["nodeId"] = new_id
                url = export_svg(token, file_key, [new_id], include_node_id=True).get(new_id)
                if url:
                    report["repaired"].append(a)
                    docs.update(node_docs(token, file_key, [new_id]))
            if url is None:
                a["status"] = "broken"
                report["broken"].append(a)
                continue
        data, why, n = fetch_svg(token, file_key, url, a["figma"]["nodeId"], docs.get(a["figma"]["nodeId"], {}))
        if why:
            report["skipped"].append((a, why))
            continue
        if n:
            report.setdefault("blends", []).append((a, n))
        record(a, data, version, stamp, report, root)

    # ---- animations: base export of the built scene frame + renderer
    for a in [a for a in todo if a["kind"] == "animation"]:
        anim_id = a.get("figma", {}).get("motion", {}).get("animId")
        spec = root / a["spec"] if a.get("spec") else None
        tracks = root / a["tracks"] if a.get("tracks") else (spec.with_name("tracks.json") if spec else None)
        if not args.renderer:
            report["skipped"].append((a, "no --renderer (animation pilot pending)"))
            continue
        # spec.json is the authored op list and exists only for builder-made animations; a Motion build
        # made by hand has none — tracks.json (dumped from the build) is what the renderer needs.
        if not anim_id or not tracks or not tracks.exists() or (spec and not spec.exists()):
            report["skipped"].append((a, "needs figma.motion.animId and tracks.json (and spec.json when listed)"))
            continue
        if not a.get("tracks"):
            a["tracks"] = tracks.relative_to(root).as_posix()  # found next to the spec — record it (schema: synced ⇒ tracks)
        url = export_svg(token, file_key, [anim_id], include_node_id=True).get(anim_id)
        if url is None:
            a["status"] = "broken"
            report["broken"].append(a)
            continue
        base, why, n = fetch_svg(token, file_key, url, anim_id, node_docs(token, file_key, [anim_id]).get(anim_id, {}))
        if why:
            report["skipped"].append((a, why))
            continue
        if n:
            report.setdefault("blends", []).append((a, n))
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
               spec_sha=sha256(spec.read_bytes()) if spec else None, tracks_sha=sha256(tracks.read_bytes()))

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
