# Featured.com / Connectively Submission Log — 2026-05-30

## Status: BLOCKED — not logged in

## What happened
- Navigated to https://featured.com/experts/questions
- Site has rebranded to **Connectively** (www.connectively.us) — featured.com URL 302-redirects to `https://www.connectively.us/experts/questions?from=featured`
- Vercel Security Checkpoint cleared after ~12 seconds
- Landing page: `https://www.connectively.us/login` — login wall, not the questions feed
- The Chrome browser session does NOT have an active WolveStack login cookie

## Why no submissions were made
Per safety rules, I cannot enter the account password on the user's behalf in an automated/unattended run. The task file says "The WolveStack account is already set up there," but the *browser session* is not currently authenticated. Login options offered:
1. LinkedIn SSO (requires user click-through)
2. Email + password (cannot auto-fill)
3. Magic link ("Sign in with a link") (requires email access + user click-through)
4. Passkey (requires hardware authentication)

## Recommended fixes (for next run)
1. **One-time manual login**: A logs into connectively.us in Chrome (the same browser the scheduled task uses) and checks "stay logged in." Subsequent scheduled runs should inherit the session cookie. This is the cleanest fix.
2. **Update the task file**: Change references from `featured.com` → `connectively.us` so future logs/links are correct.
3. **Verify cookie persistence**: Chrome may evict the session cookie if not used regularly. If the scheduled task fails again with the same blocker after ≤7 days, the cookie was wiped — consider a weekly low-priority "keep-alive" visit.
4. **Alternative**: switch the scheduled task to a different distribution channel (HARO/Qwoted/HARO successor "Featured" rival "Source of Sources" / "Qwoted") if Connectively's session model is too brittle.

## Submissions today: 0
## Answers remaining: unknown (login wall blocked the questions feed)
