#!/usr/bin/env python3
"""
GSC structured-data error sweep — local schema fixer.

Three classes of fix applied to /en/ and root /*.html:
  1. Duplicate Article LD+JSON blocks → keep the more complete one, drop the other
  2. Duplicate FAQPage LD+JSON blocks → keep the one with more questions
  3. Article schema missing required `image` field → inject one
       - prefer existing og:image meta if present
       - else use a Pinterest pin URL if /pinterest-pins-v2/pin-{slug}.png exists
       - else fall back to publisher logo (https://wolvestack.com/images/logo.png)

Skips language dirs (es/zh/ja/...) because the translation pipeline is running.
After it finishes, run again with --include-langs.

Usage:
  python3 fix_schema_errors.py --dry-run     # report only, no writes
  python3 fix_schema_errors.py               # apply fixes to /en/ + root
  python3 fix_schema_errors.py --include-langs   # also touch language dirs
"""
import os
import re
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANGS = ["es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de", "nl", "ar"]
DEFAULT_IMAGE = "https://wolvestack.com/images/logo.png"
PIN_URL_TEMPLATE = "https://wolvestack.com/pinterest-pins-v2/pin-{slug}.png"
PINS_DIR = ROOT / "pinterest-pins-v2"

LD_RE = re.compile(
    r'(<script[^>]*application/ld\+json[^>]*>)(.*?)(</script>)',
    re.DOTALL | re.IGNORECASE,
)
OG_IMAGE_RE = re.compile(
    r'<meta[^>]+(?:property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']'
    r'|content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\'])',
    re.IGNORECASE,
)
ARTICLE_TYPES = {"Article", "NewsArticle", "BlogPosting"}


def is_article(item):
    if not isinstance(item, dict):
        return False
    t = item.get("@type", "")
    tl = t if isinstance(t, list) else [t]
    return any(x in ARTICLE_TYPES for x in tl)


def is_faq(item):
    if not isinstance(item, dict):
        return False
    t = item.get("@type", "")
    tl = t if isinstance(t, list) else [t]
    return "FAQPage" in tl


def parse_block(raw):
    """Return parsed JSON (object or list) or None on failure."""
    try:
        return json.loads(raw.strip())
    except Exception:
        return None


def extract_articles_and_faqs(parsed):
    """Yield (kind, item) pairs — kind in {'article','faq'}."""
    items = parsed if isinstance(parsed, list) else [parsed]
    for item in items:
        if is_article(item):
            yield "article", item
        if is_faq(item):
            yield "faq", item


def article_completeness(item):
    """Score an article schema by how many useful fields it has."""
    if not isinstance(item, dict):
        return 0
    keys = (
        "headline description author publisher datePublished dateModified "
        "image url mainEntityOfPage reviewedBy"
    ).split()
    return sum(1 for k in keys if item.get(k))


def faq_completeness(item):
    me = item.get("mainEntity", [])
    if isinstance(me, dict):
        me = [me]
    return len(me)


def find_og_image(html):
    m = OG_IMAGE_RE.search(html)
    if not m:
        return None
    return m.group(1) or m.group(2)


def pick_image_for_slug(slug, html):
    """Pick the best image URL for a given article."""
    og = find_og_image(html)
    if og:
        return og
    pin_path = PINS_DIR / f"pin-{slug}.png"
    if pin_path.exists():
        return PIN_URL_TEMPLATE.format(slug=slug)
    return DEFAULT_IMAGE


def reserialize_block(parsed, original_indent):
    """Re-serialize a parsed JSON-LD block, preserving indentation roughly."""
    return json.dumps(parsed, indent=2, ensure_ascii=False)


def fix_file(path: Path, dry_run=False):
    """Apply all three fix classes to a single HTML file. Returns dict of changes."""
    html = path.read_text(encoding="utf-8")
    original = html
    changes = {
        "duplicate_article_dropped": 0,
        "duplicate_faq_dropped": 0,
        "image_injected": 0,
    }

    # 1) Find every LD+JSON block, parse it, classify it.
    matches = list(LD_RE.finditer(html))
    if not matches:
        return changes

    parsed_blocks = []
    for m in matches:
        raw = m.group(2)
        parsed = parse_block(raw)
        parsed_blocks.append({
            "match": m,
            "parsed": parsed,
            "raw": raw,
            "open_tag": m.group(1),
            "close_tag": m.group(3),
        })

    # 2) Identify which blocks contain Article and FAQ items.
    #    Strategy: keep the BEST single Article block + BEST single FAQ block;
    #    drop other blocks that only carry duplicates of those types and nothing else.
    article_blocks = []  # (idx, score, item)
    faq_blocks = []      # (idx, count, item)
    for i, b in enumerate(parsed_blocks):
        p = b["parsed"]
        if p is None:
            continue
        items = p if isinstance(p, list) else [p]
        for item in items:
            if is_article(item):
                article_blocks.append((i, article_completeness(item), item))
            if is_faq(item):
                faq_blocks.append((i, faq_completeness(item), item))

    # Track which block indices to drop entirely.
    drop_indices = set()
    article_winner_idx = None
    if len(article_blocks) > 1:
        article_blocks.sort(key=lambda x: -x[1])
        article_winner_idx = article_blocks[0][0]
        for idx, _, _ in article_blocks[1:]:
            # Only drop the block if it carries ONLY duplicated types.
            # Safer: instead of dropping the whole block, strip the duplicate Article from it.
            blk = parsed_blocks[idx]
            p = blk["parsed"]
            if isinstance(p, dict) and is_article(p):
                # Block is a single Article — drop it entirely.
                drop_indices.add(idx)
                changes["duplicate_article_dropped"] += 1
            elif isinstance(p, list):
                # Strip Article items from this list.
                new_list = [x for x in p if not is_article(x)]
                if len(new_list) != len(p):
                    blk["parsed"] = new_list[0] if len(new_list) == 1 else new_list
                    changes["duplicate_article_dropped"] += (len(p) - len(new_list))

    if len(faq_blocks) > 1:
        faq_blocks.sort(key=lambda x: -x[1])
        # Drop all but the winner.
        for idx, _, _ in faq_blocks[1:]:
            blk = parsed_blocks[idx]
            p = blk["parsed"]
            if isinstance(p, dict) and is_faq(p):
                drop_indices.add(idx)
                changes["duplicate_faq_dropped"] += 1
            elif isinstance(p, list):
                new_list = [x for x in p if not is_faq(x)]
                if len(new_list) != len(p):
                    blk["parsed"] = new_list[0] if len(new_list) == 1 else new_list
                    changes["duplicate_faq_dropped"] += (len(p) - len(new_list))

    # 3) Inject `image` into Article blocks that are missing it.
    slug = path.stem
    image_url = None
    for i, b in enumerate(parsed_blocks):
        if i in drop_indices:
            continue
        p = b["parsed"]
        if p is None:
            continue
        items = p if isinstance(p, list) else [p]
        modified = False
        for item in items:
            if is_article(item) and not item.get("image"):
                if image_url is None:
                    image_url = pick_image_for_slug(slug, html)
                item["image"] = image_url
                changes["image_injected"] += 1
                modified = True
        if modified:
            b["modified"] = True

    # 4) Rebuild HTML with the changes.
    if not (drop_indices or any(b.get("modified") for b in parsed_blocks)):
        return changes

    new_html = []
    cursor = 0
    for i, b in enumerate(parsed_blocks):
        m = b["match"]
        new_html.append(html[cursor:m.start()])
        if i in drop_indices:
            # Remove the entire <script>...</script> tag, including a trailing newline if any.
            tail = m.end()
            if tail < len(html) and html[tail] == "\n":
                tail += 1
            cursor = tail
            continue
        if b.get("modified"):
            new_block_text = b["open_tag"] + "\n" + reserialize_block(b["parsed"], 0) + "\n" + b["close_tag"]
            new_html.append(new_block_text)
        else:
            new_html.append(html[m.start():m.end()])
        cursor = m.end()
    new_html.append(html[cursor:])

    new_html_str = "".join(new_html)

    if dry_run:
        return changes

    path.write_text(new_html_str, encoding="utf-8")
    return changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Don't write files, just report")
    ap.add_argument("--include-langs", action="store_true", help="Also process language dirs")
    args = ap.parse_args()

    dirs_to_scan = ["en", "."]  # /en/ + root
    if args.include_langs:
        dirs_to_scan.extend(LANGS)

    totals = {
        "files_scanned": 0,
        "files_changed": 0,
        "duplicate_article_dropped": 0,
        "duplicate_faq_dropped": 0,
        "image_injected": 0,
    }

    for d in dirs_to_scan:
        dpath = ROOT / d if d != "." else ROOT
        if not dpath.is_dir():
            continue
        # Don't recurse — only direct .html children.
        files = sorted([f for f in dpath.iterdir() if f.is_file() and f.suffix == ".html"])
        for f in files:
            # Skip files that are in subdirs we don't want to process (e.g. /en/foo when scanning root)
            if d == "." and f.parent != ROOT:
                continue
            totals["files_scanned"] += 1
            changes = fix_file(f, dry_run=args.dry_run)
            if any(v > 0 for v in changes.values()):
                totals["files_changed"] += 1
                for k, v in changes.items():
                    totals[k] += v

    print("=" * 60)
    print("GSC schema sweep results" + (" (DRY RUN)" if args.dry_run else ""))
    print("=" * 60)
    for k, v in totals.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
