#!/usr/bin/env node
/* Builds the watch list from the checker's own AIRLINES array, so the watcher and the
 * tool can never disagree about what the current data is.
 *
 *   node lft/fare-watch/import-from-checker.mjs <checker.html> [> airlines.json]
 *
 * Keeps any `source` URLs already present in airlines.json — those are hand-added and
 * must survive a re-import.
 */
import { readFileSync, existsSync } from 'node:fs';
import path from 'node:path';

const src = process.argv[2];
if (!src) { console.error('usage: import-from-checker.mjs <checker.html>'); process.exit(1); }
const html = readFileSync(src, 'utf8');

const start = html.indexOf('const AIRLINES=');
if (start === -1) { console.error('No `const AIRLINES=` found in that file.'); process.exit(1); }
const open = html.indexOf('[', start);

// Brace-match so string contents and nested objects can't end the array early.
let depth = 0, inStr = null, esc = false, end = -1;
for (let i = open; i < html.length; i++) {
  const c = html[i];
  if (inStr) {
    if (esc) esc = false;
    else if (c === '\\') esc = true;
    else if (c === inStr) inStr = null;
    continue;
  }
  if (c === '"' || c === "'" || c === '`') { inStr = c; continue; }
  if (c === '[') depth++;
  else if (c === ']') { depth--; if (depth === 0) { end = i; break; } }
}
if (end === -1) { console.error('Could not find the end of the AIRLINES array.'); process.exit(1); }

let airlines;
try {
  airlines = (0, eval)('(' + html.slice(open, end + 1) + ')');   // our own data file, not user input
} catch (e) {
  console.error('AIRLINES array did not parse: ' + e.message);
  process.exit(1);
}

const prevPath = path.join(path.dirname(new URL(import.meta.url).pathname), 'airlines.json');
let prev = { airlines: [] };
if (existsSync(prevPath)) {
  // Tolerate an empty or half-written file: a shell redirect truncates the target
  // before this script runs, so a strict parse here would break `> airlines.json`.
  try { prev = JSON.parse(readFileSync(prevPath, 'utf8')) || { airlines: [] }; } catch { /* start fresh */ }
}
prev.airlines = prev.airlines || [];
const prevByKey = new Map(prev.airlines.map((a) => [a.key, a]));

const out = airlines.map((a) => {
  const key = String(a.name || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const was = prevByKey.get(key) || {};
  const allowances = [];
  for (const al of a.allowances || []) {
    allowances.push({
      code: al.code || null,
      label: al.label || '',
      cm: Array.isArray(al.maxCm) ? al.maxCm : null,
      kg: al.weight && typeof al.weight.kg === 'number' ? al.weight.kg : null
    });
    // A bundled personal item carries its own limits and changes independently.
    if (al.personalItem && Array.isArray(al.personalItem.maxCm)) {
      allowances.push({
        code: (al.code || 'fare') + '__personal_item',
        label: (al.label || '') + ' — included personal item',
        cm: al.personalItem.maxCm,
        kg: al.personalItem.weight && typeof al.personalItem.weight.kg === 'number' ? al.personalItem.weight.kg : null
      });
    }
  }
  return {
    key,
    name: a.name || key,
    region: a.region ?? null,
    enforcement: a.enforcement ?? null,
    source: was.source || null,               // hand-added; preserved across re-imports
    lastVerified: was.lastVerified || null,
    allowances
  };
});

// Tier 1 carries most of LFT's demand and changes most often — tightest SLA.
const tier1 = ['ryanair', 'easyjet', 'wizz-air', 'frontier-airlines', 'spirit-airlines', 'british-airways'];
process.stdout.write(JSON.stringify({
  generatedAt: new Date().toISOString().slice(0, 10),
  note: 'Generated from the checker source. Add a `source` URL per airline by hand; re-imports preserve it.',
  slaDays: { tier1: 7, tier2: 30, tier3: 90 },
  tier1Keys: tier1.filter((k) => out.some((a) => a.key === k)),
  airlines: out
}, null, 2) + '\n');

console.error(`${out.length} airlines, ${out.reduce((n, a) => n + a.allowances.length, 0)} allowances, ${out.filter((a) => a.source).length} with a source URL`);
