#!/usr/bin/env python3
"""
One-shot internal linker — adds Related Guides sections to older articles
that should link to the recently-published new articles.

Strategy:
- Each entry maps an older article -> list of (slug, title) tuples to inject.
- If the article already has a `<div class="related-articles"` block, we APPEND new
  links to its <ul>, preserving the existing template. We only add links not already
  present and we never push the total <li> count beyond 5 inside that div.
- If no related-articles block exists, we insert a fresh one immediately before
  the first <footer ...> tag.
- We never touch language subdirectories (only root html files).
- We do not touch index, privacy, terms, sitemap, robots, 404, about, affiliate-disclosure.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent

# Map: older article filename -> [(slug, anchor_text), ...]
PLAN: dict[str, list[tuple[str, str]]] = {
    # ---- BPC-157 cluster: route to new joint-pain & arthritis articles ----
    "bpc-157-faq.html": [
        ("bpc-157-for-arthritis", "BPC-157 for Arthritis: Research, Protocol & What to Expect"),
        ("bpc-157-for-joint-pain", "BPC-157 for Joint Pain: Research & Dosing Protocol"),
        ("bpc-157-for-injury-recovery", "BPC-157 for Injury Recovery"),
        ("bpc-157-vs-cortisone-injection", "BPC-157 vs Cortisone Injection"),
        ("bpc-157-guide", "BPC-157 Complete Guide"),
    ],
    "bpc-157-side-effects.html": [
        ("bpc-157-for-arthritis", "BPC-157 for Arthritis: Research, Protocol & What to Expect"),
        ("bpc-157-for-joint-pain", "BPC-157 for Joint Pain: Research & Dosing Protocol"),
        ("bpc-157-vs-cortisone-injection", "BPC-157 vs Cortisone Injection"),
        ("bpc-157-guide", "BPC-157 Complete Guide"),
    ],
    "bpc-157-dosage.html": [
        ("bpc-157-for-arthritis", "BPC-157 for Arthritis: Research, Protocol & What to Expect"),
        ("bpc-157-for-joint-pain", "BPC-157 for Joint Pain: Research & Dosing Protocol"),
        ("bpc-157-for-injury-recovery", "BPC-157 for Injury Recovery"),
        ("bpc-157-guide", "BPC-157 Complete Guide"),
    ],
    "bpc-157-cycle.html": [
        ("bpc-157-for-arthritis", "BPC-157 for Arthritis: Research, Protocol & What to Expect"),
        ("bpc-157-for-joint-pain", "BPC-157 for Joint Pain: Research & Dosing Protocol"),
        ("bpc-157-for-injury-recovery", "BPC-157 for Injury Recovery"),
        ("bpc-157-guide", "BPC-157 Complete Guide"),
    ],
    "bpc-157-for-tendonitis.html": [
        ("bpc-157-for-arthritis", "BPC-157 for Arthritis: Research, Protocol & What to Expect"),
        ("bpc-157-for-joint-pain", "BPC-157 for Joint Pain: Research & Dosing Protocol"),
        ("bpc-157-vs-cortisone-injection", "BPC-157 vs Cortisone Injection"),
        ("bpc-157-for-injury-recovery", "BPC-157 for Injury Recovery"),
    ],
    "bpc-157-for-back-pain.html": [
        ("bpc-157-for-arthritis", "BPC-157 for Arthritis: Research, Protocol & What to Expect"),
        ("bpc-157-for-joint-pain", "BPC-157 for Joint Pain: Research & Dosing Protocol"),
        ("bpc-157-for-injury-recovery", "BPC-157 for Injury Recovery"),
        ("bpc-157-guide", "BPC-157 Complete Guide"),
    ],
    "bpc-157-vs-cortisone-injection.html": [
        ("bpc-157-for-arthritis", "BPC-157 for Arthritis: Research, Protocol & What to Expect"),
        ("bpc-157-for-joint-pain", "BPC-157 for Joint Pain: Research & Dosing Protocol"),
        ("retatrutide-for-osteoarthritis", "Retatrutide for Osteoarthritis: TRIUMPH-4 Phase 3 Results"),
        ("retatrutide-for-joint-pain", "Retatrutide for Joint Pain"),
    ],
    # ---- Semaglutide cluster: route to half-life, what-happens, vs-gastric-sleeve ----
    "semaglutide-for-weight-loss.html": [
        ("semaglutide-half-life", "Semaglutide Half-Life: Pharmacokinetics & Duration"),
        ("semaglutide-what-happens-when-you-stop", "Semaglutide: What Happens When You Stop"),
        ("post-glp1-weight-maintenance-guide", "Post-GLP-1 Weight Maintenance Guide"),
        ("microdose-semaglutide-guide", "Microdose Semaglutide Guide"),
        ("semaglutide-vs-gastric-sleeve", "Semaglutide vs Gastric Sleeve"),
    ],
    "semaglutide-stacking.html": [
        ("semaglutide-half-life", "Semaglutide Half-Life: Pharmacokinetics & Duration"),
        ("semaglutide-what-happens-when-you-stop", "Semaglutide: What Happens When You Stop"),
        ("microdose-semaglutide-guide", "Microdose Semaglutide Guide"),
        ("post-glp1-weight-maintenance-guide", "Post-GLP-1 Weight Maintenance Guide"),
    ],
    # ---- Tirzepatide cluster ----
    "tirzepatide-vs-semaglutide.html": [
        ("tirzepatide-half-life", "Tirzepatide Half-Life: Pharmacokinetics & Dosing"),
        ("semaglutide-half-life", "Semaglutide Half-Life: Pharmacokinetics & Duration"),
        ("tirzepatide-what-happens-when-you-stop", "Tirzepatide: What Happens When You Stop"),
        ("semaglutide-what-happens-when-you-stop", "Semaglutide: What Happens When You Stop"),
        ("post-glp1-weight-maintenance-guide", "Post-GLP-1 Weight Maintenance Guide"),
    ],
    # ---- Retatrutide cluster: extend the 2-link sections in dosage/cycle/how-it-works/vs-tirzepatide ----
    "retatrutide-dosage.html": [
        ("retatrutide-dysesthesia-side-effect", "Retatrutide Dysesthesia: TRIUMPH-4 Safety Signal"),
        ("retatrutide-for-osteoarthritis", "Retatrutide for Osteoarthritis: TRIUMPH-4 Phase 3 Results"),
        ("retatrutide-for-joint-pain", "Retatrutide for Joint Pain: Beyond Knee OA"),
    ],
    "retatrutide-cycle.html": [
        ("retatrutide-dysesthesia-side-effect", "Retatrutide Dysesthesia: TRIUMPH-4 Safety Signal"),
        ("retatrutide-for-osteoarthritis", "Retatrutide for Osteoarthritis: TRIUMPH-4 Phase 3 Results"),
        ("retatrutide-for-joint-pain", "Retatrutide for Joint Pain: Beyond Knee OA"),
    ],
    "retatrutide-how-it-works.html": [
        ("retatrutide-dysesthesia-side-effect", "Retatrutide Dysesthesia: TRIUMPH-4 Safety Signal"),
        ("retatrutide-for-osteoarthritis", "Retatrutide for Osteoarthritis: TRIUMPH-4 Phase 3 Results"),
        ("retatrutide-for-joint-pain", "Retatrutide for Joint Pain: Beyond Knee OA"),
    ],
    "retatrutide-vs-tirzepatide.html": [
        ("retatrutide-dysesthesia-side-effect", "Retatrutide Dysesthesia: TRIUMPH-4 Safety Signal"),
        ("retatrutide-for-osteoarthritis", "Retatrutide for Osteoarthritis: TRIUMPH-4 Phase 3 Results"),
        ("retatrutide-for-joint-pain", "Retatrutide for Joint Pain: Beyond Knee OA"),
    ],
    # ---- Best-of pages route to maintenance + half-life articles ----
    "best-peptides-for-weight-loss.html": [
        ("semaglutide-half-life", "Semaglutide Half-Life: Pharmacokinetics & Duration"),
        ("tirzepatide-half-life", "Tirzepatide Half-Life: Pharmacokinetics & Dosing"),
        ("semaglutide-what-happens-when-you-stop", "Semaglutide: What Happens When You Stop"),
        ("tirzepatide-what-happens-when-you-stop", "Tirzepatide: What Happens When You Stop"),
        ("semaglutide-vs-gastric-sleeve", "Semaglutide vs Gastric Sleeve"),
    ],
    "best-peptides-for-fat-loss.html": [
        ("semaglutide-what-happens-when-you-stop", "Semaglutide: What Happens When You Stop"),
        ("tirzepatide-what-happens-when-you-stop", "Tirzepatide: What Happens When You Stop"),
        ("microdose-tirzepatide-guide", "Microdose Tirzepatide Guide"),
    ],
    "best-peptides-2026.html": [
        ("retatrutide-dysesthesia-side-effect", "Retatrutide Dysesthesia: TRIUMPH-4 Safety Signal"),
        ("retatrutide-for-osteoarthritis", "Retatrutide for Osteoarthritis"),
        ("post-glp1-weight-maintenance-guide", "Post-GLP-1 Weight Maintenance Guide"),
        ("fda-pcac-docket-2026", "FDA PCAC Docket FDA-2025-N-6895: Public Comment Guide"),
    ],
    # ---- Regulatory routing ----
    "peptide-regulations-2026.html": [
        ("retatrutide-dysesthesia-side-effect", "Retatrutide Dysesthesia: TRIUMPH-4 Safety Signal"),
    ],
}


RELATED_TEMPLATE = '''<div class="related-articles" style="margin:2rem auto;padding:1.5rem;background:#f8f9fa;border-radius:8px;border-left:4px solid #6c63ff;max-width:800px">
  <h3 style="margin:0 0 1rem;color:#1a1a2e;font-size:1.1rem">Related Guides</h3>
  <ul style="margin:0;padding-left:1.2rem;line-height:2">
{items}
  </ul>
</div>

'''

LI_TEMPLATE = '    <li><a href="/{slug}.html" style="color:#6c63ff">{title}</a></li>'

RELATED_DIV_RE = re.compile(
    r'(<div class="related-articles"[^>]*>.*?<ul[^>]*>)(.*?)(</ul>\s*</div>)',
    re.DOTALL,
)


def append_to_existing(html: str, candidates: list[tuple[str, str]]) -> tuple[str, int]:
    m = RELATED_DIV_RE.search(html)
    if not m:
        return html, 0
    head, ul_inner, tail = m.group(1), m.group(2), m.group(3)

    existing_count = ul_inner.count("<li")
    if existing_count >= 5:
        return html, 0  # already maxed

    added = 0
    new_lis = []
    for slug, title in candidates:
        if existing_count + added >= 5:
            break
        # Skip if already linked anywhere in the file
        if f'/{slug}.html' in html:
            continue
        new_lis.append(LI_TEMPLATE.format(slug=slug, title=title))
        added += 1

    if not new_lis:
        return html, 0

    # Insert the new LIs at the end of the existing UL, preserving formatting
    # If ul_inner ends with whitespace+newline, append before the final close
    if ul_inner.endswith("\n  "):
        injection = "\n".join(new_lis) + "\n  "
        new_block = head + ul_inner.rstrip() + "\n" + "\n".join(new_lis) + "\n  " + tail
    else:
        new_block = head + ul_inner.rstrip("\n ") + "\n" + "\n".join(new_lis) + "\n  " + tail

    return html.replace(m.group(0), new_block, 1), added


def insert_new_block(html: str, candidates: list[tuple[str, str]]) -> tuple[str, int]:
    # Filter candidates that are already linked
    items = []
    added = 0
    for slug, title in candidates:
        if added >= 5:
            break
        if f'/{slug}.html' in html:
            continue
        items.append(LI_TEMPLATE.format(slug=slug, title=title))
        added += 1
    if not items:
        return html, 0

    block = RELATED_TEMPLATE.format(items="\n".join(items))

    # Insert before the first <footer ...> tag
    footer_re = re.compile(r'(<footer\b[^>]*>)', re.IGNORECASE)
    m = footer_re.search(html)
    if m:
        return html[:m.start()] + block + html[m.start():], added

    # Fallback: insert before </body>
    body_close_re = re.compile(r'(</body>)', re.IGNORECASE)
    m = body_close_re.search(html)
    if m:
        return html[:m.start()] + block + html[m.start():], added
    return html, 0


def process(filename: str, candidates: list[tuple[str, str]]) -> tuple[bool, int, str]:
    p = ROOT / filename
    if not p.exists():
        return False, 0, "missing"
    html = p.read_text(encoding="utf-8")

    if RELATED_DIV_RE.search(html):
        new_html, added = append_to_existing(html, candidates)
        mode = "extended"
    else:
        new_html, added = insert_new_block(html, candidates)
        mode = "inserted"

    if added > 0 and new_html != html:
        p.write_text(new_html, encoding="utf-8")
        return True, added, mode
    return False, 0, mode


def main():
    total_added = 0
    files_changed = 0
    print(f"{'FILE':50s} {'MODE':10s} {'ADDED':>6s}")
    print("-" * 70)
    for fname, candidates in PLAN.items():
        ok, added, mode = process(fname, candidates)
        marker = "OK" if ok else "--"
        print(f"{marker} {fname:47s} {mode:10s} {added:>6d}")
        if ok:
            files_changed += 1
            total_added += added
    print("-" * 70)
    print(f"Files changed: {files_changed}")
    print(f"Total links added: {total_added}")


if __name__ == "__main__":
    main()
