# Squelette de chaîne (`starter/`) et fichiers de la racine du dépôt

Cette page décrit chaque fichier du squelette `plugins/studio-faceless/starter/` (copié une fois pour créer une chaîne) et chaque fichier de la racine du dépôt du plugin (installation, catalogue, journal, contrôle avant commit), plus le manifeste du plugin.

## Table des matières
- [Vue d'ensemble](#vue-densemble)
- [Le squelette `starter/`](#le-squelette-starter)
  - [Racine du squelette](#racine-du-squelette) : `CLAUDE.md`, `package.json`, `package-lock.json`, `requirements.txt`, `.gitignore`, `.gitattributes`
  - [`.claude/`](#claude) : `settings.json`
  - [`.githooks/`](#githooks) : les cinq crochets
  - [`direction/`](#direction) : `LIGNE_EDITORIALE.md`, `ECARTS.md`
  - [`marque/`](#marque) : `README.md`, `couleurs_interdites.json`, `son/README.md`
- [Racine du dépôt du plugin](#racine-du-dépôt-du-plugin) : `README.md`, `INSTALLATION.md`, `NOUVELLE_CHAINE.md`, `CHANGELOG.md`, `.gitattributes`, `.gitignore`, `.githooks/pre-commit`, `.claude-plugin/marketplace.json`, `plugin.json`
- [Squelette contre dépôt du plugin : ce qui diffère](#squelette-contre-dépôt-du-plugin--ce-qui-diffère)
- [Points à vérifier et incohérences](#points-à-vérifier-et-incohérences)

## Vue d'ensemble
Il y a **deux dépôts Git distincts** :
- le **dépôt du plugin** (`studio-faceless`, privé) : contient le plugin, son squelette, sa documentation. Aucun fichier en Git LFS (une installation de plugin ne télécharge pas le contenu LFS) ;
- le **dépôt d'une chaîne** (un par chaîne, privé) : créé en copiant `starter/`. Il reçoit les règles du plugin par l'installation, garde son identité (`CLAUDE.md`, `direction/`, `marque/`) et ses `episodes/`. Ses binaires de marque sont en Git LFS.

Le squelette ne contient que ce qui doit vivre **dans la chaîne** (un plugin ne peut ni fournir de permissions, ni contenir de fichiers en Git LFS, ni lire hors de son dossier : [`../ARCHITECTURE.md`](../ARCHITECTURE.md)). Il ne contient pas `episodes/`, `templates/` ni `docs/` : les modèles viennent du plugin (`${CLAUDE_PLUGIN_ROOT}/templates/`), `episodes/<id>/` se crée au premier épisode.

Arborescence du squelette (17 fichiers) :
```
starter/
  CLAUDE.md                  .gitignore        .gitattributes
  package.json               package-lock.json requirements.txt
  .claude/settings.json
  .githooks/                 pre-commit  post-checkout  post-commit  post-merge  pre-push
  direction/                 LIGNE_EDITORIALE.md  ECARTS.md
  marque/                    README.md  couleurs_interdites.json  son/README.md
```
Parcours qui l'utilise : [`../workflows/nouvelle-chaine.md`](../workflows/nouvelle-chaine.md) (création) et [`../workflows/installation-et-mise-a-jour.md`](../workflows/installation-et-mise-a-jour.md) (branchement d'une chaîne existante).

## Le squelette `starter/`

### Racine du squelette

#### starter/CLAUDE.md
- **Rôle** : modèle du `CLAUDE.md` de la chaîne : identité, propriétaire, langues, public, voix, règles propres, état. Les règles communes arrivent du plugin ; ce fichier les complète et **l'emporte en cas de conflit**.
- **Quand il sert** : recopié à la création de la chaîne, rempli avec le propriétaire par une porte de questions (skill `studio-faceless:grilling`), tout en `PROPOSÉ`. Ensuite, Claude Code le charge à chaque session dans la chaîne ; il nomme le **propriétaire** (celui qui décide et valide, partout où le plugin dit « le propriétaire »).
- **Contenu** (placeholders `<…>` à remplacer) :
  | Section | À remplir |
  |---|---|
  | Titre + phrase d'ouverture | nom de la chaîne ; une phrase : genre, promesse, public |
  | Identité | propriétaire (prénom) ; langues (documents internes / ce que voit ou entend le spectateur) ; public ; voix de synthèse retenue (service, nom, réglages) |
  | Quoi lire (propre à la chaîne) | tableau : `direction/LIGNE_EDITORIALE.md`, `direction/ECARTS.md`, `marque/README.md` et `marque/son/README.md`, `episodes/<id>/CLAUDE.md` |
  | Règles propres à la chaîne | chaque règle avec statut et date (ex. « VALIDÉ, <propriétaire>, JJ/MM/AAAA ») ; une règle qui modifie une règle du plugin va dans `direction/ECARTS.md` |
  | État | épisode en cours et son étape ; renvoi au `CLAUDE.md` de l'épisode |
- **Liens** : cite `direction/LIGNE_EDITORIALE.md`, `direction/ECARTS.md`, `marque/README.md`, `marque/son/README.md`. Le modèle du `CLAUDE.md` d'épisode est `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.episode.template.md` ([`templates.md`](templates.md)).
- **À savoir** : le squelette ne recopie pas les règles communes (statuts, sous-agents, garde-fou, tokens) : elles sont injectées au début de chaque session par `REGLES_STUDIO.md` ([`outils-et-garde.md`](outils-et-garde.md)). Garder ce fichier court.

#### starter/package.json
- **Rôle** : déclare l'unique dépendance Node de la chaîne : **HyperFrames 0.8.149**, version exacte (sans `^` ni `~`).
- **Quand il sert** : `npm ci` l'installe (propriétaire ou Claude avec son accord). Les gabarits (`render.sh` du gabarit de séquence v3) vérifient que `node_modules/hyperframes/package.json` porte exactement `0.8.149`. La version de ce fichier **fait foi** (définition de `studio-maintainer`).
- **Contenu** : `name` `ma-chaine` (à remplacer), `version` `0.1.0`, `private: true`, `devDependencies.hyperframes: "0.8.149"`. Aucun script npm.
- **À savoir** : aucune mise à jour (`upgrade`, `skills update`, `npm install` d'une autre version) sans décision du propriétaire ; le garde-fou la refuse. La version de HyperFrames est écrite à plusieurs endroits du plugin : voir [`../workflows/faire-evoluer-le-plugin.md`](../workflows/faire-evoluer-le-plugin.md).

#### starter/package-lock.json
- **Rôle** : fige l'arbre complet des dépendances de `package.json`, pour que `npm ci` installe exactement la même chose partout. Version figée de HyperFrames : **0.8.149** (entrée `node_modules/hyperframes`, licence Apache-2.0, moteur Node `>=22`).
- **Quand il sert** : par `npm ci` seulement. Ne se modifie jamais à la main.
- **Contenu** : `lockfileVersion` 3, 125 entrées `node_modules/…`, toutes `dev: true`.
- **À savoir** : le champ `name` du lock est `apparently-athletic-studiov1` (lignes 2 et 8) alors que `package.json` dit `ma-chaine` : reste d'AA dans un plugin censé n'avoir aucun nom de chaîne. `npm ci` ne contrôle que les dépendances, mais **à vérifier** avant la première installation d'une nouvelle chaîne.

#### starter/requirements.txt
- **Rôle** : dépendances Python des outils du plugin, les seuls imports hors bibliothèque standard.
- **Contenu** : `numpy>=2.4`, `scipy>=1.17`. En commentaire : testé le 14/10/2026 avec Python 3.14.5, numpy 2.4.6, scipy 1.17.1.
- **Quand il sert** : `pip install -r requirements.txt` à l'installation d'une chaîne ([`../workflows/installation-et-mise-a-jour.md`](../workflows/installation-et-mise-a-jour.md)). `numpy` est importé par `controle/controle.py`, `controle/ralentir.py`, `montage/assembler.py`, `montage/mix_film.py` et `shorts/` (`master_short.py`, `raccord.py`, `recaler.py`, `voix_short.py`) ; `scipy` par `montage/assembler.py`, `montage/mix_film.py` et `shorts/master_short.py`. Les outils sont décrits dans [`outils-et-garde.md`](outils-et-garde.md).
- **À savoir** : le propriétaire décide de toute installation ; le garde-fou ne bloque pas `pip`, la règle générale du plugin est « aucune dépendance supplémentaire sans nécessité ».

#### starter/.gitignore
- **Rôle** : liste ce qui n'entre **jamais** dans le dépôt de la chaîne (règles du plugin validées sur AA, 21/10/2026). Le dépôt garde le texte (code, configuration, gabarits, directives, fiches) ; médias, rendus et archives vont dans la sauvegarde externe.
- **Quand il sert** : à chaque `git add` / `git status`, et par le contrôle `verifier_depot.py --tout` (fichiers « que Git suivrait »).
- **Contenu** :
  - dépendances et caches : `node_modules/`, `__pycache__/`, `*.pyc` ;
  - réglages personnels : `.claude/settings.local.json` ;
  - corbeille d'archivage : `_A_SUPPRIMER/`, `*.zip`, `*.partiel` ;
  - médias d'épisode sous `episodes/**/` : vidéos (`mp4`, `mov`, `webm`, `mkv`, `qt`), sons (`wav`, `mp3`, `m4a`, `aac`, `flac`), images (`png`, `jpg`, `jpeg`, `webp`, `gif`, `tif`, `tiff`), `pdf`, polices (`ttf`, `otf`, `woff`, `woff2`) ;
  - `episodes/*/inputs/media/` (médias téléchargés à la main et pages enregistrées ; validé sur AA, 26/10/2026) ;
  - `direction/references/**/captures/` (captures d'études de chaînes tierces, médias d'un tiers) ;
  - sorties de travail : `episodes/*/outputs/`, `planche/`, `planches/`, `controle/`, `controles/`, `snapshots/`, `captures/` ;
  - modèles et mesures lourdes : `*.bin`, `*.npz`, `*.f32` ;
  - système : `Thumbs.db`, `desktop.ini`, `.DS_Store`.
- **À savoir** : les médias de `marque/` ne sont **pas** ignorés : ils passent en Git LFS (`.gitattributes`). Les images d'un épisode sont ignorées partout : une miniature ou une planche à garder doit être sauvegardée à part (`outils/sauvegarde-chaine.ps1`, voir [`../workflows/archivage-et-sauvegarde.md`](../workflows/archivage-et-sauvegarde.md)).

#### starter/.gitattributes
- **Rôle** : fins de ligne, binaires et règles Git LFS de la chaîne.
- **Contenu** :
  - `* text=auto` ; `*.sh` et `.githooks/*` en LF ; `*.ps1` en CRLF ;
  - `binary` pour `png`, `jpg`, `jpeg`, `webp`, `gif`, `mp3`, `wav`, `mp4`, `mov`, `webm`, `ttf`, `otf`, `woff`, `woff2` ;
  - **LFS** pour `marque/**` : `mp4`, `mov`, `wav`, `mp3`, `png`, `jpg`, `ttf` ; et pour `templates/**` : `mp4`, `wav`, `mp3`, `png`, `jpg`, `ttf`.
- **Quand il sert** : par Git à chaque ajout ; par `verifier_depot.py`, qui lit l'attribut `filter` pour accepter un gros fichier s'il passe par LFS (limite 10 Mo hors LFS).
- **À savoir** :
  - un fichier de `marque/` en `.webp`, `.gif`, `.otf`, `.woff2` ou `.jpeg` n'est **pas** en LFS (il est seulement `binary`) : au-delà de 10 Mo, le contrôle avant commit le refuse ;
  - les règles `templates/**` sont **sans objet dans une chaîne créée depuis le squelette** (les modèles restent dans le plugin) ; héritage probable de StudioV1, où `templates/` existait (à vérifier, voir plus bas).

### `.claude/`

#### starter/.claude/settings.json
- **Rôle** : réglages du projet pour Claude Code : déclare le catalogue du plugin, l'active et pose les permissions de la chaîne. Un plugin ne peut pas fournir de permissions : elles vivent ici.
- **Quand il sert** : lu par Claude Code à l'ouverture du dossier, **après confirmation de la confiance du dossier** (sans elle, le catalogue déclaré est ignoré).
- **Contenu** :
  | Clé | Valeur |
  |---|---|
  | `extraKnownMarketplaces.studio-faceless.source` | GitHub, dépôt `hichamsbihi/studio-faceless` |
  | `enabledPlugins` | `studio-faceless@studio-faceless: true` |
  | `permissions.allow` | HyperFrames par Node (`node node_modules/hyperframes/bin/hyperframes.mjs *`, avec ou sans préfixe) et `npx hyperframes *` ; `* render.mjs*` ; `mix.py` en huit variantes (`python`, `python -B`, `python -I -B`, `python3`, `py`, avec ou sans chemin) |
  | `permissions.deny` | `rm -rf`, `rm -fr`, `rm -r` ; `npm install`, `npm i`, `npm uninstall`, `npm update` ; `npx hyperframes@*` (autre version) ; `npx hyperframes` + `publish`, `cloud`, `cloudrun`, `lambda`, `auth`, `upgrade` |
- **Liens** : doublé par le garde-fou du plugin (`hooks/garde_commandes.py`, [`outils-et-garde.md`](outils-et-garde.md)), qui refuse aussi `npm add`, `hyperframes skills update`, etc. et **demande confirmation** pour `preview` ; il **refuse** un rendu sans `--workers 1` ou `2`.
- **À savoir** :
  - **aucune règle `ask` n'est fournie** : le connecteur ElevenLabs de la session doit y être ajouté à la main (`mcp__<identifiant>`), car l'identifiant dépend du compte ([`../../INSTALLATION.md`](../../INSTALLATION.md), § 4, point 6) ;
  - les règles `mix.py` et `render.mjs` viennent du gabarit v2 de StudioV1 ; le gabarit v3 du plugin n'a plus de `mix.py` (voix seule) mais la méthode des shorts le cite encore (`skills/shorts/references/montage-vertical.md`) : à vérifier avant de les retirer ;
  - le dépôt du catalogue est en dur (`hichamsbihi/studio-faceless`) : à changer si le dépôt est transféré.

### `.githooks/`
Le dossier est activé par `git config core.hooksPath .githooks` (étape de [`nouvelle-chaine.md`](../workflows/nouvelle-chaine.md)). Cinq crochets, tous en LF.

#### starter/.githooks/pre-commit
- **Rôle** : contrôle de chaque commit par `verifier_depot.py` du plugin installé.
- **Quand il sert** : automatiquement à chaque `git commit` dans la chaîne.
- **Contenu / usage** :
  1. si `STUDIO_FACELESS_OUTILS` est défini, utilise `$STUDIO_FACELESS_OUTILS/verifier_depot.py` ;
  2. sinon cherche `~/.claude/plugins/cache/studio-faceless/studio-faceless/*/outils/verifier_depot.py` et prend la **version la plus haute** (`sort -V | tail -1`) ;
  3. si introuvable : message « verifier_depot.py introuvable : le plugin studio-faceless est-il installé ? » et **sortie 1** (commit refusé) ;
  4. sinon `exec python -I -B "$V"`.
- **Ce que contrôle `verifier_depot.py`** (exit 0 = rien à signaler, 1 = refus ; bibliothèque standard seule) : fichier de plus de 10 Mo hors LFS ; média d'épisode sous `episodes/` ; secret probable (clé d'API, jeton GitHub, clé privée, en-tête Bearer) ; chemin propre à une machine dans du code actif. Détails : [`outils-et-garde.md`](outils-et-garde.md).
- **À savoir** : si plusieurs versions du plugin sont dans le cache, le crochet prend la plus haute, pas forcément celle qui est installée.

#### starter/.githooks/post-checkout, post-commit, post-merge, pre-push
- **Rôle** : les quatre crochets standard de **Git LFS** (générés par `git lfs install`, copiés ici parce que `core.hooksPath` remplace `.git/hooks`). Chacun vérifie que `git-lfs` est dans le PATH, puis appelle `git lfs post-checkout`, `post-commit`, `post-merge` ou `pre-push` avec ses arguments.
- **Quand ils servent** : à chaque checkout, commit, merge et push. `pre-push` envoie les objets LFS avant l'envoi des commits.
- **À savoir** : si `git-lfs` n'est pas installé, chaque crochet affiche son message et **sort avec le code 2**, ce qui bloque l'opération Git. D'où le prérequis « Git pour Windows, avec Git LFS » ([`../../INSTALLATION.md`](../../INSTALLATION.md)).

### `direction/`

#### starter/direction/LIGNE_EDITORIALE.md
- **Rôle** : squelette de la ligne éditoriale de la chaîne : ce qui est propre à elle (identité, public, territoires, principes, personnalité, sujets). La méthode de récit est celle du plugin (`METHODE_RECIT.md`).
- **Quand il sert** : rempli à la création de la chaîne (porte de questions), puis lu pour toute mission de recherche, de sujet ou de storytelling. Le registre des sujets y est tenu à jour à chaque épisode.
- **Contenu** :
  | Section | Statut au départ | À écrire |
  |---|---|---|
  | Identité et public | à fixer | format, public (qui, langue, niveau), mission, ambition, exclusions (présentateur, avatar, mascotte…) |
  | Promesse | provisoire | une ou deux phrases ; « provisoire » tant que le propriétaire n'a pas validé |
  | Territoires | à fixer | thèmes prioritaires et complémentaires ; ce que la chaîne n'est pas ; quota ou calendrier |
  | Principes | à fixer | question centrale, récit contre explication, sources et limites, conclusion |
  | Personnalité narrative | à valider | ton, slogan, voix du guide, place de l'humain, rythme, rigueur, fin ; date et accord |
  | Ambition audiovisuelle | orientation | niveau visé, moteur de rendu, documents de référence, études consultées |
  | Sujets | — | un sous-titre par sujet : titre, question de travail, origine, angle, état, renvoi `episodes/<id>/BRIEF.md` ; candidat, choisi ou publié |
  | Décisions ouvertes | — | ce qui reste à décider |
  | Registre des décisions | — | tableau Élément · Statut · Fondement |
- **Liens** : cite `${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md`, `REFERENTIEL_QUALITE_REALISATION.md`, `DIRECTION_AUDIO.md` ; renvoie à `direction/ECARTS.md`.
- **À savoir** : ne valide aucun épisode ni aucune mise en production. Les statuts utilisés sont ceux de `REGLES_STUDIO.md` : `FIXÉ`, `VALIDÉ` (date et référence), `PROPOSÉ`, `PROVISOIRE`, `QUESTION OUVERTE`.

#### starter/direction/ECARTS.md
- **Rôle** : liste des **écarts de la chaîne aux règles par défaut** du plugin. **Un écart ici l'emporte sur la règle par défaut** ; ce qui n'y figure pas suit la règle par défaut.
- **Quand il sert** : lu par tous les agents (`research`, `art-director`, `motion-producer`…) en plus des référentiels ; complété quand le propriétaire décide qu'une règle du plugin ne vaut pas pour sa chaîne. Vide au départ.
- **Contenu** : le format d'une ligne d'écart, puis cinq sections, une par référentiel :
  - **Format** : `§ visé : règle de la chaîne (statut, date)`. `§ visé` = numéro de section du référentiel, ou « Ajout » pour une règle que le référentiel ne contient pas ; `statut` = `FIXÉ`, `VALIDÉ` (propriétaire), `PROPOSÉ`, `PROVISOIRE` ou `QUESTION OUVERTE` ; `date` = jour de la décision, avec la référence si elle existe.
  - **METHODE_RECIT** : écarts aux § 1 à 5.
  - **REFERENTIEL_QUALITE_REALISATION** : écarts ; contient aussi le **§ 5 (référence d'étude)** et le **§ 6 (décisions ouvertes)**, propres à chaque chaîne.
  - **DIRECTION_AUDIO** : écarts ; contient aussi la **voix retenue (§ 1)**, ses réglages, les essais de musique et la bibliothèque de sons.
  - **MOTION_CATALOG** : écarts ; contient aussi les techniques que la chaîne ajoute (une ligne d'index et une fiche de deux ou trois phrases) et les épisodes qui ont repris une technique.
- **À savoir** : c'est le seul endroit où une chaîne s'écarte d'une règle commune. Une règle bonne pour toutes les chaînes ne s'écrit pas ici : elle se propose pour le plugin ([`../workflows/faire-evoluer-le-plugin.md`](../workflows/faire-evoluer-le-plugin.md)).

### `marque/`

#### starter/marque/README.md
- **Rôle** : squelette de la fiche de marque : éléments d'identité, couleurs, polices, réemploi.
- **Quand il sert** : rempli à la création de la chaîne ; lu par le directeur artistique, le producteur et le Studio Director (signature, appels, outro, couleurs). Les référentiels y renvoient pour les polices, les couleurs et l'arrière-plan.
- **Contenu** :
  - **Règle de versionnage** : chaque élément vit dans son dossier `<element>-vN/` ; un dossier existant ne se modifie jamais, une nouvelle version va dans un nouveau dossier ; les binaires sont en Git LFS.
  - **Éléments** (tableau Élément · Dossier · Statut) : logo et bannière (`identite-chaine-01/`), signature après l'intro (`<signature-vN>/`), appel Like + Subscribe (`<appel-vN>/`), outro (`<outro-vN>/`).
  - **Couleurs** : couleurs de marque (logo, signature, outro) ; films = un socle fixe et une palette par histoire, décidée en direction artistique avec une planche d'essai ; couleurs interdites dans `couleurs_interdites.json`.
  - **Polices des films** : polices retenues avec licence (SIL OFL de préférence).
  - **Réemploi dans un épisode** : on copie l'élément dans le kit de l'épisode ; sa provenance va dans le `PROVENANCE.md` du kit.
- **Liens** : `marque/couleurs_interdites.json`, `controle.py couleurs`. Cité par `REFERENTIEL_QUALITE_REALISATION.md` § 2 ter et `MOTION_CATALOG.md`.
- **À savoir** : un dossier existant de `marque/` est protégé par le garde-fou (producteurs et mainteneur n'y créent pas de fichier dans un dossier existant).

#### starter/marque/couleurs_interdites.json
- **Rôle** : couleurs que les films de la chaîne ne doivent pas employer (ex. une palette associée à un autre produit).
- **Quand il sert** : lu par `outils/controle/controle.py` au chargement ; la sous-commande `couleurs` l'applique à des fichiers.
- **Contenu** : un objet JSON `{"nom": "#RRGGBB"}`. Livré **vide** (`{}`) : aucune couleur interdite.
- **Usage du contrôle** (depuis la racine de la chaîne) :
  ```bash
  python -B "<plugin>/outils/controle/controle.py" couleurs <fichier.html> [<fichier2> …]
  ```
  Chaque ligne de chaque fichier est testée contre l'hexadécimal `#rrggbb` et contre `rgb(r, g, b)` / `rgba(r, g, b…)`. Sortie : `fichier:ligne : nom → texte` pour chaque occurrence ; **code 1** s'il y en a, 0 sinon. Message « Aucune couleur interdite déclarée » si le fichier est absent ou vide. La signature et l'outro gardent les couleurs de marque.
- **À savoir** : le fichier est lu dans `CLAUDE_PROJECT_DIR` (sinon le dossier courant), sous `marque/couleurs_interdites.json`. Le fichier doit être du JSON valide, sinon `controle.py` s'arrête à l'import.

#### starter/marque/son/README.md
- **Rôle** : squelette de la bibliothèque de sons de la chaîne (musiques et effets réutilisables).
- **Quand il sert** : lu avant tout choix de son ; rempli au fil des épisodes (un son neuf approuvé par le propriétaire rejoint la bibliothèque). Voir [`son.md`](son.md) et le workflow [`../workflows/sons.md`](../workflows/sons.md).
- **Contenu** :
  - **Règle d'emploi** : un épisode **puise d'abord ici** ; aucune génération sans demande explicite du propriétaire ; un son approuvé rejoint ensuite la bibliothèque avec le préfixe de son épisode et sa provenance ; les fichiers ne se modifient jamais ici, on les copie dans `episodes/<id>/kit/media/audio/` (`musique/`, `sfx/`) ; gains, coupes et boucles se règlent au mix du film (`DIRECTION_AUDIO.md` § 3) ; une génération est **illustrative** (elle ne prétend pas être le son réel d'un lieu) ; provenance, prompts et crédits dans un `E00N-PROVENANCE.md` par épisode d'origine ; empreintes dans `SHA1SUMS.txt`.
  - **Musiques** : tableau vide Fichier · Durée · Épisode · Rôle.
  - **Effets et ambiances** : même tableau, vide.
- **À savoir** : les sons de la bibliothèque sont des binaires de `marque/` : Git LFS pour `wav` et `mp3`.

## Racine du dépôt du plugin
Chemins relatifs à la racine du dépôt (`studio-faceless/`).

### racine : README.md
- **Rôle** : page d'accueil du dépôt : ce qu'est le plugin, les deux étages (plugin / espace de chaîne), le contenu, comment démarrer, règles d'or, comment faire évoluer, licences.
- **Quand il sert** : première lecture de tout nouveau venu (propriétaire ou Claude).
- **Contenu** : schéma des deux étages · tableau du contenu de `plugins/studio-faceless/` (`skills/`, `agents/`, `hooks/`, `REGLES_STUDIO.md`, `referentiels/`, `outils/`, `templates/`, `starter/`, `vendor/claude-skills/`) · noms préfixés (`studio-faceless:episode`) · « Démarrer » (renvois vers `INSTALLATION.md`, `NOUVELLE_CHAINE.md`, `docs/ARCHITECTURE.md`) · **cinq règles d'or** (seul le propriétaire valide ; Claude ne publie, n'achète ni ne supprime rien ; on n'écrase jamais un travail ; médias réels sous licence libre ; HyperFrames figé en 0.8.149) · « Faire évoluer le plugin » en 4 étapes · licences.
- **Liens** : [`../../README.md`](../../README.md) ; décrit en détail dans [`../workflows/faire-evoluer-le-plugin.md`](../workflows/faire-evoluer-le-plugin.md).
- **À savoir** : la section « Licence » nomme trois skills MIT (`humanizer`, `javascript-animation`, `soundtrack`) ; `skills/regarder/references/claude-video/` porte aussi sa propre licence MIT, non citée (voir « Points à vérifier »). Convention de commit : `skills :`, `agents :`, `outils :`, `garde :`, `docs :`.

### racine : INSTALLATION.md
- **Rôle** : mode d'emploi pour **installer une machine** et brancher une chaîne existante, puis mettre à jour le plugin. Versions de référence : celles de la machine du 28/10/2026.
- **Quand il sert** : au premier jour sur une machine, ou à chaque changement de machine. Le propriétaire installe les prérequis ; Claude peut dérouler la suite avec son accord.
- **Contenu** : 1 Prérequis (Git + LFS 3.6.1, GitHub CLI, nvm puis Node 22.0.0, Python 3.14, FFmpeg 9.0, Claude Code 2.1.169 ou plus ; compte GitHub avec 2FA ; compte claude.ai avec connecteurs ; Chrome sans fenêtre ≈ 270 Mo) · 2 Identifiants Git (`gh auth login`, `gh auth setup-git`) · 3 Skills HyperFrames figés · 4 Brancher une chaîne existante (7 points) · 5 Vérifier (invite à donner à Claude) · 6 Mettre à jour le plugin.
- **Liens** : workflow détaillé dans [`../workflows/installation-et-mise-a-jour.md`](../workflows/installation-et-mise-a-jour.md) ; skills figés : [`vendor.md`](vendor.md).
- **À savoir** : le studio tourne sous **Windows avec Git Bash** ; `node` en PowerShell peut être une version trop ancienne.

### racine : NOUVELLE_CHAINE.md
- **Rôle** : mode d'emploi pour **créer une nouvelle chaîne** à partir du squelette.
- **Quand il sert** : quand le propriétaire lance une nouvelle chaîne (machine déjà installée : `INSTALLATION.md`, sections 1 à 3).
- **Contenu** : 1 Créer l'espace (dossier vide, copie de `starter/` fichiers cachés compris, `git init -b main`, `git lfs install`, `git config core.hooksPath .githooks`, dépendances, confiance du dossier, `claude plugin install … --scope project`) · 2 Remplir l'identité (invite à donner à Claude, porte de questions `studio-faceless:grilling`, tout en `PROPOSÉ`) · 3 Ce qui se décide par chaîne (tableau des quatre emplacements).
- **Liens** : workflow détaillé dans [`../workflows/nouvelle-chaine.md`](../workflows/nouvelle-chaine.md).
- **À savoir** : ne mentionne ni `pip install -r requirements.txt`, ni la règle `ask` du connecteur ElevenLabs, ni le modèle Whisper, qui figurent dans `INSTALLATION.md` § 4 (à rapprocher).

### racine : CHANGELOG.md
- **Rôle** : journal des versions du plugin. La version installée est celle de `plugin.json` ; **une modification n'arrive dans les chaînes que si ce numéro change**.
- **Quand il sert** : à chaque nouvelle version ([`../workflows/faire-evoluer-le-plugin.md`](../workflows/faire-evoluer-le-plugin.md)) ; lu par le propriétaire pour savoir ce qu'apporte une mise à jour.
- **Contenu** : une seule version à ce jour, `0.1.0 (28/10/2026)` : première version tirée de StudioV1 ; liste des skills (onze), des agents (cinq), du garde-fou (rôle déduit du type d'agent, écriture dans le plugin installé refusée), des règles communes injectées, des référentiels, des outils, des gabarits, du squelette et des skills HyperFrames figés ; décisions du 28/10/2026 intégrées (crédits CC BY par défaut, fiche `BRAND-SPLIT`, § 4 de `DIRECTION_AUDIO.md` réécrit pour les deux connecteurs ElevenLabs, modèle de miniature, statut `APPROUVE_PAR_<PROPRIETAIRE>`).
- **À savoir** : format = titre `## <version> (JJ/MM/AAAA)` puis puces. Le dépôt n'impose pas de règle de numérotation.

### racine : .gitattributes
- **Rôle** : fins de ligne et binaires du **dépôt du plugin**. Première ligne : « aucun fichier en Git LFS (une installation de plugin ne télécharge pas le contenu LFS) ».
- **Contenu** : `* text=auto` ; `*.sh`, `.githooks/*` et `plugins/studio-faceless/starter/.githooks/*` en LF ; `*.ps1` en CRLF ; `binary` pour `png`, `jpg`, `jpeg`, `webp`, `gif`, `mp3`, `wav`, `mp4`, `mov`, `webm`, `ttf`, `otf`, `woff`, `woff2`.
- **À savoir** : la ligne propre au squelette garde ses crochets en LF une fois copiés (le motif `.githooks/*` ne couvre que la racine). Les règles LFS sont dans le **squelette**, pas ici.

### racine : .gitignore
- **Rôle** : exclut du dépôt du plugin les caches et réglages personnels.
- **Contenu** : `__pycache__/`, `*.pyc`, `node_modules/`, `.claude/settings.local.json`, `Thumbs.db`, `desktop.ini`, `.DS_Store`.
- **À savoir** : beaucoup plus court que celui du squelette : ce dépôt ne contient aucun épisode.

### racine : .githooks/pre-commit
- **Rôle** : contrôle de chaque commit **du dépôt du plugin** par `verifier_depot.py`.
- **Quand il sert** : à chaque `git commit` dans le dépôt, une fois activé par `git config core.hooksPath .githooks`.
- **Usage** : `exec python -I -B plugins/studio-faceless/outils/verifier_depot.py` (chemin relatif à la racine du dépôt). Même contrôle que le crochet du squelette (taille hors LFS, médias d'épisode, secrets, chemins de machine).
- **À savoir** : contrairement au crochet du squelette, il lit le script **dans le dépôt**, pas dans le cache du plugin installé. Dans ce dépôt, `verifier_depot.py` ignore les dossiers `vendor/` (copie de tiers) pour la recherche de chemins de machine.

### racine : .claude-plugin/marketplace.json
- **Rôle** : le **catalogue** (marketplace) privé : liste les plugins que `claude plugin install` peut installer.
- **Contenu** : `name` `studio-faceless` ; `description` « Catalogue privé du studio de chaînes YouTube faceless de Hicham. » ; `owner.name` `Hicham` ; `plugins[0]` : `name` `studio-faceless`, `source` `./plugins/studio-faceless`, `description`.
- **Quand il sert** : lu par Claude Code quand une chaîne déclare le catalogue (`extraKnownMarketplaces` du `settings.json` du squelette). L'identifiant d'installation est `studio-faceless@studio-faceless` (plugin@catalogue).
- **À savoir** : **aucune `version`** dans le catalogue : la version vient de `plugin.json` ([`../ARCHITECTURE.md`](../ARCHITECTURE.md)). Ne jamais renommer le plugin : un renommage casse les installations.

### plugins/studio-faceless/.claude-plugin/plugin.json
- **Rôle** : manifeste du plugin : nom, version, description, auteur.
- **Contenu** : `name` `studio-faceless` ; `version` `0.1.0` ; `description` (« Studio de chaînes YouTube documentaires faceless avec Claude Code et HyperFrames : fabrication d'un épisode du sujet au mix, shorts, miniatures, dossier de publication, direction sonore, agents de production, garde-fou et outils de contrôle. ») ; `author.name` `Hicham`.
- **Quand il sert** : `version` **fige la version installée** : le cache d'installation est rangé par version (`~/.claude/plugins/cache/studio-faceless/studio-faceless/<version>/`). Sans changement de ce nombre, `claude plugin update` n'apporte rien.
- **À savoir** : à augmenter à chaque modification ; à noter dans `CHANGELOG.md`.

## Squelette contre dépôt du plugin : ce qui diffère
| Sujet | Squelette (chaîne) | Dépôt du plugin |
|---|---|---|
| Git LFS | oui, pour `marque/**` (et `templates/**`) | aucun fichier LFS |
| Crochets Git | 5 (pre-commit + 4 de LFS) | 1 (pre-commit) |
| `pre-commit` cherche le script | dans le cache du plugin installé (ou `STUDIO_FACELESS_OUTILS`) | dans `plugins/studio-faceless/outils/` |
| `.gitignore` | médias d'épisode, rendus, zips, corbeille d'archivage | caches seulement |
| Épisodes | oui (`episodes/<id>/`) | aucun |

## Points à vérifier et incohérences
- **`starter/package-lock.json:2` et `:8`** : `apparently-athletic-studiov1` contre `starter/package.json:2` `ma-chaine`. Le plugin est présenté sans nom de chaîne (`README.md`, § Deux étages) : à nettoyer.
- **`starter/.gitattributes:31-36`** : règles LFS sur `templates/**`, alors que le squelette n'a pas de dossier `templates/` (les modèles restent dans le plugin).
- **`starter/.claude/settings.json:19-26`** : huit permissions `mix.py` héritées du gabarit v2 ; le gabarit v3 n'a plus de `mix.py` (`templates/sequence-gabarit-v3/README.md:8`). **`:18`** `render.mjs` : le gabarit v3 utilise `render.sh`.
- **`README.md:54-57`** (licences) ne cite pas la licence MIT de `plugins/studio-faceless/skills/regarder/references/claude-video/LICENSE` (« Copyright (c) 2026 Bradley Bonanno »).
- **`plugins/studio-faceless/vendor/claude-skills/README.md`** annonce la licence Apache-2.0 des skills HyperFrames mais le dossier ne contient aucun fichier de licence (voir [`vendor.md`](vendor.md)).
- **`README.md:51`** liste cinq préfixes de commit (`skills`, `agents`, `outils`, `garde`, `docs`) ; l'historique Git du dépôt emploie aussi `plugin :`.
- `plugin.json` et `marketplace.json` nomment « Hicham » (auteur, propriétaire du catalogue), alors que le README dit que le plugin « ne contient aucun nom de chaîne ni de personne ». Probablement voulu (métadonnées) ; à confirmer.
- Le comportement exact de `claude plugin install … --scope project` sur `.claude/settings.json` (déjà rempli par le squelette) n'est pas décrit dans les fichiers : à vérifier à la première installation.
