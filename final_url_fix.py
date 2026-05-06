#!/usr/bin/env python3
"""Catch the final 383 'particlepeptides.com?refs=' URLs (no slash before ?)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANGS = ("en", "es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de", "nl", "ar")

PARTICLE_GOOD = "https://particlepeptides.com/en/16-buy-peptides?refs=25135"
LIMITLESS_GOOD = "https://www.limitlesslifenootropics.com/?_ef_transaction_id=&oid=1&affid=10704"

# Permissive: any particlepeptides URL containing refs=25135 that ISN'T already canonical
PARTICLE_BAD = re.compile(
    r'https?://(?:www\.)?particlepeptides\.com'
    r'(?!/en/16-buy-peptides\?refs=25135)'
    r'[^"\s\'<>]*?refs=25135[^"\s\'<>]*'
)
# Permissive limitless: anything that smells like a limitless typo
LIMITLESS_BAD = re.compile(
    r'https?://(?:www\.)?(?:limitlesslifenoo\.com|limitlesslifenotropics\.com|'
    r'limitlesslifebiotech\.com|limitless-biohacking\.com|limitless-peptides\.com)'
    r'[^"\s\'<>]*'
)
# Limitless without _ef_ tracking — upgrade
LIMITLESS_PLAIN = re.compile(
    r'https?://(?:www\.)?limitlesslifenootropics\.com/\?affid=10704'
)

files = list(ROOT.glob("*.html"))
for lang in LANGS:
    files += list((ROOT / lang).glob("*.html"))

fixed = 0
total_repls = 0
for p in files:
    try:
        html = p.read_text(encoding="utf-8")
    except Exception:
        continue
    if 'refs=25135' not in html and 'affid=10704' not in html and 'limitless' not in html.lower():
        continue
    original = html
    # Protect canonical URLs
    token_p = "\x00P\x00"
    token_l = "\x00L\x00"
    html = html.replace(PARTICLE_GOOD, token_p).replace(LIMITLESS_GOOD, token_l)
    html, n1 = PARTICLE_BAD.subn(PARTICLE_GOOD, html)
    html, n2 = LIMITLESS_BAD.subn(LIMITLESS_GOOD, html)
    html, n3 = LIMITLESS_PLAIN.subn(LIMITLESS_GOOD, html)
    html = html.replace(token_p, PARTICLE_GOOD).replace(token_l, LIMITLESS_GOOD)
    if html != original:
        p.write_text(html, encoding="utf-8")
        fixed += 1
        total_repls += n1 + n2 + n3

print(f"Fixed {fixed} files, {total_repls} replacements")
