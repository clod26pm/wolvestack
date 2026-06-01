# WolveStack Content Gap Tracker — Scorecard

**Report date:** 2026-06-01 (Monday)
**Total priority articles:** 24 / 24 complete (100%)
**Status:** All Tier 1, Tier 2, and Tier 3 priority articles are present at repo root and mirrored in `/en/`.

---

## Tier 1 — Highest Impact (10 / 10)

| # | File | Status | Root size | First committed |
|---|------|--------|----------:|-----------------|
| 1 | cotadutide-guide.html | EXISTS | 67,558 B | 2026-04-19 |
| 2 | maritide-guide.html | EXISTS | 60,054 B | 2026-04-19 |
| 3 | orforglipron-guide.html | EXISTS | 58,484 B | 2026-04-19 |
| 4 | gonadorelin-guide.html | EXISTS | 51,879 B | 2026-04-23 |
| 5 | peptides-for-fertility.html | EXISTS | 46,564 B | 2026-04-23 |
| 6 | peptides-for-pcos.html | EXISTS | 43,664 B | 2026-04-23 |
| 7 | peptides-for-menopause.html | EXISTS | 77,164 B | 2026-04-09 |
| 8 | peptides-for-hair-growth.html | EXISTS | 42,510 B | 2026-04-23 |
| 9 | peptides-for-longevity.html | EXISTS | 42,762 B | 2026-04-09 |
| 10 | best-peptides-2026.html | EXISTS | 63,979 B | 2026-04-19 |

## Tier 2 — Comparison Articles (4 / 4)

| # | File | Status | Root size | First committed |
|---|------|--------|----------:|-----------------|
| 1 | oral-vs-injectable-peptides.html | EXISTS | 43,288 B | 2026-04-23 |
| 2 | semax-vs-selank-vs-cerebrolysin.html | EXISTS | 43,312 B | 2026-04-23 |
| 3 | bpc-157-vs-tb-500-vs-ghk-cu.html | EXISTS | 42,017 B | 2026-04-23 |
| 4 | peptides-vs-hgh-therapy.html | EXISTS | 42,684 B | 2026-04-23 |

## Tier 3 — Expanding Coverage (7 / 7)

| # | File | Status | Root size | First committed |
|---|------|--------|----------:|-----------------|
| 1 | cagrisema-guide.html | EXISTS | 41,212 B | 2026-04-23 |
| 2 | survodutide-guide.html | EXISTS | 39,356 B | 2026-04-23 |
| 3 | pemvidutide-guide.html | EXISTS | 38,167 B | 2026-04-23 |
| 4 | amhr2bp-guide.html | EXISTS | 51,288 B | 2026-04-25 |
| 5 | peptide-regulations-2026.html | EXISTS | 43,929 B | 2026-04-23 |
| 6 | how-to-verify-peptide-purity.html | EXISTS | 54,253 B | 2026-04-25 |
| 7 | peptide-stacking-advanced.html | EXISTS | 54,119 B | 2026-04-25 |

## Already Done — Verified Still Live (3 / 3)

| # | File | Status | Root size | First committed |
|---|------|--------|----------:|-----------------|
| 1 | glp1-comparison-2026.html | EXISTS | 82,691 B | 2026-04-09 |
| 2 | peptides-for-women.html | EXISTS | 58,663 B | 2026-04-09 |
| 3 | oral-semaglutide-guide.html | EXISTS | 114,801 B | 2026-04-09 |

---

## This Week's New Additions (since 2026-05-25)

**No new priority articles were added since last Monday.** The 24-article priority list has been complete since 2026-04-25. The May 31 modifications across these files were sweeping site-wide fixes (broken affiliate URLs, cross-language link bleed, legal-page CSS) applied by the `Site-wide fix: broken affiliate URLs (4465 files), cross-lang link bleed (21757 files)` commit — not new content.

## Next 5 Priorities to Write

The original 24-article tracker is exhausted. Recommended additions to a refreshed priority list, ordered by current SEO + commercial value (high confidence on (1)–(3); moderate on (4)–(5)):

1. **retatrutide-guide.html** — triple agonist (GLP-1 / GIP / glucagon); Lilly Phase 3 readouts are the highest-volume new GLP-1 search target not yet covered.
2. **ecnoglutide-guide.html** — emerging GLP-1 cAMP-biased agonist with Chinese Phase 3 data; almost no English long-form coverage; first-mover SEO opening.
3. **mazdutide-guide.html** — GLP-1 / glucagon dual agonist nearing approval in China (Innovent); growing search volume, very thin existing coverage.
4. **peptides-for-skin-aging.html** — high commercial intent (GHK-Cu / copper peptides / matrixyl); strong affiliate fit and currently missing as a hub page.
5. **tirzepatide-vs-retatrutide.html** — head-to-head comparison piece designed to capture mid-funnel intent once (1) ships; pairs with existing `glp1-comparison-2026.html`.

## Estimated Completion Date at Current Pace

**N/A — current scorecard is 100% complete.** From the original 24 priority articles, the first batch landed 2026-04-09 and the last (Tier 3 finishers) on 2026-04-25 — a 16-day completion window at roughly 1.5 articles/day. If a refreshed 5-article list (above) is adopted at the same historical cadence, projected completion is **~2026-06-04** (3–4 working days from this report).

---

## Operational Notes (not part of scorecard)

- `git pull origin main` could not fast-forward: local `main` has 2 commits and `origin/main` has 3 divergent commits (the upstream `Fix broken affiliate URLs in article generator` series, `f17e82071` → `d6063673d`). The working tree also carries a large set of staged/unstaged changes from the prior site-wide fix run. **No merge or push was performed beyond the report commit** to avoid entangling unrelated changes. A human should reconcile the divergence (likely `git pull --no-rebase` after reviewing the upstream three commits) before the next scheduled run.
- All 24 files also exist under `/en/` (canonical English directory), consistent with the project's hreflang structure.
