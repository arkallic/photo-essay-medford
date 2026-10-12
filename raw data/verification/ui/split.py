import re,sys,os
out=sys.argv[1]
for f in sys.argv[2:]:
    t=open(f).read(); b=os.path.basename(f).replace('.html','')
    scripts=[m.group(2) for m in re.finditer(r'<script([^>]*)>(.*?)</script>',t,re.S) if m.group(2).strip()]
    open(f'{out}/{b}.js','w').write(scripts[0])
    # stripped version: data URIs shortened
    s=re.sub(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', 'DATAURI', t)
    # shorten very long json literals
    open(f'{out}/{b}.stripped.html','w').write(s)
    print(b, len(t), len(s))
