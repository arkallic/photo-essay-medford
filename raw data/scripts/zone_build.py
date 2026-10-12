# Build the shaded zone as one explicit outline (drawn AND used for every inside/outside test).
# zone = (loop interior OR within BUF of the route) + tapered local bulges - small notches around lone edge houses.
# usage: python3 -I scripts/zone_build.py <raw data folder>     (reads settings/zone_cfg.json, writes outputs/zone.json)
import json, math, sys
S = sys.argv[1]
KX, KY = 82427.8, 111079.6
P = lambda lat, lng: (lng * KX, lat * KY)
cfg = json.load(open(S + "/settings/zone_cfg.json"))
BUF = cfg["buf"]
R = [P(*p) for p in json.load(open(S + "/data/route.json"))]

def in_loop(x, y):
    c = False
    for (ax, ay), (bx, by) in zip(R, R[1:]):
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax: c = not c
    return c
def seg_d(x, y, a, b):
    (ax, ay), (bx, by) = a, b; dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
    t = max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / L)) if L else 0
    return math.hypot(x - ax - t * dx, y - ay - t * dy), (ax + t * dx, ay + t * dy)
def d_route(x, y):
    return min(seg_d(x, y, a, b)[0] for a, b in zip(R, R[1:]))
def nearest_on_route(x, y):
    return min((seg_d(x, y, a, b) for a, b in zip(R, R[1:])), key=lambda r: r[0])[1]

# bulges: disks sampled from the nearest route point (radius BUF) to the target point (radius r_end), radius tapering linearly
bulges = []
for bg in cfg["bulges"]:
    tg = [P(*t) for t in bg["targets"]]
    T = (sum(p[0] for p in tg) / len(tg), sum(p[1] for p in tg) / len(tg))
    r_end = max(max(math.dist(T, p) for p in tg) + bg.get("margin", 30), bg.get("min_r", 45))
    P0 = nearest_on_route(*T); L = math.dist(P0, T); n = max(2, int(L / 2))
    disks = [((P0[0] + (T[0] - P0[0]) * k / n, P0[1] + (T[1] - P0[1]) * k / n), BUF + (r_end - BUF) * k / n) for k in range(n + 1)]
    xs = [c[0] for c, r in disks]; ys = [c[1] for c, r in disks]; rm = max(r for c, r in disks)
    bulges.append(dict(name=bg["name"], disks=disks, bb=(min(xs) - rm, min(ys) - rm, max(xs) + rm, max(ys) + rm), T=T, r_end=r_end, L=L))

def base_field(x, y):
    f = 1000.0 if in_loop(x, y) else BUF - d_route(x, y)
    for b in bulges:
        x0, y0, x1, y1 = b["bb"]
        if x0 <= x <= x1 and y0 <= y <= y1:
            f = max(f, max(r - math.hypot(x - c[0], y - c[1]) for c, r in b["disks"]))
    return f
# notches: a disk around the house that reaches just past the edge (radius = distance to edge + clearance)
carves = []
for cv in cfg.get("carves", []):
    h = P(cv["lat"], cv["lng"]); f = base_field(*h)
    carves.append(dict(name=cv.get("name", ""), c=h, r=f + cv.get("clear", 12)))
def field(x, y):
    f = base_field(x, y)
    for cv in carves: f = min(f, math.hypot(x - cv["c"][0], y - cv["c"][1]) - cv["r"])
    return f

# sample on a grid and trace the f = 0 contour (marching squares, linear interpolation)
STEP = 2.0
xs = [p[0] for p in R]; ys = [p[1] for p in R]
pad = BUF + 30
X0 = min([min(xs) - pad] + [b["bb"][0] for b in bulges]); X1 = max([max(xs) + pad] + [b["bb"][2] for b in bulges])
Y0 = min([min(ys) - pad] + [b["bb"][1] for b in bulges]); Y1 = max([max(ys) + pad] + [b["bb"][3] for b in bulges])
nx = int((X1 - X0) / STEP) + 2; ny = int((Y1 - Y0) / STEP) + 2
F = [[field(X0 + i * STEP, Y0 + j * STEP) for i in range(nx)] for j in range(ny)]
def interp(p, q, fp, fq):
    t = fp / (fp - fq); return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
segs = []
for j in range(ny - 1):
    for i in range(nx - 1):
        c = [(X0 + i * STEP, Y0 + j * STEP), (X0 + (i + 1) * STEP, Y0 + j * STEP), (X0 + (i + 1) * STEP, Y0 + (j + 1) * STEP), (X0 + i * STEP, Y0 + (j + 1) * STEP)]
        v = [F[j][i], F[j][i + 1], F[j + 1][i + 1], F[j + 1][i]]
        idx = sum(1 << k for k in range(4) if v[k] > 0)
        if idx in (0, 15): continue
        e = {k: interp(c[k], c[(k + 1) % 4], v[k], v[(k + 1) % 4]) for k in range(4) if (v[k] > 0) != (v[(k + 1) % 4] > 0)}
        ks = sorted(e)
        if len(ks) == 2: segs.append((e[ks[0]], e[ks[1]]))
        else:   # saddle: pair edges using the cell-centre value
            centre = sum(v) / 4 > 0
            pairs = [(0, 1), (2, 3)] if (v[1] > 0) == centre else [(0, 3), (1, 2)]
            for a, b in pairs: segs.append((e[a], e[b]))
key = lambda p: (round(p[0], 4), round(p[1], 4))
adj = {}
for a, b in segs:
    adj.setdefault(key(a), []).append((key(b), b)); adj.setdefault(key(b), []).append((key(a), a))
pos = {}
for a, b in segs: pos[key(a)] = a; pos[key(b)] = b
seen = set(); rings = []
for k0 in list(adj):
    if k0 in seen: continue
    ring = [pos[k0]]; seen.add(k0); prev = None; cur = k0
    while True:
        nxt = [n for n, p in adj[cur] if n != prev and n not in seen]
        if not nxt:
            break
        prev, cur = cur, nxt[0]; seen.add(cur); ring.append(pos[cur])
    ring.append(ring[0])
    if len(ring) > 10: rings.append(ring)
def dp(pts, tol):   # Douglas-Peucker
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        d = seg_d(pts[i][0], pts[i][1], a, b)[0]
        if d > dmax: dmax, idx = d, i
    if dmax > tol: return dp(pts[:idx + 1], tol)[:-1] + dp(pts[idx:], tol)
    return [a, b]
rings = [dp(r, 0.4) for r in rings]
def area(r): return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(r, r[1:])) / 2
total = sum(abs(area(r)) * (1 if i == 0 else -1) for i, r in enumerate(sorted(rings, key=lambda r: -abs(area(r)))))
out = dict(rings=[[[round(y / KY, 7), round(x / KX, 7)] for x, y in r] for r in sorted(rings, key=lambda r: -abs(area(r)))], m2=total,
           bulges=[dict(name=b["name"], r_end=round(b["r_end"], 1), length=round(b["L"], 1)) for b in bulges],
           carves=[dict(name=c["name"], r=round(c["r"], 1)) for c in carves])
json.dump(out, open(S + "/outputs/zone.json", "w"))
json.dump(dict(m2=total), open(S + "/outputs/zone_area.json", "w"))
print("rings", len(rings), "vertices", [len(r) for r in rings], "area %.0f m2 = %.2f acres" % (total, total / 4046.8564))
for b in out["bulges"]: print("  bulge", b)
for c in out["carves"]: print("  notch", c)
