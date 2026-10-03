# Keeping fare-aware data current

The wedge is that the checker knows the limit **for the fare you booked**. The moat is
therefore the data, which means data decay is the one thing that can kill the product: being
wrong costs the user £50–95 at the gate, and that trust doesn't come back.

So the requirement isn't "audit it quarterly". It's **know within a day that something moved**.

## The system: detect daily, verify by hand, publish deliberately

Three layers. Each catches what the one above it misses.

### Layer 1 — automated daily detection (this folder)

A watcher fetches each airline's own baggage page and asks one question per allowance: *is
the dimension set we publish still printed on their page?* It never writes to the tool. A
change becomes a review item with the before, the after and the source link.

Comparing as a sorted set rather than a sequence matters: airlines print the same three
numbers in different orders, and matching on order alone produces constant false alarms.

```bash
node lft/fare-watch/watch.mjs --tier1        # the six that change most, daily
node lft/fare-watch/watch.mjs                # everything with a source URL, weekly
node lft/fare-watch/watch.mjs --only ryanair # one carrier
```

Exit 0 means nothing to review. Exit 1 means drift or staleness. The GitHub Action at
`.github/workflows/fare-watch.yml` runs it daily and opens (or comments on) one
`fare-watch` issue when there's something to look at. **A clean run is silent** — otherwise
the alert becomes noise and gets ignored, which is the usual way these systems die.

### Layer 2 — human verification queue

A flagged change takes about two minutes: open the source, confirm the new number, update
the checker, set `lastVerified`. Never auto-publish a scraped value into the tool. A parser
that misreads a marketing page and silently ships a wrong limit is worse than no watcher,
because it breaks the one thing the product is trusted for.

### Layer 3 — the field signal

The people at the gate find out before any scraper does.

- A **"this was wrong at the gate"** link under the verdict. One click, logs
  `airline` + `allowance` + `verdict`. Three reports on one airline in a week outranks
  anything the watcher says.
- The **alerts list** replies. People who've asked to be told about rule changes are the ones
  who notice them.
- A **weekly glance at the fare-watch issue** even when it's quiet.

## The SLA, and showing it

`airlines.json` carries `slaDays`: tier 1 verified within 7 days, everything else within 30.
`tier1Keys` is the six carriers that both change most and carry most of LFT's demand:
Ryanair, easyJet, Wizz Air, Frontier, Spirit, British Airways.

**Show `last_verified` per airline in the checker UI.** Nobody else does it, it's a trust
asset rather than an admission, and it forces the discipline — a stale date is visible to
you and to the user at the same moment.

## The data file

`airlines.json` is **generated from the checker's own source**, so the watcher and the tool
can't drift apart:

```bash
node lft/fare-watch/import-from-checker.mjs path/to/carry-on-size-checker.html > lft/fare-watch/airlines.json
```

Currently 51 airlines, 112 allowances (bundled personal items counted separately, because
they change independently of the fare they're attached to). Re-importing preserves the
`source` and `lastVerified` fields you've added by hand.

**What's still needed: the `source` URL per airline.** None are populated yet. The watcher
only checks airlines that have one, so this is the gating task — about an hour to paste in
51 official baggage-page URLs, and nothing automated runs until it's done.

## Dead carriers are a trust problem too

The watcher checks whether a published dimension still matches the airline's page. It does
not check whether the airline still exists.

**Spirit Airlines ceased operations on 2 May 2026** (verified 3 Oct 2026 against NPR, CNN,
CNBC and Flightradar24) and is **still live in the checker**, returning carry-on verdicts
for an airline that does not fly. It is flagged `status: ceased_operations` in
`airlines.json`; removing or relabelling it in the tool is a product decision.

Add a liveness check to the quarterly audit: for each carrier, is it still operating? It is
a slower-moving question than dimensions, but getting it wrong is worse — a wrong dimension
costs someone £75, a dead airline makes the whole tool look unmaintained.

## What this does not cover

- **JS-rendered pages.** If an airline renders its limits client-side, the fetch sees
  nothing and the watcher reports "no dimensions found" rather than pretending it passed.
  Those carriers need Playwright or a manual check; the report tells you which.
- **Prose-only changes.** A carrier tightening *enforcement* without changing a number won't
  trip the watcher. That's what layer 3 is for.
- **Fares appearing or disappearing.** A new fare tier is a `NEW` dimension set on the page
  that we don't store — visible in the "page shows" line of a finding, but a human has to
  notice it's a new product rather than a reformatting.

## Tests

```bash
node lft/fare-watch/watch.mjs --offline lft/fare-watch/test/fixtures --only ryanair,easyjet
```

Fixtures simulate Ryanair changing its free bag from 40×30×20 to 40×30×15 while easyJet
stays put. Expected: two Ryanair findings (the standalone allowance and the personal item
bundled into the priority fare), nothing for easyJet, exit 1.
