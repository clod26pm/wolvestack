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

# Step 2: Check/install language packs
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

# Step 3: Count what needs translating
echo ""
echo "Scanning files..."
TOTAL_HTML=$(ls *.html 2>/dev/null | grep -v 'ARTICLE-TEMPLATE\|404\|search' | wc -l | tr -d ' ')
echo "  $TOTAL_HTML English articles"
echo "  12 target languages"
echo "  $(($TOTAL_HTML * 12)) total translations"

# Step 4: Start translation with caffeinate
echo ""
echo "Starting translation (with caffeinate to prevent sleep)..."
echo "  Log: $LOG"
echo "  PID: $PID_FILE"
echo ""
echo "  To monitor: tail -f $LOG"
echo "  To stop:    kill \$(cat $PID_FILE)"
echo ""

# Run with --force to overwrite fake translations
# caffeinate -i keeps Mac awake (prevents idle sleep)
caffeinate -i python3 translate_site.py --all --force > "$LOG" 2>&1 &
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
