#!/usr/bin/env python3
"""Parse the tool's AIRLINES array into the same shape as airlines.json.

The tool stores a bundled personal item as a nested `personalItem` object on its parent
allowance, not as a separate row. airlines.json stores it as `<parentcode>__personal_item`.
This maps between the two so they can be compared field by field.
"""
import re, json, sys

def parse(path='carry-on-size-checker.html'):
    s = open(path, encoding='utf-8').read()
    blk = s[s.index('const AIRLINES=['):s.index('const FIXED_GUIDES=[')]
    out = {}
    for b in re.split(r'(?=\{name:")', blk):
        m = re.match(r'\{name:"([^"]+)"', b)
        if not m: continue
        rows = {}
        # split the airline block into one chunk per allowance, so a nested personalItem
        # can only ever be attributed to the allowance it physically sits inside
        chunks = re.split(r'(?=\{code:")', b)
        for ch in chunks:
            cm_ = re.match(r'\{code:"([^"]+)"', ch)
            if not cm_: continue
            code = cm_.group(1)
            # the allowance's own maxCm is the FIRST maxCm in the chunk; a nested
            # personalItem's maxCm comes after the literal "personalItem:{"
            pi_at = ch.find('personalItem:{')
            own = ch[:pi_at] if pi_at != -1 else ch
            mm = re.search(r'maxCm:\[([\d.,\s]+)\]', own)
            if mm: rows[code] = [int(float(x)) for x in mm.group(1).split(',')]
            if pi_at != -1:
                pm = re.search(r'maxCm:\[([\d.,\s]+)\]', ch[pi_at:])
                if pm: rows[code + '__personal_item'] = [int(float(x)) for x in pm.group(1).split(',')]
        out[m.group(1)] = rows
    return out

if __name__ == '__main__':
    tool = parse()
    ds = json.load(open('../../fare-watch/airlines.json'))['airlines']
    diff, missing = [], []
    for a in ds:
        t = tool.get(a['name'], {})
        for al in a['allowances']:
            tv = t.get(al['code'])
            if tv is None: missing.append((a['name'], al['code'], al['cm']))
            elif tv != al['cm']: diff.append((a['name'], al['code'], tv, al['cm']))
    extra = [(n, c) for n, r in tool.items() for c in r
             if c not in {al['code'] for a in ds if a['name'] == n for al in a['allowances']}]
    print(f"tool airlines: {len(tool)}  tool rows: {sum(len(r) for r in tool.values())}")
    print(f"dataset rows : {sum(len(a['allowances']) for a in ds)}")
    print(f"\nVALUE MISMATCHES: {len(diff)}")
    for n,c,t_,d in diff: print(f"  {n:<32} {c:<32} tool={t_} dataset={d}")
    print(f"\nIN DATASET, ABSENT FROM TOOL: {len(missing)}")
    for n,c,d in missing: print(f"  {n:<32} {c:<32} {d}")
    print(f"\nIN TOOL, ABSENT FROM DATASET: {len(extra)}")
    for n,c in extra: print(f"  {n:<32} {c}")
