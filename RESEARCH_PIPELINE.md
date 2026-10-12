# Research pipeline: how this map was made and checked

This document explains how `analysis-and-map.html` was produced: where the data came from, what was looked up online, how the numbers were calculated, and how the result was independently checked by teams of AI agents. For how to *use* or *rebuild* the map, see `README.md`. For the full source list and formula citations, see `raw data/SOURCES.md`.

The work was done in one long conversation (Sunday, Oct 11, 2026, about 11:57 AM – 8:30 PM; the walk itself was on Saturday, Oct 10) between Jordan and Claude, an AI assistant from Anthropic, running in Claude Code on this Mac.

- **Claude's part:** wrote and ran the scripts, downloaded the data Jordan pointed to, ran the checks, and reported back.
- **Jordan's part:** decided what the project would be and steered it at every step: what to show, what to calculate, which statistics to run and display, what to research and how, and when the result was right.

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

## Who did what

### Jordan
- **Set the project.** Asked for a numbered map of where the photos were taken, ordered by capture time. Then asked for a second map that shades the area around the walk and shows the services and homes in it, and later a third with every building coloured by type.
- **Drew the route and the area by hand.** Sketched the walking route on a screenshot, corrected it between photos #4 and #5 with a second sketch, and sketched how wide the shaded band should be. Asked for the inside of the loop to be filled with the same shade as the band. Later widened the band evenly by a measure they chose: the distance between the Alba Park and Oregon Pacific Financial icons.
  - Asked for the band to be extended only locally, and naturally, to take in nearby services: the Education Service District and Holly Theater, Medford Police, and the community center.
  - Asked for notches to leave out a block's only house where it sits at the edge (W 8th St near Lincoln St, and N Oakdale Ave near W 3rd St).
- **Decided what counts as a service, and how each is shown.**
  - Chose which places to add: the employment department, city hall, the park along S Ivy, Health & Human Services, St Mark's, First Presbyterian, Bank of America, the old library, McLoughlin field, the Lausmann Annex, and others.
  - Chose which to merge: the courthouse and county offices.
  - Picked the icons and their sizes and colours:
    - crosses for churches;
    - a government-building icon, based on an example image they supplied;
    - scales for courts;
    - a running man for the YMCA;
    - trees for parks;
    - a school icon;
    - a medical cross for clinics;
    - a clearer apple for the food pantry;
    - a money sign for the bank;
    - a recreation icon for the school field;
    - bus icons, first small cars, then larger buses in their own bubble and in a colour that stands out.
  - Asked for the jail dot to be removed.
  - Corrected how places were described (for example, the sheriff entry is a jail with some sheriff staff).
- **Defined the categories and chose what to measure, how to measure it, and how to show it.** The full list is in [Measurements and statistics Jordan chose](#measurements-and-statistics-jordan-chose) below.
- **Directed the research and how it was done.**
  - Asked for business vs. house to be verified. They first asked whether Google Maps could be used, then approved downloading the Jackson County assessor data instead.
  - Asked how we know the county map server really belongs to Jackson County, and for proof.
  - Asked for every formula to be written down with sources proving it.
- **Designed the page.**
  - Icons must never overlap the photo numbers or each other. Popups show the name only.
  - The page has an icon legend and a building colour key.
  - Icon sizes were set at the zoom level they planned to use for screenshots.
  - The list is compressed to fit a reasonable screenshot.
  - The stats sit under the map in a drawer that covers most of the window. A button that is always visible opens it, and it starts closed on every load.
  - The map opens fully zoomed out on a computer and closer in on a phone.
- **Reviewed every version.** Checked the map in the browser and reported problems: overlapping icons, the zoom limits, the map not fitting smaller windows, a stats drawer that was too short, and wording that was confusing or wrong.
- **Set the rules for the files.**
  - Keep only the final map.
  - Rename it, and organise everything behind it into `raw data`.
  - Write `SOURCES.md` and these documents.
  - Publish it all on GitHub, with a public web page for the map.
  - Never delete permanently; move things to the Trash.
  - Never download owner names or addresses.
  - Leave Jordan's own folders (`photos/`, `preview screenshots/`) untouched.

### Measurements and statistics Jordan chose

Every number on the page exists because Jordan asked for it, or asked for it to be changed.

**What gets counted**
- **Homes:**
  - Asked for apartment buildings and houses inside the shading to be counted, ignoring businesses, restaurants and the Bible college, and marked as approximate.
  - Decided apartments count as "homes", and that each apartment building counts once (floors vary, so per-unit counts would be unreliable).
  - Then asked for every building to be coloured by how it was counted.
- **The shaded area only:** decided every figure covers only what is inside the shading. After noticing theater figures came from outside the zone, asked for outside places to be separate figures, then removed them.
- **Services as map icons, not buildings:** pointed out that "all services" wrongly sounded like a count of every building, when it counts the icons placed on the map. This led to the "map icons" wording, and to keeping icon counts separate from building counts.
- **Businesses:** asked for businesses to have their own stat tile, without adding them to the list.
- **Public buildings separate from businesses:**
  - Asked for public buildings to be counted separately from businesses, in their own colours.
  - Then defined "public" as government-run (city, county, state). That split churches and nonprofits (such as the clinic and the YMCA) out from government buildings.
- **Banking and education:** asked for these to be separate categories.
- **Parks:** asked for the school field and track to count as recreation, and kept the second park.
- **Bus stops:**
  - Gave the true count (7 at the time), so a missing stop was found.
  - Asked for bus stops to be removed from the list, and for no numbers on bus icons.
  - Spotted a missing bus stop icon by the community center.
- **Garages and sheds:** as part of asking for each building to be coloured by how it was counted, these are shown on the map but not counted as homes.

**Area and density**
- Asked for the area of the shaded band to be measured and used to calculate home density. The density covers the whole shaded area, streets and public land included. Asked for the same per-area idea to be applied to every icon category, so each category gets a density.
- Proposed the idea behind the "homes per service" figures: if you know how dense the homes are, you can work out how much access each home has to services, per acre. They asked whether there was a better way to show it. Together we arrived at measuring the walk from every home to its nearest service of each kind, and they finalized how it is shown: typical home, farthest home, and share within 10 minutes.
- **Units:**
  - Dropped square feet because the numbers were too large to grasp.
  - Questioned "36 bus stops per sq mi" and "0.33 sq mi", which led to a recheck and a unit change.
  - Settled on acres only, everywhere.
  - Intersection density is shown per 100 acres.

**Walk times**
- Questioned the 3- and 4-minute walk times as too short. Asked for them to be checked against the photo timestamps and the distance walked between photos, which produced the walking pace used (≈ 60 m/min, ≈ 2.2 mph).
- Asked how far off the original figures were, then had them updated.
- Asked whether distance walked followed the route line or straight lines between photos.
- Remembered a roughly 15-minute food stop between photos #4 and #5, and asked whether it changed the pace.
- Questioned whether the longest walk (11 minutes) was too low. Asked if any maximums were wrong, and required all walking figures to follow roads, which replaced the straight-line estimates with routed walks.
- Questioned what the "about 6 min" bus-stop figure meant. This led to the "typical home" and "farthest home" labels.

**Road access**
- Proposed road access as a new category of statistics, "because that's how you get places". It became the Streets tile: miles of streets and alleys, intersections, intersections per 100 acres, and homes per street mile.

**Block counts**
- Asked for temporary per-block home counts and on/off toggles for them, then removed the toggles.
- Set the bubble rules:
  - The black number is houses; a "+N" for multi-unit buildings is always kept.
  - No bubble on a bus stop.
  - Minimum sizes were reconsidered.
  - Bubbles shrink as you zoom out instead of combining, because combining would defeat the per-block count.
- Compared the count with a ChatGPT estimate of 250 homes.

**Removed on purpose**
- Removed figures that didn't help:
  - distance in feet on each list entry and along the path ("no point in this concept throughout the whole thing");
  - square feet;
  - the colour coding under the housing numbers;
  - addresses, phone numbers, links and hours (popups show the name only);
- Asked "does anything else need a note like that?" and "any other stats … need updating?", so that each change was carried through every figure.

**Layout of the numbers**
- Asked for:
  - the home totals in a grid of tiles;
  - a shorter explanatory paragraph;
  - each explanation placed next to the tile it explains;
  - the stats under the map, with a collapse caret;
  - the stats drawer to cover most of the window.

### How Jordan directed the agents and guided the checking
- **Set the standard the agents worked to, not just the instruction to use them.** On Oct 11, about 2:26 PM, Jordan declared the map final and asked for "a full pass on all data we have and verify." At the same time they raised Claude Code's thinking level to its highest setting (Ultracode). The meat of the request, and what they wanted, was more than "use agents". It was:
  - check everything, not a sample;
  - don't trust the first answer;
  - prove each number from the raw data;
  - make sure nothing is missed.

  How the agents operated in section 4 is what they wanted, put into practice:
  - **"A full pass on all data"** meant splitting the work so every part was covered. One checker owned each area: photos and route, zone geometry, places and bus stops, buildings, statistics, and page behaviour. Each recomputed its area from the raw files instead of reading the existing numbers.
  - **"Verify"** meant the checks had to be independent. Each agent started fresh, with no access to the reasoning that produced the numbers, and wrote its own scripts. Agreement therefore meant two separate routes arrived at the same answer.
  - **Not trusting the first answer** applied to the checkers too. Every problem a checker reported went to three skeptics whose job was to *disprove* it by reproducing it themselves. A problem only counted if it survived. This is why two-thirds of all agents were skeptics.
  - **Making sure nothing was missed** meant a completeness critic. It reviewed what had been covered and named what nobody had checked, and gap agents then checked those things.
  - **Fixes were checked too.** Once the problems were fixed, a second team re-verified the changed parts (Run 2). After Jordan's next round of changes, a third team checked again (Run 3).
  - **Sources were held to the same standard.** When Jordan asked for proof of the formulas, each source a researcher found was reopened by two separate verifiers. They had to confirm the source states the exact formula or value claimed (Run 4). That is how the WGS 72 vs. WGS 84 mix-up was caught.
- **Kept that standard on for all the agent work.** The highest thinking level stayed on until about 6:30 PM. All four agent runs happened inside that window. Jordan then switched it off for the remaining smaller edits, which were made directly, without agent teams.
- **What prompted each run:**
  - **Run 1, the full verification:** the request above.
  - **Run 2, the re-check:** Run 1's fixes, made under the same standing instruction.
  - **Run 3, the final check:** Jordan's next round of changes: separating public buildings from businesses, the bus icon colour, the icon legend, the zoom bounds, and more.
  - **Run 4, the formula sources:** their direct request to "find sources that prove" each formula.
- **Pointed the checking at specific doubts.** Many checks started from something Jordan questioned. Each doubt listed under *Measurements and statistics Jordan chose* was rechecked from the raw data and, where it was wrong, corrected. So were the page problems they reported (see *Reviewed every version* above).

**Agent stats: what Jordan's request added up to**

| | |
|---|---|
| Agents started / finished | **245 / 237**, in 4 runs (Run 3 was stopped early once its problems were already fixed) |
| Per run (started) | Run 1: 151 · Run 2: 13 · Run 3: 18 · Run 4: 63 |
| By job (started) | 14 checkers · 164 skeptics · 1 completeness critic · 3 gap checkers · 7 source researchers · 56 source verifiers |
| Work done | ≈ 3,247 tool actions (own scripts run, files read, web searches, pages opened), ≈ 20 million tokens read and written, ≈ 2 hours of agent run time |
| Map checking vs. source checking | 182 agents (≈ ¾) checked the map from the raw data, offline; 63 (≈ ¼) found and confirmed formula sources online (355 web searches and page reads) |
| Problems tested | 53 reported problems sent to skeptics: 47 in Run 1, 3 in Run 2, 6 in Run 3. No skeptic refuted any of them. |
| Sources tested | 28 sources, each confirmed by 2 independent verifiers (56 checks); 1 correction (WGS 72 vs. WGS 84) |

The full breakdown, by job and by subject, is in section 4 under *Agent statistics*.

### Claude
- **Turned each request into working code.** Wrote the Python scripts and the web page, and rebuilt the map after every change.
- **Fetched the data.** Downloaded from the sources Jordan approved: OpenStreetMap, the Jackson County layers and code tables, and the Nominatim place search. Read the photo times and positions, and stripped the camera metadata from the photos.
- **Did the research legwork.** Ran web searches and read pages to find the county layers, what the codes mean, who owns the code tables, what some places are, and published sources for the formulas.
- **Worked out the methods.** Designed the methods for Jordan to approve or change: the zone outline, matching buildings to parcels, routing along roads, measuring the pace from the photos, and keeping icons apart.
- **Ran the checks** described below, reported the problems found, and fixed them. Corrections were made where Jordan had questioned something.

---

## At a glance

| | |
|---|---|
| Inputs from Jordan | 6 iPhone photos (HEIC), 3 hand-drawn sketches, and many rounds of feedback |
| Public data sources | OpenStreetMap (map data + place search), Jackson County Assessor & GIS (parcels, buildings, code tables) |
| Software | Python 3 standard library only (no extra packages); Leaflet 1.9.4 for the web map |
| AI agents used for checking and research | **245 started, 237 finished**, across 4 multi-agent runs (details below) |
| Their total work | about 20 million tokens of reading/writing, 3,247 tool actions (scripts run, files read, web pages opened), about 2 hours of run time |
| Final test | the map is rebuilt from `raw data/` and must match the published file byte for byte |

---

## 1. Gathering the data

**Jordan's photos.** The capture time and GPS position of each photo were read with macOS's built-in `mdls` tool. Photos were numbered 1–6 by capture time. Copies were converted to JPEG with camera metadata removed (location, device details), and photo #3 was rotated upright.

**Jordan's sketches.** The three sketches (route, route correction, band width) are kept in `raw data/data/sketches/`. After the widening described above, the band is 152 m.

**OpenStreetMap.** One download from the official OpenStreetMap API (`/api/0.6/map`) for a box around the walk gave every street, alley, building outline, named place and bus stop. The Overpass query service was tried first, but it was overloaded and returned errors, so the main API was used instead. The OpenStreetMap place search (Nominatim) gave the positions of N Ross Ln and E 9th St, which set the zoom-out limit.

**Jackson County.** Two layers from the county's public map server (`jcportal.jacksoncountyor.gov`):
- *Taxlots2*: parcel outlines with their property class.
- *Improvements*: every building record on each parcel, with its building ("stat") class and floor areas.

Only the parcel ID, class codes and floor areas were requested. Both layers also hold owner names and mailing addresses; these were deliberately left out. The county's two code tables (what each property class and building class number means) came from the county's ArcGIS Online account.

**How we know the code tables are really Jackson County's.** The code tables are on a generic ArcGIS address (`services1.arcgis.com/DwYBkWQPdaJNWrPG`), so this was checked separately:
- The ArcGIS catalog search showed the account owner is `JCGIS_Owner`, in the organisation "Jackson County GIS".
- The county's official open-data site (`gis.jacksoncountyor.gov`) lists both tables with those exact service addresses.

The exact download commands are in `README.md`.

## 2. Web research

Web searches and page reads were used to:
- Find the Jackson County GIS map layers and their field definitions.
- Find what the county property class and building class codes mean, and confirm the code tables are official.
- Identify places on the map. For example, the **Lausmann Annex** (200 S Ivy St) was confirmed as City of Medford building-department offices through the Southern Oregon builders' association directory (buildso.com).
- Find authoritative sources for every formula (section 4, Round 4).

When Jordan asked for business vs. house to be verified, they approved downloading the county assessor records. Each building's type now comes from its official county class, not from checking buildings one at a time. Places that appear on the map but not in OpenStreetMap's tags (for example the old Medford library and the merged Courthouse & County Offices) were added or changed on Jordan's instructions. They are listed in the "user edits" block of `raw data/scripts/build.py`.

## 3. Turning data into the map

All processing is done by nine small Python scripts in `raw data/scripts/`, run in a fixed order (listed in `README.md`):

1. **Shaded zone.** The loop of the route, plus everything within 152 m of the route line, plus three tapered bulges, minus two small notches. It is traced as one outline on a 2 m grid. The same outline is used both to draw the shading and to decide what counts as "inside".
2. **Building classes.** Each OpenStreetMap building outline is matched to the county parcel it sits on. It is then classed from that parcel's county records: house, duplex–fourplex, apartment, business, government, church, nonprofit, or garage/shed. Government, church and nonprofit are told apart by the parcel's owner type (city, county, state, school district, church, benevolent organisation…), as recorded in the county's property class.
3. **Places and bus stops.** Named places and bus stops inside the zone come from OpenStreetMap, plus Jordan's additions, removals and merges.
4. **Walk times.** For every home, the shortest walk along streets and alleys only (Dijkstra's shortest-path method) is found to the nearest place of each kind. Walk distances are turned into minutes at about 60 m/min (≈ 2.2 mph), the pace measured from Jordan's own photo timestamps.
5. **Page.** Everything is written into one self-contained HTML file, with the photos embedded.

## 4. Independent checking by AI agent teams

Rather than trusting the first calculation, the work was handed to separate teams of AI agents. These are independent instances of Claude, each starting fresh, with no access to the reasoning that produced the numbers. Each agent got the raw data and a description of what the page claims. It had to recompute the claims itself, writing its own scripts, and report anything wrong. Those scripts and their results are kept in `raw data/verification/`.

Three patterns were used:
- **Independent checkers.** Each one owns one area of the map and recomputes it from the raw data.
- **Skeptics.** Every problem a checker reports goes to three more agents whose job is to try to *refute* it by reproducing it themselves. A problem only counts if it survives.
- **Completeness critic.** It reads everything the checkers covered and lists what nobody checked. Extra "gap" agents then check those things.

### Round 1: full verification (151 agents, all finished)
- **6 checkers**, one per area: photos & route, zone geometry, places & bus stops, buildings, statistics, page behaviour.
- They reported **47 problems**: 5 errors, 14 inaccuracies, 28 minor issues.
- **141 skeptics** (3 per problem) tried to refute them. All 47 survived (0 refuted).
- **1 completeness critic** found 3 unchecked areas: what the density figure divides by, how sensitive park/school walk times are to the point chosen for a large area, and the block-label grouping. **3 gap agents** checked those.

Main problems found and then fixed:
- A church inside the zone (Christ Unity) was missing.
- Two-storey and basement duplex codes were dropped, so 26 duplex–fourplex buildings showed as houses.
- Extra apartment buildings in complexes showed as garages.
- Garages at the zone edge were counted as homes.
- Townhouse rows showed as single houses.
- Walk times were described as "along streets" but were actually straight-line estimates. They were switched to true street routing.
- The flat-map conversion understated distances by 0.6%.
- The Courthouse and County Offices were counted twice.
- A financial-advisor office was counted as a bank.
- Block labels overlapped photo pins.

### Round 2: re-check of the fixes (13 agents, all finished)
- **4 checkers** re-examined the changed parts: buildings, street-routed walk times, places, and the pages.
- They reported 3 significant problems (plus 11 minor ones). **9 skeptics** confirmed all 3:
  - cottage-court apartment units still showing as garages;
  - a block label spanning both sides of a dead-end street;
  - the bank count still including the advisor office.
- All three were fixed.

### Round 3: final check after layout changes (18 started, 10 finished)
- **4 checkers** re-examined the zone, places, statistics and page layout.
- They reported 6 problems to verify and 14 minor ones, mostly about the page layout. Examples: the zoom-out limit going stale after resizing the window, tooltips saying businesses were "not counted", and the walking method no longer being explained on the page.
- The 6 skeptics that finished all confirmed their problems.
- The run was **stopped early on purpose**: the problems it was confirming had already been fixed in the meantime, so the remaining 8 skeptics were not needed.

### Round 4: finding sources for every formula (63 agents, all finished)
- **7 researchers**, one per formula group: metres per degree of latitude/longitude, WGS 84 Earth-shape constants, the local flat-map approximation, Vincenty's distance method, acre and mile conversions, polygon area and point-in-polygon tests, and the algorithms (shortest path, outline tracing, line simplification). Each researcher found 4 authoritative sources (28 in total), preferring primary sources: NGA, NIST, USGS, IOGP, the original journal papers.
- **56 verifiers** (2 per source) each reopened the source on their own and confirmed it states the exact formula or value claimed.
- This produced one correction. The Bowditch navigation-table coefficients turned out to be computed for the older **WGS 72** Earth model, not WGS 84. `SOURCES.md` now says so, and gives the exact WGS 84 figures actually used (they agree to within 0.05 m).

| Run | Purpose | Started | Finished | Run time |
|---|---|---|---|---|
| 1 | Full verification | 151 | 151 | 73 min |
| 2 | Re-check of fixes | 13 | 13 | 17 min |
| 3 | Final check (stopped early) | 18 | 10 | 19 min |
| 4 | Formula sources | 63 | 63 | 13 min |
| **Total** | | **245** | **237** | **≈ 2 h** |

### Agent statistics: what the agents were assigned to

These figures come from the session's run logs. A "tool action" is one step an agent took: running one of its own scripts, reading a file, doing a web search, or opening a web page.

**By job**

| Job | What Jordan had them do | Agents started | Finished | Tool actions | Share of agents |
|---|---|---|---|---|---|
| Checkers | Own one area of the map and recompute it from the raw data | 14 | 14 | 573 | 6% |
| Skeptics | Try to refute each reported problem by reproducing it independently (3 per problem) | 164 | 156 | 1,754 | 67% |
| Completeness critic | List what no checker had verified | 1 | 1 | 21 | < 1% |
| Gap checkers | Check what the critic found missing | 3 | 3 | 85 | 1% |
| Source researchers | Find 4 authoritative sources for each formula group | 7 | 7 | 203 | 3% |
| Source verifiers | Reopen each source and confirm it says exactly what's claimed (2 per source) | 56 | 56 | 611 | 23% |
| **Total** | | **245** | **237** | **3,247** | **100%** |

**By subject**

Each row counts that subject's checkers and skeptics across all runs.

| Subject | Agents | Runs |
|---|---|---|
| Page behaviour and layout (icons, legend, labels, zoom, drawer, wording) | 41 | 1, 2, 3 |
| Building classes (houses, duplexes, apartments, businesses, garages) | 38 | 1, 2 |
| Places and bus stops | 36 | 1, 2, 3 |
| Statistics and walk times | 33 | 1, 2, 3 |
| Photos and route | 16 | 1 |
| Shaded-zone geometry and area | 14 | 1, 3 |
| Gaps the critic found (density, park/school walk points, block labels) | 4 | 1 |
| Formula sources (7 formula groups, 9 agents each) | 63 | 4 |

**How the effort was divided**
- **About three-quarters of the agents (182 of 245) checked the map itself.** The other quarter (63) found and confirmed sources for the formulas.
- **Two-thirds of all agents were skeptics.** Most of the effort went into trying to disprove reported problems rather than finding new ones. A problem had to be reproduced by independent skeptics before it counted.
- **The checking runs (1–3) used only local data.** Those agents worked offline from the downloaded files, writing and running their own scripts, with no web access.
- **Only Run 4 went online.** Its researchers and verifiers made 355 web searches and page reads.

## 5. Other checks

- **Visual testing.** The map was opened in a built-in browser at several window sizes, from phone to wide desktop. This checked icon overlap, the legend, the stats drawer, the zoom-out limit and click behaviour, and caught problems such as the zoom limit not fitting smaller windows.
- **Floating-point care.** One building-centre calculation lost precision with large coordinate numbers. It was rewritten to work relative to the building's first corner.
- **Reproducibility.** After every change, and after reorganising the folders, the whole map was rebuilt from `raw data/` with the scripts. The rebuild had to reproduce `analysis-and-map.html` exactly, byte for byte. This proves the published map comes only from the data and scripts in this folder.

## 6. Limits worth knowing

- OpenStreetMap and county records are only as current and complete as their volunteers and assessors make them. A few county dwelling records have no matching building outline, so homes may be slightly undercounted.
- Walk times use roads and alleys only (no cut-throughs across parking lots or parks), at one person's measured pace.
- Which places count as "services", and in which category, are editorial choices made by Jordan, not something the data decides.
- The verification agents are AI models. They are independent of each other and of the original work, and every reported problem had to be reproduced by several of them. Still, they are not a substitute for a human expert's review.
