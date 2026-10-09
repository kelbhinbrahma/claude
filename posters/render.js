// node render.js -> PNG (300dpi) + PDF for every SVG here
const {chromium}=require('/opt/node-tools/node_modules/playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:794,height:1123},deviceScaleFactor:3.125});
for(const f of fs.readdirSync('.').filter(f=>f.endsWith('.svg'))){const n=f.slice(0,-4);
await p.goto('file://'+process.cwd()+'/'+f);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({path:`export/${n}.png`});await p.evaluate(()=>document.getElementById('grain-texture').remove());await p.pdf({path:`export/${n}.pdf`,width:'210mm',height:'297mm',printBackground:true,pageRanges:'1'});}
await b.close()})()
