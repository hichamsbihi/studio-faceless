# Référence : les modèles (`templates/`)

Ce document décrit chaque fichier du dossier `templates/` du plugin `studio-faceless` : le contrat de mission, les modèles de `CLAUDE.md`, de `BRIEF.md` et de `STATE.md` d'un épisode, le modèle d'`INDEX.md` des épisodes, et le gabarit de séquence v3 (composition HyperFrames, scripts, matières, polices). Les fichiers du plugin font foi ; en cas d'écart, la documentation se corrige.

## Table des matières
- [Vue d'ensemble](#vue-densemble)
- [Fiches](#fiches)
  - [templates/CONTRAT_MISSION.template.md](#templatescontrat_missiontemplatemd)
  - [templates/CLAUDE.episode.template.md](#templatesclaudeepisodetemplatemd)
  - [templates/BRIEF.episode.template.md](#templatesbriefepisodetemplatemd)
  - [templates/STATE.template.md et templates/INDEX.template.md](#templatesstatetemplatemd-et-templatesindextemplatemd)
  - [templates/sequence-gabarit-v3/README.md](#templatessequence-gabarit-v3readmemd)
  - [templates/sequence-gabarit-v3/PROVENANCE.md](#templatessequence-gabarit-v3provenancemd)
  - [templates/sequence-gabarit-v3/index.html](#templatessequence-gabarit-v3indexhtml)
  - [templates/sequence-gabarit-v3/render.sh](#templatessequence-gabarit-v3rendersh)
  - [templates/sequence-gabarit-v3/voix.py](#templatessequence-gabarit-v3voixpy)
  - [templates/sequence-gabarit-v3/compositions/m01-titre.html](#templatessequence-gabarit-v3compositionsm01-titrehtml)
  - [templates/sequence-gabarit-v3/compositions/m02-fiche.html](#templatessequence-gabarit-v3compositionsm02-fichehtml)
  - [templates/sequence-gabarit-v3/media/ (matières, polices, fond d'exemple)](#templatessequence-gabarit-v3media-matières-polices-fond-dexemple)
- [Écarts et points à vérifier relevés dans ces fichiers](#écarts-et-points-à-vérifier-relevés-dans-ces-fichiers)

## Vue d'ensemble
```
templates/
├── CONTRAT_MISSION.template.md       modèle du message de délégation à un agent
├── CLAUDE.episode.template.md        modèle du CLAUDE.md d'un épisode
├── BRIEF.episode.template.md         modèle du BRIEF.md (brief éditorial) d'un épisode
├── STATE.template.md                 modèle du manifeste de reprise STATE.md d'un épisode (0.2.2)
├── INDEX.template.md                 modèle de episodes/INDEX.md, une ligne par épisode (0.2.2)
└── sequence-gabarit-v3/              point de départ de chaque séquence (voix seule)
    ├── README.md  PROVENANCE.md      mode d'emploi, provenance et licences des matières
    ├── index.html                    composition racine 1920 × 1080
    ├── render.sh  voix.py            rendu final, piste de la voix
    ├── compositions/                 m01-titre.html, m02-fiche.html (moments d'exemple)
    └── media/                        fonds/, fonts/, matieres/
```
- **Qui s'en sert** : le Studio Director (Claude principal). Il copie les modèles d'épisode à l'étape 0 du skill `episode`, le gabarit à l'étape 5 (le kit), et recopie le contrat de mission dans chaque délégation. Le `motion-producer` ne copie pas depuis `templates/` : il part de la copie du gabarit placée dans `episodes/<id>/kit/gabarit/` ; son garde-fou refuse toute commande Bash qui cite `templates/`, sauf un chemin du plugin installé sans « .. » ([`agents.md`](agents.md#agentsmotion-producermd)).
- **Règle d'or** : un épisode ne modifie jamais `${CLAUDE_PLUGIN_ROOT}/templates/`. Le hook du plugin refuse en outre tout Write ou Edit dans le plugin installé : les modèles se changent dans le dépôt du plugin ([`../workflows/faire-evoluer-le-plugin.md`](../workflows/faire-evoluer-le-plugin.md)).
- **`${CLAUDE_PLUGIN_ROOT}` dans les modèles** : cette variable n'existe pas dans l'environnement de Bash. Dans une commande, écrire le chemin complet du plugin installé (`REGLES_STUDIO.md`, première section ; [`../ARCHITECTURE.md`](../ARCHITECTURE.md), « Chemins »).
- **Trois sortes de « brief »** à ne pas confondre : le `BRIEF.md` d'épisode (éditorial, modèle ci-dessous) ; le brief de séquence court (contenu du contrat de mission, 3 Ko au plus) ; le brief de short (modèle dans `skills/shorts/references/brief-short.md`).
- **Workflows** : la séquence de bout en bout est dans [`../workflows/sequence.md`](../workflows/sequence.md) ; le parcours d'un épisode dans [`../workflows/episode.md`](../workflows/episode.md) ; les agents dans [`agents.md`](agents.md).

---

## Fiches

### templates/CONTRAT_MISSION.template.md
**Rôle** : modèle du message de délégation à un sous-agent, avec les neuf champs du contrat et le brief de séquence court destiné au `motion-producer`.

**Quand il sert** : le Studio Director en recopie le bloc `text` dans **chaque** délégation (research, reviewer, art-director, motion-producer, shorts-producer, studio-maintainer). C'est aussi la forme qu'attendent les agents : sans les champs essentiels, ils ne commencent pas et renvoient la liste des champs manquants.

**Contenu**
- **Bloc des neuf champs** (un champ sans objet vaut « aucun ») :

  | Champ | Ce qu'on y met |
  |---|---|
  | `episode_id` | `episode-00N`, ou `studio` (mission hors épisode, toujours le cas du mainteneur) |
  | `objectif` | une phrase |
  | `brief` | chemin ou texte court |
  | `fichiers autorisés en lecture` | chemins exacts |
  | `fichiers autorisés en écriture` | un dossier exact, ou « aucun » |
  | `sources communes` | `direction/…`, `marque/…`, ou « aucune » |
  | `livrables` | liste |
  | `décisions validées` | décision, date et référence, ou « aucune » |
  | `restrictions` | interdits propres à la mission |

- **Section « Règles de la chaîne utiles à la mission »** (0.2.2) : 10 lignes au plus (protection des personnes, sources admises, langues, autres), recopiées du `CLAUDE.md` de la chaîne par l'orchestrateur, à la suite des neuf champs. **Obligatoire pour `research` et `studio-maintainer`**, qui démarrent sans le `CLAUDE.md` de la chaîne (`omitClaudeMd`) ; facultative pour les autres agents.
- **« Selon l'agent »** :
  - `research` : écriture toujours « aucun » ; section des règles de la chaîne obligatoire ;
  - `reviewer` : écriture toujours « aucun » ; le contrat nomme l'objet à contrôler (script, séquence ou film), ses fichiers et la durée visée ;
  - `art-director` : écriture limitée au dossier des images extraites ;
  - `motion-producer` : il faut en plus le chemin du kit (`episodes/<id>/kit/`), un brief de séquence court et un dossier d'écriture exact `episodes/<id>/production/<séquence>-vN/` ; le producteur s'arrête à `render.sh` ; les restrictions rappellent l'interdiction de l'effet diaporama avec sa définition (`REFERENTIEL_QUALITE_REALISATION.md` § 2) ; une correction après visionnage se fait dans la même version (validé sur AA, 24/10/2026) : reprise du producteur si son cache est chaud, sinon un agent court avec un brief de quelques lignes ; nouvelle version seulement pour un défaut majeur ;
  - `shorts-producer` : kit shorts (`episodes/<id>/kit/shorts/`), brief de short, dossier `episodes/<id>/production/short-0N-vM/` ; mêmes règles que le producteur de séquences ;
  - `studio-maintainer` : `episode_id` = « studio » ; sans écriture autorisée, il constate seulement ; section des règles de la chaîne obligatoire.
- **Brief de séquence court** (une page, **3 Ko au plus**, validé sur AA le 18/10/2026). Le producteur ne lit que ce brief, le kit et le `CLAUDE.md` de l'épisode : les règles de `direction/` y sont recopiées en extraits de quelques lignes, jamais renvoyées à un fichier entier. Dix champs :

  | Champ | Contenu |
  |---|---|
  | `séquence` | numéro, titre, durée de la bande voix |
  | `voix` | `kit/voix/…wav` ; repères recalés |
  | `narration minutée` | phrase → début–fin (s), une ligne par phrase |
  | `plan de plans` | moment (s) → média du kit → mouvement voulu → raison d'être |
  | `son` | musique du kit et gain relatif ; effets au moment exact, ou « aucun » |
  | `gabarit` | `kit/gabarit/` ; éléments à réutiliser |
  | `règles utiles` | extraits courts de `direction/` et des consignes de l'épisode (palette, typographie, vibration, photos répétées…) |
  | `fiches du catalogue` | identifiants suggérés, ou « aucune » ; le producteur lit l'index de `MOTION_CATALOG.md` et choisit lui-même |
  | `épisode précédent` | retours du propriétaire à appliquer ; techniques déjà employées, à améliorer et non à recopier |
  | `sortie` | dossier d'écriture exact ; nom du MP4 prévu |

**Liens** : cite `REGLES_STUDIO.md` (« Sous-agents », définition des neuf champs), `referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2, `referentiels/MOTION_CATALOG.md`, `skills/shorts/references/brief-short.md`. Cité par chaque fichier de [`agents/`](agents.md), par `skills/episode/references/production.md` § 2 et `REGLES_STUDIO.md`.

**À savoir**
- Le contrat du producteur est plus riche que ce modèle : `production.md` § 2 ajoute « à lire d'abord », règles d'image, point de départ, moteur, fiche d'effets, son, livrables, plafond de 300 k et réponse finale de 12 lignes au plus ([`../workflows/sequence.md`](../workflows/sequence.md)).
- Le brief renvoie à l'index du catalogue par « début du fichier, jusqu'à la première fiche `###` », et non par des numéros de ligne.
- Statut : le modèle ne porte pas de statut ; le parcours raccourci qu'il décrit a été validé sur AA le 16/10/2026.

### templates/CLAUDE.episode.template.md
**Rôle** : modèle du `CLAUDE.md` d'un épisode (instructions propres à l'épisode, quatrième et dernier niveau de l'ordre des règles : `REGLES_STUDIO.md` et référentiels, puis `direction/ECARTS.md`, puis `CLAUDE.md` de la chaîne, puis celui de l'épisode ; [`../ARCHITECTURE.md`](../ARCHITECTURE.md)).

**Quand il sert** : à l'étape 0 du skill `episode`, le Studio Director crée `episodes/<id>/` à partir des modèles du plugin et copie ce fichier en `episodes/<id>/CLAUDE.md`, puis le complète sans inventer de validation. Il est ensuite tenu à jour à la fin de chaque étape (état, dernier travail, prochaine action) ; les agents en lisent les constats techniques.

**Contenu** (le fichier se déclare « inactif tant qu'il n'est pas utilisé pour un épisode autorisé »)
- **Cadre applicable** : respecter le `CLAUDE.md` de la chaîne ; référentiels à consulter selon la mission (`direction/LIGNE_EDITORIALE.md`, `METHODE_RECIT.md`, `REFERENTIEL_QUALITE_REALISATION.md`, `DIRECTION_AUDIO.md`) ; les écarts de `direction/ECARTS.md` l'emportent ; renvoyer sans recopier ; langues de la chaîne (son `CLAUDE.md`) ; ne pas importer les acquis d'autres épisodes.
- **Périmètre de l'épisode** : identifiant et sujet, brief de référence, travail actuellement autorisé, limites particulières (quatre champs à remplir).
- **Structure et périmètre des sous-agents** : dossiers de l'épisode (`BRIEF.md`, `inputs/` en lecture seule, `research/`, `assets/` avec leur `PROVENANCE.md`, `kit/`, `production/<séquence>-vN/`, `montage/`, `outputs/`, `miniatures-vN/`) ; lecture par défaut d'un sous-agent (ce dossier, les référentiels utiles, les ressources approuvées listées ici) ; écriture seulement aux chemins du contrat ; constats techniques (HyperFrames, rendus), lus par `motion-producer` ; mémoire (un enseignement durable est proposé au propriétaire puis versé dans `direction/`, une technique d'animation dans la section MOTION_CATALOG de `direction/ECARTS.md`).
- **Recherche et narration** : partir de la question du brief, relier les affirmations à des sources, distinguer faits, hypothèses et interprétations, ne pas promettre de découverte.
- **Décisions et état** : décisions éditoriales consignées dans le brief avec leur statut ; toute modification importante du sujet, de l'angle ou de la promesse demande la validation de l'utilisateur ; deux lignes depuis la 0.2.2 : l'état courant renvoie à `STATE.md` (à lire seul pour reprendre, réécrit à chaque fin d'étape) et à `HISTORIQUE_ETAT.md`, puis la prochaine action autorisée (avant 0.2.2 : trois champs à renseigner, état actuel, dernier travail et points non résolus, prochaine action autorisée).
- **Dernière ligne** : « Ce fichier définit des instructions ; il ne lance aucune action ni aucun processus autonome. »

**Champs à remplacer** (entre crochets) : `[identifiant et sujet]` (titre), `[chemin du brief propre à cet épisode]`, `[à renseigner d'après la demande utilisateur]` (travail autorisé), `[à renseigner si nécessaire]` (limites), `[à renseigner]` (ressources approuvées du studio), `[à renseigner au fil de la production]` (constats techniques), `[non démarré / recherche / autre état explicitement établi]`, `[à renseigner]` (dernier travail), `[à renseigner ; ne pas supposer une autorisation de production]` (prochaine action).

**Liens** : cite `REGLES_STUDIO.md` (via les référentiels), `referentiels/*.md`, `BRIEF.episode.template.md` (par `BRIEF.md`) ; cité par `skills/episode/references/etapes.md` § 0 et par `agents/motion-producer.md` (constats HyperFrames).

**À savoir**
- La liste des dossiers comprend `kit/`, `montage/` et `miniatures-vN/`, que les skills créent (`skills/episode/references/socle.md`, `rendu-collage.md`, `thumbnail-strategist`).
- Les langues ne sont plus écrites en dur : la ligne 8 renvoie aux « langues de la chaîne (son `CLAUDE.md`) ».

### templates/BRIEF.episode.template.md
**Rôle** : modèle du `BRIEF.md` d'un épisode : le brief **éditorial** (question, angle, preuves, hooks, décisions). Ce n'est pas un brief HyperFrames.

**Quand il sert** : le Studio Director le copie en `episodes/<id>/BRIEF.md` à l'étape 0 ; il se remplit au fil des étapes ; chaque étape finit par une décision inscrite au `BRIEF.md`, avec son statut et sa date (`skills/episode/references/etapes.md`, en-tête). Le propriétaire valide les décisions.

**Contenu** (notes en français, formulations destinées au spectateur en anglais ; « un champ non renseigné ou une proposition ne vaut pas validation ») :
- **Référentiels applicables** : renvoie au `CLAUDE.md` de l'épisode, à `direction/LIGNE_EDITORIALE.md`, aux référentiels du plugin ; les écarts de `direction/ECARTS.md` l'emportent.
- **Question centrale** ; **Intérêt du sujet** (pour un curieux non spécialiste, lien avec les territoires de la chaîne) ; **Angle et promesse** (statut proposé ou validé) ; **Hypothèses** ; **Preuves et sources à rechercher** (pistes distinguées des sources consultées) ; **Contradictions et limites** ; **Découverte attendue** (sans prédéterminer le résultat) ; **Pistes de hook et rehook** (en anglais, avec ce dont elles dépendent) ; **Points à approfondir**.
- **Préparation visuelle et audio — si comprise dans la mission** : seulement les choix propres à l'épisode ; rappelle qu'aucune image clé n'est soumise avant animation et que chaque producteur met en scène sa séquence à partir du kit.
- **Décisions et statut de validation** : statut du sujet (candidat, validé pour recherche…), travail autorisé, production autorisée (« non, sauf validation explicite »), puis un tableau à trois colonnes (décision ; statut proposée / validée / à revoir ; référence de la validation, vide sans validation).

**Liens** : cite `REFERENTIEL_QUALITE_REALISATION.md` § 3, `DIRECTION_AUDIO.md`, le skill `episode` ; cité par `CLAUDE.episode.template.md`.

**À savoir** : les statuts du tableau (`proposée`, `validée`, `à revoir`) et du sujet (`candidat`, `validé pour recherche`) sont en minuscules ; `REGLES_STUDIO.md` fixe les statuts de décision `FIXÉ`, `VALIDÉ`, `PROPOSÉ`, `PROVISOIRE`, `QUESTION OUVERTE`. Utiliser les statuts de `REGLES_STUDIO.md` pour rester lisible par les contrôles (voir « Écarts »).

### templates/STATE.template.md et templates/INDEX.template.md
**Rôle** (0.2.2, 30/10/2026) : modèles du manifeste de reprise d'un épisode (`episodes/<id>/STATE.md`) et de l'index des épisodes (`episodes/INDEX.md`). Génériques : ils ne contiennent aucun contenu d'un épisode réel ; ils ont été établis d'après les fichiers de reprise d'une chaîne qui les utilisait déjà.

**Quand ils servent** : `STATE.md` est créé à l'étape 0 du skill `episode` (avec le `CLAUDE.md` et le `BRIEF.md`) puis **réécrit en entier à chaque fin d'étape** ; `INDEX.md` reçoit une ligne par épisode, mise à jour au même moment. Après un `/clear`, la reprise lit seulement `INDEX.md`, puis le `STATE.md` indiqué (`skills/episode/SKILL.md`, « État, reprise et contexte » ; `references/tokens-contexte.md`).

**Contenu**
- **`STATE.template.md`** : un commentaire d'usage à retirer à la copie, puis cinq rubriques : étape courante ; décisions `VALIDÉ` (dont la voix et son `voice_id`, le film visé) ; chemins utiles (voix, médias, direction artistique, gabarits, rendus et leur statut) ; budget (total, consommé, reste, date de la dernière mesure `suivi_tokens.py`) ; prochaine action. **2,5 Ko au plus** une fois rempli : un fait par ligne, rien de ce qui est déjà dans le `BRIEF.md` ou le `CLAUDE.md` ; le détail daté va dans `HISTORIQUE_ETAT.md` (journal lu par `grep`).
- **`INDEX.template.md`** : un commentaire d'usage à retirer, puis un tableau `Id · Sujet · Statut · Reprise` (lien vers le `STATE.md`) et une ligne d'exemple à remplacer.

**Pourquoi** : un `/compact` remet dans le contexte les skills appelés et les fichiers lus (124,6 k au premier appel, contre 81 à 88 k pour une session neuve, mesure du 30/10/2026) ; écrire l'état puis faire `/clear` coûte moins cher.

**Liens** : `skills/episode/SKILL.md`, `references/etapes.md` (en-tête et § 0), `references/tokens-contexte.md` ; `CLAUDE.episode.template.md` (ligne « État courant »).

### templates/sequence-gabarit-v3/README.md
**Rôle** : mode d'emploi du gabarit de séquence v3 : ce qui change par rapport à la v2, le tableau des effets proposés, la liste des fichiers, l'utilisation pas à pas, les règles techniques et la palette.

**Quand il sert** : lu par le Studio Director quand il prépare le kit, et par le `motion-producer` (copié avec le gabarit) quand il construit sa séquence.

**Statut** : `PROPOSÉ` (Claude, 24/10/2026), à la suite des décisions validées sur AA le 24/10/2026 (mix du film à la fin, skill `episode`). La v2 (`VALIDÉ` sur AA le 20/10/2026, avec son `mix.py`) reste dans les archives de la chaîne AA.

**Contenu**
- **Changements par rapport à la v2** : voix seule (plus de `mix.py` ; `voix.py` fait `media/audio/piste-voix.wav` et `pistes/stem-voix.wav`) ; effets proposés dans le README au lieu d'être mixés ; recette d'image v3 (`REFERENTIEL_QUALITE_REALISATION.md` § 2 ter et `production.md` § 1) ; contrôle de l'en-tête (aucun texte nu dans `<head>`, chaque commentaire s'ouvre par `<!--` et se ferme par `-->`) ; inchangés : fond, polices, palette en variables, moments d'exemple, `render.sh`, règles techniques.
- **Tableau des effets proposés** (à recopier dans le README de la séquence) : colonnes code, instant local (s), image qui le justifie, type (souffle, impact, montée, déclic, ambiance…), facultatif. Exemple : `T01-fiche-posee`, 12,40, « la fiche touche le mur », déclic, non. Les sons viennent de `marque/son/` ou du kit ; le Studio Director décide au mix du film.
- **Origine** : séquence 6 v2 de l'E003 d'AA, préférée à la séquence 4 v3 (arrière-plan en un bloc, matières et licences rangées ensemble, mix en pistes séparées, fiche d'étude conforme) ; la séquence 4 v3 dépend d'une caméra 2,5D maison et son `check` signalait du texte masqué par la vignette.
- **Contenu** : table des fichiers (rôle de chacun, repris dans les fiches ci-dessous).
- **Utilisation** : 1. le Studio Director vérifie que `episodes/<id>/kit/gabarit/` n'existe pas, puis copie le gabarit (`cp -r <chemin du plugin>/templates/sequence-gabarit-v3 episodes/<id>/kit/gabarit`) ; 2. le producteur copie `kit/gabarit/` dans un dossier neuf `episodes/<id>/production/<séquence>-vN/` et y copie `media/photos/`, `media/fonds/` (fonds flous de 2112 × 1188, flou σ 14–18, teints à 55 % de `--teinte`), `media/audio/bande-voix.wav` (ni musique ni effets) et l'extrait de provenance, **ajouté** à `PROVENANCE.md` ; 3. il remplace tout ce qui est marqué « À REMPLACER » (liste dans la fiche d'`index.html`), lance `voix.py`, décommente `<audio id="voix">`, écrit le tableau des effets, règle `NOM` dans `render.sh` ; 4. il vérifie : `npx hyperframes check <dossier>` (viser 0 remarque), une planche (`npx hyperframes snapshot <dossier> --at t1,…,t16 --no-end --describe false -o <dossier>/planche`), assemblée en une image par un `ffmpeg … tile=4x4` (la commande exacte est dans le README).
- **Règles techniques** (constats d'AA, E003) : animation = fonction pure du temps, `render(t)` à l'évènement `hf-seek`, un seul système par séquence (pas de GSAP, aucune horloge, aucun `Math.random` ; seul le grain change à chaque image) ; sous-composition : tout dans `<template>`, même `data-composition-id` sur l'hôte et sur la racine du fichier, `data-no-timeline` sur les deux, identifiants préfixés `mNN-`, `data-start` numérique sur l'hôte, temps local par `AA.debutHote()` ; `AA.op()` met `visibility: inherit`, jamais `visible` ; **aucune vibration** (texte posé immobile, pas d'échelle, de flou ni de rotation animés ; transformations 2D seulement ; aucun arrondi au pixel pendant un mouvement lent ; aucun plan figé plus de 2,5 s) ; polices (Newsreader en `@font-face`, IBM Plex Mono injectée par le compilateur) ; taille (plus de 300 lignes : `composition_file_too_large`, donc un moment par fichier).
- **Palette** : socle fixe (papier charbon, contexte flou, vignette, brume, grain) et variables de `:root` (tableau dans la fiche d'`index.html`) ; couleurs d'entités réelles jamais retouchées ; couleurs que la chaîne exclut des films (liste dans `marque/README.md`) interdites ; la signature et l'outro gardent leurs couleurs et s'ajoutent au collage ; contrôle : `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py couleurs <dossier>/index.html <dossier>/compositions/*.html`.

**Liens** : cite `REFERENTIEL_QUALITE_REALISATION.md` § 2 ter, `DIRECTION_AUDIO.md` § 3, `outils/montage/`, `outils/controle/controle.py`, `skills/episode/references/production.md` § 1, `marque/README.md` ; cité par `skills/episode/SKILL.md`, `socle.md`, `production.md`, `agents/motion-producer.md`.

**À savoir**
- Le chemin `${CLAUDE_PLUGIN_ROOT}` de la commande `cp` doit être remplacé par le chemin complet du plugin installé.
- L'exemple du tableau (12,40 s ; « la fiche touche le mur ») est illustratif : il ne correspond pas aux moments d'exemple du gabarit (séquence de 12 s, fiche posée vers 5,7 s).
- « Aucune image immobile plus de 1 s » (`REFERENTIEL_QUALITE_REALISATION.md` § 2 quater ; le gabarit disait 2,5 s jusqu'au 29/10/2026).
- Le gabarit mêle des références propres à la chaîne d'origine (E001, E003, AA) à des consignes générales ; elles servent de provenance, pas de règle.

### templates/sequence-gabarit-v3/PROVENANCE.md
**Rôle** : registre de provenance des matières et polices du gabarit, avec leur licence et leur empreinte SHA-1. Il devient la provenance de la séquence (le producteur y ajoute l'extrait du kit : photos, fonds, voix, musiques, effets).

**Quand il sert** : copié avec le gabarit ; lu par le Studio Director pour les licences, et par `controle.py licences` (qui liste les lignes citant CC BY-SA ou une licence à vérifier).

**Contenu**
- En-tête : toutes les matières sont des copies non modifiées de celles de l'E001 d'AA, sauf la licence du papier (copie de celle de la séquence 6 v2 de l'E003 d'AA) et le fond d'exemple (calcul). SHA-1 vérifiés le 16/10/2026.
- **Resource Boy** : usage personnel et commercial, sans attribution ; pas de revente, de sous-licence ni de redistribution des fichiers seuls, même gratuite. Les fichiers restent dans les projets de la chaîne ; ils ne sortent que fondus dans un film.
- **Tableau** : fichier · origine · licence · SHA-1, pour les six fichiers du dossier `media/` plus IBM Plex Mono (aucun fichier). Détail dans la fiche [`media/`](#templatessequence-gabarit-v3media-matières-polices-fond-dexemple).
- Licences jointes : `resourceboy-License.txt` (`717e5083…`), `resourceboy-fog-License.txt` (`f9e3bee5…`), `Newsreader-OFL.txt` (`b05a591a…`).
- Dernière phrase : dans un projet de séquence, ce fichier devient la provenance de la séquence.

**Liens** : cité par `README.md` du gabarit, `agents/motion-producer.md` (l'extrait est ajouté à la fin de `PROVENANCE.md`, sans effacer les licences des matières).

**À savoir**
- **Empreintes revérifiées** le 28/10/2026 : les neuf SHA-1 (six médias et trois textes de licence) recalculés sur les fichiers du plugin sont identiques à ceux du registre.
- IBM Plex Mono : le registre indique un cache local `~/.cache/hyperframes/fonts/ibm-plex-mono` qui évite tout téléchargement au `check` ; sur une machine sans ce cache, le comportement est à vérifier.
- La clause de non-redistribution de Resource Boy compte pour le dépôt du plugin : il est privé (`README.md` du dépôt) ; ne pas le rendre public ni distribuer le plugin sans retirer ces matières.

### templates/sequence-gabarit-v3/index.html
**Rôle** : composition racine HyperFrames d'une séquence, 1920 × 1080 (rendue à 30 i/s). Elle porte l'arrière-plan commun, la palette (variables CSS), les composants (classes), l'objet JavaScript `window.AA` (outils) et l'habillage (étiquette du coin, crédit, noir d'entrée et de sortie). Les moments se placent dans `compositions/`.

**Quand il sert** : copié avec le gabarit ; adapté par le `motion-producer` (retouches par `Edit`) ; compilé par HyperFrames au `check`, au `snapshot` et au rendu.

**Principe** : chaque élément est une **fonction pure du temps** `t` (secondes de la bande voix). À chaque image, le moteur diffuse l'évènement `hf-seek` ; `render(t)` recalcule tout l'état visible. Ni GSAP, ni horloge, ni `Math.random` : seul le grain change à chaque image, par des positions pseudo-aléatoires fixes (`AA.hasard`).

**Structure du fichier**
| Zone | Contenu |
|---|---|
| `<head>` | `lang="en"` ; `meta` (largeur et hauteur 1920 × 1080) ; `<title>` ; **commentaire d'en-tête** (principe, couches, anti-tremblement, règle du texte) ; `<style>` ; `<script>` qui définit `window.AA` |
| `<style>` : polices | `@font-face` Newsreader (fichier local `media/fonts/Newsreader-VariableFont.ttf`, graisses 200–800) ; IBM Plex Mono injectée par le compilateur |
| `<style>` : palette | variables de `:root` (tableau ci-dessous) |
| `<style>` : arrière-plan | `#papier` (fond `paper-charcoal-rb09.jpg`), `.contexte` (fond flou 2112 × 1188, opacité 0 au départ), `#vignette` (dégradé radial), `.brume` (2304 × 1447, mode `screen`), `#grain` (mode `overlay`, opacité 0,085) |
| `<style>` : composants | `.mono` ; `.etq` (étiquette, 22 px) et `.etq-sous` (ligne d'appoint, 18 px) ; `.titre` (132 px) et `.titre-sous` (60 px) ; `.chiffre` (300 px, couleur `--accent`) ; `.fiche` (1180 × 700, en x 370, y 190) avec `.fiche-revue`, `.fiche-titre`, `.fiche-auteurs`, `.fiche-lieu` ; `.surligne` (trait de surligneur animé par `AA.surligne`) |
| `<style>` : habillage | `#coin` (en haut à gauche, x 96, y 64), `#credit` (en bas à droite), `#noir` |
| `window.AA` | `C` (borne), `L` (progression linéaire bornée), `S`, `SIO`, `EO`, `EI` (courbes), `lerp`, `f` (formatage sans arrondi au pixel), `op` (opacité avec `visibility: inherit`), `flou`, `surligne`, `melange` (mélange de deux couleurs hexadécimales à 6 chiffres), `couleur` (lit une variable de `:root`), `hasard` (aléa fixe), `debutHote` (début de l'hôte d'une sous-composition) |
| `<body>`, racine `#film` | `data-composition-id="gabarit-sequence"`, `data-start="0"`, `data-width="1920"`, `data-height="1080"`, `data-duration="12"`, `data-no-timeline` |
| 1. arrière-plan | `#fond` : `#papier`, `#ctx1` (image de contexte), `#vignette`, `#brume1`, `#brume2`, `#grain` |
| 2. moments | hôtes `#m01` (`m01-titre`, début 0, durée 5,8, piste 2) et `#m02` (`m02-fiche`, début 5,4, durée 6,6, piste 3), avec `data-composition-src` vers `compositions/` |
| 3. habillage | `#habillage` : `#coin` (`#coinT`, `#coinS`), `#credit`, `#noir` |
| 4. son | `<audio id="voix" src="media/audio/piste-voix.wav" …>` **commenté** (à décommenter quand `voix.py` a produit la piste) |
| script final | constantes `T`, `CONTEXTES`, `CONTEXTE_SOUS_FICHE`, `BRUMES`, `PLANS`, `COIN`, `CREDITS` ; fonction `render(t)` ; écouteur `hf-seek` ; premier rendu après le chargement des polices |

**Que fait `render(t)`**
1. *Arrière-plan* : le papier dérive de 1,00 à 1,04 sur la durée de chaque plan de `PLANS` ; chaque contexte de `CONTEXTES` apparaît et disparaît en fondu (opacité plafonnée, baisse sous une fiche), avec une dérive d'échelle de 1 à 1,05 ; les brumes de `BRUMES` glissent lentement ; le grain change de position à chaque image (30 positions par seconde).
2. *Habillage* : l'étiquette du coin (`COIN`) et le crédit (`CREDITS`) apparaissent et s'effacent ; le noir d'entrée se dissipe en 0,6 s, puis le noir de sortie monte de `T.fin − 0,75` à `T.fin − 0,05`.
3. Les moments (sous-compositions) sont minutés par leur hôte et calculent leur propre temps local.

**Variables à remplacer** (marquées « À REMPLACER » dans le fichier)
| Où | Quoi | Par quoi |
|---|---|---|
| `<title>` | `Channel name — EXXX, sequence N "title" (v1)` | nom de la chaîne, épisode, séquence, titre (visible côté spectateur : anglais) |
| `#film` | `data-composition-id` (`gabarit-sequence`) | identifiant unique de la séquence |
| `#film` | `data-duration` (`12`) | durée de la bande voix arrondie à l'image suivante, **identique** à celle de `<audio>` et de la piste son |
| `:root` | `--teinte`, `--teinte75`, `--texte`, `--fiche`, `--encre`, `--surligneur`, `--encre-surligneur`, `--accent` | palette de la direction artistique de l'épisode (hexadécimal à 6 chiffres) |
| `#ctx1` | `src="media/fonds/fond-exemple.jpg"` | fonds du kit (2112 × 1188, flou σ 14–18, teints à 55 % de `--teinte`), un `<img class="contexte">` par fond ; le fond d'exemple ne va dans aucun film |
| hôtes `#m01`, `#m02` | `data-composition-id`, `data-composition-src`, `data-start`, `data-duration`, `data-track-index` | un hôte par moment ; `data-start` numérique en secondes |
| `<audio id="voix">` | ligne commentée | la décommenter, avec la même `data-duration` |
| `T` | `{m02: 5.4, fin: 12.0}` | repères de la voix (débuts de phrase par `silencedetect`, mots internes recalés) ; `T.fin` = durée de la bande |
| `CONTEXTES` | `[id, début, fin, fondu d'entrée, fondu de sortie, opacité 0,25–0,45]` | un contexte par fond |
| `CONTEXTE_SOUS_FICHE` | `[début, fin de la baisse, opacité]` | à régler ou à supprimer |
| `BRUMES` | `[id, début, fin, opacité 0,15–0,35]` | plans d'atmosphère seulement ; pas de brume derrière une fiche d'étude |
| `PLANS` | `[[début, fin], …]` | plans du papier |
| `COIN` | `[début, fin, étiquette, ligne d'appoint]` | textes vus : anglais |
| `CREDITS` | `[début, fin, crédit]` | idem ; visible tant que la photo l'est |

**Palette de `:root`** (valeurs par défaut du gabarit)
| Variable | Rôle | Défaut |
|---|---|---|
| `--teinte`, `--teinte75` | teinte des fonds flous ; fond des crédits et des sous-titres d'étiquette (75 %) | `#0B1622`, `rgba(11,22,34,.75)` |
| `--texte` | texte sur fond, titres | `#F1F3F5` |
| `--fiche`, `--encre` | papier et texte des fiches | `#F1F3F5`, `#0B1622` |
| `--surligneur`, `--encre-surligneur` | surligneur, étiquettes, texte dessus | `#FFE600`, `#0B1622` |
| `--accent` | accent qui porte le sens du récit (chiffre clé, minute décisive) | `#E10600` |

**Commande de rendu** : `index.html` ne se rend pas à la main. Le rendu passe par `render.sh` (fiche suivante), qui appelle `hyperframes render` sur le dossier de la séquence. Contrôles avant rendu : `npx hyperframes check <dossier>` et une planche par `npx hyperframes snapshot <dossier> --at t1,…,t16 --no-end --describe false -o <dossier>/planche`.

**Liens** : charge `media/fonts/`, `media/matieres/`, `media/fonds/` ; appelle `compositions/m01-titre.html` et `m02-fiche.html` ; son audio vient de `voix.py` ; contrôlé par `render.sh` (présence d'une piste `voix` ou `mix` active) et par `controle.py couleurs`.

**À savoir**
- L'objet global s'appelle `window.AA` : héritage de la chaîne d'origine. Les deux moments d'exemple l'utilisent ; le renommer demande de modifier les trois fichiers.
- Un texte posé reste immobile : jamais d'échelle, de flou ni de rotation animés sur un texte ou un bloc qui en contient ; entrée et sortie en opacité ou en glissement linéaire de 1 à 2 px entiers par image (`REFERENTIEL_QUALITE_REALISATION.md` § 2 ter).
- `AA.op()` met `visibility: inherit` : un enfant `visible` resterait affiché hors de la fenêtre de son hôte.
- Le fichier raisonne en système unique (`hf-seek`). Le moteur recale aussi une animation WAAPI en pause, mais le gabarit demande un seul système par séquence ; le `motion-producer` précharge `hyperframes-animation` en WAAPI et CSS : à choisir en connaissance de cause.
- Le commentaire d'en-tête doit rester une vraie balise `<!-- … -->` : un texte nu dans `<head>` s'affichait en bandeau (défaut de l'E007 seq2 v3).
- Les anciennes mentions « v2 », « v1 » dans le commentaire d'en-tête sont historiques : le fichier est le gabarit v3.

### templates/sequence-gabarit-v3/render.sh
**Rôle** : rendu final d'une séquence en MP4 1920 × 1080, 30 i/s, H.264 + AAC 48 kHz, avec `--workers 2`, sans jamais écraser une sortie existante. Repris tel quel de la v2 (20/10/2026).

**Quand il sert** : le producteur l'**écrit** (il règle `NOM`) et ne le lance pas ; le Studio Director le lance en arrière-plan, après les contrôles, depuis Git Bash (Node 22 ou plus).

**Usage** (depuis la racine de la chaîne)
```bash
bash episodes/<id>/production/<séquence>-vN/render.sh
```
En pratique, le Studio Director passe par le script de garde, qui attend la fin des rendus des autres sessions (chemin complet du plugin à écrire en entier) :
```bash
bash "<chemin du plugin>/outils/rendu/rendre_si_libre.sh" episodes/<id>/production/<séquence>-vN/render.sh <journal>
```
Voir [`../workflows/rendu-et-controle.md`](../workflows/rendu-et-controle.md).

**Variable à remplacer** : `NOM="Chaine-EXXX-sequenceN-nom-v1"` (chaîne, épisode, séquence, nom court, version). Le MP4 sort dans le dossier de la séquence : `$DIR/$NOM.mp4`.

**Déroulement**
1. `set -euo pipefail` : le script s'arrête à la première erreur.
2. `DIR` = dossier du script ; `ROOT` = premier dossier parent qui contient `node_modules/hyperframes/package.json` (la racine de la chaîne). Sinon : « HyperFrames introuvable », **code 2**.
3. FFmpeg : `HYPERFRAMES_FFMPEG_PATH`, sinon `ffmpeg` du `PATH`. Aucun chemin absolu.
4. Contrôles : Node 22 ou plus (sinon code 2) ; HyperFrames exactement `0.8.149` dans `node_modules` (sinon code 2) ; sortie absente (sinon « Export existant, aucun écrasement », **code 1**).
5. Avertissement (sans arrêt) si `index.html` n'a aucune ligne `<audio id="voix">` (ou `id="mix"`) active : le film serait muet. Une ligne commentée ne compte pas.
6. Rendu : `node node_modules/hyperframes/bin/hyperframes.mjs render "$DIR" --output "$SORTIE" --fps 30 --workers 2 --quality delivery`, lancé depuis `ROOT`. Le Chrome de HyperFrames (`~/.cache/hyperframes/chrome`) est utilisé sauf si `HYPERFRAMES_BROWSER_PATH` est défini.
7. Décodage complet du MP4 par FFmpeg (`-v error -xerror … -f null -`) : aucune erreur permise.
8. Message « Rendu terminé : <sortie> ».

**Codes de sortie** : 0 rendu et décodage réussis ; 1 export existant ; 2 prérequis manquant (HyperFrames, Node, version) ; tout autre code non nul : échec du rendu ou du décodage (le script s'arrête sur le code de la commande fautive, `set -e`).

**Dépendances** : Git Bash (ou shell POSIX), Node 22+, HyperFrames 0.8.149 dans le `node_modules` de la chaîne, FFmpeg. **Variables d'environnement** : `HYPERFRAMES_FFMPEG_PATH`, `HYPERFRAMES_BROWSER_PATH`.

**Liens** : lit `index.html` (grep de la piste audio) ; lancé par `outils/rendu/rendre_si_libre.sh` ; contrôles suivants : `outils/controle/controle.py` ([`../workflows/rendu-et-controle.md`](../workflows/rendu-et-controle.md)).

**À savoir**
- Le garde-fou voit la commande `bash …/render.sh`, pas la commande interne `hyperframes render` : c'est le script lui-même qui garantit `--workers 2`.
- Pour refaire un rendu, ranger l'ancien MP4 et sa planche de contrôle dans `_rendu-N/` : le script refuse d'écraser.
- Le numéro `0.8.149` est écrit en dur : une montée de version de HyperFrames, décidée par le propriétaire, oblige à modifier ce test (et le `package.json` de la chaîne).
- La ligne 2 du fichier cite « le gabarit v2 » : voir la note historique d'`index.html`.

### templates/sequence-gabarit-v3/voix.py
**Rôle** : produit la piste son de la séquence : la **voix seule**. Depuis le 24/10/2026, une séquence ne porte que la voix ; musique et effets se mixent sur le film collé (`outils/montage/mix_film.py`).

**Quand il sert** : le producteur le lance une fois, après avoir copié la bande voix du kit dans `media/audio/bande-voix.wav` ; puis il décommente `<audio id="voix">` dans `index.html`. Le Studio Director s'en sert ensuite comme référence (`pistes/stem-voix.wav` pour `controle.py son --voix`).

**Usage** (depuis la racine de la chaîne)
```bash
python -I -B episodes/<id>/production/<séquence>-vN/voix.py
```
Aucune option ni sous-commande.

**Entrées et sorties**
| Fichier | Sens | Contenu |
|---|---|---|
| `media/audio/bande-voix.wav` | lu | bande ralentie et vérifiée du kit |
| `pistes/stem-voix.wav` | écrit | voix en double mono, 48 kHz, `pcm_f32le`, **gain 1**, sans coupe ni recalage (référence du mix du film) |
| `media/audio/piste-voix.wav` | écrit | même voix, gain unique vers −18 LUFS, crête d'échantillon ≤ −3 dBFS, `pcm_s24le` (écoute de travail ; ce que charge `<audio>`) |
| `pistes/voix-rapport.txt` | écrit | mesures : LUFS et crête du stem, gain appliqué, LUFS et crête de la piste |

**Fonctionnement** : mesure par `ebur128=peak=sample` (dernier `I` et dernier `Peak` du rapport) ; gain = le plus petit de `(−18 − I)` et `(−3 − crête)`, donc la crête prime sur la cible de sonie.

**Codes de sortie** : 0 réussi ; 1 FFmpeg introuvable, bande voix manquante, **sortie déjà présente** (aucun écrasement, message en français) ou erreur FFmpeg.

**Dépendances** : Python 3 (bibliothèque standard seule), FFmpeg. **Variable** : `HYPERFRAMES_FFMPEG_PATH`, sinon `ffmpeg` du `PATH`. Aucun chemin absolu.

**Liens** : lit la bande du kit (`kit/voix/`, préparée par `ralentir.py`, [`../workflows/voix-off.md`](../workflows/voix-off.md)) ; alimente `index.html` (`<audio>`) ; cité par le README du gabarit, étape 3.

**À savoir** : « −18 LUFS » est un niveau d'écoute de travail ; le niveau final est réglé au mix du film (−16 LUFS), pas ici (`skills/episode/references/rendu-collage.md` § 2 : le son d'une séquence en voix seule n'a pas de cible de sonie). Pour refaire la piste, supprimer ou ranger d'abord les trois sorties (le script ne supprime rien).

### templates/sequence-gabarit-v3/compositions/m01-titre.html
**Rôle** : moment d'exemple n° 1 : un titre, son mot clé surligné, une ligne d'appoint.

**Quand il sert** : copié avec le gabarit ; le producteur le remplace par un fichier par moment, `mNN-nom.html`. Chargé par l'hôte `#m01` d'`index.html` (`data-composition-src="compositions/m01-titre.html"`).

**Contenu**
- `<head>` : un seul commentaire `<!-- … -->` (le moteur ne garde que le contenu de `<template>`).
- `<template>` : un `<style>` (`#m01-titre`, `#m01-bloc` à x 150, y 330), le balisage (`#m01-titre` avec `data-composition-id="m01-titre"`, `data-width`, `data-height`, `data-no-timeline`, puis `#m01-bloc` qui contient `#m01-t` « Title of the *moment* » et `#m01-s` « Day, 1 Month 2000 »), et un `<script>`.
- **Script** : `T0 = AA.debutHote(...)` ; repères locaux `R = {entre: 0.6, mot: 1.6, sous: 2.4, sort: 5.3, fin: 5.8}` (à remplacer, caler sur les premiers mots de la voix) ; `render(t)` : entrée du bloc (monte de 24 px en 12 images, soit 2 px par image, et apparaît), sortie en fondu sur place, trait de surligneur sur le mot clé (le texte passe de `--texte` à `--encre-surligneur` par `AA.melange`), apparition de la ligne d'appoint ; écouteur `hf-seek` avec `ev.detail.time - T0`.

**À remplacer** : les textes (anglais, ce que voit le spectateur), les repères `R` (multiples de 1/30 s), la position du bloc.

**Liens** : utilise `.titre`, `.titre-sous`, `.surligne` et `window.AA` d'`index.html` ; hôte `#m01` ; règle de texte immobile : `REFERENTIEL_QUALITE_REALISATION.md` § 2 ter.

**À savoir** : pas de transformation d'échelle, de flou ni de rotation animée sur le bloc ; le mouvement du plan vient du papier et du contexte d'`index.html`. Le moment dure 5,8 s et son hôte chevauche le suivant de 0,4 s (5,4 à 5,8).

### templates/sequence-gabarit-v3/compositions/m02-fiche.html
**Rôle** : moment d'exemple n° 2 : la fiche « papier » d'une étude se pose, un passage est surligné.

**Quand il sert** : idem `m01-titre.html` ; hôte `#m02` (début 5,4 s, durée 6,6 s).

**Contenu**
- `<head>` : commentaire qui renvoie aux classes `.fiche*`, `.surligne` et `AA`, et indique que le son de la pose (code `P1`) et du trait (`P2`) se place au mix du film aux mêmes instants (temps de la séquence = début de l'hôte + repère local).
- `<template>` : `<style>` (`#m02-fiche`, `#m02-carte`), balisage (`#m02-fiche` puis `#m02-carte.fiche` avec `.fiche-revue` « Journal name · 2000 », `.fiche-titre` avec `#m02-hl.surligne` « key finding », `.fiche-auteurs`, `.fiche-lieu` « University »), `<script>`.
- **Script** : `R = {pose: 0.3, trait: 1.8}` ; pose : descend de 40 px en 20 images (2 px par image) avec une rotation **fixe** de −1,5°, et apparaît en opacité ; trait du surligneur de 0,6 s sur le passage clé.

**À remplacer** : textes (anglais, vérifiés à la source : revue et année, titre exact, auteurs, institution), repères.

**Liens** : `.fiche`, `.surligne`, `window.AA` d'`index.html` ; effets sonores : tableau des effets proposés du README.

**À savoir** : la fiche ne sert que pour une étude réelle, au titre exact ; aucune fausse donnée (`REFERENTIEL_QUALITE_REALISATION.md` § 1, exigence 7). Les codes `P1` et `P2` ne sont définis nulle part dans le gabarit : le code d'effet du README (`T01-fiche-posee`) suit une autre convention ; à harmoniser au besoin.

### templates/sequence-gabarit-v3/media/ (matières, polices, fond d'exemple)
**Rôle** : les matières communes de l'arrière-plan, la police des titres et un fond d'exemple. Aucun média d'épisode. Source de vérité des licences : `PROVENANCE.md` du gabarit. Les SHA-1 ci-dessous ont été recalculés le 28/10/2026 et correspondent au registre.

**Quand ils servent** : chargés par `index.html` (chemins relatifs `media/…`). Ils restent dans le projet de la séquence ; les matières Resource Boy ne sortent que fondues dans un film.

| Fichier | Nature | Taille, dimensions | Licence (d'après `PROVENANCE.md`) | Rôle dans `index.html` |
|---|---|---|---|---|
| `media/matieres/paper-charcoal-rb09.jpg` | image : papier charbon, quasi noir, grain fin | 2560 × 1440, 1 018 282 octets | Resource Boy, `resourceboy-License.txt` | `#papier` (fond, dérive 1,00 → 1,04) |
| `media/matieres/fog-08_resourceboy.jpg` | image : fumée blanche sur fond noir (pack « 200 Fog Textures ») | 3840 × 2411, 1 589 847 octets | Resource Boy, `resourceboy-fog-License.txt` | `#brume1` (mode `screen`) |
| `media/matieres/fog-65_resourceboy.jpg` | image : brume, même pack | 3840 × 2411, 1 363 484 octets | idem | `#brume2` |
| `media/matieres/grain-512.png` | image calculée : bruit gaussien raccordable (graine 20261012, flou σ 0,9, moyenne 128, écart-type 30) | 512 × 512, 202 418 octets | calcul, aucun tiers | `#grain` (mode `overlay`, répété) |
| `media/matieres/resourceboy-License.txt` | texte : licence Resource Boy (papier) | 1 077 octets | — | joint au papier |
| `media/matieres/resourceboy-fog-License.txt` | texte : licence Resource Boy (brumes) | 1 078 octets | — | jointe aux brumes |
| `media/fonts/Newsreader-VariableFont.ttf` | police variable, graisses 200–800 (Production Type, via Google Fonts) | 451 664 octets | SIL OFL 1.1, `Newsreader-OFL.txt` | `@font-face` Newsreader |
| `media/fonts/Newsreader-OFL.txt` | texte : licence SIL OFL 1.1 (© 2020 The Newsreader Project Authors) | 4 394 octets | — | jointe à la police |
| `media/fonds/fond-exemple.jpg` | image calculée : dégradé sombre, quatre halos, bande texturée en bas ; **aucune photo** | 2112 × 1188, 43 715 octets | calcul, aucun tiers | `#ctx1` ; **à remplacer** : il ne montre rien du récit |

SHA-1 : `afa59b2d…` (papier), `c07dbd79…` (brume 08), `9aa290df…` (brume 65), `05625d79…` (grain), `1f3f3359…` (Newsreader), `9c6137c9…` (fond d'exemple) ; les valeurs complètes sont dans `PROVENANCE.md`.

**IBM Plex Mono** : aucun fichier ; la police est injectée par le compilateur HyperFrames (Google Fonts, SIL OFL 1.1, cache `~/.cache/hyperframes/fonts`).

**À savoir**
- Resource Boy interdit la revente, la sous-licence et la redistribution des fichiers seuls, même gratuite (`PROVENANCE.md`, ligne 5 ; licences jointes).
- Le fond d'exemple « ne va dans aucun film » : le remplacer par les fonds du kit (flou σ 14–18, teints à 55 % de `--teinte`).
- Les binaires sont dans le dépôt du plugin en fichiers ordinaires : le dépôt n'a aucune règle Git LFS ([`../ARCHITECTURE.md`](../ARCHITECTURE.md)).

---

## Écarts et points à vérifier relevés dans ces fichiers
Constats de lecture, du plus gênant au moins gênant. Les écarts réglés par la correction du 28/10/2026 (corrections d'une séquence, plage de lecture de l'index du catalogue, dossiers d'épisode du modèle de `CLAUDE.md`, langues en dur de ce modèle, `PROVENANCE.md` du gabarit) ont été retirés.

| # | Constat | Fichiers (lignes) |
|---|---|---|
| 1 | **Planche** : 16 instants (gabarit), 16 à 20 (agent), 24 dont 6 milieux de transition (contrat du producteur). | `templates/sequence-gabarit-v3/README.md:64`, `agents/motion-producer.md:50`, `skills/episode/references/production.md:65` |
| 2 | **Plan figé** : réglé le 29/10/2026, 1 s partout (décision D1). | — |
| 3 | **Statuts** : le `BRIEF.md` utilise `proposée / validée / à revoir`, `candidat`, en minuscules ; les règles communes fixent `PROPOSÉ`, `VALIDÉ`… | `templates/BRIEF.episode.template.md:41`, `45` contre `REGLES_STUDIO.md:79-80` |
| 4 | **Langues en dur** : le modèle de brief écrit encore « français pour les échanges, anglais pour le spectateur », alors que la langue se règle dans le `CLAUDE.md` de la chaîne (le modèle de `CLAUDE.md` d'épisode a été corrigé). | `templates/BRIEF.episode.template.md:3`, `31` contre `REGLES_STUDIO.md:3` |
| 5 | **Nom de chaîne dans le plugin** : le dépôt dit que le plugin « ne contient aucun nom de chaîne » ; le gabarit cite AA, l'E001 et l'E003 (30 mentions de « AA » ou d'« Apparently » dans `templates/`), son code utilise l'objet `window.AA`, et `REGLES_STUDIO.md` nomme Apparently Athletic. | `README.md:16` (dépôt) contre `templates/sequence-gabarit-v3/PROVENANCE.md:3`, `index.html:8`, `README.md:3`, `REGLES_STUDIO.md:3` |
| 6 | **Codes d'effets sonores** : `P1` et `P2` (moment 2) contre `T01-fiche-posee` (README) : deux conventions, aucune table dans le gabarit. À vérifier. | `templates/sequence-gabarit-v3/compositions/m02-fiche.html:6`, `README.md:17` |
