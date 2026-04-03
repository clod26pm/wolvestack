#!/usr/bin/env bash
# translate_all.sh — Run all language translations in parallel
# Usage: ./translate_all.sh
# Keeps your Mac awake and logs each language to its own file.

set -euo pipefail

LANGS=(es zh ja pt ru it pl fr id de nl ar)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$SCRIPT_DIR/translation-logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)

echo "Starting translations for ${#LANGS[@]} languages at $(date)"
echo "Logs → $LOG_DIR/"
echo ""

PIDS=()

for lang in "${LANGS[@]}"; do
  LOG_FILE="$LOG_DIR/${lang}-${TIMESTAMP}.log"
  echo "  Launching $lang → $LOG_FILE"
  caffeinate -i python3 "$SCRIPT_DIR/translate_site.py" --lang "$lang" \
    > "$LOG_FILE" 2>&1 &
  PIDS+=("$!:$lang")
done

echo ""
echo "All ${#LANGS[@]} translations launched. Waiting for completion..."
echo ""

FAILED=0
for entry in "${PIDS[@]}"; do
  pid="${entry%%:*}"
  lang="${entry##*:}"
  if wait "$pid"; then
    echo "  ✓ $lang finished successfully"
  else
    echo "  ✗ $lang FAILED (exit code $?) — check $LOG_DIR/${lang}-${TIMESTAMP}.log"
    FAILED=$((FAILED + 1))
  fi
done

echo ""
if [ "$FAILED" -eq 0 ]; then
  echo "All translations completed successfully at $(date)"
else
  echo "$FAILED translation(s) failed. Check logs above."
  exit 1
fi
