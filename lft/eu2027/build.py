#!/usr/bin/env python3
"""Builds the EU 2027 hand-baggage dataset from the checker's own airline data.

Journalist-facing. Every computed column is derived from two things only: the
published allowance data, and the regulation thresholds set in RULE below. Change
a threshold, re-run, and the whole analysis moves with it.

    python3 lft/eu2027/build.py

Writes CSVs plus an .xlsx into lft/eu2027/out/.
"""
import json, csv, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- the rule
# Sourced from reporting on the adopted regulation, NOT yet read against the
# Official Journal text. Treat every figure here as pending verification.
RULE = {
    'personal_item_cm': (40, 30, 15),   # free, must fit under the seat
    'cabin_linear_cm': 100,             # free, total of the three dimensions
    'cabin_kg': 7,
    'applies_from': '2027-10-23',       # expected; verify at source
    'parliament': '2026-07-07',
    'council': '2026-07-13',
}
EU_PERSONAL_SORTED = sorted(RULE['personal_item_cm'], reverse=True)

EEA_REGIONS = {'Europe'}

PAID_WORDS = ('priority', 'paid', 'upgrade', 'eligible fares', 'purchase', 'add-on', 'addon')
FREE_WORDS = ('free', 'all fares', 'included', 'complimentary')

def fare_basis(label):
    """Derive whether a fare product is free or paid from its label.
    Heuristic, so the raw label ships alongside it for checking."""
    low = label.lower()
    if any(w in low for w in PAID_WORDS):
        return 'Paid / fare-gated'
    if any(w in low for w in FREE_WORDS):
        return 'Free with every fare'
    return 'Unclear — check label'

def meets_floor(dims):
    """Does this allowance permit at least the EU free personal item?"""
    if not dims or any(d is None for d in dims):
        return None
    return all(a >= b for a, b in zip(sorted(dims, reverse=True), EU_PERSONAL_SORTED))

def load():
    with open(os.path.join(HERE, '..', 'fare-watch', 'airlines.json')) as f:
        return json.load(f)

db = load()
today = datetime.date.today().isoformat()

# ---------------------------------------------------------------- fare rows
fares = []
for a in db['airlines']:
    eea = a.get('region') in EEA_REGIONS
    for al in a['allowances']:
        dims = al.get('cm')
        linear = sum(dims) if dims and all(d is not None for d in dims) else None
        kg = al.get('kg')
        label = al.get('label', '')
        code = al.get('code') or ''
        basis = fare_basis(label)
        paid = basis == 'Paid / fare-gated'
        floor_ok = meets_floor(dims)

        # A row whose code ends __personal_item is the free item bundled INSIDE a fare.
        # It inherits its parent's label, so without this flag a paid parent makes it
        # look like an add-on the regulation abolishes. It is not one.
        bundled = code.endswith('__personal_item')
        is_personal = 'personal_item' in code or 'under-seat' in label.lower()

        # Distance from the free cabin entitlement, in cm. Negative means inside it.
        margin = None if linear is None else linear - RULE['cabin_linear_cm']

        if linear is None:
            verdict = 'No dimensions published'
        elif bundled:
            verdict = 'Bundled with a paid fare — free under the entitlement regardless'
        elif not paid:
            if floor_ok is False:
                verdict = 'MUST INCREASE — free allowance is below 40x30x15'
            elif margin > 0:
                verdict = 'Already more generous than the free entitlement'
            else:
                verdict = 'Already within the free entitlement'
        else:
            if margin > 0:
                verdict = 'Survives only for bags above the free entitlement'
            elif kg is None:
                verdict = 'Becomes free on size — no weight limit published, check'
            elif kg <= RULE['cabin_kg']:
                verdict = 'BECOMES FREE — this product cannot be sold'
            else:
                verdict = 'Becomes free on size; weight limit above 7kg, check'

        fares.append({
            'Airline': a['name'],
            'Region': a.get('region') or '',
            'In scope': 'EU/EEA carrier' if eea else 'Non-EU carrier — EU departures only',
            'Fare / product': label,
            'Code': code,
            'Free or paid (derived)': basis,
            'Max cm': ' x '.join(str(d) for d in dims) if dims else '',
            'Linear cm': linear if linear is not None else '',
            'Weight kg': kg if kg is not None else '',
            'Meets the free 40x30x15 floor': {True: 'Yes', False: 'NO — below the floor', None: ''}[floor_ok],
            'cm vs the free 100cm entitlement': (('+%d' % margin) if margin > 0 else str(margin)) if margin is not None else '',
            'What changes on 23 Oct 2027': verdict,
            'Under-seat / personal item': 'Yes' if is_personal else '',
            'Bundled into a paid fare': 'Yes' if bundled else '',
            'Current add-on price (GBP)': '',          # deliberately blank - no verified price data
            'Price source URL': '',
            'Enforcement': a.get('enforcement') or '',
        })

# ------------------------------------------------------- per-airline summary
summary = []
for a in db['airlines']:
    rows = [f for f in fares if f['Airline'] == a['name']]
    free_rows = [r for r in rows if r['Free or paid (derived)'] == 'Free with every fare']
    paid_rows = [r for r in rows if r['Free or paid (derived)'] == 'Paid / fare-gated']
    # The best free allowance they offer today, by linear size.
    best_free = max((r for r in free_rows if r['Linear cm'] != ''), key=lambda r: r['Linear cm'], default=None)
    below = [r for r in rows if r['What changes on 23 Oct 2027'].startswith('MUST INCREASE')]
    killed = [r for r in rows if r['What changes on 23 Oct 2027'].startswith('BECOMES FREE')]
    shrunk = [r for r in rows if r['What changes on 23 Oct 2027'].startswith('Survives only')]
    summary.append({
        'Airline': a['name'],
        'Region': a.get('region') or '',
        'In scope': 'EU/EEA carrier' if a.get('region') in EEA_REGIONS else 'Non-EU carrier — EU departures only',
        'Fare products listed': len(rows),
        'Best free allowance today': best_free['Max cm'] if best_free else '',
        'Free allowance meets the 40x30x15 floor': 'NO' if below else ('Yes' if free_rows else ''),
        'Free products below the floor': len(below),
        'Paid products that become free': len(killed),
        'Paid products only partly superseded': len(shrunk),
        'Enforcement': a.get('enforcement') or '',
    })

# ------------------------------------------------- the headline: what changes
changes = [f for f in fares if f['What changes on 23 Oct 2027'].startswith('BECOMES FREE')]
shrinks = [f for f in fares if f['What changes on 23 Oct 2027'].startswith('Survives only')]
below_floor = [f for f in fares if f['What changes on 23 Oct 2027'].startswith('MUST INCREASE')]

def write_csv(name, rows):
    if not rows:
        return
    p = os.path.join(OUT, name)
    with open(p, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    return p

write_csv('every-fare.csv', fares)
write_csv('summary-by-airline.csv', summary)
write_csv('paid-products-that-become-free.csv', changes)
write_csv('paid-products-that-shrink.csv', shrinks)
write_csv('free-allowances-below-the-floor.csv', below_floor)

# ---------------------------------------------------------------- workbook
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

INK = '1A1A1A'; HEAD = '10322E'; ACCENT = 'A62558'
wb = Workbook()

def style_sheet(ws, rows, widths=None, freeze='A2'):
    if not rows:
        return
    headers = list(rows[0].keys())
    ws.append(headers)
    for r in rows:
        ws.append([r[h] for h in headers])
    hf = Font(bold=True, color='FFFFFF', size=10)
    fill = PatternFill('solid', fgColor=HEAD)
    thin = Side(style='thin', color='D9DDD8')
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = hf; cell.fill = fill
        cell.alignment = Alignment(vertical='center', wrap_text=True)
    ws.row_dimensions[1].height = 34
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(headers)):
        for cell in row:
            cell.border = Border(bottom=thin)
            cell.alignment = Alignment(vertical='top', wrap_text=False)
            v = str(cell.value)
            if v.startswith('NO') or v.startswith('MUST INCREASE'):
                cell.font = Font(bold=True, color='A3261F')
            elif v.startswith('BECOMES FREE'):
                cell.font = Font(bold=True, color='1A7F4B')
    for i, h in enumerate(headers, start=1):
        longest = max([len(str(h))] + [len(str(r[h])) for r in rows])
        ws.column_dimensions[get_column_letter(i)].width = min(max(longest + 2, 10), 46)
    ws.freeze_panes = freeze
    ws.auto_filter.ref = ws.dimensions

# Read me
ws = wb.active; ws.title = 'Read me'
readme = [
    ('EU hand baggage rules 2027 — what changes, airline by airline', 16, True),
    ('', 10, False),
    (f'Compiled by Luggage For Travel (GMK Media Ltd) · {today}', 11, False),
    ('luggagefortravel.com · free to quote with attribution', 11, False),
    ('', 10, False),
    ('WHAT THIS IS', 12, True),
    ('Published cabin-baggage allowances for %d airlines, %d fare products in total, set against the' % (len(db['airlines']), len(fares)), 11, False),
    ('incoming EU entitlement. Most reporting so far has covered the rule. This covers what it costs', 11, False),
    ('each airline to comply, fare by fare.', 11, False),
    ('', 10, False),
    ('THE RULE, AS USED IN THIS ANALYSIS', 12, True),
    ('Free personal item: %d x %d x %d cm, under the seat' % RULE['personal_item_cm'], 11, False),
    ('Free cabin bag: %d cm total of the three dimensions, %d kg' % (RULE['cabin_linear_cm'], RULE['cabin_kg']), 11, False),
    ('Fares must be shown inclusive of hand baggage at the start of booking', 11, False),
    ('Parliament %s · Council %s · application expected %s' % (RULE['parliament'], RULE['council'], RULE['applies_from']), 11, False),
    ('', 10, False),
    ('VERIFICATION STATUS — READ BEFORE PUBLISHING', 12, True),
    ('The allowance data is taken from each airline\'s published terms and is the basis of a live', 11, False),
    ('public tool. The REGULATION figures above are from reporting on the adopted text and have NOT', 11, False),
    ('been read against the Official Journal. Verify them at source before printing.', 11, False),
    ('', 10, False),
    ('SCOPE — the honest caveat', 12, True),
    ('EU/EEA carriers are treated as in scope. Non-EU carriers are marked as in scope on EU', 11, False),
    ('departures only. That is a plain reading, not a legal opinion, and a lawyer should confirm it', 11, False),
    ('before it is asserted as fact.', 11, False),
    ('', 10, False),
    ('WHAT IS NOT IN HERE', 12, True),
    ('Prices. The add-on price columns are deliberately empty. No verified price data was available', 11, False),
    ('and nothing has been estimated. Those columns are for filling, not for citing as they stand.', 11, False),
    ('', 10, False),
    ('THE SHEETS', 12, True),
    ('Summary by airline — one row per carrier, the at-a-glance view', 11, False),
    ('Every fare — all %d products with the full working' % len(fares), 11, False),
    ('Paid becomes free — add-ons the entitlement abolishes outright', 11, False),
    ('Paid products that shrink — add-ons surviving only for oversized bags', 11, False),
    ('Below the floor — free allowances smaller than 40 x 30 x 15', 11, False),
    ('', 10, False),
    ('Contact: glen@luggagefortravel.com', 11, True),
]
for text, size, bold in readme:
    ws.append([text])
    c = ws.cell(row=ws.max_row, column=1)
    c.font = Font(size=size, bold=bold, color=ACCENT if bold and size >= 12 else INK)
ws.column_dimensions['A'].width = 108

style_sheet(wb.create_sheet('Summary by airline'), summary)
style_sheet(wb.create_sheet('Every fare'), fares)
if changes:
    style_sheet(wb.create_sheet('Paid becomes free'), changes)
if shrinks:
    style_sheet(wb.create_sheet('Paid products that shrink'), shrinks)
if below_floor:
    style_sheet(wb.create_sheet('Below the floor'), below_floor)

xlsx = os.path.join(OUT, 'EU-hand-baggage-2027-by-airline.xlsx')
wb.save(xlsx)

# ---------------------------------------------------------------- what it found
print(f'{len(db["airlines"])} airlines, {len(fares)} fare products')
print(f'  EU/EEA carriers: {sum(1 for s in summary if s["In scope"].startswith("EU/EEA"))}')
print(f'  Paid products fully superseded (become free): {len(changes)}')
print(f'  Paid products only partly superseded: {len(shrinks)}')
print(f'  Free allowances below the 40x30x15 floor: {len(below_floor)}')
print(f'  Airlines with at least one free allowance below the floor: '
      f'{sum(1 for s in summary if s["Free allowance meets the 40x30x15 floor"] == "NO")}')
print(f'\nwrote {xlsx}')
