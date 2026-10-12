import sys, re, json, math

def lit(html, name):
    m = re.search(r'const ' + name + r'\s*=\s*', html)
    i = m.end()
    dec = json.JSONDecoder()
    v, _ = dec.raw_decode(html[i:])
    return v

def proj(lat, lng, z):
    s = 256 * 2 ** z
    x = (lng + 180) / 360 * s
    sl = math.sin(math.radians(lat))
    y = (0.5 - math.log((1 + sl) / (1 - sl)) / (4 * math.pi)) * s
    return x, y

def unproj(x, y, z):
    s = 256 * 2 ** z
    lng = x / s * 360 - 180
    n = math.pi - 2 * math.pi * y / s
    lat = math.degrees(math.atan(math.sinh(n)))
    return lat, lng

def bounds_zoom(b, size, inside, pad=(0, 0), snap=0.25, zmin=0, zmax=19, z0=0):
    (s, w), (n, e) = b
    x1, y1 = proj(n, w, z0)
    x2, y2 = proj(s, e, z0)
    bx, by = abs(x2 - x1), abs(y2 - y1)
    sx = (size[0] - pad[0]) / bx
    sy = (size[1] - pad[1]) / by
    sc = max(sx, sy) if inside else min(sx, sy)
    z = z0 + math.log2(sc)
    z = round(z / (snap / 100)) * (snap / 100)
    z = math.ceil(z / snap) * snap if inside else math.floor(z / snap) * snap
    return max(zmin, min(zmax, z)), z0 + math.log2(sc)

def rebound(left, right):
    if left + right > 0:
        return round(left - right) / 2
    return max(0, math.ceil(left)) - max(0, math.floor(right))

def limit_center(c, z, size, mb):
    cx, cy = proj(c[0], c[1], z)
    hx, hy = size[0] / 2, size[1] / 2
    (s, w), (n, e) = mb
    mnx, mny = proj(n, w, z)
    mxx, mxy = proj(s, e, z)
    minoff = (mnx - (cx - hx), mny - (cy - hy))
    maxoff = (mxx - (cx + hx), mxy - (cy + hy))
    dx = rebound(minoff[0], -maxoff[0])
    dy = rebound(minoff[1], -maxoff[1])
    if abs(dx) <= 1 and abs(dy) <= 1:
        return c
    return unproj(cx + dx, cy + dy, z)

def bbox(pts):
    la = [p[0] for p in pts]; ln = [p[1] for p in pts]
    return ((min(la), min(ln)), (max(la), max(ln)))

html = open(sys.argv[1]).read()
route = lit(html, 'route')
rings = lit(html, 'zoneRings')
stops = lit(html, 'stops')
services = lit(html, 'services')
zpts = [p for r in rings for p in r]
ZB = bbox(zpts)
RB = bbox(route)
VIEW = ((42.3170, -122.8994), (42.3340, -122.8693))
print('zone bbox', ZB)
print('route bbox', RB)
ptsall = [(s['lat'], s['lng'], 'stop%s' % s['n']) for s in stops] + [(s['lat'], s['lng'], s.get('name', '?')) for s in services]

def px(b, z):
    (s, w), (n, e) = b
    x1, y1 = proj(n, w, z); x2, y2 = proj(s, e, z)
    return abs(x2 - x1), abs(y2 - y1)

pad = int(sys.argv[2]) if len(sys.argv) > 2 else 50
cases = [(a, b) for a, b in [tuple(map(int, c.split('x'))) for c in sys.argv[3:]]]
for (W, H) in cases:
    zmin, raw = bounds_zoom(VIEW, (W, H), True)
    zf, _ = bounds_zoom(RB, (W, H), False, pad=(2 * pad, 2 * pad), zmin=zmin)
    # fitBounds center
    swx, swy = proj(RB[0][0], RB[0][1], zf); nex, ney = proj(RB[1][0], RB[1][1], zf)
    c = unproj((swx + nex) / 2, (swy + ney) / 2, zf)
    c = limit_center(c, zf, (W, H), VIEW)
    cx, cy = proj(c[0], c[1], zf)
    top = unproj(cx, cy - H / 2, zf)[0]; bot = unproj(cx, cy + H / 2, zf)[0]
    left = unproj(cx - W / 2, cy, zf)[1]; right = unproj(cx + W / 2, cy, zf)[1]
    zw, zh = px(ZB, zmin)
    off = [nm for (la, ln, nm) in ptsall if not (bot <= la <= top and left <= ln <= right)]
    print(f'map {W}x{H}: minZoom raw {raw:.3f} -> {zmin}; zone at min {zw:.0f}x{zh:.0f}px fits={zw<=W and zh<=H}; '
          f'initial zoom {zf} view lat {bot:.5f}-{top:.5f} lng {left:.5f}-{right:.5f}; '
          f'zone cut top {max(0,(ZB[1][0]-top))*111079.6:.0f} m bottom {max(0,(bot-ZB[0][0]))*111079.6:.0f} m; off-view: {off}')
