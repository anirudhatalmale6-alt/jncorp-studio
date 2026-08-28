# -*- coding: utf-8 -*-
"""La charte du site de l'agence.

Refondue apres les references envoyees par le client (Locomotive, DIA Studio,
Instrument, Fantasy, Clay, Bureau Borsche). Ce que ces six-la ont en commun,
et qui a ete repris ici — la GRAMMAIRE, pas les pages :

  - une typographie de titre demesuree, chassee serree, qui porte le message
    a elle seule. Pas d'illustration pour combler ;
  - une grille volontairement asymetrique, et du vide assume ;
  - un index numerote plutot qu'une grille de cartes : on lit une liste, on
    ouvre ce qui interesse ;
  - du mouvement declenche par le defilement, discret, et une seule
    micro-interaction par element ;
  - tres peu de couleurs. Un fond, un texte, un accent.

TROIS REGLES QUI NE SE NEGOCIENT PAS, quelles que soient les references :

  1. Rien n'est cache par defaut. Les animations d'apparition ne s'activent
     que si le script a tourne (classe `js` posee sur <html>). Sans elle,
     tout est visible : un site dont le contenu depend du JavaScript est un
     site blanc le jour ou le JavaScript echoue.
  2. `prefers-reduced-motion` coupe TOUT : les transitions, le defilement
     anime, le bandeau defilant, le curseur. Un mouvement qu'on ne peut pas
     arreter est un defaut d'accessibilite, pas un effet.
  3. Le contraste reste mesure sur les couleurs REELLEMENT appliquees, et
     les controles echouent en dessous des seuils WCAG.
"""

CSS = """
:root{
  --nuit:#08080b;
  --nuit2:#0e0e13;
  --nuit3:#15151d;
  --trait:rgba(233,233,244,.11);
  --trait2:rgba(233,233,244,.24);
  --texte:#e9e9f4;
  --doux:#a9a9bd;
  --faible:#7b7b93;
  --vif:#8b7cff;
  --vif-doux:rgba(139,124,255,.13);
  --vif-fort:#a596ff;
  --sans:'Inter','Segoe UI',system-ui,-apple-system,Roboto,Helvetica,Arial,
         sans-serif;
  --mono:ui-monospace,'SF Mono','JetBrains Mono','Cascadia Mono',Menlo,
         Consolas,monospace;
  --duree:.5s;
  --court:.22s;
  --courbe:cubic-bezier(.16,1,.3,1);
  --rayon:3px;
}
@media(prefers-reduced-motion:reduce){ :root{ --duree:0s; --court:0s } }
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media(prefers-reduced-motion:reduce){ html{scroll-behavior:auto} }
html,body{margin:0;padding:0}
body{background:var(--nuit);color:var(--texte);font-family:var(--sans);
 font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased;
 overflow-x:hidden}
a{color:inherit}
img{max-width:100%}
.env{max-width:1400px;margin:0 auto;padding:0 40px}
::selection{background:var(--vif);color:#0a0714}

/* ------------------------------------------------------- apparitions ---- */
/* La classe `js` n'existe que si le script a tourne. Sans elle, aucune de
   ces regles ne s'applique et la page est simplement visible. */
.js .rev{opacity:0;transform:translateY(20px);
 transition:opacity var(--duree) var(--courbe),
            transform var(--duree) var(--courbe)}
.js .rev.vu{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){
  .js .rev{opacity:1;transform:none;transition:none}
}

/* --------------------------------------------------------- etiquettes --- */
.eti{font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;
 text-transform:uppercase;color:var(--vif);margin:0 0 20px;
 display:flex;align-items:center;gap:14px}
.eti::before{content:'';width:26px;height:1px;background:var(--vif);flex:none}
.num{font-family:var(--mono);font-size:11.5px;color:var(--faible);
 letter-spacing:.1em}

/* ------------------------------------------------------------ en-tete --- */
.haut{position:fixed;top:0;left:0;right:0;z-index:80;
 background:rgba(8,8,11,.72);backdrop-filter:blur(18px);
 border-bottom:1px solid transparent;transition:border-color var(--court)}
.haut.pose{border-bottom-color:var(--trait)}
.haut-in{display:flex;align-items:center;gap:24px;max-width:1400px;
 margin:0 auto;padding:16px 40px}
.marque{display:flex;align-items:center;gap:11px;text-decoration:none;
 font-weight:700;font-size:18px;letter-spacing:-.01em;white-space:nowrap}
.marque b{color:var(--vif);font-weight:700}
.ph-marque{font-family:var(--mono);font-size:9.5px;letter-spacing:.04em;
 font-weight:400;color:var(--vif);border:1px dashed var(--trait2);
 border-radius:var(--rayon);padding:1px 6px;white-space:nowrap}
.nav{display:flex;gap:26px;margin-left:auto;align-items:center}
/* Le soulignement se dessine de gauche a droite au survol : une seule
   micro-interaction, la meme partout. */
.nav a{position:relative;font-family:var(--mono);font-size:12px;
 letter-spacing:.1em;text-transform:uppercase;text-decoration:none;
 color:var(--doux);padding:6px 0;transition:color var(--court)}
.nav a::after{content:'';position:absolute;left:0;right:100%;bottom:0;
 height:1px;background:var(--vif);transition:right var(--court) var(--courbe)}
.nav a:hover{color:var(--texte)}
.nav a:hover::after,.nav a[aria-current]::after{right:0}
.langue{display:flex;border:1px solid var(--trait);border-radius:var(--rayon);
 overflow:hidden}
.langue button{background:none;border:0;color:var(--doux);cursor:pointer;
 font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;padding:6px 10px;
 transition:background var(--court),color var(--court)}
.langue button[aria-pressed=true]{background:var(--vif);color:#0a0714}

/* ---------------------------------------------------------------hero --- */
.hero{position:relative;padding:152px 0 0;overflow:hidden}
.grille-fond{position:absolute;inset:0;pointer-events:none;
 background-image:
   linear-gradient(to right,var(--trait) 1px,transparent 1px),
   linear-gradient(to bottom,var(--trait) 1px,transparent 1px);
 background-size:96px 96px;
 mask-image:radial-gradient(ellipse 70% 55% at 30% 0%,#000 10%,transparent 72%);
 -webkit-mask-image:radial-gradient(ellipse 70% 55% at 30% 0%,#000 10%,transparent 72%)}
.hero .env{position:relative}
/* La typographie de titre porte la page a elle seule. Chassee serree, et
   coupee ligne par ligne pour que chaque ligne entre en decale. */
h1{font-size:clamp(38px,7.4vw,116px);line-height:.96;letter-spacing:-.042em;
 font-weight:700;margin:0 0 44px;max-width:15ch}
h1 em{font-style:normal;color:var(--vif)}
.ligne{display:block;overflow:hidden}
.js .ligne > span{display:block;transform:translateY(105%);
 transition:transform .85s var(--courbe)}
.js .ligne.vu > span{transform:none}
@media(prefers-reduced-motion:reduce){
  .js .ligne > span{transform:none;transition:none}
}
.hero-bas{display:grid;grid-template-columns:1fr minmax(320px,42%);
 gap:60px;align-items:end;padding-bottom:70px}
.chapo{font-size:18px;color:var(--doux);max-width:56ch;margin:0 0 30px}
.actions{display:flex;gap:14px;flex-wrap:wrap}

/* ------------------------------------------------------- le bandeau --- */
/* Defilant, decoratif, `aria-hidden` : rien ne s'y lit qui ne soit ailleurs.
   Il s'arrete completement sous « mouvement reduit ». */
.bandeau{border-top:1px solid var(--trait);border-bottom:1px solid var(--trait);
 overflow:hidden;padding:20px 0;background:var(--nuit2)}
.bandeau-piste{display:flex;width:max-content;
 animation:defile 46s linear infinite}
.bandeau-piste span{font-family:var(--mono);font-size:12.5px;
 letter-spacing:.2em;text-transform:uppercase;color:var(--faible);
 padding:0 26px;white-space:nowrap;display:flex;align-items:center;gap:26px}
.bandeau-piste span::after{content:'';width:5px;height:5px;
 border:1px solid var(--vif);transform:rotate(45deg);display:block}
@keyframes defile{ from{transform:translateX(0)} to{transform:translateX(-50%)} }
@media(prefers-reduced-motion:reduce){
  .bandeau-piste{animation:none}
  .bandeau{overflow-x:auto}
}

/* ---------------------------------------------------------- sections --- */
section{padding:120px 0;border-bottom:1px solid var(--trait)}
.t2{font-size:clamp(30px,5.2vw,72px);line-height:1.02;letter-spacing:-.035em;
 font-weight:700;margin:0 0 24px;max-width:16ch}
.intro{color:var(--doux);max-width:60ch;margin:0 0 56px;font-size:17px}
/* Grille asymetrique : le titre ne demarre pas au meme endroit que le texte.
   C'est ce decalage qui fait la difference avec une page centree. */
.duo{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);
 gap:80px;align-items:start}

/* ------------------------------------------------------ les mesures --- */
.mesures{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
 gap:0;border-top:1px solid var(--trait)}
.mesure{padding:32px 28px 32px 0;border-right:1px solid var(--trait)}
.mesure:last-child{border-right:0}
.mesure b{display:block;font-size:clamp(38px,5.4vw,68px);line-height:1;
 font-weight:700;letter-spacing:-.04em}
.mesure span{display:block;margin-top:12px;font-family:var(--mono);
 font-size:11px;letter-spacing:.14em;text-transform:uppercase;
 color:var(--faible)}

/* --------------------------------------------- l'index des services --- */
/* Un index numerote plutot qu'une grille de cartes : on parcourt une liste,
   on ouvre ce qui interesse. Le detail s'ouvre en hauteur (0fr -> 1fr), ce
   qui s'anime sans hauteur codee en dur. */
.index{border-top:1px solid var(--trait)}
.ligne-idx{border-bottom:1px solid var(--trait)}
.ligne-idx > button{width:100%;background:none;border:0;color:inherit;
 font:inherit;text-align:left;cursor:pointer;padding:34px 0;
 display:grid;grid-template-columns:64px 1fr auto;gap:28px;align-items:baseline;
 transition:color var(--court)}
.ligne-idx > button:hover{color:var(--vif)}
.ligne-idx h3{font-size:clamp(21px,2.9vw,38px);line-height:1.08;
 letter-spacing:-.025em;font-weight:650;margin:0}
.ligne-idx .plus{font-family:var(--mono);font-size:20px;color:var(--faible);
 line-height:1;transition:transform var(--court) var(--courbe),
                          color var(--court)}
.ligne-idx[data-ouvert=oui] .plus{transform:rotate(45deg);color:var(--vif)}
.detail{display:grid;grid-template-rows:0fr;
 transition:grid-template-rows var(--duree) var(--courbe)}
.ligne-idx[data-ouvert=oui] .detail{grid-template-rows:1fr}
.detail > div{overflow:hidden}
.detail-in{display:grid;grid-template-columns:64px minmax(0,1fr) minmax(0,1fr);
 gap:28px;padding:0 0 38px}
.detail-in p{margin:0;color:var(--doux);font-size:16px}
.detail-in ul{margin:0;padding:0;list-style:none}
.detail-in li{position:relative;padding-left:20px;font-size:15px;
 color:var(--doux);margin-bottom:9px}
.detail-in li::before{content:'';position:absolute;left:0;top:9px;width:6px;
 height:6px;border:1px solid var(--vif);transform:rotate(45deg)}

/* ----------------------------------------------------- la methode --- */
/* Colonne de gauche collante, etapes qui defilent a droite : la structure
   reste visible pendant qu'on lit le detail. */
.methode{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);
 gap:80px;align-items:start}
.methode-fixe{position:sticky;top:120px}
.etape{padding:44px 0;border-top:1px solid var(--trait)}
.etape:first-child{border-top:0;padding-top:0}
.etape h3{font-size:clamp(22px,2.6vw,32px);margin:14px 0 12px;font-weight:650;
 letter-spacing:-.02em}
.etape p{margin:0;color:var(--doux);font-size:16px;max-width:52ch}

/* --------------------------------------------------- la technique --- */
.tech{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
 gap:0;border-top:1px solid var(--trait)}
.tech-bloc{padding:32px 30px 34px 0;border-right:1px solid var(--trait)}
.tech-bloc:last-child{border-right:0}
.tech-bloc h3{font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--vif);margin:0 0 18px;font-weight:600}
.tech-bloc ul{margin:0;padding:0;list-style:none}
.tech-bloc li{font-size:15px;color:var(--doux);padding:11px 0;
 border-bottom:1px solid var(--trait)}
.tech-bloc li:last-child{border-bottom:0}

/* -------------------------------------------------- les realisations --- */
.travaux{border-top:1px solid var(--trait)}
.travail{display:grid;grid-template-columns:64px minmax(0,1fr) minmax(0,320px);
 gap:36px;align-items:center;padding:44px 0;
 border-bottom:1px solid var(--trait);text-decoration:none;
 transition:padding-left var(--duree) var(--courbe),color var(--court)}
.travail:hover{padding-left:18px;color:var(--vif)}
.travail h3{font-size:clamp(24px,4vw,54px);line-height:1.02;
 letter-spacing:-.035em;font-weight:700;margin:0}
.travail .res{margin:12px 0 0;color:var(--doux);font-size:15.5px;
 max-width:54ch}
.travail .cote{display:flex;flex-direction:column;gap:8px;
 font-family:var(--mono);font-size:12px;color:var(--faible)}
.travail .cote b{color:var(--texte);font-weight:600}
.fleche{display:inline-block;transition:transform var(--court) var(--courbe)}
.travail:hover .fleche{transform:translateX(6px)}

/* ------------------------------------------------------- variables --- */
.vars{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
 gap:0;border-top:1px solid var(--trait)}
.var{padding:30px 28px 34px 0;border-right:1px solid var(--trait)}
.var:last-child{border-right:0}
.var h3{font-size:18px;margin:0 0 10px;font-weight:650;letter-spacing:-.01em}
.var p{margin:0;font-size:15px;color:var(--doux)}
.avis{margin-top:34px;border-left:2px solid var(--vif);
 padding:6px 0 6px 20px;color:var(--doux);font-size:16px;max-width:68ch}

/* ------------------------------------------------------- fondateur --- */
.fond{background:var(--nuit2)}
.fond-in{display:grid;grid-template-columns:300px minmax(0,1fr);gap:60px;
 align-items:center}
.fond-photo img{display:block;width:100%;height:auto;
 border:1px solid var(--trait);border-radius:var(--rayon)}
.fond-role{font-family:var(--mono);font-size:12px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--vif);margin:0 0 24px}
.devise{display:flex;align-items:center;gap:14px;margin:0 0 24px;
 font-size:clamp(20px,2.4vw,30px);font-weight:650;letter-spacing:-.02em;
 line-height:1.2}
.devise .diamant{width:26px;height:26px;color:var(--vif)}
.diamant{fill:none;stroke:currentColor;stroke-width:1.25;
 stroke-linejoin:round;stroke-linecap:round;flex:none}
.marque .diamant{width:20px;height:20px;color:var(--vif)}
/* `.demo` est une classe A PART, et pas seulement une variante visuelle :
   c'est elle que le controle compte pour verifier que chaque realisation
   annonce ses donnees de demonstration. Compter une couleur ou une chaine
   de caracteres se casse a la premiere retouche. */
.tbc.demo{border-style:solid;border-color:rgba(139,124,255,.34)}
.tbc{display:inline-block;font-family:var(--mono);font-size:12px;
 padding:4px 10px;border:1px dashed var(--trait2);border-radius:var(--rayon);
 background:var(--vif-doux);color:var(--vif);letter-spacing:.04em}

/* --------------------------------------------------------- boutons --- */
.btn{position:relative;display:inline-flex;align-items:center;gap:10px;
 background:var(--vif);color:#0a0714;text-decoration:none;
 font-family:var(--mono);font-size:12.5px;letter-spacing:.1em;
 text-transform:uppercase;font-weight:600;padding:16px 30px;
 border:1px solid var(--vif);border-radius:var(--rayon);cursor:pointer;
 overflow:hidden;transition:color var(--court)}
.btn > span{position:relative;z-index:1}
/* Le fond se remplit du bas au survol, plutot qu'un changement de couleur. */
.btn::before{content:'';position:absolute;inset:auto 0 0 0;height:0;
 background:var(--vif-fort);transition:height var(--court) var(--courbe)}
.btn:hover::before{height:100%}
.btn.creux{background:none;color:var(--texte);border-color:var(--trait2)}
.btn.creux::before{background:rgba(233,233,244,.07)}
.btn.creux:hover{border-color:var(--vif)}

/* --------------------------------------------------------- contact --- */
.form{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:820px}
.form .large{grid-column:1/-1}
.form label{display:block;font-family:var(--mono);font-size:11px;
 letter-spacing:.13em;text-transform:uppercase;color:var(--faible);
 margin-bottom:8px}
.champ{width:100%;background:transparent;color:var(--texte);border:0;
 border-bottom:1px solid var(--trait2);padding:12px 2px;font:inherit;
 font-size:16px;border-radius:0;transition:border-color var(--court)}
.champ:focus{outline:0;border-bottom-color:var(--vif)}
.champ::placeholder{color:var(--faible)}
select.champ{background:var(--nuit)}
textarea.champ{min-height:120px;resize:vertical}
.recu{border:1px solid rgba(139,124,255,.36);background:var(--vif-doux);
 border-radius:var(--rayon);padding:20px;font-size:16px}

/* ------------------------------------------------------------ pied --- */
footer{padding:70px 0 80px;color:var(--faible);font-size:13.5px}
footer a{color:var(--doux)}
.avert{border:1px dashed var(--trait2);border-radius:var(--rayon);
 padding:17px 19px;margin-bottom:30px;color:var(--doux);font-size:13.5px}
.liens-sites{display:flex;gap:26px;flex-wrap:wrap;margin-top:18px}

/* ---------------------------------------------------------- curseur --- */
/* Uniquement sur un pointeur fin (souris). Sur un ecran tactile il n'y a pas
   de curseur a suivre, et un rond qui traine derriere le doigt est un bug. */
.curseur{position:fixed;top:0;left:0;width:26px;height:26px;
 border:1px solid var(--vif);border-radius:50%;pointer-events:none;z-index:200;
 transform:translate3d(-100px,-100px,0);opacity:0;
 transition:opacity var(--court),width var(--court) var(--courbe),
            height var(--court) var(--courbe)}
.curseur.actif{opacity:1}
.curseur.gros{width:52px;height:52px;background:var(--vif-doux)}
@media(pointer:coarse){ .curseur{display:none} }
@media(prefers-reduced-motion:reduce){ .curseur{display:none} }

/* Le focus clavier reste visible sur TOUS les fonds sombres. */
a:focus-visible,button:focus-visible,input:focus-visible,
select:focus-visible,textarea:focus-visible{
  outline:2px solid var(--vif);outline-offset:3px}

/* --------------------------------------------------------- reglages --- */
@media(max-width:1100px){
  .duo,.methode{grid-template-columns:1fr;gap:40px}
  .methode-fixe{position:static}
  .hero-bas{grid-template-columns:1fr;gap:34px}
  .travail{grid-template-columns:44px minmax(0,1fr);gap:22px}
  .travail .cote{grid-column:2;flex-direction:row;flex-wrap:wrap;gap:20px;
   margin-top:14px}
  .detail-in{grid-template-columns:1fr;gap:18px}
  .ligne-idx > button{grid-template-columns:44px 1fr auto;gap:18px}
  .mesure,.tech-bloc,.var{border-right:0;border-bottom:1px solid var(--trait);
   padding-right:0}
  .mesure:last-child,.tech-bloc:last-child,.var:last-child{border-bottom:0}
  .fond-in{grid-template-columns:1fr;gap:30px}
  .fond-photo{max-width:260px}
}
@media(max-width:620px){
  .env,.haut-in{padding-left:20px;padding-right:20px}
  section{padding:64px 0}
  .hero{padding-top:150px}
  .hero-bas{padding-bottom:44px}
  .haut-in{gap:12px;flex-wrap:wrap}
  .nav{order:3;width:100%;margin-left:0;gap:18px;
   border-top:1px solid var(--trait);padding-top:10px;overflow-x:auto}
  .nav a{white-space:nowrap;font-size:11px}
  .langue{margin-left:auto}
  .form{grid-template-columns:1fr}
  .marque{font-size:16px}
  .ligne-idx > button{padding:26px 0}
}
"""
