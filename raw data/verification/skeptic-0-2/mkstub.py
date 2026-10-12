import sys, re, os
# Make a measurement copy: Leaflet replaced by a chainable stub (no network), plus a script that
# records the page geometry relevant to "click a list item -> map.setView / openPopup".
src, out = sys.argv[1], sys.argv[2]
h = open(src, encoding="utf-8").read()
h = h.replace('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">', '')
stub = r'''<script>
(function(){
  const calls = [];
  window.__calls = calls;
  function P(name){
    const f = function(){};
    return new Proxy(f, {
      get(t, k){
        if (k === Symbol.toPrimitive) return () => 0;
        if (k === Symbol.iterator) return function*(){};
        if (k === 'then') return undefined;
        if (k === 'length') return 0;
        return P(name + '.' + String(k));
      },
      set(){ return true; },
      apply(t, th, args){
        if (/\.(setView|openPopup|flyTo|panTo)$/.test(name)) calls.push(name);
        return P(name + '()');
      },
      construct(){ return P(name + ' new'); }
    });
  }
  window.L = P('L');
})();
</script>'''
h = h.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>', stub)
measure = r'''<script>
window.addEventListener('load', () => setTimeout(() => {
  const r = e => { const b = e.getBoundingClientRect(); return [Math.round(b.top + scrollY), Math.round(b.bottom + scrollY)]; };
  const map = document.getElementById('map'), list = document.getElementById('list');
  const items = [...document.querySelectorAll('#list .svc')];
  const lau = items.find(e => /Lausmann/.test(e.textContent));
  const vh = innerHeight, mr = r(map);
  const mapCentre = Math.round((mr[0] + mr[1]) / 2);
  const firstItem = items.length ? r(items[0]) : null, lastItem = items.length ? r(items[items.length-1]) : null;
  // Minimum scroll at which the item is fully on screen; where the map centre lands then.
  const vis = it => { const s = Math.max(0, it[1] - vh); return { scrollY: s, mapCentreInViewport: mapCentre - s, mapBottomInViewport: mr[1] - s }; };
  // click Lausmann and capture calls / scroll change
  const before = scrollY;
  window.scrollTo(0, lau ? Math.max(0, r(lau)[1] - vh) : 0);
  const s0 = scrollY;
  if (lau) lau.click();
  const res = { vw: innerWidth, vh, map: mr, mapCentre, toggleBar: r(document.querySelector('.toggle-bar')),
    list: r(list), nItems: items.length, firstItem, lastItem, lausmann: lau ? r(lau) : null,
    firstVisible: firstItem && vis(firstItem), lausmannVisible: lau && vis(r(lau)), lastVisible: lastItem && vis(lastItem),
    docHeight: document.documentElement.scrollHeight,
    clickCalls: window.__calls.slice(), scrollBeforeClick: s0, scrollAfterClick: scrollY };
  const pre = document.createElement('pre'); pre.id = 'MEASURE'; pre.textContent = JSON.stringify(res);
  document.body.appendChild(pre);
}, 300));
</script></body>'''
h = h.replace('</body>', measure)
open(out, 'w', encoding='utf-8').write(h)
print('wrote', out, os.path.getsize(out))
