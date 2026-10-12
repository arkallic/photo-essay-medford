import sys,json,re,collections
t=open(sys.argv[1]).read()
ring=json.loads(re.search(r"const zoneRings = (.*?);\n",t,re.S).group(1))[0]
B=json.loads(re.search(r"const BLDG = (.*?);\n",t,re.S).group(1))
K=json.loads(re.search(r"const BLOCKS = (.*?);\n",t,re.S).group(1))
xy=lambda p:(p[1]*82427.8,p[0]*111079.6)
R=[xy(p) for p in ring]
def inside(p):
    x,y=xy(p); c=False
    for (ax,ay),(bx,by) in zip(R,R[1:]):
        if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax: c=not c
    return c
def centroid(pts):
    P0=[xy(p) for p in pts]; ox,oy=P0[0]; P=[(x-ox,y-oy) for x,y in P0]; A=cx=cy=0
    for (x0,y0),(x1,y1) in zip(P,P[1:]):
        c=x0*y1-x1*y0; A+=c; cx+=(x0+x1)*c; cy+=(y0+y1)*c
    if abs(A)<1e-9: x=sum(p[0] for p in P)/len(P); y=sum(p[1] for p in P)/len(P)
    else: x=cx/(3*A); y=cy/(3*A)
    return ((y+oy)/111079.6, (x+ox)/82427.8)
cnt=collections.Counter(c for c,_ in B); out=collections.Counter(c for c,p in B if not inside(centroid(p)))
print("BLDG counts",dict(cnt),"centroid outside zone",dict(out))
print("BLOCKS outside zone",[k for k in K if not inside((k["lat"],k["lng"]))])
