#!/usr/bin/env python3
"""
Two real bugs:
1. The 'Ascension' (apollo-card) vendor card text mismatch — its href was replaced
   with the Particle URL by URL normalization, but the card still says "Shop Ascension"
   and brand-text "Ascension". Visible site-wide as a broken/inconsistent card.
   Fix: remove the apollo-card entirely; keep just Particle + Limitless.
2. /cookie-banner.js gets 301'd by the catchall to /en/cookie-banner.js. Add an
   explicit exception in _redirects.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANGS = ("en", "es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de", "nl", "ar")

# Pattern: the entire apollo-card vendor div block (before the particle-card)
APOLLO_CARD_RX = re.compile(
    r'<div\s+class="vendor-card\s+apollo-card">\s*'
    r'<h3>[^<]*</h3>\s*'
    r'<p>[^<]*</p>\s*'
    r'<a\s+class="vendor-btn\s+apollo-btn"[^>]*>[^<]*</a>\s*'
    r'</div>\s*',
    re.DOTALL | re.IGNORECASE,
)

files = list(ROOT.glob("*.html"))
for lang in LANGS:
    files += list((ROOT / lang).glob("*.html"))

apollo_removed_files = 0
apollo_total = 0
for p in files:
    try:
        html = p.read_text(encoding="utf-8")
    except Exception:
        continue
    if 'apollo-card' not in html:
        continue
    new_html, n = APOLLO_CARD_RX.subn('', html)
    if n > 0:
        p.write_text(new_html, encoding="utf-8")
        apollo_removed_files += 1
        apollo_total += n

print(f"Removed apollo-card from {apollo_removed_files} files ({apollo_total} blocks)")

# Update _redirects with cookie-banner.js exception
red = ROOT / "_redirects"
content = red.read_text(encoding="utf-8")
needle = "/cookie-banner.js"
if needle not in content:
    # Insert RIGHT AFTER the IIAS terms exception (a reliable anchor)
    anchor = "/isitascam-terms.html   /isitascam-terms.html              200"
    if anchor in content:
        replacement = anchor + "\n\n# Cookie consent banner — must be served at root, not redirected to /en/\n/cookie-banner.js       /cookie-banner.js                  200"
        content = content.replace(anchor, replacement, 1)
        red.write_text(content, encoding="utf-8")
        print("Added /cookie-banner.js exception to _redirects")
    else:
        print("WARN: anchor not found, /cookie-banner.js exception NOT added")
else:
    print("/cookie-banner.js exception already present")
