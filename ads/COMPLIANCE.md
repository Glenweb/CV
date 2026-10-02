# Ad compliance — GMK Media portfolio

Last reviewed: 2026-10-02. Review again before any spend.

## Rule zero: never advertise a claude.ai artifact URL

Every money artifact must be mirrored onto a GMK-owned domain before a penny of paid traffic
points at it. A `claude.ai/artifact/...` destination fails on four counts:

1. **Destination policy** — Meta and Google both require the advertiser to control the
   destination. A third-party preview URL is a display/final URL mismatch on Google Search
   and a low-quality destination signal on Meta.
2. **No measurement** — you cannot install a pixel, a conversion tag, or consent management.
3. **No ownership** — the link can change or be revoked and the campaign dies mid-flight.
4. **No SEO value** — all the ranking equity accrues to someone else's domain.

Artifacts are for building and reviewing. Owned domains are for advertising.

## Portfolio triage

### 🟢 Greenlit — run paid today
| Artifact | Vertical | Notes |
|---|---|---|
| Best VPN Services UK 2026 | Software/privacy | Clean. Avoid price and speed claims in creative. |
| TopCashback vs Quidco 2026 | Cashback | Clean if no earnings figures appear. |
| Best Web Hosting UK 2026 | Software | Clean. |
| Best Home Security Systems UK 2026 | Consumer tech | Avoid fear-based creative (burglary imagery trips Meta's shocking-content rules). |
| WebPromote | Own agency service | Cleanest in the portfolio. First-party, no disclosure needed. |
| LFT / luggagefortravel.com | Travel content | Clean organically. See the airline-trademark note below for paid. |

### 🔴 Closed to paid social and paid search
| Artifact group | Blocking policy |
|---|---|
| Pineal Guard, Red Boost, Alpha Tonic, Prostadine, Brain Song, Sacred Sound Healing, Mystery School Code, Shifting Vibrations, His Secret Obsession, Wellness Library | **Meta** Personal Health & Appearance + unrealistic outcomes. **Google** Healthcare & Medicines; several ingredients sit on the unapproved-substances list. Red Boost, Alpha Tonic and Prostadine additionally trip sexual-wellness restrictions. |
| Profit Maximiser, US Sports Bonus Calculator, US Sports Bonus Market | **Google** gambling certification requires a UKGC licence for UK targeting. **Meta** requires written gambling permission. Affiliates without a licence do not get certified. |
| GMK Signal Desk — Crypto Buy Radar | **Google** financial products certification (FCA authorisation for UK). **Meta** crypto written permission. "Buy signals" reads as regulated investment advice. |

**Correct channel for the red group:** native advertising (Taboola, Outbrain, MGID, RevContent)
with a compliant advertorial bridge page, plus organic video. Not paid social. Attempting
paid social here risks the Business Manager, not just the ad.

## Creative rules applied to these three ads

| Rule | How the creative complies |
|---|---|
| No unverifiable test claims | "We tested 18 VPNs over 90 days" and "200 purchases over 12 months" appear on the landing pages but **not** in the videos. If those tests did not happen as described, fix the pages — they are an ASA and CMA exposure independent of any ad. |
| No prices on screen | Prices move weekly; a stale on-screen price is a misleading-pricing complaint. Prices stay on the landing page where they can be updated. |
| No earnings or savings figures | "Earn £300/year" is a financial claim requiring typicality evidence. Absent by design. |
| No specific results claims | WebPromote's "#6 → #1 in three weeks" was cut from the creative. It belongs on the landing page as a named, dated case study with context. |
| Affiliate disclosure in-creative | Both affiliate ads carry a disclosure card in the final frame, not just on the landing page. Exceeds the minimum and reduces review friction. |
| No fake UI | No mock notifications, fake comment threads, fake system dialogs or simulated platform chrome. Meta rejects all of these. |
| No shocking or fear-based imagery | No surveillance, break-in or threat imagery. |
| No brand logos | Third-party brands appear as plain text only, never as logos or liveries. Logos are a trademark exposure separate from ad policy. |

## Airline trademark note (LFT)

Organic and paid are genuinely different here:

- **Organic:** naming airlines in titles, on-screen text and captions is ordinary descriptive
  use and standard editorial practice. No change needed.
- **Paid:** Google permits trademarks in ad text for informational sites whose landing page
  genuinely informs about that product — **but that permission is scoped to US, CA, UK, IE, AU
  and NZ targeting.** EU/EFTA targeting is materially stricter, which is exactly where the
  strongest hooks (Ryanair, easyJet, Wizz) live. Expect disapprovals.
- **Always:** never use an airline logo, livery or branded gate sizer in any creative, paid or
  organic.
- **If boosting:** cut a generic variant ("your airline's limit") with no airline named.

## Pre-launch checklist

- [ ] Landing page lives on a GMK-owned domain, not claude.ai
- [ ] Affiliate placeholder links replaced with live tracking links
- [ ] Affiliate disclosure visible above the fold on the landing page
- [ ] Prices and product facts re-verified against the provider's own site, today
- [ ] Any test or methodology claim on the page is one you can evidence
- [ ] Pixel/tag firing and a conversion event defined
- [ ] Consent banner live (PECR/UK GDPR) before any tracking
- [ ] UTM parameters on every destination URL
