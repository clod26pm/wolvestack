# WolveStack Content Gap Tracker — Scorecard

**Run date:** 2026-05-25 (Monday)
**Repo:** clod26pm/wolvestack — branch `main`
**HEAD at run:** `3fe740ce7` — "Compatibility: push May 9 legal updates (Bahamas governing law, compatibility2@pm.me contact)" (2026-05-11)
**Working tree state at run:** HEAD matches origin/main (fetch succeeded; `git pull` failed to write `ORIG_HEAD` because stale `.git/*.lock` files from prior sessions cannot be removed under the sandbox's permission set, but `git log HEAD` and `git log origin/main` resolve to the same SHA so file-existence checks are authoritative). 271 uncommitted working-tree changes are present (233 modified, 38 untracked) — none touch the tracked-article list; details in "Operational Notes" below.

---

## Headline

**Total tracked articles complete: 24 / 24 (100%).**

No change since the 2026-05-11 run. Every Tier 1, Tier 2, and Tier 3 article remains on disk, remains committed to `main`, and continues to exceed the 3,500-word floor from `IMPROVEMENT_CHECKLIST.md`. Smallest tracked file is now `pemvidutide-guide.html` at 3,633 words; largest is `oral-semaglutide-guide.html` at 11,359 words. Word counts have drifted slightly from the May 11 report because the count was re-tokenized with a stricter HTML-strip regex this run — content has not been edited. Confidence: high (direct filesystem check plus `git log --diff-filter=A` for first-commit dates).

---

## Tier-by-Tier Status

### Tier 1 — Highest Impact (10/10 complete)

| File | Status | First commit | Word count |
|---|---|---|---|
| cotadutide-guide.html | EXISTS | 2026-04-19 | 5,217 |
| maritide-guide.html | EXISTS | 2026-04-19 | 4,969 |
| orforglipron-guide.html | EXISTS | 2026-04-19 | 4,764 |
| gonadorelin-guide.html | EXISTS | 2026-04-23 | 5,240 |
| peptides-for-fertility.html | EXISTS | 2026-04-23 | 4,597 |
| peptides-for-pcos.html | EXISTS | 2026-04-23 | 4,272 |
| peptides-for-menopause.html | EXISTS | 2026-04-09 | 7,203 |
| peptides-for-hair-growth.html | EXISTS | 2026-04-23 | 4,072 |
| peptides-for-longevity.html | EXISTS | 2026-04-09 | 4,057 |
| best-peptides-2026.html | EXISTS | 2026-04-19 | 6,234 |

### Tier 2 — Comparison Articles (4/4 complete)

| File | Status | First commit | Word count |
|---|---|---|---|
| oral-vs-injectable-peptides.html | EXISTS | 2026-04-23 | 4,144 |
| semax-vs-selank-vs-cerebrolysin.html | EXISTS | 2026-04-23 | 4,061 |
| bpc-157-vs-tb-500-vs-ghk-cu.html | EXISTS | 2026-04-23 | 3,975 |
| peptides-vs-hgh-therapy.html | EXISTS | 2026-04-23 | 4,048 |

### Tier 3 — Expanding Coverage (7/7 complete)

| File | Status | First commit | Word count |
|---|---|---|---|
| cagrisema-guide.html | EXISTS | 2026-04-23 | 3,926 |
| survodutide-guide.html | EXISTS | 2026-04-23 | 3,788 |
| pemvidutide-guide.html | EXISTS | 2026-04-23 | 3,633 |
| amhr2bp-guide.html | EXISTS | 2026-04-25 | 5,246 |
| peptide-regulations-2026.html | EXISTS | 2026-04-23 | 4,045 |
| how-to-verify-peptide-purity.html | EXISTS | 2026-04-25 | 5,566 |
| peptide-stacking-advanced.html | EXISTS | 2026-04-25 | 5,544 |

### Already Done — re-verified live (3/3)

| File | Status | First commit | Word count |
|---|---|---|---|
| glp1-comparison-2026.html | EXISTS | 2026-04-09 | 7,744 |
| peptides-for-women.html | EXISTS | 2026-04-09 | 5,738 |
| oral-semaglutide-guide.html | EXISTS | 2026-04-09 | 11,359 |

---

## This Week's New Additions (since 2026-05-18)

**Zero commits to `main` in the past seven days.** `git log --since="2026-05-18"` returns empty. The most recent commit on `main` is still `3fe740ce7` from 2026-05-11. No first-commit `A` entries against any of the 24 tracked filenames; none against any other content file either.

This is the **second consecutive Monday with no new tracker additions**, which is consistent with the tracker being at 100% but is also consistent with overall commit throughput on the repo having stalled — the May 11 → May 25 window shows zero pushed commits despite 271 uncommitted edits sitting in the working tree (see Operational Notes). Confidence: high on the commit-log facts, moderate on the interpretation (the working-tree edits may simply be in-flight on the author's machine and not yet pushed; this run cannot distinguish "stalled" from "staged-but-unpushed").

---

## Cumulative Pace (April 9 → today)

| Date | Articles added | Running total |
|---|---|---|
| 2026-04-09 | 5 | 5 |
| 2026-04-19 | 4 | 9 |
| 2026-04-23 | 12 | 21 |
| 2026-04-25 | 3 | 24 |
| 2026-04-25 → 2026-05-25 | 0 | 24 |

The tracker list was completed in **16 calendar days** between 2026-04-09 and 2026-04-25, averaging ~1.5 articles/day with a 12-article publishing burst on 2026-04-23. The 30 calendar days since completion have added zero tracked articles, as expected — the list is exhausted.

---

## Estimated Completion Date at Current Pace

**Not applicable — tracker is at 100% and has been since 2026-04-25 (now thirty days).** No remaining items, no ETA to project.

If a successor priority list were adopted today (see "Next 5 Priorities" below), the historical Apr 9–25 throughput (~1.5 articles/day) would land five articles inside one working week; a one-article-per-day cadence would land them inside seven calendar days; a one-per-week cadence would push completion into early July.

---

## Next 5 Priorities to Write (Recommended Expansion)

Unchanged from the 2026-05-11 report — none of the proposed gaps have been filled in the intervening two weeks, and no fresh keyword pull or content-queue update is available to revise the list. Re-verified absent from `en/` and root by filename scan. Confidence: moderate (based on observable repo gaps and the site's known SEO posture; not a fresh SERP/keyword analysis).

1. **`mazdutide-guide.html`** — Innovent's GLP-1/glucagon dual agonist; cleared Phase 3 in China for obesity. Natural Tier-3 follow-on to `cagrisema-guide`, `survodutide-guide`, `pemvidutide-guide`. Still absent.
2. **`retatrutide-vs-cagrisema.html`** — Both stand-alone guides exist; head-to-head comparison page is the obvious missing piece given the existence of `retatrutide-vs-tirzepatide` and `retatrutide-vs-semaglutide`. Still absent.
3. **`peptides-for-cardiovascular-health.html`** — Umbrella page for the SELECT/SUMMIT-era cardiovascular-outcomes search demand. The repo has fertility, PCOS, menopause, hair, and longevity umbrellas but no cardiovascular one. Still absent.
4. **`peptide-half-life-explained.html`** — High AI-citation candidate; every individual peptide page references half-life but no canonical explainer exists to link them to. Still absent.
5. **`how-to-cycle-peptides.html`** — Companion to `peptide-stacking-advanced.html`. Cycling is the second-most-asked operational question after stacking. Still absent.

Alternative bench (unchanged): `tirzepatide-microdose-vs-microdose-semaglutide.html`, `peptides-for-cognition.html`, `glp1-side-effects-2026.html`, `enlicitide-guide.html`, `muvalaplin-guide.html`.

---

## Operational Notes for Next Run

- **Stale git locks persist and continue to block writes.** `.git/ORIG_HEAD.lock` (May 4 02:43) and `.git/gc.pid.lock` (Apr 28 17:44) are still present, owned by the sandbox user but flagged as "Operation not permitted" on removal. `git pull` fails partway (fetch OK, ref-update fails), and `git commit`/`git push` will fail the same way. This is now a **two-week-old blocker**. Recommended fix: run `rm -f .git/ORIG_HEAD.lock .git/gc.pid.lock .git/index.lock` from the host shell (outside the sandbox) once, or amend the scheduled task to invoke the cleanup with elevated permissions. Without this, the task's "commit + push" step has not executed for at least two consecutive runs.
- **271 uncommitted changes are sitting in the working tree** (233 modified files, 38 untracked). None of them touch tracked priority articles, so the scorecard is unaffected. The modified set is concentrated in legacy root `.html` files (`best-peptide-stacks.html`, `cjc-1295-guide.html`, `dsip-*.html`, `mk-677-*.html`, etc.) — 78 root HTML files have mtimes after 2026-05-11. Per CLAUDE.md, root `.html` should be 301 redirects to `/en/`, so editing them is either a regression to revert or a pattern change to document. The 38 untracked files are mostly content-batch logs, reddit/quora draft logs, featured-log markdown files, and a `content-queue/reddit-topics-2026-05-25.md` — i.e., operational artifacts, not user-facing content. Sweeping this backlog should happen before the next push.
- **The tracker has produced an identical "all-done" report for thirty days running.** The fixed 24-item list is now a static check that will keep returning 24/24 indefinitely. To make the weekly run useful again, replace the static list with a dynamic gap-detection rule — e.g., "any `*-guide.html` referenced by a `content-queue/*.md` entry but not yet present as `en/*.html`", or "any peptide named in `IMPROVEMENT_CHECKLIST.md` with no corresponding guide page." Until that change lands, the scorecard adds little signal and the run could reasonably be downgraded to monthly.
