import re,sys,json,hashlib,difflib
D=sys.argv[1]
P={k:open(f"{D}/{k}.html").read() for k in ["photo-walk-map","services-along-walk","homes-and-services"]}
def lit(t,name):
    m=re.search(r"const "+name+r" = (.*?);\n",t,re.S)
    return m.group(1) if m else None
h=lambda s: hashlib.md5(s.encode()).hexdigest()[:10] if s else None
for name in ["stops","route","zoneRings","services","busStops","BLDG","BLOCKS","COLORS","ICONS","ICON_LABEL","VIEW"]:
    print(name, {k:(h(lit(t,name)), len(lit(t,name) or "")) for k,t in P.items()})
def block(t, start, end):
    i=t.find(start); j=t.find(end,i); return t[i:j]
s1=P["services-along-walk"]; s2=P["homes-and-services"]
for a,b in [('<div class="homes">','<div id="list">'),('<p class="src">','</p>'),('<p class="sub">','</p>'),('<style>','</style>'),('function declutter','map.on("zoomend", declutter)'),('const list =','function addMark'),('function addMark','function declutter')]:
    x=block(s1,a,b); y=block(s2,a,b); print(a, "identical" if x==y else "DIFF", len(x), len(y))
    if x!=y and a!='<style>':
        for l in difflib.unified_diff(x.splitlines(),y.splitlines(),lineterm="",n=0): print("   ",l[:300])
# h1/title
for k,t in P.items(): print(k, re.findall(r"<title>(.*?)</title>",t), re.findall(r"<h1>(.*?)</h1>",t))
