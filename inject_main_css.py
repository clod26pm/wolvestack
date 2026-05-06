#!/usr/bin/env python3
"""
Critical fix: 1,686 pages on wolvestack.com are missing the main site CSS,
rendering as default browser HTML ("1995-look"). These are the thin/polish
template pages from the in-progress Haiku polish run.

Extract canonical main CSS block from bpc-157-guide.html (lines 162-488)
and inject it into every article page that doesn't already have it.

Idempotent — checks for `.nav-inner` rule presence before injecting.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Read canonical CSS block from a known-good page
canonical_path = ROOT / "bpc-157-guide.html"
if not canonical_path.exists():
    raise SystemExit(f"missing {canonical_path}")
canonical = canonical_path.read_text(encoding="utf-8")

# Match the FIRST <style>...</style> in bpc-157 (the main site CSS)
m = re.search(r'<style>\s*\n.*?</style>', canonical, re.DOTALL)
if not m:
    raise SystemExit("could not extract main CSS from bpc-157-guide.html")
MAIN_CSS = m.group(0)
print(f"Canonical CSS extracted: {len(MAIN_CSS)} chars")

LANGS = ("en", "es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de", "nl", "ar")
SKIP = {
    "404.html", "search.html", "ARTICLE-TEMPLATE.html", "TEMPLATE-CSS.html",
    "TEMPLATE-BODY.html", "category.html", "isitascam.html",
    "isitascam-privacy.html", "isitascam-support.html", "isitascam-terms.html",
}

# Inject CSS just BEFORE </head> (so it loads before the body renders)
# Skip pages that already have .nav-inner OR .article-hero rule (they have CSS).
def needs_inject(html: str) -> bool:
    # `.nav-inner` is the canary class for the canonical site template.
    # Pages with stripped-down inline CSS may have `.article-hero {` but
    # not `.nav-inner` — those still need the canonical CSS injected.
    if '.nav-inner' in html:
        return False
    return '</head>' in html


files = list(ROOT.glob("*.html"))
for lang in LANGS:
    files += list((ROOT / lang).glob("*.html"))

injected = 0
for p in files:
    if p.name in SKIP or "isitascam" in p.name or p.name.endswith("-legal.html"):
        continue
    try:
        html = p.read_text(encoding="utf-8")
    except Exception:
        continue
    if not needs_inject(html):
        continue
    new_html = html.replace('</head>', MAIN_CSS + '\n</head>', 1)
    p.write_text(new_html, encoding="utf-8")
    injected += 1

print(f"Injected main CSS into {injected} pages")
