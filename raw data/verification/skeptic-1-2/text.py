import sys, re, html
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    # strip big data scripts but keep strings in JS that may generate text
    body = re.sub(r'<style.*?</style>', '', s, flags=re.S)
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', body, flags=re.S)
    nos = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', nos)
    txt = html.unescape(re.sub(r'\s+', ' ', txt))
    print('=====', p, len(s))
    print('VISIBLE TEXT:', txt[:6000])
    # JS strings containing keywords (excluding huge data)
    print('--- JS strings with keywords')
    for sc in scripts:
        if len(sc) > 200000:
            # drop data literals
            sc2 = re.sub(r'\[[\d\.,\-\[\]\s]{200,}\]', '[..]', sc)
        else:
            sc2 = sc
        for m in re.finditer(r"(['\"`])((?:(?!\1).){0,600}?(?:alley|street|edge|footpath|ground|walk|minute|pace|path)(?:(?!\1).){0,600}?)\1", sc2, flags=re.I):
            print('  JS:', m.group(2)[:700])
