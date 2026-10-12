# Sources

Where every piece of data on `../analysis-and-map.html` came from. All downloads were made on **Oct 11, 2026**.

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

## Jordan's own material

| What | Used for | File(s) here |
|---|---|---|
| 6 iPhone photos (HEIC), taken Sat Oct 10, 2026, 3:38–4:37 PM | Photo pins (numbered by capture time), photo locations, walking pace | Originals in `../photos/`; pin data in `data/photos/photos.json`, metadata-free images in `data/photos/photo-1–6.jpg` |
| Photo capture times and GPS positions | Order of the photos, pin positions, pace (≈ 2.2 mph from the time and distance between photos) | Read from the photos' metadata with macOS Spotlight (`mdls`) |
| Route sketch drawn with a mouse on a map screenshot | The walking route | `data/sketches/Pasted 2026-10-11 at 12.00.35 PM.png` |
| Band-width sketch (black lines showing roughly how far out to shade on each side of the route) | The original band width | `data/sketches/Pasted 2026-10-11 at 12.07.43 PM.png` |
| Route correction between photos #4 and #5 | The corrected route | `data/sketches/Pasted 2026-10-11 at 12.22.01 PM.png` |
| Screenshots of the map at the zoom level Jordan planned to use, and of later versions | Icon sizes, overlap fixes, the zoom-out limits, layout fixes | `../preview screenshots/` |

## Jordan's local knowledge

Jordan has lived in this area for over 20 years. These facts about the walk and the neighbourhood came from that first-hand knowledge, not from a dataset:

- **The food stop.** Jordan stopped for about 15 minutes (Jordan's best guess) between photos #4 and #5 for food and drinks, across from Schuller apartments. That leg is left out of the walking pace.
- **Adult Supervision is also an election office.** Jackson County Adult Supervision Service is also the election office / ballot drop box, so they share one icon.
- **The "Sheriff" entry is really the jail**, with a small amount of sheriff's staff.
- **The Lausmann Annex.** Jordan noted it as a postal service, which is why it was included. Research then identified it as City of Medford offices; see *Other references*.
- **The McLoughlin school field** is used by the public as a walking and running track, for walking dogs and for hanging out on the grass. That is why it counts as recreation.
- **The bus stop count.** There are 7 bus stops along the walk (at that point the map was missing one). Jordan also spotted a bus stop by the community center that wasn't counted.
- **Places to add**, which Jordan knew were there: the employment department, city hall, the park along S Ivy St, Jackson County Health & Human Services, St Mark's Episcopal Parish Church, First Presbyterian, Bank of America and the old library.
- **Things that looked wrong**, which led to checks and corrections: the La Clinica, YMCA and church buildings shown as "public"; walk times that seemed too short for the pace Jordan walked; "36 bus stops per sq mi" and "0.33 sq mi"; and "9 government and courts".

## Jordan's ideas and decisions (what to measure)

These shape every number on the page. They are choices, so no outside source applies. The biggest:

| Idea or decision | Where it shows up |
|---|---|
| Study only what is inside a shaded band along the route. Jordan set its width and shaped its edges. | The shaded zone; every count and statistic; `settings/zone_cfg.json` |
| Count houses and apartment buildings as homes, each building once, and turn the count into density | Homes and Density tiles; coloured buildings |
| Access to services: the ratio of homes to services per acre. Together we arrived at measuring each home's walk to the nearest service, and Jordan finalized how it is shown. | "1 per ≈ N acres", "≈ N homes each" and walk-time lines on every tile |
| Count services as map icons, separate from buildings. Split government, businesses, churches and nonprofits. | Tile wording; building colours; Businesses and Other buildings tiles |
| Road access as its own category, and all walking on roads, checked against Jordan's photo timestamps | Streets tile; walk-time method and pace |
| Acres only | Units throughout |

The full list is in `../RESEARCH_PIPELINE.md`, under *Measurements and statistics Jordan chose*.

## Jordan's design

**The map and page.** Jordan designed what the map shows and how it reads. It grew in three steps: a photo map, then the shaded services map, then coloured buildings. Jordan's rules shaped every layer:
- Jordan's choice of icons;
- nothing overlapping at any zoom;
- name-only popups;
- a stats drawer that can always be opened;
- zoom limits set by real streets.

Claude built each version, and Jordan reviewed it in the browser until it was right.

**The research and verification process.** Jordan set the standard the work was held to:
- official county data instead of guesses, with proof the source is Jackson County's;
- written formulas, each backed by published sources;
- a full independent verification of everything, at Claude Code's highest thinking level.

That standard produced the 245-agent checking and source research. Jordan reviewed every result and had each fix carried through.

For the full detail of everything Jordan designed, decided and directed, see `../RESEARCH_PIPELINE.md` (*Who did what*).

## OpenStreetMap

© OpenStreetMap contributors, available under the Open Database License (ODbL) — https://www.openstreetmap.org/copyright

| What | Source | File(s) here |
|---|---|---|
| Streets, alleys, building outlines, named places, bus stops (RVTD platforms) | OpenStreetMap API 0.6 `map` request, bounding box lng −122.8905 to −122.8730, lat 42.3200 to 42.3305 — `https://api.openstreetmap.org/api/0.6/map?bbox=-122.8905,42.3200,-122.8730,42.3305` | `data/openstreetmap/area.osm` |
| Positions of N Ross Ln (≈ lng −122.8994) and E 9th St (≈ lng −122.8693), used for the zoom-out limits | Nominatim place search — `https://nominatim.openstreetmap.org` | Values written into `settings/page_template.html` (not saved as a file) |
| Background street map (map tiles) | `https://tile.openstreetmap.org` | Loaded live by the page; needs internet |

## Jackson County, Oregon (Assessor & GIS)

Public ArcGIS services published by Jackson County. Only the fields listed were requested — no owner names or mailing addresses.

| What | Source | Fields requested | File here |
|---|---|---|---|
| Parcels (taxlots) | Taxlots2 layer — `https://jcportal.jacksoncountyor.gov/server/rest/services/Property/Taxlots2/FeatureServer/1` (updated weekly from Assessor and Cartography data) | MAPTAXLOT, PROPCLASS, parcel outline | `data/jackson-county/taxlots.geojson` |
| Building records | Improvements layer — `https://jcportal.jacksoncountyor.gov/server/rest/services/Property/Improvements/FeatureServer/0` (current tax year, from the Assessor's ORCATS system) | MAPTAXLOT, IMPROVEMENTID, STATCLASS, FIRSTFLOOR, SECONDFLOOR, THIRDFLOOR | `data/jackson-county/improvements.json` |
| Property class code meanings | Property Class Descriptions (JCGIS_Owner) — `https://services1.arcgis.com/DwYBkWQPdaJNWrPG/arcgis/rest/services/Property_Class_Descriptions/FeatureServer` | all | `data/jackson-county/Property_Class_Descriptions.json` |
| Building (stat) class code meanings | Stat Class Descriptions (JCGIS_Owner) — `https://services1.arcgis.com/DwYBkWQPdaJNWrPG/arcgis/rest/services/Stat_Class/FeatureServer` | all | `data/jackson-county/Stat_Class.json` |

Both data layers were requested for the same box as the OpenStreetMap data: lng −122.8905 to −122.8730, lat 42.3200 to 42.3305.

**How the two code tables are known to be Jackson County, Oregon's:** they are hosted on ArcGIS Online (`services1.arcgis.com`) rather than the county's own server, so this was checked on Oct 11, 2026:
- Both items (`da67c2060ed2409db3ccef5f4419af75`, `e52fa1f266bf458195b244adf7ddbc8c`) belong to the ArcGIS organization `DwYBkWQPdaJNWrPG`, named **"Jackson County GIS"** (account `JCGIS_Owner`).
- Jackson County, Oregon's official GIS site lists both, with source "Jackson County GIS" and these exact service addresses: https://gis.jacksoncountyor.gov/datasets/property-class-descriptions and https://gis.jacksoncountyor.gov/datasets/e52fa1f266bf458195b244adf7ddbc8c_0
- The Property Class item's description cites Oregon Administrative Rule 150-308.215, and every code in the county parcel and building data above has a matching entry in these tables.

## Other references

| What | Source |
|---|---|
| Lausmann Annex (200 S Ivy St) is City of Medford offices (building officials and inspectors) | Southern Oregon builders' association directory — https://members.buildso.com/list/member/city-of-medford-3560 |
| Metres per degree at Medford's latitude (42.325° N): 111,079.6 m (latitude), 82,427.8 m (longitude) | Exact WGS 84 ellipsoid formulas — see **Formulas** below |

## Software and icons

| What | Source / license |
|---|---|
| Map library | Leaflet 1.9.4 (BSD-2-Clause), loaded from cdnjs — `https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/` |
| Icons: government building, runner, tree, graduation cap, dollar sign, bus, book, people | Adapted from Google Material Icons (Apache License 2.0) |
| Icons: cross, scales, apple, running track, medical cross, shield, mask | Drawn for this map |
| Data processing | Python 3 scripts in `scripts/` (standard library only) |

## Formulas

Every source below was opened and checked against the formula or value on Oct 11, 2026, each by two independent checks.

### 1. Metres per degree (WGS 84 ellipsoid)

```
e²  = f·(2 − f)                                   (a = 6,378,137 m,  1/f = 298.257223563)
M   = a·(1 − e²) / (1 − e²·sin²φ)^(3/2)           meridian radius of curvature
N   = a / √(1 − e²·sin²φ)                         prime-vertical radius of curvature
metres per degree of latitude  = (π/180)·M
metres per degree of longitude = (π/180)·N·cos φ
```

At the walk's centre, φ = 42.325° N: **111,079.598 m** per degree of latitude and **82,427.843 m** per degree of longitude. The scripts use these rounded to 0.1 m: **111,079.6** and **82,427.8**.

- WGS 84 parameters (a, 1/f): NGA, *NGA.STND.0036_1.0.0_WGS84 — Department of Defense World Geodetic System 1984* (2014), https://earth-info.nga.mil/index.php?dir=wgs84&action=wgs84 ; NIMA *Technical Report TR8350.2*, 3rd ed. (1997, amended 2000), Eqs. 3-1 and 3-2, https://geodesy.unr.edu/hanspeterplag/library/geodesy/wgs84fin.pdf ; OGC/EPSG ellipsoid 7030 "WGS 84", https://www.opengis.net/def/crs/OGC/0/CRS84
- Radii of curvature M (ρ) and N (ν), and e² = 2f − f²: IOGP, *Geomatics Guidance Note 7, part 2: Coordinate Conversions and Transformations including Formulas* (Publication 373-7-2, 2019), https://www.iogp.org/wp-content/uploads/2019/09/373-07-02.pdf
- Length of a degree of latitude = (π/180)·M: Wikipedia, "Latitude", section *Meridian distance on the ellipsoid* (cites Rapp 1991, *Geometric Geodesy*), https://en.wikipedia.org/wiki/Latitude

**Cross-check — the series form.** The U.S. *American Practical Navigator* (Bowditch, Pub. No. 9, 2002 ed.), "Explanation of Navigation Tables", Table 7 (p. 558) gives

```
metres per degree of latitude  ≈ 111,132.92 − 559.82·cos 2φ + 1.175·cos 4φ − 0.0023·cos 6φ
metres per degree of longitude ≈ 111,412.84·cos φ − 93.5·cos 3φ + 0.118·cos 5φ
```

computed for the older **WGS 72** ellipsoid (not WGS 84). At 42.325° N it gives 111,079.57 and 82,427.81 — within 0.05 m of the WGS 84 values above. Copy: https://thenauticalalmanac.com/2002_Bowditch-_American_Practical_Navigator/EXPLANATION%20OF%20NAVIGATION%20TABLES.pdf (also https://www.starpath.com/downloads/TblExpl.pdf). The same series with WGS 84 coefficients (111,132.95255 − 559.84957 cos 2φ + 1.17514 cos 4φ − 0.00230 cos 6φ; 111,412.87733 cos φ − 93.50412 cos 3φ + 0.11774 cos 5φ) is in Wikipedia, "Geographic coordinate system", section *Length of a degree*, https://en.wikipedia.org/wiki/Geographic_coordinate_system

### 2. Local flat coordinates (equirectangular approximation)

```
x (metres east)  = longitude × 82,427.8
y (metres north) = latitude  × 111,079.6
distance between two points = √((x₂ − x₁)² + (y₂ − y₁)²)
```

This is the equidistant cylindrical (plate carrée / equirectangular) projection with true scale at the walk's latitude, used as a local flat-earth approximation.

- J. P. Snyder, *Map Projections — A Working Manual*, USGS Professional Paper 1395 (1987), Equidistant Cylindrical projection (x = R(λ − λ₀)·cos φ₁, y = R·φ), https://pubs.usgs.gov/publication/pp1395
- IOGP Guidance Note 7-2 (above), Equidistant Cylindrical (Plate Carrée), EPSG method 1029 (spherical form)
- E. Williams, *Aviation Formulary* v1.47, "Local, flat earth approximation" (north distance = R₁·Δlat, east distance = R₂·cos lat₀·Δlon, with WGS 84 radii), https://edwilliams.org/avform147.htm
- C. Veness, *Calculate distance, bearing and more between latitude/longitude points*, "Equirectangular approximation" (Pythagoras on x = Δλ·cos φm, y = Δφ), https://www.movable-type.co.uk/scripts/latlong.html

Accuracy check: compared with exact ellipsoid distances (Vincenty's method, below) between the corners of the data area, the largest difference is 0.12 m over 1,442 m.

### 3. Vincenty's method (used only for the accuracy check)

- T. Vincenty, "Direct and inverse solutions of geodesics on the ellipsoid with application of nested equations", *Survey Review* 23(176): 88–93 (1975), doi:10.1179/sre.1975.23.176.88 ; scan hosted by NOAA NGS: https://www.ngs.noaa.gov/PUBS_LIB/inverse.pdf
- NOAA NGS, *NGS Toolkit, Part 4: General Geodetic Computations* — the NGS INVERSE tool uses Vincenty's 1975 formulae, https://www.ngs.noaa.gov/TOOLS/Professional_Surveyor_Articles/GeodeticComputations.pdf
- C. F. F. Karney, "Algorithms for geodesics", *Journal of Geodesy* 87(1): 43–55 (2013), doi:10.1007/s00190-012-0578-z, https://arxiv.org/abs/1109.4448 — notes the method can fail to converge only for nearly opposite points on the globe, which does not apply over a few kilometres.

### 4. Unit conversions

```
1 acre        = 43,560 ft² = 4,046.856 422 4 m²
1 mile        = 5,280 ft   = 1,609.344 m           (so 60 m per minute = 1 m/s = 2.237 mph)
walk minutes  = walking distance in metres ÷ 60
```

- NIST, *U.S. Survey Foot: Revised Unit Conversion Factors* (exact international values), https://www.nist.gov/pml/us-surveyfoot/revised-unit-conversion-factors
- NIST *Handbook 44* (2026), Appendix C: General Tables of Units of Measurement, https://www.nist.gov/document/2026-nist-handbook-44-appendix-c
- NIST *Guide to the SI* (Special Publication 811), Appendix B.8: mile = 1.609 344 × 10³ m, mile per hour = 0.447 04 m/s (exact), https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8
- *Refinement of Values for the Yard and the Pound*, Federal Register notice 59-5442 (1959) — 1 yard = 0.9144 m exactly, the basis of the international foot and mile, https://geodesy.noaa.gov/PUBS_LIB/FedRegister/FRdoc59-5442.pdf

### 5. Geometry used in the scripts

```
polygon area (shoelace):   A  = ½ · |Σ (xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)|
polygon centroid:          Cx = (1 / 6A) · Σ (xᵢ + xᵢ₊₁)·(xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)     (Cy likewise with y)
inside a polygon:          even–odd rule — a ray from the point crosses the boundary an odd number of times
distance point → segment:  t = clamp(((P − A)·(B − A)) / |B − A|², 0, 1);  distance = |P − (A + t·(B − A))|
```

- R. Nürnberg, "Calculating the area and centroid of a polygon in 2d" (Imperial College London, 2013), hosted by P. Bourke, https://paulbourke.net/geometry/polygonmesh/
- E. W. Weisstein, "Polygon Centroid", *MathWorld*, https://mathworld.wolfram.com/PolygonCentroid.html
- W3C, *Scalable Vector Graphics (SVG) 1.1, 2nd ed.* (2011), chapter 11 (Painting), 'fill-rule' property — the even-odd rule, https://www.w3.org/TR/SVG11/painting.html
- D. Eberly, "Distance Between Point and Line, Ray, or Line Segment", Geometric Tools, https://www.geometrictools.com/Documentation/DistancePointLine.pdf

### 6. Algorithms

- Shortest walking routes — E. W. Dijkstra, "A note on two problems in connexion with graphs", *Numerische Mathematik* 1: 269–271 (1959), doi:10.1007/BF01386390, https://ir.cwi.nl/pub/9256
- Zone outline traced from a grid — marching squares, the 2-D case of W. E. Lorensen & H. E. Cline, "Marching cubes: a high resolution 3D surface construction algorithm", *ACM SIGGRAPH Computer Graphics* 21(4): 163–169 (1987), doi:10.1145/37402.37422 ; described with linear interpolation in the scikit-image documentation for `measure.find_contours`, https://scikit-image.org/docs/stable/api/skimage.measure.html
- Outline simplification — D. H. Douglas & T. K. Peucker, "Algorithms for the reduction of the number of points required to represent a digitized line or its caricature", *Cartographica* 10(2): 112–122 (1973), doi:10.3138/FM57-6770-U75U-7727

### 7. Walking pace (from Jordan's photos — no outside source)

Distance along the route between consecutive photos ÷ time between their timestamps, over the legs #1→#2, #2→#3, #3→#4 and #5→#6 (the #4→#5 leg, with the food stop, is left out): 1,733 m in 29.1 min ≈ 60 m per minute.
