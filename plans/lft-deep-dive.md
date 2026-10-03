# LFT — four breakdowns

Written 2026-10-02 in answer to four direct questions. Where a number comes from LFT's own
GSC export it's labelled GSC; where I'm doing arithmetic on a hypothetical, it says so.

---

# 1. The CTR opportunity — and a correction to how I framed it

## The arithmetic

| Page cluster | Impressions/mo | Avg position | Clicks | CTR |
|---|---|---|---|---|
| Airlines that charge for carry on | 3,613 | 7.09 | ~1 | **0.03%** |
| Frontier carry on size | 3,269 | 12.77 | low | — |
| Ryanair cabin bag size (two pages) | 1,974 + 1,454 | 9.26 / 21.75 | low | — |
| easyJet cabin bag size | 1,883 | 31.28 | low | — |
| How strict are airlines | 766 | 7.62 | low | — |
| **Across the airline cluster** | **~27,000** | — | **~17** | **~0.06%** |

A normal CTR at position 7 is somewhere around 2–3%. You're at 0.03%. If the cluster
performed at a plain 2%, 27,000 impressions would be ~540 clicks a month instead of 17.
**That is arithmetic on a hypothetical, not a forecast** — but the gap is roughly 30×, and
a gap that size is not a content problem. It's a diagnosis problem.

## The correction

I told you "video on those pages is a CTR fix." That was too loose, and acting on it as
stated would waste a fortnight. Here's the accurate version.

A 0.03% CTR at an average position of 7 almost never means "the title is weak." Average
position is a **weighted average across every query the page appears for**. Three
explanations fit the data, and they need completely different responses:

1. **Long-tail dilution (most likely).** You rank 3rd for a handful of low-volume variants
   and 60th for hundreds of others. The average lands at 7; the impressions are mostly from
   the queries where you're invisible. **Response: nothing is broken. Ignore the average and
   work the query-level data.**
2. **An AI Overview or answer box is satisfying the query above you.** "Which airlines charge
   for carry on" is exactly the kind of list question Google now answers inline.
   **Response: target the queries a summary can't answer — the ones needing *your* fare-level
   data — and get into the citation set rather than fighting for the blue link.**
3. **Title/intent mismatch.** The page ranks but the snippet doesn't look like the answer.
   **Response: rewrite titles and metas. Cheap, fast, testable.**

**Do this before filming anything:** open GSC, filter to that single page, and pull the
**query-level** report — not the page-level one. Thirty minutes. You'll see immediately
which of the three you've got. Everything downstream depends on the answer, and right now
nobody knows which it is.

## What video actually does here

Video is **not** primarily a CTR lever on an existing listing. What it does:

- **Earns a second surface on the same SERP.** A YouTube result and a video carousel are
  separate listings. That's additive impressions, not a better CTR on the one you have.
- **Wins key-moments treatment** via `VideoObject` + `Clip` + `SeekToAction`, which occupies
  far more vertical space in the result than a text snippet.
- **Feeds a traffic source Google doesn't control** — the real strategic point. Your entire
  current demand is one algorithm's opinion.
- **Adds engagement depth** on pages where that's a tiebreaker, not a primary signal.

So: titles and query diagnosis fix CTR. **Video buys you surfaces and independence.** Both
are worth doing. They're different jobs and conflating them was my error.

---

# 2. The wedge — what "fare-aware" actually means

## The thing itself

Every other size checker asks one question: *what airline?* Yours asks two: **what airline,
and what fare?** That second question is the whole product.

Concretely, from the tool source:

| Airline | Fare / allowance | Dimensions | Reality |
|---|---|---|---|
| Ryanair | Personal item (all fares) | 40×30×20 | Free |
| Ryanair | Priority cabin bag | 55×40×20, 10kg | Paid add-on |
| easyJet | Standard under-seat | 45×36×20 | Free |
| easyJet | Large cabin bag | 56×45×25 | Paid add-on |

Same airline. Same passenger. **Different legal answer**, depending on a checkbox they
ticked at booking three weeks ago. Across 51 airlines the tool carries roughly 50 distinct
fare labels, plus a per-airline enforcement flag and advisory note.

## Why this is the defensible position

**1. It's the only version of the question that has a true answer.** "Will my bag fit on
Ryanair?" is unanswerable. There is no Ryanair carry-on size. There are four. Every
competitor answering the one-airline-one-number version is giving people a confidently wrong
answer, and the person finds out at the gate.

**2. The competitors probably can't easily follow — but check before claiming it.** KAYAK's
tool is AR camera measurement in an iOS-only app (2018). **Momondo also has a web page at
`momondo.com/discover/carry-on-checker`**, so "they're app-only" is wrong as stated. Whether
Momondo is *fare-aware* is unverified — nobody has been able to open it from here. Until
someone does, keep the exclusivity claim out of scripts and say "fare-aware" rather than
"the only fare-aware". The wedge survives either way; the superlative is what's at risk.
What is clear is the incentive: both are built around That tells you what they optimise for:
measurement accuracy as a feature demo, inside a product whose business is flight booking.
Fare-level allowance data is a maintenance treadmill — 51 airlines changing policy
independently — with no booking revenue attached. It's a cost centre for them and the core
asset for you. That asymmetry is the moat.

**3. It converts better, structurally.** A FAIL verdict is not a sad outcome. It's a
qualified buyer identifying themselves, naming their airline and their fare, at the exact
moment they realise they need a different bag. There is no colder-to-warmer transition
available anywhere else on the site. That's why `verdict` is the highest-value parameter in
the instrumentation.

**4. No download.** KAYAK's is iOS-only and needs an app. Yours answers in a browser, from a
Google result, in under 30 seconds. On the "I'm flying Tuesday and I'm worried" use case,
that's not a small advantage.

## Where the moat is thin — be honest about this

The moat **is** the data, so the data decaying kills it. One wrong dimension and the trust
is gone permanently, because the cost of being wrong lands on the user at the gate with a
£50–95 bill. The current data checks out (Ryanair's 40×30×20 matches the August 2025 change),
but that's a snapshot.

You need a maintenance cadence or the wedge inverts into a liability:
- A quarterly all-airline audit, dated on the page.
- A `last_verified` timestamp per airline, shown in the UI. Nobody else does this, and it's
  itself a trust differentiator.
- A watch on the big six (Ryanair, easyJet, Wizz, Frontier, Spirit, BA) — those change most
  and carry most of your impressions.

Ironically the rule-change alerts magnet and this maintenance obligation are the same work.
Do it once, monetise it twice.

## How to express the wedge

**In marketing:** the single demo is cycling the fare dropdown on one airline and letting the
limits visibly change. That's V2 in the video plan and it's the one video nobody else can
make. Hook: *"Your airline doesn't have a carry-on size. It has four."*

**In the product:** consider asking for the fare **first**, before dimensions. It front-loads
the differentiator and makes the "four limits" fact unmissable rather than buried in a
dropdown.

**In SEO:** build fare-level pages, not just airline-level ones — "Ryanair Basic fare bag
size" is a different query from "Ryanair cabin bag size" and nobody is targeting it.

**In the EU 2027 story:** when the free 40×30×15 personal item lands, every airline's fare
structure gets rewritten at once. A fare-aware tool is the only kind that survives that
intact. That's a reason to be the authority *before* it happens.

---

# 3. Durable offers — the full list

"Durable" is the test for what goes under the verdict. The result they just got is
disposable: it's true for one bag, one airline, one fare, today. The offer has to be worth
more than the thing they already have for free, or it's just a tax on using the tool.

Four things make an offer durable: it **outlives this trip**, it **covers cases they haven't
hit yet**, it **keeps working as the world changes**, or it **saves money they haven't spent
yet**.

| # | Offer | Why it's durable | Best shown to |
|---|---|---|---|
| 1 | **Printable 51-airline size sheet** | One screenshot answers every future flight, for every airline, offline at the gate | PASS |
| 2 | **Rule-change alerts for their airline** | Keeps working after the rules move — the only offer that improves with time | All, esp. BORDERLINE |
| 3 | **Bags that clear [airline]'s sizer** | Solves the problem the FAIL just created | **FAIL** |
| 4 | **This result, emailed** | Something to show staff at the gate, and a record of what they measured | All (bundle, never alone) |
| 5 | **Baggage fee tracker, updated quarterly** | Priced data decays fastest, so maintained data is worth most | FAIL |
| 6 | **Their airline's enforcement profile** | "Ryanair sizes every bag; Delta almost never does" — changes the decision, not just the measurement | BORDERLINE |
| 7 | **Printable sizer template + measuring guide** | Teaches the method (wheels and handles included) so they never need the tool again — give it away precisely because it builds trust | All |
| 8 | **Pre-flight checklist timed to a departure date** | They tell you when they fly; you become useful twice more before the trip | All |
| 9 | **Family / group allowance planner** | What pools, what doesn't, pushchairs and car seats — an entirely different and underserved problem | All |
| 10 | **Liquids and restrictions card** | Genuinely confusing right now, with airports diverging — high perceived value, must be maintained |All |
| 11 | **Price watch on the bag they need** | Converts a FAIL into a purchase on *their* timeline, not yours | FAIL |
| 12 | **Gate-check rescue scripts** | What to say in the 60 seconds when staff stop you — low intent, very high shareability | All |
| 13 | **EU 2027 rule-change briefing** | A dated future event they'll want warning of; near-zero competition today | All |

## What to actually ship

Don't offer thirteen things. Offer **one bundle, worded by verdict**, which is what the
deployed code does:

- **FAIL** → *"That bag won't pass — here's what will."* Bags that clear the sizer + the
  51-airline sheet + alerts. (#3 + #1 + #2)
- **BORDERLINE** → *"That's close enough to get stopped."* Enforcement profile + sheet +
  alerts. (#6 + #1 + #2)
- **PASS** → *"Keep this for the airport."* Sheet + alerts. (#1 + #2)

One email field, one promise, three wordings. Items 5, 7, 8 and 13 become later emails in the
sequence — that's what the welcome flow is for. Items 9–12 are second-wave magnets for
other pages.

## What not to offer

A generic newsletter. "Travel tips." A discount code (you don't sell anything). An ebook.
Anything that requires them to believe you'll be interesting later rather than useful now.

---

# 4. The Amazon architecture, fully specified

## The policy position, precisely

Two Amazon documents disagree:

- **Participation Requirements** now permit Special Links in email, SMS and social DMs
  *where the recipient opted in*.
- The **Operating Agreement's** offline clause still prohibits Special Links "in any other
  offline manner (e.g., in any printed material, mailing, SMS, MMS, email or attachment to
  email…)".

The Operating Agreement is the governing contract. The penalty for guessing wrong is account
termination **with unpaid commissions forfeited**. The upside of guessing right is a small
CTR improvement. That asymmetry decides it on its own.

**Position: no Amazon Special Links in email. Ever, until you hold written confirmation from
Associates support saying otherwise.**

## The architecture

```
  Kit email                  luggagefortravel.com                  Amazon
  ─────────                  ────────────────────                  ──────
  "Bags that clear    ──►    /best-ryanair-cabin-bag/        ──►   product page
   Ryanair's sizer"          ?utm_source=kit                       (Special Link, on-page)
   [ no affiliate link ]     &utm_campaign=welcome_d5
                             &utm_content=ryanair_fail
                             │
                             ├─ Amazon links live HERE only
                             ├─ display/ad revenue earned HERE
                             ├─ internal links earned HERE
                             └─ retargeting pixel fires HERE
```

**Every commercial email's job is a click to an LFT page. Never a sale.** That single rule
keeps you compliant and is also the better business.

## Why this is better, not merely safer

| | Direct Amazon link in email | Email → LFT page → Amazon |
|---|---|---|
| Amazon ToS | Contested; termination risk | Unambiguously fine |
| Pageview | Lost | **Earned** — display/ad revenue on every click |
| Internal links | None | **Earned** — every email send is an engagement signal to a money page |
| Swapping merchants | Resend the email | **Edit the page.** Every past email updates itself |
| Price changes | Email is instantly stale and non-compliant | Page is live and correct |
| Out-of-stock | Dead click | Page shows alternatives |
| Attribution | Amazon's report only | **Your** GA4 funnel, end to end |
| Retargeting | Impossible | Pixel fires on the page |
| Non-Amazon revenue | None | Page can carry Awin, CJ, Impact and display alongside |

The last row is the strategic one: a bridge page can monetise five ways. An email link
monetises one, badly, against a 24-hour cookie.

## Three more Amazon rules people break in email

Even with no links, these still bite:

1. **No Amazon prices in email.** Amazon requires prices to be API-sourced and
   time-stamped. A price in an email is stale the moment it sends. Say *"around £40"* or
   nothing, and put the live price on the page.
2. **No Amazon product images in email.** Product imagery is licensed for use on approved
   sites via approved methods, not for redistribution in mail. Shoot or commission your own,
   or use text.
3. **Disclosure is required wherever the link is.** The LFT page needs its affiliate
   disclosure above the fold. The email doesn't need an Amazon disclosure (there's no Amazon
   link in it) but does need one if it carries any other affiliate link.

## Bridge page spec

Each money page the emails point at should carry, in this order:

1. **Affiliate disclosure**, above the fold, plain English.
2. **The answer in the first screen** — the shortlist, not a 900-word preamble. These readers
   arrived from an email that already sold them.
3. **Verified dimensions per bag**, with the airline limit shown beside them. This is the
   fare-aware wedge expressed commercially and nobody else does it.
4. **`last_verified` date.** Trust asset and a maintenance forcing-function.
5. **Amazon links `rel="sponsored nofollow"`**, plus at least one non-Amazon merchant per
   product where one exists — insurance against a single-programme dependency.
6. **A second capture point** for people who arrived from email but aren't buying today.

## Tracking it end to end

Amazon won't tell you which email drove a sale, so instrument your own side:

```
Kit link →  ?utm_source=kit
            &utm_medium=email
            &utm_campaign=welcome_d5          ← which email
            &utm_content=ryanair_fail         ← which segment
```

On the page, `checker_affiliate_click` (already in the deployed script) fires with the
airline and verdict attached. You then have: **email sent → opened → clicked → landed →
clicked out to Amazon**, by segment. The only gap is Amazon's conversion, which you
reconcile in aggregate monthly against Amazon's own report. That's as good as affiliate
attribution gets, and it's four steps more than you have now.

## Non-Amazon programmes that CAN go directly in email

These are candidates to apply to, not verified approvals, and **each has its own email
policy to check before you link**:

| Programme | Why it fits LFT |
|---|---|
| **Holiday Extras** | Airport parking and lounges. Exceptional fit for a UK travel audience. |
| **AirHelp** | Flight delay and **baggage** compensation. Unusually aligned with a baggage-problem audience. |
| **Airalo / Holafly** | eSIM. Natural pre-flight sequence placement. |
| **SafetyWing / World Nomads** | Travel insurance. High value, recurring. |
| **Awin / CJ / Impact** | Luggage brands direct: Antler, Tripp, Samsonite, Osprey, Eastpak, Decathlon, John Lewis, Argos. Often better rates than Amazon and **email is usually permitted**. |
| **Trainline, GetYourGuide, Booking.com** | Adjacent trip spend. |
| **Wise / Revolut** | Travel money. High payouts, UK-appropriate. |

**The strategic read: the Amazon constraint is the reason to build non-Amazon revenue, and
that diversification is the real win regardless of how Amazon's policy conflict resolves.**
A luggage site whose entire income depends on a 24-hour cookie at one retailer is one
commission-rate change away from a bad quarter.
