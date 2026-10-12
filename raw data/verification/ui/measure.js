ObjC.import('AppKit');
function w(str, size, weight){
  var f=$.NSFont.systemFontOfSizeWeight(size, weight);
  var d=$.NSDictionary.dictionaryWithObjectForKey(f, $.NSFontAttributeName);
  return $(str).sizeWithAttributes(d).width;
}
function run(argv){
  var out={};
  // bold 11 (700) and semibold 9.1667 (600)
  for (var i=0;i<=40;i++){ out['b'+i]=w(String(i),11,$.NSFontWeightBold); out['s+'+i]=w('+'+i,11/1.2,$.NSFontWeightSemibold); }
  out['space']=w(' ',11,$.NSFontWeightBold);
  // legend label widths at 11px regular
  ['Photo (in order)','Bus stop','Church','Government office','Court','Jail / police','Medical clinic','Food pantry','Community center','School','Park','Field & track','Fitness center','Bank / finance','Theater','Library (historic)','Map icons ▾'].forEach(function(s){ out['L11:'+s]=w(s,11,$.NSFontWeightRegular); out['L11.5:'+s]=w(s,11.5,$.NSFontWeightRegular);});
  ['House','Duplex to fourplex','Apartment building','Garage or shed','Business','Public building','per block: houses ','+ multi-unit'].forEach(function(s){ out['K12:'+s]=w(s,12,$.NSFontWeightRegular); out['K12b:'+s]=w(s,12,$.NSFontWeightSemibold);});
  return JSON.stringify(out);
}
