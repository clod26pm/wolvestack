#!/usr/bin/env python3
"""Fast affiliate URL fix — reads file list from /tmp/bad_url_files.txt."""
import re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ASCENSION_BAD = re.compile(
    r'https?://(?:www\.)?(?:ascensionsupps|ascensionresearch\.co|ascensionsupplements)[a-z.\-]*'
    r'(?:/[^"\'\s<>]*)?'
)
ASCENSION_BAD_2 = re.compile(r'https?://(?:www\.)?ascensionresearch\.co[^"\'\s<>]*')
APOLLO_BAD = re.compile(r'https?://(?:www\.)?apolloresearchcompounds\.com[^"\'\s<>]*')
APOLLO_REF = re.compile(r'https://apollopeptidesciences\.com/\?ref=wolvestack')
ASCENSION_WWW = re.compile(r'https://www\.ascensionpeptides\.com')
LIMITLESS_BAD = re.compile(
    r'https?://(?:www\.)?(?:limitlesslifenoo|limitlesslifenotropics|limitlesslifebiotech|'
    r'limitless-biohacking|limitless-peptides|limitlesspeptides)\.com[^"\'\s<>]*'
)

ASCENSION_GOOD = 'https://ascensionpeptides.com/?ref=wolvestack'
APOLLO_GOOD = 'https://apollopeptidesciences.com/?rfsn=9022946'
LIMITLESS_GOOD = ('https://www.limitlesslifenootropics.com/'
                  '?_ef_transaction_id=&oid=1&affid=10704')

TEXT_FIXES = [
    ('Ascension Research Compounds', 'Ascension Peptides'),
    ('Ascension Research', 'Ascension Peptides'),
    ('Ascension Supplements', 'Ascension Peptides'),
    ('Ascension Supps', 'Ascension Peptides'),
    ('Apollo Research Compounds', 'Apollo Peptide Sciences'),
    ('Apollo Research', 'Apollo Peptide Sciences'),
]


def transform(text):
    new = text
    new = ASCENSION_BAD.sub(ASCENSION_GOOD, new)
    new = ASCENSION_BAD_2.sub(ASCENSION_GOOD, new)
    new = ASCENSION_WWW.sub('https://ascensionpeptides.com', new)
    new = APOLLO_BAD.sub(APOLLO_GOOD, new)
    new = APOLLO_REF.sub(APOLLO_GOOD, new)
    new = LIMITLESS_BAD.sub(LIMITLESS_GOOD, new)
    for old, fresh in TEXT_FIXES:
        if old in new:
            new = new.replace(old, fresh)
    return new


def main():
    started = time.time()
    list_path = Path('/tmp/bad_url_files.txt')
    files = [ROOT / line.lstrip('./').strip()
             for line in list_path.read_text().splitlines() if line.strip()]
    n_total = len(files)
    n_changed = 0
    for i, fp in enumerate(files, 1):
        try:
            original = fp.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError, FileNotFoundError):
            continue
        new = transform(original)
        if new != original:
            fp.write_text(new, encoding='utf-8')
            n_changed += 1
    elapsed = time.time() - started
    print(f'Done. Files seen: {n_total}, changed: {n_changed}, '
          f'elapsed: {elapsed:.1f}s')


if __name__ == '__main__':
    main()
