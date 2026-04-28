#!/bin/bash
# WolveStack — push Phase 11/12/13/14 commits
# These commits exist locally but the bash sandbox couldn't push them
# (each ~30-55MB diff, exceeded 45s timeout). Run from your Mac terminal
# (no timeout), should take 3-5 minutes total.

set -e
cd "$(dirname "$0")"

echo "=========================================="
echo "  WolveStack — Phase 11/12/13/14 Push"
echo "=========================================="
echo

# Increase HTTP buffers so large pushes don't choke
git config http.postBuffer 524288000
git config http.lowSpeedTime 600

# Show what's pending
PENDING=$(git rev-list --count origin/main..main 2>/dev/null || echo "?")
echo "Local main is $PENDING commits ahead of origin/main"
echo
echo "Pending commits:"
git log --oneline origin/main..main
echo
echo "Total file changes:"
git diff --shortstat origin/main main 2>/dev/null
echo

read -p "Press Enter to push all of them to origin/main (or Ctrl-C to abort)..."

echo
echo "==> Pushing all pending commits..."
git push origin main

echo
echo "==> Verifying..."
git fetch origin
LOCAL=$(git rev-parse main)
REMOTE=$(git rev-parse origin/main)
if [ "$LOCAL" = "$REMOTE" ]; then
  echo
  echo "  ✓ SUCCESS — local main matches origin/main"
  echo "  ✓ All Phase 11/12/13/14 work is now live"
  echo
  echo "Next steps:"
  echo "  1. Watch Netlify build: https://app.netlify.com/teams/wolvestack"
  echo "     (Pro plan 3000 credits/mo should comfortably handle these)"
  echo "  2. Once Netlify deploys, in GSC at clod26@pm.me account:"
  echo "     - Sitemaps → resubmit sitemap.xml"
  echo "     - URL Inspection → Request Indexing for top cornerstones:"
  echo "       /en/bpc-157-guide.html, /en/tb-500-guide.html,"
  echo "       /en/semaglutide-guide.html, /en/tirzepatide-guide.html,"
  echo "       /en/retatrutide-guide.html, /en/peptide-beginners-guide.html"
  echo "       (~10/day GSC limit; spread across multiple sessions)"
  echo "  3. Validate FAQ schema renders via Google Rich Results Test:"
  echo "     https://search.google.com/test/rich-results"
  echo
  echo "Recovery monitoring (weekly):"
  echo "  - GSC Performance → Search Results: 7-day trend"
  echo "  - Target: <30 → 200 by week 2 → 600 by week 4 → 900+ by week 8"
else
  echo
  echo "  ⚠ WARNING — local ($LOCAL) != remote ($REMOTE)"
  echo "  Try re-running this script. If it fails again, run manually:"
  echo "    git push origin main --no-verify"
fi
