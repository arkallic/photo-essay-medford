# Targets, notched houses, buildings cut out by notches / added by bulges, near-edge items.
import sys, json, math, collections
import xml.etree.ElementTree as ET
S, V = sys.argv[1], sys.argv[2]
exec(open(V + "/myzone.py").read())
lit = json.load(open(V + "/lits_services.json")); lith = json.load(open(V + "/lits_homes.json"))
ring = [P(lat, lng) for lat, lng in lit["zoneRings"][0]]
segs = list(zip(ring, ring[1:]))
def sd_page(x, y):   # + inside, - outside (distance to page outline)
    d = min(segdist(x, y, a[0], a[1], b[0], b[1])[0] for a, b in segs)
    return d if pip(x, y, ring) else -d
def why(x, y):
    w = []
    if pip(x, y, RP): w.append("loop")
    elif droute(x, y) <= BUF: w.append("band(%.1f)" % (BUF - droute(x, y)))
    for k, b in enumerate(BULGES):
        if in_bulge(x, y, b): w.append("bulge%d" % (k + 1))
    for k, nt in enumerate(NOTCHES):
        if math.dist((x, y), nt["c"]) < nt["r"]: w.append("NOTCH%d" % (k + 1))
    return ",".join(w) or "-"

print("== bulge targets (cfg) : signed dist to page outline / to my exact boundary, end-disk margin")
for k, b in enumerate(BULGES):
    for t in b["tg"]:
        print("  bulge%d target" % (k + 1), LL(*t), "page %.1f m" % sd_page(*t), "| inside end disk by %.1f m" % (b["rend"] - math.dist(t, b["T"])), "| why", why(*t))
print("== services / bus stops: signed dist to page outline (sorted)")
rows = []
for s in lit["services"]:
    x, y = P(s["lat"], s["lng"]); rows.append((sd_page(x, y), "svc", s["name"], why(x, y), in_zone_mine(x, y), s.get("inside")))
for s in lit["busStops"]:
    x, y = P(s["lat"], s["lng"]); rows.append((sd_page(x, y), "bus", s["name"], why(x, y), in_zone_mine(x, y), None))
for r in sorted(rows): print("  %7.1f m  %s  %-50s %-22s mine=%s flag=%s" % r)
# compare cfg targets with page positions
nm = {s["name"]: s for s in lit["services"]}; nb = {s["name"]: s for s in lit["busStops"]}
for name, src in [("Southern Oregon Education Service District", nm), ("Historic Holly Theater", nm), ("Medford Police", nm), ("Station 71five community center", nm), ("W 8th St - East of Lincoln St", nb)]:
    s = src[name]; p = P(s["lat"], s["lng"])
    dmin = min(math.dist(p, t) for b in BULGES for t in b["tg"])
    print("  page pos of %-45s vs nearest cfg target: %.2f m" % (name, dmin))

# --- OSM buildings ---
root = ET.parse(S + "/wide/area.osm").getroot()
nodes = {n.get("id"): (float(n.get("lat")), float(n.get("lon"))) for n in root.iter("node")}
def centroid(q):
    ox, oy = q[0]; A = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(q, q[1:]):
        x0 -= ox; y0 -= oy; x1 -= ox; y1 -= oy
        cr = x0 * y1 - x1 * y0; A += cr; cx += (x0 + x1) * cr; cy += (y0 + y1) * cr
    A /= 2
    if abs(A) < 1e-9: return 0, (sum(p[0] for p in q) / len(q), sum(p[1] for p in q) / len(q))
    return abs(A), (cx / (6 * A) + ox, cy / (6 * A) + oy)
blds = []
for w in root.iter("way"):
    t = {x.get("k"): x.get("v") for x in w.findall("tag")}
    if "building" not in t: continue
    ll = [nodes[r.get("ref")] for r in w.findall("nd") if r.get("ref") in nodes]
    if len(ll) < 4 or ll[0] != ll[-1]: continue
    q = [P(*p) for p in ll]; A, c = centroid(q)
    blds.append(dict(id=w.get("id"), tags=t, q=q, A=A, c=c))
print("== OSM buildings:", len(blds))
cls = {b["id"]: b["cls"] for b in json.load(open(S + "/site/bclass_county.json"))}
for k, nt in enumerate(NOTCHES):
    wid = nt["name"].split("(")[-1].rstrip(")")
    b = [b for b in blds if b["id"] == wid][0]
    x, y = b["c"]
    fo = sum(1 for p in b["q"][:-1] if not pip(p[0], p[1], ring))
    print("  notch%d way %s: centroid" % (k + 1, wid), LL(x, y), "cfg pt off by %.2f m" % math.dist((x, y), nt["c"]),
          "| page sd %.1f m | in base zone (no notch): %s depth %.1f | footprint vertices outside page: %d/%d | tags %s | area %.0f m2 | in page BLDG list: %s" %
          (sd_page(x, y), in_base(x, y), BUF - droute(x, y), fo, len(b["q"]) - 1, b["tags"].get("building"), b["A"], wid in cls))
# flips caused by notches / bulges
cut, added, edge = [], [], []
for b in blds:
    x, y = b["c"]
    if abs(x - RP[0][0]) > 1500 or abs(y - RP[0][1]) > 1500: continue
    base_nb = in_base(x, y, use_bulges=False); base = in_base(x, y); mine = in_zone_mine(x, y); pg = pip(x, y, ring)
    if base and not pg: cut.append(b)
    if pg and not base_nb: added.append(b)
    if mine != pg: edge.append((b, sd_page(x, y)))
    b["pg"] = pg
print("== buildings with centroid in the un-notched zone but outside the page outline:", len(cut))
for b in cut: print("   way", b["id"], LL(*b["c"]), b["tags"].get("building"), "%.0f m2" % b["A"], why(*b["c"]), "page sd %.1f" % sd_page(*b["c"]))
print("== buildings inside page outline only thanks to bulges:", len(added), collections.Counter(cls.get(b["id"], "?") for b in added))
for b in added: print("   way", b["id"], cls.get(b["id"], "?"), b["tags"].get("building"), "%.0f m2" % b["A"], why(*b["c"]))
print("== buildings where my exact zone and page outline disagree:", len(edge))
for b, d in edge: print("   way", b["id"], cls.get(b["id"], "?"), "page sd %.2f" % d, why(*b["c"]))
# page BLDG consistency: every BLDG entry centroid inside page outline; all in-page OSM buildings in BLDG?
inpage = {b["id"] for b in blds if b.get("pg")}
print("== OSM buildings with centroid inside page outline:", len(inpage), "| bclass_county entries:", len(cls), "| missing from bclass:", len(inpage - set(cls)), "| bclass not inside:", len(set(cls) - inpage))
print("   missing:", [(i, [b["tags"].get("building") for b in blds if b["id"] == i][0]) for i in sorted(inpage - set(cls))][:20])
print("   not inside:", sorted(set(cls) - inpage)[:20])
# buildings near the page edge (centroid within 3 m)
near = sorted([(abs(sd_page(*b["c"])), b["id"], cls.get(b["id"], "out"), sd_page(*b["c"])) for b in blds if abs(b["c"][0] - RP[0][0]) < 1500 and abs(sd_page(*b["c"])) < 3])
print("== building centroids within 3 m of the outline:", [(i, c, round(s, 2)) for _, i, c, s in near])
json.dump([dict(id=b["id"], c=b["c"], A=b["A"], tag=b["tags"].get("building")) for b in cut], open(V + "/cut.json", "w"))
