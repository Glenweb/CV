# LFT content — Spirit Airlines rewrites

Two pages, rewritten because **Spirit Airlines ceased operations on 2 May 2026** and both
pages were still publishing live carry-on rules for an airline that does not fly.

| File | Target URL | 12-month impressions |
|---|---|---|
| `spirit-airlines-carry-on-size.html` | `/spirit-airlines-carry-on-size/` | 881 |
| `spirit-airlines-personal-item-size-2026.html` | `/spirit-airlines-personal-item-size-2026/` | 453 |

## Why rewrite rather than delete or redirect

1,334 impressions a year is residual demand that keeps arriving for a long time after an
airline dies — people check an old booking, an old bag, or simply don't know. A 301 to
Frontier throws the intent away and reads as a bait-and-switch. A rewrite answers the
question that was asked ("what size?"), then answers the one they didn't know they had
("which airline now?"), and earns the internal link into Frontier, Allegiant, Southwest
and the checker.

**Keep both URLs. No redirects. Keep the `2026` in the second slug** — the year is part of
why it ranks, and the page now says what actually happened in 2026.

## How the two pages differ

Deliberately no overlap beyond the status box:

- **`/spirit-airlines-carry-on-size/`** — the news (shutdown, Chapter 11, job losses),
  refunds and chargebacks, who took over which routes, then the full US carrier comparison
  table with the free/paid split.
- **`/spirit-airlines-personal-item-size-2026/`** — one question only: *what free bag do I
  get now?* A single ranked table, biggest free allowance to smallest, plus the three
  traps. Links back to page one for refunds and routes.

## Install

1. Load `content.css` once (theme stylesheet or **Appearance → Customise → Additional
   CSS**). Both pages use `.lft-status`, `.lft-table`, `.lft-note`.
2. Replace each page's body with the matching HTML in a **Custom HTML** block.
3. Remove the old meta description. Suggested replacements:
   - *Spirit Airlines ceased operations on 2 May 2026. Its carry-on and personal item
     limits, what happens to your booking, and where a Spirit-sized bag fits now.*
   - *Spirit's personal item was 45 × 35 × 20 cm. Spirit stopped flying in May 2026 — here
     is the free cabin bag you get on every airline that took over its routes.*
4. Each file carries its own `NewsArticle` + `FAQPage` JSON-LD. **Update `datePublished`**
   to the real publish date; `dateModified` is already 3 Oct 2026.
5. Insert the static cheat-sheet form block at the `LFT-OPTIN-SLOT` comment. Do **not**
   load `lft/checker/lft-checker-capture.js` on these pages — that script is
   checker-page-only and its opt-in is verdict-triggered.
6. Request indexing for both URLs in Search Console. These are substantive rewrites, not
   tweaks; waiting on an organic recrawl wastes the news window.

## Where the numbers came from

Every dimension on both pages is read from `lft/fare-watch/airlines.json` — the checker's
own dataset — in centimetres, with inches converted and rounded to the nearest inch. That
is stated on the page. Verified programmatically: all 18 cm triples across the two files
match the dataset exactly, and every inch conversion matches.

**Do not hand-edit dimensions in these files.** Change the dataset and re-export, or the
pages will drift away from the checker and contradict it.

## Facts that still need a human check before publishing

Gathered from news reporting (NPR, CNN, CNBC, Flightradar24) on 3 Oct 2026:

- Ceased operations 2 May 2026; Chapter 11 filings November 2024 and August 2025; a federal
  support package of roughly $500m did not come through; 17,000+ jobs; 34-year run.
- Refunds processed automatically for direct credit/debit bookings, most completed within
  days; third-party bookings refunded by the booking company; chargebacks under the Fair
  Credit Billing Act; vouchers, credits and Free Spirit points go through the bankruptcy
  process.
- JetBlue took nine former Spirit routes with major Fort Lauderdale expansion (FLL to IAH,
  BNA, BWI, CLT, MCO, ORD); Breeze took most Atlantic City routes; Frontier, United, Delta
  and Southwest announced Spirit-market expansions.

**Refund mechanics are the one section to re-confirm**, because consumer guidance ages
badly and this page will rank for people with money at stake. Check the bankruptcy docket
or current official guidance and adjust wording if anything has moved.

## Still open — the checker itself

The live checker **still lists Spirit with `enforcement: extreme`** and publishes verdicts
for an airline that has not flown since May. The dataset now records
`status: "ceased_operations"` and `ceasedOn: "2026-05-02"`, but the tool does not read it.

That is a bigger credibility problem than these two pages were: a user can pick Spirit
today and get a confident pass/fail. The fix is to surface the status in the tool — either
remove Spirit from the dropdown or show a "ceased operations, see alternatives" state that
deep-links to `/spirit-airlines-carry-on-size/`. Needs doing against the live tool source.
