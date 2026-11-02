# Copies figées de tiers (`vendor/claude-skills/` et `vendor/roast-room/`)

Cette page décrit les deux copies de tiers rangées dans `plugins/studio-faceless/vendor/` : les dix skills HyperFrames 0.8.149 (`vendor/claude-skills/` : ce que chaque skill fait, combien de fichiers il compte, quels agents du plugin le chargent) et le protocole roast-room de l'agent `strategist` (`vendor/roast-room/`, 0.4.0, MIT). Ce sont des **copies de tiers inchangées** : il n'y a pas de fiche par fichier interne.

## Table des matières
- [Principe et statut de la copie](#principe-et-statut-de-la-copie) (HyperFrames)
- [Vue d'ensemble](#vue-densemble)
- [Fiche du dossier : README.md](#vendorclaude-skillsreadmemd)
- [Fiches des dix skills](#fiches-des-dix-skills)
  - [hyperframes](#vendorclaude-skillshyperframes) · [hyperframes-animation](#vendorclaude-skillshyperframes-animation) · [hyperframes-audio](#vendorclaude-skillshyperframes-audio) · [hyperframes-cli](#vendorclaude-skillshyperframes-cli) · [hyperframes-core](#vendorclaude-skillshyperframes-core)
  - [hyperframes-creative](#vendorclaude-skillshyperframes-creative) · [hyperframes-keyframes](#vendorclaude-skillshyperframes-keyframes) · [hyperframes-registry](#vendorclaude-skillshyperframes-registry) · [hyperframes-studio](#vendorclaude-skillshyperframes-studio) · [media-use](#vendorclaude-skillsmedia-use)
- [vendor/roast-room (0.4.0)](#vendorroast-room-040) : copie du protocole de conseil lu par `strategist`
- [Qui charge quoi](#qui-charge-quoi)
- [Où ces skills s'installent et comment les faire évoluer](#où-ces-skills-sinstallent-et-comment-les-faire-évoluer)
- [Points à vérifier et tensions avec les règles du studio](#points-à-vérifier-et-tensions-avec-les-règles-du-studio)

## Principe et statut de la copie
- **Pourquoi** : le moteur est figé en **HyperFrames 0.8.149** (`package.json` de la chaîne). Les skills de Claude Code qui l'accompagnent peuvent être plus récents que le CLI. Une nouvelle machine doit recevoir *exactement* ces versions (validé sur AA, 21/10/2026), pas les plus récentes.
- **D'où** : copie prise le 21/10/2026 dans `~/.claude/skills/` de la machine de référence.
- **Licence** : Apache License 2.0 (celle du paquet `hyperframes` 0.8.149, champ `license` de son `package.json`) ; © HeyGen et les auteurs de HyperFrames. Copie sans modification.
- **Ce ne sont pas des skills du plugin** : ils sont hors du dossier `skills/` du plugin et restent des **skills d'utilisateur** (`~/.claude/skills/`), **sans préfixe** : un agent les charge sous leur nom court (`hyperframes-core`, pas `studio-faceless:…`). Les skills du studio, eux, arrivent par le plugin (`studio-faceless:…`).
- **Totaux** : 389 fichiers sous `vendor/claude-skills/` (388 pour les dix skills, plus le `README.md`).

## Vue d'ensemble
| Skill | Fichiers | Rôle en une ligne | Préchargé par | Chargé à la demande par |
|---|---|---|---|---|
| `hyperframes` | 31 | point d'entrée obligatoire HyperFrames : état du projet, choix du flux (briefs, storyboards, relecture) | — (les agents du studio sont dispensés de son entretien) | — |
| `hyperframes-animation` | 122 | tout le savoir d'animation : règles atomiques, plans en plusieurs phases, transitions de scène, sept « adaptateurs » d'exécution | `motion-producer` (WAAPI et CSS seulement), `art-director` | `shorts-producer` |
| `hyperframes-audio` | 8 | mixage dans la composition : fondus, gain, automation, ducking, effets, bus | — | `motion-producer` (brief ancien), `shorts-producer` ; cité par `direction-sonore` |
| `hyperframes-cli` | 11 | boucle de commandes du CLI : check, snapshot, render, preview… | — | `motion-producer`, `shorts-producer` |
| `hyperframes-core` | 11 | le contrat d'une composition (attributs `data-*`, pistes, sous-compositions, déterminisme) | `motion-producer`, `shorts-producer` | — |
| `hyperframes-creative` | 79 | direction créative : palettes, typographie, narration, plan des plans, styles | `art-director` | — |
| `hyperframes-keyframes` | 3 | mouvement par images clés : zoom, caméra, masques, tracés, profondeur, preuves au CLI | `motion-producer`, `shorts-producer` | — |
| `hyperframes-registry` | 12 | blocs et composants du registre HyperFrames (`hyperframes add`, `catalog`) | — | — |
| `hyperframes-studio` | 1 | conventions de l'éditeur Studio : parler avant de construire, une scène = une sous-composition, pistes | — | — |
| `media-use` | 110 | « système d'exploitation » des médias : retrouver, générer, opérer (couper, recadrer), mémoriser | — | `motion-producer`, `shorts-producer` |

## vendor/claude-skills/README.md
- **Rôle** : décrit la copie : pourquoi elle existe, sa date, sa licence, comment l'installer et la mettre à jour.
- **Quand il sert** : à lire par le propriétaire ou Claude avant d'installer une machine (`INSTALLATION.md` § 3) ou avant de toucher à la version de HyperFrames.
- **Contenu** :
  - **Titre** : « Skills HyperFrames figés (copie du 21/10/2026) ».
  - **Contenu** : la liste des dix dossiers.
  - **Licence** : Apache-2.0, © HeyGen et auteurs de HyperFrames, copie sans modification.
  - **Installation** : recopier chaque dossier dans `~/.claude/skills/` (`INSTALLATION.md`, section 3).
  - **À savoir** : ces skills sont parfois plus récents que le CLI 0.8.149 et demandent de mettre HyperFrames à jour (`upgrade`, `skills update`) ; les règles du studio l'interdisent sans décision du propriétaire et le garde-fou le refuse ; `hyperframes usage` et `hyperframes figma` n'existent pas en 0.8.149 ; `play` se remplace par `preview`.
  - **Mise à jour de cette copie** : seulement avec une montée de version de HyperFrames décidée par le propriétaire ; nouvelle copie datée, ce fichier mis à jour, nouvelle version du plugin.
- **Liens** : [`../../INSTALLATION.md`](../../INSTALLATION.md), [`../workflows/installation-et-mise-a-jour.md`](../workflows/installation-et-mise-a-jour.md), [`../workflows/faire-evoluer-le-plugin.md`](../workflows/faire-evoluer-le-plugin.md), `REGLES_STUDIO.md` (§ Moteur et outils).
- **À savoir** : aucun fichier de licence n'accompagne les dix skills (voir « Points à vérifier »).

## Fiches des dix skills
Chaque fiche donne le dossier, le nombre de fichiers, le rôle d'après le `SKILL.md` du skill, qui le charge, et les écarts avec les règles du studio. Tous les `SKILL.md` commencent par la même mention : « Plugin installs: … follow plugin execution rules … when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below » (règles dans `hyperframes/references/plugin-installation.md`). Dans le studio, ils sont installés comme skills d'utilisateur (« standalone »).

### vendor/claude-skills/hyperframes
- **Fichiers** : 31 (`SKILL.md` ; `references/` 25 fichiers, dont 10 flux dans `routes/` : sous-titres intégrés, « faceless explainer », vidéo générale, motion design, musique vers vidéo, lancement de produit, PR vers vidéo, port Remotion, diaporama, recoupe de tête parlante ; `scripts/` 5 fichiers : `plugin-cli.mjs`, son test et `lib/`).
- **Rôle** (d'après son `SKILL.md`) : **point d'entrée obligatoire** pour toute demande de vidéo ou d'animation HyperFrames. Il reprend l'état du projet, capte l'intention (entretien), choisit le flux propriétaire (présentation, sous-titres, vidéo musicale, motion design, port Remotion, etc.) et route vers les skills de domaine. Tableau d'états en § 1 (projet existant, `BRIEF.md`, `STORYBOARD.md`, création neuve), table de routage en § 2.
- **Références** : contrat du brief, format de brief, menu de capacités, entretien d'intention, tour de pitch, boucle de production, boucle de relecture, dispatch de sous-agents, format de storyboard et de script, cycle de vie des skills, `plugin-installation.md`, un dossier `routes/`.
- **Chargé par** : aucun agent du plugin. Les définitions de `motion-producer` et `shorts-producer` écrivent : « **Pas d'entretien d'intention ni de routage « création »** du skill `hyperframes` : le contrat et le brief en tiennent lieu. »
- **À savoir** : son § « Check remaining usage » demande `npx hyperframes usage --json`, commande **absente de la 0.8.149** (à ignorer, `REGLES_STUDIO.md`) ; son § « Keep the project's CLI current » propose `npx hyperframes@latest upgrade --project . --check`, que le garde-fou refuse (autre version par `npx`, `upgrade`).

### vendor/claude-skills/hyperframes-animation
- **Fichiers** : 122 (`SKILL.md`, `rules-index.md`, `blueprints-index.md`, `techniques.md` ; `rules/` 48, `blueprints/` 22, `transitions/` 16, `adapters/` 12, `examples/` 13, `references/` 1, `scripts/` 6).
- **Rôle** : « toute la connaissance d'animation » : **règles atomiques** (on en compose 2 à 4), **plans de scène** à plusieurs phases, **transitions** de scène à scène, **techniques** plus larges, et **sept adaptateurs d'exécution** : GSAP (par défaut), Lottie, Three.js, Anime.js, animations CSS, Web Animations API (WAAPI), TypeGPU ; il couvre aussi l'audit d'une chorégraphie (carte d'animation) et 24 effets de texte nommés. Tout est « HyperFrames-natif » : une seule timeline en pause, sans état caché.
- **Scripts** : `animation-map.mjs` (audit d'une composition GSAP), `animation-map-sampling.mjs`, `package-loader.mjs` et leurs tests.
- **Chargé par** : `motion-producer` (préchargé, **en WAAPI et CSS seulement : jamais GSAP, Lottie, Three.js ni Anime.js**, validé sur AA, 24/10/2026) ; `art-director` (préchargé, « seulement si leur vocabulaire t'est utile ») ; `shorts-producer` (à la demande). Le référentiel de réalisation y renvoie (transitions de scène et plans en plusieurs phases, § 2 quater).
- **À savoir** : le défaut du skill est une timeline **GSAP** ; le studio en retient seulement les parties WAAPI/CSS. `animation-map.mjs` lit les timelines GSAP, il ne sert donc pas à une séquence en WAAPI/CSS.

### vendor/claude-skills/hyperframes-audio
- **Fichiers** : 8 (`SKILL.md` ; `references/` 4 : `attributes.md`, `diagnosis.md`, `fx-registry.md`, `presets.md` ; `scripts/` 3 fichiers : `carve.mjs`, `carve.test.mjs`, `lib/main-module.mjs`).
- **Rôle** : mixage de l'audio **déjà placé** dans une composition : fondus, fondus enchaînés, gain de piste, automation de volume, ducking (la musique cède à la voix, « carve »), effets (EQ, compresseur, limiteur, gate, saturation, delay, reverb, chorus, phaser, bitcrush) et bus de mixage (`<hf-audio-group>`). Trois attributs portent tout : `data-fx-chain`, `data-automation`, `data-fx-carve`. L'aperçu et le rendu partagent le même graphe Web Audio. La **source** de l'audio (musique, SFX, voix) n'est pas son rôle : c'est `media-use`.
- **Chargé par** : `motion-producer` à la demande, **seulement si un brief ancien demande encore un mix dans la séquence** (depuis le 24/10/2026 les séquences ne portent que la voix, le mix se fait sur le film collé) ; `shorts-producer` à la demande. Cité par le skill `direction-sonore` (mise en œuvre dans la composition, rang 2 de l'ordre de préséance) et par `transitions-et-silences.md`.
- **À savoir** : rappel du projet (agents) : les valeurs d'automation sont **absolues** et remplacent `data-volume` ; `DIRECTION_AUDIO.md` cite sa source officielle ([S8]).

### vendor/claude-skills/hyperframes-cli
- **Fichiers** : 11 (`SKILL.md` ; `references/` 10 : `beats.md`, `cloud.md`, `cloudrun.md`, `compare-and-batch.md`, `doctor-browser.md`, `init-and-scaffold.md`, `lambda.md`, `lint-validate-inspect.md`, `preview-render.md`, `upgrade-info-misc.md`).
- **Rôle** : la boucle de développement par le **CLI** : `init`, `add`, `catalog`, `capture`, `lint`, `check`, `snapshot`, `compare`, `preview`, `play`, `beats`, `keyframes`, `render` (unique ou en lot), `publish`, `cloud`, `cloudrun`, `lambda`, `doctor`, `browser`, `upgrade`, `skills`, `transcribe`, `tts`, `remove-background`, `telemetry`… Conseille de lire la référence de la commande avant de la lancer. `validate`, `inspect` et `layout` sont des alias obsolètes de `check`.
- **Chargé par** : `motion-producer` (« check, snapshot, render ») et `shorts-producer`, à la demande.
- **À savoir** : le skill décrit des commandes que le garde-fou **refuse** (`publish`, `cloud`, `cloudrun`, `lambda`, `auth`, `upgrade`, `skills update`) ou **demande de confirmer** (`preview`) ; un rendu sans `--workers 1` ou `2` est lui aussi **refusé** ; sa fin décrit `usage --json`, commande absente de la 0.8.149. Le studio travaille avec `snapshot --describe false`, `check` et `render.sh` (`--workers 2`).

### vendor/claude-skills/hyperframes-core
- **Fichiers** : 11 (`SKILL.md` ; `references/` 10 : `minimal-composition.md`, `composition-patterns.md`, `data-attributes.md`, `tracks-and-clips.md`, `creator-editing-recipes.md`, `sub-compositions.md`, `variables-and-media.md`, `determinism-rules.md`, `full-screen-motion.md`, `tailwind.md`).
- **Rôle** : **le contrat technique** d'une composition : un fichier HTML dont le DOM déclare le temps par des attributs `data-*`, dont l'animation est « seekable » (pilotable à l'image près) et dont la lecture des médias appartient au framework. Couvre la structure, `class="clip"`, les pistes, les sous-compositions, les variables, le déterminisme (pas de `Math.random`, pas de `Date.now`…) et la validation. Règle d'or de l'en-tête : lire avant d'écrire du HTML de composition.
- **Chargé par** : `motion-producer` et `shorts-producer` (préchargé).
- **À savoir** : exige que `window.__timelines["id"]` corresponde au `data-composition-id` racine. Les règles du studio ajoutent : une seule composition racine par dossier (les autres dans `compositions/`, rendues avec `-c`) ; vidéo source à images clés espacées = elle se fige au rendu (réencoder avec `-g 15`).

### vendor/claude-skills/hyperframes-creative
- **Fichiers** : 79 (`SKILL.md` ; `frame-presets/` 48, `palettes/` 9, `references/` 16, `scripts/` 4, `templates/` 1).
- **Rôle** : direction créative **hors animation** : spécification de design (`frame.md` / `design.md`), palettes, typographie, narration, plan des plans (rythme), motifs de composition, décisions de marque et de style. Deux lectures obligatoires pour toute composition non triviale : `references/house-style.md` et `references/video-composition.md`.
- **Scripts** : `contrast-report.mjs` (avertissements de contraste sur des images rendues), `extract-audio-data.py` (bandes audio pour visuels réactifs), `package-loader.mjs`.
- **Chargé par** : `art-director` (préchargé).
- **À savoir** : ses palettes et préréglages sont des *défauts* ; dans le studio, la palette d'une histoire se décide en direction artistique avec une planche d'essai (`marque/README.md` de la chaîne) et les couleurs interdites de la chaîne (`marque/couleurs_interdites.json`, contrôlées par `controle.py couleurs`) priment.

### vendor/claude-skills/hyperframes-keyframes
- **Fichiers** : 3 (`SKILL.md`, `agents/openai.yaml`, `references/keyframe-patterns.md`).
- **Rôle** : mouvement par images clés « sûr à l'image près » : zoom, punch-in/out, recadrage, Ken Burns, mouvements de caméra, masques, tracés SVG, morphose, traînées de texte, profondeur 2D/3D, et diagnostics (`hyperframes keyframes`). Un contrat de poses : états visibles, identité du sujet continue, exécution « seek-safe », pixels vérifiés. Procédure en 5 étapes (sujet et états ; mécanisme le plus simple ; images clés ; vérification par `check`, `keyframes`, un `--shot` et des instantanés ; correction du plus petit échec).
- **Chargé par** : `motion-producer` et `shorts-producer` (préchargé). Le référentiel de réalisation (§ 2 quater) y renvoie pour la caméra, les masques, les tracés et la profondeur.
- **À savoir** : ne s'occupe pas du montage (couper, rogner, réordonner) : c'est `hyperframes-core`.

### vendor/claude-skills/hyperframes-registry
- **Fichiers** : 12 (`SKILL.md` ; `references/` 9 ; `examples/` 2).
- **Rôle** : chercher, installer et brancher les **blocs** (sous-compositions autonomes) et **composants** (extraits d'effet) du registre HyperFrames, par `hyperframes add` et `hyperframes catalog`. À consulter *avant* de construire à la main un effet nommé (scanlines, glitch, grain, etc.).
- **Chargé par** : aucun agent.
- **À savoir** : `hyperframes add` installe des éléments venus d'un registre externe : le contrat de production du studio dit « aucun `npm install` ni `hyperframes add` » (`skills/episode/references/production.md`). Ce skill est donc présent dans la copie mais **sans usage prévu**.

### vendor/claude-skills/hyperframes-studio
- **Fichiers** : 1 (`SKILL.md`).
- **Rôle** : conventions du **Studio** (l'éditeur de HyperFrames) : (0) *parler avant de construire* — un message qui nomme un changement le déclenche, une question reçoit une réponse sans modification, « ne change rien » interdit toute écriture ; (1) chaque scène est une sous-composition ; (2) une seule piste de sous-titres ; (3) un type d'élément par piste ; (4) zones de sécurité ; (5) nouveau film : plan, storyboard, ordre de construction.
- **Chargé par** : aucun agent.
- **À savoir** : conçu pour une personne qui travaille dans l'éditeur Studio, que le studio n'utilise pas (pas de `preview` sans demande). Sa règle « parler avant de construire » rejoint la règle du plugin « faire seulement ce qui est demandé ».

### vendor/claude-skills/media-use
- **Fichiers** : 110 (`SKILL.md`, `.gitignore` ; `audio/` 68, `references/` 10, `scripts/` 28, `luts/` 2).
- **Rôle** : « système d'exploitation des médias » d'un projet HyperFrames : **résoudre** (une commande `npx hyperframes media-use resolve --type <bgm|sfx|image|icon|logo|voice|grade|lut> --intent … --project <dir>`), **générer** par modèles de synthèse vocale, musique ou image quand le catalogue ne répond pas, **opérer** (couper, recadrer, transformer), **se souvenir** (réutilisation entre projets). Sert aussi à transcrire, produire des sous-titres, détourer, et à répondre aux retours visuels vagues (étalonnage, grain, rétro…).
- **Scripts** : `resolve.mjs`, `transcribe.mjs`, `transcript-cut.mjs`, `audio-duck.mjs`, `dither.mjs`, `recipe.mjs`, `prefs.mjs`, `eval.mjs`, plus des tests.
- **Chargé par** : `motion-producer` (« opérations sur les médias ») et `shorts-producer`, à la demande.
- **À savoir** :
  - le skill passe par le catalogue HeyGen et le CLI `heygen` (installation et connexion au premier usage : « install and sign in to the `heygen` CLI »). Le garde-fou refuse la connexion et le cloud HyperFrames (`hyperframes auth`, `login`, `cloud`…) mais n'a pas de règle propre à `media-use` ni au CLI `heygen` : à vérifier avant tout usage, et à ne faire qu'avec l'accord du propriétaire ;
  - `direction-sonore` précise : « `media-use` n'est pas une source de sons pour la chaîne » : ses effets fournis (whoosh, riser, glitch…) n'ont ni la provenance ni le registre voulus ; les sons viennent de `marque/son/` ;
  - ses images de catalogue ne respectent pas la règle des médias du studio (réels, sous licence libre, provenance consignée).

## vendor/roast-room (0.4.0)
- **D'où** : https://github.com/nateherkai/roast-room, commit `e40f406`, copié le 02/11/2026 sans modification. **Licence** : MIT (`vendor/roast-room/LICENSE`, © 2026 AI Automation Society).
- **Contenu** (118 fichiers : 117 copiés et le `README.md` ajouté ; environ 1,5 Mo) : le protocole du Chair (`SKILL.md`), `roster.json`, `references/`, les cerveaux des 12 sièges (`brains/`), leurs consignes (`seats/council-<clé>.md`, venues de `.claude/agents/`), `scripts/check_quotes.py`. Correspondance des chemins : `vendor/roast-room/README.md`.
- **Non copié** : la salle visuelle (`app/`), le skill `newroaster` (il télécharge des vidéos pour bâtir un siège), la session d'exemple.
- **Ce n'est ni un skill ni un agent du plugin** : rien ne se charge au démarrage. Seul `strategist` le lit, en phase `conseil` ; les sièges n'existent pas comme agents (un sous-agent ne peut pas en lancer d'autres).

## Qui charge quoi
| Agent | Préchargés (champ `skills:`) | À la demande (outil Skill) |
|---|---|---|
| `motion-producer` | `hyperframes-core`, `hyperframes-keyframes`, `hyperframes-animation` (WAAPI et CSS seulement) | `studio-faceless:direction-sonore`, `hyperframes-cli`, `hyperframes-audio` (brief ancien), `media-use` |
| `shorts-producer` | `studio-faceless:shorts`, `hyperframes-core`, `hyperframes-keyframes` | `hyperframes-cli`, `hyperframes-animation`, `hyperframes-audio`, `media-use`, `studio-faceless:direction-sonore` |
| `art-director` | `hyperframes-creative`, `hyperframes-animation`, `studio-faceless:thumbnail-strategist` | `studio-faceless:direction-sonore` ; « jamais les dix ensemble » |
| `research`, `reviewer`, `studio-maintainer`, `strategist` | aucun | — (`strategist` lit `vendor/roast-room/` avec Read, pas comme skill) |

Précisions : ce tableau reprend le champ `skills:` de l'en-tête de chaque définition dans `agents/` et les phrases « Skills » de leur corps. Un plugin ignore les champs `hooks`, `mcpServers` et `permissionMode` des en-têtes d'agent ([`../ARCHITECTURE.md`](../ARCHITECTURE.md)) ; que `skills:` soit honoré tel quel pour des skills d'utilisateur sans préfixe est **à vérifier** à la première session. Pas d'entretien d'intention ni de routage « création » du skill `hyperframes` pour les producteurs. Détail des agents : [`agents.md`](agents.md).

## Où ces skills s'installent et comment les faire évoluer
- **Installation** (une fois par machine) : cloner le dépôt, puis copier chaque dossier de `plugins/studio-faceless/vendor/claude-skills/` dans `~/.claude/skills/`, **sans écraser** un dossier existant (`INSTALLATION.md`, section 3). Exemple en Git Bash (non fourni par le dépôt) : `cp -rn plugins/studio-faceless/vendor/claude-skills/<skill> ~/.claude/skills/`. Voir [`../workflows/installation-et-mise-a-jour.md`](../workflows/installation-et-mise-a-jour.md).
- **Mise à jour** : jamais seule. Elle suit une montée de version de HyperFrames **décidée par le propriétaire** : nouvelle copie datée, `README.md` du dossier mis à jour, nouvelle version du plugin (`CHANGELOG.md`). Autres endroits à mettre à jour en même temps : [`../workflows/faire-evoluer-le-plugin.md`](../workflows/faire-evoluer-le-plugin.md), section « Monter la version de HyperFrames ».
- **Garde-fou** : `hyperframes skills update`, `skills install`, `skills add` et `npx hyperframes@…` sont refusés (`hooks/garde_commandes.py`).

## Points à vérifier et tensions avec les règles du studio
- **Pas de fichier de licence** : `vendor/claude-skills/README.md` annonce la licence Apache-2.0, mais ni le dossier ni les dix skills ne contiennent de `LICENSE` ni de `NOTICE` (recherche faite sur le dépôt). Apache-2.0 demande de joindre le texte de la licence à une redistribution : à vérifier avec le propriétaire (dépôt privé, usage personnel).
- **Copie « sans modification »** : le dépôt ne conserve pas d'empreintes de cette copie (contrairement à `skills/humanizer/PROVENANCE.md`). Impossible de prouver ici l'identité avec `~/.claude/skills/` ; à vérifier si besoin.
- **Instructions obsolètes pour le studio** : les `SKILL.md` décrivent des commandes (`usage`, `upgrade --check`, `skills update`, `cloud`, `publish`, `heygen` connecté) que les règles du studio ignorent ou que le garde-fou refuse. La règle du studio fait foi (`REGLES_STUDIO.md` § Moteur et outils).
- **GSAP par défaut** dans `hyperframes-animation`, `hyperframes-core` et `hyperframes-keyframes` (squelette « GSAP Skeleton »), alors que le studio impose WAAPI et CSS seulement pour le producteur (`agents/motion-producer.md`) : l'agent doit n'en tirer que les parties WAAPI/CSS.
- **Version du CLI** : tous les chemins du plugin supposent la 0.8.149 ; une montée de version (décision du propriétaire) impose de refaire la copie.
