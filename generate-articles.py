#!/usr/bin/env python3
"""
WolveStack Article Generator Pipeline v2.0
Generates SEO-optimized HTML articles with ANGLE-SPECIFIC content.
Each article angle (dosage, side effects, stacking, etc.) gets its own
content builder that highlights the most relevant data.

Usage:
  python3 generate-articles.py [--batch N] [--tier T] [--type TYPE] [--dry-run] [--overwrite]
"""

import json, os, sys, re, html as html_mod
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MATRIX_FILE = os.path.join(SCRIPT_DIR, "new-articles-todo.json")
TEMPLATE_FILE = os.path.join(SCRIPT_DIR, "ARTICLE-TEMPLATE.html")
OUTPUT_DIR = SCRIPT_DIR
DATE_TODAY = datetime.now().strftime("%Y-%m-%d")

# Import the comprehensive knowledge base
sys.path.insert(0, SCRIPT_DIR)
from peptide_knowledge_base import PEPTIDE_DATA, DEFAULT_PEPTIDE_DATA

# Affiliate links
AFFILIATE_LINKS = {
    "Ascension": "https://www.ascensionresearch.co/?ref=wolvestack",
    "Particle": "https://particlepeptides.com/en/16-buy-peptides?refs=25135",
    "Limitless": "https://limitlesslifenootropics.com/?affid=10704",
    "Apollo": "https://apolloresearchcompounds.com/?rfsn=9022946",
}

# ============================================================
# ANGLE DETECTION — figure out what the article is about
# ============================================================
ANGLE_PATTERNS = [
    ("dosage", ["dosage", "dose", "protocol"]),
    ("benefits", ["benefits"]),
    ("side-effects", ["side-effects", "side effects", "safety"]),
    ("before-after", ["before-and-after", "before and after"]),
    ("results-timeline", ["results-timeline", "results timeline"]),
    ("half-life", ["half-life"]),
    ("reconstitution", ["reconstitution", "mixing"]),
    ("cycle", ["-cycle."]),
    ("stacking", ["stacking", "stack"]),
    ("beginners", ["for-beginners", "beginner"]),
    ("mechanism", ["how-it-works", "mechanism"]),
    ("research", ["-research."]),
    ("where-to-buy", ["where-to-buy"]),
    ("injection", ["injection-guide", "injection"]),
    ("women", ["for-women"]),
    ("men", ["for-men"]),
    ("reviews", ["reviews", "review"]),
    ("faq", ["-faq."]),
    ("storage", ["storage", "how-to-store"]),
    ("legal", ["-legal."]),
]

def detect_angle(filename, title):
    """Detect the article angle from filename and title."""
    fn = filename.lower()
    tl = title.lower()
    for angle, patterns in ANGLE_PATTERNS:
        for p in patterns:
            if p in fn or p in tl:
                return angle
    # Condition-specific detection
    for condition in ["healing", "weight-loss", "fat-loss", "muscle", "hair",
                      "anti-aging", "aging", "skin", "gut", "sleep", "brain",
                      "cognitive", "anxiety", "depression", "inflammation",
                      "joint", "tendon", "energy", "immune", "libido", "sexual",
                      "tanning", "pain", "neuroprotection", "cardio", "cardiac"]:
        if condition in fn:
            return "condition"
    return "guide"  # default comprehensive guide angle


# ============================================================
# HELPER UTILITIES
# ============================================================

def slugify(text):
    return re.sub(r'[^a-z0-9-]', '', text.lower().replace(' ', '-').replace('+', '-plus'))

def esc(text):
    """Escape text for HTML attributes and JSON-LD."""
    return html_mod.escape(str(text), quote=True)

def get_peptide(name):
    """Get peptide data with fallback to defaults."""
    if name in PEPTIDE_DATA:
        d = dict(PEPTIDE_DATA[name])
        # Ensure all fields exist
        for k, v in DEFAULT_PEPTIDE_DATA.items():
            d.setdefault(k, v)
        return d
    # Try fuzzy match
    name_lower = name.lower().strip()
    for k, v in PEPTIDE_DATA.items():
        if k.lower() == name_lower:
            d = dict(v)
            for dk, dv in DEFAULT_PEPTIDE_DATA.items():
                d.setdefault(dk, dv)
            return d
    return None

def internal_link(peptide, angle="guide"):
    """Generate internal link to another article."""
    slug = slugify(peptide)
    if angle == "guide":
        return f'<a href="/{slug}-guide.html">{peptide} guide</a>'
    return f'<a href="/{slug}-{angle}.html">{peptide} {angle.replace("-", " ")}</a>'

def related_peptides(peptide, pdata, limit=3):
    """Find related peptides from stacking info or same class."""
    related = []
    stacking = pdata.get("stacking", "")
    for name in PEPTIDE_DATA:
        if name != peptide and name in stacking:
            related.append(name)
    if len(related) < limit:
        pclass = pdata.get("class", "").lower()
        for name, d in PEPTIDE_DATA.items():
            if name != peptide and name not in related:
                if any(w in d.get("class", "").lower() for w in pclass.split()[:2] if len(w) > 3):
                    related.append(name)
            if len(related) >= limit:
                break
    return related[:limit]

def vendor_links_html(peptide, pdata, vendors_str=""):
    """Generate affiliate vendor link HTML."""
    links = []
    # Use peptide-specific vendors if available
    pvendors = pdata.get("vendors", {})
    if pvendors:
        for name, url in pvendors.items():
            links.append(f'<p><a href="{url}" target="_blank" rel="nofollow sponsored">{name} &rarr; Browse {peptide}</a></p>')
    if not links:
        # Fall back to vendors from matrix data
        if vendors_str:
            for v in vendors_str.split(", "):
                v = v.strip()
                if v in AFFILIATE_LINKS:
                    links.append(f'<p><a href="{AFFILIATE_LINKS[v]}" target="_blank" rel="nofollow sponsored">{v} &rarr; Browse {peptide}</a></p>')
        if not links:
            for name, url in AFFILIATE_LINKS.items():
                links.append(f'<p><a href="{url}" target="_blank" rel="nofollow sponsored">{name} &rarr; Browse Peptides</a></p>')
    return "\n      ".join(links)

def reading_time(angle, article_type):
    """Estimate reading time by angle/type."""
    times = {
        "guide": "10", "dosage": "8", "benefits": "7", "side-effects": "7",
        "before-after": "9", "results-timeline": "9", "half-life": "6",
        "reconstitution": "6", "cycle": "7", "stacking": "8", "beginners": "10",
        "mechanism": "8", "research": "9", "where-to-buy": "7", "injection": "7",
        "women": "8", "men": "8", "reviews": "8", "faq": "6", "storage": "5",
        "legal": "6", "condition": "8",
    }
    type_override = {"Comparison": "10", "Roundup": "12"}
    return type_override.get(article_type, times.get(angle, "8"))


# ============================================================
# QUICK ANSWER BUILDERS — angle-specific 2-3 sentence answers
# ============================================================

def quick_answer_for(peptide, pdata, angle, title):
    """Build a quick-answer that directly answers the specific query."""
    p = peptide
    if angle == "dosage":
        return (f"The most common research dosage for <strong>{p}</strong> is "
                f"<strong>{pdata['dosage_range']}</strong>, administered "
                f"<strong>{pdata['frequency']}</strong> via {pdata['route']}. "
                f"Typical cycles run {pdata['cycle_length']}. With a half-life of "
                f"{pdata['half_life']}, timing matters for optimal results.")
    elif angle == "benefits":
        return (f"<strong>{p}</strong> ({pdata['full_name']}) is researched primarily for "
                f"<strong>{pdata['key_benefits']}</strong>. {pdata.get('unique_angle', '')} "
                f"It belongs to the {pdata['class']} category of compounds.")
    elif angle == "side-effects":
        return (f"{pdata['side_effects']} {p} is {pdata['legal_status'].lower()} "
                f"As with any research compound, individual responses vary.")
    elif angle == "before-after" or angle == "results-timeline":
        return (f"<strong>{p}</strong> results typically emerge over a {pdata['cycle_length']} "
                f"research cycle. Early changes may be noticeable within the first 1-2 weeks, with "
                f"more significant effects on {pdata['key_benefits'].split(',')[0].strip()} appearing by "
                f"weeks 4-8. Results depend on dosage ({pdata['dosage_range']}), consistency, and individual factors.")
    elif angle == "half-life":
        return (f"The half-life of <strong>{p}</strong> is <strong>{pdata['half_life']}</strong>. "
                f"This means dosing {pdata['frequency']} is typical to maintain stable levels. "
                f"The half-life directly affects how long {p} remains active and influences optimal injection timing.")
    elif angle == "reconstitution":
        return (f"<strong>{p}</strong> is typically reconstituted with bacteriostatic water (BAC water). "
                f"The standard dosage of {pdata['dosage_range']} is administered {pdata['frequency']} via {pdata['route']}. "
                f"Use our <a href='/peptide-calculator.html'>peptide calculator</a> for exact mixing ratios.")
    elif angle == "cycle":
        return (f"A typical <strong>{p}</strong> cycle runs <strong>{pdata['cycle_length']}</strong> "
                f"at {pdata['dosage_range']} administered {pdata['frequency']}. "
                f"Cycle length depends on research goals — shorter cycles for acute applications, longer for chronic support.")
    elif angle == "stacking":
        return (f"{pdata.get('stacking', f'{p} can be combined with complementary peptides for synergistic effects.')} "
                f"Proper stacking requires understanding each compound's mechanism and timing.")
    elif angle == "beginners":
        return (f"<strong>{p}</strong> ({pdata['full_name']}) is a {pdata['class']} researched for "
                f"{pdata['key_benefits']}. For beginners, start at the lower end of the dosage range "
                f"({pdata['dosage_range']}) and administer {pdata['frequency']} via {pdata['route']}.")
    elif angle == "mechanism":
        return (f"{pdata['mechanism']}")
    elif angle == "research":
        return (f"{pdata['research_summary']} "
                f"{p} is {pdata['legal_status'].lower()}")
    elif angle == "where-to-buy":
        return (f"<strong>{p}</strong> is available as a research compound from several vetted suppliers. "
                f"When sourcing {p}, prioritize vendors with third-party certificates of analysis (COA), "
                f"HPLC purity testing above 98%, and proper cold-chain shipping.")
    elif angle == "injection":
        return (f"<strong>{p}</strong> is administered via <strong>{pdata['route']}</strong> at "
                f"{pdata['dosage_range']} {pdata['frequency']}. Subcutaneous injections into the abdominal "
                f"fat or thigh are most common. Proper reconstitution with bacteriostatic water is required first.")
    elif angle == "women":
        return (f"<strong>{p}</strong> research in female subjects shows potential benefits for "
                f"{pdata['key_benefits']}. Dosing for women often starts at the lower end of the "
                f"{pdata['dosage_range']} range. {pdata['side_effects']}")
    elif angle == "men":
        return (f"<strong>{p}</strong> has been studied in male subjects for "
                f"{pdata['key_benefits']}. Standard male dosing ranges from {pdata['dosage_range']} "
                f"administered {pdata['frequency']}. {pdata.get('unique_angle', '')}")
    elif angle == "reviews":
        return (f"<strong>{p}</strong> is one of the most discussed peptides in the research community, "
                f"with reports focusing on its effects on {pdata['key_benefits']}. {pdata['research_summary']}")
    elif angle == "faq":
        return (f"<strong>{p}</strong> ({pdata['full_name']}) is a {pdata['class']} researched for "
                f"{pdata['key_benefits']}. Common dosages range from {pdata['dosage_range']} "
                f"administered {pdata['frequency']}. Below are the most frequently asked questions.")
    elif angle == "storage":
        return (f"Lyophilized (freeze-dried) <strong>{p}</strong> should be stored at -20°C for long-term "
                f"stability. Once reconstituted with bacteriostatic water, store at 2-8°C (refrigerated) and "
                f"use within 4-6 weeks. Never freeze reconstituted peptides.")
    elif angle == "legal":
        return (f"<strong>{p}</strong> is <strong>{pdata['legal_status']}</strong> "
                f"Regulations vary by country, and the legal landscape for peptides is evolving. "
                f"This guide covers the current legal status and what researchers need to know.")
    elif angle == "condition":
        # Extract condition from title
        condition = "various applications"
        for word in ["healing", "weight loss", "fat loss", "muscle", "hair", "anti-aging",
                     "skin", "gut", "sleep", "brain", "cognitive", "anxiety", "inflammation",
                     "joint", "tendon", "energy", "immune", "libido", "pain", "tanning"]:
            if word in title.lower():
                condition = word
                break
        return (f"<strong>{p}</strong> is being researched for <strong>{condition}</strong> applications. "
                f"{pdata['mechanism'][:200]}. "
                f"Common dosages for this use range from {pdata['dosage_range']} {pdata['frequency']}.")
    else:
        # Generic guide
        return (f"<strong>{p}</strong> ({pdata['full_name']}) is a {pdata['class']}. "
                f"{pdata['origin']}. "
                f"It is researched for {pdata['key_benefits']}. Common dosages range from "
                f"{pdata['dosage_range']} administered {pdata['frequency']}.")


# ============================================================
# ANGLE-SPECIFIC BODY CONTENT BUILDERS
# ============================================================

def _section(heading_id, heading, *paragraphs):
    """Build an HTML section with H2 and paragraphs."""
    ps = "\n    ".join(f"<p>{p}</p>" for p in paragraphs if p)
    return f'<h2 id="{heading_id}">{heading}</h2>\n    {ps}'

def _subsection(heading, *paragraphs):
    """Build an HTML subsection with H3 and paragraphs."""
    ps = "\n    ".join(f"<p>{p}</p>" for p in paragraphs if p)
    return f'<h3>{heading}</h3>\n    {ps}'

def _calc_cta(peptide):
    return f'''<div style="background: linear-gradient(135deg, #e8f4f5 0%, #f0fdf9 100%); border: 2px solid var(--teal); border-radius: 12px; padding: 24px 28px; margin: 32px 0; text-align: center;">
      <h3 style="margin-top: 0;">Calculate Your {peptide} Dose</h3>
      <p>Use our free peptide dosing calculator to get exact reconstitution math and syringe units for {peptide}.</p>
      <a href="/peptide-calculator.html" style="display: inline-block; background: var(--teal); color: white; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-weight: 600;">Open Calculator &rarr;</a>
    </div>'''

def _related_reading(peptide, pdata, exclude_angle=""):
    """Generate a related reading section with internal links."""
    slug = slugify(peptide)
    links = []
    angles = [
        ("dosage", "Dosage Guide"), ("benefits", "Benefits"), ("side-effects", "Side Effects"),
        ("stacking", "Stacking Guide"), ("cycle", "Cycle Guide"), ("research", "Research"),
    ]
    for a, label in angles:
        if a != exclude_angle:
            links.append(f'<li><a href="/{slug}-{a}.html">{peptide} {label}</a></li>')
    # Also link related peptides
    rel = related_peptides(peptide, pdata)
    for rp in rel:
        links.append(f'<li><a href="/{slugify(rp)}-guide.html">{rp} Complete Guide</a></li>')
    items = "\n      ".join(links[:6])
    return f'''<h3>Related Reading</h3>
    <ul style="list-style: none; padding: 0;">
      {items}
    </ul>'''


def build_dosage_body(p, d):
    """DOSAGE angle — lead with dosing details, reconstitution, timing."""
    sections = []
    sections.append(_section("overview", f"What Is {p} and Why Does Dosing Matter?",
        f"{p} ({d['full_name']}) is a {d['class']}. {d['origin']}. Getting the dosage right is critical — too little may produce no measurable effect, while excessive amounts increase risk without proportional benefit.",
        f"The standard research dosage for {p} has been established through preclinical studies and community protocols. This guide covers the evidence-backed dosing range, timing, and cycle structure."
    ))
    sections.append(_section("recommended-dose", f"What Is the Recommended {p} Dosage?",
        f"The most widely used {p} dosage is <strong>{d['dosage_range']}</strong>, administered <strong>{d['frequency']}</strong> via <strong>{d['route']}</strong>.",
        f"Beginners should start at the lower end of this range and titrate upward only if needed. The half-life of {p} is {d['half_life']}, which directly determines how often you need to dose to maintain stable blood levels.",
        f"For {p} specifically, the {d['cycle_length']} cycle length is standard. Longer isn't always better — {d['class']} compounds require cycling to maintain receptor sensitivity."
    ))
    sections.append(_section("timing", f"When Should You Dose {p}?",
        f"With a half-life of {d['half_life']}, timing your {p} administration affects peak blood levels. Most protocols call for {d['frequency']}.",
        f"For peptides administered before bed (common with GH-related compounds), the goal is to amplify the natural nocturnal growth hormone pulse. For healing peptides, proximity to the injury site via local injection can improve outcomes."
    ))
    sections.append(_calc_cta(p))
    sections.append(_section("reconstitution", f"How Do You Reconstitute {p}?",
        f"{p} typically comes as a lyophilized (freeze-dried) powder. Reconstitute with bacteriostatic water — never saline or sterile water, as BAC water contains 0.9% benzyl alcohol that prevents bacterial growth and extends shelf life to 4-6 weeks.",
        f"Use our <a href='/peptide-calculator.html'>peptide dosing calculator</a> to determine the exact amount of BAC water to add based on your vial size and desired dose per injection."
    ))
    sections.append(_section("cycle-structure", f"How Long Should a {p} Cycle Last?",
        f"Standard {p} cycles run <strong>{d['cycle_length']}</strong>. This timeframe is based on the compound's mechanism and the time needed to observe measurable effects.",
        f"{d['research_summary']}"
    ))
    sections.append(_section("side-effects", f"What Side Effects Can Affect Dosing?",
        f"{d['side_effects']}",
        f"If side effects emerge, the first step is typically reducing the dose rather than discontinuing entirely. Most {p}-related side effects are dose-dependent."
    ))
    sections.append(_section("stacking-doses", f"How Does {p} Dosing Change When Stacking?",
        f"{d.get('stacking', f'{p} can be combined with other peptides for enhanced effects.')}",
        f"When stacking, some researchers reduce individual peptide doses by 20-30% since synergistic effects mean full doses of each aren't always necessary."
    ))
    sections.append(_section("bottom-line", f"What Is the Bottom Line on {p} Dosing?",
        f"Start at <strong>{d['dosage_range'].split('-')[0] if '-' in d['dosage_range'] else d['dosage_range']}</strong>, dose {d['frequency']}, and run cycles of {d['cycle_length']}. Monitor your response and adjust within the established range.",
        f"Source matters — always use research-grade {p} from vendors with third-party COA testing. Underdosed or contaminated products are the most common reason for poor results."
    ))
    sections.append(_related_reading(p, d, "dosage"))
    return "\n\n    ".join(sections)


def build_benefits_body(p, d):
    sections = []
    benefits_list = [b.strip() for b in d['key_benefits'].split(',')]
    sections.append(_section("overview", f"What Is {p}?",
        f"{p} ({d['full_name']}) is a {d['class']}. {d['origin']}.",
        f"{d.get('unique_angle', '')} It has attracted significant research interest for its potential effects on {d['key_benefits']}."
    ))
    sections.append(_section("how-it-works", f"How Does {p} Produce These Benefits?",
        f"{d['mechanism']}",
        f"This multi-pathway activity is why {p} shows potential across several different applications rather than being limited to a single use case."
    ))
    # Individual benefit sections
    for i, benefit in enumerate(benefits_list[:5]):
        benefit_clean = benefit.strip()
        sections.append(_section(f"benefit-{i+1}", f"Can {p} Help With {benefit_clean.title()}?",
            f"Research suggests {p} may support {benefit_clean} through its {d['class'].lower()} activity. {d['research_summary']}",
            f"Protocols targeting {benefit_clean} typically use {d['dosage_range']} administered {d['frequency']} for {d['cycle_length']}."
        ))
    sections.append(_section("stacking", f"Can Stacking Enhance {p} Benefits?",
        f"{d.get('stacking', f'{p} may be combined with complementary compounds.')}",
        f"See our <a href='/{slugify(p)}-stacking.html'>{p} stacking guide</a> for detailed combination protocols."
    ))
    sections.append(_section("bottom-line", f"What Is the Bottom Line on {p} Benefits?",
        f"{p} is researched for {d['key_benefits']}. The evidence base includes: {d['research_summary']}",
        f"{p} is {d['legal_status'].lower()} Source from reputable vendors with third-party testing for reliable results."
    ))
    sections.append(_related_reading(p, d, "benefits"))
    return "\n\n    ".join(sections)


def build_side_effects_body(p, d):
    sections = []
    sections.append(_section("overview", f"Is {p} Safe?",
        f"Safety is the most important consideration with any research compound. {p} ({d['full_name']}) is a {d['class']} with a safety profile established through preclinical research.",
        f"{d['research_summary']}"
    ))
    sections.append(_section("known-effects", f"What Are the Known Side Effects of {p}?",
        f"<strong>{d['side_effects']}</strong>",
        f"These effects are based on preclinical data and community reports at standard dosages of {d['dosage_range']}. Higher doses generally increase both the likelihood and severity of side effects."
    ))
    sections.append(_section("dose-dependent", f"Are {p} Side Effects Dose-Dependent?",
        f"Most reported {p} side effects are dose-dependent — meaning they're more likely at higher doses and less likely at the lower end of the {d['dosage_range']} range.",
        f"This is why starting at the minimum effective dose and titrating up is the standard approach. With a half-life of {d['half_life']}, any adverse effects will typically resolve within a few half-life periods after discontinuation."
    ))
    sections.append(_section("long-term", f"What About Long-Term {p} Use?",
        f"Long-term safety data for {p} is limited, as with most research peptides. Standard cycles run {d['cycle_length']}.",
        f"{p} is {d['legal_status'].lower()} Extended use beyond recommended cycles should be approached with caution."
    ))
    sections.append(_section("interactions", f"Does {p} Interact With Other Compounds?",
        f"{d.get('stacking', f'{p} interaction data with other compounds is limited.')}",
        f"When stacking peptides, be aware that combining multiple compounds increases the total side-effect surface area. Monitor closely when introducing any new compound."
    ))
    sections.append(_section("minimize", f"How Can You Minimize {p} Side Effects?",
        f"Start at the lower end of the dosage range ({d['dosage_range']}). Use proper reconstitution and injection technique to minimize injection site reactions. Store correctly (lyophilized at -20°C, reconstituted at 2-8°C) to maintain purity.",
        f"Source only from vendors with third-party COA testing — contaminated or mislabeled products are a significant source of unexpected adverse effects."
    ))
    sections.append(_section("bottom-line", f"What Is the Bottom Line on {p} Safety?",
        f"{d['side_effects']} Overall, {p} is considered {'well-tolerated' if 'well-tolerated' in d['side_effects'].lower() else 'a compound requiring careful monitoring'} at standard research doses.",
        f"Read our <a href='/{slugify(p)}-dosage.html'>{p} dosage guide</a> for protocols designed to minimize risk."
    ))
    sections.append(_related_reading(p, d, "side-effects"))
    return "\n\n    ".join(sections)


def build_results_timeline_body(p, d):
    sections = []
    cycle = d['cycle_length']
    benefits = d['key_benefits'].split(',')
    sections.append(_section("overview", f"What Results Can You Expect From {p}?",
        f"{p} ({d['full_name']}) is a {d['class']} researched for {d['key_benefits']}. Results depend on dosage ({d['dosage_range']}), administration frequency ({d['frequency']}), and individual factors.",
        f"The following timeline is based on standard {d['dosage_range']} protocols over a {cycle} cycle."
    ))
    sections.append(_section("week-1-2", f"What Happens in Weeks 1-2 of {p}?",
        f"During the first two weeks, {p} is establishing baseline blood levels. With a half-life of {d['half_life']}, steady-state concentrations are typically reached within 4-5 half-lives.",
        f"Subtle changes researchers may notice: improved {benefits[0].strip() if benefits else 'general wellbeing'}, better sleep quality (commonly reported across peptide protocols), and mild injection site reactions that typically resolve."
    ))
    sections.append(_section("week-3-4", f"What Changes by Weeks 3-4?",
        f"By week 3-4, the biological pathways {p} targets are becoming measurably activated. {d['mechanism'][:200]}.",
        f"More noticeable effects on {', '.join(b.strip() for b in benefits[:3])} begin to emerge. This is the phase where most researchers report the first clear evidence that the compound is working."
    ))
    sections.append(_section("week-5-8", f"What Results Appear at Weeks 5-8?",
        f"Weeks 5-8 represent the peak response window for most {d['class']} compounds. Cumulative effects of consistent {d['frequency']} dosing at {d['dosage_range']} produce the most visible changes.",
        f"Key results during this phase typically include pronounced improvements in {d['key_benefits']}. This is when before-and-after differences become most apparent."
    ))
    if "12" in cycle or "ongoing" in cycle.lower():
        sections.append(_section("week-8-12", f"What About Weeks 8-12 and Beyond?",
            f"For extended {p} cycles ({cycle}), weeks 8-12 often show the most dramatic cumulative results. However, diminishing returns and receptor adaptation can occur.",
            f"Many protocols include a washout period after the cycle to restore baseline sensitivity. {d.get('stacking', '')}"
        ))
    sections.append(_section("maximize", f"How Can You Maximize {p} Results?",
        f"Consistent dosing at {d['dosage_range']} {d['frequency']} is the single biggest factor. Skipping doses or inconsistent timing significantly reduces outcomes.",
        f"Proper storage (reconstituted at 2-8°C), sourcing from COA-tested vendors, and supporting protocols (nutrition, sleep, training where applicable) all contribute to results.",
        f"{d.get('stacking', '')}"
    ))
    sections.append(_calc_cta(p))
    sections.append(_section("bottom-line", f"What Is the Realistic {p} Timeline?",
        f"Expect initial effects in weeks 1-2, noticeable changes by weeks 3-4, and peak results during weeks 5-8 of a {cycle} cycle. {p} is not instant — consistent dosing and patience are required.",
        f"{p} is {d['legal_status'].lower()}"
    ))
    sections.append(_related_reading(p, d, "results-timeline"))
    return "\n\n    ".join(sections)


def build_before_after_body(p, d):
    """Reuse results timeline but framed around before/after expectations."""
    return build_results_timeline_body(p, d)


def build_half_life_body(p, d):
    sections = []
    sections.append(_section("overview", f"What Is the Half-Life of {p}?",
        f"The half-life of <strong>{p}</strong> is <strong>{d['half_life']}</strong>. This is the time it takes for blood concentration to drop by 50% after administration.",
        f"Understanding half-life is essential for designing effective dosing protocols — it determines how often you need to administer {p} to maintain therapeutic blood levels."
    ))
    sections.append(_section("what-it-means", f"What Does {p}'s Half-Life Mean for Dosing?",
        f"With a half-life of {d['half_life']}, {p} requires dosing {d['frequency']} to maintain stable levels. The standard dosage of {d['dosage_range']} via {d['route']} accounts for this pharmacokinetic profile.",
        f"After approximately 4-5 half-lives, {p} reaches steady-state concentration — the point where the amount being absorbed equals the amount being eliminated. For {p}, this occurs within the first few days of consistent dosing."
    ))
    sections.append(_section("timing", f"When Is the Best Time to Inject {p}?",
        f"Optimal timing depends on your research goals. A half-life of {d['half_life']} means peak blood levels occur shortly after injection and decline predictably.",
        f"Common timing approaches: morning injection for daytime activity, pre-bed injection for overnight effects, or split dosing ({d['frequency']}) for more stable levels throughout the day."
    ))
    sections.append(_section("vs-others", f"How Does {p}'s Half-Life Compare to Similar Peptides?",
        f"{p} is a {d['class']}. Its half-life of {d['half_life']} positions it {'with a shorter' if 'minute' in d['half_life'].lower() or 'hour' in d['half_life'].lower() else 'with a longer'} duration of action compared to some alternatives in this class.",
        f"Shorter half-lives require more frequent dosing but allow for more precise control. Longer half-lives are more convenient but carry risk of accumulation."
    ))
    sections.append(_calc_cta(p))
    sections.append(_section("bottom-line", f"Bottom Line: {p} Half-Life and Dosing",
        f"{p} has a half-life of {d['half_life']}, supporting the standard protocol of {d['dosage_range']} dosed {d['frequency']} over {d['cycle_length']}.",
        f"Read our <a href='/{slugify(p)}-dosage.html'>{p} dosage guide</a> for complete protocol details."
    ))
    sections.append(_related_reading(p, d, "half-life"))
    return "\n\n    ".join(sections)


def build_reconstitution_body(p, d):
    sections = []
    sections.append(_section("overview", f"How Do You Reconstitute {p}?",
        f"{p} is supplied as a lyophilized (freeze-dried) powder that must be reconstituted before use. Proper reconstitution is critical for accurate dosing and maintaining stability.",
        f"This guide covers the step-by-step process for mixing {p} with bacteriostatic water to achieve your target concentration."
    ))
    sections.append(_section("supplies", f"What Supplies Do You Need?",
        f"To reconstitute {p}, you need: the {p} vial (lyophilized powder), bacteriostatic water (BAC water with 0.9% benzyl alcohol), insulin syringes (typically 1mL/100-unit), alcohol swabs, and a clean workspace.",
        f"<strong>Important:</strong> Always use bacteriostatic water — not sterile water or saline. BAC water's benzyl alcohol prevents bacterial contamination, extending the usable life of reconstituted {p} to 4-6 weeks."
    ))
    sections.append(_section("steps", f"Step-by-Step {p} Reconstitution",
        f"<strong>Step 1:</strong> Clean the vial tops of both the {p} and BAC water with alcohol swabs.",
        f"<strong>Step 2:</strong> Draw the calculated amount of BAC water into an insulin syringe. Use our <a href='/peptide-calculator.html'>peptide calculator</a> to determine the exact amount.",
        f"<strong>Step 3:</strong> Insert the needle into the {p} vial at an angle, and let the water run down the side of the glass — <strong>never spray directly onto the powder</strong> as this can damage the peptide bonds.",
        f"<strong>Step 4:</strong> Gently swirl (do not shake) the vial until the powder is fully dissolved. The solution should be clear.",
        f"<strong>Step 5:</strong> Label the vial with the date and concentration. Store at 2-8°C."
    ))
    sections.append(_calc_cta(p))
    sections.append(_section("dosing-after", f"How Do You Dose Reconstituted {p}?",
        f"After reconstitution, the standard {p} dose is {d['dosage_range']} administered {d['frequency']} via {d['route']}. The number of units on your insulin syringe depends on how much BAC water you added.",
        f"Our <a href='/peptide-calculator.html'>calculator</a> will tell you exactly how many units to draw for your dose based on your specific reconstitution ratio."
    ))
    sections.append(_section("storage-after", f"How Do You Store Reconstituted {p}?",
        f"Store reconstituted {p} at 2-8°C (standard refrigerator temperature). Use within 4-6 weeks. Keep away from light and temperature fluctuations.",
        f"Unreconstituted {p} powder can be stored at -20°C for 12+ months. Once you reconstitute it, the clock starts."
    ))
    sections.append(_section("bottom-line", f"Bottom Line",
        f"Reconstituting {p} is straightforward — add BAC water, swirl gently, refrigerate. The key is using the right amount of water for accurate dosing. Use our <a href='/peptide-calculator.html'>peptide calculator</a> every time.",
    ))
    sections.append(_related_reading(p, d, "reconstitution"))
    return "\n\n    ".join(sections)


def build_cycle_body(p, d):
    sections = []
    sections.append(_section("overview", f"How Long Is a {p} Cycle?",
        f"A standard {p} cycle runs <strong>{d['cycle_length']}</strong> at {d['dosage_range']} administered {d['frequency']}. Cycle length is determined by the compound's mechanism, receptor dynamics, and the time needed to observe measurable effects.",
        f"{p} is a {d['class']}. {d['mechanism'][:200]}."
    ))
    sections.append(_section("structure", f"How Should You Structure a {p} Cycle?",
        f"<strong>Loading Phase (Week 1-2):</strong> Start at the lower end of {d['dosage_range']} to assess tolerance. Administer {d['frequency']} via {d['route']}.",
        f"<strong>Standard Phase (Weeks 3-{d['cycle_length'].split('-')[0] if '-' in d['cycle_length'] else '8'}):</strong> Move to full dosage range if no adverse effects. Maintain consistent timing and frequency.",
        f"<strong>Taper/End:</strong> Some protocols taper the final week; others stop abruptly. The half-life of {d['half_life']} means the compound clears relatively quickly."
    ))
    sections.append(_section("off-cycle", f"What Happens Between {p} Cycles?",
        f"A washout period between cycles helps restore receptor sensitivity and prevents desensitization. Common protocols use a 4-week off period between {d['cycle_length']} cycles.",
        f"During the off-cycle, the biological effects of {p} gradually diminish as the compound clears. Some benefits (like tissue remodeling) may persist longer than others."
    ))
    sections.append(_section("stacking-in-cycle", f"How Does Stacking Affect the Cycle?",
        f"{d.get('stacking', f'{p} can be combined with complementary compounds during a cycle.')}",
        f"When stacking, all compounds should ideally start and end together, though some researchers stagger introductions to isolate individual effects."
    ))
    sections.append(_calc_cta(p))
    sections.append(_section("bottom-line", f"Bottom Line on {p} Cycling",
        f"Run {p} for {d['cycle_length']} at {d['dosage_range']} {d['frequency']}. Take a 4-week break between cycles. Start conservatively and maintain consistency throughout.",
        f"See our <a href='/{slugify(p)}-dosage.html'>{p} dosage guide</a> for detailed protocol information."
    ))
    sections.append(_related_reading(p, d, "cycle"))
    return "\n\n    ".join(sections)


def build_stacking_body(p, d):
    sections = []
    sections.append(_section("overview", f"What Is {p} Stacking?",
        f"Stacking means combining {p} with one or more complementary peptides to potentially achieve synergistic effects. Because different peptides work through different mechanisms, strategic combinations can target multiple pathways simultaneously.",
        f"{p} ({d['full_name']}) is a {d['class']} researched for {d['key_benefits']}."
    ))
    sections.append(_section("best-stack", f"What Is the Best {p} Stack?",
        f"{d.get('stacking', f'{p} pairs well with peptides that target complementary pathways.')}",
        f"This combination is popular because it targets multiple mechanisms without significant overlap in side-effect profiles."
    ))
    rel = related_peptides(p, d, 4)
    for rp in rel[:3]:
        rd = get_peptide(rp)
        if rd:
            sections.append(_section(f"stack-{slugify(rp)}", f"How Does {p} Stack With {rp}?",
                f"{rp} ({rd['full_name']}) is a {rd['class']} that works through {rd['mechanism'][:150]}.",
                f"Combined with {p}'s effects on {d['key_benefits']}, this stack covers {rd['key_benefits']} as well.",
                f"Typical stacking protocol: {p} at {d['dosage_range']} {d['frequency']} alongside {rp} at {rd['dosage_range']} {rd['frequency']}. See our <a href='/{slugify(rp)}-guide.html'>{rp} guide</a> for details."
            ))
    sections.append(_section("timing", f"How Do You Time a {p} Stack?",
        f"When stacking, timing each injection based on half-life is important. {p} has a half-life of {d['half_life']}, which influences when to administer relative to other compounds.",
        f"Some researchers inject all peptides at the same time; others stagger by 15-30 minutes. There's limited data on whether timing within the same session matters significantly."
    ))
    sections.append(_section("avoid", f"What Should You NOT Stack With {p}?",
        f"Avoid stacking peptides with similar mechanisms of action at full doses — this can lead to receptor desensitization without proportional benefit. Also avoid combining compounds where side-effect profiles overlap significantly.",
        f"When in doubt, introduce one new compound at a time to isolate its effects before building a full stack."
    ))
    sections.append(_calc_cta(p))
    sections.append(_section("bottom-line", f"Bottom Line on {p} Stacking",
        f"{d.get('stacking', f'{p} stacking should be approached systematically.')} Start with a single compound, assess response, then add complements.",
        f"See our <a href='/peptide-cycling-guide.html'>stacking and cycling guide</a> for general principles."
    ))
    sections.append(_related_reading(p, d, "stacking"))
    return "\n\n    ".join(sections)


def build_beginners_body(p, d):
    sections = []
    sections.append(_section("what-is", f"What Is {p}?",
        f"{p} ({d['full_name']}) is a {d['class']}. {d['origin']}.",
        f"It is researched for its potential effects on {d['key_benefits']}. {d.get('unique_angle', '')}",
        f"<strong>For beginners:</strong> This guide assumes no prior peptide experience. We'll cover everything from what {p} is to how to reconstitute, inject, and structure your first cycle."
    ))
    sections.append(_section("how-it-works", f"How Does {p} Work?",
        f"{d['mechanism']}",
        f"Understanding the mechanism helps set realistic expectations about what {p} can and cannot do."
    ))
    sections.append(_section("getting-started", f"How Do You Get Started With {p}?",
        f"<strong>Step 1 — Source:</strong> Purchase {p} from a vendor with third-party Certificate of Analysis (COA) testing. This confirms purity (aim for 98%+) and rules out contamination.",
        f"<strong>Step 2 — Supplies:</strong> You'll need bacteriostatic water, insulin syringes (1mL/100-unit), alcohol swabs, and a clean workspace.",
        f"<strong>Step 3 — Reconstitute:</strong> Add BAC water to the {p} vial — use our <a href='/peptide-calculator.html'>peptide calculator</a> for exact amounts. Let the water run down the side of the vial; never spray directly on the powder. Swirl gently.",
        f"<strong>Step 4 — Dose:</strong> Draw {d['dosage_range']} using the calculator's syringe unit conversion.",
        f"<strong>Step 5 — Inject:</strong> Clean the injection site with alcohol. Pinch a fold of abdominal fat and insert the needle at 45° for subcutaneous injection. Push the plunger slowly and hold for 5 seconds."
    ))
    sections.append(_calc_cta(p))
    sections.append(_section("first-cycle", f"What Should Your First {p} Cycle Look Like?",
        f"<strong>Dosage:</strong> Start at the <em>lower end</em> of {d['dosage_range']}. This lets you assess tolerance before committing to a full cycle.",
        f"<strong>Frequency:</strong> {d['frequency']} via {d['route']}.",
        f"<strong>Duration:</strong> {d['cycle_length']}. Don't cut cycles short — many {d['class']} effects take weeks to fully manifest.",
        f"<strong>Off-cycle:</strong> Plan a 4-week break before starting another cycle."
    ))
    sections.append(_section("side-effects", f"What Side Effects Should Beginners Watch For?",
        f"{d['side_effects']}",
        f"As a beginner, track everything — dose, time, injection site, and any effects (positive or negative). This data helps optimize future cycles."
    ))
    sections.append(_section("mistakes", f"What Are Common Beginner Mistakes?",
        f"<strong>Not using BAC water:</strong> Sterile water lacks the preservative that prevents bacterial growth. Always use bacteriostatic water.",
        f"<strong>Inconsistent dosing:</strong> Skipping doses or varying timing significantly reduces outcomes. Set a daily alarm.",
        f"<strong>Poor storage:</strong> Reconstituted {p} must stay refrigerated at 2-8°C. Leaving it at room temperature degrades the compound rapidly.",
        f"<strong>Buying cheap:</strong> Low-cost peptides without COA testing may be underdosed, contaminated, or mislabeled. Quality matters more than price."
    ))
    sections.append(_section("bottom-line", f"Bottom Line for {p} Beginners",
        f"Start at the lower end of {d['dosage_range']}, dose {d['frequency']}, cycle for {d['cycle_length']}, and track everything. Source from COA-tested vendors and follow proper reconstitution protocol.",
        f"Read our <a href='/peptide-beginners-guide.html'>complete peptide beginner's guide</a> for general peptide education beyond {p}."
    ))
    sections.append(_related_reading(p, d, "beginners"))
    return "\n\n    ".join(sections)


def build_mechanism_body(p, d):
    sections = []
    sections.append(_section("overview", f"How Does {p} Work in the Body?",
        f"{p} ({d['full_name']}) is a {d['class']}. {d['origin']}.",
        f"Understanding its mechanism of action helps researchers design protocols and predict outcomes."
    ))
    sections.append(_section("primary-mechanism", f"What Is the Primary Mechanism of {p}?",
        f"{d['mechanism']}",
        f"This mechanism operates at the cellular level and influences downstream pathways that produce the observable effects researchers study."
    ))
    sections.append(_section("pathways", f"What Biological Pathways Does {p} Affect?",
        f"As a {d['class']}, {p} interacts with specific receptors and signaling cascades. These pathways are responsible for the compound's effects on {d['key_benefits']}.",
        f"The multi-pathway activity is what gives {p} its broad potential application range — each pathway contributes to different aspects of the overall effect profile."
    ))
    sections.append(_section("timeline", f"How Quickly Does {p}'s Mechanism Take Effect?",
        f"With a half-life of {d['half_life']}, {p} begins interacting with its target receptors within minutes of administration. However, the downstream biological effects take longer to manifest — typically days to weeks depending on the application.",
        f"Standard cycles run {d['cycle_length']} because that's the timeframe needed for the mechanism to produce measurable, cumulative results."
    ))
    sections.append(_section("research", f"What Does the Research Say?",
        f"{d['research_summary']}",
        f"{d.get('unique_angle', '')}"
    ))
    sections.append(_section("bottom-line", f"Bottom Line on {p}'s Mechanism",
        f"{p} works through {d['class'].lower()} activity to influence {d['key_benefits']}. Its mechanism involves multiple pathways, which is why it shows potential across several research applications.",
        f"See our <a href='/{slugify(p)}-benefits.html'>{p} benefits guide</a> for how this mechanism translates to practical outcomes."
    ))
    sections.append(_related_reading(p, d, "mechanism"))
    return "\n\n    ".join(sections)


def build_research_body(p, d):
    sections = []
    sections.append(_section("overview", f"What Does the Research Say About {p}?",
        f"{d['research_summary']}",
        f"{p} ({d['full_name']}) is a {d['class']}. Research interest has focused on its potential effects on {d['key_benefits']}."
    ))
    sections.append(_section("mechanism-data", f"What Is the Evidence for {p}'s Mechanism?",
        f"{d['mechanism']}",
        f"These pathways have been identified through in vitro studies, animal models, and where available, human trials."
    ))
    sections.append(_section("clinical", f"Are There Human Clinical Trials for {p}?",
        f"{d['research_summary']}",
        f"The gap between preclinical promise and clinical validation remains the biggest challenge in peptide research. However, {p} has shown {'encouraging' if 'promising' in d['research_summary'].lower() or 'clinical' in d['research_summary'].lower() else 'preliminary'} results."
    ))
    sections.append(_section("safety-data", f"What Does the Safety Research Show?",
        f"{d['side_effects']}",
        f"{p} is {d['legal_status'].lower()}"
    ))
    sections.append(_section("unique", f"What Makes {p} Unique in Research?",
        f"{d.get('unique_angle', f'{p} occupies a distinctive niche in peptide research.')}",
        f"This differentiator is important because it means {p} fills a role that other compounds in its class may not fully replicate."
    ))
    sections.append(_section("bottom-line", f"Bottom Line on {p} Research",
        f"The evidence base for {p} is {'strong' if '100' in d['research_summary'] or '1,000' in d['research_summary'] else 'growing'}. Key research areas include {d['key_benefits']}.",
        "Stay current with <a href='https://pubmed.ncbi.nlm.nih.gov/?term=" + p.replace(" ", "+") + "' target='_blank' rel='nofollow'>PubMed searches for " + p + "</a> for the latest publications."
    ))
    sections.append(_related_reading(p, d, "research"))
    return "\n\n    ".join(sections)


def build_where_to_buy_body(p, d):
    sections = []
    sections.append(_section("overview", f"Where Can You Buy {p}?",
        f"{p} is {d['legal_status'].lower()} It is available from several research chemical suppliers. The quality difference between vendors is significant — sourcing from a tested, reputable supplier is the single most important decision.",
    ))
    sections.append(_section("what-to-look-for", f"What Should You Look For in a {p} Vendor?",
        f"<strong>Third-party COA testing:</strong> Every batch should come with a Certificate of Analysis from an independent lab confirming identity and purity (98%+ HPLC).",
        f"<strong>Cold-chain shipping:</strong> Peptides degrade in heat. Quality vendors use insulated packaging and cold packs.",
        f"<strong>Proper packaging:</strong> Lyophilized powder in sealed, labeled vials. Avoid pre-mixed or pre-loaded products.",
        f"<strong>Reputation:</strong> Established vendors with consistent community feedback are safer than new or untested sources."
    ))
    sections.append(_section("recommended", f"Which Vendors Carry {p}?",
        f"WolveStack has reviewed the following suppliers for purity, COA availability, shipping practices, and community reputation. These are the vendors we recommend for sourcing research-grade {p}.",
    ))
    sections.append(_section("avoid", f"What Red Flags Should You Watch For?",
        f"<strong>No COA:</strong> If a vendor can't provide a current, third-party COA for their {p}, move on. This is non-negotiable.",
        f"<strong>Unusually low prices:</strong> Peptide synthesis is expensive. Prices dramatically below market average usually indicate underdosed or substituted product.",
        f"<strong>Pre-mixed solutions:</strong> Reconstituted peptides have a shelf life of 4-6 weeks. Vendors selling pre-mixed {p} in syringes or vials are shipping degraded product.",
        f"<strong>No contact/return policy:</strong> Legitimate vendors stand behind their products."
    ))
    sections.append(_section("storage", f"How Should You Store {p} After Purchase?",
        f"Unreconstituted {p} (lyophilized powder): Store at -20°C (freezer) for up to 12+ months. Keep sealed and away from moisture.",
        f"Reconstituted {p}: Store at 2-8°C (refrigerator). Use within 4-6 weeks. Never freeze reconstituted peptides."
    ))
    sections.append(_section("bottom-line", f"Bottom Line on Buying {p}",
        f"Source {p} from vendors with current third-party COA testing, cold-chain shipping, and established reputations. Quality directly determines results — cheap peptides are expensive mistakes."
    ))
    sections.append(_related_reading(p, d, "where-to-buy"))
    return "\n\n    ".join(sections)


def build_injection_body(p, d):
    sections = []
    sections.append(_section("overview", f"How Do You Inject {p}?",
        f"{p} is administered via <strong>{d['route']}</strong>. For most researchers, subcutaneous injection is the standard approach — it's simple, relatively painless, and effective for {d['class']} compounds.",
        f"This guide covers injection technique, site selection, needle choices, and common mistakes."
    ))
    sections.append(_section("preparation", f"How Do You Prepare for a {p} Injection?",
        f"<strong>Step 1:</strong> Wash your hands thoroughly.",
        f"<strong>Step 2:</strong> Clean the top of the {p} vial and BAC water vial with alcohol swabs. If not yet reconstituted, see our <a href='/{slugify(p)}-reconstitution.html'>{p} reconstitution guide</a>.",
        f"<strong>Step 3:</strong> Draw your dose ({d['dosage_range']}) into an insulin syringe. Use our <a href='/peptide-calculator.html'>calculator</a> for exact units.",
        f"<strong>Step 4:</strong> Clean the injection site with an alcohol swab and let it dry."
    ))
    sections.append(_section("technique", f"What Is the Correct Injection Technique?",
        f"<strong>Subcutaneous (most common):</strong> Pinch a fold of skin — typically abdominal fat 2+ inches from the navel, or the thigh. Insert the needle at a 45-degree angle. Push the plunger slowly and steadily. Hold for 5 seconds, then withdraw.",
        f"<strong>Intramuscular (less common for {p}):</strong> Insert the needle at 90 degrees into the muscle (deltoid or vastus lateralis). This route provides faster absorption but isn't necessary for most peptide protocols.",
        f"Rotate injection sites to prevent lipodystrophy (fat tissue changes from repeated injections in the same spot)."
    ))
    sections.append(_section("needles", f"What Size Needle Should You Use?",
        f"For subcutaneous {p} injections, 29-31 gauge insulin needles (½ inch or 8mm) are standard. These are thin enough to be nearly painless while long enough for proper subcutaneous delivery.",
        f"Use a fresh needle for every injection. Never reuse or share needles."
    ))
    sections.append(_calc_cta(p))
    sections.append(_section("side-effects", f"What Are Common Injection Side Effects?",
        f"Mild redness, swelling, or itching at the injection site is normal and typically resolves within hours. Small bruises can occur, especially if you hit a capillary.",
        f"If you experience persistent pain, swelling, warmth, or redness lasting more than 24 hours, discontinue and consult a healthcare provider — these may indicate infection."
    ))
    sections.append(_section("bottom-line", f"Bottom Line on {p} Injection",
        f"{p} is administered via {d['route']} at {d['dosage_range']} {d['frequency']}. Subcutaneous injection with a 29-31 gauge insulin needle into abdominal fat is the standard technique. Rotate sites and use a fresh needle every time."
    ))
    sections.append(_related_reading(p, d, "injection"))
    return "\n\n    ".join(sections)


def build_gender_body(p, d, gender):
    sections = []
    sections.append(_section("overview", f"Can {'Women' if gender=='women' else 'Men'} Use {p}?",
        f"Yes — {p} ({d['full_name']}) is researched in both male and female subjects. As a {d['class']}, its mechanism ({d['mechanism'][:150]}) is not gender-specific.",
        f"However, dosing, goals, and side-effect monitoring may differ between {'female' if gender=='women' else 'male'} and {'male' if gender=='women' else 'female'} subjects."
    ))
    sections.append(_section("benefits", f"What Benefits Does {p} Offer {'Women' if gender=='women' else 'Men'}?",
        f"{p} is researched for {d['key_benefits']}. {'For women, particular interest areas often include skin health, anti-aging, healing, and body composition.' if gender=='women' else 'For men, focus areas often include recovery, body composition, growth hormone optimization, and performance.'}",
        f"{d.get('unique_angle', '')}"
    ))
    sections.append(_section("dosing", f"What Is the Recommended {p} Dosage for {'Women' if gender=='women' else 'Men'}?",
        f"{'Women typically start at the lower end of the dosage range: ' + d['dosage_range'] + '. Body weight and composition differences may warrant dose adjustments.' if gender=='women' else 'Standard male dosing: ' + d['dosage_range'] + ' administered ' + d['frequency'] + ' via ' + d['route'] + '.'}",
        f"Cycle length: {d['cycle_length']}. {'Women should pay extra attention to any hormonal effects and adjust accordingly.' if gender=='women' else 'Standard cycling protocols apply.'}"
    ))
    sections.append(_section("side-effects", f"Are There {'Female' if gender=='women' else 'Male'}-Specific Side Effects?",
        f"{d['side_effects']}",
        f"{'Women should be aware of potential hormonal interactions, particularly with compounds that affect GH, cortisol, or sex hormones. If pregnant, nursing, or trying to conceive, peptide use is not recommended.' if gender=='women' else 'Men should monitor for any androgenic or estrogenic effects, particularly with GH-related peptides that can influence IGF-1 and insulin sensitivity.'}"
    ))
    sections.append(_calc_cta(p))
    sections.append(_section("bottom-line", f"Bottom Line on {p} for {'Women' if gender=='women' else 'Men'}",
        f"{p} can be used by {'women' if gender=='women' else 'men'} at {'appropriately adjusted' if gender=='women' else 'standard'} doses of {d['dosage_range']}. {d['frequency'].capitalize()} administration via {d['route']} for {d['cycle_length']}.",
        f"As always, source from COA-tested vendors and follow proper protocols. See our <a href='/{slugify(p)}-dosage.html'>{p} dosage guide</a> for full details."
    ))
    sections.append(_related_reading(p, d, "women" if gender=="women" else "men"))
    return "\n\n    ".join(sections)


def build_reviews_body(p, d):
    sections = []
    sections.append(_section("overview", f"What Do Researchers Report About {p}?",
        f"{p} ({d['full_name']}) is one of the most discussed {d['class']} compounds in the peptide research community. Reports span effects on {d['key_benefits']}.",
        f"{d['research_summary']}"
    ))
    sections.append(_section("positive", f"What Are the Most Common Positive Reports?",
        f"Researchers frequently cite {p}'s effects on {d['key_benefits']} as the primary benefits observed during standard cycles of {d['cycle_length']}.",
        f"{d.get('unique_angle', '')} This distinctive profile is a key reason {p} maintains its popularity despite the growing number of alternatives."
    ))
    sections.append(_section("negative", f"What Are the Common Criticisms?",
        f"The most common complaints about {p}: {d['side_effects']}",
        f"Cost and sourcing quality are also frequent concerns — results vary significantly between vendors, which is why COA testing is essential."
    ))
    sections.append(_section("vs-alternatives", f"How Does {p} Compare to Alternatives?",
        f"As a {d['class']}, {p} competes with several similar compounds. {d.get('unique_angle', 'Its specific advantages depend on the research application.')}",
        f"{d.get('stacking', 'Many researchers combine ' + p + ' with complementary peptides for enhanced results.')}"
    ))
    sections.append(_section("bottom-line", f"Bottom Line: Is {p} Worth It?",
        f"Based on the available research and community reports, {p} is {'well-regarded' if 'well-tolerated' in d['side_effects'].lower() else 'considered promising'} for {d['key_benefits']}. The key factors for success: consistent dosing ({d['dosage_range']} {d['frequency']}), quality sourcing, and realistic expectations over {d['cycle_length']} cycles.",
    ))
    sections.append(_related_reading(p, d, "reviews"))
    return "\n\n    ".join(sections)


def build_faq_body(p, d):
    faqs = [
        (f"What is {p}?", f"{p} ({d['full_name']}) is a {d['class']}. {d['origin']}. It is researched for {d['key_benefits']}."),
        (f"What is the recommended {p} dosage?", f"Common dosages range from {d['dosage_range']}, administered {d['frequency']} via {d['route']}. Cycles typically run {d['cycle_length']}."),
        (f"What are the side effects of {p}?", d['side_effects']),
        (f"Is {p} legal?", d['legal_status']),
        (f"What is the half-life of {p}?", f"The half-life of {p} is {d['half_life']}, which determines the {d['frequency']} dosing schedule."),
        (f"How do you reconstitute {p}?", f"Add bacteriostatic water to the lyophilized {p} vial. Let the water run down the side — never spray on the powder. Swirl gently. Use our peptide calculator for exact amounts."),
        (f"Can you stack {p} with other peptides?", d.get('stacking', f'{p} can be combined with complementary compounds.')),
        (f"Where can you buy {p}?", f"{p} is available as a research chemical from vetted suppliers with third-party COA testing."),
        (f"How long does it take {p} to work?", f"Initial effects may be noticed within 1-2 weeks, with more significant results typically appearing by weeks 4-8 of a {d['cycle_length']} cycle."),
        (f"What makes {p} unique?", d.get('unique_angle', f'{p} has a distinctive mechanism and application profile.')),
    ]
    sections = []
    sections.append(f'<h2 id="faq-list">Frequently Asked Questions About {p}</h2>')
    for q, a in faqs:
        sections.append(f'''<h3>{q}</h3>
    <p>{a}</p>''')
    sections.append(_related_reading(p, d, "faq"))
    return "\n\n    ".join(sections)


def build_storage_body(p, d):
    sections = []
    sections.append(_section("overview", f"How Do You Store {p}?",
        f"Proper storage is critical for maintaining {p}'s potency and safety. As a {d['class']}, {p} is sensitive to heat, light, and moisture — improper storage can render it ineffective or harmful.",
    ))
    sections.append(_section("lyophilized", f"How Do You Store Lyophilized {p}?",
        f"<strong>Unreconstituted (freeze-dried) {p}:</strong> Store at -20°C (standard freezer) for maximum shelf life of 12-24+ months. Keep the vial sealed and away from moisture.",
        f"Room temperature storage is acceptable for short periods (shipping) but degrades potency over weeks. Refrigerator (2-8°C) storage extends this to several months."
    ))
    sections.append(_section("reconstituted", f"How Do You Store Reconstituted {p}?",
        f"<strong>After mixing with bacteriostatic water:</strong> Store at 2-8°C (standard refrigerator). Use within 4-6 weeks for optimal potency.",
        f"<strong>Never freeze reconstituted {p}.</strong> Freezing and thawing damages the peptide structure. The bacteriostatic water's benzyl alcohol preservative is what allows the 4-6 week window — sterile water would give you only days.",
        f"Keep the vial upright and away from the refrigerator door (temperature fluctuations from opening/closing)."
    ))
    sections.append(_section("signs", f"How Do You Know if {p} Has Gone Bad?",
        f"Reconstituted {p} should be clear and colorless. If you see cloudiness, particles, or discoloration — discard it. These indicate bacterial contamination or peptide degradation.",
        f"If stored properly, degradation is gradual and may not be visually apparent. This is why the 4-6 week window for reconstituted peptides exists."
    ))
    sections.append(_section("travel", f"Can You Travel With {p}?",
        f"Lyophilized {p} can be shipped with cold packs and insulation. For short trips, a small cooler bag with an ice pack maintains adequate temperature.",
        f"Reconstituted {p} is more temperature-sensitive and should be kept refrigerated during travel if possible."
    ))
    sections.append(_section("bottom-line", f"Bottom Line on {p} Storage",
        f"Freeze-dried: -20°C, sealed, 12+ months. Reconstituted: 2-8°C, use within 4-6 weeks, never freeze. Source from vendors who ship with proper cold-chain packaging."
    ))
    sections.append(_related_reading(p, d, "storage"))
    return "\n\n    ".join(sections)


def build_legal_body(p, d):
    sections = []
    sections.append(_section("overview", f"Is {p} Legal?",
        f"<strong>{d['legal_status']}</strong>",
        f"The legal landscape for peptides like {p} is nuanced and varies by jurisdiction. This guide covers the current regulatory status and what researchers need to know."
    ))
    sections.append(_section("us-status", f"What Is the Legal Status of {p} in the United States?",
        f"{p} is generally available as a research chemical in the US. It is not FDA-approved for human use, which means it cannot be marketed, sold, or prescribed as a drug or supplement.",
        f"However, research chemicals can be legally purchased for laboratory, in vitro, or educational use. The key legal distinction is between personal research use and human consumption — the latter is not approved."
    ))
    sections.append(_section("international", f"Is {p} Legal Internationally?",
        f"Peptide regulations vary significantly by country. Some jurisdictions classify peptides as prescription-only compounds, while others allow research chemical sales similar to the US.",
        f"<strong>Australia:</strong> Most peptides require a prescription. <strong>UK:</strong> Generally available for research. <strong>Canada:</strong> Research chemical status. <strong>EU:</strong> Varies by country. Always check local regulations before purchasing."
    ))
    sections.append(_section("athletic", f"Is {p} Banned in Sports?",
        f"{'WADA (World Anti-Doping Agency) has banned ' + p + ' in athletic competition.' if 'WADA' in d['legal_status'] or 'banned' in d['legal_status'].lower() else p + ' may be subject to anti-doping regulations depending on its class and mechanism. Athletes should check the current WADA prohibited list.'}",
        f"If you compete in any organized sport, assume all peptides are prohibited unless you have confirmed otherwise with your sport's governing body."
    ))
    sections.append(_section("future", f"How Is the Legal Landscape Changing?",
        f"Peptide regulation is an evolving area. The FDA has increased scrutiny of compounding pharmacies and research chemical vendors in recent years. Some peptides that were freely available have faced new restrictions.",
        f"Staying informed about regulatory changes is important for researchers working with {p} and similar compounds."
    ))
    sections.append(_section("bottom-line", f"Bottom Line on {p} Legality",
        f"{d['legal_status']} Researchers should ensure compliance with their local laws and use {p} only for legitimate research purposes."
    ))
    sections.append(_related_reading(p, d, "legal"))
    return "\n\n    ".join(sections)


def build_condition_body(p, d, title):
    """Condition-specific article: peptide + specific use case."""
    condition = "this application"
    for word in ["healing", "weight loss", "fat loss", "muscle growth", "muscle", "hair growth",
                 "hair", "anti-aging", "aging", "skin", "gut health", "gut", "sleep",
                 "brain health", "brain", "cognitive", "anxiety", "depression", "inflammation",
                 "joint pain", "joint", "tendon", "energy", "immune", "libido", "sexual health",
                 "tanning", "pain relief", "pain", "neuroprotection", "cardiac", "heart"]:
        if word in title.lower():
            condition = word
            break
    sections = []
    sections.append(_section("overview", f"Can {p} Help With {condition.title()}?",
        f"{p} ({d['full_name']}) is being researched for {condition} applications based on its mechanism as a {d['class']}.",
        f"{d['mechanism']}"
    ))
    sections.append(_section("research", f"What Does the Research Show for {p} and {condition.title()}?",
        f"{d['research_summary']}",
        f"The relevance to {condition} specifically comes from {p}'s effects on {d['key_benefits']}."
    ))
    sections.append(_section("protocol", f"What Protocol Is Used for {condition.title()}?",
        f"For {condition} applications, the standard {p} protocol is {d['dosage_range']} administered {d['frequency']} via {d['route']} for {d['cycle_length']}.",
        f"Some researchers adjust dosing based on the specific {condition} application — see our <a href='/{slugify(p)}-dosage.html'>{p} dosage guide</a> for full protocol details."
    ))
    sections.append(_section("stacking", f"Can Stacking Improve {condition.title()} Results?",
        f"{d.get('stacking', f'{p} may be combined with complementary compounds for enhanced {condition} effects.')}",
    ))
    sections.append(_section("side-effects", f"What Side Effects Apply to {condition.title()} Use?",
        f"{d['side_effects']}",
        f"Side effects are generally consistent regardless of the specific application. See our <a href='/{slugify(p)}-side-effects.html'>{p} side effects guide</a> for details."
    ))
    sections.append(_calc_cta(p))
    sections.append(_section("bottom-line", f"Bottom Line: {p} for {condition.title()}",
        f"{p} shows {'promising' if 'promising' in d['research_summary'].lower() else 'preliminary'} research potential for {condition}. Standard protocols ({d['dosage_range']}, {d['frequency']}, {d['cycle_length']}) apply.",
        f"Source from COA-tested vendors and maintain consistent dosing for the full cycle duration."
    ))
    sections.append(_related_reading(p, d, "condition"))
    return "\n\n    ".join(sections)


def build_guide_body(p, d):
    """Comprehensive guide — the default catch-all for generic or unlabeled articles."""
    sections = []
    sections.append(_section("what-is", f"What Is {p}?",
        f"{p} ({d['full_name']}) is a {d['class']}. {d['origin']}. Also known as {d['aka']}, it has been studied for its potential effects on {d['key_benefits']}.",
        f"{d.get('unique_angle', '')} In the research community, {p} has gained attention for its distinctive profile."
    ))
    sections.append(_section("mechanism", f"How Does {p} Work?",
        f"{d['mechanism']}",
        f"This multi-pathway activity helps explain why {p} shows potential across several different applications."
    ))
    sections.append(_section("research", f"What Does the Research Say About {p}?",
        f"{d['research_summary']}",
        f"Researchers should consult the latest peer-reviewed literature for the most current findings."
    ))
    sections.append(_section("dosing", f"What Is the Recommended {p} Dosage?",
        f"Standard {p} dosing: <strong>{d['dosage_range']}</strong>, administered <strong>{d['frequency']}</strong> via <strong>{d['route']}</strong>.",
        f"Half-life: {d['half_life']}. Cycle length: {d['cycle_length']}.",
        f"Use our <a href='/peptide-calculator.html'>peptide dosing calculator</a> for exact reconstitution ratios."
    ))
    sections.append(_calc_cta(p))
    sections.append(_section("side-effects", f"What Are the Side Effects of {p}?",
        f"{d['side_effects']}",
        f"{p} is {d['legal_status'].lower()}"
    ))
    sections.append(_section("stacking", f"Can You Stack {p} With Other Peptides?",
        f"{d.get('stacking', f'{p} can be combined with complementary compounds for enhanced effects.')}",
    ))
    sections.append(_section("bottom-line", f"What Is the Bottom Line on {p}?",
        f"{p} is a {d['class']} researched for {d['key_benefits']}. Standard protocols use {d['dosage_range']} {d['frequency']} for {d['cycle_length']}.",
        f"Source from COA-tested vendors. Read our <a href='/peptide-beginners-guide.html'>beginner's guide</a> for more, or use the <a href='/peptide-calculator.html'>dosing calculator</a> to plan your protocol."
    ))
    sections.append(_related_reading(p, d, "guide"))
    return "\n\n    ".join(sections)


# ============================================================
# COMPARISON & ROUNDUP BODY BUILDERS
# ============================================================

def build_comparison_body(peptide_str, title):
    """Build comparison article body for two peptides."""
    parts = peptide_str.split(" vs ")
    if len(parts) != 2:
        return build_roundup_body(peptide_str, title)
    p1, p2 = parts[0].strip(), parts[1].strip()
    d1 = get_peptide(p1)
    d2 = get_peptide(p2)
    if not d1:
        d1 = {k: DEFAULT_PEPTIDE_DATA.get(k, "Data not available") for k in ["mechanism","research_summary","side_effects","legal_status","key_benefits","dosage_range","frequency","route","half_life","cycle_length","class","full_name","origin","aka","stacking","unique_angle"]}
        d1.update({"full_name": p1, "class": "research peptide", "origin": "Synthetic peptide", "aka": p1, "key_benefits": "various applications", "dosage_range": "varies", "frequency": "varies", "route": "varies", "half_life": "varies", "cycle_length": "varies"})
    if not d2:
        d2 = dict(d1)
        d2.update({"full_name": p2, "aka": p2})

    sections = []
    sections.append(_section("overview", f"What Are {p1} and {p2}?",
        f"<strong>{p1}</strong> ({d1.get('full_name', p1)}) is a {d1.get('class', 'research peptide')}. {d1.get('origin', '')}. It is researched for {d1.get('key_benefits', 'various applications')}.",
        f"<strong>{p2}</strong> ({d2.get('full_name', p2)}) is a {d2.get('class', 'research peptide')}. {d2.get('origin', '')}. It is researched for {d2.get('key_benefits', 'various applications')}.",
        f"While both are popular research peptides, they work through fundamentally different mechanisms and serve different primary purposes."
    ))
    sections.append(_section("mechanisms", f"How Do {p1} and {p2} Work Differently?",
        f"<strong>{p1} mechanism:</strong> {d1.get('mechanism', 'Research ongoing.')}",
        f"<strong>{p2} mechanism:</strong> {d2.get('mechanism', 'Research ongoing.')}",
        f"These distinct mechanisms are why the two peptides are often used for different research goals — or combined to target multiple pathways."
    ))
    sections.append(_section("dosing", f"How Do the Dosing Protocols Compare?",
        f"<strong>{p1}:</strong> {d1.get('dosage_range', 'varies')} administered {d1.get('frequency', 'varies')} via {d1.get('route', 'varies')}. Half-life: {d1.get('half_life', 'varies')}. Cycle: {d1.get('cycle_length', 'varies')}.",
        f"<strong>{p2}:</strong> {d2.get('dosage_range', 'varies')} administered {d2.get('frequency', 'varies')} via {d2.get('route', 'varies')}. Half-life: {d2.get('half_life', 'varies')}. Cycle: {d2.get('cycle_length', 'varies')}.",
        f"Use our <a href='/peptide-calculator.html'>peptide calculator</a> for reconstitution math for either compound."
    ))
    sections.append(_section("benefits", f"How Do the Benefits Compare?",
        f"<strong>{p1} benefits:</strong> {d1.get('key_benefits', 'various')}.",
        f"<strong>{p2} benefits:</strong> {d2.get('key_benefits', 'various')}.",
        f"The overlap in benefits determines whether these peptides compete for the same use case or complement each other in a stack."
    ))
    sections.append(_section("side-effects", f"How Do the Side Effects Compare?",
        f"<strong>{p1}:</strong> {d1.get('side_effects', DEFAULT_PEPTIDE_DATA['side_effects'])}",
        f"<strong>{p2}:</strong> {d2.get('side_effects', DEFAULT_PEPTIDE_DATA['side_effects'])}"
    ))
    sections.append(_section("stacking", f"Can You Stack {p1} and {p2} Together?",
        f"Many researchers combine {p1} and {p2} in stacking protocols. The different mechanisms mean they can potentially provide complementary effects without competing for the same receptors.",
        f"{d1.get('stacking', '')} See our <a href='/peptide-cycling-guide.html'>stacking guide</a> for general principles."
    ))
    sections.append(_section("verdict", f"Which Is Better: {p1} or {p2}?",
        f"There is no universal answer. {p1} may be preferable for researchers focused on {d1.get('key_benefits', 'its primary applications').split(',')[0].strip()}, while {p2} is stronger for {d2.get('key_benefits', 'its primary applications').split(',')[0].strip()}.",
        f"For the most comprehensive results, many researchers combine both. Review each compound's individual guide for detailed protocols: <a href='/{slugify(p1)}-guide.html'>{p1}</a> | <a href='/{slugify(p2)}-guide.html'>{p2}</a>."
    ))
    return "\n\n    ".join(sections)


def build_roundup_body(peptide_str, title):
    """Build roundup article for multiple peptides in a category."""
    # Try to identify which peptides belong in this roundup from the title
    category = "research"
    for cat in ["healing", "weight loss", "fat loss", "muscle", "hair", "anti-aging",
                "skin", "sleep", "brain", "cognitive", "immune", "growth hormone",
                "longevity", "anxiety", "tanning", "sexual health", "libido", "energy"]:
        if cat in title.lower():
            category = cat
            break

    # Find peptides relevant to this category
    relevant = []
    for name, d in PEPTIDE_DATA.items():
        benefits = d.get("key_benefits", "").lower()
        if category.lower() in benefits or category.lower() in d.get("class", "").lower():
            relevant.append((name, d))
    if len(relevant) < 3:
        # Include top peptides by default
        for name in ["BPC-157", "TB-500", "CJC-1295", "Ipamorelin", "GHK-Cu"]:
            if name in PEPTIDE_DATA and not any(r[0] == name for r in relevant):
                relevant.append((name, PEPTIDE_DATA[name]))
    relevant = relevant[:8]

    sections = []
    sections.append(_section("overview", f"What Are the Best Peptides for {category.title()}?",
        f"This guide ranks the top research peptides for {category} based on current evidence, safety profiles, and practical considerations.",
        f"Each compound below has been evaluated on its mechanism of action, research depth, ease of use, and availability from quality sources."
    ))

    for i, (name, d) in enumerate(relevant):
        sections.append(_section(f"peptide-{i+1}", f"#{i+1}: {name} — {d.get('full_name', name)}",
            f"{name} is a {d.get('class', 'research peptide')} researched for {d.get('key_benefits', 'various applications')}.",
            f"<strong>Mechanism:</strong> {d.get('mechanism', 'Research ongoing.')[:200]}",
            f"<strong>Dosage:</strong> {d.get('dosage_range', 'varies')} {d.get('frequency', '')} via {d.get('route', 'injection')}. <strong>Cycle:</strong> {d.get('cycle_length', 'varies')}.",
            f"<strong>Why it made the list:</strong> {d.get('unique_angle', 'Strong research base.')} <a href='/{slugify(name)}-guide.html'>Read the full {name} guide &rarr;</a>"
        ))

    sections.append(_section("stacking", f"Can You Combine Multiple {category.title()} Peptides?",
        f"Stacking complementary peptides for {category} is a common research approach. The key is combining compounds with different mechanisms to target multiple pathways without overlapping side effects.",
        f"See our <a href='/peptide-cycling-guide.html'>stacking and cycling guide</a> for principles on combining peptides safely."
    ))
    sections.append(_section("getting-started", f"How to Get Started",
        f"For beginners, start with a single, well-researched peptide rather than a complex stack. Use our <a href='/peptide-calculator.html'>dosing calculator</a> for reconstitution math and our <a href='/peptide-beginners-guide.html'>beginner's guide</a> for step-by-step instructions.",
        f"Source from vendors with third-party COA testing — quality is the most important factor in achieving consistent research results."
    ))
    return "\n\n    ".join(sections)


# ============================================================
# BODY CONTENT ROUTER
# ============================================================

def build_body(peptide, pdata, angle, article_type, title, keyword, vendors_str):
    """Route to the correct angle-specific body builder."""
    if article_type == "Comparison":
        return build_comparison_body(peptide, title)
    if article_type == "Roundup":
        return build_roundup_body(peptide, title)

    # Must have peptide data for angle-specific content
    if not pdata:
        # Build minimal fallback
        pdata = dict(DEFAULT_PEPTIDE_DATA)
        pdata.update({
            "full_name": peptide, "aka": peptide, "class": "research peptide",
            "origin": "Synthetic peptide under investigation",
            "key_benefits": "various research applications",
            "dosage_range": "varies by application",
            "frequency": "per protocol",
            "route": "subcutaneous injection",
            "half_life": "varies",
            "cycle_length": "4-12 weeks (varies)",
            "stacking": f"{peptide} can be combined with complementary compounds.",
            "unique_angle": "",
        })

    builders = {
        "dosage": lambda: build_dosage_body(peptide, pdata),
        "benefits": lambda: build_benefits_body(peptide, pdata),
        "side-effects": lambda: build_side_effects_body(peptide, pdata),
        "before-after": lambda: build_before_after_body(peptide, pdata),
        "results-timeline": lambda: build_results_timeline_body(peptide, pdata),
        "half-life": lambda: build_half_life_body(peptide, pdata),
        "reconstitution": lambda: build_reconstitution_body(peptide, pdata),
        "cycle": lambda: build_cycle_body(peptide, pdata),
        "stacking": lambda: build_stacking_body(peptide, pdata),
        "beginners": lambda: build_beginners_body(peptide, pdata),
        "mechanism": lambda: build_mechanism_body(peptide, pdata),
        "research": lambda: build_research_body(peptide, pdata),
        "where-to-buy": lambda: build_where_to_buy_body(peptide, pdata),
        "injection": lambda: build_injection_body(peptide, pdata),
        "women": lambda: build_gender_body(peptide, pdata, "women"),
        "men": lambda: build_gender_body(peptide, pdata, "men"),
        "reviews": lambda: build_reviews_body(peptide, pdata),
        "faq": lambda: build_faq_body(peptide, pdata),
        "storage": lambda: build_storage_body(peptide, pdata),
        "legal": lambda: build_legal_body(peptide, pdata),
        "condition": lambda: build_condition_body(peptide, pdata, title),
        "guide": lambda: build_guide_body(peptide, pdata),
    }

    builder = builders.get(angle, builders["guide"])
    return builder()


# ============================================================
# FAQ SCHEMA BUILDER — angle-specific FAQ answers
# ============================================================

def build_faq_answers(peptide, pdata, angle, title):
    """Generate angle-specific FAQ answers for JSON-LD schema."""
    if not pdata:
        return {
            "FAQ_ANSWER_1": f"{peptide} is a research peptide being studied for various potential biological applications.",
            "FAQ_ANSWER_2": f"Dosage protocols for {peptide} vary. Consult current literature for dosing information.",
            "FAQ_ANSWER_3": DEFAULT_PEPTIDE_DATA["side_effects"],
            "FAQ_ANSWER_4": f"Research on {peptide} is ongoing. It is not FDA-approved for human use.",
        }
    p = peptide
    d = pdata
    return {
        "FAQ_ANSWER_1": f"{p} ({d.get('full_name', p)}) is a {d.get('class', 'research peptide')}. {d.get('origin', '')}. It is researched for {d.get('key_benefits', 'various applications')}.",
        "FAQ_ANSWER_2": f"Common dosages: {d.get('dosage_range', 'varies')} administered {d.get('frequency', 'per protocol')} via {d.get('route', 'injection')}. Cycle length: {d.get('cycle_length', 'varies')}. Half-life: {d.get('half_life', 'varies')}.",
        "FAQ_ANSWER_3": d.get("side_effects", DEFAULT_PEPTIDE_DATA["side_effects"]),
        "FAQ_ANSWER_4": f"{p} has shown a {'favorable' if 'well-tolerated' in d.get('side_effects','').lower() else 'preliminary'} safety profile in research. {d.get('legal_status', DEFAULT_PEPTIDE_DATA['legal_status'])} All research should follow appropriate safety protocols.",
    }


# ============================================================
# META DESCRIPTION — angle-specific, under 160 chars
# ============================================================

def build_meta_desc(peptide, pdata, angle, title):
    """Build an angle-specific meta description under 160 chars."""
    p = peptide
    if not pdata:
        desc = f"{title} — Research-backed guide from WolveStack."
        return desc[:157] + "..." if len(desc) > 160 else desc

    descs = {
        "dosage": f"{p} dosage: {pdata['dosage_range']} {pdata['frequency']}. Cycle length, timing, reconstitution guide.",
        "benefits": f"{p} benefits include {pdata['key_benefits'][:60]}. Evidence-based research guide.",
        "side-effects": f"{p} side effects, safety data, and risk mitigation. What researchers need to know.",
        "before-after": f"{p} results timeline: what to expect week by week over a {pdata['cycle_length']} cycle.",
        "results-timeline": f"{p} results: week-by-week timeline of effects over {pdata['cycle_length']}.",
        "half-life": f"{p} half-life is {pdata['half_life']}. How it affects dosing frequency and timing.",
        "reconstitution": f"How to reconstitute {p}: step-by-step mixing guide with bacteriostatic water.",
        "cycle": f"{p} cycle guide: {pdata['cycle_length']} protocol structure with dosing and timing.",
        "stacking": f"Best {p} stacks for synergistic results. Combination protocols and dosing.",
        "beginners": f"{p} beginner's guide: what it is, how to use it, dosing, and first cycle setup.",
        "mechanism": f"How {p} works: mechanism of action, biological pathways, and research evidence.",
        "research": f"{p} research: clinical studies, evidence summary, and current findings.",
        "where-to-buy": f"Where to buy {p}: vetted vendors with COA testing, quality criteria, red flags.",
        "injection": f"How to inject {p}: technique, needle size, site selection, and preparation steps.",
        "women": f"{p} for women: dosing, benefits, safety considerations, and protocol adjustments.",
        "men": f"{p} for men: dosing protocols, benefits, and what to expect from research.",
        "reviews": f"{p} reviews: researcher reports, community feedback, and real-world results.",
        "faq": f"{p} FAQ: answers to the most common questions about dosing, safety, and use.",
        "storage": f"How to store {p}: temperature, shelf life, and stability for powder and solution.",
        "legal": f"Is {p} legal? Current regulatory status, sports bans, and jurisdictional rules.",
    }
    desc = descs.get(angle, f"{title} — Research-backed guide from WolveStack.")
    if len(desc) > 160:
        desc = desc[:157] + "..."
    return desc


# ============================================================
# MAIN ARTICLE GENERATOR
# ============================================================

def load_template():
    with open(TEMPLATE_FILE) as f:
        return f.read()

def load_matrix():
    with open(MATRIX_FILE) as f:
        return json.load(f)


def generate_article(article_data, template):
    """Generate a complete HTML article from template + article data."""
    peptide = article_data["peptide"]
    title = article_data["title"]
    filename = article_data["filename"]
    category = article_data["category"]
    keyword = article_data["primary_keyword"]
    article_type = article_data["type"]
    vendors = article_data.get("vendors", "")

    # Detect angle and get peptide data
    angle = detect_angle(filename, title)
    pdata = get_peptide(peptide)

    # Build meta description
    meta_desc = build_meta_desc(peptide, pdata, angle, title)

    # Reading time
    read_time = reading_time(angle, article_type)

    # Quick answer
    if pdata:
        quick_answer = quick_answer_for(peptide, pdata, angle, title)
    elif article_type == "Comparison" and " vs " in peptide:
        parts = peptide.split(" vs ")
        p1d = get_peptide(parts[0].strip())
        p2d = get_peptide(parts[1].strip())
        quick_answer = (f"<strong>{parts[0].strip()}</strong> and <strong>{parts[1].strip()}</strong> "
                       f"are both popular research peptides that work through different mechanisms. "
                       f"{parts[0].strip()} is a {p1d['class'] if p1d else 'research peptide'} focused on "
                       f"{p1d['key_benefits'].split(',')[0].strip() if p1d else 'various applications'}, "
                       f"while {parts[1].strip()} is a {p2d['class'] if p2d else 'research peptide'} targeting "
                       f"{p2d['key_benefits'].split(',')[0].strip() if p2d else 'various applications'}.")
    elif article_type == "Roundup":
        quick_answer = (f"The best peptides for this category have been ranked based on research evidence, "
                       f"safety profiles, and practical considerations. This guide covers the top compounds "
                       f"with specific dosing protocols and evidence summaries for each.")
    else:
        quick_answer = (f"<strong>{peptide}</strong> is a research peptide being studied for various potential "
                       f"biological effects. This guide covers the latest research, protocols, and practical "
                       f"considerations.")

    # Build the HTML from template
    html = template

    # Replace all template variables
    replacements = {
        "{{TITLE}}": title,
        "{{META_DESCRIPTION}}": esc(meta_desc),
        "{{META_DESCRIPTION_SHORT}}": esc(meta_desc[:120]),
        "{{FILENAME}}": filename,
        "{{CATEGORY}}": category,
        "{{CATEGORY_TAG}}": category.upper(),
        "{{PEPTIDE_NAME}}": peptide,
        "{{H1_TITLE}}": title.split(":")[0] if ":" in title else title,
        "{{HERO_SUBTITLE}}": title.split(":", 1)[1].strip() if ":" in title else f"Research-backed guide to {peptide} from WolveStack.",
        "{{READ_TIME}}": read_time,
        "{{DATE_PUBLISHED}}": DATE_TODAY,
        "{{DATE_MODIFIED}}": DATE_TODAY,
        "{{QUICK_ANSWER}}": quick_answer,
    }

    for key, val in replacements.items():
        html = html.replace(key, val)

    # Build angle-specific body content
    body_content = build_body(peptide, pdata, angle, article_type, title, keyword, vendors)

    # Replace the body section
    body_marker_start = '<!-- GEO: Use question-format H2 headers that mirror how people ask AI -->'
    body_marker_end = '<!-- Affiliate CTA -->'

    start_idx = html.find(body_marker_start)
    end_idx = html.find(body_marker_end)

    if start_idx != -1 and end_idx != -1:
        html = html[:start_idx] + body_content + "\n\n    " + html[end_idx:]

    # Replace affiliate CTA vendor links
    vlinks = vendor_links_html(peptide, pdata if pdata else {}, vendors)
    # Replace the default vendor link in the template
    default_link = f'<p><a href="https://www.ascensionresearch.co/?ref=wolvestack" target="_blank" rel="nofollow sponsored">Ascension Research → Browse {peptide}</a></p>'
    html = html.replace(default_link, vlinks)
    # Also try the unicode arrow version
    default_link2 = f'<p><a href="https://www.ascensionresearch.co/?ref=wolvestack" target="_blank" rel="nofollow sponsored">Ascension Research &rarr; Browse {peptide}</a></p>'
    if default_link2 in html:
        html = html.replace(default_link2, vlinks)

    # Replace FAQ schema answers
    faq_answers = build_faq_answers(peptide, pdata, angle, title)
    for key, val in faq_answers.items():
        html = html.replace("{{" + key + "}}", esc(val))

    # Calculator CTA (add before affiliate CTA if not already in body)
    if '/peptide-calculator.html' not in body_content:
        calc_cta = _calc_cta(peptide)
        html = html.replace('<!-- Affiliate CTA -->', calc_cta + '\n\n    <!-- Affiliate CTA -->')

    return html


# ============================================================
# MAIN
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, default=0, help="Generate only first N articles")
    parser.add_argument("--tier", type=int, default=0, help="Only tier T")
    parser.add_argument("--type", type=str, default="", help="Only this type")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="store_true", default=True, help="Overwrite existing files (default: True)")
    parser.add_argument("--no-overwrite", action="store_true", help="Skip existing files")
    args = parser.parse_args()

    template = load_template()
    articles = load_matrix()

    # Filter
    if args.tier:
        articles = [a for a in articles if a["tier"] == args.tier]
    if args.type:
        articles = [a for a in articles if a["type"].lower() == args.type.lower()]

    # Skip existing only if explicitly requested
    if args.no_overwrite:
        articles = [a for a in articles if not os.path.exists(os.path.join(OUTPUT_DIR, a["filename"]))]

    if args.batch:
        articles = articles[:args.batch]

    print(f"Generating {len(articles)} articles (v2.0 — angle-specific content)...")
    print(f"Knowledge base: {len(PEPTIDE_DATA)} peptides loaded")

    if args.dry_run:
        for a in articles:
            angle = detect_angle(a["filename"], a["title"])
            has_data = "✓" if get_peptide(a["peptide"]) else "○"
            print(f"  [{has_data}] [{angle:16s}] {a['filename']}")
        return

    created = 0
    errors = 0
    for i, article in enumerate(articles):
        try:
            html = generate_article(article, template)
            outpath = os.path.join(OUTPUT_DIR, article["filename"])
            with open(outpath, 'w') as f:
                f.write(html)
            created += 1
            if (i + 1) % 100 == 0:
                print(f"  ...{i+1}/{len(articles)} done")
        except Exception as e:
            errors += 1
            print(f"  ERROR: {article['filename']}: {e}")
            if errors > 10:
                print("Too many errors, stopping.")
                break

    print(f"\nDone! Created {created} articles. Errors: {errors}")


if __name__ == "__main__":
    main()
