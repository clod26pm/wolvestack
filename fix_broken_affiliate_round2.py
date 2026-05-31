#!/usr/bin/env python3
"""Round 2: fix visible bad-domain text labels left behind by round 1."""
import re, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Plain-text label fixes (no scheme, often appearing inside <a> text)
LABEL_FIXES = [
    (r'\bascensionsupps\.com/\?ref=wolvestack\b',
     'ascensionpeptides.com/?ref=wolvestack'),
    (r'\bascensionsupps\.com\b', 'ascensionpeptides.com'),
    (r'\bascensionresearch\.co/\?ref=wolvestack\b',
     'ascensionpeptides.com/?ref=wolvestack'),
    (r'\bascensionresearch\.co\b', 'ascensionpeptides.com'),
    (r'\bascensionsupplements\.com/\?ref=wolvestack\b',
     'ascensionpeptides.com/?ref=wolvestack'),
    (r'\bascensionsupplements\.com\b', 'ascensionpeptides.com'),
    (r'\bapolloresearchcompounds\.com/\?rfsn=9022946\b',
     'apollopeptidesciences.com/?rfsn=9022946'),
    (r'\bapolloresearchcompounds\.com\b', 'apollopeptidesciences.com'),
    (r'\blimitlesslifenoo\.com\b', 'limitlesslifenootropics.com'),
    (r'\blimitlesslifenotropics\.com\b', 'limitlesslifenootropics.com'),
    (r'\blimitlesslifebiotech\.com\b', 'limitlesslifenootropics.com'),
    (r'\blimitless-biohacking\.com\b', 'limitlesslifenootropics.com'),
    (r'\blimitless-peptides\.com\b', 'limitlesslifenootropics.com'),
    (r'\blimitlesspeptides\.com\b', 'limitlesslifenootropics.com'),
]
COMPILED = [(re.compile(p), r) for p, r in LABEL_FIXES]


def transform(text):
    new = text
    for pat, repl in COMPILED:
        new = pat.sub(repl, new)
    return new


def main():
    started = time.time()
    list_path = Path('/tmp/bad_url_files.txt')
    files = [ROOT / line.lstrip('./').strip()
             for line in list_path.read_text().splitlines() if line.strip()]
    n_changed = 0
    for fp in files:
        try:
            original = fp.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError, FileNotFoundError):
            continue
        new = transform(original)
        if new != original:
            fp.write_text(new, encoding='utf-8')
            n_changed += 1
    print(f'Round 2 done. Files seen: {len(files)}, changed: {n_changed}, '
          f'elapsed: {time.time() - started:.1f}s')


if __name__ == '__main__':
    main()
