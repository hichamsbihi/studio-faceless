# Référentiel de qualité de réalisation (V0.3, partiellement validé)

> Règles par défaut du plugin studio-faceless.
> Les écarts de la chaîne (`direction/ECARTS.md`) l'emportent.

**Statut : PROPOSITION À VALIDER**, sauf ce qui suit, validé sur AA par son propriétaire :
- la règle « besoin narratif → médias » (§3), demandée le 12 octobre 2026. L'étape « images clés validées » est **supprimée le 15 octobre 2026** (§3) ;
- l'interdiction de l'effet diaporama, et ses moyens (§2), règle générale validée le 15 octobre 2026 ;
- les règles de choix des médias (§2 bis), le contrat de plan (§3 bis) et les portes A à C (§4), validés le 14 octobre 2026 ;
- les règles d'animation, de transitions et de médias au bon moment (§2 quater), validées le 28 octobre 2026 (épisode 009) ;
- les règles de rythme, de réalisme, de profondeur et d'arrière-plan (§2 ter), validées le 15 octobre 2026 pendant l'épisode 003. Ce document fixe un niveau d'exigence ; ce n'est ni une charte graphique ni une méthode imposée. Les pratiques propres à un épisode vont dans son `CLAUDE.md`, pas ici.

## 1. Sept exigences
1. **Chaque transformation fait progresser le récit.** Pour chaque plan : que sait-on avant ? que découvre-t-on ? que comprend-on après ? Un mouvement qui ne change ni information, ni relation, ni émotion est suspect.
2. **Un repère reste reconnaissable** (personne, objet, lieu, document) quand l'échelle ou la nature de l'explication change, sauf si une coupe franche est meilleure.
3. **L'attention est dirigée** : point focal, hiérarchie, trajet du regard. Aucune couche décorative ; tout doit rester lisible sur mobile.
4. **Début, transformation, état de lecture** pour chaque mouvement important, avec assez de maintien pour lire.
5. **Le langage visuel varie avec le contenu** (archives, documents, cartes, graphiques, typographie) sans effet répété comme liant.
6. **Chaque transition a une raison** : continuité de sujet, opposition, changement d'échelle, de temps ou de point de vue. Coupe franche acceptée ; pas de transition « vitrine ».
7. **Vérité documentaire** : distinguer archive authentique, illustration, graphisme et reconstitution ; conserver les originaux ; aucune causalité ou donnée suggérée sans preuve.

## 2. À éviter
- **Effet diaporama, interdit dans tous les films** (règle générale, validée sur AA, 15/10/2026 : « pas d'effet diaporama », « règle générale ») : une suite d'images fixes traitées de la même façon (une photo ou un fond, un zoom ou un titre, un fondu, puis la même chose) pendant que la voix avance. Moyens validés le même jour :
  - **un espace continu par séquence**, que la caméra traverse en profondeur ; les photos, documents et données s'y posent. On ne remplace pas une image par la suivante. Un plan de plans qui associe un média à chaque phrase ne se monte jamais photo après photo ;
  - **une grammaire qui change avec le contenu** (vidéo réelle, document, carte, données, typographie, transitions propres au film), jamais deux fois de suite le même traitement ;
  - **des techniques choisies pour le film, anciennes ou nouvelles** (validé sur AA, 18/10/2026 ; remplace la règle du 15/10/2026 « de nouvelles idées à chaque film ») :
    - une technique déjà employée (`${CLAUDE_PLUGIN_ROOT}/referentiels/MOTION_CATALOG.md`, colonne « Épisodes ») se reprend quand elle sert le récit et la vision du film ; on l'améliore plutôt qu'on la recopie, et l'emploi est noté (colonne « Épisodes » ou section MOTION_CATALOG de `direction/ECARTS.md`) ;
    - le choix des techniques d'un film, anciennes ou nouvelles, revient au directeur artistique (`studio-faceless:art-director`), selon ce qui sert le mieux le film ;
    - objectif : améliorer la production petit à petit, d'un film à l'autre ;
  - **la consigne et sa définition dans chaque contrat de mission** d'un producteur ;
  - **le contrôle** sur la planche contact de chaque rendu, et dans la critique de `studio-faceless:art-director`.
- Effet « PowerPoint » : une diapositive remplacée par la suivante, sans espace commun ni mouvement qui relie.
- Sensation de récitation ou de lecture : l'image ne suit pas le rythme de la voix (§2 ter).
- Zoom permanent ou mouvement sur chaque phrase.
- Statistiques sans unité, contexte ni source.
- Faux documents, témoignages, portraits ou archives présentés comme authentiques.
- Fabriquer de nombreuses variantes avant d'avoir testé la scène décisive.
- Valider sur le lint, FFprobe ou une capture seule.

## 2 bis. Choix des médias (validé sur AA, 14 octobre 2026)
- **Une situation authentique** (un événement daté, une réaction réelle) vaut mieux qu'un montage de plans génériques. Le montage ne change pas la nature d'une scène (exemple AA : un échauffement ne devient pas une défaite).
- **Chaque média a une fonction narrative** qu'on peut formuler en une phrase ; « c'est un stade » ne suffit pas. Un média qui ne raconte rien sort du montage.
- **Les mots habitent l'image** (le plan de l'événement, sa profondeur, un support réel) au lieu de flotter en surimpression.
- **Image adaptée au récit** : chaque image correspond au contexte et au niveau de l'histoire racontée. Une image amateur ou semi-pro n'est acceptée que si c'est ce que montre réellement le récit.
- **Médias non libres en citation encadrée** (validé sur AA, 24/10/2026) :
  - on prend la photo qui représente le mieux le moment, dans la meilleure qualité, même non libre (agence, presse, organisation), par exemple une personne avec son trophée ;
  - à trois conditions : elle est le sujet de ce que dit la voix ; elle reste à l'écran le temps utile ; elle est créditée (auteur et agence) ;
  - logos permis quand le film en a besoin (élargi sur AA, 28/10/2026 : « on peut utiliser si besoin ») : organisations, instances, compétitions, trophées, médias cités ; toujours avec mesure (recette v3 ci-dessous) ;
  - extraits vidéo courts permis (conférences, reportages, cérémonies) ;
  - **vraies vidéos d'événements permises** (validé sur AA, 28/10/2026, après des exceptions sur deux épisodes) : les compétitions et les instances admises sont listées dans `direction/ECARTS.md`. Un vrai moment d'événement se montre en vraie vidéo, jamais en animation ; l'animation sert à expliquer. Le risque de réclamation Content ID est assumé par le propriétaire ;
  - aucune image retournée ni maquillée pour échapper à la détection ; le risque de réclamation est assumé par le propriétaire ;
  - dans `PROVENANCE.md` : source, auteur, ayant droit et motif de la citation ; chaque téléchargement avec l'accord du propriétaire.
  - **gratuit, choisi sur la scène** (validé sur AA, 24/10/2026) : aucun achat de licence ; le média se choisit seulement sur ce qu'il apporte à la scène, la licence ne compte pas ; on le prend là où il est librement accessible (article, site d'une organisation, Wikipédia), jamais en retirant un filigrane ni en contournant un accès payant ; **aucune photo avec filigrane** à l'écran (validé sur AA, 24/10/2026).
  - **ajouts du 24/10/2026** (validé sur AA) : la source de chaque média est notée pour pouvoir le remplacer vite en cas de réclamation ; un extrait vidéo dure **6 s au plus à l'écran** ; **fichiers tirés de YouTube permis** quand c'est nécessaire, dans la meilleure définition, 1080p si possible (validé sur AA, 28/10/2026 ; remplace l'interdiction du 24/10/2026) ;
  - **téléchargements par le propriétaire** (validé sur AA, 24/10/2026) : Claude donne une liste de liens avec le nom imposé de chaque fichier et un dossier de dépôt ; le propriétaire télécharge à la main ; Claude vérifie ensuite chaque fichier déposé (empreinte, image, provenance). Aucun téléchargement en lot.

## 2 ter. Rythme, réalisme, profondeur et arrière-plan (validé sur AA, 15 octobre 2026)
Ces règles viennent des retours du propriétaire sur un épisode de la première chaîne (AA, épisode 003) : « immersion totale du spectateur ».

- **Les images suivent la voix.**
  - Chaque phrase déclenche un événement visuel sur son premier mot (±2 images).
  - Les pauses sont tenues par l'image et le son.
  - Aucun plan ne reste sans mouvement plus de 2,5 s. Ce mouvement vient des photos et des fonds, jamais du texte posé (voir « Aucune vibration »).
  - Pas de récitation ni de sensation de lecture.
- **Plus de photos réelles**, pour garder « le lien de réalisme avec le spectateur ».
  - Un fond uni devient l'exception.
  - Derrière les fiches, les données et les titres, on place une photo réelle liée au propos : floutée, assombrie, teintée, avec un vignettage.
  - Cette photo reste soumise au §2 bis, à la licence et au crédit.
- **Profondeur 2,5D** : au moins trois plans qui bougent à des vitesses différentes pendant un lent travelling.
  1. Une photo floutée au fond.
  2. Une photo nette en carte, avec une ombre profonde.
  3. Les fiches et le texte devant, avec au plus une légère rotation 2D fixe : jamais `perspective()` ni rotation 3D, qui font trembler le texte (E003).

  La caméra se déplace dans la profondeur plutôt que de remplacer l'image. Pas de 3D (Three.js abandonné sur AA, 15/10/2026), pas de détourage automatique sans outil installé.
- **Arrière-plan de la chaîne**, partout où il n'y a pas de photo plein cadre : un fond à couches (matière de fond, couche de contexte floutée, vignettage, brume, grain déterministe). Sa recette, ses matières et ses valeurs sont celles de la chaîne (`marque/README.md`, `direction/ECARTS.md`).
- **Couleurs et polices des films** : `marque/README.md`.
- **Aucune photo répétée** d'une séquence à l'autre dans un même film. Seule exception : un rappel voulu, consigné dans le README de la séquence. En cas de répétition, on la remplace par de la typographie, une animation ou une autre photo.
- **Aucune vibration.**
  - Un élément immobile ne bouge pas d'un pixel d'une image à l'autre.
  - Un mouvement lent reste continu.
  - **Un texte posé reste immobile** (validé sur AA, 20/10/2026 ; mesures de l'E005 du 19/10/2026) : entrée et sortie courtes, en glissement et en opacité ; jamais d'échelle ni de flou animés sur un texte ou un bloc qui en contient. L'échelle fait sauter les lettres. Le flou, la brume, le grain et `--workers 2` imposent un rendu recalé au pixel, où même un glissement lent saccade.
  - Interdits : secousse de caméra, valeurs aléatoires recalculées à chaque image hors du grain, arrondi au pixel pendant un mouvement lent.
  - Contrôle : porte B.

- **Recette d'image v3** (validé sur AA, 24/10/2026, sur E007 seq5 v3 : « cette diversification d'effets, transitions et cette immersivité était celle que je recherchais » ; détail et contrat : skill `studio-faceless:episode`, `references/production.md` § 1 ; modèles : archives de la chaîne) :
  - un événement visuel toutes les 1,5 à 3 s ; aucun plan de plus de 5 s ; coupes sur la voix ; effets et transitions variés, tirés de la matière du sujet ;
  - **rien de vide qu'on ne comprend pas** : aucun cadre vide ni cadre « de verdict » vide ; jamais un écran occupé à moins d'un tiers plus de 0,5 s ; jamais d'écran noir en milieu de séquence ; un cadre reçoit son contenu pendant son tracé ;
  - un fait retiré se montre par la vraie photo du moment, puis un passage en graphite avec une plaque (exemple AA : E007) ;
  - dessins (podium, frise, liste, schéma) et cartes au trait dans les passages d'explication, au moins 15 % du temps ;
  - logos avec mesure (un ou deux par passage, seulement s'ils aident) ; aucun filtre de grille ;
  - chiffres-cibles : plein cadre ≥ 25 % ; photo ≥ 45 % de la hauteur pendant ≥ 55 % du temps.
- **Ajouts du 26/10/2026** (validé sur AA, étude AA du 26/10/2026 d'une chaîne de référence, Tifo Sports) :
  - **personnes détourées** : quelques personnes clés par film, détourées à la main (`clip-path` en polygone, comme les miniatures ; le détourage automatique reste exclu sans outil installé), en couleurs réelles, jamais en bichromie. Elles se posent dans les dessins, cartes et graphiques, à 45 % de la hauteur au moins, et leur étiquette entre en opacité ou en glissement au pixel entier. Les grandes photos plein cadre restent intactes (fiche CUTOUT-FIGURE) ;
  - **une idée abstraite = une métaphore dessinée** (argent, audience, temps, probabilité, risque), tirée de la matière du sujet, nommée dans le plan de plans et montrée sur le mot (fiche DRAWN-METAPHOR) ;
  - **effets choisis avant de construire** (le propriétaire : « obliger le producteur à bien choisir les effets avec une réflexion au préalable ; chaque vidéo doit être meilleure que la précédente »). Le producteur lit l'index de `${CLAUDE_PLUGIN_ROOT}/referentiels/MOTION_CATALOG.md`, y compris les techniques vues chez Tifo, et écrit sa fiche d'effets avant toute scène (skill `studio-faceless:episode`, `references/production.md` § 2) ;
  - **non retenu** : la coupe franche par défaut et le changement de couleur de fond à chaque bloc. La recette v3 et le fond fixe restent la règle ; un changement de bloc se marque par l'impact (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 2) et par la nouvelle photo de contexte.

## 2 quater. Animation, transitions et médias au bon moment (validé sur AA, 28/10/2026)
Ces règles viennent des retours du propriétaire sur la séquence témoin de l'E009 d'AA (26/10/2026) : « le plan est figé pendant presque la moitié de l'accroche », puis « l'objectif n'est pas de faire un collage de vidéos, l'objectif est d'avoir des animations bien faites, une bonne maîtrise des transitions et utiliser les médias dans le bon moment ». Elles complètent le § 2 ter et la recette v3 ; en cas d'écart, la règle la plus stricte s'applique.

- **Des animations, pas des schémas posés.** Un dessin se construit et vit à l'image : tracés, éléments qui entrent avec leur propre mouvement, chiffres qui défilent, symboles qui se déplacent sur leurs trajectoires. La caméra bouge dans le monde dessiné (poussée, travelling, légère rotation, calques en parallaxe 2,5D). **Aucune image immobile plus de 1 s**, hors les 3 images d'une jonction.
- **Une idée de mise en scène par passage d'explication.** L'objet dessiné peut se montrer en profondeur ; la caméra s'en approche ou en fait le tour ; ses parties s'ouvrent et les éléments y entrent avec élan, rebond ou traîne. Jamais seulement des aplats qui s'allument. La perspective CSS se limite aux dessins et aux photos, jamais sur un texte (§ 2 ter).
- **Une transition pensée à chaque coupe**, liée au récit :
  - raccord de forme (le dessin se pose exactement sur la vraie image, ou l'inverse) ;
  - poussée à travers un objet ;
  - morphose d'une forme en une autre ;
  - masque de matière qui découvre l'image, trait qui balaie ;
  - raccord de mouvement (le geste d'un plan continue dans le suivant).

  Jamais deux fois de suite la même ; pas de fondu enchaîné par défaut. La fiche d'effets nomme le type et la raison de chaque transition.
- **Les médias au bon moment, pas de collage de vidéos.** Un extrait ou une photo arrive quand la voix parle de ce qu'il montre, et il y est mis en valeur (cadre, rampe de vitesse, caméra qui bouge). Entre deux médias, les animations portent le récit. Une banque de plans est une réserve, jamais un remplissage ; chaque plan n'est attribué qu'à une séquence.
- **Arrêt sur image** : 2 s au plus, avec une caméra qui bouge.
- **Aucun temps sans voix ajouté.** Une pause écrite au script peut se retirer de la bande ; celles qui restent tombent sur une image réelle qui bouge (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 2).
- **Jonctions vivantes** : les objets de jonction bougent (aiguille, pupille, craie qui frémit) ; ils ne sont au pixel que sur les 3 images de la jonction.
- **Savoir-faire avant la fiche d'effets** : le producteur lit, dans `hyperframes-animation` (WAAPI et CSS seulement), les transitions de scène et les plans en plusieurs phases, et, dans `hyperframes-keyframes`, la caméra, les masques, les tracés et la profondeur.
- **Restent propres à chaque épisode** : le rythme chiffré des événements (exemple AA, E009 : 1,5 s au plus dans l'accroche, 2,5 s ailleurs ; recette v3 : 1,5 à 3 s) et la répartition de la banque de plans.

## 3. Contrat de scène (avant fabrication)
Définir d'abord le besoin narratif, puis choisir des médias adaptés à ce besoin, à la vérité documentaire et aux droits. Une image disponible n'est pas forcément une bonne image.

**Pas d'images clés soumises au propriétaire** (décision du 15/10/2026, validée sur AA, qui remplace la règle du 12/10) :
- dès son feu vert de production, le Studio Director délègue chaque séquence à un `studio-faceless:motion-producer` ;
- chaque producteur conçoit la mise en scène complète à partir du brief de séquence (narration, plan de plans, son) et du kit de l'épisode ;
- depuis le 16/10/2026 (parcours raccourci, `CLAUDE.md` de la chaîne), il s'arrête à `render.sh` ; le Studio Director rend et contrôle ;
- le propriétaire juge le rendu. Ses corrections se font dans une nouvelle version, par un nouvel agent.

| Champ | Question |
|---|---|
| Enjeu | Quelle question ou émotion porte le passage ? |
| Avant / après | Que comprend-on avant, et après ? |
| Matériaux | Quels médias, avec quel statut et quels droits ? |
| Progression | Quels états visibles, dans quel ordre ? |
| Raccords | Pourquoi ça bouge ; comment on entre et on sort. |
| Lecture | Ce qui doit rester stable assez longtemps. |
| Audio | Relation avec voix, ambiance, musique, silence (voir `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md`). |
| Refus | Ce qui rendrait le résultat plat, trompeur, illisible ou gratuit. |

Si un média indispensable manque, proposer une représentation honnête ou signaler le blocage ; ne jamais substituer en silence une image générique.

## 3 bis. Contrat de plan
Chaque unité audiovisuelle importante précise :
1. la phrase ou le temps de narration ;
2. la découverte voulue ;
3. le média réel et son statut (archive, illustration, graphisme, reconstitution) ;
4. l'état visuel initial ;
5. la transformation ou le mouvement de caméra ;
6. le raccord, et sa raison ;
7. l'état final visible.

Une transformation qui n'apporte ni découverte ni changement de lecture est à reprendre.

## 4. Portes de qualité
- **A — Intention, avant toute animation lourde** : question de scène, matériaux licites, fiche de séquence validée.
  - Les médias se choisissent avant les effets. Plusieurs angles ou sources cohérentes quand ils existent vraiment ; jamais de travelling qui montrerait ce que la photo ne contient pas.
  - Le producteur fixe lui-même ses images clés (entrée, découverte centrale, transformation, raccord, état final) et les vérifie sur sa planche de la porte B. Depuis le 15/10/2026, elles ne sont plus soumises au propriétaire (§3).
  - Les médias réels, ou leurs alternatives graphiques honnêtes, avec leur provenance et leurs droits.
  - S'il n'existe qu'une photo, le dire et construire une structure éditoriale plutôt que 40 s de zoom.
  - Refusé : un prototype où la voix avance pendant que l'image ne fait que dériver ou changer légèrement d'échelle.
- **B — Technique et preuve du mouvement** : composition déterministe, médias valides, décodage complet, durée, fps, aucun flash, mauvais recadrage ni déformation.
  - Une planche de captures (16 à 20 instants) vérifie l'entrée, la transformation, la sortie et le raccord. Depuis le 18/10/2026, aucun essai de 8 à 15 s n'est plus demandé, même pour une technique nouvelle (validé sur AA).
  - On examine la planche d'images, le mouvement, la continuité de caméra, la lisibilité des sujets, la découverte réelle et le montage avec les plans voisins. Le jugement est perceptif, pas seulement chiffré.
  - Depuis le 15/10/2026, aucun plan ne reste sans mouvement plus de 2,5 s (§2 ter). Une tenue sans information ni intention nouvelle se corrige ; une pause expressive reste permise si quelque chose y vit (lumière, profondeur, son).
  - **Vibration** : différence entre images successives sur une zone censée être immobile, après réduction et léger flou, pour neutraliser le grain :

    `ffmpeg -i X.mp4 -vf "crop=W:H:X:Y,scale=iw/4:ih/4,gblur=sigma=2,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -f null -`

    On cherche des pics réguliers d'une image à l'autre, puis on confirme à l'œil sur dix images consécutives en pleine taille. Avec le grain et la brume, un « 0 » parfait n'est pas attendu (mesure AA du 15/10/2026 : moyenne 1,5 à 1,9 sur la séquence 3).
  - **Photos répétées** : comparer les photos de toutes les séquences avant le collage, y compris redimensionnées.
  - **Outils** : ces contrôles, et ceux du niveau, des couleurs et des licences, sont prêts dans `${CLAUDE_PLUGIN_ROOT}/outils/controle/` (mode d'emploi : `${CLAUDE_PLUGIN_ROOT}/outils/controle/README.md`).
  - La grammaire varie avec intention (plan large, moyen ou détail ; perspective ; archive ; vidéo ; composition graphique), sans quota aveugle de coupes, et sans zoom ni transition répétés par défaut.
- **C — Visionnage et critique** : le MP4 exact, à vitesse normale et en taille mobile. Si personne n'a pu le regarder, le dire.
  - `studio-faceless:art-director` examine le MP4 produit (planches denses, images aux raccords) et rend : temps → défaut précis → raison → correction à fort impact.
  - Aucun verdict « conforme » fondé seulement sur les LUFS, les 30 i/s, un CLI sans erreur ou une compilation.
- **D — Son et image** : écoute selon `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md`.
- **E — Revue humaine** : le propriétaire décide.

Bloquant même si c'est beau : preuve fabriquée ou trompeuse, droits non clarifiés, élément majeur illisible, plan essentiel manquant, audio non contrôlé.

Grille indicative (0 / 1 / 2, sans total magique) : utilité narrative, choix des médias, composition, mouvement, raccords et respiration, lisibilité mobile, cohérence documentaire, audio.

## 5. Référence d'étude de la chaîne
Propre à la chaîne : voir `direction/ECARTS.md`.

## 6. Décisions ouvertes
Propres à la chaîne : voir `direction/ECARTS.md`.
