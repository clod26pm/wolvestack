#!/usr/bin/env python3
"""Multi-language bulk pattern fixer for Argos translation artifacts.

Each language gets its own dictionary of (pattern, replacement) pairs.
Patterns target the highest-frequency residual issues:
- "TENIDO WolveStack" / " TEN WolveStack" — corrupted pipe separator
- Hebrew "י" character bug in callout-label
- &quot; HTML entity remnants in article-meta
- English headings left untranslated
- Specific mistranslated words known across the corpus
"""
import os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Universal: applies to all languages (where the pattern survives Argos)
UNIVERSAL = [
    # Title corruption — "TENIDO" / "TEN" appear identically across all languages
    ('Investigación TENIDO WolveStack', 'Investigación | WolveStack'),
    ('TENIDO WolveStack', '| WolveStack'),
    (' TEN WolveStack', ' | WolveStack'),
    # Hebrew character bug
    ('<div class="callout-label">י Route Selection Matters</div>', '<div class="callout-label">🛤️ Route matters</div>'),
    ('<span class="callout-label">י Route Selection Matters</span>', '<span class="callout-label">🛤️ Route matters</span>'),
    ('<div class="callout-label">י ', '<div class="callout-label">🛤️ '),
    ('<span class="callout-label">י ', '<span class="callout-label">🛤️ '),
    # &quot; entity in article-meta
    ('🔬 Investigación &quot; Educación', '🔬 Investigación · Educación'),
    ('🔬 Investigation &quot; Education', '🔬 Investigation · Education'),
    ('🔬 Foundation &quot; Education', '🔬 Foundation · Education'),
    # Common typo
    ('secretogogogo', 'secretagogo'),
    # Brand-name corruption
    ('Apollo Peptide Sciences', 'Apollo Peptide Sciences'),
]

# Language-specific patterns: each list is (pat, repl) tuples
LANGS = {
    'es': [
        ('>Reclamación médica<', '>Aviso médico<'),
        ('Acaso no hay consejos médicos', 'No constituye asesoramiento médico'),
        ('# 12 min read', '📖 12 min de lectura'),
        ('# 14 min read', '📖 14 min de lectura'),
        ('# 15 min read', '📖 15 min de lectura'),
        ('# 18 min read', '📖 18 min de lectura'),
        ('# 10 min read', '📖 10 min de lectura'),
        ('# 8 min read', '📖 8 min de lectura'),
        ('Ø 14 min leer', '📖 14 min de lectura'),
        ('Ø 12 min leer', '📖 12 min de lectura'),
        ('↑ Última revisión', '✅ Última revisión'),
        ('Dive profunda', 'Análisis profundo'),
        ('Peptides de investigación', 'Péptidos de investigación'),
        ('Peptide de investigación', 'Péptido de investigación'),
        ('mode los animales', 'modelos animales'),
        ('Mode los animales', 'Modelos animales'),
        ('bioaspiración', 'biohacking'),
        ('Tema básico', 'Conclusión'),
        ('>Tema</h2>', '>Conclusión</h2>'),
        ('con la caverna que', 'con la advertencia explícita de que'),
        ('con la gruta explícita que', 'con la advertencia explícita de que'),
        ('<h3>Topical</h3>', '<h3>Tópica</h3>'),
        ('Rankeado por la evidencia', 'clasificados por la evidencia'),
        ('Rankeado', 'Clasificados'),
        ('Secretagoga', 'Secretagogo'),
        ('Peptides for Women', 'Péptidos para mujeres'),
        ('GROWTH HORMONE', 'Hormona del crecimiento'),
        ('GHK-Cu: The Copper Peptide Research Roundup', 'GHK-Cu: guía del péptido de cobre'),
    ],
    'pt': [
        ('>Reclamação médica<', '>Aviso médico<'),
        ('Não há conselhos médicos', 'Não constitui aconselhamento médico'),
        ('# 12 min read', '📖 12 min de leitura'),
        ('# 14 min read', '📖 14 min de leitura'),
        ('# 15 min read', '📖 15 min de leitura'),
        ('# 18 min read', '📖 18 min de leitura'),
        ('# 10 min read', '📖 10 min de leitura'),
        ('Peptides de investigação', 'Péptidos de investigação'),
        ('Peptide de investigação', 'Péptido de investigação'),
        ('Peptides for Women', 'Péptidos para mulheres'),
        ('mode los animais', 'modelos animais'),
        ('Dive profunda', 'Análise profunda'),
        ('GROWTH HORMONE', 'Hormônio do crescimento'),
        ('Foundation · Research Peptides', 'Fundamentos · Péptidos de Investigação'),
    ],
    'it': [
        ('>Reclamo medico<', '>Avviso medico<'),
        ('Forse non c\'è alcun consiglio medico', 'Non costituisce un consiglio medico'),
        ('# 12 min read', '📖 12 min di lettura'),
        ('# 14 min read', '📖 14 min di lettura'),
        ('# 15 min read', '📖 15 min di lettura'),
        ('# 18 min read', '📖 18 min di lettura'),
        ('# 10 min read', '📖 10 min di lettura'),
        ('Peptides di ricerca', 'Peptidi di ricerca'),
        ('Peptide di ricerca', 'Peptide di ricerca'),
        ('mode gli animali', 'modelli animali'),
        ('Dive profonda', 'Analisi approfondita'),
        ('GROWTH HORMONE', 'Ormone della crescita'),
        ('Peptides for Women', 'Peptidi per donne'),
    ],
    'fr': [
        ('>Réclamation médicale<', '>Avertissement médical<'),
        ('Peut-être pas de conseil médical', 'Ne constitue pas un avis médical'),
        ('# 12 min read', '📖 12 min de lecture'),
        ('# 14 min read', '📖 14 min de lecture'),
        ('# 15 min read', '📖 15 min de lecture'),
        ('# 18 min read', '📖 18 min de lecture'),
        ('# 10 min read', '📖 10 min de lecture'),
        ('Peptides de recherche', 'Peptides de recherche'),
        ('Peptide de recherche', 'Peptide de recherche'),
        ('mode les animaux', 'modèles animaux'),
        ('Dive profonde', 'Analyse approfondie'),
        ('GROWTH HORMONE', 'Hormone de croissance'),
        ('Peptides for Women', 'Peptides pour femmes'),
    ],
    'de': [
        ('>Medizinische Beschwerde<', '>Medizinischer Hinweis<'),
        ('# 12 min read', '📖 12 min Lesezeit'),
        ('# 14 min read', '📖 14 min Lesezeit'),
        ('# 15 min read', '📖 15 min Lesezeit'),
        ('# 18 min read', '📖 18 min Lesezeit'),
        ('# 10 min read', '📖 10 min Lesezeit'),
        ('Peptide für Forschung', 'Forschungspeptide'),
        ('GROWTH HORMONE', 'Wachstumshormon'),
        ('Peptides for Women', 'Peptide für Frauen'),
        ('mode die Tiere', 'Tiermodelle'),
    ],
    'pl': [
        ('# 12 min read', '📖 12 min czytania'),
        ('# 14 min read', '📖 14 min czytania'),
        ('# 15 min read', '📖 15 min czytania'),
        ('# 18 min read', '📖 18 min czytania'),
        ('# 10 min read', '📖 10 min czytania'),
        ('Peptydy badawcze', 'Peptydy badawcze'),
        ('GROWTH HORMONE', 'Hormon wzrostu'),
        ('Peptides for Women', 'Peptydy dla kobiet'),
    ],
    'ru': [
        ('# 12 min read', '📖 12 мин чтения'),
        ('# 14 min read', '📖 14 мин чтения'),
        ('# 15 min read', '📖 15 мин чтения'),
        ('# 18 min read', '📖 18 мин чтения'),
        ('# 10 min read', '📖 10 мин чтения'),
        ('Peptides for Women', 'Пептиды для женщин'),
        ('GROWTH HORMONE', 'Гормон роста'),
    ],
    'zh': [
        ('# 12 min read', '📖 阅读 12 分钟'),
        ('# 14 min read', '📖 阅读 14 分钟'),
        ('# 15 min read', '📖 阅读 15 分钟'),
        ('# 18 min read', '📖 阅读 18 分钟'),
        ('# 10 min read', '📖 阅读 10 分钟'),
        ('Peptides for Women', '女性研究肽指南'),
        ('GROWTH HORMONE', '生长激素'),
    ],
    'ja': [
        ('# 12 min read', '📖 12分で読める'),
        ('# 14 min read', '📖 14分で読める'),
        ('# 15 min read', '📖 15分で読める'),
        ('# 18 min read', '📖 18分で読める'),
        ('# 10 min read', '📖 10分で読める'),
        ('Peptides for Women', '女性向け研究ペプチド'),
        ('GROWTH HORMONE', '成長ホルモン'),
    ],
    'id': [
        ('# 12 min read', '📖 12 menit baca'),
        ('# 14 min read', '📖 14 menit baca'),
        ('# 15 min read', '📖 15 menit baca'),
        ('# 18 min read', '📖 18 menit baca'),
        ('# 10 min read', '📖 10 menit baca'),
        ('Peptides for Women', 'Peptida untuk wanita'),
        ('GROWTH HORMONE', 'Hormon pertumbuhan'),
    ],
}


def main():
    grand_total_files = 0
    grand_total_repls = 0
    for lang, fixes in LANGS.items():
        d = ROOT / lang
        if not d.is_dir():
            continue
        files = sorted(d.glob('*.html'))
        all_fixes = UNIVERSAL + fixes
        fixed = 0
        repls = 0
        for f in files:
            try:
                content = f.read_text(encoding='utf-8')
            except Exception:
                continue
            orig = content
            file_repls = 0
            for pat, repl in all_fixes:
                if pat in content:
                    n = content.count(pat)
                    content = content.replace(pat, repl)
                    file_repls += n
            if content != orig:
                f.write_text(content, encoding='utf-8')
                fixed += 1
                repls += file_repls
        print(f"{lang}: {fixed}/{len(files)} files updated, {repls} replacements", flush=True)
        grand_total_files += fixed
        grand_total_repls += repls
    print(f"\nTOTAL: {grand_total_files} files updated, {grand_total_repls} replacements", flush=True)


if __name__ == '__main__':
    main()
