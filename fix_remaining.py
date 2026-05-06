#!/usr/bin/env python3
"""
Cleanup pass for remaining issues after fix_affiliates_and_styles.py:
1. Inject vendor-card CSS into pages that received vendor blocks but no CSS
   (the original script ran block-injection AFTER css-check, leaving a gap).
2. Catch any remaining broken affiliate URLs that the regex missed.

Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANGS = ("en", "es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de", "nl", "ar")

PARTICLE_GOOD = "https://particlepeptides.com/en/16-buy-peptides?refs=25135"
LIMITLESS_GOOD = "https://www.limitlesslifenootropics.com/?_ef_transaction_id=&oid=1&affid=10704"

# Aggressive URL replacements (catch all known typos and variants)
URL_REPLACEMENTS = [
    # any limitless typo / variant URL (anything containing affid=10704 that isn't the canonical)
    (r'https?://(?:www\.)?limitlesslifenoo(?:tropics)?\.com/?\??[^"\s\']*affid=10704[^"\s\']*', LIMITLESS_GOOD),
    (r'https?://(?:www\.)?limitlesslifenotropics\.com/?\??[^"\s\']*affid=10704[^"\s\']*', LIMITLESS_GOOD),
    (r'https?://(?:www\.)?limitlesslifebiotech\.com/?\??[^"\s\']*affid=10704[^"\s\']*', LIMITLESS_GOOD),
    (r'https?://(?:www\.)?limitless-biohacking\.com/?\??[^"\s\']*affid=10704[^"\s\']*', LIMITLESS_GOOD),
    (r'https?://(?:www\.)?limitless-peptides\.com/?\??[^"\s\']*affid=10704[^"\s\']*', LIMITLESS_GOOD),
    # particle variants
    (r'https?://(?:www\.)?particlepeptides\.com/?\??[^"\s\']*refs=25135[^"\s\']*', PARTICLE_GOOD),
    # ascension typo placeholder
    (r'https?://(?:www\.)?ascensionsupplements\.com/?\??[^"\s\']*ref=wolvestack[^"\s\']*', PARTICLE_GOOD),
]

# Don't double-replace the canonical URLs (regex would match itself otherwise)
CANONICAL_GUARD = re.compile(
    r'https://particlepeptides\.com/en/16-buy-peptides\?refs=25135'
    r'|https://www\.limitlesslifenootropics\.com/\?_ef_transaction_id=&oid=1&affid=10704'
)

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


def main():
    files = list(ROOT.glob("*.html"))
    for lang in LANGS:
        files += list((ROOT / lang).glob("*.html"))

    url_fixed_files = 0
    url_total_repls = 0
    css_injected = 0

    for p in files:
        try:
            html = p.read_text(encoding="utf-8")
        except Exception:
            continue
        original = html

        # 1. URL fixes — but make sure we don't re-mangle canonical URLs.
        # Strategy: replace every match, then ensure canonicals remain.
        # Since canonical URL doesn't contain "affid=10704" duplicated elsewhere
        # and contains specific path "16-buy-peptides", the patterns above won't
        # match the canonical limitless URL (which has _ef_transaction_id= before affid)
        # — but to be safe, we PROTECT canonicals by tokenizing first.
        token_p = "\x00PARTICLE_GOOD\x00"
        token_l = "\x00LIMITLESS_GOOD\x00"
        html_t = html.replace(PARTICLE_GOOD, token_p).replace(LIMITLESS_GOOD, token_l)
        for pattern, replacement in URL_REPLACEMENTS:
            new_html, n = re.subn(pattern, replacement, html_t)
            if n > 0:
                html_t = new_html
                url_total_repls += n
        html = html_t.replace(token_p, PARTICLE_GOOD).replace(token_l, LIMITLESS_GOOD)
        if html != original:
            url_fixed_files += 1

        # 2. CSS injection: anywhere vendor-card HTML is used but CSS isn't defined.
        uses_classes = bool(re.search(r'class="[^"]*vendor-(card|btn)', html))
        has_css = ('id="vendor-cards-styles"' in html) or bool(re.search(r'\.vendor-cards?\s*\{', html))
        if uses_classes and not has_css and '</head>' in html:
            html = html.replace('</head>', f'{VENDOR_CARDS_CSS}\n</head>', 1)
            css_injected += 1

        if html != original:
            p.write_text(html, encoding="utf-8")

    print(f"URL fixes:            {url_fixed_files} files, {url_total_repls} total replacements")
    print(f"CSS injections:       {css_injected} files")


if __name__ == "__main__":
    main()
