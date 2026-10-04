# The two link assets

Built 4 Oct 2026. Both are generated, not hand-written — regenerate, don't edit.

| Asset | Source | Generator | Output |
|---|---|---|---|
| Chromeless embed | `lft/checker/tool/carry-on-size-checker.html` | `build-embed.py` | `embed.html` |
| Data page + dataset | `lft/fare-watch/airlines.json` | `lft/data/build.py` | `carry-on-enforcement-index.html`, `.csv`, `.json` |

---

## 1. The embed — `/carry-on-size-checker/embed/`

Derived from the patched tool by script, so it can never drift from it. 82 KB vs 96 KB:
site header, footer, intro, the measuring guide, the FAQ, the enforcement prose and the
nested embed section are all stripped. The tool is all that remains.

**What was added:**
- `noindex, follow` — **critical.** Without it the embed duplicates the canonical checker
  and competes with it. The canonical tag still points at `/carry-on-size-checker/`.
- `<base target="_blank">` — links break out of the frame instead of navigating inside it.
- **Attribution the host cannot remove**, rendered as part of the widget: *"Carry-on size
  checker by Luggage for Travel — 51 airlines, fare-aware."* The `<a href>` is a real link
  with `?utm_source=embed`, so embeds are attributable in GA4.
- **iframe auto-height.** The widget `postMessage`s its height to the parent on every
  change (ResizeObserver, load, click, 1s interval). This replaces the old fixed
  `height="700"`, which clipped.
- Both JSON-LD blocks dropped — structured data belongs on the canonical page only.

**Verified:** `node lft/checker/tool/test-embed.mjs` — 14 assertions inside a real host
iframe, all passing, no page errors. It confirms the chrome is gone, the tool still returns
verdicts, the Spirit ceased-airline handling survives the strip, the attribution renders
with a live link, and **the host actually resized from 300px to 1,515px off the posted
messages.**

### The snippet to give people

```html
<iframe id="lft-checker"
        src="https://luggagefortravel.com/carry-on-size-checker/embed/"
        width="100%" height="900" loading="lazy"
        style="border:1px solid #e2e8f0;border-radius:8px"
        title="Carry-on size checker"></iframe>
<script>
addEventListener("message", function (e) {
  if (e.origin !== "https://luggagefortravel.com") return;
  if (e.data && e.data.type === "lft-checker-height") {
    document.getElementById("lft-checker").style.height = e.data.height + "px";
  }
});
</script>
```

The resize script is optional — without it the iframe just stays 900px. **Offer both**:
people pasting into a locked-down CMS cannot run script.

### Before pitching it
1. Publish at `/carry-on-size-checker/embed/`.
2. Confirm your host allows framing. `X-Frame-Options: DENY` or a restrictive
   `frame-ancestors` CSP will silently break every embed. It needs to permit cross-origin
   framing **for this path**.
3. Update the "Copy embed code" box on the main checker to ship this snippet and the
   `/embed/` URL — it currently frames the full page.
4. Add a GA4 view on `?utm_source=embed` so you can see which sites are actually using it.

---

## 2. The data page — `/carry-on-enforcement-index/`

**51 airlines, 112 allowances, 5 enforcement bands.** The novel claim is the pairing: every
airline publishes a size, almost none publishes how hard it enforces one.

Generated figures, all cross-checked against the dataset: **50 operating airlines, 11 in
the three strictest bands, 38 visual-check, 1 rarely sizes.** Spirit is excluded from the
live tiers and placed in an archive section instead.

Includes `schema.org/Dataset` markup with both download distributions, a CC BY 4.0 licence
with attribution required, a copy-paste citation block, and CSV + JSON downloads. The
licence *is* the link mechanism: people who use data cite data.

**Verified:** 24 cm triples on the page all exist in the dataset, every inch conversion is
correct, JSON-LD parses, and all 112 CSV rows match source values.

### Two things to resolve before this goes to a journalist

**1. The provenance gap — this is the blocker.** `source` is populated on **2 of 51**
records and `lastVerified` on **2 of 51**. The page states this plainly in the methodology
rather than hiding it, which is the right call for publishing but a weak position for
pitching: the first question a travel desk asks is "where did you get this and when."

Fill those fields before any PR push. It is 51 airline pages and a date — a day of agent
work, and it converts the page from "a blog's table" into something citable.

**2. ~~The tool's prose contradicts the dataset.~~ FIXED 4 Oct 2026.**

The tool's Tier 1 list was hand-written and read *"Ryanair, Wizz Air, easyJet (small cabin
bag), Frontier, Allegiant, AirAsia, Scoot, Jetstar, IndiGo"*. **Jetstar is not in the
dataset at all**, and Aer Lingus, Vueling and flydubai — which are in the strict bands —
were missing.

The whole section is now generated from the tool's own `AIRLINES` array by
`lft/checker/tool/build-tiers.py`. It states five tiers with counts, flags Spirit inline as
ceased, and reports **11 of 50 operating airlines in the three strictest bands** — the same
figure this data page states, because both derive from the same source. It also now links
to `/carry-on-enforcement-index/`, giving the data page an internal link from an indexed
page.

**`lft/test-consistency.py` is the real fix.** Three defects this week came from one cause:
copy written by hand while the data moved underneath it — Spirit live in the checker,
Jetstar invented in the prose, and a ceased flag my own first generator read off the wrong
airline. A count stated in prose is a claim, and claims need a test. It asserts the tool's
AIRLINES array, the tool's prose, `airlines.json` and this data page all agree — 12
assertions, and it was validated by injecting a fake "Jetstar" and confirming it failed.

---

## Regenerating

```sh
python3 lft/checker/tool/build-embed.py    # after any change to the tool
python3 lft/data/build.py                  # after any change to airlines.json
node    lft/checker/tool/test-embed.mjs    # 14 assertions
node    lft/checker/tool/test-ceased.mjs   # 13 assertions
python3 lft/checker/tool/build-tiers.py    # after any change to AIRLINES
python3 lft/test-consistency.py            # 12 assertions across all four files
```

Both generators assert on their inputs and fail loudly if the source HTML shifts under
them, rather than silently producing a broken page.
