=== LFT Checker Capture ===
Requires at least: 6.0
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPL-2.0-or-later

Analytics and result-aware email capture for the carry-on size checker.

== Description ==

Adds ten analytics events and a verdict-aware email opt-in to the carry-on size checker.
Loads only on the checker page. Ships in preview mode: analytics run immediately and the
opt-in validates, but no address is sent anywhere until a Kit form UID is saved.

The checker result is never gated. The opt-in is injected below the verdict after an answer
has been shown, so it cannot shift layout on load and is not an intrusive interstitial.

== Installation ==

1. Plugins > Add New > Upload Plugin, choose the zip, Install, Activate.
2. Settings > LFT Checker.
3. Leave the Kit form UID empty for now, tick Debug, Save.
4. Open the checker, run a check, open the browser console and confirm the events fire and
   the opt-in block appears below the verdict.
5. Paste in the Kit form UID and untick Debug to go live.

== Before going live ==

* Create custom fields `airline`, `verdict` and `allowance` in Kit, or they are dropped.
* Turn double opt-in on in Kit.

== Changelog ==

= 1.0.0 =
* First release.
