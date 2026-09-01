"""
Seed French (fr) translations for all live EN pages using wagtail-localize's
copy_for_translation API.

Usage:
    python manage.py seed_fr_content
    python manage.py seed_fr_content --overwrite   # re-apply even if FR page exists

Run once after the English content is live and the FR locale exists.
"""
from django.core.management.base import BaseCommand
from wagtail.models import Locale, Page

from home.models import HomePage, AboutPage, ContactPage, LegalPage
from portfolio.models import (
    ServiceIndexPage, ServicePage,
    PortfolioIndexPage, ProjectPage,
    PlatformIndexPage,
)


# ---------------------------------------------------------------------------
# French strings — Quebec professional French
# ---------------------------------------------------------------------------

HOME_FR = dict(
    title="Accueil",
    seo_title="Catalystdev — Conception web Montréal",
    search_description="Agence numérique montréalaise spécialisée en développement web, stratégie de marque et stratégie numérique. Demandez une démo.",
    parralax_Subtitle="Agence numérique",
    parralax_Title="Des expériences numériques pensées pour durer",
    parralax_ButtonText="Voir nos réalisations",
    about_Subtitle="Qui sommes-nous",
    about_Title="Un studio boutique pour les PME",
    about_Description=(
        "Fondé à Montréal en 2019, Catalystdev conçoit des expériences numériques "
        "intentionnelles, durables et profondément ancrées dans les réalités des "
        "entreprises qui les utilisent. Nous travaillons directement avec nos clients — "
        "souvent en prolongement de leur équipe — pour transformer la complexité en clarté "
        "et les idées en outils qui fonctionnent."
    ),
    about_ButtonText="En savoir plus",
    services_title="Nos services",
    portfolio_one_Subtitle="Développement web",
    portfolio_one_Title="Des plateformes sur mesure",
    portfolio_one_Description=(
        "De la page vitrine au portail ERP, nous construisons des outils numériques "
        "adaptés à vos opérations, pas l'inverse."
    ),
    portfolio_one_ButtonText="Voir nos projets",
    portfolio_two_Subtitle="Image de marque",
    portfolio_two_Title="Une identité qui tient dans le temps",
    portfolio_two_Description=(
        "Nous créons des systèmes d'identité visuelle cohérents — logos, typographie, "
        "couleurs — qui s'appliquent uniformément sur tous vos supports."
    ),
    portfolio_two_ButtonText="Découvrir",
    portfolio_three_Subtitle="Stratégie numérique",
    portfolio_three_Title="Visibilité et croissance en ligne",
    portfolio_three_Description=(
        "SEO, publicité payante, médias sociaux et stratégie de lancement : "
        "nous transformons votre présence en ligne en levier de croissance mesurable."
    ),
    portfolio_three_ButtonText="En savoir plus",
    contact_title="Travaillons ensemble",
    contact_subtitle="Décrivez-nous votre projet et nous reviendrons vers vous personnellement.",
    contact_button_text="Nous contacter",
    contact_address="4388 Rue Saint-Denis #182, Montréal, QC H2J 2L1",
)

ABOUT_FR = dict(
    title="À propos",
    seo_title="À propos de Catalystdev",
    search_description="Découvrez l'histoire, les valeurs et l'approche de Catalystdev, agence numérique montréalaise.",
    about_sub_title="Notre histoire",
    about_text=(
        "<p>Catalystdev est née en 2019, à la croisée de la curiosité, de la créativité "
        "et du code. Basés à Montréal, nous avons débuté avec une conviction simple : les "
        "expériences numériques doivent être intentionnelles, durables et profondément "
        "alignées avec les personnes qui les utilisent.</p>"
        "<p>Nos débuts ont été honnêtes. Nous réparions des sites WordPress brisés, "
        "rafraîchissions de petites pages vitrines et aidions les PME à donner du sens à "
        "leur présence en ligne. Ces premiers projets nous ont appris à écouter, à valoriser "
        "la clarté plutôt que la complexité, et à construire des solutions qui servent "
        "réellement les entreprises.</p>"
        "<p>Au fil du temps, notre ambition a grandi. Nous avons évolué des simples sites "
        "web vers la création de plateformes complètes pour des organismes à but non "
        "lucratif — des outils conçus pour soutenir leurs opérations et évoluer avec leur "
        "mission. En 2023, nous avons intégré Laravel à notre boîte à outils, puis Django "
        "en 2025, apportant structure, fiabilité et maintenabilité à chaque plateforme.</p>"
        "<p>Aujourd'hui, Catalystdev est un studio boutique pour les PME. Nous travaillons "
        "en étroite collaboration avec nos clients — souvent comme une extension de leur "
        "équipe — pour transformer la complexité en clarté et les idées en outils qui "
        "fonctionnent simplement. Notre vision a toujours été la même : des solutions clés "
        "en main, entièrement intégrées, où le site web, le logiciel, la marque et le "
        "message parlent le même langage.</p>"
    ),
    breadcrumb_home="Accueil",
)

CONTACT_FR = dict(
    title="Contactez-nous",
    seo_title="Contactez Catalystdev",
    search_description="Contactez Catalystdev pour votre projet web, stratégie de marque ou marketing numérique.",
    contact_Title="Écrivez-nous",
    contact_Subtitle=(
        "Nous serions ravis d'avoir de vos nouvelles. Dites-nous comment nous pouvons vous aider."
    ),
    form_Title="Votre projet",
    form_Subtitle=(
        "<p>Pour nous permettre de mieux comprendre vos besoins et d'agir rapidement, "
        "dites-nous dans quel domaine vous souhaitez être accompagné. Que ce soit pour "
        "concevoir votre marque, développer une plateforme numérique ou accroître votre "
        "présence en ligne, nous vous accompagnerons personnellement à chaque étape.</p>"
    ),
    btn_Text="Envoyer",
    box_title="Nos coordonnées",
    box_city="Montréal",
    box_address="4388 Rue Saint-Denis #182",
    faq_title="Questions fréquentes",
    faq_subtitle="Des réponses claires aux questions que vous vous posez",
    breadcrumb_home="Accueil",
    breadcrumb_contact="Contact",
    form_thank_you_text="Merci pour votre message",
    form_other_message_text="Autre précision",
)

PRIVACY_FR = dict(
    title="Politique de confidentialité",
    seo_title="Politique de confidentialité — Catalystdev",
    Legal_sub_title="Politique de confidentialité",
    legal_text=(
        "<p><b>Date d'entrée en vigueur :</b> 8 janvier 2026</p>"
        "<p>Catalystdev (« nous », « notre ») exploite le site web www.catalystdv.com "
        "(le « Service »). Nous nous engageons à protéger votre vie privée. La présente "
        "politique explique comment nous collectons, utilisons, divulguons et protégeons "
        "vos renseignements personnels.</p>"
        "<h3>1. Renseignements que nous collectons</h3>"
        "<p>Nous collectons des renseignements lorsque vous les soumettez volontairement "
        "via des formulaires sur notre site.</p>"
        "<p><b>a. Renseignements personnels</b> : nom complet, adresse courriel, numéro "
        "de téléphone, nom de l'entreprise, et tout autre renseignement fourni dans un "
        "formulaire.</p>"
        "<p><b>b. Données d'utilisation</b> : adresse IP, type de navigateur, pages "
        "visitées et durée de visite, afin de comprendre l'utilisation du Service.</p>"
        "<p><b>c. Témoins et traçage</b> : nous utilisons des témoins (cookies) pour "
        "analyser l'activité et améliorer le Service. Vous pouvez gérer vos préférences "
        "de témoins depuis votre navigateur.</p>"
        "<h3>2. Utilisation des renseignements</h3>"
        "<p>Nous utilisons vos données pour répondre à vos demandes, fournir un soutien "
        "à la clientèle, surveiller et améliorer le Service, communiquer avec vous et "
        "respecter nos obligations légales.</p>"
        "<h3>3. Partage des renseignements</h3>"
        "<p>Nous ne vendons ni ne louons vos données personnelles. Nous pouvons les "
        "partager avec des fournisseurs de services tiers dans la stricte mesure nécessaire "
        "à l'exploitation du Service. Nous pouvons également les divulguer si la loi l'exige.</p>"
        "<h3>4. Conservation des données</h3>"
        "<p>Nous conservons les données personnelles uniquement aussi longtemps que nécessaire "
        "aux fins décrites dans la présente politique ou pour respecter nos obligations légales.</p>"
        "<h3>5. Mineurs</h3>"
        "<p>Notre Service ne s'adresse pas aux personnes de moins de 18 ans. Nous ne "
        "collectons pas sciemment de données auprès de mineurs.</p>"
        "<h3>6. Transferts internationaux</h3>"
        "<p>Vos renseignements peuvent être traités au Canada, où se trouve notre siège "
        "social (<b>4388 Rue Saint-Denis #182, Montréal, QC H2J 2L1, Canada</b>). En "
        "soumettant des renseignements, vous consentez à ces transferts.</p>"
        "<h3>7. Sécurité</h3>"
        "<p>Nous utilisons des mesures raisonnables sur le plan commercial pour protéger "
        "vos données. Toutefois, aucune méthode de transmission sur Internet ou de stockage "
        "électronique n'est entièrement sécurisée.</p>"
        "<h3>8. Modifications de la présente politique</h3>"
        "<p>Nous pouvons mettre à jour cette politique de confidentialité. Les modifications "
        "seront publiées sur cette page avec une nouvelle date d'entrée en vigueur.</p>"
        "<h3>9. Nous joindre</h3>"
        "<p>Pour toute question concernant cette politique, écrivez-nous :<br/>"
        "<b>Courriel :</b> <a href=\"mailto:info@catalystdv.com\">info@catalystdv.com</a><br/>"
        "<b>Adresse :</b> 4388 Rue Saint-Denis #182, Montréal, QC H2J 2L1, Canada</p>"
    ),
)

TERMS_FR = dict(
    title="Conditions d'utilisation",
    seo_title="Conditions d'utilisation — Catalystdev",
    Legal_sub_title="Conditions d'utilisation",
    legal_text=(
        "<p><b>Date d'entrée en vigueur :</b> 8 janvier 2026</p>"
        "<p>Les présentes conditions d'utilisation (« Conditions ») régissent l'utilisation "
        "du site web www.catalystdv.com (le « Service »). En accédant au Service, vous "
        "acceptez d'être lié par ces Conditions.</p>"
        "<h3>1. Utilisation du Service</h3>"
        "<p>Le Service est fourni par Catalystdev, une agence numérique basée à Montréal, "
        "Canada. Vous acceptez d'utiliser le Service uniquement à des fins légales et "
        "conformes aux présentes Conditions.</p>"
        "<h3>2. Formulaires — aucune transaction</h3>"
        "<p>Notre site ne traite pas de transactions financières. Vous pouvez soumettre "
        "des renseignements via des formulaires (formulaire de contact, demande de soumission). "
        "Vous acceptez de fournir des renseignements exacts et complets.</p>"
        "<h3>3. Propriété intellectuelle</h3>"
        "<p>Tout le contenu du Service — textes, graphiques, logos, images et logiciels — "
        "est la propriété de Catalystdev ou de ses concédants, et est protégé par les "
        "lois applicables sur la propriété intellectuelle. Toute reproduction, modification "
        "ou distribution sans autorisation écrite est interdite.</p>"
        "<h3>4. Liens vers des tiers</h3>"
        "<p>Le Service peut contenir des liens vers des sites tiers fournis à titre de "
        "commodité. Nous ne contrôlons pas ces sites et déclinons toute responsabilité "
        "quant à leur contenu ou leurs pratiques.</p>"
        "<h3>5. Confidentialité</h3>"
        "<p>L'utilisation du Service est également régie par notre Politique de "
        "confidentialité, incorporée aux présentes Conditions par référence.</p>"
        "<h3>6. Exclusion de garanties</h3>"
        "<p>Le Service est fourni « tel quel » et « selon disponibilité ». Nous ne faisons "
        "aucune garantie, expresse ou implicite, quant au Service ou à son contenu.</p>"
        "<h3>7. Limitation de responsabilité</h3>"
        "<p>Dans toute la mesure permise par la loi, Catalystdev ne sera pas responsable "
        "des dommages indirects, accessoires, spéciaux, consécutifs ou punitifs découlant "
        "de votre utilisation du Service.</p>"
        "<h3>8. Droit applicable</h3>"
        "<p>Les présentes Conditions sont régies par les lois de la province de Québec "
        "et les lois fédérales du Canada applicables.</p>"
        "<h3>9. Modifications</h3>"
        "<p>Nous pouvons réviser ces Conditions en tout temps. Les Conditions révisées "
        "entrent en vigueur dès leur publication. Votre utilisation continue du Service "
        "après toute modification vaut acceptation des nouvelles Conditions.</p>"
        "<h3>10. Nous joindre</h3>"
        "<p>Pour toute question, écrivez-nous :<br/>"
        "<b>Courriel :</b> <a href=\"mailto:info@catalystdv.com\">info@catalystdv.com</a><br/>"
        "<b>Adresse :</b> 4388 Rue Saint-Denis #182, Montréal, QC H2J 2L1, Canada</p>"
    ),
)

# Service pages: keyed by EN title slug -> FR fields
SERVICE_TRANSLATIONS = {
    "brand-guidelines": dict(
        title="Guide de marque",
        seo_title="Guide de marque — Catalystdev",
        service_title="Guide de marque",
        service_subtitle="Le manuel que votre marque respecte même en votre absence",
        service_tagline="La cohérence avant tout",
        service_description=(
            "<p>Une marque ne fonctionne que si elle survit à la distance. Quand des "
            "fichiers sont envoyés à des imprimeurs ou que des collaborateurs créent du "
            "contenu en votre nom, chaque décision renforce ou érode votre image. Un guide "
            "de marque élimine l'interprétation et remplace les décisions arbitraires par "
            "un système reproductible.</p>"
            "<p>Nous ne créons pas des documents décoratifs. Nous produisons une "
            "documentation opérationnelle pour que votre identité se comporte de façon "
            "cohérente sur le web, en impression et en communication.</p>"
        ),
        service_conclusion_title="La structure crée la mémorisation",
        service_conclusion_description=(
            "<p>Votre marque ne devrait pas dépendre d'explications. Elle devrait reposer "
            "sur une structure. Nous la documentons une fois pour que toutes vos futures "
            "productions s'alignent automatiquement — qu'elles soient créées par vous, "
            "un collaborateur, ou quelqu'un que vous n'avez pas encore embauché.</p>"
        ),
    ),
    "overhaul-rebrand": dict(
        title="Refonte de marque",
        seo_title="Refonte et repositionnement de marque — Catalystdev",
        service_title="Refonte de marque",
        service_subtitle="Quand votre entreprise a évolué mais que votre image est restée derrière",
        service_tagline="Continuité sans traîner le passé",
        service_description=(
            "<p>La plupart des entreprises ne deviennent pas soudainement dépassées — "
            "elles croissent de façon inégale. Les services s'élargissent, le positionnement "
            "s'affine, les audiences changent… pourtant la marque reste liée à des décisions "
            "antérieures. Une refonte n'est pas une réinitialisation. C'est une correction.</p>"
            "<p>Nous identifions ce qui détient déjà une reconnaissance et rebâtissons "
            "tout le reste autour de cela, en préservant la familiarité tout en alignant "
            "la perception sur qui vous êtes aujourd'hui.</p>"
        ),
        service_conclusion_title="Devenez ce que vous êtes déjà",
        service_conclusion_description=(
            "<p>Une bonne refonte n'introduit pas une nouvelle entreprise. Elle révèle "
            "celle qui existe déjà. Nous alignons la perception sur la réalité pour que "
            "votre image cesse d'expliquer le passé et commence à soutenir le présent.</p>"
        ),
    ),
    "photographer-identity-system": dict(
        title="Identité visuelle photographe",
        seo_title="Système d'identité pour photographes — Catalystdev",
        service_title="Système d'identité pour photographes",
        service_subtitle="Une signature visuelle qui met en valeur votre travail sans lui faire concurrence",
        service_tagline="La marque qui s'efface",
        service_description=(
            "<p>Les photographes n'ont pas besoin d'une image de marque plus forte — "
            "ils ont besoin d'une présentation plus claire. Une identité de photographe "
            "est construite différemment : au lieu d'ajouter du poids visuel, nous "
            "contrôlons la façon dont la marque s'efface — guidant l'attention vers les "
            "images tout en créant une paternité reconnaissable.</p>"
            "<p>Votre marque devient la structure derrière le travail, et non le sujet "
            "devant lui.</p>"
        ),
        service_conclusion_title="Votre travail reste le héros",
        service_conclusion_description=(
            "<p>L'objectif n'est pas de rendre votre marque visible. L'objectif est de "
            "rendre votre paternité indéniable. Nous construisons un système où chaque "
            "image semble provenir du même regard — avant même que le spectateur lise "
            "votre nom.</p>"
        ),
    ),
    "visual-identity-system": dict(
        title="Système d'identité visuelle",
        seo_title="Système d'identité visuelle — Catalystdev",
        service_title="Système d'identité visuelle",
        service_subtitle="Une marque qui se comporte de façon cohérente sur chaque support",
        service_tagline="Du logo au langage",
        service_description=(
            "<p>Un logo vous identifie. Un système d'identité visuelle vous rend "
            "reconnaissable. La plupart des marques reposent sur des éléments isolés — "
            "un logo, quelques couleurs, une police. Le résultat fonctionne en isolation "
            "mais s'effondre dans l'usage réel.</p>"
            "<p>Un système d'identité visuelle relie chaque décision visuelle en un "
            "langage cohérent. Au lieu de concevoir des pièces, nous concevons un "
            "comportement — comment votre marque apparaît, s'adapte et évolue selon "
            "les contextes.</p>"
        ),
        service_conclusion_title="La cohérence construit la reconnaissance",
        service_conclusion_description=(
            "<p>La reconnaissance ne vient pas de la répétition seule — elle vient d'un "
            "comportement prévisible. Nous construisons une structure visuelle qui permet "
            "à votre marque d'évoluer sans se perdre, de sorte que chaque nouvelle "
            "production renforce la précédente au lieu de la remplacer.</p>"
        ),
    ),
    "business-launch-support": dict(
        title="Lancement et accompagnement",
        seo_title="Lancement d'entreprise et accompagnement — Catalystdev",
        service_title="Lancement et accompagnement d'entreprise",
        service_subtitle="De l'idée au marché avec confiance",
        service_tagline="Un lancement rapide et structuré",
        service_description=(
            "<p>Une bonne idée ne suffit pas — l'exécution compte. Lancer une entreprise "
            "implique de nombreuses pièces mobiles : image de marque, site web, aspects "
            "légaux, opérations et marketing. Nous concevons un processus structuré où "
            "chaque étape mène à une entreprise fonctionnelle et évolutive.</p>"
        ),
        service_conclusion_title="Votre entreprise, entièrement équipée",
        service_conclusion_description=(
            "<p>Nous fournissons les systèmes, la stratégie et le soutien pour transformer "
            "votre idée en entreprise opérationnelle et évolutive — dès le premier jour "
            "et au-delà.</p>"
        ),
    ),
    "paid-advertising": dict(
        title="Publicité payante",
        seo_title="Publicité payante et campagnes — Catalystdev",
        service_title="Publicité payante",
        service_subtitle="Une visibilité immédiate quand le moment compte",
        service_tagline="Rapidité et contrôle",
        service_description=(
            "<p>La croissance organique prend du temps. Parfois, vous avez besoin de "
            "résultats maintenant — un lancement, une offre saisonnière ou atteindre "
            "rapidement un nouveau public. La publicité payante ne consiste pas à dépenser "
            "davantage ; il s'agit de cibler avec précision.</p>"
            "<p>Nous concevons des campagnes où la visibilité mène à l'action, "
            "pas seulement à des impressions.</p>"
        ),
        service_conclusion_title="Une visibilité que vous pouvez activer et désactiver",
        service_conclusion_description=(
            "<p>Une bonne publicité n'est pas une dépense permanente — c'est une "
            "accélération contrôlée. Nous construisons des campagnes qui produisent des "
            "résultats mesurables, de sorte que la promotion devienne un choix stratégique, "
            "pas un pari.</p>"
        ),
    ),
    "seo-analytics": dict(
        title="Référencement et analytique",
        seo_title="SEO et analytique web — Catalystdev",
        service_title="Référencement et analytique",
        service_subtitle="Comprenez qui vous trouve, pourquoi, et ce qu'ils font vraiment",
        service_tagline="La visibilité sans mesure, c'est de la supposition",
        service_description=(
            "<p>Beaucoup d'entreprises investissent dans des sites web et du contenu sans "
            "jamais vraiment savoir ce qui fonctionne. Les chiffres de trafic seuls "
            "n'expliquent pas le comportement. Le référencement amène des visiteurs "
            "qualifiés. L'analytique explique leurs actions. Ensemble, ils transforment "
            "votre site en outil commercial mesurable.</p>"
        ),
        service_conclusion_title="De la présence à la compréhension",
        service_conclusion_description=(
            "<p>Être en ligne, c'est de la visibilité. Savoir ce qui s'y passe, "
            "c'est du contrôle. Nous structurons votre site pour que chaque amélioration "
            "soit guidée par le comportement — transformant votre site en système "
            "qui s'améliore en continu.</p>"
        ),
    ),
    "social-media-campaigns": dict(
        title="Campagnes médias sociaux",
        seo_title="Gestion des médias sociaux — Catalystdev",
        service_title="Campagnes médias sociaux",
        service_subtitle="Engagez, développez et convertissez votre audience là où elle passe son temps",
        service_tagline="Connexion avec intention",
        service_description=(
            "<p>Publier régulièrement ne suffit pas. Pour développer votre marque, vous "
            "avez besoin d'un engagement stratégique. Les campagnes de médias sociaux ne "
            "consistent pas à être le plus fort ; elles consistent à être vu par les "
            "bonnes personnes, avec le bon message, au bon moment.</p>"
            "<p>Nous élaborons des campagnes où chaque publication, histoire ou reel "
            "génère de l'interaction, renforce la confiance et guide les abonnés vers "
            "des actions concrètes.</p>"
        ),
        service_conclusion_title="Un engagement que vous pouvez développer",
        service_conclusion_description=(
            "<p>Les médias sociaux ne sont pas que de la diffusion — c'est un levier de "
            "croissance. Nous construisons des campagnes qui génèrent des interactions "
            "et des conversions mesurables.</p>"
        ),
    ),
    "business-starter-page": dict(
        title="Page vitrine",
        seo_title="Page vitrine pour entreprises — Catalystdev",
        service_title="Page vitrine",
        service_subtitle="Une présence professionnelle en ligne — sans long processus de conception",
        service_tagline="La visibilité ne devrait pas prendre des mois",
        service_description=(
            "<p>Beaucoup d'entreprises retardent le lancement de leur site parce qu'elles "
            "croient que cela nécessite un projet complet. Entre-temps, des clients "
            "potentiels cherchent, comparent et passent à autre chose.</p>"
            "<p>Une page vitrine se concentre sur l'essentiel : qui vous êtes, ce que "
            "vous offrez et comment vous joindre. Rien de plus, rien qui manque. Au lieu "
            "d'attendre un site web parfait, vous obtenez un site fonctionnel immédiatement.</p>"
        ),
        service_conclusion_title="Lancez d'abord, améliorez ensuite",
        service_conclusion_description=(
            "<p>La présence en ligne devrait commencer tôt, pas parfaitement. Cette page "
            "donne à votre entreprise un point d'ancrage professionnel pour que les clients "
            "puissent vous trouver, vous comprendre et vous contacter aujourd'hui.</p>"
        ),
    ),
    "erp-client-portals": dict(
        title="ERP et portails clients",
        seo_title="ERP et portails clients sur mesure — Catalystdev",
        service_title="ERP et portails clients",
        service_subtitle="Remplacez les chaînes de courriels et les tableurs par un système qui fonctionne",
        service_tagline="Vos opérations ne devraient pas dépendre de la mémoire",
        service_description=(
            "<p>La plupart des entreprises ne manquent pas d'outils — elles manquent de "
            "structure. Les demandes arrivent par courriel, les fichiers sont envoyés par "
            "liens, le statut est suivi mentalement, et l'information vit en plusieurs "
            "endroits. Ça fonctionne tant que le volume est bas, puis ça devient "
            "progressivement chaotique.</p>"
            "<p>Un portail centralise l'activité en un seul espace opérationnel. Les "
            "clients savent où soumettre. Les équipes savent où agir. La progression "
            "devient visible. Au lieu de gérer la communication, vous gérez le flux "
            "de travail.</p>"
        ),
        service_conclusion_title="Des flux de travail, pas des conversations",
        service_conclusion_description=(
            "<p>La croissance ne devrait pas multiplier la complexité. Nous construisons "
            "des plateformes opérationnelles qui évoluent avec le volume, pour que plus "
            "d'activité signifie plus de production — pas plus de confusion.</p>"
        ),
    ),
    "online-store-systems": dict(
        title="Boutiques en ligne",
        seo_title="Systèmes de commerce en ligne — Catalystdev",
        service_title="Systèmes de boutique en ligne",
        service_subtitle="Vendez vos produits avec une boutique adaptée à votre entreprise — pas l'inverse",
        service_tagline="Chaque boutique ne fonctionne pas de la même façon",
        service_description=(
            "<p>La plupart des problèmes de commerce électronique ne viennent pas de la "
            "vente elle-même — ils viennent de faire rentrer votre entreprise dans une "
            "boutique qui n'a pas été conçue pour elle. Nous offrons deux approches : "
            "une boutique structurée prête au lancement ou une plateforme de commerce "
            "entièrement personnalisée — choisie selon la façon dont vous opérez réellement.</p>"
        ),
        service_conclusion_title="Conçu pour soutenir la croissance",
        service_conclusion_description=(
            "<p>La bonne boutique n'est pas la plus complexe — c'est celle qui correspond "
            "à votre stade. Nous mettons en place la structure qui vous permet de vendre "
            "aujourd'hui tout en restant évolutive pour demain.</p>"
        ),
    ),
    "photographer-launch-site": dict(
        title="Site de lancement photographe",
        seo_title="Site web pour photographes — Catalystdev",
        service_title="Site de lancement pour photographe",
        service_subtitle="Une présence professionnelle en ligne en jours, pas en mois",
        service_tagline="Votre portfolio mérite mieux que les médias sociaux",
        service_description=(
            "<p>La plupart des photographes dépendent de plateformes qu'ils ne contrôlent "
            "pas. Les algorithmes décident de la visibilité, la compression affecte la "
            "qualité d'image, et les clients naviguent à travers des distractions avant "
            "même d'atteindre votre travail. Un site dédié rétablit la clarté.</p>"
            "<p>Ce service est conçu pour la rapidité et la simplicité. Au lieu d'un long "
            "processus de conception personnalisée, nous déployons une structure éprouvée "
            "spécifiquement conçue pour les photographes — prête à présenter votre "
            "travail professionnellement en un temps record.</p>"
        ),
        service_conclusion_title="Lancez d'abord, peaufinez ensuite",
        service_conclusion_description=(
            "<p>Beaucoup de photographes retardent leur site en attendant la perfection. "
            "Ce service vous offre une base solide immédiatement — une vraie présence "
            "que vous contrôlez — pour que votre travail commence à travailler pour vous "
            "dès maintenant.</p>"
        ),
    ),
    "tax-season-client-hub": dict(
        title="Portail fiscal client",
        seo_title="Portail de saison des impôts — Catalystdev",
        service_title="Portail fiscal client",
        service_subtitle="Un système de collecte structuré pour les déclarations de revenus individuelles au Québec",
        service_tagline="Remplacez le chaos de la saison des impôts par un flux organisé",
        service_description=(
            "<p>Pendant la saison des impôts, la vraie charge de travail n'est pas la "
            "comptabilité — c'est la coordination. Les documents manquants, les courriels "
            "répétés, les mises à jour de statut floues et les fichiers dispersés ralentissent "
            "la préparation plus que les déclarations elles-mêmes.</p>"
            "<p>Le portail centralise l'ensemble du processus de collecte. Les clients "
            "soumettent leurs documents en un seul endroit, répondent à des questionnaires "
            "structurés et voient ce qui est encore requis — sans avoir besoin de vous "
            "contacter. Vous cessez de gérer des conversations et commencez à traiter "
            "des déclarations.</p>"
        ),
        service_conclusion_title="Une saison des impôts plus calme",
        service_conclusion_description=(
            "<p>Plus de clients ne devrait pas signifier plus de stress. Ce portail "
            "structure la période la plus chargée de l'année pour que la préparation "
            "devienne prévisible, vous permettant de vous concentrer sur la précision "
            "plutôt que sur la coordination.</p>"
        ),
    ),
}

# Project pages: keyed by EN title slug -> FR fields
PROJECT_TRANSLATIONS = {
    "accountant-portal": dict(
        title="Portail fiscal",
        seo_title="Portail fiscal — Catalystdev",
        subtitle="<p>Simplifier la saison des impôts avec une expérience numérique sécurisée et centrée sur le client.</p>",
        description=(
            "<p>Le portail fiscal est une plateforme sur mesure conçue pour simplifier "
            "la saison des impôts pour les clients québécois, offrant une façon intuitive, "
            "sécurisée et efficace de gérer les déclarations de revenus personnelles.</p>"
            "<p>Construit sur Laravel, la plateforme s'intègre aux comptes Dropbox des "
            "clients pour faciliter le téléversement et le stockage de documents. Un "
            "questionnaire dynamique guidé assure que chaque utilisateur fournit les "
            "renseignements nécessaires, optimisant les crédits et déductions fiscales.</p>"
        ),
        project_requirement=(
            "<p>Concevoir et développer un portail Laravel sur mesure · Intégration sécurisée "
            "avec Dropbox pour la gestion documentaire · Flux de questions guidées pour "
            "maximiser les crédits fiscaux · Conformité complète avec les programmes de "
            "crédits québécois et la réglementation provinciale · Mises à jour continues "
            "pour suivre les changements fiscaux et réglementaires</p>"
        ),
        project_result=(
            "<p>Le lancement du portail fiscal a transformé le flux de travail de la saison "
            "des impôts du client. La gestion centralisée des documents, des questions et "
            "des déclarations a réduit la charge administrative, tandis que le cadre "
            "flexible de Laravel permet à la plateforme d'évoluer avec les réglementations "
            "fiscales en vigueur.</p>"
        ),
        info_description="Description",
        info_requirement="Exigences",
        info_client="Client",
        info_industry="Secteur",
        info_services="Services",
        info_platforms="Plateformes",
        info_date="Date",
        info_website="Site web",
        btn_text="Voir le projet",
        project_result_title="Résultats",
    ),
    "alternative-naissance": dict(
        title="Alternative Naissance",
        seo_title="Alternative Naissance — Catalystdev",
        subtitle="<p>Renforcer le soutien à la naissance en communauté grâce à une plateforme numérique sur mesure.</p>",
        description=(
            "<p>Alternative Naissance est un groupe communautaire autonome à but non "
            "lucratif qui offre, depuis 1982, des activités et services pour humaniser "
            "la naissance et renforcer la vie familiale et communautaire.</p>"
            "<p>L'objectif était de remplacer un système vieux d'une décennie par une "
            "plateforme moderne construite sur Wagtail, conçue pour répondre aux besoins "
            "opérationnels spécifiques d'Alternative Naissance : gestion des demandes "
            "clients, planification et coordination du bénévolat.</p>"
        ),
        project_requirement=(
            "<p>Concevoir et développer une plateforme Wagtail sur mesure · Gérer les "
            "demandes d'accompagnement, la planification et la coordination des bénévoles "
            "· Remplacer un système vieux de dix ans par une solution moderne et évolutive "
            "· Assurer l'accessibilité pour le personnel et les bénévoles</p>"
        ),
        project_result=(
            "<p>Le lancement de la nouvelle plateforme Alternative Naissance a modernisé "
            "les opérations de l'organisation, permettant une gestion plus rapide et plus "
            "efficace des demandes d'accompagnement à la naissance et en post-partum. En "
            "remplaçant le système obsolète par une solution Wagtail sur mesure, Alternative "
            "Naissance a renforcé sa capacité à servir la communauté.</p>"
        ),
        info_description="Description",
        info_requirement="Exigences du projet",
        info_client="Client",
        info_industry="Secteur",
        info_services="Services",
        info_platforms="Plateformes",
        info_date="Date",
        info_website="Site web",
        btn_text="En savoir plus",
        project_result_title="Résultats",
    ),
    "catalystdev-content-production": dict(
        title="Production de contenu Catalystdev",
        seo_title="Production de contenu — Catalystdev",
        subtitle="<p>Créer du contenu engageant et humoristique avec une touche professionnelle.</p>",
        description=(
            "<p>Catalystdev produit des vidéos courtes de style sketch pour Instagram et "
            "TikTok, mêlant créativité, humour et la personnalité authentique de l'équipe. "
            "Le projet visait à élever la présence sur les médias sociaux tout en mettant "
            "en valeur le talent et la culture de Catalystdev à travers du contenu "
            "divertissant.</p>"
            "<p>Le contenu a été produit en collaboration avec l'équipe de Catalystdev "
            "et filmé au studio partenaire Maison Lior, avec des caméras professionnelles "
            "pour garantir des visuels et un son de haute qualité.</p>"
        ),
        project_requirement=(
            "<p>Produire des vidéos courtes optimisées pour Instagram et TikTok · "
            "Inclure des membres de l'équipe Catalystdev · Capturer humour et créativité "
            "en format court · Tournage au studio Maison Lior avec équipement professionnel</p>"
        ),
        project_result=(
            "<p>Les vidéos ont rapidement stimulé l'engagement sur les médias sociaux, "
            "mettant en valeur le côté créatif et accessible de Catalystdev. En combinant "
            "une production professionnelle avec des sketchs authentiques et humoristiques, "
            "le contenu a résonné auprès du public et renforcé la visibilité de la marque.</p>"
        ),
        info_description="Description",
        info_requirement="Exigences",
        info_client="Client",
        info_industry="Secteur",
        info_services="Services",
        info_platforms="Plateformes",
        info_date="Date",
        info_website="Site web",
        btn_text="Voir le projet",
        project_result_title="Résultats",
    ),
    "brand-project": dict(  # Chez Specter — renamed to anonymize
        title="Projet de marque e-commerce",
        seo_title="Projet e-commerce — Catalystdev",
        subtitle="<p>Créer une identité de marque cohérente et une expérience e-commerce fluide.</p>",
        description=(
            "<p>Ce projet de marque créative centrait sur le développement d'une identité "
            "visuelle unifiée tout en créant un écosystème numérique et opérationnel "
            "capable de soutenir plusieurs lignes de produits et canaux de vente.</p>"
            "<p>Nous avons coordonné le système visuel de la marque, incluant logos, "
            "maquettes d'emballage et esthétique globale, pour assurer la cohérence sur "
            "tous les points de contact. Le site web personnalisé, construit avec Wagtail "
            "et Django Oscar, s'intègre à des plateformes tierces via des API pour une "
            "gestion centralisée des produits et des commandes.</p>"
        ),
        project_requirement=(
            "<p>Concevoir et coordonner une identité visuelle cohérente · Construire un "
            "site e-commerce personnalisé · Créer des maquettes d'emballage · Intégrer "
            "des API tierces pour centraliser les opérations · Automatiser la génération "
            "d'étiquettes d'expédition et le traitement des paiements</p>"
        ),
        project_result=(
            "<p>La plateforme unifie l'identité de marque et le flux de travail opérationnel "
            "en un système unique et évolutif. Les API intégrées, les processus automatisés "
            "et le design cohérent positionnent la marque pour un lancement fluide et une "
            "gestion efficace des commandes.</p>"
        ),
        info_description="Description",
        info_requirement="Exigences",
        info_client="Client",
        info_industry="Secteur",
        info_services="Services",
        info_platforms="Plateformes",
        info_date="Date",
        info_website="Site web",
        btn_text="Voir le projet",
        project_result_title="Résultats",
    ),
    "parts-boss": dict(
        title="Parts Boss",
        seo_title="Parts Boss — Catalystdev",
        subtitle="<p>Soutenir la croissance multicanal avec une présence e-commerce dédiée.</p>",
        description=(
            "<p>PartsBoss est un détaillant canadien de pièces automobiles avec un "
            "historique de ventes éprouvé sur eBay. Bien que le succès sur les marchés "
            "tiers ait validé la demande, il limitait le contrôle de la marque, la "
            "fidélisation des clients et la croissance à long terme.</p>"
            "<p>Nous avons conçu et développé un site e-commerce WordPress + WooCommerce "
            "qui s'intègre parfaitement à l'écosystème eBay existant du client. "
            "L'inventaire, les commandes et l'expédition sont synchronisés en temps réel, "
            "permettant à l'équipe de tout gérer depuis un seul système.</p>"
        ),
        project_requirement=(
            "<p>Concevoir et développer un site e-commerce WordPress · Intégration "
            "WooCommerce pour les commandes, paiements et expéditions · Synchronisation "
            "eBay pour l'inventaire et les listes de produits · Gestion centralisée des "
            "commandes · Structure SEO pour la croissance organique</p>"
        ),
        project_result=(
            "<p>Le lancement du site PartsBoss a rapidement démontré la valeur de "
            "dépasser les marchés tiers. En quelques jours, la plateforme a généré ses "
            "premières ventes directes. Les initiatives SEO continues augmentent la "
            "visibilité organique et génèrent un trafic qualifié constant.</p>"
        ),
        info_description="Description",
        info_requirement="Exigences",
        info_client="Client",
        info_industry="Secteur",
        info_services="Services",
        info_platforms="Plateformes",
        info_date="Date",
        info_website="Site web",
        btn_text="Voir le projet",
        project_result_title="Résultats",
    ),
    "wheel-boys": dict(
        title="Wheel-Boys",
        seo_title="Wheel-Boys — Catalystdev",
        subtitle="<p>Soutenir la croissance multicanal avec une présence e-commerce dédiée.</p>",
        description=(
            "<p>Wheel-Boys est un détaillant canadien spécialisé dans les roues "
            "d'automobiles, avec une forte présence sur eBay. L'objectif était de "
            "passer de la dépendance envers les plateformes tierces à une boutique "
            "numérique entièrement propriétaire — sans interrompre les ventes quotidiennes.</p>"
            "<p>Nous avons conçu et développé un site e-commerce WordPress + WooCommerce "
            "qui s'intègre parfaitement à la configuration eBay existante de Wheel-Boys. "
            "L'inventaire, les commandes et l'expédition sont synchronisés en temps réel.</p>"
        ),
        project_requirement=(
            "<p>Concevoir et développer un site e-commerce WordPress · Intégration "
            "WooCommerce · Synchronisation eBay · Gestion centralisée · Architecture de "
            "produits évolutive · Structure SEO optimisée</p>"
        ),
        project_result=(
            "<p>Le lancement du site Wheel-Boys a rapidement mis en évidence les avantages "
            "de dépasser les marchés tiers. La plateforme a généré ses premières ventes "
            "directes en quelques jours. Les initiatives SEO continues stimulent la "
            "visibilité organique et renforcent la marque Wheel-Boys.</p>"
        ),
        info_description="Description",
        info_requirement="Exigences",
        info_client="Client",
        info_industry="Secteur",
        info_services="Services",
        info_platforms="Plateformes",
        info_date="Date",
        info_website="Site web",
        btn_text="Voir le projet",
        project_result_title="Résultats",
    ),
}


class Command(BaseCommand):
    help = "Seed French (fr) translations for all live English pages."

    def add_arguments(self, parser):
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Re-apply FR content even if a FR translation already exists.",
        )

    def handle(self, *args, **options):
        overwrite = options["overwrite"]
        try:
            fr_locale = Locale.objects.get(language_code="fr")
        except Locale.DoesNotExist:
            self.stderr.write("FR locale not found. Run migrations and ensure WAGTAIL_I18N_ENABLED=True.")
            return

        self._seed_home(fr_locale, overwrite)
        self._seed_about(fr_locale, overwrite)
        self._seed_contact(fr_locale, overwrite)
        self._seed_legal(fr_locale, overwrite)
        self._seed_services(fr_locale, overwrite)
        self._seed_projects(fr_locale, overwrite)
        self.stdout.write(self.style.SUCCESS("FR content seeding complete."))

    # ── helpers ────────────────────────────────────────────────────────────

    def _copy_or_get(self, en_page, fr_locale, overwrite):
        """Return the FR copy of en_page. Creates it if absent."""
        existing = type(en_page).objects.filter(
            translation_key=en_page.translation_key,
            locale=fr_locale,
        ).first()
        if existing:
            if not overwrite:
                self.stdout.write(f"  skip (exists): {existing.title}")
                return None
            return existing
        try:
            fr_page = en_page.copy_for_translation(locale=fr_locale, copy_parents=True)
            return fr_page
        except Exception as exc:
            self.stderr.write(f"  error copying {en_page.title}: {exc}")
            return None

    def _publish(self, page, label):
        rev = page.save_revision()
        rev.publish()
        self.stdout.write(f"  published: {label}")

    # ── page seeders ───────────────────────────────────────────────────────

    def _seed_home(self, fr_locale, overwrite):
        en = HomePage.objects.filter(locale__language_code="en").live().first()
        if not en:
            self.stderr.write("  HomePage (EN) not found — skipping.")
            return
        fr = self._copy_or_get(en, fr_locale, overwrite)
        if not fr:
            return
        for k, v in HOME_FR.items():
            if hasattr(fr, k):
                setattr(fr, k, v)
        self._publish(fr, "HomePage (FR)")

    def _seed_about(self, fr_locale, overwrite):
        en = AboutPage.objects.filter(locale__language_code="en").live().first()
        if not en:
            self.stderr.write("  AboutPage (EN) not found — skipping.")
            return
        fr = self._copy_or_get(en, fr_locale, overwrite)
        if not fr:
            return
        for k, v in ABOUT_FR.items():
            if hasattr(fr, k):
                setattr(fr, k, v)
        self._publish(fr, "AboutPage (FR)")

    def _seed_contact(self, fr_locale, overwrite):
        en = ContactPage.objects.filter(locale__language_code="en").live().first()
        if not en:
            self.stderr.write("  ContactPage (EN) not found — skipping.")
            return
        fr = self._copy_or_get(en, fr_locale, overwrite)
        if not fr:
            return
        for k, v in CONTACT_FR.items():
            if hasattr(fr, k):
                setattr(fr, k, v)
        self._publish(fr, "ContactPage (FR)")

    def _seed_legal(self, fr_locale, overwrite):
        en_pages = LegalPage.objects.filter(locale__language_code="en").live()
        translations = {
            "privacy": PRIVACY_FR,
            "terms": TERMS_FR,
        }
        for en in en_pages:
            slug_key = "privacy" if "privacy" in en.slug else "terms"
            data = translations.get(slug_key)
            if not data:
                continue
            fr = self._copy_or_get(en, fr_locale, overwrite)
            if not fr:
                continue
            for k, v in data.items():
                if hasattr(fr, k):
                    setattr(fr, k, v)
            self._publish(fr, f"LegalPage ({slug_key}) (FR)")

    def _seed_services(self, fr_locale, overwrite):
        # Seed service index
        en_index = ServiceIndexPage.objects.filter(locale__language_code="en").live().first()
        if en_index:
            fr_index = self._copy_or_get(en_index, fr_locale, overwrite)
            if fr_index:
                fr_index.title = "Services"
                fr_index.intro = "<p>Des solutions numériques complètes — conception de marque, développement web et stratégie numérique — toutes gérées directement par notre équipe.</p>"
                fr_index.breadcrumb_home = "Accueil"
                fr_index.breadcrumb_services = "Services"
                fr_index.about_title = "Notre approche"
                fr_index.about_subtitle = "Un studio boutique pour les PME"
                fr_index.services_title = "Ce que nous offrons"
                fr_index.contact_title = "Commençons"
                fr_index.contact_subtitle = "Parlez-nous de votre projet."
                fr_index.btn_text = "Nous contacter"
                self._publish(fr_index, "ServiceIndexPage (FR)")

        # Seed each service page
        en_services = ServicePage.objects.filter(locale__language_code="en").live()
        for en in en_services:
            matched = None
            for slug_key, data in SERVICE_TRANSLATIONS.items():
                if slug_key in en.slug:
                    matched = data
                    break
            if not matched:
                # Fallback: copy with title note
                self.stdout.write(f"  no FR data for service slug '{en.slug}' — copying as-is")
                continue
            fr = self._copy_or_get(en, fr_locale, overwrite)
            if not fr:
                continue
            for k, v in matched.items():
                if hasattr(fr, k):
                    setattr(fr, k, v)
            fr.breadcrumb_home = "Accueil"
            self._publish(fr, f"ServicePage '{en.slug}' (FR)")

    def _seed_projects(self, fr_locale, overwrite):
        # Seed portfolio index
        en_index = PortfolioIndexPage.objects.filter(locale__language_code="en").live().first()
        if en_index:
            fr_index = self._copy_or_get(en_index, fr_locale, overwrite)
            if fr_index:
                fr_index.title = "Projets"
                fr_index.portfolio_title = "Nos réalisations"
                fr_index.portfolio_subtitle = "Des plateformes, des marques et des stratégies construites pour durer."
                fr_index.breadcrumb_home = "Accueil"
                fr_index.breadcrumb_portfolio = "Projets"
                fr_index.project_title = "Projet"
                fr_index.project_summary = "Résumé"
                fr_index.date_title = "Date"
                self._publish(fr_index, "PortfolioIndexPage (FR)")

        # Seed each project page
        en_projects = ProjectPage.objects.filter(locale__language_code="en").live()
        for en in en_projects:
            matched = None
            for slug_key, data in PROJECT_TRANSLATIONS.items():
                if slug_key in en.slug:
                    matched = data
                    break
            if not matched:
                self.stdout.write(f"  no FR data for project slug '{en.slug}' — skipping")
                continue
            fr = self._copy_or_get(en, fr_locale, overwrite)
            if not fr:
                continue
            for k, v in matched.items():
                if hasattr(fr, k):
                    setattr(fr, k, v)
            self._publish(fr, f"ProjectPage '{en.slug}' (FR)")
