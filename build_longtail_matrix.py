#!/usr/bin/env python3
"""
Build long-tail keyword matrix for WolveStack.
Generates highly specific, low-competition article targets.

Categories:
1. Peptide + specific injury/body part
2. Peptide + drug/supplement interaction
3. Peptide + practical micro-questions
4. Peptide + specific side effect concerns
5. Peptide + vs mainstream treatment
6. Peptide + lifestyle/demographic
"""

import json, csv, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Only target peptides with real search volume for long-tail
# Tier 1: Highest search volume peptides
TIER1_PEPTIDES = [
    "BPC-157", "TB-500", "Semaglutide", "Tirzepatide", "MK-677",
    "CJC-1295", "Ipamorelin", "GHK-Cu", "PT-141", "Melanotan II",
]

# Tier 2: Moderate search volume
TIER2_PEPTIDES = [
    "Sermorelin", "Tesamorelin", "AOD-9604", "Retatrutide", "Epithalon",
    "Selank", "Semax", "NAD+", "GHRP-6", "GHRP-2", "Thymosin Alpha-1",
    "IGF-1 LR3", "LL-37", "MOTS-C", "Noopept", "5-Amino-1MQ",
]

# Tier 3: Niche / lower volume
TIER3_PEPTIDES = [
    "Dihexa", "KPV", "Kisspeptin", "SS-31", "Hexarelin", "DSIP",
    "Cerebrolysin", "Melanotan I", "Oxytocin", "PE-22-28", "Pinealon",
    "BPC-157 + TB-500",  # stack combo
    "CJC-1295 + Ipamorelin",  # stack combo
]

# =================================================================
# CATEGORY 1: Peptide + Specific Injury/Body Part
# =================================================================
INJURIES_BY_PEPTIDE = {
    "BPC-157": [
        "rotator cuff", "achilles tendon", "knee injury", "meniscus tear",
        "tennis elbow", "plantar fasciitis", "herniated disc", "ACL tear",
        "shoulder injury", "back pain", "hip pain", "wrist injury",
        "ankle sprain", "golfers elbow", "carpal tunnel", "shin splints",
        "torn labrum", "hamstring tear", "quad tear", "muscle tear",
        "ligament damage", "nerve damage", "ulcer", "IBS",
        "leaky gut", "gastritis", "colitis", "GERD",
        "tendonitis", "bursitis", "arthritis", "post surgery",
    ],
    "TB-500": [
        "rotator cuff", "achilles tendon", "knee injury", "meniscus tear",
        "tennis elbow", "muscle tear", "hamstring injury", "shoulder injury",
        "back injury", "ankle sprain", "ligament injury", "post surgery",
        "tendonitis", "hair loss", "wound healing", "cardiac injury",
        "joint pain", "flexibility", "scar tissue",
    ],
    "GHK-Cu": [
        "wrinkles", "acne scars", "hair loss", "hair thinning",
        "wound healing", "skin aging", "sun damage", "stretch marks",
        "dark spots", "fine lines", "collagen loss", "surgical scars",
    ],
    "Semaglutide": [
        "type 2 diabetes", "PCOS weight gain", "insulin resistance",
        "metabolic syndrome", "fatty liver", "NAFLD",
        "binge eating", "emotional eating",
    ],
    "MK-677": [
        "muscle wasting", "bone density", "insomnia", "poor appetite",
        "growth hormone deficiency",
    ],
}

# =================================================================
# CATEGORY 2: Peptide + Drug/Supplement Interaction
# =================================================================
INTERACTIONS = {
    "BPC-157": [
        "ibuprofen", "NSAIDs", "alcohol", "antibiotics", "aspirin",
        "creatine", "prednisone", "cortisone", "testosterone", "HGH",
        "metformin", "omeprazole", "CBD",
    ],
    "Semaglutide": [
        "metformin", "alcohol", "birth control", "insulin", "ozempic",
        "levothyroxine", "antidepressants", "berberine", "phentermine",
        "coffee", "ibuprofen", "antibiotics", "Wellbutrin",
    ],
    "Tirzepatide": [
        "metformin", "alcohol", "insulin", "birth control",
        "levothyroxine", "semaglutide", "phentermine",
    ],
    "MK-677": [
        "creatine", "alcohol", "melatonin", "testosterone", "HGH",
        "caffeine", "ashwagandha", "GABA",
    ],
    "CJC-1295": [
        "alcohol", "melatonin", "HGH", "testosterone", "creatine",
    ],
    "Ipamorelin": [
        "alcohol", "melatonin", "HGH", "CJC-1295", "GHRP-6",
    ],
    "TB-500": [
        "BPC-157", "HGH", "alcohol", "NSAIDs", "testosterone",
    ],
    "PT-141": [
        "viagra", "cialis", "alcohol", "blood pressure medication",
    ],
    "Melanotan II": [
        "alcohol", "sunscreen", "antihistamines",
    ],
}

# =================================================================
# CATEGORY 3: Practical Micro-Questions
# =================================================================
MICRO_QUESTIONS = {
    "BPC-157": [
        ("where to inject for {condition}", ["shoulder", "knee", "elbow", "gut", "back", "hip", "ankle"]),
        ("morning or night", []),
        ("how long to see results", []),
        ("can you take orally", []),
        ("subcutaneous vs intramuscular", []),
        ("how much bacteriostatic water to add", []),
        ("how many times a day", []),
        ("empty stomach or with food", []),
        ("how long does a vial last", []),
        ("can you travel with", []),
        ("does it need to be refrigerated", []),
    ],
    "Semaglutide": [
        ("how long to see weight loss results", []),
        ("what to eat while on", []),
        ("best injection site", []),
        ("when to take", []),
        ("how to deal with nausea", []),
        ("plateau what to do", []),
        ("how to store pen", []),
        ("can you drink alcohol", []),
        ("does it cause hair loss", []),
        ("how long can you stay on", []),
        ("what happens when you stop", []),
        ("does it affect fertility", []),
    ],
    "MK-677": [
        ("morning or night", []),
        ("does it cause cancer", []),
        ("water retention how to reduce", []),
        ("does it increase cortisol", []),
        ("blood sugar concerns", []),
        ("how long to see results", []),
        ("with or without food", []),
        ("does it affect testosterone", []),
    ],
    "Tirzepatide": [
        ("how long to see results", []),
        ("best injection site", []),
        ("what to eat while on", []),
        ("what happens when you stop", []),
        ("does it affect fertility", []),
        ("nausea how long does it last", []),
    ],
    "TB-500": [
        ("where to inject for {condition}", ["knee", "shoulder", "elbow"]),
        ("how long to see results", []),
        ("loading phase explained", []),
    ],
    "CJC-1295": [
        ("best time to inject", []),
        ("with or without DAC", []),
        ("does it cause cancer", []),
    ],
    "Ipamorelin": [
        ("best time to inject", []),
        ("does it increase cortisol", []),
        ("how long to see results", []),
    ],
    "GHK-Cu": [
        ("topical vs injectable", []),
        ("how to use for hair", []),
        ("how to use for face", []),
        ("microneedling with", []),
    ],
    "PT-141": [
        ("how long does it last", []),
        ("how fast does it work", []),
        ("can women use", []),
        ("how often can you use", []),
    ],
}

# =================================================================
# CATEGORY 4: Specific Side Effect Concerns
# =================================================================
SIDE_EFFECT_QUERIES = {
    "Semaglutide": [
        "hair loss", "nausea", "constipation", "diarrhea", "fatigue",
        "pancreatitis", "thyroid cancer", "gallbladder problems",
        "muscle loss", "face aging", "ozempic face",
        "gastroparesis", "stomach paralysis", "depression",
    ],
    "Tirzepatide": [
        "nausea", "hair loss", "pancreatitis", "muscle loss",
        "constipation", "fatigue",
    ],
    "MK-677": [
        "water retention", "blood sugar", "insulin resistance",
        "numbness tingling", "increased appetite", "lethargy",
        "carpal tunnel",
    ],
    "BPC-157": [
        "cancer risk", "tumor growth", "anxiety", "insomnia",
        "headache", "nausea", "dizziness",
    ],
    "Melanotan II": [
        "nausea", "facial flushing", "moles darkening",
        "unwanted erections", "freckles",
    ],
    "PT-141": [
        "nausea", "headache", "flushing", "blood pressure",
    ],
    "GHRP-6": [
        "extreme hunger", "cortisol increase", "water retention",
    ],
}

# =================================================================
# CATEGORY 5: Peptide vs Mainstream Treatment
# =================================================================
VS_TREATMENTS = {
    "BPC-157": [
        "cortisone injection", "PRP therapy", "stem cell therapy",
        "physical therapy alone", "surgery",
    ],
    "Semaglutide": [
        "ozempic", "mounjaro", "wegovy", "phentermine",
        "gastric sleeve", "lap band", "metformin for weight loss",
        "saxenda", "contrave",
    ],
    "Tirzepatide": [
        "semaglutide", "ozempic", "wegovy", "mounjaro",
        "gastric sleeve", "phentermine",
    ],
    "MK-677": [
        "HGH injections", "sermorelin", "ipamorelin",
        "natural growth hormone boosters",
    ],
    "GHK-Cu": [
        "retinol", "vitamin C serum", "hyaluronic acid",
        "microneedling alone", "botox",
    ],
    "PT-141": [
        "viagra", "cialis", "levitra", "supplements for ED",
    ],
    "Melanotan II": [
        "spray tan", "tanning beds", "DHA self tanner",
    ],
    "TB-500": [
        "BPC-157", "PRP therapy", "stem cell therapy",
        "cortisone injection",
    ],
}

# =================================================================
# CATEGORY 6: Lifestyle/Demographic Long-tails
# =================================================================
LIFESTYLE_QUERIES = [
    # Format: (peptide, demographic/context)
    ("BPC-157", "for dogs"),
    ("BPC-157", "for cats"),
    ("BPC-157", "for horses"),
    ("BPC-157", "for athletes"),
    ("BPC-157", "for bodybuilders"),
    ("BPC-157", "for runners"),
    ("BPC-157", "for crossfit"),
    ("BPC-157", "for elderly"),
    ("BPC-157", "while breastfeeding"),
    ("BPC-157", "after surgery"),
    ("TB-500", "for dogs"),
    ("TB-500", "for horses"),
    ("TB-500", "for athletes"),
    ("TB-500", "for bodybuilders"),
    ("Semaglutide", "for PCOS"),
    ("Semaglutide", "for teenagers"),
    ("Semaglutide", "over 60"),
    ("Semaglutide", "with hypothyroidism"),
    ("Semaglutide", "while breastfeeding"),
    ("Semaglutide", "for athletes"),
    ("Semaglutide", "for emotional eating"),
    ("Semaglutide", "for binge eating disorder"),
    ("Semaglutide", "without diabetes"),
    ("Tirzepatide", "for PCOS"),
    ("Tirzepatide", "over 60"),
    ("Tirzepatide", "for non diabetics"),
    ("MK-677", "for athletes over 40"),
    ("MK-677", "for bodybuilders"),
    ("MK-677", "for sleep"),
    ("MK-677", "for elderly"),
    ("Ipamorelin", "for athletes"),
    ("Ipamorelin", "for anti-aging"),
    ("Ipamorelin", "for bodybuilders"),
    ("GHK-Cu", "for hair loss men"),
    ("GHK-Cu", "for hair loss women"),
    ("GHK-Cu", "for acne scars"),
    ("GHK-Cu", "after microneedling"),
    ("PT-141", "for women"),
    ("PT-141", "for men over 50"),
    ("Selank", "for social anxiety"),
    ("Selank", "for PTSD"),
    ("Semax", "for ADHD"),
    ("Semax", "for studying"),
    ("NAD+", "for anti-aging"),
    ("NAD+", "for chronic fatigue"),
    ("NAD+", "for addiction recovery"),
    ("Epithalon", "for longevity"),
    ("MOTS-C", "for diabetes"),
    ("MOTS-C", "for weight loss"),
    ("5-Amino-1MQ", "for stubborn belly fat"),
    ("LL-37", "for Lyme disease"),
    ("LL-37", "for mold illness"),
    ("Thymosin Alpha-1", "for cancer support"),
    ("Thymosin Alpha-1", "for long COVID"),
    ("DSIP", "for insomnia"),
    ("DSIP", "for shift workers"),
    ("Retatrutide", "vs semaglutide"),
    ("Retatrutide", "vs tirzepatide"),
]


def slugify(text):
    import re
    return re.sub(r'[^a-z0-9-]', '', text.lower().replace(' ', '-').replace('+', '-plus'))


def build_matrix():
    articles = []
    existing_filenames = set()

    # Load existing articles to avoid duplicates
    existing_file = os.path.join(SCRIPT_DIR, "new-articles-todo.json")
    if os.path.exists(existing_file):
        with open(existing_file) as f:
            for a in json.load(f):
                existing_filenames.add(a["filename"])

    def add_article(filename, title, keyword, peptide, category, article_type, tier, vendors=""):
        if filename in existing_filenames:
            return
        existing_filenames.add(filename)
        articles.append({
            "filename": filename,
            "title": title,
            "primary_keyword": keyword,
            "peptide": peptide,
            "category": category,
            "type": article_type,
            "tier": tier,
            "vendors": vendors,
        })

    # Determine category from peptide
    def cat_for(peptide):
        cats = {
            "BPC-157": "Healing", "TB-500": "Healing", "GHK-Cu": "Longevity", "GHK": "Longevity",
            "Semaglutide": "Weight Loss", "Tirzepatide": "Weight Loss", "Retatrutide": "Weight Loss",
            "AOD-9604": "Weight Loss", "5-Amino-1MQ": "Weight Loss", "Setmelanotide": "Weight Loss",
            "CJC-1295": "Growth Hormone", "Ipamorelin": "Growth Hormone", "Sermorelin": "Growth Hormone",
            "MK-677": "Growth Hormone", "GHRP-2": "Growth Hormone", "GHRP-6": "Growth Hormone",
            "Hexarelin": "Growth Hormone", "Tesamorelin": "Growth Hormone", "IGF-1 LR3": "Growth Hormone",
            "Epithalon": "Longevity", "NAD+": "Longevity", "MOTS-C": "Longevity", "SS-31": "Longevity",
            "Selank": "Cognitive", "Semax": "Cognitive", "Noopept": "Cognitive", "Dihexa": "Cognitive",
            "PT-141": "Sexual Health", "Kisspeptin": "Sexual Health", "Oxytocin": "Sexual Health",
            "Melanotan II": "Tanning", "Melanotan I": "Tanning",
            "Thymosin Alpha-1": "Immune", "LL-37": "Immune", "KPV": "Immune", "Thymalin": "Immune",
            "DSIP": "Sleep", "Pinealon": "Sleep",
        }
        return cats.get(peptide, "Research")

    def tier_for(peptide):
        if peptide in [p for p in TIER1_PEPTIDES]:
            return 1
        if peptide in TIER2_PEPTIDES:
            return 2
        return 3

    # --- CATEGORY 1: Peptide + Injury ---
    for peptide, injuries in INJURIES_BY_PEPTIDE.items():
        for injury in injuries:
            slug_p = slugify(peptide)
            slug_i = slugify(injury)
            fn = f"{slug_p}-for-{slug_i}.html"
            title = f"{peptide} for {injury.title()}: Research, Protocol & What to Expect"
            kw = f"{peptide} for {injury}"
            add_article(fn, title, kw, peptide, cat_for(peptide), "Condition-Specific", tier_for(peptide))

    # --- CATEGORY 2: Interactions ---
    for peptide, drugs in INTERACTIONS.items():
        for drug in drugs:
            slug_p = slugify(peptide)
            slug_d = slugify(drug)
            fn = f"{slug_p}-and-{slug_d}.html"
            title = f"{peptide} and {drug.title()}: Interactions, Safety & What to Know"
            kw = f"{peptide} and {drug}"
            add_article(fn, title, kw, peptide, cat_for(peptide), "Single Peptide", tier_for(peptide))

    # --- CATEGORY 3: Micro-Questions ---
    for peptide, questions in MICRO_QUESTIONS.items():
        for q_template, conditions in questions:
            if "{condition}" in q_template and conditions:
                for cond in conditions:
                    q = q_template.replace("{condition}", cond)
                    slug_p = slugify(peptide)
                    slug_q = slugify(q)
                    fn = f"{slug_p}-{slug_q}.html"
                    title = f"{peptide} {q.title()}: What You Need to Know"
                    kw = f"{peptide} {q}"
                    add_article(fn, title, kw, peptide, cat_for(peptide), "Single Peptide", tier_for(peptide))
            else:
                q = q_template
                slug_p = slugify(peptide)
                slug_q = slugify(q)
                fn = f"{slug_p}-{slug_q}.html"
                title = f"{peptide} {q.title()}: Complete Guide"
                kw = f"{peptide} {q}"
                add_article(fn, title, kw, peptide, cat_for(peptide), "Single Peptide", tier_for(peptide))

    # --- CATEGORY 4: Specific Side Effect Concerns ---
    for peptide, effects in SIDE_EFFECT_QUERIES.items():
        for effect in effects:
            slug_p = slugify(peptide)
            slug_e = slugify(effect)
            fn = f"{slug_p}-{slug_e}-risk.html"
            title = f"{peptide} and {effect.title()}: Risk, Research & How to Manage"
            kw = f"{peptide} {effect}"
            add_article(fn, title, kw, peptide, cat_for(peptide), "Single Peptide", tier_for(peptide))

    # --- CATEGORY 5: Vs Mainstream Treatment ---
    for peptide, treatments in VS_TREATMENTS.items():
        for treatment in treatments:
            slug_p = slugify(peptide)
            slug_t = slugify(treatment)
            fn = f"{slug_p}-vs-{slug_t}.html"
            title = f"{peptide} vs {treatment.title()}: Comparison, Pros & Cons"
            kw = f"{peptide} vs {treatment}"
            add_article(fn, title, kw, peptide, "Comparison", "Comparison", tier_for(peptide))

    # --- CATEGORY 6: Lifestyle/Demographic ---
    for peptide, demo in LIFESTYLE_QUERIES:
        slug_p = slugify(peptide)
        slug_d = slugify(demo)
        fn = f"{slug_p}-{slug_d}.html"
        title = f"{peptide} {demo.title()}: Safety, Dosing & Research Guide"
        kw = f"{peptide} {demo}"
        atype = "Comparison" if " vs " in demo else "Condition-Specific"
        add_article(fn, title, kw, peptide, cat_for(peptide), atype, tier_for(peptide))

    return articles


def main():
    articles = build_matrix()
    print(f"Generated {len(articles)} long-tail articles")

    # Save
    out_file = os.path.join(SCRIPT_DIR, "longtail-articles-todo.json")
    with open(out_file, 'w') as f:
        json.dump(articles, f, indent=2)

    # Also save CSV
    csv_file = os.path.join(SCRIPT_DIR, "longtail-keyword-matrix.csv")
    with open(csv_file, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=["filename","title","primary_keyword","peptide","category","type","tier","vendors"])
        w.writeheader()
        w.writerows(articles)

    # Stats
    from collections import Counter
    types = Counter(a["type"] for a in articles)
    tiers = Counter(a["tier"] for a in articles)
    cats = Counter(a["category"] for a in articles)
    print(f"\nBy type: {dict(types)}")
    print(f"By tier: {dict(tiers)}")
    print(f"By category: {dict(cats)}")

    # Show samples
    print(f"\nSample articles:")
    for a in articles[:10]:
        print(f"  {a['filename']} — {a['title'][:70]}")


if __name__ == "__main__":
    main()
