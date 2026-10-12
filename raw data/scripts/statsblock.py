# Writes the stats card (summary tiles + category tiles) into settings/page_template.html.
# usage: python3 -I scripts/statsblock.py <raw data folder>
import re, json, sys
S = sys.argv[1] if len(sys.argv) > 1 else "."
d = json.load(open(S + "/outputs/stats.json")); R = {r["label"]: r for r in d["rows"]}
c = d["counts"]; st = d["streets"]
H = c["house"] + c["multi"] + c["apartment"]; acres = d["acres"]
r10 = lambda x: int(round(x, -1)) if x >= 100 else int(round(x))
order = [("All services", "Services", "all categories, not bus stops", "map icons"),
         ("Bus stops", "Bus stops", "each side of the street counts", "stops"),
         ("Government & courts", "Government & courts", "", "map icons"),
         ("Health & social services", "Health & social", "", "map icons"),
         ("Parks only", "Parks & open space", "2 parks + school field; YMCA not counted", "map icons"),
         ("Places of worship", "Places of worship", "", "map icons"),
         ("Banking", "Banking & finance", "", "map icons"),
         ("Education", "Education", "", "map icons"),
         ("Businesses", "Businesses", "yellow buildings on the map, no icons (county records); not listed below", "buildings")]
def tile(k, lab, note, unit):
    r = R[k]
    return (f'        <div class="tile"><div class="t-h">{lab}{f" <span class=t-note>{note}</span>" if note else ""}</div>'
            f'<div class="t-big">{r["n"]}<span> {unit}</span></div><div class="t-l">1 per ≈ {r["acres_each"]:.0f} acres<br>≈ {r10(r["homes_each"])} homes each<br>'
            f'Typical home: <b>≈ {round(r["walk_min"])} min</b> walk<br>Farthest home: ≈ {round(r["walk_max"])} min<br>'
            f'<b>{round(r["pct10"])}%</b> of homes within 10 min</div></div>\n')
tiles = "".join(tile(*o) for o in order if o[0] in R)
tiles += (f'        <div class="tile"><div class="t-h">Streets <span class="t-note">road access inside the shading</span></div><div class="t-big">≈ {st["street_mi"]:.1f}<span> mi of streets</span></div>'
          f'<div class="t-l">+ ≈ {st["alley_mi"]:.1f} mi of alleys<br>{st["intersections"]} intersections (3+ way)<br>≈ {st["per_100_acres"]:.0f} intersections per 100 acres<br>'
          f'≈ {r10(st["homes_per_street_mi"])} homes per street mile</div></div>\n')
block = f'''      <div class="sum">
        <div class="tile sum-t"><div class="t-h">Homes <span class="t-note">green, teal and blue buildings on the map; one per building, so a duplex or apartment building counts once</span></div><div class="t-big">≈ {r10(H)}</div><div class="t-l">{c["house"]} houses<br>{c["multi"]} duplex–fourplex<br>{c["apartment"]} apartment bldgs</div></div>
        <div class="tile sum-t"><div class="t-h">Shaded area</div><div class="t-big">≈ {acres:.0f}</div><div class="t-l">acres</div></div>
        <div class="tile sum-t"><div class="t-h">Density <span class="t-note">whole shaded area, streets and public land included</span></div><div class="t-big">≈ {H / acres:.0f}</div><div class="t-l">homes per acre<br>of shaded area</div></div>
        <div class="tile sum-t"><div class="t-h">Other buildings <span class="t-note">colored buildings on the map, no icons (county records); not listed below</span></div><div class="t-big">{c["business"] + c["government"] + c["worship"] + c["nonprofit"]}</div><div class="t-l">{c["business"]} businesses<br>{c["government"]} government buildings (city, county, state, federal, school)<br>{c["worship"]} churches<br>{c["nonprofit"]} nonprofit / community<br>+ {c["outbuilding"]} garages/sheds (not counted)</div></div>
      </div>
      <div class="howto"><b>Reading the tiles:</b> tiles marked <i>map icons</i> or <i>stops</i> count the places with icons on the map. <b>Homes</b>, <b>Businesses</b> and <b>Other buildings</b> count building outlines from county records, shown as colored buildings rather than icons, so the two kinds of numbers differ (a place can span several buildings, and some places, like Health &amp; Human Services or the school, are government-owned buildings). Walk times run from each home to its <i>nearest</i> one inside the shading. <b>Typical home</b> is the middle home (half walk less, half more). <b>Farthest home</b> is the worst-off home's walk to its own nearest one, not the walk to the farthest service. Parks, the school and the field count from their nearest edge. Times use the pace from the photo walk (≈ 2.2 mph, from the photo timestamps; the #4→#5 stretch with the food stop is left out).</div>
      <div class="stats">
{tiles}      </div>
'''
t = open(S + "/settings/page_template.html").read()
t, n = re.subn(r'      <div class="(?:homes-n|sum)">.*?\n      <div class="stats">\n.*?      </div>\n', block, t, count=1, flags=re.S); assert n == 1, n
open(S + "/settings/page_template.html", "w").write(t); print(re.sub(r"<[^>]+>", " ", block))
