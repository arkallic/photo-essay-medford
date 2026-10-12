import json, math, sys, xml.etree.ElementTree as ET
OSM = sys.argv[1]; lat0, lng0, R = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
KX, KY = 82427.8, 111079.6
root = ET.parse(OSM).getroot()
nodes = {}; ntags = {}
def tg(el): return {t.get("k"): t.get("v") for t in el.findall("tag")}
for n in root.iter("node"):
    nodes[n.get("id")] = (float(n.get("lat")), float(n.get("lon"))); ntags[n.get("id")] = tg(n)
def d(p): return math.hypot((p[1] - lng0) * KX, (p[0] - lat0) * KY)
for i, t in ntags.items():
    if t and d(nodes[i]) < R: print("node", i, round(d(nodes[i])), t)
for w in root.iter("way"):
    t = tg(w); pts = [nodes[r.get("ref")] for r in w.findall("nd") if r.get("ref") in nodes]
    if not pts: continue
    if t.get("highway"):
        md = min(d(p) for p in pts)
        if md < R: print("street", w.get("id"), t.get("name"), t.get("highway"), "min d", round(md), "lng range %.5f..%.5f lat %.5f..%.5f" % (min(p[1] for p in pts), max(p[1] for p in pts), min(p[0] for p in pts), max(p[0] for p in pts)))
        continue
    q = pts[:-1] if pts[0] == pts[-1] and len(pts) > 1 else pts
    c = (sum(p[0] for p in q) / len(q), sum(p[1] for p in q) / len(q))
    if d(c) < R and t: print("way", w.get("id"), round(d(c)), "%.6f,%.6f" % c, {k: v for k, v in t.items() if k not in ("source",)})
for r in root.iter("relation"):
    t = tg(r)
    for m in r.findall("member"):
        if m.get("ref") in sys.argv[5:]: print("relation", r.get("id"), "has member", m.get("type"), m.get("ref"), m.get("role"), t)
