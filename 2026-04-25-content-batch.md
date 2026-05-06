# 2026-04-25 — Content Batch

## Summary

Wrote 10 new WolveStack peptide articles, propagated to all 13 languages plus root copies (140 HTML files total), added each to the 14 sitemaps with hreflang alternates, removed noindex tags from the 7 stubs that had been carrying the noindex signal, and updated the content list.

## The 10 Articles

### Priority (Tier 3 gaps from gap-tracker-report.md)

1. **amhr2bp-guide.html** — body 2,771 words / 11 H2s + FAQ — emerging AMH receptor modulator research
2. **how-to-verify-peptide-purity.html** — body 3,177 words / 11 H2s + FAQ — HPLC, MS, COA reading guide
3. **peptide-stacking-advanced.html** — body 3,004 words / 11 H2s + FAQ — multi-compound protocol design

### Noindex Stub Fills (replaced with full content + noindex removed)

4. **mif-1-for-gut-health.html** — body 2,280 words / 10 H2s + FAQ
5. **mif-1-for-immune-system.html** — body 2,020 words / 10 H2s + FAQ
6. **mif-1-for-inflammation.html** — body 1,880 words / 10 H2s + FAQ
7. **ll-37-vs-bpc-157.html** — body 2,185 words / 10 H2s + FAQ
8. **mk-677-vs-ghrp-6.html** — body 2,079 words / 10 H2s + FAQ
9. **setmelanotide-vs-bpc-157.html** — body 1,972 words / 10 H2s + FAQ
10. **setmelanotide-vs-glp-1.html** — body 2,204 words / 10 H2s + FAQ

## Per-Article Build Quality

Each article was generated through the same templated pipeline used for previous batches:

- robots `index, follow`
- canonical URL pointing at the language-specific `/lang/slug` form
- full hreflang block for all 13 languages plus x-default
- OG / Twitter card metadata
- Article + Breadcrumb + FAQPage JSON-LD schemas
- Quick-answer box (134–160 words target, AI-citation friendly)
- Medical disclaimer block
- 8+ H2 sections (10–11 actual)
- 6+ FAQ items per article
- Vendor cards: Ascension (`?ref=wolvestack`), Particle (`?refs=25135`), Limitless (`?affid=10704`)
- TOC sidebar + sidebar cards (Beginner's Guide, Wolverine Stack)
- Full WolveStack template CSS (Inter + Space Grotesk, teal/navy palette)
- Footer with disclaimer, GA tag (G-MLF04PQ0JV), email-popup.js script

## Languages and Sitemaps

Each of the 10 articles is now live in all 14 locations:

- Canonical: `/en/{slug}`
- Root copy (redirects to /en/ via Netlify _redirects)
- 12 other language directories: es, zh, ja, pt, ru, it, pl, fr, id, de, nl, ar

Each `<html lang="">` and the language dropdown active class were set per-language. Each language folder's `sitemap.xml` received a new `<url>` block with hreflang alternates, and `sitemap-root.xml` received the root URL entry. Total sitemap edits: 14 sitemaps × 10 articles = 140 sitemap entries.

## Tracking Updates

- `content-list.txt`: 1916 → 1926 entries
- `stub-list.txt`: unchanged (only `search.html` remains, which is the search page, not an article stub)
- `gap-tracker-report.md`: 3 priority Tier 3 articles flipped from ❌ Missing to ✅ Added 2026-04-25 — full priority list now complete

## Notes for Next Run

- Roadmap of explicit priority articles is now complete (gap-tracker-report.md).
- Additional noindex stubs remain in `en/`: at least 8 more files still carry noindex with mismatched-content stubs. These are good candidates for the next batch:
  - `melanotan-i-for-skin-protection.html`
  - `melanotan-i-for-vitiligo.html`
  - `melanotan-ii-vs-melanotan-i.html`
  - `nadplus-for-addiction-recovery.html`
  - `nadplus-for-chronic-fatigue.html`
  - `nadplus-for-energy.html`
  - `nadplus-iv-vs-oral.html`
  - `semaglutide-how-long-to-see-results.html`
- The article generator script (`scripts/article_gen.py`) and per-article configs are saved in `outputs/scripts/` for reuse — adding a future article is a one-config-file change.
