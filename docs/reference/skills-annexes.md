# Skills annexes du plugin

> **Historique, non normatif** (bandeau posé par la 1.1.0, 04/11/2026) : cette page décrit le plugin tel qu'il était quand elle a été écrite. Les règles en vigueur sont dans `plugins/studio-faceless/` (`REGLES_STUDIO.md`, `referentiels/`, skills, agents) ; là où elle s'en écarte, ce sont elles qui s'appliquent.

Cette page décrit les neuf skills « annexes » de `plugins/studio-faceless/skills/` : `grilling`, `humanizer`, `find-skills`, `conseil`, `elevenlabs-sound-effects`, `elevenlabs-music`, `frontend-design`, `lemo-wake`, `lemo-layers` (ces deux derniers depuis la 1.0.0 : voir leur `PROVENANCE.md`). Les skills de métier (`episode`, `shorts`, `thumbnail-strategist`, `youtube-seo`, `direction-sonore`, `regarder`) sont décrits dans [`skill-episode.md`](skill-episode.md), [`publication.md`](publication.md) et [`son.md`](son.md).

## Table des matières
- [Vue d'ensemble](#vue-densemble)
- [grilling](#grilling) : [SKILL.md](#skillsgrillingskillmd)
- [humanizer](#humanizer) : [SKILL.md](#skillshumanizerskillmd), [PROVENANCE.md](#skillshumanizerprovenancemd), [LICENSE](#skillshumanizerlicense)
- [find-skills](#find-skills) : [SKILL.md](#skillsfind-skillsskillmd), [PROVENANCE.md](#skillsfind-skillsprovenancemd), [LICENSE](#skillsfind-skillslicense)
- [conseil](#conseil) : [SKILL.md](#skillsconseilskillmd), [conseil-workflow.js](#skillsconseilconseil-workflowjs), [PROVENANCE.md et LICENSE](#skillsconseilprovenancemd-et-license)
- [elevenlabs-sound-effects et elevenlabs-music](#elevenlabs-sound-effects-et-elevenlabs-music)
- [frontend-design](#frontend-design) : [SKILL.md](#skillsfrontend-designskillmd), [PROVENANCE.md](#skillsfrontend-designprovenancemd), [LICENSE.txt](#skillsfrontend-designlicensetxt)
- [Points à vérifier et incohérences](#points-à-vérifier-et-incohérences)

## Vue d'ensemble
| Skill | Origine | Licence | Statut | Qui l'appelle |
|---|---|---|---|---|
| `studio-faceless:grilling` | écrit pour le studio | — | en service | Claude principal, à chaque **porte** du skill `episode` et à la création d'une chaîne |
| `studio-faceless:humanizer` | blader/humanizer v3.1.0 (Siqi Chen), copie du 28/10/2026 | MIT | `PROPOSÉ` (essai sur un script d'AA) | le **propriétaire** seul, avec `/humanizer`, comme surcouche de relecture des scripts (appel automatique bloqué depuis la 0.2.2) |
| `studio-faceless:find-skills` | vercel-labs/skills, commit `773fb2c`, copie du 29/10/2026 avec une section « Règles du studio » | MIT | `VALIDÉ` (Hicham, 29/10/2026) | le **propriétaire** seul, avec `/find-skills`, quand il cherche un skill (appel automatique bloqué depuis la 0.2.2) |
| `studio-faceless:conseil` | adapté de amgadelgamal/claude-council (commit `819c1d0`) et de tsenart/council-skill (commit `2040ee1`), 04/11/2026 | MIT | `VALIDÉ` (Hicham, 04/11/2026) ; réglages à confirmer au premier conseil | le **propriétaire**, avec `/conseil` ; Claude principal lance le workflow après l'accord sur la question, les sièges et le coût |
| `studio-faceless:elevenlabs-sound-effects` | elevenlabs/skills `sound-effects`, commit `503d4e9`, copie du 29/10/2026 avec une section « Règles du studio » | MIT | `VALIDÉ` (Hicham, 29/10/2026) | le **propriétaire** avec `/elevenlabs-sound-effects`, ou Claude qui lit le `SKILL.md` quand il demande une génération, son par son, coût annoncé avant (appel automatique bloqué depuis la 0.2.2) |
| `studio-faceless:elevenlabs-music` | elevenlabs/skills `music`, même commit et même traitement | MIT | idem | idem |
| `studio-faceless:frontend-design` | anthropics/skills `frontend-design`, commit `ca45fc4`, copie du 29/10/2026 avec une section « Règles du studio » | Apache 2.0 | `VALIDÉ` (Hicham, 29/10/2026) | Claude principal et les producteurs, pour les planches de direction artistique et les compositions |
| `studio-faceless:lemo-wake` | lemomo-ai/lemo-wake `skills/wake`, commit `f070df8`, copie du 04/11/2026 avec une section « Règles du studio » (HyperFrames seul moteur, aucune installation, aucun remplissage, aucun corps qui bouge) | CC BY-NC 4.0 | `VALIDÉ` (Hicham, 04/11/2026) ; à l'essai (fiche LIVING-PHOTO, `expérimental`) | les producteurs et Claude principal, quand une fiche de style validée prévoit une photo vivante |
| `studio-faceless:lemo-layers` | lemomo-ai/lemo-wake `skills/layers`, même commit et même traitement ; `skills/upload` non copié (publication vers leur galerie) | CC BY-NC 4.0 | idem | idem, pour découper une photo en calques |

**Depuis la 0.2.2**, quatre de ces skills portent `disable-model-invocation: true` (`humanizer`, `find-skills`, `elevenlabs-music`, `elevenlabs-sound-effects`), et `conseil` depuis la 0.8.0 : leur description n'est plus dans la liste proposée à Claude au démarrage, et Claude ne les appelle plus par l'outil Skill. Le propriétaire les appelle avec `/nom`, ou Claude lit leur `SKILL.md` quand il le demande. Vérifié avant le réglage : aucun fichier du plugin ne les précharge ni ne demande de les invoquer.

Aucun agent du plugin ne précharge un de ces skills (champ `skills:` des agents : voir [`agents.md`](agents.md)). Seul `grilling` est cité ailleurs dans le plugin (`REGLES_STUDIO.md`, `skills/episode/`), et `humanizer`, `find-skills`, `elevenlabs-sound-effects`, `elevenlabs-music` ne sont cités que dans leurs propres dossiers (`find-skills` est aussi nommé dans la provenance de `humanizer`).

## grilling

### skills/grilling/SKILL.md
- **Rôle** : interroger le propriétaire sans relâche jusqu'à un accord partagé. C'est le format des « portes de questions » du studio.
- **Quand il sert** : appelé par Claude principal (outil Skill, `studio-faceless:grilling`) à chaque porte du parcours d'un épisode (`skills/episode/SKILL.md`, règle 1 ; banques de questions dans `skills/episode/references/grilles.md`), et pour poser les questions de départ d'une nouvelle chaîne ([`../workflows/nouvelle-chaine.md`](../workflows/nouvelle-chaine.md)).
- **Contenu** (30 lignes, en anglais) :
  - **Arbre de décisions** : chaque décision se ramifie en décisions qui en dépendent.
  - **Tours** : la **frontière** est l'ensemble des décisions dont les prérequis sont tranchés ; on pose toute la frontière en un tour, puis on attend les réponses avant le tour suivant.
  - **Format d'une question** : `❓ **Q1** - **<titre>**: <corps, choix éventuels>` puis `➡️ <réponse recommandée>`, séparées par `---`. La question est formulée pour que « oui » accepte la réponse recommandée.
  - **Faits et décisions** : trouver un fait est le travail de Claude (un sous-agent si besoin, sans bloquer le reste de la frontière) ; la décision est au propriétaire.
  - **Fin** : la session est finie quand la frontière est vide ; on n'agit pas avant que le propriétaire confirme l'accord.
- **Liens** : le propriétaire l'invoque directement (`grilling`). Les réponses d'une porte s'écrivent au `BRIEF.md` de l'épisode, avec leur date (`grilles.md`).
- **À savoir** : en-tête `name: grilling`, `description` seulement (pas de `disable-model-invocation`) : Claude peut l'appeler seul. Les réponses recommandées ne valent pas décision : seul le propriétaire valide.

## humanizer

### skills/humanizer/SKILL.md
- **Rôle** : réécrire un texte qui sonne « écrit par IA » pour qu'il sonne comme son auteur, **sans changer ce qu'il dit** et sans rien inventer. Copie fidèle de blader/humanizer v3.1.0 (32 348 octets, 397 lignes, MIT, auteur Siqi Chen).
- **Quand il sert** : surcouche de relecture des scripts, appelée par le propriétaire (`/humanizer`) ; elle porte sur la **narration anglaise** d'un script, après le script v1 et avant les contrôles de densité. Usage décidé sur AA en essai (28/10/2026) ; voir `PROVENANCE.md`.
- **Contenu** :
  | Partie | Contenu |
  |---|---|
  | Pourquoi le texte IA sonne ainsi | cinq familles (mise en scène, rythme par règle, inflation, mise en forme par règle, restes) + « mauvais lecteur » ; une règle : chaque phrase apporte quelque chose de neuf |
  | Comment travailler | 4 étapes : marquer les tics, rédiger, vérifier (aucun fait ajouté ni perdu), écrire la version finale |
  | Voix | un échantillon de l'auteur prime sur les motifs, y compris la règle des tirets ; sans échantillon, la voix dépend du type de texte |
  | Ce qu'il faut rendre | texte collé (brouillon, tics restants, version finale) ; mode fichier (seule la prose change) ; mode intégré (texte final seul) |
  | A. Mise en scène au lieu d'énoncer | 1 « Not X but Y » · 2 phrases de clôture et fragments dramatiques · 3 formules « profondes » · 4 amorces mises en scène · 5 débat avec personne |
  | B. Rythme par règle | 6 triades forcées · 7 débuts de phrase répétés · 8 tirets partout · 9 réserves empilées · 10 mots composés partout · 11 passif et sujets absents |
  | C. Inflation et autorité empruntée | 12 mots d'IA · 13 importance gonflée · 14 liens vagues · 15 participes en « -ing » · 16 langage commercial · 17 autorité empruntée · 18 éviter « is/are/has » |
  | D. Mise en forme | 19 gras décoratif · 20 titres décoratifs · 21 guillemets courbes |
  | E. Restes de conversation | 22 résidu de chatbot · 23 limites de connaissance · 24 titre répété dans la 1re phrase · 25 écrire sur le document au lieu de son sujet |
  | F. Mauvais lecteur | 26 réexpliquer ce que le lecteur sait |
  | Quand ne pas agir | citations, titres, noms propres ; textes d'avant le 30/11/2022 ; détails de voix à garder (détail inhabituel, tension, aparté) |
  | Source | liste « Signs of AI writing » de Wikipédia |
- **Liens** : `PROVENANCE.md` (source, empreintes, usage décidé), `LICENSE`. Aucun autre fichier du plugin ne l'appelle.
- **À savoir** :
  - le fichier est **gardé tel quel** (aucune mise à jour sans décision du propriétaire) ; il est écrit en anglais, et précise que le motif « Not X but Y » se traite de la même façon dans toute langue ;
  - en essai, il ne devient une règle du studio qu'avec l'accord du propriétaire, après l'épisode, versé dans `direction/` de la chaîne ou dans le skill `episode` ;
  - restent intouchables : les « But… » de l'évidence démentie (`METHODE_RECIT.md` § 2), la question de 0:45, les citations, les faits sourcés.

### skills/humanizer/PROVENANCE.md
- **Rôle** : trace l'origine du skill, ses empreintes et l'usage décidé.
- **Quand il sert** : avant toute mise à jour ou tout audit de licence ; lu par le Studio Director et le propriétaire.
- **Contenu** :
  - **Statut** : `PROPOSÉ`, essai sur un script de la chaîne AA (28/10/2026) ;
  - **Source** : dépôt blader/humanizer, version 3.1.0, commit `d4b81278e6604e237bf32f0f7ce5c217aee94269` (28/09/2026), trouvé avec la méthode du skill `find-skills` ; fichiers copiés à la main depuis `raw.githubusercontent.com` ; `npx skills` non lancé ;
  - **Empreintes** (tableau) : `SKILL.md` 32 348 octets, blob Git `19fc6342…`, SHA-256 `0612f1df…` ; `LICENSE` 1 066 octets, blob `625297fb…`, SHA-256 `4ac48102…` ;
  - **Licence** MIT, « Copyright (c) 2025 Siqi Chen » ; le reste du dépôt d'origine (`scripts/`, `agents/`, extensions) n'est pas copié ;
  - **Usage décidé sur AA** : une passe sur la narration anglaise seulement, avec la courte liste des tics corrigés ; intouchables listés ; échantillon de voix = un script déjà validé de la chaîne (style seulement, aucun fait repris).
- **À savoir** : empreintes **vérifiées le 28/10/2026 lors de cette documentation** : SHA-256 et blobs Git identiques aux valeurs annoncées.

### skills/humanizer/LICENSE
- **Rôle** : texte de la licence MIT (« Copyright (c) 2025 Siqi Chen »), exigé par la licence pour accompagner la copie.
- **À savoir** : ne pas le modifier.

## find-skills

### skills/find-skills/SKILL.md
- **Rôle** : trouver des skills d'agent utiles au studio dans l'écosystème skills.sh, les vérifier et les présenter au propriétaire. Copie de vercel-labs/skills (`skills/find-skills/SKILL.md`, commit `773fb2c`, MIT), en anglais, avec une section « Règles du studio » en français sous le titre.
- **Quand il sert** : quand le propriétaire cherche une capacité qui pourrait exister en skill (premier usage, 29/10/2026 : effets sonores et musique de fond).
- **Contenu** : règles du studio (pas de `npx skills` ; recherche sur skills.sh et GitHub par le web ; vérification des installations, de la source, des étoiles, des licences et des dépendances ; adoption par copie à la main, sur décision du propriétaire, avec `LICENSE` et `PROVENANCE.md`, puis nouvelle version du plugin) ; puis le texte d'origine : classement de skills.sh, recherche, seuils (1 000 installations, méfiance sous 100 ; dépôt de moins de 100 étoiles), présentation des options, catégories de recherche.
- **Liens** : `PROVENANCE.md`, `LICENSE` ; méthode déjà suivie pour `humanizer` (28/10/2026).
- **À savoir** : les étapes du texte d'origine qui lancent `npx skills` (`find`, `add … -g -y`, `update`, `init`) sont remplacées par la section du studio ; le garde-fou refuse de toute façon les installations npm.

### skills/find-skills/PROVENANCE.md
- **Rôle** : trace l'origine du skill, ses empreintes et la modification du studio.
- **Contenu** : statut `VALIDÉ` (Hicham, 29/10/2026) ; dépôt, commits de `SKILL.md` et de `LICENSE` ; empreintes (octets, blob Git, SHA-256) du `SKILL.md` d'origine, du `SKILL.md` du studio et de `LICENSE` ; raison de la section ajoutée.

### skills/find-skills/LICENSE
- **Rôle** : texte de la licence MIT (« Copyright (c) 2026 Vercel, Inc. »), exigé par la licence pour accompagner la copie.
- **À savoir** : ne pas le modifier.

## elevenlabs-sound-effects et elevenlabs-music

### skills/elevenlabs-sound-effects/ et skills/elevenlabs-music/
- **Rôle** : générer des effets sonores et ambiances (`eleven_text_to_sound_v2` : 0,5 à 30 s, boucle, fidélité au prompt) et de la musique (`music_v2_5` : prompt ou plan de composition, jusqu'à 10 min, musique calée sur une vidéo) avec l'API ElevenLabs. Copies d'elevenlabs/skills (`sound-effects/`, `music/`, commit `503d4e9`, MIT), en anglais, champ `name` préfixé par `elevenlabs-`.
- **Quand il sert** : seulement à la demande explicite du propriétaire, son par son, avec une estimation des crédits avant ; sons de la marque et des épisodes. Appelé par le propriétaire avec `/nom`, ou lu par Claude quand il demande une génération (appel automatique bloqué depuis la 0.2.2).
- **Contenu** : section « Règles du studio » (SDK Python `elevenlabs` figé dans le `requirements.txt` de la chaîne ; ni CLI, ni npm, ni `npx`, ni installateur ; clé `ELEVENLABS_API_KEY` posée par le propriétaire, que Claude ne lit jamais et dont il vérifie seulement l'existence ; provenance de chaque son ; forfait payant pour l'usage commercial, obligatoire pour la musique ; son illustratif ; depuis la 0.2.2, connecteur claude.ai coupé par défaut et appel automatique bloqué, `DIRECTION_AUDIO.md` § 4), puis le texte d'origine : démarrage, paramètres, formats, conseils de prompt, erreurs ; pour la musique, plans de composition, streaming, inpainting, finetunes, video-to-music (ces trois derniers seulement sur décision du propriétaire).
- **Fichiers** : `SKILL.md`, `references/installation.md` (encadré du studio en tête : seule la section Python s'applique), `references/api_reference.md` (musique, inchangé), `LICENSE` (« Copyright (c) 2024 ElevenLabs »), `PROVENANCE.md` (source, empreintes d'origine et du studio, modifications).
- **À savoir** : l'encadré « Setup » d'origine lançait `npx -y @elevenlabs/cli@latest onboard init` (version non figée, sans confirmation, connexion d'un compte) ; il est remplacé par un renvoi à la section du studio. Le garde-fou ne bloque pas `npx` hors HyperFrames : la règle tient par le texte du skill.

## frontend-design

### skills/frontend-design/SKILL.md
- **Rôle** : méthode de directeur artistique pour des visuels qui ne ressemblent pas à des modèles par défaut. Copie d'anthropics/skills (`skills/frontend-design/SKILL.md`, commit `ca45fc4`, Apache 2.0), en anglais, avec une section « Règles du studio » en français sous le titre.
- **Quand il sert** : planches de direction artistique des chaînes et compositions HyperFrames (premier usage, 29/10/2026 : planche de grammaire visuelle d'une chaîne, jugée trop schématique en v1).
- **Contenu** : règles du studio (planches et compositions, marque validée d'abord, règles propres à la vidéo, images et polices) ; puis le texte d'origine : partir du sujet, typographie, structure, mouvement rare et orchestré, défauts visuels génériques à éviter, plan de jetons relu contre le brief avant de construire, retenue et critique sur captures, écriture.
- **À savoir** : vise les interfaces web ; la section du studio écarte ce qui ne vaut que pour une interface. Pour le mouvement, `hyperframes-animation` fait foi.

### skills/frontend-design/PROVENANCE.md
- **Rôle** : trace l'origine du skill, ses empreintes et la modification du studio.
- **Contenu** : statut `VALIDÉ` (Hicham, 29/10/2026) ; dépôt, commits de `SKILL.md` et de `LICENSE.txt` ; empreintes du `SKILL.md` d'origine, du `SKILL.md` du studio et de `LICENSE.txt` ; raison de la section ajoutée.

### skills/frontend-design/LICENSE.txt
- **Rôle** : texte de la licence Apache 2.0, exigé par la licence pour accompagner la copie.
- **À savoir** : ne pas le modifier.

## conseil

### skills/conseil/SKILL.md
- **Rôle** : faire débattre plusieurs agents Claude indépendants d'une décision du studio (méthode de fabrication, architecture, outil ou service, stratégie), puis rendre au propriétaire un compte rendu `PROPOSÉ`.
- **Quand il sert** : quand le propriétaire demande un conseil avec `/conseil` (premier besoin, 04/11/2026 : la refonte de la fabrication pour plusieurs chaînes). Pas pour une porte d'épisode ; positionnement et titres : `strategist`.
- **Contenu** : porte du propriétaire avant le lancement (question au mot près, sièges, fichiers, mode, nombre d'agents et coût, chemin du compte rendu) ; déroulé en quatre tours ; appel de l'outil Workflow et ses `args` ; ce que le directeur rend ; erreurs et reprises.
- **À savoir** : 2N + 2 agents pour N sièges en mode complet (contre-hypothèse toujours lancée depuis la 1.0.1) ; coût mesuré sur AA : de 68 à 110 k tokens par agent.

### skills/conseil/conseil-workflow.js
- **Rôle** : script de l'outil Workflow. Tour 1, avis en aveugle (sièges en parallèle, agent `conseiller`) ; tour 2, débat sur les avis anonymes (critiques, désaccord principal et gravité, avis qui renforce, ce qui a changé, position finale, classement) ; tour 3, contre-hypothèse, toujours en mode complet (1.0.1) ; tour 4, président, agent `conseiller` en lecture seule (1.0.1), qui rend le compte rendu dans `contenu` ; le directeur l'écrit, sans écraser de fichier.
- **À savoir** : ni horloge ni hasard (la date passe par `args`) ; reprise par `resumeFromRunId` ; essai à sec du 04/11/2026 dans Node avec de faux agents (9 cas).

### skills/conseil/PROVENANCE.md et LICENSE
- **Rôle** : origine (deux dépôts, commits, empreintes des fichiers d'origine et du studio) et changements du studio ; `LICENSE` reproduit les deux textes MIT.
- **À savoir** : ne pas modifier `LICENSE`.

## Points à vérifier et incohérences
- **`skills/humanizer/SKILL.md`** n'est cité par aucun autre fichier du plugin (ni l'étape « script » de `skills/episode/`) : son usage reste un essai d'AA, et depuis la 0.2.3 seul le propriétaire l'appelle (`/humanizer`), comme surcouche de relecture des scripts.
- `README.md` (racine) range `humanizer`, `find-skills`, `conseil`, `elevenlabs-sound-effects` et `elevenlabs-music` parmi les skills MIT ; leurs `LICENSE` sont bien présents dans leurs dossiers.
