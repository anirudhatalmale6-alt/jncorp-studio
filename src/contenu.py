# -*- coding: utf-8 -*-
"""Le contenu du site de l'agence.

Separe des gabarits pour une seule raison : les CHIFFRES de la page doivent
etre calcules a partir de ce fichier, jamais tapes dans le HTML. « Trois
sites livres » ecrit a la main survit a l'ajout d'un quatrieme, et le site
se met a mentir sur lui-meme.

DEUX REGLES TENUES ICI, et elles se ressemblent :

  - AUCUN TARIF. Le prix d'un site depend du perimetre, du nombre de
    langues, des integrations, de l'hebergement et de la maintenance. Un
    « a partir de » invente est un engagement commercial pris a la place du
    client, exactement comme un prix de shooting sur la page photographie.
  - AUCUN CHIFFRE D'AGENCE INVENTE. Pas de « 200 projets livres », pas de
    « 15 ans d'experience », pas de temoignage client fabrique. Ce qui est
    affiche ici est ce qui a ete reellement construit et reellement mesure,
    et un controle recompte les suites de tests pour le verifier.
"""

# ---------------------------------------------------------------------------
# CE QUE L'AGENCE FAIT. Chaque ligne dit un LIVRABLE, pas une competence.
# « Nous maitrisons React » ne dit rien a un client ; « une application que
# vos equipes utilisent depuis un navigateur » se commande.
#
# cle, titre fr, titre en, texte fr, texte en, [details fr], [details en]
# ---------------------------------------------------------------------------
SERVICES = [
    ('sites', 'Sites et plateformes sur mesure',
     'Bespoke sites and platforms',
     'Un site ecrit pour ce qu\'il doit faire, pas un theme achete puis '
     'contorsionne. Structure, contenu, referencement technique, '
     'performance.',
     'A site written for what it has to do, not a bought theme bent into '
     'shape. Structure, content, technical SEO, performance.',
     ['Pages statiques ultra rapides ou application dynamique',
      'Multilingue des le premier jour',
      'Administration ou le client edite sans nous appeler'],
     ['Ultra-fast static pages or a dynamic application',
      'Multilingual from day one',
      'An admin area the client edits without calling us']),
    ('annuaires', 'Annuaires et catalogues filtrables',
     'Directories and filterable catalogues',
     'Des milliers de fiches, des filtres qui repondent a la vraie question '
     'du visiteur, et des compteurs qui annoncent le resultat avant le clic.',
     'Thousands of records, filters that answer the visitor\'s real '
     'question, and counters that announce the result before the click.',
     ['Filtres croises, tri, recherche insensible aux accents',
      'Fiches detaillees, liens profonds partageables',
      'Import et export par fichier'],
     ['Cross-filters, sorting, accent-insensitive search',
      'Detail sheets with shareable deep links',
      'File import and export']),
    ('commerce', 'Vente en ligne et paiement',
     'Online sales and payment',
     'Catalogue, panier, paiement, factures, suivi. Y compris les cas qui '
     'font mal : les produits telechargeables, les devises multiples, la '
     'TVA selon le pays.',
     'Catalogue, cart, payment, invoices, tracking. Including the parts '
     'that hurt: downloadable goods, multiple currencies, country VAT.',
     ['Passerelles de paiement, remboursements, relances',
      'Devises et taxes par pays',
      'Espace client et historique de commandes'],
     ['Payment gateways, refunds, dunning',
      'Currencies and taxes by country',
      'Customer area and order history']),
    ('metier', 'Outils metier et espaces prives',
     'Business tools and private areas',
     'Ce que le tableur ne fait plus : plusieurs utilisateurs, des droits, '
     'un historique, et des regles qui s\'appliquent partout au lieu d\'etre '
     'respectees a la main.',
     'What the spreadsheet no longer does: several users, permissions, an '
     'audit trail, and rules enforced everywhere instead of by hand.',
     ['Comptes, roles et permissions',
      'Tableaux de bord et exports',
      'Regles metier appliquees au niveau des donnees'],
     ['Accounts, roles and permissions',
      'Dashboards and exports',
      'Business rules enforced at the data layer']),
    ('integration', 'Integrations et automatisations',
     'Integrations and automation',
     'Relier ce qui existe deja : une messagerie, un CRM, une comptabilite, '
     'un fournisseur. Le travail interessant n\'est pas l\'appel, c\'est ce '
     'qui se passe quand il echoue.',
     'Connecting what already exists: mail, a CRM, accounting, a supplier. '
     'The interesting work is not the call, it is what happens when it '
     'fails.',
     ['API, webhooks, taches planifiees',
      'Reprises sur erreur et journaux consultables',
      'Aucune double saisie'],
     ['APIs, webhooks, scheduled jobs',
      'Retries and readable logs',
      'No double entry']),
    ('reprise', 'Reprise, migration et sauvetage',
     'Takeover, migration and rescue',
     'Un site herite, un prestataire parti, un serveur qui ne repond plus. '
     'On commence par mesurer ce qui existe, avant de proposer quoi que ce '
     'soit.',
     'An inherited site, a departed contractor, a server that stopped '
     'answering. We start by measuring what exists, before proposing '
     'anything.',
     ['Audit et inventaire de l\'existant',
      'Migration d\'hebergement sans coupure',
      'Remise en securite et mises a jour'],
     ['Audit and inventory of what is there',
      'Zero-downtime hosting migration',
      'Security clean-up and updates']),
]

# ---------------------------------------------------------------------------
# LA METHODE. Quatre etapes, et la troisieme est celle qui distingue une
# agence d'un prestataire : on montre en ligne avant de facturer la suite.
# ---------------------------------------------------------------------------
ETAPES = [
    ('cadrer', 'Cadrer', 'Frame',
     'Une conversation, pas un questionnaire. Ce que le site doit FAIRE, '
     'pour qui, et comment on saura qu\'il le fait.',
     'A conversation, not a form. What the site must DO, for whom, and how '
     'we will know it does it.'),
    ('maquette', 'Montrer', 'Show',
     'Une version en ligne, cliquable, avant tout engagement long. On juge '
     'sur une page qui existe, pas sur une capture retouchee.',
     'A live, clickable version before any long commitment. Judgement on a '
     'page that exists, not on a retouched mockup.'),
    ('construire', 'Construire', 'Build',
     'Par tranches livrees au fil de l\'eau. Chaque tranche est en ligne le '
     'jour ou elle est finie, et se paie quand elle est acceptee.',
     'In slices, delivered as they go. Each slice goes live the day it is '
     'done, and is paid when accepted.'),
    ('verifier', 'Verifier', 'Verify',
     'Des controles automatiques qui rejouent le parcours dans un vrai '
     'navigateur. Ce qui n\'est pas mesure n\'est pas annonce.',
     'Automated checks that replay the journey in a real browser. What is '
     'not measured is not claimed.'),
]

# ---------------------------------------------------------------------------
# LA TECHNIQUE. Groupee par role, parce qu'une liste de logos ne dit pas
# quel probleme chaque outil resout.
# ---------------------------------------------------------------------------
TECHNIQUE = [
    ('front', 'Cote visiteur', 'Front end',
     ['HTML, CSS et JavaScript ecrits a la main quand la vitesse compte',
      'React et TypeScript quand l\'interface devient un outil',
      'Accessibilite : contrastes, clavier, lecteurs d\'ecran'],
     ['Hand-written HTML, CSS and JavaScript when speed matters',
      'React and TypeScript when the interface becomes a tool',
      'Accessibility: contrast, keyboard, screen readers']),
    ('back', 'Cote serveur', 'Back end',
     ['Python, PHP et Node selon ce que le client heberge deja',
      'PostgreSQL et MySQL, schemas et migrations versionnes',
      'API REST documentees, authentification, limites de debit'],
     ['Python, PHP and Node, depending on what the client already hosts',
      'PostgreSQL and MySQL, versioned schemas and migrations',
      'Documented REST APIs, authentication, rate limits']),
    ('cms', 'Ce que le client edite', 'What the client edits',
     ['WordPress quand c\'est le bon outil, theme ecrit et non achete',
      'Administration sur mesure quand le contenu a une structure',
      'Import et export par fichier, pour ne jamais etre enferme'],
     ['WordPress when it is the right tool, with a written, not bought, theme',
      'A bespoke admin when the content has a structure',
      'File import and export, so nobody is ever locked in']),
    ('infra', 'Ou ca tourne', 'Where it runs',
     ['Hebergement mutualise, VPS ou conteneurs, selon le besoin reel',
      'HTTPS, sauvegardes, journaux, supervision',
      'Deploiements repetables : la meme commande donne le meme resultat'],
     ['Shared hosting, VPS or containers, according to the real need',
      'HTTPS, backups, logs, monitoring',
      'Repeatable deployments: the same command gives the same result']),
]

# ---------------------------------------------------------------------------
# LES REALISATIONS. Ce sont de VRAIS livrables, en ligne, construits pour ce
# client. Aucun projet invente, aucun logo de marque qu'on n'a pas servie,
# aucun temoignage fabrique.
#
# `controles` est le nombre de controles automatiques de la suite du projet.
# Il est verifie : tests-agence.py relance chaque suite quand l'arbre est
# accessible et compare. Un chiffre d'agence qu'on ne peut pas recompter est
# un chiffre invente qui a juste l'air modeste.
#
# cle, nom, url, suite (dossier, fichier), controles, resume fr/en, points fr/en
# ---------------------------------------------------------------------------
REALISATIONS = [
    ('annuaire', 'Annuaire de franchises',
     'https://anirudhatalmale6-alt.github.io/annuaire-franchises-demo/',
     ('franchises', 'tests.py'), 76,
     'Deux cents enseignes, vingt categories, vingt-deux pays. Filtres '
     'croises, devise par pays, comparateur, dossier de candidature.',
     'Two hundred brands, twenty categories, twenty-two countries. Cross '
     'filters, currency per country, comparison, application form.',
     ['Filtres a compteurs predictifs',
      'Classement sur une valeur de reference commune, affichage en '
      'devise locale',
      'Francais et anglais, un seul jeu de donnees'],
     ['Filters with predictive counters',
      'Ranking on a common reference value, display in local currency',
      'French and English from a single data set']),
    ('hotellerie', 'Hotellerie de chaine',
     'https://anirudhatalmale6-alt.github.io/annuaire-franchises-demo/hotellerie.html',
     ('franchises', 'tests-hotels.py'), 62,
     'Section separee, parce qu\'un hotel ne s\'achete pas au montant mais '
     'A LA CLE. Filtre par taille d\'hotel, deux redevances, quatre types '
     'de contrat.',
     'A separate section, because a hotel is not bought for a sum but PER '
     'KEY. Filter by hotel size, two fees, four contract types.',
     ['Cout du projet calcule, jamais tire au hasard',
      'Le filtre de taille demande l\'appartenance a une fourchette',
      'Vocabulaire du metier plutot que colonnes generiques'],
     ['Project cost computed, never drawn at random',
      'The size filter asks for membership of a range',
      'The trade\'s vocabulary rather than generic columns']),
    ('prestige', 'Maisons de prestige',
     'https://anirudhatalmale6-alt.github.io/maisons-de-prestige/',
     ('prestige', 'tests-prestige.py'), 108,
     'Site noir, cinq etoiles. Contrats de gestion, honoraires de base et '
     'd\'incitation sur deux assiettes differentes, apport du groupe.',
     'A black site, five stars. Management contracts, base and incentive '
     'fees on two different bases, group contribution.',
     ['Charte sombre complete, accessible en contraste',
      'Cinq distinctions, quatre modes d\'exploitation',
      'Formulaire proprietaire et fiches en lien profond'],
     ['A full dark design system, accessible in contrast',
      'Five distinctions, four operating structures',
      'Owner form and deep-linked detail sheets']),
]

# ---------------------------------------------------------------------------
# CE QUI FAIT VARIER UN DEVIS. A la place d'un tarif : les cinq choses qui
# le determinent. Plus honnete, et beaucoup plus facile a defendre dans une
# negociation que « a partir de X ».
# ---------------------------------------------------------------------------
VARIABLES = [
    ('Le perimetre', 'Scope',
     'Cinq pages de presentation et un annuaire de dix mille fiches ne se '
     'chiffrent pas dans la meme unite.',
     'Five presentation pages and a ten-thousand-record directory are not '
     'priced in the same unit.'),
    ('Les langues', 'Languages',
     'Une deuxieme langue n\'est pas une traduction : c\'est un jeu de '
     'donnees, une navigation et des controles en plus.',
     'A second language is not a translation: it is another data set, '
     'another navigation and more checks.'),
    ('Ce que le client edite', 'What the client edits',
     'Un contenu fige coute peu. Une administration ou le client cree, '
     'trie et publie coute ce qu\'elle vaut.',
     'Fixed content costs little. An admin where the client creates, sorts '
     'and publishes costs what it is worth.'),
    ('Les integrations', 'Integrations',
     'Paiement, messagerie, comptabilite, transporteur : chacune ajoute un '
     'cas d\'echec a traiter, pas seulement un appel a ecrire.',
     'Payment, mail, accounting, carrier: each adds a failure case to '
     'handle, not just a call to write.'),
    ('La suite', 'What follows',
     'Hebergement, sauvegardes, mises a jour et corrections. Un site livre '
     'et abandonne coute plus cher qu\'un site suivi.',
     'Hosting, backups, updates and fixes. A site delivered and abandoned '
     'costs more than a site looked after.'),
]

FONDATEUR = {
    'nom': 'Hakim Adjaoudi',
    'role_fr': 'Fondateur, JNCORP INC.',
    'role_en': 'Founder, JNCORP INC.',
    'devise': 'Equilibrium, Equity and Light',
}

# Ce qui reste a trancher avec le client avant la mise en ligne reelle.
A_TRANCHER = [
    'Le nom de l\'agence (« JNCORP Studio » est un placeholder)',
    'L\'adresse ou arrivent les demandes du formulaire',
    'Le numero de telephone et les horaires, s\'il en faut',
    'L\'entite juridique et le pays, pour les mentions legales',
    'Les photos d\'equipe, s\'il y en a',
]
