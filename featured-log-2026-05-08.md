# Featured.com Daily Run — 2026-05-08

## Summary
**Submitted 0 Featured.com responses.** 9th consecutive blocked run (sequence: 04-30, 05-01, 05-03, 05-04, 05-05, 05-07, 05-08).

## What happened
1. Navigated to `https://featured.com/experts/questions` from a fresh MCP tab in the connected Chrome browser.
2. Featured.com immediately redirected to `https://featured.com/login?callbackURL=%2Fexperts%2Fquestions`. No active session cookie.
3. Login page renders the same four auth paths it did on 05-07: LinkedIn SSO, Email+password, "Sign In with a link" magic link, passkey.
4. Stopped at the login wall. No submissions possible.

## Blockers (no change since 2026-04-30)
1. **Browser session expired** since 04-30. Even the questions list redirects to the login page — read access is gone.
2. **LinkedIn requirement** since 04-19. Even after a fresh login, the expert profile cannot post answers until a LinkedIn URL is attached. "Answers Remaining" has been 0 throughout.
3. **No automatable login path** for an unattended scheduled run:
   - LinkedIn SSO — no WolveStack LinkedIn page exists.
   - Email + password — Cowork policy prohibits Claude from entering passwords.
   - Magic link — goes to `wolvestack.research@gmail.com`, which is not the Gmail MCP's authorized inbox (that's `clod26@pm.me`).
   - Passkey — no platform credential stored on this device.

## Submissions
- Attempted: 0
- Completed: 0
- Answers remaining: unknown (counter is behind the login wall)

## Recommendation: pause this scheduled task

Nine consecutive runs have produced zero submissions. Each run also burns a Netlify-adjacent cost (browser session, scheduled task slot) for no marginal gain. Recommended action for A:

1. Open Cowork → Scheduled Tasks → `featured-daily-queries` → set `enabled: false`.
2. Re-enable only after BOTH of the following are true:
   - A has manually signed into Featured.com inside the connected Chrome profile (creds in `../.featured-creds`) so the session cookie is fresh.
   - A LinkedIn page exists at a public URL Featured.com can resolve, and is attached to the Featured.com expert profile.

I am again NOT auto-pausing the task — flipping a user-created scheduled job to disabled is a state change that should be confirmed in chat. Logging the recommendation here for the third run in a row instead.

## Page snapshot
- Final URL: `https://featured.com/login?callbackURL=%2Fexperts%2Fquestions`
- Title: "Login | Featured"
- Auth options visible: LinkedIn SSO, Email + password, "Sign In with a link", "Use a passkey instead"
- Banner CTA: "Log in to your account / Don't have an account? Sign Up."

## Status line printed to scheduler
`Featured.com: 0 answers remaining — login wall, 9th consecutive blocked run. Log saved to featured-log-2026-05-08.md`
