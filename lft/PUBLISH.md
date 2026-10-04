# Publish — the checker, the widget, the data page

Written 2026-10-04. Three uploads and two pastes. Nothing here depends on anything in
`consolidation/RUN-ORDER.md`, so this can go first.

**I cannot do any of this for you.** There is no WordPress connector in this session and
luggagefortravel.com is blocked by the container's network policy, so I have no way to write to
the site. Everything below is built, tested and packaged — the clicks are yours.

---

## Why the checker is a plugin and not a paste

`carry-on-size-checker.html` and `embed.html` are **complete HTML documents** — their own
`<!DOCTYPE>`, `<head>`, fonts, `<style>`, `<script>`, site header, footer and navigation. A
WordPress page body cannot hold a document; the block editor strips the head and mangles the
scripts. That is why they ship as a plugin that serves the files directly.

It also solves the framing problem on its own. The widget needs
`Content-Security-Policy: frame-ancestors *` and no `X-Frame-Options`, which a page body
cannot set.

The data page is different — it is a body fragment, and it pastes normally.

---

## 1. Upload the checker plugin

**File:** `lft/checker/wordpress/lft-checker-embed.zip` (45 KB)

1. Plugins → Add New → Upload Plugin → the zip → Install → Activate.
2. Open **`/carry-on-size-checker/embed/`**. The widget should render on its own — no site
   header, no footer. If it 404s: Settings → Permalinks → Save Changes, reload. That is the
   only failure mode, and that is the only fix.
3. Settings → **LFT Checker Pages** → **Run the test**.

### What the test tells you

It asks the live URL what headers it actually returns. The one that matters:

> **X-Frame-Options** — absent is what you want.

If it is present, your host is setting it in nginx or Apache and **PHP cannot remove it**. Every
embed then renders as a blank box on the other site and nobody tells you. That is the single
silent failure in this whole plan. If the test flags it, ask your host to drop the header on
`/carry-on-size-checker/embed/` before you pitch the widget to anybody.

The test request comes from your own server, so a CDN in front of the site can still add headers
only an outside visitor sees. Frame the URL from one other domain once, and you are done
worrying about it.

---

## 2. Switch the full checker over — read this first

Still in Settings → LFT Checker Pages, under **The full checker page**, tick
**Serve the full checker**.

This **shadows whatever is currently at `/carry-on-size-checker/`**. The settings page names
what is there before you tick it and links you to it. Nothing is deleted, and unticking the box
gives the old page straight back — but look at what you are about to cover first.

What the switch gets you, versus the version live now:

- The 15 corrected measurements. None of them had ever reached the live tool.
- The at-limit bug fixed. A bag at exactly the published cm limit was failing as "too large by
  0 cm" on **every airline** — it compared inches against a 1-decimal figure.
- Linear-sum limits enforced, so Finnair at 56×45×25 is now correctly rejected.
- Spirit marked ceased, with the checker hidden rather than giving advice for an airline that
  no longer flies.
- Generated enforcement tiers, so the prose cannot drift from the data.
- The embed code box, with both the auto-resize and the no-script version.

If you would rather not touch the main URL yet, leave it off. The widget works regardless, and
everything above waits.

---

## 3. The capture plugin — preview mode

**File:** `lft/checker/wordpress/lft-checker-capture.zip` (10 KB)

Upload and activate the same way. Settings → **LFT Checker**: leave the Kit form UID **empty**
and tick **Debug**. In that state the analytics run and the opt-in form validates, but no
address is sent anywhere.

Run a check with the console open, confirm the events fire and the opt-in appears below the
verdict, then untick Debug. Paste the Kit form UID in only once you have created the
`airline`, `verdict` and `allowance` custom fields in Kit, or they are dropped silently.

---

## 4. The data page

**File:** `lft/data/carry-on-enforcement-index.html`

New page at **`/carry-on-enforcement-index/`**. Paste the file into one **Custom HTML** block.
It needs `lft/content/content.css` plus the extra rules in `lft/data/data.css`.

The checker links to this page from the enforcement section, so publishing it closes that link.
It carries `schema.org/Dataset` markup and a CC BY 4.0 licence, which is what makes it a link
target rather than another article.

Then upload `lft-carry-on-allowances.csv` and `.json` to the media library and point the
download links at them.

---

## 5. Then, and only then

Add a GA4 exploration filtered to `utm_source=embed` so you can see which sites actually run
the widget. Without it you are shipping a backlink mechanism you cannot measure.

---

## Order, and what breaks if you ignore it

| # | Step | If you skip it |
|---|---|---|
| 1 | Upload the checker plugin | Nothing else here works |
| 2 | Run the framing test | You pitch a widget that renders blank |
| 3 | Switch the full checker on | The live tool keeps serving 15 wrong measurements and the at-limit bug |
| 4 | Data page | The checker's enforcement link 404s |
| 5 | Capture plugin | No cost — it is additive |

Steps 1 and 2 take about five minutes. Step 3 is the one worth reading before you click.

---

## What is verified, and how

Run from the repo root:

```
python3 lft/test-consistency.py                 # 16 — data, prose and both bundled copies agree
php    lft/checker/wordpress/lft-checker-embed/test-plugin.php   # 63 — routing, headers, shortcode
cd lft/checker/tool && for t in ceased linear embed embedbox; do node test-$t.mjs; done
                                                # 13 + 14 + 14 + 7 = 48 behavioural, in a real browser
```

`lft/checker/wordpress/build-plugin.py` rebuilds the zip: it re-bundles both documents from
`lft/checker/tool/`, lints the PHP, runs the 63 tests and refuses to ship the test file. Run it
after any edit to the tool, or the zip goes stale without saying so.
