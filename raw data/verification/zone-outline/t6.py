# necks (non-adjacent edges), holes/islands via grid components, footprint coverage of key buildings
import sys, json, math
import xml.etree.ElementTree as ET
S, V = sys.argv[1], sys.argv[2]
exec(open(V + "/myzone.py").read())
lit = json.load(open(V + "/lits_services.json"))
ring = [P(lat, lng) for lat, lng in lit["zoneRings"][0]]
pts = ring[:-1]; n = len(pts)
E = [(pts[i], pts[(i + 1) % n]) for i in range(n)]
cum = [0.0]
for i in range(n): cum.append(cum[-1] + math.dist(*E[i]))
per = cum[-1]
def segseg(a, b, c, d):
    return min(segdist(a[0], a[1], c[0], c[1], d[0], d[1])[0], segdist(b[0], b[1], c[0], c[1], d[0], d[1])[0],
               segdist(c[0], c[1], a[0], a[1], b[0], b[1])[0], segdist(d[0], d[1], a[0], a[1], b[0], b[1])[0])
res = []
for i in range(n):
    for j in range(i + 2, n):
        if i == 0 and j == n - 1: continue
        # along-ring gap between the closest ends of the two edges
        gap = min(abs(cum[j] - cum[i + 1]), per - abs(cum[j + 1] - cum[i]))
        d = segseg(*E[i], *E[j])
        res.append((d / max(gap, 1e-9), d, gap, i, j))
# a sliver/neck = two parts of the ring far apart along the ring but close in space
necks = sorted([r for r in res if r[2] > 40], key=lambda r: r[1])
print("closest approach of ring parts >40 m apart along the ring:")
for q, d, gap, i, j in necks[:6]: print("   %.1f m apart (along-ring %.0f m) e%d/e%d" % (d, gap, i, j), LL(*pts[i]), LL(*pts[j]))
# grid components (4 m) of my zone and of the page polygon
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
X0, X1, Y0, Y1 = min(xs) - 40, max(xs) + 40, min(ys) - 40, max(ys) + 40
G = 2.0; nx = int((X1 - X0) / G) + 1; ny = int((Y1 - Y0) / G) + 1
def comps(f):
    grid = [[f(X0 + i * G, Y0 + j * G) for i in range(nx)] for j in range(ny)]
    seen = [[False] * nx for _ in range(ny)]; out = {True: [], False: []}
    for j in range(ny):
        for i in range(nx):
            if seen[j][i]: continue
            v = grid[j][i]; st = [(j, i)]; seen[j][i] = True; c = 0
            while st:
                a, b = st.pop(); c += 1
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    p, q = a + da, b + db
                    if 0 <= p < ny and 0 <= q < nx and not seen[p][q] and grid[p][q] == v:
                        seen[p][q] = True; st.append((p, q))
            out[v].append(c)
    return out
print("my zone components on 2 m grid: inside", comps(in_zone_mine)[True], "outside", comps(in_zone_mine)[False])
print("page polygon components on 2 m grid: inside", comps(lambda x, y: pip(x, y, ring))[True], "outside", comps(lambda x, y: pip(x, y, ring))[False])
# footprint coverage
root = ET.parse(S + "/wide/area.osm").getroot()
nodes = {nd.get("id"): (float(nd.get("lat")), float(nd.get("lon"))) for nd in root.iter("node")}
ways = {w.get("id"): w for w in root.iter("way")}
def cover(wid):
    w = ways[wid]; ll = [nodes[r.get("ref")] for r in w.findall("nd") if r.get("ref") in nodes]
    q = [P(*p) for p in ll]
    bx0, bx1 = min(p[0] for p in q), max(p[0] for p in q); by0, by1 = min(p[1] for p in q), max(p[1] for p in q)
    tot = ins = 0; h = 0.5
    y = by0 + h / 2
    while y < by1:
        x = bx0 + h / 2
        while x < bx1:
            if pip(x, y, q):
                tot += 1; ins += pip(x, y, ring)
            x += h
        y += h
    t = {x.get("k"): x.get("v") for x in w.findall("tag")}
    return ins / max(tot, 1), tot * h * h, t.get("name")
for wid in ["224277672", "953191972", "953191399", "953191735", "1122799914", "967132180", "1122804654"]:
    f, A, nm = cover(wid)
    print("  way %s %-40s footprint %5.0f m2, %.0f%% inside the shading" % (wid, nm, A, 100 * f))
