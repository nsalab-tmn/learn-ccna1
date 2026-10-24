#!/usr/bin/env python3
"""figma_sync.py — pull a course's Figma figures into its repo (D3 sync against the D4 contract).

Reads `figma-assets.json`, exports every selected `illustration` as SVG through the Figma REST
Images endpoint, writes it to `out.path` only when the bytes changed, and records
`provenance.synced` + `status`. An `animation` is exported as the built scene frame (SVG with
`data-node-id`) and rendered to animated SVG when `--renderer` and a `tracks.json` next to the
spec exist; otherwise it is skipped with a reason. The whole file is never fetched: nodes are
addressed by id, and a page is read (depth 2) only to repair a lost node through the
`⟨<id>⟩` layer-name stamp (contract §3).

An entry with `ref` (a shared figure, contract §2) has no frame of its own: the owner's frame —
found through the owner's entry in this manifest or, for another course's owner, in that course's
manifest on its main (GitHub API, read-only) — is exported into the referrer's own `out.path`, and
its node is cached in the referrer's `figma.nodeId`. `--scope refs` syncs only those entries.

Exit codes: 0 ok · 2 some entries ended `broken` (manifest and artifacts still written) ·
1 usage / auth / transport error. Stdlib only, except that rendering an animation imports
svg_optimize (fonttools, brotli, Pillow), which embeds the fonts of its live text. Token: env `FIGMA_TOKEN` — a read-only PAT
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


def export_svg(token: str, file_key: str, node_ids: list[str], include_node_id: bool = False,
               absolute_bounds: bool = False, outline_text: bool = True) -> dict[str, str | None]:
    """Images endpoint: returns {nodeId: url|None} (None = Figma could not render / node gone).
    absolute_bounds: canvas = the node's own bounding box (content at bbox-relative coordinates), not
    the cropped render bounds — what a standalone export needs to be placed back into its frame.
    outline_text=False keeps text as <text> (animations: svg_optimize embeds the fonts)."""
    out: dict[str, str | None] = {}
    for i in range(0, len(node_ids), BATCH):
        chunk = node_ids[i:i + BATCH]
        params = {"ids": ",".join(chunk), "format": "svg", "svg_outline_text": "true" if outline_text else "false"}
        if include_node_id:
            params["svg_include_node_id"] = "true"
        if absolute_bounds:
            params["use_absolute_bounds"] = "true"
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
    """Find the frame stamped with the entry's own id. Never called for an entry with `ref` (see repair_owner)."""
    return find_stamped(token, file_key, asset["id"], asset.get("figma", {}).get("page"), pages)


def find_stamped(token: str, file_key: str, stamp_id: str, hint: str | None, pages: list[tuple[str, str]]) -> str | None:
    stamp = f"⟨{stamp_id}⟩"
    ordered = sorted(pages, key=lambda p: 0 if p[1] == hint else 1)
    for pid, _name in ordered:
        found = search_stamp(token, file_key, pid, stamp)
        if found:
            return found
    return None


# ---------------------------------------------------------------- shared figures (`ref`, contract §2)

GITHUB_API = "https://api.github.com"
SIBLING_REPO = "nsalab-tmn/learn-{course}"


def github_manifest(repo: str, branch: str = "main", tries: int = 3) -> dict:
    """A sibling course's figma-assets.json on its `branch`, read-only through the GitHub contents API.
    The token (env GH_TOKEN or GITHUB_TOKEN — the workflow's own) goes only to api.github.com; the course
    repos are public, so it only lifts the anonymous rate limit. The Figma token is never sent here."""
    url = f"{GITHUB_API}/repos/{repo}/contents/figma-assets.json?ref={urllib.parse.quote(branch)}"
    headers = {"Accept": "application/vnd.github.raw+json", "User-Agent": UA, "X-GitHub-Api-Version": "2022-11-28"}
    gh = (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or "").strip()
    if gh:
        headers["Authorization"] = f"Bearer {gh}"
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                time.sleep(5 * 2 ** i)
                continue
            raise SyncError(f"HTTP {e.code} reading {repo}@{branch}:figma-assets.json") from None
        except urllib.error.URLError as e:
            if i < tries - 1:
                time.sleep(5 * 2 ** i)
                continue
            raise SyncError(f"network error reading {repo}@{branch}:figma-assets.json: {e.reason}") from None
        except ValueError as e:
            raise SyncError(f"{repo}@{branch}:figma-assets.json is not JSON: {e}") from None
    raise SyncError(f"gave up reading {repo}@{branch}:figma-assets.json")


def course_of(asset_id: str) -> str:
    return asset_id.split("-", 1)[0]


class Owners:
    """Owner manifests by course: this course's own (in memory, so a repair made earlier in the run is
    seen), a sibling's from a local file (--sibling-manifest) or from its repo's main via the GitHub API.
    Read once per course per run; a failed read is remembered as the reason."""

    def __init__(self, manifest: dict, local: dict[str, Path], repo_tmpl: str):
        self.cache: dict[str, dict | str] = {manifest["course"]: manifest}
        self.local, self.repo_tmpl = local, repo_tmpl

    def manifest(self, course: str) -> dict | str:
        if course not in self.cache:
            try:
                if course in self.local:
                    self.cache[course] = json.loads(self.local[course].read_text(encoding="utf-8"))
                else:
                    self.cache[course] = github_manifest(self.repo_tmpl.format(course=course))
            except (OSError, ValueError, SyncError) as e:
                self.cache[course] = f"owner manifest of {course} unreadable: {e}"
        return self.cache[course]


def owner_frame(owner: dict) -> str | None:
    """The frame the owner's own sync exports: the scene frame for an animation, else figma.nodeId."""
    fig = owner.get("figma") or {}
    if owner["kind"] == "animation":
        return (fig.get("motion") or {}).get("animId") or fig.get("nodeId")
    return fig.get("nodeId")


def resolve_owner(a: dict, file_key: str, owners: Owners) -> tuple[dict | None, dict | None, str | None]:
    """(owner entry, owner manifest, None) or (None, None, reason). The checks the schema cannot make:
    the owner exists, is not a referrer itself, is of the same kind, is not the entry, lives in the same
    Figma file and has a frame."""
    ref = a["ref"]
    if ref == a["id"]:
        return None, None, f"`ref` points at the entry itself ({ref})"
    om = owners.manifest(course_of(ref))
    if isinstance(om, str):
        return None, None, om
    owner = next((o for o in om.get("assets", []) if o.get("id") == ref), None)
    if owner is None:
        return None, None, f"unknown owner {ref}: no such id in the {course_of(ref)} manifest"
    if owner.get("ref"):
        return None, None, f"owner {ref} is itself a referrer (ref → {owner['ref']}); a ref never points at another referrer"
    if owner["kind"] != a["kind"]:
        return None, None, f"owner {ref} is of kind {owner['kind']}, this entry of kind {a['kind']}"
    if om.get("figma", {}).get("fileKey") != file_key:
        return None, None, f"owner {ref} lives in another Figma file ({om.get('figma', {}).get('fileKey')})"
    if not owner_frame(owner):
        return None, None, f"owner {ref} has no figma.nodeId"
    return owner, om, None


def tracks_dumps(token: str, file_key: str, node_ids: list[str]) -> dict[str, str | None]:
    """The Motion tracks dump the plugin stored on each frame (shared plugin data nsalab/tracks), raw."""
    out: dict[str, str | None] = {}
    for i in range(0, len(node_ids), BATCH):
        chunk = node_ids[i:i + BATCH]
        res = api(f"/v1/files/{file_key}/nodes", token, {"ids": ",".join(chunk), "plugin_data": "shared", "depth": 1})
        for nid in chunk:
            doc = ((res.get("nodes") or {}).get(nid) or {}).get("document") or {}
            out[nid] = (doc.get("sharedPluginData") or {}).get("nsalab", {}).get("tracks")
    return out


def tracks_bytes(raw: str) -> bytes:
    """A dump as committed: the plugin's JSON verbatim (single line) plus a newline."""
    return raw.strip().encode("utf-8") + b"\n"


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


def image_paint_nodes(node: dict, visible: bool = True, clipped: bool = False, root: bool = True):
    """Yield (node, n, clipped) for every visible node carrying n visible IMAGE paints (fills + strokes);
    `clipped` = it sits under a clipping container other than the exported root (the exporter may cull it)."""
    visible = visible and node.get("visible", True)
    if visible:
        n = sum(1 for p in node.get("fills", []) + node.get("strokes", [])
                if p.get("type") == "IMAGE" and p.get("visible", True))
        if n:
            yield node, n, clipped
    clipped = clipped or (not root and bool(node.get("clipsContent")))
    for c in node.get("children", []):
        yield from image_paint_nodes(c, visible, clipped, root=False)


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
    for node, n, clipped in image_paint_nodes(doc):
        i = text.find(f'data-node-id="{node["id"]}"')
        if i < 0:
            # Absent from the export. Figma's own verdict decides: a node it renders (absoluteRenderBounds
            # set) must be there; one it does not (null — no geometry, clipped away) is not a loss. Under a
            # clipping window the exporter also culls nodes that only graze the window (render bounds set,
            # a few px wide) — those are parked animation layers, not a fill loss (complete_base handles them).
            if node.get("absoluteRenderBounds") and not clipped:
                expected += n
            continue
        j = text.find("data-node-id=", i + 14)
        expected += n
        got += min(n, text.count("url(#pattern", i, j if j > 0 else len(text)))
    return (got, expected) if got < expected else None


def _num(v: float) -> str:
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def _find_elem(svg: str, nid: str) -> tuple[int, int] | None:
    import re
    m = re.search(r'<[a-zA-Z]+[^>]*\sdata-node-id="' + re.escape(nid) + r'"', svg)
    return _element_span(svg, m.start()) if m else None


def _insert_child(svg: str, parent: dict, node: dict, fragment: str) -> str:
    """Put `fragment` where `node` belongs among `parent`'s children (z-order): right after the last earlier
    sibling the export emitted, else first — past the fills the exporter writes before a container's children
    and inside the id-less clip group it opens for an instance."""
    import re
    s, e = _find_elem(svg, parent["id"])
    kids = parent.get("children", [])
    before = kids[:[k["id"] for k in kids].index(node["id"])]
    for k in reversed(before):
        ks = _find_elem(svg, k["id"])
        if ks and s < ks[0] < e:
            return svg[:ks[1]] + fragment + svg[ks[1]:]
    pos = svg.index(">", s) + 1
    head = re.compile(r"\s*<([a-zA-Z]+)([^>]*?)(/?)>")
    while True:
        m = head.match(svg, pos)
        if not m or "data-node-id=" in m.group(2):
            break
        if m.group(1) == "g" and "clip-path=" in m.group(2) and not m.group(3):
            pos = m.end()          # instance content lives inside its clip group
        elif m.group(3):
            pos = m.end()          # a leading fill of the container
        else:
            break
    return svg[:pos] + fragment + svg[pos:]


CONTAINERS = {"GROUP", "FRAME", "INSTANCE", "COMPONENT", "COMPONENT_SET", "SECTION"}


def _clip_box(a: dict | None, b: dict | None) -> dict | None:
    if a is None or b is None:
        return a or b
    x0, y0 = max(a["x"], b["x"]), max(a["y"], b["y"])
    x1, y1 = min(a["x"] + a["width"], b["x"] + b["width"]), min(a["y"] + a["height"], b["y"] + b["height"])
    return {"x": x0, "y": y0, "width": max(0, x1 - x0), "height": max(0, y1 - y0)}


def culled_descendants(node: dict, present) -> list[str]:
    """Visible drawn descendants of a layer the export emitted that the export left out. The exporter culls
    what lies outside a clipping ancestor at rest; for a tracked layer that clipping ancestor is the window it
    moves into, so a part parked outside the window is lost although it shows once the layer moves (6.2.3:
    the arrowhead of 4687:26). Containers the exporter may emit without an id are looked through; children of
    a boolean operation are merged into its path; a part outside a clip INSIDE the layer moves with that
    clip and is legitimately invisible — only parts within every inner clip count. Figma's own render
    bounds decide that a part draws at all."""
    out: list[str] = []

    def rec(n: dict, clip: dict | None, merged: bool) -> None:
        for c in n.get("children", []):
            if not c.get("visible", True) or c.get("opacity", 1) == 0:
                continue
            if not merged and c.get("type") not in CONTAINERS and not present(c["id"]):
                rb = c.get("absoluteRenderBounds")
                box = _clip_box(rb, clip) if rb else None
                if rb and (clip is None or (box["width"] > 0.5 and box["height"] > 0.5)):
                    out.append(c["id"])
                continue
            inner = _clip_box(clip, c.get("absoluteBoundingBox")) if c.get("clipsContent") else clip
            rec(c, inner, merged or c.get("type") == "BOOLEAN_OPERATION")
    rec(node, node.get("absoluteBoundingBox") if node.get("clipsContent") else None, node.get("type") == "BOOLEAN_OPERATION")
    return out


def empty_tracked(svg: str, doc: dict, tracked: list[str]) -> list[str]:
    """Tracked layers that are visible in the scene but come out of the export as nothing (an empty
    element): Figma renders nothing for them — a glyph the font lacks (3.3.2: a `●` typed in Golos Text),
    an empty vector, a lost image. The animation would ship without that part, so the summary flags it."""
    import re
    idx: dict[str, tuple[dict, dict | None]] = {}

    def walk(n: dict, p: dict | None) -> None:
        idx[n["id"]] = (n, p)
        for c in n.get("children", []):
            walk(c, n)
    walk(doc, None)

    def visible(nid: str) -> bool:
        while nid in idx:
            n, p = idx[nid]
            if not n.get("visible", True):
                return False
            if p is None:
                return True
            nid = p["id"]
        return True
    out = []
    for t in tracked:
        if t not in idx or not visible(t) or idx[t][0].get("clipsContent"):
            continue
        if re.search(r'<g\b[^>]*\sdata-node-id="' + re.escape(t) + r'"[^>]*?(/>|>\s*</g>)', svg):
            out.append(t)
    return out


def complete_base(svg: str, doc: dict, tracked: list[str], token: str, file_key: str, outline_text: bool = True
                  ) -> tuple[str, list[str], list[str], str | None]:
    """Put back the tracked layers the frame export left out. The exporter culls a layer that sits entirely
    (or all but a few px) outside a clipping container at rest — exactly how a Motion build parks a wave,
    an arrow or a label that slides into a window, and how an empty window itself disappears. Each such
    layer is exported standalone (its own bounding box as canvas) and injected at its place in the tree
    inside a `<g data-node-id=… data-export-origin="dx dy" transform="translate(dx dy)">`; a missing
    clipping window is synthesised as a `<g clip-path>` with the window's rectangle; a hidden layer gets an
    empty placeholder. A tracked layer the export did emit but with a part culled (`culled_descendants`) is
    re-exported standalone and replaces its truncated element in place. Returns (svg, injected ids, hidden
    ids, skip_reason)."""
    import re
    idx: dict[str, tuple[dict, dict | None]] = {}

    def walk(n: dict, p: dict | None) -> None:
        idx[n["id"]] = (n, p)
        for c in n.get("children", []):
            walk(c, n)
    walk(doc, None)
    present = lambda nid: f'data-node-id="{nid}"' in svg  # noqa: E731
    missing = [t for t in tracked if not present(t)]
    partial = [t for t in tracked if t in idx and present(t) and culled_descendants(idx[t][0], present)]
    if not missing and not partial:
        return svg, [], [], None
    unknown = [t for t in missing if t not in idx]
    if unknown:
        return svg, [], [], f"tracked nodes absent from the export and not in the scene: {unknown}"
    fb = doc.get("absoluteBoundingBox") or {"x": 0, "y": 0}

    def visible(nid: str) -> bool:
        while nid in idx:
            n, p = idx[nid]
            if not n.get("visible", True):
                return False
            if p is None:
                return True
            nid = p["id"]
        return True

    def chain(nid: str) -> list[str]:  # absent ancestors (nearest the root first), then nid
        out = []
        while nid in idx and idx[nid][1] is not None and not present(nid):
            out.append(nid)
            nid = idx[nid][1]["id"]
        return out[::-1]
    def expand(nid: str) -> list[str]:
        """nid, then — when it is a clipping container (synthesised empty below) — its visible absent
        children, depth-first. The exporter culls a parked window together with everything in it, and
        what it shows is usually an untracked instance (the arrow inside a tracked window frame): without
        this the window comes back empty (learn-ccna1#25 review: 6.2.5-1, 16.2.3-2)."""
        out = [nid]
        n = idx[nid][0]
        if n.get("clipsContent") and visible(nid):
            for c in n.get("children", []):
                if c.get("visible", True) and not present(c["id"]):
                    out += expand(c["id"])
        return out
    todo: list[str] = []
    for t in missing:
        for nid in chain(t):
            for x in expand(nid):
                if x not in todo:
                    todo.append(x)
    partial = [t for t in partial if visible(t)]
    cand = [nid for nid in todo if visible(nid) and not idx[nid][0].get("clipsContent")] + partial
    urls = export_svg(token, file_key, cand, include_node_id=True, absolute_bounds=True, outline_text=outline_text) if cand else {}
    injected, hidden, defs = [], [], []
    for nid in todo + partial:
        if nid in partial:
            # present, but a part of it was culled (6.2.3: the arrowhead below its window at rest) — the
            # standalone export of the whole layer replaces the frame export's truncated element
            span = _find_elem(svg, nid)
            if not span or not urls.get(nid):
                continue
        elif present(nid):
            continue  # came along with an ancestor's standalone export
        n, p = idx[nid]
        b = n.get("absoluteBoundingBox") or {"x": fb["x"], "y": fb["y"], "width": 0, "height": 0}
        dx, dy = b["x"] - fb["x"], b["y"] - fb["y"]
        op = f' opacity="{_num(n["opacity"])}"' if n.get("opacity", 1) < 1 else ""
        if not visible(nid):
            fragment, _ = f'<g data-node-id="{nid}"/>', hidden.append(nid)
        elif n.get("clipsContent") and nid not in partial:
            cid = "nsalab-clip-" + nid.replace(":", "-").replace(";", "-")
            defs.append(f'<clipPath id="{cid}"><rect x="{_num(dx)}" y="{_num(dy)}" width="{_num(b["width"])}" height="{_num(b["height"])}"/></clipPath>')
            fragment = f'<g data-node-id="{nid}" clip-path="url(#{cid})"{op}></g>'
            injected.append(nid)
        elif not urls.get(nid):
            fragment = f'<g data-node-id="{nid}"/>'  # Figma renders nothing for it — empty_tracked() reports it
        else:
            data = download(urls[nid])
            short = degraded(data, n)
            if short:
                retry = export_svg(token, file_key, [nid], include_node_id=True, absolute_bounds=True,
                                   outline_text=outline_text).get(nid)
                if retry:
                    data = download(retry)
                    short = degraded(data, n)
            if short:
                return svg, injected, hidden, f"degraded standalone export of {nid} — {short[0]} of {short[1]} image fills, twice; committed file kept"
            text = data.decode("utf-8")
            inner = text[text.index(">", text.index("<svg")) + 1:text.rindex("</svg>")]
            for d in re.findall(r"<defs>.*?</defs>", inner, re.S):
                defs.append(d[6:-7])
                inner = inner.replace(d, "")
            inner = inner.replace(f'data-node-id="{nid}"', f'data-export-root="{nid}"', 1)
            fragment = (f'<g data-node-id="{nid}" data-export-origin="{_num(dx)} {_num(dy)}" '
                        f'transform="translate({_num(dx)} {_num(dy)})"{op}>{inner}</g>')
            if nid in partial:
                injected.append(f"{nid} (culled part)")
                svg = svg[:span[0]] + fragment + svg[span[1]:]  # in place: same z-order, parent may carry no id
                continue
            injected.append(nid)
        svg = _insert_child(svg, p, n, fragment)
    if defs:
        block = "".join(defs)
        svg = svg.replace("</defs>", block + "</defs>", 1) if "</defs>" in svg else svg.replace("</svg>", f"<defs>{block}</defs></svg>")
    return svg, injected, hidden, None


def ensure_window_clips(svg: str, doc: dict, tracked: list[str]) -> tuple[str, list[str]]:
    """The exporter writes a clip-path for a clipping frame only when something overflows it at rest; a
    window whose content slides out during the animation (the bit box of 3.6.4) comes back unclipped and
    the layer rides over the scene. Give every clipping ancestor of a tracked node (below the root) that
    the export left unclipped the frame's own rectangle as a clip. Returns (svg, window ids clipped)."""
    import re
    idx: dict[str, tuple[dict, dict | None]] = {}

    def walk(n: dict, p: dict | None) -> None:
        idx[n["id"]] = (n, p)
        for c in n.get("children", []):
            walk(c, n)
    walk(doc, None)
    fb = doc.get("absoluteBoundingBox") or {"x": 0, "y": 0}
    done: list[str] = []
    defs: list[str] = []
    for t in tracked:
        nid = idx[t][1]["id"] if t in idx and idx[t][1] else None
        while nid and idx[nid][1] is not None:   # ancestors below the root
            n = idx[nid][0]
            b = n.get("absoluteBoundingBox")
            if n.get("clipsContent") and n.get("type") != "INSTANCE" and nid not in done and b:
                m = re.search(r'<g data-node-id="' + re.escape(nid) + r'"([^>]*)>', svg)
                if m and "clip-path=" not in m.group(1):
                    cid = "nsalab-clip-" + nid.replace(":", "-").replace(";", "-")
                    defs.append(f'<clipPath id="{cid}"><rect x="{_num(b["x"] - fb["x"])}" y="{_num(b["y"] - fb["y"])}" '
                                f'width="{_num(b["width"])}" height="{_num(b["height"])}"/></clipPath>')
                    svg = svg[:m.start()] + f'<g data-node-id="{nid}" clip-path="url(#{cid})"' + m.group(1) + ">" + svg[m.end():]
                    done.append(nid)
            nid = idx[nid][1]["id"]
    if defs:
        block = "".join(defs)
        svg = svg.replace("</defs>", block + "</defs>", 1) if "</defs>" in svg else svg.replace("</svg>", f"<defs>{block}</defs></svg>")
    return svg, done


def fetch_svg(token: str, file_key: str, url: str, node_id: str, doc: dict, tracked: list[str] | None = None,
              outline_text: bool = True) -> tuple[bytes, str | None, int, list[str], list[str]]:
    """Download one export; re-export once if its image fills are missing; put back tracked layers the
    exporter culled (animations); re-inject the blend modes the exporter dropped. Returns (data,
    skip_reason, blends_reinjected, injected_ids, empty_tracked_ids) — a skip means the committed file is
    kept, so a flaky export can never replace a faithful one."""
    data = download(url)
    short = degraded(data, doc)
    if short:
        retry = export_svg(token, file_key, [node_id], include_node_id=True, outline_text=outline_text).get(node_id)
        if retry:
            data = download(retry)
            short = degraded(data, doc)
    if short:
        return data, f"degraded export — {short[0]} of {short[1]} image fills came back, twice; committed file kept", 0, [], []
    text = data.decode("utf-8")
    injected: list[str] = []
    empty: list[str] = []
    if tracked:
        text, injected, hidden, why = complete_base(text, doc, tracked, token, file_key, outline_text)
        if why:
            return data, why, 0, injected, []
        text, clipped = ensure_window_clips(text, doc, tracked)
        injected += [f"{h} (hidden)" for h in hidden] + [f"{w} (clip)" for w in clipped]
        empty = empty_tracked(text, doc, tracked)
    n = 0
    blends, pblends = blend_map(doc), paint_blend_map(doc)
    if blends or pblends:
        text, n1 = reinject_blend_modes(text, blends)
        text, n2 = reinject_paint_blends(text, pblends)
        n = n1 + n2
    if n or injected:
        data = text.encode("utf-8")
    return data, None, n, injected, empty


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
        if scope == "refs" and not a.get("ref"):
            continue  # the shared figures only: re-exported after an owner's sync PR merges
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

    report = {"written": [], "unchanged": [], "repaired": [], "broken": [], "skipped": [], "why": {}, "refs": [], "drift": []}
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

    probe = next((a["figma"]["nodeId"] for a in todo if not a.get("ref") and a.get("figma", {}).get("nodeId")), None)
    owners = Owners(manifest, {c: Path(p) for c, p in (s.split("=", 1) for s in args.sibling_manifest)}, args.sibling_repo)
    if probe is None:  # a run of `ref` entries only: probe with an owner's frame
        probe = next((owner_frame(o) for o, _, _ in (resolve_owner(a, file_key, owners) for a in todo) if o), None)
    version = file_version(token, file_key, probe) if probe else ""
    stamp = now_iso()
    pages: list[tuple[str, str]] | None = None
    refs = [a for a in todo if a.get("ref")]
    todo = [a for a in todo if not a.get("ref")]   # the owners' path below never sees a referrer

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
        data, why, n, _, _ = fetch_svg(token, file_key, url, a["figma"]["nodeId"], docs.get(a["figma"]["nodeId"], {}))
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
        data = render_animation(args, token, file_key, url, anim_id, tracks, a, report)
        if data is None:
            continue
        record(a, data, version, stamp, report, root,
               spec_sha=sha256(spec.read_bytes()) if spec else None, tracks_sha=sha256(tracks.read_bytes()))

    # ---- shared figures: the owner's frame into each referrer's own out.path
    if refs:
        sync_refs(args, token, file_key, refs, owners, version, stamp, report, root, course, prefix)

    save_manifest(mpath, manifest, indent)
    return finish(args, manifest, report, version, wrote_manifest=True)


def render_animation(args: argparse.Namespace, token: str, file_key: str, url: str, frame: str, tracks: Path,
                     a: dict, report: dict) -> bytes | None:
    """Complete the base export of the scene frame and run the renderer with `tracks`; None = skipped
    (the reason is in the report)."""
    doc = node_docs(token, file_key, [frame]).get(frame, {})
    try:
        tracked = [n["id"] for n in json.loads(tracks.read_text(encoding="utf-8")).get("nodes", [])]
    except (ValueError, TypeError, AttributeError) as e:
        report["skipped"].append((a, f"tracks.json unreadable: {e}"))
        return None
    # live text: an outlined export of a text-heavy scene runs to tens of MB; svg_optimize embeds the fonts
    live = export_svg(token, file_key, [frame], include_node_id=True, outline_text=False).get(frame) or url
    base, why, n, injected, empty = fetch_svg(token, file_key, live, frame, doc, tracked, outline_text=False)
    if why:
        report["skipped"].append((a, why))
        return None
    if empty:
        report.setdefault("empty", []).append((a, empty))
    if n:
        report.setdefault("blends", []).append((a, n))
    if injected:
        report.setdefault("injected", []).append((a, injected))
    with tempfile.TemporaryDirectory() as td:
        bp, op, dp = Path(td) / "base.svg", Path(td) / "out.svg", Path(td) / "frame.json"
        bp.write_bytes(base)
        dp.write_text(json.dumps(doc), encoding="utf-8")
        r = subprocess.run([sys.executable, args.renderer, str(bp), str(tracks), str(op), "--doc", str(dp)],
                           capture_output=True, text=True)
        if r.returncode != 0 or not op.exists():
            report["skipped"].append((a, f"renderer failed: {r.stderr.strip()[:200]}"))
            return None
        rendered = op.read_bytes()
    import svg_optimize  # fonttools, brotli, Pillow: needed only here (the workflow installs them)
    data, summary = svg_optimize.optimize(rendered, doc)
    report.setdefault("optimized", []).append((a, summary))
    return data


def cache_owner_frame(a: dict, frame: str, owner: dict) -> None:
    """The referrer's figma block is a cache of the owner's frame (contract §2 field table)."""
    fig = a.setdefault("figma", {})
    fig["nodeId"] = frame
    page = (owner.get("figma") or {}).get("page")
    if page:
        fig["page"] = page
    if "motion" in fig:
        fig["motion"]["animId"] = frame


def sync_refs(args: argparse.Namespace, token: str, file_key: str, refs: list[dict], owners: Owners, version: str,
              stamp: str, report: dict, root: Path, course: str, prefix: str) -> None:
    """Contract §2 «Shared figures», §3, §5. Each referrer is resolved through its owner: the owner's
    frame (figma.motion.animId for an animation, else figma.nodeId), and if that node is gone, the frame
    stamped ⟨owner id⟩ on the owner course's pages. A referrer is never resolved or repaired by its own
    id: the old stamp left on its former duplicate frame is ignored. The resolved frame is cached in the
    referrer's figma.nodeId and exported as for the owner's kind into the referrer's own out.path; an
    animation also gets its own tracks.json, pulled from the frame's plugin data and checked by the frame
    node (`anim`), not by the display key."""
    pages_of: dict[str, tuple[str, list[tuple[str, str]]]] = {}

    def broken(a: dict, why: str) -> None:
        a["status"] = "broken"
        report["broken"].append(a)
        report["why"][a["id"]] = why

    def pages_for(c: str) -> tuple[str, list[tuple[str, str]]]:
        if c not in pages_of:
            pfx = prefix if c == course else f"{c.upper()} ·"
            pages_of[c] = (pfx, course_pages(token, file_key, pfx))
        return pages_of[c]

    resolved: list[tuple[dict, dict]] = []
    for a in refs:
        owner, _om, why = resolve_owner(a, file_key, owners)
        if why:
            broken(a, why)
        elif a["kind"] == "animation" and not args.renderer:
            report["skipped"].append((a, "no --renderer (animation pilot pending)"))
        else:
            resolved.append((a, owner))
    if not resolved:
        return
    frames = sorted({owner_frame(o) for _, o in resolved})
    urls = export_svg(token, file_key, frames, include_node_id=True)
    ill_frames = sorted({owner_frame(o) for a, o in resolved if a["kind"] == "illustration" and urls.get(owner_frame(o))})
    docs = node_docs(token, file_key, ill_frames) if ill_frames else {}
    moved: dict[str, tuple[str | None, str | None]] = {}   # owner id → (stamped frame, its url), searched once

    for a, owner in resolved:
        frame = owner_frame(owner)
        url = urls.get(frame)
        if url is None:
            oid = owner["id"]
            pfx, pages = pages_for(course_of(oid))
            if oid not in moved:
                new = find_stamped(token, file_key, oid, (owner.get("figma") or {}).get("page"), pages)
                moved[oid] = (new, export_svg(token, file_key, [new], include_node_id=True).get(new) if new else None)
                if moved[oid][1] and a["kind"] == "illustration":
                    docs.update(node_docs(token, file_key, [new]))
            if moved[oid][1] is None:
                broken(a, f"owner {oid}'s frame {frame} is gone and no frame on the «{pfx}» pages carries ⟨{oid}⟩")
                continue
            frame, url = moved[oid]
            report["repaired"].append(a)
        cache_owner_frame(a, frame, owner)

        if a["kind"] == "illustration":
            data, why, n, _, _ = fetch_svg(token, file_key, url, frame, docs.get(frame, {}))
            if why:
                report["skipped"].append((a, why))
                continue
            if n:
                report.setdefault("blends", []).append((a, n))
            record(a, data, version, stamp, report, root)
        else:
            raw = tracks_dumps(token, file_key, [frame]).get(frame)
            if not raw:
                report["skipped"].append((a, f"the owner's frame {frame} carries no tracks dump (plugin data nsalab/tracks) — re-dump the owner (runbook §5)"))
                continue
            try:
                anim = json.loads(raw).get("anim")
            except (ValueError, AttributeError):
                report["skipped"].append((a, f"the tracks dump on {frame} is not a JSON object"))
                continue
            if anim != frame:
                report["skipped"].append((a, f"the tracks dump on {frame} was taken from frame {anim} — re-dump the owner (runbook §5)"))
                continue
            tb = tracks_bytes(raw)
            with tempfile.TemporaryDirectory() as td:
                tp = Path(td) / "tracks.json"
                tp.write_bytes(tb)
                data = render_animation(args, token, file_key, url, frame, tp, a, report)
            if data is None:
                continue
            a["tracks"] = a.get("tracks") or f"animations/{a['id']}/tracks.json"
            write_if_changed(root, a["tracks"], tb)
            record(a, data, version, stamp, report, root, tracks_sha=sha256(tb))
            owner_tracks = (owner.get("provenance") or {}).get("synced", {}).get("tracksSha256")
            if owner_tracks != sha256(tb):
                report["drift"].append((a, owner, owner_tracks))
        result = "written" if report["written"] and report["written"][-1] is a else "unchanged"
        same = (owner.get("provenance") or {}).get("synced", {}).get("sha256") == a["provenance"]["synced"]["sha256"]
        report["refs"].append((a, owner, result, same))


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
    if report.get("refs"):
        lines.append(f"| shared (ref → owner) | {len(report['refs'])} |")
    if report.get("drift"):
        lines.append(f"| ⚠ tracks differ from the owner's | {len(report['drift'])} |")
    if report.get("empty"):
        lines.append(f"| ⚠ empty tracked layers | {sum(len(ids) for _, ids in report['empty'])} |")
    lines.append("")
    if report["written"]:
        if any(a.get("ref") for a in report["written"]):
            lines += ["### Written", "", "| key | id | ref → owner | file |", "|---|---|---|---|"]
            lines += [f"| {a['display']['key']} | `{a['id']}` | " + (f"→ `{a['ref']}`" if a.get("ref") else "") +
                      f" | `{a['out']['path']}` |" for a in report["written"]]
        else:
            lines += ["### Written", "", "| key | id | file |", "|---|---|---|"]
            lines += [f"| {a['display']['key']} | `{a['id']}` | `{a['out']['path']}` |" for a in report["written"]]
        lines.append("")
    if report["refs"]:
        lines += ["### Shared figures — ref → owner (the owner's frame exported into the referrer's own file)", "",
                  "| key | id | ref → owner | owner's file | frame | result | bytes = owner's synced sha256 |",
                  "|---|---|---|---|---|---|---|"]
        lines += [f"| {a['display']['key']} | `{a['id']}` | → `{o['id']}` ({o['display']['key']}) | `{course_of(o['id'])}:{o['out']['path']}` "
                  f"| `{a['figma']['nodeId']}` | {res} | {'yes' if same else '**no**'} |" for a, o, res, same in report["refs"]]
        lines.append("")
    if report["drift"]:
        lines += ["### ⚠ Tracks differ from the owner's (the referrer's tracks.json ≠ the owner's tracksSha256)", ""]
        lines += [f"- {a['display']['key']} `{a['id']}` → `{o['id']}`: `{a['provenance']['synced'].get('tracksSha256', '')[:12]}` vs owner "
                  f"`{(ot or 'none')[:12]}` — re-sync the owner, or re-dump its tracks (runbook §5)" for a, o, ot in report["drift"]]
        lines.append("")
    if report["repaired"]:
        lines += ["### Repaired via ⟨id⟩ stamp (nodeId updated in the manifest)", ""]
        lines += [f"- {a['display']['key']} `{a['id']}` → `{a['figma']['nodeId']}`" +
                  (f" (the owner's stamp ⟨{a['ref']}⟩)" if a.get("ref") else "") for a in report["repaired"]]
        lines.append("")
    if report["broken"]:
        lines += ["### ⚠ Broken — node gone and no ⟨id⟩ stamp found" +
                  (", or a `ref` that cannot be resolved" if report.get("why") else ""), ""]
        lines += [f"- {a['display']['key']} `{a['id']}` (was `{a.get('figma', {}).get('nodeId')}`)" +
                  (f" — {report['why'][a['id']]}" if a["id"] in report.get("why", {}) else "") for a in report["broken"]]
        lines.append("")
    if report.get("empty"):
        lines += ["### ⚠ Visible tracked layers Figma renders as nothing — the animation ships without them "
                  "(a glyph the font lacks, an empty vector, a lost image: fix the scene and re-sync)", ""]
        lines += [f"- {a['display']['key']} `{a['id']}` — " + ", ".join(f"`{i}`" for i in ids) for a, ids in report["empty"]]
        lines.append("")
    if report["skipped"]:
        lines += ["### Skipped", ""]
        lines += [f"- {a['display']['key']} `{a['id']}` — {why}" for a, why in report["skipped"]]
        lines.append("")
    if report.get("optimized"):
        lines += ["### Animations: live text with embedded fonts, textures cut down (svg_optimize)", "",
                  "| key | id | rendered | written | faces | textures shrunk |", "|---|---|---|---|---|---|"]
        lines += [f"| {a['display']['key']} | `{a['id']}` | {s['before'] / 1e6:.1f} MB | {s['after'] / 1e6:.1f} MB | "
                  f"{len(s['faces'])}" + (f" (⚠ not embedded: {', '.join(s['unknown'])})" if s["unknown"] else "") +
                  f" | {s['images']} |" for a, s in report["optimized"]]
        lines.append("")
    if report.get("injected"):
        lines += ["### Parked layers put back (culled by the frame export, exported standalone; `(culled part)` = emitted with a part culled, re-exported whole; `(hidden)` = kept out on purpose, `(clip)` = a window the export left unclipped, now clipped)", ""]
        lines += [f"- {a['display']['key']} — " + ", ".join(f"`{i}`" for i in ids) for a, ids in report["injected"]]
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
    ap.add_argument("--scope", choices=["pending", "all", "refs"], default="pending",
                    help="pending = status pending|broken; all = also re-export synced entries; "
                         "refs = only the entries with `ref` (the shared figures)")
    ap.add_argument("--keys", default="", help="comma-separated display keys to sync (overrides scope; includes orphans)")
    ap.add_argument("--ids", default="", help="comma-separated stable ids to sync (overrides scope)")
    ap.add_argument("--renderer", default="", help="path to render.py; animations are skipped without it")
    ap.add_argument("--sibling-manifest", action="append", default=[], metavar="COURSE=PATH",
                    help="read a sibling course's manifest from a local file instead of its repo's main (repeatable)")
    ap.add_argument("--sibling-repo", default=SIBLING_REPO,
                    help=f"GitHub repo of a sibling course, read for cross-course `ref` owners (default {SIBLING_REPO})")
    ap.add_argument("--page-prefix", default="", help="page-name prefix of this course (default '<COURSE> ·')")
    ap.add_argument("--summary", default="", help="write the markdown report here (e.g. $GITHUB_STEP_SUMMARY)")
    ap.add_argument("--dry-run", action="store_true", help="select only; no network, no writes")
    args = ap.parse_args(argv)
    bad = [s for s in args.sibling_manifest if "=" not in s]
    if bad:
        ap.error(f"--sibling-manifest wants COURSE=PATH, got {bad[0]!r}")
    try:
        return run(args)
    except SyncError as e:
        print(f"figma-sync: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
