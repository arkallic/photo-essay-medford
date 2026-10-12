# usage: python3 -I pace.py <route.json>
import sys, json, math
KX, KY = 82427.8, 111079.6
R = [(b * KX, a * KY) for a, b in json.load(open(sys.argv[1]))]
cum = [0]
for p, q in zip(R, R[1:]): cum.append(cum[-1] + math.dist(p, q))
photos = [(42.32662167, -122.88713833, "15:38:01"), (42.32378, -122.88760333, "15:43:32"), (42.32367833, -122.88433, "15:48:16"),
          (42.32258333, -122.877905, "15:59:11"), (42.32481333, -122.87884500, "16:30:02"), (42.32836667, -122.88093667, "16:37:59")]
def proj(p, start, end=1e18):
    best = None
    for i in range(len(R) - 1):
        (ax, ay), (bx, by) = R[i], R[i + 1]; dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
        t = max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2)) if L2 else 0
        s = cum[i] + t * math.sqrt(L2)
        if s < start - 1e-6 or s > end: continue
        off = math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)
        if best is None or off < best[0] - 1e-9: best = (off, s)
    return best
sec = lambda t: sum(int(x) * m for x, m in zip(t.split(":"), (3600, 60, 1)))
pos = []; s0 = 0
for j, (la, lo, t) in enumerate(photos):
    off, s = proj((lo * KX, la * KY), s0, 100 if j == 0 else 1e18); pos.append((s, sec(t), off)); s0 = s
print("route length %.0f m" % cum[-1])
tot_d = tot_t = 0
for k in range(5):
    d = pos[k + 1][0] - pos[k][0]; t = pos[k + 1][1] - pos[k][1]
    print("#%d->#%d  %.0f m  %d s  %.1f m/min  (%.2f mph)  offs %.0f/%.0f" % (k + 1, k + 2, d, t, d / t * 60, d / t * 2.236936, pos[k][2], pos[k + 1][2]))
    if k != 3: tot_d += d; tot_t += t
print("excluding #4->#5: %.0f m in %d s = %.1f m/min = %.2f mph" % (tot_d, tot_t, tot_d / tot_t * 60, tot_d / tot_t * 2.236936))
print("60 m/min = %.3f mph" % (60 / 60 * 2.236936))
