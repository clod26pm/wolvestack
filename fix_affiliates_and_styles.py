#!/usr/bin/env python3
"""
Critical fixes for wolvestack.com affiliate links and vendor card styling.

Issues found 2026-05-06:
1. 5 different particlepeptides URL formats — only ONE works without redirect mangling.
   The most common format (`https://www.particlepeptides.com/?refs=25135`) gets URL-encoded
   by the vendor's redirect, destroying the affiliate parameter.
2. 8 different limitless URL formats — including TYPO domains
   (limitlesslifenoo.com, limitlesslifenotropics.com, limitless-biohacking.com).
3. Pages use `.vendor-card` / `.vendor-cards` / `.vendor-btn` CSS classes but
   the actual CSS rules are MISSING from those pages — vendor cards render unstyled.
4. Many articles entirely missing vendor cards (no affiliate links at all).
5. Footer links to `/disclaimer.html` etc. use root paths from /en/ pages.

This script:
- Normalizes ALL affiliate URLs to the working format.
- Injects vendor-card CSS into all pages that need it.
- Injects a standard vendor card block into articles that don't have one.
- Idempotent — safe to re-run.

Run from peptide-daily-content/:
    python3 fix_affiliates_and_styles.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ---- Canonical affiliate URLs (verified 2026-05-06 — these resolve correctly) ----
# Particle: their redirect on the apex domain mangles the query string.
# The /en/16-buy-peptides path preserves it cleanly.
PARTICLE_GOOD = "https://particlepeptides.com/en/16-buy-peptides?refs=25135"

# Limitless: the EverFlow tracked URL is the format their tracking expects;
# it works and credits the affid properly.
LIMITLESS_GOOD = "https://www.limitlesslifenootropics.com/?_ef_transaction_id=&oid=1&affid=10704"

# All known broken / variant URLs and what they should become
URL_REPLACEMENTS = [
    # Particle variants (incl. typos)
    (r'https?://(?:www\.)?particlepeptides\.com/\?refs=25135',                    PARTICLE_GOOD),
    (r'https?://(?:www\.)?particlepeptides\.com\?refs=25135',                     PARTICLE_GOOD),
    (r'https?://(?:www\.)?particlepeptides\.com/en/\?refs=25135',                 PARTICLE_GOOD),
    # already-good URL — leave alone (no replacement, regex won't match itself once normalized)

    # Limitless variants (incl. typos)
    (r'https?://limitlesslifenoo\.com/?\?affid=10704',                            LIMITLESS_GOOD),
    (r'https?://(?:www\.)?limitless-biohacking\.com/?\?affid=10704',              LIMITLESS_GOOD),
    (r'https?://(?:www\.)?limitlesslifebiotech\.com/\?affid=10704',               LIMITLESS_GOOD),
    (r'https?://(?:www\.)?limitless-peptides\.com/\?affid=10704',                 LIMITLESS_GOOD),
    (r'https?://(?:www\.)?limitlesslifenotropics\.com/\?affid=10704',             LIMITLESS_GOOD),
    (r'https?://limitlesslifenootropics\.com/\?affid=10704',                      LIMITLESS_GOOD),
    # Already correct (full tracked) — leave alone

    # Ascension placeholder — kill if it's a non-functional ?ref=wolvestack
    # (Replace with Particle as a safer, working partner)
    (r'https?://ascensionsupplements\.com/\?ref=wolvestack',                      PARTICLE_GOOD),
]


# ---- Vendor-card CSS that must be present on any page using these classes ----
VENDOR_CARDS_CSS = """\
<style id="vendor-cards-styles">
/* Vendor cards — injected by fix_affiliates_and_styles.py */
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
@media (max-width: 600px) {
  .vendor-cards { grid-template-columns: 1fr; }
}
</style>
"""

# ---- Standard vendor card block to inject into articles missing one ----
VENDOR_BLOCK_HTML = """\
<!-- AFFILIATE-VENDORS -->
<h2 id="trusted-vendors">Trusted Research-Grade Sources</h2>
<p>Below are the two vendors we recommend for research peptides — both publish independent third-party Certificates of Analysis (COAs) and ship internationally. Affiliate links: we earn a small commission at no extra cost to you (see <a href="/en/affiliate-disclosure.html">Affiliate Disclosure</a>).</p>
<div class="vendor-cards">
<div class="vendor-card particle-card">
<h3>Particle Peptides</h3>
<p>Independently HPLC-tested, transparent COAs, comprehensive product range.</p>
<a class="vendor-btn particle-btn" href="__PARTICLE__" rel="nofollow sponsored" target="_blank">Browse Particle Peptides →</a>
</div>
<div class="vendor-card limitless-card">
<h3>Limitless Life Nootropics</h3>
<p>Premium research peptides with strong customer support and verified purity.</p>
<a class="vendor-btn limitless-btn" href="__LIMITLESS__" rel="nofollow sponsored" target="_blank">Browse Limitless Life →</a>
</div>
</div>
""".replace("__PARTICLE__", PARTICLE_GOOD).replace("__LIMITLESS__", LIMITLESS_GOOD)


def has_vendor_card_css(html: str) -> bool:
    """Check if page already has vendor-card styles defined."""
    # Look for the style block id, OR an actual `.vendor-card` rule (not just class usage)
    if 'id="vendor-cards-styles"' in html:
        return True
    # Look for ".vendor-card {" or ".vendor-card  " in a <style> block
    return bool(re.search(r'\.vendor-cards?\s*\{', html))


def has_vendor_card_html(html: str) -> bool:
    """Check if page already has a vendor card block in the body (not just CSS)."""
    return bool(re.search(r'<div\s+class="vendor-cards?"', html))


def is_article_page(path: Path, html: str) -> bool:
    """Skip non-article pages (legal, search, index, IIAS, etc.)."""
    skip_names = {
        "privacy.html", "terms.html", "disclaimer.html", "affiliate-disclosure.html",
        "404.html", "search.html", "ARTICLE-TEMPLATE.html", "TEMPLATE-CSS.html",
        "TEMPLATE-BODY.html", "isitascam.html", "isitascam-privacy.html",
        "isitascam-support.html", "isitascam-terms.html", "category.html",
        "about.html", "contact.html", "index.html",
    }
    if path.name in skip_names:
        return False
    if "isitascam" in path.name:
        return False
    # Must have an article-hero section to be a real article
    return 'class="article-hero"' in html


def fix_urls(html: str) -> tuple[str, int]:
    """Replace all bad affiliate URLs. Returns (new_html, replacements_count)."""
    count = 0
    for pattern, replacement in URL_REPLACEMENTS:
        new_html, n = re.subn(pattern, replacement, html)
        if n > 0:
            html = new_html
            count += n
    return html, count


def inject_css_if_needed(html: str) -> tuple[str, bool]:
    """Inject vendor-cards CSS if classes are used but styles are missing."""
    uses_classes = bool(re.search(r'class="[^"]*vendor-(card|btn)', html))
    if not uses_classes:
        return html, False
    if has_vendor_card_css(html):
        return html, False
    # Inject right before </head>
    if '</head>' not in html:
        return html, False
    new_html = html.replace('</head>', f'{VENDOR_CARDS_CSS}\n</head>', 1)
    return new_html, True


def inject_vendor_block_if_missing(html: str) -> tuple[str, bool]:
    """Inject a standard vendor card block in articles that don't have one.
    Insert just before the FAQ section, related-articles, or the footer."""
    if has_vendor_card_html(html):
        return html, False
    # Anchor candidates (in order of preference):
    anchors = [
        # Before FAQ schema container
        re.compile(r'(<h2[^>]*>(?:\s|<[^>]+>)*(?:Frequently Asked Questions|FAQ|FAQs)\b)', re.IGNORECASE),
        # Before related-cards section
        re.compile(r'(<section[^>]*class="[^"]*related[^"]*"[^>]*>)', re.IGNORECASE),
        # Before article footer
        re.compile(r'(<footer\b)', re.IGNORECASE),
        # Before closing </article>
        re.compile(r'(</article>)', re.IGNORECASE),
    ]
    for rx in anchors:
        m = rx.search(html)
        if m:
            new_html = html[:m.start()] + VENDOR_BLOCK_HTML + "\n" + html[m.start():]
            return new_html, True
    return html, False


def main():
    files = list(ROOT.glob("*.html"))
    for lang in ("en", "es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de", "nl", "ar"):
        files += list((ROOT / lang).glob("*.html"))
    files += list((ROOT / "app").glob("*.html"))

    total = 0
    url_fixed = 0
    css_injected = 0
    block_injected = 0
    article_count = 0
    skipped = 0

    for p in files:
        try:
            html = p.read_text(encoding="utf-8")
        except Exception:
            skipped += 1
            continue

        original = html
        # Always normalize URLs (even on legal/static pages with affiliate links)
        html, n = fix_urls(html)
        if n > 0:
            url_fixed += n

        # CSS + vendor block injection only on article pages
        is_article = is_article_page(p, html)
        if is_article:
            article_count += 1
            html, css_done = inject_css_if_needed(html)
            if css_done:
                css_injected += 1
            html, block_done = inject_vendor_block_if_missing(html)
            if block_done:
                block_injected += 1

        if html != original:
            p.write_text(html, encoding="utf-8")
            total += 1

    print(f"Files written:           {total}")
    print(f"  URL normalizations:    {url_fixed}")
    print(f"  CSS blocks injected:   {css_injected}")
    print(f"  Vendor blocks injected: {block_injected}")
    print(f"Article pages scanned:   {article_count}")
    print(f"Files skipped (errors):  {skipped}")


if __name__ == "__main__":
    main()
