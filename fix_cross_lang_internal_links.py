#!/usr/bin/env python3
"""
fix_cross_lang_internal_links.py — 2026-05-31

Fixes cross-language link bleed: foreign-language pages had ~4,700 anchor
tags pointing to /en/<slug>.html instead of /<lang>/<slug>.html. That's a
massive same-language internal-linking SEO leak.

Strategy: per language dir, rewrite `<a href="/en/<slug>.html"` →
`<a href="/<lang>/<slug>.html"` IF /<lang>/<slug>.html exists on disk.
"""
import re, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANGS = ['es', 'zh', 'ja', 'pt', 'ru', 'it', 'pl', 'fr', 'id', 'de', 'nl', 'ar']

# Match: <a ... href="/en/SLUG.html" ...>
LINK_RE = re.compile(
    r'(<a\b[^>]*?\bhref=")/en/([a-z0-9][a-z0-9\-]*\.html)("[^>]*>)',
    re.IGNORECASE,
)


def main():
    t0 = time.time()
    for lang in LANGS:
        lang_dir = ROOT / lang
        if not lang_dir.is_dir():
            continue
        existing_slugs = {p.name for p in lang_dir.glob('*.html')}
        n_files = 0
        n_changed = 0
        n_rewrites = 0
        for fp in lang_dir.glob('*.html'):
            try:
                src = fp.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            n_files += 1
            changes = [0]

            def repl(m):
                pre, slug, post = m.group(1), m.group(2), m.group(3)
                # Only rewrite if same-lang equivalent exists.
                if slug in existing_slugs:
                    changes[0] += 1
                    return f'{pre}/{lang}/{slug}{post}'
                return m.group(0)

            new = LINK_RE.sub(repl, src)
            if new != src:
                fp.write_text(new, encoding='utf-8')
                n_changed += 1
                n_rewrites += changes[0]
        print(f'{lang}: scanned={n_files}, files_changed={n_changed}, '
              f'links_rewritten={n_rewrites}')
    print(f'\nTotal elapsed: {time.time() - t0:.1f}s')


if __name__ == '__main__':
    main()
