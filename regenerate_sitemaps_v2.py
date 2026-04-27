#!/usr/bin/env python3
"""
Regenerate per-language sitemaps to match real indexable content.

Problem: pipeline finished pl/fr/id (and partially de/nl/ar) but their sitemaps
still only listed 10 URLs each from an old run. Google has no signal to
re-crawl the now-real-content pages, so the index still shows stub content.

Fix: rebuild each affected sitemap from disk — include every .html that doesn't
carry a noindex meta tag. Bump master sitemap.xml lastmod.

Usage:  python3 regenerate_sitemaps_v2.py
"""
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANGS = ["en", "es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de", "nl", "ar"]
BASE_URL = "https://wolvestack.com"
NOINDEX_RE = re.compile(r'<meta\s+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.IGNORECASE)
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def is_indexable(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:8000]
    except Exception:
        return False
    return not NOINDEX_RE.search(head)


def build_lang_sitemap(lang: str) -> int:
    lang_dir = ROOT / lang
    if not lang_dir.is_dir():
        return 0

    urls = []
    for f in sorted(lang_dir.iterdir()):
        if f.suffix != ".html":
            continue
        if f.name in {"sitemap.xml", "404.html", "search.html"}:
            continue
        if is_indexable(f):
            urls.append(f"{BASE_URL}/{lang}/{f.name}")

    parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url in urls:
        parts.append("  <url>")
        parts.append(f"    <loc>{url}</loc>")
        parts.append(f"    <lastmod>{TODAY}</lastmod>")
        parts.append("    <changefreq>weekly</changefreq>")
        parts.append("    <priority>0.7</priority>")
        parts.append("  </url>")
    parts.append("</urlset>")

    out = lang_dir / "sitemap.xml"
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return len(urls)


def update_master_sitemap(counts: dict[str, int]):
    parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    parts.append('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for lang in LANGS:
        if counts.get(lang, 0) == 0:
            continue
        parts.append("  <sitemap>")
        parts.append(f"    <loc>{BASE_URL}/{lang}/sitemap.xml</loc>")
        parts.append(f"    <lastmod>{TODAY}</lastmod>")
        parts.append("  </sitemap>")
    parts.append("</sitemapindex>")
    (ROOT / "sitemap.xml").write_text("\n".join(parts) + "\n", encoding="utf-8")


def main():
    counts = {}
    print(f"Regenerating sitemaps with lastmod={TODAY}\n")
    for lang in LANGS:
        n = build_lang_sitemap(lang)
        counts[lang] = n
        print(f"  {lang}: {n} URLs")
    update_master_sitemap(counts)
    print(f"\nMaster sitemap.xml updated.")
    print(f"Total indexable URLs across all languages: {sum(counts.values())}")


if __name__ == "__main__":
    main()
