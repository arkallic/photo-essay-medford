import sys, re
from html.parser import HTMLParser
for p in sys.argv[1:]:
    src=open(p,encoding='utf-8').read()
    css=src[:src.find('</style>')]
    print('==',p.split('/')[-1])
    print(' css order/flex-direction/grid-row/display:none on relevant classes:',
          re.findall(r'[^\n]*(?:\border\s*:|flex-direction|grid-row|column-reverse)[^\n]*',css))
    print(' homes-d hidden?', bool(re.search(r'\.homes-d[^{]*\{[^}]*display\s*:\s*none',css)))
    class P(HTMLParser):
        def __init__(s): super().__init__(); s.seq=[]; s.cur=None; s.buf=''
        def handle_starttag(s,t,a):
            c=dict(a).get('class') or ''
            if c in ('tile sum-t','tile','howto','homes-d'): s.seq.append([c,'']); s.cur=s.seq[-1]
        def handle_data(s,d):
            if s.cur is not None and len(s.cur[1])<60: s.cur[1]+=d
    pp=P(); pp.feed(src)
    for i,(c,t) in enumerate(pp.seq): print(f'  {i:2d} {c:12s} {t[:55]!r}')
    hd=[i for i,(c,_) in enumerate(pp.seq) if c=='homes-d'][0]
    for name in ('Homes','Density','Other buildings'):
        i=[k for k,(c,t) in enumerate(pp.seq) if c=='tile sum-t' and t.startswith(name)][0]
        print(f'  {name}: block index {i}, homes-d index {hd}, tiles between = {sum(1 for c,_ in pp.seq[i+1:hd] if c.startswith("tile"))}')
    m=re.search(r'<div class="homes-d">(.*?)</div>',src,re.S); print('  homes-d text:',re.sub('<[^>]+>','',m.group(1)))
    js=src[src.find('</style>'):]
    print('  JS touching homes-d/sum (moving nodes?):',re.findall(r'[^\n;]*(?:homes-d|\.sum\b|insertBefore|prepend\()[^\n;]*',js)[:5])
