import sys, json, math
S, V = sys.argv[1], sys.argv[2]
exec(open(V + "/myzone.py").read())
page = json.load(open(V + "/lits_services.json"))["zoneRings"]
pts = [P(lat, lng) for lat, lng in page[0]][:-1]; n=len(pts)
def info(i):
    x,y=pts[i]
    s = "band %.2f" % (BUF - droute(x,y))
    for k,b in enumerate(BULGES): 
        sd = bulge_sd(x,y,b)
        if abs(sd) < 30: s += " | bulge%d %.2f (dT %.2f)" % (k+1, -sd, math.dist((x,y),b["T"])-b["rend"])
    for k,nt in enumerate(NOTCHES):
        d = math.dist((x,y),nt["c"])-nt["r"]
        if abs(d)<30: s += " | notch%d %.2f" % (k+1, d)
    return s
for rng in [range(130,170), range(0,2)]:
    for i in rng:
        print("v%d"%i, LL(*pts[i]), info(i))
    print()
