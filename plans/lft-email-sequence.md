# LFT welcome sequence — build spec

Seven emails, fourteen days. Every commercial link points at an LFT bridge page, never at
Amazon. Written to be built in Kit as-is.

**Entry:** any opt-in. Email 1 varies by magnet; emails 2–7 are shared.
**Exit:** tag `seq:welcome-complete` on email 7, then the regular broadcast cadence.
**Suppression:** anyone who grabs a second magnet mid-sequence gets a one-off delivery email,
not a second run of this.

---

## The architecture every commercial email obeys

```
  Kit email  ──►  LFT bridge page  ──►  Amazon / Awin / CJ
  no affiliate    all affiliate         merchant
  link, ever      links live here
                  display revenue here
                  pixel fires here
```

**Each email's job is a click to an LFT page. Never a sale.** Three Amazon rules bite even
with no links present: no Amazon prices in email (they must be API-sourced and time-stamped,
so an email price is stale on send — say "around £40" or nothing), no Amazon product images
in email, and disclosure wherever the link actually is, which is the page.

## Link convention

```
https://luggagefortravel.com/<bridge-page>/
  ?utm_source=kit
  &utm_medium=email
  &utm_campaign=welcome
  &utm_content=e4_bags_ryanair     ← email number + purpose + segment
```

`checker_affiliate_click` already fires on the page with airline and verdict attached, so the
chain reads end to end: sent → opened → clicked → landed → clicked out.

---

## Email 1 · Day 0 · Deliver the thing

Sent within seconds. Your highest-open email ever and the one that sets inbox placement.
**One job. No selling.**

> **Subject:** Your carry-on size sheet (all 51 airlines)
> **Preview:** Screenshot it before you fly.

> Here it is — every airline's cabin and personal-item limits on one page:
>
> **[Open the size sheet →]**
>
> Screenshot it now. It works at the gate with no signal.
>
> One thing most people get wrong: airlines measure with the wheels and handles included.
> Measure yours the same way or the sizer will disagree with you.
>
> Over the next fortnight I'll send you the five things that actually stop bags at the gate.
> If that's not what you want, the unsubscribe link below works in one click.
>
> — Glen, Luggage For Travel

Variant for the Ryanair/easyJet/Wizz magnets: swap the first line and link, keep the rest.

**Tags:** `magnet:<name>`, `source:<origin>`, plus `airline:<x>` if the capture knew it.

---

## Email 2 · Day 1 · The quick win

Trust before anything commercial.

> **Subject:** The 2cm that costs £75
> **Preview:** Almost everyone measures their bag wrong.

> Most people measure a carry-on empty, flat, without the wheels. Airlines don't.
>
> They measure the widest point of the packed bag, wheels and handle included. That's
> usually 2–4cm more than the number on the manufacturer's label — which is exactly the
> margin that gets a bag pulled at the gate.
>
> **[How to measure the way the airline does →]**
>
> Takes ninety seconds and it's the single most useful thing in this whole sequence.

**Links to:** the measuring guide section on the checker page. No affiliate links.

---

## Email 3 · Day 3 · Segment

The highest-value email in the sequence. Buttons apply tags on click — no reply needed.

> **Subject:** Which airline do you fly most?
> **Preview:** So I stop sending you Frontier rules you'll never use.

> Baggage rules are completely different between carriers, and most of what I could send you
> won't apply to you. Tap the one you fly most and I'll keep it relevant:
>
> **[Ryanair] [easyJet] [Wizz Air] [British Airways] [A US airline] [Something else]**
>
> You can tap more than one. That's it — nothing else to do.

**Tags:** `airline:*` by link click. Anyone who doesn't tap falls through to the generic
branch on email 4.

---

## Email 4 · Day 5 · First monetisation

The first email that points at a money page. Dynamic by `airline:*`, generic fallback.

> **Subject:** Bags that actually clear the Ryanair sizer
> **Preview:** Measured, not guessed.

> Ryanair's free allowance is 40 × 30 × 20cm. Loads of bags sold as "Ryanair cabin bags"
> are bigger than that — the label says one thing, the packed bag measures another.
>
> These are the ones we've measured packed, with the limit shown next to each so you can
> check the maths yourself:
>
> **[Bags that fit Ryanair's 40×30×20 →]**
>
> If you've got priority, the limit is 55 × 40 × 20 at 10kg and the list is different —
> it's on the same page, further down.

**Links to:** `/airline-baggage-rules/best-ryanair-cabin-bag/`
**Tags on click:** `clicked:money-page`, `cat:cabin-bag`

---

## Email 5 · Day 8 · The fee maths

Makes the cost concrete, then offers the cheaper path.

> **Subject:** What a gate fee actually costs you
> **Preview:** It's not the £75. It's the £75 every time.

> A gate bag fee is somewhere between £45 and £95 depending on the airline and how late
> they catch you. Pay it twice and you've spent more than a bag that would have fitted.
>
> The part people miss: it's charged per flight, not per trip. A return is two.
>
> **[What every airline charges, 2026 →]**
>
> Worth five minutes before you book anything this year.

**Links to:** `/airline-baggage-fees/`. Non-Amazon affiliate slots (airport parking, travel
insurance, eSIM) can live on that page and, unlike Amazon, could also go directly in the
email later — check each programme's own email policy first.

---

## Email 6 · Day 11 · The tool

Drives to the checker, which is where capture and intent both peak.

> **Subject:** Settle it in thirty seconds
> **Preview:** Your bag, your airline, your fare.

> Here's the thing no size chart tells you: your airline doesn't have *a* carry-on size. It
> has four, and which one applies depends on the fare you booked.
>
> Ryanair's free allowance is 40 × 30 × 20. With priority it's 55 × 40 × 20. easyJet's
> under-seat is 45 × 36 × 20; the large cabin bag is 56 × 45 × 25. Same airline, different
> answer.
>
> Put your bag's measurements in and it'll tell you which fares it clears:
>
> **[Check my bag against 51 airlines →]**

**Links to:** `/carry-on-size-checker/`

---

## Email 7 · Day 14 · Set the relationship

> **Subject:** What happens now
> **Preview:** Roughly one email a week, and an alert if your airline changes the rules.

> That's the useful stuff out of the way. From here you'll get about one email a week —
> what's changed, what's worth buying, and the occasional thing that saves you money at the
> airport.
>
> One more worth turning on: **[alert me when my airline changes its baggage rules →]**.
> Carriers change limits with almost no notice, and finding out at the gate is the expensive
> way.
>
> Big one coming: from 2027 the EU is set to require a free personal item of 40 × 30 × 15cm
> on every flight. That rewrites every airline's fare structure at once. I'll send the
> details as they firm up.
>
> Reply any time — it comes to me.

**Tags:** `seq:welcome-complete`

---

## Build order in Kit

1. Create the tag taxonomy first — `airline:*`, `trip:*`, `cat:*`, `magnet:*`, `source:*`,
   `seq:*`, `region:*`. Retrofitting tags onto an existing list is miserable.
2. Create the three custom fields the capture script writes: `airline`, `verdict`, `allowance`.
3. Build emails 2–7 as one sequence. Build email 1 per magnet.
4. Wire link-click tagging on **every** airline and category link, not just email 3. It
   compounds for free.
5. Turn on double opt-in before the first subscriber.
6. Set the cold rule: no opens in 180 days → `cold:180d` → one re-permission email → remove.

## What it needs that doesn't exist yet

| Needed | Status |
|---|---|
| The 51-airline size sheet (the magnet itself) | Not built |
| Bridge page: bags that fit Ryanair, with measured dimensions and `last_verified` | Page exists; needs the measured-dimensions treatment |
| `/airline-baggage-fees/` current for 2026 | Exists; verify before email 5 goes out |
| Alerts mechanism (email 7 offers it) | Not built — don't offer it until it exists |
| GMK Media Ltd postal address for the footer | Legally required, still outstanding |

**Don't send email 7 until the alerts mechanism actually exists.** Offering something you
can't deliver on the last email of the welcome is the worst possible first impression.
