#!/usr/bin/env python3
"""Apply (or revert) the 17 lesser-issue fixes. See corrections-lesser-2026-10-04.json.

Usage: python3 apply-lesser.py [--revert] [--dry-run]

Reversible by the same contract as apply-corrections.py: every op records what it replaced,
with an explicit ABSENT sentinel so a field that existed holding null comes back as null
rather than being deleted.
"""
import json, sys, pathlib
ABSENT = '__absent__'
here = pathlib.Path(__file__).resolve().parent
A, C = here/'airlines.json', here/'corrections-lesser-2026-10-04.json'
air = json.loads(A.read_text(encoding='utf-8'))
cor = json.loads(C.read_text(encoding='utf-8'))
revert, dry = '--revert' in sys.argv, '--dry-run' in sys.argv
by = {a['key']: a for a in air['airlines']}

if revert and not cor.get('applied'): sys.exit('nothing to revert')
if not revert and cor.get('applied'): sys.exit('already applied; pass --revert first')

def find(key, code):
    for i, al in enumerate(by[key]['allowances']):
        if al['code'] == code: return i, al
    return None, None

n = 0
ops = list(reversed(cor['ops'])) if revert else cor['ops']
for o in ops:
    als = by[o['key']]['allowances']
    if o['op'] == 'add':
        if revert:
            i, _ = find(o['key'], o['row']['code'])
            assert i is not None, f"{o['key']}: row {o['row']['code']} not found to remove"
            als.pop(i)
        else:
            # An add that duplicates an existing code makes find() ambiguous and the
            # revert pops the wrong row. Caught exactly that on Air Canada.
            existing = {al['code'] for al in als}
            assert o['row']['code'] not in existing, (
                f"{o['key']}: row {o['row']['code']} already exists — use 'set', not 'add'")
            anchor = o.get('after') or o.get('before')
            i, _ = find(o['key'], anchor)
            assert i is not None, f"{o['key']}: anchor {anchor} not found"
            als.insert(i + 1 if 'after' in o else i, json.loads(json.dumps(o['row'])))
    elif o['op'] == 'set':
        _, al = find(o['key'], o['code'])
        assert al, f"{o['key']}/{o['code']} not found"
        if revert:
            for f, v in o['replaced'].items():
                if v == ABSENT: al.pop(f, None)
                else: al[f] = v
        else:
            o['replaced'] = {f: (al[f] if f in al else ABSENT) for f in o['fields']}
            al.update(o['fields'])
    elif o['op'] == 'drop_field':
        _, al = find(o['key'], o['code'])
        assert al, f"{o['key']}/{o['code']} not found"
        if revert:
            for f, v in o['replaced'].items():
                if v != ABSENT: al[f] = v
        else:
            o['replaced'] = {f: (al[f] if f in al else ABSENT) for f in o['fields']}
            for f in o['fields']: al.pop(f, None)
    elif o['op'] == 'recode':
        if not revert:
            # the recode target must not already exist, for the same reason an add must not
            existing = {al['code'] for al in als}
            assert o['newCode'] not in existing, (
                f"{o['key']}: {o['newCode']} already exists — recode would duplicate it")
        src = o['newCode'] if revert else o['code']
        _, al = find(o['key'], src)
        assert al, f"{o['key']}/{src} not found"
        if revert:
            al['code'] = o['code']
            for f, v in o['replaced'].items():
                if v == ABSENT: al.pop(f, None)
                else: al[f] = v
        else:
            o['replaced'] = {f: (al[f] if f in al else ABSENT) for f in o['fields']}
            al['code'] = o['newCode']
            al.update(o['fields'])
    else:
        sys.exit(f"unknown op {o['op']}")
    n += 1

cor['applied'] = not revert
if dry:
    print(f'[dry run] {n} operations would be {"reverted" if revert else "applied"}')
    sys.exit(0)
A.write_text(json.dumps(air, indent=1, ensure_ascii=False), encoding='utf-8')
C.write_text(json.dumps(cor, indent=1, ensure_ascii=False), encoding='utf-8')
print(f'{"reverted" if revert else "applied"}: {n} operations across {len({o["key"] for o in cor["ops"]})} airlines')
