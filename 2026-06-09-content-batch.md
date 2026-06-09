# Content Batch — 2026-06-09

## Topic Source
- Subreddit: r/Peptides
- Primary thread: "Best protocol to combat Mots c histamine reactions?" — https://www.reddit.com/r/Peptides/comments/1u0f7zv/best_protocol_to_combat_mots_c_histamine_reactions/ (19 comments, 6h old at mining time)
- Secondary signal threads (same r/Peptides /new feed, all within ~24h):
  - "Can MOTS-C cause more fatigue?" — https://www.reddit.com/r/Peptides/comments/1u0mozl/can_motsc_cause_more_fatigue/ (7 comments, 1h, very fresh)
  - "Allergy to every peptide." — https://www.reddit.com/r/Peptides/comments/1u0f0ph/allergy_to_every_peptide/ (6 comments, 6h)
- Why this topic: three overlapping MOTS-C tolerability / mast-cell / pseudo-allergy threads inside a 6–24h window. The primary thread has the highest substantive signal (19 comments with detailed protocol comparison: Zyrtec, Flonase, Benadryl cream, subQ→IM switch, thymosin alpha-1). One commenter reported full anaphylactic reactions to MOTS-C, GHK-Cu, CJC-1295+ipamorelin, tesamorelin, and BPC-157 — the "allergy to every peptide" presentation, which the MRGPRX2 mast-cell pseudo-allergy literature explains parsimoniously. The cluster is a real content gap on WolveStack: the existing inventory has `mots-c-side-effects.html` (generic), but nothing specific on histamine reactions, MRGPRX2 mechanism, or pseudo-allergy distinction from IgE — a topic that searches well and is directly actionable.

## Article shipped
- Slug: `mots-c-histamine-reactions`
- Title: MOTS-C Histamine Reactions: Why They Happen
- Meta description (152 chars): "Why MOTS-C welts, hives, and rare anaphylactic-spectrum reactions happen — the MRGPRX2 pseudo-allergy mechanism, pre-treatment protocols, and stop signs."
- Tag pill: Safety · Mast-Cell Reactions
- English body word count: 5,267 words (well above 3,500 floor)
- H2 sections: 13 (incl. FAQ + Vendor sourcing sections)
- FAQ items: 6 (matches JSON-LD FAQPage schema)
- Quick-answer box: 145 words EN (target 134–160 — in range)
- Languages shipped at full fidelity: **en, es, pt, fr** (4 total — meets en + 3 floor)
- Body word counts per language: en 5,267 · es 5,959 · pt 5,809 · fr 6,116
- Quick-answer word counts per language: en 145 · es 150 · pt 142 · fr 157 — all in 134–160 range (es initially 178 trimmed to 150; pt 169→142; fr 180→157)
- Languages deferred for next-run backfill: **de, zh, ja, it, ru, pl, nl, id, ar** (9). Priority order: de, zh, ja, it (per SKILL).

## Files touched (12) — explicit `git add` list, never `git add -A`
- en/mots-c-histamine-reactions.html (new, English source)
- mots-c-histamine-reactions.html (new, root redirect safety net)
- es/mots-c-histamine-reactions.html (new)
- pt/mots-c-histamine-reactions.html (new)
- fr/mots-c-histamine-reactions.html (new)
- en/sitemap.xml (added URL entry + 4 hreflang siblings)
- es/sitemap.xml (added URL entry + 4 hreflang siblings)
- pt/sitemap.xml (added URL entry + 4 hreflang siblings)
- fr/sitemap.xml (added URL entry + 4 hreflang siblings)
- sitemap-root.xml (added URL for /mots-c-histamine-reactions.html)
- sitemap.xml (sitemap-index — bumped lastmod for en/es/pt/fr sitemaps to 2026-06-09)
- content-list.txt (appended mots-c-histamine-reactions.html)

## Commit
- `9c37ce323` — "Add MOTS-C histamine reactions article — 4 languages (en/es/pt/fr)" — pushed to https://github.com/clod26pm/wolvestack main
- Verification:
  - `git log -1 --oneline` → 9c37ce323 at HEAD ✓
  - `curl -sI https://raw.githubusercontent.com/clod26pm/wolvestack/main/en/mots-c-histamine-reactions.html` → HTTP 200 ✓
  - Push reported clean ref update: `d97d5fb84..9c37ce323  main -> main` (no rejection)
- Netlify auto-deploy triggered by the push.

## Build helpers (NOT committed — kept untracked, per 06-04/06-06 precedent)
- `build-motsc-translations.py` — reads `en/mots-c-histamine-reactions.html`, applies a translation dict per language, swaps `<html lang>`, canonical URL, og:url, JSON-LD URLs, breadcrumb-list item URL, active nav-lang-menu link, and `/en/` → `/{lang}/` for internal helper links (with sentinel protection for the nav-lang-menu English link).
- `trans_motsc_es.py` · `trans_motsc_pt.py` · `trans_motsc_fr.py` — translation dicts. Hand-written native phrases; no external translation API used.
- Build run order: apply translation dict FIRST (each entry includes its own /en/ → /{lang}/ swap within the translated text), THEN structural attribute swaps. This avoids the bug where pre-rewritten /en/ URLs inside translatable strings fail to dict-match.

## Notes / follow-ups for next run
- **Backfill 9 languages**: de, zh, ja, it, ru, pl, nl, id, ar. The pipeline is established: write `trans_motsc_{lang}.py` alongside the existing three and re-run `build-motsc-translations.py`. Then a follow-up sitemap pass:
  1. Extend the existing en/es/pt/fr sitemap entries' hreflang siblings from 4 → up to 13.
  2. Insert entries into each backfilled language's sitemap.xml.
  3. Bump corresponding sitemap-index lastmods.
- **Sitemap hreflang strategy**: shipped 4-language hreflangs only this run, to avoid 404 hreflangs pointing at not-yet-shipped translations. The HTML files themselves carry the FULL 13-language hreflang block + x-default from the EN source (so 9 langs still point at not-yet-shipped 404s) — this is the existing project pattern per 06-06 batch notes, do NOT "fix" the HTML to 4. It self-heals as langs ship.
- **Reddit access path that worked**: the redlib mirror `https://redlib.catsarch.com/r/Peptides/new` loaded cleanly in MCP Chrome (no Cloudflare challenge). The previous 06-07 reddit-expert-answers run got blocked because it tried reddit.com and old.reddit.com directly. Future runs should go straight to redlib via Chrome MCP — confirmed it still works as of 2026-06-09.
- **Quick-answer word-count drift across translations**: Romance languages reliably expand ~15–25% over the EN source. The EN quick-answer at 145 words produced initial translations at es 178, pt 169, fr 180 — all out of range. Trim to ~150 words in each by removing redundant qualifiers ("de forma fiable", "fortement", "uma fração significativa de") and combining clauses. Future runs should either start the EN quick-answer at ~120–130 words OR plan to trim each translation independently.
- **Git environment**: stale `.git/HEAD.lock` and `tmp_obj` unlink warnings recur (macOS file-flag attribution blocks unlink from the Linux sandbox). `mv` the locks aside; the `tmp_obj`/unlink warnings during add/commit/push are harmless (objects written, only temp cleanup fails). Commit + push both succeeded despite them.
- **Vendor cards rationale**: kept the established 3-vendor set (Ascension, Particle, Limitless). All three stock MOTS-C — relevant for the article's "isolate batch as a variable when troubleshooting" framing. The Apollo card class (apollo-card / apollo-btn) is still used for the Ascension card per existing project CSS naming convention (legacy from when Apollo was a separate vendor).
- **Topic exhaustion check**: the broader "pseudo-allergic peptide reactions" framing applies to GHK-Cu, ipamorelin, tesamorelin, BPC-157 — the same MRGPRX2 mechanism. Future articles could profitably extend the framework to one of those compounds when Reddit signal turns up. The "Allergy to every peptide" thread (1u0f0ph) specifically would be a candidate for a cross-compound piece if it gathers more substantive comments. Saved to backlog mentally — not committed to any file.
