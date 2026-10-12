# Sensitivity of tile values to the "single nearest road" access rule.
# usage: python3 -I variant.py <scratch> <services html> <homes html> <out json>
import sys, math, runpy, io, contextlib, heapq, statistics
from collections import defaultdict
sys.argv = ["vstats.py"] + sys.argv[1:5]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    g = runpy.run_path("vstats.py")
NODES, SEGS, HOMES, GROUPS, GRID, CELL, dest_points, KX, KY = [g[k] for k in "NODES SEGS HOMES GROUPS GRID CELL dest_points KX KY".split()]
def near_all(p, slack):
    # all segments whose distance <= nearest + slack
    best = []; r = 0
    while True:
        gx0, gy0 = int(p[0] // CELL), int(p[1] // CELL); cand = set()
        for gx in range(gx0 - r, gx0 + r + 1):
            for gy in range(gy0 - r, gy0 + r + 1): cand.update(GRID.get((gx, gy), ()))
        res = []
        for i in cand:
            a, b = SEGS[i][:2]; (ax, ay), (bx, by) = NODES[a], NODES[b]
            dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
            t = 0 if L2 == 0 else max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
            res.append((math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy), i, t))
        if res:
            m = min(res)[0]
            if m + slack <= r * CELL: return [x for x in res if x[0] <= m + slack]
        r += 1
def run(hs, ds):
    snaps = {}   # key -> list of (off, i, t)
    homes = []
    for b in HOMES: k = ("h", b["id"]); snaps[k] = near_all(b["_c"], hs); homes.append((b, k))
    dk = {}
    for gname, items in GROUPS:
        ks = []
        for s in items:
            for p, nm in dest_points(s):
                k = ("d", nm, round(p[0], 3), round(p[1], 3))
                if k not in snaps: snaps[k] = near_all(p, ds)
                ks.append((k, nm))
        dk[gname] = ks
    on_seg = defaultdict(list)
    for k, lst in snaps.items():
        for j, (off, i, t) in enumerate(lst): on_seg[i].append((t, (k, j)))
    ADJ = defaultdict(list)
    for i, (a, b, *_ ) in enumerate(SEGS):
        L = math.dist(NODES[a], NODES[b])
        ch = [(0.0, ("n", a))] + sorted(on_seg.get(i, []), key=lambda x: x[0]) + [(1.0, ("n", b))]
        for (t0, u), (t1, v) in zip(ch, ch[1:]):
            w = (t1 - t0) * L; ADJ[u].append((v, w)); ADJ[v].append((u, w))
    out = {}
    for gname, items in GROUPS:
        dist = {}; pq = []; org = {}
        for k, nm in dk[gname]:
            for j, (off, i, t) in enumerate(snaps[k]):
                u = (k, j)
                if off < dist.get(u, 1e18): dist[u] = off; org[u] = nm; heapq.heappush(pq, (off, id(u), u))
        while pq:
            d, _, u = heapq.heappop(pq)
            if d > dist[u]: continue
            for v, w in ADJ[u]:
                if d + w < dist.get(v, 1e18): dist[v] = d + w; org[v] = org[u]; heapq.heappush(pq, (d + w, id(v), v))
        mins = []
        for b, k in homes:
            best = min((dist[(k, j)] + off, org[(k, j)]) for j, (off, i, t) in enumerate(snaps[k]))
            mins.append((best[0] / 60, b["id"], best[1]))
        ms = sorted(m for m, _, _ in mins); w = max(mins)
        out[gname] = (statistics.median(ms), ms[-1], 100 * sum(m <= 10 for m in ms) / len(ms), w[1], w[2])
    return out
for hs, ds in ((0, 0), (1, 0), (5, 0), (10, 0), (10, 10), (20, 20)):
    r = run(hs, ds)
    print("slack home %2d m, dest %2d m:" % (hs, ds))
    for gname, (med, mx, p10, wid, wd) in r.items():
        print("   %-20s typical %5.2f (%2d)  farthest %5.2f (%2d)  <=10 %5.1f%% (%3d%%)  worst %s -> %s" % (gname, med, round(med), mx, round(mx), p10, round(p10), wid, wd))
