#!/usr/bin/env python3
"""
fix_broken_affiliate_2026_05.py — 2026-05-31

Fast version: uses ripgrep to find only the files that contain a bad domain,
then applies regex substitutions just to those files.
"""
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

URL_FIXES = [
    (re.compile(r'https?://(?:www\.)?ascensionsupps\.com[^"\'\s<>]*'),
     'https://ascensionpeptides.com/?ref=wolvestack'),
    (re.compile(r'https?://(?:www\.)?ascensionresearch\.co[^"\'\s<>]*'),
     'https://ascensionpeptides.com/?ref=wolvestack'),
    (re.compile(r'https?://(?:www\.)?ascensionsupplements\.com[^"\'\s<>]*'),
     'https://ascensionpeptides.com/?ref=wolvestack'),
    (re.compile(r'https://www\.ascensionpeptides\.com'),
     'https://ascensionpeptides.com'),
    (re.compile(r'https?://(?:www\.)?apolloresearchcompounds\.com[^"\'\s<>]*'),
     'https://apollopeptidesciences.com/?rfsn=9022946'),
    (re.compile(r'https://apollopeptidesciences\.com/\?ref=wolvestack'),
     'https://apollopeptidesciences.com/?rfsn=9022946'),
    (re.compile(r'https?://(?:www\.)?limitlesslifenoo\.com[^"\'\s<>]*'),
     'https://www.limitlesslifenootropics.com/?_ef_transaction_id=&oid=1&affid=10704'),
    (re.compile(r'https?://(?:www\.)?limitlesslifenotropics\.com[^"\'\s<>]*'),
     'https://www.limitlesslifenootropics.com/?_ef_transaction_id=&oid=1&affid=10704'),
    (re.compile(r'https?://(?:www\.)?limitlesslifebiotech\.com[^"\'\s<>]*'),
     'https://www.limitlesslifenootropics.com/?_ef_transaction_id=&oid=1&affid=10704'),
    (re.compile(r'https?://(?:www\.)?limitless-biohacking\.com[^"\'\s<>]*'),
     'https://www.limitlesslifenootropics.com/?_ef_transaction_id=&oid=1&affid=10704'),
    (re.compile(r'https?://(?:www\.)?limitless-peptides\.com[^"\'\s<>]*'),
     'https://www.limitlesslifenootropics.com/?_ef_transaction_id=&oid=1&affid=10704'),
    (re.compile(r'https?://(?:www\.)?limitlesspeptides\.com[^"\'\s<>]*'),
     'https://www.limitlesslifenootropics.com/?_ef_transaction_id=&oid=1&affid=10704'),
]

TEXT_FIXES = [
    ('Ascension Research Compounds', 'Ascension Peptides'),
    ('Ascension Research', 'Ascension Peptides'),
    ('Ascension Supplements', 'Ascension Peptides'),
    ('Ascension Supps', 'Ascension Peptides'),
    ('Apollo Research Compounds', 'Apollo Peptide Sciences'),
    ('Apollo Research', 'Apollo Peptide Sciences'),
]


def find_target_files():
    """Use ripgrep to get the set of HTML files that contain any bad token."""
    tokens = [
        'ascensionsupps.com', 'ascensionresearch.co',
        'ascensionsupplements.com', 'www.ascensionpeptides.com',
        'apolloresearchcompounds.com',
        'apollopeptidesciences.com/?ref=wolvestack',
        'limitlesslifenoo.com', 'limitlesslifenotropics.com',
        'limitlesslifebiotech.com', 'limitless-biohacking.com',
        'limitless-peptides.com', 'limitlesspeptides.com',
        'Ascension Research', 'Ascension Supplements',
        'Ascension Supps', 'Apollo Research',
    ]
    pattern = '|'.join(re.escape(t) for t in tokens)
    out = subprocess.run(
        ['grep', '-rlE', '--include=*.html', pattern, '.'],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    return [ROOT / p.lstrip('./') for p in out.stdout.splitlines() if p.strip()]


def fix_file(path: Path):
    try:
        original = path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, OSError):
        return None
    new = original
    for pat, repl in URL_FIXES:
        new = pat.sub(repl, new)
    for old, fresh in TEXT_FIXES:
        if old in new:
            new = new.replace(old, fresh)
    if new == original:
        return False
    path.write_text(new, encoding='utf-8')
    return True


def main():
    started = time.time()
    files = find_target_files()
    n_total = len(files)
    print(f'Target files (containing bad tokens): {n_total}')
    n_changed = 0
    n_skipped = 0
    for i, fp in enumerate(files, 1):
        r = fix_file(fp)
        if r is True:
            n_changed += 1
        elif r is None:
            n_skipped += 1
        if i % 2000 == 0:
            print(f'  [{i}/{n_total}] changed={n_changed} skipped={n_skipped} '
                  f'elapsed={time.time() - started:.1f}s', flush=True)
    elapsed = time.time() - started
    print(f'\nDone. Files seen: {n_total}, changed: {n_changed}, '
          f'unreadable: {n_skipped}, elapsed: {elapsed:.1f}s')
    return 0


if __name__ == '__main__':
    sys.exit(main())
