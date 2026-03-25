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
LONGTAIL_MATRIX_FILE = os.path.join(SCRIPT_DIR, "longtail-articles-todo.json")
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

def detect_angle(filename, title, article_type=""):
    """Detect the article angle from filename, title, and article type."""
    fn = filename.lower()
    tl = title.lower()

    # Long-tail type overrides — check article_type first
    if article_type == "Condition-Specific":
        return "condition-specific"
    if article_type == "Single Peptide" and "-and-" in fn:
        return "interaction"

    # Comparison: peptide vs mainstream treatment (not peptide vs peptide)
    if article_type == "Comparison" and "-vs-" in fn:
        return "vs-treatment"

    for angle, patterns in ANGLE_PATTERNS:
        for p in patterns:
            if p in fn or p in tl:
                return angle
    # Condition-specific detection (general categories)
    for condition in ["healing", "weight-loss", "fat-loss", "muscle", "hair",
                      "anti-aging", "aging", "skin", "gut", "sleep", "brain",
                      "cognitive", "anxiety", "depression", "inflammation",
                      "joint", "tendon", "energy", "immune", "libido", "sexual",
                      "tanning", "pain", "neuroprotection", "cardio", "cardiac"]:
        if condition in fn:
            return "condition"
    return "guide"  # default comprehensive guide angle


def extract_condition(filename, peptide):
    """Extract the specific condition/injury from a condition-specific filename."""
    slug = slugify(peptide)
    # e.g. bpc-157-for-rotator-cuff.html → rotator cuff
    suffix = filename.replace(".html", "").replace(slug + "-for-", "")
    return suffix.replace("-", " ").strip().title()


def extract_interacting_substance(filename, peptide):
    """Extract the drug/supplement from an interaction filename."""
    slug = slugify(peptide)
    # e.g. bpc-157-and-ibuprofen.html → Ibuprofen
    suffix = filename.replace(".html", "").replace(slug + "-and-", "")
    return suffix.replace("-", " ").strip().title()


def extract_treatment(filename, peptide):
    """Extract the mainstream treatment from a vs-treatment filename."""
    slug = slugify(peptide)
    # e.g. bpc-157-vs-cortisone-injection.html → Cortisone Injection
    suffix = filename.replace(".html", "").replace(slug + "-vs-", "")
    return suffix.replace("-", " ").strip().title()


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
        "condition-specific": "9", "interaction": "8", "vs-treatment": "10",
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
    elif angle == "condition-specific":
        condition = extract_condition(title.lower().replace(" ", "-").replace(":", ""), p)
        if condition == "various applications":
            # Fallback: parse from title
            parts = title.split(" for ", 1)
            condition = parts[1].split(":")[0].strip() if len(parts) > 1 else "this condition"
        return (f"<strong>{p}</strong> is being actively researched for <strong>{condition.lower()}</strong>. "
                f"{pdata['mechanism'][:150]}. "
                f"Researchers typically use {pdata['dosage_range']} {pdata['frequency']} via {pdata['route']} for this application, "
                f"with cycles running {pdata['cycle_length']}.")
    elif angle == "interaction":
        # Extract the interacting substance from the title
        parts = title.split(" and ", 1)
        substance = parts[1].split(":")[0].strip() if len(parts) > 1 else "this substance"
        return (f"Combining <strong>{p}</strong> with <strong>{substance}</strong> is a common question in the research community. "
                f"While direct interaction studies are limited, understanding each compound's mechanism helps assess compatibility. "
                f"{p} works as a {pdata['class']} while {substance} operates through its own pathways — the key concern is whether they interfere, compete, or complement each other.")
    elif angle == "vs-treatment":
        parts = title.split(" vs ", 1)
        treatment = parts[1].split(":")[0].strip() if len(parts) > 1 else "this treatment"
        return (f"<strong>{p}</strong> and <strong>{treatment}</strong> represent different approaches to the same underlying problem. "
                f"{treatment} is an established mainstream option, while {p} is a research compound — {pdata['class']} — studied for "
                f"{pdata['key_benefits'].split(',')[0].strip()}. This guide compares their mechanisms, evidence, costs, and practical considerations.")
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


def build_condition_specific_body(p, d, title, filename):
    """CONDITION-SPECIFIC long-tail: peptide + specific injury/condition (e.g. BPC-157 for Rotator Cuff)."""
    condition = extract_condition(filename, p)
    condition_lower = condition.lower()
    # Build a knowledge-based body section about the specific injury + peptide
    sections = []

    sections.append(_section("overview", f"Can {p} Help With {condition}?",
        f"{condition} is a common issue that affects millions of people annually. Standard treatments range from rest and physical therapy to medication and surgery, depending on severity. <strong>{p}</strong>, a {d['class']}, has attracted research interest for this specific application because of its mechanism of action.",
        f"{d['mechanism']}",
        f"The question researchers ask is whether these mechanisms translate to meaningful outcomes for {condition_lower} specifically. Below, we examine the evidence."
    ))

    sections.append(_section("how-it-works", f"How Might {p} Address {condition}?",
        f"To understand why {p} is being investigated for {condition_lower}, consider what's happening at the tissue level. {condition} typically involves damage to connective tissue, inflammation, and impaired healing — all areas where {p}'s mechanism is relevant.",
        f"{p} ({d['full_name']}) is known for its effects on {d['key_benefits']}. For {condition_lower}, the most relevant pathways include promoting angiogenesis (new blood vessel formation), modulating inflammatory signaling, and supporting tissue remodeling.",
        f"Unlike many standard treatments that address symptoms (pain, swelling), {p}'s proposed mechanism targets the underlying repair process itself — which is why it has generated interest among researchers looking at {condition_lower} recovery."
    ))

    sections.append(_section("research", f"What Does the Research Say About {p} and {condition}?",
        f"{d['research_summary']}",
        f"While much of the published research on {p} involves general injury models rather than {condition_lower} specifically, the biological mechanisms are relevant. Studies on tendon, ligament, and soft tissue healing demonstrate effects that would logically extend to {condition_lower}.",
        f"<strong>Important caveat:</strong> most {p} studies are preclinical (animal models). Human clinical trials specific to {condition_lower} are limited or ongoing. Extrapolating from animal data requires caution — effective doses, timelines, and outcomes may differ significantly in humans."
    ))

    sections.append(_section("protocol", f"What Protocol Do Researchers Use for {condition}?",
        f"For {condition_lower} applications, researchers typically follow the standard {p} protocol: <strong>{d['dosage_range']}</strong> administered <strong>{d['frequency']}</strong> via <strong>{d['route']}</strong>.",
        f"Some protocols for localized conditions like {condition_lower} involve injecting as close to the affected area as possible (subcutaneously near the site), based on the theory that local concentration may improve outcomes. However, systemic administration (e.g., abdominal subcutaneous) is also used with reported effects.",
        f"Cycle length: <strong>{d['cycle_length']}</strong>. For {condition_lower}, some researchers extend beyond the standard cycle if improvement is ongoing but incomplete — though this should be evaluated on a case-by-case basis."
    ))

    sections.append(_calc_cta(p))

    sections.append(_section("timeline", f"What Results Timeline Can You Expect for {condition}?",
        f"Based on community reports and the general {p} research timeline, here's what researchers typically describe for {condition_lower}-related applications:",
        f"<strong>Weeks 1-2:</strong> Reduced inflammation and pain may be noticeable. The compound is building to therapeutic levels. Don't expect structural healing yet.",
        f"<strong>Weeks 3-5:</strong> The primary therapeutic window. Improvements in mobility, pain reduction, and functional recovery are most commonly reported in this phase.",
        f"<strong>Weeks 6-8+:</strong> Continued improvement for more severe or chronic cases. Some {condition_lower} cases (particularly chronic or degenerative) may require the full cycle length or even a second cycle after a washout period.",
        f"Individual results vary significantly based on severity, age, concurrent treatment (physical therapy, etc.), and the specific nature of the {condition_lower}."
    ))

    sections.append(_section("complementary", f"What Else Helps With {condition} Alongside {p}?",
        f"{d.get('stacking', f'{p} can be combined with complementary peptides for enhanced effects.')}",
        f"Beyond peptide stacking, researchers addressing {condition_lower} often combine {p} with conventional rehabilitation — physical therapy, targeted exercises, and proper rest. {p} is not a replacement for these foundational treatments but may complement them.",
        f"Nutrition also plays a role: adequate protein, vitamin C, zinc, and collagen support the tissue repair processes that {p} targets."
    ))

    sections.append(_section("side-effects", f"What Are the Side Effects and Risks?",
        f"{d['side_effects']}",
        f"For {condition_lower} applications specifically, the injection-site side effects (redness, swelling) may be slightly more noticeable when injecting near the affected area, but these typically resolve within hours.",
        f"{p} is {d['legal_status'].lower()}"
    ))

    sections.append(_section("bottom-line", f"Bottom Line: {p} for {condition}",
        f"<strong>{p}</strong> shows research potential for {condition_lower} based on its mechanism of action involving {d['key_benefits'].split(',')[0].strip()}. The standard protocol ({d['dosage_range']}, {d['frequency']}, {d['cycle_length']}) applies, with some researchers opting for local injection near the affected area.",
        f"This is a research compound — not an FDA-approved treatment. It works best as part of a comprehensive approach that includes proper rehabilitation, nutrition, and medical guidance. Source from vendors with third-party COA testing, and consult a healthcare provider before beginning any protocol."
    ))

    sections.append(_related_reading(p, d, "condition-specific"))
    return "\n\n    ".join(sections)


def build_interaction_body(p, d, title, filename):
    """INTERACTION long-tail: peptide + drug/supplement (e.g. BPC-157 and Ibuprofen)."""
    substance = extract_interacting_substance(filename, p)
    substance_lower = substance.lower()
    sections = []

    # Build detailed substance-specific knowledge
    substance_info = _get_substance_info(substance_lower)

    sections.append(_section("overview", f"Can You Use {p} and {substance} Together?",
        f"Combining <strong>{p}</strong> with <strong>{substance}</strong> is one of the most common questions in the peptide research community. The short answer: direct interaction studies between {p} and {substance_lower} are extremely limited, so most guidance comes from understanding each compound's mechanism and pharmacology.",
        f"<strong>{p}</strong> is a {d['class']}. {d['mechanism'][:200]}.",
        f"<strong>{substance}</strong> {substance_info['description']}"
    ))

    sections.append(_section("mechanisms", f"How Do {p} and {substance} Work Differently?",
        f"Understanding the mechanisms helps assess potential interactions:",
        f"<strong>{p} mechanism:</strong> {d['mechanism']}",
        f"<strong>{substance} mechanism:</strong> {substance_info['mechanism']}",
        f"The key question is whether these mechanisms conflict, compete for the same pathways, or work independently. In most cases, peptides and {substance_info['class']} operate through sufficiently different biological pathways that direct pharmacological interaction is unlikely — but this doesn't mean timing and context don't matter."
    ))

    sections.append(_section("concerns", f"What Are the Potential Concerns?",
        f"{substance_info['interaction_concern']}",
        f"From a pharmacokinetic perspective, {p} (administered via {d['route']}) and {substance_lower} (typically {substance_info['route']}) enter the body through different routes and are metabolized differently, reducing the likelihood of direct metabolic competition.",
        f"However, pharmacodynamic interactions — where two compounds affect the same biological process from different angles — are theoretically possible. For example, if both compounds affect inflammation, the combined effect could be either synergistic or counterproductive depending on timing."
    ))

    sections.append(_section("timing", f"How Should You Time {p} and {substance}?",
        f"When researchers choose to use both compounds, timing is often the primary consideration:",
        f"<strong>General principle:</strong> Separate administration by at least 30-60 minutes when possible. This reduces any potential for direct chemical interaction at the injection/absorption site.",
        f"<strong>For {substance_lower} specifically:</strong> {substance_info['timing_advice']}",
        f"The half-life of {p} is {d['half_life']}, while {substance_lower}'s effects typically last {substance_info['duration']}. Understanding these windows helps researchers plan dosing schedules that minimize overlap if desired."
    ))

    sections.append(_section("protocol", f"What Protocol Do Researchers Follow?",
        f"For {p}, the standard protocol remains: <strong>{d['dosage_range']}</strong> administered <strong>{d['frequency']}</strong> via <strong>{d['route']}</strong> for <strong>{d['cycle_length']}</strong>.",
        f"When using {substance_lower} concurrently, most researchers don't modify their {p} protocol. Instead, they maintain the standard {p} dosing and manage {substance_lower} usage according to its own guidelines.",
        f"<strong>What some researchers avoid:</strong> {substance_info['what_to_avoid']}"
    ))

    sections.append(_calc_cta(p))

    sections.append(_section("research", f"What Does the Research Say?",
        f"Direct studies examining the {p} + {substance_lower} combination are {substance_info['research_status']}. Most of what we know comes from understanding each compound independently:",
        f"<strong>{p} research:</strong> {d['research_summary']}",
        f"Without controlled studies on the combination, recommendations are based on mechanistic reasoning and community experience rather than clinical evidence. This is an important limitation to acknowledge."
    ))

    sections.append(_section("side-effects", f"What Are the Combined Side Effect Risks?",
        f"<strong>{p} side effects:</strong> {d['side_effects']}",
        f"<strong>{substance} side effects:</strong> {substance_info['side_effects']}",
        f"When combining compounds, the general principle is that side effect profiles are additive. If both compounds affect the same system (e.g., both affect GI function), the combined risk for that specific side effect may be higher than either alone."
    ))

    sections.append(_section("bottom-line", f"Bottom Line: {p} and {substance}",
        f"Direct evidence on the {p} + {substance_lower} combination is limited. Based on mechanistic analysis, {substance_info['bottom_line']}",
        f"As always, consult a qualified healthcare provider before combining any compounds. {p} is a research compound ({d['legal_status'].lower()}), and this information is for educational purposes only."
    ))

    sections.append(_related_reading(p, d, "interaction"))
    return "\n\n    ".join(sections)


def _get_substance_info(substance):
    """Get structured info about a drug/supplement for interaction articles."""
    substance_lower = substance.lower().strip()

    # Comprehensive substance database for high-quality interaction content
    substances = {
        "ibuprofen": {
            "description": "is a non-steroidal anti-inflammatory drug (NSAID) that reduces pain, fever, and inflammation by inhibiting cyclooxygenase (COX-1 and COX-2) enzymes.",
            "mechanism": "Ibuprofen blocks prostaglandin synthesis by inhibiting COX enzymes. This reduces inflammation and pain at the tissue level but also impairs some natural healing processes that depend on the inflammatory cascade.",
            "class": "NSAIDs",
            "route": "oral",
            "duration": "4-6 hours",
            "interaction_concern": "The primary theoretical concern with combining peptides and NSAIDs is that NSAIDs suppress inflammation — which is part of the body's natural healing response. Some researchers argue that suppressing inflammation during the early healing phase could reduce the effectiveness of healing-focused peptides. However, others note that excessive inflammation is itself detrimental to healing.",
            "timing_advice": "Some researchers avoid taking ibuprofen during the first 2-3 days of a peptide cycle to allow the initial inflammatory signaling to occur. After the acute phase, moderate NSAID use for pain management is generally considered acceptable.",
            "what_to_avoid": "Chronic high-dose NSAID use during peptide cycles — this creates sustained suppression of the inflammatory cascade that healing peptides rely on.",
            "research_status": "essentially non-existent as controlled studies",
            "side_effects": "GI upset, increased bleeding risk, kidney stress with chronic use, potential cardiovascular effects with long-term use.",
            "bottom_line": "the two compounds likely don't directly interfere pharmacologically, but the anti-inflammatory action of ibuprofen could theoretically reduce the effectiveness of healing-focused peptides. Many researchers use them concurrently but try to minimize NSAID use during active peptide cycles."
        },
        "nsaids": {
            "description": "are a class of anti-inflammatory drugs (including ibuprofen, naproxen, aspirin) that reduce inflammation by blocking COX enzymes.",
            "mechanism": "NSAIDs inhibit cyclooxygenase enzymes (COX-1 and COX-2), reducing prostaglandin synthesis. This lowers inflammation but also affects platelet function and GI protective mechanisms.",
            "class": "anti-inflammatory drugs",
            "route": "oral",
            "duration": "4-12 hours (varies by specific NSAID)",
            "interaction_concern": "The concern is the same as with individual NSAIDs: suppressing the inflammatory cascade may interfere with the healing processes that certain peptides target. The degree of concern depends on which NSAID, the dose, and the duration of use.",
            "timing_advice": "If using NSAIDs for pain management during a peptide cycle, consider using them only as needed (PRN) rather than on a fixed schedule. This allows natural inflammatory signaling to occur between doses.",
            "what_to_avoid": "Scheduled, high-dose NSAID regimens during the first week of a healing peptide cycle. If pain management is essential, consider acetaminophen (Tylenol) as an alternative — it provides pain relief without significant anti-inflammatory effects.",
            "research_status": "largely absent in the context of peptide combination therapy",
            "side_effects": "GI bleeding risk, kidney damage with chronic use, cardiovascular effects, impaired platelet function.",
            "bottom_line": "moderate, as-needed NSAID use during peptide cycles is common and generally considered acceptable by researchers. However, some prefer to minimize NSAID use during the initial healing phase."
        },
        "alcohol": {
            "description": "is a central nervous system depressant that affects liver metabolism, hydration, inflammation, and growth hormone secretion.",
            "mechanism": "Alcohol is metabolized primarily by the liver via alcohol dehydrogenase and CYP2E1. It impairs protein synthesis, increases systemic inflammation, suppresses growth hormone release, and dehydrates tissues.",
            "class": "recreational substances",
            "route": "oral",
            "duration": "2-6 hours (varies with amount consumed)",
            "interaction_concern": "Alcohol creates a broadly catabolic environment that opposes many of the processes peptides target. It suppresses GH release (directly counteracting GH-related peptides), impairs protein synthesis (reducing healing potential), and increases inflammation.",
            "timing_advice": "Most researchers recommend avoiding alcohol entirely during peptide cycles. If that's unrealistic, separating peptide administration and alcohol consumption by at least 3-4 hours minimizes direct interference, though systemic effects persist longer.",
            "what_to_avoid": "Heavy drinking during any peptide cycle — it fundamentally opposes the biological processes peptides are designed to enhance.",
            "research_status": "very limited in the peptide context, though the negative effects of alcohol on healing and growth hormone are well-established independently",
            "side_effects": "Liver stress, dehydration, impaired recovery, suppressed GH release, increased cortisol, systemic inflammation.",
            "bottom_line": "alcohol is generally counterproductive to peptide research goals. It suppresses GH, impairs healing, and increases inflammation. While occasional moderate consumption is unlikely to completely negate peptide effects, it does reduce their efficacy."
        },
        "creatine": {
            "description": "is a naturally occurring compound used as a supplement to enhance athletic performance, muscle strength, and cellular energy production via the phosphocreatine system.",
            "mechanism": "Creatine increases intracellular phosphocreatine stores, enabling faster ATP regeneration during high-intensity activity. It also draws water into muscle cells (cell volumization) and may support protein synthesis.",
            "class": "sports supplements",
            "route": "oral",
            "duration": "ongoing (saturated with daily dosing)",
            "interaction_concern": "There are essentially no known concerns about combining creatine with peptides. They operate through entirely different mechanisms — creatine affects energy metabolism while peptides typically affect signaling pathways. The combination is commonly used.",
            "timing_advice": "No special timing considerations. Creatine is taken daily regardless of peptide timing. Both can be used on the same day without adjustment.",
            "what_to_avoid": "No specific combination risks identified. Standard creatine usage guidelines apply (adequate hydration, standard loading/maintenance dosing).",
            "research_status": "non-existent as a specific combination, but neither compound is known to interact with the other's pathways",
            "side_effects": "Water retention, GI upset at high doses, minimal other concerns. Creatine is one of the most thoroughly researched supplements.",
            "bottom_line": "no known interaction exists. Creatine and peptides work through completely different mechanisms and are commonly used together without issues."
        },
        "caffeine": {
            "description": "is a central nervous system stimulant that blocks adenosine receptors, increases alertness, and has mild thermogenic and performance-enhancing effects.",
            "mechanism": "Caffeine blocks adenosine A1 and A2A receptors, preventing the normal sleep-promoting signal. It also increases catecholamine release and modestly boosts metabolic rate.",
            "class": "stimulants",
            "route": "oral",
            "duration": "3-7 hours (half-life ~5 hours)",
            "interaction_concern": "Minimal direct concern. Caffeine and peptides operate through different pathways. One consideration: caffeine can temporarily elevate cortisol, which could theoretically oppose some anabolic peptide effects. However, this effect is modest and transient.",
            "timing_advice": "For GH-related peptides (e.g., MK-677, CJC-1295), avoid caffeine within 1-2 hours of dosing since elevated cortisol can blunt GH release. For healing peptides, no special timing is needed.",
            "what_to_avoid": "Excessive caffeine intake (>400mg/day) during peptide cycles, as chronically elevated cortisol can impair healing and recovery.",
            "research_status": "essentially non-existent as a specific combination study",
            "side_effects": "Anxiety, insomnia, increased heart rate, GI upset, cortisol elevation with chronic high intake.",
            "bottom_line": "caffeine and peptides don't directly interact. Moderate caffeine use is fine during peptide cycles. Researchers using GH-related peptides may want to time caffeine away from peptide doses."
        },
    }

    # Return specific info if available, otherwise generate reasonable defaults
    if substance_lower in substances:
        return substances[substance_lower]

    # Intelligent defaults based on common categories
    return {
        "description": f"is a compound that may be encountered alongside peptide research. Its specific interactions with peptides have not been extensively studied.",
        "mechanism": f"{substance.title()} works through its own pharmacological pathways. Understanding the specific mechanism is important for assessing any potential interaction.",
        "class": "pharmaceutical or supplement compounds",
        "route": "varies by formulation",
        "duration": "varies",
        "interaction_concern": f"Direct interaction data between peptides and {substance_lower} is limited. The primary considerations are whether the two compounds affect overlapping biological pathways and whether they are metabolized through the same systems.",
        "timing_advice": f"As a general precaution, separating administration of {substance_lower} and peptide doses by 30-60 minutes is a reasonable approach until more data is available.",
        "what_to_avoid": f"Avoid making assumptions about safety based on the absence of reported problems. The lack of interaction data means caution is warranted.",
        "research_status": "essentially non-existent as controlled combination studies",
        "side_effects": f"Side effects of {substance_lower} should be evaluated independently. When combining with peptides, monitor for any unusual or amplified effects.",
        "bottom_line": f"insufficient data exists to make definitive claims about the {substance_lower} combination. Researchers should proceed with caution, monitor for unexpected effects, and consult healthcare professionals."
    }


def build_vs_treatment_body(p, d, title, filename):
    """VS-TREATMENT long-tail: peptide vs mainstream treatment (e.g. BPC-157 vs Cortisone)."""
    treatment = extract_treatment(filename, p)
    treatment_lower = treatment.lower()
    treatment_info = _get_treatment_info(treatment_lower)
    sections = []

    sections.append(_section("overview", f"How Do {p} and {treatment} Compare?",
        f"<strong>{p}</strong> and <strong>{treatment}</strong> represent fundamentally different approaches. {treatment} is {treatment_info['status']} — an established option with clinical data behind it. {p} is a {d['class']}, a research compound studied for {d['key_benefits']}.",
        f"This comparison isn't about declaring a winner. It's about understanding the trade-offs so researchers can make informed decisions about which approach (or combination of approaches) makes sense for their situation."
    ))

    sections.append(_section("how-they-work", f"How Do They Work Differently?",
        f"<strong>{p} mechanism:</strong> {d['mechanism']}",
        f"<strong>{treatment} mechanism:</strong> {treatment_info['mechanism']}",
        f"These are fundamentally different approaches. {treatment_info['approach_type']} while {p} {treatment_info['peptide_contrast']}."
    ))

    sections.append(_section("evidence", f"What Does the Evidence Look Like?",
        f"<strong>{treatment} evidence:</strong> {treatment_info['evidence']}",
        f"<strong>{p} evidence:</strong> {d['research_summary']}",
        f"The evidence gap is significant. {treatment} has been used in clinical settings for {treatment_info['history']}, while {p}'s evidence is primarily preclinical. This doesn't mean {p} doesn't work — it means we have less human data to draw conclusions from."
    ))

    sections.append(_section("pros-cons", f"What Are the Pros and Cons of Each?",
        f"<strong>{treatment} advantages:</strong> {treatment_info['pros']}",
        f"<strong>{treatment} disadvantages:</strong> {treatment_info['cons']}",
        f"<strong>{p} advantages:</strong> Non-invasive administration ({d['route']}), targets underlying repair mechanisms rather than just symptoms, can be self-administered, relatively low side effect profile based on available research.",
        f"<strong>{p} disadvantages:</strong> Limited human clinical data, not FDA-approved, requires sourcing from research vendors, results can be variable, typical cycle duration of {d['cycle_length']} means effects aren't immediate."
    ))

    sections.append(_section("cost", f"How Do the Costs Compare?",
        f"<strong>{treatment} cost:</strong> {treatment_info['cost']}",
        f"<strong>{p} cost:</strong> Research-grade {p} typically runs $80-150 per vial (5mg) from reputable vendors. A full {d['cycle_length']} cycle requires multiple vials plus bacteriostatic water and supplies. Total cycle cost: roughly $200-600 depending on dosage and cycle length.",
        f"Insurance typically covers {treatment_lower} but does not cover research peptides. This cost difference is significant for many people."
    ))

    sections.append(_section("combination", f"Can You Use Both Together?",
        f"Some researchers use {p} alongside conventional treatments like {treatment_lower}, treating them as complementary rather than competing approaches.",
        f"{treatment_info['combination_note']}",
        f"The logic: {treatment_lower} addresses {treatment_info['addresses']} while {p} may support {treatment_info['peptide_supports']}. Different mechanisms targeting the same problem from different angles."
    ))

    sections.append(_calc_cta(p))

    sections.append(_section("who-chooses-what", f"Who Might Choose Which Option?",
        f"<strong>{treatment} may be preferable when:</strong> {treatment_info['when_preferred']}",
        f"<strong>{p} may interest researchers who:</strong> Want to explore options beyond conventional treatment, are interested in supporting natural repair mechanisms, have tried {treatment_lower} without satisfactory results, or are looking for a lower-intervention approach.",
        f"Many people don't treat this as an either-or decision. They use {treatment_lower} for immediate needs while exploring {p} research for longer-term support."
    ))

    sections.append(_section("side-effects", f"How Do the Side Effect Profiles Compare?",
        f"<strong>{treatment} risks:</strong> {treatment_info['risks']}",
        f"<strong>{p} side effects:</strong> {d['side_effects']}",
        f"{p} is {d['legal_status'].lower()}"
    ))

    sections.append(_section("bottom-line", f"Bottom Line: {p} vs {treatment}",
        f"{treatment} is the established, evidence-backed option with {treatment_info['history']} of clinical use. {p} is a research compound with promising preclinical data but limited human evidence.",
        f"The best approach depends on your specific situation, risk tolerance, and access to medical supervision. Consult a qualified healthcare provider before making decisions about either option. This guide is for educational purposes only."
    ))

    sections.append(_related_reading(p, d, "vs-treatment"))
    return "\n\n    ".join(sections)


def _get_treatment_info(treatment):
    """Get structured info about mainstream treatments for comparison articles."""
    treatment_lower = treatment.lower().strip()

    treatments = {
        "cortisone injection": {
            "status": "an FDA-approved medical treatment",
            "mechanism": "Cortisone is a corticosteroid that powerfully suppresses inflammation at the injection site. It blocks the inflammatory cascade, reducing swelling, pain, and immune activity in the treated area.",
            "approach_type": "Cortisone addresses symptoms (pain and inflammation) directly and rapidly",
            "peptide_contrast": "aims to support underlying tissue repair processes",
            "evidence": "Decades of clinical use with extensive human data. Cortisone injections are considered standard of care for various inflammatory conditions. Effectiveness is well-documented for short-term pain relief, though long-term effects on tissue health are debated.",
            "history": "decades",
            "pros": "Rapid pain relief (often within days), covered by insurance, administered by medical professionals, extensive safety data, proven short-term efficacy.",
            "cons": "May weaken tendons and cartilage with repeated use, effects are temporary (weeks to months), doesn't address underlying tissue damage, limited to 3-4 injections per year per site, can mask injury leading to further damage.",
            "cost": "$100-500 per injection (often covered by insurance with copay of $20-75). Typically 2-4 injections per year.",
            "combination_note": "Using peptides alongside cortisone is a topic of discussion. Some researchers space them apart (cortisone first for acute relief, peptides for ongoing tissue support). The anti-inflammatory action of cortisone could theoretically interfere with healing peptides' mechanism in the short term.",
            "addresses": "immediate pain and inflammation",
            "peptide_supports": "underlying tissue repair and regeneration",
            "when_preferred": "Acute flare-ups requiring immediate relief, when a medical professional recommends it, when insurance coverage matters, when short-term symptom management is the priority.",
            "risks": "Tendon weakening with repeated injections, infection risk (rare), skin depigmentation at injection site, temporary blood sugar elevation, potential cartilage degradation with overuse."
        },
        "prp therapy": {
            "status": "an FDA-recognized regenerative treatment",
            "mechanism": "Platelet-Rich Plasma (PRP) concentrates the patient's own platelets (containing growth factors like PDGF, TGF-beta, VEGF) and injects them into the injured area to accelerate natural healing.",
            "approach_type": "PRP works with the body's own growth factors to enhance natural repair",
            "peptide_contrast": "provides exogenous signaling molecules to trigger similar pathways",
            "evidence": "Growing clinical evidence with multiple randomized controlled trials. Results vary by condition — strong evidence for certain tendon injuries, mixed evidence for joint conditions. PRP has regulatory clearance but isn't always covered by insurance.",
            "history": "15-20 years of clinical application",
            "pros": "Uses the body's own biology, growing clinical evidence base, targets repair rather than just symptoms, medical professional oversight, single or few treatments may suffice.",
            "cons": "Expensive ($500-2000 per treatment), inconsistent insurance coverage, results vary significantly, requires blood draw and processing, multiple treatments often needed, effectiveness depends on preparation technique.",
            "cost": "$500-2000+ per treatment session (rarely covered by insurance). Most conditions require 1-3 treatments.",
            "combination_note": "Some regenerative medicine practitioners combine PRP with peptide protocols, theorizing that the endogenous growth factors in PRP and the signaling effects of peptides may be complementary.",
            "addresses": "tissue healing through concentrated autologous growth factors",
            "peptide_supports": "similar healing pathways through exogenous signaling molecules",
            "when_preferred": "When regenerative (not just symptomatic) treatment is desired, when working with a sports medicine or regenerative medicine specialist, when willing to invest in out-of-pocket treatment, for specific conditions with good PRP evidence.",
            "risks": "Post-injection pain and swelling, infection risk (rare), no standardized preparation protocol (results vary between providers), limited efficacy for some conditions."
        },
        "stem cell therapy": {
            "status": "an emerging regenerative treatment",
            "mechanism": "Stem cell therapy introduces undifferentiated cells (typically mesenchymal stem cells from bone marrow or adipose tissue) to damaged areas. These cells can differentiate into needed tissue types and secrete regenerative growth factors.",
            "approach_type": "Stem cell therapy attempts to rebuild tissue through cellular replacement and paracrine signaling",
            "peptide_contrast": "aims to enhance existing repair mechanisms through molecular signaling",
            "evidence": "Promising but still developing. Some conditions show strong results in clinical trials, while others remain experimental. The field is plagued by clinics offering unproven treatments at high cost.",
            "history": "10-15 years of clinical application (research ongoing)",
            "pros": "Potential for actual tissue regeneration, addresses root cause, growing evidence for specific conditions, can treat damage beyond the body's normal repair capacity.",
            "cons": "Very expensive ($5,000-50,000+), limited availability, inconsistent quality between providers, many unproven claims, regulatory uncertainty, risk of immune rejection with allogeneic cells.",
            "cost": "$5,000-50,000+ depending on source, processing, and provider. Not covered by insurance in most cases.",
            "combination_note": "Some regenerative medicine protocols include peptides as adjunctive therapy alongside stem cell treatments, with the theory that peptides may support the survival and function of transplanted cells.",
            "addresses": "tissue regeneration through cellular replacement",
            "peptide_supports": "the molecular environment that may enhance natural or assisted healing",
            "when_preferred": "Severe injuries beyond normal repair capacity, when other treatments have failed, when budget allows, when working with an experienced regenerative medicine specialist.",
            "risks": "Infection, immune rejection, tumor risk (theoretical), unregulated providers may use unsafe practices, high cost with variable outcomes."
        },
        "physical therapy alone": {
            "status": "a first-line medical treatment",
            "mechanism": "Physical therapy uses targeted exercises, manual therapy, and progressive loading to strengthen tissues, improve range of motion, and promote natural healing through controlled mechanical stress.",
            "approach_type": "Physical therapy works through mechanical stimulus to promote natural tissue adaptation",
            "peptide_contrast": "may enhance the biological response to that mechanical stimulus at the molecular level",
            "evidence": "Extensive evidence base across virtually all musculoskeletal conditions. Physical therapy is considered standard of care and is recommended as a first-line treatment for most injuries.",
            "history": "many decades",
            "pros": "Strong evidence base, covered by insurance, addresses functional deficits directly, builds long-term tissue resilience, low risk, addresses movement patterns that may have contributed to injury.",
            "cons": "Results take time (weeks to months), requires consistent attendance and home exercise compliance, may not be sufficient for severe injuries, quality varies by provider.",
            "cost": "$50-300 per session (usually covered by insurance with copay). Typical course: 8-16 sessions over 6-12 weeks.",
            "combination_note": "Peptides and physical therapy may be highly complementary. PT provides the mechanical stimulus for tissue adaptation while peptides may enhance the biological repair response. Many researchers consider this one of the most logical combinations.",
            "addresses": "functional deficits, movement quality, and mechanical tissue health",
            "peptide_supports": "the molecular healing process that physical therapy's mechanical stimulus initiates",
            "when_preferred": "For most injuries as a first-line approach, when a comprehensive functional recovery is the goal, when insurance coverage matters, when building long-term tissue resilience.",
            "risks": "Minimal when properly supervised. Overaggressive progression can cause re-injury. Requires time commitment."
        },
        "surgery": {
            "status": "a definitive medical intervention",
            "mechanism": "Surgery directly repairs, removes, or reconstructs damaged tissue through operative intervention. For musculoskeletal conditions, this may include arthroscopic repair, tendon reattachment, joint replacement, or reconstructive procedures.",
            "approach_type": "Surgery directly addresses structural damage through operative repair",
            "peptide_contrast": "aims to support biological healing without surgical intervention",
            "evidence": "Extensive evidence for specific indications. Surgery is often considered when conservative treatments fail, though indications and outcomes vary significantly by procedure and condition.",
            "history": "many decades of refinement",
            "pros": "Directly addresses structural damage, definitive treatment for many conditions, extensive outcome data, can address issues beyond biological repair capacity.",
            "cons": "Invasive with inherent surgical risks (infection, anesthesia, complications), significant recovery time (weeks to months), expensive, may not guarantee better long-term outcomes than conservative treatment for some conditions.",
            "cost": "$5,000-50,000+ depending on procedure (usually covered by insurance with deductible and copay). Plus post-operative rehabilitation costs.",
            "combination_note": "Some orthopedic surgeons are interested in peptides as adjunctive therapy to enhance post-surgical healing. The theory is that peptides may accelerate the biological repair process after surgical intervention. This is an active area of interest but not standard practice.",
            "addresses": "structural tissue damage directly",
            "peptide_supports": "pre- and post-surgical healing and tissue repair",
            "when_preferred": "When structural damage is severe, when conservative treatments have failed, when the condition is progressive and will worsen without intervention, when a medical team recommends it.",
            "risks": "Surgical complications, infection, nerve damage, blood clots, prolonged recovery, potential need for revision surgery, general anesthesia risks."
        },
    }

    # GLP-1 / weight loss treatments
    for drug in ["ozempic", "wegovy", "mounjaro", "saxenda", "contrave", "phentermine", "metformin for weight loss"]:
        if treatment_lower == drug or drug in treatment_lower:
            return _get_weight_loss_treatment_info(treatment)

    # Skin treatments
    for skin in ["retinol", "vitamin c serum", "hyaluronic acid", "microneedling alone", "botox"]:
        if treatment_lower == skin:
            return _get_skin_treatment_info(treatment)

    # ED treatments
    for ed in ["viagra", "cialis", "levitra", "supplements for ed"]:
        if treatment_lower == ed or ed in treatment_lower:
            return _get_ed_treatment_info(treatment)

    # Tanning treatments
    for tan in ["spray tan", "tanning beds", "dha self tanner"]:
        if treatment_lower == tan or tan in treatment_lower:
            return _get_tanning_treatment_info(treatment)

    # GH treatments
    for gh in ["hgh injections", "sermorelin", "natural growth hormone boosters"]:
        if treatment_lower == gh or gh in treatment_lower:
            return _get_gh_treatment_info(treatment)

    # Gastric procedures
    for gastric in ["gastric sleeve", "lap band"]:
        if treatment_lower == gastric:
            return _get_bariatric_treatment_info(treatment)

    if treatment_lower in treatments:
        return treatments[treatment_lower]

    # Intelligent default
    return {
        "status": "an established treatment option",
        "mechanism": f"{treatment} works through its own established mechanism of action. Understanding this mechanism is key to comparing it with peptide-based approaches.",
        "approach_type": f"{treatment} addresses the condition through conventional therapeutic mechanisms",
        "peptide_contrast": "targets biological repair pathways at the molecular level",
        "evidence": f"{treatment} has an established evidence base from clinical use. The depth and quality of evidence varies by specific application.",
        "history": "years of clinical application",
        "pros": f"Established treatment with clinical data, medical professional oversight, may be covered by insurance.",
        "cons": f"Varies by specific treatment — may have side effects, limited duration of effect, or not address underlying causes.",
        "cost": "Varies — consult with providers for current pricing. Insurance coverage varies.",
        "combination_note": f"Some researchers explore combining peptides with {treatment_lower} as complementary approaches. The feasibility depends on the specific mechanisms involved.",
        "addresses": "the condition through its specific therapeutic mechanism",
        "peptide_supports": "biological repair and regeneration processes",
        "when_preferred": f"When medical professional guidance recommends it, when evidence supports its use for the specific condition, when conventional approaches are appropriate.",
        "risks": f"Varies by treatment — consult medical literature and healthcare providers for specific risk information."
    }


def _get_weight_loss_treatment_info(treatment):
    """Info for GLP-1 and weight loss drug comparisons."""
    t = treatment.title()
    return {
        "status": "an FDA-approved weight loss treatment",
        "mechanism": f"{t} works through pharmacological pathways targeting appetite regulation, metabolism, or fat absorption. These medications have undergone rigorous clinical trials for weight management.",
        "approach_type": f"{t} uses pharmaceutical intervention to regulate body weight",
        "peptide_contrast": "may affect weight through different metabolic and hormonal pathways",
        "evidence": f"{t} has been evaluated in large-scale clinical trials with published data on efficacy and safety for weight management.",
        "history": "years of clinical use (varies by specific medication)",
        "pros": f"FDA-approved with clinical data, prescribed and monitored by physicians, insurance may cover in some cases, predictable dose-response relationship.",
        "cons": f"Prescription required, potential side effects, cost can be significant, may need ongoing use to maintain results, not suitable for all patients.",
        "cost": "Varies significantly — $200-1500+/month depending on the specific medication and insurance coverage.",
        "combination_note": f"Combining research peptides with prescription weight loss medications should only be considered under direct medical supervision, as both affect metabolic and hormonal pathways.",
        "addresses": "weight management through regulated pharmaceutical pathways",
        "peptide_supports": "metabolic function through research-stage biological mechanisms",
        "when_preferred": f"When working with a physician, when FDA-approved treatment is desired, when insurance coverage is available, when clinical evidence for weight loss is the priority.",
        "risks": f"GI side effects (nausea, diarrhea), potential pancreatitis risk, thyroid concerns (varies by medication), rebound weight gain after discontinuation."
    }


def _get_skin_treatment_info(treatment):
    """Info for skin/anti-aging treatment comparisons."""
    t = treatment.title()
    return {
        "status": "an established skincare treatment",
        "mechanism": f"{t} works through dermatological pathways to improve skin health, appearance, and function. It has been studied and used in clinical and cosmetic settings.",
        "approach_type": f"{t} addresses skin concerns through topical or procedural intervention",
        "peptide_contrast": "targets skin biology at the cellular signaling level through peptide receptor activation",
        "evidence": f"{t} has established dermatological evidence for its intended applications, with varying levels of clinical study support.",
        "history": "years to decades of clinical/cosmetic use",
        "pros": f"Established safety profile, widely available, regulated manufacturing standards, extensive user experience data.",
        "cons": f"Results may be gradual, effectiveness varies by individual, may require ongoing use, potential for skin irritation or sensitivity.",
        "cost": "Varies from $10-500+ depending on formulation and professional application.",
        "combination_note": f"Some dermatology-focused researchers combine peptides with conventional skincare treatments like {treatment.lower()}, viewing them as complementary layers in a comprehensive skin protocol.",
        "addresses": "skin concerns through established dermatological mechanisms",
        "peptide_supports": "skin biology at the cellular and molecular level through growth factor signaling",
        "when_preferred": f"When proven, accessible skincare is the priority, when working with a dermatologist, when a gradual, evidence-based approach is preferred.",
        "risks": f"Generally low risk — potential for irritation, sensitivity, or allergic reaction depending on the specific product and individual skin type."
    }


def _get_ed_treatment_info(treatment):
    """Info for ED treatment comparisons."""
    t = treatment.title()
    return {
        "status": "an FDA-approved medication",
        "mechanism": f"{t} addresses erectile function through pharmacological pathways (typically PDE5 inhibition) that increase blood flow to erectile tissue.",
        "approach_type": f"{t} works through direct vasodilation and blood flow enhancement",
        "peptide_contrast": "targets sexual function through central nervous system melanocortin receptor pathways rather than peripheral blood flow",
        "evidence": f"{t} has extensive clinical trial data and real-world evidence from millions of prescriptions. It is one of the most studied medications in this category.",
        "history": "decades of clinical use",
        "pros": f"Well-studied mechanism, rapid onset (30-60 minutes), high success rate, available as generic in many cases, medical supervision.",
        "cons": f"Only addresses symptoms (not underlying causes), requires planning around sexual activity, drug interactions (especially nitrates), may cause headache/flushing/visual changes, doesn't increase desire.",
        "cost": "$2-70 per dose depending on brand vs generic and insurance coverage.",
        "combination_note": f"Combining peptides with PDE5 inhibitors like {treatment.lower()} should be approached with caution due to potential synergistic effects on blood pressure. Medical supervision is essential.",
        "addresses": "erectile function through peripheral vasodilation",
        "peptide_supports": "sexual function through central nervous system pathways that may affect both desire and function",
        "when_preferred": f"When rapid, proven results are needed, when a physician recommends it, when the issue is primarily blood flow related, when insurance coverage is available.",
        "risks": f"Headache, facial flushing, nasal congestion, visual disturbances, dangerous interaction with nitrate medications, priapism (rare), hearing changes (rare)."
    }


def _get_tanning_treatment_info(treatment):
    """Info for tanning method comparisons."""
    t = treatment.title()
    return {
        "status": "a widely used cosmetic method",
        "mechanism": f"{t} produces a tanned appearance through either UV exposure (stimulating melanin production) or topical color application (DHA reaction with skin proteins).",
        "approach_type": f"{t} changes skin color through external application or UV exposure",
        "peptide_contrast": "stimulates the body's own melanin production system through melanocortin receptor activation",
        "evidence": f"{t} has well-understood mechanisms and decades of consumer use. The trade-offs between appearance and health risks are well-documented.",
        "history": "decades of consumer use",
        "pros": f"Widely available, immediate or rapid results, no injection required, predictable outcome, regulated products.",
        "cons": f"UV methods increase skin cancer risk, results are temporary, spray tans can appear unnatural, ongoing maintenance required.",
        "cost": "Varies from $10-50 per session for spray tans to minimal cost for self-tanners.",
        "combination_note": f"Some users combine melanocyte-stimulating peptides with reduced UV exposure, theorizing that enhanced melanin production allows for tanning with less UV damage. This is a common but unproven approach.",
        "addresses": "skin appearance through external color modification",
        "peptide_supports": "the body's natural melanin production pathway from the inside",
        "when_preferred": f"When a non-injectable approach is preferred, when immediate results are needed, when UV exposure is acceptable or when using UV-free methods.",
        "risks": f"UV-based: skin cancer risk, premature aging, sunburn. Topical: potential allergic reactions, uneven application, temporary staining of clothes."
    }


def _get_gh_treatment_info(treatment):
    """Info for growth hormone treatment comparisons."""
    t = treatment.title()
    return {
        "status": "a growth hormone intervention",
        "mechanism": f"{t} affects growth hormone levels either through direct GH replacement or by stimulating the body's own GH production through various mechanisms.",
        "approach_type": f"{t} modifies GH levels through its specific intervention pathway",
        "peptide_contrast": "may affect GH secretion through secretagogue pathways or GHRH stimulation",
        "evidence": f"{t} has clinical data supporting its effects on GH levels, though the strength of evidence varies by specific product/approach.",
        "history": "years to decades depending on the specific approach",
        "pros": f"Established mechanism for affecting GH levels, medical supervision (for prescription options), measurable effects via blood testing.",
        "cons": f"Cost can be significant, may require ongoing use, potential side effects, prescription options require medical evaluation.",
        "cost": "Varies significantly — from $50/month for supplements to $500-2000+/month for prescription GH.",
        "combination_note": f"GH secretagogue peptides are sometimes used alongside or as alternatives to {treatment.lower()}. Combining multiple GH-elevating compounds requires careful monitoring of IGF-1 levels.",
        "addresses": "growth hormone levels through its specific mechanism",
        "peptide_supports": "GH secretion and metabolic pathways through peptide receptor signaling",
        "when_preferred": f"When medical supervision is available, when a proven approach to GH modulation is preferred, when the specific mechanism matches the research goal.",
        "risks": f"GH-related: joint pain, water retention, insulin resistance, potential tumor growth stimulation (theoretical). Specific risks vary by intervention."
    }


def _get_bariatric_treatment_info(treatment):
    """Info for bariatric surgery comparisons."""
    t = treatment.title()
    return {
        "status": "an FDA-approved surgical weight loss procedure",
        "mechanism": f"{t} surgically modifies the digestive system to restrict food intake and/or reduce nutrient absorption, leading to significant weight loss.",
        "approach_type": f"{t} produces weight loss through surgical modification of the GI tract",
        "peptide_contrast": "aims to affect weight through metabolic and hormonal signaling without surgical intervention",
        "evidence": f"{t} has extensive long-term clinical data showing significant and sustained weight loss. It is considered the most effective intervention for severe obesity.",
        "history": "decades of surgical refinement and long-term outcome data",
        "pros": f"Most effective weight loss intervention available, sustained results in most patients, improvement in obesity-related comorbidities, extensive long-term data.",
        "cons": f"Major surgery with inherent risks, irreversible (or difficult to reverse), nutritional deficiencies requiring lifelong supplementation, dietary restrictions, potential complications.",
        "cost": "$15,000-35,000+ (often covered by insurance for qualifying patients with BMI >35-40).",
        "combination_note": f"Peptides are not a substitute for bariatric surgery in patients who qualify. Some researchers explore peptides as complementary support for metabolic health post-surgery.",
        "addresses": "severe obesity through direct surgical modification",
        "peptide_supports": "metabolic and hormonal pathways that influence body composition",
        "when_preferred": f"When BMI qualifies for surgical intervention (>35-40), when obesity-related health conditions are present, when conservative approaches have failed, when a medical team recommends it.",
        "risks": f"Surgical complications, infection, nutritional deficiencies, dumping syndrome, gallstones, hernias, need for revision surgery, anesthesia risks."
    }


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

def build_body(peptide, pdata, angle, article_type, title, keyword, vendors_str, filename=""):
    """Route to the correct angle-specific body builder."""
    # Long-tail article types
    if angle == "condition-specific" and pdata:
        return build_condition_specific_body(peptide, pdata, title, filename)
    if angle == "interaction" and pdata:
        return build_interaction_body(peptide, pdata, title, filename)
    if angle == "vs-treatment" and pdata:
        return build_vs_treatment_body(peptide, pdata, title, filename)

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
        "condition-specific": lambda: build_condition_specific_body(peptide, pdata, title, filename),
        "interaction": lambda: build_interaction_body(peptide, pdata, title, filename),
        "vs-treatment": lambda: build_vs_treatment_body(peptide, pdata, title, filename),
        "guide": lambda: build_guide_body(peptide, pdata),
    }

    builder = builders.get(angle, builders["guide"])
    return builder()


# ============================================================
# FAQ SCHEMA BUILDER — angle-specific FAQ answers
# ============================================================

def build_visible_faq(peptide, pdata, angle, title):
    """Build visible FAQ HTML that users can actually see on the page."""
    p = peptide
    if not pdata:
        pdata = dict(DEFAULT_PEPTIDE_DATA)
        pdata.update({"full_name": p, "class": "research peptide", "key_benefits": "various applications",
                      "dosage_range": "varies", "frequency": "per protocol", "route": "subcutaneous injection",
                      "half_life": "varies", "cycle_length": "4-12 weeks", "origin": "Synthetic peptide"})
    d = pdata

    # Build FAQ pairs — the questions match the JSON-LD schema
    faqs = [
        (f"What is {p}?",
         f"{p} ({d.get('full_name', p)}) is a {d.get('class', 'research peptide')}. {d.get('origin', '')}. It is researched for {d.get('key_benefits', 'various applications')}."),
        (f"What is the recommended {p} dosage?",
         f"Common dosages: {d.get('dosage_range', 'varies')} administered {d.get('frequency', 'per protocol')} via {d.get('route', 'injection')}. Cycle length: {d.get('cycle_length', 'varies')}. Half-life: {d.get('half_life', 'varies')}. Use our <a href='/peptide-calculator.html'>peptide calculator</a> for exact reconstitution math."),
        (f"What are the side effects of {p}?",
         d.get("side_effects", DEFAULT_PEPTIDE_DATA["side_effects"])),
        (f"Is {p} safe?",
         f"{p} has shown a {'favorable' if 'well-tolerated' in d.get('side_effects','').lower() else 'preliminary'} safety profile in research. {d.get('legal_status', DEFAULT_PEPTIDE_DATA['legal_status'])} All research should follow appropriate safety protocols."),
    ]

    html_parts = []
    for q, a in faqs:
        html_parts.append(f'''<div style="border-bottom: 1px solid var(--gray-200, #e2e8f0); padding: 20px 0;">
      <h3 style="font-size: 17px; font-weight: 700; color: var(--navy, #0f2240); margin-bottom: 10px;">{q}</h3>
      <p style="font-size: 15px; color: #374151; line-height: 1.75; margin: 0;">{a}</p>
    </div>''')

    return "\n    ".join(html_parts)


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
        "condition-specific": f"{title.split(':')[0]} — research evidence, protocol, and what to expect.",
        "interaction": f"{title.split(':')[0]} — interaction safety, timing, and what researchers need to know.",
        "vs-treatment": f"{title.split(':')[0]} — comparing mechanisms, evidence, costs, and pros vs cons.",
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
    angle = detect_angle(filename, title, article_type)
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
    body_content = build_body(peptide, pdata, angle, article_type, title, keyword, vendors, filename)

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

    # Build visible FAQ content for the bottom of the page
    visible_faq = build_visible_faq(peptide, pdata, angle, title)
    html = html.replace("{{VISIBLE_FAQ}}", visible_faq)

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
    parser.add_argument("--matrix", type=str, default="", help="Path to article matrix JSON (default: new-articles-todo.json)")
    parser.add_argument("--longtail", action="store_true", help="Use longtail-articles-todo.json as the matrix")
    args = parser.parse_args()

    template = load_template()

    # Determine which matrix file to use
    if args.matrix:
        matrix_path = args.matrix
    elif args.longtail:
        matrix_path = LONGTAIL_MATRIX_FILE
    else:
        matrix_path = MATRIX_FILE

    with open(matrix_path) as f:
        articles = json.load(f)

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
            angle = detect_angle(a["filename"], a["title"], a.get("type", ""))
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
