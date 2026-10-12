# Stats tiles with walking distance measured along the OSM street/path network (replaces straight-line x1.25).
# Homes: outputs/building_classes.json (house / multi / apartment, one per building), origin = building centroid.
# Destinations: items INSIDE the zone; parks and the school grounds are reached at their nearest edge.
# Pace 60 m/min (photo-walk pace). True metres per degree at 42.325 N.
# usage: python3 -I scripts/stats.py <raw data folder> <in-between services page>
import sys, json, math, re, heapq, statistics as st, xml.etree.ElementTree as ET
S, HTML = sys.argv[1], sys.argv[2]
KX, KY = 82427.8, 111079.6
P = lambda lat, lng: (lng * KX, lat * KY)
PACE = 60.0
R = [P(*p) for p in json.load(open(S + "/data/route.json"))]
def in_loop(x, y):
    c = False
    for (ax, ay), (bx, by) in zip(R, R[1:]):
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax: c = not c
    return c
def d_route(x, y):
    m = 1e9
    for (ax, ay), (bx, by) in zip(R, R[1:]):
        dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
        t = max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / L)) if L else 0
        m = min(m, math.hypot(x - ax - t * dx, y - ay - t * dy))
    return m
exec(open(S + "/scripts/zone_lib.py").read())
inzone = lambda p: in_zone_xy(*p)        # shared zone outline (band + local bulges - notches)

root = ET.parse(S + "/data/openstreetmap/area.osm").getroot()
nodes = {n.get("id"): P(float(n.get("lat")), float(n.get("lon"))) for n in root.iter("node")}
ways = {w.get("id"): w for w in root.iter("way")}
ROADS = {"primary", "secondary", "tertiary", "unclassified", "residential", "living_street", "primary_link", "secondary_link", "tertiary_link"}
adj = {}; segs = []
for w in root.iter("way"):
    t = {x.get("k"): x.get("v") for x in w.iter("tag")}
    hw = t.get("highway")
    if not (hw in ROADS or (hw == "service" and t.get("service") == "alley")) or t.get("access") in ("private", "no") or t.get("foot") == "no": continue
    ids = [nd.get("ref") for nd in w.iter("nd") if nd.get("ref") in nodes]
    for a, b in zip(ids, ids[1:]):
        d = math.dist(nodes[a], nodes[b])
        adj.setdefault(a, []).append((b, d)); adj.setdefault(b, []).append((a, d)); segs.append((a, b))
CELL = 50; grid = {}
for i, (a, b) in enumerate(segs):
    (ax, ay), (bx, by) = nodes[a], nodes[b]
    for gx in range(int(min(ax, bx) // CELL) - 1, int(max(ax, bx) // CELL) + 2):
        for gy in range(int(min(ay, by) // CELL) - 1, int(max(ay, by) // CELL) + 2):
            grid.setdefault((gx, gy), []).append(i)
def snap(p):
    best = None
    for r in (1, 2, 3, 5, 8):
        cands = set()
        for gx in range(int(p[0] // CELL) - r, int(p[0] // CELL) + r + 1):
            for gy in range(int(p[1] // CELL) - r, int(p[1] // CELL) + r + 1):
                cands.update(grid.get((gx, gy), []))
        for i in cands:
            a, b = segs[i]; (ax, ay), (bx, by) = nodes[a], nodes[b]
            dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
            t = max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2)) if L2 else 0
            off = math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy); L = math.sqrt(L2)
            if best is None or off < best[0]: best = (off, a, b, t * L, (1 - t) * L)
        if best is not None: return best
    raise RuntimeError("no walkable way near %s" % (p,))
def msdijkstra(sources):
    dist = {}; pq = []
    for p in sources:
        off, a, b, da, db = snap(p)
        for n, d in ((a, off + da), (b, off + db)):
            if d < dist.get(n, 1e18): dist[n] = d; heapq.heappush(pq, (d, n))
    while pq:
        d, n = heapq.heappop(pq)
        if d > dist.get(n, 1e18): continue
        for m, w in adj.get(n, []):
            nd = d + w
            if nd < dist.get(m, 1e18): dist[m] = nd; heapq.heappush(pq, (nd, m))
    return dist
def edge_points(osm_id, step=5.0):
    w = ways[osm_id.split("/")[1]]
    q = [nodes[r.get("ref")] for r in w.findall("nd") if r.get("ref") in nodes]
    pts = []
    for a, b in zip(q, q[1:]):
        n = max(1, int(math.dist(a, b) // step))
        pts += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(n)]
    return pts
EDGE = {"tree", "school", "track"}   # areas you arrive at when you reach their edge

B = json.load(open(S + "/outputs/building_classes.json"))
homes = [(P(*b["c"]), snap(P(*b["c"]))) for b in B if b["cls"] in ("house", "multi", "apartment")]
assert all(inzone(c) for c, _ in homes)
h = open(HTML, encoding="utf-8").read()
sv = json.loads(re.search(r"const services = (\[.*?\]);\n", h, re.S).group(1))
bus = json.loads(re.search(r"const busStops = (\[.*?\]);\n", h, re.S).group(1))
ins = [s for s in sv if inzone(P(s["lat"], s["lng"]))]
assert len(ins) == sum(s["inside"] for s in sv), "inside flags disagree with zone test"
binz = [b for b in bus if inzone(P(b["lat"], b["lng"]))]
acres = json.load(open(S + "/outputs/zone_area.json"))["m2"] / 4046.8564
groups = [("All services", ins), ("Bus stops", binz),
          ("Government & courts", [s for s in ins if s["cat"] == "Government & courts"]),
          ("Health & social services", [s for s in ins if s["cat"] == "Health & social services"]),
          ("Parks only", [s for s in ins if s.get("icon") in ("tree", "track")]),
          ("Places of worship", [s for s in ins if s["cat"] == "Places of worship"]),
          ("Banking", [s for s in ins if s["cat"] == "Banking & finance"]),
          ("Education", [s for s in ins if s["cat"] == "Education"]),
          ("Recreation & parks", [s for s in ins if s["cat"] == "Recreation & parks"]),
          ("Businesses", [dict(lat=b["c"][0], lng=b["c"][1]) for b in B if b["cls"] == "business"])]
H = len(homes); rows = []
print("graph nodes", len(adj), "homes", H, "acres %.2f" % acres)
for name, items in groups:
    if not items: continue
    src = []
    for s in items:
        if s.get("icon") in EDGE and s.get("osm", "").startswith("way/"): src += edge_points(s["osm"])
        else: src.append(P(s["lat"], s["lng"]))
    dist = msdijkstra(src)
    mins = []
    for c, (off, a, b, da, db) in homes:
        dn = min(dist.get(a, 1e18) + da, dist.get(b, 1e18) + db) + off
        dn = max(dn, min(math.dist(c, q) for q in src))   # never shorter than straight line
        mins.append(dn / PACE)
    mins.sort()
    r = dict(label=name, n=len(items), acres_each=acres / len(items), homes_each=H / len(items), walk_min=st.median(mins), walk_max=mins[-1],
             pct5=100 * sum(x <= 5 for x in mins) / H, pct10=100 * sum(x <= 10 for x in mins) / H)
    rows.append(r)
    print("%-26s n=%2d acres %5.1f homes %5.1f typical %4.1f max %4.1f <=10 %5.1f%%" % (name, r["n"], r["acres_each"], r["homes_each"], r["walk_min"], r["walk_max"], r["pct10"]))
# --- streets ("road access"): length inside the zone and street intersections ---
street_len = alley_len = 0.0; deg = {}
for w in root.iter("way"):
    t = {x.get("k"): x.get("v") for x in w.iter("tag")}
    hw = t.get("highway"); is_alley = hw == "service" and t.get("service") == "alley"
    if not (hw in ROADS or is_alley): continue
    ids = [nd.get("ref") for nd in w.iter("nd") if nd.get("ref") in nodes]
    for a, b in zip(ids, ids[1:]):
        (ax, ay), (bx, by) = nodes[a], nodes[b]; L = math.dist(nodes[a], nodes[b]); n = max(1, int(L))
        inside = sum(in_zone_xy(ax + (bx - ax) * (k + .5) / n, ay + (by - ay) * (k + .5) / n) for k in range(n)) / n * L
        if is_alley: alley_len += inside
        else:
            street_len += inside
            deg.setdefault(a, set()).add(b); deg.setdefault(b, set()).add(a)
inter = [n for n, nb in deg.items() if len(nb) >= 3 and in_zone_xy(*nodes[n])]
streets = dict(street_mi=street_len / 1609.344, alley_mi=alley_len / 1609.344, intersections=len(inter), per_100_acres=len(inter) / acres * 100,
               homes_per_street_mi=H / (street_len / 1609.344))
print("streets:", {k: round(v, 2) for k, v in streets.items()})
counts = {c: sum(1 for b in B if b["cls"] == c) for c in ("house", "multi", "apartment", "business", "government", "worship", "nonprofit", "outbuilding")}
json.dump(dict(H=H, acres=acres, rows=rows, method="network-roads", pace=PACE, streets=streets, counts=counts), open(S + "/outputs/stats.json", "w"), indent=1)
