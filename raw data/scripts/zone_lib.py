# Shared zone test. Load with: exec(open(S + "/scripts/zone_lib.py").read()) after defining S.
# Provides ZONE_KX, ZONE_KY, zone_xy(lat,lng) -> metres, in_zone(lat, lng), in_zone_xy(x, y), ZONE_M2.
import json as _json
ZONE_KX, ZONE_KY = 82427.8, 111079.6
_Z = _json.load(open(S + "/outputs/zone.json"))
_ZR = [[(lng * ZONE_KX, lat * ZONE_KY) for lat, lng in ring] for ring in _Z["rings"]]
_ZB = [(min(p[0] for p in r), min(p[1] for p in r), max(p[0] for p in r), max(p[1] for p in r)) for r in _ZR]
ZONE_M2 = _Z["m2"]
def zone_xy(lat, lng): return (lng * ZONE_KX, lat * ZONE_KY)
def in_zone_xy(x, y):
    c = False
    for r, (x0, y0, x1, y1) in zip(_ZR, _ZB):
        if not (x0 <= x <= x1 and y0 <= y <= y1): continue
        for (ax, ay), (bx, by) in zip(r, r[1:]):
            if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax: c = not c
    return c
def in_zone(lat, lng): return in_zone_xy(lng * ZONE_KX, lat * ZONE_KY)
