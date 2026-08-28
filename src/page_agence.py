# -*- coding: utf-8 -*-
"""Construit les deux pages de l'agence : l'accueil et les realisations.

Refonte du 28 aout, apres les references du client (Locomotive, DIA Studio,
Instrument, Fantasy, Clay, Bureau Borsche). Ce qui a change dans la STRUCTURE,
pas seulement dans la couleur :

  - un titre demesure, coupe ligne par ligne, chaque ligne entrant en decale ;
  - les services passent d'une grille de cartes a un INDEX NUMEROTE qui
    s'ouvre au clic : on parcourt une liste, on ouvre ce qui interesse ;
  - la methode devient une colonne collante a gauche et des etapes qui
    defilent a droite ;
  - les realisations deviennent des lignes de titre pleine largeur ;
  - un bandeau defilant, decoratif et coupable.

Les CHIFFRES restent calcules a partir de contenu.py, jamais tapes dans le
HTML : « trois sites livres » ecrit a la main survit a l'ajout d'un
quatrieme, et la page se met a mentir sur elle-meme.

RIEN N'EST CACHE PAR DEFAUT. Les apparitions dependent d'une classe `js`
posee par le script lui-meme ; sans JavaScript, tout le contenu est visible.
Un site dont le texte depend d'un script est un site blanc le jour ou le
script echoue.
"""

import html as _H
import os
import re

from style_agence import CSS
from contenu import (A_TRANCHER, BANDEAU, DEVISE_EN, DEVISE_FR, ETAPES,
                     FONDATEUR, REALISATIONS, SERVICES, TECHNIQUE, VARIABLES)
from chemins import dossier_pages

ICI = os.path.dirname(os.path.abspath(__file__))
DEMO = dossier_pages(ICI)

# ---------------------------------------------------------------------------
# LES ADRESSES DES AUTRES SITES DU GROUPE. Sites separes, donc liens absolus,
# et tous ici, en haut. Ce sont les seules lignes a changer le jour des noms
# de domaine.
# ---------------------------------------------------------------------------
URL_ANNUAIRE = 'https://anirudhatalmale6-alt.github.io/annuaire-franchises-demo/'
URL_PRESTIGE = 'https://anirudhatalmale6-alt.github.io/maisons-de-prestige/'

# Le meme diamant que sur le site de prestige : c'est la marque du groupe, et
# une marque qui change de dessin d'un site a l'autre n'est plus une marque.
DIAMANT = (
    '<svg class="diamant" viewBox="0 0 24 24" aria-hidden="true" '
    'focusable="false">'
    '<path d="M6 3h12l4 6-10 12L2 9z"/>'
    '<path d="M2 9h20M6 3l3 6M18 3l-3 6M12 3l-3 6M12 3l3 6'
    'M9 9l3 12M15 9l-3 12"/>'
    '</svg>')


def e(x):
    return _H.escape(str(x), quote=True)


def bi(fr, en, balise='p', classe=''):
    c = ' class="%s"' % e(classe) if classe else ''
    return ('<%s%s data-fr="%s" data-en="%s">%s</%s>'
            % (balise, c, e(fr), e(en), fr, balise))


def rev(html, delai=0):
    """Enveloppe un bloc dans une apparition au defilement.

    Le style d'attente n'existe que sous la classe `js`, posee par le script.
    Sans JavaScript, cette balise est un <div> ordinaire et tout se voit.
    """
    d = ' style="transition-delay:%dms"' % delai if delai else ''
    return '<div class="rev"%s>%s</div>' % (d, html)


def liste(fr, en, classe=''):
    """Une liste bilingue, chaque <li> portant ses deux langues.

    Traduire la liste entiere d'un bloc obligerait a stocker du HTML dans un
    attribut, et la moindre apostrophe casserait la page.
    """
    c = ' class="%s"' % e(classe) if classe else ''
    out = ['<ul%s>' % c]
    for a, b in zip(fr, en):
        out.append('<li data-fr="%s" data-en="%s">%s</li>' % (e(a), e(b), e(a)))
    out.append('</ul>')
    return ''.join(out)


def photo(src, alt_fr, alt_en):
    """Une vraie image, avec ses dimensions lues DANS le fichier.

    Ecrites a la main, elles deviennent fausses au premier remplacement du
    fichier et plus personne ne s'en apercoit ; le navigateur reserve alors
    une place fausse et la page saute au chargement.
    """
    chemin = os.path.join(DEMO, src)
    larg, haut = dimensions_jpeg(chemin)
    if not larg:
        raise SystemExit('dimensions illisibles : %s' % chemin)
    return ('<figure class="fond-photo" data-photo="%s" data-ratio="%d/%d">'
            '<img src="%s" alt="%s" data-alt-fr="%s" data-alt-en="%s" '
            'width="%d" height="%d" style="aspect-ratio:%d/%d">'
            '</figure>'
            % (e(src), larg, haut, e(src), e(alt_fr), e(alt_fr), e(alt_en),
               larg, haut, larg, haut))


def dimensions_jpeg(chemin):
    """Largeur et hauteur d'un JPEG, lues dans ses marqueurs SOF."""
    with open(chemin, 'rb') as f:
        if f.read(2) != b'\xff\xd8':
            return None, None
        while True:
            octet = f.read(1)
            if not octet:
                return None, None
            if octet != b'\xff':
                continue
            while octet == b'\xff':
                octet = f.read(1)
            marqueur = octet[0]
            taille = int.from_bytes(f.read(2), 'big')
            if 0xC0 <= marqueur <= 0xCF and marqueur not in (0xC4, 0xC8, 0xCC):
                f.read(1)
                h = int.from_bytes(f.read(2), 'big')
                w = int.from_bytes(f.read(2), 'big')
                return w, h
            f.read(taille - 2)


MARQUE = ('<a class="marque" href="index.html">__DIAMANT__'
          '<span>JN<b>CORP</b> Studio</span>'
          '<span class="ph-marque" data-fr="nom a definir" '
          'data-en="name to be set">nom a definir</span></a>')


def entete(page):
    def lien(href, cle, fr, en):
        a = ' aria-current="page"' if cle == page else ''
        return ('<a href="%s"%s data-fr="%s" data-en="%s">%s</a>'
                % (href, a, e(fr), e(en), fr))
    liens = ''.join([
        lien('index.html#services', '', 'Ce que nous faisons', 'What we do'),
        lien('index.html#methode', '', 'La methode', 'Method'),
        lien('realisations.html', 'realisations', 'Realisations', 'Work'),
        lien('index.html#contact', '', 'Contact', 'Contact'),
    ])
    return ('<header class="haut" id="haut"><div class="haut-in">'
            + MARQUE.replace('__DIAMANT__', DIAMANT)
            + '<nav class="nav">' + liens + '</nav>'
            + '<div class="langue">'
              '<button type="button" data-l="fr" aria-pressed="true">FR</button>'
              '<button type="button" data-l="en" aria-pressed="false">EN</button>'
              '</div></div></header>')


AVERT_FR = ('DEMONSTRATION. Ce site presente une agence en cours de '
            'constitution : le nom, l\'entite juridique et l\'adresse de '
            'contact ne sont pas encore arretes. Les realisations, elles, '
            'sont reelles et en ligne — ce sont les liens ci-dessous.')
AVERT_EN = ('DEMONSTRATION. This site presents an agency being set up: the '
            'name, the legal entity and the contact address are not settled '
            'yet. The work, however, is real and live — those are the links '
            'below.')


def pied():
    return ('<footer><div class="env">'
            + '<div class="avert" data-fr="%s" data-en="%s">%s</div>'
              % (e(AVERT_FR), e(AVERT_EN), e(AVERT_FR))
            + '<div class="liens-sites">'
            + '<a href="%s" data-fr="Annuaire des franchises" '
              'data-en="Franchise directory">Annuaire des franchises</a>'
              % URL_ANNUAIRE
            + '<a href="%s" data-fr="Maisons de prestige" '
              'data-en="Prestige houses">Maisons de prestige</a>'
              % URL_PRESTIGE
            + '</div></div></footer>')


# ---------------------------------------------------------------------------
# LE SCRIPT. Aucune bibliotheque : tout ce qui suit tient en quelques
# dizaines de lignes et n'a rien a telecharger. Une agence qui charge 300 Ko
# de JavaScript pour faire apparaitre trois blocs se contredit sur sa propre
# page de performance.
# ---------------------------------------------------------------------------
JS_SOCLE = r"""
/* La classe `js` conditionne TOUTES les regles d'apparition. Posee ici, en
   premier : sans elle, la feuille de style laisse le contenu visible. */
document.documentElement.classList.add('js');

(function(){
  var doux = window.matchMedia &&
             window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- apparitions au defilement ------------------------------------- */
  var cibles = document.querySelectorAll('.rev, .ligne');
  if (doux || !('IntersectionObserver' in window)){
    /* Pas d'observateur, ou mouvement refuse : on montre tout, tout de
       suite. Le contenu n'est jamais l'otage d'une animation. */
    for (var i=0;i<cibles.length;i++) cibles[i].classList.add('vu');
  } else {
    var obs = new IntersectionObserver(function(entrees){
      entrees.forEach(function(en){
        if (en.isIntersecting){ en.target.classList.add('vu');
                                obs.unobserve(en.target); }
      });
    }, {rootMargin:'0px 0px -8% 0px', threshold:.08});
    for (var j=0;j<cibles.length;j++) obs.observe(cibles[j]);
  }

  /* --- l'en-tete prend son filet une fois qu'on a quitte le haut ----- */
  var haut = document.getElementById('haut');
  function surDefilement(){
    if (haut) haut.classList.toggle('pose', window.scrollY > 12);
  }
  surDefilement();
  window.addEventListener('scroll', surDefilement, {passive:true});

  /* --- l'index des services ------------------------------------------ */
  /* Un seul ouvert a la fois. `aria-expanded` suit l'etat : sans lui, un
     lecteur d'ecran annonce un bouton qui ne dit pas ce qu'il fait. */
  document.addEventListener('click', function(ev){
    var b = ev.target.closest && ev.target.closest('.ligne-idx > button');
    if (!b) return;
    var l = b.parentNode;
    var ouvert = l.getAttribute('data-ouvert') === 'oui';
    var toutes = document.querySelectorAll('.ligne-idx');
    for (var i=0;i<toutes.length;i++){
      toutes[i].setAttribute('data-ouvert','non');
      toutes[i].querySelector('button').setAttribute('aria-expanded','false');
    }
    if (!ouvert){
      l.setAttribute('data-ouvert','oui');
      b.setAttribute('aria-expanded','true');
    }
  });

  /* --- le curseur ----------------------------------------------------- */
  /* Seulement sur un pointeur fin, et jamais sous mouvement reduit : un
     rond qui traine derriere un doigt sur un ecran tactile est un bug. */
  var fin = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
  if (fin && !doux){
    var c = document.createElement('div');
    c.className = 'curseur';
    c.setAttribute('aria-hidden','true');
    document.body.appendChild(c);
    var x = 0, y = 0, cx = 0, cy = 0, vu = false;
    document.addEventListener('mousemove', function(ev){
      x = ev.clientX; y = ev.clientY;
      if (!vu){ vu = true; c.classList.add('actif'); cx = x; cy = y; }
      var sur = ev.target.closest &&
                ev.target.closest('a,button,input,select,textarea');
      c.classList.toggle('gros', !!sur);
    });
    (function boucle(){
      cx += (x - cx) * .18; cy += (y - cy) * .18;
      c.style.transform = 'translate3d(' + (cx - 13) + 'px,'
                                         + (cy - 13) + 'px,0)';
      requestAnimationFrame(boucle);
    })();
    document.addEventListener('mouseleave', function(){
      c.classList.remove('actif'); vu = false;
    });
  }
})();
"""

JS_LANGUE = """
(function(){
  var L = 'fr';
  function pose(l){
    L = l;
    document.documentElement.lang = l;
    var n = document.querySelectorAll('[data-fr][data-en]');
    for (var i=0;i<n.length;i++) n[i].innerHTML = n[i].getAttribute('data-'+l);
    /* Le texte alternatif d'une image est du contenu, pas de la decoration :
       c'est meme le seul contenu que lit un lecteur d'ecran. */
    var im = document.querySelectorAll('img[data-alt-fr][data-alt-en]');
    for (var k=0;k<im.length;k++)
      im[k].setAttribute('alt', im[k].getAttribute('data-alt-'+l));
    var ph = document.querySelectorAll('[data-ph-fr][data-ph-en]');
    for (var q=0;q<ph.length;q++)
      ph[q].setAttribute('placeholder', ph[q].getAttribute('data-ph-'+l));
    var b = document.querySelectorAll('.langue button');
    for (var j=0;j<b.length;j++)
      b[j].setAttribute('aria-pressed',
                        b[j].getAttribute('data-l') === l ? 'true' : 'false');
    try { localStorage.setItem('jn-langue', l); } catch(e){}
    if (window.surLangue) window.surLangue(l);
  }
  window.langue = function(){ return L; };
  document.addEventListener('click', function(ev){
    var b = ev.target.closest && ev.target.closest('.langue button');
    if (b) pose(b.getAttribute('data-l'));
  });
  var m = null;
  try { m = localStorage.getItem('jn-langue'); } catch(e){}
  pose(m === 'en' ? 'en' : 'fr');
})();
"""

JS_FORM = r"""
/* Le formulaire n'envoie rien : c'est une demonstration, et le dire est plus
   honnete qu'un faux « message envoye ». Il valide quand meme, parce que la
   validation est justement ce qu'il faut montrer. */
(function(){
  var f = document.getElementById('demande');
  if (!f) return;
  var T = {
    fr:{manque:'Il manque : ', nom:'votre nom', ecrire:'un moyen de vous repondre',
        projet:'quelques mots sur le projet',
        recu:"Demonstration : rien n'a ete envoye. Sur le site reel, cette demande arriverait a l'agence. Recapitulatif : "},
    en:{manque:'Missing: ', nom:'your name', ecrire:'a way to reply to you',
        projet:'a few words about the project',
        recu:'Demonstration: nothing was sent. On the live site this request would reach the agency. Summary: '}
  };
  f.addEventListener('submit', function(ev){
    ev.preventDefault();
    var L = window.langue ? window.langue() : 'fr';
    var t = T[L];
    var nom = document.getElementById('f-nom').value.trim();
    var rep = document.getElementById('f-contact').value.trim();
    var pro = document.getElementById('f-projet').value.trim();
    var manque = [];
    if (!nom) manque.push(t.nom);
    if (!rep) manque.push(t.ecrire);
    if (!pro) manque.push(t.projet);
    var r = document.getElementById('recu');
    r.hidden = false;
    if (manque.length){ r.textContent = t.manque + manque.join(', '); return; }
    var s = document.getElementById('f-service');
    r.textContent = t.recu + [nom, rep,
      s.options[s.selectedIndex].text].join(' — ');
  });
})();
"""

SQUELETTE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITRE__</title>
<meta name="description" content="__DESC__">
<meta name="robots" content="noindex">
<style>
__CSS__
</style>
</head>
<body>
__CORPS__
<script>
__JS__
</script>
</body>
</html>
"""


def squelette(titre, desc, corps, js):
    return (SQUELETTE.replace('__TITRE__', e(titre))
                     .replace('__DESC__', e(desc))
                     .replace('__CSS__', CSS.strip())
                     .replace('__CORPS__', corps)
                     .replace('__JS__', js.strip()))


def titre_coupe(lignes_fr, lignes_en, balise='h1'):
    """Un titre coupe LIGNE PAR LIGNE, chaque ligne entrant en decale.

    Les coupures sont ecrites a la main plutot que calculees : une coupure
    automatique tombe au hasard des largeurs d'ecran, et un titre de trois
    mots se retrouve coupe apres « de ».
    """
    o = ['<%s>' % balise]
    for i, (fr, en) in enumerate(zip(lignes_fr, lignes_en)):
        o.append('<span class="ligne" style="transition-delay:%dms">'
                 '<span data-fr="%s" data-en="%s">%s</span></span>'
                 % (i * 90, e(fr), e(en), fr))
    o.append('</%s>' % balise)
    return ''.join(o)


def bandeau():
    """Le bandeau defilant. Decoratif, donc `aria-hidden`.

    La piste est ecrite DEUX FOIS : l'animation translate de -50 %, donc la
    seconde moitie prend exactement la place de la premiere et la boucle est
    invisible. Avec une seule copie, le bandeau se vide puis saute.
    """
    mots = ''.join('<span>%s</span>' % e(m) for m in BANDEAU)
    return ('<div class="bandeau" aria-hidden="true">'
            '<div class="bandeau-piste">%s%s</div></div>' % (mots, mots))


def bloc_fondateur():
    o = ['<section class="fond" id="fondateur"><div class="env">',
         '<div class="fond-in">',
         rev(photo('images/fondateur.jpg',
                   '%s, fondateur' % FONDATEUR['nom'],
                   '%s, founder' % FONDATEUR['nom'])),
         '<div class="rev">',
         bi('Le fondateur', 'The founder', 'p', 'eti'),
         '<h2 class="t2">%s</h2>' % e(FONDATEUR['nom']),
         '<p class="fond-role" data-fr="%s" data-en="%s">%s</p>'
         % (e(FONDATEUR['role_fr']), e(FONDATEUR['role_en']),
            e(FONDATEUR['role_fr'])),
         # La devise est la sienne, reprise telle qu'il l'a formulee.
         '<p class="devise">' + DIAMANT
         + '<span data-fr="%s" data-en="%s">%s</span></p>'
         % (e(DEVISE_FR), e(DEVISE_EN), e(DEVISE_FR)),
         # Aucune biographie ecrite a sa place : trois lignes plausibles sur
         # une personne reelle sont une affirmation publiee sur elle.
         '<p class="tbc" data-fr="%s" data-en="%s">%s</p>'
         % (e('Texte du fondateur a fournir'),
            e('Founder statement to be supplied'),
            e('Texte du fondateur a fournir')),
         '</div></div></div></section>']
    return ''.join(o)


# ===========================================================================
#                                 L'ACCUEIL
# ===========================================================================
def page_accueil():
    n_reas = len(REALISATIONS)
    n_controles = sum(r[4] for r in REALISATIONS)

    o = [entete('accueil')]

    # ------------------------------------------------------------------ hero
    o.append('<div class="hero"><div class="grille-fond" aria-hidden="true">'
             '</div><div class="env">')
    o.append(rev(bi('Agence de developpement web', 'Web development studio',
                    'p', 'eti')))
    o.append(titre_coupe(
        ['Des sites qui', '<em>font</em> quelque chose,',
         'pas des sites qui', 'y ressemblent.'],
        ['Sites that', '<em>do</em> something,',
         'not sites that', 'look like it.']))
    o.append('<div class="hero-bas"><div class="rev">')
    o.append(bi('Nous ecrivons des sites et des outils sur mesure : '
                'annuaires filtrables, boutiques, espaces prives, '
                'integrations. Chaque livraison part en ligne le jour ou '
                'elle est finie, et chacune est verifiee par des controles '
                'qui rejouent le parcours dans un vrai navigateur.',
                'We write bespoke sites and tools: filterable directories, '
                'shops, private areas, integrations. Every delivery goes '
                'live the day it is done, and each one is verified by checks '
                'that replay the journey in a real browser.', 'p', 'chapo'))
    o.append('<div class="actions">')
    o.append('<a class="btn" href="#contact"><span data-fr="Parler d\'un '
             'projet" data-en="Talk about a project">Parler d\'un projet'
             '</span></a>')
    o.append('<a class="btn creux" href="realisations.html"><span '
             'data-fr="Voir les realisations" data-en="See the work">'
             'Voir les realisations</span></a>')
    o.append('</div></div>')

    # Les trois nombres, dans le hero. Recomptables, tous les trois : une
    # agence qui commence n'a pas « 200 projets », et les ecrire quand meme
    # donne une page indefendable en rendez-vous.
    o.append('<div class="rev" style="transition-delay:120ms">'
             '<div class="mesures">')
    for val, fr, en in ((n_reas, 'Sites en ligne', 'Sites live'),
                        (n_controles, 'Controles automatiques',
                         'Automated checks'),
                        (2, 'Langues par site', 'Languages per site')):
        o.append('<div class="mesure"><b>%d</b>'
                 '<span data-fr="%s" data-en="%s">%s</span></div>'
                 % (val, e(fr), e(en), e(fr)))
    o.append('</div></div></div></div></div>')

    o.append(bandeau())

    # -------------------------------------------------------------- services
    o.append('<section id="services"><div class="env">')
    o.append('<div class="duo">')
    o.append('<div class="rev">')
    o.append(bi('Ce que nous faisons', 'What we do', 'p', 'eti'))
    o.append(bi('Six livrables, pas six competences.',
                'Six deliverables, not six skills.', 'h2', 't2'))
    o.append('</div><div class="rev">')
    o.append(bi('« Nous maitrisons React » ne dit rien a personne. Ce qui se '
                'commande, c\'est un resultat : un annuaire qui filtre, une '
                'boutique qui encaisse, un outil que vos equipes ouvrent le '
                'matin. Ouvrez une ligne pour le detail.',
                '"We know React" tells nobody anything. What can be ordered '
                'is a result: a directory that filters, a shop that takes '
                'money, a tool your teams open in the morning. Open a row '
                'for the detail.', 'p', 'intro'))
    o.append('</div></div>')

    # L'index. Un bouton par ligne, `aria-expanded` tenu par le script : un
    # <div> cliquable n'est pas atteignable au clavier et ne s'annonce pas.
    o.append('<div class="index">')
    for i, (cle, tfr, ten, pfr, pen, dfr, den) in enumerate(SERVICES, 1):
        o.append('<div class="ligne-idx rev" data-ouvert="non">')
        o.append('<button type="button" aria-expanded="false" '
                 'aria-controls="d-%s">' % e(cle))
        o.append('<span class="num">%02d</span>' % i)
        o.append('<h3 data-fr="%s" data-en="%s">%s</h3>'
                 % (e(tfr), e(ten), e(tfr)))
        o.append('<span class="plus" aria-hidden="true">+</span>')
        o.append('</button>')
        o.append('<div class="detail" id="d-%s"><div><div class="detail-in">'
                 % e(cle))
        o.append('<span></span>')
        o.append('<p data-fr="%s" data-en="%s">%s</p>'
                 % (e(pfr), e(pen), e(pfr)))
        o.append(liste(dfr, den))
        o.append('</div></div></div></div>')
    o.append('</div></div></section>')

    # -------------------------------------------------------------- methode
    o.append('<section id="methode"><div class="env"><div class="methode">')
    o.append('<div class="methode-fixe rev">')
    o.append(bi('La methode', 'Method', 'p', 'eti'))
    o.append(bi('On montre en ligne avant de facturer la suite.',
                'We show it live before invoicing what comes next.',
                'h2', 't2'))
    o.append(bi('C\'est la seule facon honnete de vendre du developpement : '
                'vous jugez sur une page qui existe, pas sur une maquette '
                'retouchee ni sur le portfolio d\'un autre.',
                'It is the only honest way to sell development work: you '
                'judge a page that exists, not a retouched mockup or '
                'somebody else\'s portfolio.', 'p', 'intro'))
    o.append('</div><div>')
    for i, (cle, tfr, ten, pfr, pen) in enumerate(ETAPES, 1):
        o.append('<div class="etape rev">')
        o.append('<div class="num">%02d</div>' % i)
        o.append('<h3 data-fr="%s" data-en="%s">%s</h3>'
                 % (e(tfr), e(ten), e(tfr)))
        o.append('<p data-fr="%s" data-en="%s">%s</p>'
                 % (e(pfr), e(pen), e(pfr)))
        o.append('</div>')
    o.append('</div></div></div></section>')

    # ------------------------------------------------------------ technique
    o.append('<section id="technique"><div class="env">')
    o.append('<div class="duo"><div class="rev">')
    o.append(bi('La technique', 'The stack', 'p', 'eti'))
    o.append(bi('Groupee par role.', 'Grouped by role.', 'h2', 't2'))
    o.append('</div><div class="rev">')
    o.append(bi('Une rangee de logos ne dit pas quel probleme chaque outil '
                'resout, ni pourquoi on en choisit un plutot qu\'un autre '
                'selon ce que vous hebergez deja.',
                'A row of logos does not say which problem each tool solves, '
                'nor why one is picked over another depending on what you '
                'already host.', 'p', 'intro'))
    o.append('</div></div>')
    o.append('<div class="tech rev">')
    for cle, tfr, ten, lfr, len_ in TECHNIQUE:
        o.append('<div class="tech-bloc">')
        o.append('<h3 data-fr="%s" data-en="%s">%s</h3>'
                 % (e(tfr), e(ten), e(tfr)))
        o.append(liste(lfr, len_))
        o.append('</div>')
    o.append('</div></div></section>')

    # --------------------------------------------------------- realisations
    o.append('<section id="realisations"><div class="env">')
    o.append('<div class="duo"><div class="rev">')
    o.append(bi('Realisations', 'Work', 'p', 'eti'))
    o.append(bi('Trois sites, en ligne, ouvrables maintenant.',
                'Three sites, live, open them now.', 'h2', 't2'))
    o.append('</div><div class="rev">')
    o.append(bi('Ce sont de vraies livraisons, pas des visuels de '
                'presentation. Les donnees qu\'ils affichent sont des '
                'donnees de demonstration, et chaque site le dit lui-meme '
                'en toutes lettres.',
                'These are real deliveries, not presentation visuals. The '
                'data they show is demonstration data, and each site says so '
                'itself in plain words.', 'p', 'intro'))
    o.append('</div></div>')
    o.append('<div class="travaux">')
    for i, (cle, nom, url, _s, ctrl, rfr, ren, _a, _b) in enumerate(
            REALISATIONS, 1):
        o.append('<a class="travail rev" href="realisations.html#%s">'
                 % e(cle))
        o.append('<span class="num">%02d</span>' % i)
        o.append('<div><h3>%s <span class="fleche" aria-hidden="true">&rarr;'
                 '</span></h3>' % e(nom))
        o.append('<p class="res" data-fr="%s" data-en="%s">%s</p></div>'
                 % (e(rfr), e(ren), e(rfr)))
        o.append('<div class="cote">')
        o.append('<span><b>%d</b> <span data-fr="controles" '
                 'data-en="checks">controles</span></span>' % ctrl)
        o.append('<span data-fr="Francais et anglais" '
                 'data-en="French and English">Francais et anglais</span>')
        o.append('</div></a>')
    o.append('</div></div></section>')

    # ------------------------------------------------------------ variables
    o.append('<section id="devis"><div class="env">')
    o.append('<div class="duo"><div class="rev">')
    o.append(bi('Combien ca coute', 'What it costs', 'p', 'eti'))
    o.append(bi('Aucun tarif ici, et ce n\'est pas un oubli.',
                'No price here, and it is not an oversight.', 'h2', 't2'))
    o.append('</div><div class="rev">')
    o.append(bi('Un « a partir de » affiche sans connaitre le projet est '
                'faux dans un sens ou dans l\'autre : soit il fait fuir un '
                'client dont le besoin etait simple, soit il engage sur un '
                'chiffre intenable. Voici plutot les cinq choses qui '
                'determinent un devis.',
                'A "from X" shown without knowing the project is wrong in '
                'one direction or the other: it either scares off a client '
                'whose need was simple, or commits to a figure that cannot '
                'hold. Here instead are the five things that set a quote.',
                'p', 'intro'))
    o.append('</div></div>')
    o.append('<div class="vars rev">')
    for tfr, ten, pfr, pen in VARIABLES:
        o.append('<div class="var">')
        o.append('<h3 data-fr="%s" data-en="%s">%s</h3>'
                 % (e(tfr), e(ten), e(tfr)))
        o.append('<p data-fr="%s" data-en="%s">%s</p>'
                 % (e(pfr), e(pen), e(pfr)))
        o.append('</div>')
    o.append('</div>')
    o.append(rev(bi('Nous travaillons par tranches : chaque tranche est '
                    'chiffree avant d\'etre commencee, livree en ligne, et '
                    'payee une fois acceptee.',
                    'We work in slices: each slice is quoted before it '
                    'starts, delivered live, and paid once accepted.',
                    'p', 'avis')))
    o.append('</div></section>')

    o.append(bloc_fondateur())

    # -------------------------------------------------------------- contact
    o.append('<section id="contact"><div class="env">')
    o.append('<div class="duo"><div class="rev">')
    o.append(bi('Contact', 'Contact', 'p', 'eti'))
    o.append(bi('Dites ce que le site doit faire. Le reste suit.',
                'Say what the site has to do. The rest follows.',
                'h2', 't2'))
    o.append('</div><div class="rev">')
    o.append(bi('Formulaire de demonstration : il valide, il recapitule, et '
                'il n\'envoie rien. L\'adresse de reception reste a definir.',
                'Demonstration form: it validates, it summarises, and it '
                'sends nothing. The receiving address is still to be set.',
                'p', 'intro'))
    o.append('</div></div>')
    o.append('<form class="form rev" id="demande" novalidate>')
    o.append('<div><label for="f-nom" data-fr="Votre nom" '
             'data-en="Your name">Votre nom</label>'
             '<input class="champ" id="f-nom" name="nom"></div>')
    o.append('<div><label for="f-contact" data-fr="Ou vous repondre" '
             'data-en="Where to reply">Ou vous repondre</label>'
             '<input class="champ" id="f-contact" name="contact" '
             'data-ph-fr="Telephone, messagerie, ce que vous voulez" '
             'data-ph-en="Phone, messaging, whatever suits you" '
             'placeholder="Telephone, messagerie, ce que vous voulez"></div>')
    o.append('<div class="large"><label for="f-service" '
             'data-fr="Ce dont il s\'agit" data-en="What it is about">'
             'Ce dont il s\'agit</label>'
             '<select class="champ" id="f-service" name="service">'
             + ''.join('<option value="%s" data-fr="%s" data-en="%s">%s</option>'
                       % (e(s[0]), e(s[1]), e(s[2]), e(s[1]))
                       for s in SERVICES)
             + '</select></div>')
    o.append('<div class="large"><label for="f-projet" '
             'data-fr="Le projet, en quelques lignes" '
             'data-en="The project, in a few lines">'
             'Le projet, en quelques lignes</label>'
             '<textarea class="champ" id="f-projet" name="projet"></textarea>'
             '</div>')
    o.append('<div class="large"><button class="btn" type="submit">'
             '<span data-fr="Envoyer la demande" data-en="Send the request">'
             'Envoyer la demande</span></button></div>')
    o.append('<div class="large recu" id="recu" hidden></div>')
    o.append('</form>')

    o.append('<div class="rev" style="margin-top:56px">')
    o.append(bi('A trancher avant la mise en ligne',
                'To settle before going live', 'p', 'eti'))
    o.append(liste(A_TRANCHER, A_TRANCHER))
    o.append('</div>')
    o.append('</div></section>')

    o.append(pied())

    return squelette(
        'JNCORP Studio — agence de developpement web',
        'Sites et outils sur mesure : annuaires filtrables, boutiques, '
        'espaces prives, integrations. Chaque livraison en ligne et '
        'verifiee.',
        ''.join(o), JS_SOCLE + '\n' + JS_LANGUE + '\n' + JS_FORM)


# ===========================================================================
#                             LES REALISATIONS
# ===========================================================================
def page_realisations():
    o = [entete('realisations')]
    o.append('<div class="hero" style="padding:170px 0 0">'
             '<div class="grille-fond" aria-hidden="true"></div>'
             '<div class="env">')
    o.append(rev(bi('Realisations', 'Work', 'p', 'eti')))
    o.append(titre_coupe(['Trois sites,', 'en ligne, ouverts.'],
                         ['Three sites,', 'live, open.']))
    o.append('<div class="hero-bas"><div class="rev">')
    o.append(bi('Aucun visuel de presentation : les liens vont vers les '
                'sites eux-memes. Les donnees affichees sont des donnees de '
                'demonstration, et chaque site le dit lui-meme.',
                'No presentation visuals: the links go to the sites '
                'themselves. The data shown is demonstration data, and each '
                'site says so itself.', 'p', 'chapo'))
    o.append('</div></div></div></div>')

    o.append('<section><div class="env"><div class="travaux">')
    for i, (cle, nom, url, _s, ctrl, rfr, ren, pfr, pen) in enumerate(
            REALISATIONS, 1):
        o.append('<article class="travail rev" id="%s" '
                 'style="align-items:start">' % e(cle))
        o.append('<span class="num">%02d</span>' % i)
        o.append('<div><h3>%s</h3>' % e(nom))
        o.append('<p class="res" data-fr="%s" data-en="%s">%s</p>'
                 % (e(rfr), e(ren), e(rfr)))
        o.append(liste(pfr, pen))
        o.append('<p style="margin-top:22px"><a class="btn" href="%s">'
                 '<span data-fr="Ouvrir le site" data-en="Open the site">'
                 'Ouvrir le site</span></a></p></div>' % url)
        o.append('<div class="cote">')
        o.append('<span><b>%d</b> <span data-fr="controles automatiques" '
                 'data-en="automated checks">controles automatiques</span>'
                 '</span>' % ctrl)
        o.append('<span data-fr="Francais et anglais" '
                 'data-en="French and English">Francais et anglais</span>')
        o.append('<span data-fr="En ligne" data-en="Live">En ligne</span>')
        o.append('<span class="tbc demo" data-fr="Donnees de demonstration" '
                 'data-en="Demonstration data">Donnees de demonstration'
                 '</span>')
        o.append('</div></article>')
    o.append('</div></div></section>')

    o.append(bloc_fondateur())
    o.append(pied())

    return squelette(
        'Realisations — JNCORP Studio',
        'Trois sites livres et en ligne : annuaire de franchises, '
        'hotellerie de chaine, maisons de prestige.',
        ''.join(o), JS_SOCLE + '\n' + JS_LANGUE)


def main():
    if not os.path.isdir(DEMO):
        os.makedirs(DEMO)
    pages = {'index.html': page_accueil(),
             'realisations.html': page_realisations()}
    ecrits = []
    for nom, html in pages.items():
        chemin = os.path.join(DEMO, nom)
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(html)
        ecrits.append((chemin, len(html.encode('utf-8'))))
    return ecrits


if __name__ == '__main__':
    for c, n in main():
        print('%s  (%d octets)' % (c, n))
    tout = ''
    for nom in ('index.html', 'realisations.html'):
        tout += open(os.path.join(DEMO, nom), encoding='utf-8').read()
    print('%d elements traduits, %d diamants, %d blocs a apparition'
          % (len(re.findall(r'data-fr="', tout)),
             tout.count('class="diamant"'),
             len(re.findall(r'class="[^"]*\brev\b', tout))))
