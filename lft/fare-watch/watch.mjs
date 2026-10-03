#!/usr/bin/env node
/* Fare-aware freshness watcher.
 *
 * Fetches each airline's own baggage page and checks that every dimension set we publish
 * still appears on it. Finds drift; never writes to the tool. A change raises a review
 * item with the before, the after and the source — a human decides.
 *
 *   node lft/fare-watch/watch.mjs                      # all airlines with a source URL
 *   node lft/fare-watch/watch.mjs --tier1              # just the six that change most
 *   node lft/fare-watch/watch.mjs --only ryanair,easyjet
 *   node lft/fare-watch/watch.mjs --offline lft/fare-watch/test/fixtures
 *   node lft/fare-watch/watch.mjs --json report.json
 *
 * Exit 0 = nothing to review. Exit 1 = drift or staleness found. Exit 2 = it broke.
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';

const HERE = path.dirname(new URL(import.meta.url).pathname);
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(`--${k}`); return i === -1 ? d : argv[i + 1]; };
const has = (k) => argv.includes(`--${k}`);

const UA = 'LuggageForTravel-FareWatch/1.0 (+https://luggagefortravel.com; checks published baggage limits)';
const TIMEOUT_MS = 20000;
const POLITE_GAP_MS = 1500;

const db = JSON.parse(readFileSync(path.join(HERE, 'airlines.json'), 'utf8'));
const offlineDir = arg('offline');
const only = (arg('only') || '').split(',').map((s) => s.trim()).filter(Boolean);

let targets = db.airlines;
if (has('tier1')) targets = targets.filter((a) => db.tier1Keys.includes(a.key));
if (only.length) targets = targets.filter((a) => only.includes(a.key));
if (!offlineDir) targets = targets.filter((a) => a.source);

/* ---------------------------------------------------------------- extraction */

// Strip tags and entities so "40<span>x</span>30" still reads as one measurement.
function toText(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;|&#160;/g, ' ')
    .replace(/&times;|&#215;/g, '×')
    .replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ');
}

const TRIPLE = /(\d{2,3}(?:\.\d)?)\s*(?:cm)?\s*[x×*]\s*(\d{2,3}(?:\.\d)?)\s*(?:cm)?\s*[x×*]\s*(\d{2,3}(?:\.\d)?)\s*(?:cm)?/gi;
const KG = /(\d{1,2}(?:\.\d)?)\s*kg\b/gi;

// Airlines print the same three numbers in different orders, so compare as a set.
const norm = (t) => [...t].map(Number).sort((a, b) => b - a).join('x');

function extract(text) {
  const triples = new Set();
  for (const m of text.matchAll(TRIPLE)) triples.add(norm([m[1], m[2], m[3]]));
  const weights = new Set();
  for (const m of text.matchAll(KG)) weights.add(Number(m[1]));
  return { triples, weights };
}

/* ---------------------------------------------------------------- fetching */

async function load(a) {
  if (offlineDir) {
    const f = path.join(offlineDir, `${a.key}.html`);
    if (!existsSync(f)) return { ok: false, reason: 'no fixture' };
    return { ok: true, html: readFileSync(f, 'utf8') };
  }
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(a.source, {
      signal: ctrl.signal,
      redirect: 'follow',
      headers: { 'User-Agent': UA, Accept: 'text/html,application/xhtml+xml' }
    });
    if (!res.ok) return { ok: false, reason: `HTTP ${res.status}` };
    return { ok: true, html: await res.text() };
  } catch (e) {
    return { ok: false, reason: e.name === 'AbortError' ? 'timeout' : e.message };
  } finally {
    clearTimeout(t);
  }
}

/* ---------------------------------------------------------------- staleness */

const DAY = 86400000;
function staleness(a) {
  const sla = db.tier1Keys.includes(a.key) ? db.slaDays.tier1 : db.slaDays.tier2;
  if (!a.lastVerified) return { stale: true, days: null, sla };
  const days = Math.floor((Date.now() - Date.parse(a.lastVerified)) / DAY);
  return { stale: days > sla, days, sla };
}

/* ---------------------------------------------------------------- run */

const findings = [];
const errors = [];
const stale = [];

for (const [i, a] of targets.entries()) {
  const s = staleness(a);
  if (s.stale) stale.push({ key: a.key, name: a.name, days: s.days, sla: s.sla });

  if (!offlineDir && i > 0) await new Promise((r) => setTimeout(r, POLITE_GAP_MS));
  const got = await load(a);
  if (!got.ok) { errors.push({ key: a.key, name: a.name, reason: got.reason, source: a.source }); continue; }

  const { triples, weights } = extract(toText(got.html));
  if (triples.size === 0) {
    errors.push({ key: a.key, name: a.name, reason: 'no dimensions found on page (layout change or JS-rendered?)', source: a.source });
    continue;
  }

  for (const al of a.allowances) {
    if (!al.cm) continue;
    const want = norm(al.cm);
    if (!triples.has(want)) {
      findings.push({
        kind: 'missing',
        key: a.key, name: a.name, allowance: al.code, label: al.label,
        weStore: al.cm.join('×'),
        pageHas: [...triples].slice(0, 8),
        source: a.source
      });
    }
    if (al.kg && !weights.has(al.kg)) {
      findings.push({
        kind: 'weight',
        key: a.key, name: a.name, allowance: al.code, label: al.label,
        weStore: `${al.kg}kg`,
        pageHas: [...weights].slice(0, 8).map((w) => `${w}kg`),
        source: a.source
      });
    }
  }
}

/* ---------------------------------------------------------------- report */

const lines = [];
lines.push(`# Fare watch — ${new Date().toISOString().slice(0, 10)}`);
lines.push('');
lines.push(`Checked ${targets.length} airline${targets.length === 1 ? '' : 's'}. ` +
           `${findings.length} to review, ${errors.length} unreachable, ${stale.length} past their check-by date.`);

if (findings.length) {
  lines.push('', '## Review these', '');
  for (const f of findings) {
    lines.push(`- **${f.name}** · ${f.label || f.allowance}`);
    lines.push(`  - we publish \`${f.weStore}\`, not found on their page`);
    lines.push(`  - page shows: ${f.pageHas.join(', ') || '(none)'}`);
    lines.push(`  - ${f.source}`);
  }
}
if (errors.length) {
  lines.push('', '## Could not check', '');
  for (const e of errors) lines.push(`- **${e.name}** — ${e.reason}${e.source ? ` (${e.source})` : ''}`);
}
if (stale.length) {
  lines.push('', '## Past their check-by date', '');
  for (const s of stale) {
    lines.push(`- **${s.name}** — ${s.days === null ? 'never verified' : `${s.days} days ago`} (SLA ${s.sla}d)`);
  }
}
if (!findings.length && !errors.length && !stale.length) lines.push('', 'Everything current. Nothing to do.');

const report = lines.join('\n');
console.log(report);

const jsonOut = arg('json');
if (jsonOut) writeFileSync(jsonOut, JSON.stringify({ date: new Date().toISOString(), findings, errors, stale }, null, 2));

process.exit(findings.length || stale.length ? 1 : 0);
