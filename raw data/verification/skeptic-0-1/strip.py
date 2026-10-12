import sys, re
# print HTML with long base64 data URIs / long literal lines truncated, to inspect code only
for p in sys.argv[1:]:
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', 'data:IMG', t)
    lines = t.split('\n')
    out = p.replace('/', '_')
    for i, l in enumerate(lines, 1):
        if len(l) > 600: l = l[:600] + ' ...[%d chars]' % len(l)
        print('%s:%d: %s' % (p.rsplit('/',1)[-1], i, l))
