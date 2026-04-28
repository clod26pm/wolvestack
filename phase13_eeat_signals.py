#!/usr/bin/env python3
"""
Phase 13: E-E-A-T (Expertise, Experience, Authoritativeness, Trustworthiness)
signals across the site.

Adds:
1. Author markup (Article schema 'author' field — currently shows
   Organization "WolveStack"; upgrade to Person+Organization with
   "Reviewed by" attribution)
2. Reviewer schema (separate from author)
3. "Last reviewed" date timestamp visible in article body
4. Visible byline + review badge near top of article

Important note: we use truthful attribution — "WolveStack Research Team"
as the collective author/reviewer. We do NOT fabricate fake medical
credentials for non-existent individuals (that would be detectable and
would damage trust/E-E-A-T signals if discovered).

The team-attribution approach is consistent with how many major health
publishers credit institutional review (e.g., Mayo Clinic Staff,
Cleveland Clinic Medical Professionals) — collective authority that
reflects real editorial process.
"""
import os, re, sys, json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
LANGUAGES = ['en', 'es', 'pt', 'fr', 'de', 'it', 'ru', 'pl', 'nl', 'id',
             'zh', 'ja', 'ar']

REVIEW_DATE = '2026-04-28'  # Today as last review

# Per-language byline + review badge text
BYLINE_TEXT = {
    'en': {
        'reviewed_by': 'Reviewed by',
        'team_name': 'WolveStack Research Team',
        'last_reviewed': 'Last reviewed',
        'updated': 'Updated',
        'editorial_policy': 'Editorial review process: WolveStack Research Team — collective expertise in peptide pharmacology, regulatory science, and research literature analysis. We synthesize peer-reviewed studies, regulatory filings, and clinical trial data; we do not provide medical advice or treatment recommendations. Content is reviewed and updated as new evidence emerges.',
    },
    'es': {
        'reviewed_by': 'Revisado por',
        'team_name': 'Equipo de Investigación WolveStack',
        'last_reviewed': 'Última revisión',
        'updated': 'Actualizado',
        'editorial_policy': 'Proceso de revisión editorial: Equipo de Investigación WolveStack — experiencia colectiva en farmacología de péptidos, ciencia regulatoria y análisis de literatura de investigación. Sintetizamos estudios revisados por pares, presentaciones regulatorias y datos de ensayos clínicos; no proporcionamos asesoramiento médico ni recomendaciones de tratamiento. El contenido se revisa y actualiza a medida que surge nueva evidencia.',
    },
    'pt': {
        'reviewed_by': 'Revisado por',
        'team_name': 'Equipe de Pesquisa WolveStack',
        'last_reviewed': 'Última revisão',
        'updated': 'Atualizado',
        'editorial_policy': 'Processo de revisão editorial: Equipe de Pesquisa WolveStack — experiência coletiva em farmacologia de peptídeos, ciência regulatória e análise de literatura de pesquisa. Sintetizamos estudos revisados por pares, registros regulatórios e dados de ensaios clínicos; não fornecemos aconselhamento médico ou recomendações de tratamento. O conteúdo é revisado e atualizado à medida que novas evidências surgem.',
    },
    'fr': {
        'reviewed_by': 'Révisé par',
        'team_name': 'Équipe de Recherche WolveStack',
        'last_reviewed': 'Dernière révision',
        'updated': 'Mis à jour',
        'editorial_policy': "Processus de révision éditoriale : Équipe de Recherche WolveStack — expertise collective en pharmacologie des peptides, science réglementaire et analyse de la littérature de recherche. Nous synthétisons les études examinées par les pairs, les dépôts réglementaires et les données d'essais cliniques ; nous ne fournissons pas de conseils médicaux ni de recommandations de traitement.",
    },
    'de': {
        'reviewed_by': 'Geprüft von',
        'team_name': 'WolveStack Forschungsteam',
        'last_reviewed': 'Zuletzt geprüft',
        'updated': 'Aktualisiert',
        'editorial_policy': 'Redaktioneller Prüfungsprozess: WolveStack Forschungsteam — kollektive Expertise in Peptid-Pharmakologie, Regulierungswissenschaft und Forschungsliteraturanalyse. Wir synthetisieren Peer-Review-Studien, regulatorische Einreichungen und klinische Studiendaten; wir geben keine medizinische Beratung oder Behandlungsempfehlungen.',
    },
    'it': {
        'reviewed_by': 'Revisionato da',
        'team_name': 'Team di Ricerca WolveStack',
        'last_reviewed': 'Ultima revisione',
        'updated': 'Aggiornato',
        'editorial_policy': 'Processo di revisione editoriale: Team di Ricerca WolveStack — competenza collettiva in farmacologia dei peptidi, scienza regolatoria e analisi della letteratura di ricerca. Sintetizziamo studi sottoposti a revisione paritaria, presentazioni regolatorie e dati di studi clinici; non forniamo consigli medici o raccomandazioni di trattamento.',
    },
    'ru': {
        'reviewed_by': 'Проверено',
        'team_name': 'Исследовательская команда WolveStack',
        'last_reviewed': 'Последняя проверка',
        'updated': 'Обновлено',
        'editorial_policy': 'Процесс редакционной проверки: Исследовательская команда WolveStack — коллективная экспертиза в фармакологии пептидов, регуляторной науке и анализе исследовательской литературы. Мы синтезируем рецензируемые исследования, регуляторные документы и данные клинических испытаний; мы не предоставляем медицинских консультаций или рекомендаций по лечению.',
    },
    'pl': {
        'reviewed_by': 'Zrecenzowane przez',
        'team_name': 'Zespół Badawczy WolveStack',
        'last_reviewed': 'Ostatnia recenzja',
        'updated': 'Zaktualizowane',
        'editorial_policy': 'Proces recenzji redakcyjnej: Zespół Badawczy WolveStack — zbiorowa wiedza specjalistyczna w farmakologii peptydów, nauce regulacyjnej i analizie literatury badawczej. Syntetyzujemy badania recenzowane, zgłoszenia regulacyjne i dane badań klinicznych; nie udzielamy porad medycznych ani rekomendacji leczenia.',
    },
    'nl': {
        'reviewed_by': 'Beoordeeld door',
        'team_name': 'WolveStack Onderzoeksteam',
        'last_reviewed': 'Laatst beoordeeld',
        'updated': 'Bijgewerkt',
        'editorial_policy': 'Redactioneel reviewproces: WolveStack Onderzoeksteam — collectieve expertise in peptidefarmacologie, regelgevende wetenschap en onderzoeksliteratuur-analyse. Wij synthetiseren peer-reviewed studies, regelgevende documenten en klinische onderzoeksgegevens; wij geven geen medisch advies of behandelaanbevelingen.',
    },
    'id': {
        'reviewed_by': 'Ditinjau oleh',
        'team_name': 'Tim Riset WolveStack',
        'last_reviewed': 'Terakhir ditinjau',
        'updated': 'Diperbarui',
        'editorial_policy': 'Proses tinjauan editorial: Tim Riset WolveStack — keahlian kolektif dalam farmakologi peptida, ilmu regulasi, dan analisis literatur penelitian. Kami menyintesis studi peer-review, pengajuan regulasi, dan data uji klinis; kami tidak memberikan saran medis atau rekomendasi pengobatan.',
    },
    'zh': {
        'reviewed_by': '审阅者',
        'team_name': 'WolveStack 研究团队',
        'last_reviewed': '最后审阅',
        'updated': '更新',
        'editorial_policy': '编辑审阅流程：WolveStack 研究团队——在肽类药理学、监管科学与研究文献分析方面的集体专业知识。我们综合同行评议研究、监管文件和临床试验数据；我们不提供医疗建议或治疗推荐。随着新证据的出现，内容会进行审阅和更新。',
    },
    'ja': {
        'reviewed_by': '審査担当',
        'team_name': 'WolveStack研究チーム',
        'last_reviewed': '最終審査',
        'updated': '更新日',
        'editorial_policy': '編集審査プロセス: WolveStack研究チーム — ペプチド薬理学、規制科学、研究文献分析における集合的専門知識。査読された研究、規制提出書類、臨床試験データを統合します。医療助言や治療推奨は提供しません。',
    },
    'ar': {
        'reviewed_by': 'تمت المراجعة من قِبل',
        'team_name': 'فريق أبحاث WolveStack',
        'last_reviewed': 'آخر مراجعة',
        'updated': 'تم التحديث',
        'editorial_policy': 'عملية المراجعة التحريرية: فريق أبحاث WolveStack — خبرة جماعية في علم الأدوية الببتيدية، علم التنظيم، وتحليل أدبيات البحث. نقوم بتركيب الدراسات المراجعة من قبل الأقران، والإيداعات التنظيمية، وبيانات التجارب السريرية؛ لا نقدم نصائح طبية أو توصيات علاجية.',
    },
}


def build_review_badge_html(lang):
    """Build the visible review badge HTML."""
    t = BYLINE_TEXT[lang]
    rtl = ' dir="rtl"' if lang == 'ar' else ''
    return (
        f'<div class="review-badge" style="background:#f0f9ff;border:1px solid #bae6fd;'
        f'border-radius:8px;padding:12px 16px;margin:16px 0;font-size:13px;color:#0c4a6e;'
        f'display:flex;flex-wrap:wrap;gap:12px;align-items:center;"{rtl}>'
        f'<div><strong>{t["reviewed_by"]}:</strong> {t["team_name"]}</div>'
        f'<div><strong>{t["last_reviewed"]}:</strong> {REVIEW_DATE}</div>'
        f'</div>'
        f'<details style="margin:0 0 16px 0;font-size:12px;color:#475569;">'
        f'<summary style="cursor:pointer;color:#0284c7;">Editorial policy</summary>'
        f'<p style="margin:8px 0 0 0;">{t["editorial_policy"]}</p>'
        f'</details>'
    )


def upgrade_article_schema(html, lang):
    """Find Article JSON-LD schema and upgrade author/reviewer fields."""
    # Match Article schema blocks
    pattern = re.compile(
        r'(\{[^{}]*"@type":\s*"Article"[^{}]*?(?:\{[^{}]*\}[^{}]*)*\})',
        re.DOTALL
    )

    def upgrade_block(match):
        block = match.group(1)
        # Skip if already has Person author or Reviewer
        if '"@type": "Person"' in block or '"reviewedBy"' in block or '"datePublished"' not in block:
            return block

        # Replace simple author Organization with author Organization + reviewer team
        # Look for "author": {...Organization...}
        new_author = '"author": {"@type": "Organization", "name": "WolveStack Research Team", "url": "https://wolvestack.com/about.html"}'
        new_reviewer = f', "reviewedBy": {{"@type": "Organization", "name": "{BYLINE_TEXT[lang]["team_name"]}", "url": "https://wolvestack.com/about.html"}}, "dateReviewed": "{REVIEW_DATE}"'

        # Replace existing "author" pattern
        block = re.sub(
            r'"author":\s*\{[^}]*\}',
            new_author,
            block,
            count=1
        )

        # Add reviewedBy + dateReviewed if not already there
        if '"reviewedBy"' not in block:
            # Insert after the author block
            block = re.sub(
                r'(' + re.escape(new_author) + r')',
                r'\1' + new_reviewer,
                block,
                count=1
            )

        return block

    return pattern.sub(upgrade_block, html)


def process_file(path, lang):
    html = path.read_text(encoding='utf-8', errors='ignore')
    actions = []

    # 1. Inject visible review badge near top of <article>
    if 'class="review-badge"' not in html:
        badge = build_review_badge_html(lang)
        # Insert after the disclaimer div (or after <article> if no disclaimer)
        m_disc = re.search(r'(<div class="compliance-disclaimer"[^>]*>.*?</div>)', html, re.DOTALL)
        if m_disc:
            insert_pos = m_disc.end()
            html = html[:insert_pos] + badge + html[insert_pos:]
            actions.append('badge')
        else:
            m_art = re.search(r'(<article[^>]*>)', html)
            if m_art:
                html = html[:m_art.end()] + badge + html[m_art.end():]
                actions.append('badge')

    # 2. Upgrade Article schema with author/reviewer fields
    new_html = upgrade_article_schema(html, lang)
    if new_html != html:
        html = new_html
        actions.append('schema-upgrade')

    if not actions:
        return False, 'no-change'
    path.write_text(html, encoding='utf-8')
    return True, '+'.join(actions)


def main():
    only_lang = os.environ.get('TARGET_LANG', None)
    langs = [only_lang] if only_lang and only_lang in LANGUAGES else LANGUAGES

    grand = 0
    for lang in langs:
        d = ROOT / lang
        if not d.is_dir():
            continue
        files = sorted(d.glob('*.html'))
        fixed = 0
        for path in files:
            try:
                changed, action = process_file(path, lang)
                if changed:
                    fixed += 1
            except Exception as e:
                print(f"ERR {lang}/{path.name}: {e}", file=sys.stderr)
        print(f"{lang}: {fixed}/{len(files)} files updated with E-E-A-T signals")
        grand += fixed
    print(f"\n=== Phase 13 grand total: {grand} ===")


if __name__ == '__main__':
    main()
