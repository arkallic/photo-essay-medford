# Classify every OSM building in the shaded zone using Jackson County assessor records.
# v2 fixes (from the verification pass):
#  - every MULTI-FMLY stat code (incl. two-story / basement variants 232, 242, 332, 333, 432, 434, 442, 243) is a multi-unit building
#  - each lot is judged with ALL its buildings (inside and outside the zone); only in-zone buildings are output
#  - dwelling records are paired with buildings by size (largest record <-> largest building)
#  - extra large buildings (>= 90 m2 and >= 8 m wide) on apartment lots are apartment buildings, not garages
#  - lots with no improvement records: only the largest building takes the lot's residential fallback class
#  - building point = area-weighted polygon centroid; true metres per degree at 42.325 N
# usage: python3 -I scripts/county_classify.py <raw data folder>
import json, collections, sys, math, xml.etree.ElementTree as ET
S = sys.argv[1]; C = S + "/data/jackson-county/"
KX, KY = 82427.8, 111079.6
xy = lambda lat, lng: (lng * KX, lat * KY)
BUF = 152
route = json.load(open(S + "/data/route.json")); R = [xy(*p) for p in route]

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
in_zone = lambda x, y: in_loop(x, y) or d_route(x, y) <= BUF
exec(open(S + "/scripts/zone_lib.py").read()); in_zone = in_zone_xy      # the shared zone outline (band + bulges - notches)

sc = {int(f["attributes"]["STAT_Class"]): f["attributes"]["Description"] for f in json.load(open(C + "Stat_Class.json"))["features"]}
def kind(stat):
    if stat is None: return None
    d = sc.get(stat, "")
    if stat in (137, 147, 300): return "outbuilding"          # area over garage/shop, other residential improvements
    if d in ("RESIDENCE", "MANF STRCT"): return "house"
    if d == "MULTI-FMLY": return "multi"                        # duplex .. fourplex, any level variant = one building
    if stat in (530, 531, 533, 537): return "apartment"
    if stat in (651, 652, 661, 780): return None                # yard improvements, parking, billboards, machinery
    if stat in (685, 686, 687, 688, 692): return "public"       # exempt, church, school, gov office, community bldg (owner decides which kind, below)
    return "business"
recs = collections.defaultdict(list)
for f in json.load(open(C + "improvements.json"))["features"]:
    a = f["attributes"]
    st = int(a["STATCLASS"]) if a["STATCLASS"] else None
    fp = (a["FIRSTFLOOR"] or 0) * 0.092903
    recs[a["MAPTAXLOT"]].append(dict(stat=st, kind=kind(st), fp=fp))

lots = []
for f in json.load(open(C + "taxlots.geojson"))["features"]:
    g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    rings = [[xy(p[1], p[0]) for p in poly[0]] for poly in polys]
    xs = [p[0] for r in rings for p in r]; ys = [p[1] for r in rings for p in r]
    lots.append(dict(id=f["properties"]["MAPTAXLOT"], pc=f["properties"]["PROPCLASS"] or "", rings=rings, bb=(min(xs), min(ys), max(xs), max(ys))))
def pip(x, y, ring):
    c = False
    for (ax, ay), (bx, by) in zip(ring, ring[1:]):
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax: c = not c
    return c
def find_lot(x, y):
    for l in lots:
        x0, y0, x1, y1 = l["bb"]
        if x0 <= x <= x1 and y0 <= y <= y1 and any(pip(x, y, r) for r in l["rings"]): return l
    return None

def poly_metrics(q):
    ox, oy = q[0]                                  # work relative to the first vertex (avoids float cancellation)
    A, (cx, cy) = _poly_metrics([(x - ox, y - oy) for x, y in q])
    return A, (cx + ox, cy + oy)
def _poly_metrics(q):
    A = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(q, q[1:]):
        cr = x0 * y1 - x1 * y0; A += cr; cx += (x0 + x1) * cr; cy += (y0 + y1) * cr
    A /= 2
    if abs(A) < 1e-6:
        u = q[:-1] if q[0] == q[-1] else q
        return 0.0, (sum(p[0] for p in u) / len(u), sum(p[1] for p in u) / len(u))
    return abs(A), (cx / (6 * A), cy / (6 * A))
def obb_width(q): return obb(q)[0]
def obb(q):
    best = None; ox, oy = q[0]; q = [(x - ox, y - oy) for x, y in q]
    for (ax, ay), (bx, by) in zip(q, q[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < 0.5: continue
        ux, uy = (bx - ax) / L, (by - ay) / L
        us = [x * ux + y * uy for x, y in q]; vs = [-x * uy + y * ux for x, y in q]
        w, h = max(us) - min(us), max(vs) - min(vs)
        if best is None or w * h < best[0]: best = (w * h, min(w, h), max(w, h))
    return (best[1], best[2]) if best else (0, 0)
def garage_row(b):                                  # long narrow carport / garage row
    w, l = obb(b["q"]); return w < 7 and l > 3 * w

root = ET.parse(S + "/data/openstreetmap/area.osm").getroot()
nodes = {n.get("id"): (float(n.get("lat")), float(n.get("lon"))) for n in root.iter("node")}
blds = []
for w in root.iter("way"):
    t = {x.get("k"): x.get("v") for x in w.findall("tag")}
    if "building" not in t: continue
    ll = [nodes[r.get("ref")] for r in w.findall("nd") if r.get("ref") in nodes]
    if len(ll) < 4 or ll[0] != ll[-1]: continue
    q = [xy(*p) for p in ll]
    area, (cx, cy) = poly_metrics(q)
    blds.append(dict(id=w.get("id"), pts=[[round(a, 7), round(b, 7)] for a, b in ll], q=q, a=area, c=(cx, cy), zone=in_zone(cx, cy)))
zone_lots = set()
for b in blds:
    x0, y0 = b["c"]
    if not b["zone"] and d_route(x0, y0) > BUF + 300: b["lot"] = None; continue   # far from the zone: cannot share a lot with a zone building
    l = find_lot(x0, y0); b["lot"] = l
    if b["zone"] and l: zone_lots.add(l["id"])

bylot = collections.defaultdict(list)
for b in blds:
    if b.get("lot") and b["lot"]["id"] in zone_lots: bylot[b["lot"]["id"]].append(b)
def lots_covered(b):
    xs = [p[0] for p in b["q"]]; ys = [p[1] for p in b["q"]]; hit = collections.Counter(); n = 0
    x = min(xs) + 0.5
    while x < max(xs):
        y = min(ys) + 0.5
        while y < max(ys):
            if pip(x, y, b["q"]):
                n += 1; l = find_lot(x, y)
                if l: hit[l["id"]] += 1
            y += 1.0
        x += 1.0
    return {k: v / n for k, v in hit.items()} if n else {}
FALLBACK = {"1": "house", "7": "apartment", "2": "business", "3": "business", "9": "public"}
def owner_type(pc, stats):
    """Split tax-exempt / institutional buildings by who owns or runs them (county property class + building class)."""
    if 686 in stats or (pc in ("911", "912") and not stats): return "worship"      # building coded church/temple (or a church parcel with no building record)
    if pc[:2] in ("92", "94", "95", "96", "97") or pc in ("991", "996") or 688 in stats or 687 in stats:
        return "government"                                                          # school district, city, county, state, federal, port/municipal, housing authority; gov office or school building
    return "nonprofit"                                                               # benevolent/fraternal owners (98x), church-run non-church buildings (e.g. a pantry), community buildings, other exempt
for lid, bs in bylot.items():
    lot = bs[0]["lot"]; rs = recs.get(lid, [])
    # pair by footprint; apartment (commercial) records carry no floor area, so they pair with the largest building
    dw = sorted([r for r in rs if r["kind"] in ("house", "multi", "apartment")],
                key=lambda r: -(r["fp"] if r["fp"] > 0 else (1e9 if r["kind"] == "apartment" else 0)))
    main = [r["kind"] for r in rs if r["kind"] in ("house", "multi", "apartment", "business", "public")]
    bs.sort(key=lambda b: -b["a"])
    if dw:
        apt_lot = any(r["kind"] == "apartment" for r in dw) or lot["pc"].startswith("7")
        cand = [b for b in bs if not (apt_lot and garage_row(b))] or bs     # don't hand an apartment record to a carport row
        for b in bs: b["cls"] = "outbuilding"
        for i, b in enumerate(cand[:len(dw)]):
            fp = dw[i]["fp"]; need = max(25, 0.7 * fp) if fp > 0 else 45
            if i == 0 or b["a"] >= need: b["cls"] = dw[i]["kind"]
        if apt_lot:   # extra buildings on apartment lots: big blocks, or cottage-court units (near-square, >= 55 m2, >= 7 m wide)
            for b in bs:
                if b["cls"] != "outbuilding" or garage_row(b): continue
                w, l = obb(b["q"])
                if (b["a"] >= 90 and w >= 8) or (b["a"] >= 55 and w >= 7): b["cls"] = "apartment"
    else:
        fb = not main
        top = collections.Counter(main).most_common(1)[0][0] if main else FALLBACK.get(lot["pc"][:1], "business")
        if lot["pc"].startswith("9") or top == "public": top = owner_type(lot["pc"], {r["stat"] for r in rs})
        for i, b in enumerate(bs):
            if fb and top == "apartment": b["cls"] = "apartment" if i == 0 and b["a"] >= 90 and obb_width(b["q"]) >= 8 else "outbuilding"
            elif fb and top == "house": b["cls"] = "house" if i == 0 and b["a"] >= 45 else "outbuilding"
            else: b["cls"] = top if ((i == 0 and b["a"] >= 20) or b["a"] >= 40) else "outbuilding"
dwell_lots = {k for k, v in recs.items() if any(r["kind"] in ("house", "multi") for r in v)}
for b in blds:
    if b["zone"] and b.get("cls") == "house" and b["a"] >= 150:
        cov = lots_covered(b)
        if sum(1 for k, f in cov.items() if k in dwell_lots and f >= 0.10) >= 3: b["cls"] = "multi"   # attached townhouse row
out = []
nolot = 0
for b in blds:
    if not b["zone"]: continue
    if "cls" not in b:
        nolot += 1; b["cls"] = "outbuilding" if b["a"] < 60 else "business"
    out.append(dict(id=b["id"], cls=b["cls"], a=round(b["a"], 1), c=[round(b["c"][1] / KY, 7), round(b["c"][0] / KX, 7)], pts=b["pts"], src="county" if b.get("lot") else "guess"))
cnt = collections.Counter(b["cls"] for b in out)
print("zone buildings", len(out), dict(cnt), "homes", cnt["house"] + cnt["multi"] + cnt["apartment"], "not on a lot", nolot)
json.dump(out, open(S + "/outputs/building_classes.json", "w"))
