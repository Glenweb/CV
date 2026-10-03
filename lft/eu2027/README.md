# EU 2027 hand-baggage dataset

Built against the primary text. **Regulation (EU) 2026/2202** of 16 September 2026,
**OJ L, 2026/2202, 2.10.2026**, ELI `http://data.europa.eu/eli/reg/2026/2202/oj`.

```bash
python3 lft/eu2027/build.py      # CSVs + workbook into out/
```

## The dates, verified

| | |
|---|---|
| Parliament legislative resolution | 7 July 2026 |
| Council decision | 13 July 2026 |
| Signed at Strasbourg | 16 September 2026 |
| **Published in the Official Journal** | **2 October 2026** |
| In force (Art. 3, twentieth day following publication) | **22 October 2026** |
| **Applies from** (Art. 3, stated expressly) | **23 October 2027** |

23 October 2027 is written into Article 3. It is not derived from a formula, and it is not
an estimate.

## Three things the earlier version got wrong

**1. There is no 100 cm and no 7 kg in the act.** Those figures circulated widely in
reporting and are absent from the adopted text. Every calculation that rested on a "free
100 cm / 7 kg cabin entitlement" has been removed.

**2. The cabin trolley does not become free.** Article 11a(1) requires carriers to permit a
personal item "and at no extra cost", and separately to permit a piece of hand baggage
"subject to the capacity of the aircraft cabin" — with no free-of-charge wording. The same
paragraph expressly preserves "commercially differentiated offers to passengers who
voluntarily choose to travel without hand baggage". Recital 45 defers uniform minimum
hand-baggage dimensions to a future review of Regulation (EC) No 1008/2008.

**3. 40 × 30 × 15 is not a floor.** Article 2(ah) defines a personal item as unchecked
baggage "either with maximum dimensions of 40 x 30 x 15 cm **or** on the condition that it
fits under the seat in front". It is an alternative qualifying test. A carrier whose free
bag is smaller than those dimensions is not thereby non-compliant — **which retires the
Lufthansa Group finding entirely.** Lufthansa, Swiss and Austrian at 40 × 30 × 10 qualify
through the under-seat limb.

## What the regulation actually changes

**The price display, not the bag.** Article 11a(1): "air fares including allowance for a
piece of hand baggage shall be displayed by default before the start of any booking
process." Carriers may still sell a cheaper no-trolley fare — but the trolley-inclusive
price is what has to be shown first.

Four EU/EEA carriers in this dataset sell a paid cabin trolley and must therefore change
how their headline fare is displayed:

| Carrier | Paid trolley product |
|---|---|
| **Ryanair** | Priority / paid overhead cabin bag, 55 × 40 × 20 |
| **easyJet** | Large cabin bag, 56 × 45 × 25 |
| **Wizz Air** | Priority trolley bag, 55 × 40 × 23 |
| **Aer Lingus** | Cabin bag, Plus fare / Priority boarding, 55 × 40 × 24 |

Spirit, Frontier and Allegiant also sell paid carry-ons, but the rule reaches them only on
EU departures, which they do not generally operate. They are marked accordingly rather than
counted.

**Nobody in the dataset charges for the under-seat personal item today**, so the
free-personal-item limb changes nothing for these 51 carriers. That is a finding in itself.

## The story

Most coverage reported that cabin bags become free in 2027. **The text does not say that.**
It guarantees a free personal item — which essentially every carrier already provides — and
otherwise regulates how the fare is *displayed*. Trolley dimensions are explicitly left
unstandardised.

That is the contrarian, checkable, primary-source story: *"You were told your cabin bag is
free from 2027. Read Article 11a."* It is better than the version we had because it is
verifiable in one click and almost nobody has written it.

## Two labels not to misread

- **"Not recorded in our data"** in the personal-item column is a gap in this dataset, not a
  finding about the airline. 23 carriers, mostly full-service, record only a cabin bag in
  our source. Most of them do allow a handbag as well. **Do not report it as non-compliance.**
- **Prices.** The add-on price columns are empty by design. Fill them from the carriers' own
  booking flows, or delete the columns before sending.

## Before this goes to a journalist

1. Spot-check five carriers against their own published terms. Twenty minutes.
2. Fill or delete the price columns.
3. Have the scope reading checked — Article 3 covers EU/EEA departures by any carrier, and
   arrivals into the EU/EEA where the operator is a Union carrier. That is a plain reading,
   not a legal opinion.

## Sheets

| Sheet | What it is |
|---|---|
| Read me | The source, what the act does and does not do, and the two labels above |
| Summary by airline | One row per carrier |
| Every fare | All 112 products with the article-by-article verdict |
| Fare display must change | The four EU carriers, plus the three marked out of scope |
