# Skills annexes du plugin

Cette page décrit les neuf skills « annexes » de `plugins/studio-faceless/skills/` : `grilling`, `grill-me`, `humanizer`, `javascript-animation`, `soundtrack`, `find-skills`, `elevenlabs-sound-effects`, `elevenlabs-music`, `frontend-design`. Les skills de métier (`episode`, `shorts`, `thumbnail-strategist`, `youtube-seo`, `direction-sonore`, `regarder`) sont décrits dans [`skill-episode.md`](skill-episode.md), [`publication.md`](publication.md) et [`son.md`](son.md).

## Table des matières
- [Vue d'ensemble](#vue-densemble)
- [grilling](#grilling) : [SKILL.md](#skillsgrillingskillmd)
- [grill-me](#grill-me) : [SKILL.md](#skillsgrill-meskillmd)
- [humanizer](#humanizer) : [SKILL.md](#skillshumanizerskillmd), [PROVENANCE.md](#skillshumanizerprovenancemd), [LICENSE](#skillshumanizerlicense)
- [javascript-animation](#javascript-animation) : [SKILL.md](#skillsjavascript-animationskillmd), [PROVENANCE.md](#skillsjavascript-animationprovenancemd), [LICENSE](#skillsjavascript-animationlicense), [scripts](#scripts-de-javascript-animation), [templates](#skillsjavascript-animationtemplatesstarterhtml), [références](#références-de-javascript-animation)
- [soundtrack](#soundtrack) : [SKILL.md](#skillssoundtrackskillmd), [LICENSE](#skillssoundtracklicense), [références](#skillssoundtrackreferencesai-musicmd), [script](#skillssoundtrackscriptssync-checkmjs), [templates](#templates-de-soundtrack)
- [find-skills](#find-skills) : [SKILL.md](#skillsfind-skillsskillmd), [PROVENANCE.md](#skillsfind-skillsprovenancemd), [LICENSE](#skillsfind-skillslicense)
- [elevenlabs-sound-effects et elevenlabs-music](#elevenlabs-sound-effects-et-elevenlabs-music)
- [frontend-design](#frontend-design) : [SKILL.md](#skillsfrontend-designskillmd), [PROVENANCE.md](#skillsfrontend-designprovenancemd), [LICENSE.txt](#skillsfrontend-designlicensetxt)
- [Points à vérifier et incohérences](#points-à-vérifier-et-incohérences)

## Vue d'ensemble
| Skill | Origine | Licence | Statut | Qui l'appelle |
|---|---|---|---|---|
| `studio-faceless:grilling` | écrit pour le studio | — | en service | Claude principal, à chaque **porte** du skill `episode` et à la création d'une chaîne |
| `studio-faceless:grill-me` | écrit pour le studio | — | en service | le **propriétaire** seul (`disable-model-invocation`) ; il renvoie à `grilling` |
| `studio-faceless:humanizer` | blader/humanizer v3.1.0 (Siqi Chen), copie du 28/10/2026 | MIT | `PROPOSÉ` (essai sur un script d'AA) | le **propriétaire** seul, avec `/humanizer` (appel automatique bloqué depuis la 0.2.2) |
| `studio-faceless:javascript-animation` | iart.ai v0.4.1, intégré le 14/10/2026 | MIT | intégré sur demande du propriétaire d'AA | le **propriétaire** seul, avec `/javascript-animation`, quand il veut une animation dessinée en code (appel automatique bloqué depuis la 0.2.2) |
| `studio-faceless:soundtrack` | iart.ai v0.4.1, intégré le 14/10/2026 | MIT | idem | idem, avec `/soundtrack` (appel automatique bloqué depuis la 0.2.2) |
| `studio-faceless:find-skills` | vercel-labs/skills, commit `773fb2c`, copie du 29/10/2026 avec une section « Règles du studio » | MIT | `VALIDÉ` (Hicham, 29/10/2026) | le **propriétaire** seul, avec `/find-skills`, quand il cherche un skill (appel automatique bloqué depuis la 0.2.2) |
| `studio-faceless:elevenlabs-sound-effects` | elevenlabs/skills `sound-effects`, commit `503d4e9`, copie du 29/10/2026 avec une section « Règles du studio » | MIT | `VALIDÉ` (Hicham, 29/10/2026) | le **propriétaire** avec `/elevenlabs-sound-effects`, ou Claude qui lit le `SKILL.md` quand il demande une génération, son par son, coût annoncé avant (appel automatique bloqué depuis la 0.2.2) |
| `studio-faceless:elevenlabs-music` | elevenlabs/skills `music`, même commit et même traitement | MIT | idem | idem |
| `studio-faceless:frontend-design` | anthropics/skills `frontend-design`, commit `ca45fc4`, copie du 29/10/2026 avec une section « Règles du studio » | Apache 2.0 | `VALIDÉ` (Hicham, 29/10/2026) | Claude principal et les producteurs, pour les planches de direction artistique et les compositions |

**Depuis la 0.2.2**, six de ces skills portent `disable-model-invocation: true` (`humanizer`, `find-skills`, `javascript-animation`, `soundtrack`, `elevenlabs-music`, `elevenlabs-sound-effects`) : leur description n'est plus dans la liste proposée à Claude au démarrage (environ 480 tokens de moins, estimation de `claude plugin details`), et Claude ne les appelle plus par l'outil Skill. Le propriétaire les appelle avec `/nom`, ou Claude lit leur `SKILL.md` quand il le demande. Vérifié avant le réglage : aucun fichier du plugin ne les précharge ni ne demande de les invoquer ; un renvoi de `javascript-animation` vers `soundtrack` a été reformulé.

Aucun agent du plugin ne précharge un de ces skills (champ `skills:` des agents : voir [`agents.md`](agents.md)). Seul `grilling` est cité ailleurs dans le plugin (`REGLES_STUDIO.md`, `skills/episode/`) ; `grill-me` ne l'est que dans `README.md` et `CHANGELOG.md`, et `humanizer`, `javascript-animation`, `soundtrack`, `find-skills`, `elevenlabs-sound-effects`, `elevenlabs-music` ne sont cités que dans leurs propres dossiers (`find-skills` est aussi nommé dans la provenance de `humanizer`).

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
- **Liens** : appelé par `grill-me`. Les réponses d'une porte s'écrivent au `BRIEF.md` de l'épisode, avec leur date (`grilles.md`).
- **À savoir** : en-tête `name: grilling`, `description` seulement (pas de `disable-model-invocation`) : Claude peut l'appeler seul. Les réponses recommandées ne valent pas décision : seul le propriétaire valide.

## grill-me

### skills/grill-me/SKILL.md
- **Rôle** : raccourci utilisateur vers `grilling`.
- **Quand il sert** : quand le propriétaire écrit lui-même la commande du skill pour être « cuisiné » sur un plan ou une idée, hors parcours d'épisode.
- **Contenu** : 7 lignes. En-tête : `name: grill-me`, `description: A relentless interview to sharpen a plan or design.`, `disable-model-invocation: true` (Claude ne peut pas l'appeler de lui-même). Corps : « Call the Skill tool with "studio-faceless:grilling". »
- **Liens** : `skills/grilling/SKILL.md`.
- **À savoir** : n'a aucune logique propre ; tout passe par `grilling`.

## humanizer

### skills/humanizer/SKILL.md
- **Rôle** : réécrire un texte qui sonne « écrit par IA » pour qu'il sonne comme son auteur, **sans changer ce qu'il dit** et sans rien inventer. Copie fidèle de blader/humanizer v3.1.0 (32 348 octets, 397 lignes, MIT, auteur Siqi Chen).
- **Quand il sert** : Claude principal, sur la **narration anglaise** d'un script, après le script v1 et avant les contrôles de densité. Usage décidé sur AA en essai (28/10/2026) ; voir `PROVENANCE.md`.
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

## javascript-animation

### skills/javascript-animation/SKILL.md
- **Rôle** : faire de courts films animés dont **chaque image est dessinée en code JavaScript** (canvas), sans image ni police externes, et les rendre en MP4 avec un autocontrôle. Skill d'iart.ai, v0.4.1, MIT.
- **Quand il sert** : **seulement si le propriétaire demande** une animation dessinée en code (la description le dit). Pas pour des graphiques de données ni de la 3D. Pas appelé par les agents ni par le skill `episode`.
- **Contenu** (84 lignes, en anglais) :
  - **Encadré « Adaptation studio-faceless » (ajout local du 14/10/2026, prioritaire)** : le `CLAUDE.md` de la chaîne, les référentiels et `direction/ECARTS.md` font foi ; rendu par HyperFrames 0.8.149 (un `<canvas>` redessiné à chaque `hf-seek`, vérifié le 14/10/2026) ; `render.mjs` et `layout-check.mjs` exigent `playwright-core`, **non installé** (ne pas l'installer sans décision) ; **pas d'« image zéro » obligatoire** (photos sourcées et polices de la chaîne permises) ; toute fiction dessinée est déclarée « Dramatized scene » ; pour une reconstitution réaliste, ni trait tremblé ni « line boil ».
  - **Modèle** : testé avec Claude Opus 5.5 ; l'autocontrôle exige de voir les images (sinon dire que la vérification visuelle n'est pas faite).
  - **Flux par défaut** (6 étapes, sans s'arrêter pour demander) : lire le brief ; planifier le look et le son depuis le sujet ; grille de temps, storyboard et blocage **comme des données** (`BPM`, `SECTIONS`, `SHOTS`, `EVENTS`) ; construire depuis `templates/starter.html` ; autocontrôle puis rendu ; livrer le MP4 et le HTML.
  - **Autocontrôle** : les six commandes (voir scripts) puis deux passes à l'œil (conformité au storyboard ; passe de réalisateur sur la planche à 2 images par seconde, deux tours au moins).
  - **Seulement si déclenché** : personnage dans plusieurs scènes, photos fournies, texte qui suit un personnage, texte non latin, page publiée.
  - **Règles qui évitent les échecs courants** : fonction pure du temps ; le trait « bout » et ne tremble pas (nouvelle graine toutes les 4 images) ; formes arrondies pour les corps ; choisir l'angle qui fait lire la pose ; dessiner de l'arrière vers l'avant ; points d'impact sur chaque coupe ; le texte ne doit jamais se chevaucher.
  - **Fichiers** : liste des références, scripts et modèle.
  - **Prérequis** (dernière ligne) : Node 18+, ffmpeg, Chrome (ou `npx playwright install chromium`), et `npm i playwright-core` dans le dossier où l'on lance les scripts.
- **Liens** : `soundtrack` (musique, vérification de synchro), `PROVENANCE.md`, `LICENSE`, `REFERENTIEL_QUALITE_REALISATION.md` et `DIRECTION_AUDIO.md` (font foi en cas d'écart).
- **À savoir** :
  - **les scripts `render.mjs`, `layout-check.mjs` et le contrôle dynamique d'`asset-audit.mjs` ne tournent pas aujourd'hui** : `playwright-core` n'est pas installé et le garde-fou refuse `npm install` (installation à décider par le propriétaire) ;
  - le texte des commandes d'autocontrôle (`node scripts/…`) se lance depuis le dossier du skill ; dans le plugin installé, écrire le chemin complet `${CLAUDE_PLUGIN_ROOT}/skills/javascript-animation/scripts/…` ;
  - la mention `outils/capture.sh` « du projet » (encadré d'adaptation, ligne 14) renvoie à un outil qui n'est pas dans le plugin (aucun `capture*` sous `plugins/studio-faceless/`, hors `vendor/`) : à vérifier.

### skills/javascript-animation/PROVENANCE.md
- **Rôle** : provenance **commune** de `javascript-animation` et de `soundtrack`.
- **Contenu** : source `iart-ai/javascript-animation-skills` (iart.ai), branche `main`, v0.4.1 (dépôt créé le 23/09/2026, dernier envoi le 30/09/2026) ; licence MIT « Copyright (c) 2026 iart.ai » ; intégration le 14/10/2026 sur AA, demandée puis validée par le propriétaire (le contrôle de sécurité automatique avait d'abord refusé la copie) ; fichiers copiés : `SKILL.md`, `references/`, `scripts/`, `templates/` des deux skills (exemples, GIF et manifeste de plugin non copiés) ; tous les fichiers lus avant l'intégration, aucun appel réseau dans les modèles ; seul `references/ai-music.md` décrit un service payant (exclu) ; modifications locales : un encadré « Adaptation studio-faceless » en tête de chaque `SKILL.md`.
- **À savoir** : ne donne pas d'empreintes de fichiers (contrairement à `humanizer`).

### skills/javascript-animation/LICENSE
- **Rôle** : licence MIT, « Copyright (c) 2026 iart.ai ». Un `LICENSE` identique existe dans `skills/soundtrack/`.

### Scripts de javascript-animation
Tous en JavaScript (modules ES), à lancer avec Node depuis le dossier de travail. Dépendances communes : `playwright-core` (**non installé**), Chrome (essaie `channel: 'chrome'`, sinon le Chromium de Playwright), FFmpeg. La résolution de `playwright-core` se fait depuis le dossier du skill, sinon depuis le dossier courant. Sans lui : erreur « playwright-core not found: run `npm i playwright-core` in this folder ».

#### skills/javascript-animation/scripts/render.mjs
- **Rôle** : rendre une page-animation en MP4, en images fixes ou en planche contact.
- **Quand il sert** : autocontrôle et rendu final (flux de `SKILL.md`).
- **Contrat de la page** : doit définir `window.draw(frame)`, `window.FRAMES`, `window.FPS` ; en option `window.CUES` (secondes des coupes/points d'impact) et `window.SCORE = ac => {…}` (partition Web Audio). La page est chargée avec `?render`.
- **Usage** (depuis le dossier de travail, Node ≥ 18) :
  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/skills/javascript-animation/scripts/render.mjs" page.html out.mp4
  node ".../render.mjs" page.html shot --stills 0,150,300      # ou en secondes : 2.5s,7s
  node ".../render.mjs" page.html sheet.jpg --sheet [N]        # une image toutes les N s (1 par défaut)
  ```
  | Mode | Option | Sortie |
  |---|---|---|
  | rendu complet | aucune | `out.mp4` (H.264 yuv420p, crf 18, `+faststart`) ; extension absente → `.mp4` ; **taille de canvas paire exigée** ; écrit `<out>.cues.json` si `CUES` ; si `SCORE` : rendu hors ligne en `<out>.wav` (48 kHz, stéréo 16 bits, crête à 0,89) mixé en AAC 192 k dans le MP4 ; sans `SCORE`, MP4 muet |
  | images fixes | `--stills f1,f2` | `<out>-NNNN.jpg` par image (numéro d'image, ou temps avec suffixe `s`) |
  | planche | `--sheet [secondes]` | une image JPEG : une capture toutes les N s, décalée d'une demi-pas et écartée des coupes (`CUES`), horodatée dans le navigateur, vignettes de 360 px assemblées par FFmpeg (`tile`) |
- **Fichiers lus / écrits** : lit la page ; écrit les sorties ci-dessus ; dossier temporaire `sheet-…` dans le temp du système (supprimé après la planche).
- **Codes de sortie** : 0 ; 1 si arguments manquants, page sans `draw/FRAMES/FPS`, canvas de taille impaire, ou échec FFmpeg (sortie incomplète). Les erreurs de la page sont affichées en avertissement.
- **À savoir** : le mode `--sheet`/`--stills` n'écrit pas dans le dossier du plugin ; pour le plugin installé, écrire les sorties dans le projet.

#### skills/javascript-animation/scripts/asset-audit.mjs
- **Rôle** : prouver qu'une page est « zéro asset » (rien de chargé ni d'embarqué).
- **Usage** : `node ".../asset-audit.mjs" page.html`.
- **Fonctionnement** : (1) analyse statique par 13 motifs : balises `<img>`, médias/embeds, `<link>` externes, `<script src>`, URI `data:`, `url(…)` CSS, `@import`, `@font-face`, appels réseau, `new Image/Audio/FontFace`, `import()` dynamique, références à des fichiers, longs blobs base64 ; (2) contrôle dynamique : charge la page et note toute requête autre que la page elle-même (1,5 s d'attente). Le contrôle dynamique est **sauté** (avertissement) si `playwright-core` manque : seul le statique tourne.
- **Sortie / code** : `CLEAN: <fichier> (<ko> KB) embeds and loads nothing…` et code 0 ; sinon liste « line N: … » et « network request: … », puis `NOT zero-asset`, code 1.
- **À savoir** : l'encadré d'adaptation précise que, dans le studio, le zéro-asset n'est pas obligatoire (photos sourcées permises) : l'audit sert alors à savoir ce qui est chargé.

#### skills/javascript-animation/scripts/layout-check.mjs
- **Rôle** : trouver le texte qui chevauche un autre texte ou un objet clé.
- **Usage** : `node ".../layout-check.mjs" page.html [--every 0.1] [--min 4]` (`--every` = pas d'échantillonnage en secondes, 0,1 par défaut ; `--min` = chevauchement minimal ignoré en pixels, 4 par défaut).
- **Contrat de la page** : enregistre ses boîtes pendant le dessin dans `window.LAYOUT` (`[{id, kind: 'text'|'keep', x, y, w, h}]`), via `claim()` du modèle. Signale texte contre texte (tout chevauchement) et texte contre objet « keep » partiellement chevauché (un texte entièrement dedans est admis).
- **Sortie / code** : `CLEAN: no text collisions in N sampled frames…` (0) ; sinon une ligne `a × b: <intervalles de temps>` par collision et le décompte (1). Si la page n'expose pas `window.LAYOUT` : message d'erreur, code 1.

### skills/javascript-animation/templates/starter.html
- **Rôle** : modèle de page-animation (310 lignes) : bibliothèque de dessin et squelette piloté par le storyboard. Les valeurs (palette grise, démo) sont des **emplacements à remplacer**, pas un style de maison.
- **Contenu** :
  - **Contrat** : `draw(frame)` est une fonction pure du numéro d'image ; jamais `Math.random` ni `Date` (utiliser `rng(seed)` / `hash2()`) ;
  - constantes `W`, `H`, `FPS`, `DUR`, `FRAMES` et objet `LOOK` (fond, police, tremblement…) ;
  - mathématiques : `hash2`, `vnoise`, `rng` ;
  - primitives « main levée » : `jit`, `resample`, `tracePath`, `ink`, `fill`, `hatch`, `withShadow`, `label`, `note`, `drawOn` ;
  - primitives « illustration » : `shape`, `blush` ; primitives « flat/blueprint » : `flatMass`, `guide`, `glow` ;
  - caméra et mise en page : `withCamera`, `claim`, `placeFree` ;
  - papier et calques filtrés : `drawLayer` ;
  - **storyboard** : `BPM`, `SECTIONS`, `SHOTS`, `BOX` (blocage), `EVENTS` ; `world(t)` ; `window.draw`, `window.FRAMES`, `window.FPS`, `window.CUES`.
  - Une aide intégrée indique de coller `soundtrack/templates/groove.js` pour la partition.
- **À savoir** : le canvas fait 1920 × 1080 par défaut ; le canvas doit rester de taille paire pour le MP4.

### Références de javascript-animation
Cinq fichiers en anglais, lus à la demande par le skill.

#### skills/javascript-animation/references/character.md
- **Rôle** : n'est lu que si un personnage apparaît dans plusieurs scènes. Concevoir le personnage **seul** d'abord (toutes expressions et poses sur une planche, `--stills 0`), le coder comme une fonction avec options, définir des **points d'ancrage** (bouche, mains), construire un personnage à partir de photos fournies (elles restent locales), poses qui se lisent. 32 lignes.

#### skills/javascript-animation/references/forms.md
- **Rôle** : notes de structure par forme (récit, explication, poème/ambiance, boucle, page interactive) : durée de plan, nombre de plans, comment finir. À adapter au sujet. 35 lignes.

#### skills/javascript-animation/references/qc.md
- **Rôle** : liste d'autocontrôle avant livraison. Scripts d'abord (`asset-audit` et `layout-check` propres, `sync-check` réussi), puis sections Images, Formes et figures, Conformité au storyboard, Mise en scène, Passe de réalisateur (planche à 2 images/s), Mouvement, Faits et fichiers. 53 lignes.

#### skills/javascript-animation/references/storyboard.md
- **Rôle** : grille de temps, liste de plans, blocage (un monde, plusieurs caméras), logique du récit, événements, vérification de l'image contre le storyboard. À écrire **avant** tout code de dessin ; livré avec le film (`storyboard.md`) mais sans demander l'accord de l'utilisateur. 62 lignes.

#### skills/javascript-animation/references/techniques.md
- **Rôle** : sept techniques de dessin (trait d'encre, formes d'illustration, impression à teinte plate/risographie, gravure au trait continu, mots comme forme, remplissage feutre/gouache, plat cinématique + plan technique), avec un **tableau de maturité** : 1, 2 et 7 « utilisées dans un film entier » ; 3 à 6 « rendent correctement en image fixe, jamais utilisées dans un film entier ». Contient aussi « Dériver le style du sujet », « Pas de style de maison », « Profondeur sans 3D », « Pièges du canvas » et les briques de mouvement du modèle. 163 lignes.
- **À savoir** : le tableau demande d'être honnête avec l'utilisateur sur la maturité de chaque technique.

## soundtrack

### skills/soundtrack/SKILL.md
- **Rôle** : bande-son **synthétisée en code** (Web Audio, rendue hors ligne en WAV) pour une animation canvas, ou mise en phase d'une musique donnée avec les coupes, avec contrôle des coupes sur le temps et des sauts de volume. Skill d'iart.ai, v0.4.1, MIT.
- **Quand il sert** : **seulement si le propriétaire demande** une musique faite en code ou ce contrôle de synchro, en complément de `javascript-animation`.
- **Contenu** (51 lignes, en anglais) :
  - **Encadré « Adaptation studio-faceless » (14/10/2026, prioritaire)** : `DIRECTION_AUDIO.md` et le skill `direction-sonore` font foi ; musique facultative, choisie par le propriétaire ; aucune musique superposée sans demande ; une musique synthétisée se livre en stem séparé et se déclare comme son construit ; `references/ai-music.md` exclu sans décision ; `sync-check.mjs` n'utilise que FFmpeg et FFprobe ; HyperFrames ne capture pas Web Audio : le score se rend hors ligne (WAV) puis se place comme `<audio>`.
  - **Écrire le son pour ce film** : chaque film a sa propre partition dans `window.SCORE = ac => {…}` ; `groove.js` et `score.js` ne servent que sur demande.
  - **Comment la musique suit l'image** : carte de tempo (un nombre entier de mesures par scène), marquer les coupes par l'harmonie plutôt que le volume (un saut de +7 à +10 dB sonne comme un sursaut ; +3 à +5 dB avec changement d'accord passe), pas d'accent en plus sur le temps fort de la coupe, couches qui entrent une ou deux par mesure, silence d'une mesure avant le point fort.
  - **Autres sources** : musique par IA (Lyria via OpenRouter) ; la piste de l'utilisateur (mux FFmpeg) ; avec une musique imposée, c'est l'image qui suit la musique.
  - **Toujours vérifier** : `sync-check.mjs`.
  - **Limites** : boîte à musique, pianos pincés, nappes, cloches, percussions douces conviennent ; voix réalistes, orchestres, production de genre non (utiliser de la musique IA ou une vraie piste).
- **Liens** : `skills/javascript-animation/` (`render.mjs` rend `window.SCORE`), `LICENSE`, `../javascript-animation/PROVENANCE.md`.
- **À savoir** : pas de `PROVENANCE.md` propre : celle de `javascript-animation` couvre les deux. Pour la musique des vidéos du studio, la source est la bibliothèque `marque/son/` de la chaîne (voir [`son.md`](son.md)), pas ce skill.

### skills/soundtrack/LICENSE
- **Rôle** : licence MIT, « Copyright (c) 2026 iart.ai » (même texte que celui de `javascript-animation`).

### skills/soundtrack/references/ai-music.md
- **Rôle** : recette de musique générée par IA (Lyria 3 via OpenRouter, flux base64 décodé par un script Python) puis mixage sous l'image par FFmpeg, et réalignement de l'image sur la musique avec `sync-check`.
- **Quand il sert** : jamais par défaut. **Exclu** par l'encadré d'adaptation : il demande une clé d'API (`OPENROUTER_API_KEY`) et des frais, donc une décision du propriétaire.
- **À savoir** : il contient une commande `curl` vers un service externe ; le garde-fou n'a pas de règle propre à OpenRouter. Les règles du studio (aucun achat, ElevenLabs avec accord) s'appliquent.

### skills/soundtrack/scripts/sync-check.mjs
- **Rôle** : vérifier que la bande-son tombe sur l'image sans surprendre.
- **Usage** (Node, FFmpeg et FFprobe seulement, **pas de playwright**) :
  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/skills/soundtrack/scripts/sync-check.mjs" video.mp4 [--cues-file anim.cues.json] [--tol 100]
  ```
  | Option | Effet |
  |---|---|
  | `--cues-file` | contrôle les temps déclarés (coupes + points d'impact) au lieu de détecter les coupes dans l'image |
  | `--tol` | tolérance en millisecondes (100 par défaut, environ 3 images) |
- **Fonctionnement** : cherche les événements visuels (coupes en creux de détail, coupes sèches par pics de mouvement) sur des images grises de 64 × 64 ; cherche les attaques audio ; pour chaque événement, affiche le décalage avec l'attaque forte la plus proche et le saut de volume. Échoue sur `OFF-BEAT` (> tolérance) ou `STARTLE` (> +6 dB par rapport à la seconde d'avant). La première seconde et le fondu final sont ignorés ; une coupe vers le silence compte comme posée.
- **Sortie / code** : tableau « événement · attaque la plus proche · décalage · saut · verdict » puis `N/M … land within ±X ms … without a startle` ; **code 0** si tout est posé, **1** sinon ou si la vidéo n'a aucune piste audio.

### Templates de soundtrack
#### skills/soundtrack/templates/groove.js
- **Rôle** : partition « groove » prête à coller dans la page : grille de temps avec sections, un break, et un son synthétisé pour chaque action.
- **Usage** : coller dans le `<script>` de la page avant le bloc de prévisualisation, puis `window.SCORE = ac => buildGroove(ac, { dur: DUR, bpm: BPM, sections: SECTIONS, events: EVENTS });`.
- **Options** : `sections` = `[[mesureDébut, mesureFin, couches]]` avec les couches `pad`, `padSoft`, `kick2`, `kick4`, `hat8`, `hat16`, `clap`, `bassHalf`, `bass8`, `lead`, `pluck`, `crash` (une section sans couche = silence, les effets jouent) ; `events` = `[[secondes, nomEffet, arg?]]` ; `kit` = `electro`, `acoustic`, `keys` ou `percussion` ; `harmony` = `bright`, `wistful`, `dreamy`, `tense`, `folk`, `blues` ou des accords perso ; `key` (transposition), `gain`, `sfxGain`, `bpm`. Une erreur est levée pour un effet inconnu.
- **Effets disponibles** (table `FX`) : `click`, `clack`, `switch`, `whooshIn`, `whooshOut`, `whoosh`, `boing`, `clank`, `ding`, `pop`, `popLow`, `tick`, `swish`, `thud`, `clonk`, `creak`, `blip`, `zip`, `flag`, `alarm`, `step`, `notify`, `drip`.
- **À savoir** : règle apprise : faire entrer les couches une ou deux par mesure (kick + basse ensemble après une intro calme : +11 dB, à éviter). Réverbération et bruit à graine fixe : le rendu est identique à chaque fois.

#### skills/soundtrack/templates/score.js
- **Rôle** : partition de musique de fond **pilotée par l'image** : une carte de tempo donne à chaque scène un nombre entier de mesures, chaque scène revient à la dominante pour que la coupe tombe sur la tonique (le montage est marqué par l'harmonie, pas le volume).
- **Usage** : coller dans la page, puis `window.SCORE = ac => buildScore(ac, { dur: DUR, cues: window.CUES });`.
- **Options** : `bar` (durée cible d'une mesure en s, 2,67 ≈ 90 bpm), `key`, `tail` (accord final résolutif, s), `gain`, `chime` (cloche discrète à chaque coupe).
- **À savoir** : sans échantillon ni bibliothèque ; réverbération par impulsion générée à graine fixe.

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

## Points à vérifier et incohérences
- **`skills/javascript-animation/SKILL.md:84`** demande `npm i playwright-core`, alors que le garde-fou refuse `npm install` : ces scripts sont inutilisables tant que le propriétaire n'a pas décidé (voir aussi l'encadré `:11`).
- **`skills/javascript-animation/SKILL.md:14`** cite `outils/capture.sh` « du projet » : il n'existe pas dans `plugins/studio-faceless/outils/` (à vérifier : outil de StudioV1 non repris, ou à fournir par la chaîne).
- **`skills/humanizer/SKILL.md`** n'est cité par aucun autre fichier du plugin (ni l'étape « script » de `skills/episode/`) : son usage reste un essai d'AA, et depuis la 0.2.3 seul le propriétaire l'appelle (`/humanizer`).
- **`skills/javascript-animation/SKILL.md`** et **`skills/soundtrack/SKILL.md`** : texte en anglais avec un encadré en français ; en-tête `version: 0.4.1` (propre à l'amont).
- `README.md` (racine) range `humanizer`, `javascript-animation` et `soundtrack` parmi les skills MIT ; les trois licences sont bien présentes, dont deux identiques (`javascript-animation`, `soundtrack`).
