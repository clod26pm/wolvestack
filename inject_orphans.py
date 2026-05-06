#!/usr/bin/env python3
"""Inject vendor blocks into orphan articles — files that have an <h1>
and meaningful content but use no recognizable hero template."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANGS = ("en", "es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de", "nl", "ar")

PARTICLE_GOOD = "https://particlepeptides.com/en/16-buy-peptides?refs=25135"
LIMITLESS_GOOD = "https://www.limitlesslifenootropics.com/?_ef_transaction_id=&oid=1&affid=10704"

VENDOR_CARDS_CSS = """\
<style id="vendor-cards-styles">
.vendor-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin: 28px 0; }
.vendor-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px 22px; transition: transform .15s ease, box-shadow .15s ease; }
.vendor-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(15,34,64,0.08); }
.vendor-card h3 { font-size: 17px; font-weight: 700; margin: 0 0 8px; color: #0f2240; }
.vendor-card p { color: #475569; font-size: 14px; line-height: 1.55; margin: 0 0 14px; }
.vendor-btn { display: inline-block; padding: 10px 18px; border-radius: 8px; font-weight: 600; font-size: 13.5px; text-decoration: none !important; transition: background .15s; color: #fff !important; }
.particle-card { border-top: 4px solid #8b2fc9; }
.particle-btn { background: #6b21a8; }
.particle-btn:hover { background: #8b2fc9 !important; }
.limitless-card { border-top: 4px solid #0891b2; }
.limitless-btn { background: #0e7490; }
.limitless-btn:hover { background: #0891b2 !important; }
.apollo-card { border-top: 4px solid #ea580c; }
.apollo-btn { background: #c2410c; }
.apollo-btn:hover { background: #ea580c !important; }
@media (max-width: 600px) { .vendor-cards { grid-template-columns: 1fr; } }
</style>
"""

VENDOR_BLOCK = f"""\
<!-- AFFILIATE-VENDORS -->
<h2 id="trusted-vendors">Trusted Research-Grade Sources</h2>
<p>Below are the two vendors we recommend for research peptides — both publish independent third-party Certificates of Analysis (COAs) and ship internationally. Affiliate links: we earn a small commission at no extra cost to you (see <a href="/en/affiliate-disclosure.html">Affiliate Disclosure</a>).</p>
<div class="vendor-cards">
<div class="vendor-card particle-card">
<h3>Particle Peptides</h3>
<p>Independently HPLC-tested, transparent COAs, comprehensive product range.</p>
<a class="vendor-btn particle-btn" href="{PARTICLE_GOOD}" rel="nofollow sponsored" target="_blank">Browse Particle Peptides →</a>
</div>
<div class="vendor-card limitless-card">
<h3>Limitless Life Nootropics</h3>
<p>Premium research peptides with strong customer support and verified purity.</p>
<a class="vendor-btn limitless-btn" href="{LIMITLESS_GOOD}" rel="nofollow sponsored" target="_blank">Browse Limitless Life →</a>
</div>
</div>
"""

SKIP_NAMES = {
    "404.html", "search.html", "ARTICLE-TEMPLATE.html", "TEMPLATE-CSS.html",
    "TEMPLATE-BODY.html", "category.html", "about.html", "contact.html",
    "index.html", "privacy.html", "terms.html", "disclaimer.html",
    "affiliate-disclosure.html", "isitascam.html", "isitascam-privacy.html",
    "isitascam-support.html", "isitascam-terms.html",
}

files = list(ROOT.glob("*.html"))
for lang in LANGS:
    files += list((ROOT / lang).glob("*.html"))

block_count = 0
css_count = 0
for p in files:
    if p.name in SKIP_NAMES or "isitascam" in p.name:
        continue
    # Skip per-compound legal pages — they're regulatory reference, not article content
    if p.name.endswith("-legal.html"):
        continue
    try:
        html = p.read_text(encoding="utf-8")
    except Exception:
        continue
    if 'AFFILIATE-VENDORS' in html or '<div class="vendor-cards"' in html:
        continue
    # Real-article check: any heading tag and a closing body
    if '</body>' not in html:
        continue
    if '<h1' not in html and '<h2' not in html and '<article' not in html:
        continue
    original = html
    # Insert vendor block before </body> (or before <footer> if present)
    if '<footer' in html:
        idx = html.find('<footer')
        html = html[:idx] + VENDOR_BLOCK + "\n" + html[idx:]
    else:
        html = html.replace('</body>', VENDOR_BLOCK + '\n</body>', 1)
    # Inject CSS if missing
    if 'id="vendor-cards-styles"' not in html and not re.search(r'\.vendor-cards?\s*\{', html):
        if '</head>' in html:
            html = html.replace('</head>', f'{VENDOR_CARDS_CSS}\n</head>', 1)
            css_count += 1
    if html != original:
        p.write_text(html, encoding="utf-8")
        block_count += 1

print(f"Orphan articles fixed: {block_count} (CSS injected: {css_count})")
