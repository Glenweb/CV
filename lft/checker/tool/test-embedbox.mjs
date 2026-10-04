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
const ctx = await b.newContext({ permissions: ['clipboard-read','clipboard-write'] });
const p = await ctx.newPage();
const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
const pass=[],fail=[]; const t=(n,c)=>(c?pass:fail).push(n);
await p.goto(TOOL);
const a = await p.inputValue('#embedCode');
const s2 = await p.inputValue('#embedCodeSimple');
t('main snippet points at /embed/', a.includes('/carry-on-size-checker/embed/'));
t('main snippet no longer frames the full page', !/src="https:\/\/luggagefortravel\.com\/carry-on-size-checker\/"/.test(a));
t('main snippet carries the resize listener', a.includes('lft-checker-height') && a.includes('e.origin'));
t('main snippet checks the origin before acting', a.includes('e.origin !== "https://luggagefortravel.com"'));
t('fixed-height snippet offered, without script', s2.includes('/embed/') && !s2.includes('<script'));
await p.click('#copyEmbed'); await p.waitForTimeout(300);
t('copy button confirms', (await p.innerText('#copyEmbed')).includes('Copied'));
await p.click('#copyEmbedSimple'); await p.waitForTimeout(300);
t('fixed-height copy button confirms', (await p.innerText('#copyEmbedSimple')).includes('Copied'));
console.log(pass.map(x=>'  PASS  '+x).join('\n'));
if(fail.length) console.log(fail.map(x=>'  FAIL  '+x).join('\n'));
if(errs.length) console.log('page errors:\n'+errs.join('\n'));
console.log(`\n${pass.length} passed, ${fail.length} failed, ${errs.length} page errors`);
await b.close(); process.exit(fail.length||errs.length?1:0);
