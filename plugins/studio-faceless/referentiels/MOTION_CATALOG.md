# Catalogue des techniques d'animation et de transition

> Règles par défaut du plugin studio-faceless.
> Les écarts de la chaîne (`direction/ECARTS.md`) l'emportent.

**PROPOSITION** : des possibilités, pas un modèle. **Lire l'index, puis la seule fiche utile** (chercher `### ID`) : jamais le fichier entier (environ 31 Ko) ; l'en-tête et l'index tiennent dans les lignes 1 à 93 (lecture par plage), une fiche s'obtient par `grep -n -A 2 "^### ID"` (validé sur AA, 18/10/2026) ; chaque fiche se suffit, sans film ni projet à ouvrir. Toutes sont `expérimental` (réalisées, non jugées par le propriétaire), sauf les dix fiches « Tifo » non réalisées (ligne 18) ; `à améliorer` ou `validé` (accord daté du propriétaire) s'écrivent dans la fiche. Les fiches et la colonne « Épisodes » viennent de la première chaîne (AA, films sportifs) : la technique se transpose à une autre matière.

**Règles communes** (non répétées dans les fiches) :
- une technique sert une idée du récit, sur des médias réels, datés et sourcés (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 bis) ; jamais d'effet diaporama (§ 2) ;
- reprise permise (validé sur AA, 18/10/2026, à la place de « de nouvelles idées à chaque film » du 15/10/2026) : une fiche déjà employée se reprend si elle sert la vision du film, en l'améliorant, sans la recopier ; la colonne « Épisodes » (historique d'AA ; une autre chaîne note ses reprises dans `direction/ECARTS.md`) dit quels films l'ont employée et s'enrichit à chaque reprise ; le directeur artistique choisit les techniques du film, anciennes ou nouvelles ;
- couleurs du récit ; seules la signature, l'appel et l'outro de la chaîne gardent celles de la marque (`marque/README.md`) ;
- schéma ou dessin d'étude : « illustration, not study data » à l'écran, aucun chiffre inventé ;
- un mouvement doux part 0,13 à 0,15 s avant le mot qu'il montre, calé sur les silences réels de la voix ; courbes de caméra continues (cubique monotone) ;
- rendu Chrome : **un texte posé reste immobile** (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 ter, validé sur AA, 20/10/2026). Le rendu recale chaque image au pixel : un texte qui glisse lentement saccade, et la rotation de 0,3° autrefois conseillée n'y change rien. Entrée et sortie courtes seulement, en opacité ou en glissement linéaire de 1 à 2 px entiers par image ; le mouvement vient des photos et des fonds. Contrôle : centre des lettres image par image, car `controle.py tremblement` ne voit pas ce défaut. Flou et 3D CSS coûtent cher : précalculer les versions floues ; textures et aléas à graine fixe.

**Ajouter une technique** : une ligne d'index et une fiche de deux ou trois phrases (Recette, Attention), sans chemin ni temps de film, au statut `expérimental`. Dans une chaîne, elle s'ajoute dans la section MOTION_CATALOG de `direction/ECARTS.md`.

**Choisir** (validé sur AA, 26/10/2026) : le producteur lit cet index et choisit lui-même ses techniques, avec une réflexion écrite avant toute scène (fiche d'effets, skill `studio-faceless:episode`, `references/production.md` § 2) ; chaque film doit faire mieux que le précédent. Les fiches dont la colonne « Épisodes » porte « — (Tifo) » viennent de l'étude AA de Tifo Sports (26/10/2026) : elles ne sont pas encore réalisées.

## Index
| ID | Type | Pour | Épisodes |
|---|---|---|---|
| PAPER-DEPTH | Espace | donner de la profondeur aux images fixes | E003, E004 |
| CONTINUOUS-WORLD | Espace | un seul monde à stations pour une séquence | E004 |
| STRATA | Espace | des époques empilées, traversées en profondeur | E004 |
| ARCHIVE-TABLE | Espace | parcourir une table de tirages réels | E001 |
| DOC-SPACE | Espace | passer d'un groupe de preuves à un autre | E003 |
| TIME-DEPTH | Espace | des années comme une distance, sans frise | E004 |
| SKY-LIFT | Transition | changer de lieu ou d'époque par le ciel | E004 |
| SLOW-HOLD | Transition | faire sentir un arrêt du récit | E004 |
| MATCH-DISSOLVE | Transition | raccord par forme ou par matière | E004 |
| BLUR-PASS | Transition | traverser une photo qui devient décor flou | E004 |
| GUIDE-OBJECT | Transition | un objet de la photo mène la caméra | E004 |
| ECLIPSE-PASS | Transition | une ombre réelle ouvre l'image suivante | E004 |
| CHALK-STRIKE | Transition | un trait raye, l'image s'ouvre le long du trait | E004 |
| WASH-OUT | Transition | effacer un moment comme lavé | E004 |
| NIGHTFALL | Transition | éteindre un moment dans le silence | E004 |
| WHIP-JUMP | Transition | une rupture de temps brutale | E003 |
| SPLIT-SYNC | Transition | deux camps au même instant | E003 |
| TEXT-WINDOW | Transition | un mot qui ouvre sur l'image | E003 |
| LIGHT-WAKE | Transition | une photo qui s'allume au mot | E004 |
| IRIS-OPEN | Transition | un objet rond ouvre la scène suivante | — (Tifo) |
| MATTER-WIPE | Transition | une matière du sujet recouvre et ouvre | — (Tifo) |
| HOLLOW-WORD | Texte | un mot qui naît, puis devient un nom | E004 |
| REDACT-REVEAL | Texte | un mot qui attend d'être dit | E003, E004 |
| PRESS-HIGHLIGHT | Texte | citer la presse, surlignée sur la voix | E003 |
| YEAR-ROLL | Texte | « x years later » | E004 |
| FLEETING-INK | Texte | des lettres qui s'effacent | E004 |
| STRIKE-KEEP | Texte | barrer une idée et la garder | E004 |
| SIGN-RING | Texte | un signe réel devient un fil | E001 |
| RESULT-STRIP | Texte | un score qui revient au même dessin | E001 |
| MATCH-CLOCK | Texte | le chronomètre comme colonne du récit | E003 |
| STACK-LIST | Texte | une liste qui s'empile sur la voix | — (Tifo) |
| DOC-DETAIL | Archive | le détail qui corrige la lecture | E001 |
| PAGE-LIFT | Archive | un vrai titre qui quitte sa page | E004 |
| FOCUS-SHIFT | Archive | passer du fond aux personnes | E001 |
| PRINT-FLIP | Archive | recto, puis verso de tirages réels | E001 |
| BURST | Archive | du mouvement avec des photos en rafale | E003 |
| VIEWFINDER | Archive | « ce moment a été photographié » | E004 |
| HOIST | Archive | un rituel réel sur son vrai lieu | E004 |
| PAPER-CARD | Archive | poser un fait vérifié sur une fiche | E003 |
| BEFORE-AFTER | Archive | l'anomalie en deux images au même cadrage | — (Tifo) |
| CUTOUT-FIGURE | Archive | une personne réelle posée dans un dessin | — (Tifo) |
| UNIT-ROWS | Donnée | une statistique en unités qu'on compte | E004 |
| PHOTO-TO-UNIT | Donnée | une photo qui devient l'unité du graphique | E004 |
| WINDOW-TOKEN | Donnée | la rangée vide s'ouvre sur les gens | E004 |
| GAP-DROP | Donnée | un écart qui ne se reproduit pas | E004 |
| SPOTLIGHT | Donnée | allumer le bloc ou le mot regardé | E004 |
| TICKET-TO-BAR | Donnée | l'objet de l'expérience devient la barre | E004 |
| SCORE-PLATES | Donnée | un score changé à la main | E004 |
| GROWTH-STEPS | Donnée | une histoire qui grossit à chaque retour | E004 |
| STUDY-CURVES | Donnée | la forme d'un résultat publié | E003 |
| RIVALRY-LINE | Donnée | un siècle de matchs en un geste | E003 |
| LEAGUE-FALL | Donnée | une relégation dans un vrai classement | E001 |
| TIERS-LADDER | Donnée | situer un club dans la pyramide | E001 |
| RANK-REVEAL | Donnée | un classement qui confirme, puis casse l'évidence | — (Tifo) |
| DIMENSION-STRETCH | Donnée | une mesure physique qui s'étire à sa valeur | — (Tifo) |
| TALLY | Trait | rendre physique une durée | E004 |
| NAME-BOND | Trait | relier des personnes sans leur image | E004 |
| VERSION-FORK | Trait | deux versions d'une même histoire | E004 |
| CAUSE-SLOT | Schéma | chercher la cause hors de soi | E004 |
| SCAN-REDRAW | Schéma | ce que mesure une étude, sans ses figures | E003 |
| WE-THEY-DIAGRAM | Schéma | le « we » qui devient « they » | E001 |
| BROKEN-THREAD | Schéma | ce qui fait tenir ou céder un lien | E001 |
| SPRING-POP | Schéma | une forme sans texte qui entre à ressort | — (Tifo) |
| ANSWER-ICONS | Schéma | le plan de la réponse en pictogrammes | — (Tifo) |
| DRAWN-METAPHOR | Schéma | une idée abstraite devenue objet du sujet | — (Tifo) |
| ORBIT-DIVE | Carte | de la Terre de nuit à un lieu précis | E001 |
| NIGHT-ROUTE | Carte | un trajet réel sans images du trajet | E001 |
| ARGUMENT-MAP | Carte | une carte qui porte l'argument | E001 |
| BRAND-SPLIT | Marque | signature et outro de la chaîne (ex-AA-SPLIT) | E001, E003, E004 |
| HOLD-CALL | Montage | placer l'appel Like + Subscribe | E004 |

## Fiches

### PAPER-DEPTH · Profondeur en trois plans
**Recette** : sur le fond commun (papier, grain, brume dans les plans de nuit), trois plans à parallaxe différente : fonds flous teintés et vignettés (≈ 0,35 de la vitesse), images nettes à ombre profonde (1), textes et données devant (1,08 à 1,25). Chaque station garde un travelling lent continu (plan proche ≈ 20 à 140 px/s), posé dans sa dernière seconde. **Attention** : c'est un décor, pas une transition ; seul, il n'empêche pas le diaporama.

### CONTINUOUS-WORLD · Un seul monde à stations
**Recette** : toutes les images d'une séquence posées dans un même monde (PAPER-DEPTH) ; la caméra va de station en station par des passages tirés du contenu (bascule vers le bas pour lire, plongée dans une foule, montée en diagonale), avec un seul travelling latéral. Une fois, sur le mot qui élargit l'idée, recul jusqu'au monde entier (zoom ≈ 0,25, étiquettes retirées), puis le pas vers la station suivante. Étiquettes date et lieu attachées à leur image, à taille fixe à l'écran. **Attention** : recul, glissé et zoom avant à chaque image font la structure « Prezi », un diaporama déguisé.

### STRATA · Strates traversées en profondeur
**Recette** : une strate plein cadre par époque ou par lieu, chacune un petit monde 2,5D ; dans une strate, la caméra va d'image en image sans arrêt, souvent avec un léger recul ; on change de strate seulement par un événement du récit (ombre, trait, lavage, nuit). Aucune photo n'en remplace une autre par un fondu. **Attention** : changer de grammaire d'une strate à l'autre, sinon on retombe dans la structure « Prezi ».

### ARCHIVE-TABLE · Table d'archives parcourue
**Recette** : caméra 2D sur un monde de tirages à ombres posés sur papier ; raccords invisibles entre l'intérieur d'une photo et son tirage ; extinction sélective de la lumière. **Attention** : glisse vite vers le diaporama ou le best-of ; pas une grammaire de conclusion par défaut.

### DOC-SPACE · Documents dans l'espace
**Recette** : les fiches et coupures d'une partie flottent en perspective sur fond sombre et sortent par les bords ; la caméra avance et glisse jusqu'au document suivant, où elle se pose (jamais de fondu). Sert de raccord entre deux parties. **Attention** : pas un enchaînement fiche après fiche.

### TIME-DEPTH · Le temps en profondeur
**Recette** : *couloir* : des bornes d'années posées dans le monde, allumées sur le mot, que la caméra dépasse devant un même décor fixé à la caméra (le lieu reste, les années passent). *Écart* : deux dates posées à deux profondeurs, la plus ancienne devant ; un recul fait voir la distance. **Attention** : pas d'axe gradué.

### SKY-LIFT · Le ciel comme passage
**Recette** : la caméra lève les yeux vers le ciel noir de la photo ; l'image suivante (une carte de nuit) naît de ce noir par un masque radial : même nuit, autre lieu. *Variante époque* : montée à travers une nappe de brume (étirée à ≈ 2 900 px, glissée de −720 à +720 px, opacité en demi-sinus), puis descente sur une vue aérienne d'une autre année, en 1,5 à 2 s : la hauteur figure le temps. **Attention** : il faut un vrai ciel sombre ou vide dans la photo.

### SLOW-HOLD · Le travelling qui s'arrête
**Recette** : coupe franche sur un second angle de la scène ; le travelling, qui avançait, ralentit presque jusqu'à l'arrêt (≈ 20 px en 3 s) pendant que le son de la scène (pluie, foule) prend la place de la voix. **Attention** : seulement sur un arrêt réel du récit.

### MATCH-DISSOLVE · Raccord par forme ou par matière
**Recette** : *forme* : la caméra entre dans une forme claire (une enseigne) qui se redresse (≈ 9°) ; la suivante est posée au même endroit et à la même largeur, placement calculé sur l'image, inclinée à l'inverse (≈ −11°) ; fondu de 0,3 s quand elles se recouvrent, puis elle se redresse pendant le recul. *Matière* : des briques se fondent dans d'autres briques pendant une poussée (≈ 0,9 s), par exemple pour boucler sur l'image d'ouverture.

### BLUR-PASS · Traverser une photo jusqu'au flou
**Recette** : la caméra pousse dans la photo jusqu'à un point (une balle, une tribune) et la traverse ; la photo, en version floue précalculée (σ ≈ 9), devient le fond de la scène suivante, à échelle réduite (≈ 30 %). *Variantes* : un élément net recule dans sa propre photo floue, ou en sort. **Attention** : la scène suivante doit se passer dans le lieu traversé.

### GUIDE-OBJECT · L'objet qui guide la caméra
**Recette** : un objet réel de la photo (une balle) part sur une courbe de Bézier, avec une légère traînée ; la caméra le suit jusqu'à la scène suivante, où il devient le premier élément (la première unité d'un graphique). **Attention** : l'objet doit exister dans la photo.

### ECLIPSE-PASS · L'ombre réelle qui ouvre
**Recette** : une ombre ronde réelle de la photo (celle de la Terre sur la Lune) se prolonge en trou de masque (`radial-gradient`) centré sur son bord réel ; le rayon passe d'environ deux rayons de lune à toute l'image en ≈ 1,2 s, avec un liseré coloré ; dans le trou, l'image suivante s'éclaire de 0,55 à 1.

### CHALK-STRIKE · Le trait qui raye et ouvre
**Recette** : un trait texturé (SVG `stroke-dashoffset`, filtre `feTurbulence` + `feDisplacementMap` à graine fixe, son court) raye un compte ou une image ; l'image se fend le long du trait : deux copies découpées en `clip-path` de part et d'autre s'écartent en ≈ 0,75 s sur l'image suivante. *Variante* : une bande s'ouvre le long du trait (masque `linear-gradient` à l'angle du trait, de 0 à pleine largeur en ≈ 0,6 s). **Attention** : le trait doit être un motif du récit, pas un raccord passe-partout.

### WASH-OUT · Le lavage
**Recette** : masque en ≈ 128 bandes verticales (`linear-gradient`), front ondulé (somme de sinus fixes) et coulures de longueurs fixes, lisière ≈ 150 px, du haut vers le bas en ≈ 1,8 s ; un reflet d'eau suit le front ; le contenu lavé descend et s'étire un peu ; l'image suivante apparaît derrière.

### NIGHTFALL · La nuit tombe
**Recette** : l'image passe de la luminosité 1 à 0,1, puis s'efface (≈ 1,8 s) jusqu'au fond seul ; une citation vient dans la nuit, lettres allumées de gauche à droite en ≈ 0,85 s. **Attention** : laisser le silence au son.

### WHIP-JUMP · Le saut dans le temps
**Recette** : les deux photos côte à côte sur une bande ; panoramique filé, avec un flou directionnel au départ et dans le même sens à l'arrivée. **Attention** : une fois par film (effet vitrine).

### SPLIT-SYNC · Au même instant
**Recette** : écran partagé ; la frontière glisse avec la voix vers le camp dont on parle ; les heures des deux images restent synchrones (EXIF corrigé du décalage de chaque appareil) ; chiffres en grand aux couleurs des équipes. **Attention** : deux images au plus (lisibilité sur mobile).

### TEXT-WINDOW · Le mot-fenêtre
**Recette** : un mot en très grand sert de masque, la photo visible dans ses lettres ; la caméra passe à travers une lettre jusqu'à remplir le cadre (ou jusqu'au noir). **Attention** : une ou deux fois par film.

### LIGHT-WAKE · La photo qui s'allume
**Recette** : *néon* : luminosité de 0,1 à 1 en racine carrée, léger halo coloré, sur le mot qui nomme le lieu. *Bain révélateur* (négatif, tirage ancien) : papier blanc, puis les noirs, puis les gris, avec `filter: brightness(k) contrast(c)`, k = 1 + 11 (1 − u)^2,2 sur 1,5 s.

### IRIS-OPEN · L'iris qui part d'un objet rond
**Recette** : un masque circulaire (`clip-path: circle()`) s'ouvre depuis le centre exact d'un objet rond de l'image (cible, ballon, cadran, médaille) et découvre la scène suivante en 0,5 à 0,8 s. **Attention** : seulement quand l'objet porte le lien entre les deux scènes.

### MATTER-WIPE · Le volet de matière
**Recette** : une matière du sujet (terre battue, gazon, encre, papier journal) recouvre l'image en 0,6 à 0,8 s et s'ouvre sur la suivante, avec son bruit de matière (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 2). **Attention** : la matière vient du récit, jamais d'une banque d'effets ; à distinguer de MATCH-DISSOLVE, qui fond deux images.

### HOLLOW-WORD · Le mot creux qui se remplit
**Recette** : le mot en contour seul (`-webkit-text-stroke`), vide tant qu'il n'existe pas ; il se remplit (≈ 0,5 s) quand une source datée l'imprime. *Variante* : le mot reste centré (grille `1fr auto 1fr`, sans mesure du texte) pendant que la phrase autour change jusqu'à devenir un titre. **Attention** : date de la première occurrence vérifiée.

### REDACT-REVEAL · Le mot qui attend
**Recette** : le mot est caché par une bande de la couleur du fond, révélée à l'instant où la voix le dit ; *variante* : un trait vide tient sa place et le mot s'y pose. **Attention** : caler sur le vrai départ du mot dans la bande (silences), pas sur Whisper seul.

### PRESS-HIGHLIGHT · La citation de presse surlignée
**Recette** : citation recomposée dans la typographie du film (en-tête : source, date, heure ; aucune mise en page copiée) ; un surligneur passe sur les mots quand la voix les dit. **Attention** : une phrase surlignée, pas un paragraphe.

### YEAR-ROLL · L'année qui roule
**Recette** : fenêtres de chiffres en `translateY` ; seuls les chiffres qui changent roulent, un par un (≈ 3 s) ; l'image de l'année quittée recule et s'éteint (luminosité → 0,28, saturation → 0,4).

### FLEETING-INK · Les lettres qui s'effacent
**Recette** : une lettre par `span` ; une fois la phrase lue, chacune passe à l'opacité 0,22, monte de 10 px et se floute de 3,5 px, avec 0,16 s de décalage.

### STRIKE-KEEP · Barrer, puis garder
**Recette** : un mot est barré (on voit l'erreur), puis le trait se lève et le mot reste (on le garde).

### SIGN-RING · L'anneau sur un signe réel
**Recette** : un anneau se pose sur un signe déjà dans l'image (le « 0 » d'un score), devient un schéma, puis s'ouvre sur le plan suivant. **Attention** : le signe doit être réel et porter le sens.

### RESULT-STRIP · Le bandeau de résultat
**Recette** : bandeau fixe et peu animé (score réel, date, source), toujours au même dessin, qui revient quand le récit y revient. **Attention** : pas une béquille de sous-titrage.

### MATCH-CLOCK · L'horloge du match
**Recette** : grand compteur de minutes (0' → fin), une tique par minute ; chaque photo réelle entre à sa minute de prise de vue (EXIF corrigé du décalage d'horloge de l'appareil).

### STACK-LIST · La liste qui s'empile
**Recette** : une ligne par élément, posée au mot qui la nomme, en opacité ou en glissement linéaire au pixel entier ; les lignes déjà dites restent, celle qu'on entend s'allume (SPOTLIGHT). **Attention** : cinq lignes au plus ; texte immobile une fois posé.

### DOC-DETAIL · Le détail qui corrige
**Recette** : la caméra va au détail d'un document et s'y arrête au moins 1 s, sans cercle ni halo, puis recule sur les personnes. **Attention** : détail vérifié en pleine résolution, jamais fabriqué.

### PAGE-LIFT · Le titre qui se détache
**Recette** : le vrai titre, découpé dans le scan à sa place exacte (pose calculée dans le plan de la page), quitte la page et vient vers la caméra avec une ombre qui grandit, pendant que la page s'assombrit (≈ 1 s), sur le mot de la voix. **Attention** : ni surlignage ni retouche.

### FOCUS-SHIFT · Mise au point simulée
**Recette** : fondu entre deux versions précalculées de la photo (fond net, puis premier plan net ; détourage propre, flou par convolution normalisée) ; le texte lié au fond part avec lui. **Attention** : rien d'ajouté ni de retiré ; flou déclaré simulé dans la provenance ; une fois par film.

### PRINT-FLIP · Tirages retournés
**Recette** : recul sur des tirages en espace 3D, à des profondeurs différentes ; ils se retournent en cascade (recto, puis verso), puis la caméra s'approche du dernier. **Attention** : l'appariement recto/verso est un montage, et le dispositif doit le montrer.

### BURST · La rafale
**Recette** : les images consécutives d'un même photographe, à quelques secondes d'écart, jouées en saccade (8 à 12 images/s), sans zoom de remplissage. **Attention** : séries vraiment consécutives (écarts EXIF mesurés).

### VIEWFINDER · Le viseur
**Recette** : recul sur les photos d'un même moment ; quatre coins de viseur se referment sur l'une d'elles, avec un déclic léger et une surexposition de 4 images (+35 %) sur cette seule photo.

### HOIST · Le rituel sur son vrai lieu
**Recette** : sur la vraie photo du lieu (un mât), l'objet du rituel (un drapeau) monte pendant que sa drisse se trace depuis le sommet (`scaleY`).

### PAPER-CARD · La fiche papier
**Recette** : une fiche (papier, ombre réelle, léger angle) glisse et se pose ; elle porte un fait vérifié (étude : auteurs, année, effectif, résultat ; match : date, lieu, score ; définition) ; mots clés surlignés ; les fiches s'empilent avec les preuves ; une fiche peut se retourner. **Attention** : vite répétitive.

### BEFORE-AFTER · Avant, après, même cadrage
**Recette** : deux images réelles du même lieu ou du même objet, au même cadrage, à deux dates ; la seconde remplace la première par un volet ou un écran partagé, et un cercle ou une flèche montre la différence. **Attention** : dates sourcées ; forme d'ouverture admise par `${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` § 2 (Ouverture).

### CUTOUT-FIGURE · La personne détourée
**Recette** : une personne clé, détourée à la main (`clip-path` en polygone), en couleurs réelles, est posée dans un dessin, une carte ou un graphique, à 45 % de la hauteur au moins ; son étiquette entre en opacité ou en glissement au pixel entier. **Attention** : quelques personnes par film, photo libre créditée ; jamais de bichromie (validé sur AA, 26/10/2026).

### UNIT-ROWS · Le graphique en unités
**Recette** : rangées d'unités (un essai = une case, un succès = une case remplie, la dernière en fraction) ; une seconde étude se lit dans la même grille, l'écart en couleur. **Attention** : valeurs publiées seulement.

### PHOTO-TO-UNIT · La photo devient l'unité
**Recette** : l'action de la photo aboutit à un point (une balle tombe dans un trou) ; un iris (masque radial) se referme sur ce point et la photo se replie (échelle ≈ 1,4 → 0,16) jusqu'à la taille d'une unité du graphique, qui prend sa place.

### WINDOW-TOKEN · La rangée qui s'ouvre sur les gens
**Recette** : une rangée vide du graphique (« not studied ») s'ouvre en fenêtre (`clip-path: inset`) sur une photo de ceux qu'on n'a pas mesurés ; la photo passe en plein cadre, puis se replie en cercle (`clip-path: circle`), jeton posé dans le graphique suivant.

### GAP-DROP · L'écart qui descend
**Recette** : le segment d'écart d'une étude descend sur la ligne de l'étude suivante et s'y réduit à un point (≈ 0,4 s), dans la même grille et à la même échelle.

### SPOTLIGHT · La lumière sélective
**Recette** : sur le mot de la voix, le bloc ou le mot regardé s'allume et le reste s'éteint ; pas de surligneur ajouté.

### TICKET-TO-BAR · L'objet devient la barre
**Recette** : l'objet de l'expérience (le talon d'un billet) s'étire en barre de graphique ; un geste réel (le billet rendu) peut précéder. **Attention** : valeurs publiées.

### SCORE-PLATES · Le tableau changé à la main
**Recette** : chaque plaque glisse dans sa rainure, d'abord le nom de l'équipe, puis le chiffre ; couleurs réelles des équipes.

### GROWTH-STEPS · L'image qui grandit d'un cran
**Recette** : à chaque retour daté (étiquette d'année), l'image grandit d'un cran (≈ +3 %, somme de marches adoucies). **Attention** : cinq crans au plus ; dates sourcées.

### STUDY-CURVES · Les courbes redessinées
**Recette** : courbes redessinées d'après les valeurs publiées, tracées progressivement et déclarées approximatives à l'écran. **Attention** : sans données publiées, ni courbe ni nuage de points.

### RIVALRY-LINE · La frise d'une rivalité
**Recette** : très longue frise horizontale, un point par match aux couleurs réelles (victoire, nul, défaite) ; la caméra la parcourt vite, ralentit sur trois ou quatre jalons sourcés avec photos libres épinglées, et peut s'arrêter sur le dernier match. **Attention** : jamais la photo d'un autre match présentée comme celle du jalon.

### LEAGUE-FALL · La chute dans le classement
**Recette** : la caméra descend un classement complet jusqu'à la dernière ligne ; l'emblème s'y pose, puis tombe dans la division suivante ; la ligne de chute devient un autre tracé. **Attention** : deux tableaux au plus ; écussons rarement libres de droits.

### TIERS-LADDER · L'échelle des niveaux
**Recette** : niveaux numérotés ; le nom apparaît par fondu à son niveau, l'ancienne position en pointillés. **Attention** : un nom qui descend les niveaux se lit comme une chute.

### RANK-REVEAL · Le classement dévoilé rang par rang
**Recette** : un classement réel se dévoile une ligne à la fois sur la voix ; les premiers rangs confirment l'évidence, puis les suivants la cassent, dans une même couleur qui désigne l'anomalie. **Attention** : classement sourcé et daté ; texte immobile une fois posé.

### DIMENSION-STRETCH · La cote qui s'étire
**Recette** : une mesure physique (largeur, hauteur, distance) est montrée par une cote dessinée ; le trait s'étire en `scaleX` (environ 0,6 s, ease-out) jusqu'à sa nouvelle valeur, puis l'écart s'affiche en texte fixe. **Attention** : valeurs publiées ; seul le trait s'étire, jamais le texte.

### TALLY · Le compte en traits
**Recette** : traits par groupes de cinq (quatre et une barre), tracés en SVG (`stroke-dashoffset`) avec irrégularités et texture à graine fixe ; le compte peut accélérer (départ du trait i : t0 + D · (i / (n − 1))^0,62) et finir sur une date. **Attention** : ni frise ni axe.

### NAME-BOND · Le trait qui relie les noms
**Recette** : des croix au trait marquent des lieux (tombe, ville) ; un trait souligne un nom, puis descend souligner celui d'un proche et sa date : le lien se dessine. **Attention** : aucun portrait de substitution.

### VERSION-FORK · Le récit qui se divise
**Recette** : un trait (SVG `pathLength=1`, `stroke-dashoffset` piloté par le temps) se divise en deux branches, une par version (l'une bute contre un obstacle, l'autre passe, revient et ressort) ; étiquettes courtes, source et mention « illustration » à l'écran.

### CAUSE-SLOT · La case de la cause
**Recette** : la série (les défaites) court vers une flèche qui sort du cadre de l'équipe ; une case vide « dehors » se remplit d'une explication, puis d'une autre.

### SCAN-REDRAW · L'étude redessinée
**Recette** : coupe dessinée au trait ; la zone mesurée s'allume selon la condition que dit la voix. **Attention** : ne suggérer aucune mesure individuelle.

### WE-THEY-DIAGRAM · Le « we » devient « they »
**Recette** : marqueurs « we », du plus au moins identifié, autour du cercle du groupe ; après la défaite, les moins identifiés passent à « they » ; la fiche de l'étude reste visible comme source. **Attention** : un schéma par film au plus.

### BROKEN-THREAD · Le fil qui se rompt
**Recette** : des fils relient les lumières réelles d'une carte à un point ; un fil se distingue, se détend, se rompt, et sa lumière dérive ; une question naît dans l'écart. **Attention** : les points sont des pics lumineux, pas des personnes.

### SPRING-POP · L'apparition à ressort
**Recette** : une forme sans texte (flèche, coche, croix, pictogramme) entre en 150 à 350 ms avec un dépassement de 15 à 20 %, puis s'arrête net. **Attention** : jamais sur un texte ni sur un bloc qui en contient (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 ter) ; sans son par défaut (effets rares dans les films).

### ANSWER-ICONS · Le plan de la réponse en pictogrammes
**Recette** : après la signature, deux ou trois pictogrammes dessinés posent les pistes de la réponse sur leurs mots ; chacun revient en tête de la séquence qui le traite, et s'allume quand sa piste est tranchée. **Attention** : des pistes, jamais la conclusion (`${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` § 2).

### DRAWN-METAPHOR · La métaphore dessinée
**Recette** : une idée abstraite (argent, audience, temps, risque) devient un objet du sujet qui agit (un objet du lieu qui se remplit pour une audience, des marches qui montent pour une ascension) ; elle est nommée dans le plan de plans et apparaît sur le mot. **Attention** : tirée de la matière du sujet, jamais un cliché (pluie de billets, point d'interrogation) ; chiffres réels.

### ORBIT-DIVE · La plongée orbitale
**Recette** : poussée lente sur une photo réelle de la Terre de nuit (ISS, NASA) ; plongée qui tourne d'environ 80° à travers une brume (mode screen) ; fondu sur une carte nocturne (NASA Black Marble) ; une étiquette ancrée garde le même lieu d'une image à l'autre. **Attention** : au-delà d'un zoom ≈ 1,1, les lumières Black Marble font des blocs, flouter en proportion.

### NIGHT-ROUTE · Le trajet de nuit
**Recette** : un point s'allume ; un tracé lissé (Catmull-Rom sur un itinéraire OSRM simplifié) progresse derrière lui ; étiquettes à tige (heure, ville) ; distance posée le long du tracé ; recul jusqu'aux deux extrémités. **Attention** : trajet attesté ; « indicative route » et © OpenStreetMap à l'écran ; personne n'est présenté comme le voyageur.

### ARGUMENT-MAP · La carte qui porte l'argument
**Recette** : un tirage d'archive devient un repère posé sur une carte (OSM) ; flèche en pointillés vers le nouveau lieu ; la même carte mène aux lieux suivants ; routes et terrain inutiles masqués. **Attention** : sans argument spatial, pas de carte.

### BRAND-SPLIT · Signature et outro (ex-AA-SPLIT)
**Recette** : propre à la chaîne (signature et outro, fichiers finis de `marque/`) : voir `direction/ECARTS.md` et `marque/README.md`.

### HOLD-CALL · Pause et appel Like + Subscribe
**Recette** : après la dernière phrase d'une séquence, tenir sa dernière image ≈ 4 s ; poser l'overlay de l'appel (`marque/`) au début de la pause, clics hors de toute voix ; sous la pause, prolonger la musique de la séquence par son passage le plus régulier, au niveau de sa dernière seconde (fondu croisé 0,4 s, fondu de sortie 1 s). **Son** : depuis le 24/10/2026 (validé sur AA), la séquence ne porte que la voix ; musique et clics se posent au mix du film (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 3, `outils/montage/mix_film.py`), pas dans la composition. **Attention** : l'appel ne couvre ni texte ni étiquette.
