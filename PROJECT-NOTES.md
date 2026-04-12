# Wolvestack Project Notes

## Site & Repo
- Site: https://wolvestack.com
- Repo: https://github.com/clod26pm/wolvestack
- Content directory: peptide-daily-content/
- GitHub PAT: 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
- 13 languages: en, es, zh, ja, pt, ru, it, pl, fr, id, de, nl, ar
- Hosting: Netlify (auto-deploys from main branch via GitHub)
- IMPORTANT: English content uses /en/ directory, NOT the root directory, for GSC indexing
  - Root files exist but /en/ is the canonical English version for Google
  - All language versions: /en/, /es/, /zh/, /ja/, /pt/, /ru/, /it/, /pl/, /fr/, /id/, /de/, /nl/, /ar/
  - Root files have self-referencing canonicals; /en/ files canonical to /en/
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
- 51 articles as of 2026-04-10
- New articles added daily by scheduled task

## Key Gotchas
- Pinterest description field loses content when focus changes — always fill it last
- Pinterest "Enter website" input sometimes needs a click at ~(735, 229) before find tool locates it
- Pin builder page takes 10-20s to fully render
- Always use form_input (not type) for URL fields in Pinterest's React inputs
- Destination link auto-fills with the image URL — must be changed to the article URL
