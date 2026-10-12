import sys, json, math, time
S, V = sys.argv[1], sys.argv[2]
exec(open(V + "/myzone.py").read())
# route simplicity
def inter(p1,p2,p3,p4):
    def o(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    d1,d2,d3,d4=o(p3,p4,p1),o(p3,p4,p2),o(p1,p2,p3),o(p1,p2,p4)
    return (d1*d2<0) and (d3*d4<0)
n=len(SEGS); bad=[]
for i in range(n):
    for j in range(i+2,n):
        if i==0 and j==n-1: continue
        if inter(*SEGS[i],*SEGS[j]): bad.append((i,j))
print("route segs",n,"self-intersections",bad, "closed", ROUTE[0]==ROUTE[-1])
for b in BULGES: print("bulge",b["name"],"rend %.2f L %.2f P0"%(b["rend"],b["L"]), LL(*b["P0"]))
for nt in NOTCHES: print("notch",nt["name"],"depth %.2f r %.2f"%(nt["depth"],nt["r"]))
