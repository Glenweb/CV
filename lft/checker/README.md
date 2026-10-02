# LFT checker — analytics + email capture

Ship this to `/carry-on-size-checker/` today. It's dependency-free, it doesn't gate the
result, and it degrades to doing nothing rather than breaking the tool.

## Install (15 minutes)

1. Upload `lft-checker-capture.js` and `lft-checker-capture.css` (e.g. to `/js/` and `/css/`).
2. In the page `<head>`:
   ```html
   <link rel="stylesheet" href="/css/lft-checker-capture.css">
   ```
3. Before `</body>`:
   ```html
   <script>
     window.LFT_CHECKER_CONFIG = {
       kitFormUid: null,          // ← your Kit form UID. null = preview mode, no network call.
       kitFallbackUrl: 'https://luggagefortravel.com/cheat-sheet/',
       privacyUrl: '/privacy-policy/',
       debug: false               // true logs every event to the console
     };
   </script>
   <script src="/js/lft-checker-capture.js" defer></script>
   ```
4. Load the page, run a check, open the console and confirm the opt-in block appears below
   the verdict. In preview mode it validates and reports without sending anything.
5. Get the form UID from Kit (it's the number in your embed code / form URL), put it in
   `kitFormUid`, and you're live.

**Deploy it in preview mode first.** You get the analytics immediately and can style and
word the block before a single address is captured.

## Verify the selectors

The script targets the IDs found in the tool source: `#airlineSearch`, `#airlineDropdown`,
`#allowanceSelect`, `#checkBtn`, `#verdict`, `#recommendButtons`, `#copyEmbed`. **These were
read from the Drive copy of the tool, not from the live page.** If the live DOM differs,
override them rather than editing the script:

```js
window.LFT_CHECKER_CONFIG = {
  sel: { verdict: '#result-panel', checkBtn: '.check-button' }
};
```

A selector that doesn't match disables that one hook silently. Set `debug: true` and watch
the console to see which fired.

## Events emitted

Sent to `gtag` and `dataLayer` if either exists, and always queued on
`window.LFT_CHECKER.events` so you can inspect them with no analytics installed at all.

| Event | Fires when | Parameters |
|---|---|---|
| `checker_start` | First focus on the airline field, once per load | — |
| `checker_airline_select` | An airline is picked | `airline`, `region`, `enforcement` |
| `checker_allowance_select` | The fare/allowance changes | `airline`, `allowance_code` |
| `checker_result` | **The verdict renders** (not on button click) | `airline`, `allowance_code`, `verdict`, `units`, `weight_entered` |
| `checker_optin_view` | The opt-in block is shown | `airline`, `verdict` |
| `checker_email_optin` | A subscription succeeds | `airline`, `verdict` |
| `checker_optin_error` | Kit rejected the POST | `airline`, `verdict`, `message` |
| `checker_recommendation_click` | A post-result recommendation is clicked | `airline`, `target_url` |
| `checker_affiliate_click` | Any affiliate link anywhere on the page | `source`, `airline`, `verdict`, `target_url` |
| `checker_embed_copy` | The embed code is copied (backlink intent) | `airline` |

`checker_result` fires on the verdict rendering rather than the button click, so a
validation failure never counts as a result and your completion rate stays honest.

**`verdict` is the parameter that matters.** A `fail` is a qualified buyer who now needs a
compliant bag. Build the audience on it.

## Why the result is never gated

Gating would (a) destroy the tool's usefulness, (b) match the "dismiss before accessing
content" pattern Google names in its intrusive-interstitial guidance, and (c) kill the
embeds and links the tool earns. The block appears **after** the answer, offers something
more durable than the answer, and is injected below existing content so it cannot cause
layout shift on load.

## Consent

The checkbox is unticked and required — submission is refused without it, which is what UK
GDPR means by freely given. The copy names GMK Media Ltd and what you'll send, which is what
"specific and informed" means. Turn **double opt-in on in Kit**: the confirmation click is
the cleanest proof of consent you'll have, and it protects a new sending domain.

## Tags written to Kit

`source:checker` plus custom fields `airline`, `verdict`, `allowance`. Create those three
custom fields in Kit before going live or they'll be dropped silently.

## Tests

```bash
node lft/checker/test/run.mjs
```

Drives a mock of the checker DOM in Chromium and asserts all 12 behaviours: event firing,
parameter capture, verdict parsing, block injection, both validation refusals, and the
affiliate and embed hooks. Run it after any selector change.
