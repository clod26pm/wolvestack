#!/usr/bin/env python3
"""
Phase 7: Cornerstone v2 generators for es/pt/fr.
Top non-English traffic markets get full humanized v2 content for the
8 cornerstone compounds × 5 aspect pages = ~40 cornerstone pages per language.

Architecture: shared schema, per-language compound profiles, humanized voice
adapted per-language (varied sentence rhythm, named researchers, narrative
hooks, mild stance — same principles as en_v2 but in target language).
"""
import os, re, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Languages to process
LANGUAGES = ['es', 'pt', 'fr']

# Per-language compound profiles
# Each compound has: name, category, related, overview, mechanism, evidence, dosing, safety, quick_answer
COMPOUNDS = {
    'bpc-157': {
        'es': {
            'name': 'BPC-157',
            'category': 'Péptido de reparación tisular',
            'related': ['tb-500', 'ghk-cu', 'thymosin-alpha-1'],
            'overview': "BPC-157 es un fragmento de 15 aminoácidos de una proteína más grande presente en el jugo gástrico humano — el propio compuesto protector del cuerpo, de ahí el nombre. El laboratorio de Predrag Sikiric en la Universidad de Zagreb fue el primero en aislarlo y caracterizarlo a principios de los 90, inicialmente como protector gástrico. Lo que nadie esperaba era hasta qué punto funcionaría en otros tejidos. Para principios de los 2000, los estudios animales mostraban que BPC-157 aceleraba la cicatrización en tendones, ligamentos, músculo, cerebro, vasos sanguíneos — casi cualquier tejido que se probara. Es un perfil sospechoso (los compuestos que funcionan para todo suelen no funcionar para nada), pero la consistencia de los datos en roedores es genuinamente sorprendente, y Sikiric ha publicado más de 200 artículos sobre el tema.",
            'mechanism': "El mecanismo es complejo porque BPC-157 parece hacer varias cosas a la vez. Sobreregula VEGF y promueve angiogénesis (formación de nuevos vasos sanguíneos en sitios de lesión), lo que probablemente explica gran parte del efecto cicatrizante — mejor flujo sanguíneo, mejor reparación. Aumenta la síntesis de óxido nítrico. Modula los sistemas de dopamina y serotonina vía el eje intestino-cerebro (el marco teórico principal de Sikiric). Interactúa con la expresión del receptor de hormona del crecimiento. Resumen honesto: nadie ha identificado un mecanismo primario único, y eso incomoda a algunos investigadores. La compensación es que esa misma historia multimecánica explicaría por qué un solo péptido parece ayudar con tantas lesiones diferentes.",
            'evidence': "Aquí hay que ser cuidadoso. La evidencia animal es genuinamente impresionante — Krivic et al. (2008) mostró reparación acelerada del tendón de Aquiles en ratas, Cerovecki et al. (2010) mostró cicatrización más rápida del ligamento colateral medial, y hay una larga serie de estudios de úlcera gástrica inducida por AINE mostrando 90%+ de protección mucosa. La pega: a partir de 2026, hay cero ensayos clínicos humanos aleatorizados registrados. La comunidad de recuperación atlética ha llevado a cabo efectivamente un experimento descontrolado gigante durante 15+ años con anécdotas que van desde milagrosas hasta sin efecto, pero eso no es lo mismo que evidencia RCT.",
            'dosing': "Los protocolos de investigación típicos usan 200-500 mcg al día por vía subcutánea, a menudo divididos en dos dosis. Muchos usuarios inyectan cerca del sitio de la lesión bajo la teoría de que la concentración local ayuda — esto es plausible pero no realmente comprobado. Los protocolos orales (250-500 mcg, 1-2x al día) también se estudian; BPC-157 es inusualmente estable en ácido estomacal, lo que es parte de lo que lo hace interesante. Las lesiones agudas a menudo comienzan con dosis de carga más altas (500 mcg dos veces al día) durante 4-8 semanas. La vida media es corta (unas pocas horas subcutáneo), por eso la dosificación dos veces al día es estándar.",
            'safety': "El perfil de seguridad en estudios animales es excelente — LD50 extremadamente alto (>10g/kg), sin eventos de toxicidad aguda. Los datos humanos a largo plazo simplemente no existen. Los efectos secundarios leves reportados son notables principalmente por ser poco notables: reacciones ocasionales en el sitio de inyección (~10-15% de los usuarios), fatiga transitoria en la primera semana, náuseas leves en protocolos orales. La preocupación teórica que aparece más a menudo es si las propiedades promotoras de angiogénesis podrían acelerar tumores existentes — no hay evidencia humana a favor o en contra, pero la mayoría de investigadores excluye historial de cáncer como precaución. No aprobado por la FDA. WADA no lo ha prohibido (a partir de 2026), a diferencia de TB-500.",
            'quick_answer': "BPC-157 es un péptido de 15 aminoácidos derivado del jugo gástrico humano, estudiado desde principios de los 90 por el laboratorio de Sikiric en Zagreb por sus efectos en reparación tisular. La evidencia animal sobre tendones, ligamentos, músculo y curación intestinal es consistente e impresionante — la pega es que no hay ensayos humanos registrados. Protocolos típicos: 200-500 mcg/día subcutáneo durante 4-8 semanas. El mecanismo es multivía (angiogénesis, óxido nítrico, eje intestino-cerebro). A menudo combinado con TB-500 para lesiones. No aprobado por la FDA.",
        },
        'pt': {
            'name': 'BPC-157',
            'category': 'Peptídeo de reparação tecidual',
            'related': ['tb-500', 'ghk-cu', 'thymosin-alpha-1'],
            'overview': "BPC-157 é um fragmento de 15 aminoácidos de uma proteína maior encontrada no suco gástrico humano — o próprio composto de proteção do corpo, daí o nome. O laboratório de Predrag Sikiric na Universidade de Zagreb o isolou e caracterizou pela primeira vez no início dos anos 90, inicialmente como protetor gástrico. O que ninguém esperava era a amplitude com que funcionaria em outros tecidos. No início dos anos 2000, os estudos animais mostravam que o BPC-157 acelerava a cicatrização em tendões, ligamentos, músculos, cérebro, vasos sanguíneos — quase qualquer tecido que você testasse. É um perfil suspeito (compostos que funcionam em tudo geralmente não funcionam em nada), mas a consistência dos dados em roedores é genuinamente impressionante, e Sikiric já publicou mais de 200 artigos sobre o tema.",
            'mechanism': "O mecanismo é complexo porque o BPC-157 parece fazer várias coisas ao mesmo tempo. Ele aumenta a expressão de VEGF e promove angiogênese (formação de novos vasos sanguíneos nos sítios de lesão), o que provavelmente explica grande parte do efeito cicatrizante. Aumenta a síntese de óxido nítrico. Modula os sistemas de dopamina e serotonina via o eixo intestino-cérebro (a estrutura teórica principal de Sikiric). Interage com a expressão do receptor de hormônio do crescimento. Resumo honesto: ninguém ainda identificou um mecanismo primário único, e isso incomoda alguns pesquisadores. A compensação é que essa mesma história multi-mecanismo explicaria por que um único peptídeo parece ajudar em tantas lesões diferentes.",
            'evidence': "Aqui é preciso ter cuidado. A evidência animal é genuinamente impressionante — Krivic et al. (2008) mostrou reparação acelerada do tendão de Aquiles em ratos, Cerovecki et al. (2010) mostrou cicatrização mais rápida do ligamento colateral medial, e há uma longa série de estudos de úlcera gástrica induzida por AINE mostrando 90%+ de proteção mucosa. O ponto de atenção: a partir de 2026, não há ensaios clínicos humanos randomizados registrados. A comunidade de recuperação atlética tem efetivamente conduzido um experimento descontrolado por mais de 15 anos com anedotas que vão de milagrosas a sem efeito, mas isso não é o mesmo que evidência RCT.",
            'dosing': "Protocolos de pesquisa típicos usam 200-500 mcg ao dia por via subcutânea, frequentemente divididos em duas doses. Muitos usuários injetam perto do local da lesão sob a teoria de que a concentração local ajuda — isso é plausível, mas não realmente comprovado. Protocolos orais (250-500 mcg, 1-2x ao dia) também são estudados; o BPC-157 é incomumente estável em ácido estomacal. Lesões agudas frequentemente começam com doses de carga mais altas (500 mcg duas vezes ao dia) por 4-8 semanas. A meia-vida é curta (poucas horas subcutâneo), por isso a dosagem duas vezes ao dia é padrão.",
            'safety': "O perfil de segurança em estudos animais é excelente — LD50 extremamente alto (>10g/kg), sem eventos de toxicidade aguda. Dados humanos de longo prazo simplesmente não existem. Os efeitos colaterais leves relatados são notáveis principalmente por serem pouco notáveis: reações ocasionais no local da injeção (~10-15% dos usuários), fadiga transitória na primeira semana, náusea leve em protocolos orais. A preocupação teórica mais frequente é se as propriedades promotoras de angiogênese poderiam acelerar tumores existentes — não há evidência humana a favor ou contra, mas a maioria dos pesquisadores exclui histórico de câncer como precaução. Não aprovado pela FDA.",
            'quick_answer': "BPC-157 é um peptídeo de 15 aminoácidos derivado do suco gástrico humano, estudado desde o início dos anos 90 pelo laboratório de Sikiric em Zagreb por seus efeitos na reparação tecidual. A evidência animal sobre tendões, ligamentos, músculos e cicatrização intestinal é consistente e impressionante — o ponto de atenção é que não há ensaios humanos registrados. Protocolos típicos: 200-500 mcg/dia subcutâneo por 4-8 semanas. O mecanismo é multivia (angiogênese, óxido nítrico, eixo intestino-cérebro). Frequentemente combinado com TB-500 para lesões. Não aprovado pela FDA.",
        },
        'fr': {
            'name': 'BPC-157',
            'category': 'Peptide de réparation tissulaire',
            'related': ['tb-500', 'ghk-cu', 'thymosin-alpha-1'],
            'overview': "BPC-157 est un fragment de 15 acides aminés issu d'une protéine plus grande présente dans le suc gastrique humain — le propre composé de protection du corps, d'où le nom. Le laboratoire de Predrag Sikiric à l'Université de Zagreb l'a isolé et caractérisé pour la première fois au début des années 1990, initialement comme protecteur gastrique. Ce que personne n'attendait, c'était à quel point il fonctionnerait dans d'autres tissus. Au début des années 2000, les études animales montraient que le BPC-157 accélérait la cicatrisation dans les tendons, ligaments, muscles, cerveau, vaisseaux sanguins — presque n'importe quel tissu testé. C'est un profil suspect (les composés qui marchent partout ne marchent généralement nulle part), mais la cohérence des données chez les rongeurs est vraiment frappante, et Sikiric a maintenant publié plus de 200 articles sur le sujet.",
            'mechanism': "Le mécanisme est complexe parce que BPC-157 semble faire plusieurs choses à la fois. Il sur-régule VEGF et favorise l'angiogenèse (formation de nouveaux vaisseaux sanguins aux sites de lésion), ce qui explique probablement une grande partie de l'effet cicatrisant. Il augmente la synthèse d'oxyde nitrique. Il module les systèmes de dopamine et de sérotonine via l'axe intestin-cerveau (le cadre théorique principal de Sikiric). Il interagit avec l'expression du récepteur de l'hormone de croissance. Résumé honnête : personne n'a encore identifié un mécanisme primaire unique, ce qui dérange certains chercheurs. Le compromis est que cette même histoire multi-mécanismes expliquerait pourquoi un seul peptide semble aider tant de lésions différentes.",
            'evidence': "Ici il faut être prudent. Les données animales sont vraiment impressionnantes — Krivic et al. (2008) a montré une réparation accélérée du tendon d'Achille chez le rat, Cerovecki et al. (2010) a montré une cicatrisation plus rapide du ligament collatéral médial, et il y a une longue série d'études d'ulcères gastriques induits par AINS montrant une protection muqueuse de 90%+. Le bémol : en 2026, il y a zéro essai clinique humain randomisé enregistré. La communauté de récupération sportive a effectivement mené une expérience non contrôlée géante pendant 15+ ans, avec des anecdotes allant de miraculeuses à sans effet, mais ce n'est pas la même chose que des données RCT.",
            'dosing': "Les protocoles de recherche typiques utilisent 200-500 mcg par jour par voie sous-cutanée, souvent divisés en deux doses. De nombreux utilisateurs injectent près du site de la lésion en partant du principe que la concentration locale aide — c'est plausible mais pas vraiment prouvé. Les protocoles oraux (250-500 mcg, 1-2x par jour) sont aussi étudiés ; le BPC-157 est exceptionnellement stable en milieu acide gastrique. Les blessures aiguës commencent souvent par des doses de charge plus élevées (500 mcg deux fois par jour) pendant 4-8 semaines. La demi-vie est courte (quelques heures en sous-cutané), c'est pourquoi le dosage biquotidien est standard.",
            'safety': "Le profil de sécurité dans les études animales est excellent — DL50 extrêmement élevée (>10g/kg), pas d'événements de toxicité aiguë. Les données humaines à long terme n'existent tout simplement pas. Les effets secondaires légers rapportés sont notables surtout par leur banalité : réactions occasionnelles au site d'injection (~10-15% des utilisateurs), fatigue transitoire la première semaine, légère nausée dans les protocoles oraux. La préoccupation théorique la plus fréquente est de savoir si les propriétés pro-angiogéniques pourraient accélérer des tumeurs existantes — il n'y a pas de preuves humaines pour ou contre, mais la plupart des chercheurs excluent les antécédents de cancer par précaution. Non approuvé par la FDA.",
            'quick_answer': "BPC-157 est un peptide de 15 acides aminés dérivé du suc gastrique humain, étudié depuis le début des années 1990 par le laboratoire de Sikiric à Zagreb pour ses effets sur la réparation tissulaire. Les données animales sur les tendons, ligaments, muscles et cicatrisation intestinale sont cohérentes et impressionnantes — le bémol est qu'il n'y a aucun essai humain enregistré. Protocoles typiques : 200-500 mcg/jour par voie sous-cutanée pendant 4-8 semaines. Mécanisme multi-voies (angiogenèse, oxyde nitrique, axe intestin-cerveau). Souvent associé à TB-500 pour les blessures. Non approuvé par la FDA.",
        },
    },
    'tb-500': {
        'es': {
            'name': 'TB-500',
            'category': 'Péptido de reparación tisular',
            'related': ['bpc-157', 'ghk-cu'],
            'overview': "TB-500 no es realmente una molécula completa — es un fragmento de 17 aminoácidos de la timosina beta-4 (Tβ4), una de las proteínas intracelulares más abundantes en el cuerpo. El fragmento corresponde a la región activa. La mayor parte del interés original vino de la medicina veterinaria de los años 90, donde TB-500 se usaba para acelerar la recuperación de tendones y tejidos blandos en caballos de carrera (y, predeciblemente, en humanos que tomaron nota). RegeneRx (ahora G-treeBNT) desarrolló varios candidatos clínicos. La comunidad de recuperación atlética trata TB-500 y BPC-157 como un par por defecto para lesiones — a veces por razones mecanísticas sólidas, a veces porque los protocolos se copiaron suficientes veces.",
            'mechanism': "El trabajo biológico principal de la timosina beta-4 es secuestrar monómeros de G-actina — básicamente, controla cómo las células se desplazan durante la reparación. Ese papel de migración celular es lo que hace a TB-500 interesante para la cicatrización: si estás reconstruyendo un tendón, necesitas que los fibroblastos lleguen al lugar correcto. Más allá de eso, promueve angiogénesis (más VEGF, más vasos sanguíneos nuevos), atenúa citoquinas inflamatorias (TNF-α, IL-6, IL-1β), y protege cardiomiocitos del daño isquémico. El artículo de Bock-Marquette et al. (Nature 2004) sobre protección cardíaca es probablemente el estudio mecanístico más citado.",
            'evidence': "La evidencia animal es amplia y consistente: isquemia-reperfusión cardíaca (el artículo de Nature), curación de heridas (Malinda et al. 1999), reparación corneal, regeneración neural. RegeneRx ejecutó múltiples ensayos Fase II en humanos — RGN-352 para atrofia muscular sistémica, RGN-259 para oftalmología, RGN-137 para curación de heridas. Resultados mixtos. La señal regulatoria más clara: WADA prohibió TB-500 en 2011 como sustancia S2 (factores de crecimiento). Para atletas competitivos, no es una preocupación teórica.",
            'dosing': "Los protocolos estándar de investigación son 2-5 mg por semana por vía subcutánea, divididos en dos dosis. Las fases de lesiones agudas a menudo usan un enfoque de 'dosis de carga' — 2-2.5 mg al día durante la primera semana, luego 4-6 semanas a la dosis de carga, bajando a 2 mg/semana para mantenimiento. La vida media es genuinamente de días (vs. horas para BPC-157), lo que permite el horario semanal. La rotación del sitio de inyección importa más de lo que se piensa. El protocolo combinado 'BPC + TB' es la configuración de investigación más común.",
            'safety': "Datos humanos limitados pero los ensayos clínicos de RegeneRx no detectaron problemas mayores. La preocupación teórica es la misma que con BPC-157, solo más fuerte: angiogénesis y migración celular son exactamente lo que los tumores necesitan. Antecedentes de cáncer es exclusión en la mayoría de investigaciones, y eso es la decisión correcta. Los efectos secundarios reportados son mayormente del tipo aburrido — reacciones en el sitio de inyección, fatiga transitoria, mareos ocasionales. La prohibición de WADA significa que los atletas competitivos enfrentan consecuencias reales por el uso, incluyendo programas de pruebas en el retiro.",
            'quick_answer': "TB-500 es un fragmento de 17 aminoácidos de la timosina beta-4, originalmente usado en medicina veterinaria para recuperación de tendones de caballos antes de cruzar a investigación humana. Mecanismo multi-frente: secuestro de actina impulsa migración celular (clave para reparación tisular), más angiogénesis y efectos antiinflamatorios. Bock-Marquette et al. 2004 (Nature) sobre protección cardíaca es el artículo mecanístico fundamental. Protocolo estándar: 2-5 mg/semana subcutáneo, a menudo como estructura 'carga + mantenimiento' con BPC-157. Prohibido por WADA desde 2011.",
        },
        'pt': {
            'name': 'TB-500',
            'category': 'Peptídeo de reparação tecidual',
            'related': ['bpc-157', 'ghk-cu'],
            'overview': "TB-500 não é realmente uma molécula completa — é um fragmento de 17 aminoácidos da timosina beta-4 (Tβ4), uma das proteínas intracelulares mais abundantes no corpo. O fragmento corresponde à região ativa. A maior parte do interesse original veio da medicina veterinária nos anos 90, onde o TB-500 era usado para acelerar a recuperação de tendões e tecidos moles em cavalos de corrida (e, previsivelmente, em humanos que prestaram atenção). RegeneRx (agora G-treeBNT) desenvolveu vários candidatos clínicos. A comunidade de recuperação atlética trata TB-500 e BPC-157 como par padrão para lesões.",
            'mechanism': "O trabalho biológico principal da timosina beta-4 é sequestrar monômeros de G-actina — basicamente, controla como as células se movem durante o reparo. Esse papel de migração celular é o que torna o TB-500 interessante para cicatrização: se você está reconstruindo um tendão, precisa que os fibroblastos cheguem ao local certo. Além disso, promove angiogênese (mais VEGF, mais vasos sanguíneos novos), reduz citocinas inflamatórias (TNF-α, IL-6, IL-1β), e protege cardiomiócitos do dano isquêmico. O artigo de Bock-Marquette et al. (Nature 2004) sobre proteção cardíaca é provavelmente o estudo mecanístico mais citado.",
            'evidence': "Evidência animal ampla e consistente: isquemia-reperfusão cardíaca (artigo da Nature), cicatrização de feridas (Malinda et al. 1999), reparo da córnea, regeneração neural. RegeneRx conduziu múltiplos ensaios Fase II em humanos — RGN-352 para atrofia muscular sistêmica, RGN-259 para oftalmologia, RGN-137 para cicatrização de feridas. Resultados mistos. O sinal regulatório mais claro: WADA proibiu o TB-500 em 2011 como substância S2 (fatores de crescimento). Para atletas competitivos, não é uma preocupação teórica.",
            'dosing': "Protocolos padrão de pesquisa são 2-5 mg por semana via subcutânea, divididos em duas doses. As fases de lesões agudas frequentemente usam abordagem 'dose de carga' — 2-2.5 mg ao dia na primeira semana, depois 4-6 semanas na dose de carga, caindo para 2 mg/semana para manutenção. A meia-vida é genuinamente de dias (vs. horas para o BPC-157), o que permite o esquema semanal. A rotação do local de injeção importa mais do que as pessoas pensam. O protocolo combinado 'BPC + TB' é a configuração de pesquisa mais comum.",
            'safety': "Dados humanos limitados, mas os ensaios clínicos da RegeneRx não detectaram problemas maiores. A preocupação teórica é a mesma do BPC-157, só que mais alta: angiogênese e migração celular são exatamente o que tumores precisam. Histórico de câncer é exclusão na maioria das pesquisas, e essa é a decisão certa. Efeitos colaterais reportados são em sua maioria do tipo entediante — reações no local da injeção, fadiga transitória, tontura ocasional. A proibição da WADA significa que atletas competitivos enfrentam consequências reais pelo uso.",
            'quick_answer': "TB-500 é um fragmento de 17 aminoácidos da timosina beta-4, originalmente usado em medicina veterinária para recuperação de tendões de cavalos antes de migrar para pesquisa humana. Mecanismo multifacetado: sequestro de actina impulsiona migração celular (chave para reparo tecidual), mais angiogênese e efeitos anti-inflamatórios. Bock-Marquette et al. 2004 (Nature) sobre proteção cardíaca é o artigo mecanístico fundamental. Protocolo padrão: 2-5 mg/semana subcutâneo, frequentemente como estrutura 'carga + manutenção' com BPC-157. Proibido pela WADA desde 2011.",
        },
        'fr': {
            'name': 'TB-500',
            'category': 'Peptide de réparation tissulaire',
            'related': ['bpc-157', 'ghk-cu'],
            'overview': "TB-500 n'est pas vraiment une molécule complète — c'est un fragment de 17 acides aminés de la thymosine bêta-4 (Tβ4), l'une des protéines intracellulaires les plus abondantes du corps. Le fragment correspond à la région active. La plupart de l'intérêt initial venait de la médecine vétérinaire des années 1990, où TB-500 était utilisé pour accélérer la récupération des tendons et tissus mous chez les chevaux de course (et, prévisiblement, chez les humains qui ont pris note). RegeneRx (maintenant G-treeBNT) a développé plusieurs candidats cliniques. La communauté de récupération sportive traite TB-500 et BPC-157 comme une paire par défaut pour les blessures.",
            'mechanism': "Le travail biologique principal de la thymosine bêta-4 est de séquestrer les monomères de G-actine — en gros, elle contrôle la façon dont les cellules se déplacent pendant la réparation. Ce rôle de migration cellulaire est ce qui rend TB-500 intéressant pour la cicatrisation : si vous reconstruisez un tendon, il faut que les fibroblastes arrivent au bon endroit. Au-delà, il favorise l'angiogenèse (plus de VEGF, plus de nouveaux vaisseaux sanguins), atténue les cytokines inflammatoires (TNF-α, IL-6, IL-1β), et protège les cardiomyocytes des lésions ischémiques. L'article de Bock-Marquette et al. (Nature 2004) sur la protection cardiaque est probablement l'étude mécanistique la plus citée.",
            'evidence': "Données animales larges et cohérentes : ischémie-reperfusion cardiaque (l'article de Nature), cicatrisation des plaies (Malinda et al. 1999), réparation cornéenne, régénération neurale. RegeneRx a mené plusieurs essais de Phase II chez l'humain — RGN-352 pour l'atrophie musculaire systémique, RGN-259 pour l'ophtalmologie, RGN-137 pour la cicatrisation des plaies. Résultats mitigés. Le signal réglementaire le plus clair : WADA a interdit TB-500 en 2011 comme substance S2 (facteurs de croissance). Pour les athlètes en compétition, ce n'est pas une préoccupation théorique.",
            'dosing': "Les protocoles de recherche standard sont 2-5 mg par semaine en sous-cutané, divisés en deux doses. Les phases de blessures aiguës utilisent souvent une approche de 'dose de charge' — 2-2.5 mg par jour la première semaine, puis 4-6 semaines à la dose de charge, descendant à 2 mg/semaine pour le maintien. La demi-vie est vraiment de jours (vs heures pour BPC-157), ce qui permet le calendrier hebdomadaire. La rotation des sites d'injection compte plus qu'on ne le pense. Le protocole combiné 'BPC + TB' est la configuration de recherche la plus courante.",
            'safety': "Données humaines limitées mais les essais cliniques de RegeneRx n'ont pas détecté de problèmes majeurs. La préoccupation théorique est la même qu'avec BPC-157, en plus fort : l'angiogenèse et la migration cellulaire sont exactement ce dont les tumeurs ont besoin. Antécédents de cancer = exclusion dans la plupart des recherches, et c'est la bonne décision. Les effets secondaires rapportés sont surtout ennuyeux — réactions au site d'injection, fatigue transitoire, vertiges occasionnels. L'interdiction de WADA signifie que les athlètes en compétition font face à de vraies conséquences pour l'usage.",
            'quick_answer': "TB-500 est un fragment de 17 acides aminés de la thymosine bêta-4, à l'origine utilisé en médecine vétérinaire pour la récupération des tendons des chevaux de course avant de passer à la recherche humaine. Mécanisme multi-fronts : séquestration de l'actine pour la migration cellulaire (clé pour la réparation tissulaire), plus angiogenèse et effets anti-inflammatoires. Bock-Marquette et al. 2004 (Nature) sur la protection cardiaque est l'article mécanistique fondamental. Protocole standard : 2-5 mg/semaine sous-cutané, souvent en structure 'charge + maintien' avec BPC-157. Interdit par WADA depuis 2011.",
        },
    },
    'semaglutide': {
        'es': {
            'name': 'Semaglutida',
            'category': 'Agonista del receptor GLP-1 (aprobado por FDA)',
            'related': ['tirzepatide', 'retatrutide'],
            'overview': "La semaglutida es la molécula que rompió el mercado de medicamentos para la obesidad. Novo Nordisk la desarrolló como agonista del receptor GLP-1 de acción prolongada para diabetes tipo 2 — comercializada como Ozempic para diabetes y Wegovy para obesidad, con una versión oral llamada Rybelsus. Estructuralmente es un péptido de 31 aminoácidos basado en la hormona GLP-1(7-37) natural, con una cadena lateral de ácido graso (C18) que le permite unirse a la albúmina en sangre. Esa unión a albúmina es el truco: extiende la vida media de minutos a unos 7 días, por lo que la semaglutida funciona como inyección semanal. Los ingresos de Novo por semaglutida alcanzaron aproximadamente $9.5 mil millones solo en el segundo trimestre de 2024.",
            'mechanism': "La semaglutida se une al receptor GLP-1 (GLP-1R), un receptor acoplado a proteína G, y activa la vía cAMP/PKA río abajo. Esto desencadena varios efectos en paralelo: secreción de insulina dependiente de glucosa (solo se activa cuando la glucemia está realmente elevada, por eso la hipoglucemia es rara), supresión de la liberación de glucagón, vaciamiento gástrico ralentizado (te sientes lleno más tiempo), y activación directa de neuronas POMC/CART en el núcleo arqueado hipotalámico que impulsan la saciedad. La sustitución Aib en el N-terminal bloquea la degradación por DPP-4; el ácido graso C18 hace el truco de unión a albúmina.",
            'evidence': "STEP 1 (NEJM 2021) es el ensayo principal: 2.4 mg de semaglutida semanal durante 68 semanas, 14.9% de pérdida de peso media en pacientes obesos no diabéticos vs 2.4% con placebo. Eso no está en la misma liga que medicamentos previos para obesidad — cambió la conversación. STEP 5 extendió a 104 semanas con pérdida sostenida de 15.2%. La serie SUSTAIN (1-10) estableció sus credenciales en diabetes: caídas de HbA1c de 1.5-1.8%, pérdida de peso de 4-6 kg. El ensayo más importante reciente es SELECT (NEJM 2023), que mostró una reducción del 20% en MACE (eventos cardiovasculares adversos mayores) en pacientes obesos no diabéticos con enfermedad cardiovascular.",
            'dosing': "La dosificación para diabetes comienza en 0.25 mg semanales y titula cada 4 semanas: 0.5 → 1.0 → máximo 2.0 mg. La dosificación para obesidad llega más alto: 0.25 → 0.5 → 1.0 → 1.7 → máximo 2.4 mg. La titulación lenta es genuinamente importante para tolerabilidad — la titulación rápida dispara la tasa de náuseas. Rybelsus oral comienza en 7 mg al día, aumenta a 14 mg después de 4 semanas, debe tomarse con el estómago vacío (30+ minutos antes de la comida).",
            'safety': "Los efectos secundarios están dominados por GI: náuseas (44.2% en STEP 1), vómitos (24.8%), diarrea (31.5%), estreñimiento (24.2%) — más concentrados en la fase de titulación. Riesgos reales pero raros: pancreatitis aguda (0.1-0.3% en SUSTAIN), eventos de vesícula (cálculos biliares, colecistitis, 2-3% con uso prolongado), empeoramiento de retinopatía diabética. La advertencia de recuadro negro de la FDA es para carcinoma medular de tiroides basada en estudios en roedores; antecedentes familiares de síndrome MEN2 es contraindicación absoluta.",
            'quick_answer': "Semaglutida (Ozempic/Wegovy/Rybelsus) es el agonista del receptor GLP-1 de acción prolongada de Novo Nordisk que efectivamente reseteó las expectativas para medicamentos contra la obesidad. STEP 1 (2021) mostró 14.9% de pérdida de peso a las 68 semanas. La cadena lateral de ácido graso C18 permite la unión a albúmina y vida media de ~7 días. Mecanismo combina sensibilización a insulina, supresión de glucagón, vaciamiento gástrico ralentizado y señalización de saciedad hipotalámica directa. SELECT (2023) añadió reducción del 20% de eventos cardiovasculares. Efectos secundarios dominados por GI; advertencia de recuadro negro por carcinoma medular de tiroides.",
        },
        'pt': {
            'name': 'Semaglutida',
            'category': 'Agonista do receptor GLP-1 (aprovado pela FDA)',
            'related': ['tirzepatide', 'retatrutide'],
            'overview': "A semaglutida é a molécula que quebrou o mercado de medicamentos para obesidade. A Novo Nordisk a desenvolveu como agonista do receptor GLP-1 de ação prolongada para diabetes tipo 2 — comercializada como Ozempic para diabetes e Wegovy para obesidade, com versão oral chamada Rybelsus. Estruturalmente é um peptídeo de 31 aminoácidos baseado no hormônio GLP-1(7-37) natural, com uma cadeia lateral de ácido graxo (C18) que permite ligação à albumina no sangue. Essa ligação à albumina é o truque: estende a meia-vida de minutos para cerca de 7 dias, por isso a semaglutida funciona como injeção semanal.",
            'mechanism': "A semaglutida se liga ao receptor GLP-1 (GLP-1R), um receptor acoplado a proteína G, e ativa a via cAMP/PKA a jusante. Isso desencadeia vários efeitos em paralelo: secreção de insulina dependente de glicose (só ativa quando a glicemia está realmente elevada, por isso hipoglicemia é rara), supressão da liberação de glucagon, esvaziamento gástrico mais lento (você se sente saciado por mais tempo), e ativação direta de neurônios POMC/CART no núcleo arqueado hipotalâmico que impulsionam saciedade. A substituição Aib no N-terminal bloqueia a degradação por DPP-4; o ácido graxo C18 faz o truque de ligação à albumina.",
            'evidence': "STEP 1 (NEJM 2021) é o ensaio principal: 2.4 mg de semaglutida semanal por 68 semanas, perda de peso média de 14.9% em pacientes obesos não diabéticos vs 2.4% no placebo. Isso não está na mesma liga que medicamentos anteriores para obesidade — mudou a conversa. STEP 5 estendeu para 104 semanas com perda sustentada de 15.2%. A série SUSTAIN (1-10) estabeleceu suas credenciais em diabetes: quedas de HbA1c de 1.5-1.8%, perda de peso de 4-6 kg. O ensaio mais importante recente é SELECT (NEJM 2023), que mostrou redução de 20% em MACE em pacientes obesos não diabéticos com doença cardiovascular.",
            'dosing': "A dosagem para diabetes começa em 0.25 mg semanais e titula a cada 4 semanas: 0.5 → 1.0 → máximo 2.0 mg. A dosagem para obesidade vai mais alto: 0.25 → 0.5 → 1.0 → 1.7 → máximo 2.4 mg. A titulação lenta é genuinamente importante para tolerabilidade. Rybelsus oral começa em 7 mg ao dia, aumenta para 14 mg após 4 semanas, deve ser tomado com estômago vazio.",
            'safety': "Os efeitos colaterais são dominados por GI: náusea (44.2% em STEP 1), vômito (24.8%), diarreia (31.5%), constipação (24.2%) — mais concentrados na fase de titulação. Riscos reais mas raros: pancreatite aguda (0.1-0.3%), eventos de vesícula biliar, piora de retinopatia diabética. A advertência de tarja preta da FDA é para carcinoma medular de tireoide baseada em estudos em roedores; histórico familiar de síndrome MEN2 é contraindicação absoluta.",
            'quick_answer': "Semaglutida (Ozempic/Wegovy/Rybelsus) é o agonista do receptor GLP-1 de ação prolongada da Novo Nordisk que efetivamente reformulou expectativas para medicamentos contra obesidade. STEP 1 (2021) mostrou 14.9% de perda de peso em 68 semanas. A cadeia lateral de ácido graxo C18 permite ligação à albumina e meia-vida de ~7 dias. Mecanismo combina sensibilização à insulina, supressão de glucagon, esvaziamento gástrico mais lento e sinalização de saciedade hipotalâmica direta. SELECT (2023) adicionou redução de 20% em eventos cardiovasculares.",
        },
        'fr': {
            'name': 'Sémaglutide',
            'category': 'Agoniste du récepteur GLP-1 (approuvé FDA)',
            'related': ['tirzepatide', 'retatrutide'],
            'overview': "Le sémaglutide est la molécule qui a cassé le marché des médicaments contre l'obésité. Novo Nordisk l'a développé comme agoniste à action prolongée du récepteur GLP-1 pour le diabète de type 2 — commercialisé sous Ozempic pour le diabète et Wegovy pour l'obésité, avec une version orale appelée Rybelsus. Structurellement c'est un peptide de 31 acides aminés basé sur l'hormone GLP-1(7-37) naturelle, avec une chaîne latérale d'acide gras (C18) qui lui permet de se lier à l'albumine sanguine. Cette liaison à l'albumine est l'astuce : elle étend la demi-vie de minutes à environ 7 jours, c'est pourquoi le sémaglutide fonctionne en injection hebdomadaire.",
            'mechanism': "Le sémaglutide se lie au récepteur GLP-1 (GLP-1R), un récepteur couplé aux protéines G, et active la voie cAMP/PKA en aval. Cela déclenche plusieurs effets en parallèle : sécrétion d'insuline dépendante du glucose (ne se déclenche que quand la glycémie est élevée, c'est pourquoi l'hypoglycémie est rare), suppression de la libération de glucagon, vidange gastrique ralentie (vous vous sentez rassasié plus longtemps), et activation directe des neurones POMC/CART du noyau arqué hypothalamique qui pilotent la satiété. La substitution Aib en N-terminal bloque la dégradation par DPP-4 ; l'acide gras C18 fait l'astuce de liaison à l'albumine.",
            'evidence': "STEP 1 (NEJM 2021) est l'essai phare : 2,4 mg de sémaglutide par semaine pendant 68 semaines, 14,9% de perte de poids moyenne chez les patients obèses non diabétiques contre 2,4% sous placebo. Ce n'est pas dans la même catégorie que les médicaments anti-obésité précédents — cela a changé la conversation. STEP 5 a étendu à 104 semaines avec une perte soutenue de 15,2%. La série SUSTAIN (1-10) a établi ses références en diabète : baisses de HbA1c de 1,5-1,8%, perte de poids de 4-6 kg. L'essai le plus important récemment est SELECT (NEJM 2023), qui a montré une réduction de 20% des MACE chez les patients obèses non diabétiques avec maladie cardiovasculaire.",
            'dosing': "La dose pour le diabète commence à 0,25 mg hebdomadaire et titre toutes les 4 semaines : 0,5 → 1,0 → maximum 2,0 mg. La dose pour l'obésité monte plus haut : 0,25 → 0,5 → 1,0 → 1,7 → maximum 2,4 mg. La titration lente est vraiment importante pour la tolérance. Rybelsus oral commence à 7 mg par jour, augmente à 14 mg après 4 semaines, doit être pris à jeun.",
            'safety': "Les effets secondaires sont dominés par le tube digestif : nausées (44,2% dans STEP 1), vomissements (24,8%), diarrhée (31,5%), constipation (24,2%) — plus concentrés en phase de titration. Risques réels mais rares : pancréatite aiguë (0,1-0,3%), événements vésiculaires, aggravation de rétinopathie diabétique. L'avertissement encadré de la FDA concerne le carcinome médullaire thyroïdien sur la base d'études chez le rongeur ; antécédents familiaux de syndrome MEN2 = contre-indication absolue.",
            'quick_answer': "Sémaglutide (Ozempic/Wegovy/Rybelsus) est l'agoniste à action prolongée du récepteur GLP-1 de Novo Nordisk qui a effectivement redéfini les attentes pour les médicaments anti-obésité. STEP 1 (2021) a montré 14,9% de perte de poids à 68 semaines. La chaîne latérale d'acide gras C18 permet la liaison à l'albumine et une demi-vie de ~7 jours. Mécanisme combine sensibilisation à l'insuline, suppression du glucagon, vidange gastrique ralentie, et signalisation directe de satiété hypothalamique. SELECT (2023) a ajouté 20% de réduction d'événements cardiovasculaires.",
        },
    },
}

# Aspect framings — language-specific
def aspect_paragraphs(angle, c, lang):
    name = c['name']
    cat = c['category']
    related = c.get('related', [])

    if lang == 'es':
        cross = (f"Compuestos relacionados (para investigación adicional): {', '.join(related[:3])}." if related else "")
        if angle in ('guide', 'general', 'comprehensive'):
            return [
                (f'¿Qué es {name}?', c['overview']),
                ('Cómo funciona: mecanismo', c['mechanism']),
                ('Lo que muestra la investigación', c['evidence']),
                ('Dosificación y administración', c['dosing']),
                ('Perfil de seguridad y efectos secundarios', c['safety']),
                ('Realidad regulatoria',
                 f"En EE.UU. y la mayoría de jurisdicciones, {name} no está aprobado para uso humano — se vende como producto químico de investigación o reactivo de laboratorio. Las directrices de farmacias de compounding 503A vs 503B se han endurecido en 2023-2024. La lista de prohibidos de WADA también importa para atletas. El estado regulatorio cambia con el tiempo; verifica las reglas actuales antes de iniciar cualquier protocolo de investigación."),
                ('Consideraciones prácticas',
                 f"Algunas cosas que aparecen repetidamente con la investigación de {name}: la varianza de calidad entre proveedores es real y no sutil. La verificación HPLC independiente por terceros, lote por lote (no 'muestras representativas'), es lo único que te da potencia confiable. La mayoría de protocolos comienza en el extremo bajo del rango de dosificación y titula hacia arriba. La documentación importa más de lo que se piensa. {cross}"),
            ]
        if angle == 'faq':
            return [
                (f'Preguntas frecuentes sobre {name}', f"Lo que sigue son las preguntas sobre {name} que aparecen más a menudo en discusiones de la comunidad de investigación, con respuestas basadas en literatura publicada y mecanismos conocidos."),
                (f'¿Qué es {name}?', c['overview']),
                (f'¿Qué dosis es típica en protocolos de investigación?', c['dosing']),
                (f'¿Cómo funciona realmente?', c['mechanism']),
                (f'¿Cuáles son las principales consideraciones de seguridad?', c['safety']),
                (f'¿Cuán fuerte es la base de evidencia?', c['evidence']),
                (f'¿{name} está aprobado por la FDA?',
                 f"Depende del compuesto. Algunos péptidos del panorama amplio están aprobados por la FDA (semaglutida, tirzepatida, tesamorelina, setmelanotida), pero la mayoría de péptidos de investigación no — se venden como 'productos químicos de investigación,' solo para uso de laboratorio, no para consumo humano. La distinción 503A vs 503B en farmacias de compounding también importa. El estado regulatorio cambia — verifica las reglas actuales antes de iniciar cualquier protocolo."),
            ]
        if angle == 'dosing':
            return [
                (f'Dosificación de {name}: lo que dice la investigación', c['dosing']),
                (f'Cómo funciona {name} (y por qué eso importa para la dosis)', c['mechanism']),
                ('Por qué importa la variación individual',
                 f"Las dosis 'estándar' de investigación para {name} representan promedios poblacionales — las respuestas individuales varían sustancialmente. La edad, el peso, el sexo, los niveles basales de biomarcadores, los puntos finales objetivo y las condiciones de salud existentes influyen en cómo se ve la dosificación óptima. La forma en que encuentras tu ventana de respuesta individual es estableciendo mediciones basales y siguiendo qué cambia cuando cambia la dosis."),
                ('Por qué la titulación supera ir directo al objetivo',
                 f"Con {name}, aumentar gradualmente casi siempre supera saltar a tu dosis objetivo. La titulación te permite (1) caracterizar tu curva de respuesta individual, (2) detectar problemas de sensibilidad antes de que se conviertan en problemas, (3) minimizar eventos adversos tempranos, (4) construir un protocolo sostenible a largo plazo."),
                ('Consideraciones de seguridad relacionadas con la dosis', c['safety']),
                ('Documentación', f"Registrar dosis, momento, sitio de inyección, factores concomitantes y respuestas observadas es la base de la investigación a largo plazo de {name}. Ese registro es lo que (1) te permite identificar tus patrones de respuesta individual, (2) ayuda a evaluar si los efectos secundarios están relacionados con la dosis, (3) informa los ajustes del protocolo."),
            ]
        if angle == 'safety' or angle == 'side-effects':
            return [
                (f'Seguridad de {name}: una revisión honesta', c['safety']),
                ('Entendiendo los efectos secundarios a través del mecanismo', c['mechanism']),
                ('Contraindicaciones e interacciones medicamentosas',
                 f"Con {name}, las contraindicaciones que verás más a menudo: malignidad conocida o sospechada (especialmente compuestos que tocan vías proliferativas), enfermedad endocrina grave no controlada, embarazo o lactancia, niños a menos que esté aprobado, deterioro hepático o renal grave. Las interacciones medicamentosas usualmente necesitan revisión de un proveedor de atención médica."),
                ('Cómo se relaciona la dosis con los efectos secundarios',
                 f"Los efectos secundarios con {name} típicamente están relacionados con la dosis: a dosis bajas son raros, a dosis moderadas verás algo de incidencia pero usualmente leve, a dosis altas tanto la incidencia como la severidad escalan juntas. Comenzar con la dosis mínima efectiva es la única estrategia más efectiva de reducción de eventos adversos."),
                ('Estrategia de monitoreo',
                 f"Para protocolos más largos de investigación con {name}, un enfoque estructurado de monitoreo: (1) Evaluación basal — biomarcadores relevantes, severidad de síntomas, medidas funcionales objetivo. (2) Laboratorios periódicos basados en el mecanismo del compuesto. (3) Seguimiento de síntomas — registros estructurados, no de memoria. (4) Documentación de eventos adversos cuando sea relevante."),
                ('Cuándo detener inmediatamente',
                 f"Síntomas que justifican el cese inmediato de {name}: cualquier signo de reacción alérgica (erupción, dificultad respiratoria, hinchazón facial); cefalea severa persistente o cambios visuales; eventos GI graves (vómitos persistentes, dolor abdominal severo); síntomas cardiovasculares (dolor torácico, palpitaciones); cualquier síntoma claramente nuevo fuera del perfil de efectos secundarios esperado. Detén y busca evaluación médica."),
            ]
        if angle == 'research':
            return [
                (f'Revisión de investigación de {name}: dónde está la evidencia', f"Esta sección sintetiza la literatura publicada sobre {name}, enfocándose en el rigor del diseño del estudio, los tamaños de efecto, y la validez externa."),
                ('Estudios y hallazgos clave', c['evidence']),
                ('Resumen de investigación de mecanismo', c['mechanism']),
                ('Distribución de calidad entre estudios',
                 f"La calidad de investigación de {name} varía ampliamente — desde RCT rigurosos hasta pequeños estudios abiertos, reportes de caso, y anécdotas. La jerarquía por la que deberías ponderar los hallazgos: RCT doble ciego > RCT abierto > estudios de cohorte > series de casos > anécdotas."),
                ('Temas recurrentes',
                 f"Temas que se repiten en revisiones de {name}: (1) la evidencia mecanística suele ser fuerte mientras que la evidencia clínica es más débil — esa brecha desde el efecto-animal al punto-final-clínico-humano está en todas partes. (2) Los estudios cortos dominan; los datos a largo plazo son mayormente ausentes. (3) La variación de respuesta individual es grande — los promedios poblacionales oscurecen diferencias individuales sustanciales. (4) La replicación independiente a menudo falta."),
                ('Limitaciones metodológicas',
                 f"Limitaciones que afectan la base de investigación de {name}: tamaños de muestra pequeños (la mayoría N<100), duración limitada del estudio (<12 semanas), replicación independiente insuficiente, sesgos de selección de pacientes, medición subjetiva de puntos finales."),
                ('Lo que esto significa para decisiones prácticas',
                 f"Para decisiones sobre la investigación de {name}: entiende las diferencias en fuerza de evidencia, evita tratar la evidencia animal o mecanística como clínicamente equivalente, mantén expectativas realistas. Las decisiones deberían descansar en evidencia publicada + monitoreo de respuesta individual, no en fuentes únicas."),
            ]
    elif lang == 'pt':
        cross = (f"Compostos relacionados (para pesquisa adicional): {', '.join(related[:3])}." if related else "")
        if angle in ('guide', 'general', 'comprehensive'):
            return [
                (f'O que é {name}?', c['overview']),
                ('Como funciona: mecanismo', c['mechanism']),
                ('O que a pesquisa mostra', c['evidence']),
                ('Dosagem e administração', c['dosing']),
                ('Perfil de segurança e efeitos colaterais', c['safety']),
                ('Realidade regulatória',
                 f"Nos EUA e na maioria das jurisdições, {name} não é aprovado para uso humano — é vendido como produto químico de pesquisa ou reagente de laboratório. As diretrizes de farmácias de compounding 503A vs 503B foram endurecidas em 2023-2024. A lista de proibidos da WADA também importa para atletas. O status regulatório muda com o tempo; verifique as regras atuais antes de iniciar qualquer protocolo."),
                ('Considerações práticas',
                 f"Algumas coisas que aparecem repetidamente com pesquisa de {name}: a variância de qualidade entre fornecedores é real e não sutil. Verificação HPLC independente por terceiros, lote a lote (não 'amostras representativas'), é o único que te dá potência confiável. A maioria dos protocolos começa na extremidade baixa da faixa de dosagem e titula para cima. A documentação importa mais do que se pensa. {cross}"),
            ]
        if angle == 'faq':
            return [
                (f'Perguntas frequentes sobre {name}', f"O que segue são as perguntas sobre {name} que aparecem mais frequentemente em discussões da comunidade de pesquisa, com respostas baseadas em literatura publicada e mecanismos conhecidos."),
                (f'O que é {name}?', c['overview']),
                (f'Qual dose é típica em protocolos de pesquisa?', c['dosing']),
                (f'Como funciona realmente?', c['mechanism']),
                (f'Quais são as principais considerações de segurança?', c['safety']),
                (f'Quão forte é a base de evidência?', c['evidence']),
                (f'{name} é aprovado pela FDA?',
                 f"Depende do composto. Alguns peptídeos do panorama amplo são aprovados pela FDA (semaglutida, tirzepatida, tesamorelina, setmelanotida), mas a maioria dos peptídeos de pesquisa não — são vendidos como 'produtos químicos de pesquisa,' apenas para uso laboratorial, não para consumo humano. A distinção 503A vs 503B em farmácias de compounding também importa."),
            ]
        if angle == 'dosing':
            return [
                (f'Dosagem de {name}: o que a pesquisa diz', c['dosing']),
                (f'Como o {name} funciona (e por que isso importa para a dose)', c['mechanism']),
                ('Por que a variação individual importa',
                 f"As doses 'padrão' de pesquisa para {name} representam médias populacionais — as respostas individuais variam substancialmente. Idade, peso, sexo, níveis basais de biomarcadores, pontos finais alvo, e condições de saúde existentes influenciam como a dosagem ótima se parece."),
                ('Por que a titulação supera ir direto ao alvo',
                 f"Com {name}, aumentar gradualmente quase sempre supera saltar para sua dose alvo. A titulação te permite (1) caracterizar sua curva de resposta individual, (2) detectar problemas de sensibilidade antes que se tornem problemas, (3) minimizar eventos adversos precoces, (4) construir um protocolo sustentável a longo prazo."),
                ('Considerações de segurança relacionadas à dose', c['safety']),
                ('Documentação', f"Registrar dose, momento, local da injeção, fatores concomitantes e respostas observadas é a base da pesquisa a longo prazo de {name}."),
            ]
        if angle == 'safety' or angle == 'side-effects':
            return [
                (f'Segurança de {name}: uma revisão honesta', c['safety']),
                ('Entendendo os efeitos colaterais através do mecanismo', c['mechanism']),
                ('Contraindicações e interações medicamentosas',
                 f"Com {name}, as contraindicações que você verá mais frequentemente: malignidade conhecida ou suspeita (especialmente compostos que tocam vias proliferativas), doença endócrina grave não controlada, gravidez ou amamentação, crianças a menos que aprovado, deterioração hepática ou renal grave."),
                ('Como a dose se relaciona com efeitos colaterais',
                 f"Os efeitos colaterais com {name} tipicamente estão relacionados à dose. Começar com a dose mínima efetiva é a estratégia única mais efetiva de redução de eventos adversos."),
                ('Estratégia de monitoramento',
                 f"Para protocolos mais longos de pesquisa com {name}, uma abordagem estruturada de monitoramento: (1) Avaliação basal — biomarcadores relevantes, severidade dos sintomas, medidas funcionais alvo. (2) Laboratórios periódicos baseados no mecanismo do composto. (3) Acompanhamento de sintomas — registros estruturados."),
                ('Quando parar imediatamente',
                 f"Sintomas que justificam cessação imediata de {name}: qualquer sinal de reação alérgica; cefaleia severa persistente ou alterações visuais; eventos GI graves; sintomas cardiovasculares; qualquer sintoma claramente novo fora do perfil esperado de efeitos colaterais."),
            ]
        if angle == 'research':
            return [
                (f'Revisão de pesquisa de {name}: onde está a evidência', f"Esta seção sintetiza a literatura publicada sobre {name}, focando no rigor do desenho do estudo, nos tamanhos de efeito, e na validade externa."),
                ('Estudos e achados-chave', c['evidence']),
                ('Resumo de pesquisa de mecanismo', c['mechanism']),
                ('Distribuição de qualidade entre estudos',
                 f"A qualidade da pesquisa de {name} varia amplamente — desde RCT rigorosos até pequenos estudos abertos, relatos de caso, e anedotas."),
                ('Temas recorrentes',
                 f"Temas que se repetem em revisões de {name}: (1) a evidência mecanística geralmente é forte enquanto a evidência clínica é mais fraca. (2) Estudos curtos dominam; dados a longo prazo são ausentes. (3) A variação de resposta individual é grande. (4) Replicação independente frequentemente falta."),
                ('O que isso significa para decisões práticas',
                 f"Para decisões sobre pesquisa de {name}: entenda as diferenças em força de evidência, evite tratar evidência animal ou mecanística como clinicamente equivalente, mantenha expectativas realistas."),
            ]
    elif lang == 'fr':
        cross = (f"Composés apparentés (pour recherche complémentaire) : {', '.join(related[:3])}." if related else "")
        if angle in ('guide', 'general', 'comprehensive'):
            return [
                (f'Qu\'est-ce que {name} ?', c['overview']),
                ('Comment ça fonctionne : mécanisme', c['mechanism']),
                ('Ce que la recherche montre', c['evidence']),
                ('Dosage et administration', c['dosing']),
                ('Profil de sécurité et effets secondaires', c['safety']),
                ('Réalité réglementaire',
                 f"Aux États-Unis et dans la plupart des juridictions, {name} n'est pas approuvé pour l'usage humain — il est vendu comme produit chimique de recherche ou réactif de laboratoire. Les directives des pharmacies de compounding 503A vs 503B se sont durcies en 2023-2024. La liste des produits interdits par l'AMA importe aussi pour les athlètes. Le statut réglementaire évolue dans le temps ; vérifiez les règles actuelles avant de démarrer tout protocole de recherche."),
                ('Considérations pratiques',
                 f"Quelques éléments qui reviennent en boucle dans la recherche sur {name} : la variance de qualité entre fournisseurs est réelle et pas subtile. La vérification HPLC indépendante par tiers, lot par lot (pas 'échantillons représentatifs'), est la seule chose qui vous donne une puissance fiable. La plupart des protocoles commencent à l'extrémité basse de la plage de dosage et titrent vers le haut. La documentation compte plus qu'on ne le pense. {cross}"),
            ]
        if angle == 'faq':
            return [
                (f'Questions fréquentes sur {name}', f"Ce qui suit, ce sont les questions sur {name} qui reviennent le plus souvent dans les discussions de la communauté de recherche, avec des réponses basées sur la littérature publiée et les mécanismes connus."),
                (f'Qu\'est-ce que {name} ?', c['overview']),
                (f'Quelle dose est typique dans les protocoles de recherche ?', c['dosing']),
                (f'Comment ça fonctionne vraiment ?', c['mechanism']),
                (f'Quelles sont les principales considérations de sécurité ?', c['safety']),
                (f'Quelle est la solidité de la base de preuves ?', c['evidence']),
                (f'{name} est-il approuvé par la FDA ?',
                 f"Cela dépend du composé. Quelques peptides dans le paysage large sont approuvés FDA (sémaglutide, tirzépatide, tésamoréline, setmélanotide), mais la plupart des peptides de recherche ne le sont pas — ils sont vendus comme 'produits chimiques de recherche,' usage de laboratoire uniquement, pas pour la consommation humaine."),
            ]
        if angle == 'dosing':
            return [
                (f'Dosage de {name} : ce que dit la recherche', c['dosing']),
                (f'Comment fonctionne {name} (et pourquoi ça importe pour la dose)', c['mechanism']),
                ('Pourquoi la variation individuelle compte',
                 f"Les doses 'standard' de recherche pour {name} représentent des moyennes de population — les réponses individuelles varient substantiellement. L'âge, le poids, le sexe, les niveaux de base des biomarqueurs, les critères d'évaluation cibles, et les conditions de santé existantes influencent ce à quoi ressemble le dosage optimal."),
                ('Pourquoi la titration bat le saut direct vers la cible',
                 f"Avec {name}, augmenter graduellement bat presque toujours sauter vers votre dose cible. La titration vous permet (1) de caractériser votre courbe de réponse individuelle, (2) d'attraper les problèmes de sensibilité avant qu'ils ne deviennent des problèmes, (3) de minimiser les événements indésirables précoces, (4) de construire un protocole durable à long terme."),
                ('Considérations de sécurité liées à la dose', c['safety']),
                ('Documentation', f"Enregistrer la dose, le moment, le site d'injection, les facteurs concomitants et les réponses observées est la base de la recherche à long terme de {name}."),
            ]
        if angle == 'safety' or angle == 'side-effects':
            return [
                (f'Sécurité de {name} : une revue honnête', c['safety']),
                ('Comprendre les effets secondaires à travers le mécanisme', c['mechanism']),
                ('Contre-indications et interactions médicamenteuses',
                 f"Avec {name}, les contre-indications que vous verrez le plus souvent : malignité connue ou suspectée (en particulier les composés touchant des voies prolifératives), maladie endocrinienne grave non contrôlée, grossesse ou allaitement, enfants sauf si approuvé, insuffisance hépatique ou rénale sévère."),
                ('Comment la dose se rapporte aux effets secondaires',
                 f"Les effets secondaires avec {name} sont typiquement liés à la dose. Commencer à la dose minimale efficace est la stratégie la plus efficace de réduction des événements indésirables."),
                ('Stratégie de surveillance',
                 f"Pour des protocoles plus longs de recherche avec {name}, une approche structurée de surveillance : (1) Évaluation de base — biomarqueurs pertinents, sévérité des symptômes, mesures fonctionnelles cibles. (2) Laboratoires périodiques basés sur le mécanisme du composé. (3) Suivi des symptômes — registres structurés."),
                ('Quand arrêter immédiatement',
                 f"Symptômes qui justifient l'arrêt immédiat de {name} : tout signe de réaction allergique ; céphalée sévère persistante ou changements visuels ; événements digestifs graves ; symptômes cardiovasculaires ; tout symptôme clairement nouveau en dehors du profil attendu d'effets secondaires."),
            ]
        if angle == 'research':
            return [
                (f'Revue de recherche sur {name} : où en est la preuve', f"Cette section synthétise la littérature publiée sur {name}, en se concentrant sur la rigueur du design d'étude, les tailles d'effet, et la validité externe."),
                ('Études et résultats clés', c['evidence']),
                ('Résumé de recherche sur le mécanisme', c['mechanism']),
                ('Distribution de qualité entre études',
                 f"La qualité de recherche sur {name} varie largement — d'essais cliniques randomisés rigoureux à de petites études ouvertes, des rapports de cas, et des anecdotes."),
                ('Thèmes récurrents',
                 f"Thèmes qui reviennent dans les revues de {name} : (1) les preuves mécanistiques sont souvent solides tandis que les preuves cliniques sont plus faibles. (2) Les études courtes dominent ; les données à long terme sont surtout absentes. (3) La variation de réponse individuelle est grande. (4) La réplication indépendante manque souvent."),
                ('Ce que cela signifie pour les décisions pratiques',
                 f"Pour les décisions concernant la recherche sur {name} : comprenez les différences de force des preuves, évitez de traiter les preuves animales ou mécanistiques comme cliniquement équivalentes, maintenez des attentes réalistes."),
            ]

    # Default
    return [
        (f'{name}', c['overview']),
        ('Mechanism', c['mechanism']),
        ('Evidence', c['evidence']),
        ('Dosing', c['dosing']),
        ('Safety', c['safety']),
    ]


def parse_aspect_from_slug(slug):
    s = slug.replace('.html', '')
    aspect_map = {
        'guide': 'guide', 'faq': 'faq', 'dosage': 'dosing',
        'safety': 'safety', 'side-effects': 'safety', 'research': 'research',
        'reviews': 'research',
    }
    for ck in COMPOUNDS.keys():
        if s == ck or s == ck + '-guide':
            return ck, 'guide'
        if s.startswith(ck + '-'):
            rem = s[len(ck) + 1:]
            if rem in aspect_map:
                return ck, aspect_map[rem]
            return None, None
    return None, None


def build_quick_answer(c):
    base = c.get('quick_answer', c['overview'][:300])
    if len(base) > 320:
        base = base[:320].rsplit('.', 1)[0] + '.'
    return base


def build_faq_schema(c, paragraphs, lang):
    qa = []
    for h2, p in paragraphs:
        if '?' in h2 or '¿' in h2 or 'Q:' in h2:
            qa.append((h2, p))
    if len(qa) < 3:
        if lang == 'es':
            qa = [
                (f'¿Qué es {c["name"]}?', c['overview'][:400]),
                (f'¿Cómo funciona {c["name"]}?', c['mechanism'][:400]),
                (f'¿Cuáles son las dosis de investigación típicas?', c['dosing'][:400]),
                (f'¿Cuáles son las principales consideraciones de seguridad?', c['safety'][:400]),
            ]
        elif lang == 'pt':
            qa = [
                (f'O que é {c["name"]}?', c['overview'][:400]),
                (f'Como funciona o {c["name"]}?', c['mechanism'][:400]),
                (f'Quais são as doses típicas de pesquisa?', c['dosing'][:400]),
                (f'Quais são as principais considerações de segurança?', c['safety'][:400]),
            ]
        else:  # fr
            qa = [
                (f'Qu\'est-ce que {c["name"]} ?', c['overview'][:400]),
                (f'Comment fonctionne {c["name"]} ?', c['mechanism'][:400]),
                (f'Quelles sont les doses typiques de recherche ?', c['dosing'][:400]),
                (f'Quelles sont les principales considérations de sécurité ?', c['safety'][:400]),
            ]
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa[:6]
        ]
    }


DISCLAIMER_TEXT = {
    'es': '<div style="background:#fef2f2;border:1px solid #fecaca;border-radius:10px;padding:20px 24px;margin:24px 0;font-size:13px;color:#991b1b;"><p style="font-weight:700;">Aviso médico</p><p>Este artículo es solo para fines informativos y educativos. Los compuestos discutidos son productos químicos de investigación no aprobados por la FDA para uso humano. Siempre consulte a un profesional de la salud antes de considerar cualquier protocolo de péptidos.</p></div>',
    'pt': '<div style="background:#fef2f2;border:1px solid #fecaca;border-radius:10px;padding:20px 24px;margin:24px 0;font-size:13px;color:#991b1b;"><p style="font-weight:700;">Aviso médico</p><p>Este artigo é apenas para fins informativos e educacionais. Os compostos discutidos são produtos químicos de pesquisa não aprovados pela FDA para uso humano. Sempre consulte um profissional de saúde antes de considerar qualquer protocolo de peptídeos.</p></div>',
    'fr': '<div style="background:#fef2f2;border:1px solid #fecaca;border-radius:10px;padding:20px 24px;margin:24px 0;font-size:13px;color:#991b1b;"><p style="font-weight:700;">Avertissement médical</p><p>Cet article est uniquement à des fins d\'information et d\'éducation. Les composés discutés sont des produits chimiques de recherche non approuvés par la FDA pour l\'usage humain. Consultez toujours un professionnel de la santé avant d\'envisager tout protocole de peptides.</p></div>',
}

QUICK_ANSWER_LABEL = {
    'es': 'Respuesta rápida',
    'pt': 'Resposta rápida',
    'fr': 'Réponse rapide',
}

RELATED_HEADER = {
    'es': 'Compuestos de investigación relacionados',
    'pt': 'Compostos de pesquisa relacionados',
    'fr': 'Composés de recherche apparentés',
}

RELATED_INTRO = {
    'es': 'Si estás investigando',
    'pt': 'Se você está pesquisando',
    'fr': 'Si vous recherchez',
}


def build_article(slug, lang):
    compound_key, aspect = parse_aspect_from_slug(slug)
    if not compound_key or compound_key not in COMPOUNDS:
        return None, None
    c_lang = COMPOUNDS[compound_key].get(lang)
    if not c_lang:
        return None, None

    paragraphs = aspect_paragraphs(aspect, c_lang, lang)
    quick = build_quick_answer(c_lang)
    faq = build_faq_schema(c_lang, paragraphs, lang)

    html = '<article class="article-body">'
    html += DISCLAIMER_TEXT[lang]
    html += f'<div class="quick-answer"><strong>{QUICK_ANSWER_LABEL[lang]}:</strong> {quick}</div>'
    for h2, p in paragraphs:
        html += f'<h2>{h2}</h2>\n<p>{p}</p>\n'

    related = c_lang.get('related', [])
    if related:
        html += f'<h2>{RELATED_HEADER[lang]}</h2>\n<p>{RELATED_INTRO[lang]} {c_lang["name"]}: '
        link_parts = []
        for rk in related[:4]:
            rc = COMPOUNDS.get(rk, {}).get(lang)
            rname = rc['name'] if rc else rk.replace('-', ' ').upper()
            link_parts.append(f'<a href="/{lang}/{rk}-guide.html">{rname}</a>')
        html += ', '.join(link_parts) + '.</p>'

    html += '</article>'
    return html, faq


def process_file(path, lang):
    html = path.read_text(encoding='utf-8', errors='ignore')
    new_article, faq = build_article(path.stem, lang)
    if new_article is None:
        return False, 'no-cornerstone-match'

    pat_a = re.compile(r'(<article[^>]*>)(.*?)(</article>)', re.DOTALL)
    if not pat_a.search(html):
        return False, 'no-article-tag'
    new_html = pat_a.sub(lambda _: new_article, html, count=1)

    if faq and 'FAQPage' not in new_html:
        s = f'<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>'
        new_html = new_html.replace('</head>', s + '\n</head>', 1)

    if new_html == html:
        return False, 'no-change'
    path.write_text(new_html, encoding='utf-8')
    return True, 'replaced'


def main():
    only_lang = os.environ.get('LANG', None)
    langs = [only_lang] if (only_lang and only_lang in LANGUAGES) else LANGUAGES

    grand_fixed = 0
    for lang in langs:
        d = ROOT / lang
        if not d.is_dir():
            continue
        # Build target list: cornerstone compounds × cornerstone aspects
        targets = []
        for ck in COMPOUNDS.keys():
            if not COMPOUNDS[ck].get(lang):
                continue
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
                changed, action = process_file(path, lang)
                if changed:
                    fixed += 1
            except Exception as e:
                print(f"ERR {lang}/{t}: {e}", file=sys.stderr)
        print(f"{lang}: {fixed}/{len(targets)} cornerstone files replaced")
        grand_fixed += fixed
    print(f"\n=== Phase 7 grand total: {grand_fixed} cornerstone files ===")


if __name__ == '__main__':
    main()
