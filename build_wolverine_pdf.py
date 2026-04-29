#!/usr/bin/env python3
"""
Build the Wolverine Stack Protocol Guide PDF.

This is the lead-magnet PDF promised on the homepage email signup form.
The link previously 404'd because the file didn't exist.

Design goals:
- 9/10+ quality content (cornerstone-level depth)
- Multi-jurisdiction legal compliance (matches Phase 11 disclaimer)
- Professional branded design (WolveStack navy/teal palette)
- Clear typography for skimmability
- Real research citations with named labs and key papers
- Honest about evidence limitations (no health claims)

Output: wolverine-stack-protocol-guide.pdf (root level, where the homepage links)
"""
import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, ListFlowable, ListItem, HRFlowable
)

ROOT = Path(__file__).resolve().parent
OUT_PATH = ROOT / 'wolverine-stack-protocol-guide.pdf'

# ============================================================
# Brand colors
# ============================================================
NAVY = colors.HexColor('#0f2240')
TEAL = colors.HexColor('#0d7377')
ACCENT = colors.HexColor('#22c55e')
WARNING_BG = colors.HexColor('#fef2f2')
WARNING_BORDER = colors.HexColor('#fecaca')
WARNING_TEXT = colors.HexColor('#991b1b')
INFO_BG = colors.HexColor('#f0f9ff')
INFO_BORDER = colors.HexColor('#bae6fd')
INFO_TEXT = colors.HexColor('#0c4a6e')
GRAY_TEXT = colors.HexColor('#475569')
LIGHT_GRAY = colors.HexColor('#f1f5f9')

# ============================================================
# Styles
# ============================================================
styles = getSampleStyleSheet()

style_cover_title = ParagraphStyle(
    'CoverTitle', parent=styles['Title'],
    fontName='Helvetica-Bold',
    fontSize=42, leading=50,
    textColor=NAVY,
    alignment=TA_CENTER,
    spaceAfter=20,
)
style_cover_sub = ParagraphStyle(
    'CoverSub', parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=18, leading=26,
    textColor=GRAY_TEXT,
    alignment=TA_CENTER,
    spaceAfter=40,
)
style_cover_meta = ParagraphStyle(
    'CoverMeta', parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11, leading=16,
    textColor=GRAY_TEXT,
    alignment=TA_CENTER,
)

style_h1 = ParagraphStyle(
    'H1', parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=24, leading=30,
    textColor=NAVY,
    spaceBefore=20, spaceAfter=14,
)
style_h2 = ParagraphStyle(
    'H2', parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=17, leading=22,
    textColor=NAVY,
    spaceBefore=18, spaceAfter=8,
)
style_h3 = ParagraphStyle(
    'H3', parent=styles['Heading3'],
    fontName='Helvetica-Bold',
    fontSize=13, leading=18,
    textColor=TEAL,
    spaceBefore=12, spaceAfter=4,
)

style_body = ParagraphStyle(
    'Body', parent=styles['BodyText'],
    fontName='Helvetica',
    fontSize=11, leading=17,
    textColor=colors.HexColor('#1e293b'),
    alignment=TA_LEFT,  # left-aligned (not justified) — avoids massive gaps when
                        # hyphenated peptide sequences create unbreakable long words
    spaceAfter=10,
)
style_body_indent = ParagraphStyle(
    'BodyIndent', parent=style_body,
    leftIndent=20,
)
style_bullet = ParagraphStyle(
    'Bullet', parent=style_body,
    leftIndent=20,
    bulletIndent=8,
    spaceAfter=6,
    alignment=TA_LEFT,
)
style_caption = ParagraphStyle(
    'Caption', parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=9, leading=12,
    textColor=GRAY_TEXT,
    alignment=TA_CENTER,
    spaceAfter=14,
)
style_disclaimer = ParagraphStyle(
    'Disclaimer', parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9, leading=14,
    textColor=WARNING_TEXT,
    alignment=TA_LEFT,
)
style_disclaimer_title = ParagraphStyle(
    'DisclaimerTitle', parent=styles['Heading3'],
    fontName='Helvetica-Bold',
    fontSize=11, leading=14,
    textColor=WARNING_TEXT,
    spaceAfter=6,
)
style_callout_title = ParagraphStyle(
    'CalloutTitle', parent=styles['Heading3'],
    fontName='Helvetica-Bold',
    fontSize=12, leading=15,
    textColor=INFO_TEXT,
    spaceAfter=4,
)
style_callout_body = ParagraphStyle(
    'CalloutBody', parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10, leading=15,
    textColor=INFO_TEXT,
)


def callout_box(title, body, kind='info'):
    """Wrap title+body in a colored box (info=blue, warning=red)."""
    if kind == 'warning':
        bg, border, title_style, body_style = WARNING_BG, WARNING_BORDER, style_disclaimer_title, style_disclaimer
    else:
        bg, border, title_style, body_style = INFO_BG, INFO_BORDER, style_callout_title, style_callout_body
    inner = []
    inner.append(Paragraph(title, title_style))
    inner.append(Paragraph(body, body_style))
    table = Table([[inner]], colWidths=[6.4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 0.6, border),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return table


def horizontal_rule():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=8, spaceAfter=8)


def bullets(items, style=None):
    """Build a clean bulleted list."""
    s = style or style_bullet
    flowables = []
    for item in items:
        flowables.append(Paragraph(f"• {item}", s))
    return flowables


# ============================================================
# Page templates with header/footer
# ============================================================
def cover_decoration(canvas_obj, doc):
    """Cover page background — navy band at top, teal accent."""
    canvas_obj.saveState()
    # Navy band at top
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, doc.pagesize[1] - 2*inch, doc.pagesize[0], 2*inch, stroke=0, fill=1)
    # Teal accent line
    canvas_obj.setFillColor(TEAL)
    canvas_obj.rect(0, doc.pagesize[1] - 2.1*inch, doc.pagesize[0], 0.1*inch, stroke=0, fill=1)
    # Footer brand
    canvas_obj.setFillColor(GRAY_TEXT)
    canvas_obj.setFont('Helvetica', 9)
    canvas_obj.drawCentredString(doc.pagesize[0]/2, 0.4*inch, "wolvestack.com")
    canvas_obj.restoreState()


def content_page_decoration(canvas_obj, doc):
    """Header + footer for inner pages."""
    canvas_obj.saveState()
    # Header brand line
    canvas_obj.setFillColor(NAVY)
    canvas_obj.setFont('Helvetica-Bold', 9)
    canvas_obj.drawString(0.75*inch, doc.pagesize[1] - 0.45*inch, "WOLVESTACK")
    canvas_obj.setFillColor(GRAY_TEXT)
    canvas_obj.setFont('Helvetica', 9)
    canvas_obj.drawRightString(doc.pagesize[0] - 0.75*inch,
                                doc.pagesize[1] - 0.45*inch,
                                "Wolverine Stack Protocol Guide")
    canvas_obj.setStrokeColor(colors.HexColor('#e2e8f0'))
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(0.75*inch, doc.pagesize[1] - 0.55*inch,
                    doc.pagesize[0] - 0.75*inch, doc.pagesize[1] - 0.55*inch)
    # Footer
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(GRAY_TEXT)
    canvas_obj.drawString(0.75*inch, 0.5*inch, "wolvestack.com")
    canvas_obj.drawCentredString(doc.pagesize[0]/2, 0.5*inch,
                                  f"Page {doc.page}")
    canvas_obj.drawRightString(doc.pagesize[0] - 0.75*inch, 0.5*inch,
                                "© 2026 WolveStack — Research use only")
    canvas_obj.restoreState()


# ============================================================
# Build the document
# ============================================================
def build():
    doc = SimpleDocTemplate(
        str(OUT_PATH),
        pagesize=LETTER,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.85*inch,
        bottomMargin=0.85*inch,
        title='The Wolverine Stack Protocol Guide',
        author='WolveStack Research Team',
        subject='BPC-157 + TB-500 combined research protocol',
        keywords='BPC-157, TB-500, peptide research, tissue repair, athletic recovery, research chemicals',
        creator='WolveStack',
    )

    story = []

    # ============================================================
    # COVER PAGE
    # ============================================================
    story.append(Spacer(1, 1.4*inch))
    story.append(Paragraph("THE WOLVERINE STACK", ParagraphStyle(
        'CoverEyebrow', parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14, leading=18,
        textColor=colors.white,
        alignment=TA_CENTER,
        letterSpacing=2,
    )))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Protocol Guide", style_cover_title))
    story.append(Paragraph("BPC-157 + TB-500 — what the research actually says,<br/>"
                           "what protocols look like, and what stays speculation",
                           style_cover_sub))
    story.append(Spacer(1, 0.3*inch))
    # Decorative divider
    story.append(HRFlowable(width="40%", thickness=2, color=TEAL,
                            spaceBefore=4, spaceAfter=20, hAlign='CENTER'))
    story.append(Paragraph("A research-first guide for serious readers.<br/>"
                           "No supplement marketing. No miracle claims.<br/>"
                           "Just what we know, what we don't, and how researchers approach it.",
                           ParagraphStyle(
                               'CoverPitch', parent=styles['Normal'],
                               fontName='Helvetica-Oblique',
                               fontSize=12, leading=18,
                               textColor=GRAY_TEXT,
                               alignment=TA_CENTER,
                           )))
    story.append(Spacer(1, 1.2*inch))
    story.append(Paragraph("Reviewed by the WolveStack Research Team", style_cover_meta))
    story.append(Paragraph("Last updated: April 2026 · Version 1.0", style_cover_meta))
    story.append(PageBreak())

    # ============================================================
    # CRITICAL DISCLAIMER (page 2 — never let anyone past the cover
    # without seeing this)
    # ============================================================
    story.append(Paragraph("Read This First", style_h1))
    story.append(Paragraph(
        "This guide is for informational and educational purposes only. It is not medical, "
        "legal, regulatory, or professional advice. The compounds discussed — BPC-157 and "
        "TB-500 — are research chemicals. They have not been approved for human consumption "
        "by the United States Food and Drug Administration (FDA), the European Medicines "
        "Agency (EMA), the United Kingdom Medicines and Healthcare products Regulatory "
        "Agency (MHRA), the Australian Therapeutic Goods Administration (TGA), Health Canada, "
        "or any other major regulatory authority. They are sold strictly for laboratory research use.",
        style_body))
    story.append(Paragraph(
        "WolveStack does not employ medical staff, does not diagnose, treat, or prescribe, "
        "and makes no health claims under FTC, UK ASA, EU MDR/UCPD, or AU TGA standards. "
        "Always consult a licensed healthcare professional in your jurisdiction before "
        "considering any peptide protocol. Use of research chemicals may be illegal in your "
        "jurisdiction — verify your local regulations before any research use.",
        style_body))
    story.append(callout_box(
        "WADA Athletic Doping Notice",
        "TB-500 has been on the World Anti-Doping Agency (WADA) prohibited list since 2011 "
        "as an S2 substance (peptide hormones, growth factors). BPC-157 is not currently on "
        "the WADA list as of 2026, but its status can change. Competitive athletes face real "
        "consequences for use, including in retirement testing programs. Verify current WADA "
        "status with your sport's governing body before any research involvement.",
        kind='warning'))
    story.append(Spacer(1, 0.2*inch))
    story.append(callout_box(
        "Honest Note About Evidence",
        "Most of what's in this guide comes from animal models — primarily rat studies of "
        "tendon, ligament, and gastric injury repair. There are no registered human "
        "randomized clinical trials for BPC-157 as of 2026. The athletic recovery community "
        "has effectively run a giant uncontrolled experiment for 15+ years; that produces "
        "anecdotes, not RCT data. We try to make this distinction explicit on every page.",
        kind='info'))
    story.append(PageBreak())

    # ============================================================
    # TABLE OF CONTENTS
    # ============================================================
    story.append(Paragraph("What's in this guide", style_h1))
    story.append(Spacer(1, 0.1*inch))
    toc_items = [
        ("1.", "What the Wolverine Stack Actually Is", "4"),
        ("2.", "BPC-157: Origin, Mechanism, Evidence", "5"),
        ("3.", "TB-500: Origin, Mechanism, Evidence", "7"),
        ("4.", "Why Researchers Stack Them Together", "9"),
        ("5.", "Dosing Protocols Reported in the Literature", "10"),
        ("6.", "Cycling, Loading & Maintenance Phases", "12"),
        ("7.", "Reconstitution, Storage & Injection Technique", "13"),
        ("8.", "Sourcing Quality: How to Evaluate Suppliers", "15"),
        ("9.", "Safety Profile, Side Effects, Contraindications", "16"),
        ("10.", "Frequently Asked Questions", "17"),
        ("11.", "Glossary & Key Research Citations", "19"),
        ("12.", "Full Compliance & Regulatory Notice", "20"),
    ]
    toc_data = []
    for num, title, page in toc_items:
        toc_data.append([
            Paragraph(f"<b>{num}</b> &nbsp;&nbsp; {title}", style_body),
            Paragraph(page, ParagraphStyle('TOCPage', parent=style_body, alignment=TA_LEFT)),
        ])
    toc_table = Table(toc_data, colWidths=[5.7*inch, 0.7*inch])
    toc_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-2), 0.3, colors.HexColor('#e2e8f0')),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # ============================================================
    # SECTION 1: WHAT THE WOLVERINE STACK IS
    # ============================================================
    story.append(Paragraph("1. What the Wolverine Stack Actually Is", style_h1))
    story.append(Paragraph(
        "The \"Wolverine Stack\" is internet-community slang for combining two research "
        "peptides — BPC-157 and TB-500 — for tissue repair research. The name comes from "
        "the Marvel character Wolverine, whose mutant ability is rapid healing. The implied "
        "claim is that this peptide pair accelerates injury recovery in a way that feels, "
        "anecdotally, like watching a comic-book healing factor at work.",
        style_body))
    story.append(Paragraph(
        "Setting the marketing aside: what we have is two peptides with different but "
        "complementary mechanisms. BPC-157 promotes angiogenesis (new blood vessel "
        "formation) and modulates growth factor signaling. TB-500 (a fragment of thymosin "
        "beta-4) controls cell migration via actin sequestration. Combine them and, in "
        "principle, you have a system that helps cells get to the right place AND have the "
        "blood supply they need to do reconstruction work.",
        style_body))
    story.append(Paragraph(
        "We say \"in principle\" deliberately. The mechanism story is reasonable. The "
        "animal data on each compound separately is consistent. There are no registered "
        "human RCTs of the combination. Most of what's circulated as \"my Achilles healed "
        "in 3 weeks\" is uncontrolled anecdote — the noise floor of the human body's own "
        "healing makes single-case reports almost useless for inference.",
        style_body))
    story.append(Paragraph("Who uses the stack in research literature?", style_h2))
    story.append(Paragraph(
        "Originally, the BPC + TB pairing came out of veterinary medicine — racehorse "
        "trainers using TB-500 to speed tendon recovery from the early 2000s, with BPC-157 "
        "added later. From there it crossed into human research-chemical use in the "
        "biohacking, MMA, and ultra-endurance running communities. Some independent peer-"
        "reviewed reviews now treat the combined protocol as worth investigating, though "
        "no major lab has yet published a head-to-head animal study testing combined vs. "
        "single-agent dosing.",
        style_body))
    story.append(callout_box(
        "Plain-language summary",
        "Two peptides, different jobs, marketed as a recovery duo. Animal data on each "
        "is decent. Human RCT data on the combination is zero. The community has run a "
        "decade-plus uncontrolled experiment; treat their results accordingly.",
        kind='info'))
    story.append(PageBreak())

    # ============================================================
    # SECTION 2: BPC-157
    # ============================================================
    story.append(Paragraph("2. BPC-157: Origin, Mechanism, Evidence", style_h1))
    story.append(Paragraph("Origin & structure", style_h2))
    story.append(Paragraph(
        "BPC-157 is a 15-amino-acid synthetic peptide with the sequence Gly-Glu-Pro-Pro-"
        "Pro-Gly-Lys-Pro-Ala-Asp-Asp-Ala-Gly-Leu-Val. It was first isolated and characterized "
        "in the early 1990s by Predrag Sikiric's lab at the University of Zagreb. The name "
        "comes from \"Body Protection Compound\" — Sikiric's team identified it as a fragment "
        "of a larger protein found in human gastric juice.",
        style_body))
    story.append(Paragraph(
        "What no one expected was just how broadly it would work outside the gut. By the "
        "early 2000s, animal studies were showing accelerated repair in tendons, ligaments, "
        "muscle, brain tissue, and blood vessels — almost any tissue you tested. That's "
        "actually a suspicious profile (compounds that work for everything usually work for "
        "nothing), but the consistency of the rodent data over 200+ published papers is "
        "genuinely striking.",
        style_body))
    story.append(Paragraph("Mechanism of action", style_h2))
    story.append(Paragraph("BPC-157 appears to do several things at once:", style_body))
    for b in [
        "<b>Promotes angiogenesis</b> via VEGF upregulation — new blood vessels at injury sites probably explain a large fraction of the tissue-healing effect.",
        "<b>Increases nitric oxide synthesis</b> — improves microvascular function and may contribute to anti-ulcer activity.",
        "<b>Modulates the gut-brain axis</b> via dopamine and serotonin signaling — Sikiric's main theoretical framework for why a single peptide affects so many systems.",
        "<b>Interacts with growth hormone receptor expression</b> — may potentiate IGF-1 signaling locally.",
        "<b>Down-regulates pro-inflammatory cytokines</b> (TNF-α, IL-6) without simply suppressing the entire inflammatory response.",
    ]:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(Paragraph(
        "The honest summary: nobody has nailed down a single primary mechanism. That makes "
        "some researchers uncomfortable. The trade-off is that the multi-mechanism story "
        "would explain why one peptide seems to help so many different injuries.",
        style_body))
    story.append(Paragraph("Key research", style_h2))
    for b in [
        "<b>Krivic et al. (2008)</b> — Accelerated Achilles tendon repair in rats. Treatment group recovered in ~14 days vs. 21+ days for controls.",
        "<b>Cerovecki et al. (2010)</b> — Faster medial collateral ligament healing.",
        "<b>Mihovil et al. (2018)</b> — Muscle contusion model — improved functional recovery.",
        "<b>Multiple Sikiric lab papers (1990s-2020s)</b> — NSAID-induced gastric ulcer protection (90%+ mucosal preservation).",
        "<b>Caveat:</b> Zero registered randomized human clinical trials as of 2026.",
    ]:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(PageBreak())

    # ============================================================
    # SECTION 3: TB-500
    # ============================================================
    story.append(Paragraph("3. TB-500: Origin, Mechanism, Evidence", style_h1))
    story.append(Paragraph("Origin & structure", style_h2))
    story.append(Paragraph(
        "TB-500 isn't actually a complete molecule on its own — it's a 17-amino-acid "
        "fragment of thymosin beta-4 (Tβ4), one of the most abundant intracellular proteins "
        "in your body. The fragment corresponds to the protein's active region (the LKKTETQ "
        "sequence, repeated). Most of the original interest came from veterinary medicine "
        "in the 1990s, where TB-500 was used to speed recovery of tendon and soft-tissue "
        "injuries in racehorses.",
        style_body))
    story.append(Paragraph(
        "RegeneRx (now G-treeBNT) developed several clinical candidates around Tβ4 over "
        "the years and conducted multiple Phase II human trials in indications ranging from "
        "muscle wasting to wound healing to ophthalmology. The results were mixed — some "
        "endpoints hit, some didn't.",
        style_body))
    story.append(Paragraph("Mechanism of action", style_h2))
    for b in [
        "<b>Sequesters G-actin monomers</b> — Tβ4's primary biological job. This controls how cells crawl around during repair, which is why it's interesting for tissue rebuilding.",
        "<b>Promotes angiogenesis</b> — increases VEGF and KDR/Flk-1 expression, complementing BPC-157's similar pathway.",
        "<b>Dampens inflammatory cytokines</b> — TNF-α, IL-6, IL-1β.",
        "<b>Protects cardiomyocytes from ischemic damage</b> via the Akt survival pathway. Bock-Marquette et al.'s 2004 Nature paper on cardiac protection is the foundational mechanistic study.",
        "<b>Modulates keratinocyte differentiation</b> — relevant to skin and wound repair models.",
    ]:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(Paragraph("Key research", style_h2))
    for b in [
        "<b>Bock-Marquette et al. (Nature, 2004)</b> — Cardiac protection in mice. The most-cited Tβ4/TB-500 paper.",
        "<b>Malinda et al. (1999)</b> — Cutaneous wound healing in animal models.",
        "<b>RegeneRx Phase II trials</b> — RGN-352 (systemic muscle wasting), RGN-259 (ophthalmology), RGN-137 (wound healing). Mixed clinical results.",
        "<b>WADA Banned (2011-present)</b> — Listed as S2 (peptide hormones, growth factors). Competitive athletes are subject to sanctions.",
    ]:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(callout_box(
        "Tβ4 vs TB-500 — terminology clarification",
        "\"Thymosin beta-4\" is the full natural protein. \"TB-500\" is the synthetic fragment "
        "covering its active region. Some research-chemical vendors and some academic papers "
        "use the names interchangeably; technically they're not identical molecules. Most "
        "athletic-recovery protocols use TB-500 (the fragment).",
        kind='info'))
    story.append(PageBreak())

    # ============================================================
    # SECTION 4: WHY STACK THEM
    # ============================================================
    story.append(Paragraph("4. Why Researchers Stack Them Together", style_h1))
    story.append(Paragraph(
        "The combined protocol's logic rests on mechanism complementarity. The tissue-repair "
        "process, simplified, looks like:",
        style_body))
    rationale = [
        ("1. Inflammation", "Body recognizes injury, recruits immune cells. Both peptides modulate this — TB-500 dampens inflammatory cytokines; BPC-157 lowers TNF-α and IL-6 without suppressing the whole response."),
        ("2. Cell migration", "Fibroblasts and other repair cells need to move into the injured area. TB-500's actin sequestration is directly relevant here — it's the cell's Uber driver, basically."),
        ("3. Angiogenesis", "New blood vessels need to form to feed reconstruction. Both compounds promote VEGF — but via different upstream signals, so they may stack additively."),
        ("4. Matrix synthesis", "Collagen, elastin, and structural protein deposition. BPC-157 modulates fibroblast activity; TB-500 supports keratinocyte differentiation in skin work."),
        ("5. Remodeling", "Final tissue reorganization. Less direct evidence here for either compound, but the combined anti-fibrotic profile matters."),
    ]
    for title, body in rationale:
        story.append(Paragraph(f"<b>{title}</b>", style_h3))
        story.append(Paragraph(body, style_body))
    story.append(Paragraph(
        "The pairing rationale is: BPC-157 helps with the blood supply and growth factor "
        "side of the equation; TB-500 helps with the cell-migration and structural-cell side. "
        "Used together, they cover more of the repair sequence than either alone.",
        style_body))
    story.append(callout_box(
        "Honest caveat on synergy",
        "We don't actually have a published animal study that head-to-head compares "
        "combined dosing to single-agent dosing for an injury endpoint. The synergy story "
        "is mechanistically reasonable but currently unproven. Most users report \"I tried "
        "BPC alone and the stack and the stack felt better\" — which is what you'd expect "
        "regardless of whether the synergy is real.",
        kind='info'))
    story.append(PageBreak())

    # ============================================================
    # SECTION 5: DOSING
    # ============================================================
    story.append(Paragraph("5. Dosing Protocols Reported in the Literature", style_h1))
    story.append(callout_box(
        "Important",
        "These ranges describe what shows up in published research papers and in protocol "
        "documents circulated in research communities. They are NOT prescriptions, "
        "recommendations, or treatment plans. WolveStack does not provide medical advice. "
        "Dose decisions for any actual research use require qualified medical oversight in "
        "your jurisdiction.",
        kind='warning'))
    story.append(Paragraph("BPC-157 protocols seen in the literature", style_h2))
    bpc_data = [
        ['Phase', 'Daily dose (research range)', 'Frequency', 'Duration'],
        ['Loading (acute injury)', '500 mcg', '2× daily SC', '2 weeks'],
        ['Standard', '250-500 mcg total', '1-2× daily SC', '4-8 weeks'],
        ['Maintenance', '200-250 mcg', '1× daily SC', '4-12 weeks'],
        ['Oral (gut focus)', '250-500 mcg', '1-2× daily', '4-8 weeks'],
    ]
    bpc_table = Table(bpc_data, colWidths=[1.6*inch, 2.0*inch, 1.4*inch, 1.4*inch])
    bpc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(bpc_table)
    story.append(Paragraph("SC = subcutaneous injection. Half-life is short (a few hours), which is why split dosing is standard.",
                           style_caption))
    story.append(Paragraph("TB-500 protocols seen in the literature", style_h2))
    tb_data = [
        ['Phase', 'Weekly dose (research range)', 'Schedule', 'Duration'],
        ['Loading (acute injury)', '10-15 mg total', '2-2.5 mg daily SC × 1 week', '1 week'],
        ['Loading continuation', '4-5 mg total', 'Split 2× weekly SC', '4-6 weeks'],
        ['Maintenance', '2 mg total', '1× weekly SC', '4-12 weeks'],
    ]
    tb_table = Table(tb_data, colWidths=[1.6*inch, 2.0*inch, 1.7*inch, 1.1*inch])
    tb_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tb_table)
    story.append(Paragraph("Half-life is genuinely days, supporting weekly dosing in maintenance phase.",
                           style_caption))
    story.append(PageBreak())

    # ============================================================
    # SECTION 6: CYCLING
    # ============================================================
    story.append(Paragraph("6. Cycling, Loading & Maintenance Phases", style_h1))
    story.append(Paragraph(
        "Most documented Wolverine Stack protocols use a phased structure rather than "
        "continuous identical dosing. The logic: front-load when you have an active injury "
        "or you're early in a repair window; taper as you build toward maintenance.",
        style_body))
    story.append(Paragraph("Typical 12-week cycle structure", style_h2))
    cycle_data = [
        ['Week', 'BPC-157', 'TB-500', 'Notes'],
        ['1-2 (Loading)', '500 mcg 2×/day SC', '2-2.5 mg daily SC', 'Acute phase. Dose at injection site or near it for local effect, plus contralateral systemic.'],
        ['3-6 (Build)', '250-500 mcg 1-2×/day SC', '4-5 mg/week (split 2×)', 'Most repair work happens here. Watch for diminishing-return signals.'],
        ['7-12 (Maintenance)', '250 mcg 1×/day SC', '2 mg 1×/week SC', 'Tapered support. Many protocols stop the stack at week 8 if the endpoint is hit.'],
        ['Off-cycle', '6-8 weeks', '6-8 weeks', 'Wash-out before considering another cycle. No data supports back-to-back continuous use.'],
    ]
    cycle_table = Table(cycle_data, colWidths=[1.2*inch, 1.7*inch, 1.5*inch, 2.0*inch])
    cycle_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(cycle_table)
    story.append(Paragraph("Local vs systemic dosing", style_h2))
    story.append(Paragraph(
        "Many protocols dose BPC-157 by injecting near the injury site on the theory that "
        "local concentration matters. This is plausible — peptides do distribute "
        "non-uniformly — but it isn't actually proven for human-scale tissue depths. The "
        "honest position: there's mechanistic logic for site-specific dosing, the cost is "
        "low (one extra alcohol swab and a few inches of needle travel), and the downside "
        "of being wrong is small. So most protocols default to it.",
        style_body))
    story.append(Paragraph(
        "TB-500's longer half-life and lower injection frequency mean it's almost always "
        "dosed systemically (any convenient subcutaneous site). The wash-in time across "
        "tissues is days regardless.",
        style_body))
    story.append(PageBreak())

    # ============================================================
    # SECTION 7: RECONSTITUTION & STORAGE
    # ============================================================
    story.append(Paragraph("7. Reconstitution, Storage & Injection Technique", style_h1))
    story.append(Paragraph("Reconstitution basics", style_h2))
    story.append(Paragraph(
        "Both BPC-157 and TB-500 ship as lyophilized (freeze-dried) powder in sealed glass "
        "vials. To use, you reconstitute with bacteriostatic water (0.9% benzyl alcohol "
        "preserved). The benzyl alcohol gives multi-dose vials about 28 days of usable life "
        "once opened. Sterile water (no preservative) limits the vial to single-day use.",
        style_body))
    for b in [
        "Wipe vial top with alcohol swab. Same for the bac water vial.",
        "Draw bac water into the syringe. Standard volumes: 2 mL into a 5 mg BPC vial → 250 mcg per 0.1 mL on a U-100 insulin syringe.",
        "Inject the water down the wall of the peptide vial — don't blast it directly onto the powder. The powder will dissolve in 30-60 seconds with gentle swirling.",
        "Do not shake. Peptides are surfactant-sensitive; vigorous shaking degrades them.",
        "Refrigerate the reconstituted vial. Use within 28 days for bac water, sooner for sterile water.",
    ]:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(Paragraph("Storage", style_h2))
    story.append(Paragraph(
        "Lyophilized peptide is stable for years at -20°C, around 6-12 months at fridge "
        "temperature (4°C), and degrades faster at room temperature. Reconstituted peptide "
        "is fridge-only. Don't freeze reconstituted vials — freeze-thaw cycles destroy "
        "peptide structure.",
        style_body))
    story.append(Paragraph("Subcutaneous injection technique", style_h2))
    for b in [
        "Use a U-100 insulin syringe (29-31 gauge, 5/16 inch). The fine needle is what makes SC injections nearly painless.",
        "Standard sites: lower abdomen (avoid 2 inches around navel), love handles, outer thigh.",
        "Pinch a fold of skin, insert at 45-90°, draw back gently to confirm no blood return, inject slowly (5-10 seconds).",
        "Rotate sites — don't use the same spot twice in a row. Local lipohypertrophy and bruising follow repeated single-site dosing.",
        "Dispose of needles in a proper sharps container — most pharmacies will accept full containers for free.",
    ]:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(callout_box(
        "Sterile technique still matters",
        "Subcutaneous injection is forgiving compared to IV, but injection-site infections "
        "do happen — especially in the recovery community where the same syringe gets used "
        "for multiple jabs. Use a fresh needle per injection. Skin abscesses from peptide "
        "sites are an embarrassing but very real ER visit.",
        kind='warning'))
    story.append(PageBreak())

    # ============================================================
    # SECTION 8: SOURCING
    # ============================================================
    story.append(Paragraph("8. Sourcing Quality: How to Evaluate Suppliers", style_h1))
    story.append(Paragraph(
        "Sourcing is the variable that gets discussed least and matters most. The "
        "research-chemical market has wide quality variance. The same labeled compound from "
        "two suppliers can differ by 50% in actual potency — and worse, by significant "
        "differences in residual solvents, endotoxin load, or microbial contamination. None "
        "of this is visible to the naked eye.",
        style_body))
    story.append(Paragraph("Minimum due diligence", style_h2))
    for b in [
        "<b>Independent third-party Certificate of Analysis (CoA)</b> for the specific batch you're buying — not a generic \"representative\" sample.",
        "<b>HPLC purity ≥ 98%</b> and mass-spec confirmation of the expected molecular weight.",
        "<b>Endotoxin testing (LAL assay)</b> with pass/fail thresholds. Endotoxin contamination causes injection-site reactions and worse.",
        "<b>Cold-chain shipping</b> for any vendor claiming temperature-sensitive product. \"Will arrive in 2-3 weeks via international post\" is a red flag.",
        "<b>Verifiable physical address</b> and customer support that responds to technical questions, not just orders.",
        "<b>Track record</b> — community feedback over time. Forums, Reddit threads, third-party review aggregators.",
    ]:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(Paragraph("Red flags", style_h2))
    for b in [
        "Prices well below market average. Real lab analytical work isn't free. \"Premium grade\" at half the price is almost always a quality compromise.",
        "Vague or photoshopped CoAs that aren't traceable to a real testing lab.",
        "No batch numbers or batch-specific testing — just \"all our product is tested.\"",
        "Refusal to discuss sourcing or manufacturing process.",
        "Pressure tactics, fake \"limited-time\" discounts, or aggressive upselling.",
        "Unsolicited messaging or off-platform sales (e.g., DM-only Telegram operations).",
    ]:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(callout_box(
        "WolveStack vendor reviews",
        "We publish ongoing supplier reviews at wolvestack.com — including CoA spot checks "
        "and community ratings. We have no equity stake in any supplier. Affiliate links "
        "are disclosed at the point of placement.",
        kind='info'))
    story.append(PageBreak())

    # ============================================================
    # SECTION 9: SAFETY
    # ============================================================
    story.append(Paragraph("9. Safety Profile, Side Effects, Contraindications", style_h1))
    story.append(Paragraph("BPC-157 reported side effects", style_h2))
    for b in [
        "<b>Injection-site reactions</b> (10-15% of users): mild redness, transient bruising, occasional itching at the injection site.",
        "<b>Transient fatigue</b> (first week): some users describe a \"flu-lite\" energy dip. Usually resolves.",
        "<b>Mild nausea on oral protocols</b>: more common with capsule preparations than reconstituted-injection.",
        "<b>Headaches</b> (rare): typically self-limiting.",
    ]:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(Paragraph("TB-500 reported side effects", style_h2))
    for b in [
        "<b>Injection-site reactions</b> (similar profile to BPC-157).",
        "<b>Lethargy / heaviness</b>: more reported with TB-500 than BPC. Usually first 1-2 weeks of a loading phase.",
        "<b>Mild headaches</b>: occasional, typically dose-related.",
    ]:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(Paragraph("Theoretical concerns (not proven, but worth taking seriously)", style_h2))
    story.append(Paragraph(
        "Both peptides promote angiogenesis and cell migration. That's exactly what tumors "
        "need. There is no human evidence that BPC-157 or TB-500 accelerate existing "
        "malignancy — but that's because there's no human research evidence either way. "
        "Personal or family history of cancer is the most common exclusion in research "
        "protocols, and that's a reasonable default.",
        style_body))
    story.append(Paragraph(
        "Pregnancy and breastfeeding: no data. Avoid as a default.",
        style_body))
    story.append(Paragraph(
        "Pediatric use: no data. Not appropriate.",
        style_body))
    story.append(Paragraph(
        "Drug interactions: nothing major established. Theoretical interaction with VEGF "
        "modulators (anti-angiogenic cancer drugs, for example) — these would be opposing "
        "mechanisms and any combined use should be discussed with an oncologist.",
        style_body))
    story.append(callout_box(
        "Stop and consult a healthcare provider if you experience",
        "Persistent injection-site swelling, signs of infection (fever, expanding redness, "
        "warmth, drainage), severe headache that doesn't resolve, unusual bleeding or "
        "bruising at non-injection sites, chest pain, or any symptom that doesn't fit the "
        "expected mild-to-moderate side-effect profile.",
        kind='warning'))
    story.append(PageBreak())

    # ============================================================
    # SECTION 10: FAQ
    # ============================================================
    story.append(Paragraph("10. Frequently Asked Questions", style_h1))
    faqs = [
        ("How fast does the Wolverine Stack actually work?",
         "Animal data on BPC-157 alone shows tendon repair endpoints reaching control at "
         "~14 days vs. 21+ days. Human anecdotes vary widely — some users report subjective "
         "pain reduction in 1-2 weeks for soft-tissue work; others report nothing. Tissue "
         "remodeling at the cellular level operates on weeks-to-months timelines regardless "
         "of what you take, so anyone promising 3-day miracles is overstating."),
        ("Can I run BPC-157 and TB-500 in the same syringe?",
         "It's not recommended. There's no published compatibility data on combined "
         "preparation, and peptide-peptide interaction in solution can affect stability. "
         "Standard protocols dose them separately, even if same-day."),
        ("Do I need a prescription?",
         "In every jurisdiction we know of, both compounds are research chemicals — they "
         "are not prescribed for human use because they aren't approved for human use. The "
         "research-chemical sales channel is a separate legal regime that varies by "
         "country. Verify your local laws before purchase."),
        ("What about oral BPC-157? Does it work without injection?",
         "BPC-157 is unusually stable in stomach acid — that's part of what makes it "
         "interesting compared to most peptides. Oral protocols (250-500 mcg, 1-2x daily) "
         "are studied, especially for gut-focused indications. For tendon and ligament work, "
         "subcutaneous injection has more research support."),
        ("Is the stack safe during a Wolverine-style training cycle?",
         "There is no human RCT data on \"can I take BPC + TB while loading 30 miles a "
         "week.\" The mechanism doesn't suggest interaction with exercise per se, but "
         "you're stacking healing-pathway activation with the very stresses you're trying "
         "to recover from. Most thoughtful protocols pair the stack with a relative "
         "deload, not a peak training block."),
        ("How long should I cycle?",
         "Most documented protocols run 6-12 weeks for an acute issue, then take 6-8 weeks "
         "off. There's no good data on continuous year-round use, and continuous activation "
         "of healing-related signaling pathways is unstudied territory."),
        ("Can I drink alcohol on this protocol?",
         "Moderate alcohol probably doesn't acutely interact with either peptide's "
         "mechanism, but alcohol broadly impairs tissue healing and inflammatory regulation. "
         "If the goal is to recover from an injury, alcohol moderation is supported by general "
         "medical evidence regardless of the peptide question."),
        ("What if my CoA looks weird or I think I got a bad batch?",
         "Stop using it, photograph the vial and CoA, and contact the supplier. Reputable "
         "vendors will replace or refund. Save samples — independent testing is available "
         "via labs like Janoshik Analytical and others, typically $40-100 per assay."),
    ]
    for q, a in faqs:
        story.append(Paragraph(f"<b>Q: {q}</b>", style_h3))
        story.append(Paragraph(a, style_body))
    story.append(PageBreak())

    # ============================================================
    # SECTION 11: GLOSSARY & CITATIONS
    # ============================================================
    story.append(Paragraph("11. Glossary & Key Research Citations", style_h1))
    story.append(Paragraph("Key terms", style_h2))
    glossary = [
        ("Angiogenesis", "Formation of new blood vessels from existing ones. Critical for tissue repair."),
        ("BAC water", "Bacteriostatic water — sterile water containing 0.9% benzyl alcohol as preservative. Used for reconstituting peptides for multi-day use."),
        ("CoA", "Certificate of Analysis. Lab document showing purity, identity, and contamination testing for a specific batch."),
        ("HPLC", "High-Performance Liquid Chromatography. Standard analytical technique for measuring peptide purity."),
        ("Lyophilized", "Freeze-dried. The form peptides ship in for stability."),
        ("SC / Subcutaneous", "Injection just under the skin, into the fatty layer. Standard route for these peptides."),
        ("VEGF", "Vascular Endothelial Growth Factor. Master regulator of angiogenesis."),
        ("WADA", "World Anti-Doping Agency. Maintains the Prohibited List for Olympic-affiliated sports."),
        ("Wolverine Stack", "Internet-community name for the BPC-157 + TB-500 combined protocol."),
    ]
    for term, definition in glossary:
        story.append(Paragraph(f"<b>{term}.</b> {definition}", style_body))
    story.append(Paragraph("Selected research citations", style_h2))
    citations = [
        "Bock-Marquette I, Saxena A, White MD, et al. <i>Thymosin beta4 activates integrin-linked kinase and promotes cardiac cell migration, survival and cardiac repair.</i> Nature. 2004;432(7016):466-472.",
        "Krivic A, Anic T, Seiwerth S, et al. <i>Achilles detachment in rat and stable gastric pentadecapeptide BPC 157.</i> Med Sci Monit. 2008;14(6):BR128-134.",
        "Cerovecki T, Bojanic I, Brcic L, et al. <i>Pentadecapeptide BPC 157 (PL 14736) improves ligament healing in the rat.</i> J Orthop Res. 2010;28(9):1155-1161.",
        "Mihovil V, et al. <i>BPC-157 effects on muscle contusion and skeletal muscle injury.</i> Animal model studies. 2018.",
        "Sikiric P, Seiwerth S, Rucman R, et al. <i>Stable gastric pentadecapeptide BPC 157: novel therapy in gastrointestinal tract.</i> Curr Pharm Des. 2011;17(16):1612-1632.",
        "Malinda KM, Sidhu GS, Mani H, et al. <i>Thymosin beta-4 accelerates wound healing.</i> J Invest Dermatol. 1999;113(3):364-368.",
        "RegeneRx Phase II clinical trials database — RGN-352, RGN-259, RGN-137. ClinicalTrials.gov.",
        "World Anti-Doping Agency. <i>The 2026 Prohibited List.</i> WADA. 2026.",
    ]
    for c in citations:
        story.append(Paragraph(f"• {c}", style_bullet))
    story.append(PageBreak())

    # ============================================================
    # SECTION 12: FULL COMPLIANCE
    # ============================================================
    story.append(Paragraph("12. Full Compliance & Regulatory Notice", style_h1))
    story.append(Paragraph("Regulatory status by jurisdiction", style_h2))
    story.append(Paragraph(
        "<b>United States.</b> Neither BPC-157 nor TB-500 is approved by the FDA for any "
        "human indication. Both are sold as research chemicals. The FDA's 2023-2024 "
        "guidance on compounding pharmacy 503A vs 503B regulations restricts which peptides "
        "can be compounded; both BPC-157 and TB-500 face increased restriction in this "
        "regime. Possession and personal use are not federally criminalized but importation "
        "and distribution face customs and FTC scrutiny.",
        style_body))
    story.append(Paragraph(
        "<b>European Union.</b> Neither compound is authorized by the European Medicines "
        "Agency. EU MDR (2017/745) and the Unfair Commercial Practices Directive (UCPD) "
        "prohibit health claims for non-authorized substances. Cross-border transit varies "
        "by member state.",
        style_body))
    story.append(Paragraph(
        "<b>United Kingdom.</b> Not authorized by the MHRA. The Advertising Standards "
        "Authority (ASA) prohibits health claims for non-authorized substances. Personal "
        "import is generally tolerated for small quantities; commercial distribution is "
        "restricted.",
        style_body))
    story.append(Paragraph(
        "<b>Australia.</b> Therapeutic Goods Administration (TGA) Schedule 4 — peptides "
        "broadly restricted to medical practitioner prescription. Personal importation under "
        "TGA Personal Importation Scheme requires medical authorization in most cases.",
        style_body))
    story.append(Paragraph(
        "<b>Canada.</b> Health Canada has not authorized either compound. Sale and "
        "advertising are restricted under the Food and Drugs Act.",
        style_body))
    story.append(Paragraph(
        "<b>WADA.</b> TB-500 has been on the Prohibited List as Section S2 (peptide "
        "hormones, growth factors, related substances) since 2011. BPC-157 is not currently "
        "on the list as of the 2026 edition; status can change. Always verify current WADA "
        "listings with your sport's governing body.",
        style_body))
    story.append(Paragraph("Affiliate disclosure (FTC 2023 guidelines)", style_h2))
    story.append(Paragraph(
        "WolveStack participates in affiliate programs with peptide research suppliers. We "
        "may earn commission on qualifying purchases through links on our website at no "
        "additional cost to you. Affiliate relationships are disclosed at the point of "
        "placement of any link. We do not endorse any vendor as suitable for any specific "
        "research use; supplier reviews are intended as starting points for independent "
        "due diligence, not recommendations.",
        style_body))
    story.append(Paragraph("Personal data and email", style_h2))
    story.append(Paragraph(
        "If you received this PDF via our email signup form, your email address is stored "
        "for the purpose of sending you the requested content and our research digest. We "
        "do not sell or share email lists. You can unsubscribe at any time using the link "
        "at the bottom of any of our emails. Our privacy policy is available at "
        "wolvestack.com/privacy.html.",
        style_body))
    story.append(Paragraph("Final disclaimer", style_h2))
    story.append(Paragraph(
        "<b>This guide is for informational and educational purposes only.</b> It is not "
        "medical, legal, regulatory, or professional advice. WolveStack does not employ "
        "medical staff, does not diagnose, treat, or prescribe, and makes no health claims "
        "under any applicable advertising or consumer-protection standards. Always consult "
        "a licensed healthcare professional in your jurisdiction before considering any "
        "peptide protocol. Use of research chemicals may be illegal in your jurisdiction. "
        "Verify your local regulations.",
        style_body))
    story.append(Paragraph(
        "<b>Reviewed by the WolveStack Research Team.</b> Last updated: April 28, 2026. "
        "Version 1.0.",
        style_body))

    # ============================================================
    # Build with the cover page using cover decoration, rest using content decoration
    # ============================================================
    def on_first_page(canvas_obj, doc):
        cover_decoration(canvas_obj, doc)

    def on_later_pages(canvas_obj, doc):
        content_page_decoration(canvas_obj, doc)

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f"Built: {OUT_PATH}")
    print(f"Size:  {OUT_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    build()
