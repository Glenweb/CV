# The 25 March indexing check

Thirty minutes. Three of these cannot be automated — Google exposes no API for manual
actions or security issues, so those are UI-only and nothing in this folder replaces them.

## What I already checked for you (3 Oct 2026, live via URL Inspection)

| Page | Coverage | Last crawled | Canonical | Robots |
|---|---|---|---|---|
| `/carry-on-size-by-airline/` | **Submitted and indexed** | 2 Oct 2026 | self, agreed | allowed |
| `/carry-on-size-checker/` | **Submitted and indexed** | 26 Sep 2026 | self, agreed | allowed |
| `/airline-baggage-rules/best-ryanair-cabin-bag/` | **Submitted and indexed** | 25 Sep 2026 | self, agreed | allowed |

**Three things follow from this, and they narrow the problem a lot:**

1. **The money pages are indexed and being crawled normally**, within the last week. Whatever
   happened on 25 March, it is **not** deindexing and **not** a crawl failure.
2. **`/carry-on-size-by-airline/` returns a healthy 200 and is indexed.** The 404 logged
   against it in the May crawl export is stale or was fixed. One open question closed.
3. Google's chosen canonical matches the declared one on all three. No canonical conflict.

**Two new findings worth acting on:**

- **The checker is not in any sitemap.** The other two pages list
  `page-sitemap.xml` / `sitemap_index.xml`; the checker lists none. It got indexed anyway,
  but your most important asset is not being submitted. Fix that first — it is a two-minute job.
- **No structured data detected on the checker.** The other two return Breadcrumbs. The
  checker returns no rich-result types at all, despite its source carrying `WebApplication`,
  `FAQPage` and `Offer`. `FAQPage` *is* a type Google reports on, so its absence suggests the
  schema is not reaching Google — JS-injected, malformed, or stripped in the deployed page.
  **Verify with the Rich Results Test before adding `VideoObject` to that graph**, or you will
  be adding to a graph Google never reads.

## The checks that are still yours to do

### 1. Manual actions — 30 seconds, do this first

**Search Console → Security & Manual Actions → Manual actions.**

- *"No issues detected"* → rule it out and move on. This is the likely outcome.
- Anything else → stop. Nothing else in this runbook matters until it is resolved, and the
  reconsideration process is the whole job.

No API exposes this. It has to be the UI.

### 2. Security issues — 30 seconds

**Security & Manual Actions → Security issues.** Hacked content and injected spam produce
exactly this kind of cliff. Same rule: anything but "No issues detected" stops everything else.

### 3. Page indexing report — 10 minutes, the main event

**Indexing → Pages.** Look at the **trend chart first, not the table**, and set the range to
16 months so the March date is visible.

The question is narrow: **did "Indexed" fall on 25 March, or did it stay flat?**

- **Indexed count fell on/around 25 March** → pages were dropped. The reason breakdown below
  the chart names which bucket they moved into, and that is your answer.
- **Indexed count stayed flat** → nothing was deindexed. Impressions fell while indexing held,
  which is the signature of a **ranking or surface change**, not a technical one. Given what
  the query data shows, this is what I expect you will see: the AI fan-out that produced 86%
  of the year's impressions simply stopped.

Then **Export** the report and run it through the script:

```bash
node lft/indexing/check-indexing.mjs --csv ~/Downloads/Table.csv
```

It buckets every URL, flags which of the nine money pages are in a bad state, explains what
each GSC state actually means, and exits non-zero if anything needs a decision. Add
`--sitemap <file>` (an `.xml` or a plain list of URLs) and it also reports URLs that are in
your sitemap but absent from the export — pages Google has not processed at all.

### 4. The date, against Google's update timeline — 2 minutes

Check whether a core or spam update was rolling on 25 March 2026. If one was, that is the
answer, and it is an authority problem — which is consistent with zero external backlinks
being the ceiling.

### 5. Sitemaps — 2 minutes

**Indexing → Sitemaps.** Confirm every sitemap reads *Success* and check the discovered-URL
counts look right. While you are there, **add the checker to a sitemap** (finding above).

## How to read the result

| What you see | What it means | What to do |
|---|---|---|
| Manual action present | Penalty | Reconsideration request. Nothing else matters. |
| Indexed count fell on 25 Mar | Pages dropped out | The reason bucket names the cause. Work that bucket. |
| Indexed flat, impressions fell | Surface change, not technical | Confirms the fan-out reading. No technical fix exists; the answer is the YouTube/Pinterest/email plan. |
| Large "Crawled — currently not indexed" | Quality/authority judgement | Expected on a zero-backlink domain. Not a bug. Remove the 34 `/uncategorized/` duplicates, then earn links. |
| Large "Discovered — currently not indexed" | Crawl budget / low perceived value | Same cause, worse. Prune hard before publishing more. |

## What this check cannot tell you

It cannot confirm the AI fan-out reading — Search Console does not label which impressions
came from AI surfaces. The query-shape evidence in `plans/lft-search-diagnosis.md` is as
close as the data gets. What this check *can* do is rule out the alternatives: a penalty, a
deindexing event, a crawl failure or a canonical conflict. Three of those are already ruled
out for the money pages by the inspection above.

## Tests

```bash
node lft/indexing/check-indexing.mjs --csv lft/indexing/test/sample-page-indexing.csv \
  --sitemap lft/indexing/test/sample-sitemap.txt
```

The fixture covers indexed, crawled-not-indexed, discovered-not-indexed, a canonical
conflict, a 404 and a sitemap orphan. Column names are detected rather than assumed, because
GSC's export headers vary by locale and by report — override with `--url-col` / `--reason-col`
if detection misses.
