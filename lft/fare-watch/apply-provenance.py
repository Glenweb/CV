#!/usr/bin/env python3
"""Merge provenance.json into airlines.json: writes `source` and `lastVerified` only.

It never touches a dimension. Where provenance records a mismatch, the dataset keeps its
current value and gains a `dataIssue` note, because a figure read from a search summary is
not good enough to silently overwrite a published allowance with.
"""
import json, pathlib
here = pathlib.Path(__file__).resolve().parent
air = json.loads((here/'airlines.json').read_text(encoding='utf-8'))
prov = json.loads((here/'provenance.json').read_text(encoding='utf-8'))
P, DATE = prov['airlines'], prov['verifiedOn']

applied, issues, before = 0, 0, sum(1 for a in air['airlines'] if a.get('source'))
for a in air['airlines']:
    p = P.get(a['key'])
    if not p:
        continue
    a['source'] = p['source']
    a['verificationMethod'] = p['method']
    # lastVerified means "we checked the figures and they are as recorded". An airline whose
    # page could not be reached has a source URL but was NOT verified — claiming otherwise
    # would make the data page overstate its own provenance.
    if p['method'] == 'not_established':
        a.pop('lastVerified', None)
    else:
        a['lastVerified'] = DATE
    applied += 1
    if p.get('issue'):
        a['dataIssue'] = p['issue']
        issues += 1
    elif 'dataIssue' in a:
        del a['dataIssue']

air['note'] = air.get('note', '')
air['provenanceUpdated'] = DATE
(here/'airlines.json').write_text(json.dumps(air, indent=1, ensure_ascii=False), encoding='utf-8')
nonnull = sum(1 for a in air["airlines"] if a.get("source"))
print(f"provenance records applied: {applied}; non-null source: {before} -> {nonnull} of {len(air['airlines'])}")
ver = sum(1 for a in air["airlines"] if a.get("lastVerified"))
print(f"lastVerified (figures actually checked): {ver} of {len(air['airlines'])}")
print(f"airlines carrying a dataIssue note: {issues}")
print("dimensions changed: 0 (by design)")
