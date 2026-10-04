# The Spirit pages — decided

**One page, not two. Publish the shutdown page's new body, redirect everything else into it,
and never touch Spirit again.**

---

## The premise I built those drafts on was wrong

I wrote both pages on "1,334 impressions a year of residual demand — people search for a dead
airline for a long time." The 12-month timeline says otherwise:

| Window | Impressions | Position |
|---|---|---|
| Oct 2025 – 22 Feb 2026 | **0** | — |
| 23 Feb – 7 Mar | ~205 | **7–10** (and the site's only click, 7 Mar) |
| 8 Mar – 24 Mar | ~1,100 | 18.6 → **48.2** |
| 25 Mar | **cliff to zero** | |
| Apr – Jul | ~25 total | 1–13 |
| **1 Aug – 1 Oct** | **0** | — |

**~92% of the cluster's impressions fell in one four-week window**, and the cluster has had
**zero impressions for two full months.**

And the timing matters: that burst ran **February to March, while Spirit was still flying**.
Spirit ceased operations on 2 May. The demand was for a live airline, and it died with it.

This is the same fan-out pattern I diagnosed across the whole site and then failed to apply
to the pages I was writing. The 881 and 453 figures are artefacts of one burst at collapsing
positions, exactly like the 3,613 impressions on "airlines that charge for carry on". I should
have checked the Spirit numbers against the timeline before writing two pages on them.

## The decision

**1. Publish `spirit-airlines-carry-on-size.html` as the body of the existing
`/spirit-airlines-shutdown/` page.**

Not as a new URL. `/spirit-airlines-carry-on-size/` already 301s there, and four more Spirit
URLs now join it. Worth doing once, because the draft is accurate, it answers the size
question the residual queries actually ask, and the existing page gets 4 impressions a year
at position 6.5 — it is indexed and catching the trickle. Replace the body, request indexing,
move on.

**2. Do not publish the second page.** `spirit-airlines-personal-item-size-2026.html` is
marked do-not-publish and kept for the record. Its URL is "Crawled – currently not indexed",
its only internal link comes from a hotel page, and its 453 impressions are a share of the
same dead burst. **301 it into the shutdown page.** Row added to
`redirects-hotel-adjusted.csv`, now **17 rows** — still no duplicate sources, still no chains.

**3. Six Spirit URLs become one.**

| URL | Action |
|---|---|
| `/spirit-airlines-shutdown/` | **survives** — new body |
| `/spirit-airlines-carry-on-size/` | already 301s here |
| `/airline-baggage-rules/spirit-airlines-personal-item-size-2026/` | 301 (new) |
| `/best-carry-on-luggage-spirit-airlines/` | 301 |
| `/airline-baggage-rules/best-underseat-bag-for-spirit-airlines/` | 301 |
| `/best-carry-on-luggage-spirit/` | 301 if it still resolves |

### On the one click

The site's single click in twelve months came on **7 March**, from
`/airline-baggage-rules/best-underseat-bag-for-spirit-airlines/` — a page about buying a bag
for an airline that would stop flying eight weeks later. It has had zero impressions since
August.

I nearly argued for protecting it. One click, seven months ago, for a dead airline, from a
page whose position has gone from 12.4 to 68, is not an asset. Redirect it.

## What this changes about the sequencing

Spirit drops out of the critical path. It is one paste and one redirect import, not a content
project. The effort moves to the pages with live demand — and after the audit, the checker
itself, which is the only thing on the site that currently works and now finally tells the
truth.
