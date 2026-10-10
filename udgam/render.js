// node render.js -> per SVG: Instagram PNG (1080 + 2160 hi-res), social JPG, print PDF (vector, grain removed)
const {chromium}=require('/opt/node-tools/node_modules/playwright');const fs=require('fs');const {execSync}=require('child_process');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
for(const scale of [1,2]){const p=await b.newPage({viewport:{width:1080,height:1080},deviceScaleFactor:scale});
for(const f of fs.readdirSync('.').filter(f=>f.endsWith('.svg'))){const n=f.slice(0,-4);
await p.goto('file://'+process.cwd()+'/'+f);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
if(scale===1){await p.screenshot({path:`export/instagram-png/${n}_1080.png`});await p.screenshot({path:`export/social-jpg/${n}_1080.jpg`,type:'jpeg',quality:95});}
else{await p.screenshot({path:`export/instagram-png/${n}_2160-hires.png`});
await p.evaluate(()=>document.getElementById('grain-texture').remove());
await p.pdf({path:`export/print-pdf/${n}.pdf`,width:'1080px',height:'1080px',printBackground:true,pageRanges:'1'});}}
await p.close();}
await b.close()})()
