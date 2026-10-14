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
A TRANSLATION track is stored in the node's *parent's* axes (Figma Motion keys the relative transform),
so it is mapped through the linear part of every ancestor below the frame before it becomes a canvas
translate: the children of a 180°-rotated arrow frame (shaft + head, the detached "стрелка" build) moved
the wrong way and the arrow grew out of the canvas (learn-ccna3 3.9.3, 10.4.6; 2026-10-14). A tracked
ancestor contributes the dump's exact 2×2 (rotation, flips); an untracked one the REST `rotation`
(radians, r = −plugin rotation) — hence --doc. A mirrored ancestor also mirrors a ROTATION track and a
±90° one swaps the SCALE axes on the canvas.
Usage: render.py base.svg tracks.json out.svg [--doc frame.json] [--width 1100]
"""
import json, math, re, sys, xml.etree.ElementTree as ET

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
    for p in (3, 4, 5, 6, 7):  # the least precision that keeps keyTimes strictly increasing (a 1 ms step must survive rounding)
        kts = [(f"{t / dur:.{p}f}".rstrip("0").rstrip(".") or "0") for t, _, _ in pts]
        if all(float(a) < float(b) for a, b in zip(kts, kts[1:])): break
    kt = ";".join(kts)
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
    """two scalar tracks -> one 2-D track on the union of key times. A segment entering a HOLD key is a
    step (the value stays until just before the key), as in timeline(); sampling it linearly made a
    packet that should jump out and slide back drift the long way instead (learn-ccna1#25: 16.2.4-1).
    A key's easing is kept when the other track has no key there (its segment is linear anyway)."""
    def prep(kf): return sorted((float(a), float(v), e) for a, v, e in (kf or []))
    def sample(pts, t, b):  # -> (value, easing of the key at t | None when interpolated)
        if not pts: return b, None
        if t <= pts[0][0]: return pts[0][1], (pts[0][2] if t == pts[0][0] else None)
        for (t0, v0, _), (t1, v1, e1) in zip(pts, pts[1:]):
            if t == t1: return v1, e1
            if t0 <= t < t1: return (v0 if e1 == "HOLD" or t1 == t0 else v0 + (v1 - v0) * (t - t0) / (t1 - t0)), None
        return pts[-1][1], None
    px, py = prep(tx), prep(ty)
    times = {0.0, dur}
    for pts in (px, py):
        for i, (t, _, e) in enumerate(pts):
            times.add(t)
            if e == "HOLD" and i > 0 and t - pts[i - 1][0] > 0.002: times.add(t - 0.001)
    out = []
    for t in sorted(times):
        (vx, ex), (vy, ey) = sample(px, t, base[0]), sample(py, t, base[1])
        eas = [e for e in (ex, ey) if e and e != "L"]
        out.append([t, (vx, vy), "HOLD" if "HOLD" in eas else (eas[0] if eas else "L")])
    return out

def centre_from_dump(node):
    """Fallback: the dump's parent-relative matrix applied to the node's half size."""
    m = node.get("m") or [[1, 0, node["x"]], [0, 1, node["y"]]]
    w, h = node["w"] / 2, node["h"] / 2
    return (m[0][0] * w + m[0][1] * h + m[0][2], m[1][0] * w + m[1][1] * h + m[1][2])

IDENTITY = ((1.0, 0.0), (0.0, 1.0))

def ancestor_linear(nid, parents, dump_m, rot_of, root_id):
    """Product of the linear 2×2 parts of the node's ancestors below the frame, outermost first — the map
    from the node's parent axes (where Motion keys its translation) to the canvas. A tracked ancestor
    gives the dump's `m` (exact: rotation, flips, skews); an untracked one the REST `rotation` in
    radians, which is minus the plugin's rotation: [[cos r, −sin r], [sin r, cos r]]."""
    A = [[1.0, 0.0], [0.0, 1.0]]
    p = parents.get(nid)
    while p is not None and p != root_id:
        if p in dump_m:
            m = dump_m[p]; L = [[m[0][0], m[0][1]], [m[1][0], m[1][1]]]
        else:
            r = rot_of.get(p) or 0.0
            L = [[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]] if abs(r) > 1e-9 else None
        if L:
            A = [[L[0][0] * A[0][0] + L[0][1] * A[1][0], L[0][0] * A[0][1] + L[0][1] * A[1][1]],
                 [L[1][0] * A[0][0] + L[1][1] * A[1][0], L[1][0] * A[0][1] + L[1][1] * A[1][1]]]
        p = parents.get(p)
    return ((A[0][0], A[0][1]), (A[1][0], A[1][1]))

def build_smil(node, dur, centre, lin=IDENTITY):
    tr = node["tracks"]; out = []
    if "OPACITY" in tr:
        eid = "fx-" + node["id"].replace(":", "-")
        out.append(animate("opacity", tr["OPACITY"]["kf"], dur, f' href="#{eid}" xlink:href="#{eid}"'))
    tx, ty = tr.get("TRANSLATION_X", {}).get("kf"), tr.get("TRANSLATION_Y", {}).get("kf")
    rot, sx, sy = tr.get("ROTATION", {}).get("kf"), tr.get("SCALE_X", {}).get("kf"), tr.get("SCALE_Y", {}).get("kf")
    (a, b), (c, d) = lin
    plain = all(abs(x - y) < 1e-9 for x, y in zip((a, b, c, d), (1.0, 0.0, 0.0, 1.0)))
    chain = []
    if tx or ty:
        pts = merge_xy(tx, ty, dur)
        if not plain:  # parent-axes translation -> canvas translation
            pts = [[t, (a * vx + b * vy, c * vx + d * vy), e] for t, (vx, vy), e in pts]
        chain.append(animate_tf("translate", pts, dur, 2))
    if rot or sx or sy:
        cx, cy = centre
        chain.append(f'<animateTransform attributeName="transform" type="translate" additive="sum" dur="{fmt(dur)}s" repeatCount="indefinite" values="{fmt(cx)} {fmt(cy)}"/>')
        if rot:
            sgn = -1.0 if a * d - b * c < 0 else 1.0  # a mirrored ancestor mirrors the spin
            chain.append(animate_tf("rotate", [[t, -v * sgn, e] for t, v, e in rot], dur, 1))  # Figma rotation is CCW-positive; SVG rotate is CW-positive in y-down space
        if sx or sy:
            sxk = sx or [[0, tr.get("SCALE_X", {}).get("base", 1), "L"]]; syk = sy or [[0, tr.get("SCALE_Y", {}).get("base", 1), "L"]]
            pts = merge_xy(sxk, syk, dur, (1.0, 1.0))
            if abs(b) > abs(a):  # a ±90° ancestor: the node's x axis lies along the canvas y axis
                pts = [[t, (vy, vx), e] for t, (vx, vy), e in pts]
            chain.append(animate_tf("scale", pts, dur, 2))
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
    """{id: absoluteBoundingBox} for the frame subtree, the frame origin, {id: parent id} and {id: REST rotation}."""
    boxes, parents, rots = {}, {}, {}
    stack = [(doc, None)]
    while stack:
        n, p = stack.pop()
        if n.get("absoluteBoundingBox"): boxes[n["id"]] = n["absoluteBoundingBox"]
        if p is not None: parents[n["id"]] = p
        if n.get("rotation"): rots[n["id"]] = float(n["rotation"])
        stack.extend((c, n["id"]) for c in n.get("children", []))
    fb = doc.get("absoluteBoundingBox") or {"x": 0, "y": 0}
    return boxes, (fb["x"], fb["y"]), parents, rots

def render(base_svg, tracks, out_path, width=None, doc=None):
    dur = float(tracks["duration"])
    text = open(base_svg, encoding="utf-8").read()
    if "data-node-id" not in text: raise SystemExit("base SVG has no data-node-id attributes — export with svg_include_node_id=true")
    if doc:
        boxes, (fx, fy), parents, rots = index_doc(doc); root_id = doc["id"]
    else:  # no document: only tracked ancestors are known (the dump's `p` chain)
        boxes, (fx, fy), rots = {}, (0.0, 0.0), {}
        parents = {n["id"]: n["p"] for n in tracks["nodes"] if n.get("p")}; root_id = tracks.get("anim")
    dump_m = {n["id"]: n["m"] for n in tracks["nodes"] if n.get("m")}
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
        anims, chain = build_smil(node, dur, centre, ancestor_linear(nid, parents, dump_m, rots, root_id))
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
