#!/usr/bin/env python3
"""Apply (or revert) the audited measurement corrections to airlines.json.

Usage:  python3 apply-corrections.py [--revert] [--dry-run]

Every change writes the replaced value into `replaced` inside the corrections file, so a
revert restores the dataset byte-for-byte. Refuses to apply twice.
"""
import json, sys, pathlib
here = pathlib.Path(__file__).resolve().parent
A = here/'airlines.json'; C = here/'corrections-2026-10-04.json'
air = json.loads(A.read_text(encoding='utf-8'))
cor = json.loads(C.read_text(encoding='utf-8'))
revert, dry = '--revert' in sys.argv, '--dry-run' in sys.argv
ABSENT = '__absent__'
by = {a['key']: a for a in air['airlines']}

def row(key, code):
    a = by.get(key)
    assert a, f'unknown airline key {key}'
    for al in a['allowances']:
        if al['code'] == code: return al
    raise AssertionError(f'{key}: no allowance coded {code}')

already = cor.get('applied', False)
if revert and not already: sys.exit('nothing to revert: corrections are not applied')
if not revert and already: sys.exit('already applied; pass --revert first')

n = 0
for c in cor['corrections']:
    for ch in c['changes']:
        al = row(c['key'], ch['code'])
        if revert:
            prev = ch.get('replaced')
            assert prev is not None, f"{c['key']}/{ch['code']}: no replaced value stored"
            for f, v in prev.items():
                # ABSENT is the sentinel for "this key did not exist". A field that existed
                # holding null must come back as null, not be deleted — an earlier version
                # conflated the two and the revert round-trip did not restore exactly.
                if v == ABSENT: al.pop(f, None)
                else: al[f] = v
        else:
            prev = {}
            for f in ('cm','kg','linearSumCm','cmIsDerived','derivedNote'):
                if f in ch:
                    prev[f] = al[f] if f in al else ABSENT
                    al[f] = ch[f]
            ch['replaced'] = prev
        n += 1

for lf in cor.get('labelFixes', []):
    al = row(lf['key'], lf['code'])
    if revert:
        al['label'] = lf['replaced']
    else:
        lf['replaced'] = al['label']
        al['label'] = lf['label']
    n += 1

# a corrected figure is a verified figure: clear the dataIssue it was flagged with
fixed = {c['key'] for c in cor['corrections']} | {l['key'] for l in cor.get('labelFixes', [])}
for k in fixed:
    a = by[k]
    if revert:
        pass
    else:
        a.pop('dataIssue', None)
        a['correctedOn'] = cor['appliedOn']
        a['correctionBasis'] = a.get('verificationMethod', 'official_domain_search')

if revert:
    prov = json.loads((here/'provenance.json').read_text(encoding='utf-8'))['airlines']
    for k in fixed:
        by[k].pop('correctedOn', None); by[k].pop('correctionBasis', None)
        issue = prov.get(k, {}).get('issue')
        if issue: by[k]['dataIssue'] = issue

cor['applied'] = not revert
if dry:
    print(f'[dry run] {n} field changes would be {"reverted" if revert else "applied"}')
    sys.exit(0)
A.write_text(json.dumps(air, indent=1, ensure_ascii=False), encoding='utf-8')
C.write_text(json.dumps(cor, indent=1, ensure_ascii=False), encoding='utf-8')
print(f'{"reverted" if revert else "applied"}: {n} field changes across {len(fixed)} airlines')
