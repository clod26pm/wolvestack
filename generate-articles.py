#!/usr/bin/env python3
"""
WolveStack Article Generator Pipeline
Generates SEO-optimized HTML articles from the keyword matrix.
Uses the ARTICLE-TEMPLATE.html as the base structure.

Usage:
  python3 generate-articles.py [--batch N] [--tier T] [--type TYPE] [--dry-run]

  --batch N     Generate only the first N articles (default: all)
  --tier T      Only generate tier T articles (1, 2, or 3)
  --type TYPE   Only generate a specific type (Single Peptide, Comparison, Roundup, Condition-Specific)
  --dry-run     Print filenames without creating files
"""

import json, os, sys, re
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MATRIX_FILE = os.path.join(SCRIPT_DIR, "new-articles-todo.json")
TEMPLATE_FILE = os.path.join(SCRIPT_DIR, "ARTICLE-TEMPLATE.html")
OUTPUT_DIR = SCRIPT_DIR
DATE_TODAY = datetime.now().strftime("%Y-%m-%d")

# ============================================================
# PEPTIDE KNOWLEDGE BASE
# This is the core research data that populates each article.
# ============================================================
PEPTIDE_DATA = {
    "BPC-157": {
        "full_name": "Body Protection Compound-157",
        "aka": "BPC-157, Bepecin, PL 14736, PL-10",
        "class": "Pentadecapeptide (15 amino acids)",
        "origin": "Derived from a protective protein found in human gastric juice",
        "mechanism": "BPC-157 works by upregulating growth hormone receptors, promoting angiogenesis (new blood vessel formation), and modulating the nitric oxide system. It activates the FAK-paxillin pathway, which is critical for cell migration and tissue repair. Research suggests it also influences the dopaminergic, serotonergic, and GABAergic systems.",
        "key_benefits": "tissue repair, gut healing, tendon and ligament recovery, wound healing, neuroprotection",
        "dosage_range": "200-500 mcg",
        "frequency": "once or twice daily",
        "route": "subcutaneous or intramuscular injection, oral",
        "half_life": "approximately 4 hours (stable form)",
        "cycle_length": "4-12 weeks",
        "side_effects": "Generally well-tolerated in research. Minor injection site reactions reported. No significant adverse effects documented in animal studies at therapeutic doses.",
        "research_summary": "Extensive preclinical research across 100+ studies demonstrates tissue-protective effects across multiple organ systems including the GI tract, musculoskeletal system, nervous system, and cardiovascular system. No human clinical trials completed to date.",
        "legal_status": "Not FDA-approved. Available as a research chemical. Not scheduled or controlled.",
        "vendors": {"Ascension": "https://www.ascensionresearch.co/?ref=wolvestack", "Particle": "https://particlepeptides.com/en/16-buy-peptides?refs=25135", "Limitless": "https://limitlesslifenootropics.com/product/bpc-157/?affid=10704"},
    },
    "TB-500": {
        "full_name": "Thymosin Beta-4 Fragment (TB-500)",
        "aka": "TB-500, Thymosin Beta 4, Tβ4",
        "class": "43-amino acid peptide",
        "origin": "Naturally occurring peptide present in virtually all human and animal cells",
        "mechanism": "TB-500 promotes cell migration by upregulating actin, a cell-building protein. It also reduces inflammation, promotes angiogenesis, and supports stem cell differentiation. Its primary mechanism involves sequestration of actin monomers and regulation of cytoskeletal dynamics.",
        "key_benefits": "wound healing, tissue repair, inflammation reduction, hair regrowth, cardiac repair, flexibility improvement",
        "dosage_range": "2-5 mg (loading), 2 mg (maintenance)",
        "frequency": "2x weekly (loading phase), weekly (maintenance)",
        "route": "subcutaneous or intramuscular injection",
        "half_life": "approximately 2-3 hours",
        "cycle_length": "4-6 weeks loading, then ongoing maintenance",
        "side_effects": "Generally well-tolerated. Temporary lethargy, head rush, or mild headache reported in some users. Minor injection site irritation possible.",
        "research_summary": "Research shows TB-500 accelerates wound healing, promotes cardiac repair after injury, reduces inflammatory cytokines, and supports dermal healing. Used extensively in equine medicine.",
        "legal_status": "Not FDA-approved. Available as a research chemical. Banned by WADA in athletic competition.",
        "vendors": {"Ascension": "https://www.ascensionresearch.co/?ref=wolvestack", "Particle": "https://particlepeptides.com/en/16-buy-peptides?refs=25135", "Limitless": "https://limitlesslifenootropics.com/?affid=10704"},
    },
    "CJC-1295": {
        "full_name": "CJC-1295 (Modified GRF 1-29)",
        "aka": "CJC-1295, Mod GRF 1-29, CJC-1295 no DAC",
        "class": "Growth Hormone Releasing Hormone (GHRH) analog",
        "origin": "Synthetic peptide analog of GHRH (first 29 amino acids)",
        "mechanism": "CJC-1295 stimulates the pituitary gland to release growth hormone in a pulsatile manner by binding to GHRH receptors. The 'no DAC' version has a shorter half-life, resulting in more natural GH pulses. It amplifies the body's own GH release rather than replacing it.",
        "key_benefits": "increased growth hormone secretion, improved body composition, better sleep quality, enhanced recovery, anti-aging effects",
        "dosage_range": "100-300 mcg",
        "frequency": "1-3 times daily, typically before bed",
        "route": "subcutaneous injection",
        "half_life": "~30 minutes (no DAC), ~8 days (with DAC)",
        "cycle_length": "8-12 weeks, often paired with Ipamorelin",
        "side_effects": "Possible water retention, tingling/numbness in hands, increased appetite, mild headache, flushing at injection site.",
        "research_summary": "Clinical research demonstrates significant increases in GH and IGF-1 levels. Studies show improved body composition, increased lean mass, and reduced body fat when used with GHRP peptides.",
        "legal_status": "Not FDA-approved. Research chemical status. Banned by WADA.",
        "vendors": {"Ascension": "https://www.ascensionresearch.co/?ref=wolvestack", "Particle": "https://particlepeptides.com/en/16-buy-peptides?refs=25135", "Limitless": "https://limitlesslifenootropics.com/?affid=10704"},
    },
    "Ipamorelin": {
        "full_name": "Ipamorelin",
        "aka": "Ipamorelin, IPA",
        "class": "Growth Hormone Secretagogue (GHS) / Ghrelin mimetic",
        "origin": "Synthetic pentapeptide derived from GHRP-1",
        "mechanism": "Ipamorelin selectively stimulates GH release by mimicking ghrelin at the GHS receptor in the pituitary gland. Unlike other GHRPs, it does not significantly increase cortisol, prolactin, or ACTH — making it one of the cleanest GH secretagogues available.",
        "key_benefits": "growth hormone release, improved sleep, fat loss, muscle recovery, bone density support",
        "dosage_range": "200-300 mcg",
        "frequency": "2-3 times daily",
        "route": "subcutaneous injection",
        "half_life": "approximately 2 hours",
        "cycle_length": "8-12 weeks, often stacked with CJC-1295",
        "side_effects": "Minimal side effects compared to other GH secretagogues. Mild headache, light-headedness, or injection site reactions possible.",
        "research_summary": "Clinical studies confirm selective GH release without significant effects on cortisol or prolactin. Demonstrated safety profile in Phase II trials.",
        "legal_status": "Not FDA-approved. Research chemical. Banned by WADA.",
        "vendors": {"Ascension": "https://www.ascensionresearch.co/?ref=wolvestack", "Particle": "https://particlepeptides.com/en/16-buy-peptides?refs=25135", "Limitless": "https://limitlesslifenootropics.com/?affid=10704"},
    },
    "GHK-Cu": {
        "full_name": "GHK-Cu (Copper Peptide)",
        "aka": "GHK-Cu, Copper Tripeptide-1, Loren Pickart peptide",
        "class": "Tripeptide-copper complex",
        "origin": "Naturally occurring peptide found in human plasma, saliva, and urine. Levels decline significantly with age.",
        "mechanism": "GHK-Cu modulates gene expression across multiple pathways — activating genes involved in tissue remodeling, antioxidant defense, and stem cell biology while suppressing genes associated with inflammation and tissue destruction. It promotes collagen synthesis, attracts immune cells to injury sites, and supports angiogenesis.",
        "key_benefits": "skin rejuvenation, wound healing, anti-aging, hair growth, collagen production, anti-inflammatory effects",
        "dosage_range": "1-3 mg (injectable), topical formulations vary",
        "frequency": "once daily",
        "route": "subcutaneous injection or topical application",
        "half_life": "approximately 2-4 hours",
        "cycle_length": "4-12 weeks",
        "side_effects": "Well-tolerated. Mild injection site reactions. Topical use may cause temporary skin redness in sensitive individuals.",
        "research_summary": "Extensive research (1,000+ studies) on wound healing, skin remodeling, and anti-aging properties. Demonstrated effects on 4,000+ human genes. Strong evidence for collagen/elastin synthesis and anti-inflammatory activity.",
        "legal_status": "Not regulated. Available as a research chemical and in cosmetic formulations.",
        "vendors": {"Ascension": "https://www.ascensionresearch.co/?ref=wolvestack", "Particle": "https://particlepeptides.com/en/16-buy-peptides?refs=25135", "Limitless": "https://limitlesslifenootropics.com/product/ghk-cu-copper-peptide/?affid=10704"},
    },
}

# Default data for peptides not in the detailed knowledge base
DEFAULT_PEPTIDE_DATA = {
    "mechanism": "Research is ongoing to fully elucidate the mechanism of action. Preclinical studies suggest multiple biological pathways may be involved.",
    "research_summary": "Preclinical research shows promising results, though human clinical data remains limited. More studies are needed to confirm efficacy and safety in humans.",
    "side_effects": "Limited safety data available. Potential injection site reactions and individual sensitivity. Consult research literature for the latest safety information.",
    "legal_status": "Not FDA-approved. Available as a research chemical in most jurisdictions. Regulations vary by country.",
}

# Affiliate links
AFFILIATE_LINKS = {
    "Ascension": "https://www.ascensionresearch.co/?ref=wolvestack",
    "Particle": "https://particlepeptides.com/en/16-buy-peptides?refs=25135",
    "Limitless": "https://limitlesslifenootropics.com/?affid=10704",
    "Apollo": "https://apolloresearchcompounds.com/?rfsn=9022946",
}

def load_template():
    with open(TEMPLATE_FILE) as f:
        return f.read()

def load_matrix():
    with open(MATRIX_FILE) as f:
        return json.load(f)

def get_peptide_data(name):
    if name in PEPTIDE_DATA:
        return PEPTIDE_DATA[name]
    return None

def slugify(text):
    return re.sub(r'[^a-z0-9-]', '', text.lower().replace(' ', '-'))

def generate_vendor_links(peptide_name, vendors_str):
    """Generate affiliate link HTML for the sourcing CTA."""
    links = []
    if not vendors_str:
        # Default to all vendors
        for name, url in AFFILIATE_LINKS.items():
            links.append(f'<p><a href="{url}" target="_blank" rel="nofollow sponsored">{name} &rarr; Browse Peptides</a></p>')
    else:
        for v in vendors_str.split(", "):
            v = v.strip()
            if v in AFFILIATE_LINKS:
                links.append(f'<p><a href="{AFFILIATE_LINKS[v]}" target="_blank" rel="nofollow sponsored">{v} &rarr; Browse {peptide_name}</a></p>')
    return "\n      ".join(links)

def generate_article(article_data, template):
    """Generate a complete HTML article from template + article data."""
    
    peptide = article_data["peptide"]
    title = article_data["title"]
    filename = article_data["filename"]
    category = article_data["category"]
    keyword = article_data["primary_keyword"]
    article_type = article_data["type"]
    vendors = article_data.get("vendors", "")
    
    # Get peptide-specific research data if available
    pdata = get_peptide_data(peptide)
    
    # Build meta description (under 160 chars)
    meta_desc = title[:155] + "..." if len(title) > 155 else title + " — Research-backed guide from WolveStack."
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157] + "..."
    
    # Determine read time based on article type
    read_times = {"Single Peptide": "8", "Comparison": "10", "Roundup": "12", "Condition-Specific": "7"}
    read_time = read_times.get(article_type, "8")
    
    # Build quick answer
    if pdata:
        quick_answer = f"<strong>{peptide}</strong> ({pdata.get('full_name', peptide)}) is a {pdata.get('class', 'research peptide')}. {pdata.get('origin', 'It is being studied for various potential applications.')} Common research dosages range from {pdata.get('dosage_range', 'varies')} administered {pdata.get('frequency', 'as directed')}."
    elif "vs" in peptide.lower():
        parts = peptide.split(" vs ")
        quick_answer = f"<strong>{parts[0].strip()}</strong> and <strong>{parts[1].strip()}</strong> are both popular research peptides, but they work through different mechanisms and serve different purposes. This guide compares their benefits, dosing protocols, side effects, and which might be better suited for specific research goals."
    else:
        quick_answer = f"<strong>{peptide}</strong> is a research peptide being studied for various potential biological effects. This guide covers the latest research, recommended protocols, potential side effects, and practical considerations for researchers."
    
    # Build the article HTML from template
    html = template
    
    # Replace all template variables
    replacements = {
        "{{TITLE}}": title,
        "{{META_DESCRIPTION}}": meta_desc,
        "{{META_DESCRIPTION_SHORT}}": meta_desc[:120],
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
    
    # Build article body content based on type
    if pdata:
        body_content = build_detailed_body(peptide, pdata, article_type, keyword, vendors)
    else:
        body_content = build_generic_body(peptide, article_type, keyword, category, vendors)
    
    # Replace the body section
    # Find where the article body content goes (after quick-answer, before the affiliate CTA)
    body_marker_start = '<!-- GEO: Use question-format H2 headers that mirror how people ask AI -->'
    body_marker_end = '<!-- Affiliate CTA -->'
    
    start_idx = html.find(body_marker_start)
    end_idx = html.find(body_marker_end)
    
    if start_idx != -1 and end_idx != -1:
        html = html[:start_idx] + body_content + "\n\n    " + html[end_idx:]
    
    # Replace affiliate CTA vendor links
    vendor_links = generate_vendor_links(peptide, vendors)
    html = html.replace(
        f'<p><a href="https://www.ascensionresearch.co/?ref=wolvestack" target="_blank" rel="nofollow sponsored">Ascension Research → Browse {peptide}</a></p>',
        vendor_links
    )
    
    # Replace FAQ schema answers
    if pdata:
        html = html.replace("{{FAQ_ANSWER_1}}", f"{peptide} ({pdata.get('full_name', '')}) is a {pdata.get('class', 'research peptide')} {pdata.get('origin', '').lower()}. It is being studied for {pdata.get('key_benefits', 'various research applications')}.")
        html = html.replace("{{FAQ_ANSWER_2}}", f"Common research dosages for {peptide} range from {pdata.get('dosage_range', 'varies')} administered {pdata.get('frequency', 'as directed')} via {pdata.get('route', 'subcutaneous injection')}. Typical research cycles last {pdata.get('cycle_length', '4-12 weeks')}.")
        html = html.replace("{{FAQ_ANSWER_3}}", pdata.get("side_effects", DEFAULT_PEPTIDE_DATA["side_effects"]))
        html = html.replace("{{FAQ_ANSWER_4}}", f"{peptide} has shown a favorable safety profile in preclinical research. However, it is not FDA-approved for human use. All peptide research should be conducted under appropriate supervision and with proper protocols.")
    else:
        html = html.replace("{{FAQ_ANSWER_1}}", f"{peptide} is a research peptide being studied for various potential biological applications. Research is ongoing to determine its full range of effects.")
        html = html.replace("{{FAQ_ANSWER_2}}", f"Dosage protocols for {peptide} vary depending on the research application. Consult current literature for the most up-to-date dosing information.")
        html = html.replace("{{FAQ_ANSWER_3}}", DEFAULT_PEPTIDE_DATA["side_effects"])
        html = html.replace("{{FAQ_ANSWER_4}}", f"Research on {peptide} is ongoing. It is not FDA-approved for human use. Researchers should follow appropriate safety protocols and consult the latest literature.")
    
    # Add calculator CTA where relevant
    calculator_cta = f'''
    <div style="background: linear-gradient(135deg, #e8f4f5 0%, #f0fdf9 100%); border: 2px solid var(--teal); border-radius: 12px; padding: 24px 28px; margin: 32px 0; text-align: center;">
      <h3 style="margin-top: 0;">🧮 Calculate Your {peptide} Dose</h3>
      <p>Use our free peptide dosing calculator to get exact reconstitution math and syringe units for {peptide}.</p>
      <a href="/peptide-calculator.html" style="display: inline-block; background: var(--teal); color: white; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-weight: 600;">Open Calculator &rarr;</a>
    </div>'''
    
    # Insert calculator CTA before the affiliate CTA
    html = html.replace('<!-- Affiliate CTA -->', calculator_cta + '\n\n    <!-- Affiliate CTA -->')
    
    return html


def build_detailed_body(peptide, pdata, article_type, keyword, vendors):
    """Build rich article body for peptides with full research data."""
    
    sections = []
    
    sections.append(f'''<h2 id="what-is">What Is {peptide}?</h2>
    <p>{peptide} ({pdata["full_name"]}) is a {pdata["class"]}. {pdata["origin"]}. Also known as {pdata["aka"]}, it has been studied extensively for its potential effects on {pdata["key_benefits"]}.</p>
    <p>In the research community, {peptide} has gained significant attention due to its favorable safety profile and broad range of potential applications. It is one of the most widely studied peptides in its class.</p>''')
    
    sections.append(f'''<h2 id="mechanism">How Does {peptide} Work?</h2>
    <p>{pdata["mechanism"]}</p>
    <p>Understanding these mechanisms helps researchers design more effective protocols and predict potential outcomes. The multi-pathway activity of {peptide} is one reason it has attracted so much research interest.</p>''')
    
    sections.append(f'''<h2 id="research">What Does the Research Say About {peptide}?</h2>
    <p>{pdata["research_summary"]}</p>
    <p>It is important to note that while preclinical results are encouraging, the peptide research field is still evolving. Researchers should consult the latest peer-reviewed literature for the most current findings on {peptide}.</p>''')
    
    sections.append(f'''<h2 id="dosing">What Is the Recommended {peptide} Dosage?</h2>
    <p>Based on research protocols, common {peptide} dosages range from <strong>{pdata["dosage_range"]}</strong>, administered <strong>{pdata["frequency"]}</strong> via <strong>{pdata["route"]}</strong>.</p>
    <p>The half-life of {peptide} is {pdata["half_life"]}, which influences dosing frequency. Typical research cycles last {pdata["cycle_length"]}.</p>
    <p>Reconstitution is straightforward — use our <a href="/peptide-calculator.html">peptide dosing calculator</a> to determine exact mixing ratios and syringe units for your specific vial size.</p>''')
    
    sections.append(f'''<h2 id="side-effects">What Are the Side Effects of {peptide}?</h2>
    <p>{pdata["side_effects"]}</p>
    <p>As with any research compound, individual responses may vary. Researchers should start with lower doses and monitor for any adverse reactions. {peptide} is {pdata["legal_status"]}</p>''')
    
    sections.append(f'''<h2 id="bottom-line">What Is the Bottom Line on {peptide}?</h2>
    <p>{peptide} remains one of the most promising and well-researched peptides available. Its favorable safety profile, combined with a broad range of potential benefits ({pdata["key_benefits"]}), makes it a popular choice among researchers.</p>
    <p>For those looking to begin research with {peptide}, sourcing from reputable vendors with third-party testing is essential. Proper reconstitution, storage at 2-8°C, and adherence to established protocols will yield the best results.</p>
    <p>Read our <a href="/peptide-beginners-guide.html">peptide beginner's guide</a> for more information on getting started, or use the <a href="/peptide-calculator.html">dosing calculator</a> to plan your protocol.</p>''')
    
    return "\n\n    ".join(sections)


def build_generic_body(peptide, article_type, keyword, category, vendors):
    """Build article body for peptides without full research data."""
    
    if article_type == "Comparison":
        parts = peptide.split(" vs ")
        p1, p2 = parts[0].strip(), parts[1].strip()
        return f'''<h2 id="overview">What Are {p1} and {p2}?</h2>
    <p>{p1} and {p2} are both research peptides that have attracted significant attention in the peptide research community. While they may share some overlapping applications, they differ in their mechanisms of action, dosing protocols, and primary areas of research.</p>
    <p>Understanding these differences is essential for researchers who want to select the right compound — or potentially combine both — for their specific research goals.</p>

    <h2 id="mechanisms">How Do {p1} and {p2} Work Differently?</h2>
    <p>{p1} and {p2} act through distinct biological pathways. This means they can complement each other in stacking protocols, or one may be more appropriate than the other depending on the research objective.</p>
    <p>For detailed mechanism breakdowns, see our individual guides: <a href="/{slugify(p1)}-guide.html">{p1} Guide</a> and <a href="/{slugify(p2)}-guide.html">{p2} Guide</a>.</p>

    <h2 id="comparison">How Do {p1} and {p2} Compare for Key Research Areas?</h2>
    <p>Both peptides have been studied across various applications. The choice between them often comes down to the specific research context, desired outcomes, and individual protocol requirements.</p>

    <h2 id="dosing">How Do the Dosing Protocols Compare?</h2>
    <p>Dosing protocols differ between {p1} and {p2} in terms of frequency, amount, and administration route. Use our <a href="/peptide-calculator.html">peptide dosing calculator</a> to get exact reconstitution math for either compound.</p>

    <h2 id="stacking">Can You Stack {p1} and {p2} Together?</h2>
    <p>Many researchers use {p1} and {p2} together in stacking protocols. The complementary mechanisms of action can potentially provide synergistic effects. However, proper dosing and timing are important when combining compounds.</p>
    <p>See our <a href="/peptide-cycling-guide.html">peptide stacking guide</a> for general stacking principles.</p>

    <h2 id="verdict">Which Is Better: {p1} or {p2}?</h2>
    <p>There is no universal answer to which peptide is "better" — it depends entirely on the research goals. {p1} may be more suitable for some applications, while {p2} excels in others. Many researchers find that combining both yields the most comprehensive results.</p>
    <p>The best approach is to review the specific research literature for your area of interest and consider starting with the compound that most closely aligns with your primary research objective.</p>'''
    
    elif article_type == "Roundup":
        return f'''<h2 id="overview">Overview: {keyword.title()}</h2>
    <p>Choosing the right peptide for your research goals can be overwhelming given the growing number of available compounds. This guide ranks and compares the top research peptides based on current evidence, community protocols, and practical considerations.</p>

    <h2 id="top-picks">What Are the Top Peptides for This Category?</h2>
    <p>Based on the available research literature and community protocols, several peptides stand out for their evidence base and safety profiles. Each has distinct advantages depending on the specific application.</p>
    <p>The most important factors when selecting a peptide include: strength of research evidence, safety profile, ease of administration, and availability from reputable sources.</p>

    <h2 id="comparison">How Do They Compare?</h2>
    <p>When comparing peptides head-to-head, consider the mechanism of action, dosing convenience, cost per protocol, and the depth of available research. Some peptides have decades of research behind them, while others are more recently discovered with promising but limited data.</p>

    <h2 id="stacking">Can These Peptides Be Combined?</h2>
    <p>Many researchers use multiple peptides in combination (stacking) to potentially achieve synergistic effects. The key is understanding which compounds complement each other and which should not be combined. See our <a href="/peptide-cycling-guide.html">stacking guide</a> for principles.</p>

    <h2 id="getting-started">How to Get Started</h2>
    <p>For beginners, starting with a single, well-researched peptide is recommended before exploring stacks. Use our <a href="/peptide-calculator.html">dosing calculator</a> to get exact reconstitution math, and review our <a href="/peptide-beginners-guide.html">beginner's guide</a> for step-by-step instructions.</p>
    <p>Source matters — always choose vendors with third-party certificate of analysis (COA) testing.</p>'''
    
    else:
        # Single peptide or condition-specific
        return f'''<h2 id="what-is">What Is {peptide}?</h2>
    <p>{peptide} is a research peptide that has been studied for various potential biological effects. It belongs to the {category.lower()} category of peptide research and has attracted growing interest from the research community.</p>
    <p>This guide covers the current state of research, common protocols used in the literature, potential side effects, and practical considerations for working with {peptide}.</p>

    <h2 id="mechanism">How Does {peptide} Work?</h2>
    <p>Research into the mechanism of action of {peptide} is ongoing. Preclinical studies suggest it may work through multiple biological pathways relevant to its {category.lower()} applications.</p>
    <p>Understanding these mechanisms helps researchers design more effective protocols. For the latest findings, researchers should consult current peer-reviewed literature.</p>

    <h2 id="research">What Does the Research Say About {peptide}?</h2>
    <p>The research base for {peptide} continues to grow. While preclinical results are encouraging, the evidence base varies in depth compared to more established peptides like BPC-157 or TB-500.</p>
    <p>Key areas of research include its effects on {category.lower()}-related pathways and its potential applications in conjunction with other research compounds.</p>

    <h2 id="dosing">What Is the Recommended {peptide} Protocol?</h2>
    <p>Dosing protocols for {peptide} vary across the research literature. As with all peptides, proper reconstitution with bacteriostatic water is essential. Use our <a href="/peptide-calculator.html">peptide dosing calculator</a> for exact mixing ratios.</p>
    <p>Storage at 2-8°C after reconstitution is standard practice. Lyophilized powder can typically be stored at -20°C for extended periods.</p>

    <h2 id="side-effects">What Are the Side Effects of {peptide}?</h2>
    <p>Safety data for {peptide} is limited compared to more widely studied peptides. Potential side effects include injection site reactions and individual sensitivity. As a research compound, it is not FDA-approved for human use.</p>
    <p>Researchers should start with conservative doses and monitor for any adverse reactions. Consulting the latest safety literature is recommended.</p>

    <h2 id="bottom-line">What Is the Bottom Line on {peptide}?</h2>
    <p>{peptide} represents an interesting area of peptide research with promising preliminary findings. For researchers interested in {category.lower()} applications, it is worth reviewing the current literature.</p>
    <p>Sourcing from reputable vendors with third-party testing is essential for quality research. See our <a href="/peptide-sourcing-guide.html">sourcing guide</a> for more on evaluating vendor quality.</p>'''


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, default=0, help="Generate only first N articles")
    parser.add_argument("--tier", type=int, default=0, help="Only tier T")
    parser.add_argument("--type", type=str, default="", help="Only this type")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    template = load_template()
    articles = load_matrix()
    
    # Filter
    if args.tier:
        articles = [a for a in articles if a["tier"] == args.tier]
    if args.type:
        articles = [a for a in articles if a["type"].lower() == args.type.lower()]
    
    # Skip already existing files
    articles = [a for a in articles if not os.path.exists(os.path.join(OUTPUT_DIR, a["filename"]))]
    
    if args.batch:
        articles = articles[:args.batch]
    
    print(f"Generating {len(articles)} articles...")
    
    if args.dry_run:
        for a in articles:
            print(f"  [DRY] {a['filename']} — {a['title']}")
        return
    
    created = 0
    for i, article in enumerate(articles):
        try:
            html = generate_article(article, template)
            outpath = os.path.join(OUTPUT_DIR, article["filename"])
            with open(outpath, 'w') as f:
                f.write(html)
            created += 1
            if (i + 1) % 50 == 0:
                print(f"  ...{i+1}/{len(articles)} done")
        except Exception as e:
            print(f"  ERROR: {article['filename']}: {e}")
    
    print(f"Done! Created {created} articles.")


if __name__ == "__main__":
    main()
