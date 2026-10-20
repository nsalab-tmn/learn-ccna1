#!/usr/bin/env python3
"""Guard for re-syncs: report figure nodes whose exported geometry lost path segments.

Figma's REST SVG exporter silently drops some geometry that an earlier export drew — e.g. a
stroke-only segment of a vector that also has a fill region (the struck-out «no entry» marker
lost its bar, kb#340; contract §5). This compares two exports of the same figures node by node
(`data-node-id`): a node is reported when some of its old segments are gone and nothing new
replaced them. Re-ordered, re-split or re-rounded geometry, dashes written as segments and
geometry moved into <defs> are not reported.

Usage:
  svg_segments_check.py BASE [HEAD]       every *.svg changed between two git refs (HEAD default)
  svg_segments_check.py --files OLD NEW   two files
Exit code: 0 nothing lost · 1 lost segments found (listed on stdout).
"""
import re
import subprocess
import sys

TOKEN = re.compile(r'[MLHVCZmlhvcz]|-?\d*\.?\d+(?:e-?\d+)?')
ELEM = re.compile(r'<(path|g)\b([^>]*?)data-node-id="([^"]+)"([^>]*)>')
CHILD = re.compile(r'<(/g|path|g|rect|circle|ellipse|use|mask)\b([^>]*)>')
MIN_LEN = 5      # px; shorter segments are rounding noise
TOLERANCE = 3.0  # px; a lost segment whose samples all lie this close to new geometry is not lost


def segments(d):
    """Absolute-command path data → [(kind, start, end[, c1, c2])]: L straight, C cubic curve."""
    t = TOKEN.findall(d)
    i, out, cur, start, cmd = 0, [], (0.0, 0.0), (0.0, 0.0), None

    def num():
        nonlocal i
        i += 1
        return float(t[i - 1])
    while i < len(t):
        if t[i].isalpha():
            cmd = t[i]
            i += 1
        if cmd == 'M':
            cur = start = (num(), num())
            cmd = 'L'
        elif cmd == 'L':
            p = (num(), num())
            out.append(('L', cur, p))
            cur = p
        elif cmd == 'H':
            p = (num(), cur[1])
            out.append(('L', cur, p))
            cur = p
        elif cmd == 'V':
            p = (cur[0], num())
            out.append(('L', cur, p))
            cur = p
        elif cmd == 'C':
            c1, c2, p = (num(), num()), (num(), num()), (num(), num())
            out.append(('C', cur, p, c1, c2))
            cur = p
        elif cmd in 'Zz':
            if cur != start:
                out.append(('L', cur, start))
            cur, cmd = start, None
        else:
            raise ValueError(f'unsupported path command {cmd!r}')
    return out


def point(s, t):
    if s[0] == 'L':
        return (s[1][0] + (s[2][0] - s[1][0]) * t, s[1][1] + (s[2][1] - s[1][1]) * t)
    p0, p3, p1, p2 = s[1], s[2], s[3], s[4]
    u = 1 - t
    return tuple(u ** 3 * p0[i] + 3 * u * u * t * p1[i] + 3 * u * t * t * p2[i] + t ** 3 * p3[i] for i in (0, 1))


def polyline(segs):
    """The new geometry as short straight pieces (curves sampled)."""
    out = []
    for s in segs:
        n = 1 if s[0] == 'L' else 16
        pts = [point(s, k / n) for k in range(n + 1)]
        out += list(zip(pts, pts[1:]))
    return out


def key(s):
    r = lambda p: (round(p[0]), round(p[1]))
    return (s[0],) + tuple(sorted([r(s[1]), r(s[2])]))


def long_enough(s):
    return abs(s[1][0] - s[2][0]) + abs(s[1][1] - s[2][1]) >= MIN_LEN


def nodes(svg):
    """{node id: [path data]} — a path node's own d; a group's direct un-ided child paths, with
    <use> references resolved; None for dashed nodes (their dashes are written differently)."""
    defs = {m.group(1): m.group(2) for m in re.finditer(r'<path\b[^>]*\bid="([^"]+)"[^>]*\sd="([^"]+)"', svg)}
    res = {}
    for m in ELEM.finditer(svg):
        tag, nid, attrs = m.group(1), m.group(3), m.group(2) + m.group(4)
        if 'stroke-dasharray' in attrs:
            res[nid] = None
            continue
        if tag == 'path':
            d = re.search(r'\sd="([^"]+)"', attrs)
            res[nid] = [d.group(1)] if d else []
            continue
        ds = []
        for c in CHILD.finditer(svg, m.end()):
            el, a = c.group(1), c.group(2)
            if el in ('/g', 'g') or 'data-node-id' in a:
                break
            if 'stroke-dasharray' in a:
                ds = None
                break
            if el == 'path':
                d = re.search(r'\sd="([^"]+)"', a)
                if d:
                    ds.append(d.group(1))
            elif el == 'use':
                ref = re.search(r'href="#([^"]+)"', a)
                if ref and ref.group(1) in defs:
                    ds.append(defs[ref.group(1)])
        res[nid] = ds
    return res


def dist(q, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    l2 = dx * dx + dy * dy or 1e-9
    t = max(0.0, min(1.0, ((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / l2))
    return ((a[0] + t * dx - q[0]) ** 2 + (a[1] + t * dy - q[1]) ** 2) ** 0.5


def covered(s, pieces):
    """Every sample of segment s lies within TOLERANCE of the other geometry."""
    return all(min((dist(point(s, k / 8), a, b) for a, b in pieces), default=9) <= TOLERANCE for k in range(1, 8))


def lost_segments(old_svg, new_svg):
    old, new = nodes(old_svg), nodes(new_svg)
    found = []
    for nid, ds in old.items():
        if not ds or not new.get(nid):
            continue
        try:
            raw_old = [s for d in ds for s in segments(d)]
            so = {key(s) for s in raw_old}
            raw_new = [s for d in new[nid] for s in segments(d)]
        except (ValueError, IndexError):
            continue
        sn = {key(s) for s in raw_new}
        old_pieces, new_pieces = polyline(raw_old), polyline(raw_new)
        # lost: old segments the new geometry no longer draws; added: new segments the old did not
        # draw (a real edit, not an exporter loss) — re-split, re-rounded and re-stroked geometry is neither
        lost = {key(s) for s in raw_old if key(s) not in sn and long_enough(s) and not covered(s, new_pieces)}
        added = {key(s) for s in raw_new if key(s) not in so and long_enough(s) and not covered(s, old_pieces)}
        if lost and not added:
            found.append((nid, len(lost), len(so), sorted(lost)[:2]))
    return found


def git_show(ref, path):
    return subprocess.run(['git', 'show', f'{ref}:{path}'], capture_output=True, text=True, check=True).stdout


def main(argv):
    if len(argv) == 3 and argv[0] == '--files':
        pairs = [(argv[1], open(argv[1], encoding='utf-8').read(), open(argv[2], encoding='utf-8').read())]
    elif 1 <= len(argv) <= 2 and not argv[0].startswith('-'):
        base, head = argv[0], argv[1] if len(argv) == 2 else 'HEAD'
        changed = subprocess.run(['git', 'diff', '--name-only', '--diff-filter=M', base, head, '--', '*.svg'],
                                 capture_output=True, text=True, check=True).stdout.split()
        pairs = [(p, git_show(base, p), git_show(head, p)) for p in changed]
    else:
        print(__doc__)
        return 2
    bad = 0
    for path, old_svg, new_svg in pairs:
        for nid, n, total, sample in lost_segments(old_svg, new_svg):
            print(f'{path}: node {nid} lost {n} of {total} segments, e.g. {sample}')
            bad += 1
    print(f'checked {len(pairs)} file(s): {bad} node(s) lost geometry')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
