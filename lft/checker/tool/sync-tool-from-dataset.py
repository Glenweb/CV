#!/usr/bin/env python3
"""Rewrite the tool's AIRLINES dimensions from lft/fare-watch/airlines.json.

airlines.json is the source of truth. The tool carries its own copy in a different shape
(maxCm/maxIn, with a bundled personal item nested as `personalItem` on its parent), and the
two had silently diverged on 42 rows — every correction from the 4 Oct audit had been
applied to the dataset only, while the live tool kept the wrong figures.

Run after any change to airlines.json. test-consistency.py fails if they drift again.
"""
import re, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
F = HERE/'carry-on-size-checker.html'
DS = json.loads((HERE/'../../fare-watch/airlines.json').read_text(encoding='utf-8'))['airlines']
by_name = {a['name']: a for a in DS}

s = F.read_text(encoding='utf-8')
start, end = s.index('const AIRLINES=['), s.index('const FIXED_GUIDES=[')
head, blk, tail = s[:start], s[start:end], s[end:]

def inches(cm):
    return '[' + ','.join(f'{round(v/2.54, 1):g}' for v in cm) + ']'
def cms(cm):
    return '[' + ','.join(str(v) for v in cm) + ']'

edits = added_pi = added_row = 0
out_blocks = []
for b in re.split(r'(?=\{name:")', blk):
    m = re.match(r'\{name:"([^"]+)"', b)
    if not m:
        out_blocks.append(b); continue
    name = m.group(1)
    a = by_name.get(name)
    assert a, f'tool has an airline absent from the dataset: {name}'
    want = {al['code']: al for al in a['allowances']}

    chunks = re.split(r'(?=\{code:")', b)
    new_chunks = []
    for ch in chunks:
        cm_ = re.match(r'\{code:"([^"]+)"', ch)
        if not cm_:
            new_chunks.append(ch); continue
        code = cm_.group(1)
        row = want.get(code)
        assert row, f'{name}: tool row {code} is not in the dataset'
        pi_at = ch.find('personalItem:{')
        own, rest = (ch[:pi_at], ch[pi_at:]) if pi_at != -1 else (ch, '')

        def swap(txt, cm):
            """Rewrite maxCm from the dataset, and regenerate maxIn ONLY when maxCm
            actually changed. US and Canadian carriers publish round inch figures
            (18 x 14 x 8, 22 x 14 x 9) that are not exact conversions of their own
            centimetre figures; an earlier version overwrote Spirit's published
            18 x 14 x 8 with 17.7 x 13.8 x 7.9. The size comparison runs in centimetres,
            so maxIn is display only. `maxCm:null` is how the tool recorded "allowed,
            size unknown" — Qantas, ANA and AirAsia all did."""
            global edits
            n0 = txt
            cur = re.search(r'maxCm:(?:\[([\d.,\s]+)\]|null)', txt)
            cur_cm = [int(float(x)) for x in cur.group(1).split(',')] if (cur and cur.group(1)) else None
            if cur_cm != cm:
                txt = re.sub(r'maxIn:(?:\[[\d.,\s]+\]|null)', 'maxIn:' + inches(cm), txt, count=1)
                txt = re.sub(r'maxCm:(?:\[[\d.,\s]+\]|null)', 'maxCm:' + cms(cm), txt, count=1)
                if txt != n0: edits += 1
            return txt
        own = swap(own, row['cm'])
        # carry the linear-sum limit so the verdict logic can enforce it
        if row.get('linearSumCm'):
            if 'linearSumCm:' in own:
                own = re.sub(r'linearSumCm:\d+', f"linearSumCm:{row['linearSumCm']}", own, count=1)
            else:
                own = own.replace('maxCm:' + cms(row['cm']) + ',',
                                  'maxCm:' + cms(row['cm']) + f",linearSumCm:{row['linearSumCm']},", 1)

        pi = want.get(code + '__personal_item')
        if rest and pi:
            rest = swap(rest, pi['cm'])
        elif pi and not rest:
            # dataset gained a bundled personal item the tool has no object for
            note = pi.get('advisoryNote') or 'Personal item also allowed'
            inject = (f'\n   personalItem:{{maxIn:{inches(pi["cm"])},maxCm:{cms(pi["cm"])},'
                      f'note:"{note.replace(chr(34), chr(39))}"}},')
            own = re.sub(r'personalItemIncluded:false,personalItem:null,',
                         'personalItemIncluded:true,' + inject.strip(), own, count=1)
            assert 'personalItem:{' in own, f'{name}/{code}: could not inject personal item'
            added_pi += 1
        new_chunks.append(own + rest)

    nb = ''.join(new_chunks)
    # allowance rows present in the dataset but entirely absent from the tool
    have = {re.match(r'\{code:"([^"]+)"', c).group(1) for c in chunks if re.match(r'\{code:"', c)}
    for code, row in want.items():
        if code.endswith('__personal_item') or code in have: continue
        w = row.get('weight') or {}
        new = ('  {code:"%s",label:"%s",maxIn:%s,maxCm:%s,\n'
               '   weight:{policy:"%s",kg:%s,lb:%s,note:"%s"},\n'
               '   personalItemIncluded:false,personalItem:null,\n'
               '   advisoryNote:"%s"},\n') % (
            code, row['label'], inches(row['cm']), cms(row['cm']),
            w.get('policy','none'), w.get('kg') if w.get('kg') is not None else 'null',
            w.get('lb') if w.get('lb') is not None else 'null', w.get('note',''),
            (row.get('advisoryNote') or '').replace('"', "'"))
        nb = nb.replace('allowances:[\n', 'allowances:[\n' + new, 1)
        added_row += 1
    out_blocks.append(nb)

F.write_text(head + ''.join(out_blocks) + tail, encoding='utf-8')
print(f'dimension swaps: {edits} | personal items injected: {added_pi} | rows added: {added_row}')
