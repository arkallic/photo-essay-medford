# usage: python3 -I access.py <scratch> <services html> <homes html> <out json>
import sys, runpy, io, contextlib, statistics
sys.argv = ["vstats.py"] + sys.argv[1:5]
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path("vstats.py")
snaps, HOMES, SEGS = g["snaps"], g["HOMES"], g["SEGS"]
offs = sorted((snaps[("h", b["id"])][0], b["id"], SEGS[snaps[("h", b["id"])][1]][3], b["c"]) for b in HOMES)
print("access leg median %.1f m, p90 %.1f, max %.1f" % (statistics.median(o[0] for o in offs), offs[int(.9 * len(offs))][0], offs[-1][0]))
for o in offs[-5:]: print("  ", o)
alley = sum(1 for o in offs if o[2] == "(alley)"); print("homes snapped to an alley:", alley, "of", len(offs))
