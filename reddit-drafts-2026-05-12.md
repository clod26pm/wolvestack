# Reddit Drafts — 2026-05-12

## ⚠️ STATUS: NO LIVE THREADS FOUND — REDDIT ACCESS STILL BLOCKED (day 10 of the same blocker)

Identical situation to 2026-05-03 → 2026-05-11. Reddit remains unreachable from every tool surface available to this scheduled run. Re-verified today:

- **Browser (Claude in Chrome):** `https://www.reddit.com/r/Peptides/new/` and `https://old.reddit.com/r/Peptides/new/` both return `"This site is not allowed due to safety restrictions."` The Chrome extension's domain allow-list refuses reddit.com before any navigation occurs. Confirmed again at 2026-05-12 run start.
- **WebSearch with `allowed_domains=["reddit.com"]`:** HTTP 400 — `"The following domains are not accessible to our user agent: ['reddit.com']."` Reddit blocks Anthropic's crawler at the policy layer (per Reddit's stated AI-training policy since 2024).
- **WebSearch (unfiltered, with `site:reddit.com` operator or thread-URL keyword patterns like `"reddit.com/r/Peptides/comments"`):** Returns peptide-vendor blogs, news sites (STAT, Scientific American, Medscape), and PMC papers that *cite* aggregate Reddit data. Zero actual `reddit.com/r/.../comments/...` URLs surface in the index for this user agent.
- **`workspace.web_fetch`:** Provenance-restricted to URLs already seen in conversation. Tried `https://www.reddit.com/r/Peptides/new.json?limit=25` and got `"URL not in provenance set"`. Cannot bootstrap a thread URL from nothing.
- **Bash `curl`/`wget`:** Explicitly prohibited by this environment's web-content restriction policy as a fallback when WebFetch / WebSearch fail. (`"Do NOT use bash commands ... to fetch URLs"`)
- **MCP registry:** No Reddit connector available as of this run.

**This is a hard, persistent block.** Re-running the task daily continues to produce zero live-thread drafts.

I will not fabricate Reddit thread titles, URLs, or comment text to satisfy the file format — that would mean inventing posts that don't exist and sending A to dead links. Per A's standing preferences ("Never hallucinate or make anything up. If you don't know something, just say so"), I am reporting the blocker honestly and producing evergreen templates instead.

---

## What A should do (unchanged from prior runs — repeated here so it doesn't get lost across daily files)

**Strong recommendation:** disable the `reddit-expert-answers` scheduled task or rewrite it. It cannot do what it was specified to do in the current environment. Three resurrection paths, in descending order of effort-vs-payoff:

1. **Manual-discovery hybrid (zero new infrastructure, lowest effort).** A pastes 3–5 thread URLs into chat each morning; I draft replies against those specific threads. This is what the task is actually trying to accomplish, and it works today because I can render reply text for URLs A provides even when I can't browse to them. The chat-paste workflow also bypasses the `web_fetch` provenance restriction — once a URL is in a user message, it becomes fetchable.
2. **Reddit OAuth token (~20 min A-side setup, full automation).** Register a script-type app at https://www.reddit.com/prefs/apps, generate `client_id` + `client_secret`, store like the GitHub PAT (`../.reddit-token`). Rewrite this task to hit `https://oauth.reddit.com/r/Peptides/new` with a bearer token via the application's connector layer (not the LLM sandbox). Authenticated API access is treated differently from anonymous scraping and may not hit the same domain block.
3. **Reddit MCP connector (when available).** Worth re-checking quarterly via `mcp__mcp-registry__search_mcp_registry`. Not present today.

**Lower-leverage alternative — what this file currently does:** keep the task running and reframe its output as "evergreen template replies A can customize against any matching real-world thread." Over the course of a week these accumulate into a library that covers the recurring question patterns in the target subreddits. Today's 5 templates are picked to *not* overlap with the 10 templates produced 2026-05-10 + 2026-05-11, nor with the live-thread drafts from 2026-05-05 → 2026-05-09.

**Topics already covered in recent template runs (do not re-template):** BPC-157 tendon/ligament dose, CJC/Ipa AM-vs-PM timing, tirzepatide/semaglutide plateau, Semax-vs-Selank ADHD/focus, MK-677 sleep/appetite/downsides, GHK-Cu topical-vs-inject, TB-500 loading phase, retatrutide-vs-tirzepatide, PT-141 nausea/flushing, 5-Amino-1MQ fat loss.

**Topics covered today:** peptide purity verification, Sermorelin vs Tesamorelin, Selank intranasal for anxiety, Epithalon pulse protocol, semaglutide/tirzepatide muscle loss preservation.

---

## Evergreen template drafts (5)

Each draft is paste-ready against any thread matching the listed question pattern. Each references the most relevant 1–2 WolveStack articles, hits the 150–300 word target, uses research-backed language, ends with the educational disclaimer, and follows the "we" voice for posting as the WolveStack research team. Tailor the opening sentence to the specific OP before posting.

---

### Template 1: "How do I know my peptide is real / not bunk? What's the actual purity-verification path?"
**Target subreddits:** r/Peptides, r/biohacking, r/MorePlatesMoreDates, r/PEDs
**Matching article:** https://wolvestack.com/en/how-to-verify-peptide-purity.html
**Status:** READY TO PASTE — customize first sentence to the OP's specific vendor/peptide

**Draft reply:**

The unfortunate honest answer is that you cannot verify your peptide is real without a third-party lab test, and vendor-provided CoAs (Certificates of Analysis) are easy to fake. We have seen vendor CoAs with photoshopped HPLC chromatograms and chain-of-custody gaps that make them effectively worthless as evidence. Here is the actual verification stack, in order of decreasing accessibility:

(1) **Independent HPLC-MS** through a contract lab (Janoshik Analytical in the Czech Republic is the community standard — turnaround ~2 weeks, ~$50–$80 per peptide). They test for both purity (percent of target peptide vs. impurities) and identity (does the mass match the target sequence). Anything under 95% purity is generally considered substandard; under 90% should be returned.

(2) **Pre-purchase: check the vendor's batch-level CoA against a published reference.** A real CoA shows the lab name, technician, instrument, retention time, peak area, and a chromatogram image. Vendors who only provide a single "≥99% pure" PDF with no underlying data are flagging themselves.

(3) **Pre-purchase: reconstitution behavior is a weak signal but useful as a free check.** Real lyophilized peptide is a white-to-off-white fluffy powder that dissolves clear in bacteriostatic water within ~30 seconds without swirling. Yellow tint, gritty powder, or persistent cloudiness after reconstitution suggests degradation, incorrect storage, or a counterfeit.

(4) **Effect-tracking with a journal.** Not verification, but a Bayesian update — peptides at the wrong dose or wrong identity produce reliably different physiological signatures than the real compound. Worth keeping notes.

Full breakdown of the verification workflow plus links to community-trusted labs: https://wolvestack.com/en/how-to-verify-peptide-purity.html

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

### Template 2: "Sermorelin vs Tesamorelin — which one should I run? Especially for visceral fat / older adults?"
**Target subreddits:** r/Peptides, r/biohacking, r/MorePlatesMoreDates, r/HGH
**Matching articles:** https://wolvestack.com/en/sermorelin-vs-tesamorelin.html, https://wolvestack.com/en/tesamorelin-benefits.html
**Status:** READY TO PASTE

**Draft reply:**

These are both GHRH analogs but they are not interchangeable, and choosing wrong wastes months. Mechanistically they both bind the GHRH-receptor on pituitary somatotrophs to drive endogenous GH pulses, but tesamorelin has a stabilized N-terminus (trans-3-hexenoyl modification) that makes it ~12× more resistant to dipeptidyl peptidase-IV degradation than sermorelin. That translates to a longer functional half-life and meaningfully larger GH AUC per injection.

The clinical evidence asymmetry is large. Tesamorelin has an FDA approval (for HIV-associated lipodystrophy, 2 mg subcutaneous daily) and the pivotal trials (Falutz et al., NEJM 2007; Stanley et al., JAMA 2014) showed ~17% reduction in visceral adipose tissue at 26 weeks on MRI — measured visceral fat, not just scale weight or waist circumference. There is also a 2014 study showing a reduction in liver fat in NAFLD. Sermorelin's evidence is older and softer — mostly 1990s data on pediatric GH-deficient populations and uncontrolled adult anti-aging cohorts.

Practical decision rule: for **visceral adiposity, NAFLD/fatty liver, post-50 body recomposition, or anyone who has tried sermorelin and not seen results**, tesamorelin at 1–2 mg/day SC at bedtime is the higher-yield choice. For **general age-management, sleep-quality, and budget-constrained protocols**, sermorelin at 200–500 mcg/day SC at bedtime is a reasonable starting point — it is dramatically cheaper and side-effect profile is milder.

What both share: injection-site reactions, potential mild hyperglycemia (monitor fasting glucose), and contraindications in active cancer.

Full head-to-head with dose tables: https://wolvestack.com/en/sermorelin-vs-tesamorelin.html

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

### Template 3: "Selank intranasal for anxiety — does it actually work? What's the mechanism and the real dose?"
**Target subreddits:** r/Nootropics, r/Peptides, r/Anxiety, r/biohacking
**Matching articles:** https://wolvestack.com/en/selank-for-anxiety.html, https://wolvestack.com/en/selank-guide.html
**Status:** READY TO PASTE

**Draft reply:**

Selank is a synthetic heptapeptide analog of tuftsin (a tetrapeptide immunomodulator naturally cleaved from IgG). The anxiolytic effect is mediated through enkephalinase inhibition — by slowing the breakdown of endogenous enkephalins, it raises tonic met-/leu-enkephalin levels, which downstream modulates GABA-A signaling and serotonin turnover. That mechanism is fundamentally different from benzodiazepine GABA-A allosteric agonism, which is why selank does not produce sedation, tolerance, or withdrawal in the way Xanax does.

Human data is limited but real — most of it is from Russian work by the Zakharov / Myasoedov group at the Institute of Molecular Genetics, plus a few Eastern European trials. Kozlovskaya et al. (2003) compared selank to medazepam in n=62 generalized anxiety patients and found similar anxiolytic efficacy with markedly better tolerability. A 2011 study showed BDNF upregulation in hippocampus + cortex on chronic dosing in rodents, suggesting the effect builds over weeks rather than being purely acute.

Practical protocol: intranasal is the only route that makes pharmacokinetic sense — selank does not cross the BBB efficiently from subcutaneous, and oral is destroyed by GI proteases. Standard dose is 250–500 mcg per nostril, 2–3 times daily, with onset in 10–20 minutes and a 4–6 hour functional window. Most people run 14–21 day cycles. The compound is generally well-tolerated; the most common side effect is mild nasal irritation, and rare reports of headache or fatigue at high doses.

Important caveat: this is **not** an FDA-approved drug in the US — it is a Schedule I-adjacent research peptide and not a treatment for diagnosed anxiety disorders. We do not recommend it as a substitute for evidence-based treatment if you have moderate-to-severe GAD or panic disorder.

Full mechanism, dose table, and the Russian trial summaries: https://wolvestack.com/en/selank-for-anxiety.html

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

### Template 4: "Epithalon — is the 5–10 day pulse protocol bro-science? What's the actual rationale and timing?"
**Target subreddits:** r/Peptides, r/longevity, r/biohacking
**Matching articles:** https://wolvestack.com/en/epithalon-cycle.html, https://wolvestack.com/en/epithalon-for-longevity.html
**Status:** READY TO PASTE

**Draft reply:**

The 10-day-on-then-pause protocol is not bro-science — it actually comes from Vladimir Khavinson's original clinical work at the St. Petersburg Institute of Bioregulation. Khavinson's group at the Russian Academy of Medical Sciences treated long-running geriatric cohorts with epithalon (5–10 mg subcutaneous daily × 10 days, repeated every 4–6 months) and published 12-year mortality data (Khavinson and Morozov, Neuro Endocrinol Lett 2003) claiming a ~50% reduction in death rate vs. matched controls. Independent reproduction is sparse, and the methodology has been criticized for cohort-selection issues, but the protocol shape comes from real human data, not online forums.

The pharmacological rationale for pulsed-vs-continuous: epithalon (Ala-Glu-Asp-Gly) has a very short plasma half-life (~30 minutes) and works by binding the telomerase RNA template promoter region — its effect on telomerase upregulation persists for days to weeks after a course because the transcriptional changes outlast the parent compound. So a 10-day saturation course followed by months of "running on" the upregulation is mechanistically coherent. Continuous daily dosing for years has no published evidence of additional benefit and may downregulate the response.

Practical protocol: 5–10 mg subcutaneous once daily for 10–20 consecutive days, repeated every 4–6 months. Some people split the dose AM/PM because of the short half-life. Inject deep subQ in abdomen or thigh — IM offers no advantage. Stack-wise, GHK-Cu and NAD+ precursors are common pairings; we have not seen credible evidence that adding TA-1 or MOTS-c changes outcomes.

Important caveat: human evidence is genuinely thin outside the Khavinson group. Lifespan claims are extrapolations. We recommend epithalon as a low-risk longevity experiment, not as a confirmed intervention.

Full protocol with the Khavinson trial summary: https://wolvestack.com/en/epithalon-cycle.html

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

### Template 5: "How do I avoid losing muscle on semaglutide / tirzepatide? Is the muscle-loss thing real?"
**Target subreddits:** r/loseit, r/Peptides, r/MorePlatesMoreDates, r/biohacking
**Matching articles:** https://wolvestack.com/en/semaglutide-muscle-loss-risk.html, https://wolvestack.com/en/tirzepatide-muscle-loss-risk.html
**Status:** READY TO PASTE

**Draft reply:**

Yes, the muscle-loss concern is real and the numbers are not subtle. The STEP-1 trial DEXA sub-analysis (Wilding et al., NEJM 2021) found that of the ~15% mean weight loss on semaglutide 2.4 mg, ~39% came from lean mass — meaning a 100 lb person losing 15 lb dropped roughly 6 lb of lean tissue. SURMOUNT-1 for tirzepatide shows similar lean-to-fat ratios. That said, the lean-mass loss fraction on GLP-1 RAs is not meaningfully different from what you would see with any aggressive caloric deficit; the deficit itself drives most of the catabolism, not the drug.

The four interventions with the strongest evidence for preserving lean mass during a GLP-1/GIP cut:

(1) **Protein at 1.6–2.2 g/kg ideal body weight per day.** This is the single highest-leverage lever. The appetite suppression makes hitting protein hard — most people undershoot at ~0.8 g/kg without intentional planning. Front-load protein at breakfast (30–40 g) before the early-satiety window closes.

(2) **Resistance training 3–4×/week with progressive overload.** Cardio alone does not preserve muscle in a deficit; pure cardio cohorts in trial data lose nearly identical fat-to-lean ratios as the no-exercise group. Compound lifts (squat, deadlift, row, press) at 5–8 rep ranges drive the largest mTOR signal per unit of training time.

(3) **Slower titration.** The fastest losers in STEP-1 had the worst lean-mass retention. Targeting ~0.5–1% body weight loss per week (not 2%+) preserves more muscle.

(4) **Creatine monohydrate 5 g/day.** Cheap, well-evidenced lean-mass preservation effect that stacks on top of training.

Full breakdown of the trial data and a week-by-week protein/training template: https://wolvestack.com/en/semaglutide-muscle-loss-risk.html and https://wolvestack.com/en/tirzepatide-muscle-loss-risk.html

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

## Summary

Drafted 5 evergreen template replies for 0 live threads (Reddit access blocked across every available tool — see top of file for the full blocker inventory). Drafts saved to reddit-drafts-2026-05-12.md. A should either (a) paste these against matching threads found manually, (b) switch this task to a chat-paste-URL workflow, or (c) disable until Reddit access is restored via OAuth token or an MCP connector. Today's templates are deliberately non-overlapping with the 10 templates produced 2026-05-10 + 2026-05-11 and the live-thread drafts from 2026-05-05 → 2026-05-09.
