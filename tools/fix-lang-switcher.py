#!/usr/bin/env python3
"""
fix-lang-switcher.py — rewrite the broken <div class="nav-lang-menu"> block
on every HTML page so each language anchor points to the correct /{lang}/
prefix instead of the page's own locale.

Bug context: across all 13 language directories, every page's language
dropdown had 13 anchors that all pointed to the page's own locale. So "click
Spanish on the English page" stayed on English. Hreflang validation broke
across the whole site.

Run from project root: python3 tools/fix-lang-switcher.py
Use --dry-run to preview changes without writing.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ['en','es','zh','ja','pt','ru','it','pl','fr','id','de','nl','ar']

# Match the lang menu block; non-greedy body capture
MENU_RE = re.compile(
    r'(<div class="nav-lang-menu">)(.*?)(</div>)',
    re.DOTALL
)

# Match each anchor inside the menu — captures href language, slug, label
ANCHOR_RE = re.compile(
    r'<a([^>]*?)href="/([a-z]{2})/([^"]+)"([^>]*)>([^<]*)</a>',
    re.DOTALL,
)

DRY_RUN = '--dry-run' in sys.argv


def fix_menu_block(body: str, page_lang: str) -> str | None:
    """Rewrite the 13 anchors inside the menu body. Returns None if the
    block doesn't have exactly 13 anchors or is otherwise unparseable."""
    anchors = list(ANCHOR_RE.finditer(body))
    if len(anchors) != 13:
        return None

    # All 13 anchors share the same slug (the page's filename) — extract it
    # from the first anchor.
    slug = anchors[0].group(3)
    if not slug or '/' in slug:
        return None

    # Preserve each anchor's original label (the language label is localized
    # per page — e.g. "Inglés" on Spanish pages).
    new_anchors = []
    for i, m in enumerate(anchors):
        target_lang = LANGS[i]
        label = m.group(5).strip()
        is_active = (target_lang == page_lang)
        cls = ' class="active"' if is_active else ''
        new_anchors.append(f'<a{cls} href="/{target_lang}/{slug}">{label}</a>')

    # Preserve a single newline between anchors for readability — original
    # files had each anchor on its own line.
    new_body = '\n' + '\n'.join(new_anchors) + '\n'
    return new_body


def fix_file(path: Path) -> bool:
    """Apply the fix to a single file. Returns True if anything changed."""
    text = path.read_text(encoding='utf-8')
    page_lang = path.parent.name
    if page_lang not in LANGS:
        return False

    def repl(m):
        body_old = m.group(2)
        body_new = fix_menu_block(body_old, page_lang)
        if body_new is None:
            return m.group(0)
        return m.group(1) + body_new + m.group(3)

    new_text = MENU_RE.sub(repl, text)
    if new_text == text:
        return False
    if not DRY_RUN:
        path.write_text(new_text, encoding='utf-8')
    return True


def main():
    fixed = 0
    scanned = 0
    skipped = 0
    for lang in LANGS:
        lang_dir = ROOT / lang
        if not lang_dir.is_dir():
            continue
        for html_file in sorted(lang_dir.glob('*.html')):
            scanned += 1
            try:
                if fix_file(html_file):
                    fixed += 1
            except Exception as e:
                skipped += 1
                print(f"SKIP {html_file}: {e}")

    label = '[DRY RUN] would fix' if DRY_RUN else 'fixed'
    print(f"Scanned {scanned} HTML files; {label} {fixed}; skipped {skipped} (errors)")


if __name__ == '__main__':
    main()
