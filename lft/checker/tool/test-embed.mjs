import { createRequire } from 'node:module';
const require_ = createRequire(import.meta.url);
let chromium;
for (const c of ['playwright','/opt/node-tools/node_modules/playwright','/opt/node22/lib/node_modules/playwright']) {
  try { ({ chromium } = require_(c)); break; } catch {}
}
const b = await chromium.launch();
const p = await b.newPage();
const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
const pass=[],fail=[]; const t=(n,c)=>(c?pass:fail).push(n);

await p.goto('file:///home/user/CV/lft/checker/tool/host-test.html');
await p.waitForTimeout(1200);
const f = p.frameLocator('#f');

// chrome is gone
t('no site header in embed',  await f.locator('.site-header').count()===0);
t('no site footer in embed',  await f.locator('.site-footer').count()===0);
t('no FAQ section in embed',  await f.locator('#faq-heading').count()===0);
t('no enforcement prose',     await f.locator('#enforcement-heading').count()===0);
t('no nested embed section',  await f.locator('#embedCode').count()===0);

// the tool itself still works
await f.locator('#airlineSearch').fill('ryanair');
await f.locator('#airlineDropdown .search-option').first().click();
await p.waitForTimeout(200);
t('airline selectable',       await f.locator('#airlineCard').isVisible());
await f.locator('#lengthInput').fill('45');
await f.locator('#widthInput').fill('35');
await f.locator('#heightInput').fill('25');
await f.locator('#checkBtn').click();
await p.waitForTimeout(300);
const v = await f.locator('#verdict').innerText();
t('verdict renders in embed', v.trim().length>0);

// ceased handling survives the strip
await f.locator('#airlineSearch').fill('spirit');
await p.waitForTimeout(200);
await f.locator('#airlineDropdown .search-option').first().click();
await p.waitForTimeout(200);
t('ceased banner survives',   await f.locator('.ceased-note').isVisible());
t('ceased: no checker shown', await f.locator('#checkBtn').isHidden());

// attribution + auto-height
t('attribution present',      await f.locator('.lft-embed-credit').isVisible());
const href = await f.locator('.lft-embed-credit a').getAttribute('href');
t('attribution links home',  !!href && href.startsWith('https://luggagefortravel.com/'));
t('attribution is a real link (not iframe-only)', !!href);
const msgs = await p.evaluate(()=>window.__msgs);
t(`host received height messages (${msgs.length})`, msgs.length>0);
const h = await p.locator('#f').evaluate(el=>el.offsetHeight);
t(`host iframe resized to content (${h}px, not 300)`, h>400);

console.log(pass.map(x=>'  PASS  '+x).join('\n'));
if(fail.length) console.log(fail.map(x=>'  FAIL  '+x).join('\n'));
if(errs.length) console.log('page errors:\n'+errs.join('\n'));
console.log(`\n${pass.length} passed, ${fail.length} failed, ${errs.length} page errors`);
await b.close();
process.exit(fail.length||errs.length?1:0);
