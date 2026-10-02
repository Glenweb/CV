#!/usr/bin/env node
/* Drives the harness and asserts the capture script fires the right events. */
import { createRequire } from 'node:module';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const require_ = createRequire(import.meta.url);
let chromium;
for (const c of ['playwright', '/opt/node-tools/node_modules/playwright', '/opt/node22/lib/node_modules/playwright']) {
  try { ({ chromium } = require_(c)); break; } catch { /* next */ }
}

const browser = await chromium.launch();
const page = await browser.newPage();
const url = pathToFileURL(path.resolve('lft/checker/test/harness.html')).href;
await page.goto(url);

await page.focus('#airlineSearch');
await page.click('#airlineDropdown li[data-airline="Ryanair"]');
await page.selectOption('#allowanceSelect', 'priority_cabin');
await page.fill('#weight', '11');
await page.click('#checkBtn');
await page.waitForSelector('#lft-optin', { timeout: 3000 });

const events = await page.evaluate(() => window.LFT_CHECKER.events.map(e => [e.name, e.params]));
const names = events.map(e => e[0]);

// Opt-in validation: empty email must be refused.
await page.click('#lft-optin button[type="submit"]');
const emptyMsg = await page.textContent('#lft-optin .lft-optin-msg');

// Valid email but no consent must also be refused.
await page.fill('#lft-optin-email', 'glen@example.com');
await page.click('#lft-optin button[type="submit"]');
const noConsentMsg = await page.textContent('#lft-optin .lft-optin-msg');

// With consent, preview mode should record the opt-in.
await page.check('#lft-optin-consent');
await page.click('#lft-optin button[type="submit"]');
await page.waitForTimeout(150);

// Stop the harness navigating away; the capture listener runs first (capture phase).
await page.evaluate(() => {
  document.addEventListener('click', (e) => { if (e.target.closest('a')) e.preventDefault(); });
});
await page.click('#aff');
await page.click('#copyEmbed');
const finalNames = await page.evaluate(() => window.LFT_CHECKER.events.map(e => e.name));
const result = events.find(e => e[0] === 'checker_result');
const headline = await page.textContent('#lft-optin h3');
await browser.close();

const expect = [
  ['checker_start fires', names.includes('checker_start')],
  ['airline captured', result?.[1].airline === 'Ryanair'],
  ['allowance captured', result?.[1].allowance_code === 'priority_cabin'],
  ['verdict parsed as fail', result?.[1].verdict === 'fail'],
  ['units captured', result?.[1].units === 'cm'],
  ['weight flagged', result?.[1].weight_entered === true],
  ['opt-in block injected', headline?.includes("won't pass")],
  ['empty email refused', /valid email/i.test(emptyMsg || '')],
  ['missing consent refused', /tick the box/i.test(noConsentMsg || '')],
  ['opt-in recorded', finalNames.includes('checker_email_optin')],
  ['affiliate click tracked', finalNames.includes('checker_affiliate_click')],
  ['embed copy tracked', finalNames.includes('checker_embed_copy')]
];

let failed = 0;
for (const [label, pass] of expect) {
  console.log(`${pass ? '  ok  ' : ' FAIL '} ${label}`);
  if (!pass) failed++;
}
console.log(failed ? `\n${failed} assertion(s) failed` : '\nAll assertions passed');
process.exit(failed ? 1 : 0);
