import math,json,re,sys
t=open(sys.argv[1]).read()
sv=json.loads(re.search(r"const services = (.*?);\n",t,re.S).group(1))
def proj(lat,lng,z):
    s=256*2**z; x=s*(lng+180)/360; r=math.radians(lat); y=s*(1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2; return x,y
def unlat(y,z):
    s=256*2**z; n=math.pi-2*math.pi*y/s; return math.degrees(math.atan(math.sinh(n)))
for W,H,z,label in [(1440,569,16.25,"MacBook 1440x900"),(1920,691,16.5,"1920x1080")]:
    c=((42.32251+42.328405)/2,(-122.887588-122.8760241)/2)
    cx,cy=proj(*c,z); top=unlat(cy-H/2,z); bot=unlat(cy+H/2,z)
    print(label,"visible lat",round(bot,5),"to",round(top,5),"span m",round((top-bot)*111079.6),"zone span m",round((42.3297731-42.3211423)*111079.6))
    out=[s["name"] for s in sv if not (bot<=s["lat"]<=top)]
    print("  icons outside initial/min-zoom view:",out)
