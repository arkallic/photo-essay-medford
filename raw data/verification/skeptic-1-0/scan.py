import sys,re
pat=re.compile(r'(alley|footpath|footway|sidewalk|street|road|edge|path|driveway|parking|straight|walks? (follow|use)|measured|boundary)',re.I)
for p in sys.argv[1:]:
    s=open(p,encoding='utf-8').read()
    print('=====',p)
    # remove huge numeric arrays: skip lines longer than 5000 chars but scan them for words in quotes
    for m in re.finditer(r'title="[^"]*"|aria-label="[^"]*"',s):
        if pat.search(m.group(0)): print('ATTR',m.group(0)[:300])
    for sm in re.finditer(r'<script[^>]*>(.*?)</script>',s,re.S):
        js=sm.group(1)
        for q in re.finditer(r"'[^'\n]{0,400}'|\"[^\"\n]{0,400}\"|`[^`]{0,2000}`",js):
            t=q.group(0)
            if pat.search(t) and len(t)<2000: print('JS',t[:400])
