# LFT backlinks — the real picture

Pulled live 3 Oct 2026 via OpenSEO (DataForSEO backlink index), scope `subdomains`,
spam filter off for the overview. Credits spent: ~80.

**"Zero external backlinks" is wrong, and has been propagated through every plan since
28 August.** The practical conclusion was right — there is effectively no authority — but
the facts were not, and one of them needs acting on today.

## The numbers

| | |
|---|---|
| Total backlinks | **266** |
| Referring domains | **254** |
| Domains surviving a spam filter | **9** |
| Genuine editorial links | **3** |
| Profile spam score | **51 / 100** |
| Broken pages receiving links | 74 |

## A spam surge started in late September and is still running

| Month end | Backlinks | Referring domains | New domains |
|---|---:|---:|---:|
| Oct 2025 | 25 | 22 | 0 |
| Jan 2026 | 39 | 35 | 8 |
| Mar 2026 | 47 | 41 | 4 |
| Jun 2026 | 50 | 43 | 2 |
| Jul 2026 | 50 | 43 | 1 |
| Aug 2026 | 63 | 52 | 10 |
| **Sep 2026** | **247** | **236** | **+185** |

The new domains are auto-generated SEO-tool pages: `imperiousseo.link`,
`massbacklinkgenerator.website`, `dofollowbacklinkmaker.space`, `increasebacklinks.site`,
`pagerankchecker.store`, `dacheckerofwebsite.store`, and roughly 180 more in the same
pattern. Spam scores 45–60.

**They are still arriving.** Timestamps from the pull: 2026-10-01 01:23, 2026-10-02 23:55,
2026-10-03 00:36, 2026-10-03 01:08 — several per hour, overnight, as of the moment of the
query.

### What this is, most likely

Free "DA checker" and "backlink checker" tools publish a results page for every domain
submitted, and that page contains a link to the domain checked. Submit a domain to 200 of
them and you get 200 referring domains. This is the single most common form of harmless
backlink noise on the web, and Google generally ignores it.

**It needs an explanation, though, and only Glen has it.** Did anyone — you, an agency, a
freelancer, or an automated tool — start running luggagefortravel.com through SEO checkers
or sign up for a free backlink service around 29 September? The alternative readings are
an automated audit loop someone left running, or deliberate negative SEO, and the response
differs.

### What it is *not*

**It did not cause the March cliff.** The surge begins in late September; the collapse was
25 March, six months earlier. Do not let anyone connect them.

## The three links that are actually real

Everything else is auto-generated, a blog comment, or a domain-stats page.

| From | To | Anchor | Type | First seen |
|---|---|---|---|---|
| `unitedtravels.ca/blog/packing-rules-changed-2026` | `/packing-guides/tsa-liquid-rules-2026/` | "Luggage For Travel's rule-by-rule breakdown" | **dofollow**, spam 0 | 30 Sep 2026 |
| `liniaa.shop/2026/04/01/carry-on-packing-guide/` | `/carry-on-luggage-size-restrictions-by-airline/` | "Luggage for Travel's airline restrictions guide" | **dofollow**, spam 0 | 10 Apr 2026 |
| `streetdirectory.com/etoday/carry-on-travel-luggage-wlpwo.html` | homepage | bare URL | **dofollow**, spam 35, **domain rank 63** | 30 Apr 2026 |

`streetdirectory.com` at domain rank 63 is by a wide margin the strongest link pointing at
the site. It is an old-style article directory, so the value is limited, but it is real.

The other six that survive filtering are not worth counting: three `pages.dev`
auto-generated ranking pages, a `five.co.in` domain-stats page, a 2014 blog comment on
`jessicaburkhart.com` with the anchor "FranziskaTerrell", and `oppalerts.com`.

**`oppalerts.com` is worth one look for a different reason.** It links to
`/airline-baggage-rules/airlines-that-charge-for-carry-on/` from a page at
`/AI-Search-Visibility/airlines/budget-weekend-explorer/llm-search-fanout-visibility/`.
A third-party tool is tracking that page's visibility in **LLM search fan-out** —
independent corroboration of the diagnosis in `lft-search-diagnosis.md`, arrived at from
completely different data.

## What to do

**1. Do not disavow. Not yet, and probably not at all.**
Google's disavow tool is for links you or someone acting for you built, where a manual
action exists or is expected. Auto-generated checker-tool pages are exactly the category
Google's systems discount automatically. Disavowing in a panic risks removing real links
by mistake, and a disavow file is itself a signal.

**2. The manual-action check is now genuinely urgent.**
It was already the outstanding item from the 28 Aug doc. A profile spam score of 51 with
185 new spam domains in a month makes it the first thing to do, not the fourth.
Search Console → Security & Manual Actions → Manual actions. Thirty seconds.
- Clean → leave the spam alone, monitor monthly, carry on.
- "Unnatural links to your site" → *then* disavow, and the file writes itself from this data.

**3. Find the source.** See the question above. If something automated is still submitting
the domain, stopping it matters more than cleaning up after it.

**4. Nothing about the strategy changes.** Three editorial links is not meaningfully
different from zero. The authority ceiling is real, the plans built on it stand, and the
link-earning work in `lft-backlink-targets.md` is still the job.

## One correction worth carrying

The month-12 review metric in `lft-youtube-pinterest-year.md` was "referring domains —
currently zero". That baseline is now **3 genuine editorial referring domains**, and the
metric should count *editorial* domains, not raw referring domains — otherwise 185 pieces
of checker-tool spam will read as a win.
