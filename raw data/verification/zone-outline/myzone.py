# Independent zone model (exact geometry, no grid): import via exec after setting S, V.
# zone = (even-odd interior of the closed route OR dist(route) <= BUF)
#        U  per bulge: convex hull of disk(P0, BUF) and disk(T, r_end)   (== continuous union of linearly tapered disks)
#        \  per notch: open disk(house, depth(house) + clear)
import json, math
KX, KY = 82427.8, 111079.6
def P(lat, lng): return (lng * KX, lat * KY)
def LL(x, y): return (y / KY, x / KX)
CFG = json.load(open(S + "/zone_cfg.json"))
BUF = CFG["buf"]
ROUTE = json.load(open(S + "/route.json"))
RP = [P(*p) for p in ROUTE]
SEGS = list(zip(RP, RP[1:]))

def pip(x, y, ring):
    c = False
    n = len(ring)
    for i in range(n - 1):
        ax, ay = ring[i]; bx, by = ring[i + 1]
        if (ay > y) != (by > y):
            if x < ax + (bx - ax) * (y - ay) / (by - ay): c = not c
    return c

def segdist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    qx, qy = ax + t * dx, ay + t * dy
    return math.hypot(px - qx, py - qy), (qx, qy)

def droute(x, y):
    return min(segdist(x, y, a[0], a[1], b[0], b[1])[0] for a, b in SEGS)
def nearest_route_pt(x, y):
    return min((segdist(x, y, a[0], a[1], b[0], b[1]) for a, b in SEGS), key=lambda r: r[0])[1]

MIN_R = 45.0   # builder default (min_r) for the end disk
BULGES = []
for bg in CFG["bulges"]:
    tg = [P(*t) for t in bg["targets"]]
    T = (sum(p[0] for p in tg) / len(tg), sum(p[1] for p in tg) / len(tg))
    rend = max(max(math.dist(T, p) for p in tg) + bg.get("margin", 30), bg.get("min_r", MIN_R))
    P0 = nearest_route_pt(*T)
    BULGES.append(dict(name=bg["name"], tg=tg, T=T, P0=P0, rend=rend, L=math.dist(P0, T)))

def bulge_sd(x, y, b):
    # min over t of |p - c(t)| - r(t): convex in t -> golden-section search, plus endpoints
    (x0, y0), (x1, y1) = b["P0"], b["T"]; r0, r1 = BUF, b["rend"]
    g = lambda t: math.hypot(x - (x0 + (x1 - x0) * t), y - (y0 + (y1 - y0) * t)) - (r0 + (r1 - r0) * t)
    lo, hi = 0.0, 1.0
    gr = (math.sqrt(5) - 1) / 2
    c = hi - gr * (hi - lo); d = lo + gr * (hi - lo); gc, gd = g(c), g(d)
    for _ in range(60):
        if gc < gd: hi, d, gd = d, c, gc; c = hi - gr * (hi - lo); gc = g(c)
        else: lo, c, gc = c, d, gd; d = lo + gr * (hi - lo); gd = g(d)
    return min(g(0.0), g(1.0), gc, gd)

def in_bulge(x, y, b):
    (x0, y0), (x1, y1) = b["P0"], b["T"]
    if min(x0 - BUF, x1 - b["rend"]) > x or max(x0 + BUF, x1 + b["rend"]) < x: return False
    if min(y0 - BUF, y1 - b["rend"]) > y or max(y0 + BUF, y1 + b["rend"]) < y: return False
    return bulge_sd(x, y, b) <= 0

def in_base(x, y, use_bulges=True):
    if pip(x, y, RP): return True
    if droute(x, y) <= BUF: return True
    if use_bulges:
        for b in BULGES:
            if in_bulge(x, y, b): return True
    return False

def dist_to_flip(x, y, member, rmax=400.0, ndir=720):
    # exact-ish distance from (x,y) to the boundary of a set given by member(): ray bisection in ndir directions
    m0 = member(x, y); best = rmax
    for k in range(ndir):
        a = 2 * math.pi * k / ndir; ux, uy = math.cos(a), math.sin(a)
        # march outwards in 1 m steps up to current best, then bisect
        t = 0.0; prev = 0.0; hit = None
        while t < best:
            t = min(t + 1.0, best)
            if member(x + ux * t, y + uy * t) != m0: hit = t; break
            prev = t
        if hit is None: continue
        lo, hi = prev, hit
        for _ in range(30):
            mid = (lo + hi) / 2
            if member(x + ux * mid, y + uy * mid) != m0: hi = mid
            else: lo = mid
        best = min(best, hi)
    return best

NOTCHES = []
for cv in CFG.get("carves", []):
    h = P(cv["lat"], cv["lng"])
    depth = dist_to_flip(h[0], h[1], in_base, rmax=300, ndir=720) if in_base(*h) else 0.0
    NOTCHES.append(dict(name=cv["name"], c=h, depth=depth, r=depth + cv.get("clear", 12)))

def in_zone_mine(x, y):
    for n in NOTCHES:
        if math.hypot(x - n["c"][0], y - n["c"][1]) < n["r"]: return False
    return in_base(x, y)
