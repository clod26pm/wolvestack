#!/usr/bin/env python3
"""Round 2 - fix visible bad-domain text labels. Reads file list, in-place."""
import re, sys, time, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LABEL = [
    (re.compile(r'\bascensionsupps\.com/\?ref=wolvestack\b'),
     'ascensionpeptides.com/?ref=wolvestack'),
    (re.compile(r'\bascensionsupps\.com\b'), 'ascensionpeptides.com'),
    (re.compile(r'\bascensionresearch\.co/\?ref=wolvestack\b'),
     'ascensionpeptides.com/?ref=wolvestack'),
    (re.compile(r'\bascensionresearch\.co\b'), 'ascensionpeptides.com'),
    (re.compile(r'\bascensionsupplements\.com/\?ref=wolvestack\b'),
     'ascensionpeptides.com/?ref=wolvestack'),
    (re.compile(r'\bascensionsupplements\.com\b'), 'ascensionpeptides.com'),
    (re.compile(r'\bapolloresearchcompounds\.com/\?rfsn=9022946\b'),
     'apollopeptidesciences.com/?rfsn=9022946'),
    (re.compile(r'\bapolloresearchcompounds\.com\b'), 'apollopeptidesciences.com'),
    (re.compile(r'\blimitlesslifenoo\.com\b'), 'limitlesslifenootropics.com'),
    (re.compile(r'\blimitlesslifenotropics\.com\b'), 'limitlesslifenootropics.com'),
    (re.compile(r'\blimitlesslifebiotech\.com\b'), 'limitlesslifenootropics.com'),
    (re.compile(r'\blimitless-biohacking\.com\b'), 'limitlesslifenootropics.com'),
    (re.compile(r'\blimitless-peptides\.com\b'), 'limitlesslifenootropics.com'),
    (re.compile(r'\blimitlesspeptides\.com\b'), 'limitlesslifenootropics.com'),
]


def main():
    t0 = time.time()
    # Get file list freshly via ripgrep
    out = subprocess.run(
        ['rg', '-l',
         'ascensionsupps\\.com|ascensionresearch\\.co|ascensionsupplements\\.com|'
         'apolloresearchcompounds\\.com|limitlesslifenoo\\.com|'
         'limitlesslifenotropics\\.com|limitlesslifebiotech\\.com|'
         'limitless-biohacking\\.com|limitless-peptides\\.com|'
         'limitlesspeptides\\.com',
         '-g', '*.html', '.'],
        cwd=str(ROOT), capture_output=True, text=True, timeout=25,
    )
    paths = [ROOT / p.lstrip('./').strip()
             for p in out.stdout.splitlines() if p.strip()]
    print(f'Files to fix: {len(paths)} (rg time: {time.time()-t0:.1f}s)')
    n_changed = 0
    for fp in paths:
        try:
            t = fp.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError, FileNotFoundError):
            continue
        new = t
        for pat, repl in LABEL:
            new = pat.sub(repl, new)
        if new != t:
            fp.write_text(new, encoding='utf-8')
            n_changed += 1
    print(f'Round 2 done. Changed: {n_changed}, elapsed: {time.time()-t0:.1f}s')


if __name__ == '__main__':
    main()
