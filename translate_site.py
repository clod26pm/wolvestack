#!/usr/bin/env python3
"""
WolveStack Multilingual Translation Pipeline
=============================================
Translates ~1,900 HTML pages into 12 languages using argostranslate (free, offline).

Architecture:
  - Parses HTML with BeautifulSoup, only translates text nodes
  - Preserves all HTML structure, CSS, JS, JSON-LD
  - Protects peptide terminology from mistranslation
  - Updates canonical URLs, og:url, hreflang tags
  - Injects language switcher into nav + footer
  - Generates per-language sitemaps

Usage:
  # First-time setup
  pip3 install argostranslate beautifulsoup4 --break-system-packages
  python3 translate_site.py --install-languages

  # Translate everything (skip existing)
  python3 translate_site.py --all

  # Translate specific language
  python3 translate_site.py --lang es

  # Translate specific file to all languages
  python3 translate_site.py --file bpc-157-guide.html

  # Force re-translate (overwrite existing)
  python3 translate_site.py --all --force
"""

import argparse
import hashlib
import html as html_module
import json
import os
import re
import sys
import time
from copy import copy
from pathlib import Path
from html.parser import HTMLParser

from bs4 import BeautifulSoup, NavigableString, Comment, Doctype

# ─── Config ────────────────────────────────────────────────────────────────────
SITE_DIR = Path(__file__).resolve().parent / "peptide-daily-content"
DOMAIN = "https://wolvestack.com"

LANGUAGES = {
    "en": {"name": "English",    "native": "English",    "dir": "ltr"},
    "es": {"name": "Spanish",    "native": "Español",    "dir": "ltr"},
    "zh": {"name": "Chinese",    "native": "中文",        "dir": "ltr"},
    "ja": {"name": "Japanese",   "native": "日本語",      "dir": "ltr"},
    "pt": {"name": "Portuguese", "native": "Português",  "dir": "ltr"},
    "ru": {"name": "Russian",    "native": "Русский",    "dir": "ltr"},
    "it": {"name": "Italian",    "native": "Italiano",   "dir": "ltr"},
    "pl": {"name": "Polish",     "native": "Polski",     "dir": "ltr"},
    "fr": {"name": "French",     "native": "Français",   "dir": "ltr"},
    "id": {"name": "Indonesian", "native": "Bahasa",     "dir": "ltr"},
    "de": {"name": "German",     "native": "Deutsch",    "dir": "ltr"},
    "nl": {"name": "Dutch",      "native": "Nederlands", "dir": "ltr"},
    "ar": {"name": "Arabic",     "native": "العربية",     "dir": "rtl"},
}

# Argos language codes (some differ from ISO)
ARGOS_LANG_MAP = {
    "en": "en", "es": "es", "zh": "zh", "ja": "ja", "pt": "pt",
    "ru": "ru", "it": "it", "pl": "pl", "fr": "fr", "id": "id",
    "de": "de", "nl": "nl", "ar": "ar",
}

# Terms that should NEVER be translated (peptide names, brand names, units)
PROTECTED_TERMS = [
    # Peptide names
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
    "Orexin-A", "ARA-290",
    # Scientific terms that should stay English
    "VEGFR2", "BDNF", "AMPK", "GLP-1", "GIP", "GHRH",
    "ACTH", "mTOR", "IGF-1", "NF-kB", "TNF-alpha",
    # Brand/site names
    "WolveStack", "wolvestack.com", "Wolverine Stack",
    # Units
    "mcg", "mg", "ml", "IU",
    # Supplier names
    "Apollo", "Particle Peptides", "Limitless Life Nootropics",
]

# Build regex for protected terms (case-insensitive)
_protected_pattern = re.compile(
    r'\b(' + '|'.join(re.escape(t) for t in sorted(PROTECTED_TERMS, key=len, reverse=True)) + r')\b',
    re.IGNORECASE
)

# Placeholder format for protecting terms during translation
_PLACEHOLDER_PREFIX = "XTERMX"

# ─── Translation Engine ───────────────────────────────────────────────────────

_translators = {}  # Cache: (from_lang, to_lang) -> translator


def _get_translator(from_lang: str, to_lang: str):
    """Get or create an Argos translator for a language pair."""
    key = (from_lang, to_lang)
    if key not in _translators:
        import argostranslate.translate
        _translators[key] = argostranslate.translate.get_translation_from_codes(
            ARGOS_LANG_MAP[from_lang], ARGOS_LANG_MAP[to_lang]
        )
    return _translators[key]


def translate_text(text: str, to_lang: str, from_lang: str = "en") -> str:
    """
    Translate a text string while protecting peptide terminology.
    Returns the translated text with protected terms restored.
    """
    if not text or not text.strip():
        return text
    if to_lang == from_lang:
        return text

    # Step 1: Replace protected terms with placeholders
    placeholders = {}
    counter = [0]

    def _replace_protected(match):
        term = match.group(0)
        placeholder = f"{_PLACEHOLDER_PREFIX}{counter[0]:04d}"
        placeholders[placeholder] = term
        counter[0] += 1
        return placeholder

    protected_text = _protected_pattern.sub(_replace_protected, text)

    # Step 2: Translate
    translator = _get_translator(from_lang, to_lang)
    if translator is None:
        print(f"    ⚠ No translator for {from_lang}→{to_lang}, keeping original")
        return text

    try:
        translated = translator.translate(protected_text)
    except Exception as e:
        print(f"    ⚠ Translation error: {e}")
        return text

    # Step 3: Restore protected terms
    for placeholder, original_term in placeholders.items():
        translated = translated.replace(placeholder, original_term)

    # Clean up any remaining placeholders (shouldn't happen but safety net)
    translated = re.sub(rf'{_PLACEHOLDER_PREFIX}\d{{4}}', '', translated)

    # Step 4: Unescape HTML entities that the translation engine may have introduced
    # (e.g. &amp; → &) so BeautifulSoup doesn't double-encode them to &amp;amp;
    translated = html_module.unescape(translated)

    return translated


# ─── HTML Processing ──────────────────────────────────────────────────────────

# Tags whose text content should NOT be translated
SKIP_TAGS = {'script', 'style', 'code', 'pre', 'svg', 'math', 'noscript'}

# Attributes that contain translatable text
TRANSLATABLE_ATTRS = ['content', 'title', 'alt', 'placeholder', 'aria-label']


def translate_html(html_content: str, to_lang: str, filename: str) -> str:
    """
    Translate an entire HTML page while preserving structure.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. Update <html lang="">
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = to_lang
        if LANGUAGES[to_lang]["dir"] == "rtl":
            html_tag['dir'] = 'rtl'

    # 2. Update canonical URL
    canonical = soup.find('link', rel='canonical')
    if canonical and canonical.get('href'):
        old_href = canonical['href']
        # /bpc-157-guide.html → /es/bpc-157-guide.html
        canonical['href'] = old_href.replace(
            f"{DOMAIN}/", f"{DOMAIN}/{to_lang}/"
        )

    # 3. Update og:url
    og_url = soup.find('meta', property='og:url')
    if og_url and og_url.get('content'):
        og_url['content'] = og_url['content'].replace(
            f"{DOMAIN}/", f"{DOMAIN}/{to_lang}/"
        )

    # 4. Add hreflang tags
    _inject_hreflang(soup, filename)

    # 5. Update JSON-LD URLs
    for script_tag in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script_tag.string)
            _update_jsonld_urls(data, to_lang)
            # Translate FAQ questions and answers
            _translate_jsonld(data, to_lang)
            script_tag.string = json.dumps(data, ensure_ascii=False, indent=2)
        except (json.JSONDecodeError, TypeError):
            pass

    # 6. Translate text nodes in <head> meta tags
    for meta in soup.find_all('meta'):
        for attr in ['content']:
            val = meta.get(attr, '')
            if val and meta.get('name') in ['description'] or meta.get('property') in ['og:title', 'og:description']:
                meta[attr] = translate_text(val, to_lang)
    # Twitter meta
    for meta in soup.find_all('meta'):
        if meta.get('name') in ['twitter:title', 'twitter:description']:
            val = meta.get('content', '')
            if val:
                meta['content'] = translate_text(val, to_lang)

    # 7. Translate <title>
    title_tag = soup.find('title')
    if title_tag and title_tag.string:
        title_tag.string = translate_text(title_tag.string, to_lang)

    # 8. Translate body text nodes
    body = soup.find('body')
    if body:
        _translate_tree(body, to_lang)

    # 9. Inject language switcher
    _inject_language_switcher(soup, to_lang, filename)

    # 10. Update internal links to include language prefix
    _update_internal_links(soup, to_lang)

    # Use formatter="minimal" to avoid double-encoding &amp; → &amp;amp;
    return soup.decode(formatter="minimal")


def _translate_tree(element, to_lang: str):
    """Recursively translate text nodes in the DOM tree."""
    for child in list(element.children):
        if isinstance(child, (Comment, Doctype)):
            continue
        if isinstance(child, NavigableString):
            text = str(child)
            if text.strip() and not _is_inside_skip_tag(child):
                translated = translate_text(text, to_lang)
                child.replace_with(NavigableString(translated))
        elif child.name and child.name not in SKIP_TAGS:
            # Translate translatable attributes
            for attr in TRANSLATABLE_ATTRS:
                val = child.get(attr)
                if val and isinstance(val, str) and val.strip():
                    child[attr] = translate_text(val, to_lang)
            _translate_tree(child, to_lang)


def _is_inside_skip_tag(node):
    """Check if a node is inside a tag that shouldn't be translated."""
    parent = node.parent
    while parent:
        if parent.name in SKIP_TAGS:
            return True
        parent = parent.parent
    return False


def _inject_hreflang(soup, filename):
    """Add hreflang link tags for all language versions."""
    head = soup.find('head')
    if not head:
        return

    # Remove any existing hreflang tags
    for existing in head.find_all('link', rel='alternate', hreflang=True):
        existing.decompose()

    for lang_code in LANGUAGES:
        link = soup.new_tag('link')
        link['rel'] = 'alternate'
        link['hreflang'] = lang_code
        if lang_code == 'en':
            link['href'] = f"{DOMAIN}/en/{filename}"
        else:
            link['href'] = f"{DOMAIN}/{lang_code}/{filename}"
        head.append(link)

    # x-default points to root (which IS the English version)
    link = soup.new_tag('link')
    link['rel'] = 'alternate'
    link['hreflang'] = 'x-default'
    link['href'] = f"{DOMAIN}/{filename}"
    head.append(link)


def _inject_language_switcher(soup, current_lang: str, filename: str):
    """Inject a language dropdown into the nav and footer."""
    switcher_html = _build_switcher_html(current_lang, filename)

    # Inject into nav
    nav = soup.find('nav')
    if nav:
        switcher_soup = BeautifulSoup(switcher_html, 'html.parser')
        nav.append(switcher_soup)

    # Inject into footer
    footer = soup.find('footer')
    if footer:
        footer_switcher = BeautifulSoup(switcher_html, 'html.parser')
        footer.append(footer_switcher)


def _build_switcher_html(current_lang: str, filename: str) -> str:
    """Build the language switcher dropdown HTML + CSS."""
    options = []
    for code, info in LANGUAGES.items():
        selected = ' selected' if code == current_lang else ''
        url = f"/{code}/{filename}"
        options.append(f'<option value="{url}"{selected}>{info["native"]}</option>')

    return f'''
    <div class="lang-switcher" style="position:relative;display:inline-block;margin-left:12px;">
      <select onchange="window.location.href=this.value"
              style="background:rgba(255,255,255,0.1);color:inherit;border:1px solid rgba(255,255,255,0.2);
                     border-radius:6px;padding:4px 8px;font-size:13px;cursor:pointer;
                     font-family:var(--font-main,sans-serif);">
        {''.join(options)}
      </select>
    </div>
    '''


def _update_internal_links(soup, to_lang: str):
    """Update internal .html links to include language prefix."""
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Only modify internal relative links to .html files
        if href.endswith('.html') and not href.startswith('http') and not href.startswith('//'):
            # Strip any existing language prefix
            clean_href = re.sub(r'^/?(en|es|zh|ja|pt|ru|it|pl|fr|id|de|nl|ar)/', '', href.lstrip('/'))
            a_tag['href'] = f"/{to_lang}/{clean_href}"
        elif href == '/' or href == '/index.html':
            a_tag['href'] = f"/{to_lang}/index.html"


def _update_jsonld_urls(data, to_lang):
    """Update URLs in JSON-LD structured data."""
    if isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, str) and DOMAIN in val and val.endswith('.html'):
                data[key] = val.replace(f"{DOMAIN}/", f"{DOMAIN}/{to_lang}/")
            elif key == 'url' and isinstance(val, str) and DOMAIN in val:
                data[key] = val.replace(f"{DOMAIN}/", f"{DOMAIN}/{to_lang}/")
            elif key == '@id' and isinstance(val, str) and DOMAIN in val:
                data[key] = val.replace(f"{DOMAIN}/", f"{DOMAIN}/{to_lang}/")
            elif key == 'item' and isinstance(val, str) and DOMAIN in val:
                data[key] = val.replace(f"{DOMAIN}/", f"{DOMAIN}/{to_lang}/")
            else:
                _update_jsonld_urls(val, to_lang)
    elif isinstance(data, list):
        for item in data:
            _update_jsonld_urls(item, to_lang)


def _translate_jsonld(data, to_lang):
    """Translate text content in JSON-LD (FAQ answers, headlines, etc.)."""
    if isinstance(data, dict):
        # Translate FAQ questions and answers
        if data.get('@type') == 'Question':
            if 'name' in data:
                data['name'] = translate_text(data['name'], to_lang)
        if data.get('@type') == 'Answer':
            if 'text' in data:
                data['text'] = translate_text(data['text'], to_lang)
        # Translate Article headline and description
        if data.get('@type') == 'Article':
            if 'headline' in data:
                data['headline'] = translate_text(data['headline'], to_lang)
            if 'description' in data:
                data['description'] = translate_text(data['description'], to_lang)
        # Translate breadcrumb names
        if data.get('@type') == 'ListItem':
            if 'name' in data and data['name'] not in ('Home',):
                data['name'] = translate_text(data['name'], to_lang)

        for val in data.values():
            _translate_jsonld(val, to_lang)
    elif isinstance(data, list):
        for item in data:
            _translate_jsonld(item, to_lang)


# ─── Sitemap Generation ──────────────────────────────────────────────────────

def generate_sitemaps():
    """Generate per-language sitemaps and a master sitemap index."""
    # Scan root HTML files directly to build URL list
    html_files = sorted(f.name for f in SITE_DIR.glob('*.html')
                        if f.name not in ('404.html', 'ARTICLE-TEMPLATE.html'))
    if not html_files:
        print("  ⚠ No HTML files found in site directory, skipping sitemap generation")
        return

    urls = [f"{DOMAIN}/{f}" for f in html_files]

    today = time.strftime("%Y-%m-%d")

    # Generate per-language sitemaps
    for lang_code in LANGUAGES:
        lang_dir = SITE_DIR / lang_code
        if not lang_dir.exists():
            continue

        sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        sitemap_content += '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'

        for orig_url in urls:
            filename = orig_url.replace(f"{DOMAIN}/", "")
            if not filename.endswith('.html'):
                continue
            lang_url = f"{DOMAIN}/{lang_code}/{filename}"

            sitemap_content += f'  <url>\n'
            sitemap_content += f'    <loc>{lang_url}</loc>\n'
            sitemap_content += f'    <lastmod>{today}</lastmod>\n'
            sitemap_content += f'    <changefreq>weekly</changefreq>\n'

            # Add hreflang xhtml:link for each language
            for other_lang in LANGUAGES:
                other_url = f"{DOMAIN}/{other_lang}/{filename}"
                sitemap_content += f'    <xhtml:link rel="alternate" hreflang="{other_lang}" href="{other_url}"/>\n'

            sitemap_content += f'  </url>\n'

        sitemap_content += '</urlset>\n'

        out_path = lang_dir / "sitemap.xml"
        out_path.write_text(sitemap_content, encoding='utf-8')

    # Master sitemap index
    index_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    index_content += '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for lang_code in LANGUAGES:
        index_content += f'  <sitemap>\n'
        index_content += f'    <loc>{DOMAIN}/{lang_code}/sitemap.xml</loc>\n'
        index_content += f'    <lastmod>{today}</lastmod>\n'
        index_content += f'  </sitemap>\n'
    index_content += '</sitemapindex>\n'

    (SITE_DIR / "sitemap.xml").write_text(index_content, encoding='utf-8')
    print(f"  ✓ Master sitemap index + {len(LANGUAGES)} language sitemaps generated")


# ─── Cloudflare Worker for Geo-detection ──────────────────────────────────────

def generate_worker():
    """Generate _worker.js for Cloudflare Pages geo-detection."""
    # Map country codes to language codes
    worker_js = '''// Cloudflare Pages Worker — Geo-based language redirect
// Free tier: 100,000 requests/day

const COUNTRY_TO_LANG = {
  // Spanish-speaking
  ES: 'es', MX: 'es', AR: 'es', CO: 'es', CL: 'es', PE: 'es', VE: 'es',
  EC: 'es', GT: 'es', CU: 'es', BO: 'es', DO: 'es', HN: 'es', PY: 'es',
  SV: 'es', NI: 'es', CR: 'es', PA: 'es', UY: 'es',
  // Chinese
  CN: 'zh', TW: 'zh', HK: 'zh', MO: 'zh', SG: 'zh',
  // Japanese
  JP: 'ja',
  // Portuguese
  BR: 'pt', PT: 'pt', AO: 'pt', MZ: 'pt',
  // Russian
  RU: 'ru', BY: 'ru', KZ: 'ru', KG: 'ru', UA: 'ru',
  // Italian
  IT: 'it', SM: 'it', VA: 'it',
  // Polish
  PL: 'pl',
  // French
  FR: 'fr', BE: 'fr', CH: 'fr', CA: 'fr', SN: 'fr', CI: 'fr',
  ML: 'fr', BF: 'fr', NE: 'fr', TG: 'fr', BJ: 'fr', CD: 'fr',
  // Indonesian
  ID: 'id', MY: 'id',
  // German
  DE: 'de', AT: 'de',
  // Dutch
  NL: 'nl',
  // Arabic
  SA: 'ar', AE: 'ar', EG: 'ar', IQ: 'ar', MA: 'ar', DZ: 'ar',
  TN: 'ar', LY: 'ar', JO: 'ar', LB: 'ar', KW: 'ar', QA: 'ar',
  BH: 'ar', OM: 'ar', YE: 'ar', SD: 'ar', SY: 'ar',
};

const VALID_LANGS = new Set(['en','es','zh','ja','pt','ru','it','pl','fr','id','de','nl','ar']);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Already has a language prefix — serve normally
    const langMatch = path.match(/^\\/(en|es|zh|ja|pt|ru|it|pl|fr|id|de|nl|ar)\\//);
    if (langMatch) {
      return env.ASSETS.fetch(request);
    }

    // Check for language preference cookie
    const cookies = request.headers.get('Cookie') || '';
    const langCookie = cookies.match(/wolvestack_lang=(\\w{2})/);
    if (langCookie && VALID_LANGS.has(langCookie[1])) {
      return Response.redirect(`${url.origin}/${langCookie[1]}${path}`, 302);
    }

    // Geo-detect from Cloudflare headers
    const country = request.cf?.country || 'US';
    const detectedLang = COUNTRY_TO_LANG[country] || 'en';

    // Root page: redirect to detected language
    if (path === '/' || path === '/index.html') {
      const response = Response.redirect(`${url.origin}/${detectedLang}/index.html`, 302);
      return response;
    }

    // HTML page without language prefix: redirect
    if (path.endsWith('.html')) {
      return Response.redirect(`${url.origin}/${detectedLang}${path}`, 302);
    }

    // Static assets (CSS, JS, images): serve from root
    return env.ASSETS.fetch(request);
  }
};
'''
    worker_path = SITE_DIR / "_worker.js"
    worker_path.write_text(worker_js, encoding='utf-8')
    print(f"  ✓ Cloudflare Worker generated: _worker.js")


# ─── Batch Processing ────────────────────────────────────────────────────────

def get_translatable_files() -> list:
    """Get all HTML files that should be translated."""
    skip = {'ARTICLE-TEMPLATE.html', '404.html'}
    files = []
    for f in sorted(SITE_DIR.glob('*.html')):
        if f.name not in skip:
            files.append(f.name)
    return files


def translate_file(filename: str, to_lang: str, force: bool = False) -> bool:
    """Translate a single file to a target language."""
    src_path = SITE_DIR / filename
    if not src_path.exists():
        return False

    # Create language directory
    lang_dir = SITE_DIR / to_lang
    lang_dir.mkdir(exist_ok=True)

    dest_path = lang_dir / filename
    if dest_path.exists() and not force:
        return True  # Already translated

    html_content = src_path.read_text(encoding='utf-8')
    translated = translate_html(html_content, to_lang, filename)
    dest_path.write_text(translated, encoding='utf-8')
    return True


def translate_all(target_langs=None, force=False, specific_file=None):
    """Translate all files to all (or specific) languages."""
    if target_langs is None:
        target_langs = [l for l in LANGUAGES if l != 'en']

    files = [specific_file] if specific_file else get_translatable_files()
    total_files = len(files)
    total_langs = len(target_langs)
    total_work = total_files * total_langs

    print(f"\n  Translation Pipeline")
    print(f"  {'═' * 50}")
    print(f"  Files: {total_files}")
    print(f"  Languages: {total_langs} ({', '.join(target_langs)})")
    print(f"  Total pages to generate: {total_work:,}")
    print(f"  {'═' * 50}\n")

    # First, copy English files to /en/ directory
    print(f"  Setting up /en/ directory...")
    en_dir = SITE_DIR / "en"
    en_dir.mkdir(exist_ok=True)
    for filename in files:
        src = SITE_DIR / filename
        dest = en_dir / filename
        if not dest.exists() or force:
            html = src.read_text(encoding='utf-8')
            # Add hreflang + language switcher to English version too
            soup = BeautifulSoup(html, 'html.parser')
            _inject_hreflang(soup, filename)
            _inject_language_switcher(soup, 'en', filename)
            _update_internal_links(soup, 'en')
            dest.write_text(str(soup), encoding='utf-8')
    print(f"  ✓ {total_files} English files in /en/\n")

    # Translate each language
    completed = 0
    for lang_idx, lang in enumerate(target_langs):
        lang_info = LANGUAGES[lang]
        print(f"  [{lang_idx+1}/{total_langs}] {lang_info['name']} ({lang_info['native']}) → /{lang}/")

        lang_dir = SITE_DIR / lang
        lang_dir.mkdir(exist_ok=True)

        skipped = 0
        translated = 0
        errors = 0

        for file_idx, filename in enumerate(files):
            dest_path = lang_dir / filename
            if dest_path.exists() and not force:
                skipped += 1
                continue

            try:
                src_path = SITE_DIR / filename
                html_content = src_path.read_text(encoding='utf-8')
                result = translate_html(html_content, lang, filename)
                dest_path.write_text(result, encoding='utf-8')
                translated += 1
            except Exception as e:
                print(f"    ✗ {filename}: {str(e)[:80]}")
                errors += 1

            completed += 1
            if (translated + skipped + errors) % 100 == 0:
                pct = ((lang_idx * total_files) + file_idx + 1) / total_work * 100
                print(f"    ...{translated} translated, {skipped} skipped ({pct:.0f}% overall)")

        print(f"    ✓ {translated} translated, {skipped} skipped, {errors} errors")

    # Generate sitemaps
    print(f"\n  Generating sitemaps...")
    generate_sitemaps()

    # Generate Cloudflare Worker
    print(f"  Generating Cloudflare Worker...")
    generate_worker()

    print(f"\n  {'═' * 50}")
    print(f"  COMPLETE: {completed:,} pages translated")
    print(f"  {'═' * 50}")


def install_languages():
    """Install required Argos Translate language packages."""
    import argostranslate.package

    print("  Updating Argos Translate package index...")
    argostranslate.package.update_package_index()
    available = argostranslate.package.get_available_packages()

    needed_langs = [l for l in LANGUAGES if l != 'en']
    installed = 0

    for lang_code in needed_langs:
        argos_code = ARGOS_LANG_MAP[lang_code]
        pkg = next(
            (p for p in available
             if p.from_code == 'en' and p.to_code == argos_code),
            None
        )
        if pkg:
            print(f"  Installing en → {lang_code} ({LANGUAGES[lang_code]['name']})...", end=" ", flush=True)
            try:
                argostranslate.package.install_from_path(pkg.download())
                print("✓")
                installed += 1
            except Exception as e:
                print(f"✗ ({e})")
        else:
            print(f"  ⚠ No package found for en → {argos_code}")

    print(f"\n  {installed} language packs installed")


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="WolveStack Multilingual Translation Pipeline")
    parser.add_argument("--install-languages", action="store_true", help="Install Argos language packs")
    parser.add_argument("--all", action="store_true", help="Translate all files to all languages")
    parser.add_argument("--lang", type=str, help="Translate to a specific language (e.g. es, de, zh)")
    parser.add_argument("--file", type=str, help="Translate a specific file")
    parser.add_argument("--force", action="store_true", help="Overwrite existing translations")
    parser.add_argument("--sitemaps", action="store_true", help="Only regenerate sitemaps")
    parser.add_argument("--worker", action="store_true", help="Only generate Cloudflare Worker")
    args = parser.parse_args()

    if args.install_languages:
        install_languages()
        return

    if args.sitemaps:
        generate_sitemaps()
        return

    if args.worker:
        generate_worker()
        return

    if args.all:
        langs = [args.lang] if args.lang else None
        translate_all(target_langs=langs, force=args.force, specific_file=args.file)
    elif args.lang:
        translate_all(target_langs=[args.lang], force=args.force, specific_file=args.file)
    elif args.file:
        translate_all(force=args.force, specific_file=args.file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
