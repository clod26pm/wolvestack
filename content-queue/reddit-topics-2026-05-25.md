# Reddit / Trending-Topic Mining Report — 2026-05-25

## Methodology note (read first — be honest with yourself)

Reddit's API and the public reddit.com domain are not directly fetchable from this
session's web tool (URL provenance restriction), and Google web-search results in
2026 surface very few direct Reddit thread URLs for peptide queries. I therefore
built this report from a hybrid signal: (a) general web search for peptide topics
that consistently cite "Reddit" or "r/Peptides" community sentiment in their body
copy, and (b) FDA / clinical-trial / industry-news signals from May 2026 that we
KNOW will drive Reddit threads in the next 7–10 days even if those threads aren't
yet indexed. Topics flagged "high search demand" are backed by an explicit news
event (FDA approval, Phase-3 readout, regulatory action) rather than only by
anecdotal mentions. Treat the priority list as a directional brief, not a verbatim
log of specific threads.

WolveStack catalog cross-check was done locally against `/en/` (1,961 .html files);
every gap claim below was verified via `ls | grep` on the actual directory before
inclusion.

---

## High-Priority Article Ideas (write within 48hrs)

- **Orforglipron (Foundayo) complete guide** — Source: Eli Lilly press release + FDA approval coverage (AJMC, Healio, Lilly investor relations) — Estimated search demand: **VERY HIGH**. Foundayo was FDA-approved **April 1, 2026** as the first once-daily oral GLP-1 pill (no food/water restrictions). WolveStack currently has **only 1 file** (`orforglipron-guide.html`). This is a 27-article gap (dosage, side-effects, vs-semaglutide, vs-tirzepatide, results-timeline, for-beginners, before-and-after, cost, where-to-buy, etc.). Lilly's $25/month commercially-insured pricing and $149/month self-pay headline is what every Reddit thread will fixate on — write the pricing/access article first.
- **Orforglipron vs Semaglutide** — Source: AJMC + Physicians Weekly coverage of Foundayo approval — Estimated search demand: HIGH. New approval + identical patient population = the single most-Googled comparison query right now. WolveStack: **does not exist**.
- **Orforglipron vs Tirzepatide** — Estimated search demand: HIGH. Same logic; Foundayo is positioned as the oral alternative to weekly injectables. WolveStack: **does not exist**.
- **CagriSema (REDEFINE results) complete guide** — Source: Novo Nordisk REDEFINE 1 (22.7% wt loss), REDEFINE 2 (15.7%), REDEFINE 4 (failed non-inferiority vs tirzepatide), FDA submission Dec 2025, decision expected late 2026 — Estimated search demand: HIGH. WolveStack has **only 1 file** (`cagrisema-guide.html`). Build the standard 27-article cluster.
- **CagriSema vs Tirzepatide** — Source: REDEFINE 4 readout (cagrisema **failed** non-inferiority vs tirz) — Estimated search demand: HIGH. The angle is unusual because it's a negative finding — write the honest "CagriSema did NOT beat Tirzepatide" piece, not the marketing-spin version. WolveStack: does not exist.
- **CagriSema vs Semaglutide** — Source: REIMAGINE 2 (cagrisema superior to sema on HbA1c + weight). WolveStack: does not exist.
- **GLP-1 suicide-warning removal (Jan 2026 FDA action)** — Source: FDA Drug Safety Communication + Pharmacy Times + Psychiatric Times — Estimated search demand: HIGH. Reddit forums had years of "is Ozempic causing my dark thoughts" threads — the FDA in January 2026 **requested removal** of the suicidal-ideation warning from semaglutide/tirzepatide/liraglutide labels after a 91-trial / 107,910-patient meta-analysis. This is a reversal-of-narrative news event. WolveStack: not covered specifically. Suggested title: *"FDA Removed the Ozempic Suicide Warning in 2026 — Here's What the Evidence Actually Showed."*
- **FDA proposed 503B compounding ban on tirzepatide (open public comment through June 29, 2026)** — Source: Pharmacy Times, FDA.gov — Estimated search demand: HIGH. Every compounded-tirz patient on r/tirzepatidecompound is asking "when does my pharmacy stop?". The bulks-list and shortage-list pathways are both being closed. Article should cover: timeline, what happens to existing compound prescriptions, brand-name pricing alternatives, the 320+ adverse event report basis. WolveStack: not covered.
- **Microdosing GLP-1s — the wellness trend and what the data actually shows** — Source: GoodRx, Tufts Medicine, MedicalXpress coverage of the AI Reddit study — Estimated search demand: HIGH. WolveStack currently has **zero** dedicated articles on microdose-semaglutide or microdose-tirzepatide. This is one of the largest Reddit-driven wellness trends of 2026.
- **Reddit-flagged "overlooked" GLP-1 side effects: menstrual changes, chills, hot flashes** — Source: ScienceDaily 2026-05-23 + MedicalXpress 2026-04 coverage of the 400,000-Reddit-post analysis (nearly 4% of side-effect-reporting users described reproductive symptoms) — Estimated search demand: MEDIUM-HIGH. Article angle: "What 400,000 Reddit Posts Revealed About Ozempic Side Effects That Didn't Make It Into the Label." WolveStack: not covered.

## Comparison Articles Needed

- **Retatrutide vs CagriSema** — Why: Both are next-gen GLP-1+ candidates. Retatrutide hits 24.2% wt loss at 48 weeks; CagriSema hit 22.7% in REDEFINE 1 but failed non-inferiority vs tirz in REDEFINE 4. This is the comparison Reddit will ask about as both move toward 2026–2027 approval. WolveStack: does not exist.
- **Orforglipron vs Retatrutide** — Why: Oral pill vs the most potent injectable in trials. Different mechanism (single GLP-1 oral vs triple-agonist injectable). Does not exist.
- **CagriSema vs Retatrutide vs Tirzepatide vs Semaglutide — the 4-way 2026 GLP-1 landscape** — Why: A definitive overview piece. Tirz is the only one approved + on the market today; Foundayo just approved; Cagrisema FDA-pending; Retatrutide Phase 3 ongoing. Does not exist.
- **5-Amino-1MQ + Tirzepatide stack** — Why: This combo is making the rounds because the mechanisms are non-overlapping (GLP-1/GIP appetite suppression + NNMT inhibition / NAD+ preservation) and Reddit users use it to fight tirz-induced muscle/metabolic adaptation. WolveStack covers each separately but **no stack article exists**. High commercial potential (both are affiliate-relevant).
- **BPC-157 oral vs injection — when each actually wins** — Why: Recurring confusion on r/Peptides. Existing article (`bpc-157-oral-vs-injectable.html`) exists — audit it for current consensus (oral for gut/IBD/Crohn's, injection for localized musculoskeletal). 2025 per-oral quadriceps reattachment study expanded the case for oral. Refresh recommended rather than new build.

## Emerging Compounds to Research

- **Orforglipron (Foundayo)** — Context: FDA approved April 1, 2026. First once-daily oral GLP-1 with no food/water timing restriction. Phase 3 ATTAIN program: 12.4% mean wt loss at 72 weeks at highest dose. **Build the full 27-article cluster — this is the #1 priority compound for the next 30 days.**
- **CagriSema (semaglutide + cagrilintide)** — Context: Novo's amylin-co-agonist play. FDA-submitted Dec 2025. **Build the full 27-article cluster.**
- **SLU-PP-332** — Context: Exercise-mimetic / ERRα agonist out of Saint Louis University. Rodent trials show 31% body-fat reduction without exercise. Trending in biohacker/longevity communities. WolveStack: **zero coverage**. Build the full 27-article cluster (note: it's a small molecule, not technically a peptide — label it explicitly in the guide).
- **Tesofensine / Tesomet** — Context: Saniona triple-monoamine reuptake inhibitor + metoprolol fixed-dose combination, currently in Phase 3 in 2026 with potential EU/US filings 2027–2028. 10.6% body wt loss in 24 wks in Phase 2. WolveStack: **zero coverage**. Worth a guide + 5 supporting articles.
- **Enclomiphene** — Context: SERM-based oral TRT alternative gaining traction in men's-health telehealth ($150–$300/month in 2026); raises total T by ~84% in hypogonadal men while preserving fertility, unlike injectable TRT. Heavy r/Testosterone and r/moreplatesmoredates discussion volume. WolveStack: **zero coverage**. Strictly speaking enclomiphene isn't a peptide — it's a small molecule — but the audience overlap is high; consider a single guide-tier article rather than a full cluster.
- **Survodutide, Pemvidutide, Cotadutide, Maritide (MariTide)** — Context: Each in late-stage trials. WolveStack has 1 file each. Each warrants at minimum a guide + a vs-semaglutide + a vs-tirzepatide + a clinical-status article.
- **Methylene blue** — Context: Continually trending on r/Nootropics and r/Biohackers as a mitochondrial/cognitive stack adjunct. WolveStack: **zero coverage**. Same caveat as enclomiphene (small molecule, not peptide) — single guide-tier article suffices.
- **Mitopure / Urolithin A** — Context: Mitochondrial-quality / mitophagy biohacker compound. Not a peptide, but adjacent in the longevity stack conversation. WolveStack: **zero coverage**. Optional — only if site is willing to broaden scope beyond strict peptide definition.
- **Khavinson bioregulators (master guide)** — Context: WolveStack has individual clusters for Epithalon, Pinealon, Livagen, Pancragen, Bronchogen, Thymalin, Vilon, etc. — but **no unifying master article** explaining the bioregulator framework, sequences, and Khavinson's research lineage. Build a single hub article that internally links to every existing bioregulator cluster (also a strong internal-linking play for the SEO situation described in MEMORY.md — page-2 trapped, needs internal link depth).
- **KLOW / Wolverine stack expansion** — Context: WolveStack has `wolverine-stack.html` + `wolverine-stack-guide.html`. The KLOW variant (BPC-157 + TB-500 + GHK-Cu + KPV) is named in Scientific American's peptide-craze piece and is heavily discussed on Reddit. Audit existing Wolverine articles; if KLOW isn't explicitly named, write a dedicated `klow-stack.html` and link both directions.

## Trending Safety Concerns

- **FDA tirzepatide compounding ban (public comment open through June 29, 2026)** — Context: 503B outsourcing facilities lose bulks-list pathway. 320+ adverse event reports cited, many dosing errors. Patients on compounded tirz at $150–$300/month staring down brand pricing >$1,000.
- **GLP-1 suicide warning REMOVED** — Context: Counter-intuitive reversal. FDA Jan 2026 requested removal from sema/tirz/lira labels after meta-analysis of 91 trials / 107,910 patients found no causal link. Frame the article carefully — Psychiatric Times noted three semaglutide-associated deaths (incl. one suicide) allegedly underreported, so this is not a clean "all-clear."
- **Tirzepatide thyroid C-cell tumor black-box warning — what's actually known in 2026** — Context: Black-box remains in place despite zero statistically significant human signal across thousands of patients; entirely based on rodent studies where rats have far higher GLP-1R density on C-cells. WolveStack has `tirz-thyroid` coverage absent (0 files matching). Build the explainer.
- **GLP-1 reproductive side effects (menstrual irregularities)** — Context: AI-mined Reddit dataset (May 2026) flagged ~4% of side-effect-reporters mentioning menstrual changes. Not in current Wegovy/Zepbound labels.
- **BPC-157 tumor / cancer concern** — Context: WolveStack already has `bpc-157-cancer-concern.html` + `bpc-157-cancer-risk-risk.html` (note the duplicated "-risk" suffix — looks like a slug typo, **audit and fix** before chasing rankings). Reddit threads still surface this concern weekly; refresh + de-duplicate.
- **Compounded peptide FDA category-2 / bulks-list status (BPC-157, GHK-Cu, KPV, ipamorelin)** — Context: All four were placed on the FDA's restricted compounding category in 2023; status is unchanged in 2026 but Reddit users keep asking "is it banned now?" Build a single explainer covering the current legal status of every popular compound peptide.

## Dog / Pet Peptide Topics

- **LOY-002 (Loyal)** — Context: FDA Center for Veterinary Medicine accepted the Target Animal Safety and Reasonable Expectation of Effectiveness sections (2/3 of conditional approval requirements met as of early 2026). Daily beef-flavored tablet for dogs ≥10 yrs and ≥14 lbs, targets metabolic dysfunction. r/dogs, r/AskVet, r/PetLongevity threads spiking. WolveStack: **zero LOY-001 and LOY-002 articles**. Build a dedicated cluster: guide, vs-rapamycin, cost-and-access, FDA-timeline, candidate-dogs, before-and-after, side-effects.
- **LOY-001** — Context: Loyal's large-dog (40+ lbs) IGF-1-lowering injectable. WolveStack: zero coverage. Build a smaller cluster (guide + FDA-status + breed-eligibility).
- **Rapamycin for dogs (TRIAD trial)** — Context: Dog Aging Project TRIAD trial enrolling 580 dogs, 180+ enrolled as of Feb 2026. Once-weekly weight-adjusted oral dosing. WolveStack has `dog-longevity-peptides-guide.html` but no rapamycin-specific article (rapamycin isn't a peptide — same caveat as above, but the audience demands it; many Reddit threads pair it with peptide questions).
- **BPC-157 for dogs — dosing, joint pain, IVDD, CCL tears** — Context: Recurring questions from dog owners on Reddit + iHeartDogs + GLP1Forum. WolveStack has `bpc-157-for-dogs.html` — audit for breadth (specific conditions: CCL tear, IVDD, post-TPLO surgery, IBD-in-dogs). Add satellite articles per condition.
- **TB-500 for dogs** — Context: WolveStack has `tb-500-for-dogs.html`. Audit for currency; add a dosing-by-weight article and a vs-BPC-157-for-dogs comparison.
- **NAD+ injections for senior dogs** — Context: Holistic-vet community pushing it; no peer-reviewed canine evidence. WolveStack: zero coverage. Worth a guide-tier "evidence honestly" article that doesn't oversell.

---

## Suggested 7-day publication schedule (highest expected SEO impact first)

1. **Day 1**: `orforglipron-dosage.html`, `orforglipron-side-effects.html`, `orforglipron-vs-semaglutide.html`, `orforglipron-vs-tirzepatide.html`
2. **Day 2**: `orforglipron-cost-and-access.html` (Foundayo $25 commercial / $149 self-pay), `orforglipron-results-timeline.html`, `orforglipron-for-beginners.html`
3. **Day 3**: `cagrisema-vs-tirzepatide.html` (REDEFINE 4 failure angle), `cagrisema-vs-semaglutide.html`, `cagrisema-redefine-results.html`
4. **Day 4**: `glp1-suicide-warning-removed-fda-2026.html`, `tirzepatide-compounding-ban-2026.html`
5. **Day 5**: `loy-002-guide.html`, `loy-001-guide.html`, `loy-002-vs-rapamycin.html`
6. **Day 6**: `slu-pp-332-guide.html`, `slu-pp-332-dosage.html`, `slu-pp-332-vs-tirzepatide.html`
7. **Day 7**: `khavinson-bioregulators-master-guide.html` (interlink to all existing bioregulator clusters — also serves the GSC page-2-trap internal-link-depth fix noted in MEMORY.md)

## Internal cleanup items (drop into the writer's queue, low cost)

- Fix slug duplication: `bpc-157-cancer-risk-risk.html` — typo, redirect or rename to `bpc-157-cancer-risk.html`.
- Audit `bpc-157-oral-vs-injectable.html` against 2025 per-oral quadriceps-reattachment study + 2026 community consensus (oral for gut, injection for localized).
- Audit `wolverine-stack.html` + `wolverine-stack-guide.html` — these may be near-duplicates competing for the same query. Consolidate or differentiate explicitly (e.g., one targets "stack" / one targets "guide" intent).
- Verify `dog-longevity-peptides-guide.html` mentions LOY-002 by name; if not, refresh it.

---

## Sources

- [Get ready for the peptides gold rush — MM+M](https://www.mmm-online.com/news/get-ready-for-the-peptides-gold-rush/)
- [Anti-Aging Peptide Shots Are Trending on Social Media — TIME](https://time.com/7380810/anti-aging-peptide-shots-social-media/)
- [FDA Approves Lilly's Oral GLP-1 Orforglipron for Obesity — AJMC](https://www.ajmc.com/view/fda-approves-lilly-s-oral-glp-1-orforglipron-for-obesity)
- [FDA approves Foundayo, an oral GLP-1, for adults with obesity — Healio](https://www.healio.com/news/endocrinology/20260401/fda-approves-orforglipron-an-oral-glp1-for-adults-with-obesity)
- [FDA approves Lilly's Foundayo™ (orforglipron) — Eli Lilly Investor](https://investor.lilly.com/news-releases/news-release-details/fda-approves-lillys-foundayotm-orforglipron-only-glp-1-pill)
- [CagriSema: 22.7% Weight Loss in Phase 3 Trials — FindHonestCare](https://www.findhonestcare.com/metabolic-innovations/cagrisema/)
- [CagriSema Demonstrates Weight Loss, Fails Primary Endpoint vs Tirzepatide — HCPLive](https://www.hcplive.com/view/cagrisema-demonstrates-weight-loss-fails-to-achieve-primary-endpoint-compared-to-tirzepatide)
- [CagriSema Phase 3 REDEFINE 2 — Patient Care Online](https://www.patientcareonline.com/view/cagrisema-phase-3-update-weight-loss-of-nearly-16-seen-in-redefine-2-trial)
- [CagriSema submitted to FDA — Novo Nordisk](https://www.novonordisk.com/content/nncorp/global/en/news-and-media/news-and-ir-materials/news-details.html?id=916481)
- [Retatrutide vs Tirzepatide comparison — PeptideDeck](https://www.peptidedeck.com/peptides/retatrutide-vs-tirzepatide)
- [Retatrutide—A Game Changer in Obesity Pharmacotherapy — PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12190491/)
- [FDA Moves to Permanently Close the Door on Compounded GLP-1s — Pharmacy Times](https://www.pharmacytimes.com/view/fda-moves-to-permanently-close-the-door-on-compounded-glp-1s)
- [FDA clarifies policies for compounders as GLP-1 supply stabilizes — FDA.gov](https://www.fda.gov/drugs/drug-alerts-and-statements/fda-clarifies-policies-compounders-national-glp-1-supply-begins-stabilize)
- [FDA Requests Removal of Suicidal Behavior Warning from GLP-1 RAs — FDA.gov](https://www.fda.gov/drugs/drug-safety-communications/fda-requests-removal-suicidal-behavior-and-ideation-warning-glucagon-peptide-1-receptor-agonist-glp)
- [FDA Issues Removal of Suicidal Behavior Warning — Psychiatric Times](https://www.psychiatrictimes.com/view/fda-issues-removal-of-suicidal-behavior-and-ideation-warning-from-glp-1-ras)
- [AI scans 400,000 Reddit posts to flag overlooked GLP-1 side effects — MedicalXpress](https://medicalxpress.com/news/2026-04-ai-scans-reddit-flag-overlooked.html)
- [AI scans 400,000 Reddit posts — ScienceDaily](https://www.sciencedaily.com/releases/2026/05/260523103914.htm)
- [Tirzepatide and Cancer: What the Science Says in 2026 — RealPeptides](https://www.realpeptides.co/does-tirzepatide-cause-cancer-2/)
- [Investigating FDA Reports of Tirzepatide-Thyroid Cancer Connection — EMJ Reviews](https://www.emjreviews.com/oncology/news/investigating-fda-reports-of-tirzepatide-thyroid-cancer-connection/)
- [Microdosing GLP-1s: Does It Work? — GoodRx](https://www.goodrx.com/conditions/weight-loss/microdosing-glp-1)
- [Microdosing GLP-1s — Tufts Medicine](https://www.tuftsmedicine.org/about-us/news/microdosing-glp-1s-your-questions-answered)
- [Loyal Receives FDA Acceptance of Safety Package for LOY-002 — BusinessWire](https://www.businesswire.com/news/home/20260113476778/en/Loyal-Receives-FDA-Acceptance-of-Safety-Package-for-Senior-Dog-Lifespan-Extension-Drug)
- [LOY-002 Receives RXE from FDA — Loyal.com](https://loyal.com/posts/loy-002-receives-rxe-from-the-fda)
- [Second drug for canine healthy lifespan extension receives FDA support — dvm360](https://www.dvm360.com/view/second-drug-for-canine-healthy-lifespan-extension-receives-fda-support)
- [Dog Aging Project TRIAD Rapamycin Trial — AVMA](https://www.avma.org/news/7m-grant-rescues-dog-study-investigating-rapamycin-canine-aging)
- [BPC-157 for Dogs: Arthritis, Joint Pain — iHeartDogs](https://iheartdogs.com/bpc-157-for-dog-arthritis-joint-pain-a-promising-peptide-in-canine-health/)
- [Tesofensine — Wikipedia](https://en.wikipedia.org/wiki/Tesofensine)
- [SLU-PP-332: Exercise Mimetic — Champion Peptides](https://www.championpeptides.com/slu-pp-332-exercise-mimetic-research/)
- [SLU-PP-332 Benefits — PeptideDeck](https://www.peptidedeck.com/peptides/slu-pp-332)
- [Enclomiphene as TRT Alternative — FormBlends](https://formblends.com/articles/trt-hub/enclomiphene-trt-alternative)
- [Khavinson Bioregulators Complete Guide — SeekPeptides](https://www.seekpeptides.com/blog/articles/khavinson-peptides-complete-guide)
- [Most Popular Peptides on Reddit 2026 — Peptide Authority](https://peptideauthority.co.uk/blog/most-popular-peptides-reddit-2026)
- [The 7 Most Popular Peptide Stacks — Meto](https://meto.co/blog/most-popular-peptide-stacks-science)
- [The Science Behind the Peptide Craze — Scientific American](https://www.scientificamerican.com/article/the-science-behind-the-peptide-craze/)
- [BPC 157 Oral vs Injection — Amino Innovations](https://aminoinnovations.com/bpc-157-oral-versus-injection/)
- [5-Amino-1MQ vs Tirzepatide — Mokiner](https://mokiner.com/5-amino-1mq-vs-tirzepatide/)
- [Tirzepatide + 5-Amino-1MQ Stack — RealPeptides](https://www.realpeptides.co/tirzepatide-5-amino-1mq-stack-protocol-2/)
