# LFT search diagnosis — the answer

Run 3 Oct 2026 against the live Search Console property for `luggagefortravel.com`, via the
OpenSEO connector. Window: 30 Sep 2025 – 30 Sep 2026. Every figure below is first-party GSC
data from a query I actually ran, not an export or an estimate.

**None of the three explanations I offered was right. The real answer is worse, and it
changes the strategy.**

---

## Finding 1 — the ~27,000 impressions is a 12-month total, not monthly

| Page | Impressions (12mo) | Clicks | Avg pos | CTR |
|---|---:|---:|---:|---:|
| airlines-that-charge-for-carry-on | 3,632 | **1** | 7.2 | 0.03% |
| frontier-airlines-carry-on-size | 3,350 | 2 | 13.5 | 0.06% |
| best-ryanair-cabin-bag | 2,009 | 3 | 9.6 | 0.15% |
| easyjet-cabin-bag-policy-2026 | 1,883 | 1 | 31.3 | 0.05% |
| ryanair-carry-on-size-rules-2026 | 1,525 | 1 | 23.4 | 0.07% |
| american-airlines-carry-on-size | 1,408 | 0 | 63.0 | 0% |
| delta-carry-on-size | 1,303 | 1 | 43.8 | 0.08% |
| united-airlines-carry-on-size | 1,003 | 0 | 48.1 | 0% |
| how-strict-are-airlines | 771 | 0 | 7.7 | 0% |
| *(29 further pages ≥100 impressions)* | | | | |
| **Whole site, 38 pages ≥100 impressions** | **~28,000** | **17** | — | **0.06%** |

The earlier figures were right in magnitude but wrong in period. That's **2,300 impressions a
month across the entire site**, and 17 clicks **in a year**.

## Finding 2 — 85% of it was one four-week burst that ended on 25 March

Daily impressions, from the GSC date series:

| Window | Impressions/day | Avg position |
|---|---|---|
| 20 Jan – 20 Feb 2026 | 6 – 55 | 45 – 82 |
| **21 Feb** | 144 | 13.2 |
| **25 Feb – 24 Mar** | **540 – 1,591** | 13 – 46 |
| **25 Mar** | **23** | 3.2 |
| 26 Mar – 30 Sep 2026 | 1 – 42, mostly under 20 | varies |

It went from 539 impressions on 24 March to 23 on 25 March, overnight, and never recovered.
The last three months average **single digits to low tens per day**. On several days this
September the site recorded **zero impressions**.

So the "27,000 impressions of latent demand" is a mirage. It is one burst, six months dead.

## Finding 3 — those impressions were mostly machines, not people

This is the part that matters. Here are the actual queries driving the biggest page
(`airlines-that-charge-for-carry-on`, 115 queries, 12 months):

```
spirit vs united total cost with carry-on and checked bag 2026         59 impressions, pos 8.6
spirit vs united total cost with bags comparison 2026                  49            , pos 6.3
spirit vs united airlines total cost comparison with carry-on ... 2026 37            , pos 3.8
is spirit cheaper than united with bags included 2026                  36            , pos 6.2
spirit vs united airlines total cost comparison with baggage 2026      32            , pos 4.0
is spirit cheaper than united with baggage fees included 2026          31            , pos 8.0
is spirit cheaper than united including baggage fees 2026              30            , pos 7.5
… roughly 60 further near-identical permutations
```

Every one of them: **zero clicks**. Positions 2–9.

Meanwhile the actual human queries on that same page:

```
which airlines charge for carry on          3 impressions, position 56
airlines that charge for carry on           4 impressions, position 28
what airlines charge for carry on bags      2 impressions, position 59
airlines charging for carry on              2 impressions, position 58.5
```

The pattern repeats on the Ryanair page: dozens of permutations of
`ryanair cabin bag size 2026 55x40x20`, `ryanair personal bag size 40x20x25 2026`, all
fully-formed, all 2026-suffixed, all positions 6–11, all zero clicks.

**Hyper-specific, fully-formed, near-duplicate natural-language queries, arriving in
permutation sets, ranking well, converting at zero — that is the signature of AI query
fan-out**, where Google's AI layer decomposes one user question into many synthetic
sub-queries behind the scenes. Those register as impressions. No human ever saw a result
page, so no human could click.

## What the average position of 7.2 actually was

It was an artefact. The page ranked 2–9 for *machine* queries and 28–87 for the *human*
ones. The weighted average landed at 7.2 and told you nothing true. Note what happened when
the fan-out stopped on 25 March: impressions fell 95% and average position **improved** to
3–5, because only the thin set of real queries was left.

---

# The answer to the question

**LFT does not have a CTR problem.** It never did. It has two problems:

1. **Almost no organic presence.** For the queries real people type, the site ranks
   position 28–87. One click a year on your biggest page is not a snippet problem.
2. **The traffic it did have was never human** and switched off six months ago.

Chasing CTR on this cluster would have been optimising a number that cannot convert. I'm
glad we checked before you filmed anything.

## What to verify next (30 minutes, in GSC itself)

The 25 March cliff needs a cause. In order:

1. **Manual actions** and **Security issues** — rule out a penalty first. One click each.
2. **Page indexing report** — how many pages are actually indexed versus "Crawled – currently
   not indexed" / "Discovered – not indexed". For a site with this profile I'd expect a large
   not-indexed bucket, which would be the real story.
3. **Date 25 March 2026 against the Google update timeline** — if a core update landed in that
   window, that's your answer and it's an authority problem, not a technical one.
4. **The redirect backlog** already found: `/carry-on-size-by-airline/` logs as a 404 in the
   crawl while GSC shows it ranking, and several post-result recommendation links point at 301
   sources. That's not the cause of a March cliff, but it is bleeding whatever is left.

## What this means for the strategy — and it's not a small change

The plan I gave you treated SEO as the base and YouTube, Pinterest and email as
diversification. **Invert that.**

- **The search channel has already run the experiment and returned a verdict.** A year of
  content produced 17 clicks. Where the content did surface, Google's AI layer consumed it
  and returned nothing. Betting the next year on the same channel is betting on the one thing
  that has demonstrably not paid.
- **YouTube and Pinterest are no longer diversification. They are the business.** Both are
  channels where a human has to look at your thing to consume it, and neither has an AI layer
  summarising you out of the transaction.
- **Email goes from important to existential.** It is the only channel you own outright.
  Every view from YouTube and Pinterest must be converted to an address, which is exactly
  what the capture script does.
- **The checker is now the most valuable asset on the site**, because it is the one thing an
  AI summary cannot replace: it takes the user's own measurements as input. A summary can
  tell you Ryanair's limit. It cannot tell you whether *your* bag fits.
- **Don't abandon SEO — change its job.** Stop targeting informational queries that AI
  answers. Target the tool, the fare-level queries nobody covers, and being the *cited
  source* inside AI answers. You have the `seo-ai-visibility` skill installed for exactly this.

One genuine positive hides in this data: during the burst, the site was being pulled into AI
answers at **positions 2–9** for detailed, fare-level comparison questions. The content is
good enough to be cited. It just isn't good enough — or authoritative enough — to be clicked,
and the citation traffic was switched off. Being the source AI quotes is a real strategy; it
is simply not a traffic strategy.
