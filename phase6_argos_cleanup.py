#!/usr/bin/env python3
"""
Phase 6: Argos translation cleanup for top-traffic languages.
Pattern-based find-replace fixes for known mistranslations and English
residue in es/pt/fr/de file bodies.
"""
import os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Universal patterns (apply to all languages)
UNIVERSAL = [
    # Argos garbage that survived translation
    ('peptid de investigación', 'péptido de investigación'),
    ('Peptid de investigación', 'Péptido de investigación'),
    # English residue boilerplate
    ('Section One Information about this section with practical details.',
     ''),  # Just remove these
    ('Section Two Additional information and context.', ''),
    ('Section Three More comprehensive coverage of the topic.', ''),
    ('Section Four Further details and examples.', ''),
    ('Section Five Additional perspectives and information.', ''),
    ('Section Six Supplementary information.', ''),
    ('Section Seven More comprehensive coverage.', ''),
    ('Section Eight Additional details and guidance.', ''),
    ('Comprehensive guide covering all aspects of this topic with evidence-based information.', ''),
    ('Section 1 Content for section 1.', ''),
    ('Section 2 Content for section 2.', ''),
    ('Section 3 Content for section 3.', ''),
    ('Section 4 Content for section 4.', ''),
    ('Section 5 Content for section 5.', ''),
    ('Section 6 Content for section 6.', ''),
    ('Section 7 Content for section 7.', ''),
    ('Section 8 Content for section 8.', ''),
    ('Section 9 Content for section 9.', ''),
    ('Section 10 Content for section 10.', ''),
]

# Per-language fixes
LANG_FIXES = {
    'es': [
        # Translation artifacts
        ('protocolo de pedofilia', 'protocolo de péptidos'),
        ('Protocolo de pedofilia', 'Protocolo de péptidos'),
        ('Oficina de Desarrollo Forestal', 'FDA'),
        ('aprobación de la Oficina Forestal', 'aprobación de la FDA'),
        ('Reclamación médica', 'Aviso médico'),
        # Common Argos issues we observed
        ('Acaso no hay consejo médico', 'No constituye consejo médico'),
        ('No hay consejo médico', 'No constituye consejo médico'),
        ('Buceo profundo', 'Análisis profundo'),
        ('Buceo profunda', 'Análisis profundo'),
        ('Tema básico', 'Conclusión'),
        ('Banderas rojas', 'Señales de alerta'),
        ('Banderas rojas:', 'Señales de alerta:'),
        ('Bottom Line', 'Conclusión'),
        ('cueva explícita', 'advertencia explícita'),
        # Title case fixes
        ('GROWTH HORMONE', 'Hormona del crecimiento'),
        ('Peptides for Women', 'Péptidos para mujeres'),
        ('Common Reported Side Effects', 'Efectos secundarios comunes reportados'),
        ('Research Context', 'Contexto de la investigación'),
        # Compound name fixes
        ('Péptidos de investigación', 'Péptidos de investigación'),
        # Ad/CTA fixes — leave English brand names but fix surrounding text
        ('Probar Particle', 'Probar Particle Peptides'),
        # Clean up double spaces from removals
    ],
    'pt': [
        ('protocolo de pedofilia', 'protocolo de péptidos'),
        ('Protocolo de pedofilia', 'Protocolo de péptidos'),
        ('Departamento de Desenvolvimento Florestal', 'FDA'),
        ('aprovação do Departamento Florestal', 'aprovação da FDA'),
        ('Reclamação médica', 'Aviso médico'),
        ('Acaso não há conselhos médicos', 'Não constitui aconselhamento médico'),
        ('Não há conselhos médicos', 'Não constitui aconselhamento médico'),
        ('Mergulho profundo', 'Análise aprofundada'),
        ('Tema básico', 'Conclusão'),
        ('Bandeiras vermelhas', 'Sinais de alerta'),
        ('Bottom Line', 'Conclusão'),
        ('caverna explícita', 'advertência explícita'),
        ('com a caverna que', 'com a advertência explícita de que'),
        ('GROWTH HORMONE', 'Hormônio do crescimento'),
        ('Peptides for Women', 'Péptidos para mulheres'),
        ('Common Reported Side Effects', 'Efeitos secundários comuns relatados'),
        ('Research Context', 'Contexto da investigação'),
        ('Research Peptide', 'Péptido de investigação'),
        ('mode los animais', 'modelos animais'),
        ('Mode los animais', 'Modelos animais'),
    ],
    'fr': [
        ('protocole de pédophilie', 'protocole peptidique'),
        ('Protocole de pédophilie', 'Protocole peptidique'),
        ("Bureau de l'aménagement forestier", 'FDA'),
        ('approbation du Bureau forestier', 'approbation de la FDA'),
        ('Réclamation médicale', 'Avertissement médical'),
        ('Peut-être pas de conseil médical', 'Ne constitue pas un avis médical'),
        ('Plongée profonde', 'Analyse approfondie'),
        ('Plongée profonde:', 'Analyse approfondie:'),
        ('Tema básico', 'Conclusion'),
        ('Drapeaux rouges', "Signaux d'alerte"),
        ('Bottom Line', 'Conclusion'),
        ('GROWTH HORMONE', 'Hormone de croissance'),
        ('Peptides for Women', 'Peptides pour femmes'),
        ('Common Reported Side Effects', 'Effets secondaires couramment rapportés'),
        ('Research Context', 'Contexte de la recherche'),
        ('mode les animaux', 'modèles animaux'),
        # Quirky French translations
        ('Un nouveau Peptides ?', 'Nouveau aux peptides ?'),
        ('Un nouveau Peptides?', 'Nouveau aux peptides ?'),
    ],
    'de': [
        ('Pädophilie-Protokoll', 'Peptidprotokoll'),
        ('Pädophilieprotokoll', 'Peptidprotokoll'),
        ('Bundesamt für Forstwirtschaft', 'FDA'),
        ('Genehmigung des Forstamts', 'FDA-Zulassung'),
        ('Medizinische Beschwerde', 'Medizinischer Hinweis'),
        ('Vielleicht keine medizinische Beratung', 'Stellt keine medizinische Beratung dar'),
        ('Tieftauchen', 'Tiefenanalyse'),
        ('Tieftauchgang', 'Tiefenanalyse'),
        ('Tema básico', 'Fazit'),
        ('Rote Flaggen', 'Warnsignale'),
        ('Bottom Line', 'Fazit'),
        ('GROWTH HORMONE', 'Wachstumshormon'),
        ('Peptides for Women', 'Peptide für Frauen'),
        ('Common Reported Side Effects', 'Häufig gemeldete Nebenwirkungen'),
        ('Research Context', 'Forschungskontext'),
        ('Peptide für Forschung', 'Forschungspeptide'),
        ('mode die Tiere', 'Tiermodelle'),
        ('Neu an Peptide?', 'Neu bei Peptiden?'),
    ],
    'it': [
        ('protocollo di pedofilia', 'protocollo peptidico'),
        ('Protocollo di pedofilia', 'Protocollo peptidico'),
        ('Ufficio Forestale', 'FDA'),
        ('approvazione del Bureau Forestale', 'approvazione della FDA'),
        ('Reclamo medico', 'Avviso medico'),
        ('Forse non c\'è alcun consiglio medico', 'Non costituisce un parere medico'),
        ('Immersione profonda', 'Analisi approfondita'),
        ('Bandiere rosse', 'Segnali di allarme'),
        ('Bottom Line', 'Conclusione'),
        ('GROWTH HORMONE', 'Ormone della crescita'),
        ('Peptides for Women', 'Peptidi per donne'),
        ('Common Reported Side Effects', 'Effetti collaterali comuni segnalati'),
        ('Research Context', 'Contesto della ricerca'),
        ('Peptides di ricerca', 'Peptidi di ricerca'),
        ('mode gli animali', 'modelli animali'),
        ('Nuovo a Peptides?', 'Nuovo ai peptidi?'),
    ],
    'ru': [
        ('педофильский протокол', 'пептидный протокол'),
        ('Педофильский протокол', 'Пептидный протокол'),
        ('Лесное ведомство', 'FDA'),
        ('одобрение Лесного ведомства', 'одобрение FDA'),
        ('Медицинская жалоба', 'Медицинское предупреждение'),
        ('Bottom Line', 'Итог'),
        ('GROWTH HORMONE', 'Гормон роста'),
        ('Peptides for Women', 'Пептиды для женщин'),
        ('Common Reported Side Effects', 'Часто сообщаемые побочные эффекты'),
        ('Research Context', 'Контекст исследования'),
    ],
    'pl': [
        ('protokół pedofilski', 'protokół peptydowy'),
        ('Protokół pedofilski', 'Protokół peptydowy'),
        ('Urząd Leśny', 'FDA'),
        ('Bottom Line', 'Wniosek'),
        ('GROWTH HORMONE', 'Hormon wzrostu'),
        ('Peptides for Women', 'Peptydy dla kobiet'),
        ('Common Reported Side Effects', 'Najczęściej zgłaszane skutki uboczne'),
        ('Research Context', 'Kontekst badań'),
    ],
    'nl': [
        ('pedofilieprotocol', 'peptidenprotocol'),
        ('Pedofilieprotocol', 'Peptidenprotocol'),
        ('Bosbouwdepartement', 'FDA'),
        ('goedkeuring van het Bosbouw', 'FDA-goedkeuring'),
        ('Medische klacht', 'Medische waarschuwing'),
        ('Bottom Line', 'Conclusie'),
        ('GROWTH HORMONE', 'Groeihormoon'),
        ('Peptides for Women', 'Peptiden voor vrouwen'),
        ('Common Reported Side Effects', 'Veelvoorkomende gerapporteerde bijwerkingen'),
        ('Research Context', 'Onderzoekscontext'),
    ],
    'id': [
        ('protokol pedofil', 'protokol peptida'),
        ('Protokol pedofil', 'Protokol peptida'),
        ('Departemen Kehutanan', 'FDA'),
        ('persetujuan Departemen Kehutanan', 'persetujuan FDA'),
        ('Bottom Line', 'Kesimpulan'),
        ('GROWTH HORMONE', 'Hormon pertumbuhan'),
        ('Peptides for Women', 'Peptida untuk wanita'),
        ('Common Reported Side Effects', 'Efek samping yang umum dilaporkan'),
        ('Research Context', 'Konteks penelitian'),
    ],
}


def cleanup_file(path, fixes):
    """Apply find-replace patterns to a file."""
    try:
        html = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return False, 0
    orig = html
    repls = 0
    for pat, repl in fixes:
        if pat in html:
            n = html.count(pat)
            html = html.replace(pat, repl)
            repls += n
    # Only run if specific patterns matched — don't normalize whitespace globally
    if html != orig:
        # Only remove empty <p> tags created by our specific replacements
        html = re.sub(r'<p[^>]*>\s*</p>', '', html)
    if html != orig:
        path.write_text(html, encoding='utf-8')
        return True, repls
    return False, 0


def main():
    only_lang = os.environ.get('LANG', None)
    langs_to_process = [only_lang] if only_lang else list(LANG_FIXES.keys())

    grand_total_files = 0
    grand_total_repls = 0
    for lang in langs_to_process:
        d = ROOT / lang
        if not d.is_dir():
            print(f"{lang}: directory not found, skipping")
            continue
        all_fixes = UNIVERSAL + LANG_FIXES[lang]
        files = sorted(d.glob('*.html'))
        fixed = 0
        repls = 0
        for path in files:
            changed, n = cleanup_file(path, all_fixes)
            if changed:
                fixed += 1
                repls += n
        print(f"{lang}: {fixed}/{len(files)} files modified, {repls} replacements")
        grand_total_files += fixed
        grand_total_repls += repls

    print(f"\n=== Phase 6 grand total: {grand_total_files} files, {grand_total_repls} replacements ===")


if __name__ == '__main__':
    main()
