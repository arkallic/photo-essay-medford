ObjC.import('Foundation');
function run(argv){
  var out=[];
  argv.forEach(function(p){
    var s=$.NSString.stringWithContentsOfFileEncodingError(p,$.NSUTF8StringEncoding,null).js;
    try{ new Function(s); out.push(p.split('/').pop()+': OK ('+s.length+' chars)'); }
    catch(e){ out.push(p.split('/').pop()+': '+e.name+': '+e.message+' line '+e.line); }
  });
  return out.join('\n');
}
