const MESHY='https://api.meshy.ai/openapi/v1/multi-image-to-3d';
const cors={ 'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'GET,POST,OPTIONS','Access-Control-Allow-Headers':'Content-Type' };
const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{...cors,'Content-Type':'application/json'}});
export default { async fetch(request,env) {
 const url=new URL(request.url);
 if(request.method==='OPTIONS') return new Response(null,{headers:cors});
 if(!env.MESHY_API_KEY) return json({error:'MESHY_API_KEY secret is not configured.'},503);
 if(request.method==='POST'&&url.pathname==='/create'){
  let body;try{body=await request.json()}catch{return json({error:'Invalid JSON body'},400)}
  if(!Array.isArray(body.image_urls)||body.image_urls.length<2||body.image_urls.length>4) return json({error:'Send 2 to 4 shoe images.'},400);
  for(const image of body.image_urls){if(typeof image!=='string'||!/^data:image\/(jpeg|png|webp);base64,/.test(image)||image.length>12_000_000)return json({error:'Each image must be a compressed JPEG/PNG/WebP data URI under 9 MB.'},400);}
  const upstream=await fetch(MESHY,{method:'POST',headers:{Authorization:'Bearer '+env.MESHY_API_KEY,'Content-Type':'application/json'},body:JSON.stringify({image_urls:body.image_urls,ai_model:'meshy-7.1',geometry_resolution:'standard',should_texture:true,enable_pbr:false,target_formats:['glb']})});
  const data=await upstream.json();return json(data,upstream.status);
 }
 const match=url.pathname.match(/^\/status\/([A-Za-z0-9-]+)$/);
 if(request.method==='GET'&&match){const upstream=await fetch(MESHY+'/'+match[1],{headers:{Authorization:'Bearer '+env.MESHY_API_KEY}});const data=await upstream.json();return json(data,upstream.status);}
 return json({error:'Not found'},404);
}};
