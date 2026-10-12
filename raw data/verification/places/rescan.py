import json, math, sys, xml.etree.ElementTree as ET
OSM, DATA = sys.argv[1], sys.argv[2]
D = json.load(open(DATA))
KX, KY = 82427.8, 111079.6
ring = [(lng * KX, lat * KY) for lat, lng in D["zoneRings"][0]]
ring = ring + ring[:1]
def inside(lat, lng):
    x, y = lng * KX, lat * KY; c = False
    for (ax, ay), (bx, by) in zip(ring, ring[1:]):
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax: c = not c
    return c
def dseg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)
def sd(lat, lng):
    x, y = lng * KX, lat * KY
    e = min(dseg(x, y, *a, *b) for a, b in zip(ring, ring[1:]))
    return e if inside(lat, lng) else -e
root = ET.parse(OSM).getroot()
nodes = {}; feats = []
def tg(el): return {t.get("k"): t.get("v") for t in el.findall("tag")}
for n in root.iter("node"): nodes[n.get("id")] = (float(n.get("lat")), float(n.get("lon")))
wayp = {}
for n in root.iter("node"):
    t = tg(n)
    if t: feats.append(("node/" + n.get("id"), t, [nodes[n.get("id")]]))
for w in root.iter("way"):
    pts = [nodes[r.get("ref")] for r in w.findall("nd") if r.get("ref") in nodes]; wayp[w.get("id")] = pts
    t = tg(w)
    if t and pts: feats.append(("way/" + w.get("id"), t, pts))
for r in root.iter("relation"):
    t = tg(r); pts = [p for m in r.findall("member") if m.get("type") == "way" for p in wayp.get(m.get("ref"), [])]
    if t and pts: feats.append(("relation/" + r.get("id"), t, pts))
mapped = set()
for s in D["services"]:
    for o in s["osm"].split("+"): mapped.add(o)
mapped.add("relation/5318728")  # field & track multipolygon (outer way on map)
SKIPK = ("highway", "route", "boundary", "public_transport", "railway", "waterway", "power", "type", "natural", "barrier", "crossing", "traffic_signals")
POI = ("amenity", "shop", "office", "healthcare", "craft", "tourism", "leisure", "emergency", "historic", "club", "social_facility", "government", "man_made", "landuse")
rows = []
for oid, t, pts in feats:
    if oid in mapped: continue
    named = "name" in t
    poi = any(k in t for k in POI)
    if not (named or poi): continue
    if t.get("highway") or t.get("route") or t.get("boundary") or t.get("public_transport") or t.get("railway") or t.get("waterway"): continue
    q = pts[:-1] if len(pts) > 1 and pts[0] == pts[-1] else pts
    c = (sum(p[0] for p in q) / len(q), sum(p[1] for p in q) / len(q))
    nin = sum(inside(*p) for p in q)
    if nin == 0 and not inside(*c): continue
    rows.append((oid, "%.6f,%.6f" % c, round(sd(*c)), f"{nin}/{len(q)}", {k: v for k, v in t.items() if not k.startswith(("addr:city", "addr:state", "addr:postcode", "source", "check_date", "gnis", "ele", "capacity", "surface", "building:levels", "roof", "height"))}))
named = [r for r in rows if "name" in r[4]]
unnamed = [r for r in rows if "name" not in r[4]]
print("NAMED, not on map, centroid or vertex inside zone:", len(named))
for r in sorted(named, key=lambda r: r[4].get("name")): print(" ", r[0], r[1], "sd", r[2], "vin", r[3], r[4])
print("\nUNNAMED POI-tagged inside (summary by main tag):")
import collections
cnt = collections.Counter()
for r in unnamed:
    k = next((f"{k}={r[4][k]}" for k in POI if k in r[4]), "?")
    cnt[k] += 1
for k, v in cnt.most_common(): print("  ", v, k)
print("\nUNNAMED non-parking/non-landuse POIs:")
for r in unnamed:
    t = r[4]
    if t.get("amenity") in ("parking", "parking_space", "bench", "waste_basket", "bicycle_parking", "parking_entrance", "fire_hydrant", "post_box", "drinking_water") : continue
    if "landuse" in t and len(t) <= 2: continue
    if t.get("leisure") in ("pitch", "playground", "garden", "picnic_table", "swimming_pool"): continue
    if t.get("man_made") in ("street_cabinet", "manhole", "utility_pole", "flagpole", "surveillance"): continue
    print(" ", r[0], r[1], "sd", r[2], r[4])
