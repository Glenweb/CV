=== LFT Carry-On Checker ===
Requires at least: 6.0
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPL-2.0-or-later

Serves the carry-on size checker as a standalone document — the embeddable widget, and
optionally the full tool page.

== Why a plugin ==

Both files are complete HTML documents with their own `<head>`, styles, scripts, header,
footer and navigation. Neither can be pasted into a WordPress page body. This plugin serves
them directly, which also lets each one send the headers it needs.

== What it serves ==

**The embeddable widget** at `/carry-on-size-checker/embed/` — on by default:

* `X-Robots-Tag: noindex, follow` so it cannot compete with the main checker in the index,
  while links out of it still count.
* `Content-Security-Policy: frame-ancestors *` so any site can frame it.
* Any PHP-set `X-Frame-Options` removed.
* Canonical back to `/carry-on-size-checker/`. The attribution link lives inside the widget,
  so a site that embeds it cannot drop the credit by accident.

**The full checker page** at `/carry-on-size-checker/` — off by default, because turning it on
shadows whatever is already at that URL. Indexable, left on your site's own framing policy.
The settings page tells you what currently occupies the path before you switch it on, and
unticking the box gives that page straight back. Nothing is deleted either way.

Both responses carry an ETag and `Cache-Control: public, max-age=3600`, so repeat loads are a 304.

== Installation ==

1. Plugins > Add New > Upload Plugin, choose the zip, Install, Activate.
2. Open `/carry-on-size-checker/embed/`. The widget should render on its own.
   If it 404s: Settings > Permalinks > Save Changes, then reload.
3. Settings > LFT Checker Pages > Run the test.
4. Only once you have read the warning: tick "Serve the full checker" to take over
   `/carry-on-size-checker/`.

== The framing test ==

A host that sends `X-Frame-Options: DENY` from nginx or Apache breaks every embed silently —
the iframe renders blank on the other site and nobody tells you. PHP cannot remove a header set
at that level, so the settings page asks each live URL what it really returns and says whether
anything is blocking it.

Those requests come from your own server. A CDN or reverse proxy in front of the site can add
headers only an outside visitor sees, so confirm once by framing the widget URL from a different
domain before pitching the embed to anyone.

== Shortcode ==

`[lft_checker_embed]` embeds the widget on this site, with the auto-height script and the origin
pinned to this domain. Attributes: `height` (default 900), `title`.

== Updating ==

The two documents are the bundled `embed.html` and `checker.html`. To ship a new version, replace
the files and bump the plugin version — the ETag is derived from each file's size and
modification time, so caches turn over on their own.

== Changelog ==

= 1.0.0 =
* First release.
