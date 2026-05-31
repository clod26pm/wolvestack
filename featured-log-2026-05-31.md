# Featured.com / Connectively Submission Log — 2026-05-31

## Status: BLOCKED — not logged in (same as 2026-05-30)

## What happened
- Navigated to https://featured.com/experts/questions
- Redirected to https://www.connectively.us/experts/questions (Featured.com rebranded to **Connectively**)
- Vercel Security Checkpoint cleared after ~8 seconds
- Final landing page: `https://www.connectively.us/login?callbackURL=%2Fexperts%2Fquestions` — login wall
- The Chrome browser session still does NOT have an active WolveStack/Connectively login cookie
- Cannot reach the questions feed without authenticating

## Why no submissions were made
Safety rules prohibit entering passwords or authenticating accounts on the user's behalf in an automated/unattended run. The available login options all require A's direct action:
1. LinkedIn SSO — requires OAuth click-through
2. Email + password — cannot auto-fill credentials
3. Magic link — requires email access + click-through
4. Passkey — requires hardware authentication

## This is a recurring blocker
2026-05-30 log flagged the identical problem. A's recommended fix from yesterday's log has not been applied: one-time manual login to connectively.us in the Chrome instance the scheduled task uses, with "stay logged in" checked.

## Recommended action
**Option A (preserve current pipeline):** A logs into connectively.us in the Chrome MCP browser, checks "remember me." All subsequent scheduled runs should inherit the cookie until eviction (likely 30+ days).

**Option B (kill the task):** If Connectively's auth model is too brittle for unattended runs and A doesn't want to babysit it, delete the `featured-daily-queries` scheduled task. The pattern of "scheduled run → BLOCKED log → no value delivered" has now repeated 2+ times.

**Option C (replace channel):** Pivot the task to a competitor that still allows pitch submission without sustained session auth — e.g., HARO successor "Qwoted" or "Source of Sources" by Peter Shankman. Both have similar reach for wellness/peptide niches and lower friction.

My recommendation: **Option A this week, Option B if it fails again next run.** The expected value of one Featured.com placement (DA 60-80 publication backlink + brand mention) easily justifies a 90-second weekly manual login if the cookie survives. If the cookie evicts in <7 days, the math flips — kill the task.

## Submissions today: 0
## Answers remaining: unknown (login wall)
