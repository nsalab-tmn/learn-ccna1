#!/usr/bin/env python3
"""tracks.json + Figma SVG export (svg_include_node_id=true) -> animated SMIL SVG.

Design (kb#223 step-4 note): the built Motion frame is exported by the REST Images endpoint
with data-node-id on every element; the Motion property tracks are dumped per node
(OPACITY, TRANSLATION_X/Y, ROTATION, SCALE_X/Y) with rest geometry. This renderer wraps each
tracked element in a <g> and attaches SMIL: opacity animates on the wrapper; the transform
chain is translate(TX,TY) · translate(c) · rotate(θ) · scale(sx,sy) · translate(-c), c = node
centre (the chain the spike verified at <=1 px vs Figma Motion). Linear easing
-> calcMode=linear; cubic-bezier easing -> calcMode=spline with keySplines. Loops forever.

The centre must be in the export's coordinate space: the exporter bakes every ancestor transform
into the leaves, so an element's coordinates are canvas-relative, whatever its nesting. With
--doc (the REST subtree of the exported frame) c = the node's absoluteBoundingBox centre minus
the frame origin; nodes the sync injected from a standalone export (see figma_sync.complete_base)
sit inside a <g data-export-origin="dx dy" transform="translate(dx dy)"> wrapper, whose origin
is subtracted for tracked descendants. Without --doc the dump's parent-relative `m` is used,
which is only right for direct children of the frame (the 2026-10-13 "arrow falls apart" defect).
Every tracked node must be present in the base: a missing one is an error (exit 1), not a note.
Usage: render.py base.svg tracks.json out.svg [--doc frame.json] [--width 1100]
"""
import json, re, sys, xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

def fmt(v):
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"

def timeline(kf, dur, dims=1):
    """kf: [[t, v, easing], ...] -> (keyTimes, values, keySplines|None). Pads t=0 and t=dur."""
    pts = [(float(t), v, e) for t, v, e in kf]
    pts.sort(key=lambda p: p[0])
    # "HOLD" on a key = the segment entering it is a step: keep the previous value until just before it
    held = []
    for i, (t, v, e) in enumerate(pts):
        if e == "HOLD" and i > 0 and t - pts[i - 1][0] > 0.002:
            held.append((t - 0.001, pts[i - 1][1], "L"))
        held.append((t, v, "L" if e == "HOLD" else e))
    pts = held
    if pts[0][0] > 0: pts.insert(0, (0.0, pts[0][1], "L"))
    if pts[-1][0] < dur: pts.append((dur, pts[-1][1], "L"))
    if pts[-1][0] > dur: pts = [p for p in pts if p[0] <= dur] + [(dur, pts[-1][1], "L")]
    kt = ";".join(fmt(t / dur) for t, _, _ in pts)
    vals = ";".join((fmt(v) if dims == 1 else " ".join(fmt(x) for x in v)) for _, v, _ in pts)
    eas = [e for _, _, e in pts][:-1]  # easing of the segment ENTERING the next key is stored on the next key in Figma; we attach per segment
    if all(e == "L" for e in eas):
        return kt, vals, None
    spl = []
    for _, _, e in pts[1:]:
        if e == "L": spl.append("0 0 1 1")
        elif e.startswith("CUBIC_BEZIER:") or ":" in e:
            spl.append(" ".join(fmt(float(x)) for x in e.split(":")[1].split(",")))
        elif e in ("EASE_IN", "EASE_IN_AND_OUT", "EASE_OUT"):
            spl.append({"EASE_IN": "0.42 0 1 1", "EASE_OUT": "0 0 0.58 1", "EASE_IN_AND_OUT": "0.42 0 0.58 1"}[e])
        else: spl.append("0 0 1 1")
    return kt, vals, ";".join(spl)

def animate(attr, kf, dur, extra=""):
    kt, vals, spl = timeline(kf, dur)
    cm = f' calcMode="spline" keySplines="{spl}"' if spl else ' calcMode="linear"'
    return f'<animate attributeName="{attr}" dur="{fmt(dur)}s" repeatCount="indefinite" keyTimes="{kt}" values="{vals}"{cm}{extra}/>'

def animate_tf(kind, kf, dur, dims):
    kt, vals, spl = timeline(kf, dur, dims)
    cm = f' calcMode="spline" keySplines="{spl}"' if spl else ' calcMode="linear"'
    return f'<animateTransform attributeName="transform" type="{kind}" additive="sum" dur="{fmt(dur)}s" repeatCount="indefinite" keyTimes="{kt}" values="{vals}"{cm}/>'

def merge_xy(tx, ty, dur, base=(0.0, 0.0)):
    """two scalar tracks -> one 2-D track on the union of key times (piecewise-linear sampling)."""
    def sample(kf, t, b):
        if not kf: return b
        pts = sorted((float(a), float(v)) for a, v, _ in kf)
        if t <= pts[0][0]: return pts[0][1]
        for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
            if t0 <= t <= t1: return v0 if t1 == t0 else v0 + (v1 - v0) * (t - t0) / (t1 - t0)
        return pts[-1][1]
    times = sorted({float(t) for kf in (tx, ty) for t, _, _ in (kf or [])} | {0.0, dur})
    return [[t, (sample(tx, t, base[0]), sample(ty, t, base[1])), "L"] for t in times]

def centre_from_dump(node):
    """Fallback: the dump's parent-relative matrix applied to the node's half size."""
    m = node.get("m") or [[1, 0, node["x"]], [0, 1, node["y"]]]
    w, h = node["w"] / 2, node["h"] / 2
    return (m[0][0] * w + m[0][1] * h + m[0][2], m[1][0] * w + m[1][1] * h + m[1][2])

def build_smil(node, dur, centre):
    tr = node["tracks"]; out = []
    if "OPACITY" in tr:
        eid = "fx-" + node["id"].replace(":", "-")
        out.append(animate("opacity", tr["OPACITY"]["kf"], dur, f' href="#{eid}" xlink:href="#{eid}"'))
    tx, ty = tr.get("TRANSLATION_X", {}).get("kf"), tr.get("TRANSLATION_Y", {}).get("kf")
    rot, sx, sy = tr.get("ROTATION", {}).get("kf"), tr.get("SCALE_X", {}).get("kf"), tr.get("SCALE_Y", {}).get("kf")
    chain = []
    if tx or ty: chain.append(animate_tf("translate", merge_xy(tx, ty, dur), dur, 2))
    if rot or sx or sy:
        cx, cy = centre
        chain.append(f'<animateTransform attributeName="transform" type="translate" additive="sum" dur="{fmt(dur)}s" repeatCount="indefinite" values="{fmt(cx)} {fmt(cy)}"/>')
        if rot: chain.append(animate_tf("rotate", [[t, -v, e] for t, v, e in rot], dur, 1))  # Figma rotation is CCW-positive; SVG rotate is CW-positive in y-down space
        if sx or sy:
            sxk = sx or [[0, tr.get("SCALE_X", {}).get("base", 1), "L"]]; syk = sy or [[0, tr.get("SCALE_Y", {}).get("base", 1), "L"]]
            chain.append(animate_tf("scale", merge_xy(sxk, syk, dur, (1.0, 1.0)), dur, 2))
        chain.append(f'<animateTransform attributeName="transform" type="translate" additive="sum" dur="{fmt(dur)}s" repeatCount="indefinite" values="{fmt(-cx)} {fmt(-cy)}"/>')
    return out, chain

def elem_end(text, start, end_of_tag, tag, selfclose):
    """End offset of the element whose start tag spans [start, end_of_tag)."""
    if selfclose: return end_of_tag
    depth = 0
    for mm in re.finditer(r'<(/?)' + tag + r'\b[^>]*?(/?)>', text[start:]):
        if mm.group(1): depth -= 1
        elif not mm.group(2): depth += 1
        if depth == 0: return start + mm.end()
    return None

def export_origin(text, pos):
    """(dx, dy) of the innermost injected-export wrapper strictly enclosing `pos`, else (0, 0)."""
    best = None
    for m in re.finditer(r'<(g)([^>]*\sdata-export-origin="([-\d.]+) ([-\d.]+)"[^>]*)(/?)>', text):
        if m.start() < pos:
            end = elem_end(text, m.start(), m.end(), "g", m.group(5))
            if end and pos < end: best = (float(m.group(3)), float(m.group(4)))
    return best or (0.0, 0.0)

def index_doc(doc):
    """{id: absoluteBoundingBox} for the frame subtree, plus the frame origin."""
    boxes = {}
    stack = [doc]
    while stack:
        n = stack.pop()
        if n.get("absoluteBoundingBox"): boxes[n["id"]] = n["absoluteBoundingBox"]
        stack.extend(n.get("children", []))
    fb = doc.get("absoluteBoundingBox") or {"x": 0, "y": 0}
    return boxes, (fb["x"], fb["y"])

def render(base_svg, tracks, out_path, width=None, doc=None):
    dur = float(tracks["duration"])
    text = open(base_svg, encoding="utf-8").read()
    if "data-node-id" not in text: raise SystemExit("base SVG has no data-node-id attributes — export with svg_include_node_id=true")
    boxes, (fx, fy) = index_doc(doc) if doc else ({}, (0.0, 0.0))
    missing, wrapped, fallback = [], 0, []
    for node in tracks["nodes"]:
        nid = node["id"]
        m = re.search(r'<([a-zA-Z]+)([^>]*\sdata-node-id="' + re.escape(nid) + r'"[^>]*)(/?)>', text)
        if not m: missing.append(nid); continue
        end = elem_end(text, m.start(), m.end(), m.group(1), m.group(3))
        if end is None: missing.append(nid); continue
        if nid in boxes:
            b = boxes[nid]; ox, oy = export_origin(text, m.start())
            centre = (b["x"] + b["width"] / 2 - fx - ox, b["y"] + b["height"] / 2 - fy - oy)
        else:
            centre = centre_from_dump(node)
            if doc and any(k in node["tracks"] for k in ("ROTATION", "SCALE_X", "SCALE_Y")): fallback.append(nid)
        anims, chain = build_smil(node, dur, centre)
        tag, attrs, start = m.group(1), m.group(2), m.start()
        elem = text[start:end]
        if anims:  # give the element an id so the opacity <animate> can target it directly
            eid = "fx-" + nid.replace(":", "-")
            elem = re.sub(r'^<' + tag, f'<{tag} id="{eid}"', elem, count=1) if ' id="' not in attrs else elem
        wrapper = f'<g data-anim-for="{nid}">' + "".join(anims) + "".join(chain) + elem + "</g>"
        text = text[:start] + wrapper + text[end:]
        wrapped += 1
    if missing: raise SystemExit(f"tracked nodes absent from the base SVG: {missing}")
    if 'xmlns:xlink' not in text[:text.find('>')+1]: text = text.replace('<svg', '<svg xmlns:xlink="http://www.w3.org/1999/xlink"', 1)
    if width: text = re.sub(r'<svg([^>]*?)\swidth="[^"]*"', rf'<svg\1 width="{width}"', text, count=1)
    ET.fromstring(text.encode("utf-8"))  # well-formedness gate
    open(out_path, "w", encoding="utf-8").write(text)
    return wrapped, fallback

if __name__ == "__main__":
    a = sys.argv[1:]
    width = doc = None
    if "--width" in a: i = a.index("--width"); width = a[i + 1]; del a[i:i + 2]
    if "--doc" in a: i = a.index("--doc"); doc = json.load(open(a[i + 1], encoding="utf-8")); del a[i:i + 2]
    base, tr, out = a
    w, fb = render(base, json.load(open(tr, encoding="utf-8")), out, width, doc)
    print(f"wrapped {w} tracked nodes" + (f"; centre from the dump (not in --doc): {fb}" if fb else ""))
