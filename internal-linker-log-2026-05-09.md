# Internal Linker Run — 2026-05-09

## Headline result
- **0 genuinely new articles** detected since the last linker run (2026-05-06).
- **11 files cleaned up**: merged duplicate `<div class="related-articles">` blocks
  that an unlogged prior linker run had left in the working tree.
- **0 outbound links added** (no new articles to add links *from*).
- **0 inbound links added** (no new articles to add links *to*).
- All edits are uncommitted working-tree changes; no commits/pushes made.

## Why "no new articles"

`find -mtime -2` returned 145+ files in the root, but the same diagnostic from
the 2026-05-06 run applies:

| mtime bucket               | files | what it actually is                                        |
|----------------------------|------:|------------------------------------------------------------|
| 2026-05-06 03:08–03:23 UTC | 1,789 | Big bulk-polish batch (already analyzed in last run's log) |
| 2026-05-06 05:38, 05:47    |    11 | Trailing edits from the same bulk-polish wave              |
| 2026-05-07 01:06           |    91 | Another bulk-polish / template re-stamp                    |
| 2026-05-08 01:08           |    35 | Another bulk-polish / template re-stamp                    |

To distinguish polish-only re-stamps from real new content I cross-checked
`git log --diff-filter=A` for files added since 2026-05-06 — only the four
`compatibility-*.html` pages (Compatibility iOS-app marketing pages, not
peptide articles) were genuinely added. All actual peptide articles in the
05-07 / 05-08 buckets first landed in git on 2026-04-09 or 2026-04-23 and
have only been re-stamped since.

The `compatibility-*.html` pages are deliberately excluded from this linker
job: they're iOS-app marketing pages, not part of the peptide research
library, and pulling them into peptide-article Related Guides would be
topically irrelevant link-stuffing.

## What I actually fixed

A previous linker run (between 2026-05-06 and today, no log file written)
appended a second `<div class="related-articles">` block to ~125 files that
already had — or didn't have — one. The 56 files where HEAD had no Related
Guides block ended up with exactly one block (correct, no fix needed). The
11 files where HEAD already had a block ended up with **two** blocks
side-by-side (visual + structural problem; violates rule #6 of the linker
spec: "If an article already has a Related Articles section, add to it
rather than creating a duplicate").

For those 11 files I:
1. Located every `<div class="related-articles">…</div>` block.
2. Extracted every `<li><a href="…">…</a></li>` entry.
3. Dropped self-references and deduped by href (case-insensitive,
   leading-slash normalized), preserving first-seen order.
4. Capped at 5 entries per the spec.
5. Replaced both blocks with a single merged block in the canonical
   committed style (multi-line, indented, no `max-width` override).
6. Verified post-merge: exactly one block, `</body>`/`</html>`/`</article>`
   counts unchanged, every href resolves to a file in the root.

## Files edited (11)

| File | Merged links (final order) |
|---|---|
| ipamorelin-cycle.html | legal, best-time-to-inject, benefits, before-and-after, sermorelin-cycle |
| ipamorelin-for-anti-aging.html | legal, best-time-to-inject, benefits, before-and-after, sermorelin-cycle |
| mk-677-does-it-affect-testosterone.html | legal, for-anti-aging, benefits, dosage, cycle |
| mk-677-does-it-cause-cancer.html | legal, for-anti-aging, benefits, dosage, cycle |
| mk-677-does-it-increase-cortisol.html | legal, for-anti-aging, benefits, dosage, cycle |
| mk-677-for-athletes-over-40.html | legal, for-anti-aging, benefits, dosage, cycle |
| mk-677-for-insomnia.html | legal, for-anti-aging, benefits, dosage, cycle |
| mk-677-for-muscle-wasting.html | legal, for-anti-aging, benefits, dosage, cycle |
| semaglutide-half-life.html | dosage, cycle, guide, faq, results-timeline |
| semaglutide-results-timeline.html | for-weight-loss, dosage, guide, faq, tirzepatide-results-timeline |
| semaglutide-side-effects.html | microdose-semaglutide-guide, post-glp1-weight-maintenance-guide, glp1-comparison-2026, duodenal-mucosal-resurfacing-glp1, liraglutide-vs-semaglutide |

All five-link blocks. Each block is at the spec cap.

## Files NOT touched (and why)

- The other ~56 working-tree-modified files where the prior run added a
  *first* Related Guides block (no duplicate created): left as-is. Single
  block, no rule violation.
- Files where HEAD already had **2 or 3** Related Guides blocks
  pre-committed (e.g. `aod-9604-guide.html`, `peptides-for-sleep.html` with
  4 blocks, etc.): out of scope for this run. Those duplicates predate
  the current linker pipeline and fixing them is a separate cleanup
  project (~55 files, cosmetic but not urgent).
- Translation subdirectories (`/ar`, `/es`, `/de`, etc.): never touched —
  only root English articles are in scope per the spec.
- Prohibited files (`index.html`, `privacy.html`, `terms.html`,
  `404.html`, `about.html`, `affiliate-disclosure.html`): never touched.

## Verification (all 11 files)

- `class="related-articles"` count: 1 (was 2 before merge).
- `</body>`, `</html>`, `</article>` counts: unchanged from HEAD.
- All `href` targets in merged blocks resolve to existing root files.

## Deliverable script

`merge_related_blocks.py` (in the outputs directory) is the merge tool. It
auto-discovers candidates via `git status` + HEAD-vs-working-tree count
comparison, supports `--dry-run`, and validates HTML-structure markers
post-merge. Reusable for any future cleanup pass.

## Summary

Processed **0 new articles**, added **0 outbound links**, added
**0 inbound links**, and **deduped 11 files** that a prior unlogged
linker run had left with side-by-side Related Guides blocks. Net
effect: cleaner DOM, same set of internal links, no broken hrefs.
