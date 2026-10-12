import json, math, sys, xml.etree.ElementTree as ET
OSM, DATA = sys.argv[1], sys.argv[2]
D = json.load(open(DATA))
KX, KY = 82427.8, 111079.6
ring = [(lng * KX, lat * KY) for lat, lng in D["zoneRings"][0]]
assert len(D["zoneRings"]) == 1
if ring[0] != ring[-1]: ring.append(ring[0])
def inside(lat, lng):
    x, y = lng * KX, lat * KY; c = False
    for (ax, ay), (bx, by) in zip(ring, ring[1:]):
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax: c = not c
    return c
def dseg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)
def edge_d(lat, lng):
    x, y = lng * KX, lat * KY
    return min(dseg(x, y, *a, *b) for a, b in zip(ring, ring[1:]))
def sd(lat, lng):  # signed: + inside
    return edge_d(lat, lng) * (1 if inside(lat, lng) else -1)
# area
A = 0
for (ax, ay), (bx, by) in zip(ring, ring[1:]): A += ax * by - bx * ay
A = abs(A) / 2
print("zone area m2 %.0f acres %.1f sqmi %.3f  ring pts %d" % (A, A / 4046.8564, A / 2589988.11, len(ring)))
root = ET.parse(OSM).getroot()
nodes = {}; ntags = {}; ways = {}; wtags = {}; rels = {}; rtags = {}
def tg(el): return {t.get("k"): t.get("v") for t in el.findall("tag")}
for n in root.iter("node"):
    nodes[n.get("id")] = (float(n.get("lat")), float(n.get("lon"))); ntags[n.get("id")] = tg(n)
for w in root.iter("way"):
    ways[w.get("id")] = [r.get("ref") for r in w.findall("nd")]; wtags[w.get("id")] = tg(w)
for r in root.iter("relation"):
    rels[r.get("id")] = [(m.get("type"), m.get("ref"), m.get("role")) for m in r.findall("member")]; rtags[r.get("id")] = tg(r)
def wpts(i): return [nodes[r] for r in ways[i] if r in nodes]
def centroid(pts):
    # area-weighted polygon centroid in xy, fallback vertex mean
    P = [(lng * KX, lat * KY) for lat, lng in pts]
    if len(P) >= 4 and P[0] == P[-1]:
        a = cx = cy = 0
        for (x0, y0), (x1, y1) in zip(P, P[1:]):
            c = x0 * y1 - x1 * y0; a += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c
        if abs(a) > 1e-6:
            return (cy / (3 * a) / KY, cx / (3 * a) / KX)
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
def vmean(pts):
    q = pts[:-1] if len(pts) > 1 and pts[0] == pts[-1] else pts
    return (sum(p[0] for p in q) / len(q), sum(p[1] for p in q) / len(q))
def dist(a, b): return math.hypot((a[1] - b[1]) * KX, (a[0] - b[0]) * KY)
print("\n=== SERVICES vs OSM ===")
for s in D["services"]:
    ids = s["osm"].split("+")
    print("\n#", s["name"], "|", s["cat"], "|", s["icon"], "| note:", s.get("note"), "| inside flag:", s["inside"])
    allpts = []
    for oid in ids:
        typ, i = oid.split("/")
        if typ == "node":
            t = ntags.get(i); p = nodes.get(i); pts = [p] if p else []
        elif typ == "way":
            t = wtags.get(i); pts = wpts(i) if i in ways else []
        else:
            t = rtags.get(i); pts = []
        if t is None:
            print("   ", oid, "NOT IN OSM FILE"); continue
        allpts += pts
        keep = {k: v for k, v in t.items() if not k.startswith(("addr:city", "addr:state", "addr:postcode", "source", "gnis", "ele", "check_date"))}
        print("   ", oid, keep)
        if pts:
            c = centroid(pts); vm = vmean(pts)
            print("    osm centroid %.6f,%.6f vmean %.6f,%.6f | map pt %.6f,%.6f | d(map,centroid)=%.1f m d(map,vmean)=%.1f m" % (c[0], c[1], vm[0], vm[1], s["lat"], s["lng"], dist(c, (s["lat"], s["lng"])), dist(vm, (s["lat"], s["lng"]))))
            nin = sum(inside(*p) for p in pts)
            print("    vertices inside: %d/%d ; centroid inside: %s" % (nin, len(pts), inside(*c)))
    my = inside(s["lat"], s["lng"])
    print("    map point inside (recomputed): %s  signed edge dist %.1f m  flag %s %s" % (my, sd(s["lat"], s["lng"]), s["inside"], "OK" if my == s["inside"] else "MISMATCH"))
print("\n=== BUS STOPS ===")
cand = []
for i, t in ntags.items():
    if t.get("highway") == "bus_stop" or t.get("public_transport") in ("platform", "stop_position") or t.get("bus") == "yes" or t.get("amenity") == "bus_station":
        lat, lng = nodes[i]
        cand.append((i, t, lat, lng, inside(lat, lng), sd(lat, lng)))
for w, t in wtags.items():
    if t.get("highway") == "bus_stop" or t.get("public_transport") == "platform" or t.get("amenity") == "bus_station":
        print("  WAY bus feature", w, t)
for c in sorted(cand, key=lambda c: -c[5]):
    i, t, lat, lng, ins, d = c
    if d > -150:
        print("  node %s %s sd=%.0f m | %s" % (i, "IN " if ins else "out", d, {k: v for k, v in t.items() if k in ("name", "ref", "highway", "public_transport", "bus", "shelter", "bench")}))
mapped = {(round(b["lat"], 7), round(b["lng"], 7)) for b in D["busStops"]}
print("map bus stops", len(D["busStops"]), "unique coords", len(mapped), "unique names", len({b["name"] for b in D["busStops"]}), "unique refs", len({b["ref"] for b in D["busStops"]}))
inside_plat = [c for c in cand if c[4] and c[1].get("highway") == "bus_stop"]
inside_anyplat = [c for c in cand if c[4] and (c[1].get("highway") == "bus_stop" or c[1].get("public_transport") == "platform")]
print("inside highway=bus_stop:", len(inside_plat), " inside bus_stop-or-platform:", len(inside_anyplat))
for c in inside_anyplat:
    hit = (round(c[2], 7), round(c[3], 7)) in mapped
    print("   ", c[0], c[1].get("name"), c[1].get("ref"), "on map" if hit else "MISSING")
for b in D["busStops"]:
    m = [c for c in cand if abs(c[2] - b["lat"]) < 1e-7 and abs(c[3] - b["lng"]) < 1e-7]
    print("  map stop", b["name"], b["ref"], "-> osm", [(c[0], c[1].get("name"), c[1].get("ref"), c[1].get("public_transport")) for c in m], "inside", inside(b["lat"], b["lng"]), "sd %.0f" % sd(b["lat"], b["lng"]))
json.dump({"nodes_n": len(nodes)}, open(DATA + ".meta", "w"))
