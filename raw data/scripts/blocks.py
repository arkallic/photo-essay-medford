# Group counted homes into street blocks and write label positions/counts.
import xml.etree.ElementTree as ET, json, math, sys, collections
S=sys.argv[1]; root=ET.parse(S+"/data/openstreetmap/area.osm").getroot()
nodes={n.get("id"):(float(n.get("lat")),float(n.get("lon"))) for n in root.iter("node")}
lat0=math.radians(42.325); xy=lambda p:(p[1]*82427.8,p[0]*111079.6)
ROAD={"primary","secondary","tertiary","residential","unclassified","living_street","primary_link","secondary_link","tertiary_link"}
segs=[]; deg=collections.Counter(); ends=[]
for w in root.iter("way"):
    t={x.get("k"):x.get("v") for x in w.findall("tag")}
    if t.get("highway") in ROAD:
        ids=[r.get("ref") for r in w.findall("nd") if r.get("ref") in nodes]
        P=[xy(nodes[i]) for i in ids]
        segs+=list(zip(P,P[1:]))
        for i in ids: deg[i]+=1
        if t.get("name") and len(ids)>1: ends+=[(ids[0],ids[1]),(ids[-1],ids[-2])]
def ray_hit(o,d,maxlen=120):   # first road segment hit by a ray from o in direction d
    best=None
    for p,q in segs:
        ex,ey=q[0]-p[0],q[1]-p[1]; den=d[0]*ey-d[1]*ex
        if abs(den)<1e-9: continue
        t=((p[0]-o[0])*ey-(p[1]-o[1])*ex)/den; u=((p[0]-o[0])*d[1]-(p[1]-o[1])*d[0])/den
        if 1e-6<t<=maxlen and 0<=u<=1 and (best is None or t<best): best=t
    return best
# a named street that dead-ends still divides blocks: extend each dead end straight on to the next road (<= 120 m), else 60 m
ext=0
for e,prev in ends:
    if deg[e]!=1: continue
    a,b=xy(nodes[prev]),xy(nodes[e]); L=math.dist(a,b)
    if L<1: continue
    d=((b[0]-a[0])/L,(b[1]-a[1])/L); t=ray_hit(b,d)
    t=t or 60                          # no road ahead (e.g. ends at a school field): still split the block 60 m past the end
    segs.append((b,(b[0]+d[0]*t,b[1]+d[1]*t))); ext+=1
print("dead-end streets extended:",ext)
def cross(a,b,c,d):
    o=lambda p,q,r:(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    return o(a,b,c)*o(a,b,d)<0 and o(c,d,a)*o(c,d,b)<0
B=[b for b in json.load(open(S+"/outputs/building_classes.json")) if b["cls"] in ("house","multi","apartment")]
for b in B:
    c=tuple(b["c"]); b["ll"]=c; b["xy"]=xy(c)   # area-weighted centroid (same point used for the zone test)
    b["k"]="house" if b["cls"]=="house" else "apt"
par=list(range(len(B)))
def f(i):
    while par[i]!=i: par[i]=par[par[i]]; i=par[i]
    return i
for i in range(len(B)):
    for j in range(i+1,len(B)):
        a,c=B[i]["xy"],B[j]["xy"]
        if math.dist(a,c)<70:
            mn=(min(a[0],c[0]),min(a[1],c[1])); mx=(max(a[0],c[0]),max(a[1],c[1]))
            if not any(cross(a,c,p,q) for p,q in segs if not (max(p[0],q[0])<mn[0] or min(p[0],q[0])>mx[0] or max(p[1],q[1])<mn[1] or min(p[1],q[1])>mx[1])):
                par[f(i)]=f(j)
groups=collections.defaultdict(list)
for i,b in enumerate(B): groups[f(i)].append(b)
out=[]
for g in groups.values():
    h=sum(b["k"]=="house" for b in g); a=sum(b["k"]=="apt" for b in g)
    out.append(dict(lat=round(sum(b["ll"][0] for b in g)/len(g),6),lng=round(sum(b["ll"][1] for b in g)/len(g),6),h=h,a=a,ids=[b["id"] for b in g]))
json.dump(out,open(S+"/outputs/block_counts.json","w"))
print("blocks",len(out),"houses",sum(o["h"] for o in out),"apts",sum(o["a"] for o in out),"sizes",sorted(o["h"] for o in out))
