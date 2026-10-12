import json,re,sys,math
page,widths,blocksf=sys.argv[1:4]
t=open(page).read(); W=json.load(open(widths)); B=json.load(open(blocksf))
def lit(name): return json.loads(re.search(r"const "+name+r" = (.*?);\n",t,re.S).group(1))
sv=lit("services"); bus=lit("busStops")
stops=[(float(a),float(b)) for a,b in re.findall(r"\{ n:\d, lat:([\d.]+), lng:(-[\d.]+)",t)]
COLORS=["Health & social services","Government & courts","Education","Places of worship","Recreation & parks","Banking & finance","Arts & culture"]
def proj(lat,lng,z):
    s=256*2**z; x=s*(lng+180)/360; r=math.radians(lat); y=s*(1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2; return x,y
marks=[]
for b in B:
    tw=(W['b%d'%b['h']] if b['h'] else 0)+((W['space'] if b['h'] else 0)+W['s+%d'%b['a']] if b['a'] else 0)
    marks.append(dict(kind='bubble',ll=(b['lat'],b['lng']),w=tw+13,h=19,label=f"{b['h']}+{b['a']}"))
for la,ln in stops: marks.append(dict(kind='pin',ll=(la,ln),w=26,h=26,label='pin'))
for b in bus: marks.append(dict(kind='icon',ll=(b['lat'],b['lng']),w=26,h=26,label='bus:'+b['name']))
for cat in COLORS:
    for s in sorted([s for s in sv if s['cat']==cat],key=lambda s:s['name'].lower()):
        marks.append(dict(kind='icon',ll=(s['lat'],s['lng']),w=22,h=22,label=s['name']))
PRI={'pin':0,'icon':1,'bubble':2}
def run(z):
    s=1 if z>=17 else .85 if z>=16 else .72
    live=[m for m in marks if m['kind']!='bubble' or z>=16]
    box=[]
    for m in live:
        x,y=proj(*m['ll'],z); box.append(dict(x=x,y=y,w=m['w']*s,h=m['h']*s,pri=PRI[m['kind']],x0=x,y0=y,m=m))
    GAP=2; it_used=None
    for it in range(80):
        moved=False
        for i in range(len(box)):
            for j in range(i+1,len(box)):
                a,b=box[i],box[j]; dx=b['x']-a['x']; dy=b['y']-a['y']
                px=(a['w']+b['w'])/2+GAP-abs(dx); py=(a['h']+b['h'])/2+GAP-abs(dy)
                if px<=0 or py<=0: continue
                if a['pri']==0 and b['pri']==0: continue
                if a['pri']==b['pri']: sa=sb=.5
                elif a['pri']<b['pri']: sa,sb=0,1
                else: sa,sb=1,0
                if px<py:
                    sg=(1 if dx>=0 else -1)*px; a['x']-=sg*sa; b['x']+=sg*sb
                else:
                    sg=(1 if dy>=0 else -1)*py; a['y']-=sg*sa; b['y']+=sg*sb
                moved=True
        if not moved: it_used=it; break
    # overlaps (true overlap, no gap)
    bad=[]
    for i in range(len(box)):
        for j in range(i+1,len(box)):
            a,b=box[i],box[j]
            ox=(a['w']+b['w'])/2-abs(b['x']-a['x']); oy=(a['h']+b['h'])/2-abs(b['y']-a['y'])
            if ox>0.01 and oy>0.01 and not (a['pri']==0 and b['pri']==0):
                bad.append((round(min(ox,oy),1),a['m']['label'][:30],b['m']['label'][:30]))
    disp=max((math.hypot(b['x']-b['x0'],b['y']-b['y0']),b['m']['label']) for b in box if b['pri']==1)
    dispb=max((math.hypot(b['x']-b['x0'],b['y']-b['y0']),b['m']['label']) for b in box if b['pri']==2) if z>=16 else (0,'')
    print(f"z={z:5.2f} s={s} live={len(live)} converged_at_iter={it_used} overlaps_left={len(bad)} {bad[:6]} max icon shift={disp[0]:.0f}px ({disp[1][:28]}) max bubble shift={dispb[0]:.0f}px")
for z in [x/4 for x in range(58,77)]: run(z)
