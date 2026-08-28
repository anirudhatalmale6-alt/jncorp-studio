# -*- coding: utf-8 -*-
"""Controles du site de l'agence.

Un site d'agence ment plus facilement qu'un catalogue : personne ne verifie
« 200 projets livres ». Les controles les plus utiles ici ne portent donc pas
sur la mise en page, ils portent sur les AFFIRMATIONS.

  - les trois nombres de l'accueil sont-ils calcules a partir des donnees ?
  - le nombre de controles annonce a cote de chaque realisation est-il celui
    que la vraie suite de tests affiche quand on la relance ?
  - la page tient-elle sa regle « aucun tarif », symboles compris ?
  - aucune biographie n'a-t-elle ete redigee a la place du fondateur ?

Ensuite seulement : les deux langues, le contraste sur fond sombre, le
mouvement coupable, le debordement en 390 px, et le formulaire.
"""

import html as _H
import http.server
import os
import re
import socket
import subprocess
import sys
import threading

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

from chemins import dossier_pages        # noqa: E402
from contenu import (A_TRANCHER, BANDEAU, DEVISE_EN, DEVISE_FR,  # noqa: E402
                     ETAPES, FONDATEUR, REALISATIONS, SERVICES, TECHNIQUE,
                     VARIABLES)
import page_agence                       # noqa: E402

OK = []
IGNORES = []


def t(nom, cond, detail=''):
    OK.append(bool(cond))
    print('%s %s%s' % ('  ok  ' if cond else ' ECHEC', nom,
                       ('   -> ' + str(detail)) if not cond and detail else ''))


def ignore(nom, pourquoi):
    """Un controle qui n'a PAS tourne. Il ne compte pas comme reussi."""
    IGNORES.append(nom)
    print(' IGNORE %s   -> %s' % (nom, pourquoi))


subprocess.run([sys.executable, os.path.join(ICI, 'page_agence.py')],
               check=True, stdout=subprocess.DEVNULL)

RACINE_P = os.path.dirname(ICI)
DEMO = dossier_pages(ICI)
ACC = open(os.path.join(DEMO, 'index.html'), encoding='utf-8').read()
REA = open(os.path.join(DEMO, 'realisations.html'), encoding='utf-8').read()
TOUT = ACC + REA

print('\n--- les affirmations de la page ---')

# Les trois nombres de l'accueil. Recalcules ici depuis contenu.py : la page
# ne peut pas se contredire toute seule, et l'ajout d'une realisation les
# fait bouger sans que personne ait a y penser.
attendus = [len(REALISATIONS), sum(r[4] for r in REALISATIONS), 2]
ecrits = [int(x) for x in re.findall(r'<div class="mesure"><b>(\d+)</b>', ACC)]
t('les trois chiffres de l\'accueil sont ceux des donnees',
  ecrits == attendus, (ecrits, attendus))

# Aucun chiffre d'agence invente. Une agence qui commence n'a pas « 200
# projets » ni « 15 ans d'experience », et les ecrire quand meme donne une
# page indefendable en rendez-vous.
gonfle = re.findall(
    r'(?i)\b(\d{2,})\s*(?:\+|ans d\'experience|years|projets? livr|clients?'
    r'\s+satisfaits|years of experience)', TOUT)
t('aucune statistique d\'agence gonflee', not gonfle, gonfle[:3])

# La regle « aucun tarif », tenue par la machine et pas par la relecture.
# Deux passes : les codes de devise sont sensibles a la casse (« CAD » est
# une devise, « cad » ne l'est pas), la formule d'appel ne l'est pas. Un
# seul motif avec un (?i) au milieu ne compile meme pas en Python 3.11+.
argent = re.findall(r'[$€£¥]|\bEUR\b|\bUSD\b|\bCAD\b|\bCHF\b|\bGBP\b', TOUT)
t('aucun symbole ni code de devise sur les deux pages', not argent,
  sorted(set(argent))[:4])
# La page EXPLIQUE pourquoi elle n'affiche pas de prix : elle a donc le
# droit d'ecrire les mots « tarif » et « a partir de ». Ce qu'il faut
# interdire, c'est la formule SUIVIE D'UN NOMBRE — le prix lui-meme.
appel = re.findall(r'(?:a partir de|starting (?:at|from)|des seulement)'
                   r'[^.<]{0,30}\d', TOUT, re.I)
t('aucune formule de prix suivie d\'un montant', not appel,
  sorted(set(appel))[:4])
t('la page dit pourquoi elle n\'affiche pas de tarif',
  'Aucun tarif ici' in ACC)
t('les cinq variables du devis sont la',
  ACC.count('<div class="var">') == len(VARIABLES),
  ACC.count('<div class="var">'))

# Le fondateur : un nom, un role, sa phrase, et RIEN d'autre.
t('le fondateur est nomme', FONDATEUR['nom'] in ACC and FONDATEUR['nom'] in REA)
t('son role est ecrit', FONDATEUR['role_fr'] in ACC)
t('sa devise est reprise telle qu\'il l\'a formulee',
  DEVISE_FR in ACC and DEVISE_EN in ACC, DEVISE_FR)
t('l\'ancienne devise a disparu des deux pages',
  'Equilibrium, Equity and Light' not in TOUT)
# La meme devise doit figurer, mot pour mot, sur le site de prestige.
_pr = os.path.join(RACINE_P, 'prestige', 'page_prestige.py')
if os.path.isfile(_pr):
    _src = open(_pr, encoding='utf-8').read()
    t('la devise est identique a celle du site de prestige',
      ("DEVISE_FR = '%s'" % DEVISE_FR) in _src
      and ("DEVISE_EN = '%s'" % DEVISE_EN) in _src, DEVISE_FR)
else:
    ignore('devise partagee avec le site de prestige',
           'prestige/page_prestige.py absent de cet arbre')
bloc = re.search(r'<section class="fond".*?</section>', ACC, re.S)
t('le bloc fondateur existe', bool(bloc))
if bloc:
    corps = bloc.group(0)
    t('le texte du fondateur est marque comme a fournir, pas invente',
      'Texte du fondateur a fournir' in corps)
    phrases = [x for x in re.findall(r'>([^<>]{60,})<', corps)
               if DEVISE_FR not in x and DEVISE_EN not in x]
    t('aucun paragraphe biographique n\'a ete redige a sa place',
      not phrases, [x[:70] for x in phrases[:2]])

# Aucun client ni logo qu'on n'a pas servi : les seuls liens sortants sont
# les sites qu'on a reellement livres.
liens = set(re.findall(r'href="(https?://[^"]+)"', TOUT))
autorises = {r[2] for r in REALISATIONS} | {page_agence.URL_ANNUAIRE,
                                            page_agence.URL_PRESTIGE}
t('les seuls liens sortants sont les sites reellement livres',
  liens <= autorises, sorted(liens - autorises))
t('les trois realisations sont liees',
  all(r[2] in REA for r in REALISATIONS),
  [r[0] for r in REALISATIONS if r[2] not in REA])
# On compte la PASTILLE, pas la chaine : le libelle apparait deux fois par
# projet (l'attribut francais et le texte servi), et compter la chaine
# faisait attendre 3 la ou il y en a legitimement 6.
# On compte une CLASSE DEDIEE (`tbc demo`), pas une chaine de caracteres :
# le libelle apparait deux fois par projet (l'attribut francais et le texte
# servi), et une classe partagee compterait aussi le bloc fondateur.
t('chaque realisation annonce ses donnees de demonstration',
  REA.count('class="tbc demo"') == len(REALISATIONS),
  REA.count('class="tbc demo"'))

print('\n--- le nombre de controles annonce est-il le vrai ---')

# C'est LE controle de ce fichier. Un chiffre d'agence qu'on ne peut pas
# recompter est un chiffre invente qui a juste l'air modeste. On relance
# donc les vraies suites et on compare. Quand l'arbre voisin n'est pas la
# (depot livre au client), le controle est declare NON EXECUTE — pas vert.
RACINE = os.path.dirname(ICI)
for cle, nom, url, (dossier, fichier), annonce, _a, _b, _c, _d in REALISATIONS:
    chemin = os.path.join(RACINE, dossier, fichier)
    if not os.path.isfile(chemin):
        ignore('recompte de « %s »' % nom, 'suite absente : %s' % chemin)
        continue
    r = subprocess.run([sys.executable, chemin], cwd=os.path.dirname(chemin),
                       capture_output=True, text=True)
    lignes = [x for x in r.stdout.strip().splitlines() if x.strip()]
    derniere = lignes[-1] if lignes else ''
    trouve = re.search(r'(\d+)', derniere)
    reel = int(trouve.group(1)) if trouve else None
    rouges = re.search(r'(\d+)\s*(?:en echec|rouges|echecs)', derniere)
    t('« %s » annonce %d controles, la suite en compte %s'
      % (nom, annonce, reel), reel == annonce, derniere)
    t('« %s » : la suite passe entierement' % nom,
      rouges is not None and int(rouges.group(1)) == 0, derniere)

print('\n--- ce qui est ecrit dans les pages ---')

t('aucun marqueur de gabarit ne subsiste',
  not re.search(r'__[A-Z0-9_]+__', TOUT),
  sorted(set(re.findall(r'__[A-Z0-9_]+__', TOUT)))[:4])
t('les deux pages embarquent exactement la meme feuille de style',
  re.search(r'<style>\n(.*?)\n</style>', ACC, re.S).group(1)
  == re.search(r'<style>\n(.*?)\n</style>', REA, re.S).group(1))

# Un element traduit doit porter LES DEUX langues. On isole les balises puis
# on regarde dedans : une negation placee apres l'attribut ne verrait que ce
# qui le suit, et laisserait passer l'ordre normal.
balises = re.findall(r'<[a-z][^>]*>', TOUT, re.S)
boiteux = [b for b in balises if ('data-fr=' in b) != ('data-en=' in b)]
t('aucun element ne porte une seule des deux langues', not boiteux,
  [b[:90] for b in boiteux[:2]])
t('les pages portent des elements traduits',
  len(re.findall(r'data-fr="', TOUT)) > 120,
  len(re.findall(r'data-fr="', TOUT)))

# Le texte servi et le texte que le script posera doivent dire la meme chose,
# sinon la page change de mot toute seule au chargement — c'est ainsi qu'une
# faute de frappe dans un attribut passe la relecture.
ecarts = []
for m in re.finditer(r'<(\w+)[^>]*\bdata-fr="([^"]*)"[^>]*>(.*?)</\1>',
                     TOUT, re.S):
    attr = _H.unescape(m.group(2)).strip()
    dedans = _H.unescape(m.group(3)).strip()
    if '<' in m.group(3) or '__' in dedans:
        continue
    if attr != dedans:
        ecarts.append((attr[:48], dedans[:48]))
t('le texte servi et le texte francais du script disent la meme chose',
  not ecarts, ecarts[:3])

# Le diamant : la marque du groupe. Dessine, jamais telecharge, et identique
# a celui du site de prestige — une marque qui change de trace d'un site a
# l'autre n'est plus une marque.
t('le diamant est present sur les deux pages',
  ACC.count('class="diamant"') >= 2 and REA.count('class="diamant"') >= 2,
  (ACC.count('class="diamant"'), REA.count('class="diamant"')))
t('le diamant est dessine, pas une image a telecharger',
  'diamant.png' not in TOUT and 'diamant.svg' not in TOUT
  and '<svg class="diamant"' in ACC)
autre = os.path.join(RACINE, 'prestige', 'page_prestige.py')
if os.path.isfile(autre):
    src = open(autre, encoding='utf-8').read()
    m = re.search(r"'<path d=\"(M6 3h12l4 6-10 12L2 9z)\"/>'", src)
    t('le trace du diamant est le meme que sur le site de prestige',
      bool(m) and m.group(1) in page_agence.DIAMANT, bool(m))
else:
    ignore('trace du diamant partage', 'prestige/page_agence introuvable')

photos = re.findall(r'data-photo="([^"]+)" data-ratio="(\d+)/(\d+)"', ACC)
t('la page declare la photo du fondateur', len(photos) == 1, photos)
for src, w, h in photos:
    chemin = os.path.join(DEMO, src)
    t('le fichier %s existe' % src, os.path.isfile(chemin), chemin)
    if os.path.isfile(chemin):
        vrai = page_agence.dimensions_jpeg(chemin)
        t('%s : le ratio ecrit est celui du fichier %s' % (src, vrai),
          vrai == (int(w), int(h)), (vrai, (int(w), int(h))))
        balise = re.search(r'<img src="%s"[^>]*>' % re.escape(src),
                           ACC).group(0)
        t('la balise porte width, height et les deux textes alternatifs',
          all(x in balise for x in ('width="%s"' % w, 'height="%s"' % h,
                                    'data-alt-fr="', 'data-alt-en="')),
          balise)

t('les six services sont dans l\'index',
  ACC.count('class="ligne-idx') == len(SERVICES),
  ACC.count('class="ligne-idx'))
t('chaque ligne de l\'index est un vrai bouton, atteignable au clavier',
  ACC.count('<button type="button" aria-expanded="false"') == len(SERVICES),
  ACC.count('<button type="button" aria-expanded="false"'))
t('les quatre etapes sont sur la page',
  ACC.count('class="etape rev"') == len(ETAPES),
  ACC.count('class="etape rev"'))
# Le bandeau defilant est DECORATIF : il doit etre masque aux lecteurs
# d'ecran, et sa piste ecrite deux fois pour que la boucle soit invisible.
t('le bandeau defilant est masque aux lecteurs d\'ecran',
  '<div class="bandeau" aria-hidden="true">' in ACC)
for mot in BANDEAU:
    if ACC.count('<span>%s</span>' % _H.escape(mot, quote=True)) != 2:
        t('le bandeau repete « %s » exactement deux fois' % mot, False,
          ACC.count('<span>%s</span>' % _H.escape(mot, quote=True)))
        break
else:
    t('la piste du bandeau est ecrite deux fois (boucle sans saut)', True)
t('les quatre blocs techniques sont sur la page',
  ACC.count('<div class="tech-bloc">') == len(TECHNIQUE),
  ACC.count('<div class="tech-bloc">'))
# RIEN ne doit etre cache sans JavaScript : chaque regle qui masque un bloc
# d'apparition doit etre prefixee par `.js`, la classe que le script pose
# lui-meme. Sans elle, la page reste lisible.
feuille = re.search(r'<style>\n(.*?)\n</style>', ACC, re.S).group(1)
# Ce qu'on cherche n'est pas « une regle qui commence par .rev », c'est une
# regle qui CACHE : opacite nulle ou deplacement. `.ligne{overflow:hidden}`
# ne cache rien, `.ligne-idx` n'est meme pas la meme classe.
# On decoupe la feuille en REGLES (selecteur + son propre bloc), pas en
# lignes : une fenetre de trois lignes attrapait la regle suivante, et
# `.ligne{overflow:hidden}` se faisait accuser du translateY de `.js .ligne`.
nues = []
for sel, bloc in re.findall(r'([^{}@]+)\{([^{}]*)\}', feuille):
    sel = sel.strip().splitlines()[-1].strip()
    if not re.match(r'^\.(rev|ligne)(?![\w-])', sel):
        continue
    plat = bloc.replace(' ', '').replace('\n', '')
    if 'opacity:0' in plat or 'translateY' in plat:
        nues.append('%s{%s}' % (sel, plat[:60]))
t('aucune regle qui CACHE ne s\'applique sans la classe « js »',
  not nues, nues[:2])
t('les regles d\'apparition existent bien, prefixees par « js »',
  '.js .rev{opacity:0' in feuille.replace('\n', '') or
  '.js .rev{opacity:0' in feuille)
# La page est ECHAPPEE : « L'adresse » y est ecrit « L&#x27;adresse ». On
# compare donc les formes echappees, sinon le controle echoue sur son
# propre encodage et pas sur le contenu.
manquants = [x for x in A_TRANCHER
             if _H.escape(x, quote=True) not in ACC]
t('ce qui reste a trancher est ecrit, pas passe sous silence',
  not manquants, manquants[:2])
t('les pages ne sont pas indexables tant que le nom n\'est pas arrete',
  ACC.count('name="robots" content="noindex"') == 1
  and REA.count('name="robots" content="noindex"') == 1)
t('les deux pages annoncent la demonstration',
  'DEMONSTRATION' in ACC and 'DEMONSTRATION' in REA)

# Les ancres du menu doivent exister : un lien vers #methode qui ne mene
# nulle part ne provoque aucune erreur, il ne fait simplement rien.
for nom_page, src in (('index.html', ACC), ('realisations.html', REA)):
    tous = re.findall(r'\sid="([\w-]+)"', src)
    doublons = sorted({x for x in tous if tous.count(x) > 1})
    t('%s ne porte aucun identifiant en double' % nom_page, not doublons,
      doublons)

ancres = set(re.findall(r'href="index\.html#([\w-]+)"', TOUT))
ids = set(re.findall(r'id="([\w-]+)"', ACC))
t('toutes les ancres du menu existent sur l\'accueil', ancres <= ids,
  sorted(ancres - ids))

print('\n--- la page, dans un vrai navigateur ---')

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    ignore('controles navigateur', 'playwright absent')
    sync_playwright = None

if sync_playwright:
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()

    class Muet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def __init__(self, *a, **k):
            super().__init__(*a, directory=DEMO, **k)

    srv = http.server.ThreadingHTTPServer(('127.0.0.1', port), Muet)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = 'http://127.0.0.1:%d/' % port

    # Le calcul de contraste WCAG, fait dans la page sur les couleurs
    # REELLEMENT appliquees. Lire la feuille de style ne dit pas quelle
    # regle a gagne ; getComputedStyle, si.
    JS_CONTRASTE = """
    (sel)=>{
      function lum(c){
        var m = c.match(/[\\d.]+/g).slice(0,3).map(function(v){
          v = v/255;
          return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4);
        });
        return .2126*m[0] + .7152*m[1] + .0722*m[2];
      }
      var n = document.querySelector(sel);
      if (!n) return null;
      var fg = getComputedStyle(n).color;
      var el = n, bg = 'rgba(0, 0, 0, 0)';
      while (el){
        var c = getComputedStyle(el).backgroundColor;
        if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent'){ bg = c; break; }
        el = el.parentElement;
      }
      var a = lum(fg), b = lum(bg);
      var hi = Math.max(a,b), lo = Math.min(a,b);
      return Math.round(((hi + .05) / (lo + .05)) * 100) / 100;
    }
    """

    erreurs = []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={'width': 1280, 'height': 900})
        pg.on('console', lambda m: erreurs.append(m.text)
              if m.type == 'error' else None)
        pg.on('pageerror', lambda x: erreurs.append(str(x)))

        pg.goto(base + 'index.html', wait_until='networkidle')
        pg.wait_for_timeout(250)

        t('le mot d\'accent du titre est present en francais',
          pg.locator('h1 em').count() == 1,
          pg.locator('h1').inner_html()[:110])
        t('l\'accueil affiche son titre',
          'font' in pg.locator('h1').inner_text().lower(),
          pg.locator('h1').inner_text()[:60])
        fond = pg.evaluate("()=>getComputedStyle(document.body).backgroundColor")
        rgb = [int(x) for x in re.findall(r'\d+', fond)[:3]]
        t('le fond est un noir profond, pas un noir pur (%s)' % fond,
          0 < max(rgb) < 25, rgb)

        for sel, seuil, quoi in (('.chapo', 4.5, 'le chapo'),
                                 ('.intro', 4.5, 'les introductions'),
                                 ('.travail .res', 4.5,
                                  'le resume des realisations'),
                                 ('.tech-bloc li', 4.5, 'la liste technique'),
                                 ('.eti', 3.0, 'les etiquettes d\'accent'),
                                 ('.num', 3.0, 'les numeros de section')):
            c = pg.evaluate(JS_CONTRASTE, sel)
            t('%s tient le contraste sur fond sombre (%s:1, seuil %s)'
              % (quoi, c, seuil), c is not None and c >= seuil, c)

        # Une animation qu'on ne peut pas couper est un defaut
        # d'accessibilite, pas un effet.
        duree = pg.evaluate("()=>getComputedStyle(document.documentElement)"
                            ".getPropertyValue('--duree').trim()")
        t('le site anime par defaut (%s)' % duree, duree not in ('', '0s'),
          duree)

        # Le menu doit mener quelque part : on clique et on regarde ou on
        # atterrit, plutot que de relire un attribut href.
        pg.click('.nav a[href="index.html#methode"]')
        pg.wait_for_timeout(600)
        haut = pg.evaluate("()=>Math.round("
                           "document.getElementById('methode')"
                           ".getBoundingClientRect().top)")
        t('le lien « la methode » amene bien la section a l\'ecran (%d px)'
          % haut, -80 < haut < 200, haut)

        # L'index des services : un seul ouvert a la fois, et l'etat doit
        # etre annonce. Un <div> cliquable n'est ni atteignable au clavier ni
        # annonce par un lecteur d'ecran ; on verifie donc aria-expanded.
        lignes = pg.locator('.ligne-idx')
        t('l\'index affiche les %d services' % len(SERVICES),
          lignes.count() == len(SERVICES), lignes.count())
        t('tout est ferme au depart',
          pg.locator('.ligne-idx[data-ouvert=oui]').count() == 0)
        pg.locator('.ligne-idx button').nth(0).click()
        pg.wait_for_timeout(400)
        t('cliquer une ligne l\'ouvre',
          pg.locator('.ligne-idx[data-ouvert=oui]').count() == 1)
        t('la ligne ouverte l\'annonce (aria-expanded)',
          pg.locator('.ligne-idx button').nth(0)
            .get_attribute('aria-expanded') == 'true')
        # Le detail doit avoir une hauteur reelle : la grille passe de 0fr a
        # 1fr, et une transition mal ecrite laisse la hauteur a zero sans
        # provoquer la moindre erreur.
        h = pg.evaluate("()=>Math.round(document.querySelector("
                        "'.ligne-idx[data-ouvert=oui] .detail > div')"
                        ".getBoundingClientRect().height)")
        t('le detail ouvert a une hauteur reelle (%d px)' % h, h > 60, h)
        pg.locator('.ligne-idx button').nth(2).click()
        pg.wait_for_timeout(400)
        t('ouvrir une autre ligne referme la premiere',
          pg.locator('.ligne-idx[data-ouvert=oui]').count() == 1
          and pg.locator('.ligne-idx button').nth(0)
                .get_attribute('aria-expanded') == 'false')
        pg.locator('.ligne-idx button').nth(2).click()
        pg.wait_for_timeout(300)
        t('recliquer la meme ligne la referme',
          pg.locator('.ligne-idx[data-ouvert=oui]').count() == 0)

        # Les apparitions : ce qui est a l'ecran doit etre visible. Un bloc
        # reste a opacite 0 quand l'observateur ne se declenche pas — et
        # aucune erreur ne le signale.
        pg.evaluate("()=>window.scrollTo(0,0)")
        pg.wait_for_timeout(600)
        invisibles = pg.evaluate("""()=>{
          var out=[];
          document.querySelectorAll('.rev, .ligne').forEach(function(n){
            var r = n.getBoundingClientRect();
            if (r.top < window.innerHeight && r.bottom > 0
                && parseFloat(getComputedStyle(n).opacity) < .9)
              out.push((n.className||'')+' '+Math.round(r.top));
          });
          return out.slice(0,3);
        }""")
        t('tout ce qui est a l\'ecran est bien apparu', not invisibles,
          invisibles)

        # Le formulaire : il valide, il recapitule, il n'envoie rien.
        pg.evaluate("()=>document.getElementById('contact')"
                    ".scrollIntoView({block:'start'})")
        pg.wait_for_timeout(400)
        pg.click('#demande button[type=submit]')
        pg.wait_for_timeout(200)
        recu = pg.locator('#recu').inner_text()
        t('le formulaire vide dit ce qui manque', 'Il manque' in recu, recu)
        pg.fill('#f-nom', 'Test')
        pg.fill('#f-contact', '+00 000')
        pg.fill('#f-projet', 'Un annuaire filtrable.')
        pg.click('#demande button[type=submit]')
        pg.wait_for_timeout(200)
        recu = pg.locator('#recu').inner_text()
        t('le formulaire rempli confirme sans rien envoyer',
          "rien n'a ete envoye" in recu and 'Test' in recu, recu)
        # Le formulaire ne doit PAS naviguer : une soumission native
        # rechargerait la page, remettrait la langue a zero et effacerait le
        # recapitulatif — sans lever la moindre erreur.
        # Une soumission native partirait en GET et collerait les champs
        # dans l'adresse. Le fragment, lui, vient du lien de menu clique
        # plus haut : il est legitime, on ne le compte pas.
        t('le formulaire n\'a pas navigue (pas de rechargement)',
          '?' not in pg.url and pg.url.split('#')[0].endswith('index.html'),
          pg.url)

        # Les langues.
        pg.click('.langue button[data-l="en"]')
        pg.wait_for_timeout(350)
        corps = pg.locator('body').inner_text()
        # On mesure sur le TITRE, pas sur le menu : `inner_text` rend le
        # texte APRES `text-transform`, et « Ce que nous faisons » comme
        # « What we do » n'existent qu'en capitales dans la navigation. Le
        # controle aurait echoue dans les deux langues, pour la mauvaise
        # raison.
        # Le titre est coupe ligne par ligne : « Sites that do something »
        # n'existe plus comme chaine continue dans le texte rendu. On mesure
        # sur le chapo, qui est un paragraphe entier.
        t('la page passe en anglais',
          'We write bespoke sites' in corps
          and 'Nous ecrivons des sites' not in corps, corps[:140])
        # Le mot d'accent du titre est du balisage a l'interieur d'un texte
        # traduit. La bascule remplace l'innerHTML : s'il n'est present que
        # dans le HTML servi, il disparait a la premiere pose de langue.
        t('le mot d\'accent du titre survit en anglais',
          pg.locator('h1 em').count() == 1,
          pg.locator('h1').inner_html()[:110])
        alt = pg.get_attribute('.fond-photo img', 'alt')
        t('le texte alternatif de la photo suit la langue (%r)' % alt,
          alt and alt.endswith('founder'), alt)
        ph = pg.get_attribute('#f-contact', 'placeholder')
        t('le texte d\'aide des champs suit la langue (%r)' % ph,
          ph and 'whatever' in ph, ph)
        pg.click('.langue button[data-l="fr"]')
        pg.wait_for_timeout(300)

        pg.goto(base + 'realisations.html', wait_until='networkidle')
        t('la page realisations montre les %d projets' % len(REALISATIONS),
          pg.locator('article.travail').count() == len(REALISATIONS),
          pg.locator('article.travail').count())
        t('chaque projet porte un lien « ouvrir le site »',
          pg.locator('article.travail a.btn').count() == len(REALISATIONS),
          pg.locator('article.travail a.btn').count())
        t('la langue choisie survit au changement de page',
          pg.locator('.langue button[data-l="fr"]')
            .get_attribute('aria-pressed') == 'true')

        for nom in ('index.html', 'realisations.html'):
            pg.set_viewport_size({'width': 390, 'height': 800})
            pg.goto(base + nom, wait_until='networkidle')
            pg.wait_for_timeout(250)
            larg = pg.evaluate("()=>[document.documentElement.scrollWidth,"
                               "window.innerWidth]")
            coupables = pg.evaluate("""()=>{
              var out=[];
              document.querySelectorAll('*').forEach(function(n){
                var r=n.getBoundingClientRect();
                if (r.right > window.innerWidth+1)
                  out.push(n.tagName+'.'+n.className+' '+Math.round(r.right));
              });
              return out.slice(0,3);
            }""")
            t('%s ne deborde pas a 390 px (%d/%d)' % (nom, larg[0], larg[1]),
              larg[0] <= larg[1] + 1, coupables)

        nav.close()

        # SANS JAVASCRIPT. C'est le controle qui compte le plus sur un site
        # qui anime : si le contenu depend du script, la page est blanche le
        # jour ou il echoue. La classe `js` n'est jamais posee, donc aucune
        # regle d'apparition ne s'applique.
        nav3 = p.chromium.launch()
        ctx3 = nav3.new_context(java_script_enabled=False,
                                viewport={'width': 1280, 'height': 900})
        pg3 = ctx3.new_page()
        pg3.goto(base + 'index.html', wait_until='load')
        pg3.wait_for_timeout(200)
        caches = pg3.evaluate_handle  # non utilise : pas de JS dans la page
        texte = pg3.locator('body').inner_text()
        t('sans JavaScript, le titre est lisible',
          'Des sites qui' in texte, texte[:90])
        t('sans JavaScript, les six services sont lisibles',
          all(s_[1] in texte for s_ in SERVICES),
          [s_[1] for s_ in SERVICES if s_[1] not in texte][:2])
        t('sans JavaScript, le fondateur et sa devise sont lisibles',
          FONDATEUR['nom'] in texte and DEVISE_FR in texte)
        t('sans JavaScript, les realisations sont lisibles',
          all(r[1] in texte for r in REALISATIONS),
          [r[1] for r in REALISATIONS if r[1] not in texte][:2])
        t('sans JavaScript, la page ne porte pas la classe « js »',
          pg3.get_attribute('html', 'class') in (None, ''),
          pg3.get_attribute('html', 'class'))
        nav3.close()

        # Le mouvement doit disparaitre quand le systeme le demande. Teste
        # dans un contexte a part : c'est un reglage du navigateur, pas une
        # classe qu'on ajoute.
        nav2 = p.chromium.launch()
        ctx = nav2.new_context(reduced_motion='reduce',
                               viewport={'width': 1280, 'height': 900})
        pg2 = ctx.new_page()
        pg2.goto(base + 'index.html', wait_until='networkidle')
        duree = pg2.evaluate("()=>getComputedStyle(document.documentElement)"
                             ".getPropertyValue('--duree').trim()")
        defil = pg2.evaluate("()=>getComputedStyle(document.documentElement)"
                             ".scrollBehavior")
        t('sous « mouvement reduit », les animations sont coupees (%s)'
          % duree, duree == '0s', duree)
        t('sous « mouvement reduit », le defilement n\'est plus anime (%s)'
          % defil, defil == 'auto', defil)
        # Et surtout : rien ne doit rester invisible en attendant une
        # animation qui n'aura pas lieu.
        opac = pg2.evaluate("()=>{var n=document.querySelectorAll('.rev');"
                            "var m=1;for(var i=0;i<n.length;i++)"
                            "m=Math.min(m,parseFloat("
                            "getComputedStyle(n[i]).opacity));return m;}")
        t('sous « mouvement reduit », tout le contenu est visible (%s)'
          % opac, opac >= .99, opac)
        t('sous « mouvement reduit », il n\'y a pas de curseur personnalise',
          pg2.locator('.curseur').count() == 0)
        nav2.close()

    srv.shutdown()
    srv.server_close()
    t('aucune erreur JavaScript sur les deux pages', not erreurs, erreurs[:3])

print('\n%d controles, %d en echec, %d non executes'
      % (len(OK), OK.count(False), len(IGNORES)))
for n in IGNORES:
    print('   non execute : %s' % n)
sys.exit(1 if (OK.count(False) or IGNORES) else 0)
