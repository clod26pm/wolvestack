#!/usr/bin/env python3
"""
Inject vendor cards into articles that don't have them — handles BOTH templates:
- new layout: <div class="article-hero">
- older layout: <div class="hero">

Also injects CSS into any article that uses vendor-card classes but lacks the styles.
"""
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

# Skip non-article pages
SKIP = {
    "404.html", "search.html", "ARTICLE-TEMPLATE.html", "TEMPLATE-CSS.html",
    "TEMPLATE-BODY.html", "category.html", "about.html", "contact.html",
    "index.html", "privacy.html", "terms.html", "disclaimer.html",
    "affiliate-disclosure.html", "isitascam.html", "isitascam-privacy.html",
    "isitascam-support.html", "isitascam-terms.html",
}

# Anchor candidates for inserting vendor block — try in priority order
# The first regex that matches gets the block injected just before it.
INJECT_ANCHORS_RX = [
    # Right before the FAQ heading (most common cornerstone position)
    re.compile(r'(<h2[^>]*>(?:\s|<[^>]+>)*Frequently Asked Questions\b)', re.IGNORECASE),
    re.compile(r'(<h2[^>]*>(?:\s|<[^>]+>)*FAQ\b)', re.IGNORECASE),
    # Before the "related-articles" or "deep-dives" section (older template)
    re.compile(r'(<section[^>]*class="[^"]*related-articles[^"]*"[^>]*>)', re.IGNORECASE),
    re.compile(r'(<section[^>]*class="[^"]*deep-dives[^"]*"[^>]*>)', re.IGNORECASE),
    re.compile(r'(<section[^>]*class="[^"]*related[^"]*"[^>]*>)', re.IGNORECASE),
    # Before article footer
    re.compile(r'(<footer\b)', re.IGNORECASE),
    re.compile(r'(</article>)', re.IGNORECASE),
    re.compile(r'(<section[^>]*class="[^"]*newsletter)', re.IGNORECASE),
]


def is_article(path: Path, html: str) -> bool:
    if path.name in SKIP:
        return False
    if "isitascam" in path.name:
        return False
    # Either modern or older template
    return ('class="article-hero"' in html) or ('class="hero"' in html and '<h1' in html)


def has_vendor_block(html: str) -> bool:
    return ('AFFILIATE-VENDORS' in html) or bool(re.search(r'<div\s+class="vendor-cards"', html))


def inject_block(html: str) -> tuple[str, bool]:
    if has_vendor_block(html):
        return html, False
    for rx in INJECT_ANCHORS_RX:
        m = rx.search(html)
        if m:
            return html[:m.start()] + VENDOR_BLOCK + "\n" + html[m.start():], True
    return html, False


def inject_css(html: str) -> tuple[str, bool]:
    uses_classes = bool(re.search(r'class="[^"]*vendor-(card|btn)', html))
    if not uses_classes:
        return html, False
    has_css = ('id="vendor-cards-styles"' in html) or bool(re.search(r'\.vendor-cards?\s*\{', html))
    if has_css:
        return html, False
    if '</head>' not in html:
        return html, False
    return html.replace('</head>', f'{VENDOR_CARDS_CSS}\n</head>', 1), True


files = list(ROOT.glob("*.html"))
for lang in LANGS:
    files += list((ROOT / lang).glob("*.html"))

block_count = 0
css_count = 0
articles = 0
for p in files:
    try:
        html = p.read_text(encoding="utf-8")
    except Exception:
        continue
    if not is_article(p, html):
        continue
    articles += 1
    original = html
    html, b = inject_block(html)
    if b:
        block_count += 1
    html, c = inject_css(html)
    if c:
        css_count += 1
    if html != original:
        p.write_text(html, encoding="utf-8")

print(f"Articles processed: {articles}")
print(f"Vendor blocks injected: {block_count}")
print(f"CSS blocks injected: {css_count}")
