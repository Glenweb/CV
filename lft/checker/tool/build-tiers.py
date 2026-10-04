#!/usr/bin/env python3
"""Regenerate the tool's enforcement-tier prose from its own AIRLINES array.

The tier list used to be hand-written, which is how it came to name Jetstar (absent
from the data) and omit Aer Lingus, Vueling and flydubai (present in the strict bands).
Run this after any change to AIRLINES; the prose then cannot contradict the data."""
import re, sys, collections

F = 'carry-on-size-checker.html'
s = open(F, encoding='utf-8').read()

# Split AIRLINES into per-airline blocks so a flag is read from the airline that owns it.
# An earlier version scanned forward N lines from each name and attributed Spirit's
# ceased flag to the airline defined before it.
blocks = re.split(r'(?=\{name:")', s[s.index('const AIRLINES=['):s.index('const FIXED_GUIDES=[')])
rows, ceased = [], set()
for b in blocks:
    m = re.match(r'\{name:"([^"]+)",region:"([^"]+)",enforcement:"([^"]+)"', b)
    if not m:
        continue
    name, region, enf = m.groups()
    rows.append((name, region, enf))
    if re.search(r'\bceased:\{', b):
        ceased.add(name)
assert len(rows) >= 40, f'only found {len(rows)} airlines — AIRLINES shape changed?'
assert len(rows) == len(set(n for n, _, _ in rows)), 'duplicate airline names'


by = collections.defaultdict(list)
for n, _, e in rows:
    by[e].append(n)

TIERS = [
 ('extreme', 'Tier 1 — Assume the sizer will be used',
  'Every bag sized at the gate, especially on full flights. Weight is commonly enforced '
  'too, with handheld scales at the door. Margin of error: zero. Pack to 1&nbsp;cm under '
  'on every axis.'),
 ('very', 'Tier 2 — Sizer very likely',
  'Routine gate sizing, and gate fees well above the price of booking the bag online.'),
 ('strict', 'Tier 3 — Sizer likely',
  'Sized whenever a bag looks borderline, and often as standard on the smaller free bag.'),
 ('moderate', 'Tier 4 — Visual check, sizer if suspicious',
  'Screened by eye as you board; pulled to the sizer only if the bag looks clearly '
  'oversized. A bag comfortably inside the published size usually walks on unchallenged.'),
 ('relaxed', 'Tier 5 — Rarely sized',
  'Gate sizing is uncommon.'),
]

def names(lst):
    out = []
    for n in sorted(lst):
        out.append(f'{n} <em>(ceased operations)</em>' if n in ceased else n)
    return ', '.join(out)

live_hard = sum(len([n for n in by[k] if n not in ceased]) for k in ('extreme','very','strict'))
live_tot  = len([n for n,_,_ in rows if n not in ceased])

body = [
 '    <section class="section" aria-labelledby="enforcement-heading">',
 '      <h2 id="enforcement-heading">How airlines actually measure your bag at the gate</h2>',
 '      <p class="small-text">The published numbers are only half the story. The real '
 'question is <em>how strictly the airline enforces them</em> — and that varies wildly. '
 f'Of the {live_tot} operating airlines in this checker, <strong>{live_hard} sit in the '
 'three strictest bands</strong>: the carriers where a bag a centimetre over becomes a '
 'gate fee. The tiers below are generated from the same data the checker runs on, so they '
 'cannot drift out of step with the results above. '
 '<a href="/carry-on-enforcement-index/">See the full enforcement index, with every '
 'allowance and the methodology →</a></p>',
]
for key, title, desc in TIERS:
    lst = by.get(key, [])
    if not lst: continue
    body += [
      f'\n      <h3>{title} — {len(lst)} airline{"s" if len(lst)!=1 else ""}</h3>',
      f'      <p class="small-text">{names(lst)}. {desc}</p>',
    ]
body.append('    </section>')
new = '\n'.join(body) + '\n'

pat = r'    <section class="section" aria-labelledby="enforcement-heading">.*?</section>\n'
assert len(re.findall(pat, s, re.S)) == 1, 'enforcement section not found exactly once'
s = re.sub(pat, lambda _: new, s, count=1, flags=re.S)

# the generated prose must never name an airline the data does not hold
allnames = {n for n, _, _ in rows}
sec = re.search(pat, s, re.S).group(0)
for cand in re.findall(r'(?<=[>,] )([A-Z][A-Za-z0-9\'’]+(?: [A-Z&][A-Za-z0-9\'’()]+){0,3})', sec):
    if cand in ('Tier','Every','Routine','Sized','Screened','Gate','Margin','Pack','See','Of','The','A'):
        continue
    if cand not in allnames and not any(cand in n for n in allnames):
        print(f'  note: unmatched token in generated prose: {cand!r}', file=sys.stderr)

open(F, 'w', encoding='utf-8').write(s)
print(f'regenerated enforcement section: {len(rows)} airlines, '
      + ', '.join(f'{k}={len(by[k])}' for k,_,_ in TIERS))
print(f'operating: {live_tot}, in the three strictest bands: {live_hard}')
print(f'ceased flagged inline: {sorted(ceased) or "none"}')
