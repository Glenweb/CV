# LFT consolidation plan

Built from `lft/audit/gsc-pages-2026q3.csv` — live Search Console, 1 Jul – 1 Oct 2026.
**96 pages, 1,021 impressions, 0 clicks.**

Outcome: **96 URLs → 74.** 22 redirects, all in `redirects-rankmath.csv`, ready to import.

---

## Correction to yesterday's audit — my clustering over-counted

I reported "16 duplicate clusters, 42 pages." That came from matching slug tokens, and it
was wrong in one important way: **a rules page and a "best bag" page are not duplicates.**
They serve different intent and should both exist. Merging them would delete demand, not
concentrate it.

Re-clustered by intent, these pairs are **correct as they stand — do not touch**:

| Airline | Rules page | Commercial page |
|---|---|---|
| easyJet | 169 imp | 4 imp |
| Wizz Air | 16 imp | 16 imp |
| Alaska | 36 imp | 3 imp |
| Southwest | 7 imp | 3 imp |
| JetBlue | 7 imp | 1 imp |
| United | 49 imp | 5 imp |

That is six clusters removed from the plan. The real duplication is smaller than I said,
and concentrated in Ryanair, the fees pages, and the destination content.

## Three further overrides, against what the data alone suggested

The rule "keep the URL with the most impressions" is right most of the time. Three
exceptions:

1. **Hawaiian — keep the weaker URL.** `/hawaiian-airlines/` has more impressions (2 vs 1)
   but it is a bare airline name at the root with no stated topic. Keep
   `/airline-baggage-rules/hawaiian-airlines-carry-on-size/` and redirect the root into it.
   Three impressions is noise; URL clarity is permanent.

2. **United gate sizers — do not merge at all.** My script folded
   `/airline-baggage-rules/united-new-bag-sizers-gate-enforcement/` into the United rules
   page. It is a distinct news topic, and at **position 9.6 it holds the best position of
   any substantive page on the site.** Leave it alone and link it from the United rules page.

3. **Spirit — redirect both, merge neither.** Both Spirit commercial pages sell bags for an
   airline that stopped flying on 2 May 2026. Neither should survive. Both 301 to
   `/spirit-airlines-shutdown/`. (The Drive redirect CSV already claims to cover
   `best-carry-on-luggage-spirit-airlines/` — it is still appearing at position 24, so
   **verify that redirect is actually firing** before assuming this one is redundant.)

## The one URL I am renaming

`/airline-baggage-rules/best-carry-on-luggage-for-frontier-airlines-2024-complete-guide/`
is the strongest Frontier commercial page (7 imp, position 16) but carries **2024** in the
slug, visible in every SERP snippet. Both Frontier commercial URLs 301 into a new clean
slug, `/airline-baggage-rules/best-carry-on-luggage-frontier-airlines/`, carrying the
stronger page's content.

This is the only new URL in the plan. **Everywhere else I kept the existing slug even when
it carries a year**, because churning 20 URLs for tidiness costs redirects and gains
nothing. The dated-slug problem is real but the fix is to stop minting new ones, not to
rewrite the old ones.

---

## The 22 redirects

### Airline pages — 12 redirects, 12 URLs removed

| 301 from | → to | Why |
|---|---|---|
| `ryanair-carry-on-rules-2026/` | `ryanair-carry-on-size-rules-2026/` | 3 Ryanair rules pages → 1 |
| `ryanair-carry-on-size-rules/` | same | |
| `best-carry-on-luggage-ryanair/` | `best-ryanair-cabin-bag/` | 3 Ryanair commercial → 1 |
| `best-personal-item-bag-for-ryanair/` | same | see note below |
| `lufthansa-carry-on-size/` | `airline-baggage-rules/lufthansa-carry-on-size-2026/` | root twin |
| `best-carry-on-luggage-american/` | `best-carry-on-luggage-american-airlines/` | truncated twin |
| `best-carry-on-luggage-delta/` | `airline-baggage-rules/best-carry-on-luggage-delta-airlines/` | root twin |
| `best-carry-on-luggage-for-frontier-airlines-2024-complete-guide/` | `best-carry-on-luggage-frontier-airlines/` | drops 2024 |
| `best-carry-on-luggage-frontier/` | same | |
| `hawaiian-airlines/` | `airline-baggage-rules/hawaiian-airlines-carry-on-size/` | override 1 |
| `best-carry-on-luggage-spirit-airlines/` | `spirit-airlines-shutdown/` | dead airline |
| `best-underseat-bag-for-spirit-airlines/` | same | dead airline |

**One judgment call to review.** Ryanair's free 40×20×25 underseat bag and its paid
55×40×20 priority cabin bag are genuinely different purchases, so
`best-personal-item-bag-for-ryanair` arguably deserves its own page. With 4 impressions and
three editorial links site-wide, concentration beats nuance today. Fold it in as a clearly
headed section, and split it back out once the surviving page actually ranks. If you
disagree, drop that one line from the CSV — nothing else depends on it.

### Fees and generic pages — 3 redirects

| 301 from | → to |
|---|---|
| `airline-baggage-fees/` | `airline-baggage-fee-comparison/` |
| `airline-baggage-rules/airline-carry-on-fees-comparison-2026/` | `airline-baggage-fee-comparison/` |
| `luggage-reviews/best-carry-on-luggage/` | `luggage-reviews/best-carry-on-luggage-2026/` |

Three pages were competing on baggage fees. `/airline-baggage-rules/airlines-that-charge-for-carry-on/`
stays separate — "which airlines charge" is a different question from "how much," and it is
the page the 28 August analysis was built around.

### Destination content — 6 redirects, plus the 404

| 301 from | → to |
|---|---|
| `hotels-near-heathrow-airport/` | `best-hotels-near-heathrow-airport/` |
| `best-areas-to-stay-in-lisbon/` | `best-hotels-in-lisbon/` |
| `best-hotels-in-lisbon-by-budget/` | `best-hotels-in-lisbon/` |
| `where-to-stay-in-lisbon/` | `best-hotels-in-lisbon/` |
| `best-areas-to-stay-in-paris/` | `best-hotels-paris-budget/` |
| `where-to-stay-in-paris/` | `best-hotels-paris-budget/` |
| `destinations/` | `travel-destinations/` | **fixes the 404 in page-sitemap.xml** |

**Do this before deciding the hotel question, not after.** Consolidating 7 URLs into 3
costs an hour. If you later noindex or prune the hotel content, you are removing 3 pages
instead of 10, and the redirects already written stay valid either way.

---

## Execution order

1. **Import `redirects-rankmath.csv`** — RankMath → Redirections → Import. Same format as
   `luggagefortravel_rankmath-redirects-phase2-spirit.csv` already in your Drive.
   Verified: 22 rows, no duplicate sources, **no redirect chains**.
2. **Merge the content before the redirect goes live on each pair.** A 301 to a page missing
   the merged content loses whatever the old page said. Work the five briefs below first.
3. **Create `/airline-baggage-rules/best-carry-on-luggage-frontier-airlines/`** with the
   2024 page's content before importing, or those two rows 404.
4. **Update internal links** to point at survivors. The June Screaming Frog guide in your
   Drive already flagged "24 internal redirects linked" — this adds 22 more if you skip it.
5. **Re-check the checker's recommendation URLs.** The tool links to
   `/airline-baggage-rules/best-ryanair-cabin-bag/` (survivor, fine) and
   `/luggage-reviews/best-underseat-bags-budget-airlines/` (untouched, fine). No change needed —
   confirmed against the patched source in `lft/checker/tool/`.
6. **Resubmit both sitemaps** and request indexing on the 8 survivors.

---

## Merge briefs — the five highest-value clusters

### 1. Heathrow hotels — 89 impressions, the site's 2nd-highest page

**Survives:** `/best-hotels-near-heathrow-airport/` (84 imp, position **73.5**)
**Folds in:** `/hotels-near-heathrow-airport/` (5 imp, position 63.8)

Position 73.5 on 84 impressions means Google has demand mapped to this page and ranks it
nowhere. Merge the two, then **stop**. Do not invest further until the hotel question is
settled — this is the clearest example of the dilution problem, not an opportunity.

### 2. Ryanair rules — 59 impressions across 3 pages

**Survives:** `/airline-baggage-rules/ryanair-carry-on-size-rules-2026/` (47 imp, pos 55.9)
**Folds in:** `ryanair-carry-on-rules-2026/` (8 imp, pos 31.4), `ryanair-carry-on-size-rules/` (4 imp, pos 70.3)

The two folding in hold better positions than the survivor on fewer impressions — so they
each say something the main page does not. Before redirecting, read all three and carry
across anything missing. Structure the survivor:

1. The two allowances up front, free then paid — 40×20×25 cm and 55×40×20 cm, 10 kg
2. What Priority actually buys you, and when it is cheaper than the gate fee
3. Gate enforcement: Ryanair is `extreme` in your own dataset — pack 1 cm under
4. Fees, current, with the date you checked them stated on the page
5. One link to `/airline-baggage-rules/best-ryanair-cabin-bag/`, one to the checker
6. FAQ absorbing the exact questions the two retired pages ranked for

### 3. Ryanair commercial — 50 impressions across 3 pages

**Survives:** `/airline-baggage-rules/best-ryanair-cabin-bag/` (29 imp, pos 29.1)
**Folds in:** `best-carry-on-luggage-ryanair/` (17 imp, pos 68.3), `best-personal-item-bag-for-ryanair/` (4 imp, pos 39)

Two clearly headed sections, because these are two different purchases:
- **Free underseat bag (40 × 20 × 25 cm)** — absorbs the personal-item page
- **Priority cabin bag (55 × 40 × 20 cm, 10 kg)** — the existing page's core

Keep this URL exactly as it is: the patched checker links to it by name.

### 4. Lufthansa rules — 29 impressions across 2 pages

**Survives:** `/airline-baggage-rules/lufthansa-carry-on-size-2026/` (22 imp, pos 35)
**Folds in:** `/lufthansa-carry-on-size/` (7 imp, pos 24.3)

Straight de-duplication, root twin into the category page. Keep the Economy Light
distinction prominent — your dataset has it as hand-baggage-only, which is the thing people
get caught by. **Note:** the EU 2027 work retired the Lufthansa Group finding, so do not
reintroduce any claim about the trolley becoming free.

### 5. Lisbon accommodation — 4 pages, 10 impressions

**Survives:** `/best-hotels-in-lisbon/` (7 imp, pos 14.3)
**Folds in:** `best-areas-to-stay-in-lisbon/`, `best-hotels-in-lisbon-by-budget/`, `where-to-stay-in-lisbon/`

Four pages, ten impressions, zero clicks. The merge is worth an hour purely to remove three
URLs. Do not write new content for it. Same pattern applies to Paris (3 → 1) and the same
answer: consolidate, then leave alone pending the hotel decision.

---

## What this will and will not do

It removes 22 URLs, stops roughly a third of the site bidding against itself, and fixes a
404 that is currently in your sitemap. It costs a day.

**It will not produce traffic on its own.** With 3 editorial backlinks there is almost no
authority to concentrate, and a page at position 55 does not reach page one because two
siblings stopped competing with it. The honest case for doing it now is that it is free,
it compounds, and every link or content investment afterwards is worth more once the site
stops splitting its own signal.

The ceiling is still links. This clears the floor.
