import { createRequire } from 'node:module';
const require_ = createRequire(import.meta.url);
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const TOOL = pathToFileURL(join(dirname(fileURLToPath(import.meta.url)), 'carry-on-size-checker.html')).href;
let chromium;
for (const c of ['playwright','/opt/node-tools/node_modules/playwright','/opt/node22/lib/node_modules/playwright']) {
  try { ({ chromium } = require_(c)); break; } catch {}
}
const b = await chromium.launch();
const p = await b.newPage();
const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
await p.goto(TOOL);
const pass=[],fail=[];
const t=(n,c)=> (c?pass:fail).push(n);

// --- Spirit in the dropdown
await p.fill('#airlineSearch','spirit');
await p.waitForSelector('#airlineDropdown .search-option');
t('dropdown flags Spirit "Ceased"', (await p.innerHTML('#airlineDropdown')).includes('ceased-tag'));

// --- select Spirit
await p.click('#airlineDropdown .search-option');
await p.waitForTimeout(150);
t('ceased banner shown',            await p.locator('.ceased-note').isVisible());
t('banner names the date',          (await p.innerText('.ceased-note')).includes('2 May 2026'));
t('banner links to shutdown page',  (await p.getAttribute('.ceased-note a','href'))==='/spirit-airlines-shutdown/');
t('badge reads Ceased operations',  (await p.innerText('.badge')).trim().toUpperCase()==='CEASED OPERATIONS');
t('NO bag checker shown (cannot produce a verdict)', await p.locator('#checkBtn').isHidden());
t('historical limits still visible',(await p.innerText('#airlineCard')).includes('18 × 14 × 8'));
t('advisory relabelled "For reference"', (await p.innerText('#airlineCard')).includes('For reference'));
t('recommends the shutdown page',   (await p.innerText('#recommendButtons')).toLowerCase().includes('refund'));

// --- a live airline must be completely unaffected
await p.fill('#airlineSearch','ryanair');
await p.waitForSelector('#airlineDropdown .search-option');
t('live airline has no Ceased tag', !(await p.innerHTML('#airlineDropdown')).includes('ceased-tag'));
await p.click('#airlineDropdown .search-option');
await p.waitForTimeout(150);
t('live airline shows bag checker', await p.locator('#checkBtn').isVisible());
t('live airline has no ceased banner', await p.locator('.ceased-note').count()===0);
await p.fill('#lengthInput','40'); await p.fill('#widthInput','30'); await p.fill('#heightInput','20');
await p.click('#checkBtn'); await p.waitForTimeout(250);
const v=await p.innerText('#verdict');
t('live airline still returns a verdict', v.trim().length>0);

console.log(pass.map(x=>'  PASS  '+x).join('\n'));
if(fail.length) console.log(fail.map(x=>'  FAIL  '+x).join('\n'));
if(errs.length) console.log('page errors:\n'+errs.join('\n'));
console.log(`\n${pass.length} passed, ${fail.length} failed, ${errs.length} page errors`);
await b.close();
process.exit(fail.length||errs.length?1:0);
