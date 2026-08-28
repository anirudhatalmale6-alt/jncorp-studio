# -*- coding: utf-8 -*-
"""La charte du site de l'agence.

Sombre, comme le site de prestige, mais ce n'est PAS la meme charte et elle
n'est pas partagee : le prestige parle en serif et champagne, l'agence parle
en grotesque et en monospace. Deux sites du meme groupe peuvent partager une
couleur de fond sans partager un caractere.

Quatre regles tenues partout :

  - un seul accent. Un violet electrique, et rien d'autre. Deux accents sur
    un site d'agence donnent une page de promotion.
  - le monospace ne sert qu'aux ETIQUETTES : numeros de section, libelles,
    unites. Un paragraphe en monospace se lit deux fois moins vite.
  - toutes les animations passent par une seule variable de duree, mise a
    zero sous `prefers-reduced-motion`. Un mouvement qu'on ne peut pas
    couper est un defaut d'accessibilite, pas un effet.
  - les lignes de grille du fond sont decoratives : `aria-hidden`, et
    aucune information ne repose dessus.
"""

CSS = """
:root{
  --nuit:#08080b;        /* le fond */
  --nuit2:#0e0e13;       /* surface posee dessus */
  --nuit3:#15151d;       /* surface au-dessus encore */
  --trait:rgba(233,233,244,.11);
  --trait2:rgba(233,233,244,.24);
  --texte:#e9e9f4;
  --doux:#a3a3b8;
  --faible:#74748c;
  --vif:#8b7cff;         /* l'unique accent */
  --vif-doux:rgba(139,124,255,.13);
  --vif-fort:#a596ff;
  --sans:'Inter','Segoe UI',system-ui,-apple-system,Roboto,Helvetica,Arial,
         sans-serif;
  --mono:ui-monospace,'SF Mono','JetBrains Mono','Cascadia Mono',Menlo,
         Consolas,monospace;
  --duree:.22s;
  --rayon:3px;
}
@media(prefers-reduced-motion:reduce){ :root{ --duree:0s } }
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media(prefers-reduced-motion:reduce){ html{scroll-behavior:auto} }
html,body{margin:0;padding:0}
body{background:var(--nuit);color:var(--texte);font-family:var(--sans);
 font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased;
 overflow-x:hidden}
a{color:inherit}
img{max-width:100%}
.env{max-width:1240px;margin:0 auto;padding:0 32px}

/* --------------------------------------------------------------- etiquettes */
.eti{font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--vif);margin:0 0 16px;
 display:flex;align-items:center;gap:12px}
.eti::before{content:'';width:22px;height:1px;background:var(--vif);flex:none}
.num{font-family:var(--mono);font-size:11.5px;color:var(--faible);
 letter-spacing:.1em}

/* ------------------------------------------------------------------ en-tete */
.haut{position:sticky;top:0;z-index:70;background:rgba(8,8,11,.82);
 backdrop-filter:blur(16px);border-bottom:1px solid var(--trait)}
.haut-in{display:flex;align-items:center;gap:24px;max-width:1240px;
 margin:0 auto;padding:15px 32px}
.marque{display:flex;align-items:center;gap:10px;text-decoration:none;
 font-weight:700;font-size:18px;letter-spacing:.02em;white-space:nowrap}
.marque b{color:var(--vif);font-weight:700}
.ph-marque{font-family:var(--mono);font-size:9.5px;letter-spacing:.04em;
 font-weight:400;color:var(--vif);border:1px dashed var(--trait2);
 border-radius:var(--rayon);padding:1px 6px;white-space:nowrap}
.nav{display:flex;gap:20px;margin-left:auto;align-items:center}
.nav a{font-family:var(--mono);font-size:12px;letter-spacing:.09em;
 text-transform:uppercase;text-decoration:none;color:var(--doux);
 padding:6px 0;border-bottom:1px solid transparent;
 transition:color var(--duree),border-color var(--duree)}
.nav a:hover,.nav a[aria-current]{color:var(--texte);
 border-bottom-color:var(--vif)}
.langue{display:flex;border:1px solid var(--trait);border-radius:var(--rayon);
 overflow:hidden}
.langue button{background:none;border:0;color:var(--doux);cursor:pointer;
 font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;padding:6px 10px;
 transition:background var(--duree),color var(--duree)}
.langue button[aria-pressed=true]{background:var(--vif);color:#0a0714}

/* --------------------------------------------------------------------- hero */
.hero{position:relative;padding:96px 0 104px;overflow:hidden;
 border-bottom:1px solid var(--trait)}
/* Les lignes de grille sont DECORATIVES : rien ne doit s'y lire. */
.grille-fond{position:absolute;inset:0;pointer-events:none;
 background-image:
   linear-gradient(to right,var(--trait) 1px,transparent 1px),
   linear-gradient(to bottom,var(--trait) 1px,transparent 1px);
 background-size:78px 78px;
 mask-image:radial-gradient(ellipse 80% 60% at 50% 0%,#000 20%,transparent 78%);
 -webkit-mask-image:radial-gradient(ellipse 80% 60% at 50% 0%,#000 20%,transparent 78%)}
.hero .env{position:relative}
h1{font-size:clamp(36px,6.2vw,74px);line-height:1.03;letter-spacing:-.03em;
 font-weight:700;margin:0 0 26px;max-width:19ch}
h1 em{font-style:normal;color:var(--vif)}
.chapo{font-size:19px;color:var(--doux);max-width:60ch;margin:0 0 36px}
.actions{display:flex;gap:14px;flex-wrap:wrap}

/* ------------------------------------------------------------------ boutons */
.btn{display:inline-flex;align-items:center;gap:10px;background:var(--vif);
 color:#0a0714;text-decoration:none;font-family:var(--mono);font-size:12.5px;
 letter-spacing:.1em;text-transform:uppercase;font-weight:600;
 padding:14px 26px;border:1px solid var(--vif);border-radius:var(--rayon);
 cursor:pointer;transition:background var(--duree),transform var(--duree)}
.btn:hover{background:var(--vif-fort);transform:translateY(-1px)}
.btn.creux{background:none;color:var(--texte);border-color:var(--trait2)}
.btn.creux:hover{background:rgba(233,233,244,.05);border-color:var(--vif)}

/* ----------------------------------------------------------------- sections */
section{padding:86px 0;border-bottom:1px solid var(--trait)}
.t2{font-size:clamp(26px,3.6vw,42px);line-height:1.12;letter-spacing:-.02em;
 font-weight:700;margin:0 0 18px;max-width:20ch}
.intro{color:var(--doux);max-width:64ch;margin:0 0 44px;font-size:17px}

/* --------------------------------------------------------------- les chiffres */
.mesures{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
 gap:1px;background:var(--trait);border:1px solid var(--trait);
 border-radius:var(--rayon);overflow:hidden}
.mesure{background:var(--nuit);padding:26px 24px}
.mesure b{display:block;font-size:clamp(30px,4vw,44px);line-height:1;
 font-weight:700;letter-spacing:-.02em}
.mesure span{display:block;margin-top:10px;font-family:var(--mono);
 font-size:11px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--faible)}

/* --------------------------------------------------------------- les services */
.cartes{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));
 gap:20px}
.carte{position:relative;background:var(--nuit2);border:1px solid var(--trait);
 border-radius:var(--rayon);padding:28px 26px 30px;
 transition:border-color var(--duree),transform var(--duree)}
.carte:hover{border-color:var(--trait2);transform:translateY(-2px)}
/* Un filet d'accent en haut, qui se remplit au survol. */
.carte::before{content:'';position:absolute;top:-1px;left:-1px;
 width:38px;height:2px;background:var(--vif);border-radius:2px;
 transition:width var(--duree)}
.carte:hover::before{width:calc(100% + 2px)}
.carte h3{font-size:20px;line-height:1.25;margin:16px 0 10px;font-weight:650;
 letter-spacing:-.01em}
.carte p{margin:0 0 16px;color:var(--doux);font-size:15px}
.carte ul{margin:0;padding:0;list-style:none;border-top:1px solid var(--trait);
 padding-top:14px}
.carte li{position:relative;padding-left:18px;font-size:14px;color:var(--doux);
 margin-bottom:6px}
.carte li::before{content:'';position:absolute;left:0;top:9px;width:6px;
 height:6px;border:1px solid var(--vif);border-radius:1px;transform:rotate(45deg)}

/* --------------------------------------------------------------- la methode */
.etapes{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
 gap:0;border:1px solid var(--trait);border-radius:var(--rayon);
 overflow:hidden}
.etape{padding:30px 26px 34px;border-right:1px solid var(--trait);
 background:var(--nuit2)}
.etape:last-child{border-right:0}
.etape h3{font-size:19px;margin:14px 0 10px;font-weight:650}
.etape p{margin:0;color:var(--doux);font-size:14.5px}
.barre-etape{height:2px;background:var(--trait);position:relative}
.barre-etape i{position:absolute;inset:0 auto 0 0;width:26%;
 background:var(--vif);display:block}

/* -------------------------------------------------------------- la technique */
.tech{display:grid;grid-template-columns:repeat(auto-fit,minmax(268px,1fr));
 gap:20px}
.tech-bloc{border:1px solid var(--trait);border-radius:var(--rayon);
 padding:24px 22px;background:var(--nuit2)}
.tech-bloc h3{font-family:var(--mono);font-size:11.5px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--vif);margin:0 0 14px;font-weight:600}
.tech-bloc ul{margin:0;padding:0;list-style:none}
.tech-bloc li{font-size:14.5px;color:var(--doux);padding:8px 0;
 border-bottom:1px solid var(--trait)}
.tech-bloc li:last-child{border-bottom:0}

/* ------------------------------------------------------------ realisations */
.reas{display:grid;gap:20px}
.rea{display:grid;grid-template-columns:1fr 300px;gap:36px;align-items:start;
 border:1px solid var(--trait);border-radius:var(--rayon);
 padding:30px 30px 32px;background:var(--nuit2);
 transition:border-color var(--duree)}
.rea:hover{border-color:var(--trait2)}
.rea h3{font-size:24px;margin:14px 0 12px;font-weight:680;letter-spacing:-.015em}
.rea p{margin:0 0 18px;color:var(--doux)}
.rea ul{margin:0 0 20px;padding:0;list-style:none}
.rea li{position:relative;padding-left:18px;font-size:14.5px;color:var(--doux);
 margin-bottom:7px}
.rea li::before{content:'';position:absolute;left:0;top:9px;width:6px;height:6px;
 border:1px solid var(--vif);border-radius:1px;transform:rotate(45deg)}
.rea-cote{border-left:1px solid var(--trait);padding-left:28px}
.rea-mes{font-family:var(--mono);font-size:12.5px;color:var(--faible);
 display:flex;justify-content:space-between;gap:12px;padding:9px 0;
 border-bottom:1px solid var(--trait)}
.rea-mes b{color:var(--texte);font-weight:600}
.puce-vert{display:inline-flex;align-items:center;gap:7px;
 font-family:var(--mono);font-size:11px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--vif);background:var(--vif-doux);
 border:1px solid rgba(139,124,255,.3);border-radius:var(--rayon);
 padding:4px 9px}

/* ---------------------------------------------------------------- variables */
.vars{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
 gap:1px;background:var(--trait);border:1px solid var(--trait);
 border-radius:var(--rayon);overflow:hidden}
.var{background:var(--nuit);padding:24px 22px}
/* Cinq elements dans une grille a quatre colonnes laissent une case vide
   qui se lit comme un oubli. Le dernier prend la largeur restante. */
.var:last-child{grid-column:1/-1}
.var h3{font-size:17px;margin:0 0 8px;font-weight:650}
.var p{margin:0;font-size:14.5px;color:var(--doux)}
.avis{margin-top:26px;border-left:2px solid var(--vif);padding:4px 0 4px 18px;
 color:var(--doux);font-size:15px;max-width:70ch}

/* ---------------------------------------------------------------- fondateur */
.fond{background:var(--nuit2)}
.fond-in{display:grid;grid-template-columns:280px 1fr;gap:48px;
 align-items:center}
.fond-photo img{display:block;width:100%;height:auto;
 border:1px solid var(--trait);border-radius:var(--rayon)}
.fond-role{font-family:var(--mono);font-size:12px;letter-spacing:.13em;
 text-transform:uppercase;color:var(--vif);margin:0 0 20px}
.devise{display:flex;align-items:center;gap:12px;margin:0 0 20px;
 font-size:21px;font-weight:600;letter-spacing:-.01em}
.devise .diamant{width:22px;height:22px;color:var(--vif)}
.diamant{fill:none;stroke:currentColor;stroke-width:1.25;
 stroke-linejoin:round;stroke-linecap:round;flex:none}
.marque .diamant{width:20px;height:20px;color:var(--vif)}
.tbc{display:inline-block;font-family:var(--mono);font-size:12px;
 padding:4px 10px;border:1px dashed var(--trait2);border-radius:var(--rayon);
 background:var(--vif-doux);color:var(--vif);letter-spacing:.04em}

/* ----------------------------------------------------------------- contact */
.form{display:grid;grid-template-columns:1fr 1fr;gap:18px;max-width:760px}
.form .large{grid-column:1/-1}
.form label{display:block;font-family:var(--mono);font-size:11px;
 letter-spacing:.12em;text-transform:uppercase;color:var(--faible);
 margin-bottom:7px}
.champ{width:100%;background:var(--nuit3);color:var(--texte);
 border:1px solid var(--trait);border-radius:var(--rayon);padding:11px 13px;
 font:inherit;font-size:15px;transition:border-color var(--duree)}
.champ:focus{outline:0;border-color:var(--vif)}
.champ::placeholder{color:var(--faible)}
textarea.champ{min-height:120px;resize:vertical}
.recu{border:1px solid rgba(139,124,255,.36);background:var(--vif-doux);
 border-radius:var(--rayon);padding:18px;font-size:15px}

/* -------------------------------------------------------------------- pied */
footer{padding:52px 0 66px;color:var(--faible);font-size:13.5px}
footer a{color:var(--doux)}
.avert{border:1px dashed var(--trait2);border-radius:var(--rayon);
 padding:15px 17px;margin-bottom:26px;color:var(--doux);font-size:13.5px}
.liens-sites{display:flex;gap:24px;flex-wrap:wrap;margin-top:16px}

/* Le focus clavier doit rester visible sur TOUS les fonds sombres. */
a:focus-visible,button:focus-visible,input:focus-visible,
select:focus-visible,textarea:focus-visible{
  outline:2px solid var(--vif);outline-offset:2px}

/* ---------------------------------------------------------------- reglages */
@media(max-width:960px){
  .rea{grid-template-columns:1fr;gap:24px}
  .rea-cote{border-left:0;border-top:1px solid var(--trait);
   padding-left:0;padding-top:20px}
  .fond-in{grid-template-columns:1fr;gap:26px}
  .fond-photo{max-width:260px}
  .etape{border-right:0;border-bottom:1px solid var(--trait)}
  .etape:last-child{border-bottom:0}
}
@media(max-width:620px){
  .env,.haut-in{padding-left:20px;padding-right:20px}
  section{padding:56px 0}
  .hero{padding:56px 0 64px}
  .haut-in{gap:12px;flex-wrap:wrap}
  .nav{order:3;width:100%;margin-left:0;gap:14px;
   border-top:1px solid var(--trait);padding-top:10px;overflow-x:auto}
  .nav a{white-space:nowrap;font-size:11px}
  .langue{margin-left:auto}
  .form{grid-template-columns:1fr}
  .marque{font-size:16px}
}
"""
