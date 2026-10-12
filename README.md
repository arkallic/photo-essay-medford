# Photo Essay — walk map and neighbourhood analysis

**[View Data page and map](https://arkallic.github.io/photo-essay-medford/)** — https://arkallic.github.io/photo-essay-medford/

**Jordan Whitlock - PSU.edu Communities Class Assignment**

**Time spent: Sunday, Oct 11, 2026, about 11:57 AM – 8:30 PM (≈ 8½ hours)**

| | |
|---|---|
| Direct work, Jordan and Claude together | ≈ 5¾ hours of active back-and-forth: designing, building, reviewing and correcting (breaks longer than 15 minutes not counted) |
| AI agent runs | 4 runs, ≈ 2 hours of real (clock) time, running alongside the direct work. Because many of the 245 agents worked at once (up to about 10–16 at a time), this added up to ≈ 10 agent-hours of work, counting each agent's time separately, like person-hours. |
| When the agents ran | 2:29–3:42 PM full verification · 3:50–4:07 PM re-check · 5:23–5:42 PM final check · 6:12–6:26 PM formula sources |


| Run | Real time | Agent time added together |
|---|---|---|
| Full verification | 73 min | ≈ 6 h 21 min (151 agents) |
| Re-check | 17 min | ≈ 59 min (13 agents) |
| Final check | 19 min | ≈ 1 h 6 min (18 agents) |
| Formula sources | 14 min | ≈ 1 h 29 min (63 agents) |
| **Total** | **≈ 2 h** | **≈ 9 h 55 min** |

A map of a photo walk in Medford, Oregon (Saturday Oct 10, 2026), with the area around the route shaded and analysed: homes, services, bus stops, streets and walking times.

- **How this was researched, downloaded and verified:** `RESEARCH_PIPELINE.md` (Work done by myself shown here: my AI pipeline design -- How I designed workflow, personally trained AI context, and got data. Also details on personal designs, by hand work and more)
- **Where every piece of data came from, and every formula used:** `raw data/SOURCES.md`

## What's in this folder

```
Photo Essay/
├── analysis-and-map.html    the finished map — open this
├── README.md                this file
├── RESEARCH_PIPELINE.md     how the work was done and checked
├── photos/                  the six original iPhone photos (HEIC)
├── preview screenshots/     Jordan's screenshots
└── raw data/                everything needed to check or rebuild the map
    ├── SOURCES.md
    ├── data/          raw inputs (as downloaded or as Jordan provided them)
    ├── settings/      the things you might edit
    ├── scripts/       the Python scripts that build the map
    ├── outputs/       what the scripts produce (regenerated on every rebuild)
    └── verification/  the latest independent check of the map
```

`analysis-and-map.html` is self-contained (photos and data are inside the file). It only needs an internet connection for the background street map and the map library.

---

## Using the map

Open `analysis-and-map.html` in any web browser (double-click it in Finder).

**The map**
- **Orange line** — the walking route. **Orange numbered circles** — the six photos, in the order taken; click one to see the photo and time.
- **Blue shading** — the area analysed: the loop of the route plus about 150 m (≈ 500 ft) outside it, bulging out in three spots to take in nearby services and trimmed around two lone houses at its edge. Every number counts only what is inside the shading.
- **Service icons**: small white circles with a coloured symbol. The symbol says what the place is (cross = church, columned building = government office, scales = court / legal aid, shield = jail / police, tree = park, and so on). The colour gives the category:
  - dark pink: health & social services
  - purple: government & courts
  - blue: education
  - brown: places of worship
  - green: recreation & parks
  - teal: banking & finance
  - orange: arts & culture
- **Bus stops**: slightly larger white circles with a black bus symbol and a black ring.
- **Icon key**: the **Map icons** key (top right) names each symbol. Click its title to fold or unfold it; it starts folded on phones. Click any icon to see its name.
- **Crowded icons**: when icons would overlap, they are nudged apart, and a thin grey line points back to each one's true spot.
- **Coloured buildings**: every building in the shaded area, coloured by Jackson County records. The building key is bottom left. Hover over a building to see its type.

  | Colour | Building type |
  |---|---|
  | green | house |
  | teal | duplex–fourplex |
  | blue | apartment building |
  | grey | garage or shed |
  | yellow | business |
  | light purple | government building |
  | brown | church |
  | pink | nonprofit / community |
- **Number bubbles** (white, green outline; zoom in to see them): homes per street block. The black number counts houses. The blue **+N** counts multi-unit buildings, duplex up to apartment building.
- **Zoom and pan**: the map always opens fully zoomed out (on a phone it opens zoomed in to fit the shaded area). Scroll, pinch, or use the + / − buttons. You can zoom out until the view spans N Ross Ln (west) to E 9th St (east), on any screen size. Dragging stops at the edge of that area.

**The stats drawer**
- The page always opens with the drawer closed. To open it, click the orange **▴ Show stats & list** button at the top of the map, or the bar along the bottom. The drawer slides up over the map (about 85% of the window). To close it, click **Hide stats & list** or press **Esc**.
- **Summary tiles:**
  - Homes
  - Shaded area (acres)
  - Density (homes per acre)
  - Other buildings (businesses, government, churches, nonprofit / community)
- **Category tiles:** one each for services, bus stops, each service category, and businesses. Each shows:
  - how many are inside the shading;
  - one per how many acres, and how many homes per place;
  - the walk for the **typical home** (the middle home: half walk less, half more);
  - the walk for the **farthest home** (the worst-off home's walk to its own nearest one);
  - the share of homes within a 10-minute walk.
- **Walk times** follow streets and alleys only, at the pace measured from the photo walk (≈ 2.2 mph).
- **The Streets tile** is different: it gives miles of streets and alleys, intersections, intersections per 100 acres, and homes per street mile.
- **What the counts mean:** tiles marked **map icons** or **stops** count icons on the map. **Homes**, **Businesses** and **Other buildings** count building outlines (the coloured buildings, not icons), so the two kinds of numbers differ.
- **The list** under the tiles names every service inside the shading, grouped by category. Clicking a name closes the drawer, zooms to that place and opens its name. A second section, "Nearby, outside the shading", appears only if a listed place falls outside the shading (none does now).

---

## The files in `raw data/`

### `data/` — raw inputs

| File | What it is |
|---|---|
| `openstreetmap/area.osm` | OpenStreetMap data for the walk area: streets, alleys, building outlines, named places, bus stops. |
| `jackson-county/taxlots.geojson` | Jackson County parcels (parcel ID, property class, outline). No owner names or addresses. |
| `jackson-county/improvements.json` | Jackson County building records (parcel ID, building class, floor areas). |
| `jackson-county/Stat_Class.json`, `Property_Class_Descriptions.json` | Official meanings of the county codes. |
| `photos/photos.json`, `photos/photo-1.jpg`–`photo-6.jpg` | The six photo pins: number (by capture time), position, time, original file name; images with camera metadata removed (#3 rotated upright). |
| `route.json` | The walking route as a closed loop of [lat, lng] points. |
| `sketches/` | Jordan's sketches: route (`…12.00.35 PM.png`), band width (`…12.07.43 PM.png`), route correction between photos #4 and #5 (`…12.22.01 PM.png`). |

### `settings/` — what you might edit

| File | What it controls |
|---|---|
| `zone_cfg.json` | The shaded zone: band width (`buf`, metres), the bulges (`bulges`: target points to reach) and the notches (`carves`: houses to leave out). |
| `extra_places.json` | Named places added from the wider map view, with their category and icon. |
| `page_template.html` | The page design: layout, icons, legend, drawer, zoom limits. The stats tiles are written into it by `statsblock.py`. |

Which places are shown, removed, merged or renamed is set in the **"user edits"** block of `scripts/build.py` (for example the Randall Theater removal, the Courthouse & County Offices merge, the Old Medford Public Library, McLoughlin field & track, Lausmann Annex). Categories, icons and building colours are defined in `build.py`, `page_template.html` and `build_bldg.py`.

### `scripts/` — in the order they run

| Step | Script | What it does | Writes (in `outputs/`) |
|---|---|---|---|
| 1 | `zone_build.py` | Builds the shaded zone outline (band + loop + bulges − notches) and its area | `zone.json`, `zone_area.json` |
| 2 | `county_classify.py` | Matches every building in the zone to its county parcel: house / duplex–fourplex / apartment / business / government / church / nonprofit / garage | `building_classes.json` |
| 3 | `blocks.py` | Groups homes into street blocks for the number bubbles | `block_counts.json` |
| 4 | `extract.py` | Finds named places and bus stops inside the zone in the OpenStreetMap data | `places_found.json`, `bus_stops.json` |
| 5 | `build.py` | Applies the place decisions and builds a temporary in-between page | `build/services-along-walk.html` (temporary) |
| 6 | `stats.py` | Walk times along roads from every home, plus businesses and streets | `stats.json` |
| 7 | `statsblock.py` | Writes the stats tiles into `settings/page_template.html` | — |
| 8 | `build.py` again, then `build_bldg.py` | Adds the coloured buildings, block bubbles and key, writes the final map, removes the temporary page | `../analysis-and-map.html` |

`zone_lib.py` is the shared "is this inside the shaded zone?" test used by the other scripts.

### `outputs/` and `verification/`

`outputs/` holds what the scripts produce; it is fully regenerated on each rebuild. `verification/` holds the scripts and results of the latest independent check (see `RESEARCH_PIPELINE.md`); those checks were run before the folder was reorganised, so file paths inside them point to the old layout.

---

## Rebuilding the map

Needs only Python 3 (built into macOS; no extra packages). In Terminal:

```
cd "raw data"        # from inside the Photo Essay (repo) folder
S="$PWD"
python3 -I scripts/zone_build.py "$S"
python3 -I scripts/county_classify.py "$S"
python3 -I scripts/blocks.py "$S"
python3 -I scripts/extract.py "$S"
python3 -I scripts/build.py "$S"
python3 -I scripts/stats.py "$S" "$S/build/services-along-walk.html"
python3 -I scripts/statsblock.py "$S"
python3 -I scripts/build.py "$S"
python3 -I scripts/build_bldg.py "$S"
```

This rewrites `analysis-and-map.html` in the Photo Essay folder (give `build_bldg.py` a second argument to write somewhere else). With unchanged data and settings, the rebuild reproduces the map byte for byte. Run all steps after any change to data or settings.

**Common changes**
- *Widen or narrow the band:* change `buf` (metres) in `settings/zone_cfg.json`, then rebuild.
- *Add a bulge to take in a place:* add an entry to `bulges` (a `name`, the place's `[lat, lng]` in `targets`, and a `margin` in metres, 30 like the others), then rebuild.
- *Leave a house out of the zone:* add an entry to `carves` (a `name`, the house's centre `lat` / `lng`, and `clear`, the clearance in metres, 12 like the others), then rebuild.
- *Add, remove or rename a place:* edit the "user edits" block in `scripts/build.py`, or `settings/extra_places.json`, then rebuild.

**Two things a rebuild does not update:**
- *The page's intro text.* The sentence under the drawer's title ("about 150 m … bulges out in three spots … trimmed around two lone houses") is plain text in `settings/page_template.html`. Edit it by hand if you change the band, bulges or notches.
- *The downloaded data area.* All data covers only the download box (see below). If you widen the zone past it, download a bigger box first.

---

## Refreshing the data

All sources are public. Download into the folders shown, then rebuild. The box used everywhere is longitude −122.8905 to −122.8730, latitude 42.3200 to 42.3305.

**OpenStreetMap** (streets, buildings, places, bus stops) — © OpenStreetMap contributors, ODbL:

```
curl -A "photo-walk-map" -o "raw data/data/openstreetmap/area.osm" \
  "https://api.openstreetmap.org/api/0.6/map?bbox=-122.8905,42.3200,-122.8730,42.3305"
```

**Jackson County parcels** (Assessor & GIS, updated weekly) — only the parcel ID, property class and outline are requested; no owner names or addresses:

```
ENV='{"xmin":-122.8905,"ymin":42.3200,"xmax":-122.8730,"ymax":42.3305,"spatialReference":{"wkid":4326}}'
curl -G "https://jcportal.jacksoncountyor.gov/server/rest/services/Property/Taxlots2/FeatureServer/1/query" \
  --data-urlencode "geometry=$ENV" --data-urlencode "geometryType=esriGeometryEnvelope" --data-urlencode "inSR=4326" \
  --data-urlencode "spatialRel=esriSpatialRelIntersects" --data-urlencode "outFields=MAPTAXLOT,PROPCLASS" \
  --data-urlencode "returnGeometry=true" --data-urlencode "outSR=4326" --data-urlencode "f=geojson" \
  -o "raw data/data/jackson-county/taxlots.geojson"
```

**Jackson County building records** (current tax year):

```
curl -G "https://jcportal.jacksoncountyor.gov/server/rest/services/Property/Improvements/FeatureServer/0/query" \
  --data-urlencode "geometry=$ENV" --data-urlencode "geometryType=esriGeometryEnvelope" --data-urlencode "inSR=4326" \
  --data-urlencode "spatialRel=esriSpatialRelIntersects" \
  --data-urlencode "outFields=MAPTAXLOT,IMPROVEMENTID,STATCLASS,FIRSTFLOOR,SECONDFLOOR,THIRDFLOOR" \
  --data-urlencode "returnGeometry=false" --data-urlencode "f=json" \
  -o "raw data/data/jackson-county/improvements.json"
```

Each query returns at most 2,000 records; this area has about 1,600 parcels and 1,750 building records. For a bigger area, page through with `resultOffset`.

**County code tables** (what the property and building class codes mean):

```
B="https://services1.arcgis.com/DwYBkWQPdaJNWrPG/arcgis/rest/services"
curl -G "$B/Property_Class_Descriptions/FeatureServer/0/query" --data-urlencode "where=1=1" --data-urlencode "outFields=*" \
  --data-urlencode "returnGeometry=false" --data-urlencode "f=json" -o "raw data/data/jackson-county/Property_Class_Descriptions.json"
curl -G "$B/Stat_Class/FeatureServer/0/query" --data-urlencode "where=1=1" --data-urlencode "outFields=*" \
  --data-urlencode "returnGeometry=false" --data-urlencode "f=json" -o "raw data/data/jackson-county/Stat_Class.json"
```

To see every field a county layer offers, open its address with `?f=pjson` added (for example `…/Taxlots2/FeatureServer/1?f=pjson`). Both layers also contain owner names and mailing addresses; leave those out of `outFields`.

**Photo times and positions** (macOS): `mdls -name kMDItemContentCreationDate -name kMDItemLatitude -name kMDItemLongitude photos/*.heic`

**Street positions** (used for the zoom limits): the OpenStreetMap place search at `https://nominatim.openstreetmap.org/search?q=N+Ross+Ln,+Medford,+OR&format=json`.
