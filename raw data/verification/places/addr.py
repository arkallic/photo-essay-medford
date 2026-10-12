import sys, math, json, xml.etree.ElementTree as ET
OSM, D = sys.argv[1], json.load(open(sys.argv[2]))
KX, KY = 82427.8, 111079.6
ring = [(lng*KX, lat*KY) for lat, lng in D["zoneRings"][0]]
def inside(lat, lng):
    x, y = lng*KX, lat*KY; c = False
    for (ax, ay), (bx, by) in zip(ring, ring[1:]+ring[:1]):
        if (ay > y) != (by > y) and x < (bx-ax)*(y-ay)/(by-ay)+ax: c = not c
    return c
root = ET.parse(OSM).getroot(); nodes = {}
def tg(el): return {t.get("k"): t.get("v") for t in el.findall("tag")}
for n in root.iter("node"): nodes[n.get("id")] = (float(n.get("lat")), float(n.get("lon")))
for el in list(root.iter("node")) + list(root.iter("way")):
    t = tg(el)
    st = t.get("addr:street", "")
    if any(k in st for k in sys.argv[3:]):
        if el.tag == "node": p = nodes[el.get("id")]
        else:
            pts = [nodes[r.get("ref")] for r in el.findall("nd") if r.get("ref") in nodes]; q = pts[:-1]
            p = (sum(a[0] for a in q)/len(q), sum(a[1] for a in q)/len(q))
        print(el.tag, el.get("id"), t.get("addr:housenumber"), st, "%.6f,%.6f" % p, "in" if inside(*p) else "out", t.get("name"))
for w in root.iter("way"):
    t = tg(w)
    if t.get("highway") and t.get("name") in ("West 8th Street", "West 6th Street", "South Grape Street", "South Holly Street", "South Fir Street"):
        pts = [nodes[r.get("ref")] for r in w.findall("nd") if r.get("ref") in nodes]
        print("street", t.get("name"), w.get("id"), [("%.5f,%.5f" % p) for p in pts[:: max(1, len(pts)//4)]])
