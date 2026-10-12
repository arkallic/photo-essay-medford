# Ring topology + smoothness of the page outline
import sys, json, math
S, V = sys.argv[1], sys.argv[2]
exec(open(V + "/myzone.py").read())
for pg in ["lits_services.json", "lits_homes.json"]:
    zr = json.load(open(V + "/" + pg))["zoneRings"]
    print(pg, "rings:", len(zr), "vertices:", [len(r) for r in zr])
page = json.load(open(V + "/lits_services.json"))["zoneRings"]
ring = [P(lat, lng) for lat, lng in page[0]]
pts = ring[:-1]; n = len(pts)
# duplicates
dup = [(i, j) for i in range(n) for j in range(i + 1, n) if math.dist(pts[i], pts[j]) < 1e-6]
print("duplicate vertices:", dup)
# self-intersections (proper + touching)
def orient(a, b, c): return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
def seg_inter(p1, p2, p3, p4):
    d1, d2, d3, d4 = orient(p3, p4, p1), orient(p3, p4, p2), orient(p1, p2, p3), orient(p1, p2, p4)
    if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)) and d1 and d2 and d3 and d4: return True
    return False
E = [(pts[i], pts[(i + 1) % n]) for i in range(n)]
X = []
for i in range(n):
    for j in range(i + 2, n):
        if i == 0 and j == n - 1: continue
        if seg_inter(*E[i], *E[j]): X.append((i, j))
print("self-intersections:", X)
# minimum distance between non-adjacent edges (narrowest neck / sliver)
def segseg(a, b, c, d):
    return min(segdist(a[0], a[1], c[0], c[1], d[0], d[1])[0], segdist(b[0], b[1], c[0], c[1], d[0], d[1])[0],
               segdist(c[0], c[1], a[0], a[1], b[0], b[1])[0], segdist(d[0], d[1], a[0], a[1], b[0], b[1])[0])
# along-ring distance to exclude local neighbourhood
cum = [0.0]
for i in range(n): cum.append(cum[-1] + math.dist(pts[i], pts[(i + 1) % n]))
per = cum[-1]
print("perimeter m %.1f" % per)
necks = []
for i in range(n):
    for j in range(i + 1, n):
        along = abs(cum[j] - cum[i]); along = min(along, per - along)
        if along < 60: continue
        d = segseg(*E[i], *E[j])
        necks.append((d, i, j, along))
necks.sort()
print("narrowest non-local gaps (d, i, j, along-ring m):")
for d, i, j, al in necks[:6]: print("   %.1f m  v%d-v%d  along %.0f m" % (d, i, j, al), LL(*pts[i]), LL(*pts[j]))
# edge lengths
L = [math.dist(pts[i], pts[(i + 1) % n]) for i in range(n)]
Ls = sorted(L)
print("edge length: min %.2f  p10 %.2f  median %.2f  max %.2f" % (Ls[0], Ls[n // 10], Ls[n // 2], Ls[-1]))
# turning angles; orientation
A2 = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
sgn = 1 if A2 > 0 else -1   # CCW positive
tur = []
for i in range(n):
    a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
    h1 = math.atan2(b[1] - a[1], b[0] - a[0]); h2 = math.atan2(c[1] - b[1], c[0] - b[0])
    d = (h2 - h1 + math.pi) % (2 * math.pi) - math.pi
    tur.append(math.degrees(d) * sgn)    # + = convex (turn toward interior), - = concave
print("total turning %.1f deg" % sum(tur))
big = [(i, t) for i, t in enumerate(tur) if abs(t) > 20]
print("vertices with |turn| > 20 deg:")
for i, t in big:
    print("   v%d turn %+.1f  in-edge %.1f m out-edge %.1f m" % (i, t, L[i - 1], L[i]), LL(*pts[i]))
# local zig-zag: sign alternation with short edges
zz = [i for i in range(n) if abs(tur[i]) > 3 and abs(tur[(i + 1) % n]) > 3 and tur[i] * tur[(i + 1) % n] < 0 and L[i] < 3]
print("zig-zag pairs (opposite turns >3 deg joined by edge <3 m):", [(i, round(tur[i], 1), round(tur[(i + 1) % n], 1), round(L[i], 2)) for i in zz])
# curvature consistency: for arcs, turning/edge vs expected 1/r
print("per-vertex: idx turn(deg) Lin Lout  approx radius(m)")
for i in range(n):
    r = (L[i - 1] + L[i]) / 2 / max(1e-9, abs(math.radians(tur[i])))
    print("  %3d %+6.1f %6.1f %6.1f %8.1f  %s" % (i, tur[i], L[i - 1], L[i], r, LL(*pts[i])))
