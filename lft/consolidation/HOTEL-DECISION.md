# The hotel question — decided

Source: `lft/audit/gsc-pages-2026q3.csv`, live GSC, 1 Jul – 1 Oct 2026.

**Correction:** I said 24 pages. Classified precisely it is **21 pages, 152 impressions**
(15% of site impressions, 22% of its pages). My earlier regex over-caught.

More importantly: **this is not one question.** The 21 pages fall into four groups with
four different answers, and treating them as one bucket would have thrown away the best
page on the site.

---

## Group A — KEEP AND BUILD MORE: city packing checklists (2 pages, 5 imp)

| Impressions | Position | Page |
|---|---|---|
| 3 | 37.3 | `/paris-packing-checklist/` |
| 2 | **1.0** | `/prague-packing-checklist/` |

`/prague-packing-checklist/` ranks **position 1**. Nothing else on the site does.

These are not hotel content — packing is the core topic. "Destination + packing" is the
bridge that works: on-topic, rankable at this authority level, and it monetises directly
into the Amazon architecture (cubes, adapters, toiletry bags, scales) instead of into hotel
affiliates you are not set up for.

**Action:** keep both, expand them, and build more of these — Rome, Barcelona, Amsterdam,
Dublin. This is the template the destination content should have followed.

## Group B — NOINDEX, DO NOT DELETE: airport hotels (5 pages, 103 imp)

| Impressions | Position | Page |
|---|---|---|
| 84 | **73.5** | `/best-hotels-near-heathrow-airport/` |
| 11 | 39.9 | `/best-hotels-near-luton-airport/` |
| 5 | 63.8 | `/hotels-near-heathrow-airport/` |
| 2 | 32.5 | `/best-hotels-near-manchester-airport/` |
| 1 | 24.0 | `/best-hotels-near-stansted-airport/` |

68% of the off-topic impressions sit here, and this is the group with a genuine argument
for existing: someone booking a hotel near Heathrow the night before a flight is the same
person checking their carry-on size. The adjacency is real.

**The ranking case is not.** You are at position 73.5 for Heathrow against Booking.com,
Expedia, TripAdvisor, Hotels.com and Premier Inn. That is one of the most heavily
contested commercial query sets in UK travel. With three editorial backlinks it is not
winnable this year, and probably not next.

**Action: noindex, leave live.** Remove from both sitemaps, keep the pages reachable. This
is reversible, loses nothing, and stops your second-highest-impression page being one you
will never rank. Revisit in 12 months only if the link profile has genuinely changed.

I am not claiming noindexing these will lift your luggage pages. The honest case is
focus and crawl allocation, not a ranking transfer.

## Group C — PRUNE: city accommodation (9 pages, 22 imp)

`/best-hotels-in-lisbon/` · `/best-hotels-paris-budget/` · `/where-to-stay-in-paris/` ·
`/best-areas-to-stay-in-lisbon/` · `/best-areas-to-stay-in-paris/` ·
`/best-hotels-in-lisbon-by-budget/` · `/where-to-stay-in-lisbon/` ·
`/where-to-stay-in-london/` · `/where-to-stay-in-prague/`

Nine pages. Twenty-two impressions. Zero clicks. No connection to luggage, no fit with the
Amazon architecture, no path to ranking against the OTAs.

## Group D — PRUNE: city activities (3 pages, 20 imp)

`/paris-metro-guide/` (17 imp, pos 74.1) · `/top-things-to-do-in-prague/` ·
`/top-things-to-do-in-lisbon/`

Same verdict. The Paris metro guide is the only one with any volume and it sits at 74.1.

### How to prune C and D — 12 pages

**Use 410 Gone, not 301.** Redirecting off-topic content into luggage pages passes nothing
useful and leaves twelve irrelevant redirects in your config forever. 410 tells Google the
page is intentionally gone and it drops out cleanly.

**Export the content to Drive first.** Twelve articles of written work. If you ever stand up
a separate destination site, you will want them. Deleting them from WordPress without an
archive is the one irreversible mistake available here.

## Group E — one dependency to resolve first (2 pages)

`/accommodation-guide/` (1 imp, pos 4) · `/travel-destinations/` (1 imp, pos 3)

**`/travel-destinations/` is the 301 target for the `/destinations/` 404** in
`redirects-rankmath.csv`. If you prune the destination content, that hub has nothing left to
point at and the redirect lands on an empty page.

Pick one:
- **Keep `/travel-destinations/`** as a slim hub listing the packing checklists (Group A).
  The `/destinations/` redirect stays valid. Recommended — it is one page and it fixes the
  sitemap 404.
- **Prune both hubs**, and change the `/destinations/` row to 410 instead of a 301.

`/accommodation-guide/` has no dependency. Prune it with Group C.

---

## This reverses part of yesterday's plan

Yesterday I told you to do the destination merges **before** deciding the hotel question,
on the logic that consolidating 7 URLs into 3 means later pruning 3 instead of 10.

That holds only if you keep them. The recommendation is to prune, so **those merges are
wasted work.** Drop these six rows from `redirects-rankmath.csv` before importing:

```
best-areas-to-stay-in-lisbon/
best-hotels-in-lisbon-by-budget/
where-to-stay-in-lisbon/
best-areas-to-stay-in-paris/
where-to-stay-in-paris/
hotels-near-heathrow-airport/      ← now a noindex, not a merge target
```

`redirects-hotel-adjusted.csv` in this folder is the same file with those six rows already
removed: **16 redirects instead of 22.** Use that one if you accept this decision. Keep the
original if you decide to hold the destination content.

---

## Net effect

| | Before | After |
|---|---|---|
| Indexed pages | 96 | **67** |
| Off-topic indexed pages | 21 | **3** (2 packing checklists + 1 hub) |
| Pages deleted | — | 13 (Groups C, D, `/accommodation-guide/`) |
| Pages noindexed | — | 5 (airport hotels) |
| Redirects to import | 22 | 16 |

The site goes from 22% off-topic to under 5%, and what remains is on-topic by any
reading — packing content, not hotel content.

## What I am not claiming

This does not create traffic. You are deleting 42 impressions and zero clicks. The case is
that a 67-page site entirely about luggage and airline rules is a coherent thing Google can
understand and rank, and a 96-page site that is one-fifth hotel affiliate content is not.

The ceiling is still three editorial backlinks. Deleting the hotel pages does not raise it.
It makes the site worth linking to.
