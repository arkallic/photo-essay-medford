ObjC.import('Foundation');
function run(argv){
var LOG=[];
var W=JSON.parse($.NSString.stringWithContentsOfFileEncodingError(argv[1],$.NSUTF8StringEncoding,null).js);
var MAPW=+argv[2], MAPH=+argv[3];
// ---------- minimal DOM ----------
function El(tag){ this.tagName=tag; this.children=[]; this.style={ setProperty:function(k,v){this[k]=v;} }; this.className=""; this._html=""; this.listeners={}; this.classList={ _s:{}, add:function(c){this._s[c]=1;}, remove:function(c){delete this._s[c];} }; }
El.prototype.appendChild=function(c){ this.children.push(c); return c; };
El.prototype.append=function(){ for(var i=0;i<arguments.length;i++) this.children.push(arguments[i]); };
Object.defineProperty(El.prototype,"innerHTML",{ get:function(){return this._html;}, set:function(v){ this._html=v; } });
var listEl=new El("div"), mapEl=new El("div"); mapEl.clientWidth=MAPW; mapEl.clientHeight=MAPH;
var winL={}; var COLH=+argv[6]||0, EXPH=MAPH, LS={}; if(argv[7]==="stored") LS.statsCollapsed="1";
var bodyEl=new El("body"); bodyEl.classList.toggle=function(c,f){ if(f){this._s[c]=1;} else {delete this._s[c];} mapEl.clientHeight = this._s.collapsed ? COLH : EXPH; };
bodyEl.classList.contains=function(c){ return !!this._s[c]; };
var lbl=new El("span"); var btn=new El("button"); btn.attrs={}; btn.setAttribute=function(k,v){this.attrs[k]=v;}; btn.querySelector=function(){return lbl;}; btn.addEventListener=function(e,f){ btn.click=f; };
var g=this;
g.document={ getElementById:function(id){ return id==="list"?listEl:id==="statsToggle"?btn:mapEl; }, body:bodyEl, createElement:function(t){ return new El(t); }, querySelectorAll:function(){ return []; }, documentElement:{} };
g.window={ addEventListener:function(ev,fn){ (winL[ev]=winL[ev]||[]).push(fn); } };
g.localStorage={ getItem:function(k){return LS[k]===undefined?null:LS[k];}, setItem:function(k,v){LS[k]=String(v);} };
g.getComputedStyle=function(){ return { getPropertyValue:function(k){ return k==="--accent"?" #d9480f":" #2b6cb0"; } }; };
// ---------- minimal Leaflet ----------
function LatLng(a,b){ if(Array.isArray(a)){b=a[1];a=a[0];} else if(a&&a.lat!==undefined){b=a.lng;a=a.lat;} this.lat=a; this.lng=b; }
function Pt(x,y){ this.x=x; this.y=y; }
Pt.prototype.distanceTo=function(p){ return Math.hypot(p.x-this.x,p.y-this.y); };
function Bounds(sw,ne){ this.s=Math.min(sw.lat,ne.lat); this.n=Math.max(sw.lat,ne.lat); this.w=Math.min(sw.lng,ne.lng); this.e=Math.max(sw.lng,ne.lng); }
function boundsOf(pts){ var la=pts.map(function(p){return p[0]}), ln=pts.map(function(p){return p[1]}); return new Bounds(new LatLng(Math.min.apply(0,la),Math.min.apply(0,ln)), new LatLng(Math.max.apply(0,la),Math.max.apply(0,ln))); }
function proj(ll,z){ var s=256*Math.pow(2,z), r=ll.lat*Math.PI/180; return new Pt(s*(ll.lng+180)/360, s*(1-Math.log(Math.tan(r)+1/Math.cos(r))/Math.PI)/2); }
function unproj(p,z){ var s=256*Math.pow(2,z); var lng=p.x/s*360-180; var n=Math.PI-2*Math.PI*p.y/s; return new LatLng(180/Math.PI*Math.atan(0.5*(Math.exp(n)-Math.exp(-n))), lng); }
var layers=[];
function Layer(kind,opts){ this.kind=kind; this.opts=opts||{}; this._map=null; this._ev={}; }
Layer.prototype.addTo=function(m){ m.addLayer(this); return this; };
Layer.prototype.bindPopup=function(h){ this.popup=h; return this; };
Layer.prototype.bindTooltip=function(h){ this.tooltip=h; return this; };
Layer.prototype.on=function(e,f){ (this._ev[e]=this._ev[e]||[]).push(f); return this; };
Layer.prototype.openPopup=function(){ return this; };
Layer.prototype.setLatLng=function(ll){ this.ll=new LatLng(ll); return this; };
Layer.prototype.setLatLngs=function(a){ this.lls=a; return this; };
Layer.prototype.getBounds=function(){ return boundsOf(this.pts); };
Layer.prototype.getElement=function(){ return this._map && this.kind==="marker" ? this._el : undefined; };
var map;
function textW(html){ // bubble text width
  var m=html.match(/class="blk">([0-9]*)( ?)(?:<small>\+([0-9]+)<\/small>)?<\/div>/); var w=0;
  if(m[1]) w+=W["b"+m[1]]; if(m[2]) w+=W.space; if(m[3]) w+=W["s+"+m[3]]; return w+13; }
function makeEl(layer){ var html=layer.opts.icon.html, s=parseFloat(mapEl.style["--s"]||1);
  var w,h; if(/class="pin"/.test(html)){w=h=26;} else if(/class="ic bus"/.test(html)){w=h=26;} else if(/class="ic"/.test(html)){w=h=22;} else {w=textW(html);h=19;}
  return { firstElementChild:{ getBoundingClientRect:function(){ var s=parseFloat(mapEl.style["--s"]||1); return {width:w*s,height:h*s}; } } }; }
function Map(id,opts){ this.options=opts; this._ev={}; this._layers=[]; this._loaded=false; this._zoom=undefined; this._size=null; this._sizeChanged=true; this.ready=[]; }
Map.prototype.on=function(e,f){ (this._ev[e]=this._ev[e]||[]).push(f); return this; };
Map.prototype.fire=function(e){ (this._ev[e]||[]).slice().forEach(function(f){f.call(map);}); };
Map.prototype.whenReady=function(f){ if(this._loaded) f.call(this); else this.ready.push(f); return this; };
Map.prototype.addLayer=function(l){ if(this._layers.indexOf(l)<0) this._layers.push(l); l._mapToAdd=this; var self=this; this.whenReady(function(){ if(self._layers.indexOf(l)>=0){ l._map=self; if(l.kind==="marker") l._el=makeEl(l);} }); return this; };
Map.prototype.removeLayer=function(l){ var i=this._layers.indexOf(l); if(i>=0) this._layers.splice(i,1); l._map=null; return this; };
Map.prototype.hasLayer=function(l){ return this._layers.indexOf(l)>=0; };
Map.prototype.getContainer=function(){ return mapEl; };
Map.prototype.getZoom=function(){ return this._zoom; };
Map.prototype.getMinZoom=function(){ return this.options.minZoom===undefined?0:this.options.minZoom; };
Map.prototype.getMaxZoom=function(){ return 19; };
Map.prototype.getSize=function(){ if(!this._size||this._sizeChanged){ this._size=new Pt(mapEl.clientWidth,mapEl.clientHeight); this._sizeChanged=false;} return new Pt(this._size.x,this._size.y); };
Map.prototype.invalidateSize=function(){ this._sizeChanged=true; this.getSize(); return this; };
Map.prototype.setMinZoom=function(z){ var old=this.options.minZoom; this.options.minZoom=z; if(this._loaded&&old!==z){ if(this.getZoom()<z) this.setZoom(z);} return this; };
Map.prototype.setZoom=function(z){ this._setView(z); return this; };
Map.prototype.getBoundsZoom=function(b,inside,pad){ pad=pad||new Pt(0,0); var zoom=this.getZoom()||0, min=this.getMinZoom(), max=this.getMaxZoom();
  var size=this.getSize(); size=new Pt(size.x-pad.x,size.y-pad.y);
  var nw=proj(new LatLng(b.n,b.w),zoom), se=proj(new LatLng(b.s,b.e),zoom); var bx=se.x-nw.x, by=se.y-nw.y;
  var snap=this.options.zoomSnap, sx=size.x/bx, sy=size.y/by, sc=inside?Math.max(sx,sy):Math.min(sx,sy);
  zoom=zoom+Math.log(sc)/Math.LN2; zoom=Math.round(zoom/(snap/100))*(snap/100); zoom=inside?Math.ceil(zoom/snap)*snap:Math.floor(zoom/snap)*snap;
  return Math.max(min,Math.min(max,zoom)); };
Map.prototype.fitBounds=function(b,o){ var p=o&&o.padding?new Pt(o.padding[0]*2,o.padding[1]*2):new Pt(0,0); var z=this.getBoundsZoom(b,false,p); this._setView(z); return this; };
Map.prototype._setView=function(z){ z=Math.max(this.getMinZoom(),Math.min(19,z)); var loading=!this._loaded; this._loaded=true; var changed=this._zoom!==z; this._zoom=z;
  if(changed) this.fire("zoomend"); this.fire("moveend"); if(loading){ var r=this.ready; this.ready=[]; r.forEach(function(f){f.call(map);}); } };
Map.prototype.latLngToLayerPoint=function(ll){ return proj(new LatLng(ll),this._zoom); };
Map.prototype.layerPointToLatLng=function(p){ return unproj(p,this._zoom); };
g.L={
  latLngBounds:function(a){ return new Bounds(new LatLng(a[0]),new LatLng(a[1])); },
  latLng:function(a,b){ return new LatLng(a,b); }, point:function(x,y){ return new Pt(x,y); },
  map:function(id,o){ map=new Map(id,o); return map; },
  tileLayer:function(){ return new Layer("tile"); },
  polygon:function(p,o){ var l=new Layer("polygon",o); l.pts=p; return l; },
  polyline:function(p,o){ var l=new Layer("polyline",o); l.pts=p; return l; },
  marker:function(ll,o){ var l=new Layer("marker",o); l.ll=new LatLng(ll); l.home=new LatLng(ll); return l; },
  divIcon:function(o){ return o; },
  layerGroup:function(){ var l=new Layer("group"); l.addLayer=function(x){ (l.items=l.items||[]).push(x); return l; }; return l; },
  control:function(o){ var c={opts:o, addTo:function(m){ c.el=c.onAdd(m); return c; }}; return c; },
  DomUtil:{ create:function(t,c){ var e=new El(t); e.className=c; return e; } },
  DomEvent:{ disableClickPropagation:function(){}, disableScrollPropagation:function(){} }
};
var code=$.NSString.stringWithContentsOfFileEncodingError(argv[0],$.NSUTF8StringEncoding,null).js;
code=code+"\n;this.__marks=(typeof marks!=='undefined')?marks:[]; this.__fit=fit; this.__fitMinZoom=fitMinZoom; this.__declutter=(typeof declutter!=='undefined')?declutter:null; this.__iconKey=(typeof iconKey!=='undefined')?iconKey:null; this.__key=(typeof key!=='undefined')?key:null;";
try { (new Function(code)).call(g); } catch(e){ return "RUNTIME ERROR: "+e+" line "+e.line; }
LOG.push("after load: zoom="+map.getZoom()+" minZoom="+map.options.minZoom+" layers="+map._layers.length+" listChildren="+listEl.children.length);
(winL.load||[]).forEach(function(f){f();});
LOG.push("after window load: zoom="+map.getZoom()+" minZoom="+map.options.minZoom);
// overlaps / leaders
function report(tag){
  var M=g.__marks.filter(function(o){return map.hasLayer(o.m);}); var s=parseFloat(mapEl.style["--s"]||1);
  var bad=0, maxlead=0, leadNonIcon=0, hiddenBubbles=g.__marks.filter(function(o){return o.kind==="bubble"&&!map.hasLayer(o.m);}).length;
  var B=M.map(function(o){ var r=o.m.getElement()?o.m.getElement().firstElementChild.getBoundingClientRect():{width:0,height:0}; var p=map.latLngToLayerPoint(o.m.ll); return {x:p.x,y:p.y,w:r.width,h:r.height,k:o.kind,o:o}; });
  for(var i=0;i<B.length;i++) for(var j=i+1;j<B.length;j++){ var a=B[i],b=B[j]; if(a.k==="pin"&&b.k==="pin") continue;
    var ox=(a.w+b.w)/2-Math.abs(a.x-b.x), oy=(a.h+b.h)/2-Math.abs(a.y-b.y); if(ox>0.01&&oy>0.01&&(a.k==="bubble"||b.k==="bubble"||a.k!==b.k||a.k==="icon")) bad++; }
  g.__marks.forEach(function(o){ if(o.leader&&o.leader.lls&&o.leader.lls.length){ var d=map.latLngToLayerPoint(o.leader.lls[0]).distanceTo(map.latLngToLayerPoint(o.leader.lls[1])); maxlead=Math.max(maxlead,d); if(o.kind!=="icon") leadNonIcon++; } });
  var pinsMoved=g.__marks.filter(function(o){return o.kind==="pin"&&(o.m.ll.lat!==o.ll.lat||o.m.ll.lng!==o.ll.lng);}).length;
  LOG.push(tag+": zoom="+map.getZoom()+" --s="+mapEl.style["--s"]+" live="+M.length+" hiddenBubbles="+hiddenBubbles+" overlaps="+bad+" maxLeader="+maxlead.toFixed(1)+"px leadersOnNonIcons="+leadNonIcon+" pinsMoved="+pinsMoved);
}
report("initial");
[15.5,16,16.25,17,18,19].forEach(function(z){ if(z>=map.getMinZoom()){ map.setZoom(z); report("setZoom "+z);} });
if(COLH){ var z0=map.options.minZoom; btn.click(); var z1=map.options.minZoom, l1=lbl.textContent, a1=btn.attrs["aria-expanded"]; btn.click(); var z2=map.options.minZoom;
  map.options.minZoom=0; var fresh2=map.getBoundsZoom(g.L.latLngBounds([[42.3170,-122.8994],[42.3340,-122.8693]]),true); map.options.minZoom=z2;
  LOG.push("toggle: minZoom expanded "+z0+" -> collapsed("+COLH+"px) "+z1+" label='"+l1+"' aria-expanded="+a1+" -> expanded again "+z2+" (unclamped value for this size: "+fresh2+") label='"+lbl.textContent+"' stored="+LS.statsCollapsed); report("after toggle twice"); }
// resize test: enlarge container, fire window resize like the browser (Leaflet's own handler would invalidate on next frame)
var before=map.options.minZoom;
mapEl.clientWidth=+argv[4]; mapEl.clientHeight=+argv[5];
(winL.resize||[]).forEach(function(f){f();});
LOG.push("resize to "+argv[4]+"x"+argv[5]+": minZoom "+before+" -> "+map.options.minZoom+" (stale cached size used)");
map.invalidateSize(); var fresh=map.getBoundsZoom(g.L.latLngBounds([[42.3170,-122.8994],[42.3340,-122.8693]]),true);
LOG.push("   correct minZoom for new size (with clamp) would be "+fresh);
if(g.__iconKey) LOG.push("legend html length "+g.__iconKey.el.innerHTML.length+" rows "+(g.__iconKey.el.innerHTML.match(/class="row"/g)||[]).length);
if(g.__key) LOG.push("map key: "+g.__key.el.innerHTML.replace(/<[^>]+>/g,"|").replace(/\|+/g,"|"));
// list summary
var txt=[]; listEl.children.forEach(function(c){ if(c.tagName==="h3") txt.push("H3 "+c.innerHTML.replace(/<[^>]+>/g,"")); else c.children.forEach(function(gp){ txt.push("  "+gp.innerHTML.replace(/<[^>]+>/g,"")+" -> "+gp.children.map(function(x){return x.innerHTML.replace(/<svg[\s\S]*?<\/svg>/,"").replace(/<[^>]+>/g,"");}).join(" | ")); }); });
LOG.push(txt.join("\n"));
var pops=map._layers.filter(function(l){return l.popup&&l.kind==="marker"&&!/img/.test(l.popup);}).map(function(l){return l.popup;});
LOG.push("non-photo popups: "+pops.length+" with links/addresses: "+pops.filter(function(p){return !/^<b>[^<]*<\/b>$/.test(p);}).length+"; sample: "+pops.slice(0,3).join(" ; "));
return LOG.join("\n");
}
