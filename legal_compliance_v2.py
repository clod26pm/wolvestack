#!/usr/bin/env python3
"""
WolveStack legal compliance v2 — multi-jurisdiction overhaul (2026-05-05).

Updates legal pages across all 13 languages with comprehensive disclaimers
covering FDA, MHRA, EMA, TGA, Health Canada, ANVISA + GDPR, UK GDPR, CCPA/CPRA,
PIPEDA, LGPD, Australia Privacy Act + arbitration + class action waiver +
indemnification + age 18+ + research-only framing.

Also injects a prominent top-of-article disclaimer banner and a cookie consent
banner site-wide.

Run from the peptide-daily-content/ directory:
    python3 legal_compliance_v2.py

Idempotent — safe to re-run.
"""
import re
from pathlib import Path

LANGS = ["en", "es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de", "nl", "ar"]
ROOT = Path(__file__).resolve().parent

# ---------- Translations of headings only (legal text stays English; canonical) ----------
# This is the standard pattern for global sites — translated UI, English contract.
TRANSLATIONS = {
    "en": {
        "privacy_title": "Privacy Policy",
        "privacy_subtitle": "How we collect, use, and protect your data — under GDPR, UK GDPR, CCPA/CPRA, PIPEDA, LGPD, and the Australia Privacy Act.",
        "terms_title": "Terms of Use",
        "terms_subtitle": "By using WolveStack you agree to these terms. Includes binding arbitration and class action waiver for U.S. users.",
        "disclaimer_title": "Research Disclaimer & Medical Notice",
        "disclaimer_subtitle": "Read before using any information on this site. This is not medical advice. Educational purposes only. 18+ only.",
        "affiliate_title": "Affiliate Disclosure",
        "affiliate_subtitle": "Full transparency on commissions, partnerships, and editorial independence — FTC, ASA, and EU compliant.",
        "lang_notice": "",
    },
    "es": {
        "privacy_title": "Política de Privacidad",
        "privacy_subtitle": "Cómo recopilamos, usamos y protegemos sus datos — bajo el RGPD, UK GDPR, CCPA/CPRA, PIPEDA, LGPD y la Ley de Privacidad de Australia.",
        "terms_title": "Términos de Uso",
        "terms_subtitle": "Al usar WolveStack acepta estos términos. Incluye arbitraje vinculante y renuncia a demandas colectivas para usuarios de EE. UU.",
        "disclaimer_title": "Aviso de Investigación y Médico",
        "disclaimer_subtitle": "Lea antes de utilizar cualquier información de este sitio. Esto no es asesoramiento médico. Solo con fines educativos. Solo mayores de 18 años.",
        "affiliate_title": "Divulgación de Afiliados",
        "affiliate_subtitle": "Transparencia total sobre comisiones, asociaciones e independencia editorial — cumple con la FTC, ASA y UE.",
        "lang_notice": "Esta traducción se proporciona por conveniencia. La versión en inglés es la única jurídicamente vinculante.",
    },
    "zh": {
        "privacy_title": "隐私政策",
        "privacy_subtitle": "我们如何收集、使用和保护您的数据 — 符合 GDPR、英国 GDPR、CCPA/CPRA、PIPEDA、LGPD 和澳大利亚隐私法。",
        "terms_title": "使用条款",
        "terms_subtitle": "使用 WolveStack 即表示您同意这些条款。包括对美国用户的具有约束力的仲裁和集体诉讼弃权。",
        "disclaimer_title": "研究免责声明与医疗声明",
        "disclaimer_subtitle": "在使用本网站任何信息之前请阅读。这不是医疗建议。仅供教育用途。仅限 18 岁及以上人士。",
        "affiliate_title": "联盟披露",
        "affiliate_subtitle": "关于佣金、合作伙伴关系和编辑独立性的完全透明 — 符合 FTC、ASA 和欧盟规定。",
        "lang_notice": "此翻译仅为方便提供。英文版本是唯一具有法律约束力的版本。",
    },
    "ja": {
        "privacy_title": "プライバシーポリシー",
        "privacy_subtitle": "GDPR、英国GDPR、CCPA/CPRA、PIPEDA、LGPD、オーストラリアプライバシー法に基づく、データ収集・使用・保護の方法。",
        "terms_title": "利用規約",
        "terms_subtitle": "WolveStackを使用することで、これらの規約に同意したものとみなされます。米国ユーザーには拘束力のある仲裁および集団訴訟放棄が含まれます。",
        "disclaimer_title": "研究目的の免責事項および医療上の注意",
        "disclaimer_subtitle": "本サイトの情報を使用する前にお読みください。これは医療アドバイスではありません。教育目的のみ。18歳以上のみ。",
        "affiliate_title": "アフィリエイト開示",
        "affiliate_subtitle": "手数料、提携関係、編集の独立性に関する完全な透明性 — FTC、ASA、EU準拠。",
        "lang_notice": "この翻訳は便宜上提供されています。法的拘束力があるのは英語版のみです。",
    },
    "pt": {
        "privacy_title": "Política de Privacidade",
        "privacy_subtitle": "Como coletamos, usamos e protegemos os seus dados — em conformidade com GDPR, UK GDPR, CCPA/CPRA, PIPEDA, LGPD e a Lei de Privacidade da Austrália.",
        "terms_title": "Termos de Uso",
        "terms_subtitle": "Ao usar o WolveStack você aceita estes termos. Inclui arbitragem vinculante e renúncia a ações coletivas para usuários dos EUA.",
        "disclaimer_title": "Aviso de Pesquisa e Médico",
        "disclaimer_subtitle": "Leia antes de usar qualquer informação deste site. Isto não é aconselhamento médico. Apenas para fins educacionais. Apenas maiores de 18 anos.",
        "affiliate_title": "Divulgação de Afiliados",
        "affiliate_subtitle": "Transparência total sobre comissões, parcerias e independência editorial — em conformidade com FTC, ASA e UE.",
        "lang_notice": "Esta tradução é fornecida por conveniência. A versão em inglês é a única juridicamente vinculante.",
    },
    "ru": {
        "privacy_title": "Политика конфиденциальности",
        "privacy_subtitle": "Как мы собираем, используем и защищаем ваши данные — в соответствии с GDPR, UK GDPR, CCPA/CPRA, PIPEDA, LGPD и Законом о конфиденциальности Австралии.",
        "terms_title": "Условия использования",
        "terms_subtitle": "Используя WolveStack, вы соглашаетесь с этими условиями. Включает обязательный арбитраж и отказ от коллективных исков для пользователей из США.",
        "disclaimer_title": "Исследовательская оговорка и медицинское уведомление",
        "disclaimer_subtitle": "Прочтите перед использованием любой информации на этом сайте. Это не медицинский совет. Только в образовательных целях. Только для лиц старше 18 лет.",
        "affiliate_title": "Раскрытие партнерской информации",
        "affiliate_subtitle": "Полная прозрачность в отношении комиссий, партнерств и редакционной независимости — соответствует FTC, ASA и ЕС.",
        "lang_notice": "Этот перевод предоставлен для удобства. Юридически обязательной является только английская версия.",
    },
    "it": {
        "privacy_title": "Informativa sulla Privacy",
        "privacy_subtitle": "Come raccogliamo, utilizziamo e proteggiamo i tuoi dati — ai sensi del GDPR, UK GDPR, CCPA/CPRA, PIPEDA, LGPD e della legge sulla privacy australiana.",
        "terms_title": "Termini di Utilizzo",
        "terms_subtitle": "Utilizzando WolveStack accetti questi termini. Include arbitrato vincolante e rinuncia alle azioni collettive per gli utenti statunitensi.",
        "disclaimer_title": "Avviso di Ricerca e Medico",
        "disclaimer_subtitle": "Leggi prima di utilizzare qualsiasi informazione di questo sito. Questo non è un consiglio medico. Solo a scopo educativo. Solo per maggiorenni (18+).",
        "affiliate_title": "Informativa Affiliati",
        "affiliate_subtitle": "Trasparenza totale su commissioni, partnership e indipendenza editoriale — conforme a FTC, ASA e UE.",
        "lang_notice": "Questa traduzione è fornita per comodità. La versione in inglese è l'unica giuridicamente vincolante.",
    },
    "pl": {
        "privacy_title": "Polityka Prywatności",
        "privacy_subtitle": "Jak gromadzimy, wykorzystujemy i chronimy Twoje dane — zgodnie z RODO, UK GDPR, CCPA/CPRA, PIPEDA, LGPD i australijską ustawą o prywatności.",
        "terms_title": "Warunki Użytkowania",
        "terms_subtitle": "Korzystając z WolveStack, akceptujesz te warunki. Obejmuje wiążący arbitraż i rezygnację z pozwów zbiorowych dla użytkowników z USA.",
        "disclaimer_title": "Zastrzeżenie Badawcze i Medyczne",
        "disclaimer_subtitle": "Przeczytaj przed użyciem jakichkolwiek informacji z tej strony. To nie jest porada medyczna. Wyłącznie w celach edukacyjnych. Tylko 18+.",
        "affiliate_title": "Ujawnienie Partnerstwa",
        "affiliate_subtitle": "Pełna przejrzystość w zakresie prowizji, partnerstw i niezależności redakcyjnej — zgodne z FTC, ASA i UE.",
        "lang_notice": "To tłumaczenie zostało dostarczone dla wygody. Jedyną prawnie wiążącą wersją jest wersja angielska.",
    },
    "fr": {
        "privacy_title": "Politique de Confidentialité",
        "privacy_subtitle": "Comment nous collectons, utilisons et protégeons vos données — conformément au RGPD, UK GDPR, CCPA/CPRA, PIPEDA, LGPD et à la loi australienne sur la confidentialité.",
        "terms_title": "Conditions d'Utilisation",
        "terms_subtitle": "En utilisant WolveStack, vous acceptez ces conditions. Comprend un arbitrage contraignant et une renonciation aux recours collectifs pour les utilisateurs américains.",
        "disclaimer_title": "Avis de Recherche et Médical",
        "disclaimer_subtitle": "À lire avant d'utiliser toute information de ce site. Ceci n'est pas un avis médical. À des fins éducatives uniquement. 18+ uniquement.",
        "affiliate_title": "Divulgation d'Affiliation",
        "affiliate_subtitle": "Transparence totale sur les commissions, les partenariats et l'indépendance éditoriale — conforme à la FTC, ASA et UE.",
        "lang_notice": "Cette traduction est fournie à titre indicatif. Seule la version anglaise est juridiquement contraignante.",
    },
    "id": {
        "privacy_title": "Kebijakan Privasi",
        "privacy_subtitle": "Bagaimana kami mengumpulkan, menggunakan, dan melindungi data Anda — sesuai GDPR, UK GDPR, CCPA/CPRA, PIPEDA, LGPD, dan UU Privasi Australia.",
        "terms_title": "Ketentuan Penggunaan",
        "terms_subtitle": "Dengan menggunakan WolveStack, Anda menyetujui ketentuan ini. Termasuk arbitrase yang mengikat dan pengabaian gugatan kelompok untuk pengguna AS.",
        "disclaimer_title": "Penafian Penelitian & Medis",
        "disclaimer_subtitle": "Baca sebelum menggunakan informasi apa pun di situs ini. Ini bukan nasihat medis. Hanya untuk tujuan pendidikan. Hanya 18+.",
        "affiliate_title": "Pengungkapan Afiliasi",
        "affiliate_subtitle": "Transparansi penuh tentang komisi, kemitraan, dan independensi editorial — sesuai FTC, ASA, dan UE.",
        "lang_notice": "Terjemahan ini disediakan demi kenyamanan. Versi bahasa Inggris adalah satu-satunya yang mengikat secara hukum.",
    },
    "de": {
        "privacy_title": "Datenschutzerklärung",
        "privacy_subtitle": "Wie wir Ihre Daten erheben, verwenden und schützen — gemäß DSGVO, UK GDPR, CCPA/CPRA, PIPEDA, LGPD und dem australischen Datenschutzgesetz.",
        "terms_title": "Nutzungsbedingungen",
        "terms_subtitle": "Durch die Nutzung von WolveStack stimmen Sie diesen Bedingungen zu. Beinhaltet bindendes Schiedsverfahren und Verzicht auf Sammelklagen für US-Nutzer.",
        "disclaimer_title": "Forschungs- und Medizinhinweis",
        "disclaimer_subtitle": "Lesen Sie dies, bevor Sie Informationen auf dieser Website nutzen. Dies ist keine medizinische Beratung. Nur zu Bildungszwecken. Nur 18+.",
        "affiliate_title": "Affiliate-Offenlegung",
        "affiliate_subtitle": "Vollständige Transparenz über Provisionen, Partnerschaften und redaktionelle Unabhängigkeit — FTC-, ASA- und EU-konform.",
        "lang_notice": "Diese Übersetzung wird zur Bequemlichkeit bereitgestellt. Die englische Version ist die einzige rechtsverbindliche Fassung.",
    },
    "nl": {
        "privacy_title": "Privacybeleid",
        "privacy_subtitle": "Hoe wij uw gegevens verzamelen, gebruiken en beschermen — onder AVG, UK GDPR, CCPA/CPRA, PIPEDA, LGPD en de Australische Privacy Act.",
        "terms_title": "Gebruiksvoorwaarden",
        "terms_subtitle": "Door WolveStack te gebruiken gaat u akkoord met deze voorwaarden. Inclusief bindende arbitrage en afstand van collectieve acties voor Amerikaanse gebruikers.",
        "disclaimer_title": "Onderzoeksdisclaimer & Medische Mededeling",
        "disclaimer_subtitle": "Lees voordat u informatie op deze site gebruikt. Dit is geen medisch advies. Alleen voor educatieve doeleinden. Alleen 18+.",
        "affiliate_title": "Affiliate-bekendmaking",
        "affiliate_subtitle": "Volledige transparantie over commissies, partnerschappen en redactionele onafhankelijkheid — voldoet aan FTC, ASA en EU.",
        "lang_notice": "Deze vertaling is voor het gemak verstrekt. De Engelse versie is de enige juridisch bindende versie.",
    },
    "ar": {
        "privacy_title": "سياسة الخصوصية",
        "privacy_subtitle": "كيف نجمع بياناتك ونستخدمها ونحميها — بموجب GDPR و UK GDPR و CCPA/CPRA و PIPEDA و LGPD وقانون الخصوصية الأسترالي.",
        "terms_title": "شروط الاستخدام",
        "terms_subtitle": "باستخدامك WolveStack فإنك توافق على هذه الشروط. تشمل التحكيم الملزم والتنازل عن الدعاوى الجماعية لمستخدمي الولايات المتحدة.",
        "disclaimer_title": "إخلاء مسؤولية البحث والإشعار الطبي",
        "disclaimer_subtitle": "اقرأ قبل استخدام أي معلومات على هذا الموقع. هذه ليست نصيحة طبية. لأغراض تعليمية فقط. للبالغين 18+ فقط.",
        "affiliate_title": "إفصاح الشراكة",
        "affiliate_subtitle": "شفافية كاملة حول العمولات والشراكات والاستقلالية التحريرية — متوافق مع FTC و ASA و EU.",
        "lang_notice": "هذه الترجمة مقدمة للراحة. النسخة الإنجليزية هي النسخة الوحيدة الملزمة قانونياً.",
    },
}

# ---------- Comprehensive English legal copy (canonical, ~English fallback) ----------

PRIVACY_BODY = """\
<h2>1. Plain-English Summary</h2>
<p>We run a research-education website. We collect minimal data. We don't sell it. We use Google Analytics 4 to understand traffic. We use cookies; you can decline non-essential ones via the banner. If you give us your email, we email you and only us. You have rights to access, correct, delete, and export your data — see Section 8.</p>

<h2>2. Who We Are (Data Controller)</h2>
<p>WolveStack ("we," "us," "our") is the data controller for personal data collected via wolvestack.com. Contact: wolvestack@pm.me. For GDPR/UK GDPR matters, the same address acts as our point of contact under Article 27 GDPR; if you are in the EU/UK and require an EU representative or UK representative, please contact us at this email and we will provide one for any specific data subject request.</p>

<h2>3. What We Collect</h2>
<p><strong>Automatically (every visitor):</strong> IP address (truncated by Google before storage in GA4), browser type, device type, operating system, pages viewed, time on site, referrer, approximate geographic region (country/region only), and cookie identifiers. Collected via Google Analytics 4 and standard server logs.</p>
<p><strong>Voluntarily (if you submit a form):</strong> email address, any free-text you type into a form. We collect nothing else.</p>
<p><strong>We do NOT collect:</strong> precise location, government identifiers, biometric data, financial data, health data, contact lists, photos, or anything else not listed above.</p>

<h2>4. Why We Collect It (Lawful Bases under GDPR Art. 6)</h2>
<ul>
<li><strong>Legitimate interests (Art. 6(1)(f)):</strong> running the site, understanding traffic, preventing abuse, securing infrastructure.</li>
<li><strong>Consent (Art. 6(1)(a)):</strong> non-essential cookies (analytics, advertising). You give consent via the cookie banner; you may withdraw it any time by clearing cookies and revisiting the site.</li>
<li><strong>Performance of a contract (Art. 6(1)(b)):</strong> if you sign up for a newsletter or download, we process your email to deliver what you asked for.</li>
</ul>

<h2>5. Cookies and Similar Technologies</h2>
<p>We use the following categories. The cookie banner lets you accept or decline non-essential categories.</p>
<ul>
<li><strong>Strictly necessary:</strong> session cookies for navigation. Cannot be disabled — required to render the site.</li>
<li><strong>Analytics:</strong> Google Analytics 4 (_ga, _ga_*). Anonymizes IP. Retention: 14 months. Optional.</li>
<li><strong>Affiliate tracking:</strong> set by third-party vendors when you click an affiliate link. Governed by their privacy policies. Optional.</li>
</ul>
<p>You can also block cookies via your browser settings, install the Google Analytics Opt-out Browser Add-on (<a href="https://tools.google.com/dlpage/gaoptout">tools.google.com/dlpage/gaoptout</a>), or enable Do Not Track. We honor Global Privacy Control (GPC) signals where required by law.</p>

<h2>6. Sharing and Third-Party Processors</h2>
<p>We share personal data only with the following sub-processors, each under a Data Processing Agreement:</p>
<ul>
<li><strong>Google LLC</strong> (Google Analytics 4) — anonymized analytics. EU/EEA data is processed under the EU-US Data Privacy Framework.</li>
<li><strong>Netlify, Inc.</strong> (hosting and CDN) — server logs, infrastructure.</li>
<li><strong>Cloudflare, Inc.</strong> (security/CDN, where applicable) — bot mitigation, DDoS protection.</li>
<li><strong>Email service provider</strong> (only if you subscribe) — newsletter delivery.</li>
</ul>
<p>We do not sell, rent, or share your personal data for cross-context behavioral advertising. We do not use it for AI training.</p>

<h2>7. International Transfers</h2>
<p>If you are in the EU/UK, your data may be transferred to the United States. Such transfers are protected by the EU-US Data Privacy Framework (Google), Standard Contractual Clauses (where applicable), and the UK International Data Transfer Addendum. You may request a copy of the safeguards in place by emailing wolvestack@pm.me.</p>

<h2>8. Your Rights</h2>
<p>Depending on your jurisdiction, you have the following rights. To exercise any of them, email <a href="mailto:wolvestack@pm.me">wolvestack@pm.me</a> with the subject line "Data Subject Request." We will respond within 30 days (GDPR/UK GDPR), 45 days (CCPA/CPRA), 30 days (LGPD), or as required by your local law.</p>
<ul>
<li><strong>EU/UK (GDPR / UK GDPR):</strong> access, rectification, erasure ("right to be forgotten"), restriction, portability, objection, and the right to lodge a complaint with your supervisory authority (e.g., ICO in the UK, CNIL in France, BfDI in Germany). You may also withdraw consent at any time.</li>
<li><strong>California (CCPA/CPRA):</strong> right to know, right to delete, right to correct, right to opt out of sale/sharing (we do not sell or share for cross-context advertising), right to limit use of sensitive personal information (we collect none), and right to non-discrimination.</li>
<li><strong>Other US states (CO, CT, VA, UT, OR, TX, etc.):</strong> rights similar to California, exercisable through the same email.</li>
<li><strong>Canada (PIPEDA):</strong> access, correction, withdrawal of consent, complaint to the Office of the Privacy Commissioner of Canada.</li>
<li><strong>Brazil (LGPD):</strong> confirmation of processing, access, correction, anonymization, portability, deletion, information about sharing, withdrawal of consent.</li>
<li><strong>Australia (Privacy Act 1988):</strong> access and correction; complaint to the Office of the Australian Information Commissioner (OAIC).</li>
<li><strong>Other jurisdictions:</strong> we honor reasonable requests in line with applicable law.</li>
</ul>

<h2>9. Retention</h2>
<p>Email subscribers: until you unsubscribe. Analytics data: 14 months (Google's default). Server logs: 30 days. We delete or anonymize personal data when no longer needed for the purpose collected.</p>

<h2>10. Children</h2>
<p>This site is for adults aged 18 and over (21+ in some jurisdictions). We do not knowingly collect data from children under 16. If you believe a child has submitted data, contact us and we will delete it.</p>

<h2>11. Security</h2>
<p>We use HTTPS, modern TLS, content security policies, and reputable hosting providers. No system is 100% secure; you assume the risks of internet transmission.</p>

<h2>12. Changes</h2>
<p>We may update this Privacy Policy. Material changes will be flagged at the top of this page; we will not retroactively reduce your rights without your consent.</p>

<h2>13. Complaints</h2>
<p>If you believe we have processed your data unlawfully, please contact us first at <a href="mailto:wolvestack@pm.me">wolvestack@pm.me</a>. You also have the right to lodge a complaint with the data-protection authority in your country.</p>
"""

DISCLAIMER_BODY = """\
<div style="background:#fef3c7;border:2px solid #d97706;border-radius:10px;padding:18px 20px;margin:0 0 28px;color:#7c2d12;">
<strong style="font-size:1.08em;">⚠️ READ THIS BEFORE USING ANYTHING ON THIS SITE</strong>
<p style="margin:6px 0 0;">WolveStack publishes <strong>educational research</strong> about peptide compounds. This is <strong>not medical advice</strong>. The compounds discussed are <strong>research chemicals</strong>, <strong>not approved by the FDA, EMA, MHRA, TGA, Health Canada, or any other regulatory authority</strong> for human therapeutic use. They are <strong>not intended for human consumption</strong>. <strong>You must be 18 or older</strong> (21+ in some jurisdictions) to use this site. By continuing, you accept full personal responsibility for any decisions you make.</p>
</div>

<h2>1. Educational and Informational Purposes Only</h2>
<p>All content on WolveStack — articles, guides, comparisons, dosing tables, study summaries, FAQ sections — is provided <strong>strictly for educational, scientific, journalistic, and informational purposes</strong>. No content here is a substitute for professional medical advice, diagnosis, or treatment. <strong>Always consult a qualified physician or licensed healthcare provider</strong> before making any decision related to your health or medication. <strong>Never disregard professional medical advice or delay seeking it</strong> because of something you read on this site.</p>

<h2>2. Not Medical Advice — No Doctor-Patient Relationship</h2>
<p>Reading WolveStack does not create a doctor-patient, therapist-client, or any other professional relationship. We are not licensed physicians, pharmacists, naturopaths, or healthcare providers. We do not diagnose, treat, prevent, or cure any disease, condition, or symptom. Statements that may appear to describe biological effects refer to research findings in laboratory or animal models, not clinical recommendations.</p>

<h2>3. Research Chemicals — Regulatory Status (Multi-Jurisdiction)</h2>
<p>The peptide compounds discussed on this site are sold and labeled as <strong>research chemicals for laboratory use only</strong>. Their regulatory status varies by country:</p>
<ul>
<li><strong>United States (FDA):</strong> <strong>Not FDA-approved</strong> for any clinical indication. Not scheduled or controlled for the compounds we cover. Cannot be marketed for human therapeutic use. The FDA's "research-use-only" labeling is not an endorsement of safety in humans.</li>
<li><strong>European Union (EMA):</strong> <strong>Not EMA-approved</strong>. Some compounds appear on the EMA's list of substances that may not be marketed as medicinal products without authorization. Marketing for human use without authorization is illegal in EU member states.</li>
<li><strong>United Kingdom (MHRA):</strong> <strong>Not MHRA-authorized</strong>. The Medicines and Healthcare products Regulatory Agency considers products marketed with medicinal claims to require an authorization. Sale to UK consumers as therapeutic products is unlawful.</li>
<li><strong>Australia (TGA):</strong> <strong>Not on the ARTG</strong>. The Therapeutic Goods Administration prohibits supply of therapeutic goods unless registered or listed. Personal importation rules apply but are restrictive.</li>
<li><strong>Canada (Health Canada):</strong> <strong>Not authorized as a Natural Health Product or as a Drug</strong>. Importation, sale, and advertising restrictions apply under the Food and Drugs Act and Natural Health Products Regulations.</li>
<li><strong>Brazil (ANVISA):</strong> <strong>Not registered</strong> for human therapeutic use; commercialization without ANVISA authorization is prohibited.</li>
<li><strong>Japan (PMDA):</strong> Most peptides we cover are not approved as pharmaceuticals.</li>
<li><strong>Other jurisdictions:</strong> Research compound regulations vary widely. <strong>You are responsible for checking the law in your country before purchasing, importing, possessing, or using any compound discussed on this site.</strong> Some compounds we discuss are controlled, restricted, or banned in some countries.</li>
</ul>
<p>The fact that a compound is "legal to purchase as a research chemical" in your jurisdiction does <strong>not</strong> mean it is safe, approved, or appropriate for human use.</p>

<h2>4. WADA / Athletic Competition</h2>
<p>Many peptides discussed on this site are <strong>banned by the World Anti-Doping Agency (WADA)</strong> at all times for athletic competition. Substances on the WADA Prohibited List include but are not limited to BPC-157, TB-500, growth hormone secretagogues (GHRPs), GHRH analogues (CJC-1295, sermorelin, tesamorelin), follistatin-related peptides, MOTS-c, and others. <strong>Athletes subject to anti-doping testing must not use these compounds.</strong></p>

<h2>5. Risks (Non-Exhaustive List)</h2>
<p>Use of unapproved peptide compounds outside controlled clinical settings carries significant risks, including but not limited to:</p>
<ul>
<li>Contamination, mis-identification, dosing errors, and impurities (manufacturing of research chemicals is not subject to GMP standards comparable to pharmaceuticals)</li>
<li>Allergic reactions, anaphylaxis, injection-site infections (sterile technique is the user's responsibility)</li>
<li>Hormonal dysregulation, including suppression of endogenous hormone production</li>
<li>Hypoglycemia (with insulin-related compounds), cardiovascular effects, fluid retention, hypertension</li>
<li>Increased risk of malignancy with angiogenic or growth-promoting peptides; potential acceleration of pre-existing tumors</li>
<li>Drug-drug interactions with prescription medications, particularly insulin, anti-hypertensives, hormonal therapies, and immune-modulators</li>
<li>Adverse effects in pregnancy, breastfeeding, or in individuals with hepatic, renal, cardiac, or oncologic conditions</li>
<li>Long-term effects that are simply unknown — there is no extended human safety data for most research peptides</li>
<li>Legal consequences if the compound is restricted or controlled in your jurisdiction</li>
</ul>
<p>If you experience any adverse symptom after using a peptide, <strong>seek immediate medical attention</strong> and report the event to your country's adverse-event reporting system (e.g., FDA MedWatch, EMA EudraVigilance, MHRA Yellow Card, TGA Adverse Event Reporting, Health Canada Vigilance Program).</p>

<h2>6. No Endorsement of Any Specific Vendor</h2>
<p>References to vendors are based on our editorial assessment of public information and may include affiliate relationships (see our Affiliate Disclosure). We do not manufacture, distribute, or sell peptide compounds. We do not verify the contents of any product you purchase. <strong>Always require third-party Certificates of Analysis (COAs)</strong> from independent labs and assume nothing about purity, potency, or sterility based solely on a vendor's marketing.</p>

<h2>7. No Warranty</h2>
<p>Information on WolveStack is provided <strong>"AS IS"</strong> and <strong>"AS AVAILABLE"</strong>, without warranty of any kind, express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, accuracy, completeness, currency, or non-infringement. Peptide research evolves rapidly; some statements on this site may become outdated.</p>

<h2>8. No Liability</h2>
<p>To the maximum extent permitted by applicable law, WolveStack, its operators, contributors, employees, and affiliates are <strong>not liable</strong> for any direct, indirect, incidental, consequential, special, exemplary, or punitive damages — including but not limited to bodily injury, illness, death, lost profits, lost data, or emotional distress — arising from your access to or use of this site, your reliance on any content, or any decision you make based on information here, even if we have been advised of the possibility of such damages. <strong>You assume all risk.</strong></p>

<h2>9. Indemnification</h2>
<p>You agree to indemnify, defend, and hold harmless WolveStack, its operators, contributors, and affiliates from any claims, damages, losses, costs, or expenses (including reasonable attorney fees) arising from your use of this site, your violation of these terms or any law, your infringement of any third-party right, or any decision you make based on information obtained here.</p>

<h2>10. Age Restriction</h2>
<p>This site is intended for adults <strong>aged 18 or older</strong> (21+ where required by local law). If you are under 18, you must leave this site immediately. Users under 18 are not authorized to view, download, or rely on any content here.</p>

<h2>11. Personal Responsibility</h2>
<p>By using this site you affirm that: (a) you are an adult of legal age in your jurisdiction; (b) you understand that no information here is medical advice; (c) you will independently verify any decision with a licensed healthcare professional before acting on it; (d) you accept full and exclusive responsibility for any consequence of your decisions.</p>

<h2>12. Reporting Adverse Events</h2>
<p>If you or someone you know experiences an adverse event after using any compound discussed here, contact emergency services if necessary, then report the event to the appropriate authority: FDA MedWatch (US, 1-800-FDA-1088), EMA EudraVigilance (EU), MHRA Yellow Card (UK), TGA (Australia), Health Canada Vigilance Program (Canada), ANVISA (Brazil), or your country's equivalent.</p>
"""

TERMS_BODY = """\
<h2>1. Acceptance of Terms</h2>
<p>By accessing or using WolveStack ("Site"), you agree to be bound by these Terms of Use ("Terms"), our <a href="/en/privacy.html">Privacy Policy</a>, our <a href="/en/disclaimer.html">Research Disclaimer</a>, and our <a href="/en/affiliate-disclosure.html">Affiliate Disclosure</a>. If you do not agree, do not use the Site. You must be at least 18 years of age (21+ where required by local law) and legally able to enter into binding contracts in your jurisdiction.</p>

<h2>2. Educational Use Only</h2>
<p>All Site content is provided for educational and informational purposes. Nothing on the Site is medical advice or constitutes any kind of professional service. You may not use the Site or its content to advise, treat, diagnose, or counsel any person regarding peptides or health, in a professional, medical, or commercial capacity, without your own independent professional judgment.</p>

<h2>3. Intellectual Property and Limited License</h2>
<p>All original content on the Site — text, articles, images, charts, code, design, branding — is owned by WolveStack or licensed to WolveStack. We grant you a limited, non-exclusive, non-transferable, revocable license to view content in your personal browser. You may quote up to 50 words with attribution and a working link back to the original article. Bulk reproduction, scraping, training of generative AI on our content, mirroring, and republication require <strong>prior written permission</strong>. Unauthorized use is a copyright violation and may also breach computer-fraud statutes (e.g., 18 USC §1030 in the US).</p>

<h2>4. Affiliate Links and Sponsorship</h2>
<p>The Site contains affiliate links. See our <a href="/en/affiliate-disclosure.html">Affiliate Disclosure</a>. Editorial decisions are independent of commission rates.</p>

<h2>5. User Conduct</h2>
<p>You agree not to: (a) use the Site for any unlawful purpose; (b) attempt to gain unauthorized access to any part of the Site or its infrastructure; (c) interfere with or disrupt the Site; (d) use scraping, harvesting, or data-mining tools without our written permission; (e) train AI/ML models on Site content; (f) misrepresent your identity or affiliation; (g) post defamatory, harassing, or unlawful content if a comment feature is provided.</p>

<h2>6. Disclaimer of Warranties</h2>
<p>The Site is provided "AS IS" and "AS AVAILABLE." To the maximum extent permitted by law, we disclaim all warranties, express or implied, including merchantability, fitness for a particular purpose, accuracy, non-infringement, and uninterrupted availability. We do not warrant that any content is current, complete, or free from error.</p>

<h2>7. Limitation of Liability</h2>
<p>To the maximum extent permitted by applicable law, in no event will WolveStack or its operators, contributors, employees, or affiliates be liable for any indirect, incidental, special, consequential, exemplary, or punitive damages — including bodily injury, illness, death, lost profits, lost data, or emotional distress — arising from your use of the Site, your reliance on any content, or any decision you make based on the Site, even if we have been advised of the possibility of such damages. Our aggregate liability for any direct damages will not exceed USD $50.</p>

<h2>8. Indemnification</h2>
<p>You agree to indemnify, defend, and hold harmless WolveStack, its operators, contributors, and affiliates from any claims, damages, losses, costs, or expenses (including reasonable attorney fees) arising from: (a) your use of the Site; (b) your violation of these Terms; (c) your violation of any law or any third-party right; (d) any decision or action you take based on the Site.</p>

<h2>9. Binding Arbitration and Class Action Waiver (U.S. Users)</h2>
<p><strong>If you are located in the United States:</strong> Any dispute, claim, or controversy arising out of or relating to these Terms or your use of the Site shall be resolved through <strong>final and binding individual arbitration</strong> administered by the American Arbitration Association (AAA) under its Consumer Arbitration Rules, with the seat of arbitration in Wilmington, Delaware. Arbitration proceedings will be conducted in English by a single arbitrator. <strong>YOU AND WOLVESTACK AGREE THAT EACH MAY BRING CLAIMS AGAINST THE OTHER ONLY IN AN INDIVIDUAL CAPACITY AND NOT AS A PLAINTIFF OR CLASS MEMBER IN ANY PURPORTED CLASS, COLLECTIVE, OR REPRESENTATIVE PROCEEDING. YOU WAIVE ANY RIGHT TO TRIAL BY JURY.</strong> You may opt out of this arbitration provision by sending written notice to <a href="mailto:wolvestack@pm.me">wolvestack@pm.me</a> within 30 days of first accepting these Terms; the notice must include your name, contact information, and a clear statement that you wish to opt out.</p>

<h2>10. Governing Law and Jurisdiction</h2>
<p><strong>U.S. users:</strong> these Terms are governed by the laws of the State of Delaware, United States, without regard to conflict-of-laws principles, and the Federal Arbitration Act governs Section 9.</p>
<p><strong>Users in the EU/UK:</strong> nothing in these Terms limits or excludes your statutory consumer rights under the laws of your country of residence. Mandatory consumer-protection rules in your country apply notwithstanding the choice of law in this Section.</p>
<p><strong>All other jurisdictions:</strong> these Terms are governed by Delaware law, except where mandatory local consumer-protection law applies, in which case such mandatory law prevails.</p>

<h2>11. Force Majeure</h2>
<p>We are not liable for any failure or delay in performance caused by circumstances beyond our reasonable control, including natural disasters, war, terrorism, civil unrest, government action, internet outages, or third-party service failures.</p>

<h2>12. Changes to These Terms</h2>
<p>We may modify these Terms at any time by posting the updated version on this page. Material changes will be flagged at the top of the page. Your continued use of the Site after the effective date constitutes acceptance.</p>

<h2>13. Termination</h2>
<p>We may suspend or terminate your access at any time, with or without notice, for any reason, including violation of these Terms. Sections 3, 6, 7, 8, 9, 10, and this Section 13 survive termination.</p>

<h2>14. Severability</h2>
<p>If any provision of these Terms is held unenforceable, the remaining provisions remain in full force and effect, and the unenforceable provision will be interpreted to give effect to its intent to the fullest extent allowed.</p>

<h2>15. Entire Agreement</h2>
<p>These Terms, together with the documents incorporated by reference (Privacy Policy, Disclaimer, Affiliate Disclosure), constitute the entire agreement between you and us regarding the Site, and supersede any prior agreements.</p>

<h2>16. Contact</h2>
<p>Questions: <a href="mailto:wolvestack@pm.me">wolvestack@pm.me</a>.</p>
"""

AFFILIATE_BODY = """\
<h2>1. Plain-English Summary</h2>
<p>Some links on this site are affiliate links. If you click and buy, the vendor pays us a commission at no extra cost to you. We disclose this for legal compliance and because we believe in transparency. Editorial coverage is independent of commission rates — we have declined higher-paying affiliations from vendors that didn't meet our quality bar.</p>

<h2>2. Multi-Jurisdiction Compliance</h2>
<p>This disclosure is intended to satisfy:</p>
<ul>
<li><strong>United States — FTC 16 CFR Part 255:</strong> Federal Trade Commission Guides Concerning the Use of Endorsements and Testimonials in Advertising. Material connections (affiliate commissions) are disclosed clearly and conspicuously.</li>
<li><strong>United Kingdom — ASA / CAP Code:</strong> Advertising Standards Authority and Committee of Advertising Practice rules require affiliate content to be clearly labeled. We label affiliate context inline near affiliate links and on this page.</li>
<li><strong>European Union — Modernisation Directive (Directive 2019/2161, transposed into the UCPD):</strong> commercial purpose of any communication must be made clear. Affiliate commissions are disclosed.</li>
<li><strong>Australia — ACCC / ASB:</strong> Australian Competition and Consumer Commission and Ad Standards Bureau guidance on disclosure of commercial relationships in editorial content.</li>
<li><strong>Canada — Competition Bureau:</strong> deceptive marketing provisions of the Competition Act; we disclose material connections.</li>
<li><strong>Brazil — CONAR / Code of Self-Regulation:</strong> commercial intent of advertising disclosed.</li>
</ul>

<h2>3. What Counts as an Affiliate Link</h2>
<p>Vendor links in our sourcing guide, individual article sidebar vendor cards, comparison tables, and any in-line link to a vendor's product page may be affiliate links. We label these where possible (e.g., "(affiliate link)" or via context). If you are unsure whether a specific link is an affiliate link, assume it is and email us if you want clarification.</p>

<h2>4. How Editorial Decisions Are Made</h2>
<p>Vendor inclusion and ranking on WolveStack is based on:</p>
<ul>
<li>Independent assessment of HPLC purity testing data and Certificates of Analysis (COA)</li>
<li>Third-party laboratory verification</li>
<li>Community reputation and user reports</li>
<li>Customer-service responsiveness and shipping reliability</li>
<li>Transparency about sourcing and manufacturing</li>
</ul>
<p>Commission rates are <strong>not</strong> a factor in coverage or ranking. We have declined higher-commission relationships with vendors that did not meet our quality criteria, and we have included high-quality vendors that do not pay us at all.</p>

<h2>5. Vendors We Currently Have Affiliate Relationships With</h2>
<p>The current list of affiliate partners is published on our sourcing guide. We update it when relationships change.</p>

<h2>6. We Do Not</h2>
<ul>
<li>Receive payment for positive reviews — vendor coverage is independent of payment</li>
<li>Receive personally identifiable information from your affiliate clicks (we receive only aggregate commission data)</li>
<li>Sponsor content without disclosure — sponsored placements would be clearly marked "Sponsored" or "Paid"</li>
<li>Allow advertisers to dictate or pre-approve editorial content</li>
</ul>

<h2>7. Tax and Income Disclosure</h2>
<p>Affiliate commissions are reported as business income in the operator's home jurisdiction and taxed accordingly. We do not pass affiliate-tracking cookies or personally identifiable click data to any party other than the vendor whose link you clicked.</p>

<h2>8. Questions or Complaints</h2>
<p>If you believe any disclosure on this site is unclear or misleading, please email <a href="mailto:wolvestack@pm.me">wolvestack@pm.me</a>. You may also file a complaint with the relevant regulator in your jurisdiction (FTC, ASA, ACCC, etc.).</p>
"""

# ---------- Cookie consent banner (loaded site-wide via /cookie-banner.js) ----------
COOKIE_BANNER_JS = """\
/* WolveStack cookie consent banner — GDPR / UK GDPR / CCPA / LGPD compliant */
(function() {
  if (window.__cookieBannerLoaded) return;
  window.__cookieBannerLoaded = true;

  const KEY = 'wolvestack_cookie_consent_v1';
  const stored = localStorage.getItem(KEY);
  if (stored) {
    // Already decided. If accepted, GA already loaded by main page. Done.
    return;
  }

  const banner = document.createElement('div');
  banner.setAttribute('role', 'dialog');
  banner.setAttribute('aria-label', 'Cookie consent');
  banner.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#0f2240;color:#fff;padding:16px 20px;z-index:99999;box-shadow:0 -4px 24px rgba(0,0,0,0.25);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:14px;line-height:1.55;';
  banner.innerHTML = `
    <div style="max-width:1100px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;gap:14px;">
      <div style="flex:1 1 320px;min-width:240px;">
        <strong style="color:#14bdac;">We use cookies</strong> &mdash; strictly-necessary cookies always, and Google Analytics only with your consent. Read our <a href="/en/privacy.html" style="color:#14bdac;text-decoration:underline;">Privacy Policy</a> and <a href="/en/disclaimer.html" style="color:#14bdac;text-decoration:underline;">Disclaimer</a>.
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <button id="ws-cookie-decline" style="background:transparent;color:#cbd5e1;border:1px solid #475569;border-radius:6px;padding:8px 16px;cursor:pointer;font-size:13px;font-family:inherit;">Decline non-essential</button>
        <button id="ws-cookie-accept" style="background:#14bdac;color:#0f2240;border:none;border-radius:6px;padding:8px 18px;cursor:pointer;font-weight:700;font-size:13px;font-family:inherit;">Accept all</button>
      </div>
    </div>`;
  document.body.appendChild(banner);

  function decide(value) {
    try { localStorage.setItem(KEY, JSON.stringify({decision: value, timestamp: Date.now()})); } catch (e) {}
    banner.remove();
    if (value === 'accept') {
      // GA was loaded with consent denied; grant it now.
      if (typeof gtag === 'function') {
        gtag('consent', 'update', {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
      }
    }
  }
  document.getElementById('ws-cookie-accept').addEventListener('click', () => decide('accept'));
  document.getElementById('ws-cookie-decline').addEventListener('click', () => decide('decline'));
})();
"""

# ---------- Top-of-article disclaimer banner (HTML snippet) ----------
TOP_BANNER_HTML = """\
<div style="background:#fef3c7;border-left:6px solid #d97706;padding:14px 18px;margin:0 0 24px;color:#7c2d12;font-size:14.5px;line-height:1.55;border-radius:0 8px 8px 0;">
<strong>Educational research only.</strong> The compounds discussed here are <strong>not approved</strong> by the FDA, EMA, MHRA, TGA, or Health Canada for human therapeutic use. They are research chemicals. Nothing on this page is medical advice. <strong>You must be 18+.</strong> Consult a licensed healthcare professional before acting on anything you read. <a href="/en/disclaimer.html" style="color:#7c2d12;text-decoration:underline;font-weight:600;">Full disclaimer →</a>
</div>
"""


# ---------- Helpers ----------
HERO_RX = re.compile(
    r'<div class="page-hero">\s*<h1>[^<]*</h1>\s*<p>[^<]*</p>\s*</div>',
    re.DOTALL | re.IGNORECASE,
)
WRAP_RX = re.compile(
    r'<div class="content-wrap">.*?</div>\s*(?=<footer|<div class="section-card)',
    re.DOTALL,
)
LANG_NOTICE_HTML = """\
<div style="background:#f1f5f9;border:1px solid #e2e8f0;color:#475569;padding:10px 14px;border-radius:8px;margin:0 0 24px;font-size:13.5px;">
<strong>{lang}:</strong> {notice}
</div>
"""

def replace_legal_page(path: Path, hero_title: str, hero_subtitle: str, body_html: str, lang_notice: str):
    if not path.exists():
        print(f"  skip (missing): {path}")
        return False
    html = path.read_text(encoding="utf-8")
    new_hero = (
        f'<div class="page-hero">\n'
        f'<h1>{hero_title}</h1>\n'
        f'<p>{hero_subtitle}</p>\n'
        f'</div>'
    )
    notice_block = ""
    if lang_notice:
        notice_block = LANG_NOTICE_HTML.format(lang="Note", notice=lang_notice)
    new_wrap = f'<div class="content-wrap">\n{notice_block}{body_html}\n</div>\n'
    if HERO_RX.search(html):
        html = HERO_RX.sub(new_hero, html, count=1)
    if WRAP_RX.search(html):
        html = WRAP_RX.sub(new_wrap, html, count=1)
    else:
        # fallback: just replace the older content-wrap pattern that ends right before </footer>
        old_wrap = re.search(r'<div class="content-wrap">.*?</div>(?=\s*<footer)', html, re.DOTALL)
        if old_wrap:
            html = html[: old_wrap.start()] + new_wrap + html[old_wrap.end():]
    # Also inject the cookie banner script reference if missing
    if 'cookie-banner.js' not in html and '</body>' in html:
        html = html.replace('</body>', '<script defer src="/cookie-banner.js"></script>\n</body>')
    path.write_text(html, encoding="utf-8")
    return True


def update_lang_dir(lang: str):
    print(f"\n=== {lang} ===")
    base = ROOT if lang == "en_root_only" else (ROOT / lang)
    tr = TRANSLATIONS.get(lang, TRANSLATIONS["en"])

    # Files to update
    files = {
        "privacy.html":             (tr["privacy_title"], tr["privacy_subtitle"], PRIVACY_BODY),
        "terms.html":               (tr["terms_title"], tr["terms_subtitle"], TERMS_BODY),
        "disclaimer.html":          (tr["disclaimer_title"], tr["disclaimer_subtitle"], DISCLAIMER_BODY),
        "affiliate-disclosure.html":(tr["affiliate_title"], tr["affiliate_subtitle"], AFFILIATE_BODY),
    }
    for fname, (title, subtitle, body) in files.items():
        p = base / fname
        ok = replace_legal_page(p, title, subtitle, body, tr.get("lang_notice", ""))
        print(f"  {'updated' if ok else 'skipped'}: {p.relative_to(ROOT)}")


def update_root_legal_pages():
    """Root-level copies (mirrors of /en/) — keep in sync."""
    print("\n=== root ===")
    base = ROOT
    tr = TRANSLATIONS["en"]
    files = {
        "privacy.html":             (tr["privacy_title"], tr["privacy_subtitle"], PRIVACY_BODY),
        "terms.html":               (tr["terms_title"], tr["terms_subtitle"], TERMS_BODY),
        "disclaimer.html":          (tr["disclaimer_title"], tr["disclaimer_subtitle"], DISCLAIMER_BODY),
        "affiliate-disclosure.html":(tr["affiliate_title"], tr["affiliate_subtitle"], AFFILIATE_BODY),
    }
    for fname, (title, subtitle, body) in files.items():
        p = base / fname
        ok = replace_legal_page(p, title, subtitle, body, "")
        print(f"  {'updated' if ok else 'skipped'}: {fname}")


def write_cookie_banner_js():
    p = ROOT / "cookie-banner.js"
    p.write_text(COOKIE_BANNER_JS, encoding="utf-8")
    print(f"\nwrote: cookie-banner.js")


def inject_top_banner_into_articles():
    """Inject TOP_BANNER_HTML right after the closing </div> of .article-hero
    on every article page. Idempotent — bail if banner already present."""
    print("\n=== injecting top-of-article disclaimer banners ===")
    # Article pattern: contains '<div class="article-hero">' near top
    candidates = []
    for p in list(ROOT.glob("*.html")) + [q for lang in LANGS for q in (ROOT / lang).glob("*.html")]:
        # Skip legal/static pages
        if any(p.name == name for name in (
            "privacy.html", "terms.html", "disclaimer.html", "affiliate-disclosure.html",
            "404.html", "about.html", "contact.html", "search.html", "ARTICLE-TEMPLATE.html",
            "TEMPLATE-CSS.html", "TEMPLATE-BODY.html", "index.html", "category.html",
            "isitascam.html", "isitascam-privacy.html", "isitascam-support.html", "isitascam-terms.html",
        )):
            continue
        candidates.append(p)
    print(f"  found {len(candidates)} article files")
    injected = 0
    for p in candidates:
        try:
            html = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if "MULTI-JURISDICTION-DISCLAIMER" in html:
            continue  # already injected
        if 'class="article-hero"' not in html:
            continue
        # Insert right after the article-hero closing </div></div> (the inner pair)
        # Pattern: </div>\s*</div>\s*  preceded by the hero content
        marker_rx = re.compile(r'(<div class="article-hero">.*?</div>\s*</div>)', re.DOTALL)
        m = marker_rx.search(html)
        if not m:
            continue
        replacement = m.group(1) + f"\n<!-- MULTI-JURISDICTION-DISCLAIMER -->\n{TOP_BANNER_HTML}"
        html = html[: m.start()] + replacement + html[m.end():]
        # Also inject cookie banner script if missing
        if 'cookie-banner.js' not in html and '</body>' in html:
            html = html.replace('</body>', '<script defer src="/cookie-banner.js"></script>\n</body>')
        p.write_text(html, encoding="utf-8")
        injected += 1
    print(f"  injected into {injected} article files")


def main():
    update_root_legal_pages()
    for lang in LANGS:
        update_lang_dir(lang)
    write_cookie_banner_js()
    inject_top_banner_into_articles()
    print("\n✅ legal compliance v2 update complete")


if __name__ == "__main__":
    main()
