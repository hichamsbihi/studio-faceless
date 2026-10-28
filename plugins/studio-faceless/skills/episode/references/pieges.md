# Pièges connus (à compléter à la fin de chaque épisode)

Format : le piège, puis ce qu'on fait. Source entre parenthèses : les identifiants E001 à E009 sont les épisodes d'AA où le piège est apparu ; chaque chaîne ajoute les siens. Les règles citées sont les règles par défaut du plugin (`${CLAUDE_PLUGIN_ROOT}/referentiels/`) ; les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent.

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
- **Photo répétée** d'une séquence à l'autre : tenir la liste des photos prises (consignes communes).
- **Logos partout** : avec mesure, un ou deux par passage (validé sur AA, 24/10/2026).

## Médias
- **Wikimedia répond 429** aux téléchargements automatiques : le propriétaire télécharge à la main.
- **Images sous filigrane**, ou aperçus d'agence : refusés, même gratuits (validé sur AA, 24/10/2026).
- **SVG de Wikipédia qui arrivent en WebP**, images de Commons réduites : ils sont acceptés ; vérifier les dimensions et les SHA-1 quand c'est possible.
- **Ne pas confondre les objets** (exemple AA : une demi-finale n'est pas une finale). La légende dit exactement ce que montre la photo.

- **Carte du monde « corrigée » par un producteur** (y × 0,70 en seq4 v3 : la carte plate carrée du kit a des bandes vides en haut et en bas, et le « 1,43 » était une erreur de calcul) : la carte est aplatie de 30 %. Aucun producteur ne retouche une projection ; pour le monde, prendre Equal Earth (`${CLAUDE_PLUGIN_ROOT}/outils/cartes/README.md`) (E007).
- **Extrait décrit sans être regardé** : un extrait montrait l'action dès 2,3 s, ce que sa provenance ne disait pas. Regarder une planche de chaque extrait avant de le décrire ou de l'attribuer à une séquence (E009).
- **Extrait à une seule image clé** : la vidéo se fige au rendu. Réencoder chaque extrait avec `-g 15` dès le kit (E009).
- **Tremblement dans les vraies vidéos** : il vient du passage de 25 à 30 images par seconde et des ralentis à images calculées, pas de la mise en scène. Le vérifier sur les images avant de corriger (E009).

## Production et agents
- **Lots qui attendent les raccords** d'une séquence du même lot : écrire les raccords avant, et composer les lots en conséquence (E007).
- **`<!--` perdu** dans l'en-tête HTML d'une version copiée : du texte s'affiche en haut et l'image descend de 54 px. Contrôler l'en-tête de chaque `index.html` (E007 seq2 v3).
- **Retouches faites après la dernière planche du producteur** : personne ne les a vues. Claude prend des snapshots aux instants retouchés.
- **Reprendre un producteur dont le cache est froid** réécrit tout son contexte (300 à 450 k) : préférer un agent court (E007).
- **Raccord extrait d'un rendu** qui contenait un élément retiré depuis (la grille) : réextraire l'image après le nouveau rendu (E007 seq6).
- **Accroche figée, puis collage de vidéos** : la seq1 v1 tenait un extrait arrêté, un arrêt sur image de 7 s, 23 s d'une action dessinée sur un fond uni et une pause de 2 s sans voix (le propriétaire : « le plan est figé pendant presque la moitié de l'accroche »). La première reprise remplissait de vidéos ; le propriétaire l'a refusée aussitôt (« pas un collage de vidéos »). Faire des animations qui vivent, une transition pensée à chaque coupe, les médias quand la voix en parle (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 quater) (E009).

## Technique
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

## Son
- **Séquences mixées séparément**, de −16,8 à −17,8 LUFS, et crête de seq7 à −1,3 dBTP : d'où le mix du film à la fin, avec un seul gain et un seul limiteur (E007).
- **Clics de voix** (bruit de bouche, coupes sans fondu) : ils s'atténuent au collage. Ils sont relevés par `controle.py son`.
- **Son d'un extrait prévu sans l'avoir transcrit** : V1 et V2 portaient un commentaire anglais. Transcrire le son de chaque extrait avant de le prévoir ; s'il porte un commentaire, une ambiance de `marque/son/` le remplace (`DIRECTION_AUDIO.md` § 2) (E009).
