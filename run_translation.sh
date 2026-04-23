#!/bin/bash
# ============================================================
# WolveStack Full Translation Runner
# ============================================================
# Translates all 1,904 articles to 12 languages using argostranslate.
# Estimated time: 3-4 days on MacBook Air (runs in background).
#
# Usage:
#   cd ~/cowork/peptide-daily-content
#   chmod +x run_translation.sh
#   ./run_translation.sh
#
# To check progress:
#   tail -f translation_progress.log
#
# To stop:
#   kill $(cat translation.pid)
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

LOG="translation_progress.log"
PID_FILE="translation.pid"

echo "============================================================"
echo "  WolveStack Translation Pipeline"
echo "============================================================"
echo ""

# Step 1: Check dependencies
echo "Checking dependencies..."
python3 -c "import argostranslate" 2>/dev/null || {
    echo "Installing argostranslate..."
    pip3 install argostranslate --break-system-packages
}
python3 -c "from bs4 import BeautifulSoup" 2>/dev/null || {
    echo "Installing beautifulsoup4..."
    pip3 install beautifulsoup4 --break-system-packages
}
echo "  Dependencies OK"

# Step 1b: stanza stays installed (argos requires it to import) but
# sbd.py is patched to never USE it (stanza_available = False at EOF).

# Step 2: Check/install language packs (needs internet)
echo ""
echo "Checking language packs..."
python3 -c "
import argostranslate.translate
installed = argostranslate.translate.get_installed_languages()
codes = {l.code for l in installed}
needed = {'es','zh','ja','pt','ru','it','pl','fr','id','de','nl','ar'}
missing = needed - codes
if missing:
    print(f'Missing languages: {missing}')
    print('Installing...')
    import argostranslate.package
    argostranslate.package.update_package_index()
    available = argostranslate.package.get_available_packages()
    for lang in missing:
        pkg = next((p for p in available if p.from_code == 'en' and p.to_code == lang), None)
        if pkg:
            print(f'  Installing en -> {lang}...')
            argostranslate.package.install_from_path(pkg.download())
        else:
            print(f'  WARNING: No package for en -> {lang}')
    print('Done installing language packs')
else:
    print('  All 12 language packs installed')
"

# Step 3: (removed — stanza is uninstalled now, no model needed)

# Step 4: Smoke test — verify translation works OFFLINE
echo ""
echo "Smoke testing offline translation..."
python3 -c "
import os, sys

# Verify stanza is installed but disabled
import argostranslate.sbd
if argostranslate.sbd.stanza_available:
    print('  ⛔ stanza_available is True — patch sbd.py!')
    sys.exit(1)
else:
    print('  ✓ stanza_available = False (regex splitting, no network calls)')

import argostranslate.translate

langs = {'es':'Hola','zh':'你好','ja':'こんにちは','pt':'Olá','ru':'Привет',
         'it':'Ciao','pl':'Cześć','fr':'Bonjour','id':'Halo','de':'Hallo',
         'nl':'Hallo','ar':'مرحبا'}
failed = []
for lang, expected_word in langs.items():
    t = argostranslate.translate.get_translation_from_codes('en', lang)
    if t is None:
        failed.append(f'{lang}: no translator')
        continue
    result = t.translate('Hello, how are you?')
    if result == 'Hello, how are you?':
        failed.append(f'{lang}: returned English unchanged')
    else:
        print(f'  ✓ en→{lang}: \"{result[:50]}\"')
if failed:
    print(f'\n  ⛔ FAILED: {\", \".join(failed)}')
    print('  Fix these before running translation!')
    sys.exit(1)
else:
    print('\n  ✅ All 12 languages translate correctly offline!')
"

# Step 5: Count what needs translating
echo ""
echo "Scanning files..."
TOTAL_HTML=$(ls *.html 2>/dev/null | grep -v 'ARTICLE-TEMPLATE\|404\|search' | wc -l | tr -d ' ')
echo "  $TOTAL_HTML English articles"
echo "  12 target languages"
echo "  $(($TOTAL_HTML * 12)) total translations"

# Step 6: Start translation with caffeinate (fully offline — all models pre-cached)
echo ""
echo "Starting translation (with caffeinate to prevent sleep)..."
echo "  Log: $LOG"
echo "  PID: $PID_FILE"
echo ""
echo "  To monitor: tail -f $LOG"
echo "  To stop:    kill \$(cat $PID_FILE)"
echo ""

# Set env vars for offline operation, then run.
# The script also sets these internally, but belt + suspenders.
export ARGOS_STANZA_AVAILABLE=0
export STANZA_RESOURCES_DIR=/tmp/stanza_resources
caffeinate -i python3 translate_site.py --all >> "$LOG" 2>&1 &
BGPID=$!
echo $BGPID > "$PID_FILE"

echo "  Translation running in background (PID: $BGPID)"
echo "  Safe to close this terminal — it will keep running."
echo ""
echo "  When complete, run:"
echo "    git add -A && git commit -m 'Add real translations for all 12 languages'"
echo "    git push origin main"
echo ""
echo "============================================================"
