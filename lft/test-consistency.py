#!/usr/bin/env python3
"""Assert the tool's prose, the tool's data, airlines.json and the data page all agree.

This is the test that was missing. Three separate defects this week came from the same
cause: copy written by hand while the data moved underneath it — Spirit live in the
checker, "Jetstar" invented in the tier prose, and a ceased flag read off the wrong
airline. A count stated in prose is a claim, and claims need a test.
"""
import re, json, sys, collections, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
tool = (ROOT/'checker/tool/carry-on-size-checker.html').read_text(encoding='utf-8')
page = (ROOT/'data/carry-on-enforcement-index.html').read_text(encoding='utf-8')
ds   = json.loads((ROOT/'fare-watch/airlines.json').read_text(encoding='utf-8'))['airlines']

fails = []
def check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + ('' if ok else f'  got {got!r}, want {want!r}'))
    if not ok: fails.append(label)

# ── the tool's own AIRLINES array, parsed per block ─────────────────────────
blocks = re.split(r'(?=\{name:")', tool[tool.index('const AIRLINES=['):tool.index('const FIXED_GUIDES=[')])
tool_rows, tool_ceased = [], set()
for b in blocks:
    m = re.match(r'\{name:"([^"]+)",region:"([^"]+)",enforcement:"([^"]+)"', b)
    if not m: continue
    tool_rows.append(m.groups())
    if re.search(r'\bceased:\{', b): tool_ceased.add(m.group(1))

json_rows = {a['name']: a['enforcement'] for a in ds}
json_ceased = {a['name'] for a in ds if a.get('status') == 'ceased_operations'}

check('tool AIRLINES count == airlines.json count', len(tool_rows), len(json_rows))
check('tool and airlines.json hold the same airlines',
      sorted(n for n,_,_ in tool_rows), sorted(json_rows))
check('enforcement values agree across tool and dataset',
      {n:e for n,_,e in tool_rows}, json_rows)
check('ceased airlines agree across tool and dataset', tool_ceased, json_ceased)

by = collections.defaultdict(list)
for n,_,e in tool_rows: by[e].append(n)
live = [n for n,_,_ in tool_rows if n not in tool_ceased]
hard = len([n for k in ('extreme','very','strict') for n in by[k] if n not in tool_ceased])

# ── every count the tool's prose states must match the data ────────────────
sec = re.search(r'<section class="section" aria-labelledby="enforcement-heading">.*?</section>',
                tool, re.S).group(0)
m = re.search(r'Of the (\d+) operating airlines', sec)
check('tool prose: operating count', int(m.group(1)) if m else None, len(live))
m = re.search(r'<strong>(\d+) sit in the\s*three strictest bands</strong>', sec)
check('tool prose: strictest-band count', int(m.group(1)) if m else None, hard)
for key, n in (('extreme',len(by['extreme'])),('very',len(by['very'])),('strict',len(by['strict'])),
               ('moderate',len(by['moderate'])),('relaxed',len(by['relaxed']))):
    found = re.findall(r'— (\d+) airlines?</h3>', sec)
check('tool prose: five tier headings present', len(re.findall(r'— \d+ airlines?</h3>', sec)), 5)
check('tool prose tier counts, in order',
      [int(x) for x in re.findall(r'— (\d+) airlines?</h3>', sec)],
      [len(by[k]) for k in ('extreme','very','strict','moderate','relaxed')])

# every airline named in the prose must exist in the data
named = set()
# only the paragraph that follows each tier heading is an airline list; the lede is not
for para in re.findall(r'— \d+ airlines?</h3>\s*<p class="small-text">(.*?)\.\s', sec, re.S):
    named |= {re.sub(r'<[^>]*>','',x).strip() for x in para.split(',') if x.strip()}
named = {re.sub(r'\s*\(ceased operations\)$','',n) for n in named}
unknown = sorted(n for n in named if n not in json_rows)
check('no airline named in the prose is absent from the data', unknown, [])

# ── the data page must state the same numbers ──────────────────────────────
m = re.search(r'<strong>(\d+) of (\d+) airlines sit in the three strictest bands</strong>', page)
check('data page: strictest-band count matches tool', int(m.group(1)) if m else None, hard)
check('data page: operating count matches tool',     int(m.group(2)) if m else None, len(live))
m = re.search(r'<span class="lft-n">(\d+)</span>allowances', page)
check('data page: allowance count matches dataset',
      int(m.group(1)) if m else None, sum(len(a['allowances']) for a in ds))

print(f"\n{'FAILED: ' + ', '.join(fails) if fails else 'All consistency checks passed.'}")
sys.exit(1 if fails else 0)
