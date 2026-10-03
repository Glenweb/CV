#!/usr/bin/env node
/* LFT indexing check.
 *
 * Turns a Google Search Console "Page indexing" CSV export into a diagnosis:
 * which pages are indexed, which are not and why, which money pages are in a bad
 * state, and which URLs are in the sitemap but absent from the export.
 *
 * No credentials, no API setup. Export the CSV from GSC and run it.
 *
 *   node lft/indexing/check-indexing.mjs --csv ~/Downloads/Table.csv
 *   node lft/indexing/check-indexing.mjs --csv Table.csv --sitemap sitemap_urls.txt
 *   node lft/indexing/check-indexing.mjs --csv Table.csv --json out.json
 *
 * Column names differ by locale and by which GSC report you exported, so the
 * columns are detected rather than assumed. Pass --url-col / --reason-col to override.
 *
 * Exit 0 = nothing urgent. 1 = something needs attention. 2 = could not read the input.
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(`--${k}`); return i === -1 ? d : argv[i + 1]; };

const csvPath = arg('csv');
if (!csvPath || !existsSync(csvPath)) {
  console.error('usage: check-indexing.mjs --csv <GSC page-indexing export.csv> [--sitemap <urls.txt>] [--json out.json]');
  process.exit(2);
}

/* The pages whose indexing state actually matters. A problem here is urgent;
   the same problem on a /uncategorized/ duplicate is not. */
const MONEY = [
  '/carry-on-size-checker/',
  '/carry-on-size-by-airline/',
  '/airline-baggage-fee-comparison/',
  '/airline-baggage-rules/best-ryanair-cabin-bag/',
  '/airline-baggage-rules/airlines-that-charge-for-carry-on/',
  '/luggage-reviews/best-carry-on-22x14x9/',
  '/luggage-reviews/best-luggage-international-travel-2026/',
  '/luggage-reviews/best-lightweight-luggage-2026/',
  '/luggage-reviews/best-checked-luggage-2026/'
];

/* How to read each GSC state. `ok` means indexed; `act` means it needs a decision. */
const STATES = [
  { re: /submitted and indexed|^indexed/i,              key: 'Indexed',                  ok: true,  act: false },
  { re: /indexed,? though blocked by robots/i,          key: 'Indexed but robots-blocked', ok: true,  act: true,
    note: 'Google indexed it without being able to read it. Fix robots.txt or it ranks on anchor text alone.' },
  { re: /crawled -? ?currently not indexed/i,           key: 'Crawled, not indexed',     ok: false, act: true,
    note: 'Google fetched it and chose not to index. Quality or duplication judgement - the usual signal on thin pages.' },
  { re: /discovered -? ?currently not indexed/i,        key: 'Discovered, not indexed',  ok: false, act: true,
    note: 'Never even fetched. Crawl budget or perceived low value. Common on large thin-page sets.' },
  { re: /duplicate.*google chose|duplicate without user-selected/i, key: 'Duplicate, Google picked another', ok: false, act: true,
    note: 'Canonical disagreement. Google overrode the declared canonical.' },
  { re: /alternate page with proper canonical/i,        key: 'Canonicalised elsewhere',  ok: false, act: false },
  { re: /excluded by .?noindex/i,                       key: 'noindex',                  ok: false, act: false },
  { re: /blocked by robots/i,                           key: 'Blocked by robots.txt',    ok: false, act: true },
  { re: /not found|404/i,                               key: 'Not found (404)',          ok: false, act: true,
    note: 'In the index report but returning 404. Either it should 301 somewhere, or it should not be submitted.' },
  { re: /soft 404/i,                                    key: 'Soft 404',                 ok: false, act: true,
    note: 'Returns 200 with content Google judged empty. Thin-content signal.' },
  { re: /redirect/i,                                    key: 'Redirect',                 ok: false, act: false },
  { re: /server error|5\d\d/i,                          key: 'Server error',             ok: false, act: true },
  { re: /crawl anomaly/i,                               key: 'Crawl anomaly',            ok: false, act: true },
  { re: /page with redirect/i,                          key: 'Page with redirect',       ok: false, act: false }
];

function classify(reason) {
  for (const s of STATES) if (s.re.test(reason)) return s;
  return { key: reason || '(blank)', ok: false, act: true, note: 'Unrecognised state - read it in GSC directly.' };
}

/* --- CSV parsing: quoted fields, embedded commas and newlines, BOM. --- */
function parseCsv(text) {
  text = text.replace(/^﻿/, '');
  const rows = [];
  let row = [], field = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else q = false; }
      else field += c;
    } else if (c === '"') q = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else if (c !== '\r') field += c;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows.filter((r) => r.some((c) => c.trim() !== ''));
}

const rows = parseCsv(readFileSync(csvPath, 'utf8'));
if (rows.length < 2) { console.error('That CSV has no data rows.'); process.exit(2); }

const header = rows[0].map((h) => h.trim());
const find = (pats) => header.findIndex((h) => pats.some((p) => p.test(h)));
const urlCol = arg('url-col') ? header.indexOf(arg('url-col')) : find([/^url$/i, /^page$/i, /address/i, /^lien/i]);
const reasonCol = arg('reason-col') ? header.indexOf(arg('reason-col'))
  : find([/reason/i, /coverage/i, /status/i, /state/i, /motif/i]);
const crawlCol = find([/last crawl/i, /crawled/i, /date/i]);

if (urlCol === -1) {
  console.error('Could not find a URL column. Header was:\n  ' + header.join(' | ') +
                '\nPass --url-col "<exact header>".');
  process.exit(2);
}

const seen = new Map();
for (const r of rows.slice(1)) {
  const url = (r[urlCol] || '').trim();
  if (!/^https?:\/\//i.test(url)) continue;
  seen.set(url, {
    url,
    reason: reasonCol === -1 ? '' : (r[reasonCol] || '').trim(),
    crawled: crawlCol === -1 ? '' : (r[crawlCol] || '').trim()
  });
}
const pages = [...seen.values()];
if (!pages.length) { console.error('No http(s) URLs found in that column.'); process.exit(2); }

/* --- buckets --- */
const buckets = new Map();
let indexed = 0, actionable = 0;
for (const p of pages) {
  const s = classify(p.reason);
  p.state = s;
  if (s.ok) indexed++;
  if (s.act) actionable++;
  if (!buckets.has(s.key)) buckets.set(s.key, { key: s.key, ok: s.ok, act: s.act, note: s.note, urls: [] });
  buckets.get(s.key).urls.push(p);
}
const ordered = [...buckets.values()].sort((a, b) => b.urls.length - a.urls.length);

/* --- money pages --- */
const moneyRows = MONEY.map((path) => {
  const hit = pages.find((p) => new URL(p.url).pathname.replace(/\/+$/, '/') === path);
  return { path, found: !!hit, state: hit ? hit.state.key : null, ok: hit ? hit.state.ok : null };
});

/* --- sitemap cross-check --- */
let orphans = [];
const smPath = arg('sitemap');
if (smPath && existsSync(smPath)) {
  const raw = readFileSync(smPath, 'utf8');
  const urls = raw.includes('<loc>')
    ? [...raw.matchAll(/<loc>\s*([^<]+?)\s*<\/loc>/g)].map((m) => m[1])
    : raw.split(/\r?\n/).map((l) => l.trim()).filter((l) => /^https?:\/\//.test(l));
  const known = new Set(pages.map((p) => p.url.replace(/\/+$/, '')));
  orphans = urls.filter((u) => !known.has(u.replace(/\/+$/, '')));
}

/* --- report --- */
const pct = (n) => ((n / pages.length) * 100).toFixed(1) + '%';
const out = [];
out.push(`# LFT indexing check — ${new Date().toISOString().slice(0, 10)}`);
out.push('');
out.push(`${pages.length} URLs in the export. **${indexed} indexed (${pct(indexed)})**, ${actionable} needing a decision.`);
out.push('');
out.push('## By state');
out.push('');
out.push('| State | URLs | |');
out.push('|---|---:|---|');
for (const b of ordered) {
  out.push(`| ${b.key} | ${b.urls.length} | ${b.ok ? 'indexed' : b.act ? '**needs a decision**' : 'expected'} |`);
}
for (const b of ordered) {
  if (b.note) { out.push(''); out.push(`**${b.key}** — ${b.note}`); }
}

out.push('', '## Money pages', '');
out.push('| Page | State |');
out.push('|---|---|');
for (const m of moneyRows) {
  out.push(`| \`${m.path}\` | ${m.found ? (m.ok ? m.state : '**' + m.state + '**') : '_not in the export_'} |`);
}
const moneyBad = moneyRows.filter((m) => m.found && !m.ok);
if (moneyBad.length) {
  out.push('', `**${moneyBad.length} money page${moneyBad.length === 1 ? '' : 's'} not indexed. Fix these before anything else.**`);
}

if (smPath) {
  out.push('', '## In the sitemap, absent from the export', '');
  out.push(orphans.length
    ? orphans.length + ' URLs. Google has not processed these at all — worth a URL Inspection each:\n\n' +
      orphans.slice(0, 40).map((u) => '- ' + u).join('\n') + (orphans.length > 40 ? `\n- …and ${orphans.length - 40} more` : '')
    : 'None. Every sitemap URL appears in the export.');
}

const worst = ordered.filter((b) => b.act && !b.ok).sort((a, b) => b.urls.length - a.urls.length)[0];
out.push('', '## What this means', '');
if (moneyBad.length) {
  out.push(`- Your money pages are the problem: ${moneyBad.map((m) => '`' + m.path + '`').join(', ')}. Everything else is secondary.`);
} else {
  out.push('- **Every money page is indexed.** Whatever is wrong, it is not deindexing of the pages that matter.');
}
if (worst) {
  out.push(`- The biggest non-indexed bucket is **${worst.key}** (${worst.urls.length} URLs, ${pct(worst.urls.length)}).`);
  if (/crawled, not indexed|discovered/i.test(worst.key)) {
    out.push('  A large bucket here on a site with no external backlinks is the expected picture, not an anomaly. It is an authority problem, not a technical one.');
  }
}
out.push('- **GSC exposes no manual-actions data through any API.** That check is in the UI and nothing here replaces it — see `RUNBOOK.md`.');

const report = out.join('\n');
console.log(report);

const jsonOut = arg('json');
if (jsonOut) {
  writeFileSync(jsonOut, JSON.stringify({
    date: new Date().toISOString(),
    total: pages.length, indexed, actionable,
    buckets: ordered.map((b) => ({ state: b.key, count: b.urls.length, indexed: b.ok, actionable: b.act,
                                   urls: b.urls.map((u) => u.url) })),
    moneyPages: moneyRows,
    sitemapOrphans: orphans
  }, null, 2));
}

process.exit(moneyBad.length || actionable ? 1 : 0);
