#!/usr/bin/env python3
"""Generate the merged consolidation pages. Every dimension comes from
lft/fare-watch/airlines.json — nothing here is hand-typed."""
import json, pathlib, datetime

HERE = pathlib.Path(__file__).resolve().parent
DS = {a['key']: a for a in json.loads(
    (HERE/'../fare-watch/airlines.json').read_text(encoding='utf-8'))['airlines']}
TODAY = datetime.date.today().isoformat()

def row(key, code):
    for al in DS[key]['allowances']:
        if al['code'] == code: return al
    raise KeyError(f'{key}/{code}')
def cm(al): return '%d × %d × %d cm' % tuple(al['cm'])
def inch(al): return '%d × %d × %d in' % tuple(round(v/2.54) for v in al['cm'])
def both(al):
    out = f"<strong>{cm(al)}</strong> (≈{inch(al)})"
    if al.get('kg'): out += f", {al['kg']} kg"
    return out
def ld(headline, desc, url, faqs):
    return json.dumps({"@context":"https://schema.org","@graph":[
      {"@type":"Article","headline":headline,"description":desc,
       "datePublished":TODAY,"dateModified":TODAY,
       "author":{"@type":"Organization","name":"Luggage for Travel"},
       "publisher":{"@type":"Organization","name":"Luggage for Travel",
                    "url":"https://luggagefortravel.com/"},
       "mainEntityOfPage":{"@type":"WebPage","@id":url}},
      {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q,a in faqs]}]}, indent=1)

HDR = """<!--
  LFT — %(url)s
  GENERATED %(today)s by lft/content/build-merged.py. Do not hand-edit: change
  lft/fare-watch/airlines.json and re-run, so this page can never contradict the checker.

  MERGE TARGET. Publish this body BEFORE importing the redirects that point here
  (lft/consolidation/redirects-hotel-adjusted.csv), or the 301s land on the old content.
  Absorbs: %(absorbs)s
-->
"""

# ── 1 ── Ryanair rules: 3 pages into 1 ──────────────────────────────────────
r_pi, r_pc = row('ryanair','personal_item'), row('ryanair','priority_cabin')
page1 = (HDR % {'url':'/airline-baggage-rules/ryanair-carry-on-size-rules-2026/','today':TODAY,
  'absorbs':'ryanair-carry-on-rules-2026/ (8 impr), ryanair-carry-on-size-rules/ (4 impr)'}) + f"""
<p class="lft-lede">Ryanair gives every passenger one free under-seat bag. Everything bigger
costs money, and the gate is where it gets expensive. Here are both allowances, what
Priority actually buys, and how hard Ryanair enforces them.</p>

<h2>The two allowances</h2>
<table class="lft-table">
  <thead><tr><th>Allowance</th><th>Maximum size</th><th>Included with</th></tr></thead>
  <tbody>
    <tr><td><strong>Free under-seat bag</strong></td><td>{both(r_pi)}</td>
        <td>Every fare, no exceptions</td></tr>
    <tr><td><strong>Priority cabin bag</strong></td><td>{both(r_pc)}</td>
        <td>Priority &amp; 2 Cabin Bags, or a paid cabin-bag add-on</td></tr>
  </tbody>
</table>
<p class="lft-sub">Sizes include wheels, handles and bulging pockets. Ryanair measures the
bag, not the brochure.</p>

<p><a href="/carry-on-size-checker/"><strong>Check your bag against Ryanair in the size
checker →</strong></a></p>

<h2>What Priority actually buys you</h2>
<p>Priority is not boarding order with a bag thrown in — the bag <em>is</em> the product. It
adds a {cm(r_pc)} cabin bag in the overhead locker, carried alongside the free under-seat
bag, so you board with two pieces instead of one.</p>
<p>It is always cheaper added at booking than at the gate. Ryanair prices both, and the gate
price is the one designed to hurt. We do not publish the figures here because they change by
route and date — take them from the booking page, and take the gate figure as the number
you are avoiding.</p>

<h2>Enforcement: assume the sizer</h2>
<p>Ryanair sits in the strictest band of the {len(DS)} airlines we track. Gate sizing is
routine rather than occasional, especially on full flights, and a bag that will not drop
into the sizer gets put in the hold for a fee.</p>
<p><strong>Pack to one centimetre under on every axis.</strong> A soft bag that measures
{cm(r_pi)} empty will not measure that once it is full, and the sizer does not care that it
fitted at home.</p>

<h2>The mistakes that cost money</h2>
<ul>
  <li><strong>Measuring the bag empty.</strong> Packed depth is what counts.</li>
  <li><strong>Ignoring wheels and handles.</strong> They are part of the measurement.</li>
  <li><strong>Buying Priority and still packing a 40-litre rucksack.</strong> Priority adds
      a bag, it does not lift the size limit on either one.</li>
  <li><strong>Assuming last year's bag is still compliant.</strong> It usually is — but check
      rather than assume, because the gate fee is the price of being wrong.</li>
</ul>

<h2>Frequently asked questions</h2>
<h3>What is Ryanair's free bag size?</h3>
<p>{cm(r_pi)} ({inch(r_pi)}), included on every fare. It must fit under the seat in front of
you.</p>
<h3>How big is the Ryanair Priority cabin bag?</h3>
<p>{cm(r_pc)} ({inch(r_pc)}) with a {r_pc['kg']} kg limit, carried in the overhead locker.
It requires Priority &amp; 2 Cabin Bags or a paid cabin-bag add-on.</p>
<h3>Does Ryanair really measure cabin bags?</h3>
<p>Yes. Ryanair is one of the strictest enforcers in our index — gate sizing is routine, and
an oversized bag goes into the hold for a fee that is higher than the online price.</p>
<h3>Do wheels and handles count towards Ryanair's size limit?</h3>
<p>Yes. The published dimensions are external and include wheels, handles and any pockets
that bulge when the bag is full.</p>

<p><a href="/airline-baggage-rules/best-ryanair-cabin-bag/">Bags that fit both Ryanair
allowances →</a> · <a href="/carry-on-size-by-airline/">Every airline's carry-on size →</a></p>

<script type="application/ld+json">
{ld("Ryanair carry-on size rules",
    f"Ryanair's free under-seat bag is {cm(r_pi)} and the Priority cabin bag is {cm(r_pc)}. Both allowances, what Priority buys, and how strictly Ryanair enforces them.",
    "https://luggagefortravel.com/airline-baggage-rules/ryanair-carry-on-size-rules-2026/",
    [("What is Ryanair's free bag size?", f"{cm(r_pi)} ({inch(r_pi)}), included on every fare. It must fit under the seat in front of you."),
     ("How big is the Ryanair Priority cabin bag?", f"{cm(r_pc)} ({inch(r_pc)}) with a {r_pc['kg']} kg limit, carried in the overhead locker."),
     ("Does Ryanair really measure cabin bags?", "Yes. Ryanair is one of the strictest enforcers in our index. Gate sizing is routine and an oversized bag goes into the hold for a fee."),
     ("Do wheels and handles count towards Ryanair's size limit?", "Yes. The published dimensions are external and include wheels, handles and bulging pockets.")])}
</script>
"""

# ── 2 ── Ryanair commercial: 3 pages into 1 ─────────────────────────────────
page2 = (HDR % {'url':'/airline-baggage-rules/best-ryanair-cabin-bag/','today':TODAY,
  'absorbs':'best-carry-on-luggage-ryanair/ (17 impr), luggage-reviews/best-personal-item-bag-for-ryanair/ (4 impr)'}) + f"""
<p class="lft-lede">Ryanair has two cabin allowances and they need two different bags. This
page covers both, because buying the wrong one is how people end up paying at the gate.</p>

<p><a href="/carry-on-size-checker/"><strong>Already own a bag? Check it against Ryanair
first →</strong></a></p>

<h2>Which bag do you actually need?</h2>
<table class="lft-table">
  <thead><tr><th>If you are flying…</th><th>You need a bag up to</th></tr></thead>
  <tbody>
    <tr><td>On the base fare, no add-ons</td><td>{both(r_pi)} — under-seat only</td></tr>
    <tr><td>With Priority &amp; 2 Cabin Bags</td><td>{both(r_pc)} — plus the under-seat bag</td></tr>
  </tbody>
</table>

<h2>Bags for the free under-seat allowance ({cm(r_pi)})</h2>
<p>This is the one most people need, and the one most people get wrong. You are shopping for
a bag whose <em>packed</em> external size stays inside {cm(r_pi)}.</p>
<p>What matters, in order:</p>
<ol>
  <li><strong>A structured shape, not a squashy one.</strong> A bag that holds its form is
      measurable and predictable at the gate. A soft holdall expands exactly where the sizer
      is tightest.</li>
  <li><strong>Nominal size at or just under the limit.</strong> A bag advertised at
      {cm(r_pi)} exactly will usually measure over once packed. Aim a centimetre under.</li>
  <li><strong>No external pockets that bulge.</strong> They are part of the measurement.</li>
  <li><strong>Low empty weight.</strong> There is no published weight limit on this
      allowance, but a heavy empty bag wastes the capacity you are paying for.</li>
</ol>

<h2>Bags for the Priority cabin allowance ({cm(r_pc)})</h2>
<p>A {r_pc['kg']} kg limit applies here, so empty weight matters as much as dimensions. A
2.5 kg shell leaves {round(r_pc['kg'] - 2.5, 1)} kg of packing; a 4 kg one leaves
{round(r_pc['kg'] - 4, 1)} kg. That difference is a pair of shoes and a coat.</p>
<ul>
  <li><strong>Two-wheel over four-wheel</strong> for this size — spinner castors add depth
      and eat into the 20 cm axis.</li>
  <li><strong>Soft or hybrid over hard shell</strong>, because hard shells are heavier for
      the same capacity and you are weight-limited.</li>
  <li><strong>No expansion zip</strong>, or at least never use it. An expanded bag is an
      oversized bag.</li>
</ul>

<h2>Buying for both at once</h2>
<p>If you fly Ryanair on both fare types, the efficient combination is one structured
under-seat bag at {cm(r_pi)} and one lightweight {cm(r_pc)} cabin bag — not a single
mid-sized bag that is too big for the free allowance and wasteful of the paid one.</p>

<h2>Frequently asked questions</h2>
<h3>What size bag is free on Ryanair?</h3>
<p>{cm(r_pi)} ({inch(r_pi)}), under the seat, on every fare.</p>
<h3>Do I need Priority to bring a cabin bag on Ryanair?</h3>
<p>To bring a {cm(r_pc)} bag into the overhead locker, yes — Priority &amp; 2 Cabin Bags or
a paid cabin-bag add-on. Without it you get the {cm(r_pi)} under-seat bag only.</p>
<h3>What is the weight limit for a Ryanair cabin bag?</h3>
<p>{r_pc['kg']} kg for the Priority cabin bag. Ryanair publishes no weight limit for the
free under-seat bag.</p>

<p><a href="/airline-baggage-rules/ryanair-carry-on-size-rules-2026/">Ryanair's full
carry-on rules →</a> · <a href="/luggage-reviews/best-underseat-bags-budget-airlines/">Underseat
bags for budget airlines →</a></p>

<script type="application/ld+json">
{ld("Best Ryanair cabin bags, for both allowances",
    f"Ryanair has two cabin allowances — a free {cm(r_pi)} under-seat bag and a {cm(r_pc)} Priority bag at {r_pc['kg']} kg. What to look for in each.",
    "https://luggagefortravel.com/airline-baggage-rules/best-ryanair-cabin-bag/",
    [("What size bag is free on Ryanair?", f"{cm(r_pi)} ({inch(r_pi)}), under the seat, on every fare."),
     ("Do I need Priority to bring a cabin bag on Ryanair?", f"To bring a {cm(r_pc)} bag into the overhead locker, yes. Without it you get the {cm(r_pi)} under-seat bag only."),
     ("What is the weight limit for a Ryanair cabin bag?", f"{r_pc['kg']} kg for the Priority cabin bag. Ryanair publishes no weight limit for the free under-seat bag.")])}
</script>
"""

# ── 3 ── Lufthansa: 2 pages into 1 ──────────────────────────────────────────
l_hb, l_sc = row('lufthansa','handbag_only'), row('lufthansa','standard_cabin')
page3 = (HDR % {'url':'/airline-baggage-rules/lufthansa-carry-on-size-2026/','today':TODAY,
  'absorbs':'lufthansa-carry-on-size/ (7 impr, root-level duplicate)'}) + f"""
<p class="lft-lede">Lufthansa's cabin allowance depends entirely on your fare. Economy Light
gets a hand bag and nothing else — that is the detail that catches people out.</p>

<h2>What you get, by fare</h2>
<table class="lft-table">
  <thead><tr><th>Fare</th><th>Cabin allowance</th></tr></thead>
  <tbody>
    <tr><td><strong>Economy Light</strong></td>
        <td>Hand bag only: {both(l_hb)}</td></tr>
    <tr><td><strong>Economy Classic and above</strong></td>
        <td>Cabin bag {both(l_sc)}, plus a {cm(l_hb)} hand bag</td></tr>
  </tbody>
</table>
<p class="lft-sub">Both figures are external and include wheels and handles.</p>

<p><a href="/carry-on-size-checker/"><strong>Check your bag against your Lufthansa fare
→</strong></a></p>

<h2>The Economy Light trap</h2>
<p>Economy Light is sold as the cheap fare, and on a search page it looks like the others. It
is not: <strong>there is no cabin bag</strong>, only the {cm(l_hb)} hand bag that goes under
the seat. Turning up with a {cm(l_sc)} roller on an Economy Light ticket means paying at the
airport.</p>
<p>Before you book Light, price Classic with the bag you intend to bring. The gap is often
smaller than the airport charge.</p>

<h2>Enforcement: conditional</h2>
<p>Lufthansa sits in our visual-check band, not the aggressive one. Bags are screened by eye
as you board and pulled to the sizer only if they look clearly oversized. A bag comfortably
inside {cm(l_sc)} usually walks on unchallenged — which is precisely why the
{l_sc['kg']} kg weight limit, not the dimensions, is the one that catches people on full
long-haul flights.</p>

<h2>Frequently asked questions</h2>
<h3>What is Lufthansa's carry-on size?</h3>
<p>{cm(l_sc)} ({inch(l_sc)}) with a {l_sc['kg']} kg limit, on Economy Classic and above. You
may also bring a {cm(l_hb)} hand bag.</p>
<h3>Can I bring a cabin bag on Lufthansa Economy Light?</h3>
<p>No. Economy Light includes a {cm(l_hb)} hand bag that must fit under the seat. A full
cabin bag requires Economy Classic or higher, or paying for it separately.</p>
<h3>How strict is Lufthansa about cabin baggage?</h3>
<p>Moderately. Bags are visually screened at boarding and sized only if they look oversized.
The {l_sc['kg']} kg weight limit is enforced more consistently than the dimensions.</p>

<p><a href="/carry-on-size-by-airline/">Every airline's carry-on size →</a> ·
<a href="/airline-baggage-rules/how-strict-are-airlines-about-carry-on-size/">How strictly
each airline enforces →</a></p>

<script type="application/ld+json">
{ld("Lufthansa carry-on size, by fare",
    f"Lufthansa Economy Classic and above include a {cm(l_sc)} cabin bag at {l_sc['kg']} kg. Economy Light includes a {cm(l_hb)} hand bag only.",
    "https://luggagefortravel.com/airline-baggage-rules/lufthansa-carry-on-size-2026/",
    [("What is Lufthansa's carry-on size?", f"{cm(l_sc)} ({inch(l_sc)}) with a {l_sc['kg']} kg limit, on Economy Classic and above, plus a {cm(l_hb)} hand bag."),
     ("Can I bring a cabin bag on Lufthansa Economy Light?", f"No. Economy Light includes a {cm(l_hb)} hand bag only. A full cabin bag requires Economy Classic or higher."),
     ("How strict is Lufthansa about cabin baggage?", f"Moderately. Bags are visually screened at boarding. The {l_sc['kg']} kg weight limit is enforced more consistently than the dimensions.")])}
</script>
"""

# ── 4 ── Frontier commercial: NEW slug, required before the import ──────────
f_pi, f_pc = row('frontier-airlines','personal_item'), row('frontier-airlines','paid_carry_on')
page4 = (HDR % {'url':'/airline-baggage-rules/best-carry-on-luggage-frontier-airlines/','today':TODAY,
  'absorbs':'best-carry-on-luggage-for-frontier-airlines-2024-complete-guide/ (7 impr), best-carry-on-luggage-frontier/ (2 impr)'}) + f"""
<p class="lft-lede"><strong>This URL must exist before the redirects are imported.</strong>
Two older Frontier pages 301 here, one of which carried <em>2024</em> in its slug.</p>

<p>Frontier charges for the overhead bin. Your free allowance is the under-seat bag, and the
bag you buy decides whether you ever pay Frontier for luggage again.</p>

<h2>Frontier's two allowances</h2>
<table class="lft-table">
  <thead><tr><th>Allowance</th><th>Maximum size</th><th>Cost</th></tr></thead>
  <tbody>
    <tr><td><strong>Personal item</strong></td><td>{both(f_pi)}</td>
        <td>Free on every fare</td></tr>
    <tr><td><strong>Carry-on bag</strong></td><td>{both(f_pc)}</td>
        <td>Paid — cheapest at booking</td></tr>
  </tbody>
</table>

<p><a href="/carry-on-size-checker/"><strong>Check your bag against Frontier →</strong></a></p>

<h2>The free bag is the whole game</h2>
<p>Frontier's personal item at {cm(f_pi)} is larger than most US carriers allow for free, and
it is the closest match to what Spirit used to permit. A well-chosen under-seat bag at this
size means never buying a Frontier carry-on.</p>
<ul>
  <li><strong>Structured, not soft.</strong> Frontier is in the strictest enforcement band
      and sizes personal items at boarding.</li>
  <li><strong>A centimetre under on every axis.</strong> {cm(f_pi)} advertised is usually
      over once packed.</li>
  <li><strong>Front-loading over top-loading</strong> — you will be retrieving things from a
      bag wedged under a seat.</li>
</ul>

<h2>If you are buying the paid carry-on anyway</h2>
<p>Frontier's paid allowance is {cm(f_pc)} with a {f_pc['kg']} kg limit — generous on size,
and unusually one of the few US carriers to publish a cabin weight limit at all. Pick a
lightweight shell: a 3 kg bag leaves {round(f_pc['kg'] - 3, 1)} kg of packing against
{round(f_pc['kg'] - 4.5, 1)} kg for a 4.5 kg one.</p>

<h2>Frequently asked questions</h2>
<h3>What is Frontier's free personal item size?</h3>
<p>{cm(f_pi)} ({inch(f_pi)}), free on every fare, and it must fit under the seat.</p>
<h3>How big is Frontier's paid carry-on?</h3>
<p>{cm(f_pc)} ({inch(f_pc)}) with a {f_pc['kg']} kg weight limit. It is cheapest booked with
the flight and most expensive at the gate.</p>
<h3>Does Frontier check personal item size?</h3>
<p>Yes. Frontier is in the strictest enforcement band in our index and sizes personal items
at boarding.</p>

<p><a href="/airline-baggage-rules/frontier-airlines-carry-on-size/">Frontier's full carry-on
rules →</a> · <a href="/spirit-airlines-shutdown/">Replacing Spirit? Start here →</a></p>

<script type="application/ld+json">
{ld("Best carry-on luggage for Frontier Airlines",
    f"Frontier's free personal item is {cm(f_pi)} and its paid carry-on is {cm(f_pc)} at {f_pc['kg']} kg. What to buy for each.",
    "https://luggagefortravel.com/airline-baggage-rules/best-carry-on-luggage-frontier-airlines/",
    [("What is Frontier's free personal item size?", f"{cm(f_pi)} ({inch(f_pi)}), free on every fare, and it must fit under the seat."),
     ("How big is Frontier's paid carry-on?", f"{cm(f_pc)} ({inch(f_pc)}) with a {f_pc['kg']} kg weight limit."),
     ("Does Frontier check personal item size?", "Yes. Frontier is in the strictest enforcement band in our index and sizes personal items at boarding.")])}
</script>
"""

for fn, body in [('merged-ryanair-rules.html', page1),
                 ('merged-ryanair-cabin-bag.html', page2),
                 ('merged-lufthansa.html', page3),
                 ('new-frontier-carry-on-luggage.html', page4)]:
    (HERE/fn).write_text(body, encoding='utf-8')
    print(f'{fn}: {len(body):,} bytes')
