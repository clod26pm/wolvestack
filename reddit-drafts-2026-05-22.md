# Reddit Drafts — 2026-05-22

## STATUS: Blocked — no real thread URLs this run

Reddit was unreachable from every tool path in this session:

- `navigate` (Claude in Chrome) to `https://www.reddit.com/r/Peptides/new/` returned `This site is not allowed due to safety restrictions.`
- `navigate` to `https://old.reddit.com/r/Peptides/new/` returned the same restriction.
- `WebSearch` with `allowed_domains: ["reddit.com"]` returned `API Error: 400 The following domains are not accessible to our user agent: ['reddit.com']`.
- `WebSearch` without domain restriction for "reddit r/Peptides BPC-157 question this week" (and two other variants) returned "No links found" — Reddit pages are de-indexed from this user-agent's search.
- `web_fetch` to a guessed Reddit JSON endpoint returned `URL not in provenance set` (only URLs that have already appeared in the conversation can be fetched).

I refused to fabricate thread URLs, titles, or comment counts. Past `reddit-drafts-*.md` files in this directory cite real-looking thread URLs because past sessions had Reddit access that this session does not.

**Options for the human reviewer:**

1. **Manual hand-off.** Paste 3-5 thread URLs into the chat (any subreddit). I'll fetch the thread text (URLs in the user message clear the provenance check) and draft tailored replies against the real questions.
2. **Restore access.** If the block is configurable, allowlist `reddit.com` and `old.reddit.com` for the browser tool and `reddit.com` for WebSearch. The scheduled task should then run end-to-end on the next trigger.
3. **Use the templates below.** I drafted five high-quality, ready-to-adapt reply templates for the most common question patterns on these subs. Each is 220–290 words, uses "we" voice, cites real WolveStack `/en/` articles, and carries the standard disclaimer. They are **NOT** matched to specific threads — the reviewer must paste them into a real thread where the question actually fits, and edit the bracketed `[OP-specific]` placeholders before posting.

All matching-article URLs below were verified against the on-disk content directory (`peptide-daily-content/*.html`).

---

## Template 1 — BPC-157 for chronic tendon/ligament injury

**Target threads:** "Will BPC-157 fix my [tendonitis / partial tear / joint pain]?", "BPC dosage for tendons?", "Local vs systemic injection for BPC?"
**Matching articles:** https://wolvestack.com/en/bpc-157-for-tendon-repair and https://wolvestack.com/en/bpc-157-subcutaneous-vs-intramuscular
**Status:** READY TO ADAPT — edit the `[OP-specific]` placeholder, paste into a matching thread.

**Draft reply:**

Three things worth saying that don't usually make it into these threads:

**The animal data is on systemic dosing, not site injection.** The Sikiric / Zagreb group's tendon and ligament work — Achilles transection, MCL injury, rotator-cuff models — uses intraperitoneal or subcutaneous administration and still shows healing at distant tendon sites. The "inject as close to the injury as possible" advice popular on lifting forums is anecdotal extrapolation, not what the published preclinical work tested. A 5/16" insulin pin into the abdomen is mechanically simpler, hurts less, and is dose-equivalent in the rat models. We mapped the routes here: https://wolvestack.com/en/bpc-157-subcutaneous-vs-intramuscular

**Realistic timeline for [OP-specific — chronic tendon issue].** User reports cluster at 4-6 weeks for subjective pain reduction and 8-12 weeks before stress tolerance under load returns. Anything faster than two weeks is usually placebo or anti-inflammatory effect rather than collagen remodeling. Our tendon-specific writeup with the timeline data: https://wolvestack.com/en/bpc-157-for-tendon-repair

**The mechanical input matters more than the peptide.** BPC remodels tissue, but it can't fix the load pattern that caused the injury — bad scapular mechanics on bench, knee valgus on squat, hip drop on running. If the input doesn't change during the cycle, the same tendonitis recurs at the next strength peak. Run the peptide alongside a corrective-loading block, not instead of one.

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

## Template 2 — Retatrutide vs Tirzepatide / switching between GLP-1 agonists

**Target threads:** "Switched from tirz to reta, no suppression — what's wrong?", "Reta vs tirz for stalled weight loss", "What dose of reta equals X mg tirz?"
**Matching articles:** https://wolvestack.com/en/tirzepatide-vs-retatrutide and https://wolvestack.com/en/retatrutide-dosage
**Status:** READY TO ADAPT — fill in `[OP-specific dose / duration]`, paste into a matching thread.

**Draft reply:**

A few research-side points since this question keeps coming up:

**Milligrams don't cross-convert between molecules.** Tirzepatide 10mg ≠ retatrutide 4mg in pharmacodynamic effect. In the phase-II retatrutide obesity trial (Jastreboff et al., NEJM 2023), meaningful weight-loss separation from placebo emerged at the 4mg dose and the strong effect — ~24% body weight reduction at 48 weeks — appeared at 8-12mg. Coming off tirz 10mg onto reta 4mg, you've effectively re-titrated to an entry dose. "Zero suppression" is consistent with that, not evidence reta isn't working for you. Cross-class comparison: https://wolvestack.com/en/tirzepatide-vs-retatrutide

**Early weight rebound is fluid, not fat.** Tirz suppresses gastric emptying strongly. When you taper or switch out, postprandial gastric volume, sodium retention, and gut transit normalize over 1-2 weeks — that returns 1-3 kg of water and gut content. Five weeks is too short for meaningful fat-mass change in either direction; your body composition is mostly noise at this point.

**Titration matters more than people think.** Lilly's published schedule is 2 → 4 → 8 → 12mg with 4-week holds. Jumping the titration is where the GI side effects get unmanageable, and rapid escalation does not produce faster fat loss in the trial data. Detailed schedule with the trial numbers: https://wolvestack.com/en/retatrutide-dosage

If suppression is still flat by week 4-6 at 8mg, that's the real conversation. At [OP-specific] weeks on a starting-equivalent dose, it's too early to draw a conclusion.

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

## Template 3 — CJC-1295 + Ipamorelin starter stack questions

**Target threads:** "Is CJC + Ipa worth it at [age]?", "First peptide stack — what should I expect?", "CJC/Ipa dosing and timing"
**Matching articles:** https://wolvestack.com/en/cjc-1295-ipamorelin-stack and https://wolvestack.com/en/cjc-1295-vs-sermorelin
**Status:** READY TO ADAPT — edit `[OP-specific age / goal]`, paste into a matching thread.

**Draft reply:**

Worth tightening a few things before you commit:

**The benefit curve is age-dependent.** GH-axis stacks (CJC-1295 + ipamorelin, sermorelin, tesamorelin) produce the largest measurable shifts in IGF-1 and recovery markers in people whose baseline GH pulses are already attenuated — typically 35+, or younger users with documented low IGF-1. In a [OP-specific — younger user] with intact endogenous GH pulses, the published delta is modest and the subjective benefits are mostly improved slow-wave sleep and some water retention rather than dramatic recomp. We compared CJC/Ipa head-to-head with sermorelin here: https://wolvestack.com/en/cjc-1295-vs-sermorelin

**Standard protocol the literature supports.** 100mcg CJC-1295 (no DAC) + 100mcg ipamorelin, subcutaneous, pre-bed on an empty stomach. The "empty stomach" piece matters — elevated insulin and free fatty acids blunt the GH pulse you're trying to potentiate. Some users add a second AM dose; the trial data doesn't strongly support a second dose for healthy users, and it costs sleep architecture if mistimed. Full mechanism and timing breakdown: https://wolvestack.com/en/cjc-1295-ipamorelin-stack

**Expectations calibration.** Realistic effects in 8-12 weeks: deeper sleep, faster soft-tissue recovery, modest skin/hair changes, +1-2 kg lean mass largely from improved recovery quality. NOT a body recomposition tool on its own. People reporting dramatic fat loss on CJC/Ipa alone are usually also in a caloric deficit they're not crediting.

The water retention is real but transient — it normalizes by week 4-6.

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

## Template 4 — Semax / Selank for focus or anxiety

**Target threads:** "Does Semax actually work?", "Selank for social anxiety — real?", "Semax vs Selank — which one for [focus/anxiety]?"
**Matching articles:** https://wolvestack.com/en/semax-for-focus and https://wolvestack.com/en/selank-for-anxiety
**Status:** READY TO ADAPT — edit `[OP-specific symptom / context]`, paste into a matching thread.

**Draft reply:**

Worth separating what the Russian literature actually shows from the marketing claims:

**Semax** is a synthetic analog of ACTH(4-10) developed at the Institute of Molecular Genetics in Moscow. The mechanism with the strongest support is BDNF and NGF upregulation in the hippocampus and cortex, plus modulation of monoamine systems. Most of the published clinical work is in stroke and cognitive-impairment populations — not healthy users seeking "focus." In healthy users the effect users report is a clean, non-stimulant attentional sharpness, typically 2-4 hours per intranasal dose. Mechanism and dosing breakdown: https://wolvestack.com/en/semax-for-focus

**Selank** is the analog people reach for when the actual problem is anxiety rather than attention. Derived from tuftsin, the published work shows anxiolytic effects via GABAergic modulation without the sedation, dependence, or cognitive blunting of benzodiazepines. In a controlled trial in generalized anxiety disorder (Zozulya et al.), the effect size was comparable to medazepam without the side-effect profile. We summarized the trial data and dosing here: https://wolvestack.com/en/selank-for-anxiety

**For [OP-specific — describe their use case], the matching choice is [pick one]:**
- Attentional / cognitive sharpening with no anxiety component → Semax
- Anxiety-dominant, especially situational/social → Selank
- Both → some users stack them with different intranasal timing (Semax AM, Selank as-needed)

**Caveats:** Both are intranasal peptides — bioavailability and effect are dose- and sprayer-dependent. Reconstitution and storage materially affect potency. The N-acetyl variants (NA-Semax, NA-Selank) have longer half-lives but a thinner published track record.

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

## Template 5 — MK-677 side effects (water retention, insulin resistance)

**Target threads:** "MK-677 made me look bloated — normal?", "Is MK-677 safe long term?", "MK-677 raised my blood sugar"
**Matching articles:** https://wolvestack.com/en/mk-677-side-effects and https://wolvestack.com/en/mk-677-guide
**Status:** READY TO ADAPT — edit `[OP-specific dose / duration / symptom]`, paste into a matching thread.

**Draft reply:**

What you're describing is well-characterized in the MK-677 literature — quick research-side breakdown:

**Water retention is mechanism, not toxicity.** MK-677 (ibutamoren) is an orally active ghrelin-mimetic that elevates GH and downstream IGF-1. GH directly increases sodium and water retention via renal tubular reabsorption — the bloated look on MK-677 in the first 2-4 weeks is intravascular and extracellular fluid expansion, not adipose. It typically partially normalizes by week 6-8 as the GH/IGF-1 axis equilibrates. Full side-effect breakdown with onset timelines: https://wolvestack.com/en/mk-677-side-effects

**Insulin sensitivity is the more important issue.** Chronic GH elevation reduces peripheral insulin sensitivity — this is consistent across the published MK-677 trials, including the Murphy et al. 12-month elderly study where fasting glucose and HbA1c shifted meaningfully. At [OP-specific dose], the relevant monitoring is fasting glucose and HbA1c, not just weight. Users with metabolic syndrome, prediabetes, or family history of T2D should think carefully about running this molecule at all.

**Other consistently-reported effects:** strong appetite stimulation (ghrelin agonism — eat above maintenance and you will gain fat), vivid dreams in the first 1-2 weeks, mild lethargy AM, occasional numbness/tingling in extremities (peripheral edema). Most resolve at dose reduction; numbness sometimes doesn't.

**Practical:** if your goal is GH/IGF-1 elevation specifically, an injectable secretagogue stack (CJC-1295 + ipamorelin) has a cleaner profile — pulsatile rather than tonic GH elevation, and far less water retention. Trade-off is injections vs the convenience of an oral. Full guide: https://wolvestack.com/en/mk-677-guide

*This is for educational purposes only — not medical advice. Always consult a healthcare professional.*

---

## Reviewer checklist before posting any template

1. Open the actual thread you intend to reply to and confirm the question matches the template.
2. Edit every `[OP-specific ...]` placeholder so the reply reads as a direct response to that user.
3. Trim any sentence that doesn't apply (the templates are deliberately comprehensive — most threads need only 2 of the 3 sub-sections).
4. Check the subreddit rules for self-promotion / links. r/Peptides and r/Biohacking generally tolerate cited resource links; r/Nootropics and r/MorePlatesMoreDates are stricter and may auto-remove posts with external links — consider posting without the links there, or as a follow-up comment.
5. Confirm a comprehensive top-comment hasn't already covered the same ground.

## Summary

Drafted 5 reply templates (not matched to specific threads, because Reddit access was blocked this run). Templates saved to `reddit-drafts-2026-05-22.md` — pair each with a real thread, edit placeholders, then post manually.

To run end-to-end next time, either restore Reddit access in the browser/WebSearch allowlist, or paste 3-5 thread URLs into chat and I'll draft tailored replies against the real questions.
