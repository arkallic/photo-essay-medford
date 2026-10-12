import sys,re
for p in sys.argv[1:]:
    s=open(p,encoding='utf-8').read()
    a=s.index('<div class="homes">'); b=s.index('<div id="list">',a)
    blk=s[a:b]
    seq=[]
    for m in re.finditer(r'<div class="(tile sum-t|tile|howto|homes-d)">(?:<div class="t-h">([^<]*))?',blk):
        seq.append((m.group(1),(m.group(2) or '').strip()))
    print(p.split('/')[-1])
    for i,(c,h) in enumerate(seq): print(' ',i,c,h)
    hd=[i for i,(c,_) in enumerate(seq) if c=='homes-d'][0]
    print('  homes-d position',hd,'of',len(seq),'; tiles between Homes tile and homes-d:',hd-1)
