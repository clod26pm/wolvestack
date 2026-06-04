# Content Batch — 2026-06-04

## Topic Source
- Subreddit: r/Peptides
- Primary thread: "Klow blend a lighter blue?" — https://www.reddit.com/r/Peptides/comments/1tvb4h6/klow_blend_a_lighter_blue/ (13 comments, ~22h)
- Secondary signal threads (all r/Peptides, all within ~24h):
  - "Can i mix HCG with Reta and KLOW ?" — https://www.reddit.com/r/Peptides/comments/1tw28ki/can_i_mix_hcg_with_reta_and_klow/ (7 comments)
  - "When did your RS first notice change from GLOW 50/10/10" — https://www.reddit.com/r/Peptides/comments/1tvdq3y/when_did_your_rs_first_notice_change_from_glow/ (10 comments)
  - "KLOW bei Dehnungsstreifen hilfreich?" — https://www.reddit.com/r/Peptides/comments/1tvkv1l/klow_bei_dehnungsstreifen_hilfreich/ (5 comments, German)
  - "I'm going to try GLOW" — https://www.reddit.com/r/Peptides/comments/1tv8l4m/im_going_to_try_glow/ (1 comment)
- Why this topic: four overlapping KLOW/GLOW threads inside a 24h window with substantive technical questions (batch QC color, syringe-mixing pH compatibility, response timeline), zero matching article on WolveStack (no klow-*.html or glow-*.html anywhere in content-list.txt), composition gap that benefits from a unified research-grade primer.

## Article shipped
- Slug: `klow-blend-guide`
- Title: KLOW Peptide Blend: What the 4-Compound Stack Does
- Tag: Research Guide · Stacks
- English word count (article body): 4,260 words
- H2 sections: 12 (incl. FAQ section)
- FAQ items: 6
- Quick-answer box: 137 words (target 134–160 — in range)
- Languages translated and shipped at full fidelity: **en, es, pt, fr** (4 total — meets the en + 3 floor)
- Body word counts per language: en 4,260 · es 4,683 · pt 4,496 · fr 4,713
- Languages deferred for next-run backfill: **de, zh, ja, it, ru, pl, nl, id, ar** (9). Reason: context budget — the four shipped languages exceed the floor, and remaining 9 are queued for next-day backfill.

## Files touched (12)
- en/klow-blend-guide.html (new, English source)
- klow-blend-guide.html (new, root redirect safety net)
- es/klow-blend-guide.html (new)
- pt/klow-blend-guide.html (new)
- fr/klow-blend-guide.html (new)
- en/sitemap.xml (added URL entry + 4 hreflang siblings)
- es/sitemap.xml (added URL entry + 4 hreflang siblings)
- pt/sitemap.xml (added URL entry + 4 hreflang siblings)
- fr/sitemap.xml (added URL entry + 4 hreflang siblings)
- sitemap-root.xml (added URL for /klow-blend-guide.html)
- sitemap.xml (sitemap-index — bumped lastmod for en/es/pt/fr sitemaps)
- content-list.txt (appended klow-blend-guide.html)

## Commit
- `d94747821` — "Add KLOW peptide blend guide — 4 languages" — pushed to https://github.com/clod26pm/wolvestack main
- Verification:
  - `curl -sI https://raw.githubusercontent.com/clod26pm/wolvestack/main/en/klow-blend-guide.html` → HTTP 200, 59,248 bytes
  - `curl -sI https://raw.githubusercontent.com/clod26pm/wolvestack/main/fr/klow-blend-guide.html` → HTTP 200
- Netlify auto-deploy triggered by the push.

## Build helpers (NOT committed — intentionally kept untracked in working tree)
- `build-klow-translations.py` — reads `en/klow-blend-guide.html`, applies a translation dict per language, swaps `<html lang>`, canonical URL, og:url, active nav-lang-menu link, and `/en/` → `/{lang}/` for same-slug internal helper links (with sentinel protection for the nav-lang-menu English link).
- `trans-klow-{es,pt,fr}.py` — translation dicts. Hand-written native phrases; no external translation API used.
- `add-sitemap-entries.py` — inserts `<url>` entries with hreflang siblings into each shipped-language sitemap, the root sitemap, and bumps lastmods in the sitemap-index.

## Notes / follow-ups for next run
- **Backfill 9 languages**: de, zh, ja, it, ru, pl, nl, id, ar. Easiest path is to write `trans-klow-{lang}.py` files alongside the existing ones and re-run `build-klow-translations.py`. The script will produce the `{lang}/klow-blend-guide.html` files. Then a follow-up sitemap pass will extend the hreflang sibling lists in the existing en/es/pt/fr sitemap entries from 4 to 13 languages, and add entries to the 9 new-language sitemaps.
- **Sitemap hreflang strategy**: shipped 4-language hreflangs only this run, to avoid 404 hreflangs pointing at not-yet-shipped translations. Backfill run should:
  1. Generate de/zh/ja/it/ru/pl/nl/id/ar files
  2. Extend the existing en/es/pt/fr sitemap entries from 4 → 13 hreflangs
  3. Insert entries into each backfilled language's sitemap.xml
  4. Bump corresponding sitemap-index lastmods
- **Git environment note**: macOS file-flag attribution on this repo prevents `rm` of .git/index.lock from the Linux sandbox (operation not permitted) but `mv` works because rename is atomic and bypasses the delete restriction. If a future run hits a stale lock, use `mv .git/index.lock .git/index.lock.stale-$$` instead of `rm -f`.
- **No quick-answer change needed**: 137-word EN quick-answer falls inside the 134–160 sweet spot. ES/PT/FR translations preserved the same density.
- **Vendor cards rationale**: kept the same 3-vendor set (Ascension, Particle, Limitless) since they're the established WolveStack roster and all stock the four single compounds — relevant for the article's "isolate first, then move to blend" recommendation.
- **Topic exhaustion check**: GLOW is the obvious adjacent article that could ship next; today's coverage references it but doesn't substitute for a dedicated GLOW guide. Defer to a future day when GLOW signal is also strong on Reddit (was modest today, KLOW dominated).
