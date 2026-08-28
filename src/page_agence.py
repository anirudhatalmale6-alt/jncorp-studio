# -*- coding: utf-8 -*-
"""Construit les deux pages de l'agence : l'accueil et les realisations.

Les CHIFFRES annonces sur l'accueil sont calcules a partir de contenu.py,
jamais tapes dans le HTML : « trois sites livres » ecrit a la main survit a
l'ajout d'un quatrieme, et la page se met a mentir sur elle-meme.

Le nombre de controles automatiques affiche a cote de chaque realisation est
lui aussi une donnee, pas une phrase — et tests-agence.py relance les vraies
suites pour le verifier quand leur arbre est accessible. Un chiffre d'agence
qu'on ne peut pas recompter est un chiffre invente qui a l'air modeste.
"""

import html as _H
import os
import re

from style_agence import CSS
from contenu import (A_TRANCHER, ETAPES, FONDATEUR, REALISATIONS, SERVICES,
                     TECHNIQUE, VARIABLES)
from chemins import dossier_pages

ICI = os.path.dirname(os.path.abspath(__file__))
DEMO = dossier_pages(ICI)

# ---------------------------------------------------------------------------
# LES ADRESSES DES AUTRES SITES DU GROUPE. Sites separes, donc liens absolus,
# et tous ici, en haut — pas disperses dans le corps des pages. Ce sont les
# seules lignes a changer le jour des noms de domaine.
# ---------------------------------------------------------------------------
URL_ANNUAIRE = 'https://anirudhatalmale6-alt.github.io/annuaire-franchises-demo/'
URL_PRESTIGE = 'https://anirudhatalmale6-alt.github.io/maisons-de-prestige/'

# Le meme diamant que sur le site de prestige : c'est la marque du groupe, et
# une marque qui change de dessin d'un site a l'autre n'est plus une marque.
# Trace, jamais une image : net a 16 px comme a 200 px, et il prend la
# couleur du texte partout ou on le pose.
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


def liste(fr, en, classe=''):
    """Une liste bilingue.

    Chaque <li> porte ses deux langues separement. Traduire la liste entiere
    d'un bloc obligerait a stocker du HTML dans un attribut, et la moindre
    apostrophe casserait la page.
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
    return ('<header class="haut"><div class="haut-in">'
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


def bloc_fondateur():
    o = ['<section class="fond" id="fondateur"><div class="env">',
         '<div class="fond-in">',
         photo('images/fondateur.jpg',
               '%s, fondateur' % FONDATEUR['nom'],
               '%s, founder' % FONDATEUR['nom']),
         '<div>',
         bi('Le fondateur', 'The founder', 'p', 'eti'),
         '<h2 class="t2">%s</h2>' % e(FONDATEUR['nom']),
         '<p class="fond-role" data-fr="%s" data-en="%s">%s</p>'
         % (e(FONDATEUR['role_fr']), e(FONDATEUR['role_en']),
            e(FONDATEUR['role_fr'])),
         '<p class="devise">' + DIAMANT
         + '<span>%s</span></p>' % e(FONDATEUR['devise']),
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
    n_services = len(SERVICES)

    o = [entete('accueil')]

    # ------------------------------------------------------------------ hero
    o.append('<div class="hero"><div class="grille-fond" aria-hidden="true">'
             '</div><div class="env">')
    o.append(bi('Agence de developpement web', 'Web development studio',
                'p', 'eti'))
    # Le mot d'accent doit vivre DANS les deux attributs. La bascule de
    # langue remplace l'innerHTML : si le <em> n'existe que dans le texte
    # servi, il disparait des la premiere pose — c'est-a-dire au chargement,
    # avant meme que le visiteur ait touche au bouton.
    h1_fr = ('Des sites qui <em>font</em> quelque chose, pas des sites '
             'qui ressemblent a quelque chose.')
    h1_en = ('Sites that <em>do</em> something, not sites that look like '
             'something.')
    o.append('<h1 data-fr="%s" data-en="%s">%s</h1>'
             % (e(h1_fr), e(h1_en), h1_fr))
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
    o.append('<a class="btn" href="#contact" data-fr="Parler d\'un projet" '
             'data-en="Talk about a project">Parler d\'un projet</a>')
    o.append('<a class="btn creux" href="realisations.html" '
             'data-fr="Voir les realisations" data-en="See the work">'
             'Voir les realisations</a>')
    o.append('</div></div></div>')

    # -------------------------------------------------------------- mesures
    #
    # Trois chiffres, et TOUS les trois sont recomptables. Pas de « 200
    # projets », pas de « 15 ans d'experience » : une agence qui commence n'a
    # pas ces chiffres, et les ecrire quand meme est le plus court chemin
    # vers une page qu'on ne peut pas defendre en rendez-vous.
    o.append('<section><div class="env"><div class="mesures">')
    for val, fr, en in (
            (n_reas, 'Sites en ligne', 'Sites live'),
            (n_controles, 'Controles automatiques', 'Automated checks'),
            (2, 'Langues sur chaque site', 'Languages on every site')):
        o.append('<div class="mesure"><b>%d</b>'
                 '<span data-fr="%s" data-en="%s">%s</span></div>'
                 % (val, e(fr), e(en), e(fr)))
    o.append('</div>')
    o.append('<p class="avis" data-fr="%s" data-en="%s">%s</p>'
             % (e('Ces trois nombres se recomptent : les sites sont '
                  'accessibles plus bas, et le nombre de controles est '
                  'celui qu\'affiche la suite de tests de chaque projet.'),
                e('All three numbers can be recounted: the sites are linked '
                  'below, and the number of checks is the one each '
                  'project\'s test suite prints.'),
                e('Ces trois nombres se recomptent : les sites sont '
                  'accessibles plus bas, et le nombre de controles est '
                  'celui qu\'affiche la suite de tests de chaque projet.')))
    o.append('</div></section>')

    # ------------------------------------------------------------- services
    o.append('<section id="services"><div class="env">')
    o.append(bi('Ce que nous faisons', 'What we do', 'p', 'eti'))
    o.append(bi('Six livrables, pas six competences.',
                'Six deliverables, not six skills.', 'h2', 't2'))
    o.append(bi('« Nous maitrisons React » ne dit rien a personne. Ce qui se '
                'commande, c\'est un resultat : un annuaire qui filtre, une '
                'boutique qui encaisse, un outil que vos equipes ouvrent le '
                'matin.',
                '"We know React" tells nobody anything. What can be ordered '
                'is a result: a directory that filters, a shop that takes '
                'money, a tool your teams open in the morning.',
                'p', 'intro'))
    o.append('<div class="cartes">')
    for i, (cle, tfr, ten, pfr, pen, dfr, den) in enumerate(SERVICES, 1):
        o.append('<article class="carte">')
        o.append('<div class="num">%02d</div>' % i)
        o.append('<h3 data-fr="%s" data-en="%s">%s</h3>'
                 % (e(tfr), e(ten), e(tfr)))
        o.append('<p data-fr="%s" data-en="%s">%s</p>'
                 % (e(pfr), e(pen), e(pfr)))
        o.append(liste(dfr, den))
        o.append('</article>')
    o.append('</div></div></section>')

    # -------------------------------------------------------------- methode
    o.append('<section id="methode"><div class="env">')
    o.append(bi('La methode', 'Method', 'p', 'eti'))
    o.append(bi('On montre en ligne avant de facturer la suite.',
                'We show it live before invoicing what comes next.',
                'h2', 't2'))
    o.append(bi('C\'est la seule facon honnete de vendre du developpement : '
                'vous jugez sur une page qui existe, pas sur une maquette '
                'retouchee ni sur un portfolio d\'un autre.',
                'It is the only honest way to sell development work: you '
                'judge a page that exists, not a retouched mockup or '
                'somebody else\'s portfolio.', 'p', 'intro'))
    o.append('<div class="etapes">')
    for i, (cle, tfr, ten, pfr, pen) in enumerate(ETAPES, 1):
        o.append('<div class="etape">')
        o.append('<div class="num">%02d</div>' % i)
        o.append('<h3 data-fr="%s" data-en="%s">%s</h3>'
                 % (e(tfr), e(ten), e(tfr)))
        o.append('<p data-fr="%s" data-en="%s">%s</p>'
                 % (e(pfr), e(pen), e(pfr)))
        o.append('</div>')
    o.append('</div></div></section>')

    # ------------------------------------------------------------ technique
    o.append('<section id="technique"><div class="env">')
    o.append(bi('La technique', 'The stack', 'p', 'eti'))
    o.append(bi('Groupee par role, parce qu\'une rangee de logos ne dit pas '
                'quel probleme chaque outil resout.',
                'Grouped by role, because a row of logos does not say which '
                'problem each tool solves.', 'h2', 't2'))
    o.append('<div class="tech">')
    for cle, tfr, ten, lfr, len_ in TECHNIQUE:
        o.append('<div class="tech-bloc">')
        o.append('<h3 data-fr="%s" data-en="%s">%s</h3>'
                 % (e(tfr), e(ten), e(tfr)))
        o.append(liste(lfr, len_))
        o.append('</div>')
    o.append('</div></div></section>')

    # --------------------------------------------------------- realisations
    o.append('<section id="realisations"><div class="env">')
    o.append(bi('Realisations', 'Work', 'p', 'eti'))
    o.append(bi('Trois sites, en ligne, que vous pouvez ouvrir maintenant.',
                'Three sites, live, that you can open right now.',
                'h2', 't2'))
    o.append(bi('Ce sont de vraies livraisons, pas des visuels de '
                'presentation. Les donnees qu\'ils affichent sont des '
                'donnees de demonstration, et chaque site le dit lui-meme '
                'en toutes lettres.',
                'These are real deliveries, not presentation visuals. The '
                'data they show is demonstration data, and each site says so '
                'itself in plain words.', 'p', 'intro'))
    o.append('<div class="cartes">')
    for cle, nom, url, _suite, ctrl, rfr, ren, _pfr, _pen in REALISATIONS:
        o.append('<article class="carte">')
        o.append('<div class="num">%s</div>' % e(cle.upper()))
        o.append('<h3>%s</h3>' % e(nom))
        o.append('<p data-fr="%s" data-en="%s">%s</p>'
                 % (e(rfr), e(ren), e(rfr)))
        o.append('<ul><li data-fr="%s" data-en="%s">%s</li></ul>'
                 % (e('%d controles automatiques' % ctrl),
                    e('%d automated checks' % ctrl),
                    e('%d controles automatiques' % ctrl)))
        o.append('</article>')
    o.append('</div>')
    o.append('<p style="margin-top:30px"><a class="btn creux" '
             'href="realisations.html" data-fr="Le detail des trois" '
             'data-en="All three in detail">Le detail des trois</a></p>')
    o.append('</div></section>')

    # ------------------------------------------------------------ variables
    #
    # A la place d'un tarif : ce qui le determine. Un « a partir de » invente
    # ici serait un engagement commercial pris a la place du client — la
    # meme regle que sur la page photographie.
    o.append('<section id="devis"><div class="env">')
    o.append(bi('Combien ca coute', 'What it costs', 'p', 'eti'))
    o.append(bi('Aucun tarif sur cette page, et ce n\'est pas un oubli.',
                'No price on this page, and it is not an oversight.',
                'h2', 't2'))
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
    o.append('<div class="vars">')
    for tfr, ten, pfr, pen in VARIABLES:
        o.append('<div class="var">')
        o.append('<h3 data-fr="%s" data-en="%s">%s</h3>'
                 % (e(tfr), e(ten), e(tfr)))
        o.append('<p data-fr="%s" data-en="%s">%s</p>'
                 % (e(pfr), e(pen), e(pfr)))
        o.append('</div>')
    o.append('</div>')
    o.append('<p class="avis" data-fr="%s" data-en="%s">%s</p>'
             % (e('Nous travaillons par tranches : chaque tranche est '
                  'chiffree avant d\'etre commencee, livree en ligne, et '
                  'payee une fois acceptee.'),
                e('We work in slices: each slice is quoted before it starts, '
                  'delivered live, and paid once accepted.'),
                e('Nous travaillons par tranches : chaque tranche est '
                  'chiffree avant d\'etre commencee, livree en ligne, et '
                  'payee une fois acceptee.')))
    o.append('</div></section>')

    o.append(bloc_fondateur())

    # -------------------------------------------------------------- contact
    o.append('<section id="contact"><div class="env">')
    o.append(bi('Contact', 'Contact', 'p', 'eti'))
    o.append(bi('Dites ce que le site doit faire. Le reste suivra.',
                'Say what the site has to do. The rest follows.',
                'h2', 't2'))
    o.append(bi('Formulaire de demonstration : il valide, il recapitule, et '
                'il n\'envoie rien. L\'adresse de reception reste a definir.',
                'Demonstration form: it validates, it summarises, and it '
                'sends nothing. The receiving address is still to be set.',
                'p', 'intro'))
    o.append('<form class="form" id="demande" novalidate>')
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
    o.append('<div class="large"><button class="btn" type="submit" '
             'data-fr="Envoyer la demande" data-en="Send the request">'
             'Envoyer la demande</button></div>')
    o.append('<div class="large recu" id="recu" hidden></div>')
    o.append('</form>')

    o.append('<div style="margin-top:44px">')
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
        ''.join(o), JS_LANGUE + '\n' + JS_FORM)


# ===========================================================================
#                             LES REALISATIONS
# ===========================================================================
def page_realisations():
    o = [entete('realisations')]
    o.append('<div class="hero" style="padding:64px 0 56px">'
             '<div class="grille-fond" aria-hidden="true"></div>'
             '<div class="env">')
    o.append(bi('Realisations', 'Work', 'p', 'eti'))
    o.append('<h1 style="font-size:clamp(30px,4.6vw,50px)" '
             'data-fr="%s" data-en="%s">%s</h1>'
             % (e('Trois sites, en ligne, ouverts.'),
                e('Three sites, live, open.'),
                e('Trois sites, en ligne, ouverts.')))
    o.append(bi('Aucun visuel de presentation : les liens vont vers les '
                'sites eux-memes. Les donnees affichees sont des donnees de '
                'demonstration, et chaque site le dit lui-meme.',
                'No presentation visuals: the links go to the sites '
                'themselves. The data shown is demonstration data, and each '
                'site says so itself.', 'p', 'chapo'))
    o.append('</div></div>')

    o.append('<section><div class="env"><div class="reas">')
    for cle, nom, url, _suite, ctrl, rfr, ren, pfr, pen in REALISATIONS:
        o.append('<article class="rea" id="%s"><div>' % e(cle))
        o.append('<div class="num">%s</div>' % e(cle.upper()))
        o.append('<h3>%s</h3>' % e(nom))
        o.append('<p data-fr="%s" data-en="%s">%s</p>'
                 % (e(rfr), e(ren), e(rfr)))
        o.append(liste(pfr, pen))
        o.append('<a class="btn" href="%s" data-fr="Ouvrir le site" '
                 'data-en="Open the site">Ouvrir le site</a>' % url)
        o.append('</div><div class="rea-cote">')
        o.append('<div class="rea-mes"><span data-fr="Controles" '
                 'data-en="Checks">Controles</span><b>%d</b></div>' % ctrl)
        o.append('<div class="rea-mes"><span data-fr="Langues" '
                 'data-en="Languages">Langues</span><b>FR / EN</b></div>')
        o.append('<div class="rea-mes"><span data-fr="Etat" data-en="Status">'
                 'Etat</span><b data-fr="En ligne" data-en="Live">En ligne'
                 '</b></div>')
        o.append('<p style="margin-top:16px"><span class="puce-vert" '
                 'data-fr="Donnees de demonstration" '
                 'data-en="Demonstration data">Donnees de demonstration'
                 '</span></p>')
        o.append('</div></article>')
    o.append('</div></div></section>')

    o.append(bloc_fondateur())
    o.append(pied())

    return squelette(
        'Realisations — JNCORP Studio',
        'Trois sites livres et en ligne : annuaire de franchises, '
        'hotellerie de chaine, maisons de prestige.',
        ''.join(o), JS_LANGUE)


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
    print('%d elements traduits, %d diamants'
          % (len(re.findall(r'data-fr="', tout)),
             tout.count('class="diamant"')))
