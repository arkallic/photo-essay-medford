import sys, json, math
import xml.etree.ElementTree as ET
S, V = sys.argv[1], sys.argv[2]
exec(open(V + "/myzone.py").read())
lit = json.load(open(V + "/lits_services.json"))
ring = [P(lat, lng) for lat, lng in lit["zoneRings"][0]]
segs = list(zip(ring, ring[1:]))
def sd_page(x, y):
    d = min(segdist(x, y, a[0], a[1], b[0], b[1])[0] for a, b in segs)
    return d if pip(x, y, ring) else -d
root = ET.parse(S + "/wide/area.osm").getroot()
rows=[]
for nd in root.iter("node"):
    t = {x.get("k"): x.get("v") for x in nd.findall("tag")}
    if t.get("highway") == "bus_stop" or t.get("public_transport") == "platform":
        x, y = P(float(nd.get("lat")), float(nd.get("lon")))
        d = sd_page(x, y)
        if d > -60: rows.append((d, nd.get("id"), t.get("name"), t.get("highway"), t.get("public_transport")))
for r in sorted(rows): print("%7.1f" % r[0], r[1:])
# named amenities/offices just outside (within 25 m)
print("--- named POIs within 25 m outside the outline")
nodes = {nd.get("id"): (float(nd.get("lat")), float(nd.get("lon"))) for nd in root.iter("node")}
for el in list(root.iter("node")) + list(root.iter("way")):
    t = {x.get("k"): x.get("v") for x in el.findall("tag")}
    if not t.get("name") or not any(k in t for k in ("amenity", "office", "leisure", "shop", "government", "healthcare", "tourism")): continue
    if el.tag == "node": lat, lng = float(el.get("lat")), float(el.get("lon"))
    else:
        ll = [nodes[r.get("ref")] for r in el.findall("nd") if r.get("ref") in nodes]
        if not ll: continue
        lat = sum(p[0] for p in ll) / len(ll); lng = sum(p[1] for p in ll) / len(ll)
    d = sd_page(*P(lat, lng))
    if -25 < d < 0: print("%7.1f" % d, el.tag, el.get("id"), t.get("name"), {k: t[k] for k in ("amenity", "office", "leisure", "shop", "government", "healthcare") if k in t})
