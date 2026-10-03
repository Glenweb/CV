# Installing without FTP — Google Tag Manager

Use this if you'd rather not touch files on the server. It does the same job as the
WordPress plugin.

## 1. Host the two files

They need to be reachable on your domain. Any of these works:

- Upload to `/wp-content/uploads/lft/` through Media Library or your host's file manager
- Drop them in a `/js/` and `/css/` folder via cPanel
- Serve them from any static host you control

You'll end up with two URLs, e.g.
`https://luggagefortravel.com/wp-content/uploads/lft/lft-checker-capture.js` and the `.css`.

## 2. One Custom HTML tag

In GTM: **Tags → New → Custom HTML**. Name it `LFT — Checker Capture`. Paste:

```html
<script>
  (function () {
    var base = 'https://luggagefortravel.com/wp-content/uploads/lft/';

    window.LFT_CHECKER_CONFIG = {
      kitFormUid: null,                  // ← your Kit form UID. null = preview mode.
      kitFallbackUrl: 'https://luggagefortravel.com/cheat-sheet/',
      privacyUrl: '/privacy-policy/',
      debug: false
    };

    var css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = base + 'lft-checker-capture.css';
    document.head.appendChild(css);

    var js = document.createElement('script');
    js.src = base + 'lft-checker-capture.js';
    js.defer = true;
    document.head.appendChild(js);
  })();
</script>
```

## 3. Fire it only on the checker

**Triggering → New → Page View → Some Page Views**, with
`Page Path` **contains** `carry-on-size-checker`.

Don't fire this on All Pages. The script is harmless elsewhere — nothing matches its
selectors — but there's no reason to ship it site-wide.

## 4. Check it, then publish

Use GTM **Preview**, load the checker, run a check. With `debug: true` the console logs every
event. Confirm the opt-in block appears below the verdict, then **Submit**.

## Events reaching GA4

The script pushes to `dataLayer` as well as calling `gtag` directly, so with GA4 configured
through GTM the events arrive on their own. If you want them as **conversions**, mark
`checker_email_optin` and `checker_affiliate_click` as key events in GA4 — those are the two
tied to money.

To build GA4 custom dimensions, register `airline`, `verdict` and `allowance_code` as
event-scoped parameters. Without that, GA4 records the events but won't let you break them
down, and the verdict split is the whole point.

## Which install should you use?

The WordPress plugin, if you can upload a zip — it keeps the config in one settings screen
and loads the files from your own origin with proper versioning. Use GTM when you don't have
plugin-install rights, or when the checker isn't served by WordPress at all.
