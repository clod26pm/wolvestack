# Content Batch — 2026-06-10

## Topic Source
- Subreddit signal: r/Peptides + r/Biohackers + retatrutide-specific communities (RetatrutideGBP, Retatrutide, retatrutide4obesity, Peptidesource, etc.)
- Anchor: a brand-new preprint that mined those very subreddits — **Sehgal NK, Tronieri JS, Rader B, Ungar L, Guntuku SC. "Self-Reported Side Effects Among Reddit Users Taking Unapproved Retatrutide." medRxiv 2026.05.28.26352819; posted June 3, 2026.** DOI 10.64898/2026.05.28.26352819 (University of Pennsylvania).
- Why this topic: it is the freshest possible signal (posted 7 days ago) AND it is literally about what r/Peptides users report. The headline finding is genuinely counterintuitive and highly searchable: in 13,589 self-reporting Reddit users, the real-world symptom profile (increased appetite, fatigue, increased energy, nausea, food craving, insomnia, elevated heart rate) **diverges from the GI-dominated phase 2 trial profile**. WolveStack has a large retatrutide cluster (guide, side-effects, safety, vs-tirzepatide, muscle-loss, reconstitution, dosing, etc.) but NOTHING on the real-world-vs-trial divergence or this study. Clear gap, strong search intent, easily supports 3,500+ words, squarely within the research/education remit. Not medical-advice-shaped for an individual.

## Article shipped
- Slug: `retatrutide-real-world-side-effects`
- Title (53 chars): Retatrutide: Real-World Side Effects vs Clinical Trials
- Meta description (150 chars): "A 2026 Penn study of 13,589 Reddit users on gray-market retatrutide found side effects diverge from trials — appetite increase, fatigue, and insomnia lead."
- Tag pill: Safety · Real-World Evidence
- English body word count: **4,343 words** (well above the 3,500 floor)
- H2 sections: 12 (incl. study breakdown, mechanism, trial-vs-real-world table, appetite paradox, fatigue/energy, insomnia/HR, muscle, gray-market, methodology limits, what-it-means, vendors, FAQ)
- FAQ items: 6 (match FAQPage JSON-LD)
- Quick-answer box: EN 143 words (target 134–160 — in range)
- Languages shipped at full fidelity: **en, es, pt, fr** (4 total — meets the en + 3 floor)
- Body word counts per language: en 4,343 · es 5,069 · pt 4,957 · fr 5,189 (Romance expansion as expected)
- Quick-answer word counts: en 143 · es 153 · pt 151 · fr 157 — all in 134–160 range (es/pt/fr quick-answers authored pre-trimmed to avoid the overshoot logged on 06-09)
- Languages deferred for next-run backfill: **de, zh, ja, it, ru, pl, nl, id, ar** (9). Priority order per SKILL: de, zh, ja, it.

## Accuracy notes (facts pulled directly from the preprint, not invented)
- 148,640 retatrutide-related posts/comments from 38,936 unique users (collected May 1 2021 – Dec 31 2025), 6 retatrutide-specific + 21 broader subreddits.
- 13,589 unique users self-reporting current use (relevant content Mar 10 2023 – Dec 31 2025); 9,699 (71.4%) ≥1 extracted concept; 7,823 (57.6%) ≥1 mapped PT after excluding weight/appetite-suppression terms (the analytic denominator).
- LLM validation: self-use classifier 94.4% precision / 97.1% recall; symptom extraction 91.0% PPV / 98.6% recall (manual review of 100 posts each). (The paper's classifier was gpt-5.4-nano; I deliberately did NOT name the specific model vendor in the article to keep the focus on findings.)
- Phase 2 comparator: Jastreboff et al., NEJM 2023;389(6):514–26 — tri-agonist (GIP/GLP-1/glucagon), GI-dominated AEs.
- Google Trends: retatrutide rose from ~0 (pre-mid-2023) to >75% of semaglutide search interest by April 2026.
- FDA warning on unapproved GLP-1/retatrutide products: February 2026.
- NO per-symptom percentages were fabricated — the fetched preprint text gave only the rank-order of PTs (Table 1 numbers not in the HTML), so the article presents rank-order only. This is deliberate.

## Files shipped (12) — explicit `git add` list, never `git add -A`
- en/retatrutide-real-world-side-effects.html (new, English source)
- retatrutide-real-world-side-effects.html (new, root redirect safety net — 301s to /en/ via catchall, no _redirects exception needed for article pages)
- es/retatrutide-real-world-side-effects.html (new)
- pt/retatrutide-real-world-side-effects.html (new)
- fr/retatrutide-real-world-side-effects.html (new)
- en/sitemap.xml · es/sitemap.xml · pt/sitemap.xml · fr/sitemap.xml (added <url> entry + 4 hreflang siblings each)
- sitemap-root.xml (added root /retatrutide-real-world-side-effects.html entry)
- sitemap.xml (sitemap-index — bumped lastmod for en/es/pt/fr to 2026-06-10)
- content-list.txt (appended retatrutide-real-world-side-effects.html)

## Commit
- `d9a56fadb` — "Add Retatrutide Real-World Side Effects (Reddit study) — 4 languages (en/es/pt/fr)" — pushed to https://github.com/clod26pm/wolvestack main
- Verification:
  - `git log -1 --oneline` → d9a56fadb at HEAD ✓
  - Push ref update: `f2ff789b9..d9a56fadb  main -> main` (clean, no rejection) ✓
  - raw.githubusercontent 200 checks: en ✓ es ✓ pt ✓ fr ✓ root ✓ (all HTTP 200)
- Netlify auto-deploy triggered by the push.

## Build helpers (NOT committed — kept untracked, per 06-04 / 06-06 / 06-09 precedent)
- `build_reta_translations.py` — transform engine. Translates text via map FIRST (links still /en/), THEN structural swaps: protects the `hreflang="en"` alternate + the nav-lang-menu English option with sentinels, does a global `/en/ → /{lang}/` swap (fixes canonical, og:url, twitter, JSON-LD url/@id/breadcrumb item, and all internal helper links in one pass), restores sentinels, sets the target language's nav option to `class="active"`, sets `<html lang>` (+ `dir="rtl"` reserved for ar).
- `reta_maps.py` — ES map (hand-authored native Spanish) + zips PT/FR values onto the proven EN keys.
- `reta_vals.py` — PT_VALS and FR_VALS (150 hand-authored native strings each, parallel to the ES key order). Length asserted == key count to prevent silent misalignment.
- No external translation API used. All translation is native, authored in-session.

## QA performed before commit
- EN: 4,343 body words, 143-word quick-answer, 12 H2, 6 FAQ, schema present.
- es/pt/fr: tag counts (h2/h3/td/tr/p/a/div) identical to EN → no broken HTML from string replacement.
- URL integrity per language: canonical→/{lang}/ ✓, og:url→/{lang}/ ✓, JSON-LD url→/{lang}/ ✓, `hreflang="en"` alternate kept at /en/ ✓, nav English option kept at /en/ ✓, exactly one `/en/` link remaining (the nav English option) ✓, nav active class on target language ✓.
- Residual-English sentinel scan: only `gray-market` remained, and only as HTML `id=`/`href="#..."` anchors (correct to keep — they are slugs, not visible prose).
- Sitemap XML well-formedness: all 4 per-language sitemaps + sitemap-index parse clean. sitemap-root.xml throws "unbound prefix" but this is PRE-EXISTING (the committed HEAD version fails identically — the root urlset uses 23,534 `xhtml:link` elements without an `xmlns:xhtml` declaration). Not introduced by this run; my single root entry uses no xhtml prefix and matches the mots-c precedent. Left untouched intentionally.

## Notes / follow-ups for next run
- **Backfill 9 languages** for this article: de, zh, ja, it, ru, pl, nl, id, ar. Pipeline is established and fast: add `XX_VALS` lists (150 entries each, parallel to ES key order) to `reta_vals.py`, wire into `reta_maps.py` MAPS via the same zip pattern, run `python3 build_reta_translations.py de zh ...`. Then a sitemap pass: extend each shipped entry's hreflang siblings (currently 4) and insert entries into each backfilled language's sitemap.xml; bump sitemap-index lastmods. **Arabic needs `dir="rtl"`** — the engine already injects it for `ar`.
- **mots-c-histamine-reactions still has 9 languages pending** from the 06-09 run (de, zh, ja, it, ru, pl, nl, id, ar). Two articles now sharing the same 4-language footprint and the same backfill queue — a dedicated backfill day (no new article) could clear both efficiently if Reddit signal is weak.
- **Quick-answer pre-trim worked**: authoring the es/pt/fr quick-answers directly at ~150 words (instead of literally translating the 143-word EN and overshooting to 180+) avoided the trim-pass churn logged on 06-09. Keep doing this for Romance/expanding languages.
- **The build engine's global `/en/ → /{lang}/` swap with 2 sentinels** is clean and verified — reuse it for future multi-language articles instead of per-element href rewrites. The only gotcha: the JSON-LD headline contains the og:title string as a substring, so longer/more-specific keys must be ordered BEFORE their substrings in the map (handled: headline placed before og:title). And keep JSON-LD answer text byte-identical to the body FAQ answer text (I had a `94.4%` vs `94.4 percent` mismatch that left one body FAQ answer untranslated until I made them identical).
- **Topic backlog**: the same Penn group published a prior semaglutide/tirzepatide Reddit side-effect study (Nature Health, 2026 Apr 10). A "what Reddit says about Ozempic/Mounjaro side effects vs the label" companion piece is a natural follow-up if that study or a related thread re-trends. Also the FDA Feb 2026 unapproved-GLP-1 warning could anchor a standalone "is gray-market retatrutide safe / legal" explainer.
- **Reddit access this run**: WebSearch surfaced the medRxiv preprint and the ppc.land/404media meta-story directly; the medRxiv full text fetched cleanly via web_fetch (it was in the provenance set after the search). Did NOT need the redlib/Chrome path this time. Note: r/Biohackers restricted new peptide/HRT standalone posts in late May 2026 (404 Media, June 3) due to AEO manipulation — worth watching, as it may thin future Biohackers signal and push discussion to retatrutide-specific subs.
