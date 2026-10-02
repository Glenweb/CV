/*! LFT Carry-On Size Checker — analytics + email capture
 *  Drop-in, zero dependencies, no build step.
 *
 *  Install: upload this file, then before </body> on /carry-on-size-checker/:
 *      <script src="/js/lft-checker-capture.js" defer></script>
 *
 *  Designed to be safe to ship before anything else is ready:
 *   - If GA4/GTM is absent, events queue to window.LFT_CHECKER.events and nothing breaks.
 *   - If a selector doesn't match, that one hook is skipped silently. The tool keeps working.
 *   - The opt-in block is injected AFTER a result renders, below the verdict, so it can
 *     never push existing content down on load (no CLS) and is not an interstitial.
 *   - The result itself is never gated.
 *
 *  Set window.LFT_CHECKER_CONFIG before this script to override anything below.
 */
(function () {
  'use strict';

  var DEFAULTS = {
    /* --- Kit (ConvertKit) ---------------------------------------------- */
    // The form UID from your Kit embed code, e.g. "8123456". Leave null and the
    // block renders in preview mode (no network call) so you can style it first.
    kitFormUid: null,
    // Kit's own embed posts here; no API key is exposed.
    kitEndpoint: 'https://app.kit.com/forms/{uid}/subscriptions',
    // Fallback if the POST fails — your hosted Kit landing page.
    kitFallbackUrl: 'https://luggagefortravel.com/cheat-sheet/',

    /* --- Selectors (verify these against the live DOM) ------------------ */
    sel: {
      airlineSearch:   '#airlineSearch',
      airlineDropdown: '#airlineDropdown',
      allowanceSelect: '#allowanceSelect',
      checkBtn:        '#checkBtn',
      verdict:         '#verdict',
      recommend:       '#recommendButtons',
      copyEmbed:       '#copyEmbed'
    },

    /* --- Behaviour ------------------------------------------------------ */
    privacyUrl: '/privacy-policy/',
    company: 'Luggage For Travel is operated by GMK Media Ltd.',
    debug: false
  };

  var CFG = merge(DEFAULTS, window.LFT_CHECKER_CONFIG || {});
  var state = { airline: null, allowance: null, verdict: null, started: false, optedIn: false };
  var API = { events: [], state: state, config: CFG };
  window.LFT_CHECKER = API;

  /* ------------------------------------------------------------------ *
   * Analytics. Works with GA4 (gtag), GTM (dataLayer), both, or neither.
   * ------------------------------------------------------------------ */
  function track(name, params) {
    var payload = merge({ tool: 'carry_on_size_checker' }, params || {});
    API.events.push({ name: name, params: payload, at: Date.now() });

    if (typeof window.gtag === 'function') {
      window.gtag('event', name, payload);
    }
    if (Array.isArray(window.dataLayer)) {
      window.dataLayer.push(merge({ event: name }, payload));
    }
    if (CFG.debug) console.log('[LFT]', name, payload);
  }
  API.track = track;

  /* ------------------------------------------------------------------ *
   * Wiring
   * ------------------------------------------------------------------ */
  function boot() {
    var $ = function (s) { return s ? document.querySelector(s) : null; };

    // 1. checker_start — first interaction with the airline field, once per session.
    on($(CFG.sel.airlineSearch), 'focus', function () {
      if (state.started) return;
      state.started = true;
      track('checker_start', {});
    }, true);

    // 2. checker_airline_select
    on($(CFG.sel.airlineDropdown), 'click', function (e) {
      var item = e.target.closest('[data-airline], li, button, a');
      if (!item) return;
      state.airline = (item.dataset && item.dataset.airline) || text(item);
      track('checker_airline_select', {
        airline: state.airline,
        region: (item.dataset && item.dataset.region) || null,
        enforcement: (item.dataset && item.dataset.enforcement) || null
      });
    });

    // 3. checker_allowance_select
    on($(CFG.sel.allowanceSelect), 'change', function (e) {
      state.allowance = e.target.value;
      track('checker_allowance_select', { airline: state.airline, allowance_code: state.allowance });
    });

    // 4. checker_result — fires when the verdict actually renders, not on button click,
    //    so a validation failure is never counted as a result.
    var verdictEl = $(CFG.sel.verdict);
    if (verdictEl && 'MutationObserver' in window) {
      new MutationObserver(debounce(function () {
        var v = readVerdict(verdictEl);
        if (!v || v === state.verdict) return;
        state.verdict = v;
        track('checker_result', {
          airline: state.airline,
          allowance_code: state.allowance,
          verdict: v,
          units: readUnits(),
          weight_entered: hasWeight()
        });
        injectOptIn(verdictEl, v);
      }, 120)).observe(verdictEl, { childList: true, subtree: true, characterData: true });
    }

    // 5. checker_recommendation_click
    on($(CFG.sel.recommend), 'click', function (e) {
      var a = e.target.closest('a');
      if (!a) return;
      track('checker_recommendation_click', { airline: state.airline, target_url: a.href });
    });

    // 6. checker_affiliate_click — delegated across the whole page.
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href]');
      if (!a || !isAffiliate(a)) return;
      track('checker_affiliate_click', {
        source: 'checker',
        airline: state.airline,
        verdict: state.verdict,
        target_url: a.href
      });
    }, true);

    // 7. checker_embed_copy — tracks backlink intent.
    on($(CFG.sel.copyEmbed), 'click', function () {
      track('checker_embed_copy', { airline: state.airline });
    });
  }

  /* ------------------------------------------------------------------ *
   * The opt-in block. Result-aware, injected below the verdict.
   * ------------------------------------------------------------------ */
  function copyFor(verdict, airline) {
    var who = airline || 'your airline';
    if (verdict === 'fail') {
      return {
        head: "That bag won't pass — here's what will.",
        body: 'Get the bags that clear ' + who + "'s sizer, plus the printable size sheet for all 51 airlines, " +
              'and an alert the moment ' + who + ' changes its rules.'
      };
    }
    if (verdict === 'borderline') {
      return {
        head: "That's close enough to get stopped.",
        body: 'Borderline bags get sized at the gate. Get the printable sheet for all 51 airlines plus an alert ' +
              'if ' + who + ' tightens its limits.'
      };
    }
    return {
      head: 'Keep this for the airport.',
      body: 'Get the printable carry-on cheat sheet for all 51 airlines, plus an alert if ' + who +
            ' changes its rules before you fly.'
    };
  }

  function injectOptIn(afterEl, verdict) {
    if (state.optedIn) return;
    var existing = document.getElementById('lft-optin');
    if (existing) existing.parentNode.removeChild(existing);

    var c = copyFor(verdict, state.airline);
    var wrap = document.createElement('section');
    wrap.id = 'lft-optin';
    wrap.setAttribute('aria-labelledby', 'lft-optin-head');
    wrap.innerHTML =
      '<h3 id="lft-optin-head">' + esc(c.head) + '</h3>' +
      '<p class="lft-optin-body">' + esc(c.body) + '</p>' +
      '<form class="lft-optin-form" novalidate>' +
        '<label for="lft-optin-email">Email address</label>' +
        '<div class="lft-optin-row">' +
          '<input id="lft-optin-email" name="email_address" type="email" required ' +
                 'autocomplete="email" inputmode="email" placeholder="you@example.com">' +
          '<button type="submit">Send it to me</button>' +
        '</div>' +
        '<p class="lft-optin-consent">' +
          '<input id="lft-optin-consent" type="checkbox" required>' +
          '<label for="lft-optin-consent">Yes, email me the size sheet plus luggage size updates, ' +
            'baggage fee changes and bag recommendations from Luggage For Travel.</label>' +
        '</p>' +
        '<p class="lft-optin-legal">We\'ll send a confirmation link first. Unsubscribe any time in one click. ' +
          'We never sell or share your data. <a href="' + esc(CFG.privacyUrl) + '">Privacy Policy</a>. ' +
          esc(CFG.company) + '</p>' +
        '<p class="lft-optin-msg" role="status" aria-live="polite"></p>' +
      '</form>';

    afterEl.parentNode.insertBefore(wrap, afterEl.nextSibling);
    track('checker_optin_view', { airline: state.airline, verdict: verdict });

    wrap.querySelector('form').addEventListener('submit', function (e) {
      e.preventDefault();
      submitOptIn(wrap, verdict);
    });
  }

  function submitOptIn(wrap, verdict) {
    var form = wrap.querySelector('form');
    var email = wrap.querySelector('#lft-optin-email');
    var consent = wrap.querySelector('#lft-optin-consent');
    var msg = wrap.querySelector('.lft-optin-msg');
    var btn = wrap.querySelector('button[type="submit"]');

    if (!email.value || !email.checkValidity()) { say(msg, 'Please enter a valid email address.', true); email.focus(); return; }
    if (!consent.checked) { say(msg, 'Please tick the box so we can email you.', true); consent.focus(); return; }

    // Tags carry the segmentation. This is what makes the list monetise later.
    var fields = {
      'fields[airline]': state.airline || '',
      'fields[verdict]': verdict || '',
      'fields[allowance]': state.allowance || '',
      'fields[source]': 'checker',
      tags: 'source:checker'
    };

    if (!CFG.kitFormUid) {
      say(msg, 'Preview mode — set kitFormUid to go live. Captured: ' + email.value, false);
      track('checker_email_optin', merge({ airline: state.airline, verdict: verdict, preview: true }, {}));
      return;
    }

    btn.disabled = true;
    say(msg, 'Sending…', false);

    var body = new FormData();
    body.append('email_address', email.value);
    Object.keys(fields).forEach(function (k) { body.append(k, fields[k]); });

    fetch(CFG.kitEndpoint.replace('{uid}', CFG.kitFormUid), {
      method: 'POST',
      body: body,
      headers: { Accept: 'application/json' }
    }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      state.optedIn = true;
      form.innerHTML = '<p class="lft-optin-done">Check your inbox — click the confirmation link and it\'s on its way.</p>';
      track('checker_email_optin', { airline: state.airline, verdict: verdict });
    }).catch(function (err) {
      btn.disabled = false;
      say(msg, 'That didn\'t go through. Opening the signup page instead…', true);
      track('checker_optin_error', { airline: state.airline, verdict: verdict, message: String(err) });
      setTimeout(function () { window.location.href = CFG.kitFallbackUrl; }, 1200);
    });
  }

  /* ------------------------------------------------------------------ *
   * Helpers
   * ------------------------------------------------------------------ */
  function readVerdict(el) {
    var d = (el.dataset && el.dataset.verdict || '').toLowerCase();
    if (d) return d;
    var t = text(el).toLowerCase();
    if (!t) return null;
    if (/\b(too big|too deep|too wide|too tall|too heavy|won['’]t fit|does not fit|doesn['’]t fit|fail)\b/.test(t)) return 'fail';
    if (/\b(borderline|close|just about|cutting it)\b/.test(t)) return 'borderline';
    if (/\b(fits|will fit|you['’]re good|pass)\b/.test(t)) return 'pass';
    return null;
  }

  function readUnits() {
    var c = document.querySelector('input[name*="unit" i]:checked, select[name*="unit" i], [data-units]');
    if (!c) return null;
    var v = (c.dataset && c.dataset.units) || c.value || '';
    return /in|inch/i.test(v) ? 'in' : /cm/i.test(v) ? 'cm' : v || null;
  }

  function hasWeight() {
    var w = document.querySelector('input[name*="weight" i], #weight');
    return !!(w && String(w.value || '').trim());
  }

  function isAffiliate(a) {
    var rel = (a.getAttribute('rel') || '').toLowerCase();
    if (rel.indexOf('sponsored') > -1 || rel.indexOf('nofollow') > -1) {
      return a.hostname !== window.location.hostname;
    }
    return /amzn\.to|amazon\.|awin1\.com|\.prf\.hn|go\.redirectingat|shareasale|anrdoezrs|tkqlhce|jdoqocy/i.test(a.href);
  }

  function on(el, ev, fn, once) { if (el) el.addEventListener(ev, fn, once ? { once: true } : false); }
  function text(el) { return (el && (el.textContent || '')).trim(); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (m) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]; }); }
  function say(el, m, isErr) { el.textContent = m; el.className = 'lft-optin-msg' + (isErr ? ' is-error' : ''); }
  function merge(a, b) {
    var out = {}, k;
    for (k in a) if (Object.prototype.hasOwnProperty.call(a, k)) out[k] = a[k];
    for (k in b) if (Object.prototype.hasOwnProperty.call(b, k)) {
      out[k] = (b[k] && typeof b[k] === 'object' && !Array.isArray(b[k])) ? merge(a[k] || {}, b[k]) : b[k];
    }
    return out;
  }
  function debounce(fn, ms) {
    var t; return function () { clearTimeout(t); t = setTimeout(fn, ms); };
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
