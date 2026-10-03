#!/usr/bin/env python3
"""EU 2027 hand-baggage dataset, built against the actual regulation text.

Source read 3 Oct 2026: Regulation (EU) 2026/2202, OJ L, 2026/2202, 2.10.2026.
ELI http://data.europa.eu/eli/reg/2026/2202/oj

    python3 lft/eu2027/build.py      -> CSVs + workbook into lft/eu2027/out/
"""
import json, csv, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- the rule
# VERIFIED against the primary text, not reporting. Quotes are verbatim.
RULE = {
    'act': 'Regulation (EU) 2026/2202',
    'dated': '2026-09-16',
    'oj': 'OJ L, 2026/2202, 2.10.2026',
    'oj_published': '2026-10-02',
    'in_force': '2026-10-22',          # Art. 3: twentieth day following publication
    'applies_from': '2027-10-23',      # Art. 3: "It shall apply from 23 October 2027."
    'parliament': '2026-07-07',
    'council': '2026-07-13',
    # Art. 2(ah): personal item = unchecked baggage meeting security/safety rules and
    # "EITHER with maximum dimensions of 40 x 30 x 15 cm OR on the condition that it fits
    # under the seat in front". The dimensions are an ALTERNATIVE QUALIFYING TEST, not a
    # minimum an airline must offer.
    'personal_item_cm': (40, 30, 15),
    # Art. 11a(1): a personal item must be carried "at no extra cost". Hand baggage must be
    # permitted "subject to the capacity of the aircraft cabin" - with NO free-of-charge
    # wording. Recital 45 defers uniform hand-baggage dimensions to a future review of
    # Regulation (EC) 1008/2008. There is no 100 cm and no 7 kg anywhere in the act.
    'hand_baggage_free': False,
    'hand_baggage_dimensions_set': False,
}

EEA = {'Europe'}
# Labels that mark a product sold as an extra rather than included in the fare.
PAID_WORDS = ('priority', 'paid', 'upgrade', 'eligible fares', 'purchase', 'add-on', 'addon')
# Labels that describe the item you get on the entry fare.
ENTRY_WORDS = ('free', 'all fares', 'only', 'light', 'basic', 'básico', 'lowfare', 'saver',
               'discount', 'superlight', 'lite', 'go light', 'included')
UNDERSEAT_CODES = ('personal_item', 'small_bag', 'handbag', 'handbag_only', 'no_carry_on', 'lite_bag')


def is_paid(label):
    return any(w in label.lower() for w in PAID_WORDS)


def is_underseat(code, label):
    c = (code or '')
    return any(c.startswith(u) for u in UNDERSEAT_CODES) or 'under-seat' in label.lower()


def qualifies_by_dimension(dims):
    """Does the bag meet the 40x30x15 limb of the Art. 2(ah) definition?"""
    if not dims or any(d is None for d in dims):
        return None
    return all(a <= b for a, b in zip(sorted(dims, reverse=True),
                                      sorted(RULE['personal_item_cm'], reverse=True)))


db = json.load(open(os.path.join(HERE, '..', 'fare-watch', 'airlines.json')))
today = datetime.date.today().isoformat()

fares = []
for a in db['airlines']:
    eea = a.get('region') in EEA
    scope = 'EU/EEA carrier' if eea else 'Non-EU carrier — EU departures only'
    for al in a['allowances']:
        dims, kg = al.get('cm'), al.get('kg')
        label, code = al.get('label', ''), (al.get('code') or '')
        bundled = code.endswith('__personal_item')
        paid = is_paid(label)
        under = is_underseat(code, label)
        by_dim = qualifies_by_dimension(dims)

        if bundled:
            verdict = 'Personal item bundled into a fare — must be free under Art. 11a(1)'
            basis = 'Included in a fare'
        elif under and not paid:
            # This is the entry-fare under-seat item. Art. 11a(1) requires it free.
            verdict = 'Free personal item — already provided'
            basis = 'Entry fare'
        elif under and paid:
            verdict = 'MUST BECOME FREE — a personal item cannot carry a charge (Art. 11a(1))'
            basis = 'Sold as an extra'
        elif paid:
            verdict = 'Price unaffected — but must be in the default displayed fare (Art. 11a(1))'
            basis = 'Sold as an extra'
        else:
            verdict = 'Cabin bag included in this fare — no change'
            basis = 'Included in a fare'

        fares.append({
            'Airline': a['name'],
            'Region': a.get('region') or '',
            'In scope': scope,
            'Fare / product': label,
            'Code': code,
            'Sold as': basis,
            'Under-seat / personal item': 'Yes' if under else '',
            'Max cm': ' x '.join(str(d) for d in dims) if dims else '',
            'Within 40x30x15': {True: 'Yes', False: 'No — qualifies via the under-seat limb instead',
                                None: ''}[by_dim],
            'Weight kg': kg if kg is not None else '',
            'What changes on 23 Oct 2027': verdict,
            'Bundled into a paid fare': 'Yes' if bundled else '',
            'Current add-on price (GBP)': '',      # no verified price data; fill before sending
            'Price source URL': '',
            'Enforcement': a.get('enforcement') or '',
        })

# ------------------------------------------------------------- per airline
summary = []
for a in db['airlines']:
    rows = [f for f in fares if f['Airline'] == a['name']]
    standalone = [r for r in rows if not r['Bundled into a paid fare']]
    # A carrier provides a personal item whether it is sold standalone on the entry fare or
    # bundled inside a fare - both satisfy Art. 11a(1). Counting only standalone rows made
    # 23 carriers look non-compliant when their personal item is simply bundled.
    free_pi = [r for r in rows if r['What changes on 23 Oct 2027'].startswith('Free personal item')]
    bundled_pi = [r for r in rows if r['Bundled into a paid fare'] and r['Under-seat / personal item']]
    charged_pi = [r for r in rows if r['What changes on 23 Oct 2027'].startswith('MUST BECOME FREE')]
    paid_trolley = [r for r in standalone if r['Sold as'] == 'Sold as an extra' and not r['Under-seat / personal item']]
    provides_pi = free_pi or bundled_pi
    summary.append({
        'Airline': a['name'],
        'Region': a.get('region') or '',
        'In scope': rows[0]['In scope'] if rows else '',
        'Free personal item today': ('Yes, on the entry fare' if free_pi else
                                     ('Yes, bundled into a fare' if bundled_pi else
                                      ('Charged' if charged_pi else 'Not recorded in our data'))),
        'Under-seat size': (free_pi or bundled_pi)[0]['Max cm'] if provides_pi else '',
        'Within 40x30x15': (free_pi or bundled_pi)[0]['Within 40x30x15'] if provides_pi else '',
        'Paid trolley products': len(paid_trolley),
        'Must change fare display': ('YES' if paid_trolley and a.get('region') in EEA else
                                     ('Only if it operates EU departures' if paid_trolley else '')),
        'Enforcement': a.get('enforcement') or '',
    })

display_change = [f for f in fares if f['What changes on 23 Oct 2027'].startswith('Price unaffected')]
must_free = [f for f in fares if f['What changes on 23 Oct 2027'].startswith('MUST BECOME FREE')]


def write_csv(name, rows):
    if not rows:
        return
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)


write_csv('every-fare.csv', fares)
write_csv('summary-by-airline.csv', summary)
write_csv('fare-display-must-change.csv', display_change)
if must_free:
    write_csv('personal-items-that-must-become-free.csv', must_free)

# ---------------------------------------------------------------- workbook
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

INK, HEAD, ACCENT = '1A1A1A', '10322E', 'A62558'
wb = Workbook()


def sheet(ws, rows):
    if not rows:
        return
    headers = list(rows[0].keys())
    ws.append(headers)
    for r in rows:
        ws.append([r[h] for h in headers])
    fill, thin = PatternFill('solid', fgColor=HEAD), Side(style='thin', color='D9DDD8')
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = Font(bold=True, color='FFFFFF', size=10); cell.fill = fill
        cell.alignment = Alignment(vertical='center', wrap_text=True)
    ws.row_dimensions[1].height = 34
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(headers)):
        for cell in row:
            cell.border = Border(bottom=thin)
            v = str(cell.value)
            if v.startswith(('MUST', 'NO —', 'YES')):
                cell.font = Font(bold=True, color='A3261F')
            elif v.startswith('Free personal item'):
                cell.font = Font(bold=True, color='1A7F4B')
    for i, h in enumerate(headers, start=1):
        longest = max([len(str(h))] + [len(str(r[h])) for r in rows])
        ws.column_dimensions[get_column_letter(i)].width = min(max(longest + 2, 10), 48)
    ws.freeze_panes = 'A2'; ws.auto_filter.ref = ws.dimensions


ws = wb.active; ws.title = 'Read me'
for text, size, bold in [
    ('EU hand baggage from 23 October 2027 — what the regulation actually does', 16, True),
    ('', 10, False),
    (f'Luggage For Travel (GMK Media Ltd) · {today} · free to quote with attribution', 11, False),
    ('', 10, False),
    ('THE SOURCE — read, not reported', 12, True),
    (RULE['act'] + ' of 16 September 2026, amending Regulation (EC) No 261/2004.', 11, False),
    (RULE['oj'] + ' · ELI http://data.europa.eu/eli/reg/2026/2202/oj', 11, False),
    ('Published in the Official Journal 2 October 2026. In force 22 October 2026.', 11, False),
    ('Article 3: "It shall apply from 23 October 2027."', 11, False),
    ('', 10, False),
    ('WHAT IT DOES', 12, True),
    ('Art. 11a(1): carriers "shall permit passengers to carry a personal item into the cabin and at', 11, False),
    ('no extra cost". Art. 2(ah) defines a personal item as unchecked baggage "either with maximum', 11, False),
    ('dimensions of 40 x 30 x 15 cm or on the condition that it fits under the seat in front".', 11, False),
    ('Art. 11a(1) also requires that "air fares including allowance for a piece of hand baggage shall', 11, False),
    ('be displayed by default before the start of any booking process".', 11, False),
    ('', 10, False),
    ('WHAT IT DOES NOT DO — and most coverage got this wrong', 12, True),
    ('It does not make the cabin trolley free. Art. 11a(1) requires carriers to permit hand baggage', 11, False),
    ('"subject to the capacity of the aircraft cabin" with no free-of-charge wording, and expressly', 11, False),
    ('allows "commercially differentiated offers to passengers who voluntarily choose to travel', 11, False),
    ('without hand baggage".', 11, False),
    ('It does not standardise trolley dimensions. Recital 45 defers uniform minimum hand-baggage', 11, False),
    ('rules to a future review of Regulation (EC) No 1008/2008.', 11, False),
    ('There is no 100 cm and no 7 kg figure anywhere in the act. Those circulated widely in', 11, False),
    ('reporting and are not in the adopted text.', 11, False),
    ('The 40 x 30 x 15 is an alternative qualifying test, not a floor. A smaller bag that fits under', 11, False),
    ('the seat still qualifies, so a carrier whose free bag is under those dimensions is not thereby', 11, False),
    ('non-compliant.', 11, False),
    ('', 10, False),
    ('SCOPE', 12, True),
    ('Art. 3: departures from an EU/EEA airport (any carrier), and flights into the EU/EEA where the', 11, False),
    ('operating carrier is a Union carrier. Non-EU carriers are marked accordingly. A plain reading,', 11, False),
    ('not a legal opinion.', 11, False),
    ('', 10, False),
    ('TWO THINGS NOT TO MISREAD', 12, True),
    ('"Not recorded in our data" in the personal-item column is a gap in this dataset, not a', 11, False),
    ('finding about the airline. Most full-service carriers allow a handbag in addition to a cabin', 11, False),
    ('bag; our source simply does not record it separately. Do not report it as non-compliance.', 11, False),
    ('US domestic carriers appear in the display list only because they sell a paid carry-on. The', 11, False),
    ('rule reaches them only on EU departures, which most of them do not operate.', 11, False),
    ('', 10, False),
    ('NOT IN HERE', 12, True),
    ('Prices. The add-on price columns are empty by design — no verified price data, nothing', 11, False),
    ('estimated. Fill them or delete them before sending.', 11, False),
    ('', 10, False),
    ('Contact: glen@luggagefortravel.com', 11, True),
]:
    ws.append([text])
    ws.cell(row=ws.max_row, column=1).font = Font(size=size, bold=bold,
                                                  color=ACCENT if bold and size >= 12 else INK)
ws.column_dimensions['A'].width = 104

sheet(wb.create_sheet('Summary by airline'), summary)
sheet(wb.create_sheet('Every fare'), fares)
sheet(wb.create_sheet('Fare display must change'), display_change)
if must_free:
    sheet(wb.create_sheet('Personal items charged today'), must_free)

xlsx = os.path.join(OUT, 'EU-hand-baggage-2027-by-airline.xlsx')
wb.save(xlsx)

print(f'{len(db["airlines"])} airlines, {len(fares)} fare products')
print(f'  EU/EEA carriers that must change their fare display: '
      f'{sum(1 for s in summary if s["Must change fare display"] == "YES")}')
print(f'  paid trolley products affected by the display rule: {len(display_change)}')
print(f'  personal items currently charged for (must become free): {len(must_free)}')
print(f'  carriers providing a personal item today: '
      f'{sum(1 for s in summary if s["Free personal item today"].startswith("Yes"))}')
print(f'  personal item not recorded in our data (a data gap, not a finding): '
      f'{sum(1 for s in summary if s["Free personal item today"].startswith("Not recorded"))}')
print(f'\nwrote {xlsx}')
