#!/usr/bin/env python3
"""
Translation Polish — chunked + intra-file parallel.

Per file: extract text segments → split into ≤3500-char chunks → all chunks
run in parallel through a shared semaphore → reassemble. Each chunk fits
comfortably in 8192 max_tokens and completes in 5-10s.

Sandbox-friendly: a batch of 5-10 files completes in ~15-25s wall clock.

Resume-safe via polish-log.txt.
"""
import argparse
import asyncio
import os
import re
import sys
import time
from pathlib import Path

import httpx
from bs4 import BeautifulSoup, NavigableString, Comment, Doctype

ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT / "polish-log.txt"
PIPELINE_LANGS = {"nl", "ar"}
PRIORITY_ORDER = ["es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de"]
SEP = "≡≡≡SEG≡≡≡"
SKIP_TAGS = {"script", "style", "code", "pre"}
MAX_CHUNK_CHARS = 3500

LANG_NAMES = {
    "es": "Spanish (neutral, suitable for Spain and Latin America)",
    "zh": "Simplified Chinese",
    "ja": "Japanese",
    "pt": "Portuguese (Brazilian preferred when ambiguous)",
    "ru": "Russian",
    "it": "Italian",
    "pl": "Polish",
    "fr": "French (Metropolitan)",
    "id": "Indonesian (Bahasa Indonesia)",
    "de": "German",
}

PROTECTED_PATTERN = re.compile(
    r"\b("
    r"BPC-157|TB-500|GHK-Cu|CJC-1295|MK-677|MOTS-c|MOTs-C|PT-141|AOD-9604|"
    r"5-Amino-1MQ|FOXO4-DRI|GLP-1|GIP|REMAIN-1|TRIUMPH-4|STEP-4|SURMOUNT|"
    r"SURPASS|TRANSCEND-T2D-1|WOMAC|PCAC|FDA|503A|503B|"
    r"WolveStack|Wegovy|Mounjaro|Zepbound|Ozempic|Saxenda|"
    r"Ipamorelin|Tesamorelin|Semaglutide|Tirzepatide|Liraglutide|Retatrutide|"
    r"Survodutide|Cagrisema|Pemvidutide|Maritide|Cotadutide|Orforglipron|"
    r"Setmelanotide|Selank|Semax|Epitalon|Epithalon|Thymalin|Thymosin|"
    r"DSIP|KPV|Melanotan|Hexarelin|Sermorelin"
    r")\b"
)


def already_polished(rel_path: str) -> bool:
    if not LOG_FILE.exists():
        return False
    try:
        with LOG_FILE.open() as f:
            for line in f:
                if line.rstrip().endswith(rel_path):
                    return True
    except Exception:
        return False
    return False


def mark_polished(rel_path: str, tokens_in: int, tokens_out: int):
    with LOG_FILE.open("a") as f:
        f.write(f"{int(time.time())}\t{tokens_in}\t{tokens_out}\t{rel_path}\n")


def is_indexable(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:8000]
    except Exception:
        return False
    return not re.search(
        r'<meta\s+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex',
        head, re.IGNORECASE
    )


def collect_text_segments(article):
    segs = []
    def walk(el, in_skip=False):
        for child in list(el.children):
            if isinstance(child, (Comment, Doctype)):
                continue
            if isinstance(child, NavigableString):
                if in_skip:
                    continue
                t = str(child)
                if t.strip() and len(t.strip()) > 1:
                    segs.append(child)
            elif getattr(child, "name", None):
                walk(child, in_skip or child.name in SKIP_TAGS)
    walk(article)
    return segs


def chunk_segments(segs):
    """Group segment indices into chunks of ≤MAX_CHUNK_CHARS combined text length."""
    chunks = []
    current = []
    current_chars = 0
    for i, seg in enumerate(segs):
        text = str(seg)
        tlen = len(text)
        if current_chars + tlen > MAX_CHUNK_CHARS and current:
            chunks.append(current)
            current = []
            current_chars = 0
        current.append(i)
        current_chars += tlen
    if current:
        chunks.append(current)
    return chunks


async def polish_chunk(
    client: httpx.AsyncClient,
    api_key: str,
    texts: list[str],
    placeholders: dict,
    counter_box: list,
    lang_name: str,
    semaphore: asyncio.Semaphore,
    stats: dict,
    file_label: str,
) -> list[str] | None:
    """Polish one chunk of segments. Returns list of polished texts (same length) or None on fail."""
    if not texts:
        return []

    # Apply protected term placeholders
    def repl(m):
        token = m.group(0)
        for k, v in placeholders.items():
            if v == token:
                return k
        counter_box[0] += 1
        key = f"XTERMX{counter_box[0]:04d}"
        placeholders[key] = token
        return key
    protected = [PROTECTED_PATTERN.sub(repl, t) for t in texts]

    # Numbered-prefix format: more robust than separator-based
    batch = "\n".join(f"[{i+1:03d}] {t}" for i, t in enumerate(protected))
    prompt = (
        f"You are a native {lang_name} editor. Polish each numbered segment for grammar, "
        f"natural vocabulary, and fluent flow — fixing machine-translation stiffness "
        f"without changing meaning.\n\n"
        f"Rules:\n"
        f"- Preserve meaning EXACTLY. Do not add or remove ideas.\n"
        f"- Keep XTERMX#### placeholders UNCHANGED.\n"
        f"- Numbers, dates, percentages, dosages stay exactly as-is.\n"
        f"- Each segment STARTS with [NNN] where NNN is a 3-digit number.\n"
        f"- Output the SAME segments, each on its own line, starting with the SAME [NNN] prefix.\n"
        f"- Return EXACTLY {len(texts)} numbered segments. No commentary, no markdown.\n\n"
        f"INPUT:\n{batch}\n\nPOLISHED OUTPUT:"
    )

    resp = None
    for attempt in range(4):
        async with semaphore:
            try:
                resp = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-haiku-4-5",
                        "max_tokens": 8192,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                    timeout=60.0,
                )
            except Exception as e:
                if attempt == 3:
                    stats["errors"].append(f"{file_label}: chunk API fail: {e}")
                    return None
                await asyncio.sleep(2 ** attempt)
                continue
        if resp.status_code == 429:
            # Honor Retry-After if present, else exponential backoff
            ra = resp.headers.get("Retry-After")
            wait = float(ra) if ra and ra.replace(".", "", 1).isdigit() else (2 ** attempt) + 1
            await asyncio.sleep(min(wait, 8))
            continue
        if resp.status_code == 529 or resp.status_code == 503:
            await asyncio.sleep(2 ** attempt)
            continue
        break

    if resp is None or resp.status_code != 200:
        code = resp.status_code if resp is not None else "no-resp"
        body = resp.text[:120] if resp is not None else ""
        stats["errors"].append(f"{file_label}: chunk HTTP {code}: {body}")
        return None

    try:
        data = resp.json()
        polished = data["content"][0]["text"]
        usage = data.get("usage", {})
        stats["tokens_in"] += usage.get("input_tokens", 0)
        stats["tokens_out"] += usage.get("output_tokens", 0)
    except Exception as e:
        stats["errors"].append(f"{file_label}: parse fail: {e}")
        return None

    # Parse numbered output: lines starting with [NNN]
    parts = [None] * len(texts)
    pattern = re.compile(r"\[(\d{3})\]\s*(.*?)(?=\n\[\d{3}\]|\Z)", re.DOTALL)
    matched = 0
    for m in pattern.finditer(polished):
        n = int(m.group(1)) - 1
        if 0 <= n < len(texts):
            parts[n] = m.group(2).strip()
            matched += 1

    if matched == 0:
        stats["errors"].append(
            f"{file_label}: no [NNN] markers found in output"
        )
        return None

    # On partial mismatch, keep original text for missing segments
    missed = 0
    for i, p in enumerate(parts):
        if p is None or not p:
            parts[i] = texts[i]
            missed += 1
    if missed > 0:
        stats.setdefault("partial_segments", 0)
        stats["partial_segments"] += missed
    return parts


async def polish_one_file(
    client, api_key, file_path: Path, lang: str,
    semaphore: asyncio.Semaphore, stats: dict,
):
    rel = str(file_path.relative_to(ROOT))
    if already_polished(rel):
        stats["skipped"] += 1
        return
    if not is_indexable(file_path):
        stats["skipped_noindex"] += 1
        return

    try:
        html = file_path.read_text(encoding="utf-8")
    except Exception as e:
        stats["errors"].append(f"{rel}: read: {e}")
        return

    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("article", class_="article-body")
    if not article:
        stats["skipped_no_article"] += 1
        return

    segs = collect_text_segments(article)
    if not segs:
        stats["skipped_no_text"] += 1
        return

    raw_texts = [str(s) for s in segs]
    total_chars = sum(len(t) for t in raw_texts)
    if total_chars < 800:
        stats["skipped_small"] += 1
        return

    # Build chunks (lists of segment indices)
    chunk_idx_lists = chunk_segments(segs)

    # Shared placeholder state across chunks of one file
    placeholders: dict = {}
    counter_box = [0]
    lang_name = LANG_NAMES.get(lang, lang)
    tokens_before = (stats["tokens_in"], stats["tokens_out"])

    # Run all chunks for this file in parallel
    coros = [
        polish_chunk(
            client, api_key,
            [raw_texts[i] for i in idx_list],
            placeholders, counter_box, lang_name,
            semaphore, stats, rel,
        )
        for idx_list in chunk_idx_lists
    ]
    chunk_results = await asyncio.gather(*coros)

    if any(r is None for r in chunk_results):
        # At least one chunk failed; abort this file (don't write partial)
        return

    # Reassemble polished texts in original segment order
    polished_by_idx: dict[int, str] = {}
    for idx_list, polished_chunk in zip(chunk_idx_lists, chunk_results):
        for i, polished in zip(idx_list, polished_chunk):
            polished_by_idx[i] = polished

    # Restore protected terms and apply to DOM
    for i, seg in enumerate(segs):
        polished = polished_by_idx.get(i, "").strip()
        if not polished:
            continue
        for key, val in placeholders.items():
            polished = polished.replace(key, val)
        orig = str(seg)
        m_lead = re.match(r"^\s*", orig)
        m_trail = re.search(r"\s*$", orig)
        new_text = (m_lead.group(0) if m_lead else "") + polished + (m_trail.group(0) if m_trail else "")
        try:
            seg.replace_with(NavigableString(new_text))
        except Exception:
            pass

    try:
        file_path.write_text(str(soup), encoding="utf-8")
    except Exception as e:
        stats["errors"].append(f"{rel}: write: {e}")
        return

    tokens_in_file = stats["tokens_in"] - tokens_before[0]
    tokens_out_file = stats["tokens_out"] - tokens_before[1]
    mark_polished(rel, tokens_in_file, tokens_out_file)
    stats["polished"] += 1


def collect_files(limit: int) -> list[tuple[Path, str]]:
    out = []
    for lang in PRIORITY_ORDER:
        if lang in PIPELINE_LANGS:
            continue
        d = ROOT / lang
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if f.suffix != ".html":
                continue
            if f.name in {"sitemap.xml", "404.html", "search.html"}:
                continue
            rel = str(f.relative_to(ROOT))
            if already_polished(rel):
                continue
            out.append((f, lang))
            if len(out) >= limit:
                return out
    return out


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=2500)
    ap.add_argument("--concurrency", type=int, default=40)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        kp = ROOT.parent / ".anthropic-key"
        if kp.exists():
            api_key = kp.read_text().strip()
    if not api_key and not args.dry_run:
        print("ERROR: no ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)

    files = collect_files(args.limit)
    print(f"Collected {len(files)} files (priority es→zh→ja→...)", flush=True)

    if args.dry_run:
        return

    stats = {
        "polished": 0,
        "skipped": 0,
        "skipped_noindex": 0,
        "skipped_no_article": 0,
        "skipped_no_text": 0,
        "skipped_small": 0,
        "errors": [],
        "tokens_in": 0,
        "tokens_out": 0,
    }

    sem = asyncio.Semaphore(args.concurrency)
    started = time.time()

    async with httpx.AsyncClient() as client:
        tasks = [polish_one_file(client, api_key, f, lang, sem, stats) for f, lang in files]
        await asyncio.gather(*tasks, return_exceptions=False)

    elapsed = time.time() - started
    cost = stats["tokens_in"] / 1e6 * 1.0 + stats["tokens_out"] / 1e6 * 5.0
    print(
        f"DONE {elapsed:.1f}s — pol={stats['polished']} "
        f"skip={stats['skipped']} ni={stats['skipped_noindex']} na={stats['skipped_no_article']} "
        f"nt={stats['skipped_no_text']} sm={stats['skipped_small']} "
        f"err={len(stats['errors'])} | ${cost:.3f} | "
        f"tokens {stats['tokens_in']:,}/{stats['tokens_out']:,}",
        flush=True,
    )
    if stats["errors"]:
        for e in stats["errors"][:5]:
            print(f"  - {e}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
