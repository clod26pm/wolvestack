#!/usr/bin/env python3
"""Round 2 bulk polish — patterns observed in non-Spanish language directories
after the initial pass. Each language gets language-specific replacements for
the most common English residues and Argos artifacts."""
import os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Patterns shared across all languages — these survived the first round
UNIVERSAL = [
    ('  ←  ', ' | '),
    (' ← WolveStack', ' | WolveStack'),
    ('— WolveStack', '| WolveStack'),
    # Half-translated h1 with em
    ('<em>Iniciar Aqui</em>', '<em>Comece aqui</em>'),  # pt
    ('<em>Hier klicken</em>', '<em>Hier starten</em>'),  # de
    ('<em>詳細はこちら</em>', '<em>ここから始める</em>'),  # ja
    # English headings that survived
    ('<h3>Topical</h3>', '<h3>Tópica</h3>'),  # also es
    ('<h3>Side Effects</h3>', '<h3>Side Effects</h3>'),
    ('Foundation · Research Peptides', 'Fundamentos · Péptidos'),
]

LANGS = {
    'pt': [
        # Title-level fixes
        ('Novo em Peptídeos? Começar aqui — Peptídeos de pesquisa 101', 'Novo em péptidos? Comece aqui — Péptidos de investigação 101 | WolveStack'),
        ('<em>Iniciar Aqui</em>', '<em>Comece aqui</em>'),
        ('Novo em Peptídeos?<em>', 'Novo em péptidos? <em>'),
        ('Peptídeos de pesquisa', 'Péptidos de investigação'),
        ('# 12 min read', '📖 12 min de leitura'),
        ('# 14 min read', '📖 14 min de leitura'),
        ('# 15 min read', '📖 15 min de leitura'),
        ('# 18 min read', '📖 18 min de leitura'),
        ('# 10 min read', '📖 10 min de leitura'),
        ('# 8 min read', '📖 8 min de leitura'),
        ('Acaso não há conselhos médicos', 'Não constitui aconselhamento médico'),
        ('Não há conselhos médicos', 'Não constitui aconselhamento médico'),
        ('>Reclamação médica<', '>Aviso médico<'),
        ('mode los animais', 'modelos animais'),
        ('Mode los animais', 'Modelos animais'),
        ('mode los animales', 'modelos animais'),  # Argos sometimes mixed
        ('Dive profunda', 'Análise profunda'),
        ('Tema básico', 'Conclusão'),
        ('Banderas vermelhas', 'Sinais de alerta'),
        ('Bottom Line', 'Conclusão'),
        ('caverna explícita', 'advertência explícita'),
        ('com a caverna que', 'com a advertência explícita de que'),
        ('GROWTH HORMONE', 'Hormônio do crescimento'),
        ('Peptides for Women', 'Péptidos para mulheres'),
        ('Common Reported Side Effects', 'Efeitos secundários comuns relatados'),
        ('Research Context', 'Contexto da investigação'),
        ('Research Peptide', 'Péptido de investigação'),
        ('Sourcing Best Practices', 'Boas práticas de abastecimento'),
        ('Bottom Line', 'Conclusão'),
    ],
    'it': [
        ('Nuovo a Peptides?', 'Nuovo ai peptidi?'),
        ('Avviare qui — Peptidi di ricerca 101', 'Inizia qui — Peptidi di ricerca 101 | WolveStack'),
        ('Avviare qui', 'Inizia qui'),
        ('# 12 min read', '📖 12 min di lettura'),
        ('# 14 min read', '📖 14 min di lettura'),
        ('# 15 min read', '📖 15 min di lettura'),
        ('# 18 min read', '📖 18 min di lettura'),
        ('# 10 min read', '📖 10 min di lettura'),
        ('# 8 min read', '📖 8 min di lettura'),
        ('Non costituisce consiglio medico', 'Non costituisce un parere medico'),
        ('Forse non c\'è alcun consiglio medico', 'Non costituisce un parere medico'),
        ('>Reclamo medico<', '>Avviso medico<'),
        ('Peptides di ricerca', 'Peptidi di ricerca'),
        ('Peptide di ricerca', 'Peptide di ricerca'),
        ('mode gli animali', 'modelli animali'),
        ('Dive profonda', 'Analisi approfondita'),
        ('Tema básico', 'Conclusione'),
        ('Bottom Line', 'Conclusione'),
        ('caverna esplicita', 'avvertenza esplicita'),
        ('GROWTH HORMONE', 'Ormone della crescita'),
        ('Peptides for Women', 'Peptidi per donne'),
        ('Common Reported Side Effects', 'Effetti collaterali comuni segnalati'),
        ('Research Context', 'Contesto della ricerca'),
    ],
    'fr': [
        ('Un nouveau Peptides ?', 'Nouveau aux peptides ?'),
        ('Un nouveau Peptides ?<em>', 'Nouveau aux peptides ? <em>'),
        ('Un nouveau Peptides ? Commencez ici — Peptides de recherche 101.', 'Nouveau aux peptides ? Commencez ici — Peptides de recherche 101 | WolveStack'),
        ('# 12 min read', '📖 12 min de lecture'),
        ('# 14 min read', '📖 14 min de lecture'),
        ('# 15 min read', '📖 15 min de lecture'),
        ('# 18 min read', '📖 18 min de lecture'),
        ('# 10 min read', '📖 10 min de lecture'),
        ('# 8 min read', '📖 8 min de lecture'),
        ('Ne constitue pas un avis médical', 'Ne constitue pas un avis médical'),
        ('Peut-être pas de conseil médical', 'Ne constitue pas un avis médical'),
        ('>Réclamation médicale<', '>Avertissement médical<'),
        ('mode les animaux', 'modèles animaux'),
        ('Dive profonde', 'Analyse approfondie'),
        ('Tema básico', 'Conclusion'),
        ('Bottom Line', 'Conclusion'),
        ('GROWTH HORMONE', 'Hormone de croissance'),
        ('Peptides for Women', 'Peptides pour femmes'),
        ('Common Reported Side Effects', 'Effets secondaires couramment rapportés'),
        ('Research Context', 'Contexte de la recherche'),
    ],
    'de': [
        ('Neu an Peptide?', 'Neu bei Peptiden?'),
        ('<em>Hier klicken</em>', '<em>Hier starten</em>'),
        ('Neu an Peptide? Starten Sie hier – Forschungspeptide 101 | WolveStack', 'Neu bei Peptiden? Hier starten — Forschungspeptide 101 | WolveStack'),
        ('# 12 min read', '📖 12 Min. Lesezeit'),
        ('# 14 min read', '📖 14 Min. Lesezeit'),
        ('# 15 min read', '📖 15 Min. Lesezeit'),
        ('# 18 min read', '📖 18 Min. Lesezeit'),
        ('# 10 min read', '📖 10 Min. Lesezeit'),
        ('# 8 min read', '📖 8 Min. Lesezeit'),
        ('Vielleicht keine medizinische Beratung', 'Stellt keine medizinische Beratung dar'),
        ('>Medizinische Beschwerde<', '>Medizinischer Hinweis<'),
        ('Peptide für Forschung', 'Forschungspeptide'),
        ('mode die Tiere', 'Tiermodelle'),
        ('Dive tief', 'Tiefenanalyse'),
        ('Bottom Line', 'Fazit'),
        ('Tema básico', 'Fazit'),
        ('GROWTH HORMONE', 'Wachstumshormon'),
        ('Peptides for Women', 'Peptide für Frauen'),
        ('Common Reported Side Effects', 'Häufig gemeldete Nebenwirkungen'),
        ('Research Context', 'Forschungskontext'),
    ],
    'zh': [
        ('# 12 min read', '📖 阅读时间 12 分钟'),
        ('# 14 min read', '📖 阅读时间 14 分钟'),
        ('# 15 min read', '📖 阅读时间 15 分钟'),
        ('# 18 min read', '📖 阅读时间 18 分钟'),
        ('# 10 min read', '📖 阅读时间 10 分钟'),
        ('# 8 min read', '📖 阅读时间 8 分钟'),
        ('QPEPTIDE', '| WolveStack'),
        ('新到Peptides吗', '初次接触肽?'),
        ('Peptides for Women', '女性研究肽指南'),
        ('GROWTH HORMONE', '生长激素'),
        ('Bottom Line', '结论'),
        ('Common Reported Side Effects', '常见报告的副作用'),
        ('Research Context', '研究背景'),
        ('Research Peptide', '研究用肽'),
    ],
    'ja': [
        ('# 12 min read', '📖 12分で読了'),
        ('# 14 min read', '📖 14分で読了'),
        ('# 15 min read', '📖 15分で読了'),
        ('# 18 min read', '📖 18分で読了'),
        ('# 10 min read', '📖 10分で読了'),
        ('# 8 min read', '📖 8分で読了'),
        ('ペプチドに新しい?', 'ペプチド初心者の方へ'),
        ('<em>詳細はこちら</em>', '<em>ここから始めましょう</em>'),
        ('Peptides for Women', '女性向け研究用ペプチド'),
        ('GROWTH HORMONE', '成長ホルモン'),
        ('Bottom Line', '結論'),
        ('Common Reported Side Effects', '報告されている一般的な副作用'),
        ('Research Context', '研究の背景'),
        ('Research Peptide', '研究用ペプチド'),
    ],
    'ru': [
        ('# 12 min read', '📖 12 мин чтения'),
        ('# 14 min read', '📖 14 мин чтения'),
        ('# 15 min read', '📖 15 мин чтения'),
        ('# 18 min read', '📖 18 мин чтения'),
        ('# 10 min read', '📖 10 мин чтения'),
        ('# 8 min read', '📖 8 мин чтения'),
        ('Peptides for Women', 'Пептиды для женщин'),
        ('GROWTH HORMONE', 'Гормон роста'),
        ('Bottom Line', 'Итог'),
        ('Common Reported Side Effects', 'Часто сообщаемые побочные эффекты'),
        ('Research Context', 'Контекст исследования'),
    ],
    'pl': [
        ('# 12 min read', '📖 12 min czytania'),
        ('# 14 min read', '📖 14 min czytania'),
        ('# 15 min read', '📖 15 min czytania'),
        ('# 18 min read', '📖 18 min czytania'),
        ('# 10 min read', '📖 10 min czytania'),
        ('Peptides for Women', 'Peptydy dla kobiet'),
        ('GROWTH HORMONE', 'Hormon wzrostu'),
        ('Bottom Line', 'Wniosek'),
        ('Common Reported Side Effects', 'Najczęściej zgłaszane skutki uboczne'),
        ('Research Context', 'Kontekst badań'),
    ],
    'id': [
        ('# 12 min read', '📖 12 menit membaca'),
        ('# 14 min read', '📖 14 menit membaca'),
        ('# 15 min read', '📖 15 menit membaca'),
        ('# 18 min read', '📖 18 menit membaca'),
        ('# 10 min read', '📖 10 menit membaca'),
        ('Peptides for Women', 'Peptida untuk wanita'),
        ('GROWTH HORMONE', 'Hormon pertumbuhan'),
        ('Bottom Line', 'Kesimpulan'),
        ('Common Reported Side Effects', 'Efek samping yang umum dilaporkan'),
        ('Research Context', 'Konteks penelitian'),
    ],
}


def main():
    grand_total_files = 0
    grand_total_repls = 0
    for lang, fixes in LANGS.items():
        d = ROOT / lang
        if not d.is_dir(): continue
        files = sorted(d.glob('*.html'))
        all_fixes = UNIVERSAL + fixes
        fixed = 0
        repls = 0
        for f in files:
            try: content = f.read_text(encoding='utf-8')
            except: continue
            orig = content
            fr = 0
            for pat, repl in all_fixes:
                if pat in content:
                    n = content.count(pat)
                    content = content.replace(pat, repl)
                    fr += n
            if content != orig:
                f.write_text(content, encoding='utf-8')
                fixed += 1
                repls += fr
        print(f"{lang}: {fixed}/{len(files)} files, {repls} replacements", flush=True)
        grand_total_files += fixed
        grand_total_repls += repls
    print(f"\nTOTAL round 2: {grand_total_files} files, {grand_total_repls} replacements")


if __name__ == '__main__':
    main()
