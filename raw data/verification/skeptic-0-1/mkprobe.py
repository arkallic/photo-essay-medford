import sys, re
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
# remove CDN leaflet (offline); install a chainable stub instead
t = re.sub(r'<link rel="stylesheet" href="https://cdnjs[^>]*>', '', t)
stub = r'''<script>
window.__errs = [];
window.addEventListener('error', e => window.__errs.push(String(e.message)));
(function(){
  const f = function(){ return P; };
  const P = new Proxy(f, {
    get(t, k) {
      if (k === Symbol.toPrimitive) return () => 0;
      if (k === 'then') return undefined;
      if (k === Symbol.iterator) return function*(){};
      if (k in t && typeof k === 'string' && !['call','apply','bind','length','name','prototype'].includes(k)) return t[k];
      return P;
    },
    set(t, k, v) { t[k] = v; return true; },
    apply() { return P; }, construct() { return P; }
  });
  window.L = P;
})();
</script>'''
t = re.sub(r'<script src="https://cdnjs[^>]*></script>', stub, t)
probe = r'''<script>
(function(){
  const out = {};
  const r = el => { const b = el.getBoundingClientRect(); return {top: Math.round(b.top + scrollY), bottom: Math.round(b.bottom + scrollY), h: Math.round(b.height)}; };
  out.viewport = [innerWidth, innerHeight];
  out.map = r(document.getElementById('map'));
  out.list = r(document.getElementById('list'));
  const svcs = [...document.querySelectorAll('#list .svc')];
  out.nsvc = svcs.length;
  out.docH = document.documentElement.scrollHeight;
  out.collapsed = document.body.classList.contains('collapsed');
  // For every list item: scroll it to the centre of the viewport (as a reader would to click it),
  // then check how much of the map, and its centre point, is in the viewport.
  const res = [];
  svcs.forEach(el => {
    el.scrollIntoView({block: 'center'});
    const m = document.getElementById('map').getBoundingClientRect();
    const visTop = Math.max(0, m.top), visBot = Math.min(innerHeight, m.bottom);
    const cy = (m.top + m.bottom) / 2;
    res.push({name: el.textContent.trim().slice(0, 40), mapVisiblePx: Math.max(0, Math.round(visBot - visTop)), mapCentreInView: cy >= 0 && cy <= innerHeight});
  });
  // Also the most favourable case: scroll so the item sits at the very bottom of the viewport.
  const best = svcs.map(el => { el.scrollIntoView({block: 'end'}); const m = document.getElementById('map').getBoundingClientRect(); const cy=(m.top+m.bottom)/2; return {name: el.textContent.trim().slice(0,40), mapVisiblePx: Math.max(0, Math.round(Math.min(innerHeight, m.bottom) - Math.max(0, m.top))), mapCentreInView: cy >= 0 && cy <= innerHeight}; });
  out.itemsCentred = {count: res.length, mapCentreInView: res.filter(x => x.mapCentreInView).length, maxMapVisiblePx: Math.max(...res.map(x => x.mapVisiblePx)), sample: res.filter(x => /Lausmann/.test(x.name))};
  out.itemsAtBottom = {mapCentreInView: best.filter(x => x.mapCentreInView).length, maxMapVisiblePx: Math.max(...best.map(x => x.mapVisiblePx)), sample: best.filter(x => /Lausmann/.test(x.name))};
  out.errs = window.__errs;
  const pre = document.createElement('pre'); pre.id = 'probe-out'; pre.textContent = 'PROBE' + JSON.stringify(out) + 'PROBE';
  document.body.appendChild(pre);
})();
</script>
</body>'''
t = t.replace('</body>', probe, 1)
open(dst, 'w', encoding='utf-8').write(t)
