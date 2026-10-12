# Sources

Where every piece of data on `../analysis-and-map.html` came from. All downloads were made on **Oct 11, 2026**.

## Your own material

| What | Used for | File(s) here |
|---|---|---|
| 6 iPhone photos (HEIC), taken Sat Oct 10, 2026, 3:38–4:37 PM | Photo pins (numbered by capture time), photo locations, walking pace | Originals in `../photos/`; pin data in `data/photos/photos.json`, metadata-free images in `data/photos/photo-1–6.jpg` |
| Photo capture times and GPS positions | Order of the photos, pin positions, pace (≈ 2.2 mph from the time and distance between photos) | Read from the photos' metadata with macOS Spotlight (`mdls`) |
| Route sketch drawn with a mouse on a map screenshot | The walking route | `data/sketches/Pasted 2026-10-11 at 12.00.35 PM.png` |
| Band-width sketch (black lines showing roughly how far out to shade on each side of the route) | The original band width | `data/sketches/Pasted 2026-10-11 at 12.07.43 PM.png` |
| Route correction between photos #4 and #5 | The corrected route | `data/sketches/Pasted 2026-10-11 at 12.22.01 PM.png` |
| Screenshots of the map at the zoom level you planned to use, and of later versions | Icon sizes, overlap fixes, the zoom-out limits, layout fixes | `../preview screenshots/` |

## Your local knowledge

Facts about the walk and the neighbourhood that came from you, not from a dataset:

- **The food stop.** You stopped for about 15 minutes, by your best guess, between photos #4 and #5 for food and drinks, across from Schuller apartments. That leg is left out of the walking pace.
- **Adult Supervision is also an election office.** Jackson County Adult Supervision Service is also the election office / ballot drop box, so they share one icon.
- **The "Sheriff" entry is really the jail**, with a small amount of sheriff's staff.
- **The Lausmann Annex.** You noted it as a postal service, which is why it was included. Research then identified it as City of Medford offices; see *Other references*.
- **The McLoughlin school field** is used by the public as a walking and running track, for walking dogs and for hanging out on the grass. That is why it counts as recreation.
- **The bus stop count.** There are 7 bus stops along the walk (at that point the map was missing one). You also spotted a bus stop by the community center that wasn't counted.
- **Places to add**, which you knew were there: the employment department, city hall, the park along S Ivy St, Jackson County Health & Human Services, St Mark's Episcopal Parish Church, First Presbyterian, Bank of America and the old library.
- **Things that looked wrong**, which led to checks and corrections: the La Clinica, YMCA and church buildings shown as "public"; walk times that seemed too short for the pace you walked; "36 bus stops per sq mi" and "0.33 sq mi"; and "9 government and courts".

## Your ideas and decisions (what to measure)

These shape every number on the page. They are choices, so no outside source applies.

| Idea or decision | Where it shows up |
|---|---|
| Shade a band along the route and study only what is inside it | The shaded zone; every count and statistic |
| Fill the inside of the loop with the same shade as the band | The shaded zone |
| Widen the band evenly by the distance from Alba Park to Oregon Pacific Financial | `buf` = 152 m in `settings/zone_cfg.json` |
| Extend the band only locally, and naturally, to take in the Education Service District and Holly Theater, Medford Police, and the community center | The three `bulges` in `settings/zone_cfg.json` |
| Pull the zone edge back where a block's only house sits at the edge (W 8th St near Lincoln St, and N Oakdale Ave near W 3rd St) | The two `carves` in `settings/zone_cfg.json` |
| Count apartment buildings and houses as "homes", ignoring businesses; count each apartment building once | Homes tile, density, coloured buildings |
| **Density, and access to services.** <br>• Measure the shaded area and turn the approximate home count into density (homes per acre, over the whole shaded area, with streets and public land included). <br>• Apply the same per-area idea to every kind of service on the map. <br>• Your reasoning: if you know the density of homes, you can work out the "density" of what those homes have access to. So the ratio of homes to services per unit of area is what matters, not the raw counts. <br>• You then asked for a better way to show that access, which led to measuring the walk from every home to its nearest service of each kind. | Density tile; the "1 per ≈ N acres" and "≈ N homes each" lines on every tile; the walk-time lines (typical home, farthest home, share within 10 min) |
| Service counts are the icons on the map, not every building | "map icons" wording; icon counts kept separate from building counts |
| Separate public (government-run: city, county, state) from businesses, churches and nonprofits, each with its own colour | Building classes and colours; Other buildings tile |
| Businesses get their own tile but are not listed | Businesses tile |
| Banking and Education are separate categories | Category tiles and list |
| Road access is a category of its own, "because that's how you get places" | Streets tile |
| All walking is on roads | Walk-time method (streets and alleys only) |
| Check walk times against the photo timestamps and distances | The measured pace (≈ 60 m/min) |
| Acres only; no square feet, no square miles, no distances in feet | Units throughout |

## Your design

### The map and page

You designed how the map looks and works. Claude built it to your specifications, and you reviewed each version in the browser.

- **The three-step build.**
  - First, a photo map: numbered pins in capture order, plus your route.
  - Then a separate copy with the shaded band and the services in it, keeping the photo map unchanged.
  - Then a copy of that with every building coloured by how it was counted.
- **The icons:**
  - crosses for churches;
  - a government-building icon (from an example image you supplied);
  - scales for courts;
  - a running man for the YMCA;
  - trees for parks;
  - a school icon distinct from government buildings;
  - a medical cross for clinics;
  - a clearer apple for the food pantry;
  - a money sign for the bank;
  - a recreation icon for the school field;
  - bus icons, first small cars and then buses, made bigger, recoloured so they don't blend in, and set in their own bubble.
- **Keeping the map readable:**
  - icons must not overlap the photo numbers or each other at any zoom;
  - no jail dot;
  - no numbers on bus stops;
  - block bubbles that shrink as you zoom out instead of covering icons;
  - popups that show the name only.
- **Legends and keys:**
  - an icon legend on the map;
  - a colour key for buildings;
  - no duplicate colour coding under the housing numbers, since it's already on the map.
- **The stats layout:**
  - tiles in a grid;
  - a shorter explanatory paragraph;
  - explanations placed next to the tiles they explain;
  - the stats moved back under the map;
  - a caret to collapse them so the map can be nearly full screen;
  - a drawer that covers most of the window;
  - a stats button that is always visible;
  - every load starts with the stats collapsed.
- **The zoom:**
  - the zoom level you planned for screenshots set the icon sizes;
  - the zoom-out limit runs from N Ross Ln to E 9th St, on any screen size;
  - the map opens fully zoomed out on a computer, and zoomed in more on a phone so it isn't cramped.
- **The list:**
  - compressed, so it fits a reasonable screenshot;
  - no bus-stop entries or addresses;
  - no feet distances.

### The research and verification process

You designed how the work was researched and checked. Claude and its AI agents carried it out.

- **Where data comes from.** You chose to verify buildings rather than guess, and approved downloading the Jackson County assessor data to do it (after asking whether Google Maps could be used). You also asked how the county map server is known to be Jackson County's, and required proof.
- **The verification standard.** You declared the map final, asked for "a full pass on all data we have and verify", and set Claude Code to its highest thinking level. That standard required:
  - every part to be checked;
  - every number to be recomputed from the raw data;
  - every reported problem to be independently tested;
  - nothing to be missed.

  It produced the 245-agent verification and source-checking described in `../RESEARCH_PIPELINE.md`.
- **Proof for the method.** You asked for every formula to be written out, and for sources that prove each one.
- **Review loop.** You checked each version yourself and questioned anything that looked off. You asked whether anything else needed the same fix, so each correction was carried through everywhere it applied.
- **Rules for the files and data:**
  - keep only the final version;
  - organise the data and scripts into `raw data/`, with scripts in their own folder;
  - keep everything needed to check or rebuild the map;
  - delete only to the Trash;
  - publish on GitHub with a public web page.
- **The documentation:** this file, `../README.md` (how to use and rebuild everything) and `../RESEARCH_PIPELINE.md` (how it was done and checked), each written to your specification and corrected by you.

## Comparisons you brought in

| What | How it was used |
|---|---|
| A ChatGPT estimate of about 250 homes ("green squares") | Compared against the county-based count; not used as data |

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

### 7. Walking pace (from your photos — no outside source)

Distance along the route between consecutive photos ÷ time between their timestamps, over the legs #1→#2, #2→#3, #3→#4 and #5→#6 (the #4→#5 leg, with the food stop, is left out): 1,733 m in 29.1 min ≈ 60 m per minute.
