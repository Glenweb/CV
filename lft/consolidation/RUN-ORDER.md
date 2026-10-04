# Execution order — redirects and the embed

Everything below is ready. This is the sequence, and the two places where doing it out of
order loses content.

---

## A. The checker and the embed — see `lft/PUBLISH.md`

Both files are complete HTML documents, so neither can be pasted into a page body. They now
ship as a WordPress plugin that serves them directly:
`lft/checker/wordpress/lft-checker-embed.zip` — upload, activate, done.

That also settles the framing problem this section used to warn about. The plugin sends
`frame-ancestors *` on the widget and strips any `X-Frame-Options` PHP set, and its settings
page has a **Run the test** button that reports what the live URL actually returns. A header
set at the nginx or Apache level still survives — PHP cannot remove one — which is exactly
what the test is there to catch.

`lft/PUBLISH.md` is the full sequence, including the warning worth reading before you let the
plugin take over `/carry-on-size-checker/`.

Then add a GA4 view filtered to `utm_source=embed` so you can see which sites actually use it.

---

## B. The redirects — order matters

**Use `redirects-hotel-adjusted.csv` (17 rows), not the original 22.** The six destination
merges were dropped when the hotel decision went to prune.

### Step 1 — publish the new Frontier URL FIRST

`new-frontier-carry-on-luggage.html` → **`/airline-baggage-rules/best-carry-on-luggage-frontier-airlines/`**

Two rows in the CSV point here. Import before this page exists and both 301s land on a 404.
This is the only genuinely new URL in the whole plan.

### Step 2 — publish the three merged bodies

| Paste | Over | Absorbs |
|---|---|---|
| `merged-ryanair-rules.html` | `/airline-baggage-rules/ryanair-carry-on-size-rules-2026/` | 2 Ryanair rules pages |
| `merged-ryanair-cabin-bag.html` | `/airline-baggage-rules/best-ryanair-cabin-bag/` | 2 Ryanair commercial pages |
| `merged-lufthansa.html` | `/airline-baggage-rules/lufthansa-carry-on-size-2026/` | the root-level Lufthansa duplicate |

These are the three clusters carrying real impressions (59, 50, 29). **Publish the merged
body before the redirect goes live**, or the 301 lands on a page that never absorbed what the
retired one said.

The remaining merges in the CSV — American, Delta, Alaska, Hawaiian, Spirit, United
commercial, and the fees cluster — are near-duplicates where the survivor already says
everything. Read the retiring page once, lift anything the survivor lacks, then redirect.
No drafts needed.

### Step 3 — import the redirects

RankMath → Redirections → Import, `redirects-hotel-adjusted.csv`. Same format as the Spirit
phase-2 file already in your Drive. Verified: 17 rows, no duplicate sources, **no chains**.
(22 original, minus the 6 hotel/destination merges, plus the one Spirit personal-item row
added by the Spirit decision.)

### Step 4 — the prune and noindex

From `prune-and-noindex.csv`:
- **410** the 13 city-accommodation and city-activity pages. **Export them to Drive first** —
  that is the one irreversible step here.
- **noindex** the 5 airport-hotel pages and remove them from both sitemaps.
- **Decide `/travel-destinations/`**: keep it as a slim hub listing the two packing
  checklists, and the `/destinations/` 404 row stays valid. Prune it instead and that row
  must become a 410.

### Step 5 — clean up after

- Update internal links to point at survivors rather than through the new 301s. Your June
  Screaming Frog guide already flagged 24 internal redirects; skipping this adds 16 more.
- Remove the stale `post-sitemap.xml` entry for
  `/airline-baggage-rules/carry-on-luggage-size-restrictions-by-airline/`. It 301s to
  `/carry-on-size-by-airline/` and **one of your two editorial backlinks points at it**.
- Resubmit both sitemaps and request indexing on the four pages above.

---

## What this leaves

| | Before | After |
|---|---|---|
| Indexed pages | 96 | ~67 |
| Off-topic indexed | 21 | 3 |
| URLs competing with a sibling | 42 | 0 in the clusters handled |
| Pages with wrong carry-on figures | 15 | 0 |

## Still on you, and not blocked by any of the above

1. **The two Spirit drafts** in `lft/content/` — decide whether they merge into the existing
   `/spirit-airlines-shutdown/` page or replace its body. They are corrected and validated
   but still unpublished.
2. **Verify the Spirit product redirects are actually firing.** Drive says they are active
   since May, yet `/best-carry-on-luggage-spirit-airlines/` still surfaced at position 24 in
   the September data.
3. **`/cheat-sheet/` is unknown to Google** and it is the fallback URL baked into the capture
   plugin. Confirm it exists before the plugin goes live.
4. **Install the capture plugin in preview mode** — still the fastest way to get real
   behavioural data on the checker.
