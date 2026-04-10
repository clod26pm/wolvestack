#!/usr/bin/env python3
"""
WolveStack Pinterest Pin Generator v2 — Clean Medical/Science Aesthetic

Generates 1000x1500 Pinterest pins with:
- White/light backgrounds
- Molecular structure decorations (hexagons, bonds)
- Clean typography hierarchy
- Subtle color accents from a medical palette
- Professional scientific journal feel
"""

import json
import math
import os
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ── Config ──────────────────────────────────────────────────────────────────
PIN_W, PIN_H = 1000, 1500
OUTPUT_DIR = Path(__file__).parent / "pinterest-pins-v2"
OUTPUT_DIR.mkdir(exist_ok=True)

# Medical/Science color palette
PALETTES = {
    "teal":    {"accent": "#0097A7", "accent_light": "#B2EBF2", "accent_dark": "#00696D", "bg_tint": "#F0FAFA"},
    "indigo":  {"accent": "#3949AB", "accent_light": "#C5CAE9", "accent_dark": "#1A237E", "bg_tint": "#F3F4FC"},
    "emerald": {"accent": "#2E7D32", "accent_light": "#C8E6C9", "accent_dark": "#1B5E20", "bg_tint": "#F1F8F1"},
    "slate":   {"accent": "#455A64", "accent_light": "#CFD8DC", "accent_dark": "#263238", "bg_tint": "#F5F7F8"},
    "purple":  {"accent": "#7B1FA2", "accent_light": "#E1BEE7", "accent_dark": "#4A148C", "bg_tint": "#F9F2FC"},
    "coral":   {"accent": "#D84315", "accent_light": "#FFCCBC", "accent_dark": "#BF360C", "bg_tint": "#FFF5F2"},
}

# ── Font helpers ────────────────────────────────────────────────────────────
def _load_font(size, bold=False):
    """Try to load a clean sans-serif font, fall back gracefully."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

FONT_TITLE      = _load_font(62, bold=True)
FONT_SUBTITLE   = _load_font(36, bold=False)
FONT_BODY       = _load_font(30, bold=False)
FONT_BODY_BOLD  = _load_font(30, bold=True)
FONT_SMALL      = _load_font(24, bold=False)
FONT_BRAND      = _load_font(28, bold=True)
FONT_CTA        = _load_font(34, bold=True)
FONT_TINY       = _load_font(20, bold=False)

# ── Molecular decoration drawing ────────────────────────────────────────────
def draw_hexagon(draw, cx, cy, radius, color, width=2):
    """Draw a single hexagon (benzene ring style)."""
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, outline=color, fill=None)
    # Re-draw lines for crisp edges
    for i in range(6):
        draw.line([points[i], points[(i + 1) % 6]], fill=color, width=width)

def draw_molecule_cluster(draw, cx, cy, base_radius, color, alpha_color):
    """Draw an organic-looking cluster of connected hexagons (molecular structure)."""
    offsets = [
        (0, 0),
        (base_radius * 1.73, 0),
        (base_radius * 0.865, -base_radius * 1.5),
        (base_radius * 0.865, base_radius * 1.5),
        (-base_radius * 0.865, -base_radius * 1.5),
        (base_radius * 2.595, -base_radius * 1.5),
    ]
    for ox, oy in offsets:
        draw_hexagon(draw, cx + ox, cy + oy, base_radius, alpha_color, width=2)

    # Draw bond lines between hexagons
    bond_pairs = [(0, 1), (0, 2), (0, 3), (1, 5), (0, 4)]
    for a, b in bond_pairs:
        ax, ay = cx + offsets[a][0], cy + offsets[a][1]
        bx, by = cx + offsets[b][0], cy + offsets[b][1]
        mid_x, mid_y = (ax + bx) / 2, (ay + by) / 2
        draw.line([(ax, ay), (mid_x, mid_y)], fill=alpha_color, width=2)


def draw_dna_helix_stripe(draw, x_start, y_start, height, color, width=2):
    """Draw a subtle DNA double-helix decoration along a vertical stripe."""
    amplitude = 30
    period = 120
    for y_off in range(0, height, 3):
        y = y_start + y_off
        x1 = x_start + amplitude * math.sin(2 * math.pi * y_off / period)
        x2 = x_start - amplitude * math.sin(2 * math.pi * y_off / period)
        draw.ellipse([x1 - 1, y - 1, x1 + 1, y + 1], fill=color)
        draw.ellipse([x2 - 1, y - 1, x2 + 1, y + 1], fill=color)
        # Rungs every period/4
        if y_off % (period // 4) < 3:
            draw.line([(x1, y), (x2, y)], fill=color, width=1)


def draw_scattered_dots(draw, region, color, count=40):
    """Draw subtle scattered dots (like a scientific diagram background)."""
    x0, y0, x1, y1 = region
    for _ in range(count):
        x = random.randint(x0, x1)
        y = random.randint(y0, y1)
        r = random.choice([1, 2, 2, 3])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)


def draw_atom_icon(draw, cx, cy, radius, color):
    """Draw a stylized atom icon (nucleus + 3 elliptical orbits)."""
    # Nucleus
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)
    # Orbits
    for angle_deg in [0, 60, 120]:
        angle = math.radians(angle_deg)
        points = []
        for t in range(0, 360, 5):
            t_rad = math.radians(t)
            x = cx + radius * math.cos(t_rad)
            y = cy + radius * 0.35 * math.sin(t_rad)
            # Rotate
            rx = cx + (x - cx) * math.cos(angle) - (y - cy) * math.sin(angle)
            ry = cy + (x - cx) * math.sin(angle) + (y - cy) * math.cos(angle)
            points.append((rx, ry))
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=color, width=2)


def draw_cross_icon(draw, cx, cy, size, color, width=4):
    """Draw a medical cross icon."""
    half = size // 2
    third = size // 6
    draw.rectangle([cx - third, cy - half, cx + third, cy + half], fill=color)
    draw.rectangle([cx - half, cy - third, cx + half, cy + third], fill=color)


def draw_pill_icon(draw, cx, cy, width_px, height_px, color1, color2):
    """Draw a stylized pill/capsule."""
    r = width_px // 2
    # Top half
    draw.rounded_rectangle(
        [cx - r, cy - height_px // 2, cx + r, cy],
        radius=r, fill=color1
    )
    # Bottom half
    draw.rounded_rectangle(
        [cx - r, cy, cx + r, cy + height_px // 2],
        radius=r, fill=color2
    )


def draw_syringe_icon(draw, cx, cy, color, scale=1.0):
    """Draw a simplified syringe icon."""
    s = scale
    # Barrel
    draw.rectangle([cx - int(8*s), cy - int(40*s), cx + int(8*s), cy + int(20*s)], outline=color, width=2)
    # Plunger
    draw.rectangle([cx - int(4*s), cy - int(60*s), cx + int(4*s), cy - int(40*s)], fill=color)
    draw.line([(cx, cy - int(60*s)), (cx, cy - int(70*s))], fill=color, width=3)
    # Needle
    draw.line([(cx, cy + int(20*s)), (cx, cy + int(45*s))], fill=color, width=2)
    # Finger grips
    draw.line([(cx - int(16*s), cy - int(40*s)), (cx + int(16*s), cy - int(40*s))], fill=color, width=3)


# ── Text wrapping helper ────────────────────────────────────────────────────
def wrap_text(text, font, max_width, draw):
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ── Main pin generator ──────────────────────────────────────────────────────
def generate_pin(
    heading: str,
    subtitle: str,
    bullets: list[str],
    url_slug: str,
    palette_name: str = "teal",
    icon_type: str = "molecule",  # molecule, atom, dna, cross, syringe, pill
    filename: str = None,
):
    """Generate a single Pinterest pin image."""
    pal = PALETTES.get(palette_name, PALETTES["teal"])
    accent = pal["accent"]
    accent_light = pal["accent_light"]
    accent_dark = pal["accent_dark"]
    bg_tint = pal["bg_tint"]

    img = Image.new("RGB", (PIN_W, PIN_H), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # ── Background subtle tint gradient ──
    for y in range(PIN_H):
        # Subtle gradient: white at top → very light tint at bottom
        ratio = y / PIN_H
        r_bg = int(255 * (1 - ratio * 0.06))
        g_bg = int(255 * (1 - ratio * 0.03))
        b_bg = int(255 * (1 - ratio * 0.02))
        # Parse bg_tint to blend
        tr = int(bg_tint[1:3], 16)
        tg = int(bg_tint[3:5], 16)
        tb = int(bg_tint[5:7], 16)
        fr = int(r_bg * (1 - ratio * 0.3) + tr * ratio * 0.3)
        fg = int(g_bg * (1 - ratio * 0.3) + tg * ratio * 0.3)
        fb = int(b_bg * (1 - ratio * 0.3) + tb * ratio * 0.3)
        draw.line([(0, y), (PIN_W, y)], fill=(fr, fg, fb))

    # ── Decorative elements (top-right and bottom-left) ──
    # Scattered dots in corners
    draw_scattered_dots(draw, (700, 20, 980, 250), accent_light, count=50)
    draw_scattered_dots(draw, (20, 1250, 300, 1480), accent_light, count=40)

    # Molecular/scientific decorations
    if icon_type == "molecule":
        draw_molecule_cluster(draw, 850, 130, 28, accent, accent_light)
        draw_molecule_cluster(draw, 120, 1380, 22, accent, accent_light)
    elif icon_type == "atom":
        draw_atom_icon(draw, 870, 140, 60, accent_light)
        draw_atom_icon(draw, 130, 1380, 45, accent_light)
    elif icon_type == "dna":
        draw_dna_helix_stripe(draw, 950, 50, 300, accent_light, width=2)
        draw_dna_helix_stripe(draw, 50, 1200, 280, accent_light, width=2)
    elif icon_type == "cross":
        draw_cross_icon(draw, 880, 120, 50, accent_light, width=4)
        draw_cross_icon(draw, 120, 1380, 35, accent_light, width=4)
    elif icon_type == "syringe":
        draw_syringe_icon(draw, 880, 150, accent_light, scale=1.5)
        draw_syringe_icon(draw, 120, 1370, accent_light, scale=1.0)
    elif icon_type == "pill":
        draw_pill_icon(draw, 880, 120, 40, 70, accent_light, accent)
        draw_pill_icon(draw, 120, 1380, 30, 50, accent_light, accent)

    # ── Top accent bar ──
    draw.rectangle([0, 0, PIN_W, 8], fill=accent)

    # ── Brand header ──
    y_cursor = 40
    # Small "WOLVESTACK" brand
    brand_text = "WOLVESTACK"
    bb = draw.textbbox((0, 0), brand_text, font=FONT_BRAND)
    brand_w = bb[2] - bb[0]
    draw.text(((PIN_W - brand_w) // 2, y_cursor), brand_text, fill=accent, font=FONT_BRAND)

    # Thin line under brand
    y_cursor += 50
    line_w = 120
    draw.line([((PIN_W - line_w) // 2, y_cursor), ((PIN_W + line_w) // 2, y_cursor)], fill=accent_light, width=2)

    # ── Main heading ──
    y_cursor += 30
    heading_lines = wrap_text(heading.upper(), FONT_TITLE, PIN_W - 120, draw)
    for line in heading_lines:
        bb = draw.textbbox((0, 0), line, font=FONT_TITLE)
        lw = bb[2] - bb[0]
        draw.text(((PIN_W - lw) // 2, y_cursor), line, fill=accent_dark, font=FONT_TITLE)
        y_cursor += bb[3] - bb[1] + 12

    # ── Subtitle ──
    y_cursor += 10
    sub_lines = wrap_text(subtitle, FONT_SUBTITLE, PIN_W - 100, draw)
    for line in sub_lines:
        bb = draw.textbbox((0, 0), line, font=FONT_SUBTITLE)
        lw = bb[2] - bb[0]
        draw.text(((PIN_W - lw) // 2, y_cursor), line, fill="#666666", font=FONT_SUBTITLE)
        y_cursor += bb[3] - bb[1] + 8

    # ── Decorative divider ──
    y_cursor += 25
    div_w = 600
    draw.line([((PIN_W - div_w) // 2, y_cursor), ((PIN_W + div_w) // 2, y_cursor)], fill=accent_light, width=2)
    # Small diamond in center
    dm = 8
    draw.polygon([
        (PIN_W // 2, y_cursor - dm),
        (PIN_W // 2 + dm, y_cursor),
        (PIN_W // 2, y_cursor + dm),
        (PIN_W // 2 - dm, y_cursor),
    ], fill=accent)

    # ── Bullet points ──
    y_cursor += 40
    left_margin = 80
    bullet_area_right = PIN_W - 80

    for i, bullet in enumerate(bullets):
        # Numbered circle
        circle_r = 22
        circle_cx = left_margin + circle_r
        circle_cy = y_cursor + circle_r + 2
        draw.ellipse(
            [circle_cx - circle_r, circle_cy - circle_r, circle_cx + circle_r, circle_cy + circle_r],
            fill=accent, outline=None
        )
        # Number
        num_text = str(i + 1)
        nb = draw.textbbox((0, 0), num_text, font=FONT_BODY_BOLD)
        nw = nb[2] - nb[0]
        nh = nb[3] - nb[1]
        draw.text((circle_cx - nw // 2, circle_cy - nh // 2 - 4), num_text, fill="#FFFFFF", font=FONT_BODY_BOLD)

        # Bullet text
        text_x = left_margin + circle_r * 2 + 20
        text_max_w = bullet_area_right - text_x
        b_lines = wrap_text(bullet, FONT_BODY, text_max_w, draw)
        for j, bl in enumerate(b_lines):
            draw.text((text_x, y_cursor + j * 38), bl, fill="#333333", font=FONT_BODY)

        line_height = max(len(b_lines) * 38, circle_r * 2 + 10)
        y_cursor += line_height + 20

        # Subtle separator between bullets (not after last)
        if i < len(bullets) - 1:
            sep_y = y_cursor - 8
            draw.line([(left_margin + 60, sep_y), (bullet_area_right - 20, sep_y)], fill=accent_light, width=1)

    # ── CTA Button ──
    y_cursor = max(y_cursor + 30, PIN_H - 250)
    btn_w, btn_h = 500, 70
    btn_x = (PIN_W - btn_w) // 2
    btn_y = y_cursor
    draw.rounded_rectangle(
        [btn_x, btn_y, btn_x + btn_w, btn_y + btn_h],
        radius=35, fill=accent
    )
    cta_text = "Read Full Guide"
    cb = draw.textbbox((0, 0), cta_text, font=FONT_CTA)
    cw = cb[2] - cb[0]
    ch = cb[3] - cb[1]
    draw.text(
        (btn_x + (btn_w - cw) // 2, btn_y + (btn_h - ch) // 2 - 4),
        cta_text, fill="#FFFFFF", font=FONT_CTA
    )
    # Arrow
    arrow_x = btn_x + (btn_w + cw) // 2 + 10
    arrow_y = btn_y + btn_h // 2
    draw.line([(arrow_x, arrow_y), (arrow_x + 18, arrow_y)], fill="#FFFFFF", width=3)
    draw.polygon([
        (arrow_x + 18, arrow_y - 6),
        (arrow_x + 26, arrow_y),
        (arrow_x + 18, arrow_y + 6),
    ], fill="#FFFFFF")

    # ── URL at bottom ──
    url_text = f"wolvestack.com/{url_slug}"
    ub = draw.textbbox((0, 0), url_text, font=FONT_TINY)
    uw = ub[2] - ub[0]
    draw.text(((PIN_W - uw) // 2, PIN_H - 50), url_text, fill="#999999", font=FONT_TINY)

    # ── Bottom accent bar ──
    draw.rectangle([0, PIN_H - 8, PIN_W, PIN_H], fill=accent)

    # ── Save ──
    if filename is None:
        filename = f"pin-{url_slug.replace('.html', '').replace('/', '-')}.png"
    out_path = OUTPUT_DIR / filename
    img.save(out_path, "PNG", quality=95)
    return str(out_path)


# ── Batch generate from pin log ─────────────────────────────────────────────
def generate_from_log(log_path: str = None, limit: int = None):
    """Read the pin log and generate new-style pins for all articles."""
    if log_path is None:
        log_path = Path(__file__).parent / "pinterest-pins-log.json"

    with open(log_path) as f:
        data = json.load(f)

    articles = data.get("pinned_articles", [])
    if limit:
        articles = articles[:limit]

    # Map topic keywords to icon types and palettes
    icon_map = {
        "weight": ("pill", "coral"),
        "muscle": ("syringe", "emerald"),
        "healing": ("cross", "teal"),
        "anti-aging": ("dna", "purple"),
        "longevity": ("dna", "purple"),
        "anxiety": ("atom", "indigo"),
        "immune": ("cross", "teal"),
        "stack": ("molecule", "indigo"),
        "guide": ("molecule", "slate"),
        "sourcing": ("atom", "slate"),
        "women": ("pill", "purple"),
        "men": ("syringe", "indigo"),
        "hair": ("dna", "emerald"),
        "skin": ("dna", "teal"),
        "injury": ("cross", "coral"),
        "tendon": ("cross", "emerald"),
        "sleep": ("atom", "indigo"),
        "cognitive": ("atom", "purple"),
        "athlete": ("syringe", "emerald"),
        "barbie": ("pill", "coral"),
        "dog": ("cross", "emerald"),
    }

    generated = []
    for article in articles:
        title = article.get("title", "")
        filename = article.get("filename", "")
        slug = filename.replace(".html", "")

        # Determine icon/palette from title keywords
        icon_type, palette = "molecule", "teal"
        title_lower = title.lower()
        for keyword, (ic, pal) in icon_map.items():
            if keyword in title_lower:
                icon_type, palette = ic, pal
                break

        # Extract a clean heading and subtitle
        parts = title.split("|")
        heading = parts[0].strip()
        subtitle = parts[1].strip() if len(parts) > 1 else "Evidence-Based Research Guide"

        # Generate contextual bullets from the title
        bullets = _generate_bullets_for_topic(title_lower, heading)

        path = generate_pin(
            heading=heading,
            subtitle=subtitle,
            bullets=bullets,
            url_slug=slug,
            palette_name=palette,
            icon_type=icon_type,
        )
        generated.append(path)
        print(f"  ✓ {os.path.basename(path)}")

    return generated


def _generate_bullets_for_topic(title_lower: str, heading: str) -> list[str]:
    """Generate relevant bullet points based on topic keywords."""
    if "bpc-157" in title_lower and "tb-500" in title_lower:
        return [
            "How each peptide heals differently",
            "Synergistic stacking protocols",
            "Dosing schedules and timing",
            "What the research actually shows",
        ]
    elif "bpc-157" in title_lower and "psychological" in title_lower:
        return [
            "Panic attacks and emotional blunting risks",
            "Dopamine and serotonin mechanisms",
            "SSRI interaction warnings",
            "Recovery timeline and management",
        ]
    elif "bpc-157" in title_lower:
        return [
            "Healing and recovery research",
            "Oral vs injectable protocols",
            "Evidence-based dosing guide",
            "Side effects and safety data",
        ]
    elif "tb-500" in title_lower:
        return [
            "Thymosin Beta-4 mechanism of action",
            "Tissue repair and flexibility data",
            "Reconstitution and dosing guide",
            "Clinical evidence review",
        ]
    elif "ghk-cu" in title_lower and "epithalon" in title_lower:
        return [
            "Skin renewal vs telomere extension",
            "Head-to-head research comparison",
            "Stacking both for maximum benefit",
            "Cost analysis and sourcing tips",
        ]
    elif "weight" in title_lower or "loss" in title_lower:
        return [
            "Peptides that target fat metabolism",
            "GLP-1 receptor agonist overview",
            "Dosing protocols for weight loss",
            "Safety profiles and side effects",
        ]
    elif "muscle" in title_lower or "growth" in title_lower:
        return [
            "Growth hormone secretagogues ranked",
            "IGF-1 and muscle protein synthesis",
            "Optimal stacking combinations",
            "Training and timing protocols",
        ]
    elif "anti-aging" in title_lower or "longevity" in title_lower:
        return [
            "Telomere and epigenetic research",
            "NAD+ and cellular repair peptides",
            "Stacking for maximum lifespan benefit",
            "Cost-effective longevity protocols",
        ]
    elif "anxiety" in title_lower:
        return [
            "Anxiolytic peptides reviewed",
            "GABA and cortisol modulation",
            "Safe stacking combinations",
            "Dosing for cognitive calm",
        ]
    elif "stack" in title_lower:
        return [
            "Synergistic peptide combinations",
            "Goal-specific stack templates",
            "Dosing and cycling schedules",
            "Budget-friendly alternatives",
        ]
    elif "sourcing" in title_lower:
        return [
            "Third-party testing standards",
            "Red flags to watch for",
            "Trusted vendor evaluation criteria",
            "Certificate of analysis guide",
        ]
    elif "immune" in title_lower:
        return [
            "Thymosin alpha-1 and BPC-157 data",
            "Immune modulation mechanisms",
            "Dosing protocols for immunity",
            "Safety and contraindications",
        ]
    elif "women" in title_lower:
        return [
            "Female-specific peptide research",
            "Hormonal considerations",
            "Skin, hair, and wellness peptides",
            "Safety during hormonal cycles",
        ]
    elif "men" in title_lower:
        return [
            "Testosterone and GH optimization",
            "Recovery and performance peptides",
            "Libido and hormonal support",
            "Evidence-based protocols",
        ]
    elif "barbie" in title_lower or "melanotan" in title_lower:
        return [
            "What the TikTok trend won't tell you",
            "Melanotan I vs II safety profiles",
            "Melanoma risk and contraindications",
            "Legal status across countries",
        ]
    elif "dog" in title_lower or "pet" in title_lower or "pup" in title_lower:
        return [
            "LOY-001 and LOY-002 breakthroughs",
            "BPC-157 veterinary applications",
            "The $5.3B pet longevity market",
            "What's available now for your dog",
        ]
    elif "retatrutide" in title_lower:
        return [
            "Triple agonist: GLP-1/GIP/Glucagon",
            "Phase 2: 24.2% weight loss results",
            "Dosing escalation from 0.5 to 12mg",
            "FDA timeline and availability",
        ]
    elif "semaglutide" in title_lower:
        return [
            "GLP-1 mechanism explained simply",
            "Clinical weight loss data reviewed",
            "Ozempic vs Wegovy vs compounded",
            "Side effects and management tips",
        ]
    elif "ipamorelin" in title_lower or "cjc" in title_lower:
        return [
            "Growth hormone pulse optimization",
            "Cleanest GH secretagogue profile",
            "Optimal dosing and timing windows",
            "Stacking with CJC-1295 protocols",
        ]
    elif "9-me-bc" in title_lower or "9mebc" in title_lower:
        return [
            "Dopamine neuron regeneration data",
            "Nootropic and neuroprotective effects",
            "Photosensitivity warnings",
            "Dosing and cycling protocols",
        ]
    elif "hair" in title_lower:
        return [
            "GHK-Cu and follicle regeneration",
            "Topical vs injectable approaches",
            "Clinical evidence for hair regrowth",
            "Combination therapy protocols",
        ]
    elif "sleep" in title_lower:
        return [
            "DSIP and sleep architecture data",
            "Growth hormone release during sleep",
            "Dosing for optimal recovery",
            "Safety and dependency concerns",
        ]
    elif "injury" in title_lower or "tendon" in title_lower or "recovery" in title_lower:
        return [
            "Targeted tissue repair mechanisms",
            "BPC-157 and TB-500 for injuries",
            "Rehabilitation protocol integration",
            "Timeline expectations by injury type",
        ]
    elif "cognitive" in title_lower or "brain" in title_lower or "nootropic" in title_lower:
        return [
            "Neuroprotective peptide research",
            "Memory and focus enhancement data",
            "BDNF and synaptic plasticity",
            "Safe nootropic stacking protocols",
        ]
    elif "athlete" in title_lower:
        return [
            "Performance and recovery peptides",
            "WADA status and testing windows",
            "Injury prevention protocols",
            "Training cycle integration",
        ]
    else:
        return [
            "Evidence-based research review",
            "Dosing and protocol guidelines",
            "Safety profile and side effects",
            "Practical recommendations",
        ]


# ── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        print("Generating all pins from log...")
        paths = generate_from_log()
        print(f"\n✅ Generated {len(paths)} pins in {OUTPUT_DIR}")
    elif len(sys.argv) > 1 and sys.argv[1] == "--sample":
        print("Generating sample pins...")
        samples = [
            {
                "heading": "BPC-157",
                "subtitle": "Complete Research Guide 2026",
                "bullets": [
                    "Healing and recovery mechanisms",
                    "Oral vs injectable protocols",
                    "Evidence-based dosing schedules",
                    "Side effects and safety data",
                ],
                "url_slug": "bpc-157-guide",
                "palette_name": "teal",
                "icon_type": "molecule",
                "filename": "SAMPLE-bpc157.png",
            },
            {
                "heading": "Best Peptides for Weight Loss",
                "subtitle": "Evidence-Based Guide 2026",
                "bullets": [
                    "Peptides that target fat metabolism",
                    "GLP-1 receptor agonist overview",
                    "Dosing protocols for weight loss",
                    "Safety profiles and side effects",
                ],
                "url_slug": "best-peptides-weight-loss",
                "palette_name": "coral",
                "icon_type": "pill",
                "filename": "SAMPLE-weight-loss.png",
            },
            {
                "heading": "Longevity Peptide Stack",
                "subtitle": "Anti-Aging Protocol Guide",
                "bullets": [
                    "Telomere and epigenetic research",
                    "NAD+ and cellular repair peptides",
                    "Stacking for maximum lifespan",
                    "Cost-effective protocols from $100/mo",
                ],
                "url_slug": "longevity-peptide-stack-guide",
                "palette_name": "purple",
                "icon_type": "dna",
                "filename": "SAMPLE-longevity.png",
            },
            {
                "heading": "Dog Longevity Peptides",
                "subtitle": "Puptides, Pettides & LOY-001 Guide",
                "bullets": [
                    "LOY-001 and LOY-002 breakthroughs",
                    "BPC-157 veterinary applications",
                    "The $5.3B pet longevity market",
                    "What's available now for your dog",
                ],
                "url_slug": "dog-longevity-peptides-guide",
                "palette_name": "emerald",
                "icon_type": "cross",
                "filename": "SAMPLE-dog-longevity.png",
            },
        ]
        for s in samples:
            path = generate_pin(**s)
            print(f"  ✓ {os.path.basename(path)}")
        print(f"\n✅ Generated {len(samples)} sample pins in {OUTPUT_DIR}")
    else:
        print("Usage:")
        print("  python pin_generator_v2.py --sample   # Generate 4 sample pins")
        print("  python pin_generator_v2.py --all      # Generate pins for all articles in log")
