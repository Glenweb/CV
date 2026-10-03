# EU 2027 hand-baggage dataset

The journalist-facing asset. Generated from the checker's own airline data, so it cannot
drift from the live tool.

```bash
python3 lft/eu2027/build.py      # writes CSVs + the workbook into lft/eu2027/out/
```

**Every threshold is a parameter** in `RULE` at the top of `build.py`. If the Official
Journal text turns out to say something different from 40×30×15 / 100cm / 7kg, change one
dict and the entire analysis re-derives.

## What it found, and it is not the story we assumed

The working assumption was "the N fare types that stop existing on 23 October 2027". **That
story is wrong.** On the published data:

**No paid cabin-bag product is abolished.** All seven survive, because every one of them
allows a bag larger than the 100cm free entitlement:

| Airline | Paid product | Over the free entitlement by |
|---|---|---|
| Ryanair | Priority / paid overhead cabin bag (55×40×20, 10kg) | +15cm |
| Wizz Air | WIZZ Priority trolley bag (55×40×23, 10kg) | +18cm |
| Aer Lingus | Cabin bag, Plus fare (55×40×24, 10kg) | +19cm |
| easyJet | Large cabin bag (56×45×25, 15kg) | +26cm |
| Allegiant | Paid carry-on (56×36×23) | +15cm |
| Spirit | Paid carry-on (56×46×25) | +27cm |
| Frontier | Paid carry-on (61×41×25, 15.9kg) | +27cm |

What actually happens is that these products **shrink to covering only the band above
100cm**. A passenger whose bag fits the free entitlement stops needing to buy one. That is a
more defensible finding than "they disappear", and more interesting, because it tells you
what the airlines will do next: reprice and resize, not withdraw.

**Nine carriers must increase a free allowance.** This is the harder-edged finding:

| Airline | Free allowance today | Shortfall |
|---|---|---|
| **Lufthansa** | 40 × 30 × **10** | 5cm too shallow |
| **Swiss** | 40 × 30 × **10** | 5cm too shallow |
| **Austrian** | 40 × 30 × **10** | 5cm too shallow |
| Norwegian | **25** × 33 × 20 | 15cm too narrow |
| Aer Lingus | **25** × 33 × 20 | 15cm too narrow |
| Iberia | 35 × **20** × 20 | 10cm short |
| SAS | 37 × **28** × 15 | 3cm short |
| United | 43 × **25** × 23 | EU departures only |
| Scoot | 35 × **25** × 15 | EU departures only |

**The Lufthansa Group is the story.** Lufthansa, Swiss and Austrian all sit at 40×30×10 —
the same 10cm depth, 5cm under the incoming floor, three carriers, one group. Nobody has
reported that, and it is checkable in thirty seconds against their own published terms.

One detail worth a line on its own: **easyJet's free cabin bag is 101cm linear — one
centimetre more generous than the entitlement it is about to be measured against.**

## What the file deliberately does not contain

**Prices.** The add-on price columns are empty on purpose. There was no verified price data,
nothing has been estimated, and a journalist who finds one invented number discards the
whole dataset. Fill them from the airlines' own booking flows before sending.

## Before this goes to anyone

1. **Verify the regulation figures against the Official Journal.** They come from reporting
   on the adopted text, not from the text. They are the spine of every computed column.
2. **Verify the 23 October 2027 application date** at source.
3. **Get the scope reading checked.** EU/EEA carriers are treated as in scope; non-EU
   carriers are marked in scope on EU departures only. That is a plain reading, not a legal
   opinion.
4. **Fill the price columns**, or delete them before sending.
5. **Spot-check five airlines** against their own published terms. If one is wrong the
   dataset is worthless, and it is a twenty-minute job.

## Sheets

| Sheet | What it is |
|---|---|
| Read me | Provenance, the rule as applied, verification status, scope caveat |
| Summary by airline | One row per carrier — the at-a-glance view |
| Every fare | All 112 products with the full working |
| Paid products that shrink | The seven add-ons that survive, and by how much |
| Below the floor | The nine free allowances that must increase |

## Classification note

A row whose code ends `__personal_item` is the free item bundled **inside** a fare, and it
inherits its parent's label. An earlier version counted those as paid add-ons, which
produced five phantom "products that become free" and double-counted the below-floor list
at 18 instead of 9. They are now flagged and excluded from both analyses. If you extend
this script, keep that distinction — it is the one place the data invites a wrong answer.
