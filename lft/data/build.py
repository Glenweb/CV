#!/usr/bin/env python3
"""Generate the citable enforcement-index data page + downloadable dataset
from lft/fare-watch/airlines.json. Never hand-edit the outputs."""
import json, csv, html, collections, datetime, pathlib

SRC = pathlib.Path(__file__).resolve().parents[1] / 'fare-watch' / 'airlines.json'
d = json.load(open(SRC, encoding='utf-8'))
ALL = d['airlines']
TODAY = datetime.date.today().isoformat()
BASE = 'https://luggagefortravel.com'
PAGE = f'{BASE}/carry-on-enforcement-index/'

# Spirit has ceased: it belongs in the archive, not in a table of who will size your bag.
live    = [a for a in ALL if a.get('status') != 'ceased_operations']
ceased  = [a for a in ALL if a.get('status') == 'ceased_operations']

TIERS = [
    ('extreme', 'Assume the sizer', 'Every bag sized at the gate. Weight often enforced with handheld scales. Margin of error: zero.'),
    ('very',    'Sizer very likely', 'Routine gate sizing, particularly on full flights.'),
    ('strict',  'Sizer likely',      'Sized whenever a bag looks borderline, and often as standard on the small free bag.'),
    ('moderate','Visual check',      'Screened by eye on boarding; pulled to the sizer only if clearly oversized.'),
    ('relaxed', 'Rarely sized',      'Gate sizing is uncommon.'),
]
by = collections.defaultdict(list)
for a in live: by[a['enforcement']].append(a)

hard = sum(len(by[k]) for k in ('extreme','very','strict'))
prov_known = sum(1 for a in ALL if a.get('source'))
verified   = sum(1 for a in ALL if a.get('lastVerified'))

def cm(x): return '—' if not x else '%d × %d × %d cm' % tuple(x)
def inch(x): return '' if not x else '%d × %d × %d in' % tuple(round(v/2.54) for v in x)
def kg(w): return f"{w} kg" if w else '—'

# ── flat dataset: one row per allowance ──────────────────────────────────────
rows = []
for a in ALL:
    for al in a['allowances']:
        rows.append({
            'airline': a['name'], 'key': a['key'], 'region': a['region'],
            'enforcement': a['enforcement'],
            'status': a.get('status', 'operating'),
            'ceased_on': a.get('ceasedOn', ''),
            'allowance_code': al['code'], 'allowance_label': al['label'],
            'length_cm': al['cm'][0] if al.get('cm') else '',
            'width_cm':  al['cm'][1] if al.get('cm') else '',
            'height_cm': al['cm'][2] if al.get('cm') else '',
            'weight_kg': al.get('kg') or '',
            'source': a.get('source') or '', 'last_verified': a.get('lastVerified') or '',
        })
with open('lft-carry-on-allowances.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
json.dump({'name':'LFT Carry-On Allowance & Enforcement Index','version':TODAY,
           'licence':'CC BY 4.0 — attribution to luggagefortravel.com required',
           'source_page':PAGE,'airlines':len(ALL),'allowances':len(rows),'rows':rows},
          open('lft-carry-on-allowances.json','w',encoding='utf-8'), indent=1, ensure_ascii=False)

# ── the page ────────────────────────────────────────────────────────────────
def tier_table(items):
    out = ['<table class="lft-table"><thead><tr><th>Airline</th><th>Region</th>'
           '<th>Free cabin bag</th><th>Larger / paid bag</th></tr></thead><tbody>']
    for a in sorted(items, key=lambda x: x['name']):
        als = a['allowances']
        free = next((x for x in als if x['code'] in ('personal_item','standard_cabin')), None)
        paid = next((x for x in als if x['code'] in ('paid_carry_on','priority_cabin')), None)
        def cell(al):
            if not al: return '<td>—</td>'
            i = inch(al.get('cm'))
            wt = kg(al.get('kg'))
            return (f"<td><strong>{cm(al['cm'])}</strong>"
                    + (f'<br><span class="lft-sub">≈{i}</span>' if i else '')
                    + (f'<br><span class="lft-sub">{wt}</span>' if al.get('kg') else '')
                    + f'<br><span class="lft-sub">{html.escape(al["label"])}</span></td>')
        out.append(f"<tr><td><strong>{html.escape(a['name'])}</strong></td>"
                   f"<td>{html.escape(a['region'])}</td>{cell(free)}{cell(paid)}</tr>")
    out.append('</tbody></table>')
    return '\n'.join(out)

tiers_html = []
for key, label, desc in TIERS:
    items = by.get(key, [])
    if not items: continue
    tiers_html.append(
f'''<h3 id="tier-{key}">{label} — {len(items)} airline{'s' if len(items)!=1 else ''}
<span class="lft-tier lft-tier--{key}">{key}</span></h3>
<p class="lft-sub">{desc}</p>
{tier_table(items)}''')

ld = {
 "@context":"https://schema.org","@type":"Dataset",
 "name":"Carry-On Allowance & Enforcement Index",
 "description":(f"Cabin baggage allowances for {len(ALL)} airlines ({len(rows)} distinct "
                "allowances), each classified by how strictly the airline enforces the limit "
                "at the gate. Maintained by Luggage for Travel."),
 "url":PAGE,"version":TODAY,"dateModified":TODAY,
 "license":"https://creativecommons.org/licenses/by/4.0/",
 "isAccessibleForFree":True,
 "creator":{"@type":"Organization","name":"Luggage for Travel","url":BASE+"/"},
 "variableMeasured":["airline","region","enforcement tier","allowance type",
                     "maximum dimensions (cm)","maximum weight (kg)"],
 "distribution":[
   {"@type":"DataDownload","encodingFormat":"text/csv",
    "contentUrl":f"{BASE}/data/lft-carry-on-allowances.csv"},
   {"@type":"DataDownload","encodingFormat":"application/json",
    "contentUrl":f"{BASE}/data/lft-carry-on-allowances.json"}]}

page = f'''<!--
  LFT — /carry-on-enforcement-index/   GENERATED {TODAY} by lft/data/build.py
  Do not hand-edit. Change lft/fare-watch/airlines.json and re-run.
  Paste into a WordPress "Custom HTML" block. Needs lft/content/content.css
  plus the extra rules in lft/data/data.css.
-->

<p class="lft-lede"><strong>Every airline publishes a carry-on size. Almost none publishes
how strictly it enforces one.</strong> This index pairs the published allowance with an
enforcement rating for {len(live)} operating airlines — {len(rows)} distinct allowances in
all — so you can tell the difference between a limit that is a guideline and a limit that
is a gate fee.</p>

<div class="lft-stats">
  <div><span class="lft-n">{len(live)}</span>airlines</div>
  <div><span class="lft-n">{len(rows)}</span>allowances</div>
  <div><span class="lft-n">{hard}</span>will size your bag</div>
  <div><span class="lft-n">{len(by.get('relaxed',[]))}</span>rarely will</div>
</div>

<p><strong>{hard} of {len(live)} airlines sit in the three strictest bands</strong> — these
are the carriers where a bag a centimetre over becomes a gate fee.
{len(by.get('moderate',[]))} screen visually and only pull obvious offenders.
{len(by.get('relaxed',[]))} rarely size at all.</p>

<p><a href="/carry-on-size-checker/"><strong>Check your own bag against any airline in this
index →</strong></a></p>

<h2>The index</h2>
{''.join(tiers_html)}

<h2>Archive — airlines no longer operating</h2>
<p class="lft-sub">Kept for reference. These allowances no longer apply to any bookable flight.</p>
{tier_table(ceased) if ceased else '<p class="lft-sub">None.</p>'}

<h2>Methodology, and its limits</h2>
<ul>
  <li><strong>Dimensions</strong> are recorded in centimetres as published by each airline.
      Inch figures shown here are converted and rounded to the nearest inch — use the
      centimetre values for anything that matters.</li>
  <li><strong>Allowances are fare-aware.</strong> Where a cheaper fare includes only an
      under-seat personal item and a higher fare adds an overhead bag, both are recorded
      separately rather than averaged into one number.</li>
  <li><strong>Enforcement ratings are our editorial classification</strong>, not an airline
      statement. They reflect documented gate-check behaviour — whether sizers are in
      routine use, whether weight is checked, and how often passengers report being
      charged at the gate. They are a judgement, and we label them as one.</li>
  <li><strong>Provenance is incomplete.</strong> Per-airline source URLs are populated for
      {prov_known} of {len(ALL)} records and last-verified dates for {verified} of {len(ALL)}.
      We are filling these in; until then, treat the dimensions as accurate to our last
      review rather than to a dated citation, and confirm anything load-bearing against the
      airline directly.</li>
  <li><strong>Airlines change allowances without notice.</strong> This index is versioned by
      date, not presented as permanent.</li>
</ul>

<h2>Use this data</h2>
<p>Free to use, including commercially, under
<a href="https://creativecommons.org/licenses/by/4.0/" rel="nofollow">CC BY 4.0</a>, with
attribution to Luggage for Travel.</p>

<ul>
  <li><a href="/data/lft-carry-on-allowances.csv">Download CSV</a> — {len(rows)} rows, one per allowance</li>
  <li><a href="/data/lft-carry-on-allowances.json">Download JSON</a> — same data, nested</li>
</ul>

<p><strong>Citing it:</strong></p>
<pre class="lft-cite">Carry-On Allowance &amp; Enforcement Index, Luggage for Travel ({TODAY}).
&lt;a href="{PAGE}"&gt;{PAGE}&lt;/a&gt;</pre>

<p class="lft-sub">Writing something that uses this and need a figure checked, a quote, or a
cut of the data you cannot get from the CSV? Ask — we would rather you published something
correct.</p>

<p class="lft-sub">Version {TODAY}. Maintained by GMK Media Ltd.</p>

<script type="application/ld+json">
{json.dumps(ld, indent=1)}
</script>
'''
open('carry-on-enforcement-index.html','w',encoding='utf-8').write(page)
print(f"page: {len(page):,} bytes")
print(f"dataset: {len(rows)} allowance rows across {len(ALL)} airlines ({len(live)} operating, {len(ceased)} ceased)")
print(f"tiers: " + ', '.join(f"{k}={len(by.get(k,[]))}" for k,_,_ in TIERS))
print(f"hard-band total (extreme+very+strict, operating only) = {hard}")
print(f"provenance: source on {prov_known}/{len(ALL)}, lastVerified on {verified}/{len(ALL)}")
