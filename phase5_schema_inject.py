#!/usr/bin/env python3
"""
Phase 5: Schema injection for 9 remaining languages.
Adds FAQ JSON-LD schema and internal cross-links to existing
es/pt/fr/de/it/ru/pl/nl/id pages WITHOUT rewriting body content.

Goal: preserve Argos translation length (median 6-8k chars) while adding
GEO/SEO infrastructure (FAQ schema, cross-links).
"""
import os, re, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LANGUAGES = ['es', 'pt', 'fr', 'de', 'it', 'ru', 'pl', 'nl', 'id']

# Per-language strings for FAQ generation
LANG_STRINGS = {
    'es': {
        'q_what': '¿Qué es {name}?',
        'q_mech': '¿Cómo funciona {name}?',
        'q_dose': '¿Cuáles son las dosis de investigación típicas para {name}?',
        'q_safety': '¿Cuáles son las principales consideraciones de seguridad?',
        'q_fda': '¿Está {name} aprobado por la FDA?',
        'a_fda': 'El estado regulatorio de la FDA depende del compuesto específico. La mayoría de los péptidos de investigación no están aprobados por la FDA para uso humano y se venden como productos químicos de investigación únicamente para uso de laboratorio.',
        'related_h2': 'Compuestos de investigación relacionados',
        'related_intro': 'Si está investigando {name}, los compuestos que probablemente querrá ver a continuación son',
        'related_outro': 'Estos aparecen con mayor frecuencia en los mismos contextos de investigación como alternativas o compuestos complementarios.',
    },
    'pt': {
        'q_what': 'O que é {name}?',
        'q_mech': 'Como o {name} funciona?',
        'q_dose': 'Quais são as doses típicas de pesquisa para {name}?',
        'q_safety': 'Quais são as principais considerações de segurança?',
        'q_fda': '{name} é aprovado pela FDA?',
        'a_fda': 'O status regulatório da FDA depende do composto específico. A maioria dos peptídeos de pesquisa não é aprovada pela FDA para uso humano e é vendida como produtos químicos de pesquisa apenas para uso laboratorial.',
        'related_h2': 'Compostos de pesquisa relacionados',
        'related_intro': 'Se você está pesquisando {name}, os compostos que provavelmente vai querer ver em seguida são',
        'related_outro': 'Estes aparecem com mais frequência nos mesmos contextos de pesquisa como alternativas ou compostos complementares.',
    },
    'fr': {
        'q_what': 'Qu\'est-ce que {name}?',
        'q_mech': 'Comment fonctionne {name}?',
        'q_dose': 'Quelles sont les doses de recherche typiques pour {name}?',
        'q_safety': 'Quelles sont les principales considérations de sécurité?',
        'q_fda': '{name} est-il approuvé par la FDA?',
        'a_fda': 'Le statut réglementaire de la FDA dépend du composé spécifique. La plupart des peptides de recherche ne sont pas approuvés par la FDA pour un usage humain et sont vendus comme produits chimiques de recherche pour usage de laboratoire uniquement.',
        'related_h2': 'Composés de recherche apparentés',
        'related_intro': 'Si vous recherchez {name}, les composés que vous voudrez probablement examiner ensuite sont',
        'related_outro': 'Ceux-ci apparaissent le plus souvent dans les mêmes contextes de recherche comme alternatives ou composés complémentaires.',
    },
    'de': {
        'q_what': 'Was ist {name}?',
        'q_mech': 'Wie wirkt {name}?',
        'q_dose': 'Was sind typische Forschungsdosen für {name}?',
        'q_safety': 'Was sind die wichtigsten Sicherheitsüberlegungen?',
        'q_fda': 'Ist {name} von der FDA zugelassen?',
        'a_fda': 'Der FDA-Regulierungsstatus hängt von der spezifischen Verbindung ab. Die meisten Forschungspeptide sind nicht von der FDA für den menschlichen Gebrauch zugelassen und werden als Forschungschemikalien nur für den Laborgebrauch verkauft.',
        'related_h2': 'Verwandte Forschungsverbindungen',
        'related_intro': 'Wenn Sie {name} erforschen, sind die Verbindungen, die Sie als Nächstes betrachten möchten',
        'related_outro': 'Diese erscheinen am häufigsten in denselben Forschungskontexten als Alternativen oder ergänzende Verbindungen.',
    },
    'it': {
        'q_what': 'Cos\'è {name}?',
        'q_mech': 'Come funziona {name}?',
        'q_dose': 'Quali sono le dosi di ricerca tipiche per {name}?',
        'q_safety': 'Quali sono le principali considerazioni di sicurezza?',
        'q_fda': '{name} è approvato dalla FDA?',
        'a_fda': 'Lo stato normativo FDA dipende dal composto specifico. La maggior parte dei peptidi di ricerca non è approvata dalla FDA per uso umano ed è venduta come sostanze chimiche di ricerca solo per uso di laboratorio.',
        'related_h2': 'Composti di ricerca correlati',
        'related_intro': 'Se stai ricercando {name}, i composti che probabilmente vorrai esaminare successivamente sono',
        'related_outro': 'Questi appaiono più spesso negli stessi contesti di ricerca come alternative o composti complementari.',
    },
    'ru': {
        'q_what': 'Что такое {name}?',
        'q_mech': 'Как работает {name}?',
        'q_dose': 'Каковы типичные исследовательские дозы для {name}?',
        'q_safety': 'Каковы основные соображения безопасности?',
        'q_fda': 'Одобрен ли {name} FDA?',
        'a_fda': 'Регулирующий статус FDA зависит от конкретного соединения. Большинство исследовательских пептидов не одобрены FDA для использования человеком и продаются как исследовательские химикаты только для лабораторного использования.',
        'related_h2': 'Связанные исследовательские соединения',
        'related_intro': 'Если вы исследуете {name}, соединения, которые вы, вероятно, захотите рассмотреть далее, это',
        'related_outro': 'Они чаще всего появляются в тех же исследовательских контекстах как альтернативы или дополнительные соединения.',
    },
    'pl': {
        'q_what': 'Czym jest {name}?',
        'q_mech': 'Jak działa {name}?',
        'q_dose': 'Jakie są typowe dawki badawcze dla {name}?',
        'q_safety': 'Jakie są główne kwestie bezpieczeństwa?',
        'q_fda': 'Czy {name} jest zatwierdzony przez FDA?',
        'a_fda': 'Status regulacyjny FDA zależy od konkretnego związku. Większość peptydów badawczych nie jest zatwierdzona przez FDA do użytku ludzkiego i jest sprzedawana jako chemikalia badawcze wyłącznie do użytku laboratoryjnego.',
        'related_h2': 'Powiązane związki badawcze',
        'related_intro': 'Jeśli badasz {name}, związki, które prawdopodobnie zechcesz zobaczyć następne to',
        'related_outro': 'Pojawiają się one najczęściej w tych samych kontekstach badawczych jako alternatywy lub związki uzupełniające.',
    },
    'nl': {
        'q_what': 'Wat is {name}?',
        'q_mech': 'Hoe werkt {name}?',
        'q_dose': 'Wat zijn typische onderzoeksdoseringen voor {name}?',
        'q_safety': 'Wat zijn de belangrijkste veiligheidsoverwegingen?',
        'q_fda': 'Is {name} goedgekeurd door de FDA?',
        'a_fda': 'De FDA-regelgevingsstatus hangt af van de specifieke verbinding. De meeste onderzoekspeptiden zijn niet goedgekeurd door de FDA voor menselijk gebruik en worden verkocht als onderzoekschemicaliën alleen voor laboratoriumgebruik.',
        'related_h2': 'Gerelateerde onderzoeksverbindingen',
        'related_intro': 'Als u {name} onderzoekt, zijn de verbindingen die u waarschijnlijk vervolgens wilt bekijken',
        'related_outro': 'Deze verschijnen het vaakst in dezelfde onderzoekscontexten als alternatieven of aanvullende verbindingen.',
    },
    'id': {
        'q_what': 'Apa itu {name}?',
        'q_mech': 'Bagaimana cara kerja {name}?',
        'q_dose': 'Apa dosis penelitian tipikal untuk {name}?',
        'q_safety': 'Apa pertimbangan keamanan utama?',
        'q_fda': 'Apakah {name} disetujui oleh FDA?',
        'a_fda': 'Status regulasi FDA tergantung pada senyawa spesifik. Sebagian besar peptida penelitian tidak disetujui oleh FDA untuk penggunaan manusia dan dijual sebagai bahan kimia penelitian hanya untuk penggunaan laboratorium.',
        'related_h2': 'Senyawa penelitian terkait',
        'related_intro': 'Jika Anda meneliti {name}, senyawa yang mungkin ingin Anda lihat selanjutnya adalah',
        'related_outro': 'Ini paling sering muncul dalam konteks penelitian yang sama sebagai alternatif atau senyawa pelengkap.',
    },
}

# Compound display names per language (just the most-trafficked compounds for now)
COMPOUND_NAMES = {
    'bpc-157': {
        'es': 'BPC-157', 'pt': 'BPC-157', 'fr': 'BPC-157', 'de': 'BPC-157',
        'it': 'BPC-157', 'ru': 'BPC-157', 'pl': 'BPC-157', 'nl': 'BPC-157', 'id': 'BPC-157',
    },
    'tb-500': {
        'es': 'TB-500', 'pt': 'TB-500', 'fr': 'TB-500', 'de': 'TB-500',
        'it': 'TB-500', 'ru': 'TB-500', 'pl': 'TB-500', 'nl': 'TB-500', 'id': 'TB-500',
    },
    'semaglutide': {
        'es': 'Semaglutida', 'pt': 'Semaglutida', 'fr': 'Sémaglutide', 'de': 'Semaglutid',
        'it': 'Semaglutide', 'ru': 'Семаглутид', 'pl': 'Semaglutyd', 'nl': 'Semaglutide', 'id': 'Semaglutide',
    },
    'tirzepatide': {
        'es': 'Tirzepatida', 'pt': 'Tirzepatida', 'fr': 'Tirzépatide', 'de': 'Tirzepatid',
        'it': 'Tirzepatide', 'ru': 'Тирзепатид', 'pl': 'Tirzepatyd', 'nl': 'Tirzepatide', 'id': 'Tirzepatide',
    },
    'ipamorelin': {
        'es': 'Ipamorelina', 'pt': 'Ipamorelina', 'fr': 'Ipamoréline', 'de': 'Ipamorelin',
        'it': 'Ipamorelina', 'ru': 'Ипаморелин', 'pl': 'Ipamorelina', 'nl': 'Ipamoreline', 'id': 'Ipamorelin',
    },
    'cjc-1295': {l: 'CJC-1295' for l in LANGUAGES},
    'mk-677': {l: 'MK-677' for l in LANGUAGES},
    'noopept': {l: 'Noopept' for l in LANGUAGES},
    'mots-c': {l: 'MOTS-c' for l in LANGUAGES},
    'epithalon': {l: 'Epitalón' if False else 'Epithalon' for l in LANGUAGES},
    'ghk-cu': {l: 'GHK-Cu' for l in LANGUAGES},
    'thymosin-alpha-1': {
        'es': 'Timosina Alfa-1', 'pt': 'Timosina Alfa-1', 'fr': 'Thymosine Alpha-1',
        'de': 'Thymosin Alpha-1', 'it': 'Timosina Alfa-1', 'ru': 'Тимозин Альфа-1',
        'pl': 'Tymozyna Alfa-1', 'nl': 'Thymosine Alpha-1', 'id': 'Thymosin Alpha-1',
    },
    'pt-141': {l: 'PT-141 (Bremelanotide)' for l in LANGUAGES},
    'tesamorelin': {l: 'Tesamorelin' for l in LANGUAGES},
    'sermorelin': {l: 'Sermorelin' for l in LANGUAGES},
    'igf-1-lr3': {l: 'IGF-1 LR3' for l in LANGUAGES},
}

RELATED_MAP = {
    'bpc-157': ['tb-500', 'ghk-cu'],
    'tb-500': ['bpc-157', 'ghk-cu'],
    'semaglutide': ['tirzepatide', 'retatrutide'],
    'tirzepatide': ['semaglutide', 'retatrutide'],
    'retatrutide': ['tirzepatide', 'semaglutide'],
    'ipamorelin': ['cjc-1295', 'sermorelin'],
    'cjc-1295': ['ipamorelin', 'sermorelin', 'tesamorelin'],
    'sermorelin': ['ipamorelin', 'tesamorelin'],
    'mk-677': ['ipamorelin', 'cjc-1295'],
    'tesamorelin': ['sermorelin', 'cjc-1295'],
    'ghk-cu': ['bpc-157', 'tb-500'],
    'mots-c': ['epithalon', 'humanin'],
    'epithalon': ['mots-c', 'foxo4-dri'],
    'noopept': ['cerebrolysin', 'semax'],
    'cerebrolysin': ['noopept', 'semax'],
    'pt-141': ['melanotan-i', 'melanotan-ii'],
    'thymosin-alpha-1': ['ll-37'],
}


def parse_compound_from_slug(slug):
    """Extract compound key from slug. Try longest-match first."""
    s = slug.replace('.html', '')
    compound_keys = sorted(COMPOUND_NAMES.keys(), key=len, reverse=True)
    for ck in compound_keys:
        if s == ck or s == ck + '-guide':
            return ck
        if s.startswith(ck + '-'):
            return ck
    return None


def extract_quick_answer(html):
    """Pull existing quick-answer text from the page if present."""
    m = re.search(r'<div class="quick-answer"[^>]*>(.*?)</div>', html, re.DOTALL)
    if m:
        text = re.sub(r'<[^>]+>', ' ', m.group(1))
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:400] if len(text) > 50 else None
    # Try meta description as fallback
    m = re.search(r'<meta\s+content="([^"]*)"\s+name="description"', html)
    if not m:
        m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
    if m:
        return m.group(1)[:400]
    return None


def extract_h2_paragraphs(html):
    """Extract H2 + first paragraph pairs from the article body."""
    m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if not m:
        m = re.search(r'<div\s+class="content"[^>]*>(.*?)</div>\s*<footer', html, re.DOTALL)
    if not m:
        return []
    body = m.group(1)
    # Find H2 sections with their following paragraph
    pattern = re.compile(r'<h2[^>]*>(.*?)</h2>\s*<p[^>]*>(.*?)</p>', re.DOTALL)
    pairs = []
    for h_match in pattern.finditer(body):
        h2 = re.sub(r'<[^>]+>', ' ', h_match.group(1)).strip()
        p_text = re.sub(r'<[^>]+>', ' ', h_match.group(2))
        p_text = re.sub(r'\s+', ' ', p_text).strip()
        if h2 and p_text and len(p_text) > 50:
            pairs.append((h2, p_text[:400]))
    return pairs


def build_faq_from_existing(html, lang, compound_key, slug):
    """Build a FAQ schema using existing page content + lang-specific Q text."""
    strings = LANG_STRINGS[lang]
    cnames = COMPOUND_NAMES.get(compound_key, {})
    name = cnames.get(lang, slug.replace('-', ' ').title())

    qa_text = extract_quick_answer(html) or f'{name} information.'
    h2_pairs = extract_h2_paragraphs(html)

    # Build 5 Q&As: prefer using extracted H2 content as answers
    qa_pairs = []

    # Q1: What is X? — use overview/quick-answer
    q1 = strings['q_what'].format(name=name)
    a1 = qa_text
    qa_pairs.append((q1, a1))

    # Q2-4: From extracted H2/p pairs (prefer ones discussing mechanism, dosage, safety)
    used_indices = set()
    keyword_priorities = [
        ('mech', strings['q_mech'].format(name=name),
         ['mechanism', 'mecanismo', 'mécanisme', 'mechanismus', 'meccanismo', 'механизм',
          'mechanizm', 'werking', 'mekanisme', 'how', 'cómo', 'come', 'comment', 'wie',
          'как', 'jak', 'hoe', 'bagaimana']),
        ('dose', strings['q_dose'].format(name=name),
         ['dose', 'dosage', 'dosering', 'dosaggio', 'dosaje', 'dosering', 'дозиров', 'dawk']),
        ('safety', strings['q_safety'].format(name=name),
         ['safety', 'seguridad', 'sicurezza', 'sicherheit', 'sécurité', 'segurança',
          'безопасн', 'bezpiecz', 'veiligheid', 'keamanan', 'side effect', 'efeito',
          'efecto', 'effetto', 'effet', 'wirkung', 'побочн', 'skutek', 'bijwerking']),
    ]
    for tag, q_text, keywords in keyword_priorities:
        for i, (h2, p_text) in enumerate(h2_pairs):
            if i in used_indices:
                continue
            h2_lower = h2.lower()
            if any(k.lower() in h2_lower for k in keywords):
                qa_pairs.append((q_text, p_text))
                used_indices.add(i)
                break

    # Q5: FDA question with lang-specific answer
    q5 = strings['q_fda'].format(name=name)
    a5 = strings['a_fda']
    qa_pairs.append((q5, a5))

    # Pad to at least 4 if we still don't have enough
    while len(qa_pairs) < 4 and len(used_indices) < len(h2_pairs):
        for i, (h2, p_text) in enumerate(h2_pairs):
            if i not in used_indices:
                qa_pairs.append((h2, p_text))
                used_indices.add(i)
                if len(qa_pairs) >= 5:
                    break
        if not h2_pairs:
            break

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa_pairs[:6]
        ]
    }


def inject_cross_links(html, lang, compound_key):
    """Inject related-compounds H2 + links section if not already present."""
    if compound_key not in RELATED_MAP:
        return html, False
    related = RELATED_MAP[compound_key]
    if not related:
        return html, False

    strings = LANG_STRINGS[lang]
    cnames = COMPOUND_NAMES.get(compound_key, {})
    name = cnames.get(lang, compound_key.upper())

    # Check if cross-links already exist
    if strings['related_h2'] in html or 'href="/' + lang + '/' + related[0] in html:
        return html, False

    # Build cross-links HTML
    link_parts = []
    for rk in related[:4]:
        rname = COMPOUND_NAMES.get(rk, {}).get(lang, rk.replace('-', ' ').upper())
        link_parts.append(f'<a href="/{lang}/{rk}-guide.html">{rname}</a>')
    if not link_parts:
        return html, False

    cross_html = (
        f'\n<h2>{strings["related_h2"]}</h2>\n'
        f'<p>{strings["related_intro"].format(name=name)}: '
        f'{", ".join(link_parts)}. '
        f'{strings["related_outro"]}</p>\n'
    )

    # Insert before </article> or </div></footer>
    if '</article>' in html:
        html = html.replace('</article>', cross_html + '</article>', 1)
        return html, True
    elif re.search(r'</div>\s*<footer', html):
        html = re.sub(r'(</div>\s*<footer)', cross_html + r'\1', html, count=1)
        return html, True
    return html, False


def process_file(path, lang):
    html = path.read_text(encoding='utf-8', errors='ignore')
    slug = path.stem
    actions = []

    compound_key = parse_compound_from_slug(slug)

    # 1. Inject FAQ schema if missing
    if 'FAQPage' not in html:
        if compound_key:
            faq_schema = build_faq_from_existing(html, lang, compound_key, slug)
            schema_tag = f'<script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>'
            if '</head>' in html:
                html = html.replace('</head>', schema_tag + '\n</head>', 1)
                actions.append('faq-injected')

    # 2. Inject cross-links if compound is known
    if compound_key and compound_key in RELATED_MAP:
        html, cl_added = inject_cross_links(html, lang, compound_key)
        if cl_added:
            actions.append('cross-links')

    if not actions:
        return False, 'no-change'

    path.write_text(html, encoding='utf-8')
    return True, '+'.join(actions)


def main():
    only_lang = os.environ.get('LANG', None)
    langs_to_process = [only_lang] if only_lang else LANGUAGES

    grand_total = {'fixed': 0, 'no-change': 0, 'errors': 0,
                   'faq-injected': 0, 'cross-links': 0,
                   'faq-injected+cross-links': 0}
    for lang in langs_to_process:
        d = ROOT / lang
        if not d.is_dir():
            continue
        files = sorted(d.glob('*.html'))
        lang_counts = {'fixed': 0, 'no-change': 0, 'errors': 0}
        per_action = {}
        for path in files:
            try:
                changed, action = process_file(path, lang)
                if changed:
                    lang_counts['fixed'] += 1
                    per_action[action] = per_action.get(action, 0) + 1
                    grand_total['fixed'] += 1
                    grand_total[action] = grand_total.get(action, 0) + 1
                else:
                    lang_counts['no-change'] += 1
                    grand_total['no-change'] += 1
            except Exception as e:
                lang_counts['errors'] += 1
                grand_total['errors'] += 1
                print(f"ERR {lang}/{path.name}: {e}", file=sys.stderr)
        print(f"{lang}: {lang_counts['fixed']}/{len(files)} fixed (errors: {lang_counts['errors']}). Actions: {per_action}")

    print(f"\n=== Phase 5 grand total ===")
    for k, v in grand_total.items():
        if v > 0:
            print(f"  {k}: {v}")


if __name__ == '__main__':
    main()
