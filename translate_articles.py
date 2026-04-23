#!/usr/bin/env python3
"""
WolveStack Article Translator
Translates untranslated HTML articles from English to 12 languages using Claude Haiku.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY="sk-ant-..."
    python translate_articles.py [--lang es] [--limit 10] [--concurrency 20] [--dry-run]

Options:
    --lang LANG       Translate only one language (e.g., es, zh, ja). Default: all 12
    --limit N         Only translate first N files per language (for testing)
    --concurrency N   Max parallel API calls (default: 20)
    --dry-run         Show what would be translated without calling API
    --resume          Skip files that appear already translated
"""

import os
import re
import sys
import json
import time
import asyncio
import argparse
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("ERROR: Install the anthropic package first:")
    print("  pip install anthropic")
    sys.exit(1)

# ─── Configuration ───────────────────────────────────────────────────────────

LANG_MAP = {
    'es': {'name': 'Spanish', 'attr': 'es'},
    'zh': {'name': 'Simplified Chinese', 'attr': 'zh-Hans'},
    'ja': {'name': 'Japanese', 'attr': 'ja'},
    'pt': {'name': 'Portuguese', 'attr': 'pt'},
    'ru': {'name': 'Russian', 'attr': 'ru'},
    'it': {'name': 'Italian', 'attr': 'it'},
    'pl': {'name': 'Polish', 'attr': 'pl'},
    'fr': {'name': 'French', 'attr': 'fr'},
    'id': {'name': 'Indonesian', 'attr': 'id'},
    'de': {'name': 'German', 'attr': 'de'},
    'nl': {'name': 'Dutch', 'attr': 'nl'},
    'ar': {'name': 'Arabic', 'attr': 'ar'},
}

# Preserve these terms untranslated
PRESERVE_TERMS = [
    'WolveStack', 'BPC-157', 'TB-500', 'CJC-1295', 'MK-677', 'PT-141',
    'GHK-Cu', 'SS-31', 'PE-22-28', 'P21', 'VIP', 'NAD+', 'IGF-1 LR3',
    'Ascension', 'Particle Peptides', 'Limitless Life Nootropics',
    'HPLC', 'FAQPage', 'JSON-LD',
]

BASE_DIR = Path(__file__).parent
EN_DIR = BASE_DIR / 'en'

# ─── Translation Logic ───────────────────────────────────────────────────────

def extract_translatable_parts(html_content):
    """Extract text that needs translation from HTML, preserving structure."""
    parts = {}

    # 1. Title tag
    m = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL)
    if m:
        parts['title'] = m.group(1)

    # 2. Meta description
    m = re.search(r'<meta\s+content="([^"]*?)"\s+name="description"', html_content)
    if not m:
        m = re.search(r'<meta\s+name="description"\s+content="([^"]*?)"', html_content)
    if m:
        parts['meta_desc'] = m.group(1)

    # 3. OG title & description
    m = re.search(r'<meta\s+content="([^"]*?)"\s+property="og:title"', html_content)
    if m:
        parts['og_title'] = m.group(1)
    m = re.search(r'<meta\s+content="([^"]*?)"\s+property="og:description"', html_content)
    if m:
        parts['og_desc'] = m.group(1)

    # 4. Body content (the main translatable block)
    body_match = re.search(r'(<body>)(.*?)(</body>)', html_content, re.DOTALL)
    if body_match:
        parts['body'] = body_match.group(2)

    return parts


def rebuild_html(original_html, translated_parts, target_lang, lang_attr):
    """Replace English text with translated text in the HTML."""
    result = original_html

    # Replace lang attribute
    result = re.sub(r'(<html[^>]*\s)lang="en"', f'\\1lang="{lang_attr}"', result)

    # Replace title
    if 'title' in translated_parts:
        result = re.sub(
            r'<title>.*?</title>',
            f'<title>{translated_parts["title"]}</title>',
            result, count=1, flags=re.DOTALL
        )

    # Replace meta description
    if 'meta_desc' in translated_parts:
        result = re.sub(
            r'(<meta\s+content=")([^"]*?)("\s+name="description")',
            f'\\1{translated_parts["meta_desc"]}\\3',
            result, count=1
        )
        result = re.sub(
            r'(<meta\s+name="description"\s+content=")([^"]*?)(")',
            f'\\1{translated_parts["meta_desc"]}\\3',
            result, count=1
        )

    # Replace OG tags
    if 'og_title' in translated_parts:
        result = re.sub(
            r'(<meta\s+content=")([^"]*?)("\s+property="og:title")',
            f'\\1{translated_parts["og_title"]}\\3',
            result, count=1
        )
    if 'og_desc' in translated_parts:
        result = re.sub(
            r'(<meta\s+content=")([^"]*?)("\s+property="og:description")',
            f'\\1{translated_parts["og_desc"]}\\3',
            result, count=1
        )

    # Replace body
    if 'body' in translated_parts:
        result = re.sub(
            r'(<body>).*?(</body>)',
            f'\\1{translated_parts["body"]}\\2',
            result, count=1, flags=re.DOTALL
        )

    return result


def is_already_translated(en_path, lang_path):
    """Check if a file is already genuinely translated."""
    if not lang_path.exists():
        return False

    with open(en_path, 'r', encoding='utf-8', errors='replace') as f:
        en_paras = re.findall(r'<p>(.*?)</p>', f.read(), re.DOTALL)
    with open(lang_path, 'r', encoding='utf-8', errors='replace') as f:
        lang_paras = re.findall(r'<p>(.*?)</p>', f.read(), re.DOTALL)

    if not en_paras or not lang_paras:
        return False

    en_sample = ' '.join(en_paras[:3])[:300]
    lang_sample = ' '.join(lang_paras[:3])[:300]

    return en_sample != lang_sample


async def translate_file(client, semaphore, en_path, lang_code, lang_info, stats):
    """Translate a single file."""
    fname = en_path.name
    lang_dir = BASE_DIR / lang_code
    lang_path = lang_dir / fname

    async with semaphore:
        try:
            with open(en_path, 'r', encoding='utf-8', errors='replace') as f:
                en_html = f.read()

            parts = extract_translatable_parts(en_html)
            if not parts.get('body'):
                stats['skipped'] += 1
                return

            # Build translation prompt
            # We send the body HTML and ask Haiku to translate text while preserving tags
            prompt = f"""Translate the following HTML content from English to {lang_info['name']}.

CRITICAL RULES:
1. Translate ALL visible text content (headings, paragraphs, list items, button text, labels)
2. DO NOT translate or modify: HTML tags, attributes, CSS classes, URLs, href values, src values
3. DO NOT translate brand names: WolveStack, Ascension, Particle Peptides, Limitless Life Nootropics
4. DO NOT translate peptide names (BPC-157, TB-500, CJC-1295, etc.) — keep them as-is
5. DO NOT translate technical abbreviations (HPLC, GMP, COA, FDA, etc.)
6. Preserve all HTML structure exactly as-is
7. Return ONLY the translated HTML — no explanations, no markdown, no code fences

<title>{parts.get('title', '')}</title>
<meta_description>{parts.get('meta_desc', '')}</meta_description>

<body_content>
{parts['body']}
</body_content>"""

            # Call Claude Haiku
            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=16000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text

            # Extract translated parts from response
            translated_parts = {}

            # Try to extract title
            title_match = re.search(r'<title>(.*?)</title>', response_text, re.DOTALL)
            if title_match:
                translated_parts['title'] = title_match.group(1)
                # Also use for OG tags
                translated_parts['og_title'] = title_match.group(1)

            # Try to extract meta description
            meta_match = re.search(r'<meta_description>(.*?)</meta_description>', response_text, re.DOTALL)
            if meta_match:
                translated_parts['meta_desc'] = meta_match.group(1)
                translated_parts['og_desc'] = meta_match.group(1)

            # Extract body content
            body_match = re.search(r'<body_content>(.*?)</body_content>', response_text, re.DOTALL)
            if body_match:
                translated_parts['body'] = body_match.group(1)
            else:
                # If Haiku didn't wrap in tags, use the whole response minus title/meta
                cleaned = response_text
                cleaned = re.sub(r'<title>.*?</title>', '', cleaned, flags=re.DOTALL)
                cleaned = re.sub(r'<meta_description>.*?</meta_description>', '', cleaned, flags=re.DOTALL)
                translated_parts['body'] = cleaned.strip()

            if not translated_parts.get('body'):
                stats['errors'] += 1
                print(f"  ERROR: Empty translation for {fname} → {lang_code}")
                return

            # Rebuild the HTML
            translated_html = rebuild_html(en_html, translated_parts, lang_code, lang_info['attr'])

            # Save
            lang_dir.mkdir(exist_ok=True)
            with open(lang_path, 'w', encoding='utf-8') as f:
                f.write(translated_html)

            # Also save to root if this is the default language variant
            root_path = BASE_DIR / fname
            # Root stays English, so we don't overwrite it

            stats['translated'] += 1
            stats['chars'] += len(parts['body'])
            stats['input_tokens'] += message.usage.input_tokens
            stats['output_tokens'] += message.usage.output_tokens

            if stats['translated'] % 25 == 0:
                cost = (stats['input_tokens'] / 1_000_000) * 0.80 + (stats['output_tokens'] / 1_000_000) * 4.00
                print(f"  [{lang_code}] {stats['translated']} done | "
                      f"${cost:.2f} spent | "
                      f"{stats['input_tokens']/1000:.0f}K in / {stats['output_tokens']/1000:.0f}K out tokens")

        except Exception as e:
            stats['errors'] += 1
            print(f"  ERROR translating {fname} → {lang_code}: {str(e)[:100]}")


async def translate_language(lang_code, lang_info, files_to_translate, concurrency, limit=None):
    """Translate all files for one language."""
    client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var
    semaphore = asyncio.Semaphore(concurrency)

    files = files_to_translate[:limit] if limit else files_to_translate

    stats = {
        'translated': 0, 'skipped': 0, 'errors': 0,
        'chars': 0, 'input_tokens': 0, 'output_tokens': 0
    }

    print(f"\n{'='*60}")
    print(f"Translating {len(files)} files to {lang_info['name']} ({lang_code})")
    print(f"{'='*60}")

    # Process in batches to avoid overwhelming the API
    batch_size = concurrency * 2
    for i in range(0, len(files), batch_size):
        batch = files[i:i + batch_size]
        tasks = [
            translate_file(client, semaphore, f, lang_code, lang_info, stats)
            for f in batch
        ]
        await asyncio.gather(*tasks)

    # Calculate costs (Haiku 3.5 pricing)
    cost = (stats['input_tokens'] / 1_000_000) * 0.80 + (stats['output_tokens'] / 1_000_000) * 4.00

    print(f"\n  {lang_info['name']} COMPLETE:")
    print(f"  Translated: {stats['translated']} | Skipped: {stats['skipped']} | Errors: {stats['errors']}")
    print(f"  Tokens: {stats['input_tokens']:,} in + {stats['output_tokens']:,} out")
    print(f"  Cost: ${cost:.2f}")

    return stats


def get_untranslated_files(lang_code, resume=True):
    """Get list of English files that need translation for a given language."""
    en_files = sorted(EN_DIR.glob('*.html'))
    en_files = [f for f in en_files if f.name != 'sitemap.xml']

    if not resume:
        return en_files

    untranslated = []
    for en_path in en_files:
        lang_path = BASE_DIR / lang_code / en_path.name
        if not is_already_translated(en_path, lang_path):
            untranslated.append(en_path)

    return untranslated


async def main():
    parser = argparse.ArgumentParser(description='Translate WolveStack articles using Claude Haiku')
    parser.add_argument('--lang', type=str, help='Single language code (e.g., es, zh)')
    parser.add_argument('--limit', type=int, help='Max files per language')
    parser.add_argument('--concurrency', type=int, default=20, help='Max parallel API calls')
    parser.add_argument('--dry-run', action='store_true', help='Show plan without translating')
    parser.add_argument('--resume', action='store_true', default=True, help='Skip already-translated files')
    args = parser.parse_args()

    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("ERROR: Set your ANTHROPIC_API_KEY environment variable first:")
        print("  export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    # Determine which languages to process
    if args.lang:
        if args.lang not in LANG_MAP:
            print(f"ERROR: Unknown language '{args.lang}'. Options: {', '.join(LANG_MAP.keys())}")
            sys.exit(1)
        languages = {args.lang: LANG_MAP[args.lang]}
    else:
        languages = LANG_MAP

    # Gather files to translate
    total_files = 0
    plan = {}
    for lang_code, lang_info in languages.items():
        files = get_untranslated_files(lang_code, resume=args.resume)
        plan[lang_code] = files
        total_files += len(files)
        print(f"{lang_info['name']:12s} ({lang_code}): {len(files)} files to translate")

    print(f"\nTotal: {total_files} files across {len(languages)} languages")

    if args.limit:
        effective = min(args.limit, max(len(f) for f in plan.values())) * len(languages)
        print(f"With --limit {args.limit}: ~{effective} files will be processed")

    if args.dry_run:
        print("\n[DRY RUN] No translations performed.")
        return

    # Translate
    start_time = time.time()
    total_stats = {
        'translated': 0, 'skipped': 0, 'errors': 0,
        'chars': 0, 'input_tokens': 0, 'output_tokens': 0
    }

    for lang_code, lang_info in languages.items():
        files = plan[lang_code]
        if not files:
            print(f"\n{lang_info['name']}: Nothing to translate, skipping.")
            continue

        stats = await translate_language(
            lang_code, lang_info, files,
            concurrency=args.concurrency,
            limit=args.limit
        )

        for k in total_stats:
            total_stats[k] += stats[k]

    # Final report
    elapsed = time.time() - start_time
    total_cost = (total_stats['input_tokens'] / 1_000_000) * 0.80 + \
                 (total_stats['output_tokens'] / 1_000_000) * 4.00

    print(f"\n{'='*60}")
    print(f"TRANSLATION COMPLETE")
    print(f"{'='*60}")
    print(f"Files translated: {total_stats['translated']}")
    print(f"Files skipped:    {total_stats['skipped']}")
    print(f"Errors:           {total_stats['errors']}")
    print(f"Total tokens:     {total_stats['input_tokens']:,} in + {total_stats['output_tokens']:,} out")
    print(f"Total cost:       ${total_cost:.2f}")
    print(f"Time elapsed:     {elapsed/60:.1f} minutes")
    print(f"\nNext steps:")
    print(f"  1. Spot-check a few translations in each language")
    print(f"  2. git add -A && git commit -m 'Translate articles to all languages'")
    print(f"  3. git push origin main")


if __name__ == '__main__':
    asyncio.run(main())
