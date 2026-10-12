import math
def proj(lat,lng,z):
    s=256*2**z; x=s*(lng+180)/360; r=math.radians(lat); y=s*(1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2; return x,y
VIEW=((42.3170,-122.8994),(42.3340,-122.8693))
ZONE=((42.3211423,-122.8894307),(42.3297731,-122.8740046))
ROUTE=((42.32251,-122.887588),(42.328405,-122.8760241))
def size(b,z):
    (s,w),(n,e)=b; x0,y0=proj(n,w,z); x1,y1=proj(s,e,z); return x1-x0,y1-y0
def boundszoom(b,W,H,inside,pad=0,snap=.25,minz=0):
    bw,bh=size(b,0); sx=(W-pad)/bw; sy=(H-pad)/bh; sc=max(sx,sy) if inside else min(sx,sy)
    z=math.log2(sc); z=round(z/(snap/100))*(snap/100); z=math.ceil(z/snap)*snap if inside else math.floor(z/snap)*snap
    return max(minz,min(19,z))
cases=[("MacBook Air 13 (1440x900, viewport ~1440x790)",1440,0.72*790),("1920x1080 monitor (viewport ~1920x960)",1920,0.72*960),
       ("1280x800 laptop (viewport ~1280x700)",1280,max(420,0.72*700)),("iPad portrait 820x1180 (viewport ~820x1100)",820,0.72*1100),
       ("iPhone 14 portrait 390x664 viewport",390,max(320,0.60*664)),("iPhone landscape 844x340 viewport",844,max(320,0.6*340)),
       ("2560x1440 (viewport ~2560x1300)",2560,0.72*1300)]
for name,W,H in cases:
    zmin=boundszoom(VIEW,W,H,True)
    zw,zh=size(ZONE,zmin); rw,rh=size(ROUTE,zmin)
    zfit=boundszoom(ROUTE,W,H,False,pad=100,minz=zmin)
    rw2,rh2=size(ROUTE,zfit); zw2,zh2=size(ZONE,zfit)
    print(f"{name}: map {W}x{H:.0f} minZoom {zmin}; at minZoom zone {zw:.0f}x{zh:.0f}px fits={zw<=W and zh<=H}; initial zoom {zfit} route+pad {rw2+100:.0f}x{rh2+100:.0f} fits={rw2+100<=W and rh2+100<=H}; zone at initial {zw2:.0f}x{zh2:.0f}")
print("--- previous layout (map = window width - 360 px sidebar, full height) ---")
for name,W,H in [("MacBook 1440x790",1440-360,790),("1920x960",1920-360,960),("1280x700",1280-360,700)]:
    zmin=boundszoom(VIEW,W,H,True); zw,zh=size(ZONE,zmin)
    print(f"{name}: map {W}x{H} minZoom {zmin} zone {zw:.0f}x{zh:.0f} fits={zw<=W and zh<=H}")
print("--- zoom at which zone fits, current layout ---")
for name,W,H in cases[:3]:
    print(name, boundszoom(ZONE,W,H,False,pad=0))
# visible lat range at min zoom on MacBook centered on zone
