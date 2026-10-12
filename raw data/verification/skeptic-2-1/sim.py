# Independent re-implementation of Leaflet 1.9.4 Map.getBoundsZoom / getMinZoom / setMinZoom / getSize
# semantics (from memory of the 1.9.4 source) to replay the page code paths.
import math, json, re, sys

def proj(lat, lng, z):
    s = 256 * 2 ** z
    x = s * (0.5 + lng / 360)
    sl = math.sin(math.radians(lat))
    y = s * (0.5 - 0.25 / math.pi * math.log((1 + sl) / (1 - sl)))
    return x, y

VIEW = ((42.3170, -122.8994), (42.3340, -122.8693))

class Map:
    def __init__(self, w, h):
        self.container = [w, h]   # real DOM size
        self._size = None
        self._sizeChanged = True
        self.minZoom = None       # options.minZoom
        self.zoom = None
        self.snap = 0.25
    def getSize(self):
        if self._size is None or self._sizeChanged:
            self._size = list(self.container); self._sizeChanged = False
        return list(self._size)
    def getMinZoom(self):
        return 0 if self.minZoom is None else self.minZoom
    def getBoundsZoom(self, b, inside, pad=(0, 0)):
        zoom = self.zoom or 0
        mn, mx = self.getMinZoom(), 19
        (s, w), (n, e) = b
        size = self.getSize(); size = [size[0] - pad[0], size[1] - pad[1]]
        x1, y1 = proj(n, w, zoom); x2, y2 = proj(s, e, zoom)
        bx, by = abs(x2 - x1), abs(y2 - y1)
        sx, sy = size[0] / bx, size[1] / by
        scale = max(sx, sy) if inside else min(sx, sy)
        z = zoom + math.log2(scale)
        snap = self.snap
        z = round(z / (snap / 100)) * (snap / 100)
        z = math.ceil(z / snap) * snap if inside else math.floor(z / snap) * snap
        return max(mn, min(mx, z))
    def setMinZoom(self, z):
        old = self.minZoom; self.minZoom = z
        if self.zoom is not None and old != z and self.zoom < z:
            self.zoom = z
    def invalidateSize(self):
        if self.zoom is None: return
        self._sizeChanged = True
        self.getSize()
    def fitMinZoom(self):
        self.setMinZoom(self.getBoundsZoom(VIEW, True))
    def fitMinZoomFixed(self):
        self.minZoom = 0
        self.setMinZoom(self.getBoundsZoom(VIEW, True))

def true_min(w, h):
    m = Map(w, h); return m.getBoundsZoom(VIEW, True)

def pxw(b, z):
    (s, w), (n, e) = b
    x1, y1 = proj(n, w, z); x2, y2 = proj(s, e, z)
    return abs(x2 - x1), abs(y2 - y1)

# zone outline bounds from the services page
s = open(sys.argv[1], encoding='utf-8').read()
m = re.search(r'const zoneRings\s*=\s*(\[.*?\]\]\]);', s, re.S)
rings = json.loads(m.group(1))
lats = [p[0] for r in rings for p in r]; lngs = [p[1] for r in rings for p in r]
ZB = ((min(lats), min(lngs)), (max(lats), max(lngs)))
print('zone bounds', ZB)
print('VIEW px at z0', pxw(VIEW, 0))

def scenario(name, w0, h0, w1, h1, route_pad=50):
    m = Map(w0, h0)
    # fit(): invalidateSize (no-op before load), fitMinZoom, fitBounds sets zoom
    m.fitMinZoom()
    m.zoom = max(m.getMinZoom(), 16)  # arbitrary current zoom >= min
    before = m.minZoom
    # window resize: DOM changes; page listener runs synchronously before Leaflet's rAF invalidateSize
    m.container = [w1, h1]
    m.fitMinZoom()
    after_listener = m.minZoom
    m.invalidateSize()  # Leaflet's rAF; page does not re-run fitMinZoom
    print(f'{name}: {w0}x{h0} -> {w1}x{h1}: minZoom before {before}, after resize {after_listener}, '
          f'correct {true_min(w1, h1)}; VIEW width at shown min = {pxw(VIEW, after_listener)[0]:.0f}px '
          f'vs map {w1}px')

scenario('services desktop', 1440, 569, 1920, 691)
scenario('photo desktop', 1100 - 340, 790, 1560 - 340, 960)
scenario('services shrink', 1920, 691, 1440, 569)

# phone toggle
m = Map(390, 398)
m.fitMinZoom(); start = m.minZoom
m.zoom = start
print('phone start minZoom', start, 'zone px', [round(v) for v in pxw(ZB, start)])
# Hide stats: map becomes 390 x (663-31)
m.container = [390, 632]; m.invalidateSize(); m.fitMinZoom(); hid = m.minZoom
m.container = [390, 398]; m.invalidateSize(); m.fitMinZoom(); shown = m.minZoom
print('after hide', hid, 'after show', shown, 'correct', true_min(390, 398),
      'zone px at stuck min', [round(v) for v in pxw(ZB, shown)], 'zoom now', m.zoom)
# with suggested fix
m2 = Map(390, 398); m2.fitMinZoomFixed(); m2.zoom = m2.minZoom
m2.container = [390, 632]; m2.invalidateSize(); m2.fitMinZoomFixed(); a = m2.minZoom
m2.container = [390, 398]; m2.invalidateSize(); m2.fitMinZoomFixed(); b = m2.minZoom
print('fixed: hide', a, 'show', b)
for w, h in [(390, 398), (390, 632), (390, 633), (1440, 569), (1920, 691), (760, 790), (1220, 960)]:
    z = true_min(w, h); print(w, h, 'min', z, 'VIEW px', [round(v) for v in pxw(VIEW, z)], 'zone px', [round(v) for v in pxw(ZB, z)])
