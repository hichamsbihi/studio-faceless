# Référence : les agents du plugin (`agents/`)

Ce document décrit les onze agents du plugin `studio-faceless` : leur en-tête, ce qu'ils lisent, ce qu'ils écrivent, ce que le garde-fou leur interdit, ce qu'ils livrent et qui les appelle. Les fichiers de `agents/` font foi ; en cas d'écart, la documentation se corrige.

## Table des matières
- [Vue d'ensemble](#vue-densemble)
- [Tableau comparatif](#tableau-comparatif)
- [Garde-fou : ce qui est imposé et ce qui repose sur la consigne](#garde-fou--ce-qui-est-imposé-et-ce-qui-repose-sur-la-consigne)
- [Fiches](#fiches)
  - [agents/research.md](#agentsresearchmd)
  - [agents/reviewer.md](#agentsreviewermd)
  - [agents/art-director.md](#agentsart-directormd)
  - [agents/motion-producer.md](#agentsmotion-producermd)
  - [agents/shorts-producer.md](#agentsshorts-producermd)
  - [agents/studio-maintainer.md](#agentsstudio-maintainermd)
  - [agents/strategist.md](#agentsstrategistmd)
  - [agents/media-fetcher.md](#agentsmedia-fetchermd)
  - [agents/sound-manager.md](#agentssound-managermd)
  - [agents/publisher.md](#agentspublishermd)
  - [agents/conseiller.md](#agentsconseillermd)
- [Écarts et points à vérifier relevés dans ces fichiers](#écarts-et-points-à-vérifier-relevés-dans-ces-fichiers)

## Vue d'ensemble
- **Un agent est un sous-agent de Claude principal** (le Studio Director). Il est lancé par le Studio Director avec un **contrat de mission** (neuf champs, modèle : [`templates/CONTRAT_MISSION.template.md`](templates.md#templatescontrat_missiontemplatemd)). Les agents ne se délèguent rien entre eux (`REGLES_STUDIO.md`, « Sous-agents »).
- **Noms** : une fois le plugin installé, chaque agent prend le préfixe du plugin : `studio-faceless:research`, `studio-faceless:reviewer`, `studio-faceless:art-director`, `studio-faceless:motion-producer`, `studio-faceless:shorts-producer`, `studio-faceless:studio-maintainer`, `studio-faceless:strategist` (0.4.0), `studio-faceless:media-fetcher` (0.6.0), `studio-faceless:sound-manager` et `studio-faceless:publisher` (0.7.0), `studio-faceless:conseiller` (0.8.0). Le champ `name:` de l'en-tête garde le nom court ([`../ARCHITECTURE.md`](../ARCHITECTURE.md), « Noms »).
- **En-tête** : chaque fichier commence par un en-tête YAML : `name`, `description` (ce que Claude lit pour décider de déléguer), `tools`, `model`, `color`, `skills` (skills préchargés dans le contexte de l'agent, quand il y en a) et, pour `research`, `studio-maintainer` (depuis la 0.2.3), `strategist` (0.4.0) et `media-fetcher` (0.6.0), `omitClaudeMd: true` : l'agent démarre sans le `CLAUDE.md` de la chaîne (champ qui demande Claude Code 2.1.271 ou plus ; l'application de bureau fait tourner son propre Claude Code, 2.1.309 le 02/11/2026, donc il y agit ; seule la copie du terminal, 2.1.169 sur la machine de mise au point, peut être plus ancienne). Claude principal tourne sur Opus (validé sur AA, 02/11/2026) : les agents en `model: inherit` (`art-director`, `motion-producer`, `shorts-producer`, `strategist`) le suivent ; `research`, `reviewer` et `studio-maintainer` restent en `sonnet` ; `sound-manager` et `publisher` sont en `opus` (0.7.0). Les règles de la chaîne dont ils ont besoin sont alors dans leur contrat, section « Règles de la chaîne utiles à la mission » ([`templates.md`](templates.md#templatescontrat_missiontemplatemd)). `reviewer` garde le `CLAUDE.md` : il contrôle les règles de la chaîne.
- **Un plugin ignore les champs `hooks`, `mcpServers` et `permissionMode`** de l'en-tête de ses agents ([`../ARCHITECTURE.md`](../ARCHITECTURE.md), « Garde-fou »). Les limites par rôle viennent donc du hook du plugin (`hooks/garde_commandes.py`), qui reconnaît le rôle au champ `agent_type` : voir le tableau `ROLES` plus bas.
- **Skills préchargés** : `hyperframes-*` sont des skills d'utilisateur (copiés dans `~/.claude/skills/`, voir [`vendor.md`](vendor.md)), sans préfixe ; `studio-faceless:…` sont les skills du plugin. Un agent ne voit ni la mémoire de Claude ni les autres épisodes : ce qu'il doit savoir est dans le contrat, `direction/`, les référentiels ou sa propre définition.
- **Qui décide** : le propriétaire de la chaîne (nommé dans son `CLAUDE.md`) est le seul à valider. Aucun agent ne valide, ne publie, n'achète ni ne déclare une écoute ou un visionnage.
- **Règles communes à tous** (rappelées dans chaque fichier) : les écarts de la chaîne (`direction/ECARTS.md`) l'emportent sur les règles par défaut du plugin ; lecture des autres épisodes seulement si le contrat les liste ; une correction après visionnage est confiée à un nouvel agent, sauf pour une séquence : elle se fait dans la même version (reprise du producteur si son cache est chaud, sinon agent court ; voir la fiche).

Workflows où ils interviennent : [`../workflows/recherche.md`](../workflows/recherche.md), [`../workflows/critique-da.md`](../workflows/critique-da.md), [`../workflows/sequence.md`](../workflows/sequence.md) ; le parcours complet est dans [`../workflows/episode.md`](../workflows/episode.md) ; les shorts dans [`../workflows/shorts.md`](../workflows/shorts.md).

## Tableau comparatif
| | `research` | `reviewer` | `art-director` | `motion-producer` | `shorts-producer` | `studio-maintainer` | `strategist` |
|---|---|---|---|---|---|---|---|
| **Fichier** | `agents/research.md` | `agents/reviewer.md` | `agents/art-director.md` | `agents/motion-producer.md` | `agents/shorts-producer.md` | `agents/studio-maintainer.md` | `agents/strategist.md` |
| **Mission en une ligne** | Vérifier faits, études, médias candidats | Contrôle qualité en lecture seule d'un script, d'une séquence ou du film contre une liste | Intention visuelle, storyboard, critique indépendante d'un rendu | Mise en scène HyperFrames d'une séquence, jusqu'à `render.sh` | Montage vertical d'un short, jusqu'à `render.sh` | Cohérence, catalogue, reproductibilité | Positionnement et stratégie éditoriale d'une chaîne, une phase par appel (dossier, brief, conseil, titres, sujets, banque) |
| **Modèle** | `sonnet` | `sonnet` | `inherit` | `inherit` | `inherit` | `sonnet` | `inherit` |
| **Couleur** | blue | yellow | purple | orange | pink | green | cyan |
| **Outils** | Read, Grep, Glob, WebFetch, WebSearch | Read, Grep, Glob, Bash | Read, Grep, Glob, Bash, WebFetch, WebSearch, Skill | Read, Write, Edit, Grep, Glob, Bash, Skill, ToolSearch, Monitor, TaskStop | idem `motion-producer` | Read, Grep, Glob, Bash, Edit, Write, WebFetch | Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch |
| **Skills préchargés** | aucun | aucun | `hyperframes-creative`, `hyperframes-animation`, `studio-faceless:thumbnail-strategist` | `hyperframes-core`, `hyperframes-keyframes`, `hyperframes-animation` (WAAPI et CSS seulement) | `studio-faceless:shorts`, `hyperframes-core`, `hyperframes-keyframes` | aucun | aucun |
| **`CLAUDE.md` de la chaîne** | omis (`omitClaudeMd`), règles dans le contrat | lu | lu | lu | lu | omis (`omitClaudeMd`), règles dans le contrat | omis (`omitClaudeMd`), règles dans le contrat |
| **Rôle du garde-fou** (`ROLES`) | aucun (pas d'outil d'écriture ni de Bash) | `relecteur` (Bash en lecture et mesure seulement) | `directeur-artistique` | `producteur` | `producteur` | `mainteneur` | `stratege` |
| **Droits d'écriture** | aucun | aucun (consigne : Bash pour lire et mesurer seulement) | aucun outil d'écriture ; Bash limité à `ffmpeg`, `ffprobe`, `mkdir` pour des images extraites dans le dossier du contrat | son dossier `episodes/<id>/production/<séquence>-vN/` | son dossier `episodes/<id>/production/short-0N-vM/` | Write et Edit seulement, dans ce que le contrat autorise ; jamais par Bash | Write et Edit seulement dans `docs/` de la chaîne, et dans `direction/BANQUE_SUJETS.md` sur accord du propriétaire cité au contrat |
| **Refusé par le garde-fou** | — | règles communes seulement | toute commande hors `ffmpeg`/`ffprobe`/`mkdir`, `-y`, sortie en zone protégée | citer `direction/`, `templates/`, `.claude/` ou un `CLAUDE.md` en Bash (sauf les chemins du plugin installé, sans « .. ») ; écrire dans `marque/` existant, `inputs/`, un MP4 existant | idem `motion-producer` | écriture Bash ; écriture dans `.claude/`, un projet de production, `marque/` existant, `inputs/`, un MP4 existant | écriture hors `docs/` et `direction/BANQUE_SUJETS.md` ; Bash hors `python` (outils du plugin), `ls`, `wc`, `grep`, `head`, `tail`, `mkdir`, `cd` ; script en ligne |
| **Livrable** | 5 rubriques : faits, études, médias candidats, limites, fichiers lus | tableau point · verdict · minutage · preuve, 25 lignes au plus | storyboard (tableau) **ou** critique (5 à 10 problèmes), techniques à proposer, fichiers lus | dossier de séquence, `render.sh`, `README.md`, `PROVENANCE.md`, planche, rapport en 5 points | dossier de short, `render.sh` (deux rendus), `README.md`, `PROVENANCE.md`, rapport en 5 points | constats, changements, propositions non appliquées, risques | synthèse de 300 mots au plus : phase, fichiers, décisions en blocs, coût, limites, fichiers lus |
| **Appelé à l'étape** | 1 (recherche) et 5 (médias du socle) | avant de montrer un script (3), une séquence (8) ou le film (10) au propriétaire | à la demande du propriétaire seulement | 6 (séquence témoin) et 7 (production) | shorts, après le film publié ou approuvé | à la demande, mission « studio » | hors parcours d'un épisode : positionnement de la chaîne, titres, banque de sujets (le skill `episode` lit la banque, `references/choix-sujet.md` § 4) ; mission « studio » |
| **Peut lancer un rendu ?** | non | non | non | non : il écrit `render.sh` et s'arrête | non : idem | non | non |
| **Correction après retour** | un nouvel agent | un nouvel agent | un nouvel agent | dans la même version : reprise si le cache est chaud, sinon agent court | nouvelle version, par un nouvel agent | nouvelle mission | nouveau fichier (`…_v2`) par un nouvel appel |

**`media-fetcher` (0.6.0)** n'a pas de colonne ici : sa fiche, en fin de section « Fiches », donne les mêmes rubriques (outils Read, Write, Bash, Glob, Grep ; `sonnet` ; couleur orange ; `omitClaudeMd` ; rôle `telechargeur` ; écriture sous `episodes/<id>/kit/media/source-vN/` ; appelé à l'étape 5, médias du socle). **`sound-manager` et `publisher` (0.7.0)** non plus : voir leurs fiches. **`conseiller` (0.8.0)** non plus : voir sa fiche.

## Garde-fou : ce qui est imposé et ce qui repose sur la consigne
Le hook `hooks/garde_commandes.py` s'applique à toute la session, sous-agents compris. Il déduit le rôle de `agent_type` (préfixe `studio-faceless:` retiré) :

| Type d'agent | Rôle |
|---|---|
| `motion-producer`, `shorts-producer` | `producteur` |
| `art-director` | `directeur-artistique` |
| `studio-maintainer` | `mainteneur` |
| `research`, Claude principal | aucun rôle : seules les règles communes s'appliquent |
| `reviewer` | `relecteur` : en Bash, seules `ffprobe`, `ffmpeg` de mesure (`-f null`), `wc`, `ls`, `grep`, `head` et `tail`, sans redirection |
| `strategist` | `stratege` : Write et Edit seulement dans `docs/` et `direction/BANQUE_SUJETS.md` ; en Bash, `python` sur les outils du plugin (sauf `youtube_retention.py`, réservé à Claude principal depuis la 0.6.0), `ls`, `wc`, `grep`, `head`, `tail`, `mkdir`, `cd` |
| `media-fetcher` | `telechargeur` (0.6.0) : Write et Edit seulement sous `episodes/<id>/kit/media/source-vN/` ; en Bash, `python` sur `outils/medias/telecharger_medias.py` du plugin installé seul (liste sous `kit/`, dépôt et manifeste sous `source-vN/`), `ls`, `wc`, `grep`, `head`, `tail`, `mkdir`, `cd` ; ni `curl` ni `wget`, aucun script en ligne |
| `sound-manager` | `ingenieur-son` (0.7.0) : voir sa fiche |
| `publisher` | `editeur` (0.7.0) : voir sa fiche |
| `conseiller` | aucun rôle (0.8.0) : ni outil d'écriture ni Bash |

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
| `omitClaudeMd` | `true` (0.2.3) : démarre sans le `CLAUDE.md` de la chaîne |
| Rôle du garde-fou | aucun : il n'a ni Bash ni outil d'écriture |

**Contenu**
- **Contrat de mission** : écriture toujours « aucune ». S'il manque `episode_id`, l'objectif, le périmètre de lecture ou la section « Règles de la chaîne utiles à la mission », il ne commence pas et renvoie la liste des champs manquants.
- **Sans `CLAUDE.md` de la chaîne** (`omitClaudeMd`, 0.2.3) : les règles de la chaîne utiles à la mission (protection des personnes, sources admises, langues) sont dans son contrat ; sinon il lit, par plages, seulement les sections que le contrat nomme.
- **Périmètre** :
  - lit les fichiers du contrat, `direction/LIGNE_EDITORIALE.md`, `direction/ECARTS.md`, `referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 bis (choix des médias), et `direction/references/` pour un besoin précis ;
  - n'ouvre aucun autre épisode, sauf fichiers listés au contrat ;
  - n'écrit rien : le Studio Director consigne ses résultats ;
  - n'envoie jamais l'adresse e-mail du propriétaire à un service externe.
- **Méthode, faits** : sources primaires d'abord (site officiel, presse datée, revue à DOI vérifié sur Crossref). Pour chaque affirmation : source, date de consultation, statut (vérifié, plausible, non vérifié), contradictions. Fait, hypothèse et interprétation sont distingués ; aucune citation, chiffre, date ou témoignage inventé.
- **Méthode, études** : référence complète, ce qu'elles montrent et ne montrent pas (population, méthode) ; une association n'est pas une causalité.
- **Méthode, médias** : ordre de préférence Wikimedia Commons (dernière révision, revue FlickreviewR, licence, SHA-1 par l'API), puis Openverse et Flickr en CC, puis Pexels ou Mixkit. Règles propres à chaque source (Commons, légendes d'auteur Flickr = témoignages, Pexels et Cloudflare, Mixkit `videoRestricted` refusé, FootageCrate, Resource Boy). Règle par défaut (`REFERENTIEL_QUALITE_REALISATION.md` § 2 bis) : choisir sur ce que le média apporte à la scène, gratuit, sans filigrane, jamais de filigrane retiré ni d'accès payant contourné ; vraies vidéos d'événement permises (compétitions listées dans `direction/ECARTS.md`) ; extraits de 6 s au plus ; source exacte notée pour remplacer vite le média.
- **Refus** : média d'une chaîne étudiée comme référence (liste dans `direction/ECARTS.md`), média présenté pour ce qu'il n'est pas, image générée présentée comme archive.
- **Téléchargements** : aucun. Le Studio Director dresse la liste (liens exacts, nom imposé, taille) que le propriétaire valide ; Claude la télécharge ensuite, lui-même ou par `media-fetcher` (0.6.0, validé sur AA, 02/11/2026) ; le propriétaire ne prend que les fichiers refusés (`manuel/`).
- **Livrable** (court, en français) : 1. faits (affirmation · source · statut) ; 2. études (référence · apport · limites) ; 3. médias candidats (lien · auteur · licence · contenu · fonction · risques) ; 4. limites, risques, questions ouvertes ; 5. fichiers locaux lus.

**Liens** : cité par `REGLES_STUDIO.md`, `skills/episode/SKILL.md` (étape 1), `skills/episode/references/socle.md` § 4 ; contrat : [`templates/CONTRAT_MISSION.template.md`](templates.md#templatescontrat_missiontemplatemd).

**À savoir**
- Rapport d'éclaireur (0.5.0) : quand le contrat lui donne celui de Perplexity, l'agent le traite comme une liste de pistes ; il ouvre chaque source et note les pistes écartées (`research.md`, « Rapport d'éclaireur »).
- Le rapport n'arrive pas dans un fichier : il est écrit par le Studio Director dans `episodes/<id>/research/` (`R-*.md`, d'après `skills/episode/SKILL.md`).
- La liste d'ordre de préférence des sources (`research.md:40-49`) indique où chercher d'abord ; la règle par défaut qui suit (`research.md:50`) dit que la licence ne décide plus du choix. Les deux se lisent ensemble : on cherche d'abord dans les sources libres, mais on peut retenir une image non libre en citation encadrée si elle est la meilleure pour la scène.
- Pexels : ouvrir les pages une à une ; un déclenchement Cloudflare ne se contourne jamais.

### agents/reviewer.md
**Rôle** : contrôle qualité en lecture seule d'un script, d'une séquence ou du film contre une liste, avant de les montrer au propriétaire. Il ne valide rien, ne corrige rien, ne déclare jamais avoir vu ou écouté. Ajouté en 0.2.3 (30/10/2026).

**Quand il sert** : lancé par le Studio Director avec un contrat de mission qui nomme l'objet à contrôler et ses fichiers : script (étape 3), séquence (étape 8), film mixé (étape 10) du skill `episode`. Il travaille sur des fichiers : script, minutage, plan de plans, transcriptions, planches, mesures `ffprobe`.

**En-tête**
| Champ | Valeur |
|---|---|
| `name` | `reviewer` |
| `tools` | Read, Grep, Glob, Bash |
| `model` | `sonnet` ; `color` : yellow |
| `skills` | aucun |
| `omitClaudeMd` | absent : il **garde** le `CLAUDE.md` de la chaîne, qui porte les règles qu'il contrôle |
| Rôle du garde-fou | `relecteur` |

**Contenu**
- **Liste de contrôle** : accroche (0 à 30 s : promesse, question) ; structure (séquences, relances, place du renversement) ; durée par rapport à la cible de la chaîne ou du `BRIEF.md` ; ton et registre de la chaîne ; protection des personnes (flou, bip, noms) ; sources et `PROVENANCE.md` ; règles propres de la chaîne (`CLAUDE.md`) et `direction/ECARTS.md`.
- **Lecture** : les fichiers du contrat, le `CLAUDE.md` et le `BRIEF.md` de l'épisode, `direction/LIGNE_EDITORIALE.md`, `direction/ECARTS.md`, le profil du domaine, et la partie des référentiels que l'objet concerne.
- **Interdits** : toute écriture, y compris par Bash (redirection, `cp`, `mv`, `rm`, script en ligne qui écrit) ; les autres épisodes hors contrat.
- **Livrable** (en français, 25 lignes au plus) : tableau point · verdict (`OK`, `À CORRIGER`, `À VÉRIFIER PAR LE PROPRIÉTAIRE`) · minutage · preuve ; les `À CORRIGER` d'abord ; aucun verdict global « conforme » ; dernière ligne : fichiers lus.

**Liens** : `skills/episode/SKILL.md` (« État, reprise et contexte ») et `references/etapes.md` (étapes 3, 8 et 10) ; contrat : [`templates/CONTRAT_MISSION.template.md`](templates.md#templatescontrat_missiontemplatemd).

**À savoir**
- Le hook `garde_commandes.py` lui donne le rôle `relecteur` (0.2.3) : en Bash, seules `ffprobe`, `ffmpeg` de mesure (`-f null`), `wc`, `ls`, `grep`, `head` et `tail`, sans redirection ; il n'a ni Write ni Edit.
- Sa `description` est en français, comme celles des autres agents.

### agents/art-director.md
**Rôle** : direction artistique. Il propose la fiche de style de chaque film et de chaque short (0.7.2, bibliothèque `vendor/lemo-opuscar/`, validé sur AA, 03/11/2026), transforme un script en intention visuelle et en storyboard, ou critique un rendu de façon indépendante. Il ne construit ni ne rend de vidéo. Le propriétaire est le directeur artistique final : l'agent propose, il ne valide pas.

**Quand il sert** : pour la fiche de style de chaque film et de chaque short (0.7.2) ; le reste **seulement à la demande du propriétaire** (`REGLES_STUDIO.md` : critique indépendante des rendus ; storyboard seulement sur demande ; `skills/episode/references/socle.md` § 3). Il choisit lui-même les techniques d'animation et de transition d'un film (validé sur AA, 18/10/2026). Parcours : [`../workflows/critique-da.md`](../workflows/critique-da.md).

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
- Le plugin ne livre aucun gabarit vertical dans `templates/` (seul existe `sequence-gabarit-v3/`). Le « gabarit vertical du kit » est préparé par le Studio Director ; sa source est à vérifier (voir « Écarts »). Décidé le 29/10/2026 : à créer au pilote des shorts.
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
| `omitClaudeMd` | `true` (0.2.3) : démarre sans le `CLAUDE.md` de la chaîne |
| Rôle du garde-fou | `mainteneur` |

**Limites du garde-fou (rôle `mainteneur`)**
- **Aucune écriture par Bash** : toute commande qui a une cible d'écriture probable (redirection, `cp`, `mv`, `tee`, `touch`, `ffmpeg`…) ou dont la tête est une commande d'écriture est refusée ; un script en ligne (`python -c`, `node -e`) qui écrit est refusé. Il écrit avec Write ou Edit.
- Write et Edit refusés dans `.claude/`, un dossier **existant** de `marque/`, `episodes/<id>/inputs/`, un projet de production (`episodes/<id>/production/<…>`) et sur un MP4 existant. Le hook ne protège ni `direction/`, ni `templates/`, ni les `CLAUDE.md` pour ce rôle : c'est le contrat qui borne l'écriture.

**Contenu**
- **Sans `CLAUDE.md` de la chaîne** (`omitClaudeMd`, 0.2.3) : les règles de la chaîne utiles à la mission sont dans son contrat (section « Règles de la chaîne utiles à la mission ») ; sinon il lit, par plages, seulement les sections que le contrat nomme. Il lit toujours, avec Read, les `CLAUDE.md` qu'une mission de cohérence lui demande de contrôler.
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

### agents/strategist.md
**Rôle** (0.4.0, validé sur AA, 02/11/2026) : positionnement et stratégie éditoriale d'une chaîne, hors du contexte du Studio Director. Six phases, une par appel : `dossier` (relevés de l'API YouTube, argent, contraintes), `brief` (question posée au conseil, sièges et poids proposés), `conseil` (protocole roast-room simulé dans un seul contexte, citations vérifiées, verdict noté), `titres`, `sujets` (vérification d'un lot de 9 sujets au plus : verdict, faits sourcés, titre corrigé, drapeau publicité) et `banque` (proposition assemblée, puis `direction/BANQUE_SUJETS.md` après accord du propriétaire).

**Quand il sert** : pour positionner une chaîne (nouvelle ou en relance), écrire une liste de titres, vérifier des sujets candidats ou tenir la banque de sujets. Le Studio Director présente chaque phase au propriétaire par blocs avant la suivante ; plusieurs appels `sujets` peuvent tourner en parallèle sur des lots disjoints.

**En-tête**
| Champ | Valeur |
|---|---|
| `name` | `strategist` |
| `tools` | Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch |
| `model` | `inherit` ; `color` : cyan |
| `skills` | aucun |
| `omitClaudeMd` | `true` : démarre sans le `CLAUDE.md` de la chaîne |
| Rôle du garde-fou | `stratege` |

**Limites du garde-fou (rôle `stratege`)** : Write et Edit seulement dans `docs/` et dans `direction/BANQUE_SUJETS.md` ; en Bash, seules `python` (outils du plugin installé, le chemin du plugin doit figurer dans la commande), `ls`, `wc`, `grep`, `head`, `tail`, `mkdir` et `cd` ; aucun script en ligne ; aucune cible d'écriture hors de `docs/`.

**Contenu**
- Contrat : neuf champs, plus `phase` et `session` (`docs/strategie/<AAAA-MM-JJ>-<sujet>/`) ; section « Règles de la chaîne utiles à la mission » obligatoire. État de la session dans `ETAT.md` (2 Ko au plus), réécrit à chaque fin de phase.
- Outils : `outils/recherche/youtube_chaine.py` (relevé complet d'une chaîne) et `youtube_resume.py` (résumé d'un relevé, sans le lire en entier) ; `vendor/roast-room/` (protocole, cerveaux, consignes des sièges, `check_quotes.py`).
- Leçons d'AA intégrées : coût d'un conseil de six sièges en agents séparés (environ 1,73 M de tokens), mots absolus des titres souvent faux, prémisses dépassées, argent jamais dans la promesse quand la ligne l'interdit.
- **Livrable** : synthèse de 300 mots au plus (phase, fichiers, décisions en blocs, coût, limites, fichiers lus).

**À savoir**
- Les sièges sont simulés dans le contexte de l'agent, donc sans indépendance réelle ; le verdict le dit. Un agent ne peut pas lancer d'autres agents.
- Aucun siège du roster n'est un spécialiste de YouTube : le dossier de faits apporte les chiffres de YouTube aux sièges.

---

### agents/media-fetcher.md
**Rôle** (0.6.0, validé sur AA, 02/11/2026, Q56 et Q57 de son E011) : télécharger les médias d'une **liste validée par le propriétaire**, dans le kit de l'épisode, sous le nom imposé, et rendre un manifeste. Il ne cherche, ne choisit et ne juge aucun média (`research` et le Studio Director). Règle : `REFERENTIEL_QUALITE_REALISATION.md` § 2 bis, « téléchargement des médias ».

**Quand il sert** : à l'étape 5 (médias du socle), quand le Studio Director préfère ne pas porter le téléchargement dans son contexte. Le Studio Director peut aussi lancer lui-même l'outil.

**En-tête**
| Champ | Valeur |
|---|---|
| `name` | `media-fetcher` |
| `tools` | Read, Write, Bash, Glob, Grep (ni WebSearch, ni Edit) |
| `model` | `sonnet` ; `color` : orange |
| `skills` | aucun |
| `omitClaudeMd` | `true` : démarre sans le `CLAUDE.md` de la chaîne |
| Rôle du garde-fou | `telechargeur` |

**Limites du garde-fou (rôle `telechargeur`)** : Write et Edit seulement sous `episodes/<id>/kit/media/source-vN/` ; en Bash, seule `python` sur `outils/medias/telecharger_medias.py` du plugin installé (le chemin du plugin doit figurer en entier dans la commande ; la liste se lit sous `episodes/<id>/kit/`, le dépôt et le manifeste s'écrivent sous `source-vN/`), plus `ls`, `wc`, `grep`, `head`, `tail`, `mkdir`, `cd` ; aucun script en ligne, ni `curl` ni `wget`. Essai : `outils/test_garde_commandes.py`.

**Contenu**
- Contrat : neuf champs, plus la **liste JSON**, la décision datée du propriétaire qui la valide, le dépôt `kit/media/source-vN/` et le **robot** (`--agent-utilisateur` : nom et adresse de la chaîne, jamais une adresse e-mail) ; section « Règles de la chaîne utiles à la mission » obligatoire.
- Méthode : vérifier la liste, aperçu sans `--executer`, puis téléchargement par l'outil, puis manifeste.
- Interdits : aucun contournement (Cloudflare, accès payant, connexion, CAPTCHA, filigrane, autre adresse) ; aucun fichier hors de la liste ; aucun fichier de YouTube ni son de Soundza (clé du propriétaire et outils MCP : Claude principal ou `sound-manager`) ; aucune vérification d'image (dimensions, planche, `PROVENANCE.md` : Studio Director).
- **Livrable** : manifeste (réf. · fichier · SHA-1 · taille · statut), liste « à télécharger par le propriétaire » (`manuel/`), écarts, risques.

**À savoir**
- Un fichier refusé n'est jamais retenté autrement : l'outil l'écrit dans `manuel/A_TELECHARGER_PAR_LE_PROPRIETAIRE_<date>.md`.
- Un plugin ignore le champ `mcpServers` : l'agent n'a pas les outils du serveur `soundza`. Les sons de Soundza sont pris par Claude principal ou, depuis la 0.7.0, par `sound-manager`.

---

### agents/sound-manager.md
**Rôle** (0.7.0, décision du propriétaire, validé sur AA, 03/11/2026) : **tout le travail sonore d'un épisode**, c'est-à-dire :
- les prises de voix, préparées et chiffrées ;
- le contrôle du texte des prises, le ralentissement et les repères mot à mot ;
- le choix et le téléchargement des sons d'une liste validée (`marque/son/`, Soundza) ;
- le repérage, le plan de cues, le plan son JSON du film et les mesures.

Il ne lance **ni l'appel payant** (Claude principal, après la confirmation du propriétaire ; `DIRECTION_AUDIO.md` § 4) **ni le mix** (`mix_film.py`, environ 6 min, lancé par Claude principal en tâche de fond) : il écrit la commande et s'arrête, comme `motion-producer` à `render.sh`. Il ne lance pas non plus **son propre script de mesure** (décision du 03/11/2026 : le garde ne lit pas un script) : il l'écrit sous `montage/mesures-vN/` et donne la commande ; Claude principal le relit, le lance, puis le relance pour la suite. Il n'écoute pas.

**Quand il sert** : étapes 4 (voix), 10 (mix) et 11 (retours de son) du skill `episode`.

**En-tête**
| Champ | Valeur |
|---|---|
| `name` | `sound-manager` |
| `tools` | Read, Write, Edit, Grep, Glob, Bash, Skill, ToolSearch, les cinq outils de lecture et de téléchargement du serveur Soundza (`search_sounds`, `get_sound`, `download_sound`, `search_packs`, `get_pack`), sans `generate_sound` |
| `disallowedTools` | `mcp__soundza__generate_sound` (génération par IA : jamais sans demande du propriétaire) |
| `model` | `opus` ; `color` : red |
| `skills` | `studio-faceless:direction-sonore` (méthode par défaut de la musique : `references/musique-par-cues.md`) |
| `omitClaudeMd` | absent : lit le `CLAUDE.md` de la chaîne |
| Rôle du garde-fou | `ingenieur-son` |

**Limites du garde-fou (rôle `ingenieur-son`)**
- **Écriture** (Write, Edit et Bash), dans l'épisode seulement : `kit/voix/`, `kit/shorts/voix/`, `kit/shorts/son/`, `kit/media/audio/`, `kit/media/source-vN/soundza/`, `kit/PROVENANCE.md`, `montage/` (sauf `montage.json`) et `outputs/controle-son*/`. Aucun MP4, aucun média existant écrasé.
- **Bash** : `python` sur les outils de la table `OUTILS` du hook :
  - `generer_voix.py` à blanc seulement, `info_elevenlabs.py` ;
  - `transcrire.py`, `ralentir.py`, `pauses.py`, `raccourcir.py`, `recaler.py`, `mesurer_sons.py` ;
  - `controle.py niveau | son | voix-reste`, `publication.py mot` ;
  - `telecharger_medias.py` vers `soundza/`.
- Un script de l'agent (sous `montage/mesures-vN/`) s'écrit avec Write mais ne se lance pas : `python` sur un script de la zone est refusé (« un script de l'agent est relu et lancé par Claude principal »). Outil `mesurer_mix.py` prévu en 0.7.2.
- Autres commandes : `ffmpeg` (sans `-y`, chaque sortie dans la zone, `file=` des filtres compris), `ffprobe`, `cp` (`-n`, `-p`, sans écrasement), `ls`, `wc`, `grep`, `head`, `tail`, `mkdir`, `date`, `sha1sum`, `sha256sum`, `cd` vers la racine.
- Les options des outils sont lues par leur nom entier (une option abrégée ou inconnue est refusée), et chaque chemin d'écriture est contrôlé, avec une espace, sans barre oblique ou en `--option=valeur`.
- Refusés : `mix_film.py`, `assembler.py`, `--executer` et `--confirme-credits` de `generer_voix.py`, ses propres scripts, les scripts en ligne et les substitutions de commande.
- Essai : `outils/test_garde_commandes.py`.

**Contenu** : contrat (phase A voix, B sons et plan son, C mesures, D retours ; décisions validées datées) ; lectures limitées à l'épisode et à `marque/son/` ; méthode par phase ; économie de contexte (4 min, 300 k, `montage/ETAT_SON.md`) ; interdits ; livrable en 6 points.

---

### agents/publisher.md
**Rôle** (0.7.0, décision du propriétaire, validé sur AA, 03/11/2026 : « un agent fort pour la création de miniature ») : **la miniature d'abord**, puis le dossier de publication.
- Miniature :
  - concepts véridiques ;
  - méthode en trois calques (`thumbnail-strategist`, `references/trois-calques-e011.md`) ;
  - détourage par `remove-background` (voie A de `fabrication.md` § 3) ;
  - rendu `miniature.py`, contrôles et planche ;
  - au moins 2 variantes pour Test & Compare.
- Dossier de publication : skill `youtube-seo`.
- Il **ne crée aucun titre** : le titre vient de `strategist`, validé par le propriétaire. Il ne publie, ne téléverse et ne modifie rien sur la chaîne.

**Quand il sert** : étape 12 du skill `episode`.

**En-tête**
| Champ | Valeur |
|---|---|
| `name` | `publisher` |
| `tools` | Read, Write, Edit, Grep, Glob, Bash, Skill |
| `model` | `opus` ; `color` : blue |
| `skills` | `studio-faceless:thumbnail-strategist`, `studio-faceless:youtube-seo` |
| `omitClaudeMd` | absent : lit le `CLAUDE.md` de la chaîne |
| Rôle du garde-fou | `editeur` |

**Limites du garde-fou (rôle `editeur`)**
- **Écriture** dans l'épisode seulement : `miniatures-vN/`, `PUBLICATION_vN.md` et `PUBLICATION_vN.<langue>.srt`. Une image existante ne s'écrase pas.
- **Bash** : `python` sur `miniature.py` (rendu, mesure, planche, grille, contraste), `publication.py` (verifier, chapitres, mot), `srt.py` et `controle.py chrome`. Le script du masque Pillow s'écrit sous `miniatures-vN/travail/` mais ne se lance pas (refusé, décision du 03/11/2026) : l'agent s'arrête et donne la commande ; Claude principal le relit, le lance, regarde le contrôle sur fond vert, puis relance l'agent pour le rendu (`miniature.py masque` prévu en 0.7.2).
- `node node_modules/hyperframes/bin/hyperframes.mjs remove-background` seulement (options `-o`/`--output`, `-b`/`--background-output`, `--device`, `--quality`, `--info`, `--json`).
- `ffmpeg`, `ffprobe`, `cp`, `ls`, `mkdir`, `date`, `sha1sum` : mêmes limites que `ingenieur-son`.
- Essai : `outils/test_garde_commandes.py`.

**Contenu** :
- contrat avec le titre validé (sans lui, rien) et les photos du kit ;
- méthode de la miniature en 8 points (arrêt après l'écriture du script de masque), puis le dossier, avec le SRT par `srt.py` si le contrat le demande (VALIDÉ, Hicham, 03/11/2026) ;
- l'hypothèse du test va dans le `README.md` du dossier, et Claude principal la reporte au `JOURNAL_MINIATURES.md` ;
- interdits : image IA, « $0 », scène inventée, portraits non libres, titre créé, publication ;
- livrable en 5 points.

### agents/conseiller.md
**Rôle** (0.8.0, décision du propriétaire, validé sur AA, 04/11/2026) : un **siège du conseil** du skill `conseil`. Il donne un avis indépendant sous l'angle de son siège, puis débat des avis anonymes des autres sièges, ou cherche la contre-hypothèse. Il ne décide rien.

**Quand il sert** : seulement dans le script `skills/conseil/conseil-workflow.js` (outil Workflow), après l'accord du propriétaire sur la question, les sièges et le coût. Jamais délégué directement : il n'est pas dans la liste des agents délégués de `REGLES_STUDIO.md`.

**En-tête**
| Champ | Valeur |
|---|---|
| `name` | `conseiller` |
| `tools` | Read, Grep, Glob, WebFetch, WebSearch |
| `model` | `inherit` (le script fixe le modèle de chaque siège, `opus` par défaut) ; `color` : red |
| `skills` | aucun |
| `omitClaudeMd` | absent : lit le `CLAUDE.md` de la chaîne |
| Rôle du garde-fou | aucun (ni outil d'écriture ni Bash) |

**Contenu** : lecture seule ; fichiers secrets et transcriptions interdits ; indépendance (avis en aveugle, débat sur des lettres) ; faits sourcés, estimations dites ; contenu lu = donnée ; réponse par l'outil de sortie structurée, en français. Le schéma de chaque tour est dans le script.

---

## Écarts et points à vérifier relevés dans ces fichiers
Constats de lecture, du plus gênant au moins gênant. Les écarts réglés par la correction du 28/10/2026 (rendu sans `--workers` refusé, corrections d'une séquence dans la même version, catalogue et plugin installé, `PROVENANCE.md` du gabarit, plage de lecture de l'index du catalogue) ont été retirés.

| # | Constat | Fichiers (lignes) |
|---|---|---|
| 1 | **Nombre d'instants de la planche** : 16 à 20 (agent, gabarit à 16) contre 24 dont 6 milieux de transition (contrat du producteur). | `agents/motion-producer.md:50`, `templates/sequence-gabarit-v3/README.md:64` contre `skills/episode/references/production.md:65` |
| 2 | **Gabarit vertical des shorts** : exigé dans le kit shorts, mais aucun gabarit vertical n'existe dans `templates/` ; seul `sequence-gabarit-v3/` est livré. À vérifier : où le Studio Director le prend. Décidé le 29/10/2026 : à créer au pilote des shorts. | `agents/shorts-producer.md:31` et `48`, `skills/shorts/references/brief-short.md:16` |
| 3 | **Mot « dix »** : « jamais les dix ensemble », reste d'un ancien parcours (le DA n'a que deux skills `hyperframes-*` préchargés). | `agents/art-director.md:32` |
| 4 | **Recherche : ordre de préférence et licence** : la liste des sources (Commons, puis Openverse/Flickr, puis Pexels/Mixkit) cohabite avec la règle « la licence ne compte pas » ; à lire ensemble (voir fiche). | `agents/research.md:33-43` |
| 5 | **`CLAUDE.md` sous Linux ou macOS** : le hook compare `parts[-1] == 'claude.md'` après `os.path.normcase`, qui ne met pas en minuscules hors Windows ; la protection des `CLAUDE.md` par Write/Edit ne s'y déclencherait pas pour `CLAUDE.md`. À vérifier si une chaîne tourne hors Windows. | `hooks/garde_commandes.py:96`, `108` |
| 6 | **`omitClaudeMd` et version de Claude Code** : le champ demande la 2.1.271 ou plus ; l'application de bureau fait tourner son propre Claude Code (2.1.309 le 02/11/2026), où il devrait agir (déduit de la version) ; seule la copie du terminal peut être plus ancienne (2.1.169 sur la machine de mise au point) : `research`, `studio-maintainer`, `strategist` et `media-fetcher` y garderaient le `CLAUDE.md`. | `agents/research.md`, `agents/studio-maintainer.md`, `agents/strategist.md` |
