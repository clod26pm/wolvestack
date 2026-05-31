# Reddit Drafts — 2026-05-31

**Status: BLOCKED — 0 drafts produced.**

## What happened

The scheduled Reddit research task could not be executed because every available path to live Reddit content is gated in this environment:

1. **Claude in Chrome blocks reddit.com** — both `https://www.reddit.com/` and `https://old.reddit.com/` return `"This site is not allowed due to safety restrictions."` at the `navigate` step. The extension safelist excludes Reddit. I tried `r/Peptides/new/` on both subdomains; both refused before any page load.

2. **web_fetch is restricted by provenance** — `mcp__workspace__web_fetch` only accepts URLs that already appeared in a prior tool result or user message. Reddit's JSON endpoints (`/r/<sub>/new.json`) cannot be fetched cold. The fallback option in the system rules (bash `curl`/Python `requests`) is explicitly prohibited by the web-content restrictions.

3. **WebSearch no longer surfaces direct Reddit thread URLs** — I ran 11 queries across `site:reddit.com/r/Peptides`, `site:reddit.com/r/MorePlatesMoreDates`, `"reddit.com/r/peptides/comments"`, `"redd.it" peptides ...`, etc. Zero results returned a `reddit.com/comments/...` URL. This matches what's been happening since Reddit's 2024 licensing deal with Google narrowed third-party search visibility — Bing/DuckDuckGo/general indexes mostly surface SEO-scraper rewrites (RealPeptides, PureMedicalSpa, Swolverine), not the underlying threads.

4. **No Reddit MCP connector** — `mcp__mcp-registry__search_mcp_registry` with `["reddit", "social", "forum"]` returned `{"results":[]}`.

## What I did NOT do

I did **not** fabricate thread titles, thread URLs, or comment counts to fill the file. Per A's standing preferences ("Never hallucinate or make anything up. If you don't know something, just say so") and per the task spec (`When in doubt, producing a report of what you found is the correct output`), the honest output is this report, not five fake threads that would waste A's time when the URLs 404.

## What needs to change before this task can run

Pick one (in order of effort, lowest first):

1. **Whitelist `reddit.com` and `redd.it` in the Claude in Chrome extension safelist.** This is almost certainly the blocker — Chrome's MCP safety list excludes social platforms by default. If the extension has an allowlist setting, adding `*.reddit.com` and `redd.it` unblocks paths 1 & 3 simultaneously (browse + click into threads).

2. **Install a Reddit MCP connector.** None is currently listed in the registry under "reddit"/"social"/"forum". If Anthropic ships one, or a community one exists outside the registry, that's the cleanest fix — read-only access to `/r/<sub>/new` JSON without a logged-in browser.

3. **Run a separate scraper outside Claude** that drops fresh thread URLs into a file (e.g., `~/cowork/peptide-daily-content/reddit-inbox-YYYY-MM-DD.json`) every morning, and rewrite this scheduled task to read from that file. Reddit's public `/r/<sub>/new.json?limit=50` works fine from a normal Python script with a custom User-Agent; the block is specifically inside the Claude environment's web tools.

## Sanity check on the matching layer (this part works fine)

The article-matching half of the task is unaffected. The WolveStack article inventory covers every peptide on the task's target list with multiple long-tail variants:

- BPC-157: 122 articles (including 19 injection-site variants, 7 cancer/risk variants, 11 drug-interaction variants, vs-comparisons with TB-500/GHK-Cu/PRP/stem-cell/cortisone)
- TB-500: 52 articles
- CJC-1295 (with and without DAC): 56 articles
- Ipamorelin: 38 articles
- Sermorelin: 28 articles
- Semax + N-Acetyl Semax Amidate: 49 articles
- Selank + N-Acetyl Selank Amidate: 49 articles
- GHK + GHK-Cu: 71 articles
- Epitalon (spelled "Epithalon" on the site): 28 articles
- PT-141: 49 articles
- Semaglutide: 84 articles
- Tirzepatide: 56 articles
- MK-677: 60 articles
- Retatrutide: 26 articles

So once Reddit access is unblocked, the matching + drafting step will run end-to-end without further changes.

---

**Drafted 0 replies for 0 threads. Drafts saved to reddit-drafts-2026-05-31.md — review and post manually.** (No drafts to post; the file is a status report explaining why.)
