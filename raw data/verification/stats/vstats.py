# Independent re-computation of the stats card on the two services pages.
# usage: python3 -I vstats.py <scratch dir> <services html> <homes html> <out json>
import sys, json, re, math, heapq, statistics, xml.etree.ElementTree as ET
from collections import Counter, defaultdict

S, SV, HM, OUT = sys.argv[1:5]
KX, KY = 82427.8, 111079.6
def P(lat, lng): return (lng * KX, lat * KY)
PACE = 60.0

def js_literal(h, name):
    i = h.index("const %s = " % name) + len("const %s = " % name)
    depth = 0; instr = False; esc = False
    for j in range(i, len(h)):
        ch = h[j]
        if instr:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': instr = False
            continue
        if ch == '"': instr = True
        elif ch in "[{": depth += 1
        elif ch in "]}":
            depth -= 1
            if depth == 0: return json.loads(h[i:j + 1])
    raise ValueError(name)

hs = open(SV, encoding="utf-8").read(); hh = open(HM, encoding="utf-8").read()
out = {}
# ---------------- zone ----------------
ZR_s = js_literal(hs, "zoneRings"); ZR_h = js_literal(hh, "zoneRings")
zj = json.load(open(S + "/zone.json"))
out["zone_same_both_pages"] = ZR_s == ZR_h
out["zone_same_as_zone_json"] = ZR_s == zj["rings"]
RINGS = [[P(a, b) for a, b in r] for r in ZR_s]
out["zone_ring_closed"] = [r[0] == r[-1] for r in RINGS]
EDGES = []
for r in RINGS:
    pts = r if r[0] == r[-1] else r + [r[0]]
    EDGES += list(zip(pts, pts[1:]))
def inside(x, y):
    c = False
    for (ax, ay), (bx, by) in EDGES:
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax: c = not c
    return c
def shoelace(r):
    pts = r if r[0] == r[-1] else r + [r[0]]
    ox, oy = pts[0]; pts = [(x - ox, y - oy) for x, y in pts]
    return sum(ax * by - bx * ay for (ax, ay), (bx, by) in zip(pts, pts[1:])) / 2
areas = [shoelace(r) for r in RINGS]
m2 = abs(sum(areas)) if len(RINGS) > 1 else abs(areas[0])
acres = m2 / 4046.8564224
out["zone_m2_shoelace"] = m2; out["zone_m2_json"] = zj["m2"]; out["acres"] = acres; out["sqmi"] = acres / 640

# ---------------- buildings ----------------
B = json.load(open(S + "/site/bclass_county.json"))
cnt = Counter(b["cls"] for b in B); out["bclass_counts"] = dict(cnt)
def centroid(pts):
    q = [P(a, b) for a, b in pts]
    if q[0] != q[-1]: q.append(q[0])
    ox, oy = q[0]; q = [(x - ox, y - oy) for x, y in q]
    A = cx = cy = 0
    for (x0, y0), (x1, y1) in zip(q, q[1:]):
        cr = x0 * y1 - x1 * y0; A += cr; cx += (x0 + x1) * cr; cy += (y0 + y1) * cr
    A /= 2
    return (cx / (6 * A) + ox, cy / (6 * A) + oy), abs(A)
cdev = []; adev = []
for b in B:
    (cx, cy), A = centroid(b["pts"]); px, py = P(*b["c"])
    cdev.append(math.hypot(cx - px, cy - py)); adev.append(abs(A - b["a"]))
    b["_c"] = (cx, cy)
out["centroid_max_dev_m"] = max(cdev); out["area_max_dev_m2"] = max(adev)
out["bclass_all_inside_by_c"] = Counter((b["cls"], inside(*P(*b["c"]))) for b in B)
out["bclass_all_inside_by_c"] = {"%s|%s" % k: v for k, v in out["bclass_all_inside_by_c"].items()}
BL = js_literal(hh, "BLDG")
map_cls = {"house": "house", "multi": "multi", "apt": "apartment", "shed": "outbuilding", "biz": "business", "pub": "public"}
bl_cnt = Counter(map_cls[c] for c, _ in BL); out["BLDG_counts"] = dict(bl_cnt)
bl_in = Counter()
for c, pts in BL:
    (cx, cy), A = centroid(pts); bl_in[(map_cls[c], inside(cx, cy))] += 1
out["BLDG_inside"] = {"%s|%s" % k: v for k, v in bl_in.items()}
BLOCKS = js_literal(hh, "BLOCKS")
out["BLOCKS_sum_h"] = sum(b["h"] for b in BLOCKS); out["BLOCKS_sum_a"] = sum(b["a"] for b in BLOCKS); out["BLOCKS_n"] = len(BLOCKS)

HOMES = [b for b in B if b["cls"] in ("house", "multi", "apartment")]
out["homes_n"] = len(HOMES)
out["homes_outside_zone"] = [b["id"] for b in HOMES if not inside(*b["_c"])]

# ---------------- road graph ----------------
root = ET.parse(S + "/wide/area.osm").getroot()
NODES = {n.get("id"): P(float(n.get("lat")), float(n.get("lon"))) for n in root.iter("node")}
WAYS = {w.get("id"): w for w in root.iter("way")}
ROAD = {"motorway_link", "trunk", "trunk_link", "primary", "secondary", "tertiary", "unclassified", "residential",
        "living_street", "primary_link", "secondary_link", "tertiary_link"}
SEGS = []   # (a, b, alley, wayname, wayid)
missing = 0
for w in root.iter("way"):
    t = {x.get("k"): x.get("v") for x in w.iter("tag")}
    hw = t.get("highway")
    alley = hw == "service" and t.get("service") == "alley"
    if not (hw in ROAD or alley): continue
    ids = [nd.get("ref") for nd in w.iter("nd")]
    missing += sum(1 for i in ids if i not in NODES)
    for a, b in zip(ids, ids[1:]):
        SEGS.append((a, b, alley, t.get("name", "(alley)" if alley else "?"), w.get("id")))
out["road_missing_nodes"] = missing; out["road_segments"] = len(SEGS)
CELL = 40; GRID = defaultdict(list)
for i, (a, b, *_ ) in enumerate(SEGS):
    (ax, ay), (bx, by) = NODES[a], NODES[b]
    for gx in range(int(min(ax, bx) // CELL), int(max(ax, bx) // CELL) + 1):
        for gy in range(int(min(ay, by) // CELL), int(max(ay, by) // CELL) + 1):
            GRID[(gx, gy)].append(i)
def snap(p):
    best = None
    r = 0
    while True:
        gx0, gy0 = int(p[0] // CELL), int(p[1] // CELL)
        cand = set()
        for gx in range(gx0 - r, gx0 + r + 1):
            for gy in range(gy0 - r, gy0 + r + 1):
                cand.update(GRID.get((gx, gy), ()))
        for i in cand:
            a, b = SEGS[i][:2]; (ax, ay), (bx, by) = NODES[a], NODES[b]
            dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
            t = 0 if L2 == 0 else max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
            off = math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)
            if best is None or off < best[0]: best = (off, i, t)
        # a candidate found within r cells is guaranteed nearest once off <= r*CELL
        if best is not None and best[0] <= r * CELL: return best
        r += 1
        if r > 50: return best

# ---------------- destinations ----------------
SVC = js_literal(hs, "services"); SVC_h = js_literal(hh, "services")
BUS = js_literal(hs, "busStops"); BUS_h = js_literal(hh, "busStops")
out["services_same_both_pages"] = SVC == SVC_h; out["bus_same_both_pages"] = BUS == BUS_h
INS = [s for s in SVC if inside(*P(s["lat"], s["lng"]))]
out["services_total"] = len(SVC); out["services_inside"] = len(INS)
out["services_inside_flag_mismatch"] = [s["name"] for s in SVC if s.get("inside") != inside(*P(s["lat"], s["lng"]))]
BIN = [b for b in BUS if inside(*P(b["lat"], b["lng"]))]
out["bus_total"] = len(BUS); out["bus_inside"] = len(BIN)
out["cat_counts_inside"] = dict(Counter(s["cat"] for s in INS))
out["icon_counts_inside"] = dict(Counter(s["icon"] for s in INS))

def ring_of_way(wid):
    w = WAYS[wid]
    return [NODES[n.get("ref")] for n in w.iter("nd")]
def edge_samples(wid, step=2.0):
    q = ring_of_way(wid); pts = []
    for a, b in zip(q, q[1:]):
        n = max(1, int(math.ceil(math.dist(a, b) / step)))
        pts += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(n)]
    return pts
EDGE_ICONS = {"tree", "school", "track"}
def dest_points(s):
    if s.get("icon") in EDGE_ICONS and str(s.get("osm", "")).startswith("way/"):
        return [(p, s["name"]) for p in edge_samples(s["osm"].split("/")[1])]
    return [(P(s["lat"], s["lng"]), s["name"])]
BIZ = [dict(name="biz " + b["id"], lat=b["c"][0], lng=b["c"][1]) for b in B if b["cls"] == "business"]
out["biz_inside"] = sum(inside(*P(b["lat"], b["lng"])) for b in BIZ)
GROUPS = [("Services", INS), ("Bus stops", [dict(b, name="bus " + b["name"]) for b in BIN]),
          ("Government & courts", [s for s in INS if s["cat"] == "Government & courts"]),
          ("Health & social", [s for s in INS if s["cat"] == "Health & social services"]),
          ("Parks & open space", [s for s in INS if s["icon"] in ("tree", "track")]),
          ("Places of worship", [s for s in INS if s["cat"] == "Places of worship"]),
          ("Banking & finance", [s for s in INS if s["cat"] == "Banking & finance"]),
          ("Education", [s for s in INS if s["cat"] == "Education"]),
          ("Businesses", BIZ)]
out["group_members"] = {g: [s["name"] for s in items] for g, items in GROUPS}

# ---------------- exact graph with virtual nodes ----------------
snaps = {}          # key -> (off, seg, t)
home_keys = []
for b in HOMES:
    k = ("h", b["id"]); snaps[k] = snap(b["_c"]); home_keys.append(k)
dest_keys = {}
for g, items in GROUPS:
    ks = []
    for s in items:
        for j, (p, nm) in enumerate(dest_points(s)):
            k = ("d", nm, round(p[0], 3), round(p[1], 3))
            if k not in snaps: snaps[k] = snap(p)
            ks.append((k, p, nm))
    dest_keys[g] = ks
on_seg = defaultdict(list)
for k, (off, i, t) in snaps.items(): on_seg[i].append((t, k))
ADJ = defaultdict(list)
def add(u, v, w): ADJ[u].append((v, w)); ADJ[v].append((u, w))
for i, (a, b, alley, nm, wid) in enumerate(SEGS):
    L = math.dist(NODES[a], NODES[b])
    chain = [(0.0, ("n", a))] + sorted(on_seg.get(i, []), key=lambda x: x[0]) + [(1.0, ("n", b))]
    for (t0, u), (t1, v) in zip(chain, chain[1:]):
        add(u, v, (t1 - t0) * L)
SEGNAME = {}
for i, (a, b, alley, nm, wid) in enumerate(SEGS):
    SEGNAME[frozenset((("n", a), ("n", b)))] = nm

def dijkstra(srcs):
    dist = {}; prev = {}; origin = {}; pq = []
    for k, p, nm in srcs:
        off = snaps[k][0]
        if off < dist.get(k, 1e18): dist[k] = off; origin[k] = (nm, p); prev[k] = None; heapq.heappush(pq, (off, k))
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, w in ADJ[u]:
            nd = d + w
            if nd < dist.get(v, 1e18): dist[v] = nd; prev[v] = u; origin[v] = origin[u]; heapq.heappush(pq, (nd, v))
    return dist, prev, origin

H = len(HOMES); res = {}
traces = {}
for g, items in GROUPS:
    dist, prev, origin = dijkstra(dest_keys[g])
    rows = []
    for b, k in zip(HOMES, home_keys):
        dn = dist[k] + snaps[k][0]
        sl = min(math.dist(b["_c"], p) for _, p, _ in dest_keys[g])
        rows.append((dn / PACE, b, k, sl))
    mins = sorted(r[0] for r in rows)
    worst = max(rows, key=lambda r: r[0])
    res[g] = dict(n=len(items), acres_each=acres / len(items), homes_each=H / len(items), median=statistics.median(mins),
                  max=mins[-1], pct10=100 * sum(m <= 10 for m in mins) / H, pct5=100 * sum(m <= 5 for m in mins) / H,
                  worst_home=worst[1]["id"], worst_home_latlng=worst[1]["c"], worst_cls=worst[1]["cls"],
                  worst_dest=origin[worst[2]][0], worst_m=worst[0] * PACE, worst_straight_m=worst[3],
                  worst_access_m=snaps[worst[2]][0])
    # trace path street names
    u = worst[2]; names = []; nodes_seq = []
    while u is not None:
        nodes_seq.append(u)
        u = prev[u]
    for x, y in zip(nodes_seq, nodes_seq[1:]):
        pass
    # map virtual chain to segment names via snap seg index
    segnames = []
    for x in nodes_seq:
        if x[0] == "n": continue
        i = snaps[x][1]; segnames.append(SEGS[i][3])
    # names of real segments traversed
    trav = []
    for x, y in zip(nodes_seq, nodes_seq[1:]):
        nm = SEGNAME.get(frozenset((x, y)))
        if nm is None:
            # find via snap seg of virtual node
            v = x if x[0] != "n" else y
            if v[0] != "n": nm = SEGS[snaps[v][1]][3]
        if nm and (not trav or trav[-1] != nm): trav.append(nm)
    res[g]["worst_route_streets"] = trav
    res[g]["worst_dest_access_m"] = snaps[nodes_seq[-1]][0] if nodes_seq[-1][0] != "n" else None
out["tiles"] = res

# ---------------- streets ----------------
def clip_len(p, q):
    ts = [0.0, 1.0]
    for (ax, ay), (bx, by) in EDGES:
        # segment p-q vs a-b intersection
        rx, ry = q[0] - p[0], q[1] - p[1]; sx, sy = bx - ax, by - ay
        den = rx * sy - ry * sx
        if den == 0: continue
        t = ((ax - p[0]) * sy - (ay - p[1]) * sx) / den
        u = ((ax - p[0]) * ry - (ay - p[1]) * rx) / den
        if 0 <= t <= 1 and 0 <= u <= 1: ts.append(t)
    ts.sort(); L = math.dist(p, q); tot = 0
    for t0, t1 in zip(ts, ts[1:]):
        if t1 - t0 <= 0: continue
        tm = (t0 + t1) / 2
        if inside(p[0] + (q[0] - p[0]) * tm, p[1] + (q[1] - p[1]) * tm): tot += (t1 - t0) * L
    return tot
street = alley_m = 0.0; nb = defaultdict(set); nb_all = defaultdict(set); ways_at = defaultdict(set)
by_hw = Counter()
for a, b, alley, nm, wid in SEGS:
    l = clip_len(NODES[a], NODES[b])
    if alley: alley_m += l
    else:
        street += l; nb[a].add(b); nb[b].add(a); ways_at[a].add(wid); ways_at[b].add(wid)
        t = {x.get("k"): x.get("v") for x in WAYS[wid].iter("tag")}; by_hw[t["highway"]] += l
    nb_all[a].add(b); nb_all[b].add(a)
inter = [n for n, s in nb.items() if len(s) >= 3 and inside(*NODES[n])]
inter_all = [n for n, s in nb_all.items() if len(s) >= 3 and inside(*NODES[n])]
# group intersections of distinct street names (to spot dual-carriageway / split-way double counts)
def wname(wid): return {x.get("k"): x.get("v") for x in WAYS[wid].iter("tag")}.get("name")
out["streets"] = dict(street_mi=street / 1609.344, alley_mi=alley_m / 1609.344, intersections=len(inter),
                      per_sqmi=len(inter) / (acres / 640), homes_per_street_mi=H / (street / 1609.344),
                      intersections_incl_alleys=len(inter_all), by_highway_mi={k: v / 1609.344 for k, v in by_hw.items()})
# near-duplicate intersections (within 15 m)
close = []
for i, a in enumerate(inter):
    for b2 in inter[i + 1:]:
        d = math.dist(NODES[a], NODES[b2])
        if d < 20: close.append((a, b2, round(d, 1), sorted({wname(w) for w in ways_at[a] | ways_at[b2]} - {None})))
out["streets"]["close_intersection_pairs"] = close
out["streets"]["deg_hist"] = dict(Counter(len(nb[n]) for n in inter))
json.dump(out, open(OUT, "w"), indent=1, default=str)
for k, v in out.items():
    if k != "tiles": print(k, json.dumps(v, default=str)[:600])
for g, r in res.items():
    print("%-22s n=%2d acres/ %.2f homes/ %.2f med %.3f max %.3f pct10 %.2f pct5 %.2f | worst %s (%s) -> %s %.0f m (straight %.0f, access %.0f) via %s" % (
        g, r["n"], r["acres_each"], r["homes_each"], r["median"], r["max"], r["pct10"], r["pct5"], r["worst_home"], r["worst_cls"], r["worst_dest"], r["worst_m"],
        r["worst_straight_m"], r["worst_access_m"], " > ".join(r["worst_route_streets"])))
