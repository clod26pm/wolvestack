#!/usr/bin/env python3
"""Fast URL-only cleanup. Skips files that have no affiliate-keyword match."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANGS = ("en", "es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de", "nl", "ar")

PARTICLE_GOOD = "https://particlepeptides.com/en/16-buy-peptides?refs=25135"
LIMITLESS_GOOD = "https://www.limitlesslifenootropics.com/?_ef_transaction_id=&oid=1&affid=10704"

# Quick keyword to skip files that don't reference affiliates at all
QUICK_SCAN = re.compile(r'particlepeptides|limitless|ascensionsupplements')

# Patterns to replace (anchored carefully to avoid clobbering canonical URLs)
URL_REPLACEMENTS = [
    # particle: any URL ending refs=25135 that isn't the canonical /en/16-buy-peptides path
    (re.compile(r'https?://(?:www\.)?particlepeptides\.com/(?!en/16-buy-peptides)(?:en/)?\??[^"\s\']*?refs=25135[^"\s\']*'), PARTICLE_GOOD),
    # limitless typos (specific known wrong domains)
    (re.compile(r'https?://(?:www\.)?limitlesslifenoo\.com[^"\s\']*'), LIMITLESS_GOOD),
    (re.compile(r'https?://(?:www\.)?limitlesslifenotropics\.com[^"\s\']*'), LIMITLESS_GOOD),
    (re.compile(r'https?://(?:www\.)?limitlesslifebiotech\.com[^"\s\']*'), LIMITLESS_GOOD),
    (re.compile(r'https?://(?:www\.)?limitless-biohacking\.com[^"\s\']*'), LIMITLESS_GOOD),
    (re.compile(r'https?://(?:www\.)?limitless-peptides\.com[^"\s\']*'), LIMITLESS_GOOD),
    # limitless variant: limitlesslifenootropics.com (no www, no _ef_ tracking)
    (re.compile(r'https?://limitlesslifenootropics\.com/\?affid=10704'), LIMITLESS_GOOD),
    # ascension placeholder
    (re.compile(r'https?://(?:www\.)?ascensionsupplements\.com/\?ref=wolvestack'), PARTICLE_GOOD),
]

files = list(ROOT.glob("*.html"))
for lang in LANGS:
    files += list((ROOT / lang).glob("*.html"))

fixed_files = 0
total_repls = 0
scanned = 0

for p in files:
    try:
        html = p.read_text(encoding="utf-8")
    except Exception:
        continue
    scanned += 1
    if not QUICK_SCAN.search(html):
        continue
    original = html
    # Protect canonical URLs from being re-matched
    token_p = "\x00P\x00"
    token_l = "\x00L\x00"
    html = html.replace(PARTICLE_GOOD, token_p).replace(LIMITLESS_GOOD, token_l)
    for rx, replacement in URL_REPLACEMENTS:
        html, n = rx.subn(replacement, html)
        if n > 0:
            total_repls += n
    html = html.replace(token_p, PARTICLE_GOOD).replace(token_l, LIMITLESS_GOOD)
    if html != original:
        p.write_text(html, encoding="utf-8")
        fixed_files += 1

print(f"Scanned: {scanned}, Fixed: {fixed_files} files, {total_repls} replacements")
