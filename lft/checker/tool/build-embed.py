#!/usr/bin/env python3
"""Derive the chromeless embed from the live tool. Never hand-edit embed.html —
re-run this whenever carry-on-size-checker.html changes."""
import re, sys

SRC, OUT = 'carry-on-size-checker.html', 'embed.html'
s = open(SRC, encoding='utf-8').read()

def cut(pattern, label, count=1):
    global s
    found = re.findall(pattern, s, re.S)
    assert len(found) == count, f"{label}: expected {count} match, got {len(found)}"
    s = re.sub(pattern, '', s, count=count, flags=re.S)

# 1 ── strip site chrome and the SEO prose: an embed is the tool, nothing else
cut(r'<header class="site-header">.*?</header>\n?', 'header')
cut(r'<footer class="site-footer">.*?</footer>\n?', 'footer')
cut(r'<section class="intro-block"[^>]*>.*?</section>\n?', 'intro')
for h in ('measure-heading', 'embed-heading', 'enforcement-heading', 'faq-heading'):
    cut(r'<section class="section" aria-labelledby="%s">.*?</section>\n?' % h, h)

# 2 ── the embed must never compete with the canonical tool in the index
s = s.replace('<meta name="robots" content="index, follow">',
              '<meta name="robots" content="noindex, follow">', 1)
assert 'noindex, follow' in s, 'robots'

# 3 ── links must break out of the frame, not navigate inside it
s = s.replace('<link rel="canonical"', '<base target="_blank">\n  <link rel="canonical"', 1)

# 4 ── drop the structured data: it belongs on the canonical page only
cut(r'<script type="application/ld\+json">.*?</script>\n?', 'ld+json', 2)

# 5 ── the JS still wires up the embed button we just removed
s = s.replace('const copyEmbed=document.getElementById("copyEmbed");\n'
              'const embedCode=document.getElementById("embedCode");',
              'const copyEmbed=document.getElementById("copyEmbed");\n'
              'const embedCode=document.getElementById("embedCode");', 1)
old = s[s.index('copyEmbed.addEventListener'):s.index('/* ── INIT ── */')]
assert old.strip().endswith('});'), 'copyEmbed listener shape'
s = s.replace(old, 'if(copyEmbed&&embedCode){\n' + old.rstrip() + '\n}\n\n', 1)

# 6 ── attribution the host cannot drop, plus iframe auto-height
ATTRIB = '''
<div class="lft-embed-credit">
  Carry-on size checker by
  <a href="https://luggagefortravel.com/carry-on-size-checker/?utm_source=embed">Luggage for Travel</a>
  — 51 airlines, fare-aware. Free to embed.
</div>
'''
CSS = '''
    body{background:transparent}
    .page-wrap{padding:0 0 12px}
    .lft-embed-credit{margin:14px 2px 0;font-size:12.5px;line-height:1.5;color:var(--lft-ink-3)}
    .lft-embed-credit a{color:var(--lft-accent);font-weight:600}
'''
HEIGHT = '''
/* ── iframe auto-height: report our height to the host on every change ── */
(function(){
  if(window.parent===window)return;
  let last=0;
  const post=()=>{
    const h=Math.ceil(document.documentElement.getBoundingClientRect().height);
    if(h&&Math.abs(h-last)>8){last=h;
      window.parent.postMessage({type:"lft-checker-height",height:h},"*");}
  };
  if(window.ResizeObserver)new ResizeObserver(post).observe(document.documentElement);
  window.addEventListener("load",post);
  document.addEventListener("click",()=>setTimeout(post,120),true);
  setInterval(post,1000);
  post();
})();
'''
s = s.replace('</main>', ATTRIB + '</main>', 1)
s = s.replace('  </style>', CSS + '  </style>', 1) if '  </style>' in s else s
assert '.lft-embed-credit' in s, 'embed css not injected'
s = s.replace('/* ── INIT ── */\nsetLabels();',
              '/* ── INIT ── */\nsetLabels();\n' + HEIGHT, 1)
assert 'lft-checker-height' in s, 'height reporter'

s = s.replace('<title>Carry-On Size Checker 2026 — Free Tool for 51 Airlines | Luggage For Travel</title>',
              '<title>Carry-On Size Checker — embeddable widget | Luggage for Travel</title>', 1)

open(OUT, 'w', encoding='utf-8').write(s)
print(f"{OUT}: {len(s):,} bytes (source {len(open(SRC,encoding='utf-8').read()):,})")
