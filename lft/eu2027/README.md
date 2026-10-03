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

**No paid cabin-bag product is abolished.** All seven allow a bag larger than the 100cm
entitlement, and if the opt-out is real they do not disappear at all — they **invert**. The
bag becomes the default and the no-bag fare becomes the discount:

| Airline | Paid product | Over the free entitlement by |
|---|---|---|
| Ryanair | Priority / paid overhead cabin bag (55×40×20, 10kg) | +15cm |
| Wizz Air | WIZZ Priority trolley bag (55×40×23, 10kg) | +18cm |
| Aer Lingus | Cabin bag, Plus fare (55×40×24, 10kg) | +19cm |
| easyJet | Large cabin bag (56×45×25, 15kg) | +26cm |
| Allegiant | Paid carry-on (56×36×23) | +15cm |
| Spirit | Paid carry-on (56×46×25) | +27cm |
| Frontier | Paid carry-on (61×41×25, 15.9kg) | +27cm |

Two things follow. A passenger whose bag fits the entitlement stops needing to buy an
add-on, so the product only earns its keep on the band above 100cm. And because airlines may
still sell a cheaper no-bag fare, the commercial move is not to withdraw these products but
to flip them: price the bag into the headline fare and sell the discount for going without.
That is a more defensible finding than "they disappear", and a more interesting one, because
it predicts what the airlines actually do next.

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

## Verification status, 3 Oct 2026

The act is **Regulation (EU) 2026/2202 of 16 September 2026**, amending Regulation (EC)
261/2004.

**The primary text has not been read.** `eur-lex.europa.eu`, `consilium.europa.eu` and
`europarl.europa.eu` are all blocked by this network's egress policy, as are most of the
news sites carrying the detail. Everything below is triangulated from search results and is
graded per figure in `RULE` at the top of `build.py`.

| Figure | Status |
|---|---|
| Regulation number and date | **Confirmed** — several sources |
| Parliament 7 Jul 2026, Council 13 Jul 2026 | **Confirmed** |
| Free personal item 40 × 30 × 15 cm, under the seat | **Confirmed** |
| Application = OJ publication + 20 days + 12 months | **Confirmed** |
| Fares shown inclusive of hand baggage at booking | **Confirmed** |
| Cabin bag 100 cm combined / 7 kg in the standard fare | **Corroborated, one outlet dissents** |
| Applies from 23 October 2027 | **Corroborated** — consistent with OJ publication ~3 Oct 2026 |
| The Official Journal publication date | **Not verified** |

**The one that matters.** At least one outlet says the reform does not make the trolley
universally free and airlines may still charge for anything that will not fit under the
seat. Recent reporting says the opposite — 100 cm / 7 kg included in the standard fare. The
likely reconciliation is that it is included **by default**, with airlines free to sell a
cheaper fare to a passenger who waives it. The dataset assumes that, and the verdicts say
"inverts" rather than "abolished" as a result.

**Someone on an unblocked connection needs to open EUR-Lex and read Regulation (EU)
2026/2202.** Twenty minutes. Until then this is well-sourced secondary reporting, not law,
and it must not be described to a journalist as verified.

## Before this goes to anyone

1. **Read Regulation (EU) 2026/2202 on EUR-Lex** and confirm the baggage article, the
   100 cm / 7 kg figures, and the opt-out.
2. **Get the Official Journal publication date**, which fixes the application date exactly.
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
