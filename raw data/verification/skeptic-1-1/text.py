import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in ('script','style'): s.skip+=1
        if t in ('div','p','li','br','h1','h2','h3','section','table','tr'): s.out.append('\n')
    def handle_endtag(s,t):
        if t in ('script','style'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
for f in sys.argv[1:]:
    src=open(f,encoding='utf8').read()
    p=P(); p.feed(src)
    txt=re.sub(r'\n\s*\n+','\n',''.join(p.out))
    print('=====',f); print(txt[:20000])
    # also search scripts for strings mentioning walk/edge/alley/street/path
    for m in re.finditer(r'(?i)[^"\'<>]{0,120}(alley|footpath|footway|edge|street network|streets and|sidewalk|straight)[^"\'<>]{0,120}', src):
        s=m.group(0)
        if len(s)<400 and 'lat' not in s: print('  HIT:',s.strip()[:300])
