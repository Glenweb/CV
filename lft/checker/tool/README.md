# LFT checker — the ceased-airline fix

**Problem:** the live carry-on size checker lists **Spirit Airlines** with
`enforcement: "extreme"` and publishes a confident pass/fail verdict for an airline that
has not flown since **2 May 2026**. A user can pick Spirit today and be told their bag is
fine for a flight that does not exist.

**Fix:** a reusable `ceased` flag on the airline record. Spirit is the first to carry it;
any future shutdown needs one line, not a code change.

## What it does

| Where | Behaviour |
|---|---|
| Airline dropdown | Red **CEASED** tag beside the name — flagged *before* anyone clicks |
| Enforcement badge | Reads **Ceased operations** instead of "Extremely strict" |
| Bag checker | **Hidden.** No dimensions can be entered, so no verdict can be produced |
| Airline card | Historical limits still shown (that is the search intent), labelled "For reference" |
| Red banner | Names the shutdown date, says there is no flight to check against, links to `/spirit-airlines-shutdown/` |
| Recommendations | Shutdown page, then Frontier as the closest match, then underseat bags |
| Fee pill | "Ceased operations — no longer flying" |
| Prose | The Tier 1 enforcement list now reads "Spirit Airlines belonged to this group until it ceased operations on 2 May 2026" |

The two Spirit advisory notes were rewritten into the past tense. No live airline's
behaviour changes — the flag is opt-in per record.

## Adding the next one

```js
{name:"Some Airline", region:"...", enforcement:"...",
 feeText:"Ceased operations — no longer flying",
 ceased:{on:"14 March 2027", url:"/some-airline-shutdown/"},
 ...}
```

That is the whole change. `isCeased()` does the rest.

## Verification

`node test-ceased.mjs` — 13 assertions, all passing, no page errors. It covers both
directions: that Spirit cannot produce a verdict, **and** that Ryanair still can.

```
13 passed, 0 failed, 0 page errors
```

## Before you deploy — one check that matters

`carry-on-size-checker.html` here was pulled from the Drive file of that name
(modified 12 June 2026, 51 airlines) — the newest of **three** checker copies in Drive.
The others are `carry-on-size-checker-FINAL.html` (21 May) and `index.html` (18 April).

**Confirm this matches what is live at `/carry-on-size-checker/` before replacing it.**
View source on the live page and compare the `<title>`; this copy reads
"Carry-On Size Checker 2026 — Free Tool for 51 Airlines". If the live page differs, do not
paste this file — tell me and I will apply the same nine patches to the correct source.

If it matches, replace the page body with this file's contents. The capture plugin
(`lft/checker/wordpress/`) is independent and needs no change.

## Still open

Spirit's product pages already redirect — `luggagefortravel_rankmath-redirects-phase2-spirit.csv`
in Drive maps `spirit-airlines-carry-on-size/`, `best-carry-on-luggage-spirit/` and
`best-carry-on-luggage-spirit-airlines/` to `/spirit-airlines-shutdown/`, all 301 and
active since May 2026. The tool was the last place still treating Spirit as live.
