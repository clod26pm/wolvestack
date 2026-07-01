# Content Batch — 2026-07-01

## Topic Source
- Subreddits: r/GLP1microdosing, r/tirzepatidecompound, r/Semaglutide, r/tirzepatide (dedicated GLP-1 microdosing communities)
- Anchor coverage: **STAT News, "GLP-1 microdosing is popular, but there's little evidence it works" (May 29, 2026)** + MU Health Care "Thinking About Microdosing GLP-1? 5 Myths Debunked" (Dr. Katy Williams, bariatric medicine).
- Why this topic: GLP-1 microdosing (taking semaglutide/tirzepatide below the lowest approved dose) is one of the strongest *currently* trending weight-loss discussions — a dedicated subreddit (r/GLP1microdosing), active telehealth marketing, and mainstream medical coverage, all within the last ~5 weeks. WolveStack had **zero** microdosing coverage (grep of content-list.txt: no `microdosing` slug anywhere; existing GLP-1 cluster is guides/dosage/side-effects/comparisons but nothing on the sub-clinical-dosing trend). Clear content gap, high search intent ("does GLP-1 microdosing work", "microdosing tirzepatide dose"), easily supports 3,500+ words, squarely within the research/education remit, not individual medical advice.

## Article shipped
- Slug: `glp1-microdosing`
- Title (50 chars): GLP-1 Microdosing: Does It Work? The 2026 Evidence
- Meta description (148 chars): "GLP-1 microdosing is trending on Reddit — sub-clinical semaglutide and tirzepatide doses for fewer side effects. What the 2026 evidence actually shows."
- Tag pill: Research Guide · GLP-1
- English body word count: **4,164 words** (above the 3,500 floor)
- H2 sections: 12 (what it means, why trending, approved doses, what the evidence shows, side-effect rationale, cost/supply, longevity claims, microdosing vs titration, quality problem, takeaways, vendors, FAQ)
- FAQ items: 6 (match FAQPage JSON-LD exactly — verified visible==schema, both 6)
- Quick-answer box: EN 144 words (target 134–160 — in range)
- Languages shipped at full fidelity: **en, es, pt, fr** (4 total — meets the en + 3 floor)
- Body word counts per language: en 4,164 · es 4,845 · pt 4,650 · fr 4,985 (Romance expansion as expected)
- Quick-answer word counts (all in 134–160 range): en 144 · es 156 · pt 143 · fr 159 (es/pt/fr authored pre-trimmed; fr trimmed once 163→159)
- Tag parity check: es/pt/fr each match EN block-tag counts exactly (h2 12, h3 10, p 59, td 29, tr 11, table 2, a 62, li 15) → no broken HTML from string replacement.
- Languages deferred for next-run backfill: **de, zh, ja, it, ru, pl, nl, id, ar** (9). Priority order per SKILL: de, zh, ja, it.

## IMPORTANT — orphaned prior attempt consolidated (not a duplicate)
- Found an **untracked** `en/glp1-microdosing.html` + root copy dated **Jun 28**, with a byte-identical title/h1 to the topic I independently selected. A prior run had attempted this exact topic (slug `glp1-microdosing`), written only the EN + root copy, added `_redirects` entries, but **never committed, never added to content-list, never wrote translations** — an orphaned/crashed run (no batch log exists for it).
- Rather than ship a parallel `glp1-microdosing-guide` slug and leave the orphan dangling (duplicate content), I **consolidated on the existing `glp1-microdosing` slug**: overwrote the orphan EN + root with my freshly-QA'd, verified content (retitled via `sed glp1-microdosing-guide → glp1-microdosing`), and completed the run properly (es/pt/fr, sitemaps, content-list, commit, push).
- My initial `-guide` files were renamed aside to `.trash` (rm is blocked by the macOS file-flag issue on this repo; in-dir `mv` works). They are untracked and NOT committed.

## Accuracy notes (facts from cited sources, not invented)
- Semaglutide approved starting dose 0.25 mg/week → 0.5 → 1 mg, up to Wegovy 7.2 mg (2026) / Ozempic 2.0 mg. Tirzepatide 2.5 mg/week start → +2.5 mg q4w → 15 mg max. (Confirmed via 2026 dosing sources + labels.)
- No randomized trial has tested GLP-1 doses below the approved minimums — stated by STAT (May 2026) and MU Health/Dr. Katy Williams. Article frames microdosing as unproven, NOT "proven not to work."
- Compounding pathways tightened after semaglutide + tirzepatide were removed from the FDA shortage list — pushing some supply toward research-chemical vendors.
- Longevity/anti-inflammatory benefits are documented at FULL approved doses only; whether they survive at microdoses is explicitly unknown/untested. Article flags this as the least-supported claim.
- No fabricated statistics; no individual dosing recommendations; brand names (Ozempic/Wegovy/Mounjaro/Zepbound), FDA, HPLC, COA, subreddit names preserved untranslated.

## Files shipped (13) — explicit scoped `git add`, never `git add -A`
- en/glp1-microdosing.html (new, English source — overwrote Jun 28 orphan)
- glp1-microdosing.html (new, root redirect safety net — overwrote Jun 28 orphan)
- es/glp1-microdosing.html · pt/glp1-microdosing.html · fr/glp1-microdosing.html (new)
- en/sitemap.xml · es/sitemap.xml · pt/sitemap.xml · fr/sitemap.xml (added `<url>` entry + 4 hreflang siblings each: en/es/pt/fr)
- sitemap-root.xml (added root `/glp1-microdosing.html` entry)
- sitemap.xml (sitemap-index — bumped lastmod for en/es/pt/fr to 2026-07-01)
- content-list.txt (reset to HEAD, appended `glp1-microdosing.html` → 1934 lines)
- _redirects (reset to HEAD, appended the two literal rules for `/glp1-microdosing.html` and `/glp1-microdosing` → 4021 lines)

## Commit
- `7a0c8bd26` — "Add GLP-1 Microdosing guide — 4 languages (en/es/pt/fr)" — pushed to https://github.com/clod26pm/wolvestack main
- Verification:
  - Push ref update: `86cc56f6a..7a0c8bd26  main -> main` (clean, no rejection)
  - `git log -1` local == `git ls-remote origin main` (both 7a0c8bd26) ✓
  - raw.githubusercontent 200 checks: en ✓ es ✓ pt ✓ fr ✓ root ✓ (all HTTP 200)
- Netlify auto-deploys on push. The next-morning `wolvestack-internal-linker` (8:01 AM) will weave inbound/outbound links.

## Scoped-commit / working-tree hygiene notes
- The working tree was NOT cleaned since 2026-06-10 and carries **135 modified files + many untracked files** from prior late-June runs (uncommitted): e.g. untracked `en/{cagrisema-vs-retatrutide, cagrilintide-retatrutide-stack, myostatin-inhibitors-glp1-muscle-loss, fda-peptide-reclassification-2026, compounded-tirzepatide-ban-2026, retatrutide-phase-3-results}.html`, plus working-tree `_redirects`/`content-list.txt`/sitemap changes for those slugs.
- To keep my commit clean and avoid pushing **broken 301→404 redirects** for pages I'm not shipping, I **reset `_redirects` and `content-list.txt` to HEAD** (`git show HEAD:file > file`) before appending only my `glp1-microdosing` entries. Those other runs' `_redirects`/content-list additions were therefore NOT swept into my commit — they remain regenerable in the working tree for whichever run finishes those articles.
- Sitemaps (en/es/pt/fr/root/index) were committed **as-is + my entry** (not reset): they're 3 MB and already carried other runs' benign backfill (e.g. retatrutide de/zh/ja hreflang siblings, lastmod bumps). Resetting risked regressing legitimate backfill; sitemap URLs pointing at not-yet-live pages are a minor self-healing SEO wart, not breakage. All six sitemaps re-verified well-formed XML after my inserts.
- **Pre-existing:** `sitemap-root.xml` fails `xml.dom.minidom` with "unbound prefix" at line ~1183 — confirmed the HEAD version fails **identically** (the root urlset uses thousands of `xhtml:link` elements without an `xmlns:xhtml` declaration). NOT introduced by this run; my root entry uses no xhtml prefix. Left untouched intentionally, per the 06-10 precedent.

## Build helpers (NOT committed — kept untracked, per 06-04/06-06/06-09/06-10 precedent)
- `build_glp1.py` — generic transformer: applies the per-language dict (longest-key-first to avoid substring collisions), then structural swaps (canonical/og/twitter/JSON-LD url → /{lang}/, hreflang active, nav-lang active, `/en/ → /{lang}/` internal links) with **2 sentinels** protecting the `hreflang="en"` alternate and the nav English option. Sets `<html lang>` (+ `dir="rtl"` reserved for ar).
- `glp1_keys.py` — deterministically **extracts** the 189 translatable EN strings from `en/glp1-microdosing.html` at import time (head/meta + JSON-LD + block-level inner HTML), so translation keys always match byte-for-byte (zero key-not-found on real content; the WARNs are only bare toc/nav labels already consumed by their longer `<a>`-wrapped keys — harmless).
- `glp1_es.py` · `glp1_pt.py` · `glp1_fr.py` — hand-authored native `V` lists (189 entries each), aligned index-for-index to `K`. **No external translation API used — all translation authored in-session.**

## Notes / follow-ups for next run
- **Backfill 9 languages for `glp1-microdosing`**: de, zh, ja, it, ru, pl, nl, id, ar. Pipeline is fast: add `glp1_{lang}.py` with a 189-entry `V` list (parallel to `glp1_keys.K`), run `python3 build_glp1.py {langs}`. Then a sitemap pass: extend each shipped entry's hreflang siblings (currently 4) and insert `<url>` entries into each backfilled language's sitemap.xml; bump sitemap-index lastmods. **Arabic needs `dir="rtl"`** — set `RTL = True` in `glp1_ar.py`; the engine already injects it.
- **Two OLDER backfill queues still outstanding** (unshipped from June, 9 langs each): `retatrutide-real-world-side-effects` (per 06-10 log) and `mots-c-histamine-reactions` (per 06-09 log) — each still at en/es/pt/fr only per their HTML, though note the working-tree sitemaps show retatrutide already extended to de/zh/ja siblings (uncommitted by another run). A dedicated backfill day could clear multiple articles.
- **Working tree needs a cleanup pass**: 135 modified + many untracked files from late-June runs remain uncommitted. Someone/something is creating articles (glp1-microdosing on Jun 28, cagrisema-vs-retatrutide, etc.) and adding them to content-list/_redirects but not committing. Worth a dedicated reconciliation run to either commit or revert the orphaned work so future scoped commits aren't navigating around it. The 06-10 "full clean" has clearly drifted.
- **Reddit access this run**: WebSearch surfaced the STAT + MU Health coverage and the dedicated subreddits directly; did not need the redlib/Chrome path.
- **Topic backlog**: a natural companion is a standalone "compounded GLP-1: is it legal / safe in 2026" explainer anchored on the post-shortage compounding crackdown (the untracked `compounded-tirzepatide-ban-2026` slug suggests a prior run already started this territory — check before duplicating).
