import sys, re
for p in sys.argv[1:]:
    t = open(p, encoding='utf-8').read()
    lines = t.split('\n')
    def find(pat):
        return [i+1 for i,l in enumerate(lines) if re.search(pat, l)]
    print('==', p.split('/')[-1])
    print(' layout:', [lines[i-1].strip()[:80] for i in find(r'\.layout \{')])
    print(' map height:', [lines[i-1].strip()[:80] for i in find(r'#map \{ height')])
    print(' onclick lines:', [(i, lines[i-1].strip()[:110]) for i in find(r'el\.onclick')])
    print(' scrollIntoView/scrollTo/sticky/focus:', find(r'scrollIntoView|scrollTo\(|position:\s*sticky|\.focus\('))
    li = find(r'id="list"'); ai = find(r'<aside')
    if li and ai:
        block = '\n'.join(lines[ai[0]-1:li[0]-1])
        print(' aside->list: lines', ai[0], '->', li[0], '; tiles before list:', block.count('class="tile'), '; text chars:', len(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',block))))
# rough geometry: map 0.72H, toggle 32, aside content above list ~700px at 1240 max-width (2 tile rows)
for H in (700, 800, 900, 1000, 1100, 1200, 1300):
    list_top = 0.72*H + 32 + 700
    need = list_top + 40 - H          # scrollY needed to see the first list item
    centre = 0.36*H                   # where setView puts the place
    print(f'H={H}: scrollY to reach first item >= {need:.0f}; place centred at y={centre:.0f}; visible={centre - 45 > need}')
