import json, re, sys
S=sys.argv[1]
import base64
# photo pins: photos/photos.json + the six metadata-free images in photos/
_P=json.load(open(S+"/data/photos/photos.json"))["photos"]
stops="const stops = [\n" + "\n".join(
    f'    {{ n:{p["n"]}, lat:{p["lat"]}, lng:{p["lng"]}, time:"{p["time"]}", src:"data:image/jpeg;base64,{base64.b64encode(open(S+"/data/photos/"+p["image"],"rb").read()).decode()}", file:"{p["original_file"]}" }},'
    for p in _P) + "\n  ];"
route=json.load(open(S+"/data/route.json"))
CAT={"amenity=restaurant":"Food & drink","amenity=doctors":"Health & social services","amenity=social_facility":"Health & social services",
 "amenity=courthouse":"Government & courts","office=government":"Government & courts","amenity=prison":"Government & courts",
 "amenity=school":"Education","amenity=college":"Education","amenity=place_of_worship":"Places of worship",
 "leisure=sports_centre":"Recreation & parks","leisure=park":"Recreation & parks","amenity=fountain":"Recreation & parks","amenity=townhall":"Government & courts","office=employment":"Government & courts","leisure=park":"Recreation & parks","healthcare=yes":"Health & social services","building=church":"Places of worship","amenity=police":"Government & courts"}
LABEL={"amenity=restaurant":"Restaurant","amenity=doctors":"Medical clinic","amenity=social_facility":"Food pantry","amenity=courthouse":"Courthouse",
 "office=government":"Government office","amenity=prison":"County jail","amenity=school":"Middle school","amenity=college":"College",
 "amenity=place_of_worship":"Church","leisure=sports_centre":"Fitness / community center","leisure=park":"Park","amenity=fountain":"Fountain","amenity=townhall":"City hall","office=employment":"Employment office","healthcare=yes":"Public health & social services","building=church":"Church","amenity=police":"Police station"}
DROP={"amenity=fountain","amenity=restaurant","amenity=prison","amenity=college"}
sv=[s for s in json.load(open(S+"/outputs/places_found.json")) if s["kind"] in CAT and s["kind"] not in DROP]
for s in sv:
    s["cat"]=CAT[s["kind"]]; s["type"]=LABEL[s["kind"]]
    if not s["name"]: s["name"]=s["type"]
for s in sv:
    if s["osm"]=="way/954473298":
        s["note"]="also election office / ballot drop box"
    if s["osm"]=="way/954473298":  # same building also hosts the election office (per user; not in OSM)
        s["type"]="Government office · Election office / ballot drop box"
ICON={"amenity=place_of_worship":"cross","building=church":"cross","office=government":"gov","amenity=townhall":"gov",
 "office=employment":"gov","amenity=courthouse":"scales","leisure=sports_centre":"run","leisure=park":"tree","healthcare=yes":"gov","amenity=doctors":"medical","amenity=school":"school","amenity=social_facility":"apple","amenity=police":"shield"}
import math
def _dist(lat,lng):
    lat0=math.radians(42.325); xy=lambda p:(p[1]*82427.8,p[0]*111079.6); best=1e9
    for k in range(len(route)-1):
        (px,py),(ax,ay),(bx,by)=xy((lat,lng)),xy(route[k]),xy(route[k+1]); dx,dy=bx-ax,by-ay; L=dx*dx+dy*dy
        t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/L)) if L else 0; best=min(best,math.hypot(px-ax-t*dx,py-ay-t*dy))
    return best
# Added on request (centroids from OSM way 953191379 and way 953191389)
for e in [dict(name="First Presbyterian Church",kind="amenity=place_of_worship",cat="Places of worship",type="Church",lat=42.324193,lng=-122.874986,addr="85 South Holly Street",osm="way/953191379"),
          dict(name="Bank of America",kind="amenity=bank",cat="Banking",type="Bank",lat=42.324935,lng=-122.875929,addr="",osm="way/953191389"),
          dict(name="Christ Unity Church",kind="amenity=place_of_worship",cat="Places of worship",type="Church",lat=42.329574,lng=-122.87985,addr="",osm="way/953205274")]:
    e.update(dist=_dist(e["lat"],e["lng"]),phone=None,web=None,hours=None); sv.append(e)
ICON["amenity=bank"]="money"
# Named services visible in the user's chosen map view (outside the shaded band is fine)
for e in json.load(open(S+"/settings/extra_places.json")):
    e["dist"]=_dist(e["lat"],e["lng"]); sv.append(e)
import re as _re
_seen_id=set(); _seen_nm=set(); _dedup=[]
for s in sorted(sv, key=lambda s: 0 if s["kind"]=="view" or s["osm"] in ("way/953191379","way/953191389","way/953205274") else 1):
    nk=_re.sub(r"[^a-z]","",s["name"].lower().replace(" church",""))
    if s["osm"] in _seen_id or nk in _seen_nm: continue
    _seen_id.add(s["osm"]); _seen_nm.add(nk); _dedup.append(s)
sv=_dedup
for s in sv: s["icon"]=s.get("icon") or ICON.get(s["kind"])
for s in sv:
    if s["name"]=="First Presbyterian": s["name"]="First Presbyterian Church"
for s in sv:
    if s["osm"]=="node/966179963":  # per user: this is the county jail, with a small sheriff's office staff
        s["name"]="Jackson County Jail"; s["type"]="County jail (with some sheriff's office staff)"; s["note"]="some sheriff's staff"
        s.update(addr="787 West 8th Street", phone="+1-541-774-6800", web=None)   # OSM's jail URL now redirects to the county home page
    if s["name"]=="Medford Police": s["web"]=None   # OSM link points to a retired city URL
_DAYS={"Mo":"Mon","Tu":"Tue","We":"Wed","Th":"Thu","Fr":"Fri","Sa":"Sat","Su":"Sun"}
def _t(hm):
    h,m=map(int,hm.split(":")); ap="am" if h<12 else "pm"; h=h%12 or 12
    return f"{h}{':%02d'%m if m else ''}{ap}"
def _hours(v):
    if not v: return v
    out=[]
    for part in re.split(r";\s*", v):
        mm=re.match(r"^(?:([A-Z][a-z](?:-[A-Z][a-z])?)\s+)?(.*)$", part.strip())
        days, times = mm.group(1), mm.group(2)
        dd = "–".join(_DAYS.get(d,d) for d in days.split("-")) if days else ""
        tt = ", ".join("–".join(_t(x) for x in rng.split("-")) for rng in times.split(","))
        out.append((dd+" " if dd else "")+tt)
    return "; ".join(out).replace("; ", ", ") if all(not re.match(r"[A-Z]",p.strip()) for p in v.split(";")[1:]) else "; ".join(out)
for s in sv:
    s["hours"]=_hours(s.get("hours"))
    if s.get("addr"): s["addr"]=re.sub(r"^(\d+);(\d+)", r"\1–\2", s["addr"])
# --- user edits (Oct 11 2026) ---
sv=[x for x in sv if x["name"]!="Randall Theater"]                                   # removed from map and counts
sv=[x for x in sv if x["osm"] not in ("way/953192627","way/953192625")]               # courthouse + offices are one complex
sv.append(dict(name="Jackson County Courthouse & County Offices",kind="merged",cat="Government & courts",type="County offices",icon="gov",
               lat=42.322976,lng=-122.877805,addr="",osm="way/953192627+way/953192625",phone=None,web=None,hours=None))
sv.append(dict(name="Old Medford Public Library",kind="building=library",cat="Arts & culture",type="Historic library building",icon="book",
               note="historic building",lat=42.323578,lng=-122.876807,addr="413 West Main Street",osm="way/224277673",phone=None,web=None,hours=None))
sv.append(dict(name="McLoughlin field & track",kind="leisure=track",cat="Recreation & parks",type="School field & running track",icon="track",
               note="public use",lat=42.329161,lng=-122.883025,addr="",osm="way/356319132",phone=None,web=None,hours=None))
sv.append(dict(name="Lausmann Annex",kind="building",cat="Government & courts",type="City of Medford offices",icon="gov",
               note="City of Medford offices",lat=42.321935,lng=-122.875125,addr="200 South Ivy Street",osm="way/224277672",phone=None,web=None,hours=None))
for x in sv:
    if x["cat"]=="Banking": x["cat"]="Banking & finance"
# website links checked Oct 11 2026: fix moved ones, drop ones that now only redirect to a home page
_WEB={"https://firstpreschurchmedford.com/":"https://www.firstpreschurchmedford.org/",
      "https://courts.oregon.gov/jackson/Pages/index.aspx":"https://www.courts.oregon.gov/courts/jackson/Pages/default.aspx",
      "https://jacksoncountyor.org/community-justice":None}
for s_ in sv:
    if s_.get("web") in _WEB: s_["web"]=_WEB[s_["web"]]
BUF=152  # shaded band, metres each side of the path
# Inside/outside the shaded area (loop interior or within BUF m of the path), same rule as the stats
exec(open(S+"/scripts/zone_lib.py").read())   # shared zone outline (band + local bulges - notches)
def _inside(lat,lng): return in_zone(lat,lng)
def _inside_old(lat,lng):
    lat0=math.radians(42.325); xy=lambda p:(p[1]*82427.8,p[0]*111079.6)
    R=[xy(p) for p in route]; x,y=xy((lat,lng)); c=False
    for (ax,ay),(bx,by) in zip(R,R[1:]):
        if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax: c=not c
    return c or _dist(lat,lng)<=BUF
for s in sv: s["inside"]=_inside(s["lat"],s["lng"])
print("inside",sum(s["inside"] for s in sv),"outside",sum(not s["inside"] for s in sv))
# distances were only used to decide inside/outside; keep them out of the page
_bus=json.load(open(S+"/outputs/bus_stops.json"))
for x in sv+_bus: x.pop("dist",None)
html=open(S+"/settings/page_template.html").read().replace("/*STOPS*/",stops).replace("/*ROUTE*/",json.dumps(route)).replace("/*ZONE*/",json.dumps(json.load(open(S+"/outputs/zone.json"))["rings"])).replace("/*SERVICES*/",json.dumps(sv)).replace("/*BUS*/",json.dumps(_bus))
import os; os.makedirs(S+"/build", exist_ok=True)
open(S+"/build/services-along-walk.html","w").write(html)   # temporary in-between page; build_bldg.py builds the final map on it, then removes it
print(len(sv))
