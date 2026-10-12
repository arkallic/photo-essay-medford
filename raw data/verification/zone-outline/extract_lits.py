# extract JS literal arrays from page: python3 -I extract_lits.py page.html out.json
import sys, json, re
t = open(sys.argv[1], encoding="utf-8").read()
out = {}
for name in ["stops", "route", "zoneRings", "services", "busStops", "BLDG", "BLOCKS"]:
    m = re.search(r"const %s\s*=\s*" % name, t)
    if not m: continue
    i = m.end(); depth = 0; instr = None; j = i
    while True:
        ch = t[j]
        if instr:
            if ch == "\\": j += 2; continue
            if ch == instr: instr = None
        elif ch in "\"'": instr = ch
        elif ch in "[{": depth += 1
        elif ch in "]}":
            depth -= 1
            if depth == 0: break
        j += 1
    s = t[i:j + 1]
    try:
        out[name] = json.loads(s)
    except Exception as e:
        # try to convert JS object keys
        s2 = re.sub(r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:', r'\1"\2":', s)
        try: out[name] = json.loads(s2)
        except Exception as e2: out[name] = {"_raw": s[:3000], "_err": str(e2)}
json.dump(out, open(sys.argv[2], "w"))
for k, v in out.items(): print(k, type(v).__name__, len(v) if isinstance(v, list) else v.get("_err"))
