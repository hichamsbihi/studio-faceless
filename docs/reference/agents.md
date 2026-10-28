# Référence : les agents du plugin (`agents/`)

Ce document décrit les cinq agents du plugin `studio-faceless` : leur en-tête, ce qu'ils lisent, ce qu'ils écrivent, ce que le garde-fou leur interdit, ce qu'ils livrent et qui les appelle. Les fichiers de `agents/` font foi ; en cas d'écart, la documentation se corrige.

## Table des matières
- [Vue d'ensemble](#vue-densemble)
- [Tableau comparatif](#tableau-comparatif)
- [Garde-fou : ce qui est imposé et ce qui repose sur la consigne](#garde-fou--ce-qui-est-imposé-et-ce-qui-repose-sur-la-consigne)
- [Fiches](#fiches)
  - [agents/research.md](#agentsresearchmd)
  - [agents/art-director.md](#agentsart-directormd)
  - [agents/motion-producer.md](#agentsmotion-producermd)
  - [agents/shorts-producer.md](#agentsshorts-producermd)
  - [agents/studio-maintainer.md](#agentsstudio-maintainermd)
- [Écarts et points à vérifier relevés dans ces fichiers](#écarts-et-points-à-vérifier-relevés-dans-ces-fichiers)

## Vue d'ensemble
- **Un agent est un sous-agent de Claude principal** (le Studio Director). Il est lancé par le Studio Director avec un **contrat de mission** (neuf champs, modèle : [`templates/CONTRAT_MISSION.template.md`](templates.md#templatescontrat_missiontemplatemd)). Les agents ne se délèguent rien entre eux (`REGLES_STUDIO.md`, « Sous-agents »).
- **Noms** : une fois le plugin installé, chaque agent prend le préfixe du plugin : `studio-faceless:research`, `studio-faceless:art-director`, `studio-faceless:motion-producer`, `studio-faceless:shorts-producer`, `studio-faceless:studio-maintainer`. Le champ `name:` de l'en-tête garde le nom court ([`../ARCHITECTURE.md`](../ARCHITECTURE.md), « Noms »).
- **En-tête** : chaque fichier commence par un en-tête YAML : `name`, `description` (ce que Claude lit pour décider de déléguer), `tools`, `model`, `color`, et `skills` (skills préchargés dans le contexte de l'agent, quand il y en a).
- **Un plugin ignore les champs `hooks`, `mcpServers` et `permissionMode`** de l'en-tête de ses agents ([`../ARCHITECTURE.md`](../ARCHITECTURE.md), « Garde-fou »). Les limites par rôle viennent donc du hook du plugin (`hooks/garde_commandes.py`), qui reconnaît le rôle au champ `agent_type` : voir le tableau `ROLES` plus bas.
- **Skills préchargés** : `hyperframes-*` sont des skills d'utilisateur (copiés dans `~/.claude/skills/`, voir [`vendor.md`](vendor.md)), sans préfixe ; `studio-faceless:…` sont les skills du plugin. Un agent ne voit ni la mémoire de Claude ni les autres épisodes : ce qu'il doit savoir est dans le contrat, `direction/`, les référentiels ou sa propre définition.
- **Qui décide** : le propriétaire de la chaîne (nommé dans son `CLAUDE.md`) est le seul à valider. Aucun agent ne valide, ne publie, n'achète ni ne déclare une écoute ou un visionnage.
- **Règles communes à tous** (rappelées dans chaque fichier) : les écarts de la chaîne (`direction/ECARTS.md`) l'emportent sur les règles par défaut du plugin ; lecture des autres épisodes seulement si le contrat les liste ; une correction après visionnage est confiée à un nouvel agent, sauf pour une séquence : elle se fait dans la même version (reprise du producteur si son cache est chaud, sinon agent court ; voir la fiche).

Workflows où ils interviennent : [`../workflows/recherche.md`](../workflows/recherche.md), [`../workflows/critique-da.md`](../workflows/critique-da.md), [`../workflows/sequence.md`](../workflows/sequence.md) ; le parcours complet est dans [`../workflows/episode.md`](../workflows/episode.md) ; les shorts dans [`../workflows/shorts.md`](../workflows/shorts.md).

## Tableau comparatif
| | `research` | `art-director` | `motion-producer` | `shorts-producer` | `studio-maintainer` |
|---|---|---|---|---|---|
| **Fichier** | `agents/research.md` | `agents/art-director.md` | `agents/motion-producer.md` | `agents/shorts-producer.md` | `agents/studio-maintainer.md` |
| **Mission en une ligne** | Vérifier faits, études, médias candidats | Intention visuelle, storyboard, critique indépendante d'un rendu | Mise en scène HyperFrames d'une séquence, jusqu'à `render.sh` | Montage vertical d'un short, jusqu'à `render.sh` | Cohérence, catalogue, reproductibilité |
| **Modèle** | `sonnet` | `inherit` | `inherit` | `inherit` | `sonnet` |
| **Couleur** | blue | purple | orange | pink | green |
| **Outils** | Read, Grep, Glob, WebFetch, WebSearch | Read, Grep, Glob, Bash, WebFetch, WebSearch, Skill | Read, Write, Edit, Grep, Glob, Bash, Skill, ToolSearch, Monitor, TaskStop | idem `motion-producer` | Read, Grep, Glob, Bash, Edit, Write, WebFetch |
| **Skills préchargés** | aucun | `hyperframes-creative`, `hyperframes-animation`, `studio-faceless:thumbnail-strategist` | `hyperframes-core`, `hyperframes-keyframes`, `hyperframes-animation` (WAAPI et CSS seulement) | `studio-faceless:shorts`, `hyperframes-core`, `hyperframes-keyframes` | aucun |
| **Rôle du garde-fou** (`ROLES`) | aucun (pas d'outil d'écriture ni de Bash) | `directeur-artistique` | `producteur` | `producteur` | `mainteneur` |
| **Droits d'écriture** | aucun | aucun outil d'écriture ; Bash limité à `ffmpeg`, `ffprobe`, `mkdir` pour des images extraites dans le dossier du contrat | son dossier `episodes/<id>/production/<séquence>-vN/` | son dossier `episodes/<id>/production/short-0N-vM/` | Write et Edit seulement, dans ce que le contrat autorise ; jamais par Bash |
| **Refusé par le garde-fou** | — | toute commande hors `ffmpeg`/`ffprobe`/`mkdir`, `-y`, sortie en zone protégée | citer `direction/`, `templates/`, `.claude/` ou un `CLAUDE.md` en Bash (sauf les chemins du plugin installé, sans « .. ») ; écrire dans `marque/` existant, `inputs/`, un MP4 existant | idem `motion-producer` | écriture Bash ; écriture dans `.claude/`, un projet de production, `marque/` existant, `inputs/`, un MP4 existant |
| **Livrable** | 5 rubriques : faits, études, médias candidats, limites, fichiers lus | storyboard (tableau) **ou** critique (5 à 10 problèmes), techniques à proposer, fichiers lus | dossier de séquence, `render.sh`, `README.md`, `PROVENANCE.md`, planche, rapport en 5 points | dossier de short, `render.sh` (deux rendus), `README.md`, `PROVENANCE.md`, rapport en 5 points | constats, changements, propositions non appliquées, risques |
| **Appelé à l'étape** | 1 (recherche) et 5 (médias du socle) | à la demande du propriétaire seulement | 6 (séquence témoin) et 7 (production) | shorts, après le film publié ou approuvé | à la demande, mission « studio » |
| **Peut lancer un rendu ?** | non | non | non : il écrit `render.sh` et s'arrête | non : idem | non |
| **Correction après retour** | un nouvel agent | un nouvel agent | dans la même version : reprise si le cache est chaud, sinon agent court | nouvelle version, par un nouvel agent | nouvelle mission |

## Garde-fou : ce qui est imposé et ce qui repose sur la consigne
Le hook `hooks/garde_commandes.py` s'applique à toute la session, sous-agents compris. Il déduit le rôle de `agent_type` (préfixe `studio-faceless:` retiré ; un préfixe historique `aa-` est aussi accepté) :

| Type d'agent | Rôle |
|---|---|
| `motion-producer`, `shorts-producer` | `producteur` |
| `art-director` | `directeur-artistique` |
| `studio-maintainer` | `mainteneur` |
| `research`, Claude principal | aucun rôle : seules les règles communes s'appliquent |

**Règles communes à tous** (rôle ou non) : refus de la publication HyperFrames, du cloud, de la connexion, de `upgrade`, de `skills update`, de `npx hyperframes@…`, de l'installation npm, de la suppression récursive ou définitive, du vidage de la corbeille ; refus de **toute écriture par Write/Edit dans le plugin installé** ; demande de confirmation pour `preview` ; refus (`deny`, sans confirmation possible) d'un rendu direct sans `--workers 1` ou `2`.

**Zones protégées** (chemins relatifs à la chaîne, `CLAUDE_PROJECT_DIR`), par rôle :

| Zone | DA (Bash/ffmpeg) | Producteur | Mainteneur |
|---|---|---|---|
| `direction/`, `templates/`, `.claude/`, tout fichier `CLAUDE.md` | oui | oui (aussi : aucune **mention** en Bash, sauf un chemin du plugin installé sans « .. ») | non protégés par le hook (limités par le contrat) |
| `.claude/` seul | (inclus ci-dessus) | (inclus) | oui |
| dossier **existant** de `marque/` | oui | oui | oui |
| `episodes/<id>/inputs/` | oui | oui | oui |
| `episodes/<id>/production/<…>` | oui | non (c'est son champ de travail) | oui |
| MP4 **existant** | oui | oui | oui |

**Ce que le hook n'impose pas** : le kit de l'épisode (`episodes/<id>/kit/`) et les projets des autres séquences ne sont pas des zones protégées. Que le producteur ne les modifie pas repose sur sa consigne, pas sur le hook. De même, le périmètre de lecture et d'écriture donné par le contrat est une consigne, hors des zones ci-dessus.

---

## Fiches

### agents/research.md
**Rôle** : recherche documentaire. Il vérifie faits, études, sources et médias candidats (dates, identités, licences, provenance) et rend un dossier ; il ne décide rien à la place du propriétaire.

**Quand il sert** : lancé par le Studio Director, une mission par grande partie du sujet (étape 1 du skill `episode`), puis pour trouver la meilleure image de chaque moment de la voix (étape 5, `skills/episode/references/socle.md` § 4). Parcours : [`../workflows/recherche.md`](../workflows/recherche.md).

**En-tête**
| Champ | Valeur |
|---|---|
| `name` | `research` |
| `tools` | Read, Grep, Glob, WebFetch, WebSearch |
| `model` | `sonnet` ; `color` : blue |
| `skills` | aucun |
| Rôle du garde-fou | aucun : il n'a ni Bash ni outil d'écriture |

**Contenu**
- **Contrat de mission** : écriture toujours « aucune ». S'il manque `episode_id`, l'objectif ou le périmètre de lecture, il ne commence pas et renvoie la liste des champs manquants.
- **Périmètre** :
  - lit les fichiers du contrat, `direction/LIGNE_EDITORIALE.md`, `direction/ECARTS.md`, `referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 bis (choix des médias), et `direction/references/` pour un besoin précis ;
  - n'ouvre aucun autre épisode, sauf fichiers listés au contrat ;
  - n'écrit rien : le Studio Director consigne ses résultats ;
  - n'envoie jamais l'adresse e-mail du propriétaire à un service externe.
- **Méthode, faits** : sources primaires d'abord (site officiel, presse datée, revue à DOI vérifié sur Crossref). Pour chaque affirmation : source, date de consultation, statut (vérifié, plausible, non vérifié), contradictions. Fait, hypothèse et interprétation sont distingués ; aucune citation, chiffre, date ou témoignage inventé.
- **Méthode, études** : référence complète, ce qu'elles montrent et ne montrent pas (population, méthode) ; une association n'est pas une causalité.
- **Méthode, médias** : ordre de préférence Wikimedia Commons (dernière révision, revue FlickreviewR, licence, SHA-1 par l'API), puis Openverse et Flickr en CC, puis Pexels ou Mixkit. Règles propres à chaque source (Commons, légendes d'auteur Flickr = témoignages, Pexels et Cloudflare, Mixkit `videoRestricted` refusé, FootageCrate, Resource Boy). Règle par défaut (`REFERENTIEL_QUALITE_REALISATION.md` § 2 bis) : choisir sur ce que le média apporte à la scène, gratuit, sans filigrane, jamais de filigrane retiré ni d'accès payant contourné ; vraies vidéos d'événement permises (compétitions listées dans `direction/ECARTS.md`) ; extraits de 6 s au plus ; source exacte notée pour remplacer vite le média.
- **Refus** : média d'une chaîne étudiée comme référence (liste dans `direction/ECARTS.md`), média présenté pour ce qu'il n'est pas, image générée présentée comme archive.
- **Téléchargements** : aucun. Le propriétaire télécharge à la main, d'après la liste que dresse le Studio Director (liens exacts, nom imposé, taille).
- **Livrable** (court, en français) : 1. faits (affirmation · source · statut) ; 2. études (référence · apport · limites) ; 3. médias candidats (lien · auteur · licence · contenu · fonction · risques) ; 4. limites, risques, questions ouvertes ; 5. fichiers locaux lus.

**Liens** : cité par `REGLES_STUDIO.md`, `skills/episode/SKILL.md` (étape 1), `skills/episode/references/socle.md` § 4 ; contrat : [`templates/CONTRAT_MISSION.template.md`](templates.md#templatescontrat_missiontemplatemd).

**À savoir**
- Le rapport n'arrive pas dans un fichier : il est écrit par le Studio Director dans `episodes/<id>/research/` (`R-*.md`, d'après `skills/episode/SKILL.md`).
- La liste d'ordre de préférence des sources (`research.md:33-42`) indique où chercher d'abord ; la règle par défaut qui suit (`research.md:43`) dit que la licence ne décide plus du choix. Les deux se lisent ensemble : on cherche d'abord dans les sources libres, mais on peut retenir une image non libre en citation encadrée si elle est la meilleure pour la scène.
- Pexels : ouvrir les pages une à une ; un déclenchement Cloudflare ne se contourne jamais.

### agents/art-director.md
**Rôle** : direction artistique. Il transforme un script en intention visuelle et en storyboard, ou critique un rendu de façon indépendante. Il ne construit ni ne rend de vidéo. Le propriétaire est le directeur artistique final : l'agent propose, il ne valide pas.

**Quand il sert** : **seulement à la demande du propriétaire** (`REGLES_STUDIO.md` : critique indépendante des rendus ; storyboard seulement sur demande ; `skills/episode/references/socle.md` § 3). Il choisit lui-même les techniques d'animation et de transition d'un film (validé sur AA, 18/10/2026). Parcours : [`../workflows/critique-da.md`](../workflows/critique-da.md).

**En-tête**
| Champ | Valeur |
|---|---|
| `name` | `art-director` |
| `tools` | Read, Grep, Glob, Bash, WebFetch, WebSearch, Skill |
| `model` | `inherit` ; `color` : purple |
| `skills` | `hyperframes-creative`, `hyperframes-animation`, `studio-faceless:thumbnail-strategist` |
| Rôle du garde-fou | `directeur-artistique` |

**Limites du garde-fou (rôle `directeur-artistique`)**
- Bash : **chaque segment** de commande doit commencer par `ffmpeg`, `ffprobe` ou `mkdir`. Un tube (`|`), un `ls`, une boucle `for` ou un `grep` sont donc refusés (le hook découpe la commande sur `&&`, `||`, `;`, `|` et les retours à la ligne).
- `ffmpeg -y` est refusé (pas d'écrasement) : écrire dans un dossier neuf.
- La sortie d'un `ffmpeg` (dernier argument sans tiret) ne peut pas tomber dans `direction/`, `templates/`, `.claude/`, un `CLAUDE.md`, un dossier existant de `marque/`, `episodes/<id>/inputs/`, `episodes/<id>/production/…` ni sur un MP4 existant.
- Il n'a ni Write ni Edit : son seul geste d'écriture est l'extraction d'images. Son livrable passe par sa réponse ; le Studio Director l'enregistre.

**Contenu**
- **Contrat de mission** : le champ « écriture » est le dossier de travail des images extraites, rien d'autre. S'il manque un champ essentiel, il renvoie la liste avant de travailler.
- **Lecture** : fichiers du contrat ; `direction/ECARTS.md` ; `REFERENTIEL_QUALITE_REALISATION.md` (« le référentiel ») ; `DIRECTION_AUDIO.md` et le skill `studio-faceless:direction-sonore` (via l'outil Skill, plus préchargé depuis le 18/10/2026) si le son compte ; `marque/README.md` (ouverture, sortie, appel Like + Subscribe) ; résumé en tête des études de `direction/references/` ; `MOTION_CATALOG.md` à la demande. Autres épisodes : exclus sauf contrat. Une fiche de catalogue décrit une méthode ; on n'en reprend jamais les médias ni les choix d'un autre épisode.
- **Concevoir un épisode ou une séquence** : une idée visuelle directrice, un motif narratif, une approche du mouvement, un traitement des médias, un rythme, les techniques d'animation et de transition (anciennes reprises et améliorées, ou nouvelles signalées avec leur raison d'être), le moment de l'appel « Like + Subscribe ». Images clés et contrat de plan seulement sur demande : depuis le 15/10/2026, aucune image clé n'est soumise au propriétaire. Pour chaque scène, il remplit le contrat de scène du référentiel (§ 3) : enjeu, avant/après, matériaux, progression, raccords, lecture, audio, refus. Chaque média respecte § 2 bis (situation authentique, fonction en une phrase, mots dans l'image, image adaptée au récit).
- **À éviter** : effet diaporama, mêmes trois transitions d'un film à l'autre, mot qui flotte, fausse donnée d'étude, fausse archive.
- **Critiquer un rendu** : 1. travailler d'abord sur le brief et le MP4 seuls, **sans lire les justifications du producteur** (README du projet) ; 2. extraire une planche à 2 images/s et des planches denses autour des raccords ; 3. juger immersion, pertinence des médias, continuité, rythme, storytelling, niveau visuel, lisibilité mobile ; 4. comparer ensuite seulement au rapport du producteur ; 5. aucun verdict « conforme » fondé sur les seules mesures techniques (porte C). Il ne prétend jamais avoir regardé à vitesse normale ni écouté : il juge sur des images.
- **Livrable** (court, en français) : soit un **storyboard** (tableau temps/phrase · média · transformation · raccord · statut A archive, I illustration, G graphisme, R reconstitution), soit une **critique** (5 à 10 problèmes classés ; pour chacun : temps, observation, raison, correction concrète) ; puis les techniques à proposer au catalogue (statut « expérimental » seulement) et les fichiers lus.

**Liens** : `referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2, § 2 bis, § 2 ter, § 3, § 3 bis, § 4 (porte C) ; `skills/thumbnail-strategist/SKILL.md` (critique de miniatures sur PNG et planches : ses scripts ne passent pas le garde-fou du DA, les mesures sont faites par Claude principal).

**À savoir**
- `hyperframes-creative` et `hyperframes-animation` sont préchargés, mais la consigne dit de ne s'en servir que si leur vocabulaire est utile (`art-director.md:32`, voir « Écarts »).
- Le propriétaire est le seul à demander cet agent : le Studio Director ne le lance pas de lui-même.

### agents/motion-producer.md
**Rôle** : mise en scène HyperFrames d'**une** séquence : il écrit les scènes, vérifie une planche de captures, prépare la commande de rendu et **s'arrête**. Le rendu final et les contrôles sont faits par le Studio Director. Il ne change ni le script, ni la voix, ni la direction artistique approuvée.

**Quand il sert** : étape 6 (séquence témoin) puis étape 7 (lots de trois au plus) du skill `episode`, une mission par séquence. Parcours : [`../workflows/sequence.md`](../workflows/sequence.md) ; contrat complet : `skills/episode/references/production.md` § 2.

**En-tête**
| Champ | Valeur |
|---|---|
| `name` | `motion-producer` |
| `tools` | Read, Write, Edit, Grep, Glob, Bash, Skill, ToolSearch, Monitor, TaskStop |
| `model` | `inherit` ; `color` : orange |
| `skills` | `hyperframes-core`, `hyperframes-keyframes`, `hyperframes-animation` (le dernier en **WAAPI et CSS seulement** : jamais GSAP, Lottie, Three.js ni Anime.js) |
| Rôle du garde-fou | `producteur` |

**Limites du garde-fou (rôle `producteur`)**
- **Bash** : refus de toute commande dont le texte cite `direction/`, `templates/`, `.claude/` ou un `CLAUDE.md` (même dans un `grep`) ; ces fichiers se lisent avec Read ou Grep. **Exception** : avant ce contrôle, le hook remplace les chemins du plugin installé (`CLAUDE_PLUGIN_ROOT`, sans « .. ») : le producteur peut donc lancer par Bash les outils du plugin (`outils/controle/…`, dont le cache est sous `~/.claude/plugins/`) sans que la règle « `.claude/` » les bloque. Refus d'une écriture (redirection, `cp`, `mv`, `tee`, `touch`, `ffmpeg` sortie…) vers un dossier existant de `marque/`, `episodes/<id>/inputs/` ou un MP4 existant, et d'un script en ligne (`python -c`, `node -e`) qui écrit vers `marque/` ou `inputs/`.
- **Write et Edit** : refusés dans `direction/`, `templates/`, `.claude/`, sur tout `CLAUDE.md`, dans un dossier existant de `marque/`, dans `inputs/` et sur un MP4 existant.
- **Conséquence pratique** : le gabarit vient du kit, pas du plugin. C'est le Studio Director qui l'a copié dans `episodes/<id>/kit/gabarit/` ; le producteur copie ce dossier du kit. Une commande qui citerait `templates/` ou `direction/` hors du plugin installé reste refusée.
- Le hook ne protège pas le kit ni les autres dossiers de production : la consigne le fait.

**Contenu**
- **Ce qu'il reçoit** : un contrat de mission avec un dossier d'écriture exact `episodes/<id>/production/<séquence>-vN/` ; un brief de séquence court (narration minutée, plan de plans, sons, règles utiles) ; le kit de l'épisode (médias convertis et provenance, bande voix ralentie et repères, gabarit v3, consignes communes). S'il manque le brief, le kit ou le dossier d'écriture, il ne crée rien et renvoie la liste.
- **Ce qu'il lit** : le brief, le kit, `episodes/<id>/CLAUDE.md` (constats HyperFrames). Un référentiel seulement pour la section que le brief cite. Le catalogue `referentiels/MOTION_CATALOG.md` : en-tête et index (début du fichier jusqu'à la première fiche `###`, par plage), puis les fiches retenues par Grep (`^### ID`) ou Read, jamais par Bash. Jamais la production d'un autre épisode.
- **Fiche d'effets** : avant toute scène, en tête du README, pour chaque moment : technique, idée qu'elle sert, pourquoi elle, effet sonore ; puis ce qui progresse par rapport à l'épisode précédent.
- **Méthode en quatre étapes** : 1. partir du gabarit (copie, scènes, une sous-composition par moment, retouches par `Edit` uniquement) ; 2. vérifier par une planche (`check`, puis **une** planche de 16 à 20 instants assemblés, une seconde au plus, aucun essai court séparé) ; 3. préparer le rendu sans le lancer (`render.sh` avec `--workers 2`, qui n'écrase rien ; `README.md` ; extrait de provenance du kit **ajouté à la fin** du `PROVENANCE.md` du gabarit, sans effacer les licences des matières) ; 4. s'arrêter avec un rapport.
- **Économie de contexte** : jamais plus de 4 min sans action (cache de 5 min) ; pas de `sleep` ; plafond de contexte de 300 k, puis `ETAT.md` dans son dossier (fait, reste, étape suivante, fichiers en cours) et arrêt ; sorties courtes ; une image à la fois ; aucun script de contrôle maison ; aucune permission en attente.
- **HyperFrames** : version de `package.json` (0.8.149) ; pas d'entretien d'intention ni de routage « création » du skill `hyperframes` ; une seule composition racine par dossier (les autres dans `compositions/`, rendues avec `-c`) ; automation de volume en valeurs absolues ; vidéo source à images clés espacées figée au rendu (kit : déjà réencodée, sinon `-g 15`) ; aucun chemin absolu vers FFmpeg ou Chrome ; pas de `preview` ; MP4 1920 × 1080, 30 i/s, H.264, AAC 48 kHz.
- **Interdits** : mixer musique et effets dans la séquence (elle ne porte que la voix ; il propose ses effets dans le README) ; régénérer, couper ou accélérer une voix ; télécharger un média ; fabriquer une preuve ; générer un média payant (pas d'accès ElevenLabs) ; publier ; déclarer une écoute ou un visionnage.
- **Livrable** (rapport court en français) : 1. dossier de production, `render.sh`, durée prévue ; 2. résultat de `check` et chemin des planches ; 3. écarts au brief ; 4. points à valider par le propriétaire et ce qui manquait ; 5. fichiers écrits (liste exacte).
- **Correction** (validé sur AA, 24/10/2026) : dans la même version, sur demande ciblée du Studio Director (reprise du producteur si son cache est chaud, sinon agent court). Nouvelle version seulement pour un défaut majeur. Le rendu déjà fait est rangé par le Studio Director dans `_rendu-N/`.

**Liens** : [`templates.md`](templates.md#templatessequence-gabarit-v3readmemd) (gabarit v3) ; `skills/episode/references/production.md` ; `referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 (diaporama), § 2 ter, § 2 quater ; `referentiels/DIRECTION_AUDIO.md` § 2 et § 3 ; `outils/controle/` (lancé par le Studio Director).

**À savoir**
- Le contenu du README demandé diffère entre `motion-producer.md:55` (liste courte) et `production.md:64` (liste détaillée, qui s'ouvre sur la fiche d'effets) : suivre le contrat de mission, qui reprend `production.md`.
- Autres écarts : voir la dernière section.

### agents/shorts-producer.md
**Rôle** : montage HyperFrames d'un short vertical (1080 × 1920), tiré d'un film de la chaîne, pour YouTube Shorts, TikTok et Facebook Reels. Il met en scène un short **déjà écrit et validé** : script, prise voix, hook, médias décidés. Il ne change ni le texte ni la voix. Objectifs du short (validé sur AA, 19/10/2026), dans l'ordre : qu'il soit regardé jusqu'au bout, faire connaître la chaîne, amener vers le film.

**Quand il sert** : après le film, un short par mission (méthode : skill `shorts`, statut `PROPOSÉ` d'après `skills/shorts/SKILL.md`). Parcours : [`../workflows/shorts.md`](../workflows/shorts.md).

**En-tête**
| Champ | Valeur |
|---|---|
| `name` | `shorts-producer` |
| `tools` | Read, Write, Edit, Grep, Glob, Bash, Skill, ToolSearch, Monitor, TaskStop |
| `model` | `inherit` ; `color` : pink |
| `skills` | `studio-faceless:shorts`, `hyperframes-core`, `hyperframes-keyframes` |
| Rôle du garde-fou | `producteur` (mêmes limites que le `motion-producer`) |

**Contenu**
- **Ce qu'il reçoit** : contrat avec un dossier d'écriture exact `episodes/<id>/production/short-0N-vM/` ; **brief de short** (modèle : `skills/shorts/references/brief-short.md`, 3 Ko au plus : script minuté, hook, plan de plans, pont vers le film, son, versions, marque) ; **kit shorts** (`episodes/<id>/kit/shorts/` : prise voix contrôlée, repères mot à mot, médias et provenance, filigrane de la chaîne, police, musique, gabarit vertical).
- **Ce qu'il lit** : le brief, le kit, `episodes/<id>/CLAUDE.md`, les références du skill `shorts` utiles au montage. Jamais un autre épisode ni les séquences du film.
- **Méthode en quatre étapes** : 1. partir du gabarit vertical du kit ; **image 0** = l'image la plus forte, la ligne du hook et la voix dès 0,0 s (ni noir, ni fondu d'entrée, ni logo animé avant le hook) ; sous-titres mot à mot (apparition en opacité, puis texte immobile ; jamais d'échelle ni de `filter: blur`) ; recomposition verticale des médias horizontaux, sans fond flouté par facilité ; logo discret pendant tout le short, carton final avec le pont vers le film ; contenu essentiel dans les zones visibles des trois plateformes ; 2. vérifier : `check`, une capture de l'image 0 en pleine taille, une planche de 12 à 16 instants avec le tracé des zones masquées, une seconde planche au plus ; 3. préparer les **deux** rendus dans `render.sh` (TikTok et Facebook, puis YouTube ; 1080 × 1920, `--workers 2`, sorties qui n'écrasent rien), `README.md`, `PROVENANCE.md` (extrait du kit et texte des crédits pour les légendes) ; 4. s'arrêter.
- **Deux exports par short** (validé sur AA, 19/10/2026) : TikTok et Facebook : tous les blocs, 65 à 85 s, en composition racine ; YouTube : sans le bloc D, **toujours sous 60 s**, dans `compositions/`, rendue avec `-c`, sur les mêmes scènes.
- **Économie de contexte** : mêmes règles que le `motion-producer` (4 min, 300 k puis `ETAT.md`, sorties courtes, images rares, pas de scripts de contrôle maison, pas de permission en attente).
- **Interdits** : régénérer, couper ou accélérer la voix ; ajouter une phrase, un chiffre ou un texte absent du script validé ; mettre un crédit photo à l'écran (les crédits vont dans les légendes) ; télécharger un média ; fabriquer une preuve ; utiliser une image générée par IA ; générer un média payant ; publier ; déclarer une écoute.
- **Livrable** : rapport court en 5 points : dossier, `render.sh` et durée de chaque version ; `check`, capture de l'image 0, planches ; écarts au brief ; points à valider et manques ; fichiers écrits.
- **Correction après visionnage** : dans une **nouvelle version**, par un **nouvel** agent muni d'un brief de quelques lignes.

**Liens** : `skills/shorts/SKILL.md`, `skills/shorts/references/montage-vertical.md`, `brief-short.md`, `plateformes.md` ; `outils/shorts/` ; `outils/controle/` (Studio Director).

**À savoir**
- Le plugin ne livre aucun gabarit vertical dans `templates/` (seul existe `sequence-gabarit-v3/`). Le « gabarit vertical du kit » est préparé par le Studio Director ; sa source est à vérifier (voir « Écarts »).
- Contrairement au `motion-producer`, la correction se fait en nouvelle version.

### agents/studio-maintainer.md
**Rôle** : maintenance de l'espace de la chaîne : cohérence des directives et des chemins, fichiers temporaires, dépendances, reproductibilité des rendus, catalogue d'animations, composants réutilisables. Il ne produit aucune vidéo et n'installe rien sans mission. Il protège l'architecture ; il ne la complique pas.

**Quand il sert** : à la demande du Studio Director, avec `episode_id` valant « studio » (sauf mission d'épisode). Sans « fichiers ou dossiers autorisés en écriture » dans le contrat, il **constate et propose** seulement. Il n'a pas de workflow dédié : c'est l'agent qui a servi à écrire la présente documentation.

**En-tête**
| Champ | Valeur |
|---|---|
| `name` | `studio-maintainer` |
| `tools` | Read, Grep, Glob, Bash, Edit, Write, WebFetch |
| `model` | `sonnet` ; `color` : green |
| `skills` | aucun |
| Rôle du garde-fou | `mainteneur` |

**Limites du garde-fou (rôle `mainteneur`)**
- **Aucune écriture par Bash** : toute commande qui a une cible d'écriture probable (redirection, `cp`, `mv`, `tee`, `touch`, `ffmpeg`…) ou dont la tête est une commande d'écriture est refusée ; un script en ligne (`python -c`, `node -e`) qui écrit est refusé. Il écrit avec Write ou Edit.
- Write et Edit refusés dans `.claude/`, un dossier **existant** de `marque/`, `episodes/<id>/inputs/`, un projet de production (`episodes/<id>/production/<…>`) et sur un MP4 existant. Le hook ne protège ni `direction/`, ni `templates/`, ni les `CLAUDE.md` pour ce rôle : c'est le contrat qui borne l'écriture.

**Contenu**
- **Cohérence** : directives (`CLAUDE.md` de chaque dossier, `direction/` dont `ECARTS.md`, `marque/`, `templates/`, `agents/`, `.claude/agents/`) et chemins ; doublons et contradictions ; les écarts de la chaîne l'emportent sur les règles par défaut.
- **Fichiers** : repérer les temporaires inutiles et les proposer à la suppression avec la liste ; il ne supprime que ce que le contrat autorise nommément.
- **Dépendances** : HyperFrames (le `package.json` fait foi), FFmpeg, Node, Python ; signaler une mise à jour, sans l'appliquer.
- **Reproductibilité** : chaque `render.mjs`, `generate.py` ou script d'assemblage pointe vers des sources existantes ; empreintes annoncées vérifiées.
- **Catalogue** (`referentiels/MOTION_CATALOG.md`) : ajouter ou mettre à jour une fiche sur demande avec des chemins vérifiés (dans une chaîne, une nouvelle technique se propose dans la section MOTION_CATALOG de `direction/ECARTS.md` ; elle n'entre au catalogue que dans le dépôt du plugin, le plugin installé ne se modifiant pas) ; statut « expérimental » ou « à améliorer » ; « validé » **seulement** si le contrat cite l'accord explicite du propriétaire ; repérer les composants réutilisables sans les extraire.
- **Il ne fait pas** : rendu ou production vidéo ; refactoring global ou déplacement de projets d'épisode ; installation ou mise à jour de dépendance ; modification des autres agents, des scripts approuvés, des rendus ou des assets historiques sans mission ; lecture d'un épisode au-delà de la mission ; interface graphique (mission future séparée : il peut seulement lister des besoins).
- **Livrable** (court, en français) : 1. constats classés par gravité avec les chemins ; 2. changements effectués (fichiers et résumé, ou « aucun ») ; 3. propositions non appliquées ; 4. risques.

**Liens** : `referentiels/MOTION_CATALOG.md` ; `templates/CONTRAT_MISSION.template.md`.

**À savoir**
- Le catalogue vit dans le plugin installé, que le hook rend non modifiable depuis une chaîne. Depuis une chaîne, une nouvelle technique se note dans la section MOTION_CATALOG de `direction/ECARTS.md` (`MOTION_CATALOG.md:16`) ; la définition de l'agent le dit désormais (`studio-maintainer.md`, section « Catalogue »).

---

## Écarts et points à vérifier relevés dans ces fichiers
Constats de lecture, du plus gênant au moins gênant. Les écarts réglés par la correction du 28/10/2026 (rendu sans `--workers` refusé, corrections d'une séquence dans la même version, catalogue et plugin installé, `PROVENANCE.md` du gabarit, plage de lecture de l'index du catalogue) ont été retirés.

| # | Constat | Fichiers (lignes) |
|---|---|---|
| 1 | **Nombre d'instants de la planche** : 16 à 20 (agent, gabarit à 16) contre 24 dont 6 milieux de transition (contrat du producteur). | `agents/motion-producer.md:50`, `templates/sequence-gabarit-v3/README.md:64` contre `skills/episode/references/production.md:65` |
| 2 | **Gabarit vertical des shorts** : exigé dans le kit shorts, mais aucun gabarit vertical n'existe dans `templates/` ; seul `sequence-gabarit-v3/` est livré. À vérifier : où le Studio Director le prend. | `agents/shorts-producer.md:31` et `48`, `skills/shorts/references/brief-short.md:16` |
| 3 | **Mot « dix »** : « jamais les dix ensemble », reste d'un ancien parcours (le DA n'a que deux skills `hyperframes-*` préchargés). | `agents/art-director.md:32` |
| 4 | **Recherche : ordre de préférence et licence** : la liste des sources (Commons, puis Openverse/Flickr, puis Pexels/Mixkit) cohabite avec la règle « la licence ne compte pas » ; à lire ensemble (voir fiche). | `agents/research.md:33-43` |
| 5 | **`CLAUDE.md` sous Linux ou macOS** : le hook compare `parts[-1] == 'claude.md'` après `os.path.normcase`, qui ne met pas en minuscules hors Windows ; la protection des `CLAUDE.md` par Write/Edit ne s'y déclencherait pas pour `CLAUDE.md`. À vérifier si une chaîne tourne hors Windows. | `hooks/garde_commandes.py:96`, `108` |
