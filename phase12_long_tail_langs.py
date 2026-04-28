#!/usr/bin/env python3
"""
Phase 12: Cornerstone v2 generators for ru/pl/nl/id long-tail languages.

Goal: protect whole-site quality signals by ensuring the cornerstone
compound pages (highest-traffic targets) in these languages have
humanized v2 content rather than Argos-translated boilerplate.

3 cornerstone compounds × 5 aspects × 4 languages = 60 pages.
Compounds: BPC-157, TB-500, Semaglutide.
"""
import os, re, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LANGUAGES = ['ru', 'pl', 'nl', 'id']

COMPOUNDS = {
    'bpc-157': {
        'ru': {
            'name': 'BPC-157',
            'category': 'Пептид восстановления тканей',
            'related': ['tb-500', 'ghk-cu'],
            'overview': 'BPC-157 — это 15-аминокислотный фрагмент более крупного белка, обнаруженного в желудочном соке человека (собственное защитное соединение организма, отсюда и название). Лаборатория Предрага Сикирича в Загребском университете впервые выделила и охарактеризовала его в начале 1990-х годов, изначально как защитное средство для желудка. Никто не ожидал, насколько широко оно будет работать в других тканях. К началу 2000-х годов исследования на животных показывали, что BPC-157 ускоряет заживление сухожилий, связок, мышц, мозга, кровеносных сосудов — практически любой ткани, которую тестировали. Подозрительный профиль (соединения, которые работают для всего, обычно не работают ни для чего), но согласованность данных на грызунах действительно впечатляет, и Сикирич опубликовал более 200 статей по этой теме.',
            'mechanism': 'Механизм сложный, потому что BPC-157, кажется, делает несколько вещей одновременно. Он повышает регуляцию VEGF и стимулирует ангиогенез (образование новых кровеносных сосудов в местах повреждения), что, вероятно, объясняет большую часть заживляющего эффекта — лучшее кровоснабжение, лучшее восстановление. Увеличивает синтез оксида азота. Модулирует системы дофамина и серотонина через ось кишечник-мозг (главная теоретическая основа Сикирича). Взаимодействует с экспрессией рецептора гормона роста. Честный итог: никто не определил единый первичный механизм, и это тревожит некоторых исследователей. Компромисс в том, что та же история о множественных механизмах объяснит, почему один пептид помогает при стольких разных травмах.',
            'evidence': 'Здесь нужно быть осторожным. Доказательства на животных действительно впечатляют — Krivic et al. (2008) показали ускоренное восстановление ахиллова сухожилия у крыс, Cerovecki et al. (2010) показали более быстрое заживление медиальной коллатеральной связки, и есть длинная серия исследований гастрита, индуцированного НПВП, показывающих 90%+ слизистой защиты. Загвоздка: по состоянию на 2026 год нет зарегистрированных рандомизированных клинических испытаний на людях. Сообщество атлетического восстановления фактически провело гигантский неконтролируемый эксперимент в течение 15+ лет с анекдотами от чудесных до без эффекта, но это не то же самое, что доказательства РКИ.',
            'dosing': 'Типичные исследовательские протоколы используют 200-500 мкг в день подкожно, часто разделенные на две дозы. Многие пользователи инжектируют близко к месту травмы по теории, что местная концентрация помогает — это правдоподобно, но фактически не доказано. Пероральные протоколы (250-500 мкг, 1-2 раза в день) также изучаются; BPC-157 необычно стабилен в желудочной кислоте. Острые травмы часто начинаются с более высоких нагрузочных доз (500 мкг два раза в день) в течение 4-8 недель. Период полураспада короткий (несколько часов подкожно), поэтому дозирование два раза в день стандартно.',
            'safety': 'Профиль безопасности в исследованиях на животных отличный — чрезвычайно высокий LD50 (>10г/кг), нет случаев острой токсичности. Долгосрочные данные на людях просто не существуют. Сообщаемые легкие побочные эффекты заметны главным образом тем, что они невыразительны: случайные реакции в месте инъекции (~10-15% пользователей), переходная усталость в первую неделю, легкая тошнота при пероральных протоколах. Теоретическая проблема, которая возникает чаще всего, — могут ли свойства, способствующие ангиогенезу, ускорять существующие опухоли — нет доказательств за или против у людей, но большинство исследователей исключают рак в анамнезе как меру предосторожности. Не одобрен FDA. Примечательно, WADA не запретило его (по состоянию на 2026 год), в отличие от TB-500.',
            'quick_answer': 'BPC-157 — это 15-аминокислотный пептид, полученный из желудочного сока человека, изучаемый с начала 1990-х годов лабораторией Сикирича в Загребе на предмет тканеремонтных эффектов. Доказательства на животных по сухожилиям, связкам, мышцам и заживлению кишечника последовательны и впечатляющи — загвоздка в том, что нет зарегистрированных испытаний на людях. Типичные протоколы: 200-500 мкг/день подкожно в течение 4-8 недель. Механизм многопутевой (ангиогенез, оксид азота, ось кишечник-мозг). Часто сочетается с TB-500 для работы с травмами. Не одобрен FDA.',
        },
        'pl': {
            'name': 'BPC-157',
            'category': 'Peptyd naprawy tkanek',
            'related': ['tb-500', 'ghk-cu'],
            'overview': 'BPC-157 to 15-aminokwasowy fragment większego białka znajdującego się w ludzkim soku żołądkowym — własny związek ochronny organizmu, stąd nazwa. Laboratorium Predraga Sikirica na Uniwersytecie Zagrzebskim po raz pierwszy wyizolowało i scharakteryzowało go na początku lat 90-tych, początkowo jako środek ochronny żołądka. Nikt nie spodziewał się, jak szeroko będzie działać w innych tkankach. Na początku lat 2000 badania na zwierzętach pokazywały, że BPC-157 przyspiesza gojenie ścięgien, więzadeł, mięśni, mózgu, naczyń krwionośnych — niemal każdej testowanej tkanki. To podejrzany profil (związki, które działają na wszystko, zwykle nie działają na nic), ale spójność danych na gryzoniach jest naprawdę uderzająca, a Sikirič opublikował teraz ponad 200 artykułów na ten temat.',
            'mechanism': 'Mechanizm jest skomplikowany, ponieważ BPC-157 wydaje się robić kilka rzeczy jednocześnie. Reguluje w górę VEGF i promuje angiogenezę (tworzenie nowych naczyń krwionośnych w miejscach urazu), co prawdopodobnie wyjaśnia dużą część efektu gojenia — lepsze ukrwienie, lepsza naprawa. Zwiększa syntezę tlenku azotu. Moduluje systemy dopaminy i serotoniny poprzez oś jelitowo-mózgową (główne ramy teoretyczne Sikiricia). Współdziała z ekspresją receptora hormonu wzrostu. Uczciwe podsumowanie: nikt nie zidentyfikował pojedynczego pierwotnego mechanizmu, i to niepokoi niektórych badaczy.',
            'evidence': 'Tutaj trzeba być ostrożnym. Dowody na zwierzętach są naprawdę imponujące — Krivic et al. (2008) wykazali przyspieszoną naprawę ścięgna Achillesa u szczurów, Cerovecki et al. (2010) wykazali szybsze gojenie więzadła pobocznego przyśrodkowego. Haczyk: w 2026 roku nie ma zarejestrowanych randomizowanych badań klinicznych u ludzi. Społeczność rekonwalescencji sportowej skutecznie prowadzi gigantyczny niekontrolowany eksperyment od 15+ lat z anegdotami od cudownych do braku efektu, ale to nie to samo, co dowody RCT.',
            'dosing': 'Typowe protokoły badawcze używają 200-500 mcg dziennie podskórnie, często podzielone na dwie dawki. Wielu użytkowników wstrzykuje blisko miejsca urazu według teorii, że lokalne stężenie pomaga — jest to wiarygodne, ale w rzeczywistości nieudowodnione. Protokoły doustne (250-500 mcg, 1-2x dziennie) są również badane; BPC-157 jest niezwykle stabilny w kwasie żołądkowym. Ostre urazy często zaczynają się od wyższych dawek nasycających (500 mcg dwa razy dziennie) przez 4-8 tygodni.',
            'safety': 'Profil bezpieczeństwa w badaniach na zwierzętach jest doskonały — niezwykle wysoka LD50 (>10g/kg), brak przypadków ostrej toksyczności. Długoterminowe dane u ludzi po prostu nie istnieją. Zgłaszane łagodne działania niepożądane są zauważalne głównie ze względu na ich niezauważalność: okazjonalne reakcje w miejscu wstrzyknięcia (~10-15% użytkowników), przejściowe zmęczenie w pierwszym tygodniu, łagodne nudności w protokołach doustnych. Nie zatwierdzony przez FDA. Co ciekawe, WADA nie zakazała go (w 2026 roku), w przeciwieństwie do TB-500.',
            'quick_answer': 'BPC-157 to 15-aminokwasowy peptyd pochodzący z ludzkiego soku żołądkowego, badany od początku lat 90-tych przez laboratorium Sikirica w Zagrzebiu pod kątem efektów naprawy tkanek. Dowody na zwierzętach dotyczące ścięgien, więzadeł, mięśni i gojenia jelit są spójne i imponujące — haczyk polega na tym, że nie ma zarejestrowanych badań klinicznych u ludzi. Typowe protokoły: 200-500 mcg/dzień podskórnie przez 4-8 tygodni. Mechanizm wielodrogowy. Często łączony z TB-500 do pracy z urazami. Niezatwierdzony przez FDA.',
        },
        'nl': {
            'name': 'BPC-157',
            'category': 'Weefselherstel-peptide',
            'related': ['tb-500', 'ghk-cu'],
            'overview': "BPC-157 is een fragment van 15 aminozuren van een groter eiwit dat voorkomt in menselijk maagsap — de eigen beschermingsverbinding van het lichaam, vandaar de naam. Het laboratorium van Predrag Sikiric aan de Universiteit van Zagreb isoleerde en karakteriseerde het voor het eerst in het begin van de jaren '90, aanvankelijk als maagbeschermer. Wat niemand verwachtte, was hoe breed het zou werken in andere weefsels. Tegen het begin van de jaren 2000 toonden dierstudies aan dat BPC-157 de genezing versnelde in pezen, ligamenten, spieren, hersenen, bloedvaten — bijna elk weefsel dat je testte. Dat is een verdacht klinkend profiel (verbindingen die overal werken, werken meestal nergens), maar de consistentie van de knaagdiergegevens is werkelijk opvallend, en Sikiric heeft nu meer dan 200 artikelen erover gepubliceerd.",
            'mechanism': "Het mechanisme is complex omdat BPC-157 verschillende dingen tegelijk lijkt te doen. Het reguleert VEGF op en bevordert angiogenese (vorming van nieuwe bloedvaten op letselplaatsen), wat waarschijnlijk een groot deel van het genezende effect verklaart. Verhoogt de stikstofmonoxide synthese. Moduleert de dopamine- en serotoninesystemen via de darm-hersenas (Sikiric's belangrijkste theoretische kader). Werkt in op groeihormoonreceptor expressie. Eerlijke samenvatting: niemand heeft één primair mechanisme vastgesteld, en dat maakt sommige onderzoekers ongemakkelijk.",
            'evidence': "Hier moet je voorzichtig zijn. Het dierbewijs is werkelijk indrukwekkend — Krivic et al. (2008) toonde versnelde achillespees-reparatie bij ratten aan, Cerovecki et al. (2010) toonde snellere mediale collaterale ligament-genezing aan. De clou: vanaf 2026 zijn er geen geregistreerde gerandomiseerde menselijke klinische studies. De atletische herstelgemeenschap voert al meer dan 15 jaar effectief een gigantisch ongecontroleerd experiment uit met anekdotes variërend van wonderbaarlijk tot geen effect, maar dat is niet hetzelfde als RCT-bewijs.",
            'dosing': "Typische onderzoeksprotocollen gebruiken 200-500 mcg per dag subcutaan, vaak verdeeld over twee doses. Veel gebruikers injecteren dicht bij de letselplaats vanuit de theorie dat lokale concentratie helpt — dit is aannemelijk maar niet echt bewezen. Orale protocollen (250-500 mcg, 1-2x per dag) worden ook bestudeerd; BPC-157 is ongewoon stabiel in maagzuur. Acute blessures beginnen vaak met hogere oplaaddoses (500 mcg tweemaal daags) gedurende 4-8 weken.",
            'safety': "Het veiligheidsprofiel in dierstudies is uitstekend — extreem hoge LD50 (>10g/kg), geen acute toxiciteitsincidenten. Langetermijngegevens bij mensen bestaan ​​simpelweg niet. Gerapporteerde milde bijwerkingen vallen vooral op door hun onopvallendheid: incidentele reacties op de injectieplaats (~10-15% van de gebruikers), voorbijgaande vermoeidheid in de eerste week, milde misselijkheid bij orale protocollen. Niet goedgekeurd door FDA. Opvallend: WADA heeft het niet verboden (vanaf 2026), in tegenstelling tot TB-500.",
            'quick_answer': "BPC-157 is een 15-aminozuur peptide afkomstig van menselijk maagsap, sinds begin jaren '90 bestudeerd door Sikiric's lab in Zagreb voor weefselherstel-effecten. Het dierbewijs over pezen, ligamenten, spieren en darm-genezing is consistent en indrukwekkend — de clou is dat er geen geregistreerde menselijke studies zijn. Typische protocollen: 200-500 mcg/dag subcutaan gedurende 4-8 weken. Mechanisme is multi-route. Vaak gecombineerd met TB-500 voor blessurewerk. Niet FDA-goedgekeurd.",
        },
        'id': {
            'name': 'BPC-157',
            'category': 'Peptida perbaikan jaringan',
            'related': ['tb-500', 'ghk-cu'],
            'overview': 'BPC-157 adalah fragmen 15-asam amino dari protein yang lebih besar yang ditemukan dalam sari lambung manusia — senyawa perlindungan tubuh sendiri, oleh karena itu namanya. Laboratorium Predrag Sikiric di Universitas Zagreb pertama kali mengisolasi dan mengkarakterisasinya pada awal 1990-an, awalnya sebagai pelindung lambung. Apa yang tidak diduga siapa pun adalah seberapa luas ia akan bekerja di jaringan lain. Pada awal tahun 2000-an, penelitian hewan menunjukkan BPC-157 mempercepat penyembuhan tendon, ligamen, otot, otak, pembuluh darah — hampir setiap jaringan yang Anda uji. Itu adalah profil yang mencurigakan (senyawa yang bekerja pada semua hal biasanya tidak bekerja pada apa pun), tetapi konsistensi data hewan pengerat sangat mencolok, dan Sikiric sekarang telah menerbitkan lebih dari 200 makalah tentang hal itu.',
            'mechanism': 'Mekanismenya rumit karena BPC-157 tampaknya melakukan beberapa hal sekaligus. Ini meningkatkan regulasi VEGF dan mempromosikan angiogenesis (pembentukan pembuluh darah baru di lokasi cedera), yang mungkin menjelaskan sebagian besar efek penyembuhan. Meningkatkan sintesis nitrit oksida. Memodulasi sistem dopamin dan serotonin melalui sumbu usus-otak (kerangka teori utama Sikiric). Berinteraksi dengan ekspresi reseptor hormon pertumbuhan.',
            'evidence': 'Di sini Anda harus berhati-hati. Bukti hewan benar-benar mengesankan — Krivic et al. (2008) menunjukkan perbaikan tendon Achilles yang dipercepat pada tikus, Cerovecki et al. (2010) menunjukkan penyembuhan ligamen kolateral medial yang lebih cepat. Tangkapan: pada tahun 2026, tidak ada uji klinis manusia teracak yang terdaftar. Komunitas pemulihan atletik secara efektif telah menjalankan eksperimen tidak terkontrol raksasa selama 15+ tahun dengan anekdot mulai dari ajaib hingga tidak ada efek.',
            'dosing': 'Protokol penelitian khas menggunakan 200-500 mcg setiap hari secara subkutan, sering dibagi menjadi dua dosis. Banyak pengguna menyuntikkan dekat dengan lokasi cedera berdasarkan teori bahwa konsentrasi lokal membantu — ini masuk akal tetapi sebenarnya tidak terbukti. Protokol oral (250-500 mcg, 1-2x sehari) juga dipelajari; BPC-157 luar biasa stabil dalam asam lambung. Cedera akut sering dimulai dengan dosis pemuatan yang lebih tinggi (500 mcg dua kali sehari) selama 4-8 minggu.',
            'safety': 'Profil keamanan dalam studi hewan sangat baik — LD50 sangat tinggi (>10g/kg), tidak ada peristiwa toksisitas akut. Data manusia jangka panjang tidak ada. Efek samping ringan yang dilaporkan terutama menonjol karena tidak menonjol: reaksi sesekali di tempat suntikan (~10-15% pengguna), kelelahan transien di minggu pertama, mual ringan pada protokol oral. Tidak disetujui oleh FDA. WADA belum melarangnya (per 2026), tidak seperti TB-500.',
            'quick_answer': 'BPC-157 adalah peptida 15-asam amino yang berasal dari sari lambung manusia, dipelajari sejak awal 1990-an oleh laboratorium Sikiric di Zagreb untuk efek perbaikan jaringan. Bukti hewan tentang tendon, ligamen, otot, dan penyembuhan usus konsisten dan mengesankan — tangkapannya adalah tidak ada uji klinis manusia yang terdaftar. Protokol khas: 200-500 mcg/hari subkutan selama 4-8 minggu. Mekanisme multi-jalur. Sering dipadukan dengan TB-500 untuk pekerjaan cedera. Tidak disetujui oleh FDA.',
        },
    },
    'tb-500': {
        'ru': {
            'name': 'TB-500',
            'category': 'Пептид восстановления тканей',
            'related': ['bpc-157', 'ghk-cu'],
            'overview': 'TB-500 не является целостной молекулой — это 17-аминокислотный фрагмент тимозина бета-4 (Tβ4), одного из самых распространенных внутриклеточных белков в организме. Большая часть первоначального интереса возникла из ветеринарной медицины 1990-х годов, где TB-500 использовался для ускорения восстановления сухожилий и мягких тканей у скаковых лошадей. RegeneRx (теперь G-treeBNT) разработал несколько клинических кандидатов. Сообщество атлетического восстановления рассматривает TB-500 и BPC-157 как стандартную пару для травм.',
            'mechanism': 'Главная биологическая функция тимозина бета-4 — секвестрация мономеров G-актина — в основном контролирует движение клеток во время восстановления. Эта роль миграции клеток делает TB-500 интересным для заживления. Помимо этого, способствует ангиогенезу, ослабляет воспалительные цитокины (TNF-α, IL-6, IL-1β) и защищает кардиомиоциты от ишемических повреждений через путь выживания Akt. Статья Bock-Marquette et al. (Nature 2004) о защите сердца, вероятно, является наиболее цитируемым механистическим исследованием.',
            'evidence': 'Исследования на животных широкие и последовательные: ишемия-реперфузия сердца (статья Nature), заживление ран (Malinda et al. 1999), восстановление роговицы, регенерация нервов. RegeneRx провел несколько клинических испытаний II фазы у людей. Самый ясный регуляторный сигнал: WADA запретил TB-500 в 2011 году как вещество S2 (факторы роста). Для соревнующихся спортсменов это не теоретическая проблема.',
            'dosing': 'Стандартные исследовательские протоколы — 2-5 мг в неделю подкожно, разделенные на две дозы. Острые фазы травм часто используют подход "нагрузочной дозы" — 2-2,5 мг ежедневно в первую неделю, затем 4-6 недель в нагрузочной дозе, снижение до 2 мг/неделю для поддерживающего. Период полураспада действительно дни (а не часы для BPC-157). Объединенный протокол "BPC + TB" — наиболее распространенная исследовательская конфигурация.',
            'safety': 'Данные о безопасности у людей ограничены, но клинические испытания RegeneRx не выявили серьезных проблем. Теоретическая проблема та же, что и с BPC-157, только громче: ангиогенез и миграция клеток — именно то, что нужно опухолям. История рака — исключение в большинстве исследований. Сообщаемые побочные эффекты в основном скучные — реакции в месте инъекции, переходная усталость. Запрет WADA означает, что соревнующиеся спортсмены сталкиваются с реальными последствиями за использование.',
            'quick_answer': 'TB-500 — это 17-аминокислотный фрагмент тимозина бета-4, изначально использовавшийся в ветеринарной медицине для восстановления сухожилий скаковых лошадей. Механизм многосторонний: связывание актина для миграции клеток, плюс ангиогенез и противовоспалительные эффекты. Bock-Marquette et al. 2004 (Nature) о защите сердца — основополагающая механистическая статья. Стандартный протокол: 2-5 мг/неделю подкожно. Запрещен WADA с 2011 года. Не одобрен FDA.',
        },
        'pl': {
            'name': 'TB-500',
            'category': 'Peptyd naprawy tkanek',
            'related': ['bpc-157', 'ghk-cu'],
            'overview': "TB-500 nie jest tak naprawdę kompletną cząsteczką — to 17-aminokwasowy fragment tymozyny beta-4 (Tβ4), jednego z najbardziej obfitych białek wewnątrzkomórkowych w organizmie. Większość pierwotnego zainteresowania pochodziła z weterynarii lat 90-tych, gdzie TB-500 był używany do przyspieszania regeneracji ścięgien i tkanek miękkich u koni wyścigowych. RegeneRx (obecnie G-treeBNT) opracował kilku kandydatów klinicznych. Społeczność rekonwalescencji sportowej traktuje TB-500 i BPC-157 jako domyślną parę przy urazach.",
            'mechanism': 'Główną biologiczną pracą tymozyny beta-4 jest sekwestracja monomerów G-aktyny — w zasadzie kontroluje, jak komórki się przemieszczają podczas naprawy. Ta rola migracji komórkowej czyni TB-500 interesującym dla gojenia. Poza tym, promuje angiogenezę, tłumi cytokiny zapalne (TNF-α, IL-6, IL-1β) i chroni kardiomiocyty przed uszkodzeniami niedokrwiennymi przez szlak przeżycia Akt. Artykuł Bock-Marquette et al. (Nature 2004) o ochronie serca jest prawdopodobnie najczęściej cytowanym badaniem mechanistycznym.',
            'evidence': 'Dowody na zwierzętach są szerokie i spójne: niedokrwienie-reperfuzja serca (artykuł Nature), gojenie ran (Malinda et al. 1999). RegeneRx przeprowadziło wiele prób II fazy u ludzi. Najjaśniejszy sygnał regulacyjny: WADA zakazała TB-500 w 2011 roku jako substancję S2 (czynniki wzrostu). Dla sportowców wyczynowych to nie jest teoretyczna obawa.',
            'dosing': 'Standardowe protokoły badawcze to 2-5 mg tygodniowo podskórnie, podzielone na dwie dawki. Ostre fazy urazów często używają podejścia "dawki nasycającej" — 2-2,5 mg dziennie w pierwszym tygodniu, następnie 4-6 tygodni przy dawce nasycającej, spadek do 2 mg/tydzień jako podtrzymanie. Połączony protokół "BPC + TB" jest najbardziej powszechną konfiguracją badawczą.',
            'safety': 'Dane o bezpieczeństwie u ludzi są ograniczone, ale próby kliniczne RegeneRx nie wykryły poważnych problemów. Obawa teoretyczna jest taka sama jak przy BPC-157, tylko głośniejsza: angiogeneza i migracja komórek to dokładnie to, czego potrzebują guzy. Historia nowotworu — wykluczenie w większości badań. Zakaz WADA oznacza, że sportowcy wyczynowi stoją w obliczu prawdziwych konsekwencji za używanie.',
            'quick_answer': 'TB-500 to 17-aminokwasowy fragment tymozyny beta-4, pierwotnie używany w weterynarii do regeneracji ścięgien koni wyścigowych. Mechanizm wielofrontowy: sekwestracja aktyny napędza migrację komórek, plus angiogeneza i efekty przeciwzapalne. Bock-Marquette et al. 2004 (Nature) o ochronie serca to fundamentalny artykuł mechanistyczny. Standardowy protokół: 2-5 mg/tydzień podskórnie. Zakazany przez WADA od 2011 roku. Niezatwierdzony przez FDA.',
        },
        'nl': {
            'name': 'TB-500',
            'category': 'Weefselherstel-peptide',
            'related': ['bpc-157', 'ghk-cu'],
            'overview': "TB-500 is niet echt een complete molecule — het is een 17-aminozuur fragment van thymosine bèta-4 (Tβ4), een van de meest voorkomende intracellulaire eiwitten in het lichaam. Het meeste oorspronkelijke belang kwam uit de veterinaire geneeskunde van de jaren '90, waar TB-500 werd gebruikt om herstel van pezen en zachte weefsels bij racepaarden te versnellen. RegeneRx (nu G-treeBNT) ontwikkelde verschillende klinische kandidaten. De atletische herstelgemeenschap behandelt TB-500 en BPC-157 als een standaardpaar voor blessures.",
            'mechanism': "De primaire biologische functie van thymosine bèta-4 is het sequestreren van G-actine monomeren — in feite controleert het hoe cellen rondkruipen tijdens reparatie. Die celmigratierol maakt TB-500 interessant voor genezing. Bevordert daarnaast angiogenese, dempt ontstekingscytokines (TNF-α, IL-6, IL-1β) en beschermt cardiomyocyten tegen ischemische schade via de Akt-overlevingsroute. Het Bock-Marquette et al. (Nature 2004) artikel over hartbescherming is waarschijnlijk de meest geciteerde mechanistische studie.",
            'evidence': "Dierbewijs is breed en consistent: hartische ischemie-reperfusie (het Nature artikel), wondgenezing (Malinda et al. 1999). RegeneRx voerde meerdere Fase II-onderzoeken bij mensen uit. Het duidelijkste reguleringssignaal: WADA verbood TB-500 in 2011 als een S2-stof (groeifactoren). Voor competitieve atleten is dat geen theoretische zorg.",
            'dosing': "Standaard onderzoeksprotocollen zijn 2-5 mg per week subcutaan, verdeeld over twee doses. Acute blessurefasen gebruiken vaak een 'oplaaddosis'-aanpak — 2-2,5 mg per dag in de eerste week, vervolgens 4-6 weken bij de oplaaddosis, dalend naar 2 mg/week voor onderhoud. Het gecombineerde 'BPC + TB' protocol is de meest voorkomende onderzoeksconfiguratie.",
            'safety': "Menselijke veiligheidsgegevens zijn beperkt, maar de klinische onderzoeken van RegeneRx hebben geen grote problemen aan het licht gebracht. De theoretische zorg is dezelfde als met BPC-157, alleen luider: angiogenese en celmigratie zijn precies wat tumoren nodig hebben. Kankergeschiedenis is een uitsluiting in de meeste onderzoeken. Het WADA-verbod betekent dat competitieve atleten echte consequenties ondervinden voor gebruik.",
            'quick_answer': "TB-500 is een 17-aminozuur fragment van thymosine bèta-4, oorspronkelijk gebruikt in de veterinaire geneeskunde voor herstel van pezen bij racepaarden. Mechanisme is multi-front: actine sequestratie drijft celmigratie aan, plus angiogenese en ontstekingsremmende effecten. Bock-Marquette et al. 2004 (Nature) over hartbescherming is het fundamentele mechanistische artikel. Standaardprotocol: 2-5 mg/week subcutaan. WADA-verboden sinds 2011. Niet FDA-goedgekeurd.",
        },
        'id': {
            'name': 'TB-500',
            'category': 'Peptida perbaikan jaringan',
            'related': ['bpc-157', 'ghk-cu'],
            'overview': 'TB-500 sebenarnya bukan molekul lengkap — ini adalah fragmen 17-asam amino dari thymosin beta-4 (Tβ4), salah satu protein intraseluler paling melimpah di tubuh. Sebagian besar minat asli datang dari kedokteran hewan pada 1990-an, di mana TB-500 digunakan untuk mempercepat pemulihan tendon dan jaringan lunak pada kuda balap. RegeneRx (sekarang G-treeBNT) mengembangkan beberapa kandidat klinis. Komunitas pemulihan atletik memperlakukan TB-500 dan BPC-157 sebagai pasangan default untuk cedera.',
            'mechanism': 'Pekerjaan biologis utama thymosin beta-4 adalah mengasingkan monomer G-aktin — pada dasarnya, mengontrol bagaimana sel bergerak selama perbaikan. Peran migrasi sel itu yang membuat TB-500 menarik untuk penyembuhan. Selain itu, ia mempromosikan angiogenesis, menekan sitokin inflamasi (TNF-α, IL-6, IL-1β), dan melindungi kardiomiosit dari kerusakan iskemik melalui jalur kelangsungan Akt. Makalah Bock-Marquette et al. (Nature 2004) tentang perlindungan jantung mungkin merupakan studi mekanistik yang paling banyak dikutip.',
            'evidence': 'Bukti hewan luas dan konsisten: iskemia-reperfusi jantung (makalah Nature), penyembuhan luka (Malinda et al. 1999). RegeneRx melakukan beberapa uji Fase II pada manusia. Sinyal regulasi yang paling jelas: WADA melarang TB-500 pada 2011 sebagai substansi S2 (faktor pertumbuhan). Untuk atlet kompetitif, itu bukan kekhawatiran teoritis.',
            'dosing': 'Protokol penelitian standar adalah 2-5 mg per minggu secara subkutan, dibagi menjadi dua dosis. Fase cedera akut sering menggunakan pendekatan "dosis pemuatan" — 2-2,5 mg setiap hari pada minggu pertama, kemudian 4-6 minggu pada dosis pemuatan, turun menjadi 2 mg/minggu untuk pemeliharaan. Protokol gabungan "BPC + TB" adalah konfigurasi penelitian yang paling umum.',
            'safety': 'Data keamanan manusia terbatas tetapi uji klinis RegeneRx tidak menemukan masalah besar. Kekhawatiran teoritis sama dengan BPC-157, hanya lebih keras: angiogenesis dan migrasi sel persis apa yang dibutuhkan tumor. Riwayat kanker adalah pengecualian dalam sebagian besar penelitian. Larangan WADA berarti atlet kompetitif menghadapi konsekuensi nyata untuk penggunaan.',
            'quick_answer': 'TB-500 adalah fragmen 17-asam amino dari thymosin beta-4, awalnya digunakan dalam kedokteran hewan untuk pemulihan tendon kuda balap. Mekanisme multi-depan: pengasingan aktin mendorong migrasi sel, ditambah angiogenesis dan efek anti-inflamasi. Bock-Marquette et al. 2004 (Nature) tentang perlindungan jantung adalah makalah mekanistik fundamental. Protokol standar: 2-5 mg/minggu subkutan. Dilarang WADA sejak 2011. Tidak disetujui FDA.',
        },
    },
    'semaglutide': {
        'ru': {
            'name': 'Семаглутид',
            'category': 'Агонист рецептора GLP-1 (одобрен FDA)',
            'related': ['tirzepatide', 'retatrutide'],
            'overview': 'Семаглутид — молекула, которая взломала рынок препаратов для лечения ожирения. Novo Nordisk разработала его как агонист рецептора GLP-1 длительного действия для диабета 2 типа — продается под маркой Ozempic для диабета и Wegovy для ожирения, с пероральной версией под названием Rybelsus. Структурно это пептид из 31 аминокислоты, основанный на гормоне GLP-1(7-37). Боковая цепь жирной кислоты C18 позволяет ему связываться с альбумином в крови, продлевая период полураспада с минут до примерно 7 дней — почему семаглутид работает как еженедельная инъекция.',
            'mechanism': 'Семаглутид связывается с рецептором GLP-1 (GLP-1R), активируя путь cAMP/PKA. Это запускает несколько эффектов параллельно: глюкозозависимую секрецию инсулина (только когда уровень сахара в крови действительно повышен, поэтому гипогликемия редка), подавление высвобождения глюкагона, замедленное опорожнение желудка, и прямую активацию POMC/CART-нейронов в гипоталамусе, которые обеспечивают чувство насыщения.',
            'evidence': 'STEP 1 (NEJM 2021) — главное испытание: 2,4 мг семаглутида еженедельно в течение 68 недель, средняя потеря веса 14,9% у пациентов с ожирением без диабета по сравнению с 2,4% на плацебо. Это другая лига по сравнению с предыдущими препаратами для лечения ожирения. SELECT (NEJM 2023) показал снижение MACE на 20% (основные неблагоприятные сердечно-сосудистые события) у пациентов с ожирением без диабета.',
            'dosing': 'Дозировка для диабета начинается с 0,25 мг еженедельно и титруется каждые 4 недели: 0,5 → 1,0 → максимум 2,0 мг. Дозировка для ожирения идет выше: 0,25 → 0,5 → 1,0 → 1,7 → максимум 2,4 мг. Медленное титрование действительно важно для переносимости — быстрое титрование сильно увеличивает частоту тошноты.',
            'safety': 'Побочные эффекты доминируются ЖКТ: тошнота (44,2% в STEP 1), рвота (24,8%), диарея (31,5%), запор (24,2%). Реальные, но редкие риски: острый панкреатит (0,1-0,3%), события желчного пузыря (камни, холецистит, 2-3% при длительном использовании), ухудшение диабетической ретинопатии. Предупреждение FDA в черной рамке для медуллярной карциномы щитовидной железы основано на исследованиях у грызунов; семейный анамнез синдрома MEN2 — абсолютное противопоказание.',
            'quick_answer': 'Семаглутид (Ozempic/Wegovy/Rybelsus) — агонист рецептора GLP-1 длительного действия от Novo Nordisk, который эффективно сбросил ожидания для препаратов от ожирения. STEP 1 (2021) показал 14,9% потери веса за 68 недель — намного превосходит любую предыдущую медикаментозную терапию ожирения. SELECT (2023) добавил снижение сердечно-сосудистых событий на 20%. Период полураспада ~7 дней, еженедельная инъекция. Побочные эффекты доминируются ЖКТ; предупреждение в черной рамке для медуллярной карциномы щитовидной железы.',
        },
        'pl': {
            'name': 'Semaglutyd',
            'category': 'Agonist receptora GLP-1 (zatwierdzony przez FDA)',
            'related': ['tirzepatide', 'retatrutide'],
            'overview': 'Semaglutyd to cząsteczka, która zrewolucjonizowała rynek leków przeciw otyłości. Novo Nordisk opracowało go jako długodziałającego agonistę receptora GLP-1 dla cukrzycy typu 2 — sprzedawany jako Ozempic dla cukrzycy i Wegovy dla otyłości, z wersją doustną Rybelsus. Strukturalnie jest to peptyd 31-aminokwasowy oparty na naturalnym hormonie GLP-1(7-37), z boczną łańcuchem kwasu tłuszczowego (C18), który pozwala mu wiązać się z albuminą we krwi.',
            'mechanism': 'Semaglutyd wiąże się z receptorem GLP-1 (GLP-1R), aktywuje szlak cAMP/PKA, wywołując kilka efektów równolegle: glukozozależne wydzielanie insuliny (tylko gdy poziom cukru we krwi jest faktycznie podniesiony), tłumienie uwalniania glukagonu, spowolnione opróżnianie żołądka oraz bezpośrednią aktywację neuronów POMC/CART w jądrze łukowatym podwzgórza, które napędzają sytość.',
            'evidence': 'STEP 1 (NEJM 2021) to przełomowa próba: 2,4 mg semaglutydu tygodniowo przez 68 tygodni, średnia utrata wagi 14,9% u niediabetycznych pacjentów otyłych w porównaniu z 2,4% na placebo. To zupełnie inna liga niż poprzednie leki przeciw otyłości. SELECT (NEJM 2023) pokazał zmniejszenie MACE o 20% u otyłych niediabetyków z chorobą sercowo-naczyniową.',
            'dosing': 'Dawkowanie cukrzycowe zaczyna się od 0,25 mg tygodniowo i titruje co 4 tygodnie: 0,5 → 1,0 → maksymalnie 2,0 mg. Dawkowanie otyłościowe idzie wyżej: 0,25 → 0,5 → 1,0 → 1,7 → maksymalnie 2,4 mg. Powolne titracja jest naprawdę ważne dla tolerancji.',
            'safety': 'Skutki uboczne są zdominowane przez przewód pokarmowy: nudności (44,2% w STEP 1), wymioty (24,8%), biegunka (31,5%), zaparcia (24,2%). Realne, ale rzadkie ryzyka: ostre zapalenie trzustki, problemy z pęcherzykiem żółciowym, pogorszenie retinopatii cukrzycowej. Ostrzeżenie FDA w czarnej ramce dotyczy raka rdzeniastego tarczycy w oparciu o badania na gryzoniach.',
            'quick_answer': 'Semaglutyd (Ozempic/Wegovy/Rybelsus) to długodziałający agonista receptora GLP-1 firmy Novo Nordisk. STEP 1 (2021) pokazał 14,9% utraty wagi w 68 tygodni. SELECT (2023) dodał 20% redukcję zdarzeń sercowo-naczyniowych. Okres półtrwania ~7 dni, cotygodniowy zastrzyk. Skutki uboczne dominują przewód pokarmowy.',
        },
        'nl': {
            'name': 'Semaglutide',
            'category': 'GLP-1 receptor agonist (FDA-goedgekeurd)',
            'related': ['tirzepatide', 'retatrutide'],
            'overview': "Semaglutide is de molecule die de markt voor obesitasmiddelen heeft veranderd. Novo Nordisk ontwikkelde het als langwerkende GLP-1 receptor agonist voor type 2 diabetes — verkocht als Ozempic voor diabetes en Wegovy voor obesitas, met een orale versie genaamd Rybelsus. Structureel is het een peptide van 31 aminozuren gebaseerd op het natuurlijke GLP-1(7-37) hormoon, met een vetzuurzijketen (C18) die het in staat stelt zich te binden aan albumine in het bloed.",
            'mechanism': "Semaglutide bindt zich aan de GLP-1 receptor (GLP-1R), activeert het cAMP/PKA-pad en triggert meerdere effecten parallel: glucose-afhankelijke insulinesecretie (alleen wanneer de bloedsuiker daadwerkelijk verhoogd is, daarom is hypoglykemie zeldzaam), onderdrukking van glucagonafgifte, vertraagde maagontlediging en directe activering van POMC/CART neuronen in de hypothalamische arcuate kern die verzadiging aandrijven.",
            'evidence': "STEP 1 (NEJM 2021) is de hoofdstudie: 2,4 mg semaglutide wekelijks gedurende 68 weken, gemiddeld 14,9% gewichtsverlies bij niet-diabetische obese patiënten versus 2,4% bij placebo. Dat is een heel andere liga dan eerdere obesitasmiddelen. SELECT (NEJM 2023) toonde 20% reductie in MACE bij obese niet-diabetische patiënten met hart- en vaatziekten.",
            'dosing': "Diabetesdosering begint bij 0,25 mg wekelijks en titreert elke 4 weken: 0,5 → 1,0 → maximaal 2,0 mg. Obesitasdosering gaat hoger: 0,25 → 0,5 → 1,0 → 1,7 → maximaal 2,4 mg. Langzame titratie is werkelijk belangrijk voor verdraagbaarheid — snelle titratie verhoogt het misselijkheidspercentage aanzienlijk.",
            'safety': "Bijwerkingen worden gedomineerd door GI: misselijkheid (44,2% in STEP 1), braken (24,8%), diarree (31,5%), constipatie (24,2%). Werkelijke maar zeldzame risico's: acute pancreatitis, galblaasevenementen, verergering van diabetische retinopathie. De FDA black box-waarschuwing is voor medullair schildkliercarcinoom op basis van knaagdierstudies; familiegeschiedenis van MEN2-syndroom is een absolute contra-indicatie.",
            'quick_answer': "Semaglutide (Ozempic/Wegovy/Rybelsus) is Novo Nordisks langwerkende GLP-1 receptor agonist die effectief de verwachtingen voor obesitasmiddelen heeft gereset. STEP 1 (2021) toonde 14,9% gewichtsverlies in 68 weken. SELECT (2023) voegde 20% reductie van cardiovasculaire gebeurtenissen toe. Halfwaardetijd ~7 dagen, wekelijkse injectie. Bijwerkingen gedomineerd door GI.",
        },
        'id': {
            'name': 'Semaglutide',
            'category': 'Agonis reseptor GLP-1 (disetujui FDA)',
            'related': ['tirzepatide', 'retatrutide'],
            'overview': 'Semaglutide adalah molekul yang merevolusi pasar obat-obatan obesitas. Novo Nordisk mengembangkannya sebagai agonis reseptor GLP-1 yang bekerja lama untuk diabetes tipe 2 — dipasarkan sebagai Ozempic untuk diabetes dan Wegovy untuk obesitas, dengan versi oral bernama Rybelsus. Secara struktural adalah peptida 31-asam amino berdasarkan hormon GLP-1(7-37) alami, dengan rantai samping asam lemak (C18) yang memungkinkannya berikatan dengan albumin dalam darah.',
            'mechanism': 'Semaglutide berikatan dengan reseptor GLP-1 (GLP-1R), mengaktifkan jalur cAMP/PKA hilir, memicu beberapa efek secara paralel: sekresi insulin yang bergantung glukosa (hanya ketika gula darah benar-benar meningkat, karenanya hipoglikemia jarang terjadi), penekanan pelepasan glukagon, pengosongan lambung yang melambat, dan aktivasi langsung neuron POMC/CART di nukleus arkuata hipotalamus yang mendorong rasa kenyang.',
            'evidence': 'STEP 1 (NEJM 2021) adalah uji coba utama: 2,4 mg semaglutide mingguan selama 68 minggu, rata-rata penurunan berat badan 14,9% pada pasien obesitas non-diabetes vs 2,4% pada plasebo. Itu liga yang sama sekali berbeda dari obat obesitas sebelumnya. SELECT (NEJM 2023) menunjukkan pengurangan MACE 20% pada pasien obesitas non-diabetes dengan penyakit kardiovaskular.',
            'dosing': 'Dosis diabetes dimulai pada 0,25 mg mingguan dan dititrasi setiap 4 minggu: 0,5 → 1,0 → maksimum 2,0 mg. Dosis obesitas naik lebih tinggi: 0,25 → 0,5 → 1,0 → 1,7 → maksimum 2,4 mg. Titrasi lambat benar-benar penting untuk toleransi.',
            'safety': 'Efek samping didominasi GI: mual (44,2% di STEP 1), muntah (24,8%), diare (31,5%), konstipasi (24,2%). Risiko nyata tetapi jarang: pankreatitis akut, peristiwa kandung empedu, perburukan retinopati diabetik. Peringatan kotak hitam FDA adalah untuk karsinoma tiroid medullary berdasarkan studi hewan pengerat.',
            'quick_answer': 'Semaglutide (Ozempic/Wegovy/Rybelsus) adalah agonis reseptor GLP-1 jangka panjang dari Novo Nordisk yang secara efektif mereset ekspektasi untuk obat-obatan obesitas. STEP 1 (2021) menunjukkan penurunan berat badan 14,9% dalam 68 minggu. SELECT (2023) menambahkan pengurangan kejadian kardiovaskular 20%. Waktu paruh ~7 hari, injeksi mingguan.',
        },
    },
}


def aspect_paragraphs(angle, c, lang):
    """Build aspect-specific paragraphs from compound data."""
    name = c['name']
    if angle == 'guide' or angle == 'general' or angle == 'comprehensive':
        h2_map = {
            'ru': ['Что такое', 'Механизм действия', 'Доказательная база', 'Дозирование и применение', 'Профиль безопасности'],
            'pl': ['Czym jest', 'Mechanizm działania', 'Baza dowodowa', 'Dawkowanie i podawanie', 'Profil bezpieczeństwa'],
            'nl': ['Wat is', 'Werkingsmechanisme', 'Bewijsbasis', 'Dosering en toediening', 'Veiligheidsprofiel'],
            'id': ['Apa itu', 'Mekanisme kerja', 'Basis bukti', 'Dosis dan administrasi', 'Profil keamanan'],
        }
        h2s = h2_map[lang]
        return [
            (f'{h2s[0]} {name}?' if lang in ('ru', 'pl', 'nl', 'id') else h2s[0], c['overview']),
            (h2s[1], c['mechanism']),
            (h2s[2], c['evidence']),
            (h2s[3], c['dosing']),
            (h2s[4], c['safety']),
        ]
    if angle == 'faq':
        # Simple FAQ structure
        if lang == 'ru':
            return [
                (f'Что такое {name}?', c['overview']),
                ('Как работает?', c['mechanism']),
                ('Каковы дозы исследования?', c['dosing']),
                ('Каковы соображения безопасности?', c['safety']),
                ('Какова доказательная база?', c['evidence']),
            ]
        if lang == 'pl':
            return [
                (f'Czym jest {name}?', c['overview']),
                ('Jak działa?', c['mechanism']),
                ('Jakie są dawki badawcze?', c['dosing']),
                ('Jakie są kwestie bezpieczeństwa?', c['safety']),
                ('Jak silna jest baza dowodowa?', c['evidence']),
            ]
        if lang == 'nl':
            return [
                (f'Wat is {name}?', c['overview']),
                ('Hoe werkt het?', c['mechanism']),
                ('Wat zijn typische onderzoeksdoseringen?', c['dosing']),
                ('Wat zijn de belangrijkste veiligheidsoverwegingen?', c['safety']),
                ('Hoe sterk is de bewijsbasis?', c['evidence']),
            ]
        if lang == 'id':
            return [
                (f'Apa itu {name}?', c['overview']),
                ('Bagaimana cara kerjanya?', c['mechanism']),
                ('Apa dosis penelitian khasnya?', c['dosing']),
                ('Apa pertimbangan keamanannya?', c['safety']),
                ('Seberapa kuat basis buktinya?', c['evidence']),
            ]
    if angle in ('safety', 'side-effects'):
        h2_map = {
            'ru': ['Профиль безопасности', 'Механизм объясняет побочные эффекты', 'Противопоказания', 'Стратегия мониторинга'],
            'pl': ['Profil bezpieczeństwa', 'Mechanizm wyjaśnia skutki uboczne', 'Przeciwwskazania', 'Strategia monitorowania'],
            'nl': ['Veiligheidsprofiel', 'Mechanisme verklaart bijwerkingen', 'Contra-indicaties', 'Monitoringstrategie'],
            'id': ['Profil keamanan', 'Mekanisme menjelaskan efek samping', 'Kontraindikasi', 'Strategi pemantauan'],
        }
        h2s = h2_map[lang]
        return [
            (h2s[0], c['safety']),
            (h2s[1], c['mechanism']),
            (h2s[2], c['evidence'][:400]),
            (h2s[3], c['dosing'][:400]),
        ]
    if angle == 'dosing':
        h2_map = {
            'ru': ['Дозирование', 'Механизм и дозирование', 'Безопасность'],
            'pl': ['Dawkowanie', 'Mechanizm a dawkowanie', 'Bezpieczeństwo'],
            'nl': ['Dosering', 'Mechanisme en dosering', 'Veiligheid'],
            'id': ['Dosis', 'Mekanisme dan dosis', 'Keamanan'],
        }
        h2s = h2_map[lang]
        return [
            (h2s[0], c['dosing']),
            (h2s[1], c['mechanism']),
            (h2s[2], c['safety']),
        ]
    if angle == 'research':
        h2_map = {
            'ru': ['Доказательная база', 'Ключевые исследования', 'Механизм', 'Безопасность'],
            'pl': ['Baza dowodowa', 'Kluczowe badania', 'Mechanizm', 'Bezpieczeństwo'],
            'nl': ['Bewijsbasis', 'Belangrijkste studies', 'Mechanisme', 'Veiligheid'],
            'id': ['Basis bukti', 'Studi utama', 'Mekanisme', 'Keamanan'],
        }
        h2s = h2_map[lang]
        return [
            (h2s[0], c['evidence']),
            (h2s[1], c['overview']),
            (h2s[2], c['mechanism']),
            (h2s[3], c['safety']),
        ]
    return [(name, c['overview']), ('Mechanism', c['mechanism'])]


QUICK_LABEL = {'ru': 'Быстрый ответ', 'pl': 'Szybka odpowiedź', 'nl': 'Snelle antwoord', 'id': 'Jawaban cepat'}
RELATED_LABEL = {'ru': 'Связанные исследовательские соединения', 'pl': 'Powiązane związki badawcze', 'nl': 'Gerelateerde onderzoeksverbindingen', 'id': 'Senyawa penelitian terkait'}
RELATED_INTRO = {'ru': 'Если вы исследуете', 'pl': 'Jeśli badasz', 'nl': 'Als u onderzoekt', 'id': 'Jika Anda meneliti'}


def build_article(slug, lang):
    parts = slug.replace('.html', '').split('-')
    compound_key = None
    aspect = 'guide'
    for ck in COMPOUNDS.keys():
        if slug.startswith(ck):
            compound_key = ck
            rem = slug.replace('.html', '')[len(ck):].lstrip('-')
            if rem == 'guide' or rem == '':
                aspect = 'guide'
            elif rem == 'faq':
                aspect = 'faq'
            elif rem == 'dosage':
                aspect = 'dosing'
            elif rem == 'safety' or rem == 'side-effects':
                aspect = 'safety'
            elif rem == 'research' or rem == 'reviews':
                aspect = 'research'
            else:
                return None, None
            break
    if not compound_key:
        return None, None
    c = COMPOUNDS[compound_key].get(lang)
    if not c:
        return None, None

    paragraphs = aspect_paragraphs(aspect, c, lang)
    quick = c.get('quick_answer', c['overview'][:300])

    html = '<article class="article-body">'
    html += f'<div class="quick-answer"><strong>{QUICK_LABEL[lang]}:</strong> {quick}</div>'
    for h2, p in paragraphs:
        html += f'<h2>{h2}</h2>\n<p>{p}</p>\n'
    related = c.get('related', [])
    if related:
        html += f'<h2>{RELATED_LABEL[lang]}</h2>\n<p>{RELATED_INTRO[lang]} {c["name"]}: '
        link_parts = []
        for rk in related[:4]:
            rc = COMPOUNDS.get(rk, {}).get(lang)
            rname = rc['name'] if rc else rk.replace('-', ' ').upper()
            link_parts.append(f'<a href="/{lang}/{rk}-guide.html">{rname}</a>')
        html += ', '.join(link_parts) + '.</p>'
    html += '</article>'

    # FAQ schema
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": h2,
             "acceptedAnswer": {"@type": "Answer", "text": p[:500]}}
            for h2, p in paragraphs[:5]
        ]
    }
    return html, faq


def process_file(path, lang):
    html = path.read_text(encoding='utf-8', errors='ignore')
    new_article, faq = build_article(path.stem, lang)
    if new_article is None:
        return False
    pat_a = re.compile(r'(<article[^>]*>)(.*?)(</article>)', re.DOTALL)
    if not pat_a.search(html):
        return False
    new_html = pat_a.sub(lambda _: new_article, html, count=1)
    if faq and 'FAQPage' not in new_html:
        s = f'<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>'
        new_html = new_html.replace('</head>', s + '\n</head>', 1)
    if new_html == html:
        return False
    path.write_text(new_html, encoding='utf-8')
    return True


def main():
    grand = 0
    for lang in LANGUAGES:
        d = ROOT / lang
        if not d.is_dir():
            continue
        targets = []
        for ck in COMPOUNDS.keys():
            for aspect in ['guide', 'faq', 'dosage', 'safety', 'research']:
                if aspect == 'guide':
                    targets.append(f'{ck}-guide.html')
                else:
                    targets.append(f'{ck}-{aspect}.html')
        fixed = 0
        for t in targets:
            path = d / t
            if not path.exists():
                continue
            try:
                if process_file(path, lang):
                    fixed += 1
            except Exception as e:
                print(f"ERR {lang}/{t}: {e}", file=sys.stderr)
        print(f"{lang}: {fixed}/{len(targets)} cornerstone files replaced")
        grand += fixed
    print(f"\n=== Phase 12 grand total: {grand} ===")


if __name__ == '__main__':
    main()
