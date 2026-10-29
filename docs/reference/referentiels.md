# Référentiels du plugin

Cette page décrit les quatre référentiels de `plugins/studio-faceless/referentiels/` : la méthode de récit, le référentiel de qualité de réalisation, le catalogue d'animations et (par renvoi) la direction audio. Ce sont les **règles par défaut** de toutes les chaînes.

## Table des matières
- [Rôle des référentiels et ordre des règles](#rôle-des-référentiels-et-ordre-des-règles)
- [Fiches](#fiches)
  - [referentiels/METHODE_RECIT.md](#referentielsmethode_recitmd)
  - [referentiels/REFERENTIEL_QUALITE_REALISATION.md](#referentielsreferentiel_qualite_realisationmd)
  - [referentiels/MOTION_CATALOG.md](#referentielsmotion_catalogmd)
  - [referentiels/DIRECTION_AUDIO.md](#referentielsdirection_audiomd)
- [Tableau des 70 fiches du catalogue](#tableau-des-70-fiches-du-catalogue)
- [Qui cite quoi](#qui-cite-quoi)
- [Points à vérifier et tensions entre fichiers](#points-à-vérifier-et-tensions-entre-fichiers)

## Rôle des référentiels et ordre des règles
Les référentiels portent ce que le studio a appris sur AA (Apparently Athletic, la première chaîne) et que le propriétaire a validé. Ils ne contiennent ni nom de chaîne ni identité de chaîne : leurs exemples « AA » sont des illustrations.

Chaque référentiel ouvre sur le même avertissement : « Règles par défaut du plugin studio-faceless. Les écarts de la chaîne (`direction/ECARTS.md`) l'emportent. » L'ordre complet (la dernière règle l'emporte) est décrit dans [`../ARCHITECTURE.md`](../ARCHITECTURE.md) :

1. `REGLES_STUDIO.md` et `referentiels/` (injectés ou lus à la demande) ;
2. `direction/ECARTS.md` de la chaîne ;
3. `CLAUDE.md` de la chaîne ;
4. `CLAUDE.md` de l'épisode.

Le mot « validé sur AA, date » veut dire : décidé par le propriétaire d'AA à cette date. Une autre chaîne peut s'en écarter dans son `ECARTS.md` (format d'une ligne d'écart : [`starter-et-depot.md`](starter-et-depot.md), fiche `starter/direction/ECARTS.md`).

| Référentiel | Taille | Quand on le lit | Chargé comment |
|---|---|---|---|
| `METHODE_RECIT.md` | 67 lignes | recherche, sujet, titre, script, shorts | à la demande (cité par `REGLES_STUDIO.md`) |
| `REFERENTIEL_QUALITE_REALISATION.md` | 185 lignes | réalisation, image, montage, critique | à la demande ; lu par `motion-producer`, `art-director`, `research` (§ 2 bis seul) |
| `MOTION_CATALOG.md` | 304 lignes (31 594 octets) | choix des techniques d'animation | **index d'abord, puis une seule fiche** (jamais le fichier entier) |
| `DIRECTION_AUDIO.md` | 138 lignes | voix, musique, SFX, mixage | à la demande ; documenté dans [`son.md`](son.md) |

## Fiches

### referentiels/METHODE_RECIT.md
- **Rôle** : méthode de récit commune à toutes les chaînes. Elle dit comment une vidéo documentaire garde la curiosité : boucle hook / rehook, ouverture de 0:00 à 1:00, corps du film, choix du sujet et du titre, shorts. Titre complet : « Méthode de récit : boucle de curiosité, ouverture, corps du film, sujet et titre, shorts ».
- **Quand il sert** : au choix du sujet, à l'angle et au découpage, à l'écriture du script (portes de `references/grilles.md` du skill `episode`), à la fabrication des shorts. Lu par le Studio Director ; aucune définition d'agent ne le cite (un agent le lit seulement si le contrat de mission le liste). Cité par les skills `episode` (`SKILL.md`, `etapes.md`, `grilles.md`, `choix-sujet.md`, `recit-retention.md`), `shorts`, `youtube-seo`, par `outils/shorts/README.md`, par le modèle `templates/CLAUDE.episode.template.md` et par les fichiers `starter/direction/`.
- **Statut** : chaque section indique le sien ; toutes les validations datées viennent d'AA. L'identité, le public, la promesse, les territoires, les principes, la personnalité narrative et les sujets sont **propres à chaque chaîne** (`direction/LIGNE_EDITORIALE.md`).
- **Contenu** :
  | § | Titre (statut) | Contenu en une ligne |
  |---|---|---|
  | 1 | Boucle de curiosité (validé sur AA, 19/10/2026) | enjeu avant la première question ; hook = question concrète ; prédiction puis retournement ; rehook = vraie avancée de l'enquête ; appel Like + Subscribe juste après l'ouverture d'une question, jamais juste après une réponse (place vers 2:00 gardée ; mesure à J+7, validé sur AA, 26/10/2026) ; progression situation → question → explication → limite → explication affinée → réponse ; on parle de curiosité, jamais d'addiction ; six questions de contrôle |
  | 2 | Ouverture, de 0:00 à 1:00 (validé sur AA, 26/10/2026) | 0:00–0:15 : visage nommé en image réelle ou anomalie par image comparée ; contradiction complète avant 0:40 (évidence démentie par défaut) ; question d'une phrase avant 0:45, dite et écrite en texte fixe ; ensuite la signature de la chaîne, puis le plan de la réponse en 2 ou 3 mots avec pictogrammes ; ce sont des normes du genre, pas des leviers prouvés |
  | 3 | Corps du film (validé sur AA, 26/10/2026) | première réponse partielle avant 1:30 ; renversement vers 75 % ; dernière révélation dans le dernier quart ; ni histoire ni cours technique avant la première réponse ; 3 chiffres d'affilée au plus, en paire ou comparés, sur une infographie qui naît sur la voix ; tout inconnu expliqué en moins de 5 s |
  | 4 | Sujet et titre (validé sur AA, 26/10/2026) | vérification éliminatoire « compris par un non-initié » ; titre « Why… » sur un fait observable, environ 7 mots et 60 caractères, sans montant ni mot tout en majuscules ; film court de 6 à 7 min en essai (comparé à J+7) ; format « Every [x] explained » en essai |
  | 5 | Shorts (validé sur AA, 19/10/2026) | trois objectifs dans l'ordre (regardé jusqu'au bout, faire connaître la chaîne, amener vers les longs) ; vraie valeur ; boucle complète puis relance ; deux versions (YouTube < 60 s, 35–50 visés ; TikTok et Facebook > 1 min, 65–85 visés) ; script dédié et prise à vitesse d'origine ; voix IA déclarée, crédits photo dans les légendes seulement ; formule des 10 règles ; choix des boucles (26/10/2026) ; agent `studio-faceless:shorts-producer` |
- **Liens** : cite `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` (prise des shorts), `marque/README.md` de la chaîne (appel Like + Subscribe, signature), `skills/shorts/references/montage-vertical.md` (formule des 10 règles). Cité par `MOTION_CATALOG.md` (fiches `BEFORE-AFTER`, `ANSWER-ICONS`). Lien : [`skill-episode.md`](skill-episode.md), [`publication.md`](publication.md).
- **À savoir** :
  - le § 2 donne des **normes du genre** que la première chaîne ne tenait pas : leur effet se mesure sur les courbes de la chaîne (rétention à 0:30 et 1:00) ;
  - l'appel Like + Subscribe : si la perte au moment de l'appel dépasse la pente des secondes voisines (capture Studio à J+7), la place est rouverte ;
  - la durée par défaut d'un film ne change pas avant le résultat de l'essai court (§ 4).

### referentiels/REFERENTIEL_QUALITE_REALISATION.md
- **Rôle** : niveau d'exigence de la réalisation (image, montage, animation) et portes de qualité. Titre : « Référentiel de qualité de réalisation (V0.3, partiellement validé) ». Ce n'est ni une charte graphique ni une méthode imposée : les pratiques propres à un épisode vont dans son `CLAUDE.md`.
- **Quand il sert** : le producteur (`motion-producer`) et le directeur artistique (`art-director`) le lisent pour toute mise en scène et toute critique ; `research` n'en lit que le § 2 bis (choix des médias). Le Studio Director s'y réfère pour les contrats de mission (consigne anti-diaporama avec sa définition) et pour les portes A à E. Cité aussi par `controle.py` / `outils/controle/README.md` (contrôles de la porte B), `skills/episode` (`production.md`, `pieges.md`), `skills/shorts`, le modèle `templates/BRIEF.episode.template.md` et le gabarit de séquence v3.
- **Statut** : « PROPOSITION À VALIDER », **sauf** ce que l'en-tête liste comme validé sur AA : besoin narratif → médias (§ 3, 12/10/2026), interdiction de l'effet diaporama (§ 2, 15/10/2026), choix des médias, contrat de plan et portes A à C (14/10/2026), rythme, réalisme, profondeur et arrière-plan (§ 2 ter, 15/10/2026), animation et transitions (§ 2 quater, 28/10/2026).
- **Contenu** :
  | § | Titre | Contenu en une ligne |
  |---|---|---|
  | 1 | Sept exigences | chaque transformation fait progresser le récit ; repère reconnaissable ; attention dirigée ; début, transformation, lecture ; langage visuel variable ; chaque transition a une raison ; vérité documentaire |
  | 2 | À éviter | **effet diaporama interdit dans tous les films** (moyens : un espace continu par séquence, grammaire qui change avec le contenu, techniques choisies par le directeur artistique, consigne dans chaque contrat, contrôle sur la planche) ; effet « PowerPoint » ; zoom permanent ; statistiques sans contexte ; faux documents |
  | 2 bis | Choix des médias | situation authentique ; fonction narrative en une phrase ; mots dans l'image ; image adaptée au récit ; **médias non libres en citation encadrée** (règle par défaut depuis le 29/10/2026, qu'une chaîne peut écarter pour s'en tenir aux licences libres ; trois conditions, logos, extraits de 6 s au plus, vraies vidéos d'événements, fichiers tirés de YouTube, aucune photo avec filigrane, source notée) ; **téléchargements par le propriétaire** (liste de liens aux noms imposés, vérification ensuite, aucun lot) |
  | 2 ter | Rythme, réalisme, profondeur, arrière-plan | images qui suivent la voix (événement sur le premier mot, ±2 images ; aucune image immobile plus de 1 s depuis le 28/10, 2,5 s auparavant) ; plus de photos réelles ; profondeur 2,5D à trois plans ; fond à couches de la chaîne ; aucune photo répétée ; **aucune vibration** (un texte posé reste immobile) ; **recette d'image v3** (événement toutes les 1,5 à 3 s, rien de vide, dessins ≥ 15 % du temps, chiffres-cibles) ; ajouts du 26/10/2026 (personnes détourées, métaphore dessinée, effets choisis avant de construire) |
  | 2 quater | Animation, transitions, médias au bon moment (28/10/2026) | animations et non schémas posés ; aucune image immobile plus de 1 s ; une idée de mise en scène par passage d'explication ; une transition pensée à chaque coupe, jamais deux fois la même ; médias au bon moment, pas de collage ; arrêt sur image 2 s au plus ; aucun temps sans voix ajouté ; jonctions vivantes ; savoir-faire à lire avant la fiche d'effets |
  | 3 | Contrat de scène | besoin narratif d'abord ; **pas d'images clés soumises au propriétaire** (15/10/2026) ; tableau de huit champs (enjeu, avant/après, matériaux, progression, raccords, lecture, audio, refus) |
  | 3 bis | Contrat de plan | sept points par unité audiovisuelle (phrase, découverte, média et statut, état initial, transformation, raccord, état final) |
  | 4 | Portes de qualité | A intention ; B technique et preuve du mouvement (planche de 16 à 20 instants, vibration par FFmpeg, photos répétées, outils de `outils/controle/`) ; C visionnage et critique par `art-director` ; D son et image ; E revue humaine ; cas bloquants ; grille 0/1/2 |
  | 5 | Référence d'étude de la chaîne | renvoie à `direction/ECARTS.md` |
  | 6 | Décisions ouvertes | renvoie à `direction/ECARTS.md` |
- **Liens** : cite `MOTION_CATALOG.md` (colonne « Épisodes », choix des techniques), `DIRECTION_AUDIO.md` (§ 2 impact, porte D), `skills/episode/references/production.md` (§ 1 recette v3, § 2 fiche d'effets), `outils/controle/` ; cite les skills HyperFrames `hyperframes-animation` (WAAPI et CSS seulement) et `hyperframes-keyframes` (voir [`vendor.md`](vendor.md)). Lien : [`agents.md`](agents.md), [`skill-episode.md`](skill-episode.md), [`outils-et-garde.md`](outils-et-garde.md).
- **À savoir** :
  - la commande de mesure de vibration du § 4 est une commande FFmpeg complète (`crop`, `gblur`, `tblend`, `signalstats`) : à lancer à la main ou par `controle.py vibration` ; le « 0 » parfait n'est pas attendu avec le grain et la brume ;
  - le § 2 quater dit que, **en cas d'écart avec le § 2 ter, la règle la plus stricte s'applique** (aucune image immobile plus de 1 s) ; le § 2 ter et la porte B disent la même chose depuis le 29/10/2026 ;
  - le texte posé ne bouge ni en échelle ni en flou : seule l'entrée/sortie courte en opacité ou en glissement est permise ;
  - aucune image générée par IA, pas de 3D, pas de détourage automatique sans outil installé.

### referentiels/MOTION_CATALOG.md
- **Rôle** : catalogue de 70 techniques d'animation et de transition. C'est une **proposition** : des possibilités, pas un modèle. Chaque fiche se suffit : aucun film ni projet à ouvrir.
- **Quand il sert** : le directeur artistique (`art-director`) choisit les techniques d'un film, anciennes ou nouvelles ; le producteur (`motion-producer`) lit l'index et écrit sa **fiche d'effets** avant toute scène (skill `episode`, `references/production.md` § 2) ; le mainteneur (`studio-maintainer`) ajoute ou met à jour une fiche sur demande. Cité aussi par `templates/CONTRAT_MISSION.template.md` et `templates/CLAUDE.episode.template.md`.
- **Comment le lire** (règle d'économie, validée sur AA le 18/10/2026) : ne jamais ouvrir le fichier entier. Lire le début du fichier, jusqu'à la première fiche `###` (en-tête et index : c'est la plage que citent le contrat de mission, le skill `episode` et le producteur), puis la seule fiche utile :
  ```bash
  grep -n -A 2 "^### ID" "${CLAUDE_PLUGIN_ROOT}/referentiels/MOTION_CATALOG.md"
  ```
  (dans Bash, écrire le chemin du plugin en entier : la variable n'y existe pas).
- **Contenu** :
  - **En-tête** (lignes 1–6) : statut, règle de lecture.
  - **Règles communes** (lignes 8–14, non répétées dans les fiches) : une technique sert une idée du récit, sur des médias réels ; reprise permise d'une fiche déjà employée (on l'améliore, on ne la recopie pas) ; couleurs du récit (seules la signature, l'appel et l'outro gardent celles de la marque) ; schéma d'étude = « illustration, not study data » ; un mouvement doux part 0,13 à 0,15 s avant le mot ; rendu Chrome : un texte posé reste immobile.
  - **Ajouter une technique** (ligne 16) : une ligne d'index et une fiche de deux ou trois phrases (Recette, Attention), sans chemin ni temps de film, au statut `expérimental`. Dans une chaîne, elle s'ajoute dans la section MOTION_CATALOG de `direction/ECARTS.md`.
  - **Choisir** (ligne 18) : le producteur choisit lui-même, avec une réflexion écrite ; chaque film doit faire mieux que le précédent.
  - **Index** (lignes 20–92) : 70 lignes, colonnes ID · Type · Pour · Épisodes.
  - **Fiches** (ligne 94 et suivantes) : 70 titres `### ID · Titre`, chacune avec **Recette** et, souvent, **Attention**.
- **Catégories (colonne « Type »)** :
  | Type | Nombre | Sens |
  |---|---|---|
  | Espace | 6 | décor en profondeur, monde à stations, strates |
  | Transition | 15 | passer d'un plan à l'autre avec une raison |
  | Texte | 10 | mots qui naissent, se cachent, se surlignent |
  | Archive | 10 | photos et documents réels mis en mouvement |
  | Donnée | 14 | chiffres, études, classements |
  | Trait | 3 | tracés dessinés (comptes, liens, versions) |
  | Schéma | 7 | diagrammes d'idées |
  | Carte | 3 | cartes et trajets |
  | Marque | 1 | signature et outro de la chaîne |
  | Montage | 1 | placement de l'appel Like + Subscribe |
- **Statuts** : toutes les fiches sont `expérimental` (réalisées, non jugées par le propriétaire), sauf les dix fiches « Tifo » non réalisées (voir ci-dessous). `à améliorer` ou `validé` (accord daté du propriétaire) s'écrivent dans la fiche. Le mainteneur ne pose « validé » que si le contrat cite l'accord explicite du propriétaire (définition de `studio-maintainer`).
- **Colonne « Épisodes »** : historique d'AA (E001, E003, E004). Une autre chaîne note ses reprises dans `direction/ECARTS.md`. Dix fiches portent « — (Tifo) » : elles viennent de l'étude AA de Tifo Sports (26/10/2026) et **ne sont pas encore réalisées** (`IRIS-OPEN`, `MATTER-WIPE`, `STACK-LIST`, `BEFORE-AFTER`, `CUTOUT-FIGURE`, `RANK-REVEAL`, `DIMENSION-STRETCH`, `SPRING-POP`, `ANSWER-ICONS`, `DRAWN-METAPHOR`).
- **Liens** : cite `REFERENTIEL_QUALITE_REALISATION.md` (§ 2, § 2 bis, § 2 ter), `METHODE_RECIT.md` § 2 (fiches `BEFORE-AFTER`, `ANSWER-ICONS`), `DIRECTION_AUDIO.md` § 2 (fiche `MATTER-WIPE`), `marque/README.md` et `direction/ECARTS.md` de la chaîne (fiches `BRAND-SPLIT`, `HOLD-CALL`).
- **À savoir** :
  - `BRAND-SPLIT` (ex-AA-SPLIT) n'a pas de recette : « propre à la chaîne » (renvoi à `direction/ECARTS.md` et `marque/README.md`) ;
  - le seul texte posé admis reste immobile : `controle.py tremblement` ne voit pas le défaut d'un texte qui glisse, il faut mesurer le centre des lettres image par image ;
  - les fiches Espace seules (ex. `PAPER-DEPTH`) « n'empêchent pas le diaporama » : ce sont des décors, pas des transitions.

### referentiels/DIRECTION_AUDIO.md
- **Rôle** : règles par défaut de la voix, de la musique, des ambiances, des effets et du mixage (cibles de livraison, chaîne ElevenLabs, contrôles).
- **Documenté ailleurs** : fiche complète dans [`son.md`](son.md), avec le skill `direction-sonore`, `outils/montage/` et les scripts `transcrire.py` et `ralentir.py`. Cette page ne le décrit pas.
- **Sections** (pour s'y repérer) : § 1 Décisions et contraintes · § 2 Principes · § 3 Mixage et livraison · § 4 ElevenLabs · § 5 Contrôles · Sources (consultées le 12/10/2026).
- **Lien utile ici** : le catalogue y renvoie (`MATTER-WIPE`, bruit de matière) ; le référentiel de réalisation en fait sa porte D.

## Tableau des 70 fiches du catalogue
Ordre de l'index du fichier. « Épisodes » = historique d'AA ; « — (Tifo) » = non réalisée.

| ID | Catégorie | Rôle en une ligne | Épisodes |
|---|---|---|---|
| PAPER-DEPTH | Espace | donner de la profondeur aux images fixes (trois plans à parallaxe) | E003, E004 |
| CONTINUOUS-WORLD | Espace | un seul monde à stations pour toute une séquence | E004 |
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
| WHIP-JUMP | Transition | une rupture de temps brutale (une fois par film) | E003 |
| SPLIT-SYNC | Transition | deux camps au même instant (écran partagé) | E003 |
| TEXT-WINDOW | Transition | un mot qui ouvre sur l'image | E004 |
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
| WE-THEY-DIAGRAM | Schéma | le « we » qui devient « they » (un schéma par film au plus) | E001 |
| BROKEN-THREAD | Schéma | ce qui fait tenir ou céder un lien | E001 |
| SPRING-POP | Schéma | une forme sans texte qui entre à ressort | — (Tifo) |
| ANSWER-ICONS | Schéma | le plan de la réponse en pictogrammes | — (Tifo) |
| DRAWN-METAPHOR | Schéma | une idée abstraite devenue objet du sujet | — (Tifo) |
| ORBIT-DIVE | Carte | de la Terre de nuit à un lieu précis | E001 |
| NIGHT-ROUTE | Carte | un trajet réel sans images du trajet | E001 |
| ARGUMENT-MAP | Carte | une carte qui porte l'argument | E001 |
| BRAND-SPLIT | Marque | signature et outro de la chaîne (ex-AA-SPLIT) | E001, E003, E004 |
| HOLD-CALL | Montage | placer l'appel Like + Subscribe | E004 |

Statut de toutes les fiches : `expérimental`.

## Qui cite quoi
| Référentiel | Cité par |
|---|---|
| `METHODE_RECIT.md` | `REGLES_STUDIO.md` ; skills `episode`, `shorts`, `youtube-seo`, `humanizer` (provenance) ; `outils/shorts/README.md` ; `templates/CLAUDE.episode.template.md` ; `starter/direction/` |
| `REFERENTIEL_QUALITE_REALISATION.md` | `REGLES_STUDIO.md` ; agents `art-director`, `motion-producer`, `research` ; skills `episode`, `shorts`, `javascript-animation` ; `outils/controle/` ; les trois modèles de `templates/` et le gabarit v3 ; `starter/direction/` |
| `MOTION_CATALOG.md` | `REGLES_STUDIO.md` ; agents `art-director`, `motion-producer`, `studio-maintainer` ; skill `episode` ; `templates/CONTRAT_MISSION.template.md` et `CLAUDE.episode.template.md` ; `starter/direction/ECARTS.md` |
| `DIRECTION_AUDIO.md` | voir [`son.md`](son.md) ; aussi `starter/marque/son/README.md` et `starter/direction/` |

## Points à vérifier et tensions entre fichiers
- Les statuts « validé sur AA » sont des décisions d'AA : à confirmer par le propriétaire d'une autre chaîne avant de les reprendre telles quelles (écart dans son `ECARTS.md` sinon).
