# Référence : le skill `episode`

Ce document décrit les dix fichiers du skill `studio-faceless:episode` (la fabrication d'un épisode, du choix du sujet au mix du film) et récapitule ses portes de questions. Le parcours, étape par étape, est dans [`../workflows/episode.md`](../workflows/episode.md).

## Table des matières
- [Vue d'ensemble](#vue-densemble)
- [Fiches des fichiers](#fiches-des-fichiers)
  - [SKILL.md](#skillsepisodeskillmd)
  - [references/etapes.md](#skillsepisodereferencesetapesmd)
  - [references/grilles.md](#skillsepisodereferencesgrillesmd)
  - [references/socle.md](#skillsepisodereferencessoclemd)
  - [references/production.md](#skillsepisodereferencesproductionmd)
  - [references/rendu-collage.md](#skillsepisodereferencesrendu-collagemd)
  - [references/recit-retention.md](#skillsepisodereferencesrecit-retentionmd)
  - [references/choix-sujet.md](#skillsepisodereferenceschoix-sujetmd)
  - [references/pieges.md](#skillsepisodereferencespiegesmd)
  - [references/tokens-contexte.md](#skillsepisodereferencestokens-contextemd)
- [Tableau des portes de questions](#tableau-des-portes-de-questions)
- [Statuts portés par le skill](#statuts-portés-par-le-skill)
- [Points à vérifier et incohérences](#points-à-vérifier-et-incohérences)

## Vue d'ensemble

| Élément | Valeur |
|---|---|
| Nom complet | `studio-faceless:episode` (en-tête `name: episode`) |
| Dossier | `plugins/studio-faceless/skills/episode/` : `SKILL.md` + `references/` (9 fichiers) |
| Déclenchement | Le propriétaire de la chaîne démarre, reprend ou planifie un épisode, ou demande comment un épisode se fabrique (champ `description` de l'en-tête). Claude principal (Studio Director) charge le skill. |
| Hors périmètre | Les shorts (`studio-faceless:shorts`), la miniature (`studio-faceless:thumbnail-strategist`) et le dossier YouTube (`studio-faceless:youtube-seo`) : le skill les appelle à leur étape et ne les décrit pas. |
| Statut | `VALIDÉ` pour la structure (validé sur AA, 24/10/2026). `recit-retention.md` et `choix-sujet.md` restent `PROPOSÉ`, à valider par blocs. |
| Ce que le skill ne fait pas | Il donne l'ordre, les portes et les listes de contrôle. Il ne recopie pas les règles : elles sont dans `REGLES_STUDIO.md`, dans les référentiels du plugin et dans la chaîne. |

Le skill n'est pas dans le champ `skills:` du `motion-producer` (qui précharge `hyperframes-core`, `hyperframes-keyframes` et `hyperframes-animation`). Le producteur reçoit le contenu utile par son contrat de mission et par son brief court.

**Ordre de ce qui fait foi** (de `SKILL.md`) : les règles communes du studio (`REGLES_STUDIO.md`, injectées au début de chaque session) puis le `CLAUDE.md` de la chaîne ; les référentiels du plugin ; `direction/LIGNE_EDITORIALE.md` de la chaîne et `direction/ECARTS.md`, qui l'emporte sur les règles par défaut ; `marque/README.md` et `marque/son/README.md` ; le `CLAUDE.md` et le `BRIEF.md` de l'épisode.

**Les 14 étapes** (numérotées 0 à 13 dans le skill, qui fait foi ; `REGLES_DETAIL.md`, section « Parcours d'un épisode », y renvoie depuis la 0.4.0) : 0 Sujet, 1 Recherche, 2 Angle et découpage, 3 Script, 4 Voix, 5 Socle, 6 Séquence témoin, 7 Production, 8 Rendus, 9 Collage en voix seule, 10 Mix du film, 11 Retours, 12 Publication, 13 Après la sortie.

**Les 8 règles qui évitent les reprises** (`SKILL.md`) : une porte de questions avant chaque étape ; l'image d'abord ; le socle fini avant le premier producteur ; une séquence témoin ; des corrections dans la même version ; un rendu à la fois ; des séquences en voix seule (un seul mix du film) ; Claude n'écoute pas et ne déclare aucun visionnage.

**Quel fichier lire à quelle étape**

| Étape | Fichier(s) |
|---|---|
| 0 Sujet | `choix-sujet.md`, `grilles.md` § 0, `etapes.md` § 0 |
| 1 Recherche | `etapes.md` § 1, `grilles.md` § 1 |
| 2 Angle | `recit-retention.md`, `grilles.md` § 2 |
| 3 Script | `recit-retention.md` § 5, `grilles.md` § 3 |
| 4 Voix | `etapes.md` § 4, `grilles.md` § 4 |
| 5 Socle | `socle.md`, `grilles.md` § 5 |
| 6 et 7 Production | `production.md`, `grilles.md` § 6 et § 7 |
| 8 à 10 Rendus, collage, mix | `rendu-collage.md`, `grilles.md` § 10 |
| 11 à 13 | `etapes.md` § 11 à § 13 |
| À tout moment | `pieges.md`, `tokens-contexte.md` |

## Fiches des fichiers

### skills/episode/SKILL.md
- **Rôle** : point d'entrée du skill. Il fixe les huit règles, la table des 14 étapes (porte de questions, livrable, condition de passage), la liste de contrôle « avant de lancer un producteur » et l'index des références.
- **Quand il sert** : chargé par Claude principal dès que le propriétaire parle d'un épisode (démarrer, reprendre, planifier, « comment ça se fabrique »). C'est le seul fichier lu en entier à chaque fois ; les références se lisent à la demande, par plages.
- **Contenu**
  - En-tête (`name`, `description` en anglais : il liste tout ce que couvre le skill et ce qu'il laisse aux autres skills).
  - Statut et origine : `VALIDÉ` pour la structure, rédigé le 24/10/2026 d'après un audit de la fabrication (étude AA).
  - « Ce qui fait foi » : l'ordre des sources (voir la vue d'ensemble).
  - « Huit règles qui évitent les reprises ».
  - « État, reprise et contexte » (0.2.3, révisé en 0.4.1) : `STATE.md` réécrit et `INDEX.md` mis à jour à chaque fin d'étape ; à chaque fin de porte, l'état écrit puis un `/compact` proposé au propriétaire avec sa consigne (validé sur AA, 02/11/2026 : plus de `/clear`) ; coût connu : 124,6 k au premier appel après compactage, contre 81 à 88 k en session neuve (mesure du 30/10/2026) ; reprise = `INDEX.md` puis `STATE.md` seulement ; le hook `contexte_alerte.py` rappelle le `/compact` dès 200 k ; Claude principal sur Opus, jamais de changement de modèle en cours de session ; contrôle par `studio-faceless:reviewer` avant de montrer un script, une séquence ou le film.
  - « Les étapes » : tableau à cinq colonnes (n°, étape, porte, livrable, condition de passage), de 0 à 13.
  - « Avant de lancer un producteur » : liste de neuf cases (voix figée ; médias vérifiés et inscrits au `PROVENANCE.md` ; aucune photo prise ailleurs ; raccords au pixel ; cartes, logos et dessins prêts ; sons choisis dans `marque/son/` ; brief court ; gabarit v3 et en-têtes HTML contrôlés ; contrat de mission complet).
  - « Références » : les neuf fichiers avec leur rôle en une ligne.
- **Liens**
  - Cite les neuf références, `REGLES_STUDIO.md`, les référentiels (`REFERENTIEL_QUALITE_REALISATION.md` § 2 bis et § 2 ter, `DIRECTION_AUDIO.md` § 3, `MOTION_CATALOG.md`, `METHODE_RECIT.md`), `templates/sequence-gabarit-v3/`, `outils/cartes/` et les skills `grilling`, `research`, `thumbnail-strategist`, `youtube-seo`.
  - Cité par `REGLES_STUDIO.md` (parcours), `agents/motion-producer.md`, `templates/BRIEF.episode.template.md`, le README du gabarit v3, `DIRECTION_AUDIO.md`, `METHODE_RECIT.md`, `REFERENTIEL_QUALITE_REALISATION.md` et `MOTION_CATALOG.md`.
- **À savoir**
  - La colonne « Porte de questions » du tableau (lignes 37 à 50) ne correspond pas toujours aux banques de `grilles.md` : voir [Points à vérifier](#points-à-vérifier-et-incohérences).
  - Condition de passage de l'étape 10 : −16 ±1 LUFS, crête vraie ≤ −1,5 dBTP, statut `ECOUTE_A_FAIRE`. Étape 11 : `APPROUVE_PAR_<PROPRIETAIRE>` (date), posé par le seul propriétaire.

### skills/episode/references/etapes.md
- **Rôle** : le détail de chaque étape, de 0 à 13, avec les entrées, la méthode et la sortie.
- **Quand il sert** : Claude principal le lit au début de chaque étape. Il rappelle d'abord la règle de fin d'étape (0.2.3) : chaque étape se termine par la décision au `BRIEF.md` (statut et date), le `STATE.md` de l'épisode réécrit en entier (2,5 Ko au plus), la ligne de l'épisode mise à jour dans `episodes/INDEX.md`, puis un `/compact` proposé au propriétaire (0.4.1, validé sur AA, 02/11/2026 : plus de `/clear`). Les étapes 3, 8 et 10 renvoient au contrôle par `studio-faceless:reviewer` avant de montrer l'objet au propriétaire ; l'étape 0 crée aussi `STATE.md` et la ligne d'`INDEX.md`.
- **Contenu**
  - § 0 Sujet : entrées (registre de `direction/LIGNE_EDITORIALE.md`, `docs/veille/`, bilans publiés), 5 à 8 candidats notés, vérification de la saturation, promesse en une phrase, titre de 60 caractères au plus ; création de `episodes/<id>/` depuis les modèles du plugin.
  - § 1 Recherche : `studio-faceless:research`, une mission par grande partie, rapports dans `research/` ; règle des médias candidats (aucun téléchargement à cette étape) ; points de vigilance dans le `CLAUDE.md` de l'épisode.
  - § 2 Angle et découpage : question d'une phrase, promesse, couches, renversement vers 75 %, séquences ; place de la signature ; place du rappel d'abonnement.
  - § 3 Script : narration en anglais, source de chaque phrase, fiche d'ouverture, script ElevenLabs sans balise, phrases d'actualité marquées [MAJ].
  - § 4 Voix : prises générées par le propriétaire, vérification, ralentissement, repères recalés, bandes montage ; la voix se fige ici.
  - § 5 Socle : renvoie à `socle.md`.
  - § 6 Séquence témoin : choix de la séquence, validation par le propriétaire, la leçon devient la recette.
  - § 7 Production, § 8 Rendus, § 9 Collage, § 10 Mix : renvois à `production.md` et `rendu-collage.md` ; le § 10 liste cinq points de la porte (effets, niveaux, jonctions musicales, silences, rappel d'abonnement).
  - § 11 Retours : une correction d'image se fait sur place puis se rend et se recolle ; une correction de son se fait par un remix.
  - § 12 Publication : miniature, dossier YouTube, SRT par `outils/montage/srt.py`, passe d'actualité sur les [MAJ], Claude ne publie jamais.
  - § 13 Après la sortie : bilans J+2, J+7, J+28, leçons ajoutées à `pieges.md`, tokens par étape ; sous-section « Nettoyage et archivage » (corbeille, zip, SFX générés, fichiers hors zip, commande de l'outil).
- **Liens** : renvoie à `grilles.md`, `socle.md`, `production.md`, `rendu-collage.md`, `recit-retention.md`, `choix-sujet.md`, `tokens-contexte.md`, `outils/controle/transcrire.py` et `ralentir.py`, `outils/montage/srt.py`, `outils/archiver_episode.py`, `outils/suivi_tokens.py`, `direction/ECARTS.md`. Détail de l'archivage : [`../workflows/archivage-et-sauvegarde.md`](../workflows/archivage-et-sauvegarde.md).
- **À savoir**
  - Les trois lignes de la § 13 sur l'archivage sont `VALIDÉ` sur AA le 28/10/2026 (Q76 à Q82 de l'E009) : l'archivage peut se faire une fois le master approuvé, même avant la mise en ligne.
  - L'outil d'archivage ne reconnaît pas seul `_etude`, `_rendu-N`, `planche-1`, `controle-planche`, ni les médias et les voix : il faut un `--essai` par chemin de la corbeille.
  - La corbeille est `_A_SUPPRIMER/<épisode>/` ; Claude ne supprime rien, le propriétaire vide ce dossier.

### skills/episode/references/grilles.md
- **Rôle** : les banques de questions des portes, avec une réponse par défaut pour chacune.
- **Quand il sert** : Claude principal le lit avant chaque porte, puis pose les questions au propriétaire avec le skill `studio-faceless:grilling`.
- **Contenu**
  - Forme d'une porte : une série par frontière de l'arbre de décision, questions numérotées, réponse recommandée formulée pour que « oui » l'accepte, faits cherchés par Claude (sous-agent si besoin) et décisions laissées au propriétaire, porte fermée quand plus aucune question n'est ouverte, réponses écrites au `BRIEF.md` avec leur date.
  - Dix banques : § 0 Sujet (8 questions), § 1 Recherche (2), § 2 Angle et découpage (6), § 3 Script (2), § 4 Voix (2), § 5 Socle (5), § 6 Séquence témoin (2), § 7 Production (2), § 10 Mix du film (4), § 12 Publication (2). Soit 35 questions. Détail dans le [tableau des portes](#tableau-des-portes-de-questions).
- **Liens** : cite `METHODE_RECIT.md` (§ 1, § 2, § 3, § 4), `DIRECTION_AUDIO.md` § 2, `rendu-collage.md` § 4, `direction/ECARTS.md`, `marque/son/`. Le skill `grilling` fixe la forme (voir [`skills-annexes.md`](skills-annexes.md)).
- **À savoir**
  - Les réponses par défaut sont des points de départ, à adapter au sujet.
  - Il n'y a pas de banque pour les étapes 8, 9, 11 et 13, bien que `SKILL.md` leur donne un intitulé de porte (décidé le 29/10/2026 : à créer au prochain épisode).
  - Les exemples « AA » sont des repères : les écarts de la chaîne (`direction/ECARTS.md`) l'emportent.

### skills/episode/references/socle.md
- **Rôle** : comment construire le kit de l'épisode (`episodes/<id>/kit/`) en une seule fois, avant le premier producteur.
- **Quand il sert** : Claude principal, à l'étape 5. Les agents `research` (médias candidats) et, à la demande du propriétaire seulement, `art-director` (planche de test) y contribuent.
- **Contenu**
  - § 1 Gabarit : le gabarit v3 (voix seule, tableau d'effets proposés) se copie dans `kit/gabarit/` ; la palette de l'épisode se règle en variables.
  - § 2 Voix : bandes montage et repères recalés dans `kit/voix/`, avec un README (durée de chaque bande, silences S1…).
  - § 3 Direction artistique : une page courte (motif matériel, monde et transition par partie, trois moments à réussir par séquence, quotas d'effets rares) et une planche de test validée.
  - § 4 Médias : recherche sans téléchargement ; liste de téléchargement pour le propriétaire (`kit/DEMANDE_TELECHARGEMENTS_vN.md`, noms imposés, dossier de dépôt `kit/media/source-vN/manuel/`) ; vérification du dépôt (SHA-1, dimensions, planche regardée, conversions sans agrandissement vers `kit/media/photos-vN/` et `logos-vN/`, section au `kit/PROVENANCE.md`) ; répartition (une photo = une séquence).
  - § 5 Cartes, logos, dessins : `outils/cartes/cartes.py` (SVG 1920 × 1080), logos téléchargés par le propriétaire, dessins de référence dans `kit/references-vN/`.
  - § 6 Sons : puisés dans `marque/son/`, copiés dans `kit/media/audio/musique/` et `sfx/` ; aucun appel ElevenLabs sans demande ; relevé musical par morceau.
  - § 7 Raccords : `kit/RACCORDS.md`, image de sortie et image d'entrée au pixel pour chaque jonction ; lots composés pour qu'aucune séquence n'attende une autre du même lot.
  - § 8 Consignes communes (`kit/CONSIGNES_COMMUNES_vN.md`) et brief par séquence (environ 3 Ko).
- **Liens** : `templates/sequence-gabarit-v3/` ([`templates.md`](templates.md)), `outils/cartes/cartes.py` ([`outils-et-garde.md`](outils-et-garde.md)), `marque/README.md`, `marque/son/`, `production.md` § 1, `rendu-collage.md` § 4 (le relevé musical sert au mix), `REFERENTIEL_QUALITE_REALISATION.md` § 2 bis. Workflows : [`recherche.md`](../workflows/recherche.md), [`sons.md`](../workflows/sons.md), [`sequence.md`](../workflows/sequence.md).
- **À savoir**
  - Une pièce manquante au lancement donne des contre-exemples et des corrections répétées (E007 v1 et v2 d'AA).
  - Après un rendu, on réextrait l'image de raccord : un élément retiré depuis (la grille de l'E007) a pu la changer.
  - L'emplacement des briefs par séquence et du relevé musical n'est pas précisé : à vérifier.

### skills/episode/references/production.md
- **Rôle** : la recette d'image v3, le contrat du producteur, les lots et les corrections (étapes 6 et 7).
- **Quand il sert** : Claude principal quand il écrit un contrat de mission pour un `motion-producer`, compose un lot ou vérifie un livrable. Le contenu utile au producteur lui arrive par son contrat, en extraits.
- **Contenu**
  - § 1 Recette v3 (`VALIDÉ` sur AA, 24/10/2026) : vivacité (un événement toutes les 1,5 à 3 s, aucun plan de plus de 5 s, coupes sur la voix) ; rien de vide qu'on ne comprend pas ; un fait retiré se montre par la vraie photo puis le graphite ; chaque média a un impact (plein cadre ou 45 % de la hauteur au moins, agrandissement de 1,6 fois au plus) ; dessins et cartes au moins 15 % du temps ; logos avec mesure ; pas de grille ; tableau de chiffres-cibles (plein cadre ≥ 25 %, photo ≥ 45 % de la hauteur ≥ 55 % du temps, dessin ≥ 15 %, plus long plan ≤ 5 s, cadre vide 0 s, texte seul ≤ 1,5 s).
  - § 2 Contrat du producteur : champs du modèle de contrat plus : à lire d'abord, règles d'image (`REFERENTIEL_QUALITE_REALISATION.md` § 2 ter et § 2 quater), point de départ (gabarit v3 sans MP4 ni planches), écriture limitée à son dossier, moteur (HyperFrames 0.8.149, Node 22 par Git Bash, WAAPI et CSS seulement, `snapshot --describe false`, jamais `preview`, `check` sans erreur, `render.sh --workers 2` non lancé), **fiche d'effets avant toute scène**, son (voix seule, tableau d'effets proposés), livrables (README ouvert sur la fiche d'effets, planche de 24 instants dont 6 milieux de transition), plafond de 300 k de contexte puis `ETAT.md`, réponse finale de 12 lignes au plus.
  - § 3 Lots : séquence témoin d'abord ; trois producteurs au plus ; ce que Claude transmet à chaque producteur (image de sortie exacte, photos prises, quotas consommés) ; option « tous à la fois » ; vérification de chaque livrable (planches, `check`, en-têtes HTML, snapshots aux instants retouchés, couleurs).
  - § 4 Corrections : sur place, dans la même version ; nouvelle version seulement pour un défaut majeur ou sur demande ; un rendu déjà fait est rangé dans `_rendu-N/` ; une ligne « Correction du JJ/MM » au README de la séquence.
- **Liens** : `templates/CONTRAT_MISSION.template.md` et `templates/sequence-gabarit-v3/` ([`templates.md`](templates.md)), `referentiels/MOTION_CATALOG.md` ([`referentiels.md`](referentiels.md)), agent `motion-producer` ([`agents.md`](agents.md)), `controle.py couleurs`. Workflow : [`sequence.md`](../workflows/sequence.md).
- **À savoir**
  - Une fiche d'effets absente, ou un choix sans raison, et la séquence n'est pas présentée au propriétaire.
  - L'option « tous les producteurs à la fois » est `VALIDÉ` sur AA comme option seulement (28/10/2026, Q72) ; par défaut, des lots de trois. Elle suppose tous les raccords écrits au pixel et les photos réparties d'avance.
  - Reprendre un producteur par `SendMessage` n'est possible que si son cache a moins de 5 min environ ; sinon, un agent court (environ 170 à 200 k).
  - Le catalogue se lit « jusqu'à la première fiche `###` » (début du fichier : en-tête et index), plus de numéros de lignes.

### skills/episode/references/rendu-collage.md
- **Rôle** : les rendus, les contrôles d'une séquence rendue, le collage en voix seule, le mix du film, le master, les sous-titres (étapes 8 à 10, et début de 12).
- **Quand il sert** : Claude principal, sans agent, de la fin de `render.sh` jusqu'au master. Il lance lui-même les outils.
- **Contenu**
  - § 1 Rendus : un rendu à la fois ; attente par `bash outils/rendu/rendre_si_libre.sh <render.sh> <journal>` ; une seule tâche suivie qui enchaîne la file ; `TaskStop` ne tue pas le `node` enfant (`taskkill //T //F //PID`) ; durées constatées (7 à 16 min pour une séquence d'une à deux minutes, plus de 5 h si la machine est chargée) ; un rendu à refaire va dans `_rendu-N/`.
  - § 2 Contrôles d'une séquence rendue : quatre commandes de `controle.py` (`tout`, `son`, `tremblement`, `planche`) ; comment lire le tremblement ; la planche est regardée avant de montrer ; statut `MESURES_TECHNIQUES_OK` ou correction sur place ; le son d'une séquence en voix seule n'a pas de cible de sonie.
  - § 3 Collage en voix seule : `assembler.py --episode <id> --voix-seule` (schéma de `montage.json` dans `outils/montage/README.md`) ; jonctions comparées par PSNR et planche des paires ; contrôles (nombre d'images, journal du collage, décodage complet).
  - § 4 Mix du film : `mix_film.py <film>-voix.mp4 plan-son.json [--son-seul]` ; le plan son (musique, effets, silences voulus) ; tableau des niveaux de départ par type (musique 13, ambiance 16, impact 14, souffle 18, montée 16, papier ou déclic 20, en LU sous la voix) ; fin du mix (un gain final vers −16 LUFS, signature et outro à leur niveau d'origine, limiteur à −2,0 dBTP) ; fin du film en douceur (paramètres de `montage.json` et de `plan-son.json`) ; contrôles du master ; une correction de son = un remix.
  - § 5 Sous-titres et publication : `srt.py` (script vérifié, mots recalés, journal du collage en voix seule `<nom>-voix.log.txt` écrit par `assembler.py`, pas celui de `mix_film.py` ; deux lignes de 42 caractères au plus, 1 à 7 s) et `publication.py chapitres` (même journal).
- **Liens** : [`outils-et-garde.md`](outils-et-garde.md) (outils), [`son.md`](son.md) (niveaux), `DIRECTION_AUDIO.md` § 3, `outils/montage/README.md`, `outils/controle/README.md`. Workflows : [`rendu-et-controle.md`](../workflows/rendu-et-controle.md), [`collage-et-mix.md`](../workflows/collage-et-mix.md), [`dossier-youtube.md`](../workflows/dossier-youtube.md).
- **À savoir**
  - Fin du film en douceur : `VALIDÉ` sur AA, 28/10/2026 (Q71 de l'E009). Niveaux de départ, gain final et écart de voix mesuré sans égalisation : `VALIDÉ` sur AA, 24/10/2026 (Q12 à Q14), à calibrer à la première écoute du propriétaire.
  - Le master reste `ECOUTE_A_FAIRE` tant que le propriétaire n'a pas écouté.
  - Un tremblement signalé se vérifie sur 10 images consécutives avant de corriger ; des crans d'un pixel sur une photo qui dérive sont tolérés, pas sur du texte.
  - La commande de garde des rendus se lance avec `bash`, comme l'indique l'en-tête du script.

### skills/episode/references/recit-retention.md
- **Rôle** : la méthode de récit appliquée à un épisode : repères d'ouverture, patron du film, accroches, relances, densité, succession des séquences, mesures après la sortie.
- **Quand il sert** : Claude principal aux étapes 2 (angle) et 3 (script), et au moment des contrôles avant la voix.
- **Contenu**
  - § 1 La perte est au début : mesure d'AA (53 à 60 % des spectateurs partent vers 0:30) et tableau des repères de 0 à 1:30 (visage nommé ou anomalie en image comparée avant 0:15 ; preuve entre 5 et 15 s ; contradiction complète avant 0:40 ; question d'une phrase avant 0:45, dite et écrite ; signature puis plan de la réponse en 2 ou 3 pistes ; première pièce de réponse avant 1:30).
  - § 2 Patron du film de 8 à 10 min (accroche, signature, première réponse, deux couches, renversement vers 75 %, dernière révélation, formule courte) et exemple de l'E007 d'AA.
  - § 3 Quatre accroches (acte inexplicable, chiffre comparé, état A puis B, évidence fausse, qui est l'accroche par défaut).
  - § 4 Relances : ce qui relance et ce qui ne relance pas ; la surprise se montre.
  - § 5 Densité et contrôles avant la voix : au plus trois chiffres d'affilée, au plus trois noms propres nouveaux par minute, pause de voix de 0,5 à 1 s avant une révélation sur image réelle, fiche d'ouverture à 125 mots par minute.
  - § 6 Succession des séquences : chaque séquence finit sur la question que la suivante reprend ; raccords exacts ; rythme d'image.
  - § 7 Après la sortie : rétention à 0:30, 1:00, 2:00 ; taux de clic au-delà d'environ 1 000 impressions ; conclusion à partir d'environ 100 spectateurs.
- **Liens** : `METHODE_RECIT.md` (règle qui fait foi, [`referentiels.md`](referentiels.md)), `DIRECTION_AUDIO.md` § 2, `socle.md` § 7. Workflow : [`episode.md`](../workflows/episode.md) (étapes 2 et 3).
- **À savoir**
  - Statut `PROPOSÉ`, à valider par blocs. Les repères d'ouverture, de première réponse, de renversement et de dernière révélation sont validés sur AA (26/10/2026, `METHODE_RECIT.md`) ; le reste du patron est `PROPOSÉ`.
  - La boucle de curiosité de `METHODE_RECIT.md` § 1 reste la règle.
  - Gemini ne juge pas une ouverture : il ne sert qu'à décrire un film publié.
  - L'appel à s'abonner au milieu du film n'est plus une question ouverte : place par défaut vers 2:00 (`METHODE_RECIT.md` § 1, validé sur AA, 26/10/2026), confirmée ou écartée à la porte (ligne 66).

### skills/episode/references/choix-sujet.md
- **Rôle** : la grille de notation d'un sujet, les vérifications en plus, la forme de la promesse et la méthode pour reprendre le principe d'un sujet qui surperforme.
- **Quand il sert** : Claude principal à l'étape 0, pour préparer les trois premiers candidats que choisira le propriétaire.
- **Contenu**
  - § 1 Grille : six critères notés de 1 à 5 (demande, nom connu et médias comptent double ; contradiction ; place libre ; accroche et durée), maximum 45 ; seuil 33/45 au moins et aucun critère double sous 3.
  - § 2 Vérifications en plus : compris par un non-initié (éliminatoire) ; un motif écrit par l'acteur ; au moins trois révélations et un renversement ; le moment (marques [MAJ]) ; personnes (aucun motif prêté sans source).
  - § 3 La promesse : titre de 60 caractères au plus, forme « Why… » par défaut, format guide « Every [x] explained » en essai, miniature et promesse tenue dans les 30 premières secondes, Test & Compare.
  - § 4 Repérer un sujet qui surperforme (`PROPOSÉ`) : vivier, vidIQ seulement sur demande du propriétaire, concurrence de chaque candidat, reprendre le principe jamais la vidéo, faire regarder la référence par `studio-faceless:regarder`, noter 5 à 8 candidats.
- **Liens** : `METHODE_RECIT.md` § 4, `REFERENTIEL_QUALITE_REALISATION.md` § 2 bis, skills `regarder` et `thumbnail-strategist`. Workflows : [`analyse-video.md`](../workflows/analyse-video.md), [`miniature.md`](../workflows/miniature.md).
- **À savoir**
  - Statut `PROPOSÉ` (Méthode v1, étude AA, bloc 1). Le test du non-initié et la forme « Why… » sont `VALIDÉ` sur AA (26/10/2026). Le § 4 est `PROPOSÉ` (28/10/2026, Q74).
  - vidIQ ne sert que sur demande du propriétaire (environ 60 crédits la recherche complète) ; jamais à partir de la chaîne elle-même.
  - 12 mots cités au plus d'une vidéo de référence.

### skills/episode/references/pieges.md
- **Rôle** : les leçons de tous les épisodes, sous la forme « le piège, puis ce qu'on fait ».
- **Quand il sert** : Claude principal le consulte en cas de doute ou avant une étape à risque ; il le complète à la fin de chaque épisode (étape 13).
- **Contenu** : 40 pièges en six familles.
  - Récit (3) : ouverture sur un décor, liste à l'écran, formule finale.
  - Image (9) : briefs qui décrivent du texte, cadres vides, vues d'ensemble en vignettes, écran presque vide pendant un tracé, écran noir en milieu de séquence, filtres d'image, petites images agrandies, photo répétée, logos partout.
  - Médias (8) : Wikimedia 429, filigranes, SVG en WebP, objets confondus, carte du monde « corrigée », extrait décrit sans être regardé, extrait à une seule image clé (réencoder avec `-g 15`), tremblement des vraies vidéos.
  - Production et agents (6) : lots qui attendent les raccords, `<!--` perdu, retouches après la dernière planche, reprise d'un producteur au cache froid, raccord extrait d'un rendu périmé, accroche figée puis collage de vidéos.
  - Technique (11) : `TaskStop`, rendu détaché, `Get-Counter`, quatre rendus en parallèle, outil de tremblement, script de garde, rendu arrêté sans message (code 1), accents dans la console Windows, `drawtext` avec un chemin Windows, `publication.py chapitres`, aperçu envoyé à distance.
  - Son (3) : séquences mixées séparément, clics de voix, son d'un extrait prévu sans transcription.
- **Liens** : cite `REFERENTIEL_QUALITE_REALISATION.md` § 2 quater, `DIRECTION_AUDIO.md` § 2 et § 3, `outils/cartes/README.md`, `outils/rendu/rendre_si_libre.sh`. Les reprises types sont regroupées dans [`../workflows/episode.md`](../workflows/episode.md) (section « Erreurs fréquentes et reprises »).
- **À savoir**
  - Les identifiants E001 à E009 sont ceux d'AA, où le piège est apparu ; chaque chaîne ajoute les siens.
  - Rien dans ce fichier ne devient une règle de la chaîne sans accord du propriétaire, versé dans `direction/`.

### skills/episode/references/tokens-contexte.md
- **Rôle** : économiser le contexte et les tokens pendant un épisode.
- **Quand il sert** : Claude principal à chaque fin de grande étape (état écrit, puis un `/compact` proposé au propriétaire) et quand il délègue une lecture ou une correction. Les règles communes (`REGLES_STUDIO.md`, « Économie de tokens et de contexte ») font foi ; ce fichier donne les mesures de l'E007 d'AA.
- **Contenu**
  - Coûts constatés (producteur de séquence 330 à 460 k ; agent court de correction 170 à 200 k ; chercheur de médias 260 à 340 k ; reprise d'un producteur au cache froid : tout son contexte réécrit).
  - Fin de porte (0.2.3, révisée en 0.4.1) : sujet, recherche, angle, script, voix, socle, séquence témoin, chaque lot, collage et mix ; `STATE.md` réécrit, `INDEX.md` à jour, puis un `/compact` proposé avec sa consigne ; le coût connu (124,6 k au premier appel après compactage, mesure du 30/10/2026) ; le hook `contexte_alerte.py` le rappelle dès 200 k, puis à chaque palier de 50 k ; Claude principal sur Opus, jamais de changement de modèle en cours de session.
  - Lire peu : lectures par plages, une planche à la fois, sorties courtes, lectures lourdes à un sous-agent, ne jamais relire le `.output` d'un agent.
  - Déléguer juste : faits préparés avant la délégation, briefs courts, corrections dans la même version, attentes de rendu en tâche suivie.
  - Écrire court : rapports de 12 lignes au plus, états d'épisode d'une ligne par fait.
- **Liens** : cite `REGLES_STUDIO.md` et `production.md` § 4. Voir aussi `outils/suivi_tokens.py`, que cite `etapes.md` § 13 ([`outils-et-garde.md`](outils-et-garde.md)). Workflow : [`../workflows/session-et-garde-fou.md`](../workflows/session-et-garde-fou.md).
- **À savoir**
  - Les coûts sont ceux d'AA (E007, 24/10/2026) : à relever de nouveau sur une autre chaîne.
  - Le cache d'un sous-agent dure 5 min : jamais d'attente de rendu dans un sous-agent.

## Tableau des portes de questions

Une porte se pose avec le skill `studio-faceless:grilling`. Les réponses vont au `BRIEF.md`, datées. Colonne « Intitulé dans `SKILL.md` » : le libellé de la colonne « Porte de questions » du tableau des étapes. Les colonnes suivantes viennent de `grilles.md`.

| Porte (étape) | Intitulé dans `SKILL.md` | Questions de `grilles.md` | Ce que la porte décide | Réponse par défaut |
|---|---|---|---|---|
| 0 Sujet | candidats, grille, promesse | 8 : résumé en cinq mots ; compris d'un non-initié et anomalie en une image ; acteur, acte et motif écrit ; renversement vers 75 % ; personne ou cas à suivre ; carte ; saturation ; durée et nombre de séquences | Le sujet retenu parmi les trois premiers, la promesse, la durée | Oui aux trois premiers tests, sinon écarter ; un cas par couche ; carte seulement si un lieu porte l'argument ; angle nettement différent si saturé ; 8 à 10 min et 6 ou 7 séquences (6 à 7 min et 5 séquences pour l'essai « Why ») |
| 1 Recherche | parties à chercher, médias candidats | 2 : parties qui méritent une mission ; points de vigilance | Les missions de recherche, ce qui va au `CLAUDE.md` de l'épisode | Le cas central, les précédents ou le mécanisme, puis les médias ; vigilance écrite dans le `CLAUDE.md` |
| 2 Angle et découpage | question, couches, renversement, séquences | 6 : question avant 0:45 ; accroche et image 0:00–0:15 ; 2 ou 3 pistes du plan de réponse et pictogrammes ; première pièce avant 1:30 ; fin de chaque séquence sur la question suivante ; place du rappel d'abonnement | L'angle, le découpage en séquences, le plan de la réponse, la place de l'appel | Question dite et écrite ; évidence démentie avant 0:40 ; pistes jamais la conclusion ; appel vers 2:00 sur un plan calme, plus l'écran de fin |
| 3 Script | fiche d'ouverture, densité, relances | 2 : densité ; balise d'émotion | Les contrôles avant la voix, l'usage éventuel d'une balise | Au plus trois chiffres d'affilée, chiffre clé en paire, inconnu expliqué en moins de 5 s ; aucune balise |
| 4 Voix | voix, prononciations | 2 : voix ElevenLabs ; mots à réécouter | La voix, la liste des mots à vérifier | Voix validée pour la chaîne ; liste jointe au script |
| 5 Socle | direction artistique, médias, sons, raccords | 5 : direction artistique ; médias à télécharger par le propriétaire ; sons ; raccords ; effets rares et quotas | La direction artistique, la liste de téléchargement, les sons, les raccords au pixel, les quotas | Base fixe de la marque plus une palette propre au sujet, testée sur une planche ; liste de liens avec noms imposés ; sons de `marque/son/` ; raccords écrits avant les lots ; un WHIP-JUMP par film, un surligneur deux fois au plus |
| 6 Séquence témoin | quelle séquence, ce qu'elle doit prouver | 2 : quelle séquence ; ce qu'elle doit prouver | La séquence qui sert de recette | La plus riche en techniques nouvelles, à raccords indépendants ; elle prouve la recette d'image et sa grammaire de transitions |
| 7 Production | lots, raccords, quotas | 2 : composition des lots ; que faire d'un défaut trouvé sur une planche | Les lots, la façon de corriger | Trois producteurs au plus, ordonnés par raccords ; correction sur place sans nouvelle version |
| 8 Rendus | ordre | aucune banque (à créer au prochain épisode) | L'ordre de la file de rendus (non détaillé) | À vérifier |
| 9 Collage en voix seule | marque, appel, jonctions | aucune banque (à créer au prochain épisode) | Non détaillé ; les jonctions se mesurent (`rendu-collage.md` § 3) | À vérifier |
| 10 Mix du film | musique, effets, niveaux, silences | 4 : effets à retenir ; niveaux par type ; où la musique continue ou se tait ; rappel d'abonnement | Le plan son | Effets des tableaux des producteurs sans les facultatifs ; niveaux de `rendu-collage.md` § 4 ; la musique continue aux jonctions et baisse en creux avant une révélation ; rappel à sa place |
| 11 Retours | ce que le propriétaire a vu et entendu | aucune banque (à créer au prochain épisode) | Les corrections demandées (image sur place, son par remix) | À vérifier |
| 12 Publication | titre, miniature | 2 : titre ; crédits dans la description | Le titre et la décision sur les crédits | Trois titres vrais et différents puis le choix du propriétaire ; crédits selon sa décision pour l'épisode |
| 13 Après la sortie | relevés, leçons | aucune banque (à créer au prochain épisode) | Non détaillé | À vérifier |

## Statuts portés par le skill

| Fichier | Statut indiqué |
|---|---|
| `SKILL.md` | `VALIDÉ` pour la structure (24/10/2026) |
| `etapes.md` | Aucun statut global ; « Nettoyage et archivage » `VALIDÉ` (28/10/2026, Q76 à Q82) |
| `grilles.md` | Réponses par défaut = points de départ |
| `socle.md` | Aucun statut global ; seule mention : vraies vidéos d'événements et fichiers tirés de YouTube `VALIDÉ` sur AA (28/10/2026) |
| `production.md` | Recette v3 `VALIDÉ` (24/10/2026) ; fiche d'effets `VALIDÉ` (26/10/2026) ; option « tous à la fois » `VALIDÉ` comme option (28/10/2026, Q72) |
| `rendu-collage.md` | Niveaux de départ `VALIDÉ` (24/10/2026, Q12) ; fin du film en douceur `VALIDÉ` (28/10/2026, Q71) |
| `recit-retention.md` | `PROPOSÉ` (repères d'ouverture et de corps `VALIDÉ` le 26/10/2026) |
| `choix-sujet.md` | `PROPOSÉ` (test du non-initié et forme « Why… » `VALIDÉ` le 26/10/2026 ; § 4 `PROPOSÉ`) |
| `pieges.md` | Aucun |
| `tokens-contexte.md` | Aucun (mesures de l'E007 d'AA) |

## Points à vérifier et incohérences
Relevés à la lecture. Les constats réglés par la correction du 28/10/2026 (rappel d'abonnement, corrections d'une séquence, modèle de `CLAUDE.md` d'épisode, plage de lecture du catalogue, `bash` devant `rendre_si_libre.sh`) ont été retirés.

| # | Constat | Fichiers |
|---|---|---|
| 1 | Le tableau des étapes donne une « porte de questions » aux étapes 8, 9, 11 et 13 ; `grilles.md` n'a pas de banque pour elles (décidé le 29/10/2026 : à créer au prochain épisode). Les intitulés de `SKILL.md` ne reprennent pas toujours les questions réelles (par exemple « couches, renversement » à l'étape 2, « fiche d'ouverture, relances » à l'étape 3, « médias candidats » à l'étape 1). | `SKILL.md:37-50`, `grilles.md:12-65`, `etapes.md:3` |
| 2 | Les emplacements du brief par séquence et du relevé musical ne sont pas indiqués. | `socle.md:44`, `socle.md:53-61` |
| 3 | `REGLES_STUDIO.md` numérote le parcours de 1 à 11 ; le skill de 0 à 13. Ce n'est pas une contradiction mais une source de confusion quand on parle de « l'étape 6 ». | `REGLES_STUDIO.md:57-69`, `SKILL.md:37-50` |
