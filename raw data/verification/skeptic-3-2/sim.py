import sys, re, json, math
R = 6378137.0
def proj(lat, lng, z):
    # Leaflet EPSG3857 -> pixel at zoom z
    d = math.pi/180
    maxlat = 85.0511287798
    lat = max(min(maxlat, lat), -maxlat)
    s = math.sin(lat*d)
    x = R*lng*d
    y = R*math.log((1+s)/(1-s))/2
    sc = 256*2**z
    k = 0.5/(math.pi*R)
    return (sc*(k*x+0.5), sc*(-k*y+0.5))
def unproj(px, py, z):
    sc = 256*2**z; k = 0.5/(math.pi*R)
    x = (px/sc-0.5)/k; y = (py/sc-0.5)/(-k)
    d = 180/math.pi
    return ((2*math.atan(math.exp(y/R))-math.pi/2)*d, x*d/R)

def bounds_zoom(b, size, inside, snap=0.25, cur=0, minz=0, maxz=19, padding=(0,0)):
    (s,w),(n,e) = b
    a = proj(n, w, cur); c = proj(s, e, cur)
    bx = abs(c[0]-a[0]); by = abs(c[1]-a[1])
    sx = (size[0]-padding[0])/bx; sy = (size[1]-padding[1])/by
    scale = max(sx,sy) if inside else min(sx,sy)
    z = cur + math.log2(scale)  # getScaleZoom (crs.zoom(scale*crs.scale(cur)))
    z = round(z/(snap/100))*(snap/100)
    z = math.ceil(z/snap)*snap if inside else math.floor(z/snap)*snap
    return max(minz, min(maxz, z))

def load(path):
    t = open(path, encoding='utf-8').read()
    def lit(name):
        m = re.search(r'const '+name+r'\s*=\s*', t)
        i = m.end(); depth=0; j=i
        # bracket match
        opener = t[i]
        for j in range(i, len(t)):
            ch = t[j]
            if ch in '[{': depth+=1
            elif ch in ']}':
                depth-=1
                if depth==0: break
        return t[i:j+1]
    zr = json.loads(lit('zoneRings'))
    rt = json.loads(lit('route'))
    sv = lit('services')
    return t, zr, rt, sv

t, zr, rt, sv = load(sys.argv[1])
pts = [p for ring in zr for p in ring]
zs, zn = min(p[0] for p in pts), max(p[0] for p in pts)
zw, ze = min(p[1] for p in pts), max(p[1] for p in pts)
print("zone bounds lat %.5f-%.5f lng %.5f..%.5f" % (zs, zn, zw, ze))
rs, rn = min(p[0] for p in rt), max(p[0] for p in rt)
rw, re_ = min(p[1] for p in rt), max(p[1] for p in rt)
print("route bounds lat %.6f-%.6f lng %.6f..%.6f" % (rs, rn, rw, re_))
# services coords near top
names = re.findall(r'name:\s*"([^"]+)"[^}]*?lat:\s*([\d.]+),\s*lng:\s*(-[\d.]+)', sv)
if not names:
    names = re.findall(r'"name":\s*"([^"]+)"[^}]*?"lat":\s*([\d.]+),\s*"lng":\s*(-[\d.]+)', sv)
svc = [(n, float(a), float(b)) for n,a,b in names]
print("services parsed:", len(svc))
VIEW = ((42.3170, -122.8994), (42.3340, -122.8693))

def sim(W, H, label):
    minz = bounds_zoom(VIEW, (W,H), True)
    # zone px size at minz
    a = proj(zn, zw, minz); c = proj(zs, ze, minz)
    zwpx, zhpx = c[0]-a[0], c[1]-a[1]
    # initial view: fitBounds(route, padding 50) -> zoom clamped to [minz, 19]
    rz = bounds_zoom(((rs,rw),(rn,re_)), (W,H), False, padding=(100,100), minz=minz)
    # center: leaflet _getBoundsCenterZoom: paddingOffset = (br - tl)/2 = 0 for symmetric padding; center = unproject((swPoint+nePoint)/2)
    sw = proj(rs, rw, rz); ne = proj(rn, re_, rz)
    cx, cy = (sw[0]+ne[0])/2, (sw[1]+ne[1])/2
    # maxBounds: panInsideBounds -> clamp center so view inside VIEW
    vnw = proj(VIEW[1][0], VIEW[0][1], rz); vse = proj(VIEW[0][0], VIEW[1][1], rz)
    def clamp(c, lo, hi, half):
        if hi-lo < 2*half: return (lo+hi)/2
        return min(max(c, lo+half), hi-half)
    cx = clamp(cx, vnw[0], vse[0], W/2); cy = clamp(cy, vnw[1], vse[1], H/2)
    top = unproj(cx, cy-H/2, rz)[0]; bot = unproj(cx, cy+H/2, rz)[0]
    left = unproj(cx-W/2, cy, rz)[1]; right = unproj(cx+W/2, cy, rz)[1]
    fits = zwpx <= W and zhpx <= H
    off = [n for n,la,lo in svc if not (bot <= la <= top and left <= lo <= right)]
    print(f"{label}: map {W}x{H} minZoom {minz} zone {zwpx:.0f}x{zhpx:.0f}px fits={fits}; initial zoom {rz} view lat {bot:.5f}-{top:.5f} lng {left:.5f}..{right:.5f}; zone cut top {max(0,zn-top)*111079.6:.0f} m, bottom {max(0,bot-zs)*111079.6:.0f} m; icons off-view: {off}")
    # also: any pan position that shows the whole zone?
    return minz

vh = {'MacBook Air 1440x900 (viewport ~1440x790)':(1440,790), '1920x1080 (viewport ~1920x960)':(1920,960), '1280x800 (viewport ~1280x700)':(1280,700), '1536x864 (viewport 1536x730)':(1536,730), '1366x768 (viewport 1366x657)':(1366,657), '2560x1440 (viewport 2560x1300)':(2560,1300), '1728x1117 MBP16 (viewport 1728x1000)':(1728,1000), '1512x982 MBP14 (viewport 1512x870)':(1512,870)}
mode = sys.argv[2]
for k,(W,Hv) in vh.items():
    if mode=='under':
        H = max(420, round(0.72*Hv)) if W>760 else max(320, round(.6*Hv))
        sim(W, H, k+' [stats under]')
        sim(W, Hv-31, k+' [stats hidden]')
    else:
        sim(W-360 if W>760 else W, Hv, k+' [sidebar]')
