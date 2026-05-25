# Featured.com Daily Submissions — 2026-05-22

## Status: BLOCKED — Not logged in

## What happened
- Navigated to https://featured.com/experts/questions
- Page redirected to https://featured.com/login?callbackURL=%2Fexperts%2Fquestions
- The WolveStack Featured.com session is no longer authenticated in this Chrome profile.

## Why I stopped
- Login page offers three auth paths: email+password, LinkedIn OAuth, or magic-link email.
- Safety rules forbid entering passwords on the user's behalf and require explicit in-chat permission for SSO/OAuth flows.
- This is a scheduled task — A is not present to grant permission or paste credentials.
- I did not attempt any login. No submissions were made.

## Submissions
- Responses submitted: 0
- Questions evaluated: 0
- Answers-remaining quota: unknown (cannot read while logged out)

## What A needs to do
1. Open Chrome → https://featured.com/login
2. Log in to the WolveStack account (email+password, LinkedIn, or "Sign In with a link")
3. Verify the session persists by visiting https://featured.com/experts/questions directly
4. Next scheduled run should then succeed. If logouts keep recurring, check whether the browser is clearing cookies on quit, or set Chrome to "Keep me signed in" / save the password in Chrome.

## Notes
- Browser used: "Browser 1" (local macOS, deviceId d7c4018c-3491-49fc-ab72-6473d079c63d)
- One transient extension disconnect during the run (recovered on retry).
- No other anomalies — the navigation, page read, and screenshot worked normally; only the auth state is the blocker.
