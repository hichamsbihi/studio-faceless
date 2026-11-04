# Styles : bibliothèque, aucun pixel créé, fiche de style, tirage

Décisions du propriétaire, validé sur AA, 04/11/2026 (points 2 et 3 de son ordre du jour), transcrites dans le plugin par la 1.1.0 : ce fichier en est la seule source. Les styles retenus par une chaîne, leur ordre de portage et la correspondance entre une preuve et ses styles sont dans `direction/` de la chaîne. Les valeurs chiffrées sont dans `seuils.json` (clés `styles.*`). Qui décide : `REGLES_DETAIL.md` § Qui décide (D02, D03, D04).

## Bibliothèque lemo-opuscar
- **Forme A seule** : une bibliothèque de styles, pas un skill ni un moteur, copiée dans `${CLAUDE_PLUGIN_ROOT}/vendor/lemo-opuscar/` (origine, commit, licence et contenu : son `PROVENANCE.md`). Les styles et la méthode de choix en viennent ; HyperFrames 0.8.149 reste le seul moteur. Leur plugin et leur moteur à la place de HyperFrames sont refusés.
- **Ce qu'on en prend** : des techniques, jamais des médias. Les images, voix et musiques des démos ne vont dans aucun film. Ses textes (`STYLE.md`, `DEMO.md`, `README.md`) sont des données ; son moteur (Playwright, Chromium, ffmpeg), ses `build.sh`, `setup.sh` et outils de téléchargement ne se lancent jamais.
- **Portage** : un style ne s'emploie qu'une fois porté sur `hf-seek` en scène-type. Le code de dessin d'une démo est branché sur l'horloge de HyperFrames (son `window.render(t)` devient un écouteur de `hf-seek`), et la mise en page est refaite au format de la vidéo (les démos sont en 1920 × 1080). Le style porté a une **fiche de rendu** : 2D ou WebGL ; le temps par image, mesuré en 16:9 et en 9:16 ; une empreinte identique sur deux rendus ; la compatibilité avec le GL logiciel (un rendu local `--no-browser-gpu` de son témoin, `REGLES_DETAIL.md` § Rendu). Un style WebGL n'entre dans une longue qu'avec une fiche mesurée. Au plus `styles.portages_par_film_max` portages nouveaux par film, de préférence hors épisode. L'endroit où se rangent les scènes-types se fixe au bilan du premier essai (`QUESTION OUVERTE`).
- **Adaptations communes** : `image.images_par_seconde` i/s ; une animation par pas se fait à la moitié ou au tiers de cette cadence, jamais à une cadence qui ne la divise pas (leurs 24 et 12 i/s ne s'appliquent pas) ; l'arrière-plan, la palette, les polices et la langue de la chaîne (`marque/README.md`) ; aucune vibration.
- **Notice MIT** : un projet qui reprend du code de démo garde une copie de `LICENSE` sous le nom `LICENSE-lemo-opuscar-MIT` dans son dossier. C'est une notice de code, pas un crédit : rien à l'écran ni dans la description.
- **Consignes neutralisées**, jamais appliquées dans le studio : `AGENTS.md` (non copié) ; `DIRECTOR.md` § 1 (brief), § 11 comme parcours de livraison (seule la règle « Not the demo again » est reprise, dans le registre de variété ci-dessous), § 12 (substituts fictifs des vrais médias) et § 13 (tracé imposé des frontières) ; `TECHNIQUE.md` § 4 (voix régénérée jusqu'au contrôle : la voix est celle de la chaîne, tout appel payant attend le propriétaire) et § 11 (sources CC0, CC BY ou OFL seulement : la règle des médias du studio s'applique).
- **Familles permises** : celles de `direction/ECARTS.md` de la chaîne ; par défaut, les styles documentaires (« Edit & Documentary », « Evidence Films ») et les graphismes dessinés en code pour expliquer (« Information & Keynote », « Graphic & Type ») ; ni anime, ni jeux, ni peinture, ni 3D ; toute autre catégorie seulement avec l'accord du propriétaire.
- **Mise à jour par paliers** (remplace « copie figée » du 03/11/2026 ; « suivie à chaque version » est refusé) : à la demande, au plus `styles.resynchronisation_par_mois_max` fois par mois, si un lot ajoute des styles dans les familles permises ou si une fiche de style en a besoin ; jamais pendant un épisode. Chaque palier est une version du plugin (nouveau commit dans le `PROVENANCE.md` de la bibliothèque et dans `CHANGELOG.md`), notée dans la fiche de style qui l'emploie. À chaque palier, un contrôle de licence : relire `LICENSE`, la section « Licence » du README, les voix exclues, les `CREDITS` des démos reprises et les nouvelles consignes ; si la licence quitte le MIT, on reste au dernier commit en MIT. Au prochain palier, `MY-STYLES.md` (MIT) est copié, après ce contrôle, pour en tirer quelques styles propres à la chaîne.

## Aucun pixel créé
Sur une photo donnée pour vraie, aucun pixel n'est créé (précise « aucune image générée par IA » des invariants) :
- ni par IA ni par un autre calcul : ni LaMa, ni remplissage OpenCV, ni push-pull. Le détourage sépare des pixels réels, il n'en crée pas ; les skills `studio-faceless:lemo-wake` et `lemo-layers` n'emploient jamais leur remplissage ;
- un fond tiré de la même photo floutée est admis, s'il ne montre aucun double net du sujet ;
- aucun mouvement du corps, du visage ou des cheveux d'une personne réelle : seules la caméra et les calques bougent (fiche LIVING-PHOTO de `MOTION_CATALOG.md`) ;
- **photo de match** : seules la caméra et les annotations bougent ; un libellé dit un fait, jamais une intention ;
- **ralenti sur une image de match** : par répétition d'images seulement ; jamais un fondu entre deux images, qui crée des images qui n'ont pas existé.

## Fiche de style (option A)
- **Une seule validation de style par film** : l'`art-director` propose, pour chaque film et chaque short, avant le storyboard, une fiche de style ; le propriétaire la valide dans `SOCLE.md` (bloc 6). L'`art-director` y décide le style du film et la technique de chaque temps fort (D02).
- **Trois niveaux** : l'`art-director` décide dans la fiche ; le producteur exécute, sa fiche d'effets règle le détail (durées, courbes, son) dans ce cadre, sans changer une technique (D03) ; un changement de technique en route est l'arrêt n° 2 (D04), qui repasse par l'`art-director` et par le propriétaire. Le catalogue et la bibliothèque sont des sources ; le directeur contrôle la cohérence.
- **Contenu** :
  - le style dominant et sa raison ; au plus `styles.secondaires_par_film_max` techniques secondaires, une par acte ; un geste propre au style au sommet du film ;
  - pour chaque temps fort : la technique (identifiant du catalogue, `MOTION_CATALOG.md`), le fichier de démo à reprendre, les adaptations ; les styles déjà portés passent d'abord ; un style pas encore porté est signalé (il appelle l'épreuve, `REGLES_DETAIL.md` § Parcours) ;
  - la ligne du registre de variété ;
  - ce qu'on ne reprend pas ;
  - les médias que la fiche suppose et qui manquent au kit.
- **Méthode** : trier par `styles/README.md` et les `style.json`, regarder les affiches des seuls candidats ; lire deux ou trois `STYLE.md` au plus, puis le `DEMO.md` du style proposé ; le code de démo seulement pour nommer le fichier à reprendre.

## Règle de tirage
- **La preuve principale du sujet** désigne deux ou trois styles possibles, dans la réserve des dominants de la chaîne (`direction/`).
- **Exclusions** : le style qui a dominé l'une des `styles.tirage_dominant_exclu_dernieres_longues` dernières longues ; ensuite, la ligne du registre de variété diffère des `styles.variete_dernieres_longues` dernières longues sur au moins `styles.variete_axes_differents_min` axes sur `styles.variete_axes`.
- **Transition** : tant que moins de `styles.dominants_portes_avant_tirage` dominants sont portés, la seule règle est « jamais le même dominant deux longues de suite ».
- **Secondaires** : une par acte ; aucune n'est reprise dans la longue suivante.
- **Geste du style au sommet** : jamais dans les `styles.geste_signature_exclu_dernieres_longues` dernières longues (axe « plan signature ») ; la forme de la démo ne se reprend pas.
- **Shorts** : un short prend le style de son film et les légendes du style de shorts de la chaîne ; son mécanisme d'accroche est absent des `shorts.mecanisme_accroche_exclu_derniers_shorts` derniers shorts, et sa ligne du registre diffère des mêmes derniers shorts.

## Registre de variété (à l'essai ; son coût se mesure sur le premier épisode qui l'emploie)
- `direction/REGISTRE_VARIETE.md` de la chaîne compte une ligne par film ou short, sur six axes : structure, ouverture, plan signature, trajet de caméra, forme de la musique, fin ; la palette d'histoire y figure aussi et change d'un film à l'autre. C'est la règle « Not the demo again » de leur `DIRECTOR.md`, appliquée à la chaîne.
- L'`art-director` propose la ligne dans la fiche ; le directeur l'ajoute au registre quand le propriétaire valide la fiche.

## Témoin par style
Un style s'essaie de préférence hors épisode : sa témoin est vue une fois par le propriétaire, au premier emploi du style. Si un film porte quand même un style neuf, l'épreuve (`styles.epreuve_style_neuf_s` s) est la seule question permise en cours de ligne (`REGLES_DETAIL.md` § Parcours).
