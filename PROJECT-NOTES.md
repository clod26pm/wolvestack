# Wolvestack Project Notes

## Site & Repo
- Site: https://wolvestack.com
- Repo: https://github.com/clod26pm/wolvestack
- Content directory: peptide-daily-content/
- GitHub PAT: stored in ../.github-pat (not committed — check this file at session start)
- 13 languages: en, es, zh, ja, pt, ru, it, pl, fr, id, de, nl, ar
- Hosting: Netlify (auto-deploys from main branch via GitHub)
- IMPORTANT: English content uses /en/ directory, NOT the root directory, for GSC indexing
  - Root files exist but /en/ is the canonical English version for Google
  - All language versions: /en/, /es/, /zh/, /ja/, /pt/, /ru/, /it/, /pl/, /fr/, /id/, /de/, /nl/, /ar/
  - Root file canonicals point to /en/ equivalents (updated 2026-04-12)
  - /en/ files have full hreflang tags for all 13 languages + x-default
  - Netlify _redirects: root /*.html → /en/*.html via 301 (except index.html, search.html, /app/*, /category/*)
  - When creating NEW content: create in /en/ first, then copy to root + other languages
  - When updating English content, ALWAYS propagate changes to /en/ directory too

## Templates
- CSS template: TEMPLATE-CSS.html
- Body template: TEMPLATE-BODY.html
- Articles are standalone .html files using these templates

## Affiliate Links
- Ascension: ?ref=wolvestack
- Particle: ?refs=25135
- Limitless: ?affid=10704
- Integrative Peptides: ?ref=wolvestack

## Pinterest
- Account: pinterest.com/wolvestack (email: wolvestack@pm.me)
- Board: "Peptide Research Guides"
- Pin images (v2 medical/science design): https://wolvestack.com/pinterest-pins-v2/pin-{slug}.png
- Pin builder URL: https://www.pinterest.com/pin-builder/?tab=save_from_url
- Tracking log: pinterest-pins-log.json
- All 51 articles have v2 pins published as of 2026-04-10

## Pinterest Publishing Workflow
1. Navigate to pin-builder/?tab=save_from_url
2. Wait 10s for page load
3. Enter image URL (use form_input, not type)
4. Submit → wait 5s → click image → "Add 1 Pin"
5. Fill title, then destination link (change from image URL to article URL)
6. Type description LAST (it loses content if you click away)
7. Click Publish immediately after description

## Scheduled Tasks
- wolvestack-article-writer: daily at 6:30am (writes new peptide articles)
- wolvestack-pinterest-pinner: daily at 12:10pm (publishes new pins)

## Article Count
- ~1,900+ articles across all languages as of 2026-04-13
- 113+ fully fleshed out articles with body content
- ~1,768 stub articles (template + disclaimer, awaiting content from daily writer)
- New articles added daily by scheduled task

## SEO / Google Search Console
- /en/ is canonical for English — root files 301 redirect to /en/ via Netlify _redirects
- Root files also have canonical tags pointing to /en/ (belt + suspenders)
- All /en/ files have hreflang tags for all 13 languages + x-default
- Netlify pretty URLs strip .html — Google may index both /slug and /slug.html
- New content workflow: write in /en/ → copy to root (for redirect) → translate to other langs
- GSC verified: ~1,000 pages indexed as of 2026-04-12 (999 from CSV export)

## AI / GEO-SEO
- llms.txt deployed at wolvestack.com/llms.txt (2026-04-13)
- robots.txt does NOT block AI crawlers (intentional)
- Quick-answer boxes optimized to 134-160 words across all 13 languages (2026-04-13)
- 1,121 articles now in the AI citation sweet spot
- New articles should always include a quick-answer box targeting 150 words

## Security
- _headers file: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
- CSP allows: self, unsafe-inline, googletagmanager, google-analytics, fonts.googleapis, fonts.gstatic, wolvestack-email worker
- .gitignore covers secrets, credentials, OS files, editor files, backups
- _redirects blocks .git, .github, .env paths
- ReDoS vulnerability fixed in search.js (2026-04-12)
- GitHub PAT rotated after exposure (2026-04-12) — old tokens deleted

## Key Gotchas
- Pinterest description field loses content when focus changes — always fill it last
- Pinterest "Enter website" input sometimes needs a click at ~(735, 229) before find tool locates it
- Pin builder page takes 10-20s to fully render
- Always use form_input (not type) for URL fields in Pinterest's React inputs
- Destination link auto-fills with the image URL — must be changed to the article URL
- GitHub PAT may need refreshing — check if push fails with auth error
- nad-plus vs nadplus: filenames use "nadplus", some internal links use "nad-plus" — redirects handle mismatch
- Netlify pretty URLs strip .html — redirects need to account for both /slug and /slug.html
