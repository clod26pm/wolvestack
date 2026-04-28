#!/usr/bin/env python3
"""
English v2 generator — humanized voice for /en/ pages.

Goals:
1. Fill the ~99 thin /en/ stub files with cornerstone-quality humanized content
2. Inject FAQ JSON-LD schema for the ~755 files missing it
3. Preserve existing substantial /en/ content (don't overwrite cornerstones)

Humanized writing principles:
- Lead with a hook (discovery story, controversy, surprising fact)
- Name specific researchers and labs (Sikiric's lab in Zagreb, Jastreboff at Yale)
- Vary sentence rhythm — mix short punchy sentences with longer analytical ones
- Use conversational connectives: "Here's the catch", "What's notable", "The thing is"
- Express measured stance — distinguish solid evidence from speculation
- Avoid SEO cliches ("comprehensive guide", "evidence-based recommendations")
- Include honest skepticism about study limitations
- Reference real studies with names + years + specific findings
"""
import os, re, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EN_DIR = ROOT / 'en'

# ============================================================
# Humanized compound profiles — written in voice, not templated
# ============================================================
COMPOUNDS = {
    'bpc-157': {
        'name': 'BPC-157',
        'category': 'Tissue repair peptide',
        'related': ['tb-500', 'ghk-cu', 'thymosin-alpha-1'],
        'overview': "BPC-157 is a 15-amino acid fragment of a larger protein found in human gastric juice — the body's own protection compound, hence the name. Predrag Sikiric's lab at the University of Zagreb first isolated and characterized it in the early 1990s, initially as a gastric protector. What no one expected was just how broadly it would work. By the early 2000s, animal studies were showing BPC-157 accelerated healing in tendons, ligaments, muscle, brain, blood vessels — almost any tissue you tested. That's a suspicious-sounding profile (compounds that work on everything usually work on nothing), but the consistency of the rodent data is genuinely striking, and Sikiric has now published over 200 papers on it.",
        'mechanism': "The mechanism story is messy because BPC-157 seems to do several things at once. It upregulates VEGF and promotes angiogenesis (new blood vessel growth at injury sites), which probably explains a lot of the tissue-healing effects — better blood supply, better repair. It boosts nitric oxide synthesis. It modulates the dopamine and serotonin systems via the gut-brain axis (Sikiric's main theoretical framework). It plays with growth hormone receptor expression. The honest summary: nobody has nailed down a single primary mechanism, and that makes some researchers uncomfortable. The trade-off is that the same multi-mechanism story would explain why a single peptide seems to help so many different injuries.",
        'evidence': "Here's where you have to be careful. The animal evidence is genuinely impressive — Krivic et al. (2008) showed accelerated Achilles tendon repair in rats, Cerovecki et al. (2010) showed faster medial collateral ligament healing, and there's a long string of NSAID-induced gastric ulcer studies showing 90%+ mucosal protection. The catch: as of 2026, there are zero registered randomized human clinical trials. The athletic recovery community has effectively run a giant uncontrolled experiment for 15+ years with anecdotes that range from miraculous to nothing-happened, but that's not the same as RCT evidence. So: solid mechanistic and animal data, no human trial data, ongoing research-only status.",
        'dosing': "Typical research protocols run 200-500 mcg daily via subcutaneous injection, often split into two doses. Many users inject near the injury site on the theory that local concentration helps — this is plausible but not actually proven. Oral protocols (250-500 mcg, 1-2x daily) are also studied; BPC-157 is unusually stable in stomach acid, which is part of what makes it interesting compared to most peptides. Acute injuries often start with higher loading doses (500 mcg twice daily) for 4-8 weeks, tapering down. The half-life is short (a few hours subcutaneously), which is why twice-daily dosing is standard.",
        'safety': "The safety profile in animal studies is excellent — extremely high LD50 (>10g/kg), no acute toxicity events. Long-term human data simply doesn't exist. Reported mild side effects are notable mostly for being unremarkable: occasional injection site reactions (~10-15% of users), transient fatigue in the first week, mild nausea on oral protocols. The theoretical concern that comes up most often is whether the angiogenesis-promoting properties could accelerate existing tumors — there's no human evidence for or against this, but most researchers exclude cancer history from research populations as a precaution. Not FDA-approved. Notably, WADA hasn't banned it (as of 2026), unlike TB-500.",
        'quick_answer': "BPC-157 is a 15-amino acid peptide derived from human gastric juice, studied since the early 1990s by Sikiric's lab in Zagreb for tissue repair effects. The animal evidence on tendons, ligaments, muscle, and gut healing is consistent and impressive — the catch is that there are no registered human trials. Typical research protocols use 200-500 mcg daily via subcutaneous injection over 4-8 weeks. The mechanism is multi-pathway (angiogenesis, nitric oxide, gut-brain axis), which is unusual but matches the broad effect profile. Often stacked with TB-500 for injury work. Not FDA-approved; the athletic recovery community has run an uncontrolled experiment for 15+ years.",
    },
    'tb-500': {
        'name': 'TB-500',
        'category': 'Tissue repair peptide',
        'related': ['bpc-157', 'ghk-cu', 'thymosin-alpha-1'],
        'overview': "TB-500 isn't actually a complete molecule — it's a 17-amino acid fragment of thymosin beta-4 (Tβ4), one of the most abundant intracellular proteins in your body. The fragment corresponds to the active region. Most of the original interest came from veterinary medicine in the 1990s, where TB-500 was being used to speed tendon and soft tissue recovery in racehorses (and, predictably, in humans who took notes). RegeneRx (now G-treeBNT) developed several clinical candidates over the years. The athletic-recovery community treats TB-500 and BPC-157 as a default pairing for injuries — sometimes for sound mechanistic reasons, sometimes because the protocols got copied around enough times that it became cargo cult.",
        'mechanism': "Thymosin beta-4's primary biological job is sequestering G-actin monomers — basically, it controls how cells crawl around during repair. That cell-migration role is what makes TB-500 interesting for healing: if you're trying to rebuild a tendon, you need fibroblasts to actually get to the right place. Beyond that, it promotes angiogenesis (more VEGF, more new blood vessels), dampens inflammatory cytokines (TNF-α, IL-6, IL-1β), and protects cardiomyocytes from ischemic damage via the Akt survival pathway. Bock-Marquette et al.'s 2004 Nature paper on cardiac protection is probably the single most-cited mechanistic study.",
        'evidence': "Animal evidence is broad and consistent: cardiac ischemia-reperfusion (the Nature paper), wound healing (Malinda et al. 1999), corneal repair, neural regeneration. RegeneRx ran multiple Phase II trials in humans — RGN-352 for systemic muscle wasting, RGN-259 for ophthalmology, RGN-137 for wound healing. The results were a mixed bag — some endpoints hit, some didn't. The clearest red flag isn't efficacy, it's regulatory: WADA banned TB-500 in 2011 as an S2 substance (growth factors). For competitive athletes, that's not a theoretical concern.",
        'dosing': "Standard research protocols are 2-5 mg per week subcutaneously, split into two doses. Acute injury phases often use a 'loading dose' approach — 2-2.5 mg daily for the first week, then 4-6 weeks at the loading dose, dropping to 2 mg/week for maintenance. The half-life is genuinely days (versus hours for BPC-157), which is what enables the weekly schedule. Site rotation matters more than people think — repeated injections in the same spot lead to local reactions and impaired absorption. The 'BPC + TB' combined protocol is overwhelmingly the most common research configuration.",
        'safety': "Human safety data is limited but RegeneRx's clinical trials didn't surface major issues. The theoretical concern is the same as with BPC-157, only louder: angiogenesis and cell migration are exactly what tumors need. Cancer history is an exclusion in most research, and that's the right call. Reported side effects are mostly the boring kind — injection site reactions, transient fatigue, occasional dizziness. The WADA ban means competitive athletes face real consequences for use, including in retirement testing programs.",
        'quick_answer': "TB-500 is a 17-amino acid fragment of thymosin beta-4, originally used in veterinary medicine for racehorse tendon recovery before crossing into human research. Mechanism is multi-pronged: actin sequestration drives cell migration (key for tissue repair), plus angiogenesis and anti-inflammatory effects. Bock-Marquette et al. 2004 (Nature) on cardiac protection is the foundational mechanistic paper. RegeneRx ran multiple Phase II human trials with mixed results. Standard protocol: 2-5 mg/week subcutaneous, often as a 'loading + maintenance' structure with BPC-157. WADA-banned since 2011 — competitive athletes can't use it. Half-life is days, supporting weekly dosing.",
    },
    'semaglutide': {
        'name': 'Semaglutide',
        'category': 'GLP-1 receptor agonist (FDA-approved)',
        'related': ['tirzepatide', 'retatrutide', 'liraglutide', 'cagrisema'],
        'overview': "Semaglutide is the molecule that broke the obesity drug market. Novo Nordisk developed it as a long-acting GLP-1 receptor agonist for type 2 diabetes — branded as Ozempic for diabetes and Wegovy for obesity, with an oral version called Rybelsus. Structurally it's a 31-amino acid peptide based on the natural GLP-1(7-37) hormone, with a fatty acid (C18) sidechain that lets it bind to albumin in your blood. That albumin binding is the trick: it extends the half-life from minutes to about 7 days, which is why semaglutide works as a weekly injection. Novo's semaglutide revenue hit roughly $9.5 billion in Q2 2024 alone. Not a typo.",
        'mechanism': "Semaglutide binds the GLP-1 receptor (GLP-1R), a G-protein-coupled receptor, and activates the cAMP/PKA pathway downstream. That triggers several effects in parallel: glucose-dependent insulin secretion (you only get the boost when blood sugar's actually elevated, which is why hypoglycemia is rare), suppression of glucagon release, slowed gastric emptying (you feel fuller longer), and direct activation of POMC/CART neurons in the hypothalamic arcuate nucleus that drive satiety. The Aib substitution at the N-terminus blocks DPP-4 degradation; the C18 fatty acid does the albumin-binding trick. Both modifications are why semaglutide is so much longer-acting than native GLP-1.",
        'evidence': "STEP 1 (NEJM 2021) is the headline trial: 2.4 mg semaglutide weekly for 68 weeks, 14.9% mean weight loss in non-diabetic obese patients versus 2.4% on placebo. That's not in the same league as previous obesity drugs — it changed the conversation. STEP 5 extended to 104 weeks with sustained 15.2% loss. The SUSTAIN trial series (1-10) established its diabetes credentials: HbA1c drops of 1.5-1.8%, weight loss of 4-6 kg. The most important recent trial is SELECT (NEJM 2023), which showed a 20% reduction in MACE (major adverse cardiovascular events) in obese non-diabetic patients with cardiovascular disease — that's a meaningful cardio-protective effect, not just weight loss. PIONEER series validated the oral form.",
        'dosing': "Diabetes dosing starts at 0.25 mg weekly and titrates every 4 weeks: 0.5 → 1.0 → max 2.0 mg. Obesity dosing goes higher: 0.25 → 0.5 → 1.0 → 1.7 → 2.4 mg max. The slow titration is genuinely important for tolerability — fast titration cranks the nausea rate way up. Oral Rybelsus starts at 7 mg daily, increases to 14 mg after 4 weeks, must be taken on an empty stomach (30+ minutes before food, with no more than 4 oz of water). The empty-stomach requirement is annoying but real; absorption tanks otherwise.",
        'safety': "Side effects are dominated by GI: nausea (44.2% in STEP 1), vomiting (24.8%), diarrhea (31.5%), constipation (24.2%) — most concentrated in the titration phase, easing over time. Real but rare risks: acute pancreatitis (0.1-0.3% in SUSTAIN), gallbladder events (gallstones, cholecystitis, 2-3% with long-term use), worsening of diabetic retinopathy (in pre-existing diabetics — likely from rapid HbA1c improvement). The FDA black box warning is for medullary thyroid carcinoma based on rodent studies; the human relevance remains unclear, but family history of MEN2 syndrome is an absolute contraindication.",
        'quick_answer': "Semaglutide (Ozempic for diabetes, Wegovy for obesity, Rybelsus oral) is Novo Nordisk's long-acting GLP-1 receptor agonist that effectively reset expectations for obesity drugs. STEP 1 (2021) showed 14.9% weight loss at 68 weeks — far beyond any previous obesity medication. The C18 fatty acid sidechain enables albumin binding and a ~7-day half-life, making weekly dosing possible. Mechanism combines insulin sensitization, glucagon suppression, slowed gastric emptying, and direct hypothalamic satiety signaling. SELECT (2023) added a 20% cardiovascular event reduction to the story. Side effects are GI-dominated; black box warning for medullary thyroid carcinoma based on rodent data.",
    },
    'tirzepatide': {
        'name': 'Tirzepatide',
        'category': 'Dual GIP/GLP-1 agonist (FDA-approved)',
        'related': ['semaglutide', 'retatrutide', 'cagrisema', 'survodutide'],
        'overview': "Tirzepatide (Mounjaro for diabetes, Zepbound for obesity) is Eli Lilly's dual GIP and GLP-1 receptor agonist — the first dual agonist of its class to get FDA approval, in 2022. Structurally it's a 39-amino acid peptide with a C20 di-fatty acid sidechain (similar albumin-binding strategy to semaglutide, but with a different sidechain chemistry). Half-life is about 5 days, supporting weekly dosing. Within two years of launch it had eaten enormous market share from semaglutide on the obesity side — Lilly reported about $4.9 billion in tirzepatide revenue in Q3 2024 alone. The interesting biology question is *why* adding GIP to GLP-1 makes such a big difference, and the honest answer is we still don't fully know.",
        'mechanism': "Tirzepatide activates both the GIP (glucose-dependent insulinotropic polypeptide) receptor and the GLP-1 receptor — that's the key difference from semaglutide. The GIP pathway appears to amplify insulin secretion synergistically, improve adipose tissue function and fat storage signaling, and somehow potentiate the GLP-1-mediated weight loss effect. 'Somehow' is the right word here: GIP alone, in some animal models, doesn't help with weight loss at all (and there are GIP antagonist drugs in development like MariTide that *also* claim weight loss benefits). The current best hypothesis is that tirzepatide is a 'biased agonist' that preferentially activates G-protein signaling over β-arrestin recruitment, which reduces receptor desensitization. This is still being worked out.",
        'evidence': "SURPASS series (diabetes): SURPASS-2 (NEJM 2021) compared tirzepatide 15 mg weekly versus semaglutide 1 mg weekly head-to-head — HbA1c reduction of -2.30% versus -1.86%, weight loss of -11.2 kg versus -5.7 kg. In the obesity domain, SURMOUNT-1 (NEJM 2022) showed 22.5% weight loss at 72 weeks on 15 mg weekly versus 2.4% on placebo. That 22.5% is the largest weight loss ever demonstrated in a non-surgical obesity trial. SURMOUNT-3 with intensive lifestyle pre-treatment pushed total reductions higher. SURMOUNT-OSA showed clinically meaningful improvements in obstructive sleep apnea AHI scores.",
        'dosing': "Starts at 2.5 mg weekly, titrates every 4 weeks through 5.0 → 7.5 → 10.0 → 12.5 → 15 mg max. The titration scheme has more steps than semaglutide because the maximum dose is higher and the GI side effect curve gets steeper at high doses. The FDA label calls 5 mg the minimum therapeutic dose — anything below that is purely for tolerance ramping. Half-life is ~5 days. Site rotation matters (abdomen, thigh, deltoid).",
        'safety': "Side effect profile largely overlaps GLP-1 monotherapy: GI is the dominant issue, with nausea rates running 33% on the 15 mg arm in SURMOUNT-1, plus 23% diarrhea, 14% vomiting, 17% constipation. Other risks parallel semaglutide: pancreatitis (0.2-0.3%), gallbladder problems (5-6% long-term), diabetic retinopathy in pre-existing diabetics. FDA black box warning for medullary thyroid carcinoma based on rodent studies — same as with all GLP-1 class drugs. MEN2 and prior medullary thyroid cancer are contraindications.",
        'quick_answer': "Tirzepatide (Mounjaro/Zepbound) is Eli Lilly's dual GIP/GLP-1 receptor agonist, FDA-approved in 2022. SURMOUNT-1 (2022) showed 22.5% weight loss at 72 weeks on 15 mg weekly — the highest ever recorded in a non-surgical obesity trial, beating semaglutide's ~15%. The GIP component synergizes with GLP-1 in ways that are still being worked out (interestingly, GIP antagonists also seem to help with weight loss, which complicates the story). Half-life of ~5 days supports weekly dosing. Side effects parallel GLP-1 drugs — GI-dominated. Black box warning for medullary thyroid carcinoma based on rodent data.",
    },
    'retatrutide': {
        'name': 'Retatrutide',
        'category': 'Triple GLP-1/GIP/glucagon agonist (Phase 3)',
        'related': ['tirzepatide', 'semaglutide', 'cagrisema'],
        'overview': "Retatrutide (LY3437943) is Eli Lilly's triple agonist — same playbook as tirzepatide but adding a third receptor (glucagon) to the existing GLP-1 + GIP stack. It's currently in Phase 3 (the TRIUMPH series), and the Phase 2 data was striking enough to make 'retatrutide' a household name in the GLP-1-watcher community well before any approval. Structurally similar to tirzepatide (39-amino acid peptide, C20 fatty acid sidechain, ~6-day half-life), the key addition is a glucagon receptor agonist component. Approval timeline points to 2026-2027 pending Phase 3 results. The grey-market scene has predictably exploded around it.",
        'mechanism': "On top of the GIP + GLP-1 synergy you get with tirzepatide, glucagon receptor activation drives energy expenditure and fat oxidation directly — it's the same mechanism that gives natural glucagon its fat-burning effects (increased hepatic glucose output, increased fatty acid oxidation). The 'triple-hit' approach is supposed to attack obesity from three angles at once: appetite suppression (GLP-1), insulin sensitization (GIP/GLP-1), and direct metabolic stimulation (glucagon). The trick is dosing the glucagon component carefully — too much and you start pushing blood glucose up, defeating part of the purpose. Lilly tuned the molecule for biased agonism to maximize fat-burning while minimizing the diabetogenic risk.",
        'evidence': "Phase 2 TRIUMPH-1 (NEJM 2023, Jastreboff et al.) is the trial everyone is talking about: 24.2% weight loss at 48 weeks on 12 mg weekly, versus 2.1% on placebo. What's almost more interesting than the headline number is the fact that the curve hadn't plateaued at 48 weeks — extended follow-up suggests the actual ceiling could be even higher. Diabetes substudy showed strong HbA1c improvements alongside the weight loss. NAFLD substudy showed 80%+ reduction in liver fat content, which is genuinely impressive for a metabolic agent. Phase 3 TRIUMPH series is ongoing: TRIUMPH-1 through TRIUMPH-4 plus TRIUMPH-NASH and a cardiovascular outcomes trial.",
        'dosing': "Trial protocols start at 0.5 mg weekly and titrate up through 1.0 → 2.0 → 4.0 → 8.0 → 12.0 mg every 4 weeks. The slow titration matters more than usual here because the glucagon component can drive heart rate increases and GI side effects more aggressively than pure GLP-1. The final approved dose schedule will depend on Phase 3 data — there's a real possibility the labeled max ends up lower than the trial max. Until approval, retatrutide is research-only or grey-market — and the grey-market quality risks are very real.",
        'safety': "So far retatrutide's side effect profile mirrors GLP-1/GIP drugs — GI-dominated, with Phase 2 reporting 39% nausea, 24% diarrhea, 21% vomiting at the highest doses. The glucagon-related concerns are mostly theoretical at this point: dose-dependent heart rate increases of 5-7 bpm have been documented, and high-dose diabetic patients need close glucose monitoring. Long-term safety data is still being collected. The NAFLD numbers suggest excellent hepatic safety so far, which is reassuring given that long-term metabolic interventions sometimes surprise you on the liver.",
        'quick_answer': "Retatrutide (LY3437943) is Lilly's triple GLP-1/GIP/glucagon agonist, currently in Phase 3 TRIUMPH trials. The Phase 2 result everyone remembers: 24.2% weight loss at 48 weeks on 12 mg weekly — and the curve hadn't plateaued, suggesting the actual ceiling could be even higher. Mechanism stacks appetite suppression (GLP-1), insulin sensitization (GIP/GLP-1), and direct fat oxidation via glucagon receptor activation. Half-life ~6 days, weekly dosing, titrated from 0.5 to 12 mg. FDA approval expected 2026-2027. NAFLD data shows 80%+ liver fat reduction. Side effects are GI-dominated; glucagon-related heart rate increases need monitoring at high doses.",
    },
    'ipamorelin': {
        'name': 'Ipamorelin',
        'category': 'Growth hormone secretagogue',
        'related': ['cjc-1295', 'sermorelin', 'tesamorelin', 'ghrp-2', 'mk-677'],
        'overview': "Ipamorelin is the GHRP that 'fixed' GHRPs. Earlier compounds in the class (GHRP-6, GHRP-2) worked, but they came with side effects nobody wanted — cortisol bumps, prolactin elevation, hunger like a switch had been flipped (the GHRP-6 hunger response was actually used in eating disorder research). Novo Nordisk developed ipamorelin in the late 1990s as compound NN703 — a pentapeptide engineered for selectivity. It hits the ghrelin receptor (GHSR-1a) cleanly and triggers GH release without meaningfully touching cortisol, prolactin, or your appetite system. Novo took it to Phase IIa as a GH deficiency diagnostic and then dropped it for commercial reasons, not safety. It's been a research staple ever since.",
        'mechanism': "Ipamorelin agonizes the ghrelin receptor (GHSR-1a) on pituitary somatotrophs, triggering pulsatile GH release. Because it doesn't touch the GHRH pathway, it pairs naturally with GHRH analogs (CJC-1295 without DAC, sermorelin) for synergistic GH release — the two pathways amplify each other through non-redundant signaling (cAMP/PKC versus PLC/IP3). The selectivity is what made it interesting in the first place: structural features of the pentapeptide make it preferentially bind GHSR-1a over related receptor subtypes, which is why you don't get the cortisol/prolactin spillover that earlier GHRPs caused.",
        'evidence': "Single-dose human studies show 3-5x peak GH elevation; IGF-1 climbs gradually over 2-4 weeks of continuous dosing. Novo's Phase IIa trial established baseline safety and tolerability. Raun et al. (1998) in the European Journal of Endocrinology is the foundational pharmacology paper if you want the receptor selectivity data in detail. There's no Phase III evidence supporting any specific indication — Novo dropped it before that. RegeneRx and others have explored applications in post-surgical recovery and muscle wasting with limited clinical traction.",
        'dosing': "Common research protocols use 100-300 mcg per dose, 2-3 times daily subcutaneously, timed for natural GH pulse windows: pre-bed (peak GH happens within 90 minutes of sleep onset) and post-workout. Pairing with CJC-1295 without DAC at 100 mcg per dose 2-3x daily — the 'ipa + CJC' protocol — is the most common research configuration. Half-life is ~2 hours, which is why the multiple-daily-dose schedule. Eating immediately before dosing tends to blunt the GH response (especially fat or carbs); 2-3 hours fasted is the standard recommendation.",
        'safety': "Ipamorelin's tolerability is genuinely good. Reported side effects: injection site reactions (~10%), mild headache (5-10%), occasional transient dizziness, facial flushing when paired with GHRH analogs (more from the GHRH analog than the ipamorelin). Theoretical concern: long-term GH elevation could affect glucose metabolism and insulin sensitivity, but Novo's short-term Phase IIa didn't see meaningful impact. Receptor downregulation (desensitization) shows up after several months of continuous dosing — cycling protocols (5 days on, 2 off, or longer cycles) are standard practice in research to manage this.",
        'quick_answer': "Ipamorelin is a pentapeptide growth hormone secretagogue developed by Novo Nordisk in the late 1990s — a 'cleaner' GHRP that triggers GH release without the cortisol, prolactin, or appetite bumps that plagued earlier compounds (GHRP-6, GHRP-2). It's a selective ghrelin receptor (GHSR-1a) agonist; for synergistic GH release, it's paired with GHRH analogs like CJC-1295 without DAC. Research protocols: 100-300 mcg, 2-3x daily subcutaneous. Half-life ~2 hours. Raun et al. (1998) is the foundational pharmacology reference. Tolerability is good — mild headaches and injection site reactions are the main complaints. Cycling is standard practice to avoid receptor desensitization.",
    },
    'cjc-1295': {
        'name': 'CJC-1295',
        'category': 'GHRH analog',
        'related': ['ipamorelin', 'sermorelin', 'tesamorelin', 'mk-677'],
        'overview': "CJC-1295 has a complicated history. ConjuChem developed it as a modified GHRH analog with two distinct forms: CJC-1295 without DAC (drug affinity complex, half-life ~30 minutes, similar to sermorelin) and CJC-1295 with DAC (half-life of 6-8 days). The DAC variant was the commercial bet — weekly dosing is way more attractive than three-times-daily. ConjuChem took it to Phase IIa for adult GH deficiency, but the trial got suspended in 2007-2008 over blood pressure issues including one fatality. Causation was never confirmed, but ConjuChem moved on. The molecule survived in the research-chemical market, where the without-DAC form is the more common configuration in serious protocols.",
        'mechanism': "CJC-1295 binds GHRH receptors on pituitary somatotrophs and triggers GH synthesis and pulsatile release. Structurally it preserves the GHRH 1-29 sequence (same as sermorelin) plus a 4-amino-acid N-terminal modification that resists DPP-4 degradation. The DAC version covalently links to serum albumin via the C-terminal modification, dramatically extending circulation time and producing a sustained 'GH bleed' rather than discrete pulses. That sustained pattern departs from normal physiology — and that's the central concern about the DAC form: GH evolved to be pulsatile, and we don't fully understand the long-term consequences of flattening that pulsatility.",
        'evidence': "Teichman et al. (JCEM 2006) is the key human Phase I/II paper: single-dose CJC-1295 with DAC raised baseline IGF-1 levels 1.5-3x for up to 7 days. Multi-dose studies pushed sustained IGF-1 elevations of +90% over baseline for 11 days. Then came the 2007-2008 Phase IIa trial — blood pressure issues plus one death (causation not confirmed) ended the program. Sackmann-Sala et al. and other follow-up work has questioned whether sustained GH exposure is biologically equivalent to pulsatile secretion.",
        'dosing': "CJC-1295 without DAC: typical research dose is 100 mcg per administration, 2-3x daily, almost always paired with ipamorelin or GHRP-2. The pulsatile pattern is the whole point — this approximates physiological GHRH/ghrelin co-stimulation. CJC-1295 with DAC: 1-2 mg weekly subcutaneously. The dosing pattern (pulsatile vs sustained) is the central debate — they produce meaningfully different downstream signaling environments, even at equivalent total IGF-1 elevations.",
        'safety': "Common side effects: injection site reactions, facial flushing (a tell-tale sign of GHRH receptor activation, dose-dependent), mild edema (more pronounced with DAC), transient headache. The DAC form's long-acting nature can amplify all of these. The blood pressure signal from the ConjuChem trial was never adequately explained — for some researchers that's a deal-breaker, for others it's noise. Long-term insulin sensitivity is a theoretical concern with sustained IGF-1 elevation.",
        'quick_answer': "CJC-1295 is a modified GHRH analog with two forms: without DAC (~30 min half-life, sermorelin-like) and with DAC (6-8 day half-life via covalent albumin binding). The DAC variant produces a sustained 'GH bleed' rather than pulses, which is biologically unusual. ConjuChem took it to Phase IIa for adult GH deficiency before suspending the program in 2007-2008 over blood pressure problems including one death (causation unconfirmed). Research dosing: without-DAC at 100 mcg 2-3x daily paired with ipamorelin (pulsatile pattern); with-DAC at 1-2 mg weekly. Side effects: injection site reactions, flushing, edema. Not FDA-approved.",
    },
    'mk-677': {
        'name': 'MK-677',
        'category': 'Oral growth hormone secretagogue',
        'related': ['ipamorelin', 'cjc-1295', 'sermorelin'],
        'overview': "MK-677 (also called ibutamoren or Nutrobal) is the GH secretagogue that almost made it through approval, then didn't. Merck developed it in the 1990s as a non-peptide oral compound — most growth hormone secretagogues are peptides that need injection, but MK-677 mimics ghrelin signaling well enough to be effective orally. Multiple Phase II/III trials in sarcopenia, hip fracture recovery, and growth hormone deficiency. The reason it never crossed the regulatory finish line wasn't safety in any catastrophic sense — it was the predictable consequences of long-term GH elevation: weight gain, fluid retention, modest blood sugar deterioration. Merck called it. Reverse Pharma (a Merck spinoff) continued partial development without approval success.",
        'mechanism': "MK-677 is a non-peptide ghrelin receptor (GHSR-1a) agonist — same receptor as ipamorelin, completely different molecule class. Oral bioavailability is >60%, which is unusual for ghrelin pathway agents. Half-life is ~4-6 hours, but the downstream effects last much longer because of receptor signaling dynamics — once-daily dosing is sufficient. Long-term use elevates IGF-1 by 60-90%, which is a substantial steady-state shift. The pulsatility is somewhat preserved (unlike CJC-1295 with DAC), which is part of why the cardiovascular and metabolic side effect profile is more manageable.",
        'evidence': "The single most important MK-677 paper is Nass et al. (2008) in the Annals of Internal Medicine — a 2-year study in healthy older adults (65+) showing 1.6 kg lean mass gain, modest bone density improvement (+0.7%), and 60% IGF-1 elevation. Murphy et al. (1998) demonstrated GH pulse restoration in adult GH-deficient patients. The hip fracture recovery trial (Adunsky et al., 2011) didn't hit primary endpoints, which contributed to Merck's decision to stop development. The long-term Nass data is what most informs current research dosing protocols.",
        'dosing': "Research protocols use 10-25 mg orally once daily. Doses above 25 mg don't show additional benefit — IGF-1 elevation plateaus. Pre-bed dosing aligns with natural GH pulse timing and tends to produce the strongest IGF-1 response. Empty stomach (30+ minutes before food) may modestly improve absorption but the effect isn't dramatic. Cycling is debatable — some research protocols cycle 8-12 weeks on, 4 weeks off; others run continuously based on the long-term Nass safety data.",
        'safety': "Side effects: appetite increase (60-70% of users — that's the ghrelin signaling), sodium and water retention (most pronounced in the first 2-4 weeks, generally improves), occasional transient muscle aches, modest glucose tolerance deterioration (HbA1c +0.1-0.2% in the Nass trial). Insulin resistance is the main long-term concern — pre-diabetics and diabetics should be cautious or avoid. CHF decompensation showed up in some trials, so heart failure is a contraindication. WADA banned (S2 class), so competitive athletes need to stay clear.",
        'quick_answer': "MK-677 (ibutamoren / Nutrobal) is Merck's oral non-peptide growth hormone secretagogue from the 1990s — works on the same ghrelin receptor (GHSR-1a) as ipamorelin but as a small molecule with >60% oral bioavailability. Nass et al. (2008) demonstrated 1.6 kg lean mass gain and 60% IGF-1 elevation in healthy older adults over a 2-year study. Merck stopped development because of weight gain and modest glucose tolerance issues, not safety failures. Research dosing: 10-25 mg orally once daily, pre-bed for best IGF-1 response. Side effects: appetite increase, water retention, mild glucose tolerance impairment. WADA-banned. Avoid in heart failure or pre-diabetes.",
    },
    'tesamorelin': {
        'name': 'Tesamorelin',
        'category': 'GHRH analog (FDA-approved for HIV lipodystrophy)',
        'related': ['sermorelin', 'cjc-1295', 'ipamorelin'],
        'overview': "Tesamorelin is the GHRH analog that actually got approved. The brand is Egrifta (Theratechnologies); the FDA approval came in November 2010 for treatment of HIV-associated lipodystrophy with excess visceral adiposity. That's a narrow indication, but it represents something rare — a GHRH-pathway peptide that crossed the regulatory finish line with proper Phase III evidence. Structurally it's GHRH 1-44 with an N-terminal trans-3-hexenoyl modification that confers DPP-IV resistance. Half-life is 26-38 minutes subcutaneously. The trans-3-hexenoyl trick is what makes the difference — without it, tesamorelin would just be sermorelin-like.",
        'mechanism': "Tesamorelin activates pituitary GHRH receptors, triggering endogenous GH release and downstream IGF-1 elevation. The crucial feature versus older GHRH analogs is the N-terminal modification that resists DPP-IV degradation, extending circulating half-life. Pulsatility is preserved (unlike CJC-1295 with DAC) — physiological negative feedback through IGF-1 and somatostatin still operates, which is why over-stimulation of the GH axis is rare. That preserved feedback is what makes Egrifta's safety profile manageable enough to get approved.",
        'evidence': "Falutz et al. (NEJM 2007) is the pivotal Phase III paper: 26 weeks of treatment reduced visceral adipose tissue (CT-measured) by 15-20%, dropped triglycerides by 25%, decreased waist circumference by 2-3 cm. Stanley et al. (2014) extended the data to 52 weeks with sustained benefit. The MERIT-1 trial explored tesamorelin for HIV-associated cognitive complaints with mixed results. Among GHRH-pathway peptides, this is essentially the only one with bona fide Phase III RCT evidence — most others (sermorelin, CJC-1295) stop at Phase II at best.",
        'dosing': "FDA-approved dose is 2 mg subcutaneously daily. Off-label research dosing tends to use similar levels. Half-life of 26-38 minutes is short enough to keep dosing daily, but long enough that single-dose-per-day works reliably. Dose adjustments are rarely needed — the standard fixed protocol is well-tolerated.",
        'safety': "Common side effects in trials: injection site reactions (~24%), arthralgia (13%), peripheral edema (6%), myalgia (5%). The notable concern is glucose tolerance — HIV trials showed mild HbA1c elevation (+0.1-0.2%). Diabetics or pre-diabetics need close monitoring. Rarely, carbohydrate intolerance becomes severe enough to require dose adjustment or discontinuation. Tumor risk warning on the label (GH/IGF-1 axis activation, theoretical concern) — active malignancy is a contraindication.",
        'quick_answer': "Tesamorelin (Egrifta, by Theratechnologies) is the FDA-approved GHRH analog — approved in November 2010 for HIV-associated lipodystrophy with visceral fat accumulation. The N-terminal trans-3-hexenoyl modification confers DPP-IV resistance and extended half-life. Falutz et al. (NEJM 2007) showed 15-20% visceral fat reduction at 26 weeks. FDA-approved dose is 2 mg subcutaneously daily. It's effectively the only GHRH-pathway peptide with proper Phase III RCT evidence. Side effects include injection site reactions, arthralgia, and modest glucose tolerance impairment (HbA1c +0.1-0.2%). Active malignancy is contraindicated.",
    },
    'melanotan-ii': {
        'name': 'Melanotan II',
        'category': 'Non-selective melanocortin receptor agonist',
        'related': ['melanotan-i', 'pt-141'],
        'overview': "Melanotan II is the peptide that wasn't supposed to be a sex drug. Norman Levine and colleagues at the University of Arizona melanoma research group developed it in the 1980s, hoping for a sunless tanning compound that could reduce skin cancer risk through MC1R-mediated melanogenesis. The clinical trials uncovered something nobody expected: dose-dependent erections in male subjects. That was the spinoff path that eventually produced PT-141 (bremelanotide). Melanotan II itself never got FDA approval — the Phase II trials had too many side effects to be viable as a tanning agent. But it survived in the grey market, where it's been sold as a research chemical for decades. National regulators and dermatologists actively warn against it because of melanoma concerns.",
        'mechanism': "Melanotan II is a non-selective agonist of all four melanocortin receptors: MC1R, MC3R, MC4R, MC5R. That receptor promiscuity is both the source of its diverse effects and the reason its side effect profile is messy. MC1R activation in skin melanocytes drives eumelanin synthesis — that's the tanning effect. MC3R/MC4R activation in the hypothalamus drives appetite suppression and sexual arousal. MC4R activation triggers erections (the route to PT-141). MC5R activation modulates exocrine gland function. The key contrast: selective agonists like Setmelanotide (MC4R-selective) and Afamelanotide (MC1R-selective) avoid most of the off-target effects. Melanotan II hits everything at once.",
        'evidence': "Tanning effects are well-documented in small trials — Dorr et al. (1996) at Arizona showed reproducible skin darkening responses. The sexual arousal observations led directly to PT-141's development as a targeted clinical candidate. The arm of the program targeting tanning never advanced past Phase II — the side effect profile (nausea, erections in male subjects, mole changes) was unworkable for a cosmetic indication. Long-term safety data is mostly absent except for case reports from grey-market use.",
        'dosing': "Research protocols are 0.25-1 mg per dose subcutaneously, starting low and titrating up. The 'loading phase' approach uses small daily doses for 1-2 weeks until target pigmentation; 'maintenance phase' is 1-2 doses per week. Doses above 1 mg push the side effect rate up sharply. Evening dosing is common to minimize daytime side effects. Some sun exposure (UV from sunlight or a tanning bed) is needed to actually trigger the melanogenesis — Melanotan II by itself doesn't darken skin without UV stimulation.",
        'safety': "Side effects: nausea (60-80% on first doses, dose-dependent), facial flushing, transient erections in male users (often unwanted), mole darkening and new mole formation (the headline melanoma concern), cardiovascular effects (heart rate, blood pressure changes), appetite suppression (welcome or unwelcome depending on user). The melanoma signal is the most concerning issue: case reports document new or accelerated melanomas in users; the mechanism is biologically plausible (MC1R activation in transformed melanocytes), but causation isn't established. Dermatologists strongly oppose Melanotan II use — any suspicious mole needs immediate evaluation.",
        'quick_answer': "Melanotan II is a non-selective melanocortin receptor agonist developed at the University of Arizona in the 1980s as a tanning agent — designed to reduce skin cancer risk through MC1R-mediated melanogenesis. The clinical trials surfaced unexpected sexual effects, leading to PT-141 (bremelanotide). FDA never approved it. Hits all four melanocortin receptors (MC1R/3R/4R/5R), which is the source of its diverse effects: tanning (MC1R), appetite suppression and arousal (MC4R), erections (MC4R). Research protocols use 0.25-1 mg subcutaneous loading then maintenance. Side effects are significant: 60-80% nausea, mole changes (melanoma concern), cardiovascular effects, unwanted erections. Dermatologists strongly oppose use. Research-only status.",
    },
}

# Cross-link map
RELATED_MAP = {
    'noopept': ['cerebrolysin', 'semax'],
    'tb-500': ['bpc-157', 'ghk-cu'],
    'mots-c': ['humanin', 'epithalon'],
    'epithalon': ['mots-c', 'foxo4-dri'],
    'igf-1-lr3': ['cjc-1295', 'ipamorelin', 'mk-677'],
    'ghk-cu': ['ghk', 'bpc-157', 'tb-500'],
    'thymosin-alpha-1': ['ll-37', 'thymalin'],
    'pt-141': ['melanotan-i', 'melanotan-ii'],
    'melanotan-i': ['melanotan-ii', 'pt-141'],
}

SKIP_SLUGS = {
    'about', 'privacy', 'terms', 'disclaimer', 'affiliate-disclosure',
    'index', 'search', '404', 'TEMPLATE-BODY', 'TEMPLATE-CSS',
    'ARTICLE-TEMPLATE',
}


def parse_slug(slug):
    s = slug.replace('.html', '')
    if s in SKIP_SLUGS:
        return ('__SKIP__', None)

    compound_keys = sorted(COMPOUNDS.keys(), key=len, reverse=True)
    for ck in compound_keys:
        if s == ck or s == ck + '-guide':
            return (ck, 'guide')
        if s.startswith(ck + '-'):
            return (ck, _map_remainder(s[len(ck) + 1:]))

    return (s, 'guide')


def _map_remainder(rem):
    if not rem:
        return 'guide'
    am = {
        'guide': 'guide', 'beginners': 'beginners', 'for-beginners': 'beginners',
        'dosage': 'dosing', 'cycle': 'cycling', 'faq': 'faq',
        'side-effects': 'safety', 'safety': 'safety', 'benefits': 'benefits',
        'research': 'research', 'reviews': 'reviews', 'reconstitution': 'reconstitution',
        'storage': 'storage', 'half-life': 'pharmacokinetics',
        'how-it-works': 'mechanism', 'injection-guide': 'injection',
        'where-to-buy': 'sourcing', 'buy': 'sourcing', 'legal': 'legal',
        'stacking': 'stacking', 'timeline': 'timeline',
        'before-and-after': 'beforeafter', 'for-men': 'men', 'for-women': 'women',
        'results-timeline': 'timeline',
    }
    if rem in am:
        return am[rem]
    if rem.startswith('vs-'):
        return f'comparison:{rem[3:]}'
    if rem.startswith('for-'):
        return f'application:{rem[4:]}'
    return 'guide'


# ============================================================
# Humanized aspect framings
# ============================================================
def aspect_paragraphs(angle, c):
    name = c['name']
    cat = c['category']
    related = c.get('related', [])
    rel_links = ', '.join(related[:3]) if related else ''

    if angle in ('guide', 'general', 'comprehensive'):
        return [
            (f'What is {name}?', c['overview']),
            ('How It Works: Mechanism', c['mechanism']),
            ('What the Research Shows', c['evidence']),
            ('Dosing and Administration', c['dosing']),
            ('Safety Profile and Side Effects', c['safety']),
            ('Where It Fits in the Broader Research Landscape',
             f"{name} sits in the {cat.lower()} category. The compounds you'll see compared most often are {rel_links}. None of them are 1:1 substitutes — each has a different mechanism profile and evidence base, and the choice usually comes down to your specific research question rather than a 'best' compound." if related else
             f"{name} sits in the {cat.lower()} category. The research landscape around it is shaped more by what we don't know than by what we do — long-term human data is the most obvious gap."),
            ('Practical Considerations',
             f"A few things that come up repeatedly with {name} research. First: the quality variance between suppliers is real and not subtle. Independent third-party HPLC verification on a per-batch basis (not 'representative samples') is the only thing that gets you reliable potency. Second: most research protocols start at the lower end of the dosing range and titrate up — this lets you identify individual response patterns before committing to higher exposure. Third: documentation matters more than people expect. Tracking dose, timing, injection site, and any subjective or biomarker changes is what turns 'I tried it' into actual research data."),
            ('Regulatory Reality',
             f"In the US and most jurisdictions, {name} is not approved for human use — it's sold as a research chemical or laboratory reagent. The FDA's 503A versus 503B compounding pharmacy guidelines have tightened in 2023-2024, restricting which peptides can be compounded. WADA's prohibited list also matters for athletes (some peptides are banned, some aren't — it varies). Regulatory status changes over time; check current rules before starting any research protocol."),
        ]

    if angle == 'beginners':
        return [
            (f'Starting Point: What {name} Actually Is', c['overview']),
            ('Three Things Beginners Should Understand First',
             f"If you're new to {name} research, the three things to nail down before anything else: (1) {name} is a {cat.lower()} — that determines what mechanisms are at play and which applications make sense. (2) The evidence base is uneven — some applications have human trial data, others rest on animal models or anecdote. Knowing the difference matters. (3) Most research peptides aren't approved for human use in most jurisdictions. The legal status varies and it's not academic."),
            ('Mechanism in Plain Terms', c['mechanism']),
            ('Why Mechanism Matters Practically',
             f"Mechanism understanding isn't just academic — it tells you which applications are mechanistically plausible, which combinations might be synergistic versus redundant, and what side effects are mechanism-related rather than incidental. With {name}, the mechanism story shapes how you'd think about dosing, timing, and what 'success' looks like."),
            ('Starting Doses', c['dosing']),
            ('Safety to Watch For', c['safety']),
            ('Sourcing Quality is Non-Negotiable',
             f"Quality variance between {name} suppliers is one of the most underestimated variables in research-chemical work. The same compound from a quality supplier versus a grey-market source can differ by 50% in potency — and purity issues affect safety, not just efficacy. Look for: independent third-party HPLC certificates of analysis (CoA), batch-specific data (not 'representative samples'), proper cold-chain handling, transparent sourcing, and a track record of customer feedback. If any of those are missing, the supplier isn't ready for serious research use."),
            ('A Practical First Protocol',
             f"For beginners researching {name}: (1) Read 5-10 peer-reviewed papers to build mechanism understanding before doing anything. (2) Define a specific research question and a measurable endpoint — vague 'see what happens' protocols generate vague results. (3) Establish baseline measurements (relevant biomarkers, symptom scales, performance metrics). (4) Verify supplier quality. (5) Plan your titration. (6) Establish a relationship with a healthcare provider for monitoring. (7) Have an adverse event response plan: what symptoms would make you stop, who would you call. This sounds like overkill until something unexpected happens."),
            ('Common Misconceptions',
             f"Three myths that come up over and over with {name}: (1) Animal effects translate directly to humans. They often don't — dose, route, and metabolic differences mean animal-to-human extrapolation needs to be cautious. (2) Anecdotal reports = clinical evidence. They generate hypotheses but don't replace controlled studies. (3) More dose = more effect. Dose-response curves are often bell-shaped or saturable; past the optimal point you usually lose benefit and gain side effects."),
            ('Where to Go Next',
             f"Once you've worked through the basics with {name}, the natural next topics are dosing optimization, mechanism in deeper detail, and how it compares to related compounds — particularly {rel_links}." if related else
             f"Once you've worked through the basics with {name}, the natural next steps are dosing optimization, mechanism in deeper detail, and the broader research-chemical landscape it fits into."),
        ]

    if angle == 'dosing':
        return [
            (f'Dosing {name}: What the Research Says', c['dosing']),
            (f'How {name} Works (and Why That Matters for Dosing)', c['mechanism']),
            ('Why Individual Variation Matters',
             f"The 'standard' research doses for {name} represent population averages — individual responses vary substantially. Age, weight, sex, baseline biomarker levels, target endpoints, and existing health conditions all influence what optimal dosing looks like. The way you find your individual response window is by establishing baseline measurements and tracking what changes as dose changes."),
            ('Why Titration Beats Direct-to-Target',
             f"With {name}, ramping up gradually almost always beats jumping to your target dose. Titration lets you (1) characterize your individual response curve, (2) catch sensitivity issues before they become problems, (3) minimize early adverse events, (4) build a sustainable long-term protocol. Typical pattern: increase every 2-4 weeks based on tolerance and observed response."),
            ('Timing Within the Day',
             f"{name}'s optimal dosing windows depend on its mechanism, half-life, and what target you're after. " + c['mechanism'][:200]),
            ('Aligning Dose with Endpoint',
             f"Different research endpoints with {name} may need different dose ranges. The dose that's optimal for one application isn't necessarily optimal for another — even when the compound is the same. Endpoint-driven dose decisions tend to outperform a generic 'standard dose' assumption."),
            ('Safety Considerations at Different Doses', c['safety']),
            ('Documentation Pays Off',
             f"Logging dose, timing, injection site, concomitant factors, and observed responses is the foundation of long-term {name} research. That log is what (1) lets you identify your individual response patterns, (2) helps assess whether side effects are dose-related, (3) informs protocol adjustments, (4) provides usable data when you need a healthcare provider's input."),
            ('A Decision Framework',
             f"Pulling it together: (1) Start at the low-to-mid end of published research doses. (2) Establish baseline. (3) Titrate gradually, watching individual response. (4) Identify your individual optimal window. (5) Document everything. (6) Re-evaluate periodically. Dosing is fundamentally a personalized research process, not a generic prescription."),
        ]

    if angle in ('safety', 'side-effects'):
        return [
            (f'{name} Safety: An Honest Review', c['safety']),
            ('Understanding Side Effects Through Mechanism', c['mechanism']),
            ('Contraindications and Drug Interactions',
             f"With {name}, the contraindications you'll see most often: known or suspected malignancy (especially compounds touching proliferative pathways), severe uncontrolled endocrine disease, pregnancy or breastfeeding, children unless approved, severe hepatic or renal impairment. Drug interactions usually need a healthcare provider's review — particularly where {name}'s metabolism overlaps with existing prescription regimens."),
            ('How Dose Relates to Side Effects',
             f"Side effects with {name} are typically dose-related: at low doses they're rare, at moderate doses you'll see some incidence but usually mild, at high doses both incidence and severity climb together. Starting at the minimum effective dose is the single most effective adverse event reduction strategy."),
            ('Monitoring Strategy',
             f"For longer {name} research protocols, a structured monitoring approach: (1) Baseline assessment — relevant biomarkers, symptom severity, target functional measures. (2) Periodic labs based on the compound's mechanism (GH-pathway compounds need IGF-1 and glucose; GLP-1 class needs HbA1c and liver/kidney function; the specifics vary). (3) Symptom tracking — structured records, not memory. (4) Adverse event documentation when relevant."),
            ('When to Stop Immediately',
             f"Symptoms that warrant immediate cessation of {name}: any allergic reaction signs (rash, breathing difficulty, facial swelling); persistent severe headache or vision changes; serious GI events (persistent vomiting, severe abdominal pain); cardiovascular symptoms (chest pain, palpitations); any clearly new symptom outside the expected side effect profile. Stop and seek medical evaluation."),
            ('Risk Mitigation Principles',
             f"Practical risk mitigation for {name}: (1) Lowest effective dose. (2) Gradual titration. (3) Baseline monitoring. (4) Document changes. (5) Maintain a healthcare provider relationship. (6) Understand contraindications proactively, not after something goes wrong."),
            ('Individual Risk Profiling',
             f"Your individual risk profile with {name} depends on age, existing conditions (especially malignancy, endocrine, cardiovascular history), concomitant medications, allergy history, family history, and lifestyle factors. These combine to shape risk that goes beyond the compound's average safety profile."),
        ]

    if angle == 'faq':
        return [
            (f'{name} Frequently Asked Questions', f"What follows are the questions about {name} that come up most often in research-community discussions, with answers based on published literature and known mechanisms."),
            (f'What is {name}, exactly?', c['overview']),
            (f'What dose is typical in research protocols?', c['dosing']),
            (f'How does {name} actually work?', c['mechanism']),
            (f'What are the main safety considerations?', c['safety']),
            (f'How strong is the evidence base?', c['evidence']),
            (f'Is {name} FDA-approved?',
             f"Depends on the compound. A few peptides in the broader landscape are FDA-approved (semaglutide, tirzepatide, tesamorelin, setmelanotide), but most research peptides aren't — they're sold as 'research chemicals,' for laboratory use only, not human consumption. The 503A versus 503B compounding pharmacy distinction also matters: 503A facilities can compound with a physician's prescription, 503B can serve broader markets but with stricter GMP requirements. Regulatory status changes — verify current rules before starting any protocol."),
            (f'How does {name} compare to similar compounds?',
             f"The differences between {name} and related research compounds usually come down to: (1) mechanism — receptor type, signaling pathway differences; (2) half-life and dosing frequency; (3) side effect profile; (4) strength of the evidence base; (5) cost and availability." +
             (f" The most common comparisons you'll encounter are with {rel_links}." if related else "")),
            (f'What should I do before starting research with {name}?',
             f"Responsible preparation: (1) Read 5-10 peer-reviewed papers to build mechanism understanding. (2) Define your specific research question and measurable endpoints. (3) Establish baseline measurements — relevant biomarkers, symptom scales, performance metrics. (4) Verify supplier quality with third-party HPLC and batch-specific CoA. (5) Plan your titration approach. (6) Establish a healthcare provider relationship for monitoring. (7) Set up an adverse event response plan."),
            (f'When should I stop using {name}?',
             f"Stop {name} for: any allergic reaction signs, serious side effects, achieving research endpoint, side effects exceeding cumulative benefit, new contraindications (pregnancy, new malignancy diagnosis, new disease), healthcare provider advice, or quality issues with the compound batch. Stopping should generally be gradual rather than abrupt — some pathways need washout periods, and abrupt cessation can produce rebound effects."),
            (f'Is long-term use of {name} safe?',
             f"Honest answer: long-term safety data for {name} is generally limited. Most studies run under 12 weeks. The plausible long-term concerns include receptor downregulation/desensitization, metabolic adaptation, unknown cumulative effects, evolving regulatory status, and quality issues over multiple supplier batches. Responsible long-term use needs periodic medical evaluation, biomarker monitoring, periodic 'rest' cycles, and ongoing risk-benefit reassessment."),
        ]

    if angle == 'mechanism' or angle.startswith('how-it-works'):
        return [
            (f'How {name} Works: The Mechanism Story', c['mechanism']),
            (f'What {name} Is', c['overview']),
            ('Downstream Pathway Effects',
             f"The initial signaling cascade {name} triggers usually produces a much broader cellular response — gene expression changes, protein synthesis modulation, cross-talk with other systems. That amplification is part of why relatively small peptide doses can produce significant biological effects."),
            ('Where the Mechanism Evidence Comes From', c['evidence']),
            ('From Molecular Mechanism to Clinical Effect',
             f"The translation from 'mechanism in cells' to 'effect in humans' is where most peptide research falls down. Mechanism evidence describes what {name} *can* do; clinical evidence describes what it *does* in specific contexts. The gap is filled by dose, route, individual variation, and concomitant factors. Understanding this gap is part of reading peptide literature critically."),
            ('Methodological Limits of Mechanism Studies',
             f"Most {name} mechanism evidence comes from in vitro (cell culture) or animal models. The limits: simplification of human physiology, dose and route differences, metabolic and pharmacokinetic differences, disease-model versus actual-pathology relevance. Mechanism work is necessary but not sufficient."),
            ('How Mechanism Guides Dosing',
             f"Mechanism understanding directly informs dose decisions for {name}: receptor agonists hit ceilings (saturable response); enzyme inhibitors may show bell-shaped dose-response; metabolic regulators have optimal doses dependent on baseline metabolic state. Mechanism-driven dosing is more precise than empirical 'standard dose' assumptions."),
            ('Mechanism and Safety Implications', c['safety']),
            ('Future Mechanism Research',
             f"Where {name} mechanism research is going: more detailed downstream pathway mapping, individual genetic variation effects (pharmacogenomics), interactions with other compounds, and long-term adaptations (receptor downregulation, epigenetic changes)."),
        ]

    if angle == 'research' or angle == 'reviews':
        return [
            (f'{name} Research Review: Where the Evidence Stands', f"This section synthesizes published {name} literature, focusing on study design rigor, effect sizes, and external validity."),
            ('Key Studies and Findings', c['evidence']),
            ('Mechanism Research Summary', c['mechanism']),
            ('Quality Distribution Across Studies',
             f"{name} research quality varies widely — from rigorous RCTs through small open-label trials, case reports, and anecdotes. The hierarchy you should weight findings by: double-blind RCTs > open-label RCTs > cohort studies > case series > anecdotes."),
            ('Recurring Themes',
             f"Themes that recur in {name} reviews: (1) Mechanism evidence is often strong while clinical evidence is weaker — that gap from animal-effect to human-clinical-endpoint is everywhere. (2) Short-term studies dominate; long-term data is mostly absent. (3) Individual response variation is large — population averages obscure substantial individual differences. (4) Independent replication is often missing — many key findings come from single labs."),
            ('Methodological Limits',
             f"Limits affecting {name} research base: small sample sizes (most N<100), limited study duration (<12 weeks), insufficient independent replication, patient selection biases, subjective endpoint measurement. These limits affect both evidence strength and how far you can extrapolate findings."),
            ('Publication Bias Considerations',
             f"Publication bias in peptide research is real — positive results publish more easily, trials that miss endpoints often don't surface. The published {name} literature may overstate true effect sizes. Cochrane-style systematic review methods (meta-analysis, funnel plots) are designed to detect this."),
            ('Future Research Priorities',
             f"What {name} research needs: (1) Long-term RCTs (≥1 year). (2) Dose-optimization studies. (3) Subgroup-specific response patterns. (4) Interaction studies with other interventions. (5) Independent replication of key findings. (6) Real-world evidence collection."),
            ('What This Means for Practical Decisions',
             f"For decisions about {name} research: understand the differences in evidence strength, avoid treating animal or mechanism evidence as clinically equivalent, maintain realistic expectations. Decisions should rest on published evidence + individual response monitoring, not single sources."),
        ]

    if angle.startswith('comparison:'):
        target = angle.split(':', 1)[1]
        target_label = target.replace('-', ' ').title() if target != 'alternatives' else 'alternatives'
        return [
            (f'{name} vs {target_label}: A Side-by-Side Look', f"This isn't about declaring a winner — most compound comparisons matter context-by-context. The goal is to clarify the differences, the trade-offs, and which contexts favor which choice."),
            (f'What {name} Is', c['overview']),
            ('Mechanism Differences', c['mechanism']),
            (f'Key Differences from {target_label}',
             f"{name} and {target_label} typically differ across several dimensions: (1) mechanism — receptor types, signaling pathways; (2) dosing and frequency — half-life affects schedule; (3) evidence base strength — RCT data versus animal models; (4) side effect profile — different mechanisms, different side effects; (5) cost and availability; (6) regulatory status. The specific differences depend on which compounds you're comparing."),
            ('Evidence Base Comparison', c['evidence']),
            ('Side Effect Profile Comparison', c['safety']),
            ('Practical Application Differences',
             f"{name} versus {target_label} can favor different choices in different contexts: short-term versus long-term applications (half-life and receptor downregulation matter), specific subgroups (age, sex, comorbidities), availability (approval status, sourcing), individual response (genetic variation, concomitant factors)."),
            ('A Decision Framework',
             f"To choose between {name} and {target_label}: (1) which compound's evidence base better matches your specific research question; (2) mechanism alignment with target pathology; (3) side effect risk tolerance versus the compound's profile; (4) practical feasibility — availability, cost, dosing complexity; (5) individual response — actual response data after 4 weeks often beats theoretical comparison."),
            ('Combined Use Considerations',
             f"In some contexts {name} and {target_label} are synergistic rather than substitutes — depending on whether mechanisms are complementary. Combined use needs careful evaluation: predictability of interactions, cumulative side effects, dose adjustment complexity. Establishing baseline response from a single compound first is responsible practice."),
            ('Limits of This Comparison',
             f"Comparison limits: (1) direct {name} vs {target_label} studies are rare; (2) individual response variability is high; (3) study quality and endpoint differences make comparison difficult; (4) 'best' is highly individualized."),
            ('Bottom Line',
             f"{name} versus {target_label} isn't a 'which is better' question — it's 'which is better for *your* research question.' Identify the goal, evaluate the evidence base for both, consider individual factors, and be ready to adjust based on actual response."),
        ]

    if angle == 'stacking':
        return [
            (f'Stacking {name}: Why and How', f"Stacking — using {name} alongside other compounds — is a common research and anecdotal approach. The theoretical case rests on synergy, complementary mechanisms, or combined effects. The practical case has more caveats."),
            (f'Why Stack {name}?', f"Common reasons researchers stack {name}: (1) synergistic mechanisms — different pathways activated together producing more than the sum of single-agent effects; (2) side effect mitigation — one compound counters another's side effects; (3) duration extension — short-acting and long-acting compounds combined for stable levels; (4) target coverage — multiple related targets simultaneously; (5) reducing tolerance and desensitization."),
            ('Mechanism as Foundation', c['mechanism']),
            ('Common Stacking Patterns',
             f"{rel_links} are the most-cited stacking partners for {name} in research literature." if related else
             f"{name} stacking patterns vary substantially based on the research target."),
            ('Synergy Versus Antagonism',
             f"Real synergy with {name} stacks requires (1) mechanism complementarity — different pathways or different steps in the same pathway; (2) animal or human evidence supporting the combination; (3) doses chosen to enable synergy; (4) side effects that don't compound disproportionately. Antagonism (one compound suppressing another) also happens — mechanism understanding helps avoid that trap."),
            ('Practical Stacking Principles',
             f"Practical wisdom for {name} stacks: (1) start single-agent to establish baseline response — you need to know each compound's individual effect. (2) Introduce new compounds one at a time, not several at once — this preserves attribution. (3) Monitor each addition. (4) Document everything. (5) Keep it simple — interactions in 3+ compound stacks compound exponentially."),
            ('Stacking Risks',
             f"Risks with {name} stacking: (1) interactions aren't fully predictable from mechanism alone; (2) cumulative side effects can amplify; (3) dose adjustments become complex; (4) attributing side effects to the right compound becomes harder; (5) economic and time burden grows. Most failed stacks fail on these practical points, not on mechanism."),
            ('Monitoring Stacked Protocols',
             f"Monitoring {name} stacks: (1) extend baseline measurements to cover all relevant biomarkers; (2) single-compound 4-6 weeks first to establish response; (3) add new compounds one at a time; (4) leave 2-4 weeks between additions; (5) re-evaluate periodically — long-term stacks may stop outperforming single agents."),
            ('When to Simplify or Stop',
             f"Reasons to simplify or stop a {name} stack: side effects exceed marginal benefit; cost-benefit shifts; new contraindications; single-compound shows enough on re-evaluation; interaction issues. Simplify one compound at a time so you can attribute the effect of removing it."),
            ('Single-Agent Optimization First',
             f"For many applications, optimized single-agent protocols beat complex stacks — better evidence base, easier side effect attribution, simpler dose adjustment. Optimize {name} as a single compound (best dose, best frequency, best concomitants) before adding others."),
            ('Bottom Line',
             f"{name} stacking decision framework: (1) optimize single-agent first; (2) add new compounds with clear mechanism rationale; (3) introduce one at a time; (4) monitor strictly; (5) keep it simple; (6) be ready to simplify or stop. Complex stacks aren't necessarily better — they often add risk faster than benefit."),
        ]

    # Default fallback for any aspect not specifically handled
    return [
        (f'What is {name}?', c['overview']),
        ('Mechanism', c['mechanism']),
        ('Research Evidence', c['evidence']),
        ('Dosing Considerations', c['dosing']),
        ('Safety', c['safety']),
        ('Related Research Directions', f"Compounds often discussed alongside {name}: {rel_links}." if related else f"{name} fits in the broader {cat.lower()} research landscape."),
    ]


def build_quick_answer(c, slug):
    base = c.get('quick_answer') or c['overview'][:300]
    if len(base) < 200:
        addition = f' Mechanism: {c["mechanism"][:120]}. Dosing: {c["dosing"][:80]}.'
        base = base + addition
    if len(base) > 320:
        base = base[:320].rsplit('.', 1)[0] + '.'
    return base


def build_faq_schema(c, paragraphs):
    name = c['name']
    qa = []
    for h2, p in paragraphs:
        if 'Q:' in h2 or '?' in h2:
            qa.append((h2, p))
    if len(qa) < 3:
        qa = [
            (f'What is {name}?', c['overview'][:400]),
            (f'How does {name} work?', c['mechanism'][:400]),
            (f'What are typical research doses for {name}?', c['dosing'][:400]),
            (f'What are the main safety considerations?', c['safety'][:400]),
            (f'Is {name} FDA-approved?', 'FDA approval status depends on the specific compound. Most research peptides are not FDA-approved for human use and are sold as research chemicals for laboratory use only. Some peptides in the broader landscape (semaglutide, tirzepatide, tesamorelin, setmelanotide) are FDA-approved.'),
        ]
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa[:6]
        ]
    }


def build_article_body(slug, title_en, original_qa):
    compound_key, aspect_key = parse_slug(slug)

    if compound_key == '__SKIP__':
        return None, None

    c = COMPOUNDS.get(compound_key)
    if not c:
        # Generic fallback for unknown compound — humanized voice
        name_guess = re.sub(r'[\|\—\-].*$', '', title_en).strip() or slug.replace('-', ' ').title()
        c = {
            'name': name_guess,
            'category': 'research peptide',
            'related': RELATED_MAP.get(compound_key, []),
            'overview': f"{name_guess} is a research compound investigated in the broader peptide research landscape. The available literature covers mechanism, applications, dosing, and safety — though the depth varies considerably depending on commercial interest and clinical development history.",
            'mechanism': f"{name_guess}'s mechanism involves specific cellular pathways and signaling cascades. Like most peptide-class compounds, the effects come from receptor agonism, enzyme modulation, or gene expression regulation — the specifics depend on the compound's structure.",
            'evidence': f"The published evidence base for {name_guess} includes preclinical research (cell culture, animal models) and human data of varying quality. Sample sizes, study durations, and replication track records differ substantially across studies.",
            'dosing': f"Research-protocol doses for {name_guess} reported in the literature vary by endpoint and population. Subcutaneous injection is the most common administration route for peptides in this class.",
            'safety': f"The {name_guess} safety profile has to be evaluated in context — known effects, individual risk factors, and regulatory status all matter.",
            'quick_answer': f"{name_guess} is a research-class peptide compound. The mechanism involves specific cellular pathways. Research doses and protocols vary by endpoint. Safety data is limited; most research peptides are not FDA-approved for human use and are sold as research chemicals for laboratory use only.",
        }

    if aspect_key and ':' in aspect_key:
        angle = aspect_key
    else:
        angle = aspect_key or 'general'

    paragraphs = aspect_paragraphs(angle, c)
    quick_answer = build_quick_answer(c, slug)
    faq_schema = build_faq_schema(c, paragraphs)

    html = '<article class="article-body">'
    html += '<div style="background:#fef2f2;border:1px solid #fecaca;border-radius:10px;padding:20px 24px;margin:24px 0;font-size:13px;color:#991b1b;"><p style="font-weight:700;">Medical Disclaimer</p><p>This article is for informational and educational purposes only. The compounds discussed are research chemicals that are not FDA-approved for human use. Always consult a licensed healthcare professional before considering any peptide protocol.</p></div>'
    html += f'<div class="quick-answer"><strong>Quick Answer:</strong> {quick_answer}</div>'
    for h2, p in paragraphs:
        html += f'<h2>{h2}</h2>\n<p>{p}</p>\n'

    related = c.get('related', [])
    if related:
        html += '<h2>Related Research Compounds</h2>\n<p>If you\'re researching ' + c['name'] + ', the compounds you\'ll likely want to look at next are: '
        link_parts = []
        for rk in related[:6]:
            if rk in COMPOUNDS:
                link_parts.append(f'<a href="/en/{rk}-guide.html">{COMPOUNDS[rk]["name"]}</a>')
            else:
                link_parts.append(f'<a href="/en/{rk}-guide.html">{rk.replace("-", " ").upper()}</a>')
        html += ', '.join(link_parts) + '. These appear most often in the same research contexts as alternatives or complementary compounds.</p>'

    html += '<h2>References and Regulatory Notes</h2>\n'
    html += f'<p>This guide synthesizes published research literature on {c["name"]}. Specific citations are referenced inline where relevant. Research-compound regulatory status varies by jurisdiction; most are not approved by the FDA or equivalent agencies for human use and should be used only in research contexts compliant with applicable ethical review and regulations. This content is for research reference purposes only and does not constitute medical advice.</p>\n'
    html += '</article>'
    return html, faq_schema


def needs_rewrite(html):
    """Check if file is a thin stub needing full rewrite."""
    boilerplate_markers = [
        'Section 1 Content for section',
        'Section One Information about this section',
        'Information about this section with practical details',
        'comprehensive guide covering all aspects',
    ]
    m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if not m:
        return False
    text = re.sub(r'<[^>]+>', ' ', m.group(1))
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) < 2500:
        return True
    if any(bp in text for bp in boilerplate_markers):
        return True
    return False


def needs_faq_injection(html):
    """Check if file is missing FAQ schema."""
    return 'FAQPage' not in html


def process_file(path, mode='auto'):
    """Process /en/ file. Mode:
       'auto' — full rewrite if thin, else just inject FAQ if missing
       'rewrite' — always full rewrite
       'faq-only' — only inject FAQ schema, never rewrite body
    """
    html = path.read_text(encoding='utf-8')
    slug = path.stem

    # Skip utility pages
    compound_key, _ = parse_slug(slug)
    if compound_key == '__SKIP__':
        return False, 'skip'

    # Check if rewrite is needed
    if mode == 'auto':
        do_rewrite = needs_rewrite(html)
    elif mode == 'rewrite':
        do_rewrite = True
    elif mode == 'faq-only':
        do_rewrite = False
    else:
        do_rewrite = False

    new_html = html
    actions = []

    if do_rewrite:
        m_title = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
        title_en = m_title.group(1).strip() if m_title else path.stem
        m_desc = re.search(r'<meta\s+content="([^"]*)"\s+name="description"', html)
        if not m_desc:
            m_desc = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
        qa_en = m_desc.group(1).strip() if m_desc else ''

        new_article, faq_schema = build_article_body(slug, title_en, qa_en)
        if new_article:
            pat_a = re.compile(r'(<article[^>]*>)(.*?)(</article>)', re.DOTALL)
            if pat_a.search(new_html):
                new_html = pat_a.sub(lambda _: new_article, new_html, count=1)
                actions.append('rewrote-body')
            if faq_schema and 'FAQPage' not in new_html:
                s = f'<script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>'
                new_html = new_html.replace('</head>', s + '\n</head>', 1)
                actions.append('added-faq')

    # FAQ injection mode (or auto without rewrite)
    if not do_rewrite and needs_faq_injection(new_html):
        # Try to extract title and quick-answer to build minimal FAQ
        compound_key, _ = parse_slug(slug)
        c = COMPOUNDS.get(compound_key)
        if c:
            faq_schema = build_faq_schema(c, [])
            s = f'<script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>'
            new_html = new_html.replace('</head>', s + '\n</head>', 1)
            actions.append('added-faq')

    if new_html == html:
        return False, 'no-change'

    path.write_text(new_html, encoding='utf-8')
    return True, '+'.join(actions)


def main():
    mode = os.environ.get('MODE', 'auto')
    list_path = os.environ.get('FILE_LIST', None)

    if list_path and os.path.exists(list_path):
        files = [EN_DIR / l.strip() for l in open(list_path) if l.strip()]
    else:
        files = sorted(EN_DIR.glob('*.html'))

    counts = {'rewrote-body': 0, 'added-faq': 0, 'rewrote-body+added-faq': 0,
              'no-change': 0, 'skip': 0}
    fixed = errors = 0
    for path in files:
        if not path.exists():
            counts['no-change'] += 1
            continue
        try:
            changed, action = process_file(path, mode=mode)
            counts[action] = counts.get(action, 0) + 1
            if changed:
                fixed += 1
        except Exception as e:
            errors += 1
            print(f"ERR {path.name}: {e}", file=sys.stderr)

    print(f"\n=== EN v2 summary (mode={mode}) ===")
    print(f"  Total: {len(files)}")
    print(f"  Fixed: {fixed}")
    print(f"  Errors: {errors}")
    for k, v in sorted(counts.items()):
        if v > 0:
            print(f"    {k}: {v}")


if __name__ == '__main__':
    main()
