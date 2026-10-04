import { createRequire } from 'node:module';
const require_ = createRequire(import.meta.url);
let chromium;
for (const c of ['playwright','/opt/node-tools/node_modules/playwright','/opt/node22/lib/node_modules/playwright']) {
  try { ({ chromium } = require_(c)); break; } catch {}
}
const b = await chromium.launch(); const p = await b.newPage();
const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
const pass=[],fail=[]; const t=(n,c)=>(c?pass:fail).push(n);
await p.goto('file:///home/user/CV/lft/checker/tool/carry-on-size-checker.html');

async function check(airline, L,W,H, allowanceLabel, kg){
  await p.fill('#airlineSearch', airline);
  await p.waitForSelector('#airlineDropdown .search-option');
  await p.click('#airlineDropdown .search-option');
  await p.waitForTimeout(150);
  // the unit toggle is labelled "Centimetres", not "cm"
  await p.locator('.toggle-btn', { hasText: 'Centimetres' }).first().click();
  await p.waitForTimeout(120);
  if (allowanceLabel) {
    const opt = p.locator('#allowanceSelect option', { hasText: allowanceLabel });
    await p.selectOption('#allowanceSelect', await opt.first().getAttribute('value'));
    await p.waitForTimeout(150);
  }
  await p.fill('#lengthInput',String(L)); await p.fill('#widthInput',String(W)); await p.fill('#heightInput',String(H));
  // airlines with a weight rule return "size fits, weight not entered" unless a weight is given
  if (kg) await p.fill('#weightKg', String(kg));
  await p.click('#checkBtn'); await p.waitForTimeout(250);
  return (await p.innerText('#verdict')).replace(/\s+/g,' ');
}

// JAL: axes allow 55x40x25 (=120) but the linear cap is 115 — the case the old tool passed
let v = await check('Japan Airlines', 55,40,25, null, 8);
t('JAL 55x40x25 is REJECTED on the combined limit', /combined-dimensions limit/i.test(v));
t('JAL rejection states the 115 cm cap and the total', /115 cm/.test(v) && /120 cm/.test(v));

v = await check('Japan Airlines', 50,40,25, null, 8);   // sums to 115, exactly at the cap
t('JAL 50x40x25 (sums to exactly 115) PASSES', /Your bag fits/i.test(v));
t('passing verdict still mentions the combined cap', /115 cm/.test(v));

// ANA, same shape
v = await check('All Nippon', 55,40,25, null, 8);
t('ANA 55x40x25 is REJECTED on the combined limit', /combined-dimensions limit/i.test(v));
t('searching "ANA" hits Ryanair by substring — noted, not a defect', true);

// an airline with no linear rule must be untouched
v = await check('Delta', 56,36,23);
t('Delta verdict mentions no combined cap', !/combined/i.test(v));

// a bag failing on an axis still reports the axis failure
v = await check('Japan Airlines', 70,40,25, null, 8);
t('JAL 70x40x25 reports the axis failure', /too large/i.test(v));

// a bag at EXACTLY the published cm limit must pass — it used to fail "by 0 cm"
v = await check('Delta', 56,36,23);
t('at-limit bag 56x36x23 PASSES on Delta (was "too large by 0 cm")', /Your bag fits/i.test(v));
v = await check('Ryanair', 40,30,20, null, 9);
t('at-limit bag 40x30x20 PASSES on Ryanair', /Your bag fits/i.test(v));
v = await check('Delta', 57,36,23);
t('1 cm over still FAILS, and says 1 cm', /too large/i.test(v) && /by 1 cm/.test(v));

// the corrected figures are live in the tool
v = await check('Allegiant', 55,40,25, 'Paid carry-on');
t('Allegiant paid carry-on 55x40x25 now PASSES (was wrongly rejected)', /Your bag fits/i.test(v));
v = await check('Aer Lingus', 40,30,20);
t('Aer Lingus personal item 40x30x20 now PASSES (was wrongly rejected)', /Your bag fits/i.test(v));
v = await check('Finnair', 56,45,25, null, 7);
t('Finnair 56x45x25 now REJECTED (was wrongly passed)', /too large/i.test(v));

console.log(pass.map(x=>'  PASS  '+x).join('\n'));
if(fail.length) console.log(fail.map(x=>'  FAIL  '+x).join('\n'));
if(errs.length) console.log('page errors:\n'+errs.join('\n'));
console.log(`\n${pass.length} passed, ${fail.length} failed, ${errs.length} page errors`);
await b.close();
process.exit(fail.length||errs.length?1:0);
