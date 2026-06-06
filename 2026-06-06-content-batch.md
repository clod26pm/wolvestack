# Content Batch — 2026-06-06

## Run type: BACKFILL (no new Reddit topic this run)

Deliberate choice. The 2026-06-04 run shipped `klow-blend-guide` in only 4 of 13
languages (en, es, pt, fr) and explicitly parked 9 for next-run backfill. No run
fired on 2026-06-05 (no batch log exists), so the backfill was still outstanding.
Rather than start a *second* fragmentary article and leave klow perpetually
incomplete, this run completed the documented follow-up: native translations of
`klow-blend-guide` into the next priority languages.

Reddit mining was technically available (Chrome MCP connected; redlib mirror path
in MEMORY.md works), but finishing started work took priority over opening a new
front. New-topic mining resumes next run.

## Article backfilled
- Slug: `klow-blend-guide`
- Title: KLOW Peptide Blend: What the 4-Compound Stack Does
- Tag: Research Guide · Stacks
- Languages ADDED this run (native, hand-authored — no MT API): **de, it, nl**
- klow now live in **7 languages**: en, es, pt, fr, de, it, nl
- Body word counts (new langs): de 4,161 · it 4,871 · nl 4,371
- Quick-answer box word counts (target 134–160): de 148 · it 147 · nl 151 — all in range
  (it initially measured 169, trimmed to 147)

## Languages still deferred (6)
**zh, ja, ru, pl, id, ar** — for future backfill runs. Priority order per SKILL:
ru, pl, then zh, ja, then id, then ar (RTL, needs `IS_RTL=True` flag → `dir="rtl"`).

## Files changed (11) — scoped git add, never `git add -A`
- de/klow-blend-guide.html (new)
- it/klow-blend-guide.html (new)
- nl/klow-blend-guide.html (new)
- en/sitemap.xml · es/sitemap.xml · pt/sitemap.xml · fr/sitemap.xml
  (klow entry hreflang siblings extended 4 → 7; entry lastmod bumped to 2026-06-06)
- de/sitemap.xml · it/sitemap.xml · nl/sitemap.xml
  (new klow <url> entry inserted, 7 hreflang siblings each)
- sitemap.xml (sitemap-index — lastmod bumped to 2026-06-06 for en/es/pt/fr/de/it/nl)

content-list.txt unchanged — `klow-blend-guide.html` was already appended on 06-04.
Root `/klow-blend-guide.html` unchanged — it is the English redirect safety net.

## Commit
- `d7ed8ce8b` — "Backfill KLOW blend guide translations — de, it, nl (now 7 languages)"
- Pushed: `ca0cacee2..d7ed8ce8b  main -> main` (no rejection)
- Verification: `git log -1` shows d7ed8ce8b at HEAD; push reported clean ref update.
  (raw.githubusercontent HTTP check skipped — blocked by fetch-provenance rules this
  session; push success line is authoritative.)
- Netlify auto-deploys on push.

## Build helpers (NOT committed — kept untracked, per 06-04 precedent)
- `gen-klow-trans.py` — generates `trans-klow-<lang>.py` from `klow_keys.json` (exact
  EN source phrases) + `values-<lang>.json` (hand-authored native text). Using a JSON
  values array keyed positionally guarantees the 167 dict keys match the EN source
  byte-for-byte (avoids hand-escaping HTML-laden keys).
- `klow_keys.json` — the 167 canonical EN source phrases (extracted from trans-klow-fr.py).
- `values-de.json` · `values-it.json` · `values-nl.json` — native translation arrays.
- `trans-klow-de.py` · `trans-klow-it.py` · `trans-klow-nl.py` — generated dicts.
- `update-klow-sitemaps.py` — deterministic sitemap extender (this run's logic).

## Notes / follow-ups for next run
- **Next backfill batch**: ru, pl (then zh, ja, id, ar). Reuse the pipeline:
  write `values-<lang>.json` (167 entries, same order as klow_keys.json) → run
  `python3 gen-klow-trans.py <lang>` (add `--rtl` for ar) → `python3 build-klow-translations.py`
  → `python3 update-klow-sitemaps.py` after editing its SHIPPED/NEW_ENTRY lists to
  include the new langs and extend the existing entries' sibling sets.
- **update-klow-sitemaps.py is run-specific**: its OLD_SIBLINGS currently encodes the
  4-lang set. For the next run, OLD_SIBLINGS must be regenerated to the *current* 7-lang
  set before extending to 9, etc. Re-derive it from one already-shipped sitemap rather
  than hardcoding.
- **HTML hreflang convention confirmed**: the klow HTML files carry the FULL 13-language
  hreflang block + x-default from the EN source (so 6 langs still point at not-yet-shipped
  404s). The SITEMAP, by contrast, lists only shipped langs. This split is the existing
  project pattern — don't "fix" the HTML to 7; it self-heals as langs ship.
- **Git env**: stale `.git/index.lock` and `tmp_obj` unlink warnings recur (macOS
  file-flag attribution blocks unlink from the Linux sandbox). `mv` the lock aside;
  the `tmp_obj`/unlink warnings during add/commit/push are harmless (objects written,
  only temp cleanup fails). Commit + push both succeeded despite them.
- **New-topic engine**: resume Reddit mining next run. KLOW/GLOW family is now well
  covered (klow guide in 7 langs); a dedicated GLOW guide remains the obvious adjacent
  topic if GLOW Reddit signal is strong.
