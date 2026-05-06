#!/usr/bin/env python3
"""Bulk-fix high-frequency Argos translation artifacts across all Spanish files.
Pattern-based replacement only — safe, fast, idempotent."""
import os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANG_DIR = ROOT / 'es'

# Critical pattern-based fixes — most common Argos artifacts.
FIXES = [
    # Title corruption (appears in many files)
    ('Investigación TENIDO WolveStack', 'Investigación | WolveStack'),
    ('TENIDO WolveStack', '| WolveStack'),
    (' TEN WolveStack', ' | WolveStack'),
    ('Complete Research Guide 2026', 'guía completa de investigación 2026'),
    # Disclaimer label
    ('>Reclamación médica<', '>Aviso médico<'),
    ('Acaso no hay consejos médicos', 'No constituye asesoramiento médico'),
    # Article meta artifacts
    ('# 12 min read', '📖 12 min de lectura'),
    ('# 14 min read', '📖 14 min de lectura'),
    ('# 15 min read', '📖 15 min de lectura'),
    ('# 18 min read', '📖 18 min de lectura'),
    ('# 10 min read', '📖 10 min de lectura'),
    ('# 8 min read', '📖 8 min de lectura'),
    ('Ø 14 min leer', '📖 14 min de lectura'),
    ('Ø 12 min leer', '📖 12 min de lectura'),
    ('↑ Última revisión', '✅ Última revisión'),
    ('🔬 Investigación &quot; Educación', '🔬 Investigación · Educación'),
    ('🔬 Foundation &quot; Education', '🔬 Fundamentos · Educación'),
    ('🔬 Foundation " Education', '🔬 Fundamentos · Educación'),
    ('🔬 Investigación " Educación', '🔬 Investigación · Educación'),
    # Common term errors
    ('Dive profunda', 'Análisis profundo'),
    ('Peptides de investigación', 'Péptidos de investigación'),
    ('Peptide de investigación', 'Péptido de investigación'),
    ('Peptides farmaceuticos', 'péptidos farmacéuticos'),
    ('Peptide Suplementos', 'suplementos peptídicos'),
    ('mode los animales', 'modelos animales'),
    ('Mode los animales', 'Modelos animales'),
    ('bioaspiración', 'biohacking'),
    ('Tema básico', 'Conclusión'),
    ('>Tema</h2>', '>Conclusión</h2>'),
    # Hebrew character artifact
    ('י Route Selection Matters', '🛤️ La elección de la vía importa'),
    ('<div class="callout-label">י ', '<div class="callout-label">🛤️ '),
    # Caves/cavern/grotto translation errors
    ('con la caverna que no son para el consumo humano', 'con la advertencia explícita de que no son aptos para el consumo humano'),
    ('con la caverna que', 'con la advertencia explícita de que'),
    ('con la gruta explícita que', 'con la advertencia explícita de que'),
    ('la gruta explícita que', 'la advertencia explícita de que'),
    # Typos
    ('secretogogogo', 'secretagogo'),
    # English-language headings (most common)
    ('<h3>Topical</h3>', '<h3>Tópica</h3>'),
    ('<h3>Common Reported Side Effects</h3>', '<h3>Efectos secundarios comunes reportados</h3>'),
    ('<h3>Actin Sequestration and Cell Migration</h3>', '<h3>Secuestro de actina y migración celular</h3>'),
    ('<h3>FAK-Paxillin Pathway Activation:</h3>', '<h3>Activación de la vía FAK-paxilina:</h3>'),
    ('<span class="callout-label">Research Context</span>', '<span class="callout-label">Contexto de la investigación</span>'),
    ('<div class="callout-label">Research Context</div>', '<div class="callout-label">Contexto de la investigación</div>'),
    # Article labels in EN
    ('GROWTH HORMONE', 'Hormona del crecimiento'),
    # Dose label
    ('<th>Dose</th>', '<th>Dosis</th>'),
    ('<th>BPC-157 Dose</th>', '<th>Dosis de BPC-157</th>'),
    ('<th>TB-500 Dose</th>', '<th>Dosis de TB-500</th>'),
    # Misc
    ('Rankeado por la evidencia', 'clasificados por la evidencia'),
    ('Rankeado por evidencia', 'clasificados por evidencia'),
    ('Secretagoga GH', 'Secretagogo de GH'),
    ('La Secretagoga GH más limpia', 'el secretagogo de GH más limpio'),
    ('GHK-Cu: The Copper Peptide Research Roundup', 'GHK-Cu: guía del péptido de cobre'),
    ('Peptides for Women', 'Péptidos para mujeres'),
]

def main():
    if not LANG_DIR.is_dir():
        print(f"ERROR: {LANG_DIR} not found"); sys.exit(1)
    files = sorted(LANG_DIR.glob('*.html'))
    print(f"Scanning {len(files)} files...", flush=True)
    fixed = 0
    total_replacements = 0
    for f in files:
        try:
            content = f.read_text(encoding='utf-8')
        except Exception as e:
            continue
        orig = content
        file_replacements = 0
        for pat, repl in FIXES:
            new_content, n = re.subn(re.escape(pat), repl, content)
            if n > 0:
                content = new_content
                file_replacements += n
        if file_replacements:
            f.write_text(content, encoding='utf-8')
            fixed += 1
            total_replacements += file_replacements
    print(f"Fixed {fixed} files, {total_replacements} total replacements")

if __name__ == '__main__':
    main()
