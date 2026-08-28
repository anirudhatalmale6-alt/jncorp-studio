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
from contenu import (A_TRANCHER, ETAPES, FONDATEUR, REALISATIONS,  # noqa: E402
                     SERVICES, TECHNIQUE, VARIABLES)
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
  'Aucun tarif sur cette page' in ACC)
t('les cinq variables du devis sont la',
  ACC.count('<div class="var">') == len(VARIABLES),
  ACC.count('<div class="var">'))

# Le fondateur : un nom, un role, sa phrase, et RIEN d'autre.
t('le fondateur est nomme', FONDATEUR['nom'] in ACC and FONDATEUR['nom'] in REA)
t('son role est ecrit', FONDATEUR['role_fr'] in ACC)
t('sa devise est reprise telle qu\'il l\'a ecrite',
  FONDATEUR['devise'] in ACC)
bloc = re.search(r'<section class="fond".*?</section>', ACC, re.S)
t('le bloc fondateur existe', bool(bloc))
if bloc:
    corps = bloc.group(0)
    t('le texte du fondateur est marque comme a fournir, pas invente',
      'Texte du fondateur a fournir' in corps)
    phrases = [x for x in re.findall(r'>([^<>]{60,})<', corps)
               if FONDATEUR['devise'] not in x]
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
t('chaque realisation annonce ses donnees de demonstration',
  REA.count('class="puce-vert"') == len(REALISATIONS),
  REA.count('class="puce-vert"'))

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

t('les six services sont sur la page',
  ACC.count('<article class="carte">') >= len(SERVICES),
  ACC.count('<article class="carte">'))
t('les quatre etapes sont sur la page',
  ACC.count('<div class="etape">') == len(ETAPES),
  ACC.count('<div class="etape">'))
t('les quatre blocs techniques sont sur la page',
  ACC.count('<div class="tech-bloc">') == len(TECHNIQUE),
  ACC.count('<div class="tech-bloc">'))
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
                                 ('.carte p', 4.5, 'le texte des cartes'),
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
        t('la page passe en anglais',
          'Sites that do something' in corps
          and 'Des sites qui' not in corps, corps[:120])
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
          pg.locator('article.rea').count() == len(REALISATIONS),
          pg.locator('article.rea').count())
        t('chaque projet porte un lien « ouvrir le site »',
          pg.locator('article.rea a.btn').count() == len(REALISATIONS))
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
        nav2.close()

    srv.shutdown()
    srv.server_close()
    t('aucune erreur JavaScript sur les deux pages', not erreurs, erreurs[:3])

print('\n%d controles, %d en echec, %d non executes'
      % (len(OK), OK.count(False), len(IGNORES)))
for n in IGNORES:
    print('   non execute : %s' % n)
sys.exit(1 if (OK.count(False) or IGNORES) else 0)
