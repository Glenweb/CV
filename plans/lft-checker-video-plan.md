# LFT — video plan for the Carry-On Size Checker

Prepared 2026-10-02. Source of truth for the tool's internals is the Drive copy of
`carry-on-size-checker.html` (94,521 chars, modified 2026-06-12) — the live site was not
reachable from the research session, so anything about the **deployed** state is unverified
and flagged. Keyword positions come from LFT's own GSC export (`Pages.csv`, 2026-05-15) and
are labelled GSC. No keyword volumes were available; treat volume as unknown.

## 1. What the checker actually is

- `/carry-on-size-checker/` — H1 *"Will my bag fit? Carry-on size checker for 51 airlines."*
- Standalone single-file HTML/CSS/JS. 51 airlines. Zero dependencies beyond Google Fonts.
- **The differentiator: it is fare-aware.** Each airline carries multiple allowances with
  separate dimension and weight sets — Ryanair personal item 40×30×20 free on all fares vs
  priority cabin 55×40×20 at 10kg; easyJet 45×36×20 vs 56×45×25. Roughly 50 distinct fare
  labels, plus a per-airline enforcement flag (`strict` / `very`) and advisory note.
- Schema already present: `WebApplication`, `FAQPage`, `Offer`. **No `VideoObject`.**
- Has an embed/iframe generator that forces an attribution link back.

**Competitive position:** KAYAK and Momondo both answer "will my bag fit" with AR camera
measurement **inside their apps** (KAYAK is iOS-only). LFT is the only fare-aware, no-download,
instant-web answer. *"Same airline, four different limits"* is the wedge no competitor has.

## 2. Three blockers to fix before any video traffic arrives

All three verified in the tool source.

1. **Zero analytics.** No `gtag`, no `dataLayer`, no analytics of any kind. Nothing the checker
   does is currently measurable.
2. **Zero email capture.** No opt-in anywhere in the tool body. Every video view leaks.
3. **Broken recommendation links.** Several post-result recommendation URLs point at known 301
   sources, and `/carry-on-size-by-airline/` appears as a 404 in the May crawl while GSC still
   shows it at position 3.7 — that conflict needs a manual check.

**Day 1 is instrumentation, not filming.** If this slips, day 14 produces no decision.

## 3. The queries the checker should own

| # | Query | Evidence |
|---|---|---|
| 1 | carry-on size checker | GSC: position 8.0, 2 impressions, 0 clicks — it ranks and captures nothing |
| 2 | will my carry-on fit / does my bag fit | SERP currently owned only by AR app tools. Open to a web tool. |
| 3 | airlines that charge for carry on | GSC: **3,613 impressions, position 7.09, CTR 0.03%** — the biggest broken-CTR pool on the site |
| 4 | frontier carry on size | GSC: 3,269 impressions, position 12.77 |
| 5 | ryanair cabin bag size | GSC: 1,974 impressions at 9.26, plus 1,454 at 21.75 |
| 6 | easyjet cabin bag size | GSC: 1,883 impressions, position 31.28 |
| 7 | how strict are airlines about carry-on size | GSC: 766 impressions, position 7.62 — a pure video query already on page one |
| 8 | EU free hand luggage 2027 / 40×30×15 | **Adopted law**, not a proposal: Parliament 7 Jul 2026, Council 13 Jul 2026. Free personal item 40×30×15 under the seat plus a cabin bag to 100cm linear / 7kg, and fares must display hand-baggage-inclusive pricing. Application expected 23 Oct 2027 — verify at source before filming. Near-zero competition, no LFT page yet. |

**The strategic read:** roughly 27,000 monthly impressions across LFT's airline pages
converting to about 17 clicks. The checker should be harvesting that demand and is currently
invisible. Video's job is to feed it a non-Google traffic source *and* to fix CTR on the
high-impression pages by putting video on them.

## 4. Eight video concepts, cheapest-and-highest-converting first

| # | Concept | Hook | Format | Length | Cost |
|---|---|---|---|---|---|
| **V1** | **Type your bag's size. I'll tell you if you're paying €75.** | Fingers typing dimensions; the panel turns red on FAIL | Pure screen recording, captions, trending audio | 25s | 20 min |
| **V2** | **Same airline. Four different carry-on limits.** | "Your airline doesn't have *a* carry-on size. It has four." | Screen recording cycling the allowance dropdown as limits change | 50s | 45 min |
| **V3** | **Your Ryanair bag is 2cm too big.** | Tape measure snapping across a packed bag | Phone on tripod + screen cap of the FAIL | 40s | 1h |
| **V4** | **From 2027 your cabin bag is free. Here's the size.** | "The EU just voted to make your hand luggage free. 40 by 30 by 15." | Talking head + dimension graphic | 70s short / 2min long | 2h |
| **V5** | **The anchor: full checker walkthrough, 51 airlines** | "I built the only size checker that knows which fare you booked." | Chaptered screen recording + voiceover | 6–8 min | 2.5h |
| **V6** | **Airlines that charge you for a carry-on — the 2026 list** | "Nine airlines will charge you to bring a bag on board." | Screen cap + table overlay | 45s + 3min | 1.5h |
| **V7** | **I measured five bags wrong on purpose** | "Everyone measures a carry-on empty. That's why you get stopped." | Hands-on, tape measure, 5 bags | 60s | 1.5h |
| **V8** | **How strict is your airline, really?** | "Ryanair will size every bag. Delta almost never will." | Needs real gate/sizer b-roll **we don't have** | 90s–2min | Parked |

**V1, V2, V5 and V6 are pure screen recordings** — zero footage risk, highest conversion.
Make those first. V3, V4 and V7 need only a phone and bags already owned. V8 is the only one
blocked on footage; script it and park it.

## 5. Distribution

| Video | YT long | Shorts | TikTok | Reels | Pinterest | On-page embed |
|---|---|---|---|---|---|---|
| V1 | — | ✅ | ✅ | ✅ | — | — |
| V2 | — | ✅ | ✅ | ✅ | Idea Pin | easyJet cabin bag policy page |
| V3 | — | ✅ | ✅ | ✅ | — | best Ryanair cabin bag |
| V4 | ✅ | ✅ | ✅ | ✅ | Idea Pin | new EU-rule page |
| V5 | ✅ anchor | — | — | — | — | **`/carry-on-size-checker/`** |
| V6 | ✅ | ✅ | ✅ | ✅ | static pin | airlines-that-charge + Frontier |
| V7 | — | ✅ | ✅ | ✅ | static pin | checker, measure section |
| V8 | ✅ | ✅ | — | — | — | how-strict page |

Embed targets were chosen by GSC impressions (3,613 / 3,269 / 1,974 / 1,883 / 766), not guesswork.

**Schema:** add `VideoObject` **into the existing `@graph`** on the checker page — do not
replace the `WebApplication` node or you lose the tool signal. For V5 also add `hasPart` `Clip`
objects per chapter and a `SeekToAction`; that's what earns key-moments treatment in SERPs and
it's the highest-leverage schema addition available to the page. Lazy-load every embed
(`youtube-nocookie` + facade thumbnail) or six raw iframes will wreck load time.

## 6. Measurement

Nothing below is measurable until the instrumentation ships. The element IDs already exist in
the source, so the hooks are exact:

```
checker_start                → first interaction on #airlineSearch
checker_airline_select       → #airlineDropdown      {airline, region, enforcement}
checker_allowance_select     → #allowanceSelect      {airline, allowance_code}
checker_result               → #checkBtn → verdict   {airline, allowance_code,
                                                      verdict:'pass'|'fail'|'borderline',
                                                      units, weight_entered}
checker_recommendation_click → #recommendButtons     {airline, target_url}
checker_affiliate_click      → outbound affiliate    {source:'checker', airline, verdict}
checker_email_optin          → new opt-in block      {airline, verdict}
checker_embed_copy           → #copyEmbed            (tracks backlink intent)
```

**The three metrics that decide whether this works:**
1. **Video → checker click-through** — sessions landing on the checker with a video UTM.
2. **Checker completion rate** — `checker_result ÷ checker_start`.
3. **Monetised action rate** — `(checker_affiliate_click + checker_email_optin) ÷ checker_result`.
   The only one tied to money. Everything else is vanity.

`verdict` is the highest-value parameter in the set: **a FAIL is a qualified buyer** who now
needs a compliant bag. Segment the recommendations and the affiliate table on it.

## 7. The 14 days

One person, phone camera, ~20 hours total.

| Day | Do | Hours |
|---|---|---|
| 1 | GA4 events on the 8 hooks. Verdict-triggered opt-in block. Repoint the broken recommendation URLs. **No filming.** | 2 |
| 2 | Create the channels. Record **V5** walkthrough, one take. | 2 |
| 3 | Edit + publish V5. Embed on the checker page, add `VideoObject` + `Clip` + `SeekToAction`. Request indexing. | 2 |
| 4 | Batch-record **V1** and **V3**. | 1.5 |
| 5 | Publish V1 and V3. Embed V3 on the Ryanair page. | 1 |
| 6 | Record + publish **V2** — the fare-aware differentiator. Embed on easyJet. | 1.5 |
| 7 | Pinterest: 3 static pins + an Idea Pin from V2. | 1 |
| 8 | Record **V4** (EU 2027). Script off verified facts only — committee passed, member states pending. Do not overstate. | 2 |
| 9 | Publish V4 as Short + 2-min. Draft the EU-rule page. | 1.5 |
| 10 | Record **V7**. | 1.5 |
| 11 | Publish V7. First data read: start vs result. Fix the drop-off step. | 1 |
| 12 | Record + publish **V6**. Embed on the 3,613-impression page and Frontier. | 2 |
| 13 | Buffer. Reshoot the weakest hook. Script V8 and park it. | 1 |
| 14 | Full read on the three metrics. Double down on the winning format, kill the rest. | 1 |

## Open decisions

1. **Paid in scope?** Recommendation: no paid in the first 14 days. The organic and on-page SEO value is the point.
2. **V8 footage** — licence stock (~£20–40/mo) or film at an airport gate?
3. **On camera or faceless?** V4 and V7 want a face. Both convert to voiceover-over-screen-cap if preferred, making the plan 100% screen recording.
4. **Deploying instrumentation + opt-in to the live checker** — a code change on the money tool. Needs sign-off.
