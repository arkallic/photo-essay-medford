import sys,re,html
for p in sys.argv[1:]:
    s=open(p,encoding='utf-8').read()
    # strip scripts and styles
    body=re.sub(r'<script.*?</script>','',s,flags=re.S)
    body=re.sub(r'<style.*?</style>','',body,flags=re.S)
    txt=re.sub(r'<[^>]+>',' ',body)
    txt=html.unescape(re.sub(r'\s+',' ',txt))
    print('=====',p,len(txt))
    print(txt[:20000])
