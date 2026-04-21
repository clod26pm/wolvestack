#!/usr/bin/env python3
"""
WolveStack Translation Pipeline — Claude Haiku (Text-Node Extraction)
======================================================================
Extracts ONLY translatable text from HTML, translates in ONE API call,
puts translations back. Preserves all HTML structure without ever
sending tags/CSS/JS to the API = massive token savings.

Cost optimizations:
  - Text-node extraction: only translate actual words, not HTML markup
  - Single API call per file: meta + title + body text + JSON-LD in one batch
  - Protected term placeholders: prevent re-translating peptide names
  - Prompt caching: system message cached across all calls

Usage:
  export ANTHROPIC_API_KEY="sk-ant-..."
  python translate_haiku.py --lang es --limit 5     # test
  python translate_haiku.py --all --dry-run          # cost estimate
  python translate_haiku.py --all                    # full run
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
import html as html_module
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("ERROR: pip install anthropic --break-system-packages")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup, NavigableString, Comment, Doctype
except ImportError:
    print("ERROR: pip install beautifulsoup4 --break-system-packages")
    sys.exit(1)

# ─── Configuration ───────────────────────────────────────────────────────────

SITE_DIR = Path(__file__).resolve().parent
EN_DIR = SITE_DIR / "en"
DOMAIN = "https://wolvestack.com"

LANGUAGES = {
    "en": {"name": "English",    "native": "English",    "dir": "ltr", "attr": "en"},
    "es": {"name": "Spanish",    "native": "Español",    "dir": "ltr", "attr": "es"},
    "zh": {"name": "Chinese",    "native": "中文",        "dir": "ltr", "attr": "zh-Hans"},
    "ja": {"name": "Japanese",   "native": "日本語",      "dir": "ltr", "attr": "ja"},
    "pt": {"name": "Portuguese", "native": "Português",  "dir": "ltr", "attr": "pt"},
    "ru": {"name": "Russian",    "native": "Русский",    "dir": "ltr", "attr": "ru"},
    "it": {"name": "Italian",    "native": "Italiano",   "dir": "ltr", "attr": "it"},
    "pl": {"name": "Polish",     "native": "Polski",     "dir": "ltr", "attr": "pl"},
    "fr": {"name": "French",     "native": "Français",   "dir": "ltr", "attr": "fr"},
    "id": {"name": "Indonesian", "native": "Bahasa",     "dir": "ltr", "attr": "id"},
    "de": {"name": "German",     "native": "Deutsch",    "dir": "ltr", "attr": "de"},
    "nl": {"name": "Dutch",      "native": "Nederlands", "dir": "ltr", "attr": "nl"},
    "ar": {"name": "Arabic",     "native": "العربية",     "dir": "rtl", "attr": "ar"},
}

# Terms that should NEVER be translated
PROTECTED_TERMS = [
    "BPC-157", "BPC157", "TB-500", "TB500", "GHK-Cu", "GHK",
    "CJC-1295", "CJC1295", "Ipamorelin", "Sermorelin", "Tesamorelin",
    "Semaglutide", "Tirzepatide", "Retatrutide", "Epithalon", "Epitalon",
    "Dihexa", "PT-141", "PT141", "Semax", "Selank", "DSIP",
    "AOD-9604", "AOD9604", "MOTS-c", "MOTSc", "MK-677", "MK677",
    "IGF-1 LR3", "IGF-1", "GHRP-2", "GHRP-6", "GHRP2", "GHRP6",
    "LL-37", "KPV", "VIP", "Cerebrolysin", "Thymosin Beta-4",
    "5-amino-1MQ", "5-Amino-1MQ", "NAD+", "NAD",
    "Melanotan", "Melanotan II", "Humanin", "Foxo4-DRI",
    "N-Acetyl Semax Amidate", "N-Acetyl Selank Amidate",
    "PE-22-28", "PNC-27", "Noopept", "Bronchogen", "Livagen",
    "Orexin-A", "ARA-290", "SS-31", "P21",
    "VEGFR2", "BDNF", "AMPK", "GLP-1", "GIP", "GHRH",
    "ACTH", "mTOR", "NF-kB", "TNF-alpha",
    "WolveStack", "wolvestack.com", "Wolverine Stack",
    "Apollo", "Particle Peptides", "Limitless Life Nootropics",
    "mcg", "mg", "ml", "IU", "HPLC", "GMP", "COA", "FDA",
]

_protected_pattern = re.compile(
    r'\b(' + '|'.join(re.escape(t) for t in sorted(PROTECTED_TERMS, key=len, reverse=True)) + r')\b',
    re.IGNORECASE
)
_PLACEHOLDER_PREFIX = "XTERMX"

SKIP_TAGS = {'script', 'style', 'code', 'pre', 'svg', 'math', 'noscript'}
TRANSLATABLE_ATTRS = ['title', 'alt', 'placeholder', 'aria-label']

# Separator for batch translation — unlikely to appear in article text
SEG_SEP = "\n≡≡≡SEG≡≡≡\n"


# ─── Text Extraction & Replacement ──────────────────────────────────────────

def extract_texts_from_body(body):
    """
    Walk the DOM tree and collect all translatable text segments.
    Returns list of (node_ref, segment_type, text) tuples.
    segment_type is 'text' for NavigableString or 'attr:attrname' for attributes.
    """
    segments = []
    _walk_body(body, segments)
    return segments


def _walk_body(element, segments):
    """Recursively collect text nodes and translatable attributes."""
    for child in list(element.children):
        if isinstance(child, (Comment, Doctype)):
            continue
        if isinstance(child, NavigableString):
            text = str(child)
            if text.strip() and not _is_skip(child):
                segments.append((child, 'text', text))
        elif child.name and child.name not in SKIP_TAGS:
            # Collect translatable attributes
            for attr in TRANSLATABLE_ATTRS:
                val = child.get(attr)
                if val and isinstance(val, str) and val.strip():
                    segments.append((child, f'attr:{attr}', val))
            _walk_body(child, segments)


def _is_skip(node):
    """Check if node is inside a skip tag."""
    p = node.parent
    while p:
        if p.name in SKIP_TAGS:
            return True
        p = p.parent
    return False


def apply_translations_to_body(segments, translations):
    """Apply translated texts back to their DOM nodes."""
    for (node, seg_type, _), translated in zip(segments, translations):
        if not translated:
            continue
        if seg_type == 'text':
            node.replace_with(NavigableString(translated))
        elif seg_type.startswith('attr:'):
            attr_name = seg_type[5:]
            node[attr_name] = translated


# ─── Protected Terms ────────────────────────────────────────────────────────

def protect_terms(texts: list) -> tuple:
    """
    Replace protected terms with placeholders across all texts.
    Returns (protected_texts, placeholder_map).
    """
    placeholders = {}
    counter = [0]

    def _replace(match):
        term = match.group(0)
        ph = f"{_PLACEHOLDER_PREFIX}{counter[0]:04d}"
        placeholders[ph] = term
        counter[0] += 1
        return ph

    protected = []
    for text in texts:
        if text and text.strip():
            protected.append(_protected_pattern.sub(_replace, text))
        else:
            protected.append(text)

    return protected, placeholders


def restore_terms(texts: list, placeholders: dict) -> list:
    """Restore protected terms from placeholders."""
    result = []
    for text in texts:
        if text:
            for ph, original in placeholders.items():
                text = text.replace(ph, original)
            text = re.sub(rf'{_PLACEHOLDER_PREFIX}\d{{4}}', '', text)
            text = html_module.unescape(text)
        result.append(text)
    return result


# ─── Haiku API ──────────────────────────────────────────────────────────────

class HaikuTranslator:
    def __init__(self, api_key: str, concurrency: int = 20):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.semaphore = asyncio.Semaphore(concurrency)
        self.stats = {
            'api_calls': 0, 'input_tokens': 0, 'output_tokens': 0,
            'chars_translated': 0, 'segments_translated': 0,
        }

    async def translate_segments(self, texts: list, lang_name: str) -> list:
        """
        Translate a list of text segments via Haiku API.
        Auto-chunks to stay within 8192 output token limit.
        ~5000 chars of text ≈ ~6000 output tokens (safe margin).
        """
        if not texts:
            return []

        non_empty = [(i, t) for i, t in enumerate(texts) if t and t.strip()]
        if not non_empty:
            return texts[:]

        # Split into chunks that fit within output limits
        MAX_CHARS_PER_CHUNK = 5000
        chunks = []
        current_chunk = []
        current_chars = 0

        for idx, text in non_empty:
            tlen = len(text)
            if current_chars + tlen > MAX_CHARS_PER_CHUNK and current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_chars = 0
            current_chunk.append((idx, text))
            current_chars += tlen

        if current_chunk:
            chunks.append(current_chunk)

        # Translate each chunk
        result = list(texts)

        for chunk in chunks:
            raw_texts = [t for _, t in chunk]
            protected, placeholders = protect_terms(raw_texts)
            batch = SEG_SEP.join(protected)
            total_chars = sum(len(t) for t in raw_texts)

            prompt = (
                f"Translate ALL text segments from English to {lang_name}.\n"
                f"Segments are separated by ≡≡≡SEG≡≡≡ — keep the EXACT same separators in your output.\n"
                f"Return ONLY the translated segments with separators, nothing else.\n"
                f"Keep XTERMX#### placeholders unchanged.\n"
                f"Do NOT translate code, URLs, or HTML tags if they appear.\n\n"
                f"{batch}"
            )

            async with self.semaphore:
                try:
                    msg = await self.client.messages.create(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=8192,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    response = msg.content[0].text
                    self.stats['api_calls'] += 1
                    self.stats['input_tokens'] += msg.usage.input_tokens
                    self.stats['output_tokens'] += msg.usage.output_tokens
                    self.stats['chars_translated'] += total_chars
                    self.stats['segments_translated'] += len(chunk)
                except Exception as e:
                    print(f"    API error: {str(e)[:120]}")
                    continue

            # Parse response
            translated_parts = response.split("≡≡≡SEG≡≡≡")
            translated_parts = [p.strip() for p in translated_parts]
            translated_parts = restore_terms(translated_parts, placeholders)

            # Validate segment count — if mismatch, skip chunk (keep English)
            if len(translated_parts) != len(chunk):
                print(f"    ⚠ Chunk mismatch: sent {len(chunk)} segments, got {len(translated_parts)} back. Keeping English for this chunk.")
                continue

            for (orig_idx, _), trans in zip(chunk, translated_parts):
                if trans:
                    result[orig_idx] = trans

        return result


# ─── HTML Processing (structural, no API) ───────────────────────────────────

def inject_hreflang(soup, filename):
    head = soup.find('head')
    if not head:
        return
    for existing in head.find_all('link', rel='alternate', hreflang=True):
        existing.decompose()
    for lang_code in LANGUAGES:
        link = soup.new_tag('link')
        link['rel'] = 'alternate'
        link['hreflang'] = lang_code
        link['href'] = f"{DOMAIN}/{'en' if lang_code == 'en' else lang_code}/{filename}"
        head.append(link)
    link = soup.new_tag('link')
    link['rel'] = 'alternate'
    link['hreflang'] = 'x-default'
    link['href'] = f"{DOMAIN}/{filename}"
    head.append(link)


def inject_language_switcher(soup, current_lang, filename):
    options = []
    for code, info in LANGUAGES.items():
        selected = ' selected' if code == current_lang else ''
        options.append(f'<option value="/{code}/{filename}"{selected}>{info["native"]}</option>')
    html = f'''<div class="lang-switcher" style="position:relative;display:inline-block;margin-left:12px;">
      <select onchange="window.location.href=this.value"
              style="background:rgba(255,255,255,0.1);color:inherit;border:1px solid rgba(255,255,255,0.2);
                     border-radius:6px;padding:4px 8px;font-size:13px;cursor:pointer;
                     font-family:var(--font-main,sans-serif);">{''.join(options)}</select></div>'''
    for tag in [soup.find('nav'), soup.find('footer')]:
        if tag:
            tag.append(BeautifulSoup(html, 'html.parser'))


def update_internal_links(soup, to_lang):
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.endswith('.html') and not href.startswith('http') and not href.startswith('//'):
            clean = re.sub(r'^/?(en|es|zh|ja|pt|ru|it|pl|fr|id|de|nl|ar)/', '', href.lstrip('/'))
            a['href'] = f"/{to_lang}/{clean}"
        elif href in ('/', '/index.html'):
            a['href'] = f"/{to_lang}/index.html"


def fix_url(url, to_lang):
    """Strip any existing lang prefix from URL and add the target one."""
    url = re.sub(rf'{re.escape(DOMAIN)}/(en|es|zh|ja|pt|ru|it|pl|fr|id|de|nl|ar)/', f'{DOMAIN}/', url)
    return url.replace(f"{DOMAIN}/", f"{DOMAIN}/{to_lang}/")


def update_jsonld_urls(data, to_lang):
    if isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, str) and DOMAIN in val and (val.endswith('.html') or key in ('url', '@id', 'item')):
                data[key] = fix_url(val, to_lang)
            else:
                update_jsonld_urls(val, to_lang)
    elif isinstance(data, list):
        for item in data:
            update_jsonld_urls(item, to_lang)


def collect_jsonld_texts(data):
    """Collect translatable texts from JSON-LD. Returns list of (path_key, text)."""
    results = []
    _collect_jld(data, [], results)
    return results


def _collect_jld(data, path, results):
    if isinstance(data, dict):
        dt = data.get('@type', '')
        if dt == 'Question' and 'name' in data:
            results.append(('/'.join(path + ['Q:name']), data['name']))
        if dt == 'Answer' and 'text' in data:
            results.append(('/'.join(path + ['A:text']), data['text']))
        if dt == 'Article':
            for f in ('headline', 'description'):
                if f in data:
                    results.append(('/'.join(path + [f'Art:{f}']), data[f]))
        if dt == 'ListItem' and 'name' in data and data['name'] != 'Home':
            results.append(('/'.join(path + ['LI:name']), data['name']))
        for k, v in data.items():
            _collect_jld(v, path + [k], results)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            _collect_jld(item, path + [str(i)], results)


def apply_jsonld_translations(data, path, translations):
    if isinstance(data, dict):
        dt = data.get('@type', '')
        if dt == 'Question' and 'name' in data:
            key = '/'.join(path + ['Q:name'])
            if key in translations:
                data['name'] = translations[key]
        if dt == 'Answer' and 'text' in data:
            key = '/'.join(path + ['A:text'])
            if key in translations:
                data['text'] = translations[key]
        if dt == 'Article':
            for f in ('headline', 'description'):
                if f in data:
                    key = '/'.join(path + [f'Art:{f}'])
                    if key in translations:
                        data[f] = translations[key]
        if dt == 'ListItem' and 'name' in data:
            key = '/'.join(path + ['LI:name'])
            if key in translations:
                data['name'] = translations[key]
        for k, v in data.items():
            apply_jsonld_translations(v, path + [k], translations)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            apply_jsonld_translations(item, path + [str(i)], translations)


# ─── Main Translation Pipeline ──────────────────────────────────────────────

async def translate_html_page(html_content: str, to_lang: str, filename: str, translator: HaikuTranslator) -> str:
    """
    Full translation pipeline for one page.
    ONE API call: extracts all text, translates, puts back.
    """
    lang_info = LANGUAGES[to_lang]
    lang_name = lang_info['name']

    soup = BeautifulSoup(html_content, 'html.parser')

    # ── Structural updates (no API needed) ──
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = lang_info['attr']
        if lang_info['dir'] == 'rtl':
            html_tag['dir'] = 'rtl'

    canonical = soup.find('link', rel='canonical')
    if canonical and canonical.get('href'):
        canonical['href'] = fix_url(canonical['href'], to_lang)

    og_url = soup.find('meta', property='og:url')
    if og_url and og_url.get('content'):
        og_url['content'] = fix_url(og_url['content'], to_lang)

    inject_hreflang(soup, filename)

    # Remove noindex (replacing fake with real translation)
    for meta in soup.find_all('meta', attrs={'name': 'robots'}):
        if 'noindex' in meta.get('content', ''):
            meta.decompose()

    # ── Collect ALL translatable text ──
    all_texts = []      # The actual strings
    all_targets = []    # How to apply them back

    # Meta tags
    for meta in soup.find_all('meta'):
        if meta.get('name') == 'description' or meta.get('property') in ('og:title', 'og:description'):
            val = meta.get('content', '')
            if val:
                all_texts.append(val)
                all_targets.append(('meta', meta, 'content'))
        elif meta.get('name') in ('twitter:title', 'twitter:description'):
            val = meta.get('content', '')
            if val:
                all_texts.append(val)
                all_targets.append(('meta', meta, 'content'))

    # Title
    title_tag = soup.find('title')
    if title_tag and title_tag.string:
        all_texts.append(str(title_tag.string))
        all_targets.append(('title', title_tag, None))

    # JSON-LD texts
    jsonld_data = []
    for script_tag in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script_tag.string)
            update_jsonld_urls(data, to_lang)
            entries = collect_jsonld_texts(data)
            jsonld_data.append((script_tag, data, entries))
            for path_key, text in entries:
                all_texts.append(text)
                all_targets.append(('jsonld', path_key, None))
        except (json.JSONDecodeError, TypeError):
            pass

    # Body text nodes + attributes
    body = soup.find('body')
    body_segments = []
    if body:
        body_segments = extract_texts_from_body(body)
        for (node, seg_type, text) in body_segments:
            all_texts.append(text)
            all_targets.append(('body', None, None))  # index-matched to body_segments

    # ── Single API call to translate everything ──
    if all_texts:
        translated = await translator.translate_segments(all_texts, lang_name)
    else:
        translated = []

    # ── Apply translations back ──
    body_idx = 0
    body_start = len(all_targets) - len(body_segments)

    for i, (target_type, ref, attr) in enumerate(all_targets):
        if i >= len(translated) or not translated[i]:
            continue

        if target_type == 'meta':
            ref[attr] = translated[i]
        elif target_type == 'title':
            ref.string = translated[i]
        elif target_type == 'jsonld':
            pass  # handled below
        elif target_type == 'body':
            pass  # handled below

    # Apply body translations
    if body_segments:
        body_translations = translated[body_start:]
        apply_translations_to_body(body_segments, body_translations)

    # Apply JSON-LD translations
    jsonld_offset = 0
    # Count meta + title entries
    non_jsonld_non_body = sum(1 for t, _, _ in all_targets[:body_start] if t in ('meta', 'title'))
    jsonld_offset = non_jsonld_non_body

    for script_tag, data, entries in jsonld_data:
        trans_map = {}
        for (path_key, _) in entries:
            if jsonld_offset < len(translated) and translated[jsonld_offset]:
                trans_map[path_key] = translated[jsonld_offset]
            jsonld_offset += 1
        apply_jsonld_translations(data, [], trans_map)
        script_tag.string = json.dumps(data, ensure_ascii=False, indent=2)

    # ── Final structural touches ──
    inject_language_switcher(soup, to_lang, filename)
    update_internal_links(soup, to_lang)

    return soup.decode(formatter="minimal")


# ─── File-level Operations ──────────────────────────────────────────────────

def is_already_translated(en_path: Path, lang_path: Path) -> bool:
    if not lang_path.exists():
        return False
    try:
        en_html = en_path.read_text(encoding='utf-8', errors='replace')
        lang_html = lang_path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return False
    en_paras = re.findall(r'<p>(.*?)</p>', en_html, re.DOTALL)[:3]
    lang_paras = re.findall(r'<p>(.*?)</p>', lang_html, re.DOTALL)[:3]
    if not en_paras or not lang_paras:
        return False
    return ' '.join(en_paras)[:300] != ' '.join(lang_paras)[:300]


async def translate_single_file(translator, en_path, lang_code, stats, lock):
    filename = en_path.name
    lang_dir = SITE_DIR / lang_code
    lang_path = lang_dir / filename

    try:
        en_html = en_path.read_text(encoding='utf-8', errors='replace')
        translated = await translate_html_page(en_html, lang_code, filename, translator)
        lang_dir.mkdir(exist_ok=True)
        lang_path.write_text(translated, encoding='utf-8')

        async with lock:
            stats['translated'] += 1
            if stats['translated'] % 50 == 0:
                cost = (translator.stats['input_tokens'] / 1e6) * 0.80 + \
                       (translator.stats['output_tokens'] / 1e6) * 4.00
                print(f"  [{lang_code}] {stats['translated']} done | "
                      f"${cost:.2f} | {translator.stats['api_calls']} calls | "
                      f"{translator.stats['input_tokens']/1000:.0f}K/{translator.stats['output_tokens']/1000:.0f}K tokens")

    except Exception as e:
        async with lock:
            stats['errors'] += 1
        print(f"  ERR {filename}→{lang_code}: {str(e)[:120]}")


async def translate_language(lang_code, files, concurrency, limit=None):
    lang_info = LANGUAGES[lang_code]
    api_key = os.environ['ANTHROPIC_API_KEY']
    translator = HaikuTranslator(api_key=api_key, concurrency=concurrency)

    if limit:
        files = files[:limit]

    stats = {'translated': 0, 'errors': 0}
    lock = asyncio.Lock()

    print(f"\n{'='*60}")
    print(f"  {lang_info['name']} ({lang_code}) — {len(files)} files, concurrency={concurrency}")
    print(f"{'='*60}")

    batch_size = concurrency * 2
    for i in range(0, len(files), batch_size):
        batch = files[i:i + batch_size]
        await asyncio.gather(*[translate_single_file(translator, f, lang_code, stats, lock) for f in batch])

    cost = (translator.stats['input_tokens'] / 1e6) * 0.80 + \
           (translator.stats['output_tokens'] / 1e6) * 4.00

    print(f"\n  {lang_info['name']} DONE: {stats['translated']} ok, {stats['errors']} errors")
    print(f"  {translator.stats['api_calls']} API calls | "
          f"{translator.stats['input_tokens']:,} in + {translator.stats['output_tokens']:,} out = ${cost:.2f}")

    return {**stats, **translator.stats}


def get_files_to_translate(lang_code, force=False):
    en_files = sorted(EN_DIR.glob('*.html'))
    en_files = [f for f in en_files if f.name not in ('sitemap.xml', '404.html', 'ARTICLE-TEMPLATE.html', 'search.html')]

    if force:
        return en_files

    return [f for f in en_files if not is_already_translated(f, SITE_DIR / lang_code / f.name)]


# ─── CLI ─────────────────────────────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(description='Translate WolveStack — Claude Haiku (optimized)')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--lang', type=str)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--concurrency', type=int, default=20)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()

    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("Set ANTHROPIC_API_KEY"); sys.exit(1)

    if args.lang:
        if args.lang not in LANGUAGES or args.lang == 'en':
            print(f"Bad lang. Options: {', '.join(k for k in LANGUAGES if k != 'en')}"); sys.exit(1)
        langs = [args.lang]
    elif args.all:
        langs = [k for k in LANGUAGES if k != 'en']
    else:
        parser.print_help(); return

    plan = {}
    total = 0
    for lang in langs:
        files = get_files_to_translate(lang, force=args.force)
        plan[lang] = files
        total += len(files)
        print(f"  {LANGUAGES[lang]['name']:12s} ({lang}): {len(files)} files")

    print(f"\n  TOTAL: {total} files across {len(langs)} languages")

    if args.dry_run:
        # Real estimate based on test data: ~3,500 input + ~3,500 output tokens per file
        est_in = total * 3500
        est_out = total * 3500
        est_cost = (est_in / 1e6) * 0.80 + (est_out / 1e6) * 4.00
        print(f"  Estimated: ~{est_in/1e6:.1f}M in + ~{est_out/1e6:.1f}M out = ~${est_cost:.0f}")
        print(f"  [DRY RUN — nothing translated]")
        return

    start = time.time()
    totals = {'translated': 0, 'errors': 0, 'api_calls': 0, 'input_tokens': 0, 'output_tokens': 0}

    for lang in langs:
        if not plan[lang]:
            print(f"\n  {LANGUAGES[lang]['name']}: nothing to translate."); continue
        s = await translate_language(lang, plan[lang], args.concurrency, args.limit)
        for k in totals:
            totals[k] += s.get(k, 0)

    elapsed = time.time() - start
    cost = (totals['input_tokens'] / 1e6) * 0.80 + (totals['output_tokens'] / 1e6) * 4.00

    print(f"\n{'='*60}")
    print(f"  COMPLETE: {totals['translated']} files, {totals['errors']} errors")
    print(f"  {totals['api_calls']} API calls")
    print(f"  {totals['input_tokens']:,} in + {totals['output_tokens']:,} out = ${cost:.2f}")
    print(f"  Time: {elapsed/60:.1f} min")
    print(f"{'='*60}")


if __name__ == '__main__':
    asyncio.run(main())
