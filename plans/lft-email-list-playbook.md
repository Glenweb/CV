# LFT — email list playbook

Prepared 2026-10-02. Specification only: the Kit (ConvertKit) connection was not reachable
during research, so nothing in section 4 has been built or verified against the live account.

## Two corrections before the plan

### The Amazon-in-email rule is murkier than usually stated — build as if it's banned anyway

Amazon's current **Participation Requirements** permit Special Links in email, SMS and social
DMs *provided the communications are solicited (opted into)*. But the **Operating Agreement's**
offline-promotion clause still separately prohibits Special Links "in any ... mailing, SMS,
MMS, email or attachment to email". The two documents conflict on their face, and the downside
of guessing wrong is account termination with funds forfeited.

**Decision: design as though Amazon links in email are banned.** Not because the ban is
unambiguous, but because the compliant architecture — *email → own-domain roundup page →
Amazon link* — is strictly better anyway. You keep the pageview, the display revenue, the
internal-link equity, the retargeting, the ability to swap merchants without resending, and
click data you own. The upside of direct linking is a marginal CTR bump; the downside is the
whole monetisation layer.

*If you ever want direct links, get written confirmation from Associates support first and keep it.*

### You already own a lead-magnet generator

`lead-magnets.js` in Drive is an Express router with versioned lead magnets, avatar-driven
generation, tone and section options, HTML preview, publish/unpublish, a per-version
`delivery: {subject, body}` and `cta: {label, url}`, and an n8n `magnet_published` webhook.
If that service is live, **don't hand-build magnets in Canva** — generate v1 through it and let
the n8n hook push delivery copy into Kit. Immutable versions are exactly what you want for
hook A/B tests.

## 1. What someone actually trades an email for

Not "travel tips". Three things, in order of pull:

1. **Fee avoidance** — "will I get stung at the gate?"
2. **Decision shortcut** — "just tell me which bag fits my airline"
3. **Change insurance** — "tell me when my airline's rules change"

Everything else converts worse because the pain isn't acute at the moment of reading.

| # | Lead magnet | Effort | Why here |
|---|---|---|---|
| 1 | **Carry-On Size Cheat Sheet by Airline** (printable, 1 page) | Low–Med | Perfect intent match on the highest-traffic cluster. Screenshot-able at the gate. Reusable across ~40 pages as a content upgrade. |
| 2 | **Ryanair / easyJet / Wizz "Will It Fit?" Packs** (3 separate PDFs) | Low | Sharpest pain, best-differentiated cluster, and it segments by airline on capture. Three magnets, not one. |
| 3 | **Baggage Fee Tracker 2026** | Med | Quantified saving. "Updated quarterly" justifies staying subscribed. |
| 4 | **Airline Rule Change Alerts** (ongoing, not a PDF) | Low to launch | Highest retention and the best segmentation device — they pick airlines, you tag them. The Spirit shutdown page proves you already do this. |
| 5 | **Checker result, emailed** | Low (tool exists) | Pure intent capture at the highest-intent moment on the site. |
| 6 | **"Bags That Actually Fit" shortlist by airline** | Med | Monetises directly. Needs genuine measurement or it's a trust liability. |
| 7 | Packing checklist by trip type | Low | Broad, lower intent, good trip-type segmentation. |
| 8 | Cabin bag fee calculator (interactive) | High | Potentially the best performer and a link magnet. Defer past 30 days. |
| 9 | Liquids & restrictions card | Low | Genuinely confusing right now. Must be maintained or it becomes misinformation. |
| 10 | Printable measuring guide + cut-out sizer | Low | Cheap, high perceived utility, very Pinterest-able. |
| 11 | Family travel baggage planner | Med | Underserved, high value. Second wave. |
| 12 | Gate-check rescue kit | Low | Shareable, low commercial intent. List-warmer. |

**Launch with 1, 2 (Ryanair first) and 4.** One broad workhorse, one sharp wedge, one retention
engine. Add 5 in week three. Ignore 8 and 11 for now.

**Avoid:** a generic "Ultimate Travel Guide" ebook. High effort, low intent-match, no segmentation value.

## 2. On-site capture

Sector benchmarks for orientation only, **not forecasts for LFT**: average site-wide opt-in
~2.1%; 3–8% counts as well optimised; average popup conversion 3.5–5%.

Google's actual intrusive-interstitial rule: problematic = a popup covering main content
*immediately on arrival from search*. Explicitly fine = easily dismissible banners using
reasonable screen space. **Timing is the hinge.**

| Mechanic | Rel. conversion | Risk | Verdict |
|---|---|---|---|
| **Inline content upgrade** (airline-specific magnet inside that airline's page) | Highest | CLS only if JS-injected | **Ship first.** 40+ pages each with a natively relevant offer — the best mechanic you have. |
| **Two-step click trigger** ("Get the Ryanair sheet" → modal) | Very high | Safe — user-initiated | **Ship first.** |
| **Checker result capture** (after the result, never before) | High | Safe | **Ship.** See below. |
| End-of-post block | Med-high | None | Ship. Cheap, zero risk. |
| Comparison-table gate | Medium | **Serious** — gating content you rank for risks thin-content problems and kills the page | **Don't gate.** Offer the printable version alongside the full visible table. Same capture, no exposure. |
| Exit-intent modal | Medium | Safe on desktop only — mobile exit detection fires on scroll-up | Ship, **desktop only**. |
| Slim sticky bar, dismissible | Low-med | Safe, inside Google's carve-out | Ship. Best risk-adjusted always-on mobile capture. |
| Scroll slide-in at 60–70% depth | Medium | Safe | Ship. The mobile-safe substitute for a popup. |
| Quiz ("which cabin bag fits your airline?") | High | Safe as a page | Phase 2. |
| Timed popup on arrival | Medium | **This is the penalty case** | **Reject.** |
| Welcome mat / full-screen entry | Low-med | Worst case on organic landing pages | **Reject.** |
| 404 page | Low volume, decent rate | None | Ship — you have a redirect backlog, so 404s get real traffic. |
| Kit-hosted landing pages per magnet | High | None | **Ship** — the destination for Pinterest/YouTube traffic. |
| Resources hub + nav/footer | Low | None | Ship. Also what you link to off-site. |
| Sidebar form | Low | Minor LCP | Low priority. Near-dead on mobile. |

### The checker: capture without wrecking it

**Do not gate the result.** It destroys the tool's utility, it's exactly the "dismiss before
accessing content" pattern Google calls out, and it kills the page's link-earning potential.

Instead:
1. Show the result **immediately, free, no email** — "Fits Ryanair cabin ✓ / Too deep for easyJet ✗ by 2cm."
2. **Directly beneath it**, offer something more durable than the result: *"Email me this result + the full size sheet for all 51 airlines + alert me if Ryanair changes its rules."*
3. Pre-fill the airline they just checked → auto-tag `airline:ryanair`, `source:checker`.
4. Below that, the money path: bags that fit, linking to the relevant roundup.

Peak intent, after you've proven value, incremental rather than extractive, and it segments
automatically. SEO-safe, CWV-safe, interstitial-safe.

**Cap it at three capture points per page** (inline upgrade + end-of-post + sticky bar). Kit's
embed is third-party JS: load it deferred, reserve explicit heights, never inject above
existing content. The realistic risk isn't a penalty — it's CLS and INP drag from stacking forms.

## 3. Off-site

**Tier 1 — do these**
- **Pinterest.** Best channel in this niche, full stop. Printables and size charts are native
  content, the audience is planning-stage, and it's a search engine with a long tail. Pin to
  the Kit landing page, not the blog post.
- **YouTube Shorts.** "Does this bag fit Ryanair's sizer" is inherently visual. Builds branded search.
- **Newsletter swaps.** Highest-quality subscribers per unit effort. Kit's Creator Network and
  Recommendations are built in and are the cheapest list-growth lever you have.
- **TikTok bio funnel.** Repurpose the Shorts; don't build a second pipeline.
- **Guest posts + digital PR.** Baggage fees are consumer-affairs news and UK outlets cover them
  constantly. **HARO queries are already arriving daily in the inbox and being ignored** — that's
  free high-authority coverage sitting unopened.

**Tier 2 — selectively**
- **Reddit/forums.** r/onebag, r/travel, r/ryanair are full of the audience and **most ban
  self-promotion and affiliate links outright.** What works: answer size questions substantively
  with **no link**, keep a profile that names the site. Never astroturf — one ban can get the
  domain sitewide-filtered.
- **Facebook groups.** Converts when you answer the recurring "will this fit?" question. Admin
  permission first.
- **Quora.** On-site links only; affiliate links get flagged. Low priority.
- **Podcast guesting.** Good authority, poor direct conversion. Use a short vanity URL.
- **Substack/beehiiv cross-promo.** Worth it.
- **Google Business Profile.** **Skip** — content publisher, no service area.

**Tier 3 — care or skip**
- **Giveaways — not in the first 90 days.** UK traps: you **cannot make marketing consent a
  condition of entry** (consent must be freely given, so entrants need a separate unticked
  opt-in, which guts the ROI case); paid entry can make it an illegal lottery under the Gambling
  Act 2005; ASA/CAP requires promoter, closing date, prize details and winner selection stated;
  Meta requires a platform release. Loop giveaways and prize aggregators will wreck deliverability.
  If run later, make the prize niche-specific (a Ryanair-compliant cabin bag), never a generic iPad.
- **Paid acquisition — not until you have ~3 months of revenue-per-subscriber data.** Amazon's
  rates plus a 24-hour cookie make paid-to-affiliate maths brutal. The one later exception is a
  small Pinterest test on a proven organic pin.

## 4. Kit build (specification — not yet built)

### Forms
1. Inline content upgrade (magnet varies by page) · 2. Sticky bar · 3. Exit intent (desktop) ·
4. Scroll slide-in · 5. Checker result capture · 6. 404 / resources hub ·
7. Kit landing pages: `/cheat-sheet`, `/ryanair-fit`, `/easyjet-fit`, `/wizz-fit`, `/fee-tracker`, `/alerts`

### Tag taxonomy — this is the whole ballgame, get it right on day one

- **Airline:** `airline:ryanair|easyjet|wizz|united|delta|american|southwest|jetblue|alaska|spirit`
- **Trip type:** `trip:weekend|1week|longhaul|family|winter|business`
- **Category:** `cat:cabin-bag|personal-item|checked|backpack|packing-cubes|accessories`
- **Source:** `magnet:cheat-sheet|ryanair-fit|fee-tracker|alerts`, `source:checker|pinterest|youtube|organic`
- **Lifecycle:** `seq:welcome-complete`, `engaged:90d`, `cold:180d`, `clicked:money-page`
- **Region:** `region:uk|eu|us` — fees, merchants and applicable law all differ

Tag automatically on capture. Never ask someone to self-select what the page already told you.

### Welcome sequence — 6 emails over 12 days

No Amazon links anywhere; every commercial link goes to an LFT page.

| # | Day | Job |
|---|---|---|
| 1 | 0 | **Deliver the magnet. Nothing else.** Your highest-open email ever — deliverability-critical. |
| 2 | 1 | Biggest quick win: the measuring mistake that gets bags stopped (wheels and handles). |
| 3 | 3 | **Segment:** "which airline do you fly most?" — buttons apply `airline:*`. Highest-value email in the sequence. |
| 4 | 5 | First monetisation: bags that fit *their* airline → the relevant roundup. Tag `clicked:money-page`. |
| 5 | 8 | The fee maths: gate fees vs a bag that fits. Non-Amazon affiliate slots live here. |
| 6 | 12 | Set the ongoing relationship, offer alerts and a second magnet. Tag `seq:welcome-complete`. |

### Automations
Magnet → tag → correct welcome entry · link-click tagging on every airline and category link ·
alerts routed by `airline:*` · cold suppression at 180 days with one re-permission email ·
dupe-magnet suppression · the n8n `magnet_published` hook wired into Kit to stop copy drift.

### Monetising without Amazon links in email
1. **Own-domain roundups are the primary path.** Every commercial email's job is a click to an
   LFT money page, not a sale.
2. **Non-Amazon programmes that *can* go directly in email** (candidates — commission rates and
   approval unverified, and some have their own email restrictions): Holiday Extras (airport
   parking/lounges — exceptional UK fit), AirHelp (delay and baggage compensation — unusually
   high fit with a baggage-problem audience), Airalo/Holafly eSIM, SafetyWing/World Nomads,
   luggage brands via Awin/CJ/Impact (Antler, Tripp, Samsonite, Osprey, Decathlon, John Lewis,
   Argos), Trainline, GetYourGuide, Booking.com, Wise/Revolut.
3. **Sponsorships** once the list supports it. Not a month-one line.

The Amazon constraint is the *reason* to build non-Amazon revenue — and that diversification is
the real win regardless of how the policy conflict resolves.

## 5. Deliverability and UK law

**Your regime is UK GDPR + PECR, not CAN-SPAM.** Consent must be freely given, specific,
informed and unambiguous; pre-ticked boxes and inactivity are explicitly not consent. The PECR
**soft opt-in does not apply** — it requires details collected during a sale or negotiation of a
sale, and LFT is a content site, not a shop. You need real consent.

**Use double opt-in.** GDPR doesn't require it, but it requires *proof*, and the confirmation
click is the cleanest proof available. You lose a little volume and gain it back in
deliverability on a new sending domain.

### Sign-up copy (use this)

> **Get the Carry-On Size Cheat Sheet**
> Enter your email and we'll send the printable cheat sheet straight away.
>
> ☐ Yes, email me the cheat sheet plus luggage size updates, baggage fee changes and bag recommendations from Luggage For Travel.
>
> We'll email you a confirmation link first. Unsubscribe any time in one click. We never sell or share your data. See our [Privacy Policy](/privacy-policy/).
> Luggage For Travel is operated by GMK Media Ltd.

Unticked, separate from the download, names who and what. Not bundled with anything unrelated.

**Also required:** one-click unsubscribe, a genuine postal address for GMK Media Ltd and the
registered company name in every email; `List-Unsubscribe` header (Kit handles it); a consent
log of date, method, form, IP and exact wording — that's your ICO defence; a cookie banner
(separate PECR obligation, don't conflate); a privacy policy covering Kit as processor, the
transfer basis, retention and data-subject rights.

### Warming the sending domain
1. SPF, DKIM and **DMARC** (`p=none`, then tighten) before the first send — non-negotiable at Gmail/Yahoo.
2. Send from a **subdomain** (`news.luggagefortravel.com`), never the root that carries business mail.
3. Never buy, scrape or import a list. One purchased list ends this.
4. Ramp over 3–4 weeks — the welcome sequence does this naturally, which is an argument for
   launching capture *before* broadcasting.
5. Most engaged first. Watch Google Postmaster from day one; keep complaints under 0.1%.
6. Consistent weekly cadence beats sporadic blasts. Suppress bounces immediately.

## 6. First 30 days

**Week 1 — foundations, zero sending.** Kit audit and the full tag taxonomy; double opt-in on
globally. DNS: SPF, DKIM, DMARC on the sending subdomain; enable Postmaster. Build magnet #1
through the existing generator. Privacy policy update and the reusable sign-up block. Kit
landing page `/cheat-sheet` plus the inline upgrade on three pages only.

**Week 2 — capture live, sequence built.** Welcome emails 1–3 (email 1 must be perfect), then
magnet #2 (Ryanair), then emails 4–6 with link-click tagging. Sticky bar and end-of-post
sitewide — measure CWV before and after. **Friday: roll the content upgrade out to all ~40
airline pages, airline-matched. Highest-value single task of the month.**

**Week 3 — the checker, and off-site.** Checker result capture with auto-tagging. Pinterest: 5
pins to Kit landing pages. Apply to 4–6 non-Amazon programmes. 404 page, resources hub,
desktop exit-intent and scroll slide-in. **Start answering the HARO queries already arriving.**

**Week 4 — alerts, swaps, first broadcast.** Alerts magnet and airline routing. First YouTube
Short. Turn on Kit Creator Network and approach 3–5 comparable UK travel newsletters for swaps.
Review Postmaster, confirmation rates and per-placement conversion; kill the worst placement.
**Draft the first broadcast for sign-off — don't send it automatically.**

**Ignore until day 30:** paid ads, giveaways, the fee calculator, the family planner, the quiz,
TikTok, podcast guesting, Quora, Google Business Profile (permanently), a second welcome
sequence, Facebook groups. *Resisting these is most of the plan's value.*

## Open items

1. **Kit account access** — the connection failed during research, so section 4 is unbuilt spec.
2. **Amazon email policy** — get written confirmation if you want direct links. Designed around the ban meanwhile.
3. **GMK Media Ltd postal address** — legally required in email footers.
4. **Privacy policy sign-off** before any capture form goes live.
5. **Is `lead-magnets.js` live, and where?** If so, magnet production gets much faster.
