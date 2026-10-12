import sys,re
from html.parser import HTMLParser
VOID={"meta","link","br","img","input","hr"}
for f in sys.argv[1:]:
    t=open(f).read()
    class P(HTMLParser):
        def __init__(s): super().__init__(); s.stack=[]; s.err=[]; s.ids=[]
        def handle_starttag(s,tag,a):
            d=dict(a)
            if "id" in d: s.ids.append(d["id"])
            if tag not in VOID: s.stack.append((tag,s.getpos()))
        def handle_endtag(s,tag):
            if tag in VOID: return
            if s.stack and s.stack[-1][0]==tag: s.stack.pop()
            else: s.err.append((tag,s.getpos(),[x[0] for x in s.stack[-3:]]))
    p=P(); p.feed(t); p.close()
    print(f.split('/')[-1], "unclosed:",p.stack,"mismatched:",p.err[:5],"dup ids:",[i for i in set(p.ids) if p.ids.count(i)>1])
