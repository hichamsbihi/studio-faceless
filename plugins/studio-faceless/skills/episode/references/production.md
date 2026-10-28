# Production des séquences (étapes 6 et 7)

## 1. La recette v3 (validé sur AA, 24/10/2026, sur E007 seq5 v3)
Le propriétaire : « cette diversification d'effets, de transitions et cette immersivité était celle que je recherchais ». Exemple complet AA (archives de la chaîne) : consignes de l'E007, séquence témoin seq5 v3, schéma de Turin de l'E003. Les règles citées dans ce fichier sont les règles par défaut du plugin (`${CLAUDE_PLUGIN_ROOT}/referentiels/`) ; les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent.
1. **Vivacité** :
   - un événement visuel toutes les 1,5 à 3 s ;
   - aucun plan de plus de 5 s, hors tenue S ;
   - coupes sur la voix ;
   - effets et transitions variés, tirés de la matière du sujet.
2. **Rien de vide qu'on ne comprend pas** :
   - aucun cadre vide, aucun cadre « de verdict » ou décoratif vide ;
   - jamais un écran occupé à moins d'un tiers pendant plus de 0,5 s ;
   - jamais d'écran noir en milieu de séquence ;
   - une colonne ou un cadre reçoit son contenu **pendant** son tracé ;
   - un manque s'explique par un dessin (podium, liste rayée, frise).
3. **Un fait retiré** se montre par la vraie photo du moment (exemple AA : la fête, le trophée), qui passe ensuite en graphite en 0,6 s, avec une plaque.
4. **Chaque média a un impact** :
   - plein cadre, ou au moins 45 % de la hauteur ;
   - une image de 800 px ou moins devient un tirage de 40 % de la hauteur au plus ;
   - agrandissement de 1,6 fois au plus ;
   - aucune vignette.
5. **Dessins et cartes** : au moins 15 % du temps, dans les passages d'explication. SVG au trait, couleur craie ou encre, tracé progressif ; mention « DIAGRAM » ou « Map: Natural Earth ».
6. **Logos avec mesure** : un ou deux par passage, seulement s'ils aident ; couleurs d'origine.
7. **Pas de grille** sur les images (retirée le 24/10/2026).
8. **Chiffres-cibles**, mesurés dans le README :

   | Mesure | Cible |
   |---|---|
   | Plein cadre | au moins 25 % du temps |
   | Photo d'au moins 45 % de la hauteur | au moins 55 % du temps |
   | Dessin | au moins 15 % du temps |
   | Plus long plan | 5 s au plus |
   | Cadre vide | 0 s |
   | Texte seul | 1,5 s au plus |

## 2. Contrat du producteur (`studio-faceless:motion-producer`)
Champs du modèle `${CLAUDE_PLUGIN_ROOT}/templates/CONTRAT_MISSION.template.md`, plus :
- **À lire d'abord** : les consignes communes de l'épisode, le brief, le modèle (séquence témoin de l'épisode, par plages), le README de la séquence précédente pour l'image d'entrée.
- **Règles d'image** : `${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 ter et § 2 quater (animation, transitions, médias au bon moment ; validé sur AA, 28/10/2026), avec la recette v3 (§ 1). Le brief en donne des extraits.
- **Point de départ** : le gabarit v3, ou la version retenue, copiée sans MP4, sans planches et sans dossiers `_copie…` ni `_rendu-N`.
- **Écriture** : son dossier seulement, qui n'existe pas encore. Rien dans le scratchpad, rien dans les dossiers temporaires du système.
- **Moteur** :
  - HyperFrames 0.8.149, Node 22 par Git Bash ;
  - skills `hyperframes-core`, `hyperframes-keyframes` et `hyperframes-animation`, ce dernier en WAAPI et CSS seulement ; jamais GSAP, Lottie, Three.js ni Anime.js ; aucun `npm install` ni `hyperframes add` ;
  - `snapshot` avec `--describe false` ;
  - jamais de `preview` ;
  - `check` sans erreur ;
  - `render.sh` avec `--workers 2`, qui refuse d'écraser, **non lancé** ;
  - aucun téléchargement ;
  - aucun Chrome laissé ouvert, et on ne touche pas aux rendus des autres.
- **Fiche d'effets, avant toute scène** (validé sur AA, 26/10/2026 : « obliger le producteur à bien choisir les effets avec une réflexion au préalable ; chaque vidéo doit être meilleure que la précédente ») :
  - le producteur lit l'en-tête et l'index de `${CLAUDE_PLUGIN_ROOT}/referentiels/MOTION_CATALOG.md` (lignes 1 à 90), puis les fiches qu'il retient ;
  - le brief lui donne les retours du propriétaire sur l'épisode précédent et les techniques déjà employées ;
  - avant de construire, il écrit en tête de son README, pour chaque moment du plan de plans :
    - la technique (identifiant, ou technique nouvelle décrite en deux phrases) ;
    - l'idée du récit qu'elle sert, et pourquoi elle plutôt qu'une autre ;
    - l'effet sonore proposé ;
  - il ajoute ce qui progresse par rapport à l'épisode précédent : retours appliqués, technique nouvelle ou mieux exécutée ;
  - une technique reprise s'améliore sans se recopier ; jamais deux fois de suite le même traitement ;
  - Claude contrôle la fiche avec la planche. Une fiche absente, ou un choix sans raison, et la séquence n'est pas présentée au propriétaire.
- **Son** : la voix seule. Un tableau des **effets proposés** dans le README (code, instant local, image qui le justifie, facultatif ou non). Aucune musique ni aucun effet dans la séquence.
- **Règles de l'épisode** : les personnes, les interdits, les couleurs, les photos déjà prises.
- **Livrables** :
  - un README qui s'ouvre sur la fiche d'effets, puis donne les départs, la carte des mouvements, les chiffres mesurés, les crédits, les écarts, les techniques du skill retenues, l'image de sortie au pixel et les effets proposés ;
  - une planche de 24 instants (dont 6 milieux de transition), regardée.
- **Plafond** : 300 k de contexte, puis `ETAT.md` et arrêt.
- **Réponse finale** : 12 lignes au plus.

## 3. Lots
- **Séquence témoin d'abord** : rendue, puis validée par le propriétaire. Sa leçon passe dans les consignes communes avant les lots.
- **Lots de trois producteurs au plus.** Claude transmet à chaque nouveau producteur :
  - l'image de sortie exacte de la séquence précédente ;
  - les photos déjà prises ;
  - les quotas d'effets rares déjà consommés.
- **Option, sur décision du propriétaire** (porte 7 de l'E009, 26/10/2026 ; validé sur AA comme option, 28/10/2026, Q72) : après la séquence témoin, tous les producteurs sont lancés à la fois ; les rendus restent un à la fois, à la suite, sans nouveau feu vert par séquence. Il faut que tous les raccords soient écrits au pixel et que les photos et les plans de banque soient répartis d'avance. Par défaut : lots de trois.
- **Chaque livrable se vérifie à son retour** :
  - planches regardées ;
  - `check` ;
  - en-têtes HTML (aucun texte nu dans `<head>` : un `<!--` perdu affichait un bandeau sur seq2 v3) ;
  - snapshots de Claude aux instants retouchés après la dernière planche ;
  - couleurs (`controle.py couleurs`).

## 4. Corrections
- **Sur place, dans la même version.** Si le producteur vient de finir (cache de moins de 5 min environ), on le reprend par `SendMessage`. Sinon, un agent court, avec un brief de quelques lignes et une écriture limitée au dossier, coûte environ 170 à 200 k.
- **Nouvelle version** seulement pour un défaut majeur, ou si le propriétaire la demande.
- **Rendu déjà fait** : on le range dans `_rendu-N/` avec sa planche de contrôle, puis on rend de nouveau. Rien ne s'écrase.
- **Chaque correction** ajoute une ligne « Correction du JJ/MM » au README de la séquence.
