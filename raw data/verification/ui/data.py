import re,sys,json,collections
t=open(sys.argv[1]).read()
def lit(name): return json.loads(re.search(r"const "+name+r" = (.*?);\n",t,re.S).group(1))
sv=lit("services"); bus=lit("busStops"); zr=lit("zoneRings")
COLORS=["Health & social services","Government & courts","Education","Places of worship","Recreation & parks","Banking & finance","Arts & culture"]
ICONS=re.findall(r"^\s+(\w+): `<svg",t,re.M)
print("n services",len(sv),"inside",sum(s["inside"] for s in sv),"bus",len(bus),"rings",len(zr),[len(r) for r in zr])
print("ICONS keys",ICONS)
for s in sorted(sv,key=lambda s:(s["cat"],s["name"])):
    print(f'{s["cat"][:22]:22} {s["icon"]:8} {s["name"][:55]:55} note={s.get("note")!r} inside={s["inside"]} {s["osm"]}')
print(collections.Counter(s["cat"] for s in sv))
print("cats not in COLORS:",[s["name"] for s in sv if s["cat"] not in COLORS])
print("icons not in ICONS:",[s["name"] for s in sv if s["icon"] not in ICONS])
print("used icons", sorted(set(s["icon"] for s in sv)))
print("keys present", sorted(set(k for s in sv for k in s)))
for b in bus: print("bus", b)
lats=[p[0] for r in zr for p in r]; lngs=[p[1] for r in zr for p in r]
print("zone bbox lat",min(lats),max(lats),"lng",min(lngs),max(lngs))
allp=[(s["lat"],s["lng"]) for s in sv]+[(b["lat"],b["lng"]) for b in bus]
print("items bbox lat",min(p[0] for p in allp),max(p[0] for p in allp),"lng",min(p[1] for p in allp),max(p[1] for p in allp))
