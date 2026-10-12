import json,re,sys
t=open(sys.argv[1]).read(); W=json.load(open(sys.argv[2]))
sv=json.loads(re.search(r"const services = (.*?);\n",t,re.S).group(1))
LAB={"cross":"Church","gov":"Government office","scales":"Court","shield":"Jail / police","medical":"Medical clinic","apple":"Food pantry","people":"Community center","school":"School","tree":"Park","track":"Field & track","run":"Fitness center","money":"Bank / finance","mask":"Theater","book":"Library (historic)"}
COL={"Health & social services":"pink","Government & courts":"purple","Education":"blue","Places of worship":"brown","Recreation & parks":"green","Banking & finance":"teal","Arts & culture":"orange"}
used=[]
for s in sv:
    if s["icon"] not in used: used.append(s["icon"])
print("legend icon order + color (first service with icon):")
for k in used:
    first=next(s for s in sv if s["icon"]==k); others=sorted(set(COL[s["cat"]] for s in sv if s["icon"]==k))
    print(f"  {k:8} {LAB[k]:20} legend color={COL[first['cat']]:7} (from {first['name'][:40]}); colors on map={others}")
labels=["Photo (in order)","Bus stop"]+[LAB[k] for k in used]
for fs,maxw in [(11.5,290),(11,250)]:
    key='L11.5:' if fs==11.5 else 'L11:'
    maxcontent=2*max(17+5+W[key+l] for l in labels)+10+18
    width=min(maxcontent,maxw); col=(width-18-10)/2; txt=col-22
    rows=[labels[i:i+2] for i in range(0,len(labels),2)]
    lh=1.2*fs
    hts=[max(17, max(lh*(2 if W[key+l]>txt else 1) for l in r)) for r in rows]
    wrapped=[l for l in labels if W[key+l]>txt]
    H=(5+5+fs*1.35)+sum(hts)+3*(len(rows)-1)+7
    print(f"font {fs}px: width {width:.0f}px (max-content {maxcontent:.0f}), text col {txt:.0f}px, wrapped={wrapped}, height≈{H:.0f}px, bottom edge at y≈{H+10:.0f}px")
# map key
rows=[W['K12:'+l]+11+6+18 for l in ['House','Duplex to fourplex','Apartment building','Garage or shed','Business','Public building']]
bub=W['b12']+W['space']+W['s+3']+13
kb=bub+5+W['K12:per block: houses ']-W['K12:'+'House']*0+5+W['K12b:+ multi-unit']+18
print(f"map key width≈{max(max(rows),kb):.0f}px, height≈{6*18+3+max(18,19)+12:.0f}px -> top edge at map_h-{6*18+3+19+12+10:.0f}")
