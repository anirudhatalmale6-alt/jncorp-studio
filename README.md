# JNCORP Studio — agence de developpement web

Site de demonstration de l'agence. Deux pages :

- `index.html` — ce que nous faisons, la methode, la technique, les
  realisations, ce qui fait varier un devis, le fondateur, le contact
- `realisations.html` — les trois sites livres, en detail
- `src/` — les sources
- `apercus/` — captures d'ecran

> **DEMONSTRATION.** Le nom, l'entite juridique et l'adresse de contact ne
> sont pas encore arretes ; les deux pages portent `noindex`. Les
> **realisations, elles, sont reelles et en ligne** — les liens y menent.

---

## Deux regles que la machine fait respecter

### 1. Aucun tarif

Le prix d'un site depend du perimetre, du nombre de langues, de ce que le
client edite lui-meme, des integrations et de la suite (hebergement,
sauvegardes, corrections). Un « a partir de » affiche sans connaitre le
projet est faux dans un sens ou dans l'autre : soit il fait fuir un client
dont le besoin etait simple, soit il engage sur un chiffre intenable.

La page affiche donc **les cinq variables**, pas un montant. Deux controles
l'imposent : aucun symbole ni code de devise, et aucune formule de prix
suivie d'un nombre.

### 2. Aucun chiffre d'agence invente

Pas de « 200 projets livres », pas de « 15 ans d'experience », aucun
temoignage fabrique, aucun logo de client qu'on n'a pas servi. Les trois
nombres de l'accueil sont **recomptables** :

| Affiche | D'ou il vient |
|---|---|
| sites en ligne | `len(REALISATIONS)` dans `src/contenu.py` |
| controles automatiques | somme des controles des trois suites |
| langues | 2, sur chaque site |

Et `src/tests-agence.py` **relance les vraies suites de tests** des trois
projets quand leur arbre est accessible, puis compare le nombre annonce a
celui qu'elles impriment. Un chiffre qu'on ne peut pas recompter est un
chiffre invente qui a juste l'air modeste.

---

## Le fondateur

Nom, role, et la phrase que le client a lui-meme ecrite. **Aucune
biographie n'a ete redigee a sa place** : un marqueur « texte a fournir »
tient la place, et un controle verifie qu'aucun paragraphe n'a ete invente.

Le **diamant** est un trace SVG, pas une image : net a 16 px comme a
200 px, 300 octets, et il prend la couleur du texte partout ou on le pose.
C'est exactement le meme trace que sur le site des maisons de prestige — un
controle compare les deux, parce qu'une marque qui change de dessin d'un
site a l'autre n'est plus une marque.

---

## Reconstruire

```sh
cd src
python3 page_agence.py     # ecrit index.html et realisations.html
python3 tests-agence.py    # 66 controles
python3 captures-agence.py # captures (playwright)
```

`tests-agence.py` verifie notamment :

- les trois nombres de l'accueil contre les donnees ;
- le nombre de controles annonce contre les suites relancees ;
- la regle « aucun tarif », symboles et formules compris ;
- qu'aucun element ne porte une seule des deux langues, et que le texte
  servi dit la meme chose que le texte du script ;
- le **contraste WCAG** des quatre couleurs de texte sur fond sombre,
  mesure sur les couleurs reellement appliquees ;
- qu'aucune page ne porte **deux fois le meme identifiant** (le navigateur
  ne signale rien : `getElementById` rend le premier, et le script travaille
  silencieusement sur le mauvais element) ;
- que les animations **et** le defilement s'arretent sous
  `prefers-reduced-motion` ;
- qu'aucune page ne deborde horizontalement a 390 px.

---

## A trancher avant la mise en ligne

1. **Le nom de l'agence.** « JNCORP Studio » est un placeholder, signale par
   une pastille `nom a definir` dans l'en-tete.
2. **L'adresse ou arrivent les demandes** du formulaire (il valide et
   recapitule, il n'envoie rien).
3. Le telephone et les horaires, s'il en faut.
4. L'entite juridique et le pays, pour les mentions legales.
5. Les photos d'equipe, s'il y en a.

## Les domaines

Les liens vers les autres sites du groupe sont absolus (ce sont des sites
separes) et regroupes en haut de `src/page_agence.py` :
`URL_ANNUAIRE` et `URL_PRESTIGE`. Ce sont les seules lignes a changer le
jour des noms de domaine.
