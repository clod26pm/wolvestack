# WolveStack Deploy Verification Checklist

Every time changes are pushed to GitHub, verify ALL of the following are live on wolvestack.com before ending the session.

## Automated checks (run on 3 random article pages)

| Check | Expected |
|-------|----------|
| Google Analytics (`G-MLF04PQ0JV`) | `<script>` tag in `<head>` |
| Quick Answer box (`.quick-answer`) | Present below disclaimer |
| FAQPage JSON-LD schema | Present in `<head>` |
| Email popup (`email-popup.js`) | Script loaded |
| Affiliate links (Ascension/Apollo) | Present in CTA section |
| Question-format H2 headers | At least some end with `?` |

## Also verify
- [ ] `https://wolvestack.com/sitemap.xml` loads with current URLs
- [ ] Latest GitHub Action at `github.com/clod26pm/wolvestack/actions` shows green ✅
- [ ] New files (if any) appear in sitemap

## Scheduled task
A "wolvestack-deploy-verify" task exists in Claude's Scheduled section. Run it after any push.
