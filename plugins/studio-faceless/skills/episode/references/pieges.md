# Pièges connus (à compléter à la fin de chaque épisode)

Format : le piège, puis ce qu'on fait. Source entre parenthèses : les identifiants E001 à E010 sont les épisodes d'AA où le piège est apparu ; chaque chaîne ajoute les siens. Les règles citées sont les règles par défaut du plugin (`${CLAUDE_PLUGIN_ROOT}/referentiels/`) ; les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent.

## Récit
- **Ouverture sur un décor, du contexte ou une personne inconnue, et question après 0:35** : on perd 53 à 60 % des spectateurs à 0:30 (mesure AA). Faire le contraire : personne nommée de face, question avant 0:45 (E001, E003, E004 ; Méthode, étude AA).
- **Une liste à l'écran pour porter l'argument** : c'est un exposé. Il faut un motif matériel tiré des photos (E007 v1).
- **Mauvaise formule finale** : une formule courte vaut mieux qu'un récapitulatif (E007, « Taking it out of memory is another matter »).

## Image
- **Briefs qui décrivent du texte**, donc un diaporama : décrire des transformations d'images (E007 v1, 0 % de plein cadre).
- **Cadres vides et cadres « de verdict » vides** : on ne les comprend pas. Le propriétaire : « le cadre reste vide sans rien dedans ». Montrer la vraie photo puis le graphite, ou un dessin qui explique le manque (E007 v2).
- **Vues d'ensemble en vignettes**, couloir sombre de cadres minuscules : c'est un schéma noir. Plans proches, cadres à 30 % de la hauteur au moins (E007 v2).
- **Écran presque vide** pendant qu'un dessin se trace (« 9 SEASONS » et un trait sur le marine) : mettre une vraie photo derrière le dessin (E007 seq1 v3).
- **Écran noir en milieu de séquence**, ou colonnes tracées avant leur contenu : le contenu se pose pendant le tracé (E007 seq2 v3).
- **Filtres d'image** (grille de 6 px) : retirés à la demande du propriétaire (E007).
- **Petites images agrandies** à la conversion (1920 px forcés) : convertir sans agrandir (E007 v2).
- **Image agrandie à l'écran** : au-delà de son pixel natif, une image s'adoucit ; elle ne dépasse pas 1,3 fois son pixel natif quand elle reste à l'écran, et une archive en 640 × 480 va en cadre-témoin plutôt qu'en plein cadre (validé sur MM, 21/10/2026, audit de son pilote : un clip agrandi deux fois était visiblement mou ; proposé au plugin 0.3.0, PROPOSÉ). Limite de 1,3 fois retenue pour tout le plugin, y compris la recette v3 de `production.md` § 1, qui tolérait 1,6 (VALIDÉ, Hicham, 30/10/2026).
- **Photo répétée** d'une séquence à l'autre : tenir la liste des photos prises (consignes communes).
- **Logos partout** : avec mesure, un ou deux par passage (validé sur AA, 24/10/2026).
- **Rangées d'unités identiques** (70 tuiles jaunes en grille) : le propriétaire y voit « un tableau périodique », qui ne captive pas. Montrer une masse une seule fois, comme un vrai objet (vitrine, terrain, urne) (E010 seq1 v1).
- **Une photo forte devenue motif** (le trophée détouré répété 70 fois) : refusé. Une photo forte se montre une fois (E010 seq1 v2).
- **Passages tout en dessin** : « un peu de vivacité de photo ou de vidéo réelle ; mélanger ». Ouvrir une vraie photo ou un vrai extrait depuis un objet dessiné, sur le mot de la voix (E010 seq1 v3).
- **Ouverture de séquence presque vide** (ligne de jonction et un trait pendant 5 à 7 s avant le premier objet) : contraire à la règle du tiers ; le raccord se remplit dès les premières images (E010 seq4 et seq5, accepté tel quel).

## Médias
- **Wikimedia répond 429** aux téléchargements automatiques : le propriétaire télécharge à la main.
- **Wikimedia, limites de l'API** (validé sur MM, 12 et 13/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ) :
  - `generator=categorymembers` avec `prop=imageinfo` ne rend l'imageinfo que d'environ 50 pages par requête : boucler sur `continue` avec `gcmlimit=50` ;
  - vignettes aux largeurs standard seulement (360, 1280) : une largeur non standard renvoie vite des 429 ;
  - des téléchargements espacés de 3,5 s ont reçu des 429 « robot policy » faute d'un User-Agent avec contact : envoyer un User-Agent conforme (URL d'un projet ou d'une page, pas l'adresse e-mail du propriétaire sans son accord), un backoff de 8 à 16 s, et ne télécharger que les originaux retenus ;
  - vérifier le SHA-1 des originaux avec `iiprop=sha1`.
- **Pexels et Mixkit** : leurs limites (vérification Cloudflare sur des requêtes rapides, licence `videoRestricted` par clip) sont dans `agents/research.md` ; les vignettes de recherche de Pexels (`?w=360`) suffisent pour une planche (validé sur MM, 13/10/2026).
- **Planche de repérage utilisée pour fixer un instant de coupe** : son horodatage est parfois décalé (5 coupes de renfort sur 14 montraient autre chose : une carte, des pieux, une salle de contrôle). Une planche sert à choisir un plan ; l'instant se cherche sur des images extraites du fichier lui-même (`ffmpeg -ss <t> -i <fichier> -frames:v 1`, `-ss` avant `-i`), puis on regarde la planche des extraits traités avant de les confier aux producteurs (validé sur MM, 28/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ).
- **Identifiants retrouvés à la main sur une planche de choix** : trier la liste une fois, garder cet ordre et retrouver les identifiants à partir des numéros de la planche par programme (trois identifiants mal copiés, trois mauvaises photos ; validé sur MM, 12/10/2026).
- **Résumés de match officiels** : l'action passe d'abord en direct, en plan large, puis en ralenti plus serré quelques secondes après. Chercher le ralenti avant de couper un moment ; ses fondus doux ne se détectent qu'avec un seuil de changement de scène d'environ 0,2 (E010).

## Recherche
- **Sources que l'agent ne lit pas** (validé sur MM, 28/10/2026, porte P4, Q11 ; proposé au plugin 0.3.0, PROPOSÉ) : PDF (sans poppler, les flux compressés et les scans restent illisibles), tableaux dynamiques, pages en 403 ou derrière une vérification. Le contrat de mission demande, pour ces sources, le lien et la page à lire, marqués « non lu » ; l'agent lit seulement les chemins que le contrat nomme. Claude les lit lui-même au moment du script.
- **Lire un PDF** : `WebFetch` sur son URL (la réponse est illisible, mais le fichier est enregistré dans les résultats d'outils de la session, avec son chemin), puis `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/recherche/pdftexte.py <pdf>` (texte seul, bibliothèque standard), puis une recherche par mots clés ; les accents ressortent en octal (`\374`). Les scans restent illisibles ; une page rendue en image se fait avec `outils/medias/rendre_page_pdf.ps1` et `jbig2_page.py`.
- **Images sous filigrane**, ou aperçus d'agence : refusés, même gratuits (validé sur AA, 24/10/2026).
- **SVG de Wikipédia qui arrivent en WebP**, images de Commons réduites : ils sont acceptés ; vérifier les dimensions et les SHA-1 quand c'est possible.
- **Ne pas confondre les objets** (exemple AA : une demi-finale n'est pas une finale). La légende dit exactement ce que montre la photo.
- **Contradiction bâtie sur un règlement lu dans la presse** : l'angle disait que le règlement ne parle pas du « meilleur » ; son article 2 le dit. Lire le règlement officiel en entier avant d'en faire un renversement (E010).
- **Nom d'un prix secondaire** : il change (le trophée Yachine est devenu « Goalkeeper of the Year » en 2026). Vérifier le nom en vigueur à la date du film (E010).

- **Carte du monde « corrigée » par un producteur** (y × 0,70 en seq4 v3 : la carte plate carrée du kit a des bandes vides en haut et en bas, et le « 1,43 » était une erreur de calcul) : la carte est aplatie de 30 %. Aucun producteur ne retouche une projection ; pour le monde, prendre Equal Earth (`${CLAUDE_PLUGIN_ROOT}/outils/cartes/README.md`) (E007).
- **Extrait décrit sans être regardé** : un extrait montrait l'action dès 2,3 s, ce que sa provenance ne disait pas. Regarder une planche de chaque extrait avant de le décrire ou de l'attribuer à une séquence (E009).
- **Extrait à une seule image clé** : la vidéo se fige au rendu. Réencoder chaque extrait avec `-g 15` dès le kit (E009).
- **Tremblement dans les vraies vidéos** : il vient du passage de 25 à 30 images par seconde et des ralentis à images calculées, pas de la mise en scène. Le vérifier sur les images avant de corriger (E009).

## Production et agents
- **Lots qui attendent les raccords** d'une séquence du même lot : écrire les raccords avant, et composer les lots en conséquence (E007).
- **`<!--` perdu** dans l'en-tête HTML d'une version copiée : du texte s'affiche en haut et l'image descend de 54 px. Contrôler l'en-tête de chaque `index.html` (E007 seq2 v3).
- **Retouches faites après la dernière planche du producteur** : personne ne les a vues. Claude prend des snapshots aux instants retouchés.
- **Identifiant en double dans une composition** : la seconde animation prend le mauvais élément (un ballon resté au-dessus d'un extrait). Chercher les `id` en double avant le rendu (E010 seq5).
- **Proposition de durée qui ajoute du temps sans voix** (4,6 s pour l'appel à s'abonner) : contraire à `REFERENTIEL` § 2 quater. Relire la règle avant chaque proposition de durée ; l'appel se pose sur une image tenue, au début de la séquence suivante (E010, Q89 puis Q96).
- **Porte du collage qui oublie une règle validée** : la question sur la fin du film proposait une coupe sèche, contre la fin en douceur (`rendu-collage.md`). Relire `rendu-collage.md` avant d'écrire la porte (E010, Q128 corrigée en Q131).
- **Appel à s'abonner ajouté au collage** : `outils/montage/` ne superpose rien ; l'appel vit dans une séquence (E008, E010).
- **Reprendre un producteur dont le cache est froid** réécrit tout son contexte (300 à 450 k) : préférer un agent court (E007).
- **Raccord extrait d'un rendu** qui contenait un élément retiré depuis (la grille) : réextraire l'image après le nouveau rendu (E007 seq6).
- **Accroche figée, puis collage de vidéos** : la seq1 v1 tenait un extrait arrêté, un arrêt sur image de 7 s, 23 s d'une action dessinée sur un fond uni et une pause de 2 s sans voix (le propriétaire : « le plan est figé pendant presque la moitié de l'accroche »). La première reprise remplissait de vidéos ; le propriétaire l'a refusée aussitôt (« pas un collage de vidéos »). Faire des animations qui vivent, une transition pensée à chaque coupe, les médias quand la voix en parle (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 quater) (E009).

## Technique
- **Vidéo source HDR cachée** (HLG ou PQ en BT.2020, fréquente chez Pexels et Pixabay quand elle est filmée au téléphone ; validé sur MM, 24/10/2026, constat d'un épisode ; proposé au plugin 0.3.0, PROPOSÉ) : si elle garde ses balises, `render` passe de lui-même en rendu HDR en couches, où les images visibles par défaut et découpées seulement par `render(t)` restent affichées plein cadre ; le rendu dure dix fois plus (70 min pour 71 s) ou s'arrête (« HDR image decode failed »), et les `snapshot` ne montrent rien. Parade : ramener chaque source en SDR BT.709 (`${CLAUDE_PLUGIN_ROOT}/outils/medias/traiter.py`), contrôler `color_transfer` par `ffprobe` (ni `arib-std-b67` ni `smpte2084`), mettre `--sdr` dans `render.sh`, lire le journal de rendu, et cacher par défaut tout élément que seul `render(t)` montre.
- **`scale()` animé sur un texte, ou sur un parent qui en contient** : les glyphes sont re-rastérisés à chaque image (saut de 0,3 à 0,9 px RMS, jusqu'à 2 px). Sans effet : `rotate(0.3deg)` (pire), `will-change`, `translate3d`, texte en canvas, `text-rendering: geometricPrecision`. Le texte posé reste statique ; les poussées se font sur les images (validé sur MM, 19/10/2026 ; complète `REFERENTIEL` § 2 ter).
- **Mode de capture** : avec `filter: blur`, `mix-blend-mode` ou `--workers 2`, HyperFrames capture par screenshot, calé au pixel entier : tout mouvement lent (moins de 1 px par image) d'un texte saccade, translation comprise, et le 4K n'y change rien. La capture sous-pixel (`drawElement`) exige `--workers 1` et ni flou, ni blend, ni 3D. En mode screenshot, seuls restent fluides le texte statique et un mouvement linéaire d'exactement 1 à 2 px par image. `controle.py tremblement` ne voit pas la vibration d'un texte : mesurer les résidus du centroïde du texte sur des images consécutives (validé sur MM, 19/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ).
- **Plusieurs HTML racine** dans un projet : `hyperframes check` échoue (`multiple_root_compositions`). Garder `index.html` seul à la racine avec `data-composition-id`, mettre les autres dans `compositions/` avec des chemins `../media/…`, et les rendre par `render -c compositions/x.html` ; les avertissements `nested_media_start_basis_ambiguous` et `duplicate_audio_track` qui suivent sont sans effet (validé sur MM, 13/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ).
- **Polices système remplacées** : le compilateur ne garde pas une pile système (`system-ui, "Segoe UI", Arial`) ; il injecte des `@font-face` déterministes et la remplace par Inter et JetBrains Mono, prises sur Google Fonts. Une police de secours nommée l'est aussi (Georgia devient EB Garamond). Embarquer la police par `@font-face` sur un fichier local, ne nommer que cette police et une famille générique, la consigner dans `PROVENANCE.md` avec sa licence, la vérifier sur une planche ; au `check`, une ligne « Fetched … from Google Fonts » signale une police non embarquée (validé sur MM, 19/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ).
- **Fichier TIFF** : le navigateur ne le lit pas ; convertir en PNG ou en JPEG dans le kit. **Faux « occluded »** de `check` pendant des volets de sortie : `data-layout-allow-occlusion` sur l'élément. **`mask` animé et animation de l'attribut `d`** : jamais testés en 0.8.149 ; un essai court précède tout emploi (validé sur MM, 20/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ).
- **Perspective isométrique en CSS** : la paire `rotateX(60deg) rotateZ(45deg)` donne des axes à 26,57°, pas à 30° (il faudrait 54,74°). Pour un dessin isométrique, tracer en SVG la projection vraie `sx = (x − z)·cos 30°`, `sy = (x + z)·sin 30° − y`, polygones triés de l'arrière vers l'avant (validé sur MM, 20/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ).
- **`TaskStop` sur un rendu** laisse le `node` enfant tourner : `taskkill //T //F //PID`.
- **Rendu lancé en tâche détachée** : aucune notification. Toujours une tâche suivie, ou une veille sur le journal.
- **`Get-Counter`** échoue en français : mesurer le processeur par WMI (`Win32_PerfFormattedData_PerfOS_Processor`).
- **Quatre rendus en parallèle**, ou une machine chargée : un rendu passe de 10 min à plus de 5 h. Un à la fois.
- **Outil de tremblement** : il signale aussi les secondes où une coupe mêle des pas de 0 et de 1 px. Vérifier sur 10 images avant de corriger.
- **Script de garde des rendus** : `${CLAUDE_PLUGIN_ROOT}/outils/rendu/rendre_si_libre.sh` (monté le 24/10/2026).
- **Rendu arrêté sans message** (code 1, seq4 de l'E009) : le relancer une fois à l'identique, avec un nouveau journal, avant de chercher la cause. Le second essai a réussi.
- **Script Python qui affiche des accents** : la console Windows (cp1252) le fait planter, parfois après qu'il a écrit son fichier. Mettre `sys.stdout.reconfigure(encoding="utf-8")` en tête et refuser d'écraser une sortie, pour pouvoir le relancer sans risque (E009, `sans_t2.py`).
- **`ffmpeg drawtext` avec un chemin de police Windows** : le filtre échoue. Planches faites sans étiquettes ; le chemin relatif, qui règle le même défaut pour `whisper` (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 3), n'a pas été essayé (E009).
- **`publication.py chapitres`** : il faut un `--titre seqN="…"` par séquence (E009).
- **Aperçu envoyé à distance** : un MP4 de plus de 30 Mo ne passe pas par Remote Control. Envoyer un aperçu en 720p, fait dans le scratchpad (E009).
- **`publication.py verifier` sur le journal du mix** : il n'a pas les segments. Lui donner le journal du film voix, dont l'image est la même (E010).
- **Tâche Bash détachée** : elle peut ignorer le `cd`. Chemins absolus pour `rendre_si_libre.sh` et le journal (E010).

## Son
- **Séquences mixées séparément**, de −16,8 à −17,8 LUFS, et crête de seq7 à −1,3 dBTP : d'où le mix du film à la fin, avec un seul gain et un seul limiteur (E007).
- **Clics de voix** (bruit de bouche, coupes sans fondu) : ils s'atténuent au collage. Ils sont relevés par `controle.py son`.
- **Son d'un extrait prévu sans l'avoir transcrit** : V1 et V2 portaient un commentaire anglais. Transcrire le son de chaque extrait avant de le prévoir ; s'il porte un commentaire, une ambiance de `marque/son/` le remplace (`DIRECTION_AUDIO.md` § 2) (E009).
- **Musique inaudible au début et après la signature** : les morceaux commencent par une introduction calme qui disparaît sous la voix (le propriétaire : « pas de musique du début »). Relever l'enveloppe de chaque source, par pas de 0,5 à 1 s, et caler son départ (`decalage`) après l'introduction calme ; la musique entre dès 0 s (E010 master v1).
- **`niveau_lu` de `plan-son.json`** : il s'applique avant la baisse sous la voix. Une musique à −13 a mesuré 16 LU sous la voix, et non 13. Mesurer l'écart réel sur l'essai `--son-seul` (musique estimée = mix moins voix) avant de livrer (E010).
