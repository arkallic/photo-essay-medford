import json, sys
S = sys.argv[1]
src = open(S + "/build/services-along-walk.html").read()
OUT = sys.argv[2] if len(sys.argv) > 2 else S + "/../analysis-and-map.html"
B = json.load(open(S + "/outputs/building_classes.json"))
CLS = {"house": "house", "multi": "multi", "apartment": "apt", "outbuilding": "shed", "business": "biz", "government": "gov", "worship": "church", "nonprofit": "npo"}
data = [[CLS[b["cls"]], [[round(a, 6), round(o, 6)] for a, o in b["pts"]]] for b in B]
print({k: sum(1 for c, _ in data if c == k) for k in CLS.values()})
blocks = [{k: v for k, v in b.items() if k != "ids"} for b in json.load(open(S + "/outputs/block_counts.json"))]
def rep(a, b):
    global src
    assert src.count(a) == 1, a[:60]; src = src.replace(a, b)
rep("<title>Services Along Walk</title>", "<title>Homes and Services</title>")
rep("<h1>Services Along the Walk</h1>", "<h1>Homes and Services Along the Walk</h1>")
rep("  /*HOMES_CSS*/", """  .map-key { background:rgba(255,255,255,.92); color:#1f1d1a; padding:6px 9px; border-radius:6px; font:12px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    box-shadow:0 1px 4px rgba(0,0,0,.3); }
  .map-key div { display:flex; align-items:center; gap:6px; }
  .map-key .key-blk { margin-top:3px; gap:5px; }
  .map-key .key-blk .blk { transform:none; }
  .map-key i { width:11px; height:11px; border-radius:2px; display:inline-block; border:1px solid rgba(0,0,0,.25); }
  .blk { background:#fff; color:#111; border:1.5px solid #2f9e44; border-radius:9px; padding:0 5px; font:700 11px/16px -apple-system, BlinkMacSystemFont, sans-serif;
    white-space:nowrap; transform:translate(-50%,-50%) scale(var(--s)); display:inline-block; box-shadow:0 1px 2px rgba(0,0,0,.3); }
  .blk small { font-weight:600; color:#1971c2; }""")
rep("  /*HOMES_LAYERS*/", """  // Buildings in the shaded area, colored by Jackson County assessor records (property + building class).
  const BLDG = """ + json.dumps(data, separators=(",", ":")) + """;
  const BCOL = { house: "#2f9e44", multi: "#15aabf", apt: "#1971c2", shed: "#adb5bd", biz: "#f2b705", gov: "#9775fa", church: "#a0785a", npo: "#f783ac" };
  const BNAME = { house: "House", multi: "Duplex to fourplex", apt: "Apartment building", shed: "Garage or shed (not counted)", biz: "Business (not a home)", gov: "Government building (not a home)", church: "Church (not a home)", npo: "Nonprofit / community (not a home)" };
  const bldgLayer = L.layerGroup().addTo(map);
  BLDG.forEach(([c, pts]) => L.polygon(pts, { color: BCOL[c], weight: .8, opacity: .9, fillColor: BCOL[c], fillOpacity: .6 })
    .bindTooltip(BNAME[c], { sticky: true }).addTo(bldgLayer));
  const key = L.control({ position: "bottomleft" });
  key.onAdd = () => { const d = L.DomUtil.create("div", "map-key");
    d.innerHTML = Object.keys(BCOL).map(k => `<div><i style="background:${BCOL[k]}"></i>${BNAME[k].replace(/ \((not counted|not a home)\)/, "")}</div>`).join("") +
      `<div class="key-blk"><span class="blk">12 <small>+3</small></span> per block: houses <span style="color:#1971c2;font-weight:600">+ multi-unit</span> (zoom in)</div>`; return d; };
  key.addTo(map);
  // Homes per block: plain number = houses, blue "+N" = multi-unit buildings (duplex to apartment). Bubbles give way to icons.
  const BLOCKS = """ + json.dumps(blocks, separators=(",", ":")) + """;
  const blockMarks = BLOCKS.map(b => L.marker([b.lat, b.lng], { interactive: false, keyboard: false, zIndexOffset: -2000,
    icon: L.divIcon({ className: "", iconSize: null, html: `<div class="blk">${b.h ? b.h : ""}${b.a ? `${b.h ? " " : ""}<small>+${b.a}</small>` : ""}</div>` }) }));
  blockMarks.forEach((m, i) => marks.push({ m, ll: L.latLng(BLOCKS[i].lat, BLOCKS[i].lng), kind: "bubble", leader: null }));
  const fitBlocks = () => blockMarks.forEach(m => map.getZoom() >= 16 ? m.addTo(map) : map.removeLayer(m));
  map.on("zoomend", fitBlocks); map.whenReady(fitBlocks);""")
open(OUT, "w").write(src)
import os   # the in-between page is only a build step: remove it once the final map is written
os.remove(S + "/build/services-along-walk.html")
if not os.listdir(S + "/build"): os.rmdir(S + "/build")
