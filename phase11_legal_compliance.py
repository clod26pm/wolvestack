#!/usr/bin/env python3
"""
Phase 11: Multi-jurisdiction legal/compliance disclaimers.

Replaces lightweight disclaimer blocks with comprehensive compliance text
covering: US FDA, EU MDR, UK ASA, AU TGA, CA Health Canada, WADA athletic
doping, FTC 2023 affiliate disclosure rules, medical advice, and the
"research chemicals only" status.

Per-language disclaimer text for all 13 languages (en, es, pt, fr, de, it,
ru, pl, nl, id, zh, ja, ar). WADA-banned compounds get an additional
warning section.

Operates by replacing the existing pink disclaimer div (which appears on
nearly every cornerstone page) with the v2 compliance block, while leaving
article body content untouched.
"""
import os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LANGUAGES = ['en', 'es', 'pt', 'fr', 'de', 'it', 'ru', 'pl', 'nl', 'id',
             'zh', 'ja', 'ar']

# WADA Section 2 (Peptide Hormones, Growth Factors, Related Substances)
# These compounds should trigger an extra athletic compliance warning.
WADA_BANNED = {
    'tb-500', 'igf-1-lr3', 'mk-677', 'cjc-1295', 'ipamorelin',
    'sermorelin', 'tesamorelin', 'ghrp-2', 'ghrp-6', 'hexarelin',
    'semaglutide', 'tirzepatide', 'retatrutide',  # GLP-1 class
    'liraglutide', 'setmelanotide',
    # Note: BPC-157 is NOT currently on WADA list (as of 2026)
}

# Comprehensive disclaimer per language
# Covers: FDA + EU MDR + UK ASA + AU TGA + CA + WADA reference + Medical + Affiliate
DISCLAIMERS = {
    'en': {
        'title': 'Compliance & Medical Disclaimer',
        'body': 'This article is for informational and educational purposes only and does not constitute medical, legal, regulatory, or professional advice. The compounds discussed are research chemicals not approved for human consumption by the US FDA, European Medicines Agency (EMA), UK MHRA, Australian TGA, Health Canada, or any other major regulatory authority. They are sold strictly for laboratory research use. WolveStack does not employ medical staff, does not diagnose, treat, or prescribe, and makes no health claims under FTC, UK ASA, EU MDR/UCPD, or AU TGA standards. Always consult a licensed healthcare professional in your jurisdiction before considering any peptide protocol. This site contains affiliate links (FTC 2023 endorsement guidelines compliant); we may earn a commission on qualifying purchases at no additional cost to you. Some compounds discussed are on the WADA prohibited list — competitive athletes should verify current status with their governing body before any research use. Use of research chemicals may be illegal in your jurisdiction.',
        'wada_extra': 'IMPORTANT: This compound is currently on the World Anti-Doping Agency (WADA) prohibited list. Competitive athletes face sanctions for use including in retirement testing programs. Verify current WADA status with your sport\'s governing body before any research involvement.',
    },
    'es': {
        'title': 'Aviso de cumplimiento y descargo médico',
        'body': 'Este artículo es solo para fines informativos y educativos y no constituye asesoramiento médico, legal, regulatorio ni profesional. Los compuestos discutidos son productos químicos de investigación no aprobados para consumo humano por la FDA de EE. UU., la Agencia Europea de Medicamentos (EMA), la MHRA del Reino Unido, la TGA australiana, Health Canada, ni ninguna otra autoridad regulatoria importante. Se venden estrictamente para uso de investigación de laboratorio. WolveStack no emplea personal médico, no diagnostica, trata ni prescribe, y no hace afirmaciones de salud bajo los estándares de la FTC, la ASA del Reino Unido, el MDR/UCPD de la UE, ni la TGA de Australia. Consulte siempre a un profesional sanitario autorizado en su jurisdicción antes de considerar cualquier protocolo de péptidos. Este sitio contiene enlaces de afiliados (cumplimiento de las directrices de respaldo de la FTC de 2023); podemos ganar una comisión por compras calificadas sin costo adicional para usted. Algunos compuestos discutidos están en la lista de prohibidos de la AMA (WADA) — los atletas competitivos deben verificar el estado actual con su organismo rector antes de cualquier uso de investigación. El uso de productos químicos de investigación puede ser ilegal en su jurisdicción.',
        'wada_extra': 'IMPORTANTE: Este compuesto está actualmente en la lista de prohibidos de la Agencia Mundial Antidopaje (AMA/WADA). Los atletas competitivos enfrentan sanciones por su uso, incluyendo programas de pruebas en el retiro. Verifique el estado actual de la AMA con el organismo rector de su deporte antes de cualquier participación en investigación.',
    },
    'pt': {
        'title': 'Aviso de Conformidade e Renúncia Médica',
        'body': 'Este artigo é apenas para fins informativos e educacionais e não constitui aconselhamento médico, legal, regulatório ou profissional. Os compostos discutidos são produtos químicos de pesquisa não aprovados para consumo humano pela FDA dos EUA, Agência Europeia de Medicamentos (EMA), MHRA do Reino Unido, TGA da Austrália, Health Canada, nem qualquer outra autoridade reguladora importante. São vendidos estritamente para uso em pesquisa laboratorial. A WolveStack não emprega pessoal médico, não diagnostica, trata ou prescreve, e não faz alegações de saúde sob os padrões da FTC, ASA do Reino Unido, MDR/UCPD da UE, ou TGA da Austrália. Consulte sempre um profissional de saúde licenciado em sua jurisdição antes de considerar qualquer protocolo de peptídeos. Este site contém links de afiliados (em conformidade com as diretrizes de endosso da FTC de 2023); podemos ganhar comissão por compras qualificadas sem custo adicional para você. Alguns compostos discutidos estão na lista de proibidos da AMA (WADA) — atletas competitivos devem verificar o status atual com seu órgão regulador antes de qualquer uso de pesquisa. O uso de produtos químicos de pesquisa pode ser ilegal em sua jurisdição.',
        'wada_extra': 'IMPORTANTE: Este composto está atualmente na lista de proibidos da Agência Mundial Antidoping (WADA). Atletas competitivos enfrentam sanções por uso, incluindo programas de testes de aposentadoria. Verifique o status atual da WADA com o órgão regulador do seu esporte antes de qualquer envolvimento em pesquisa.',
    },
    'fr': {
        'title': 'Avertissement de conformité et clause médicale',
        'body': 'Cet article est uniquement à des fins d\'information et d\'éducation et ne constitue pas un avis médical, légal, réglementaire ou professionnel. Les composés discutés sont des produits chimiques de recherche non approuvés pour la consommation humaine par la FDA américaine, l\'Agence européenne des médicaments (EMA), la MHRA britannique, la TGA australienne, Santé Canada, ou toute autre autorité réglementaire majeure. Ils sont vendus strictement pour usage en recherche de laboratoire. WolveStack n\'emploie pas de personnel médical, ne diagnostique pas, ne traite pas et ne prescrit pas, et ne fait aucune allégation de santé selon les normes de la FTC, l\'ASA britannique, le MDR/UCPD de l\'UE, ou la TGA d\'Australie. Consultez toujours un professionnel de santé agréé dans votre juridiction avant d\'envisager tout protocole de peptides. Ce site contient des liens affiliés (conformes aux directives d\'endossement FTC 2023) ; nous pouvons percevoir une commission sur les achats qualifiants sans coût supplémentaire pour vous. Certains composés discutés figurent sur la liste des interdits de l\'AMA (WADA) — les athlètes en compétition doivent vérifier le statut actuel auprès de leur instance dirigeante avant tout usage de recherche. L\'utilisation de produits chimiques de recherche peut être illégale dans votre juridiction.',
        'wada_extra': 'IMPORTANT: Ce composé figure actuellement sur la liste des interdits de l\'Agence Mondiale Antidopage (AMA/WADA). Les athlètes en compétition encourent des sanctions, y compris dans les programmes de tests à la retraite. Vérifiez le statut WADA actuel auprès de l\'instance dirigeante de votre sport avant toute implication en recherche.',
    },
    'de': {
        'title': 'Compliance- und medizinischer Haftungsausschluss',
        'body': 'Dieser Artikel dient ausschließlich Informations- und Bildungszwecken und stellt keine medizinische, rechtliche, regulatorische oder professionelle Beratung dar. Die besprochenen Verbindungen sind Forschungschemikalien, die weder von der US-amerikanischen FDA, der Europäischen Arzneimittel-Agentur (EMA), der britischen MHRA, der australischen TGA, Health Canada noch einer anderen großen Regulierungsbehörde für den menschlichen Verzehr zugelassen sind. Sie werden ausschließlich für den Laborforschungseinsatz verkauft. WolveStack beschäftigt kein medizinisches Personal, diagnostiziert, behandelt und verschreibt nicht und macht keine Gesundheitsangaben gemäß den Standards der FTC, der britischen ASA, der EU-MDR/UCPD oder der australischen TGA. Konsultieren Sie immer einen lizenzierten Arzt in Ihrem Land, bevor Sie ein Peptidprotokoll in Betracht ziehen. Diese Website enthält Affiliate-Links (FTC 2023-konform); wir erhalten möglicherweise eine Provision für qualifizierte Käufe ohne zusätzliche Kosten für Sie. Einige besprochene Verbindungen stehen auf der Verbotsliste der WADA — Wettkampfsportler sollten den aktuellen Status mit ihrem Verband überprüfen. Die Verwendung von Forschungschemikalien kann in Ihrem Land illegal sein.',
        'wada_extra': 'WICHTIG: Diese Verbindung steht derzeit auf der Verbotsliste der Welt-Anti-Doping-Agentur (WADA). Wettkampfsportler riskieren Sanktionen, einschließlich Tests im Ruhestand. Überprüfen Sie den aktuellen WADA-Status mit dem Verband Ihrer Sportart, bevor Sie sich an Forschungen beteiligen.',
    },
    'it': {
        'title': 'Avviso di conformità e disclaimer medico',
        'body': 'Questo articolo è solo a scopo informativo ed educativo e non costituisce consulenza medica, legale, regolatoria o professionale. I composti discussi sono sostanze chimiche di ricerca non approvate per il consumo umano dalla FDA statunitense, dall\'Agenzia europea per i medicinali (EMA), dalla MHRA del Regno Unito, dalla TGA australiana, da Health Canada, o da qualsiasi altra autorità regolatoria importante. Sono venduti esclusivamente per uso di ricerca di laboratorio. WolveStack non impiega personale medico, non diagnostica, non tratta o prescrive, e non fa affermazioni sanitarie secondo gli standard FTC, ASA del Regno Unito, MDR/UCPD UE, o TGA australiana. Consultare sempre un professionista sanitario autorizzato nella propria giurisdizione prima di considerare qualsiasi protocollo peptidico. Questo sito contiene link di affiliazione (conformi alle linee guida FTC 2023 sulle approvazioni); potremmo guadagnare una commissione su acquisti qualificanti senza costi aggiuntivi per te. Alcuni composti discussi sono nell\'elenco dei proibiti WADA — gli atleti in competizione devono verificare lo stato attuale con il loro organo direttivo prima di qualsiasi uso di ricerca. L\'uso di sostanze chimiche di ricerca può essere illegale nella tua giurisdizione.',
        'wada_extra': 'IMPORTANTE: Questo composto è attualmente nell\'elenco dei proibiti dell\'Agenzia Mondiale Antidoping (WADA). Gli atleti in competizione affrontano sanzioni per l\'uso, incluso nei programmi di test in pensionamento. Verificare lo stato WADA attuale con l\'organo direttivo del proprio sport prima di qualsiasi coinvolgimento di ricerca.',
    },
    'ru': {
        'title': 'Уведомление о соответствии и медицинский отказ от ответственности',
        'body': 'Данная статья предоставлена исключительно в информационных и образовательных целях и не является медицинским, юридическим, нормативным или профессиональным советом. Обсуждаемые соединения являются исследовательскими химикатами, не одобренными для потребления человеком FDA США, Европейским агентством лекарственных средств (EMA), MHRA Великобритании, TGA Австралии, Health Canada или любым другим крупным регулирующим органом. Они продаются исключительно для использования в лабораторных исследованиях. WolveStack не привлекает медицинский персонал, не диагностирует, не лечит и не назначает препараты, и не делает заявлений о здоровье в соответствии со стандартами FTC, ASA Великобритании, MDR/UCPD ЕС или TGA Австралии. Всегда консультируйтесь с лицензированным медицинским специалистом в вашей юрисдикции перед рассмотрением любого пептидного протокола. Этот сайт содержит партнерские ссылки (соответствуют правилам одобрения FTC 2023 года); мы можем получать комиссию за квалифицированные покупки без дополнительных затрат для вас. Некоторые обсуждаемые соединения находятся в запрещенном списке WADA — спортсменам соревновательного уровня следует проверить текущий статус с их руководящим органом перед любым исследовательским использованием. Использование исследовательских химикатов может быть незаконным в вашей юрисдикции.',
        'wada_extra': 'ВАЖНО: Это соединение в настоящее время находится в запрещенном списке Всемирного антидопингового агентства (WADA). Спортсмены соревновательного уровня сталкиваются с санкциями за использование, включая программы тестирования при выходе на пенсию. Проверьте текущий статус WADA с руководящим органом вашего вида спорта перед любым участием в исследованиях.',
    },
    'pl': {
        'title': 'Zgodność i Zastrzeżenie Medyczne',
        'body': 'Ten artykuł służy wyłącznie celom informacyjnym i edukacyjnym i nie stanowi porady medycznej, prawnej, regulacyjnej ani profesjonalnej. Omawiane związki są chemikaliami badawczymi niezatwierdzonymi do spożycia przez ludzi przez FDA USA, Europejską Agencję Leków (EMA), brytyjską MHRA, australijską TGA, Health Canada ani żaden inny ważny organ regulacyjny. Są sprzedawane wyłącznie do użytku w badaniach laboratoryjnych. WolveStack nie zatrudnia personelu medycznego, nie diagnozuje, nie leczy ani nie przepisuje leków, i nie składa żadnych oświadczeń zdrowotnych zgodnie ze standardami FTC, brytyjskiej ASA, MDR/UCPD UE ani australijskiej TGA. Zawsze konsultuj się z licencjonowanym pracownikiem służby zdrowia w swojej jurysdykcji przed rozważeniem jakiegokolwiek protokołu peptydowego. Ta strona zawiera linki afiliacyjne (zgodne z wytycznymi FTC 2023 dotyczącymi rekomendacji); możemy otrzymywać prowizję od kwalifikujących się zakupów bez dodatkowych kosztów dla Ciebie. Niektóre omawiane związki znajdują się na liście zabronionych WADA — sportowcy startujący w zawodach powinni zweryfikować aktualny status z ich organem zarządzającym przed jakimkolwiek wykorzystaniem badawczym. Używanie chemikaliów badawczych może być nielegalne w Twojej jurysdykcji.',
        'wada_extra': 'WAŻNE: Ten związek znajduje się obecnie na liście zabronionych Światowej Agencji Antydopingowej (WADA). Sportowcy startujący w zawodach narażeni są na sankcje za użycie, w tym w programach testów emerytalnych. Sprawdź aktualny status WADA z organem zarządzającym swoim sportem przed jakimkolwiek zaangażowaniem badawczym.',
    },
    'nl': {
        'title': 'Compliance- en medische disclaimer',
        'body': 'Dit artikel is uitsluitend bedoeld voor informatieve en educatieve doeleinden en vormt geen medisch, juridisch, regulerend of professioneel advies. De besproken verbindingen zijn onderzoekschemicaliën die niet zijn goedgekeurd voor menselijke consumptie door de Amerikaanse FDA, het Europees Geneesmiddelenbureau (EMA), de Britse MHRA, de Australische TGA, Health Canada, of enige andere belangrijke regelgevende instantie. Ze worden uitsluitend verkocht voor gebruik in laboratoriumonderzoek. WolveStack heeft geen medisch personeel in dienst, stelt geen diagnoses, behandelt of schrijft niet voor, en doet geen gezondheidsclaims volgens de normen van FTC, Britse ASA, EU MDR/UCPD, of Australische TGA. Raadpleeg altijd een geregistreerde zorgverlener in uw rechtsgebied voordat u een peptide-protocol overweegt. Deze site bevat affiliate links (FTC 2023 endorsement-richtlijnen conform); we kunnen commissie verdienen op kwalificerende aankopen zonder extra kosten voor u. Sommige besproken verbindingen staan op de WADA verbodslijst — competitieve atleten moeten de huidige status verifiëren bij hun regelgevende instantie voordat ze deelnemen aan onderzoek. Het gebruik van onderzoekschemicaliën kan illegaal zijn in uw rechtsgebied.',
        'wada_extra': 'BELANGRIJK: Deze verbinding staat momenteel op de verbodslijst van het Wereld Anti-Doping Agentschap (WADA). Competitieve atleten lopen sancties op voor gebruik, inclusief in pensioentestprogramma\'s. Verifieer de huidige WADA-status bij het regelgevend orgaan van uw sport voordat u deelneemt aan onderzoek.',
    },
    'id': {
        'title': 'Pernyataan Kepatuhan dan Pengabaian Medis',
        'body': 'Artikel ini hanya untuk tujuan informasi dan edukasi dan bukan merupakan nasihat medis, hukum, peraturan, atau profesional. Senyawa yang dibahas adalah bahan kimia penelitian yang tidak disetujui untuk konsumsi manusia oleh FDA AS, Badan Obat Eropa (EMA), MHRA Inggris, TGA Australia, Health Canada, atau otoritas regulasi besar lainnya. Mereka dijual ketat untuk penggunaan penelitian laboratorium. WolveStack tidak mempekerjakan staf medis, tidak mendiagnosis, mengobati, atau meresepkan, dan tidak membuat klaim kesehatan menurut standar FTC, ASA Inggris, MDR/UCPD UE, atau TGA Australia. Selalu konsultasikan dengan profesional kesehatan berlisensi di yurisdiksi Anda sebelum mempertimbangkan protokol peptida apa pun. Situs ini berisi tautan afiliasi (sesuai dengan pedoman dukungan FTC 2023); kami dapat memperoleh komisi atas pembelian yang memenuhi syarat tanpa biaya tambahan untuk Anda. Beberapa senyawa yang dibahas ada dalam daftar terlarang WADA — atlet kompetitif harus memverifikasi status saat ini dengan badan pengatur mereka sebelum penggunaan penelitian apa pun. Penggunaan bahan kimia penelitian mungkin ilegal di yurisdiksi Anda.',
        'wada_extra': 'PENTING: Senyawa ini saat ini ada dalam daftar terlarang Badan Anti-Doping Dunia (WADA). Atlet kompetitif menghadapi sanksi atas penggunaan, termasuk dalam program pengujian pensiun. Verifikasi status WADA saat ini dengan badan pengatur olahraga Anda sebelum keterlibatan penelitian apa pun.',
    },
    'zh': {
        'title': '合规与医疗免责声明',
        'body': '本文仅供研究信息与教育用途，不构成医疗、法律、监管或专业建议。讨论的化合物是研究化学品，未获美国 FDA、欧洲药品管理局（EMA）、英国 MHRA、澳大利亚 TGA、加拿大卫生部或任何其他主要监管机构批准用于人体消费。它们仅作为实验室研究用途销售。WolveStack 不雇用医疗人员，不进行诊断、治疗或开处方，根据美国 FTC、英国 ASA、欧盟 MDR/UCPD 或澳大利亚 TGA 标准不提出任何健康声明。在考虑任何肽类方案之前，请务必咨询您所在司法管辖区的持照医疗专业人员。本网站包含联盟营销链接（符合 FTC 2023 推荐准则）；我们可能从合格购买中获得佣金，对您不收取额外费用。讨论的部分化合物在世界反兴奋剂机构（WADA）禁用清单上——竞技运动员应在任何研究使用前向其管理机构核实当前状态。在您的司法管辖区，使用研究化学品可能违法。',
        'wada_extra': '重要提示：此化合物目前在世界反兴奋剂机构（WADA）禁用清单上。竞技运动员使用将面临制裁，包括退役测试计划。在参与任何研究前，请向所在运动项目的管理机构核实当前 WADA 状态。',
    },
    'ja': {
        'title': 'コンプライアンス＆医療免責事項',
        'body': '本記事は情報および教育目的のみであり、医療、法律、規制、または専門的助言を構成するものではありません。議論される化合物は研究用化学物質であり、米国FDA、欧州医薬品庁（EMA）、英国MHRA、オーストラリアTGA、ヘルスカナダ、その他の主要な規制当局によって人間の消費を承認されていません。これらは厳密に実験室研究用途でのみ販売されています。WolveStackは医療スタッフを雇用しておらず、診断、治療、処方を行わず、米国FTC、英国ASA、EU MDR/UCPD、またはオーストラリアTGA基準下での健康主張を行いません。ペプチドプロトコルを検討する前に、必ず管轄地域のライセンスを受けた医療専門家にご相談ください。このサイトにはアフィリエイトリンクが含まれており（FTC 2023推奨ガイドライン準拠）、適格な購入から手数料を得る場合があります。追加費用はかかりません。議論される一部の化合物は世界アンチ・ドーピング機関（WADA）禁止リストに掲載されています — 競技アスリートは、研究利用の前に統括組織で現在のステータスを確認する必要があります。研究用化学物質の使用は管轄地域で違法である可能性があります。',
        'wada_extra': '重要：この化合物は現在、世界アンチ・ドーピング機関（WADA）禁止リストに掲載されています。競技アスリートは引退後の検査プログラムを含む使用に対して制裁に直面します。研究関与前にスポーツの統括組織で現在のWADAステータスを確認してください。',
    },
    'ar': {
        'title': 'إخلاء المسؤولية للامتثال والطب',
        'body': 'هذه المقالة لأغراض إعلامية وتعليمية فقط ولا تشكل نصيحة طبية أو قانونية أو تنظيمية أو مهنية. المركبات التي تتم مناقشتها هي مواد كيميائية بحثية غير معتمدة للاستهلاك البشري من قبل إدارة الغذاء والدواء الأمريكية (FDA)، أو الوكالة الأوروبية للأدوية (EMA)، أو هيئة تنظيم الأدوية والرعاية الصحية في المملكة المتحدة (MHRA)، أو إدارة السلع العلاجية الأسترالية (TGA)، أو وزارة الصحة الكندية، أو أي سلطة تنظيمية رئيسية أخرى. يتم بيعها بشكل صارم للاستخدام في الأبحاث المخبرية. لا تستخدم WolveStack موظفين طبيين، ولا تشخص أو تعالج أو تصف الأدوية، ولا تقدم أي ادعاءات صحية وفقًا لمعايير FTC الأمريكية، أو ASA البريطانية، أو MDR/UCPD الأوروبية، أو TGA الأسترالية. استشر دائمًا أخصائي رعاية صحية مرخصًا في ولايتك القضائية قبل النظر في أي بروتوكول للببتيد. يحتوي هذا الموقع على روابط تابعة (متوافقة مع إرشادات FTC 2023 للترويج)؛ قد نكسب عمولة على عمليات الشراء المؤهلة دون أي تكلفة إضافية عليك. بعض المركبات التي تمت مناقشتها موجودة في قائمة الممنوعات الخاصة بالوكالة العالمية لمكافحة المنشطات (WADA) — يجب على الرياضيين التنافسيين التحقق من الحالة الحالية مع هيئتهم الإدارية قبل أي استخدام بحثي. قد يكون استخدام المواد الكيميائية البحثية غير قانوني في ولايتك القضائية.',
        'wada_extra': 'هام: هذا المركب موجود حاليًا في قائمة الممنوعات الخاصة بالوكالة العالمية لمكافحة المنشطات (WADA). يواجه الرياضيون التنافسيون عقوبات على الاستخدام، بما في ذلك في برامج اختبارات التقاعد. تحقق من حالة WADA الحالية مع الهيئة الإدارية لرياضتك قبل أي مشاركة بحثية.',
    },
}


def detect_compound(slug):
    """Extract compound key from slug for WADA check."""
    s = slug.replace('.html', '')
    # Common compounds to check (order longest-first for greedy match)
    known = sorted(WADA_BANNED, key=len, reverse=True)
    for k in known:
        if s == k or s.startswith(k + '-') or s.startswith(k):
            return k
    return None


def build_disclaimer_html(lang, is_wada_banned, dir_attr=''):
    """Build the HTML for the comprehensive disclaimer block."""
    d = DISCLAIMERS[lang]
    rtl = ' dir="rtl"' if lang == 'ar' else ''
    html = (f'<div class="compliance-disclaimer" style="background:#fef2f2;border:1px solid #fecaca;border-radius:10px;'
            f'padding:20px 24px;margin:24px 0;font-size:13px;color:#991b1b;line-height:1.6;"{rtl}>'
            f'<p style="font-weight:700;margin:0 0 8px 0;">{d["title"]}</p>'
            f'<p style="margin:0 0 8px 0;">{d["body"]}</p>')
    if is_wada_banned:
        html += f'<p style="margin:8px 0 0 0;border-top:1px solid #fecaca;padding-top:8px;font-weight:600;">{d["wada_extra"]}</p>'
    html += '</div>'
    return html


# Pattern to match the existing pink disclaimer div
DISCLAIMER_PATTERN = re.compile(
    r'<div\s+(?:class="[^"]*"\s+)?style="background:#fef2f2[^>]*>.*?</div>',
    re.DOTALL
)


def process_file(path, lang):
    html = path.read_text(encoding='utf-8', errors='ignore')
    slug = path.stem
    compound = detect_compound(slug)
    is_wada = compound in WADA_BANNED if compound else False

    new_disclaimer = build_disclaimer_html(lang, is_wada)

    # Replace existing disclaimer (one or more instances)
    matches = DISCLAIMER_PATTERN.findall(html)
    if matches:
        # Replace all instances with the new comprehensive disclaimer
        new_html = DISCLAIMER_PATTERN.sub(lambda _: new_disclaimer, html, count=1)
        # Remove any remaining duplicate disclaimer blocks
        new_html = DISCLAIMER_PATTERN.sub('', new_html)
    else:
        # No existing disclaimer found — try to inject after opening <article> tag
        article_match = re.search(r'(<article[^>]*>)', new_html if matches else html, re.DOTALL)
        target = new_html if matches else html
        if article_match:
            new_html = target[:article_match.end()] + new_disclaimer + target[article_match.end():]
        else:
            return False, 'no-target'

    if new_html == html:
        return False, 'no-change'
    path.write_text(new_html, encoding='utf-8')
    return True, 'updated' + ('-wada' if is_wada else '')


def main():
    only_lang = os.environ.get('TARGET_LANG', None)
    langs = [only_lang] if only_lang and only_lang in LANGUAGES else LANGUAGES

    grand_total = 0
    grand_wada = 0
    for lang in langs:
        d = ROOT / lang
        if not d.is_dir():
            continue
        files = sorted(d.glob('*.html'))
        fixed = 0
        wada = 0
        for path in files:
            try:
                changed, action = process_file(path, lang)
                if changed:
                    fixed += 1
                    if 'wada' in action:
                        wada += 1
            except Exception as e:
                print(f"ERR {lang}/{path.name}: {e}", file=sys.stderr)
        print(f"{lang}: {fixed}/{len(files)} disclaimers updated ({wada} with WADA warning)")
        grand_total += fixed
        grand_wada += wada
    print(f"\n=== Phase 11 grand total: {grand_total} files, {grand_wada} with WADA warning ===")


if __name__ == '__main__':
    main()
