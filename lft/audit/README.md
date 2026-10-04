# LFT — what the live Search Console data actually says

Pulled 4 Oct 2026 from the connected GSC property. Window: **1 Jul – 1 Oct 2026**.
`gsc-pages-2026q3.csv` is the raw page-level export. No credentials needed — GSC is wired
into the OpenSEO project, so this is repeatable on demand.

## The headline

| | |
|---|---|
| Pages with any search presence | **96** |
| Total impressions | **1,021** |
| **Total clicks** | **0** |
| Pages with at least one click | **0** |

Zero clicks in three months. Not low — none.

## Why: nothing ranks where clicks happen

| Average position | Pages | Impressions |
|---|---|---|
| 1–10 | 16 | 42 |
| 11–20 | 17 | 174 |
| 21–50 | 43 | 413 |
| 51+ | 20 | 392 |

**63 of 96 pages sit at position 21 or worse, carrying 805 of the 1,021 impressions.**
Nobody clicks position 40. The 16 pages that do reach the top 10 attract 42 impressions
between them — they rank for things nobody searches.

This supersedes the earlier reading. The pages *are* indexed and they *do* rank. They rank
in places that cannot produce traffic.

## The biggest self-inflicted problem: the site competes with itself

**42 of 96 pages (44%) sit in 16 duplicate clusters, carrying 717 impressions (70%).**

| Topic | Pages competing | Impressions |
|---|---|---|
| Ryanair | **6** | 109 |
| Lisbon accommodation | **4** | 10 |
| Frontier | 3 | 68 |
| American | 3 | 66 |
| Delta | 3 | 12 |
| Paris accommodation | 3 | 10 |
| easyJet | 2 | 173 |
| Heathrow hotels | 2 | 89 |
| United | 2 | 54 |
| Alaska | 2 | 39 |
| Wizz Air | 2 | 32 |
| Lufthansa | 2 | 29 |
| Southwest | 2 | 10 |
| JetBlue | 2 | 8 |
| Spirit | 2 | 5 |
| Hawaiian | 2 | 3 |

Six Ryanair pages split the same intent six ways. Each one is weaker than the single page
they should be. Full breakdown in the CSV.

Worth noting inside the clusters:
- `/airline-baggage-rules/best-carry-on-luggage-for-frontier-airlines-2024-complete-guide/`
  still carries **2024** in the slug.
- `/best-carry-on-luggage-spirit-airlines/` still shows at position 24, although the
  RankMath redirect CSV in Drive says it 301s to `/spirit-airlines-shutdown/`. **Verify
  that redirect is actually firing.**
- The `/airline-baggage-rules/…` versions generally out-impress their root-level twins, so
  the category path is usually the one to keep.

## The topical dilution

**24 of 96 pages are hotels and city destinations** — Lisbon, Paris, Prague, London,
airport hotels, the Paris metro. 175 impressions, zero clicks, and nothing to do with
luggage. `/best-hotels-near-heathrow-airport/` carries 84 impressions at position 73.5,
the second-highest impression count on the entire site, and it will never convert on an
affiliate luggage offer.

## Known broken things, from the same sweep

- `/destinations/` returns **404**, is linked from `/travel-destinations/`, and is still
  listed in `page-sitemap.xml`.
- `/cheat-sheet/` is **unknown to Google** — and it is the fallback URL baked into the
  checker capture plugin.
- `/airline-baggage-rules/spirit-airlines-personal-item-size-2026/` is
  **crawled, not indexed**; its only internal link is from `/hotels-near-heathrow-airport/`.
- `/airline-baggage-rules/carry-on-luggage-size-restrictions-by-airline/` 301s to
  `/carry-on-size-by-airline/` but is still in `post-sitemap.xml`. It is also where the
  site's single genuine editorial backlink points.

## What this means for sequencing

1. **Consolidate the 16 clusters first.** 42 pages down to about 16, 301 the rest into the
   survivor. This is the only lever that costs nothing but a decision and compounds
   everything after it.
2. **Decide the hotel question.** 24 pages, zero clicks, wrong topic. Noindex, prune, or
   move them off the domain.
3. **Fix the four broken items above.** Hours, not days.
4. **Then** links and depth. 269 referring domains of which 3 are editorial is the ceiling
   on how high any of this can rank — but links pointed at pages that fight each other are
   wasted, so this comes fourth, not first.

Consolidation alone will not produce traffic. With 3 editorial links the site has almost no
authority to concentrate. But concentrating what little there is costs nothing, and every
later effort is worth more once the site stops bidding against itself.
