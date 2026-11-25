const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [n,t] of [['clinical','Clinical Trials & R&D Tax Relief: Pre-Trial Checklist'],['readiness','15-Point Claim Readiness Checklist'],['hmrc','HMRC R&D Enquiry Response Checklist']]){
 const p=await b.newPage();await p.goto('file://'+process.cwd()+'/'+n+'.html',{waitUntil:'networkidle'});await p.waitForTimeout(500);
 await p.pdf({path:n+'.pdf',format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,headerTemplate:'<span></span>',
 footerTemplate:`<div style="width:100%;font-family:Arial;font-size:7.5pt;color:#6b7b8c;padding:0 16mm;display:flex;justify-content:space-between"><span>© iTax Advisors Limited | ${t.replace(/&/g,'&amp;')}</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`});
 await p.close()}
await b.close()})();
