import xml.etree.ElementTree as ET, json, math, sys
S=sys.argv[1]; BUF=152
exec(open(S+"/scripts/zone_lib.py").read())   # shared zone outline
route=json.load(open(S+"/data/route.json"))
root=ET.parse(S+"/data/openstreetmap/area.osm").getroot()
nodes={}; feats=[]
KEYS=("amenity","shop","office","healthcare","craft","tourism","leisure","emergency")
SKIP_AMEN={"bench","waste_basket","parking_space","bicycle_parking","parking_entrance","vending_machine","drinking_water","post_box","fire_hydrant","recycling","shelter","waste_disposal","motorcycle_parking","grit_bin","clock","loading_dock","telephone"}
for n in root.iter("node"):
    nodes[n.get("id")]=(float(n.get("lat")),float(n.get("lon")))
def tags(el): return {t.get("k"):t.get("v") for t in el.findall("tag")}
for n in root.iter("node"):
    t=tags(n)
    if any(k in t for k in KEYS): feats.append(("node",n.get("id"),nodes[n.get("id")],t,[nodes[n.get("id")]]))
for w in root.iter("way"):
    t=tags(w)
    if any(k in t for k in KEYS):
        pts=[nodes[r.get("ref")] for r in w.findall("nd") if r.get("ref") in nodes]
        if pts: feats.append(("way",w.get("id"),(sum(p[0] for p in pts)/len(pts),sum(p[1] for p in pts)/len(pts)),t,pts))
ways={w.get("id"):[nodes[r.get("ref")] for r in w.findall("nd") if r.get("ref") in nodes] for w in root.iter("way")}
for r in root.iter("relation"):
    t=tags(r)
    if any(k in t for k in KEYS):
        pts=[p for m in r.findall("member") if m.get("type")=="way" for p in ways.get(m.get("ref"),[])]
        if pts: feats.append(("relation",r.get("id"),(sum(p[0] for p in pts)/len(pts),sum(p[1] for p in pts)/len(pts)),t,pts))
lat0=math.radians(42.325)
def xy(p): return (p[1]*82427.8, p[0]*111079.6)
def dseg(p,a,b):
    (px,py),(ax,ay),(bx,by)=xy(p),xy(a),xy(b)
    dx,dy=bx-ax,by-ay; L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,((px-ax)*dx+(py-ay)*dy)/L))
    return math.hypot(px-ax-t*dx,py-ay-t*dy)
FORCE={"204768006":"amenity=townhall","429478438":"office=employment","198250488":"leisure=park","953191898":"healthcare=yes","954466806":"building=church"}
for w in root.iter("way"):
    if w.get("id") in FORCE and not any(f[1]==w.get("id") for f in feats):
        pts=[nodes[r.get("ref")] for r in w.findall("nd") if r.get("ref") in nodes]
        feats.append(("way",w.get("id"),(sum(p[0] for p in pts)/len(pts),sum(p[1] for p in pts)/len(pts)),tags(w),pts))
out=[]
for typ,i,p,t,pts in feats:
    d=min(dseg(q,route[k],route[k+1]) for q in pts for k in range(len(route)-1))
    if not in_zone(*p) and i not in FORCE: continue
    if t.get("amenity") in SKIP_AMEN and "name" not in t: continue
    if t.get("leisure") in ("pitch","playground","garden","picnic_table","swimming_pool","fitness_station") and "name" not in t: continue
    kind=FORCE.get(i) or next(f"{k}={t[k]}" for k in KEYS if k in t)
    addr=" ".join(x for x in (t.get("addr:housenumber"),t.get("addr:street")) if x)
    out.append(dict(name=t.get("name"),kind=kind,lat=round(p[0],6),lng=round(p[1],6),dist=round(d),addr=addr,osm=f"{typ}/{i}",
        phone=t.get("phone") or t.get("contact:phone"),web=t.get("website") or t.get("contact:website"),hours=t.get("opening_hours")))
bus=[]
for n in root.iter("node"):
    t=tags(n)
    if t.get("highway")=="bus_stop" and t.get("public_transport")=="platform":
        p=nodes[n.get("id")]; d=min(dseg(p,route[k],route[k+1]) for k in range(len(route)-1))
        if in_zone(*p): bus.append(dict(name=t.get("name"),ref=t.get("ref"),lat=p[0],lng=p[1],dist=round(d)))
json.dump(bus,open(S+"/outputs/bus_stops.json","w"),indent=1); print("bus",len(bus))
json.dump(out,open(S+"/outputs/places_found.json","w"),indent=1)
for o in sorted(out,key=lambda o:o["kind"]): print(o["dist"],"m |",o["kind"],"|",o["name"],"|",o["addr"])
print(len(out))
