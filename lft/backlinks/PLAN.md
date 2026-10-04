# LFT backlinks — the ceiling, and how to raise it

Re-derived 4 Oct 2026 from the live link index, not restated from earlier analysis.

---

## Correction: it is 2 editorial links, not 3

I said "3 editorial" twice without deriving it. Filtered to spam score under 40,
**269 referring domains collapse to 8 rows.** Of those 8:

| Domain | Link | Verdict |
|---|---|---|
| **unitedtravels.ca** | dofollow → `/packing-guides/tsa-liquid-rules-2026/`, anchor *"Luggage For Travel's rule-by-rule breakdown"*, spam 0, first seen **30 Sep 2026** | **GENUINE EDITORIAL** |
| **www.liniaa.shop** | dofollow → `/airline-baggage-rules/carry-on-luggage-size-restrictions-by-airline/`, anchor *"Luggage for Travel's airline restrictions guide"*, spam 0 | **GENUINE EDITORIAL** |
| oppalerts.com | nofollow, auto-generated AI-visibility tracker page | legitimate, not editorial |
| jessicaburkhart.com | ugc/nofollow blog **comment** on a 2014 post, anchor "FranziskaTerrell" | comment spam, not yours |
| www.five.co.in | dofollow, but a `/domains/16637/` stats listing | auto-generated |
| global-ranks.pages.dev | nofollow auto listing | auto-generated |
| global-websites.pages.dev | nofollow auto listing | auto-generated |
| isonade.pages.dev | nofollow auto listing | auto-generated |

**Two links. That is the entire editorial profile.** Everything else in the 269 is scraper
farms, PBN sales pages, URL shorteners and domain-stats listings.

`unitedtravels.ca` landed four days ago and I missed it in the first sweep — my page-1 pull
was sorted by first-seen and it was buried under 185 spam rows. Worth knowing the baseline
is 2 links in roughly 18 months with **zero outreach**, not zero. About 1.3 a year, organic.
Any deliberate effort beats that.

## What both links teach you — this is the actual finding

Both genuine links point at **reference content that answers a rules question precisely**:

- the airline restrictions guide
- the TSA liquid rules breakdown

**Neither points at a "best carry-on luggage" page.** Not one of the commercial pages has
earned a single editorial link in 18 months, and both earned links came with natural
brand-mention anchors from bloggers citing you as the source.

That settles the strategy. **The rules, data and tool pages are the link assets. The
commercial pages are the conversion layer and will never earn links on their own.** Build
links to the reference content, then pass authority internally to the money pages.

### Fix this first — it costs ten minutes

`liniaa.shop` points at `/airline-baggage-rules/carry-on-luggage-size-restrictions-by-airline/`,
which **301s** to `/carry-on-size-by-airline/` and is **still listed in post-sitemap.xml**.
One of your two links is landing on a redirect hop, and the stale sitemap entry is
advertising the dead URL. Clean the sitemap; leave the 301.

`unitedtravels.ca` points at `/packing-guides/tsa-liquid-rules-2026/` — indexed, but
position 89 on 1 impression. Your newest editorial link is pointed at one of your weakest
pages. That page is now worth real work.

---

## The three link assets you already own

### 1. The checker — already embeddable, and correctly built

`/carry-on-size-checker/` has a **"Copy embed code" button** shipping an iframe plus an
attribution paragraph with a real `<a href>` back to the domain. That matters: the iframe
itself passes nothing, the attribution line does. Whoever built that got it right.

A free, fare-aware size checker covering 51 airlines is the single most linkable thing on
the site. Tools earn links at authority levels where articles cannot, because the linker
gets something their reader uses.

Two things to improve before pitching it: the embed is a fixed `height="700"` which will
clip on mobile, and there is no lightweight standalone embed URL — framing the full page
drags in your header, footer and nav. **Build `/carry-on-size-checker/embed/`**: the tool
only, no chrome, responsive height, attribution link baked in and not removable.

### 2. The airline dataset — 51 airlines, 112 allowances, enforcement tiers

`lft/fare-watch/airlines.json` is original structured data. Nobody else publishes
carry-on allowances **with an enforcement tier attached**, and the tier classification is
the genuinely novel claim: *which airlines actually measure your bag.*

That is a journalist's story, not a blogger's. "Nine airlines will size your bag at the
gate; thirteen will only look" is a headline. Publish it as a standalone, citable data page
with a stated methodology and a last-verified date.

### 3. The EU 2027 fare-display rule — a dated news hook

The EU 2027 work is verified against the primary text of Regulation (EU) 2026/2202, with
the fare-display obligation affecting Ryanair, easyJet, Wizz Air and Aer Lingus. It has a
date attached, which is what makes a hook a hook.

**This is time-limited.** Its value decays to near zero once the mainstream travel press
covers it. Of everything here, this is the one with a deadline.

---

## The plays, in order of yield per hour at zero authority

1. **Tool embed outreach.** Target: travel bloggers, packing-guide writers, flight-deal
   newsletters, university study-abroad pages, corporate travel intranets. The pitch is a
   free widget their readers will use, not a request. Highest conversion of anything here.
2. **Data-led digital PR on the enforcement tiers.** One good pickup in a travel desk
   produces syndication, and syndicated links are the only realistic route to a
   high-authority link for a site at this level.
3. **The EU 2027 story, now.** Deadline-driven. Pitch while it is still news.
4. **Broken-link reclamation.** Spirit died in May; Spirit carry-on pages across the web are
   now dead links on live blogs. Every one is a page owner with a broken link and a
   ready-made replacement — your `/spirit-airlines-shutdown/` page. This is the cleanest
   outreach pitch in existence: *your link is broken, here is a working one.*
5. **Unlinked mention reclamation.** Cheap, low volume, worth running once.
6. **The two existing linkers.** `unitedtravels.ca` and `liniaa.shop` both chose to cite
   you unprompted. They are the warmest contacts you have and nobody has ever spoken to
   them. Thank them, offer the embed, ask what else would be useful.

---

## What the agents can do, and what only you can do

**Agents, unsupervised:**
- Build `/carry-on-size-checker/embed/` and the citable data page
- Derive the enforcement-tier dataset into press-ready form with methodology
- Find and **verify** prospect lists — pages already writing about carry-on rules and
  already linking out, which is the only prospect worth contacting
- Find every dead Spirit carry-on URL with live inbound links (broken-link targets)
- Find unlinked brand mentions
- Draft every pitch, individually, against the actual page being pitched
- Track new and lost links and report changes

**Only you:**
- **Send the email.** From your domain, in your name. Outreach from an agent's inbox is
  cold mail with worse deliverability and no recourse.
- Be the quotable human. A travel desk quotes a named person at a named company, not a
  dataset.
- Decide what GMK Media Ltd is willing to say publicly about an airline.

The honest split: agents can do roughly 80% of the hours and none of the sending.

## What not to do

- **No disavow.** Manual actions are clear and the 185 spam domains are passive scrapers.
  Filing a disavow tells Google you have a scheme to clean up.
- **No paid links, PBNs or "guest post packages."** You are already receiving pitches from
  that industry — `/all/1785/15.html` across 13 domains is a link-selling network
  advertising to you. Buying from them puts you in the same index.
- **No HARO/journalist-request platforms.** Both agents independently found this does not
  work for this vertical, and I was wrong to recommend it earlier.
- **No directory submissions.** That is what produced 185 of your 269 domains.
- **No volume guest posting.** At two editorial links, twenty mediocre guest posts read as
  a pattern, not as authority.

## A realistic 90-day target

| | |
|---|---|
| Starting point | 2 editorial links |
| Organic rate with no effort | ~1.3 per year |
| Target, 90 days, with real outreach | **10–20 editorial links** |
| Pitches required | 80–150, individually written |
| Expected reply rate | 5–15% |
| Expected link rate from replies | 30–50% |

Ten links will not put you on page one for "carry on size". It roughly quintuples the
authority the whole site is built on, which is the difference between consolidation being
pointless and consolidation being the thing that lets the next twenty links count.

**The order matters.** Build the embed page and the data page first — about a week of agent
work — because every play above except reclamation depends on having something worth
linking to. Pitching the current site is pitching 96 pages with zero clicks.
