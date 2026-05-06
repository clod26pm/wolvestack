# Internal Linker Run — 2026-05-06

## Context: find-by-mtime is broken
The `find ... -mtime -2` heuristic returned **1,739 root-level HTML files** because a bulk
operation (likely the `polish_translations.py` / `bulk_polish_*.py` scripts in this repo)
re-stamped every article on **2026-05-05 09:56 UTC**. None of those 1,739 files were
genuinely *new*. Per `git log --diff-filter=A`, the most recent batch of newly authored
peptide articles was 2026-04-27 (8 articles), already linked.

## Genuinely new/edited articles in the 48-hour window
Two files have mtimes outside the bulk batch (modified 2026-05-05 03:15–03:16 UTC,
distinct from the 09:56 bulk batch):

- `tirzepatide-results-timeline.html`
- `semaglutide-stacking.html`

Both already had a 5-link Related Guides block at the cap, so **no outbound links were
added** (per the "≤5 links per article" rule).

## Inbound link gap (severe)
Before this run:
- `tirzepatide-results-timeline.html`: **1** root-level inbound link (self-only)
- `semaglutide-stacking.html`: **2** inbound links (self + `peptide-stacking-advanced.html`)

After this run:
- `tirzepatide-results-timeline.html`: **6** inbound links
- `semaglutide-stacking.html`: **7** inbound links

## Files modified (10 total)

### Inbound to `tirzepatide-results-timeline.html`
| File | Mode | Notes |
|---|---|---|
| tirzepatide-how-long-to-see-results.html | fresh | New Related Guides div before `<footer` |
| tirzepatide-before-and-after.html | fresh | New Related Guides div before `<footer` |
| tirzepatide-vs-retatrutide.html | fresh | New Related Guides div before `<footer` |
| tirzepatide-vs-semaglutide.html | append | 5th `<li>` appended to existing list |
| semaglutide-results-timeline.html | inline | New `<li>` inserted into existing list (sibling cross-link) |

### Inbound to `semaglutide-stacking.html`
| File | Mode | Notes |
|---|---|---|
| tirzepatide-and-semaglutide.html | fresh | New Related Guides div before `<footer` |
| tirzepatide-stacking.html | fresh | New Related Guides div before `<footer` |
| semaglutide-and-phentermine.html | fresh | New Related Guides div before `<footer` |
| semaglutide-guide.html | inline | New `<li>` inserted (Related Guides was at cap) |
| best-peptide-stacks.html | inline | New `<li>` inserted (Related Guides was at cap) |

## Verification
- All 10 files have exactly one `<div class="related-articles">` block.
- All 10 files retain `</body>` and `</html>`.
- All 10 link targets resolve to existing files in the root.
- No translated subdirectories (/ar, /es, /de, etc.) were touched.
- No prohibited files (index.html, privacy.html, terms.html, sitemap.xml, robots.txt,
  404.html, about.html, affiliate-disclosure.html) were touched.

## Summary
Processed **2 new articles**, added **0 outbound links** (already at cap),
updated **10 older articles** with inbound links. Net effect: closes a real gap
where two timely 2026 articles had effectively zero discoverability from the
existing library.
