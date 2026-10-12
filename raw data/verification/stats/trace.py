# usage: python3 -I trace.py <scratch> <services html> <homes html> <out json>
import sys, math, runpy, io, contextlib
sys.argv = ["vstats.py"] + sys.argv[1:5]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    g = runpy.run_path("vstats.py")
NODES, SEGS, ADJ, snaps, HOMES, dest_keys, dijkstra, inside, KX, KY = [g[k] for k in "NODES SEGS ADJ snaps HOMES dest_keys dijkstra inside KX KY".split()]
WAYS = g["WAYS"]
def ll(p): return "%.6f,%.6f" % (p[1] / KY, p[0] / KX)
def pos(u):
    if u[0] == "n": return NODES[u[1]]
    off, i, t = snaps[u]; a, b = SEGS[i][:2]; (ax, ay), (bx, by) = NODES[a], NODES[b]
    return (ax + (bx - ax) * t, ay + (by - ay) * t)
for grp, hid in (("Services", "1122804706"), ("Parks & open space", "1122799794"), ("Government & courts", "1122804750")):
    dist, prev, origin = dijkstra(dest_keys[grp])
    b = [h for h in HOMES if h["id"] == hid][0]; k = ("h", hid)
    print("==", grp, "home", hid, b["cls"], "centroid", ll(b["_c"]), "total %.1f m = %.2f min" % (dist[k] + snaps[k][0], (dist[k] + snaps[k][0]) / 60))
    print("   access leg %.1f m to segment on %s" % (snaps[k][0], SEGS[snaps[k][1]][3]))
    u = k; seq = []
    while u is not None: seq.append(u); u = prev[u]
    cum = snaps[k][0]; last = b["_c"]
    pts = [pos(x) for x in seq]
    # compress: print turning points only with street name
    out = []
    for x, y in zip(seq, seq[1:]):
        nm = None
        if x[0] == "n" and y[0] == "n":
            for i, s in enumerate(SEGS):
                if {s[0], s[1]} == {x[1], y[1]}: nm = s[3]; break
        else:
            v = x if x[0] != "n" else y; nm = SEGS[snaps[v][1]][3]
        d = math.dist(pos(x), pos(y)); cum += d
        if out and out[-1][0] == nm: out[-1][1] += d; out[-1][2] = pos(y)
        else: out.append([nm, d, pos(y)])
    for nm, d, p in out: print("   %-28s %6.1f m  -> %s" % (nm, d, ll(p)))
    dk = seq[-1]; print("   dest leg %.1f m to %s at %s  (dist at dest node %.1f)" % (snaps[dk][0], origin[k][0], ll(origin[k][1]), dist[dk]))
# connected components of the walk graph restricted to real nodes
seen = {}; comp = 0; sizes = []
for s in SEGS:
    for n in (s[0], s[1]):
        st = ("n", n)
        if st in seen: continue
        comp += 1; stack = [st]; seen[st] = comp; c = 0
        while stack:
            u = stack.pop(); c += 1
            for v, w in ADJ[u]:
                if v not in seen: seen[v] = comp; stack.append(v)
        sizes.append(c)
print("components", comp, sorted(sizes, reverse=True)[:10])
# crossing road segments without shared node, both inside/near zone
X = []
segs = [(s, NODES[s[0]], NODES[s[1]]) for s in SEGS]
def cross(p, q, r, s):
    d = (q[0]-p[0])*(s[1]-r[1]) - (q[1]-p[1])*(s[0]-r[0])
    if d == 0: return False
    t = ((r[0]-p[0])*(s[1]-r[1]) - (r[1]-p[1])*(s[0]-r[0])) / d
    u = ((r[0]-p[0])*(q[1]-p[1]) - (r[1]-p[1])*(q[0]-p[0])) / d
    return 1e-6 < t < 1 - 1e-6 and 1e-6 < u < 1 - 1e-6
for i in range(len(segs)):
    s1, p, q = segs[i]
    for j in range(i + 1, len(segs)):
        s2, r, s = segs[j]
        if {s1[0], s1[1]} & {s2[0], s2[1]}: continue
        if max(p[0], q[0]) < min(r[0], s[0]) or max(r[0], s[0]) < min(p[0], q[0]) or max(p[1], q[1]) < min(r[1], s[1]) or max(r[1], s[1]) < min(p[1], q[1]): continue
        if cross(p, q, r, s):
            mx = ((p[0]+q[0])/2, (p[1]+q[1])/2)
            X.append((s1[3], s2[3], ll(mx), inside(*mx)))
print("crossings without shared node:", len(X)); [print("  ", x) for x in X]
# dangling ends close to another road (gap < 8 m) inside zone
deg = {}
for s in SEGS:
    deg[s[0]] = deg.get(s[0], 0) + 1; deg[s[1]] = deg.get(s[1], 0) + 1
gaps = []
for n, d in deg.items():
    if d != 1 or not inside(*NODES[n]): continue
    off, i, t = g["snap"](NODES[n])
    # nearest segment not incident to n
    best = 1e9; nm = None
    for k2, s in enumerate(SEGS):
        if n in (s[0], s[1]): continue
        (ax, ay), (bx, by) = NODES[s[0]], NODES[s[1]]; P0 = NODES[n]
        dx, dy = bx-ax, by-ay; L2 = dx*dx+dy*dy
        tt = 0 if L2 == 0 else max(0, min(1, ((P0[0]-ax)*dx+(P0[1]-ay)*dy)/L2))
        dd = math.hypot(P0[0]-ax-tt*dx, P0[1]-ay-tt*dy)
        if dd < best: best = dd; nm = s[3]
    if best < 10: gaps.append((n, ll(NODES[n]), round(best, 1), nm))
print("dead ends within 10 m of another road (inside zone):", gaps)
