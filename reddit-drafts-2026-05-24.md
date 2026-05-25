# Reddit Outreach Drafts — 2026-05-24

## RUN STATUS: PARTIALLY BLOCKED

The scheduled task could not source live Reddit threads in this run for two hard blockers:

1. **No Chrome browser connected.** `mcp__Claude_in_Chrome__list_connected_browsers` returned an empty array — Claude in Chrome is installed in the toolset but no extension instance is paired to this session. Without it, the agent cannot navigate Reddit, search subreddits, or read thread comments.
2. **`reddit.com` is blocked from Anthropic's web crawler.** `WebSearch` with `allowed_domains: ["reddit.com"]` returns a 400 error stating "The following domains are not accessible to our user agent: ['reddit.com']". Generic searches that might surface Reddit URLs from third-party indexers also returned no Reddit links, and `mcp__workspace__web_fetch` requires URLs to already be in the conversation provenance — which they cannot be without a successful prior search.

**To fix on the next run, A should do ONE of:**
- Pair a Chrome browser by installing/launching the Claude in Chrome extension and signing in, OR
- Update the scheduled task to use a Reddit MCP connector (e.g., something from the connector registry that wraps Reddit's API with auth), OR
- Pre-paste a batch of candidate thread URLs into the task prompt so the agent has provenance to fetch them.

## FALLBACK DELIVERABLE

Because the upstream sourcing step failed, the agent has produced five **evergreen template replies** below — each one targets a recurring question pattern that appears in r/Peptides, r/Nootropics, r/PEDs, r/HGH, and r/biohacking on roughly a weekly basis. Each draft is research-grounded, written in WolveStack research-team voice, includes 1–2 article links, and stays in the 150–300 word band.

**Status convention used below:**
- `READY TO POST` — only used when a real thread is matched (none today).
- `TEMPLATE — NEEDS THREAD MATCH` — copy/paste once A finds a matching live thread. Do NOT post to a thread the draft doesn't actually address.

---

### Thread: [TEMPLATE] "Should I take BPC-157 orally or injected for [tendon/joint/gut issue]?"
**Subreddit:** r/Peptides / r/MorePlatesMoreDates
**URL:** [paste thread URL here before posting]
**Matching articles:** https://wolvestack.com/en/bpc-157-guide and https://wolvestack.com/en/bpc-157-injection-guide
**Status:** TEMPLATE — NEEDS THREAD MATCH

**Draft reply:**
The route depends on what tissue you're trying to reach. For GI issues — IBD-pattern symptoms, NSAID-induced gut damage, anastomotic healing — oral or sublingual makes physiological sense because the peptide hits the GI lining directly and the rodent work (Sikiric and colleagues, Zagreb group, 1990s–2000s) used both oral and intraperitoneal routes successfully for gut models. BPC-157 appears unusually stable in gastric juice for a peptide, which is part of why it gets studied at all.

For tendon, ligament, and joint targets, the published preclinical data we trust most uses parenteral dosing — Krivic 2008 (Achilles transection in rats) and Cerovecki 2010 (medial collateral ligament) both used systemic injection, not oral. We don't have human RCT data establishing that oral dosing reaches musculoskeletal targets in meaningful concentrations. Subcutaneous near the injury site is what most researchers in this space default to.

Practical note: there are no FDA-approved indications, the systemic safety database in humans is small, and a lot of vendor marketing oversells the certainty here. We covered the route question and dose-range research in detail here: https://wolvestack.com/en/bpc-157-guide — and the actual injection mechanics (needle size, reconstitution, site rotation) here: https://wolvestack.com/en/bpc-157-injection-guide

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

### Thread: [TEMPLATE] "Hit a plateau on tirzepatide/semaglutide — what now?"
**Subreddit:** r/Peptides / r/PEDs
**URL:** [paste thread URL here before posting]
**Matching articles:** https://wolvestack.com/en/tirzepatide-dosage and https://wolvestack.com/en/semaglutide-vs-tirzepatide
**Status:** TEMPLATE — NEEDS THREAD MATCH

**Draft reply:**
Plateaus on GLP-1 / dual-agonist therapy are well-documented in the trial data, not just anecdotal. In SURMOUNT-1 the tirzepatide weight-loss curve flattens around month 9–12 at each maintenance dose, and STEP-1 showed the same pattern for semaglutide around week 60. Two mechanistic things are usually happening at once: counter-regulatory adaptation (lower resting energy expenditure as fat mass drops) and dose-response saturation at your current titration step.

The interventions with the strongest evidence are also the most boring: confirm you're actually at the labeled maintenance dose (not stuck at a sub-therapeutic titration rung), audit protein intake — research suggests 1.6 g/kg of target body weight is a reasonable floor to preserve lean mass — and add resistance training if you aren't already. Some clinicians titrate tirzepatide higher (10 → 12.5 → 15 mg) when 10 mg plateaus; that's on-label and showed additional weight loss in SURMOUNT.

Switching molecules (semaglutide → tirzepatide) is the other common move. SURPASS-2 head-to-head showed tirzepatide producing greater weight loss than semaglutide 1 mg in T2D patients, but the comparison at semaglutide's higher 2.4 mg obesity dose is less clean. We laid out the titration logic and the dose-response data here: https://wolvestack.com/en/tirzepatide-dosage — and the direct comparison here: https://wolvestack.com/en/semaglutide-vs-tirzepatide

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

### Thread: [TEMPLATE] "First CJC-1295 + Ipamorelin cycle — timing, dose, what to expect?"
**Subreddit:** r/Peptides / r/HGH
**URL:** [paste thread URL here before posting]
**Matching articles:** https://wolvestack.com/en/cjc-1295-ipamorelin-stack and https://wolvestack.com/en/ipamorelin-dosage
**Status:** TEMPLATE — NEEDS THREAD MATCH

**Draft reply:**
First thing worth clarifying because it gets conflated constantly: "CJC-1295" almost always means CJC-1295 **without DAC** (modified GRF 1-29 / tetrasubstituted GHRH analog) in this context. CJC-1295 *with* DAC has a much longer half-life (~6–8 days) which flattens the pulsatile GH signal — that's the opposite of what you want when stacking with a ghrelin mimetic, where the whole point is to amplify a discrete pulse.

The standard research protocol pairs the two because they hit different receptors — GHRH receptor (CJC) and GHSR-1a / ghrelin receptor (ipamorelin) — and their effects on GH release are synergistic rather than additive in the published rodent and small human data. Common research-context doses are 100 mcg of each, subcutaneous, on an empty stomach. Timing matters: food (especially carbs and fat) within ~30 minutes of dosing blunts the GH pulse via insulin and free fatty acid feedback.

Pre-bed dosing is popular because it aligns with the natural nocturnal GH pulse; some protocols also use a morning fasted dose. Expect water retention, possible numbness/tingling in fingers from fluid shifts, and vivid dreams — those are dose-related. Ipamorelin is favored specifically because, unlike GHRP-6 or hexarelin, it doesn't meaningfully spike cortisol or prolactin at standard doses (Raun et al., original 1998 characterization).

Stack mechanics and timing breakdown here: https://wolvestack.com/en/cjc-1295-ipamorelin-stack and standalone ipamorelin dose-response here: https://wolvestack.com/en/ipamorelin-dosage

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

### Thread: [TEMPLATE] "Semax vs Selank — which one for [anxiety / focus / both]?"
**Subreddit:** r/Nootropics
**URL:** [paste thread URL here before posting]
**Matching articles:** https://wolvestack.com/en/semax-vs-selank and https://wolvestack.com/en/selank-guide
**Status:** TEMPLATE — NEEDS THREAD MATCH

**Draft reply:**
They're cousins, not substitutes. Both are short synthetic peptides developed at the Institute of Molecular Genetics in Moscow, both are used intranasally, and both are still on the Russian formulary — but they target different things.

Semax is a heptapeptide (Met-Glu-His-Phe-Pro-Gly-Pro) derived from the ACTH(4-10) sequence. The Russian preclinical and clinical work centers on neurotrophic effects — BDNF and NGF upregulation has been documented in rat brain (Dolotov, Inozemtseva, Levitskaya groups, ~2003–2006) — and the clinical use in Russia is mostly for ischemic stroke recovery and cognitive load. Subjectively, users report it as more "wake-promoting and task-oriented" than anxiolytic.

Selank is a heptapeptide analog of the immune fragment tuftsin (Thr-Lys-Pro-Arg-Pro-Gly-Pro). The published mechanism leans GABAergic and serotonergic, and the human trial work — small Russian RCTs in generalized anxiety disorder, Zozulya et al. 2008 in Bulletin of Experimental Biology and Medicine — showed anxiolytic effects comparable to medazepam without the sedation or dependence profile of benzos.

So the heuristic most people land on: Selank if the primary complaint is anxiety, Semax if it's cognitive throughput. Stacking them is common in the Russian dosing literature.

Worth noting: the evidence base is almost entirely Russian, sample sizes are small, and neither is FDA-approved. We did a side-by-side here: https://wolvestack.com/en/semax-vs-selank — and a deeper Selank breakdown here: https://wolvestack.com/en/selank-guide

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

### Thread: [TEMPLATE] "Is MK-677 worth running long-term? Worried about water retention / insulin resistance"
**Subreddit:** r/Peptides / r/MorePlatesMoreDates / r/PEDs
**URL:** [paste thread URL here before posting]
**Matching articles:** https://wolvestack.com/en/mk-677-side-effects and https://wolvestack.com/en/mk-677-cycle
**Status:** TEMPLATE — NEEDS THREAD MATCH

**Draft reply:**
Both concerns track real findings in the published data, so this is worth taking seriously rather than dismissing.

Water retention: ibutamoren / MK-677 sustains elevated GH and IGF-1 around the clock (unlike a pulsatile GHRH/GHRP stack), and the resulting increase in extracellular fluid is dose-dependent. Murphy et al. (1998, J Clin Endocrinol Metab) and the longer Nass et al. 2008 trial both documented edema, mild arthralgia, and modest weight gain in the first weeks that often partially resolves.

Insulin resistance: this is the bigger one. The Nass 2008 two-year trial in older adults showed an increase in fasting glucose and a measurable rise in HbA1c — small in absolute terms but consistent. The mechanism is the well-described GH-induced post-receptor insulin resistance. People who are already pre-diabetic or carry significant visceral fat should treat this as a serious flag, not a footnote.

Practical implications people in this thread usually land on: time-limited runs (8–12 weeks) rather than indefinite, baseline + on-cycle fasting glucose and HbA1c testing, and skipping it entirely if you have a personal or family history of T2D. Lower doses (10 mg vs 25 mg) reduce both edema and glycemic impact in the dose-response data.

Side-effect rundown with the specific trial numbers here: https://wolvestack.com/en/mk-677-side-effects — and cycle-length reasoning here: https://wolvestack.com/en/mk-677-cycle

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

## Summary

Drafted 5 evergreen template replies. Live thread sourcing was blocked (no Chrome browser paired + reddit.com blocked from web crawler). Templates saved to reddit-drafts-2026-05-24.md — A must (a) pair Chrome or add a Reddit MCP connector for future runs to source threads autonomously, and (b) manually paste matching thread URLs before posting any of the templates above.
