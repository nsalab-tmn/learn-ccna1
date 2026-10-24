"""svg_optimize.py — shrink an animated SVG exported with live text (svg_outline_text=false).

An outlined export turns every glyph into a path: a video remake with thousands of text layers (console
lines, simulator screens, captions) came out at up to 26 MB, 61 % of it glyph outlines (kb#327,
2026-10-24). With live text the same frame is a few MB, provided the file carries its fonts and its
oversized textures are cut down. Three steps, all deterministic for the same input:

1. **Weights from the document.** Figma's live-text export writes `font-weight` only for Bold and drops
   Medium, Semi Bold and Extra Bold; a TEXT node with per-character styles comes out as a
   `<g data-node-id>` holding one `<text>` per style run, without ids. The REST document has every
   TEXT node's real weight and italic flag, so each `<text>` gets `font-weight` / `font-style` from it.
2. **Embedded fonts.** An SVG shown as `<img>` loads no external resources, so each face the file draws
   (family, weight, style) is embedded as an `@font-face` WOFF2 data: URI, subset to the characters this
   file uses — 1–12 KB a face. The faces are instanced from the variable fonts in `fonts/` (OFL).
3. **Textures.** Embedded PNGs larger than `tex_cap` px are downscaled: the library's stipple textures are
   stored at up to 3415 px but drawn on faces a few hundred px across (no visible change at 2×).

Needs fonttools, brotli and Pillow (the workflow installs them); figma_sync.py imports this module only
when it renders an animation.
"""
from __future__ import annotations

import base64
import html
import io
import re
from pathlib import Path

FONTS = Path(__file__).parent / "fonts"
FACES = {  # family -> (upright file, italic file): variable fonts from google/fonts, OFL (fonts/OFL-*.txt)
    "Inter": ("Inter[opsz,wght].ttf", "Inter-Italic[opsz,wght].ttf"),
    "JetBrains Mono": ("JetBrainsMono[wght].ttf", None),
    "Golos Text": ("GolosText[wght].ttf", None),
}
WEIGHTS = {"normal": 400, "bold": 700, "bolder": 700, "lighter": 300}
TEX_CAP = 512


def _attr(a: str, name: str) -> str | None:
    m = re.search(r'\s' + name + r'="([^"]*)"', a)
    if m:
        return m.group(1)
    m = re.search(r'\sstyle="[^"]*' + name + r':\s*([^;"]+)', a)
    return m.group(1).strip() if m else None


def _family(a: str) -> str:
    return (_attr(a, "font-family") or "").split(",")[0].strip().strip("'\"")


def apply_doc_weights(svg: str, doc: dict) -> tuple[str, int, int]:
    """Set every <text>'s font-weight / font-style from its TEXT node. Returns (svg, texts, mixed nodes)."""
    runs: dict[str, list[tuple[str, int, str]]] = {}   # TEXT id -> its style runs, the base style first
    stack = [doc]
    while stack:
        n = stack.pop()
        if n.get("type") == "TEXT":
            st = n.get("style", {})
            base = (st.get("fontFamily"), int(st.get("fontWeight", 400)), "italic" if st.get("italic") else "normal")
            rs = [base]
            for ov in (n.get("styleOverrideTable") or {}).values():
                if any(k.startswith("font") or k == "italic" for k in ov):
                    rs.append((ov.get("fontFamily", base[0]), int(ov.get("fontWeight", base[1])),
                               "italic" if ov.get("italic", base[2] == "italic") else "normal"))
            runs[n["id"]] = rs
        stack.extend(n.get("children", []))

    def pick(rs: list[tuple[str, int, str]], a: str) -> tuple[str, int, str]:
        """The run a <text> draws: the one with its family; among several, Figma's own font-weight="bold"
        marks the 700 run."""
        cand = [r for r in rs if r[0] == _family(a)] or rs[:1]
        if len(cand) > 1:
            bold = _attr(a, "font-weight") == "bold"
            cand = [r for r in cand if (r[1] == 700) == bold] or cand
        return cand[0]

    out, pos, fixed = [], 0, 0
    owner = None   # the TEXT id of the enclosing <g data-node-id> wrapper of a mixed-style node's runs
    for m in re.finditer(r'<g\b[^>]*\sdata-node-id="([^"]+)"[^>]*>|</g>|<text\b([^>]*)>', svg):
        tok = m.group(0)
        if tok.startswith("<g"):
            owner = m.group(1) if m.group(1) in runs else None
            continue
        if tok == "</g>":
            owner = None
            continue
        a = m.group(2)
        nid = re.search(r'\sdata-node-id="([^"]+)"', a)
        rid = nid.group(1) if nid and nid.group(1) in runs else owner
        if not rid:
            continue
        _, w, st = pick(runs[rid], a)
        rest = re.sub(r'\sfont-(weight|style)="[^"]*"', "", a)
        out += [svg[pos:m.start()], f'<text{rest} font-weight="{w}" font-style="{st}">']
        pos = m.end()
        fixed += 1
    out.append(svg[pos:])
    return "".join(out), fixed, sum(len(r) > 1 for r in runs.values())


def faces_used(svg: str) -> dict[tuple[str, int, str], set[str]]:
    used: dict[tuple[str, int, str], set[str]] = {}
    for m in re.finditer(r'<text\b([^>]*)>(.*?)</text>', svg, re.S):
        a = m.group(1)
        w = _attr(a, "font-weight") or "400"
        w = WEIGHTS.get(w) or int(re.sub(r"\D", "", w) or 400)
        key = (_family(a), w, _attr(a, "font-style") or "normal")
        used.setdefault(key, set()).update(html.unescape(re.sub(r"<[^>]+>", "", m.group(2))))
    return used


def face_woff2(fam: str, weight: int, style: str, chars: set[str], fonts: Path = FONTS) -> bytes:
    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    up, it = FACES[fam]
    f = TTFont(fonts / (it if style == "italic" and it else up))
    axes = {a.axisTag: a for a in f["fvar"].axes}
    loc = {"wght": max(axes["wght"].minValue, min(axes["wght"].maxValue, weight))}
    if "opsz" in axes:
        loc["opsz"] = axes["opsz"].defaultValue
    f = instancer.instantiateVariableFont(f, loc)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk"]
    opts.name_IDs = []
    opts.notdef_outline = True
    s = subset.Subsetter(opts)
    s.populate(unicodes={ord(c) for c in chars} | {0x20})
    s.subset(f)
    out = io.BytesIO()
    f.flavor = "woff2"
    f.save(out)
    return out.getvalue()


def embed_fonts(svg: str, fonts: Path = FONTS) -> tuple[str, list[str], list[str]]:
    """Returns (svg, embedded face labels, unknown families left to the viewer's fallback)."""
    rules, faces, unknown = [], [], []
    for (fam, w, st), chars in sorted(faces_used(svg).items(), key=lambda kv: str(kv[0])):
        if fam not in FACES:
            unknown.append(fam)
            continue
        data = face_woff2(fam, w, st, chars, fonts)
        faces.append(f"{fam} {w}{' italic' if st == 'italic' else ''}")
        rules.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};"
                     f"src:url(data:font/woff2;base64,{base64.b64encode(data).decode()}) format('woff2')}}")
    if rules:
        m = re.search(r"<svg\b[^>]*>", svg)
        svg = svg[:m.end()] + "<style>" + "".join(rules) + "</style>" + svg[m.end():]
    return svg, faces, unknown


def shrink_images(svg: str, cap: int = TEX_CAP) -> tuple[str, int]:
    from PIL import Image
    cache: dict[str, str] = {}
    shrunk = 0

    def rep(m: re.Match) -> str:
        nonlocal shrunk
        d = m.group(2)
        if d not in cache:
            im = Image.open(io.BytesIO(base64.b64decode(d)))
            cache[d] = m.group(0)
            if max(im.size) > cap:
                r = cap / max(im.size)
                im = im.resize((max(1, round(im.size[0] * r)), max(1, round(im.size[1] * r))), Image.LANCZOS)
                o = io.BytesIO()
                im.save(o, "PNG", optimize=True)
                cache[d] = f"data:{m.group(1)};base64," + base64.b64encode(o.getvalue()).decode()
                shrunk += 1
        return cache[d]

    return re.sub(r"data:(image/png);base64,([A-Za-z0-9+/=]+)", rep, svg), shrunk


def optimize(data: bytes, doc: dict, fonts: Path = FONTS, tex_cap: int = TEX_CAP) -> tuple[bytes, dict]:
    """The three steps on one rendered animation. Returns (bytes, a summary for the sync report)."""
    svg = data.decode("utf-8")
    svg, shrunk = shrink_images(svg, tex_cap)
    svg, texts, mixed = apply_doc_weights(svg, doc)
    svg, faces, unknown = embed_fonts(svg, fonts)
    out = svg.encode("utf-8")
    return out, {"before": len(data), "after": len(out), "texts": texts, "mixed": mixed,
                 "faces": faces, "unknown": sorted(set(unknown)), "images": shrunk}
