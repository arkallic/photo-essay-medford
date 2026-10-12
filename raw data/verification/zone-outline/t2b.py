# Compare my exact zone with the page zoneRings: area, XOR area, two-sided boundary deviation.
import sys, json, math, time
S, V = sys.argv[1], sys.argv[2]
exec(open(V + "/myzone.py").read())
page = json.load(open(V + "/lits_services.json"))["zoneRings"]
ring = [P(lat, lng) for lat, lng in page[0]]
def shoelace(r): return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(r, r[1:])) / 2
A_page = abs(shoelace(ring))
print("page ring vertices", len(ring), "closed", ring[0] == ring[-1], "area m2 %.1f acres %.3f sqmi %.4f" % (A_page, A_page / 4046.8564224, A_page / 2589988.110336))
print("signed area (orientation)", "CCW" if shoelace(ring) > 0 else "CW")
in_page = lambda x, y: pip(x, y, ring)

xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
for b in BULGES:
    xs += [b["T"][0] - b["rend"], b["T"][0] + b["rend"]]; ys += [b["T"][1] - b["rend"], b["T"][1] + b["rend"]]
X0, X1 = min(xs) - 20, max(xs) + 20; Y0, Y1 = min(ys) - 20, max(ys) + 20
G = 4.0
nx = int((X1 - X0) / G) + 1; ny = int((Y1 - Y0) / G) + 1
t0 = time.time()
M = [[in_zone_mine(X0 + i * G, Y0 + j * G) for i in range(nx + 1)] for j in range(ny + 1)]
Q = [[in_page(X0 + i * G, Y0 + j * G) for i in range(nx + 1)] for j in range(ny + 1)]
print("coarse grid", nx, ny, "%.1fs" % (time.time() - t0))
SUB = 16; h = G / SUB
A_mine = 0.0; A_xor = 0.0; A_mine_not_page = 0.0; A_page_not_mine = 0.0
bpts = []          # my boundary points (horizontal crossings, refined by bisection)
nb = 0
for j in range(ny):
    for i in range(nx):
        cm = [M[j][i], M[j][i + 1], M[j + 1][i], M[j + 1][i + 1]]
        cq = [Q[j][i], Q[j][i + 1], Q[j + 1][i], Q[j + 1][i + 1]]
        x0, y0 = X0 + i * G, Y0 + j * G
        if all(cm) and all(cq): A_mine += G * G; continue
        if not any(cm) and not any(cq):
            continue
        nb += 1
        for sj in range(SUB):
            yy = y0 + (sj + .5) * h
            row = [(in_zone_mine(x0 + (si + .5) * h, yy), in_page(x0 + (si + .5) * h, yy)) for si in range(SUB)]
            for (mm, pp) in row:
                if mm: A_mine += h * h
                if mm != pp:
                    A_xor += h * h
                    if mm: A_mine_not_page += h * h
                    else: A_page_not_mine += h * h
            # boundary crossings of my zone along this row (extended one sample beyond each side of the cell)
            rx = [x0 + (si + .5) * h for si in range(-1, SUB + 1)]
            rm = [in_zone_mine(x, yy) for x in rx]
            for si in range(len(rx) - 1):
                if rm[si] != rm[si + 1]:
                    lo, hi = rx[si], rx[si + 1]; mlo = rm[si]
                    for _ in range(25):
                        mid = (lo + hi) / 2
                        if in_zone_mine(mid, yy) == mlo: lo = mid
                        else: hi = mid
                    bpts.append(((lo + hi) / 2, yy))
        # vertical crossings too (catch horizontal-ish boundary)
        for si in range(0, SUB):
            xx = x0 + (si + .5) * h
            cy_ = [y0 + (sj + .5) * h for sj in range(-1, SUB + 1)]
            col = [in_zone_mine(xx, y) for y in cy_]
            for sj in range(len(cy_) - 1):
                if col[sj] != col[sj + 1]:
                    lo, hi = cy_[sj], cy_[sj + 1]; mlo = col[sj]
                    for _ in range(25):
                        mid = (lo + hi) / 2
                        if in_zone_mine(xx, mid) == mlo: lo = mid
                        else: hi = mid
                    bpts.append((xx, (lo + hi) / 2))
print("boundary cells", nb, "%.1fs" % (time.time() - t0))
print("my area m2 %.1f acres %.3f sqmi %.4f" % (A_mine, A_mine / 4046.8564224, A_mine / 2589988.110336))
print("XOR area m2 %.1f  (mine-not-page %.1f, page-not-mine %.1f), rel %.5f" % (A_xor, A_mine_not_page, A_page_not_mine, A_xor / A_mine))

# distance from my boundary points to page polygon edges
segs = list(zip(ring, ring[1:]))
def d_page(x, y):
    return min(segdist(x, y, a[0], a[1], b[0], b[1])[0] for a, b in segs)
dm = [(d_page(x, y), x, y) for x, y in bpts]
dm.sort(reverse=True)
print("my boundary pts", len(bpts), "-> page edge: max %.3f m, p99 %.3f, mean %.3f" % (dm[0][0], dm[len(dm) // 100][0], sum(d for d, _, _ in dm) / len(dm)))
for d, x, y in dm[:8]: print("   %.3f m at" % d, LL(x, y))
# distance from page edge samples to my boundary (via nearest boundary point; boundary pts spacing <= 0.25 m)
cell = {}
for x, y in bpts: cell.setdefault((int(x // 5), int(y // 5)), []).append((x, y))
def d_mine(x, y):
    best = 1e9; cx, cy = int(x // 5), int(y // 5); r = 1
    while True:
        for di in range(-r, r + 1):
            for dj in range(-r, r + 1):
                for (bx, by) in cell.get((cx + di, cy + dj), ()):
                    best = min(best, math.hypot(x - bx, y - by))
        if best <= (r) * 5 or r > 20: return best
        r += 1
pv = []
for a, b in segs:
    L = math.dist(a, b); n = max(1, int(L / 0.5))
    for k in range(n):
        t = k / n; x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        pv.append((d_mine(x, y), x, y, k == 0))
pv.sort(reverse=True)
print("page edge samples", len(pv), "-> my boundary: max %.3f m, p99 %.3f, mean %.3f" % (pv[0][0], pv[len(pv) // 100][0], sum(p[0] for p in pv) / len(pv)))
for d, x, y, isv in pv[:8]: print("   %.3f m at" % d, LL(x, y), "vertex" if isv else "edge")
vv = sorted([p for p in pv if p[3]], reverse=True)
print("page VERTICES -> my boundary: max %.3f m mean %.3f" % (vv[0][0], sum(p[0] for p in vv) / len(vv)))
json.dump(dict(bpts=bpts), open(V + "/my_bpts.json", "w"))
