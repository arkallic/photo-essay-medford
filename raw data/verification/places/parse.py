import json, re, sys
M = sys.argv[1]
OUT = sys.argv[2]
def grab(html, name):
    m = re.search(r"const %s = (\[.*?\]);\n" % name, html, re.S)
    return json.loads(m.group(1))
res = {}
for f in ("services-along-walk.html", "homes-and-services.html"):
    h = open(M + "/" + f).read()
    res[f] = {k: grab(h, k) for k in ("services", "busStops", "zoneRings", "route")}
a, b = res["services-along-walk.html"], res["homes-and-services.html"]
for k in a:
    print(k, "match" if a[k] == b[k] else "DIFFER", len(a[k]))
json.dump(a, open(OUT, "w"), indent=1)
# photo map: check zone/route
h = open(M + "/photo-walk-map.html").read()
m = re.search(r"const route = (\[.*?\]);\n", h, re.S)
print("photo route same:", m and json.loads(m.group(1)) == a["route"])
sv = a["services"]
print("n services", len(sv))
keys = set()
for s in sv: keys |= set(s)
print("keys", sorted(keys))
for s in sorted(sv, key=lambda s: (s["cat"], s["name"])):
    print(f'{s["cat"][:22]:22} | {s["icon"]:7} | {s["name"][:48]:48} | {s.get("note")!s:30} | {s["osm"]:28} | {s["lat"]},{s["lng"]} | inside={s["inside"]} | type={s.get("type")} | kind={s.get("kind")}')
print()
for bs in a["busStops"]: print(bs)
