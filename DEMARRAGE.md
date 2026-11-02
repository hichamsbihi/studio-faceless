# Démarrer : de la machine vide à la première vidéo d'une nouvelle chaîne

Guide pas à pas, en français, pour installer le studio `studio-faceless`, créer une chaîne YouTube faceless et fabriquer sa première vidéo, de l'installation jusqu'à l'archivage.

**État du guide** : écrit le 29/10/2026, revu le 02/11/2026 pour le plugin en version 0.4.0 (`plugins/studio-faceless/.claude-plugin/plugin.json`). Il enchaîne les workflows de [`docs/workflows/`](docs/workflows/) sans les remplacer. En cas d'écart, le fichier du plugin fait foi ([`docs/README.md`](docs/README.md)). Tout point incertain est écrit « à vérifier ».

## À qui sert ce guide
- **À toi, le propriétaire** de la chaîne (celui qui décide, valide et publie). Tu pars d'une machine Windows qui n'a pas encore le studio. Tu parles à Claude en français ; il fait le travail, tu décides.
- **À un Claude qui t'aide.** Il suit les mêmes étapes. Il respecte aussi ces règles, qui viennent de [`REGLES_STUDIO.md`](plugins/studio-faceless/REGLES_STUDIO.md) :
  - il ne valide rien à ta place (une proposition ou une absence d'objection ne vaut pas validation) ;
  - il ne publie, n'achète et ne supprime rien ;
  - il fait des commits locaux ; il n'envoie vers GitHub qu'avec ton accord, donné à chaque fois, et ne se connecte jamais à ton compte ;
  - il ne déclare jamais une écoute ou un visionnage qui n'a pas eu lieu ;
  - il ne génère rien avec ElevenLabs (par l'API), n'installe et ne télécharge rien sans ton accord, coût annoncé avant ;
  - il n'écrase aucun travail : une nouvelle version va dans un nouveau dossier.

## Ce qu'il faut avant de commencer
| Il te faut | Détail | Source |
|---|---|---|
| Une machine Windows avec Git Bash | les commandes de Claude passent par Git Bash | [`INSTALLATION.md`](INSTALLATION.md) |
| Un compte GitHub | authentification à deux facteurs, accès aux dépôts privés (le dépôt du plugin est privé) | [`INSTALLATION.md`](INSTALLATION.md) |
| Un compte ElevenLabs (clé d'API) ; un compte claude.ai si tu veux vidIQ | ElevenLabs par l'API (voix, effets, musique) : le connecteur claude.ai d'ElevenLabs reste coupé ; vidIQ en lecture seule, facultatif, seulement sur ta demande | [`INSTALLATION.md`](INSTALLATION.md), [`DIRECTION_AUDIO.md`](plugins/studio-faceless/referentiels/DIRECTION_AUDIO.md) § 4 |
| Un forfait ElevenLabs payant | pour l'usage commercial des générations : selon l'aide d'ElevenLabs, le plan gratuit n'a pas de licence commerciale | `plugins/studio-faceless/skills/youtube-seo/references/description-et-credits.md`, l. 46 |
| L'accès à YouTube Studio | pour régler la vidéo, la mettre en ligne et relever les bilans (Claude ne se connecte jamais à ta chaîne) | [`dossier-youtube.md`](docs/workflows/dossier-youtube.md) |
| De la place disque et de la mémoire | Chrome sans fenêtre : environ 270 Mo ; modèle Whisper : 148 Mo ; mix d'un film de 9 min : 2 à 3 Go de mémoire ; archivage : 1,1 fois la taille du zip, plus 1 Go libres | [`INSTALLATION.md`](INSTALLATION.md), [`collage-et-mix.md`](docs/workflows/collage-et-mix.md), [`archivage-et-sauvegarde.md`](docs/workflows/archivage-et-sauvegarde.md) |
| Des idées sur ta chaîne | nom, promesse, public et langue du spectateur, voix, territoires, principes, ton : Claude te les demandera à l'étape B8 | [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md) |

**Durée** : ce guide n'annonce aucune durée. Elle dépend de ta machine, de tes réponses et de tes retours.

## Les règles d'or
Elles viennent du [`README.md`](README.md). Elles valent pour tout ce guide.
1. **Seul le propriétaire valide.** Une proposition n'est pas une décision ; chaque décision est datée.
2. **Claude ne publie, n'achète ni ne supprime rien.** Les essais retirés à l'archivage vont dans `_A_SUPPRIMER/`, que tu vides toi-même. Aucun envoi vers GitHub sans ton accord, à chaque fois.
3. **On n'écrase jamais un travail** : une nouvelle version va dans un nouveau dossier.
4. **Médias réels**, choisis sur ce qu'ils apportent à la scène : sous licence libre ou non libres en citation encadrée (`REFERENTIEL_QUALITE_REALISATION.md` § 2 bis) ; ta chaîne peut s'en tenir aux licences libres par un écart. Provenance consignée dans un `PROVENANCE.md`. Aucune image générée par IA, sauf écart écrit de ta chaîne.
5. **HyperFrames reste figé en 0.8.149** : aucune mise à jour sans ta décision.

> **Pas encore éprouvé.** La méthode et les outils viennent de StudioV1 (chaîne AA, la chaîne d'origine) et y ont servi. Ce qui n'a pas encore servi, c'est le plugin lui-même : le CLI `claude` de la machine où il a été écrit n'est connecté à aucun compte ([`docs/POINTS_OUVERTS.md`](docs/POINTS_OUVERTS.md), « Non testé »). En rédigeant ce guide, on a constaté que le dossier `~/.claude/plugins/` de cette machine ne contient aucun cache `studio-faceless` : **l'installation depuis GitHub n'a jamais été faite**. À confirmer à la première utilisation, selon `POINTS_OUVERTS.md` :
> - l'arrivée de `REGLES_STUDIO.md` dans le contexte au début d'une vraie session, et après `/clear`, `/compact` ou `/reload-plugins` ;
> - le `agent_type` reçu par le garde-fou dans un vrai sous-agent (c'est lui qui donne le rôle) ;
> - le préchargement de `studio-faceless:thumbnail-strategist` et de `studio-faceless:shorts` par les agents ;
> - le chemin du cache cherché par le crochet `pre-commit` de la chaîne ;
> - l'effet de `claude plugin install --scope project` sur `.claude/settings.json`.
>
> Ces tests étaient prévus « à la bascule de StudioV1 ». Une chaîne neuve ajoute d'autres inconnues, signalées plus bas : fabrication de la marque, bibliothèque de sons vide, langue autre que l'anglais.

## Comment lire ce guide

### Les trois parties
| Partie | Contenu | Étapes |
|---|---|---|
| [A](#partie-a--préparer-la-machine-une-fois) | Préparer la machine, une fois par ordinateur | A1 à A7 |
| [B](#partie-b--créer-la-chaîne) | Créer le dossier de la chaîne, le dépôt Git, installer le plugin, écrire l'identité | B1 à B11 |
| [C](#partie-c--la-première-vidéo) | Préparer la marque, puis fabriquer, publier et archiver la première vidéo | C1 à C34 |

### Ce que dit chaque étape
Chaque étape donne : **Qui** agit, **À faire** (la commande ou le message à Claude), **Fichiers créés**, **Tu valides**, **Vérifier**, **Détail** (le workflow à ouvrir). Les messages à donner à Claude sont en citation (> …). Tu les tapes dans la session Claude Code ouverte dans le dossier de ta chaîne.

### Où taper les commandes et ce que signifient les noms entre `<>`
Les commandes se tapent dans **Git Bash**, dans le dossier de la chaîne, sauf mention contraire. Les commandes `claude plugin …` se lancent dans un **terminal** (Git Bash), pas dans la conversation.

| Écrit dans le guide | Signifie |
|---|---|
| `<clone>` | le dossier où tu as cloné le dépôt du plugin, par exemple `~/Desktop/studio-faceless` |
| `<chaîne>` | le dossier de ta chaîne, par exemple `~/Desktop/MaChaine` |
| `<plugin>` | le plugin installé : `$HOME/.claude/plugins/cache/studio-faceless/studio-faceless/0.4.0` (le dernier élément est le champ `version` de `plugin.json`) |
| `<id>` | l'identifiant de l'épisode, par exemple `episode-001` |
| `<séquence>-vN` | un dossier de séquence versionné, par exemple `seq1-v1` |

`${CLAUDE_PLUGIN_ROOT}`, que tu verras dans les documents du plugin, n'existe pas dans Bash : dans une commande, on écrit le chemin complet (`<plugin>`). Dans Git Bash, `~` ne se développe pas entre guillemets : écris `$HOME`.

### Les statuts
| Sorte | Valeurs |
|---|---|
| Décisions | `FIXÉ`, `VALIDÉ` (date et référence), `PROPOSÉ`, `PROVISOIRE`, `QUESTION OUVERTE` |
| Production | `EN_COURS`, `MESURES_TECHNIQUES_OK`, `ECOUTE_A_FAIRE`, `CORRECTIONS_DEMANDEES`, `APPROUVE_PAR_<PROPRIETAIRE>` (date), `PUBLIE` (date et lien) |

Écriture d'une validation : `VALIDÉ, <ton prénom>, JJ/MM/AAAA`.

### Une « porte » de questions
Avant chaque grande étape, Claude ouvre une porte avec le skill `studio-faceless:grilling`. Il pose des questions numérotées (Q1, Q2…), chacune avec sa réponse recommandée. Répondre « oui » accepte la réponse recommandée. Il les pose par séries, à mesure que les décisions se débloquent. La porte se ferme quand plus aucune question n'est ouverte. Les faits, Claude les cherche ; les décisions sont à toi. Les réponses vont au `BRIEF.md`, datées.

### Le rythme de travail (à chaque fin de grande étape)
Source : [`REGLES_STUDIO.md`](plugins/studio-faceless/REGLES_STUDIO.md), « Économie de tokens et de contexte » (depuis la 0.2.3).
- Demande à Claude de réécrire `episodes/<id>/STATE.md` (un manifeste de 2,5 Ko au plus : étape courante, décisions validées, chemins, voix, budget restant, prochaine action) et de mettre à jour `episodes/INDEX.md`.
- Lance ensuite `/clear` (et non `/compact`) : après un `/compact`, Claude Code remet dans le contexte les skills appelés et les fichiers lus, et le premier appel pèse 124,6 k contre 81 à 88 k dans une session neuve. Pour reprendre, Claude lit seulement `INDEX.md`, puis `STATE.md`.
- `/compact` reste permis au milieu d'une longue porte (contexte au-delà de 150 à 200 k), après avoir écrit l'état. Ne change le modèle de Claude que juste après un `/clear`.

> Réécris le STATE.md de l'épisode et mets à jour l'INDEX.md, puis je lance /clear. Pour reprendre, tu liras seulement INDEX.md puis STATE.md.

Claude peut mesurer la consommation à chaque fin d'étape :
```bash
python -B "<plugin>/outils/suivi_tokens.py" --depuis AAAA-MM-JJ
```
Reste devant l'écran quand des agents travaillent : une demande de permission en attente pendant ton absence bloque tout. Ce qui demande ton accord se règle avant la délégation.

## Table des matières
- [Partie A — Préparer la machine (une fois)](#partie-a--préparer-la-machine-une-fois)
  [A1](#a1-installer-les-outils) · [A2](#a2-contrôler-les-versions) · [A3](#a3-connecter-la-machine-à-github) · [A4](#a4-cloner-le-dépôt-du-plugin) · [A5](#a5-copier-les-skills-hyperframes-figés) · [A6](#a6-brancher-les-connecteurs-du-compte) · [A7](#a7-préparer-le-modèle-whisper)
- [Partie B — Créer la chaîne](#partie-b--créer-la-chaîne)
  [B1](#b1-créer-le-dossier-de-la-chaîne) · [B2](#b2-initialiser-git-lfs-et-les-crochets) · [B3](#b3-ouvrir-le-dossier-dans-claude-code) · [B4](#b4-installer-le-plugin-pour-ce-projet) · [B5](#b5-installer-les-dépendances) · [B6](#b6-régler-elevenlabs-clé-dapi) · [B7](#b7-vérifier-linstallation) · [B8](#b8-poser-les-questions-de-départ) · [B9](#b9-remplir-lidentité-de-la-chaîne) · [B10](#b10-faire-le-premier-commit-local) · [B11](#b11-créer-le-dépôt-distant-privé)
- [Partie C — La première vidéo](#partie-c--la-première-vidéo)
  - Avant le collage : [C1](#c1-faire-linventaire-de-la-marque) · [C2](#c2-confirmer-la-voix-de-synthèse) · [C3](#c3-fixer-couleurs-couleurs-interdites-et-polices) · [C4](#c4-fabriquer-le-logo-et-la-bannière) · [C5](#c5-fabriquer-la-signature) · [C6](#c6-fabriquer-lappel-like-et-subscribe) · [C7](#c7-fabriquer-loutro) · [C8](#c8-contrôler-les-pièces-de-marque)
  - Fabrication : [C9](#c9-choisir-le-sujet) · [C10](#c10-faire-la-recherche) · [C11](#c11-valider-langle-et-le-découpage) · [C12](#c12-écrire-et-valider-le-script) · [C13](#c13-générer-les-prises-de-voix) · [C14](#c14-contrôler-les-prises-contre-le-texte) · [C15](#c15-ralentir-recaler-et-figer-la-voix) · [C16](#c16-fixer-la-direction-artistique-et-poser-le-gabarit) · [C17](#c17-réunir-les-médias) · [C18](#c18-préparer-les-sons) · [C19](#c19-finir-le-socle) · [C20](#c20-lancer-la-séquence-témoin) · [C21](#c21-rendre-et-valider-la-séquence-témoin) · [C22](#c22-produire-les-autres-séquences-par-lots-de-trois) · [C23](#c23-rendre-les-séquences-une-à-une) · [C24](#c24-coller-le-film-en-voix-seule) · [C25](#c25-mixer-le-film) · [C26](#c26-donner-tes-retours-et-approuver)
  - Publication : [C27](#c27-faire-la-miniature) · [C28](#c28-préparer-le-dossier-youtube) · [C29](#c29-mettre-en-ligne) · [C30](#c30-faire-les-bilans-j2-j7-et-j28)
  - Après la sortie : [C31](#c31-verser-les-sons-approuvés-à-la-bibliothèque) · [C32](#c32-sauvegarder-la-chaîne) · [C33](#c33-archiver-lépisode) · [C34](#c34-commiter-et-envoyer)
- [Si quelque chose bloque](#si-quelque-chose-bloque)
- [Et ensuite](#et-ensuite)
- [Pour aller plus loin](#pour-aller-plus-loin)

---

## Partie A — Préparer la machine (une fois)

À faire une seule fois par ordinateur. Workflow de référence : [`installation-et-mise-a-jour.md`](docs/workflows/installation-et-mise-a-jour.md) (parties A et B), qui suit [`INSTALLATION.md`](INSTALLATION.md). Les versions sont celles de la machine de référence au 28/10/2026.

### A1. Installer les outils
- **Qui** : toi.
- **À faire** : installe chaque outil. Les commandes ci-dessous sont à taper dans PowerShell (installation suggérée par `INSTALLATION.md`). Une commande par outil.

Git pour Windows, avec Git LFS :
```powershell
winget install Git.Git
```
GitHub CLI :
```powershell
winget install GitHub.cli
```
nvm pour Windows :
```powershell
winget install CoreyButler.NVMforWindows
```
Node 22 (HyperFrames exige Node 22 ou plus) :
```powershell
nvm install 22.0.0
```
```powershell
nvm use 22.0.0
```
Python :
```powershell
winget install Python.Python.3.14
```
FFmpeg :
```powershell
winget install Gyan.FFmpeg
```
Claude Code (2.1.271 ou plus : le champ `omitClaudeMd` de `research`, `studio-maintainer` et `strategist` le demande) : l'application de bureau, ou la commande `claude` en terminal. Les fichiers du plugin ne donnent pas de commande d'installation pour Claude Code.
- **Fichiers créés** : aucun dans un projet.
- **Tu valides** : rien.
- **Vérifier** : étape A2.
- **À savoir** : en PowerShell, `node` peut lancer une version plus ancienne que 22. Les commandes de Claude passent par Git Bash.
- **Détail** : [`installation-et-mise-a-jour.md`](docs/workflows/installation-et-mise-a-jour.md), A1.

### A2. Contrôler les versions
- **Qui** : toi (ou Claude, dans Git Bash).
- **À faire** : ouvre **Git Bash** et tape chaque commande du tableau.

| Commande | Réponse attendue |
|---|---|
| `git --version` | Git 2.49 (version de référence) |
| `git lfs version` | Git LFS 3.6.1 (version de référence) |
| `gh --version` | une version récente |
| `nvm list` | Node 22.0.0 actif sous Git Bash |
| `node --version` | v22 ou plus |
| `python --version` | 3.14 (3.12 au moins) ; Python doit être dans le `PATH` de Git Bash, car les deux hooks du plugin sont lancés par `python -I` |
| `ffmpeg -version` | 9.0 (version de référence) |
| `ffmpeg -hide_banner -filters \| grep whisper` | une ligne : le filtre `whisper` sert à contrôler les prises de voix |
| `claude --version` | 2.1.271 ou plus |

- **Fichiers créés** : aucun.
- **Tu valides** : rien.
- **Vérifier** : toutes les réponses sont conformes. Si `node` répond v20, change de version avec `nvm use 22.0.0` et recommence dans Git Bash.
- **Détail** : [`installation-et-mise-a-jour.md`](docs/workflows/installation-et-mise-a-jour.md), A1.

### A3. Connecter la machine à GitHub
- **Qui** : toi. Claude Code installe le plugin avec les identifiants Git de la machine, sans jamais en demander.
- **À faire** :
```bash
gh auth login
```
```bash
gh auth setup-git
```
- **Fichiers créés** : aucun dans un projet (la configuration d'authentification de Git et de `gh` sur la machine).
- **Tu valides** : rien.
- **Vérifier** : `gh auth status` (commande standard de GitHub CLI, non citée dans les fichiers du plugin) indique que tu es connecté. Le vrai test est l'étape B4.
- **Détail** : [`installation-et-mise-a-jour.md`](docs/workflows/installation-et-mise-a-jour.md), A2.

### A4. Cloner le dépôt du plugin
- **Qui** : toi. Ce clone sert de réserve : on y prend le squelette de chaîne (`starter/`) et les skills HyperFrames figés (`vendor/`). Tu n'y travailles pas sur ta chaîne.
- **À faire** :
```bash
git clone https://github.com/hichamsbihi/studio-faceless.git ~/Desktop/studio-faceless
```
Si tu as déjà ce clone, mets-le à jour avec `git -C ~/Desktop/studio-faceless pull`.
- **Fichiers créés** : le dossier `~/Desktop/studio-faceless`. Ce dépôt n'a aucune règle Git LFS.
- **Tu valides** : rien.
- **Vérifier** : `ls ~/Desktop/studio-faceless/plugins/studio-faceless` liste `agents`, `hooks`, `outils`, `referentiels`, `REGLES_STUDIO.md`, `skills`, `starter`, `templates`, `vendor`.
- **Détail** : [`installation-et-mise-a-jour.md`](docs/workflows/installation-et-mise-a-jour.md), A3 ; [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

### A5. Copier les skills HyperFrames figés
- **Qui** : toi, ou Claude avec ton accord.
- **Pourquoi** : les agents préchargent les skills HyperFrames 0.8.149. Une nouvelle machine doit recevoir exactement ces versions, pas les plus récentes.
- **À faire** : le dépôt ne fournit pas de script. Cette boucle est l'exemple de [`installation-et-mise-a-jour.md`](docs/workflows/installation-et-mise-a-jour.md) (A3) répété pour les dix dossiers ; `-n` empêche d'écraser un fichier existant.
```bash
mkdir -p ~/.claude/skills
```
```bash
for s in hyperframes hyperframes-animation hyperframes-audio hyperframes-cli hyperframes-core hyperframes-creative hyperframes-keyframes hyperframes-registry hyperframes-studio media-use; do cp -rn ~/Desktop/studio-faceless/plugins/studio-faceless/vendor/claude-skills/$s ~/.claude/skills/; done
```
- **Fichiers créés** : `~/.claude/skills/<skill>/` pour les dix skills. Ce sont des skills d'utilisateur, sans préfixe.
- **Tu valides** : rien.
- **Vérifier** : `ls ~/.claude/skills` liste les dix dossiers.
- **À savoir** : ne lance jamais `hyperframes skills update` ni `hyperframes upgrade` : le garde-fou les refuse. Si un skill te demande de mettre HyperFrames à jour, ignore la consigne.
- **Détail** : [`docs/reference/vendor.md`](docs/reference/vendor.md).

### A6. Brancher les connecteurs du compte
- **Qui** : toi.
- **À faire** :
  - **ElevenLabs** : crée ta clé d'API sur elevenlabs.io (Settings, API Keys). ElevenLabs passe par l'API, pas par le connecteur claude.ai, qui reste coupé (30/10/2026). Tu poseras la clé toi-même à l'étape B6 ;
  - **YouTube Data et Gemini** : si tu veux relever les vidéos d'une chaîne (agent `strategist`) ou faire « regarder » une vidéo (skill `regarder`), crée une clé d'API pour chaque service ; tu les poseras aussi à l'étape B6 ;
  - si tu veux, dans ton compte claude.ai, **vidIQ** en lecture seule. Claude ne s'en sert que sur ta demande.
- **Fichiers créés** : aucun.
- **Tu valides** : rien.
- **Vérifier** : la clé existe sur elevenlabs.io ; ne la donne à personne et ne la colle jamais dans une conversation.
- **Détail** : [`sons.md`](docs/workflows/sons.md), partie C ; [`DIRECTION_AUDIO.md`](plugins/studio-faceless/referentiels/DIRECTION_AUDIO.md) § 4.

### A7. Préparer le modèle Whisper
- **Qui** : toi, ou Claude avec ton accord.
- **À faire** : télécharge `ggml-base.en.bin` (licence MIT, 148 Mo) dans un dossier **hors de toute chaîne**. Il sert à `transcrire.py`, qui compare chaque prise de voix au texte validé. Aucun téléchargement sans ton accord. L'adresse du modèle n'est écrite dans aucun fichier du plugin : Claude te la propose, tu l'acceptes.
- **Fichiers créés** : le fichier modèle (le `.gitignore` de la chaîne ignore les `*.bin`). Note son chemin : tu le donneras à `--modele` à l'étape C14. Tu peux aussi faire cette étape plus tard, juste avant C14.
- **Tu valides** : le téléchargement.
- **Vérifier** : le fichier existe et pèse environ 148 Mo.
- **Détail** : [`voix-off.md`](docs/workflows/voix-off.md), « Prérequis ».

> **À vérifier : la langue.** `ggml-base.en.bin` est un modèle **anglais**. Pour une chaîne dont le spectateur parle une autre langue, le contrôle des prises par `transcrire.py` n'est pas garanti : un modèle multilingue serait nécessaire, et les fichiers du plugin ne l'ont pas testé. Les valeurs par défaut de la voix (tempo ×0,97, débit visé de 130 à 135 mots par minute) ont aussi été validées sur AA, en anglais.

**Tu es prêt pour la partie B quand** : les versions de A2 sont bonnes, `gh` est connecté, le clone est là, les dix skills sont dans `~/.claude/skills`, la clé ElevenLabs est créée.

---

## Partie B — Créer la chaîne

Une chaîne est un dossier, et un dépôt Git privé, créé à partir du squelette `plugins/studio-faceless/starter/`. Workflow de référence : [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md), qui suit [`NOUVELLE_CHAINE.md`](NOUVELLE_CHAINE.md). Ordre à respecter : installer le plugin (B4) **avant le premier commit** (B10).

### B1. Créer le dossier de la chaîne
- **Qui** : toi, ou Claude avec ton accord.
- **À faire** : crée un dossier vide, puis copies-y le contenu du squelette, **fichiers cachés compris** (`.claude/`, `.githooks/`, `.gitignore`, `.gitattributes`). Le dépôt ne fournit pas de script de copie : ces commandes sont l'exemple de `nouvelle-chaine.md` (étape 2).
```bash
mkdir ~/Desktop/<NomDeLaChaine>
```
```bash
cp -a ~/Desktop/studio-faceless/plugins/studio-faceless/starter/. ~/Desktop/<NomDeLaChaine>/
```
```bash
cd ~/Desktop/<NomDeLaChaine>
```
- **Fichiers créés** : les 17 fichiers du squelette.
```text
<NomDeLaChaine>/
├── CLAUDE.md
├── package.json
├── package-lock.json
├── requirements.txt
├── .gitignore
├── .gitattributes
├── .claude/settings.json
├── .githooks/        (pre-commit, post-checkout, post-commit, post-merge, pre-push)
├── direction/        (LIGNE_EDITORIALE.md, ECARTS.md)
└── marque/           (README.md, couleurs_interdites.json, son/README.md)
```
- **Tu valides** : rien.
- **Vérifier** : `ls -a` montre `.claude`, `.githooks`, `.gitignore`, `.gitattributes`, `CLAUDE.md`, `direction`, `marque`, `package.json`, `package-lock.json`, `requirements.txt`.
- **À savoir** : `package.json` et `package-lock.json` portent le nom `ma-chaine`. Tu peux le remplacer par le nom de ta chaîne dans les deux fichiers ; ce n'est pas obligatoire. `.claude/settings.json` déclare le catalogue du plugin (`hichamsbihi/studio-faceless`), l'active et fournit les permissions : ne change ni le nom du plugin ni celui du catalogue (un renommage casse les installations).
- **Détail** : [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md), étapes 1 et 2 ; [`docs/reference/starter-et-depot.md`](docs/reference/starter-et-depot.md).

### B2. Initialiser Git, LFS et les crochets
- **Qui** : toi, ou Claude avec ton accord.
- **À faire** : dans le dossier de la chaîne.
```bash
git init -b main
```
```bash
git lfs install
```
```bash
git config core.hooksPath .githooks
```
- **Fichiers créés** : `.git/`. La dernière commande active les cinq crochets du squelette : le contrôle avant commit et les quatre crochets Git LFS.
- **Tu valides** : rien.
- **Vérifier** : `git config core.hooksPath` répond `.githooks` ; `git status` montre les fichiers du squelette comme non suivis. Si un crochet sort en erreur (code 2), Git LFS n'est pas dans le `PATH`.
- **Détail** : [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md), étape 3 ; [`depot-git.md`](docs/workflows/depot-git.md).

### B3. Ouvrir le dossier dans Claude Code
- **Qui** : toi.
- **À faire** : ouvre le dossier de la chaîne dans Claude Code (application de bureau, ou `claude` lancé dans le dossier). **Accepte la confiance du dossier.** Sans elle, Claude Code ignore le catalogue déclaré dans `.claude/settings.json`.
- **Fichiers créés** : aucun.
- **Tu valides** : la confiance du dossier.
- **Vérifier** : la preuve est à l'étape B4 : si le catalogue est connu, l'installation passe. Si le plugin n'est pas proposé, vois « Si quelque chose bloque ».
- **Détail** : [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md), étape 4.

### B4. Installer le plugin pour ce projet
- **Qui** : toi, ou Claude avec ton accord. **Dans un terminal Git Bash**, dans le dossier de la chaîne.
- **À faire**, dans cet ordre : déclarer le catalogue du plugin, puis installer le plugin.
```bash
claude plugin marketplace add hichamsbihi/studio-faceless --scope project
```
```bash
claude plugin install studio-faceless@studio-faceless --scope project
```
  Sans la première commande, l'installation échoue avec « Plugin "studio-faceless" not found in marketplace » : le CLI ne lit pas le catalogue déclaré dans `.claude/settings.json` (`extraKnownMarketplaces`) d'un dossier qui ne lui a pas encore été confié (Claude Code 2.1.169, constaté le 29/10/2026).
- **Fichiers créés** : le plugin arrive dans le cache `~/.claude/plugins/cache/studio-faceless/studio-faceless/<version>/` (seul `plugins/studio-faceless/` est copié). Le cache sert à tous les projets de la machine.
- **Tu valides** : rien.
- **Vérifier** :
```bash
ls ~/.claude/plugins/cache/studio-faceless/studio-faceless/
```
  Le dossier de la version (`0.4.0`) doit apparaître.
- **Détail** : [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md), étape 5 ; [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), « Chemins ».

> **Pas encore éprouvé (à vérifier).**
> - **L'installation depuis GitHub** a servi une première fois le 29/10/2026, à la création d'une chaîne, avec l'étape `marketplace add` ci-dessus ; les autres points de l'encadré de l'introduction restent à confirmer.
> - **L'effet de `--scope project` sur `.claude/settings.json`** : le fichier active déjà le plugin, et le comportement exact de la commande n'est pas décrit dans le dépôt.
> - **La commande `/plugin` interactive** n'est citée dans aucun fichier du plugin. Dans l'onglet Code de l'application de bureau, elle peut ne pas être disponible : à vérifier. Garde un terminal Git Bash ouvert pour les commandes `claude plugin …`.

### B5. Installer les dépendances
- **Qui** : tu décides, Claude lance avec ton accord. Dans Git Bash (Node 22), dans le dossier de la chaîne.
- **À faire** :
```bash
npm ci
```
```bash
pip install -r requirements.txt
```
  `npm ci` installe **HyperFrames 0.8.149**, figé par `package-lock.json`. Ne lance jamais `npm install` : le garde-fou le refuse. `requirements.txt` contient `numpy>=2.4` et `scipy>=1.17`.
- **Fichiers créés** : `node_modules/` (ignoré par Git) ; les paquets Python de la machine.
- **Tu valides** : l'installation.
- **Vérifier** :
```bash
grep -m1 '"version"' node_modules/hyperframes/package.json
```
  Réponse attendue : `"version": "0.8.149"`. Si `npm ci` échoue, vérifie Node 22 et ne tente jamais `npm install`.
- **Détail** : [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md), étape 6.

### B6. Régler ElevenLabs (clé d'API)
- **Qui** : toi. Claude ne lit, n'affiche, ne demande ni n'écrit jamais la clé.
- **À faire** : pose la clé dans la variable d'environnement `ELEVENLABS_API_KEY` de ta session Windows (ou dans un `.env` ignoré par Git), puis relance Claude Code. Le SDK Python `elevenlabs` ne s'installe que sur ta décision, à la version figée dans le `requirements.txt` de la chaîne. Aucune règle `ask` à ajouter : le connecteur est coupé, et chaque génération te demande ton accord en conversation, coût annoncé avant. Aucun sous-agent ne génère.
  Deux autres clés se posent de la même façon, par toi, dans l'environnement ; Claude ne les lit ni ne les affiche, et aucune n'est écrite dans un fichier :
  - `YOUTUBE_API_KEY` (API YouTube Data v3, créée par toi) : `outils/recherche/youtube_chaine.py` et l'agent `strategist`, pour relever les vidéos d'une chaîne ; sans elle, l'outil s'arrête ;
  - `GEMINI_API_KEY` : le skill `regarder` (`regarder.py`) et `relire.py` ; un contenu inédit ne part chez Google qu'avec la clé du palier payant, décision à toi.
- **Fichiers créés** : aucun.
- **Tu valides** : la pose de la clé.
- **Vérifier** : Claude peut seulement constater que la variable existe (réponse oui ou non), sans la lire.
- **Détail** : [`session-et-garde-fou.md`](docs/workflows/session-et-garde-fou.md), « Permissions de la chaîne ».

### B7. Vérifier l'installation
- **Qui** : Claude, à ta demande.
- **À faire** : donne ce message à Claude (texte de `INSTALLATION.md`, § 5) :

> Vérifie l'installation : liste les skills et agents `studio-faceless`, vérifie que les règles communes du studio sont arrivées au début de la session, lance `hyperframes check` sur le gabarit de séquence v3 du plugin copié dans un dossier temporaire, un rendu test de 3 secondes avec `--workers 1`, un contrôle `controle.py niveau` sur ce rendu et `controle.py chrome`. Vérifie à la fin qu'aucun Chrome ne reste ouvert.

  Au premier contrôle ou rendu, HyperFrames télécharge `chrome-headless-shell` (environ 270 Mo) dans `~/.cache/hyperframes/`. Réponds à la demande d'accord.
- **Fichiers créés** : un dossier temporaire de test, et le Chrome dans `~/.cache/hyperframes/`. Rien dans la chaîne.
- **Tu valides** : tu **lis le bilan avant de continuer**. C'est la porte.
- **Vérifier** : le bilan liste les 14 skills (`studio-faceless:episode`, `shorts`, `thumbnail-strategist`, `youtube-seo`, `direction-sonore`, `regarder`, `grilling`, `humanizer`, `find-skills`, `elevenlabs-sound-effects`, `elevenlabs-music`, `frontend-design`, `remove-background`, `blender-pro`) et les sept agents (`research`, `reviewer`, `art-director`, `motion-producer`, `shorts-producer`, `studio-maintainer`, `strategist`). Il montre les règles communes reçues, un `check` sans erreur, un rendu de 3 s, et `controle.py chrome` à 0. Si les règles communes ne sont pas visibles, redemande à Claude de les lister, puis vois « Si quelque chose bloque ».
- **Détail** : [`installation-et-mise-a-jour.md`](docs/workflows/installation-et-mise-a-jour.md), partie C.

> **Pas encore éprouvé.** Ce contrôle est le premier test réel de l'arrivée des règles communes (`SessionStart`), du préchargement des skills par les agents et du rôle reçu par le garde-fou. Si un résultat surprend, note-le : il corrige la documentation du plugin.

### B8. Poser les questions de départ
- **Qui** : Claude pose, toi tu réponds. Skill `studio-faceless:grilling`.
- **À faire** : donne ce message (texte de `NOUVELLE_CHAINE.md`) :

> Nouvelle chaîne. Avec le skill `studio-faceless:grilling`, pose-moi les questions de départ, une porte à la fois : nom et promesse, public et langues, propriétaire, voix, territoires, principes, personnalité narrative, ce qui s'écarte des règles par défaut du plugin. Puis remplis `CLAUDE.md`, `direction/LIGNE_EDITORIALE.md` et `direction/ECARTS.md`, tout en `PROPOSÉ`, sans rien valider à ma place.

  Là où tes réponses s'écrivent :

| Question | Où |
|---|---|
| Nom et promesse | `CLAUDE.md` (titre et phrase d'ouverture) ; `LIGNE_EDITORIALE.md` § Promesse (`PROVISOIRE`) |
| Public et langues | `CLAUDE.md` § Identité ; `LIGNE_EDITORIALE.md` § Identité et public |
| Propriétaire | `CLAUDE.md` § Identité (ton prénom) |
| Voix | `CLAUDE.md` § Identité ; `ECARTS.md` § DIRECTION_AUDIO |
| Territoires | `LIGNE_EDITORIALE.md` § Territoires |
| Principes | `LIGNE_EDITORIALE.md` § Principes |
| Personnalité narrative | `LIGNE_EDITORIALE.md` § Personnalité narrative |
| Écarts aux règles par défaut | `ECARTS.md`, section du référentiel concerné |

  Les référentiels du plugin renvoient plusieurs points à `direction/ECARTS.md`. Ajoute si tu veux ce second message pour ne rien oublier :

> Dans la même porte, tranche aussi ce que les référentiels du plugin renvoient à `direction/ECARTS.md` : les compétitions et instances dont on admet les vraies vidéos, la liste des chaînes de référence dont aucun média ne se reprend, les crédits CC BY dans la description (par défaut ils y sont), la voix retenue et ses réglages (dont le tempo de ralentissement), la recette du fond de la chaîne, et la place du rappel d'abonnement.

  D'où viennent ces points : [`REFERENTIEL_QUALITE_REALISATION.md`](plugins/studio-faceless/referentiels/REFERENTIEL_QUALITE_REALISATION.md) § 2 bis (compétitions et instances) et § 2 ter (fond de la chaîne) ; [`recherche.md`](docs/workflows/recherche.md) (chaînes de référence) ; [`dossier-youtube.md`](docs/workflows/dossier-youtube.md) (crédits) ; [`DIRECTION_AUDIO.md`](plugins/studio-faceless/referentiels/DIRECTION_AUDIO.md) (voix) ; [`etapes.md`](plugins/studio-faceless/skills/episode/references/etapes.md) § 2 (rappel d'abonnement).
- **Fichiers créés** : aucun encore (Claude n'écrit qu'après ta confirmation de la fin de la porte).
- **Tu valides** : tes réponses. La porte est finie quand la liste des questions ouvertes est vide.
- **Vérifier** : Claude te redit ce qu'il a compris, et rien n'est supposé en silence.
- **Détail** : [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md), étape 8.

### B9. Remplir l'identité de la chaîne
- **Qui** : Claude rédige, tu relis et tu valides.
- **À faire** : Claude remplit, en `PROPOSÉ` :
  - `CLAUDE.md` : remplace chaque `<…>` (nom, phrase d'ouverture, propriétaire, langues, public, voix) ; « Règles propres » : une règle par ligne avec statut et date ; « État » : « aucun épisode » ;
  - `direction/LIGNE_EDITORIALE.md` : chaque section selon son statut de départ ; « Sujets » vide ; le registre des décisions avec une ligne par décision ;
  - `direction/ECARTS.md` : une ligne par écart, au format `§ visé : règle de la chaîne (statut, date)`. Le fichier reste vide tant que la chaîne suit les règles par défaut.

  Tri : une règle propre à ta chaîne va dans `CLAUDE.md` ; une règle qui **remplace** une règle du plugin va dans `ECARTS.md` (elle l'emporte) ; une règle bonne pour toutes les chaînes ne s'écrit pas ici.
- **Fichiers créés** : `CLAUDE.md`, `direction/LIGNE_EDITORIALE.md` et `direction/ECARTS.md` remplis.
- **Tu valides** : **ligne à ligne**. Claude remplace alors `PROPOSÉ` par `VALIDÉ, <ton prénom>, JJ/MM/AAAA` avec la référence. Une absence d'objection ne vaut pas validation ; ce que tu n'as pas validé reste `PROPOSÉ`.
- **Vérifier** : plus aucun `<…>` du squelette dans la section Identité de `CLAUDE.md` ; chaque décision de `LIGNE_EDITORIALE.md` a son statut et sa date.
- **À savoir** : le modèle `BRIEF.episode.template.md` fixe encore « français » (ligne 3) et « anglais » (ligne 31) pour les langues. Si ta chaîne a d'autres langues, Claude corrige le `BRIEF.md` de l'épisode (à vérifier). La correction commune au plugin passe par [`faire-evoluer-le-plugin.md`](docs/workflows/faire-evoluer-le-plugin.md).
- **Détail** : [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md), étape 9 et « Ce qui se décide par chaîne ».

### B10. Faire le premier commit local
- **Qui** : Claude, **commit local seulement**.
- **À faire** : d'abord le contrôle de tout ce que Git suivrait, puis le commit. Le crochet `pre-commit` relance `verifier_depot.py` sur les fichiers indexés.
```bash
python -I -B "<plugin>/outils/verifier_depot.py" --tout
```
```bash
git add -A
```
```bash
git commit -m "chaîne : squelette et identité"
```
  Le plugin ne fixe pas de convention de message pour une chaîne. Au dépôt du plugin, les messages sont courts, en français, préfixés par la zone.
- **Fichiers créés** : un commit local.
- **Tu valides** : rien. Aucun envoi vers GitHub à cette étape.
- **Vérifier** : le commit passe. Si le crochet répond « verifier_depot.py introuvable : le plugin studio-faceless est-il installé ? », reviens à B4.
- **Détail** : [`depot-git.md`](docs/workflows/depot-git.md), parties A et B.

> **Pas encore éprouvé.** Le crochet `pre-commit` cherche `verifier_depot.py` dans `~/.claude/plugins/cache/studio-faceless/studio-faceless/*/outils/` et prend la version la plus haute. Ce chemin n'a pas encore été testé sur une vraie installation. La variable `STUDIO_FACELESS_OUTILS` peut désigner un autre dossier `outils/` (par exemple celui de ton clone).

### B11. Créer le dépôt distant privé
- **Qui** : toi. Claude ne se connecte jamais à ton compte GitHub.
- **À faire** : crée sur GitHub un dépôt **privé**, vide. Réglages recommandés par l'audit d'AA (21/10/2026) : branche `main` protégée (pas de `force push`, pas de suppression), authentification à deux facteurs (à vérifier pour ta chaîne). Les fichiers du plugin ne décrivent pas cette création. Ensuite, deux commandes Git standard :
```bash
git remote add origin https://github.com/<compte>/<depot-de-la-chaine>.git
```
```bash
git push -u origin main
```
  Le premier envoi se fait **avec ton accord explicite**, comme chaque envoi ensuite. Le crochet `pre-push` envoie d'abord les objets LFS.
- **Fichiers créés** : rien en local ; le dépôt distant.
- **Tu valides** : chaque envoi, à chaque fois.
- **Vérifier** : `git status -sb` indique `main...origin/main`.
- **Détail** : [`depot-git.md`](docs/workflows/depot-git.md), partie C.

**Tu es prêt pour la partie C quand** : le bilan de B7 est propre, `CLAUDE.md`, `LIGNE_EDITORIALE.md` et `ECARTS.md` sont remplis et validés, le premier commit est fait.

---

## Partie C — La première vidéo

La fabrication suit le skill `studio-faceless:episode`, du choix du sujet au mix du film, puis la publication et l'archivage. Workflow de référence : [`episode.md`](docs/workflows/episode.md) (étapes 0 à 13 du skill). Pour une chaîne neuve, il faut d'abord ce qu'elle n'a pas encore.

### Avant le collage : ce qu'une chaîne neuve n'a pas encore
Les fichiers du plugin **prévoient la place** de chaque élément de marque et la règle qui l'emploie. Ils **ne fournissent aucun de ces éléments** : pas de logo, pas de bannière, et surtout **aucun gabarit de signature, d'appel Like + Subscribe ou d'outro** dans le plugin. La fiche `BRAND-SPLIT` du catalogue d'animations dit seulement que la recette est « propre à la chaîne » ; `nouvelle-chaine.md` (étape 10) note que « le squelette ne fournit pas de méthode de fabrication » de ces pièces. C'est à toi et à Claude de les fabriquer (C4 à C7).

| Élément | Où dans la chaîne | Ce que les fichiers du plugin prévoient | Ce qu'ils ne fournissent pas | À avoir avant |
|---|---|---|---|---|
| Voix de synthèse | `CLAUDE.md` § Identité ; `ECARTS.md` § DIRECTION_AUDIO | la porte « Voix » (`grilles.md` § 4), la règle de la prise approuvée, `ralentir.py` (tempo ×0,97 par défaut), le contrôle des prises | aucune voix retenue, aucune procédure d'essai de voix | les prises (C13) |
| Logo et bannière | `marque/identite-chaine-01/` | une ligne du tableau de `marque/README.md` ; le logo sert aux miniatures | aucun logo, aucune bannière, aucun gabarit ; aucune taille de bannière | le logo : la miniature (C27) ; la bannière : à décider |
| Signature (après l'intro) | `marque/<signature-vN>/`, un MP4 fini | sa place dans `montage.json` (clé `marque`, après `seq1`, 0,5 s de noir de chaque côté), son propre son gardé, niveau d'origine au mix | aucun gabarit | le collage (C24) |
| Appel Like + Subscribe | `marque/<appel-vN>/` | la technique `HOLD-CALL` (dernière image tenue environ 4 s, l'overlay de `marque/` posé au début de la pause) ; place par défaut vers 2:00 | aucun gabarit ; le format de l'overlay n'est pas précisé ; le collage n'a pas de pièce dédiée pour lui | la séquence qui le porte (C20, C22) |
| Outro (écran de fin) | `marque/<outro-vN>/`, un MP4 fini | la clé `outro` de `montage.json`, `noir_avant` de 4,0 s, fondu « noir>outro » de 15 images | aucun gabarit | le collage (C24) |
| Couleurs interdites | `marque/couleurs_interdites.json` | livré vide (`{}`) ; `controle.py couleurs` cherche les couleurs listées (hexadécimal et `rgb()`), sauf dans la signature et l'outro | aucune couleur choisie | le premier rendu (C21) |
| Polices | `marque/README.md` § Polices des films | Newsreader (SIL OFL) dans le gabarit v3, IBM Plex Mono injectée par le compilateur ; Montserrat (SIL OFL) pour les miniatures, à télécharger une fois avec ton accord et à ranger dans `marque/` avec sa licence | aucune police de marque choisie | la direction artistique (C16) |
| Bibliothèque de sons | `marque/son/README.md` | la règle d'emploi et deux tableaux **vides** | aucun son : **la première vidéo génère ses sons, avec ton accord** | le socle (C18) |

### C1. Faire l'inventaire de la marque
- **Qui** : Claude.
- **À faire** : donne ce message :

> Fais l'inventaire de `marque/` : pour le logo, la bannière, la signature, l'appel Like + Subscribe, l'outro, les couleurs interdites, les polices et la bibliothèque de sons, dis-moi ce qui existe, ce qui manque, et ce que `marque/README.md` et les référentiels exigent avant le collage du premier film. Ne crée rien.

- **Fichiers créés** : aucun.
- **Tu valides** : l'ordre dans lequel tu veux traiter ce qui manque.
- **Vérifier** : la liste de Claude correspond au tableau ci-dessus. La bibliothèque de sons est vide : c'est normal.
- **Détail** : [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md), étapes 10 et 11.

### C2. Confirmer la voix de synthèse
- **Qui** : toi (tu choisis), Claude (il écrit). Si tu as tout tranché à l'étape B8, vérifie seulement que c'est écrit et `VALIDÉ`.
- **À faire** :

> Avec `studio-faceless:grilling`, pose-moi les questions sur la voix : quel service et quelle voix, quels réglages, le tempo de ralentissement (0,97 par défaut), les mots à réécouter. Écris le résultat en `PROPOSÉ` dans `CLAUDE.md` (Voix) et dans `direction/ECARTS.md` (DIRECTION_AUDIO).

  Tu écoutes les voix toi-même dans ElevenLabs : Claude n'écoute pas. Les fichiers du plugin ne décrivent aucune procédure d'essai de voix (à vérifier).
- **Fichiers créés** : `CLAUDE.md` et `direction/ECARTS.md` mis à jour.
- **Tu valides** : la voix retenue, `VALIDÉ, <prénom>, JJ/MM/AAAA`. Une fois les prises faites, une prise approuvée ne se régénère, ne se réécrit, ne s'accélère ni ne se coupe sans ton autorisation (seule exception : le ralentissement de C15).
- **Vérifier** : `CLAUDE.md` nomme le service, la voix et les réglages.
- **Détail** : [`voix-off.md`](docs/workflows/voix-off.md) ; [`DIRECTION_AUDIO.md`](plugins/studio-faceless/referentiels/DIRECTION_AUDIO.md) § 1 et § 2.

### C3. Fixer couleurs, couleurs interdites et polices
- **Qui** : toi (tu décides), Claude (il écrit).
- **À faire** :

> Avec `studio-faceless:grilling`, pose-moi les questions sur la marque : les couleurs de la marque (logo, signature, outro), les couleurs à interdire dans les films, les polices. Remplis `marque/README.md` et `marque/couleurs_interdites.json` en `PROPOSÉ`.

  Règles du squelette (`marque/README.md`) :
  - **couleurs de marque** : celles du logo, de la signature et de l'outro ;
  - **couleurs des films** : un socle fixe, plus une palette propre à chaque histoire, décidée en direction artistique avec une planche d'essai (C16) ;
  - **couleurs interdites** : `{"nom": "#RRGGBB"}` dans `marque/couleurs_interdites.json`. Vide, il n'interdit rien ;
  - **polices** : avec leur licence, SIL OFL de préférence. Le gabarit v3 apporte Newsreader ; pour les miniatures, Montserrat se télécharge une fois avec ton accord (C27).
- **Fichiers créés** : `marque/README.md` et `marque/couleurs_interdites.json` mis à jour ; les fichiers de polices, si tu en ajoutes, dans un dossier versionné de `marque/` (le nom n'est pas imposé).
- **Tu valides** : couleurs, interdits, polices : `VALIDÉ, <prénom>, JJ/MM/AAAA`.
- **Vérifier** : `marque/couleurs_interdites.json` est un JSON valide ; chaque police a sa licence à côté.
- **À savoir** : le fond par défaut du gabarit v3 est un fond « papier charbon » avec brumes et grain (Resource Boy, licences dans le gabarit) et la police Newsreader. Décide en direction artistique (C16) si ta chaîne le garde ou le remplace.
- **Détail** : [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md), étape 10 ; [`docs/reference/templates.md`](docs/reference/templates.md).

### Méthode commune aux pièces de marque (C4 à C7)
Elle découle de `marque/README.md` du squelette, de `montage.json` et du garde-fou. Les fichiers du plugin ne décrivent pas la **fabrication** d'une pièce de marque : ce qui suit applique les règles du moteur. Considère-le comme **à vérifier** au premier essai.

1. **Un dossier par élément, versionné** : `marque/<element>-v1/`. Vérifie qu'il n'existe pas. Un dossier existant ne se modifie jamais : une correction va dans `-v2`. Les binaires (`mp4`, `mov`, `wav`, `mp3`, `png`, `jpg`, `ttf`) passent en Git LFS.
2. **Deux voies.**
   - **Tu fournis le fichier fini**, fait avec l'outil de ton choix. Claude le contrôle (C8).
   - **Claude le fabrique avec HyperFrames.** Règles du moteur (`production.md` § 2 pour les producteurs) : HyperFrames 0.8.149, Node 22 par Git Bash, animations en WAAPI et CSS seulement, `npx hyperframes check` sans erreur, une planche par `snapshot … --describe false`, un `render.sh` avec `--workers 2` (il refuse d'écraser), jamais de `preview` sans ta demande. Pour la structure d'un projet, le seul modèle du plugin est le gabarit de séquence v3 (`index.html`, `render.sh`) ; Claude peut en reprendre l'ossature, sans `voix.py` ni les moments d'exemple. Proposition : range le projet source dans le dossier de l'élément, à côté du MP4, pour pouvoir le refaire.
3. **Inspiration** : les skills HyperFrames installés en A5 contiennent des modèles de fins de film et d'appels (`~/.claude/skills/hyperframes-animation/blueprints/logo-assemble-lockup.md`, rôle `Brand_Outro` ; `cta-morph-press.md`, rôle `CTA`). Leurs exemples emploient GSAP, alors que la règle du plugin pour les productions est WAAPI et CSS seulement et aucun `npm install` : adapte-les, ne les recopie pas (à vérifier).
4. **Format** : l'assembleur n'accepte que du **1920 × 1080 à 30 i/s** (`assembler.py`, message « Format inattendu »). Une pièce de marque garde **son propre son** dans le film voix et son niveau d'origine au mix (le gain final ne s'applique pas sous la marque).
5. **Couleurs** : la signature et l'outro peuvent porter les couleurs de marque, même interdites dans les films.
6. **Provenance** : polices, images et sons employés vont dans un `PROVENANCE.md` du dossier de l'élément.
7. **Son d'une pièce** : si elle a besoin d'un son nouveau, la même règle s'applique qu'aux autres sons : génération seulement à ta demande, estimation, accord (C18).
8. **Validation** : tu regardes et tu écoutes ; Claude ne le fait pas. Il note le statut dans le tableau de `marque/README.md` : `VALIDÉ, <prénom>, JJ/MM/AAAA`.

### C4. Fabriquer le logo et la bannière
- **Qui** : toi (tu fournis ou tu valides), Claude (il fabrique si tu le demandes).
- **À faire** : applique la méthode commune. Pour une image fixe, le seul chemin décrit dans les fichiers est une page HTML rendue en PNG par le Chrome de HyperFrames (c'est ainsi que se font les miniatures, en 1280 × 720). Pour un logo et une bannière à d'autres tailles, ce chemin est **à vérifier**. La taille de bannière attendue par YouTube n'est écrite dans aucun fichier : lis-la dans YouTube Studio.

> Fabrique le logo de la chaîne dans `marque/identite-chaine-01/`, d'après les couleurs et polices validées de `marque/README.md`. Propose deux pistes, ne valide rien. Range les polices et leurs licences à côté et note-les dans un `PROVENANCE.md`.

- **Fichiers créés** : `marque/identite-chaine-01/` (logo, bannière, `PROVENANCE.md`).
- **Tu valides** : le logo et la bannière, `VALIDÉ, <prénom>, JJ/MM/AAAA` dans le tableau de `marque/README.md`.
- **Vérifier** : le dossier est nouveau, les fichiers s'ouvrent, les licences sont à côté. Le logo sera réemployé tel quel dans les miniatures.
- **Détail** : [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md), étape 10.

### C5. Fabriquer la signature
- **Qui** : toi (tu fournis ou tu valides), Claude (il fabrique si tu le demandes).
- **Rôle** : une courte pièce MP4 placée **juste après l'accroche** du film, avec **0,5 s de noir de part et d'autre** (règle gardée du skill `episode`, étape 2 ; `montage.json`, clé `marque`, `apres: "seq1"`).
- **À faire** : applique la méthode commune. Le son de la pièce reste le sien au collage. La séquence qui suit la signature démarre sur une musique d'ouverture de documentaire, jamais sur des voix de foule (`collage-et-mix.md`).

> Fabrique la signature de la chaîne dans `marque/<signature-v1>/` (choisis le nom du dossier avec moi) : un MP4 de 1920 × 1080 à 30 i/s, avec sa piste son. Applique la méthode commune aux pièces de marque (dossier versionné, HyperFrames en WAAPI et CSS, `check`, planche, `render.sh`). Ne valide rien.

- **Fichiers créés** : `marque/<signature-v1>/` (MP4, source, `PROVENANCE.md`).
- **Tu valides** : tu la regardes et l'écoutes, puis `VALIDÉ, <prénom>, JJ/MM/AAAA` au tableau de `marque/README.md`.
- **Vérifier** : C8.
- **Détail** : [`collage-et-mix.md`](docs/workflows/collage-et-mix.md), étape 2 ; fiche `BRAND-SPLIT` de [`MOTION_CATALOG.md`](plugins/studio-faceless/referentiels/MOTION_CATALOG.md).

### C6. Fabriquer l'appel Like et Subscribe
- **Qui** : toi (tu fournis ou tu valides), Claude (il fabrique si tu le demandes).
- **Rôle** : un **overlay** de `marque/`, posé **dans** une séquence selon la technique `HOLD-CALL` : après la dernière phrase de la séquence, on tient sa dernière image environ 4 s et l'overlay se pose au début de cette pause ; les clics sont hors de toute voix ; l'overlay ne couvre ni texte ni étiquette. Sa musique et ses clics se posent **au mix du film**, pas dans la séquence. La place par défaut est **vers 2:00**, juste après l'ouverture d'une question, jamais juste après une réponse (`METHODE_RECIT.md` § 1). La porte de l'angle (C11) la confirme ou l'écarte.
- **À faire** : applique la méthode commune. **Il doit exister avant la production de la séquence qui le porte** (C20 ou C22), car le producteur le pose dans sa composition.

> Fabrique l'appel Like + Subscribe de la chaîne dans `marque/<appel-v1>/`, en overlay pour la technique HOLD-CALL. Dis-moi d'abord quel format tu proposes (vidéo avec transparence, ou composition HTML copiée dans la séquence), car les fichiers du plugin ne le précisent pas.

- **Fichiers créés** : `marque/<appel-v1>/`.
- **Tu valides** : le format proposé, puis l'overlay (`VALIDÉ, <prénom>, JJ/MM/AAAA`).
- **Vérifier** : le format est **à vérifier** : le collage n'a pas de pièce dédiée pour l'appel ; il est posé dans la séquence par son producteur. Ce qu'il vaut se mesure à J+7 (C30), sur la perte au moment de l'appel.
- **Détail** : fiche `HOLD-CALL` de [`MOTION_CATALOG.md`](plugins/studio-faceless/referentiels/MOTION_CATALOG.md) ; [`collage-et-mix.md`](docs/workflows/collage-et-mix.md).

### C7. Fabriquer l'outro
- **Qui** : toi (tu fournis ou tu valides), Claude (il fabrique si tu le demandes).
- **Rôle** : l'écran de fin, un MP4 posé en dernier (`montage.json`, clé `outro`). Fin du film en douceur, validée sur AA (28/10/2026) : fondu `"seqN>noir"` de 36 images, noir de 4,0 s (`noir_avant`), fondu `"noir>outro"` de 15 images. Le morceau de fin de la musique est calé pour que l'accord final tombe sur le noir.
- **À faire** : applique la méthode commune.

> Fabrique l'outro de la chaîne dans `marque/<outro-v1>/` : un MP4 de 1920 × 1080 à 30 i/s, avec sa piste son. Applique la méthode commune aux pièces de marque. Ne valide rien.

- **Fichiers créés** : `marque/<outro-v1>/`.
- **Tu valides** : tu la regardes et l'écoutes, puis `VALIDÉ, <prénom>, JJ/MM/AAAA`.
- **Vérifier** : C8.
- **Détail** : [`collage-et-mix.md`](docs/workflows/collage-et-mix.md), étape 2.

### C8. Contrôler les pièces de marque
- **Qui** : Claude.
- **À faire** : pour chaque MP4 de `marque/` (signature, outro, appel s'il est en vidéo), ces contrôles. Ils sont déduits de `assembler.py` : à vérifier au premier collage.

| Contrôle | Commande | Réponse attendue |
|---|---|---|
| Format | `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 <fichier>` | `1920,1080,30/1` |
| Piste son | `ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 <fichier>` | un nom de codec. Une réponse vide veut dire « pas de piste son » : ce que fait alors l'assembleur est à vérifier |
| Niveau | `python -I -B "<plugin>/outils/controle/controle.py" niveau <fichier>` | une mesure, à noter dans `PROVENANCE.md` (aucune cible n'est écrite pour la signature ni l'outro) |
| Git LFS | `git lfs ls-files`, après `git add` | les MP4 de `marque/` figurent dans la liste |

  Puis un commit local :
```bash
git add marque
```
```bash
git commit -m "marque : identité, signature, appel et outro"
```
- **Fichiers créés** : un commit local.
- **Tu valides** : le tableau de `marque/README.md` est complet, chaque élément avec son statut et sa date.
- **Vérifier** : le commit passe le contrôle `verifier_depot.py` (rien de plus de 10 Mo hors LFS).
- **Détail** : [`depot-git.md`](docs/workflows/depot-git.md), partie B.

**Tu es prêt pour l'épisode quand** : la voix, les couleurs, les polices, le logo, la signature, l'outro sont validés ; l'appel l'est avant la séquence qui le porte.

---

### C9. Choisir le sujet
Étape 0 du skill `episode`.
- **Qui** : Claude (Studio Director) propose, toi tu choisis.
- **À faire** :

> On démarre l'épisode 1 de la chaîne avec le skill `studio-faceless:episode`. Étape 0, le sujet : avec `studio-faceless:grilling`, ouvre la porte « Sujet » (`grilles.md` § 0). Propose 5 à 8 candidats notés, vérifie la saturation, écris la promesse en une phrase et le titre en 60 caractères au plus. Crée `episodes/episode-001/` à partir des modèles du plugin et inscris le sujet au registre de `direction/LIGNE_EDITORIALE.md`.

  La porte pose huit questions, chacune avec sa réponse recommandée : le spectateur résume-t-il le sujet en cinq mots ; un non-initié comprend-il la question ; qui est l'acteur connu, quel acte intrigant, où est le motif écrit ; quel renversement vers 75 % ; quel cas à suivre ; faut-il une carte ; le sujet est-il saturé ; quelle durée (défaut : 8 à 10 min, 6 ou 7 séquences). Les candidats sont notés sur 45 (seuil 33/45, aucun critère double sous 3). Le skill n'indique aucune commande de création du dossier : Claude copie `CLAUDE.episode.template.md` et `BRIEF.episode.template.md`, après avoir vérifié que `episodes/episode-001/` n'existe pas. Une chaîne neuve n'a ni registre, ni veille, ni bilans à lire.
- **Fichiers créés** : `episodes/episode-001/CLAUDE.md` et `BRIEF.md` ; une ligne au registre de `LIGNE_EDITORIALE.md`. Dossiers prévus par le modèle : `inputs/`, `research/`, `assets/`, `kit/`, `production/`, `montage/`, `outputs/`, `miniatures-vN/`.
- **Tu valides** : tu **choisis parmi les trois premiers candidats**. Statut du sujet au `BRIEF.md` : « candidat », puis « validé pour recherche ».
- **Vérifier** : le dossier existe ; le registre porte le sujet ; le `BRIEF.md` donne le statut.
- **Détail** : [`episode.md`](docs/workflows/episode.md#0-sujet).

### C10. Faire la recherche
Étape 1.
- **Qui** : Claude lance l'agent `studio-faceless:research` (lecture seule), une mission par grande partie.
- **À faire** : tu réponds d'abord à la porte « Recherche » : quelles parties méritent une mission (défaut : le cas central, les précédents ou le mécanisme, les médias) ; quels points de vigilance (procédure en cours, personnes à protéger, chiffres de presse non officiels).

> Étape 1, la recherche : avec `studio-faceless:grilling`, ouvre la porte « Recherche ». Puis, pour chaque grande partie, écris un contrat de mission (écriture : aucune) et lance `studio-faceless:research`. Consigne chaque rapport dans `episodes/episode-001/research/R-*.md`. Aucun téléchargement.

  Chaque rapport a cinq rubriques : faits, études, médias candidats, limites et questions ouvertes, fichiers lus. L'agent n'écrit pas : Claude consigne. Un complément se fait avec un **nouvel** agent.
- **Fichiers créés** : `episodes/episode-001/research/R-*.md` ; les points de vigilance dans le `CLAUDE.md` de l'épisode.
- **Tu valides** : tes réponses à la porte ; tu tranches les légendes d'auteur importées de Flickr et les risques d'image que Claude te signale.
- **Vérifier** : chaque fait a sa source, sa date de consultation et un statut (vérifié, plausible, non vérifié) ; aucun média n'est téléchargé.
- **Détail** : [`recherche.md`](docs/workflows/recherche.md).

### C11. Valider l'angle et le découpage
Étape 2.
- **Qui** : Claude propose, toi tu valides.
- **À faire** :

> Étape 2, l'angle et le découpage : avec `studio-faceless:grilling`, ouvre la porte « Angle et découpage » (`grilles.md` § 2), puis écris `ANGLE_DECOUPAGE_v1.md` : la question en une phrase, la promesse, les couches et leurs révélations, le renversement vers 75 %, les séquences et la question qui finit chacune.

  Repères de la porte (méthode de récit, validés sur AA) : la question posée avant 0:45 ; l'accroche et l'image de 0:00 à 0:15 ; la première pièce de réponse avant 1:30 ; chaque séquence finit sur la question que la suivante reprend ; la signature de la chaîne vient après l'accroche ; le rappel d'abonnement vers 2:00, ou ailleurs si la porte le décide.
- **Fichiers créés** : `episodes/episode-001/ANGLE_DECOUPAGE_v1.md` ; décisions au `BRIEF.md`.
- **Tu valides** : l'angle et le découpage : `VALIDÉ, <prénom>, JJ/MM/AAAA`.
- **Vérifier** : le `BRIEF.md` porte les réponses de la porte, datées.
- **Détail** : [`episode.md`](docs/workflows/episode.md#2-angle-et-découpage).

### C12. Écrire et valider le script
Étape 3.
- **Qui** : Claude rédige, toi tu valides.
- **À faire** :

> Étape 3, le script : avec `studio-faceless:grilling`, ouvre la porte « Script » (`grilles.md` § 3). Écris une fiche de narration par séquence (`SEQUENCES_*_NARRATION.md`) : chaque phrase avec sa source, le plan de plans, le son, la fiche d'ouverture de 0 à 2:00. Écris aussi `SCRIPT_v1.md`, avec un titre `## seqN` par séquence et la narration dans un bloc ```text, sans balise ElevenLabs. Marque [MAJ] les phrases d'actualité. Fais les contrôles de densité avant la voix et signale-les.

  Le fichier `SCRIPT_v1.md` servira plus tard aux sous-titres (`srt.py` lit ses blocs ```text sous `## seqN`). Contrôles de densité (`recit-retention.md` § 5) : au plus trois chiffres d'affilée ; chaque chiffre clé en paire ou comparé à un repère ; chaque inconnu expliqué en moins de 5 s ; au plus trois noms propres nouveaux par minute. Script **sans balise** : une balise d'émotion (`[calm]`, `[thoughtful]`, `[serious]`, `[softly]`) seulement là où un passage l'exige, jamais de balise de pause ni de vitesse. Le skill `humanizer` est à l'essai (`PROPOSÉ`, 28/10/2026) pour une passe sur la narration en anglais ; il n'est pas intégré au skill `episode`.
- **Fichiers créés** : `episodes/episode-001/SEQUENCES_*_NARRATION.md` ; `SCRIPT_v1.md`.
- **Tu valides** : le script, `VALIDÉ` avant toute voix. Il ne change plus ensuite : toute modification de texte après les prises oblige à refaire la prise.
- **Vérifier** : chaque phrase a sa source ; les contrôles de densité sont faits et signalés ; la fiche d'ouverture couvre 0 à 2:00.
- **À savoir** : le modèle `BRIEF.episode.template.md` fixe « français » et « anglais » ; pour d'autres langues, voir B9.
- **Détail** : [`episode.md`](docs/workflows/episode.md#3-script).

### C13. Générer les prises de voix
Étape 4, première partie.
- **Qui** : **toi.** Claude ne génère pas la voix dans ce parcours, et aucun sous-agent n'appelle ElevenLabs.
- **À faire** : Claude te donne le texte de chaque séquence et la liste des mots à réécouter (noms propres, nombres). Tu génères chaque prise dans ElevenLabs avec la voix validée en C2, en collant le texte tel quel (sans balise ajoutée par habitude), puis tu la déposes dans `episodes/episode-001/inputs/voix/`. Les entrées d'un épisode sont des **fichiers protégés** : les producteurs et le mainteneur ne peuvent pas les modifier.
- **Fichiers créés** : `episodes/episode-001/inputs/voix/<prise>.mp3`, une par séquence.
- **Tu valides** : rien encore. La voix n'est validée qu'en C15.
- **Vérifier** : il y a une prise par séquence, sous le nom que Claude a donné.
- **Détail** : [`voix-off.md`](docs/workflows/voix-off.md), étapes 1 à 3.

### C14. Contrôler les prises contre le texte
Étape 4, deuxième partie.
- **Qui** : Claude, dès réception de chaque prise.
- **À faire** : le texte de référence contient **uniquement la narration** (sans titre Markdown : il créerait de faux écarts). Le dossier de travail est neuf ; l'outil refuse d'écraser.
```bash
python -I -B "<plugin>/outils/controle/transcrire.py" episodes/episode-001/inputs/voix/<prise>.mp3 --modele <dossier-du-modèle>/ggml-base.en.bin --sortie <dossier-de-travail> --texte <narration-de-la-séquence>.txt
```
  Pour vérifier un écart douteux sur le passage isolé (début 37,5 s, durée 4,5 s ; rien n'est écrit) :
```bash
python -I -B "<plugin>/outils/controle/transcrire.py" episodes/episode-001/inputs/voix/<prise>.mp3 --modele <dossier-du-modèle>/ggml-base.en.bin --isoler 37.5 4.5
```
  Les nombres en chiffres, les accents perdus et les noms propres approximatifs ne sont **pas** des écarts. Un mot « doublé » est souvent un artefact de Whisper : toujours `--isoler` avant de signaler.
- **Fichiers créés** : dans `--sortie` : `<prise>-texte.txt`, `<prise>-mots.json`, `<prise>-phrases.txt`.
- **Tu valides** : s'il reste un **écart réel**, Claude te le signale en tête du compte rendu et **tu décides** : nouvelle prise, ou acceptation. Claude ne corrige pas le texte pour qu'il colle à la prise sans ton accord.
- **Vérifier** : tous les écarts restants sont des artefacts vérifiés, ou tranchés par toi.
- **Détail** : [`voix-off.md`](docs/workflows/voix-off.md), étape 4.

### C15. Ralentir, recaler et figer la voix
Étape 4, troisième partie.
- **Qui** : Claude, puis toi pour figer la voix.
- **À faire** : le dossier `kit/voix/` doit exister (l'outil ne le crée pas, à vérifier).
```bash
mkdir -p episodes/episode-001/kit/voix
```
  Ralentissement (tempo ×0,97 par défaut, ou la valeur de `direction/ECARTS.md`) :
```bash
python -I -B "<plugin>/outils/controle/ralentir.py" episodes/episode-001/inputs/voix/<prise>.mp3 episodes/episode-001/kit/voix/<bande>.wav
```
  Mots horodatés de la bande ralentie (sans `--texte`) :
```bash
python -I -B "<plugin>/outils/controle/transcrire.py" episodes/episode-001/kit/voix/<bande>.wav --modele <dossier-du-modèle>/ggml-base.en.bin --sortie <dossier-de-travail>
```
  Recalage des repères sur les vrais départs de la voix. Ne donne **jamais** les mots non recalés aux producteurs : leurs débuts arrivent jusqu'à 1,6 s trop tôt.
```bash
python -I -B "<plugin>/outils/shorts/recaler.py" episodes/episode-001/kit/voix/<bande>.wav <dossier-de-travail>/<bande>-mots.json episodes/episode-001/kit/voix/<séquence>-montage
```
  Claude écrit `kit/voix/README.md` : durée de chaque bande, silences (S1…), pauses de respiration. Il vérifie dans `<bande>.positions.txt` : tempo conforme, environ −19 LUFS en mesure mono, crête vraie ≤ −2 dBTP, « auto-contrôle : 0 recopie exacte ». Il calcule le débit (mots par minute, pauses comprises) et le note. La cible de 130 à 135 vient d'AA, en anglais.
- **Fichiers créés** : `kit/voix/<bande>.wav`, `<bande>.positions.txt`, `<séquence>-montage-mots-recales.json`, `<séquence>-montage-phrases-recalees.txt`, `README.md`.
- **Tu valides** : **tu figes la voix.** Claude écrit la décision datée, avec son statut `VALIDÉ`, au `BRIEF.md`, et l'état dans le `CLAUDE.md` de l'épisode. Désormais, toute nouvelle prise oblige à recaler toutes les séquences.
- **Vérifier** : les phrases ne se chevauchent pas, aucun mot n'a une durée nulle ; si l'auto-contrôle trouve une recopie, l'outil n'écrit rien et donne les instants : ne force pas, cherche la cause.
- **À savoir** : le skill `episode` ne nomme pas `recaler.py` ; `voix-off.md` le range dans `outils/shorts/` et demande de vérifier avec toi avant d'en faire la règle des épisodes (à vérifier).
- **Détail** : [`voix-off.md`](docs/workflows/voix-off.md), étapes 5 à 9.

### C16. Fixer la direction artistique et poser le gabarit
Étape 5, première partie.
- **Qui** : Claude propose, toi tu valides sur une planche. `studio-faceless:art-director` seulement si tu le demandes.
- **À faire** :

> Étape 5, le socle. Avec `studio-faceless:grilling`, ouvre la porte « Socle » (`grilles.md` § 5), partie direction artistique : écris une page courte (un motif matériel tiré de vraies photos, un monde et une transition par partie, trois moments à réussir par séquence, les quotas d'effets rares), fais une planche de test, et copie le gabarit de séquence v3 dans `episodes/episode-001/kit/gabarit` après avoir vérifié que ce dossier n'existe pas.

  La commande de copie, que Claude lance :
```bash
cp -r "<plugin>/templates/sequence-gabarit-v3" episodes/episode-001/kit/gabarit
```
  La palette de l'histoire se règle en variables CSS dans `index.html` ; la base fixe vient de la marque. Défauts de la porte : un WHIP-JUMP par film, un surligneur deux fois au plus.
- **Fichiers créés** : `kit/gabarit/` ; la page de direction artistique (son emplacement exact n'est pas fixé : à vérifier) ; la planche de test.
- **Tu valides** : la planche de test et la palette. Choisis aussi si ta chaîne garde le fond par défaut du gabarit (papier charbon, brumes, grain, Newsreader).
- **Vérifier** : `kit/gabarit/` contient `index.html`, `compositions/`, `media/`, `PROVENANCE.md`, `README.md`, `render.sh`, `voix.py`.
- **Détail** : [`episode.md`](docs/workflows/episode.md#5-socle) ; [`sequence.md`](docs/workflows/sequence.md).

### C17. Réunir les médias
Étape 5, deuxième partie.
- **Qui** : Claude et l'agent `studio-faceless:research` cherchent ; **toi tu télécharges à la main** ; Claude vérifie et convertit.
- **À faire** :

> Étape 5, les médias : pour chaque moment de la voix, lance `studio-faceless:research` pour trouver la meilleure image, gratuite et sans filigrane (deux candidats au plus par moment), sans rien télécharger. Puis écris `kit/DEMANDE_TELECHARGEMENTS_v1.md` : pour chaque fichier, le lien de la page (pour Commons, « Original file »), le nom imposé, la taille et le rôle dans la scène. Crée le dossier de dépôt `kit/media/source-v1/manuel/`.

  Tu télécharges chaque fichier depuis la liste, sous le nom imposé (Wikimedia répond 429 aux téléchargements automatiques). Tu préviens Claude. Il vérifie :
  - les SHA-1, comparés à ceux de Commons quand l'API les donne ; les dimensions ;
  - une planche de tous les fichiers, regardée : il écarte filigrane, mauvais sujet, date fausse, mineur identifiable ;
  - les conversions sans agrandissement (1920 px au plus) dans `kit/media/photos-v1/` et `logos-v1/` ;
  - une section par fichier au `kit/PROVENANCE.md` (source, auteur, licence ou « citation », SHA-1, date et lieu, remarque).

  Règles : médias réels, aucune image générée par IA ; une photo appartient à **une seule séquence** (rappels voulus inscrits au `BRIEF.md`) ; extraits vidéo de 6 s au plus, réencodés avec `-g 15` pour qu'ils ne se figent pas au rendu ; planche de chaque extrait regardée avant de le décrire. Les vraies vidéos d'événements ne sont admises que pour les compétitions et instances listées dans ton `ECARTS.md` (B8).
- **Fichiers créés** : `kit/DEMANDE_TELECHARGEMENTS_v1.md`, `kit/media/source-v1/manuel/` (tes téléchargements), `kit/media/photos-v1/`, `kit/media/logos-v1/`, `kit/PROVENANCE.md`.
- **Tu valides** : tes téléchargements ; les risques de droits que Claude te signale.
- **Vérifier** : chaque fichier a sa section de provenance avec son SHA-1 ; `controle.py licences` ne signale aucune licence en attente ni exclue.
- **Détail** : [`recherche.md`](docs/workflows/recherche.md) ; [`episode.md`](docs/workflows/episode.md#5-socle).

### C18. Préparer les sons
Étape 5, troisième partie. **Ta bibliothèque `marque/son/` est vide.**
- **Qui** : Claude décide du besoin avec toi ; **toi tu demandes toute génération, tu accordes le coût, tu écoutes et tu choisis les variantes** ; Claude seul génère et télécharge.
- **Règle** : un épisode puise d'abord dans `marque/son/`. Comme elle est vide, la première vidéo doit **générer ses musiques, ambiances et effets**, un par un, avec ton accord. Les sons arrivent au mix du film, pas dans les séquences.
- **À faire** :

> Étape 5, les sons. Ma bibliothèque `marque/son/` est vide. Ouvre la porte « Quels sons ? » avec `studio-faceless:grilling`. Les générations passent par l'API ElevenLabs (clé posée par moi), jamais par le connecteur. Écris le contrat audio et la feuille de repérage, puis un brief par son (450 caractères au plus, des attributs, jamais « comme » un artiste). Montre-moi l'estimation en crédits et attends mon accord avant chaque lot. Aucune génération sans mon accord.

  Ce que les fichiers écrivent :
  - **coûts constatés sur AA** (20/10/2026, [`DIRECTION_AUDIO.md`](plugins/studio-faceless/referentiels/DIRECTION_AUDIO.md) § 4) : effets environ 3,3 crédits par seconde ; musique environ 27,5 crédits par seconde et par variante ;
  - **l'estimation affichée dépasse largement la facturation** (35 crédits facturés pour 115,5 estimés) : lis-la, mais n'en fais pas ton budget ;
  - **solution éprouvée sur AA** quand la musique est jugée trop chère : des nappes en boucle générées par le modèle d'effets (`loop: true`, 30 s, 2 variantes) ;
  - Suno, Udio et équivalents sont exclus sans ta décision ;
  - regroupe les générations : un lancement par lot de 20 au plus, `generations_count: 1` (ou 2 si tu dois choisir entre variantes) ; les liens de téléchargement expirent au bout de 2 h ;
  - les sons générés sont des **illustrations**, jamais le son réel d'un lieu ou d'un événement ;
  - le vrai son d'un extrait vidéo se **transcrit avant** de le prévoir : s'il porte un commentaire, une ambiance de la bibliothèque le remplace.
  Claude trie (une seule paire appui/relâchement pour un clic ; boucle dont le raccord est propre), puis tu écoutes et tu choisis.
- **Fichiers créés** : `kit/media/audio/musique/` et `sfx/` ; le registre des sons au `kit/PROVENANCE.md` (prompt, identifiant, crédits dépensés, licence de l'abonnement, SHA-1, « génération illustrative », « retenu » ou « provisoire ») ; le relevé musical par morceau (tempo, boucles sur mesures entières, silences voulus, rôle par séquence ; emplacement non fixé : à vérifier).
- **Tu valides** : chaque lot (accord du coût), puis le choix des variantes à l'écoute.
- **Vérifier** : chaque son a son SHA-1 et sa provenance. La bibliothèque `marque/son/` reste vide jusqu'à C31.
- **Détail** : [`sons.md`](docs/workflows/sons.md), parties A à C.

### C19. Finir le socle
Étape 5, fin.
- **Qui** : Claude, toi tu donnes le feu vert de production.
- **À faire** :

> Finis le socle : cartes (seulement pour un lieu qui porte l'argument), `kit/RACCORDS.md`, `kit/CONSIGNES_COMMUNES_v1.md`, un brief court par séquence (3 Ko environ, d'après `templates/CONTRAT_MISSION.template.md`). Puis montre-moi la liste de contrôle « Avant de lancer un producteur », case par case.

  Pour une carte, Claude écrit `SPEC.json` (voir `outils/cartes/README.md`). Le shapefile Natural Earth 1:50m se télécharge **par toi**, avec ton accord, avec son `.dbf` à côté du `.shp` :
```bash
python -I -B "<plugin>/outils/cartes/cartes.py" SPEC.json --shp episodes/episode-001/kit/donnees/ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp --out episodes/episode-001/kit/donnees
```
  `RACCORDS.md` donne, pour chaque jonction, l'image de sortie et l'image d'entrée **au pixel**. Les lots se composent pour qu'aucune séquence n'attende la sortie d'une autre du même lot. Les consignes communes adaptent la recette v3 au sujet (règles de l'épisode, médias déjà pris, cartes, méthode de sortie). L'emplacement des briefs n'est pas fixé : à vérifier.

  La liste « Avant de lancer un producteur » (`SKILL.md`) :
  - voix figée, repères recalés, durée de chaque bande ;
  - médias déposés, vérifiés, inscrits au `PROVENANCE.md` ;
  - aucune photo prise par une autre séquence ;
  - image d'entrée et de sortie au pixel ;
  - cartes, logos, dessins prêts ;
  - sons choisis ; le producteur ne mixe rien ;
  - brief court ;
  - gabarit v3 avec en-têtes HTML contrôlés ;
  - contrat de mission complet.
- **Fichiers créés** : `kit/donnees/` (si carte), `kit/RACCORDS.md`, `kit/CONSIGNES_COMMUNES_v1.md`, les briefs.
- **Tu valides** : le feu vert de production.
- **Vérifier** : toutes les cases sont cochées, et l'appel Like + Subscribe de C6 existe si une séquence le porte. Réécris le `STATE.md`, mets à jour l'`INDEX.md`, puis je lance `/clear` (voir « Le rythme de travail »).
- **Détail** : [`episode.md`](docs/workflows/episode.md#5-socle) ; [`sequence.md`](docs/workflows/sequence.md), partie A.

### C20. Lancer la séquence témoin
Étape 6, première partie.
- **Qui** : Claude écrit le contrat ; l'agent `studio-faceless:motion-producer` met en scène jusqu'à `render.sh`.
- **À faire** : tu choisis la séquence témoin avec Claude (porte `grilles.md` § 6) : la séquence qui porte le plus de techniques nouvelles, ou la plus difficile, et qui ne dépend d'aucune autre pour ses raccords. Reste présent : aucune demande de permission ne doit rester en attente.

> Étape 6, la séquence témoin. Ouvre la porte « Séquence témoin » avec `studio-faceless:grilling`. Une fois la séquence choisie, écris le contrat de mission complet (`templates/CONTRAT_MISSION.template.md` plus `production.md` § 2) et lance `studio-faceless:motion-producer` dans `episodes/episode-001/production/<séquence>-v1/`, qui ne doit pas exister. Il s'arrête à `render.sh` et ne rend rien.

  Le producteur écrit d'abord la **fiche d'effets** en tête de son README (pour chaque moment : la technique, l'idée du récit qu'elle sert, l'effet sonore proposé). Pour une première vidéo, le champ « épisode précédent » du brief est « aucun ». Il vérifie `check` et une planche. Il ne lance jamais `preview`, ne télécharge rien et ne met ni musique ni effet dans la séquence.

  À son retour, Claude vérifie le livrable : la planche regardée, `check` sans erreur (0 remarque visée), l'en-tête HTML de chaque `index.html` (aucun texte nu dans `<head>`), la fiche d'effets, les couleurs.
```bash
npx hyperframes check episodes/episode-001/production/<séquence>-v1
```
```bash
python -I -B "<plugin>/outils/controle/controle.py" couleurs episodes/episode-001/production/<séquence>-v1/index.html
```
- **Fichiers créés** : `episodes/episode-001/production/<séquence>-v1/` (copie du gabarit, `index.html`, `compositions/`, `media/`, `voix.py`, `render.sh`, `README.md` avec la fiche d'effets en tête, `PROVENANCE.md`, planche). `ETAT.md` si le plafond de contexte de 300 k est atteint.
- **Tu valides** : le choix de la séquence témoin.
- **Vérifier** : fiche d'effets présente avec une raison à chaque choix, sans quoi la séquence n'est pas présentée. La planche compte 16 à 20 instants, ou 16, ou 24 selon les fichiers du plugin : suis le contrat de mission (`docs/POINTS_OUVERTS.md`).
- **Détail** : [`sequence.md`](docs/workflows/sequence.md), parties A et B ; [`episode.md`](docs/workflows/episode.md#6-séquence-témoin).

> **Pas encore éprouvé.** Le producteur ne peut écrire que dans son projet de production parce que le garde-fou lui donne son rôle d'après `agent_type`. Si une commande légitime du producteur est refusée, ou si une commande interdite passe, c'est le test à noter (voir « Si quelque chose bloque »).

### C21. Rendre et valider la séquence témoin
Étape 6, deuxième partie.
- **Qui** : Claude rend et contrôle, sans agent ; toi tu regardes.
- **À faire** : Claude rend la séquence **en tâche suivie**, un rendu à la fois, puis contrôle. Le script attend la fin des rendus des autres sessions.
```bash
bash "<plugin>/outils/rendu/rendre_si_libre.sh" episodes/episode-001/production/<séquence>-v1/render.sh episodes/episode-001/production/<séquence>-v1/rendu.log.txt
```
```bash
python -I -B "<plugin>/outils/controle/controle.py" tout --projet episodes/episode-001/production/<séquence>-v1 <mp4>
```
```bash
python -I -B "<plugin>/outils/controle/controle.py" planche --sortie episodes/episode-001/production/<séquence>-v1/controle-planche --pas 4 <mp4>
```
```bash
python -I -B "<plugin>/outils/controle/controle.py" tremblement <mp4>
```
```bash
python -I -B "<plugin>/outils/controle/controle.py" son --voix episodes/episode-001/production/<séquence>-v1/pistes/stem-voix.wav <mp4>
```
```bash
python -I -B "<plugin>/outils/controle/controle.py" chrome
```
  `<mp4>` est le fichier écrit à côté de `render.sh`. Le contrôle `son` ne sert que si la séquence a une piste mixée et une voix séparée ; une séquence v3 ne porte que la voix, il est alors sans objet. Lecture des contrôles : `tout` donne niveau, couleurs, licences, Chrome (un écart de niveau est attendu en voix seule, puisqu'il n'y a pas de cible de sonie avant le mix du film ; à vérifier sur ce premier rendu). Le tremblement se lit avec méthode : des crans d'un pixel sur une photo qui dérive sont tolérés, pas sur du texte. `chrome` doit répondre 0. Claude **regarde la planche, une planche à la fois**, avant de te montrer quoi que ce soit.
  Pour une correction, le rendu déjà fait est rangé dans `_rendu-N/` avec sa planche (`render.sh` refuse d'écraser).
- **Fichiers créés** : le MP4 de la séquence, `controle-planche/`, `rendu.log.txt`.
- **Tu valides** : **tu regardes la séquence et tu valides la recette.** Ta réponse passe dans les consignes communes avant les lots. Statut posé par Claude avant ton visionnage : `MESURES_TECHNIQUES_OK`. Après : `CORRECTIONS_DEMANDEES`, ou ta validation.
- **Vérifier** : aucune image immobile plus de 1 s, aucun cadre vide, texte lisible, aucun Chrome resté ouvert. Une mesure ne vaut jamais un visionnage.
- **Détail** : [`rendu-et-controle.md`](docs/workflows/rendu-et-controle.md) ; [`episode.md`](docs/workflows/episode.md#6-séquence-témoin).

### C22. Produire les autres séquences par lots de trois
Étape 7.
- **Qui** : Claude, avec un `studio-faceless:motion-producer` par séquence, **trois producteurs au plus par lot**.
- **À faire** :

> Étape 7, la production. Ouvre la porte « Production » (`grilles.md` § 7) et compose les lots. Pour chaque séquence, écris un contrat de mission avec l'image de sortie exacte de la séquence précédente, la liste des photos déjà prises et les quotas d'effets rares consommés, puis lance `studio-faceless:motion-producer`. Vérifie chaque livrable à son retour. Reporte dans les consignes communes ce que j'ai dit sur la séquence témoin.

  Option, à décider à cette porte : lancer tous les producteurs d'un coup après la séquence témoin ; les rendus restent un à la fois. Elle exige tous les raccords écrits au pixel et les photos réparties d'avance. Par défaut : lots de trois. Un défaut trouvé sur une planche se corrige **sur place**, dans la même version (voir C23).
- **Fichiers créés** : `episodes/episode-001/production/<séquence>-v1/` pour chaque séquence.
- **Tu valides** : la composition des lots.
- **Vérifier** : pour chaque livrable, les mêmes contrôles qu'en C20, et la fiche d'effets.
- **Détail** : [`sequence.md`](docs/workflows/sequence.md) ; [`episode.md`](docs/workflows/episode.md#7-production).

### C23. Rendre les séquences une à une
Étape 8.
- **Qui** : Claude, sans agent ; toi tu regardes chaque séquence.
- **À faire** : **un rendu à la fois**, dans **une seule tâche suivie** qui enchaîne la file (une tâche détachée ne prévient jamais). Quatre rendus en parallèle peuvent faire passer un rendu de 10 minutes à plus de 5 heures. Exemple de file :
```bash
for q in seq2 seq3 seq4; do bash "<plugin>/outils/rendu/rendre_si_libre.sh" episodes/episode-001/production/$q-v1/render.sh episodes/episode-001/production/$q-v1/rendu.log.txt; done
```
  Puis, pour chaque séquence, les contrôles de C21. Avant le collage, contre les photos répétées :
```bash
python -I -B "<plugin>/outils/controle/controle.py" doublons episodes/episode-001/production/seq1-v1/media episodes/episode-001/production/seq2-v1/media
```
  (ajoute le dossier `media` de chaque séquence). Si le rendu s'arrête sans message (code 1), relance-le **une fois** à l'identique avec un nouveau journal avant de chercher la cause.
- **Fichiers créés** : un MP4 par séquence et son `controle-planche/`.
- **Tu valides** : tu regardes chaque séquence ; `CORRECTIONS_DEMANDEES` si tu veux des retouches, ou ton approbation (`APPROUVE_PAR_<ton prénom>`, avec la date) quand elle te convient. Une correction se fait **dans la même version** : reprise du producteur si son cache est chaud (moins de 5 min), sinon un agent court avec un brief de quelques lignes. Une nouvelle version (`-v2`) seulement pour un défaut majeur. L'ancien rendu va dans `_rendu-N/`.
- **Vérifier** : `MESURES_TECHNIQUES_OK` pour chaque séquence, `controle.py chrome` à 0, aucune photo répétée. Le collage ne commence que quand **toutes** les séquences sont validées par toi.
- **À savoir** : la porte de l'étape 8 n'a pas de banque de questions (`docs/POINTS_OUVERTS.md`, D4) ; Claude te demande l'ordre des rendus.
- **Détail** : [`rendu-et-controle.md`](docs/workflows/rendu-et-controle.md) ; [`episode.md`](docs/workflows/episode.md#8-rendus).

### C24. Coller le film en voix seule
Étape 9.
- **Qui** : Claude.
- **À faire** : tu as validé toutes les séquences, et la signature et l'outro existent (C5, C7).

> Étape 9, le collage en voix seule. Vérifie d'abord les jonctions (dernière image de chaque séquence contre première de la suivante, PSNR et planche des paires). Puis écris `episodes/episode-001/montage/montage.json` avec les séquences dans l'ordre, la signature juste après `seq1` avec 0,5 s de noir de chaque côté, l'outro avec `noir_avant` 4,0, les fondus, la fin en douceur (`"seqN>noir"` 36 images, `"noir>outro"` 15 images) et les noms de sortie. Fais l'essai sans écriture, puis le collage en tâche suivie.

  Si seuls des crédits ou une plaque changent à une jonction, un fondu de 4 à 6 images suffit ; si l'image saute, **on corrige la séquence**, pas le collage. L'essai, qui n'écrit rien et ne code pas l'image :
```bash
python -I -B "<plugin>/outils/montage/assembler.py" --episode episode-001 --voix-seule --son-seul
```
  Le collage (22 min pour 15 655 images sur AA ; environ 2 à 3 Go de mémoire pour un film de 9 min) :
```bash
python -I -B "<plugin>/outils/montage/assembler.py" --episode episode-001 --voix-seule
```
  L'assembleur est autorisé sans demande par `.claude/settings.json`. **Il sort en code 0 même quand son journal dit ÉCART** : Claude lit le journal. Il vérifie le nombre d'images attendu, le début de chaque séquence, la ligne `Contrôles du MP4 : OK` et le décodage complet.
- **Fichiers créés** : `episodes/episode-001/montage/montage.json` ; dans `outputs/` : `<nom_voix>.mp4`, `<nom_voix>.voix.wav`, `<nom_voix>.log.txt`, `<nom_voix>.journal.json`. Le `.log.txt` du film voix sert aux chapitres et au SRT.
- **Tu valides** : rien d'obligatoire. La porte de l'étape 9 (« marque, appel, jonctions ») n'a pas de banque de questions (D4) : Claude te pose celles qu'il juge utiles.
- **Vérifier** : images attendues, jonctions mesurées. Une correction d'image repasse par la séquence, un nouveau rendu et un nouveau collage vers un nom neuf.
- **À savoir** : l'assembleur lit les clés `marque` et `outro` avec `c.get(...)` : elles sont facultatives pour l'outil. Mais la règle du plugin veut la signature après l'accroche et l'outro à la fin.
- **Détail** : [`collage-et-mix.md`](docs/workflows/collage-et-mix.md), partie A ; [`episode.md`](docs/workflows/episode.md#9-collage-en-voix-seule).

### C25. Mixer le film
Étape 10. Un seul mix, sur le film collé.
- **Qui** : Claude écrit et mixe ; toi tu réponds à la porte et tu écoutes.
- **À faire** :

> Étape 10, le mix du film. Ouvre la porte « Mix du film » (`grilles.md` § 10) avec `studio-faceless:grilling` : effets retenus (ceux des tableaux des producteurs, sans les facultatifs), niveaux par type, où la musique continue ou se tait, place du rappel d'abonnement. Écris `episodes/episode-001/montage/plan-son.json`, fais l'essai, puis le mix.

  Niveaux de départ, en LU sous la voix (à calibrer à ta première écoute) :

| Type | Niveau |
|---|---|
| musique | 13 (plage 12 à 15) |
| ambiance en boucle | 16 |
| impact, battement | 14 |
| souffle, whoosh | 18 |
| montée | 16, coupée avant la phrase |
| papier, craie, surligneur, déclic | 20 |

  La musique baisse de 3 à 5 dB sous la voix. Avant une révélation, elle baisse d'environ 8 dB en rampes de 0,8 s au lieu de se couper. Un seul gain final vers −16 LUFS ; la signature et l'outro gardent leur niveau d'origine ; limiteur à −2,0 dBTP.

  Dans le plan, la clé `racine` est un simple dossier : le kit de l'épisode convient tant que `marque/son/` est vide. Attention : le kit range les effets dans `sfx/`, alors que l'exemple du plan parle de `effets/` : écris le chemin réel. Le `type` de chaque effet doit être **identique** à une clé de `niveaux_par_type` (`montee` n'est pas `montée`).
```bash
python -I -B "<plugin>/outils/montage/mix_film.py" episodes/episode-001/outputs/<nom_voix>.mp4 episodes/episode-001/montage/plan-son.json --son-seul
```
```bash
python -I -B "<plugin>/outils/montage/mix_film.py" episodes/episode-001/outputs/<nom_voix>.mp4 episodes/episode-001/montage/plan-son.json
```
  Le premier est l'essai (rien n'est écrit) : itère sur le plan jusqu'à ce qu'il convienne. Le second écrit le master ; l'image est copiée telle quelle. Contrôles du master :
```bash
python -I -B "<plugin>/outils/controle/controle.py" niveau episodes/episode-001/outputs/<nom>.mp4
```
```bash
python -I -B "<plugin>/outils/controle/controle.py" planche episodes/episode-001/outputs/<nom>.mp4 --sortie <dossier-de-contrôle> --pas 8
```
- **Fichiers créés** : `montage/plan-son.json` ; dans `outputs/` : `<nom>.mp4` (master), `<nom>.mix.wav`, `<nom>.log.txt`.
- **Tu valides** : tes réponses à la porte ; puis **tu écoutes** le master (image seule, son seul, texte seul, complet ; puis en mono et sur petit haut-parleur). Claude ne déclare aucune écoute. Statuts : `MESURES_TECHNIQUES_OK`, puis `ECOUTE_A_FAIRE` jusqu'à ton écoute.
- **Vérifier** : −16 ±1 LUFS ; crête vraie ≤ −1,5 dBTP ; images identiques au film voix (empreinte MD5 du flux vidéo) ; décodage complet ; aucune jointure musicale avec saut de niveau ; planche toutes les 8 s regardée.
- **Détail** : [`collage-et-mix.md`](docs/workflows/collage-et-mix.md), partie B ; [`sons.md`](docs/workflows/sons.md) ; [`episode.md`](docs/workflows/episode.md#10-mix-du-film).

### C26. Donner tes retours et approuver
Étape 11.
- **Qui** : toi ; Claude corrige.
- **À faire** : tu regardes et tu écoutes le master, puis tu dis ce que tu veux changer. Claude range chaque changement :
  - **correction d'image** : sur place, dans la séquence, puis nouveau rendu (l'ancien MP4 va dans `_rendu-N/`), nouveau collage vers un nom neuf, nouveau mix ;
  - **correction de son** : un **remix**. Claude modifie `plan-son.json` et relance `mix_film.py` vers une nouvelle sortie, sans rendu d'image.
- **Fichiers créés** : `_rendu-N/`, nouveaux rendus ou remix ; une ligne « Correction du JJ/MM » au README de la séquence.
- **Tu valides** : `CORRECTIONS_DEMANDEES` tant que tu as des retours ; **`APPROUVE_PAR_<ton prénom>` (date)** quand le master te convient. Seul toi le poses. Un retour ne devient règle de ta chaîne qu'avec ton accord, versé dans `direction/`.
- **Vérifier** : le statut et la date sont écrits au `BRIEF.md` et au `CLAUDE.md` de l'épisode. `studio-faceless:art-director` ne critique un rendu que si tu le demandes.
- **À savoir** : la porte de l'étape 11 n'a pas de banque de questions (D4).
- **Détail** : [`episode.md`](docs/workflows/episode.md#11-retours) ; [`critique-da.md`](docs/workflows/critique-da.md).

### C27. Faire la miniature
Étape 12, première partie.
- **Qui** : Claude (skill `studio-faceless:thumbnail-strategist`) ; toi tu choisis et tu lances le test.
- **À faire** :

> Étape 12, la miniature : avec le skill `studio-faceless:thumbnail-strategist`, écris la promesse en une phrase (la même que le titre) avec le minutage de l'accroche qui la tient, au moins cinq concepts véridiques, puis choisis trois variantes très différentes. Fabrique-les en HTML/CSS dans `episodes/episode-001/miniatures-v1/` (qui ne doit pas exister), mesure-les et fais la fiche de contrôle de chacune.

  Particularités d'une chaîne neuve :
  - il n'y a pas de « dernière miniature validée » à copier : pour la première, Claude part des extraits de CSS de `fabrication.md` ;
  - la police **Montserrat** (SIL OFL) se télécharge une fois depuis Google Fonts, **avec ton accord**, et se range dans `marque/` avec sa licence ; chaque miniature en copie les deux fichiers dans son `media/` ;
  - le logo de ta chaîne est pris dans `marque/` (C4) ;
  - sujet = une personnalité publique, photo réelle sous licence libre ; aucune image générée par IA ; aucune émotion ni parole prêtée à une personne réelle.

  Commandes de Claude (un exemple de rendu, puis les mesures) :
```bash
python -B "<plugin>/skills/thumbnail-strategist/scripts/miniature.py" rendu episodes/episode-001/miniatures-v1/miniature-1-<mots>.html episodes/episode-001/miniatures-v1/<NomChaine>-E001-miniature-v1-1-<mots>.png
```
```bash
python -B "<plugin>/skills/thumbnail-strategist/scripts/miniature.py" mesure episodes/episode-001/miniatures-v1/*.png
```
```bash
python -I -B "<plugin>/outils/controle/controle.py" chrome
```
  Le script ne télécharge rien : il emploie le Chrome déjà téléchargé par HyperFrames. Il refuse d'écraser.
- **Fichiers créés** : `episodes/episode-001/miniatures-v1/` (sources HTML, PNG 1280 × 720, `media/`, `PROVENANCE.md`, planche de contrôle, fiche de contrôle par variante) ; `episodes/episode-001/JOURNAL_MINIATURES.md` avec l'hypothèse écrite **avant** le test.
- **Tu valides** : tu choisis la variante qui sort et celles du test : `VALIDÉ, <prénom>, JJ/MM/AAAA`. Le regard humain reste « non fait » dans la fiche tant que tu n'as pas répondu. Tu vérifies dans YouTube Studio qu'aucun remplacement automatique de miniature n'est activé. Tu mets en ligne et tu lances Test & Compare (jusqu'à 3 miniatures) ; **tu ne modifies rien pendant le test**.
- **Vérifier** : neuf contrôles par variante (format, aperçus 320 × 180 et 168 × 94, coin inférieur droit, contraste, fonds clair et sombre, économie, flèche, promesse, exactitude et droits) ; poids sous 2 Mo ; `chrome` à 0.
- **Détail** : [`miniature.md`](docs/workflows/miniature.md).

> **Pas encore éprouvé.** Le préchargement du skill `thumbnail-strategist` par l'agent `art-director` est dans la liste « non testé » de `POINTS_OUVERTS.md`. Claude, lui, charge le skill par l'outil Skill.

### C28. Préparer le dossier YouTube
Étape 12, deuxième partie.
- **Qui** : Claude (skill `studio-faceless:youtube-seo`) ; toi tu choisis le titre et tu valides.
- **À faire** :

> Étape 12, le dossier de publication : avec le skill `studio-faceless:youtube-seo`, écris `episodes/episode-001/PUBLICATION_v1.md` : la promesse, trois titres vraiment différents (A « Why… » sur un fait observable, B proche de la requête, C cas concret ; 100 caractères au plus), les chapitres, les crédits, la description, les tags, la playlist, le commentaire épinglé et sa réponse, les réglages à la mise en ligne. Fais le SRT, lance le contrôle, et fais la passe d'actualité sur les phrases [MAJ].

  Les chapitres, le SRT et le contrôle (le journal est celui du **film voix**, pas du master mixé) :
```bash
python -I -B "<plugin>/outils/controle/publication.py" chapitres episodes/episode-001/outputs/<nom_voix>.log.txt --titre seq1="Titre un" --titre seq2="Titre deux"
```
```bash
python -I -B "<plugin>/outils/montage/srt.py" --script episodes/episode-001/SCRIPT_v1.md --mots "kit/voix/{seq}-montage-mots-recales.json" --journal episodes/episode-001/outputs/<nom_voix>.log.txt --sortie episodes/episode-001/PUBLICATION_v1.en.srt
```
```bash
python -I -B "<plugin>/outils/controle/publication.py" verifier episodes/episode-001/PUBLICATION_v1.md --journal episodes/episode-001/outputs/<nom_voix>.log.txt --srt episodes/episode-001/PUBLICATION_v1.en.srt
```
  `chapitres` demande un `--titre seqN="…"` par séquence. Le premier chapitre est forcé à `0:00` ; chaque chapitre dure 10 s au moins. Le suffixe du SRT suit la langue de la chaîne. Règles du dossier :
  - crédits CC BY dans la description par défaut, sauf écart de ta chaîne dans `ECARTS.md` ;
  - la **déclaration des voix et sons générés reste toujours** dans la description (bloc AUDIO, avec l'outil nommé ; ambiances et foules « illustrative, not recordings of the events shown ») ;
  - la promesse du titre se tient avant 30 s ;
  - aucune liste de mots-clés dans la description, aucun chevron.
  Claude vérifie par sondage trois phrases du SRT contre le film.
- **Fichiers créés** : `episodes/episode-001/PUBLICATION_v1.md` (statut `PROPOSÉ`) ; `PUBLICATION_v1.en.srt` ; la fiche de conformité.
- **Tu valides** : tu **choisis le titre** et tu valides les éléments (`VALIDÉ`, date) ou tu demandes une reprise (`PUBLICATION_v2.md`, sans écraser).
- **Vérifier** : `publication.py verifier` répond 0 écart (code 0). Il mesure des limites : il ne relit ni les crédits, ni la déclaration d'IA, ni la promesse. Fais ce travail toi-même avec Claude.
- **Détail** : [`dossier-youtube.md`](docs/workflows/dossier-youtube.md).

### C29. Mettre en ligne
Étape 12, fin. **Claude ne publie jamais.**
- **Qui** : **toi.**
- **À faire** : dans YouTube Studio :
  - mets la vidéo en ligne avec le titre, la description, les chapitres, le SRT et la miniature validés ;
  - règle les cases que le dossier te rappelle, aucune action de Claude : « contenu modifié ou synthétique » (relis la formulation de Studio au moment de cocher ; la décision est la tienne, surtout si des voix, des foules ou des sons générés accompagnent des photos réelles), la langue, l'audience, la catégorie, la miniature ; le forfait ElevenLabs payant ;
  - publie le **commentaire épinglé, puis sa réponse 1, dans cet ordre** ; crée et classe la playlist ;
  - lance Test & Compare si tu l'as décidé.
  Dis ensuite à Claude que l'épisode est en ligne, avec la date et le lien.
- **Fichiers créés** : rien dans la chaîne. Claude note `PUBLIE` (date et lien) dans le `BRIEF.md` et le `CLAUDE.md` de l'épisode.
- **Tu valides** : toute la mise en ligne.
- **Vérifier** : la miniature en ligne est la validée ; les chapitres s'affichent ; `PUBLIE` est écrit avec la date et le lien.
- **Détail** : [`dossier-youtube.md`](docs/workflows/dossier-youtube.md), étapes 11 à 14.

### C30. Faire les bilans J+2, J+7 et J+28
Étape 13, première partie.
- **Qui** : toi (tu relèves dans Studio), Claude (il lit et écrit). Il ne se connecte jamais à ta chaîne.
- **À faire** : tu exportes les données de YouTube Studio (« Exporter la vue », mode avancé, ou captures) et tu les donnes à Claude.

| Quand | À relever |
|---|---|
| **J+2** | impressions et taux de clic par source de trafic ; vues engagées ; durée moyenne et pourcentage regardé ; part encore présente à 30 s ; miniature toujours la tienne ; état de Test & Compare |
| **J+7** | les mêmes ; les termes de recherche YouTube comparés à la requête principale ; les premiers commentaires ; la **perte au moment de l'appel à s'abonner** comparée à la pente des secondes voisines |
| **J+28** | les mêmes relevés ; trois leçons au plus pour l'épisode suivant (le skill `video-postmortem` annoncé n'existe pas encore) |

> Fais le bilan J+2 de l'épisode 1 avec le skill `studio-faceless:youtube-seo` : voici mes relevés Studio. Ajoute une section datée à `episodes/episode-001/BILANS_PUBLICATION.md`, sans réécrire les précédentes ; chaque phrase est marquée « mesuré », « calculé » ou « hypothèse ».

  Règles de lecture : ne touche pas un titre qui marche (un changement se propose à partir de J+7, sur un écart net, avec ton accord) ; sous quelques centaines de vues, le taux de clic et la courbe sont surtout du bruit : on note, on ne conclut pas ; compare en vues engagées.
- **Fichiers créés** : `episodes/episode-001/BILANS_PUBLICATION.md`.
- **Tu valides** : toute leçon avant qu'elle devienne règle de ta chaîne (versée dans `direction/`).
- **Vérifier** : chaque section est datée ; chaque phrase porte sa qualité.
- **À savoir** : les fichiers donnent deux seuils pour lire le taux de clic : environ 1 000 impressions (`etapes.md` § 13) et « quelques centaines de vues » (`apres-publication.md`). Ils ne sont pas harmonisés : à vérifier avec toi (`docs/POINTS_OUVERTS.md`).
- **Détail** : [`dossier-youtube.md`](docs/workflows/dossier-youtube.md), « Bilans » ; [`episode.md`](docs/workflows/episode.md#13-après-la-sortie-et-archivage).

### C31. Verser les sons approuvés à la bibliothèque
Étape 13, deuxième partie. À faire **avant l'archivage**.
- **Qui** : Claude (les agents ne peuvent pas écrire dans un dossier existant de `marque/`).
- **À faire** :

> Verse dans `marque/son/` les sons générés pour l'épisode 1 que j'ai approuvés : copie chaque fichier avec le préfixe `E001-`, ajoute une ligne au tableau « Musiques » ou « Effets et ambiances » de `marque/son/README.md` (fichier, durée, épisode, rôle), écris `E001-PROVENANCE.md` (prompts, crédits, provenance) et `SHA1SUMS.txt`. Ne modifie aucun fichier de la bibliothèque.

  Les `.mp3` et `.wav` de `marque/` sont suivis par Git LFS. Si le mix n'a puisé que dans la bibliothèque, il n'y a rien à verser (ce n'est pas le cas de ta première vidéo).
- **Fichiers créés** : `marque/son/E001-*` ; `marque/son/E001-PROVENANCE.md` ; `marque/son/SHA1SUMS.txt` ; le `README.md` de la bibliothèque mis à jour.
- **Tu valides** : la liste des sons versés.
- **Vérifier** : chaque ligne du `README.md` correspond à un fichier ; les empreintes sont dans `SHA1SUMS.txt`. Le deuxième épisode puisera d'abord ici.
- **Détail** : [`sons.md`](docs/workflows/sons.md), partie D.

### C32. Sauvegarder la chaîne
- **Qui** : toi (tu choisis la destination), Claude (il lance).
- **À faire** : le dépôt Git garde le texte et les binaires de `marque/` ; les médias des épisodes, les rendus et les zips n'y sont pas. **La sauvegarde est leur seule copie.** Elle est conseillée avant la première exécution de l'archivage. Choisis un disque externe ou un dossier hors de la chaîne (une destination synchronisée, comme OneDrive, envoie les fichiers en ligne : à toi de décider). Simulation d'abord :
```bash
powershell -File "<plugin>/outils/sauvegarde-chaine.ps1" -Destination E:\Sauvegardes -Simulation
```
```bash
powershell -File "<plugin>/outils/sauvegarde-chaine.ps1" -Destination E:\Sauvegardes
```
  Adapte `E:\Sauvegardes`. Le script copie, vérifie chaque fichier par empreinte SHA-256, ne supprime ni ne remplace rien, et refuse une destination dans la chaîne.
- **Fichiers créés** : un dossier `<chaîne>_AAAA-MM-JJ_HHMM` à la destination, avec `MANIFEST.sha256.txt`.
- **Tu valides** : la destination.
- **Vérifier** : la sortie finit par « Sauvegarde terminée et vérifiée : N fichiers dans … » et le manifeste existe. Un avertissement « Absent, ignoré : templates » est normal pour une chaîne neuve.
- **Détail** : [`archivage-et-sauvegarde.md`](docs/workflows/archivage-et-sauvegarde.md), partie B.

### C33. Archiver l'épisode
Étape 13, fin. À faire quand tu dis que l'épisode est publié ; sur ta demande, l'archivage peut aussi se faire une fois le master approuvé, avant la mise en ligne.
- **Qui** : Claude montre l'aperçu, **toi tu donnes l'accord**, Claude exécute, **toi tu vides la corbeille**.
- **À faire** : d'abord l'aperçu. Il n'écrit et ne déplace rien. L'outil ne reconnaît pas seul les médias, les voix, `_etude`, `_rendu-N`, `planche-1` ni `controle-planche` : Claude ajoute **un `--essai` par chemin à mettre à la corbeille**.
```bash
python -I -B "<plugin>/outils/archiver_episode.py" episodes/episode-001 --master episodes/episode-001/outputs/<master>.mp4 --essai episodes/episode-001/inputs/media --essai episodes/episode-001/kit/media --essai episodes/episode-001/inputs/voix --essai episodes/episode-001/kit/voix
```
  Ce n'est qu'un exemple, à compléter avec les chemins réels de ton épisode (`etapes.md` § 13 liste ce qui va à la corbeille : médias, voix, séquences ratées et essais, captures de contrôle). Claude te montre le plan ; tu lis : rien d'utile dans les essais, rien d'inutile dans le zip. `--garder CHEMIN` corrige un cas classé à tort. **Sans ton accord, on s'arrête à l'aperçu.** Avec ton accord, la même commande avec `--executer` :
```bash
python -I -B "<plugin>/outils/archiver_episode.py" episodes/episode-001 --master episodes/episode-001/outputs/<master>.mp4 --essai episodes/episode-001/inputs/media --essai episodes/episode-001/kit/media --essai episodes/episode-001/inputs/voix --essai episodes/episode-001/kit/voix --executer
```
  Le zip est écrit en `.partiel`, relu (CRC de chaque fichier), renommé ; si le zip n'est pas conforme, rien n'est déplacé. Claude ajoute la commande utilisée à `ARCHIVE.md`.
- **Fichiers créés** : `episodes/episode-001/episode-001_archive_<date>.zip` (projets des séquences sans médias ni rendus, master et film voix, `montage/`, `research/` et `PROVENANCE.md`, kit écrit, miniatures) ; `episodes/episode-001/ARCHIVE.md` ; `_A_SUPPRIMER/episode-001/` (`essais_<date>/`, `originaux_<date>/`, `LISEZMOI_<date>.md`). Les fichiers de la racine de l'épisode (`BRIEF`, `CLAUDE`, `PUBLICATION`, SRT, `JOURNAL_MINIATURES`, script, narration…) restent en place, hors du zip, pour le statut `PUBLIE` et les bilans.
- **Tu valides** : l'accord à `--executer`. **Tu vérifies puis tu supprimes toi-même** `_A_SUPPRIMER/episode-001/` : Claude ne supprime rien. D'ici là, tout se restaure en remettant les dossiers à leur place.
- **Vérifier** : « Fait : essais et originaux dans … » ; le contenu de `_A_SUPPRIMER/`; `ARCHIVE.md` porte la commande. Il faut au moins 1,1 fois la taille du zip, plus 1 Go, de place libre.
- **À savoir** : l'archivage reconnaît le dossier `montage/` du parcours v3 depuis le 29/10/2026 ; il a été testé en aperçu sur un épisode d'AA.
- **Détail** : [`archivage-et-sauvegarde.md`](docs/workflows/archivage-et-sauvegarde.md), partie A.

### C34. Commiter et envoyer
- **Qui** : Claude fait les commits locaux ; **toi tu autorises chaque envoi.**
- **À faire** : à chaque lot de travail à garder (une étape d'épisode, une règle versée dans `direction/`, un ajout à `marque/`). Commits courts et atomiques, en français, préfixés par la zone.
```bash
git status
```
```bash
git add <fichiers d'un même thème>
```
```bash
git commit -m "épisode 1 : <résumé court>"
```
  Pour un envoi, Claude prépare d'abord ce qui partirait, tu le lis, et tu donnes ton accord pour cet envoi seulement :
```bash
python -I -B "<plugin>/outils/verifier_depot.py" --tout
```
```bash
git push
```
  Le crochet `pre-commit` refuse : un fichier de plus de 10 Mo hors Git LFS, un média sous `episodes/`, un secret probable, un chemin propre à une machine. Un refus se corrige ; il ne se contourne pas par `--no-verify`. Ne pousse jamais par `force`.
- **Fichiers créés** : des commits locaux.
- **Tu valides** : chaque `git push`. Les médias des épisodes, les rendus et les zips restent hors du dépôt (`.gitignore`).
- **Vérifier** : `git status` est propre ; `git log --oneline` montre les commits attendus.
- **À savoir** : l'étiquette d'un épisode publié (par exemple `e001-publie`) n'est qu'une recommandation d'AA, écrite nulle part dans le plugin (à décider).
- **Détail** : [`depot-git.md`](docs/workflows/depot-git.md).

**Ta première vidéo est faite quand** : le master est `APPROUVE_PAR_<ton prénom>`, la vidéo est `PUBLIE` avec sa date et son lien, les bilans J+2, J+7 et J+28 sont écrits, les sons approuvés sont dans `marque/son/`, l'épisode est archivé et `_A_SUPPRIMER/episode-001/` est vidé par toi.

---

## Si quelque chose bloque

### Installation et plugin
| Symptôme | Cause probable | Reprise |
|---|---|---|
| Le plugin n'est pas proposé à l'ouverture, ou Claude Code ignore le catalogue | **confiance du dossier non acceptée**, ou `.claude/` non copié (dossier caché) | recopie `starter/.claude/settings.json`, rouvre le dossier, accepte la confiance |
| Aucune règle commune en début de session ; ou « verifier_depot.py introuvable » | **plugin activé mais non installé** : `enabledPlugins` de `settings.json` l'active, mais `claude plugin install … --scope project` n'a pas été lancé, donc le cache est vide. Autres causes : dossier non approuvé, Python absent du `PATH` | lance la commande de B4 dans un terminal ; vérifie `ls ~/.claude/plugins/cache/studio-faceless/studio-faceless/` ; `/reload-plugins` ; `python -I <plugin>/hooks/regles_studio.py` à la main |
| `claude plugin install` : accès refusé ou dépôt introuvable | identifiants Git absents, ou compte sans accès au dépôt privé | refais A3 (`gh auth login`, `gh auth setup-git`) ; vérifie l'accès au dépôt |
| `claude plugin install` : « Plugin "studio-faceless" not found in marketplace » | le CLI ne lit pas `extraKnownMarketplaces` de `.claude/settings.json` dans un dossier qui ne lui a pas encore été confié (Claude Code 2.1.169) | lance `claude plugin marketplace add hichamsbihi/studio-faceless --scope project`, puis relance l'installation (B4) |
| `/plugin` introuvable dans l'application de bureau | la commande interactive peut ne pas être disponible dans l'onglet Code (à vérifier) | utilise un terminal Git Bash pour les commandes `claude plugin …` |
| `claude plugin update` n'apporte rien | le champ `version` de `plugin.json` n'a pas augmenté | la version s'augmente dans le dépôt du plugin ([`faire-evoluer-le-plugin.md`](docs/workflows/faire-evoluer-le-plugin.md)) |
| Plusieurs versions dans le cache | anciennes versions conservées (à vérifier) | le crochet `pre-commit` prend la plus haute ; Claude ne supprime rien, tu nettoies |
| Les agents ne trouvent pas `hyperframes-core` | skills figés non copiés | refais A5 |
| Un skill HyperFrames demande `upgrade`, `skills update`, `usage` ou `figma` | skills plus récents que le CLI 0.8.149 | ignore la consigne ; en cas de doute `hyperframes <commande> --help` ; `play` se remplace par `preview` |

### Machine et outils
| Symptôme | Cause probable | Reprise |
|---|---|---|
| `hyperframes check` : Node trop ancien ; `render.sh` code 2 | PowerShell, Node 20 par défaut ; ou HyperFrames absent ou différent de 0.8.149 | passe par Git Bash avec `nvm use 22.0.0` ; `npm ci` ; aucune mise à jour sans ta décision |
| `controle.py` : `ModuleNotFoundError: numpy` | dépendances Python manquantes | `pip install -r requirements.txt` |
| `transcrire.py` : modèle introuvable | le modèle est gardé hors du projet | retrouve-le ou retélécharge-le avec ton accord (A7) |
| Un Chrome reste ouvert (`controle.py chrome` ne répond pas 0) | `check`, `snapshot`, `render` ou `preview` interrompu | si un rendu d'une autre session tourne, **ne touche à rien** ; sinon prévenir toi : le plugin n'écrit pas de procédure de fermeture (à vérifier). Un rendu arrêté par `TaskStop` laisse son `node` : `taskkill //T //F //PID <pid>` |
| Wikimedia répond 429 | téléchargement automatique | tu télécharges à la main depuis la liste |
| Un script Python plante sur des accents | console en cp1252 | `sys.stdout.reconfigure(encoding="utf-8")` dans le script en cause |

### Garde-fou
| Message ou symptôme | Cause | Reprise |
|---|---|---|
| refus d'un rendu `hyperframes … render` | pas de `--workers 1` ou `2` | utilise `render.sh` (il impose `--workers 2`) |
| demande de confirmation pour `preview` | aperçu HyperFrames, dont le Chrome reste ouvert jusqu'à l'arrêt | ne l'accepte que si tu l'as demandé ; arrête-le aussitôt ; `controle.py chrome` |
| « installation ou mise à jour npm » | `npm install`, `npm i`, `npm update`… | décision à toi d'abord ; `npm ci` n'est pas vu par le garde |
| « suppression récursive : passer par la corbeille » | `rm -r`, `Remove-Item -Recurse`, `shutil.rmtree`… | déplacer vers `_A_SUPPRIMER/` ; tu supprimes |
| « le plugin installé ne se modifie pas depuis une chaîne » | `Write` ou `Edit` sur le cache du plugin | modifie le dépôt du plugin, change sa version, mets la chaîne à jour |
| producteur : « direction/, templates/, .claude/ et les CLAUDE.md se lisent avec Read ou Grep » | une commande Bash du producteur cite l'un de ces chemins | lis avec Read ou Grep ; le brief donne les extraits |
| mainteneur : « aucune écriture par Bash » | redirection, `cp`, `mv`, `mkdir`, script qui écrit | passer par Write ou Edit |
| directeur artistique : « seules ffmpeg, ffprobe et mkdir sont permises » | autre commande, y compris `cd` | une commande par appel, chemins complets |
| Le garde-fou ne réagit plus | le script plante (Python absent) : il sort alors sans rien dire | `python -I <plugin>/hooks/garde_commandes.py` avec un JSON d'essai (à vérifier dans la documentation de Claude Code) |

### Git et Git LFS
| Symptôme | Cause probable | Reprise |
|---|---|---|
| Les fichiers de `marque/` sont de petits fichiers texte | clone fait sans `git lfs install` : ce sont des **pointeurs LFS** | `git lfs install`, puis `git lfs pull` |
| Un crochet sort en erreur (code 2) ; « git-lfs was not found » | Git LFS absent du `PATH` | installe Git LFS, relance `git lfs install` |
| `git commit` refusé : « verifier_depot.py introuvable » | plugin non installé, ou cache différent | refais B4 ; ou pose `STUDIO_FACELESS_OUTILS` sur le dossier `outils/` de ton clone |
| `git commit` refusé : « Mo hors Git LFS (limite 10 Mo) » | gros fichier hors règle LFS | sors-le du dépôt (sauvegarde externe), ou propose une règle LFS (ta décision) |
| `git commit` refusé : « média d'épisode » | `git add -f` sur un média, ou un `.pdf`/`.zip` sous `episodes/` | `git restore --staged <fichier>` ; le média reste dans la sauvegarde |
| « secret probable » ; « chemin propre à une machine » | clé ou jeton dans un fichier texte ; `C:/Users/<nom>` dans un fichier de code | retire la valeur (si elle est déjà poussée, prévenir : elle est à révoquer) ; chemin relatif ou variable |
| Le crochet ne se lance pas | `core.hooksPath` non réglé | `git config core.hooksPath .githooks` |

### Voix, production et publication
| Symptôme | Cause probable | Reprise |
|---|---|---|
| La prise ne dit pas le texte validé | écart réel | Claude te le signale en tête du compte rendu ; tu décides : nouvelle prise ou acceptation |
| « Sortie existante, aucun écrasement » | tous les outils refusent d'écraser | choisis un nouveau nom ou dossier ; ne supprime rien |
| Voix régénérée après le gel | prise nouvelle après C15 | toutes les séquences sont à recaler : ne rien régénérer sans toi |
| `render.sh` : « Export existant, aucun écrasement » | un MP4 du même nom existe | range l'ancien MP4 et sa planche dans `_rendu-N/`, puis relance |
| Rendu arrêté sans message (code 1) | cause non identifiée | relance **une fois** à l'identique avec un nouveau journal |
| Rendu très long | plusieurs rendus en parallèle | un seul à la fois, par `rendre_si_libre.sh` |
| Bandeau de texte parasite, image décalée de 54 px | `<!--` perdu dans l'en-tête HTML | contrôle l'en-tête de chaque `index.html` |
| Photo répétée d'une séquence à l'autre | répartition non respectée | `controle.py doublons` avant le collage |
| `assembler.py` : « Format inattendu » | un MP4 n'est pas en 1920 × 1080 à 30 i/s | reprends le rendu ou la pièce de marque |
| `mix_film.py` s'arrête sur un `type` d'effet | le type n'est pas une clé de `niveaux_par_type` (`montee` ≠ `montée`) | écris le type à l'identique |
| `srt.py` : « Séquences du script absentes du journal » | journal du master mixé donné au lieu du film voix | donne `<nom_voix>.log.txt` |
| `publication.py verifier` : « aucun titre trouvé » | bloc sous un titre sans le bon mot-clé | garde « Titres », « Description », « Tags », « Commentaire épinglé », « Réponse … », « Playlist » dans les titres |
| Claude annonce avoir « écouté » ou « regardé » | interdit | statut `ECOUTE_A_FAIRE` ; seules des mesures sont possibles |
| Une proposition est présentée comme validée | une absence d'objection a été prise pour un accord | remets `PROPOSÉ` ; seul toi valides |
| Plus de contexte, coûts qui explosent | lectures entières, agents au cache froid | état écrit (`STATE.md`) puis `/clear` ; `/compact` seulement au milieu d'une longue porte ; lectures par plages, un agent court par correction |

## Et ensuite

### Mettre à jour le plugin
La mise à jour automatique est **désactivée** pour un dépôt privé : rien ne change sans ton action.
1. Lis le [`CHANGELOG.md`](CHANGELOG.md) du dépôt du plugin : une section par version.
2. Dans chaque chaîne, dans un terminal Git Bash :
```bash
claude plugin update studio-faceless@studio-faceless
```
3. Dans la session déjà ouverte, tape `/reload-plugins`. Si cela réinjecte les règles communes est à vérifier : demande à Claude de les lister, ou refais le contrôle de B7.

Une mise à jour **ne change pas** les fichiers déjà copiés dans ta chaîne (`.claude/settings.json`, `.gitignore`, `.gitattributes`, `.githooks/`, `package.json`, `package-lock.json`, `requirements.txt`, `CLAUDE.md`, `direction/`, `marque/`) ni la version de HyperFrames : si le squelette change, le report se fait à la main (aucun mécanisme n'est décrit : à vérifier). Ne renomme jamais le plugin. Pour modifier le plugin lui-même : [`faire-evoluer-le-plugin.md`](docs/workflows/faire-evoluer-le-plugin.md).

### Le deuxième épisode
- Reprends à C9 : `studio-faceless:episode`. La partie A, la partie B et la préparation de la marque (C1 à C8) ne se refont pas.
- Ta bibliothèque `marque/son/` n'est plus vide : l'épisode **puise d'abord** dedans, et ne génère qu'à ta demande.
- Tu as maintenant une « dernière miniature validée » pour les suivantes, un épisode précédent pour le brief des producteurs, des bilans et un registre.
- Les portes des étapes 8, 9, 11 et 13 n'ont pas encore de questions écrites ; la décision du 29/10/2026 est de les écrire au prochain épisode (`docs/POINTS_OUVERTS.md`, D4).
- Les leçons de la première vidéo : une leçon propre à ta chaîne va dans `direction/` avec ton accord. Ce qui vaut pour toutes les chaînes se propose pour le plugin.

### Les shorts
Les shorts verticaux (1080 × 1920) tirés d'un film approuvé ont leur propre parcours : [`shorts.md`](docs/workflows/shorts.md). Le skill `studio-faceless:shorts` est `PROPOSÉ` : il reste à valider sur un pilote. Le plugin ne livre ni gabarit vertical ni modèle de `SHORTS_JOURNAL.md` : ils sont à créer au pilote (`docs/POINTS_OUVERTS.md`, D5). Les shorts ne ralentissent pas la voix.

### Autres parcours
- Étudier une vidéo publique par Gemini : [`analyse-video.md`](docs/workflows/analyse-video.md).
- Demander une critique indépendante d'un rendu, ou un storyboard : [`critique-da.md`](docs/workflows/critique-da.md).
- Comprendre les règles injectées et le garde-fou : [`session-et-garde-fou.md`](docs/workflows/session-et-garde-fou.md).

## Pour aller plus loin
| Sujet | Fichier |
|---|---|
| Vue d'ensemble | [`README.md`](README.md), [`docs/README.md`](docs/README.md) |
| Installation et chaîne | [`INSTALLATION.md`](INSTALLATION.md), [`NOUVELLE_CHAINE.md`](NOUVELLE_CHAINE.md), [`installation-et-mise-a-jour.md`](docs/workflows/installation-et-mise-a-jour.md), [`nouvelle-chaine.md`](docs/workflows/nouvelle-chaine.md) |
| Architecture, points ouverts | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/POINTS_OUVERTS.md`](docs/POINTS_OUVERTS.md) |
| Règles communes | [`REGLES_STUDIO.md`](plugins/studio-faceless/REGLES_STUDIO.md), [`referentiels/`](plugins/studio-faceless/referentiels/) |
| Un épisode, étape par étape | [`episode.md`](docs/workflows/episode.md), [`skills/episode/`](plugins/studio-faceless/skills/episode/SKILL.md) |
| Recherche, voix, sons | [`recherche.md`](docs/workflows/recherche.md), [`voix-off.md`](docs/workflows/voix-off.md), [`sons.md`](docs/workflows/sons.md) |
| Séquence, rendu, collage, mix | [`sequence.md`](docs/workflows/sequence.md), [`rendu-et-controle.md`](docs/workflows/rendu-et-controle.md), [`collage-et-mix.md`](docs/workflows/collage-et-mix.md) |
| Publication | [`miniature.md`](docs/workflows/miniature.md), [`dossier-youtube.md`](docs/workflows/dossier-youtube.md) |
| Archivage, Git | [`archivage-et-sauvegarde.md`](docs/workflows/archivage-et-sauvegarde.md), [`depot-git.md`](docs/workflows/depot-git.md) |
| Une fiche par fichier du plugin | [`docs/reference/`](docs/reference/) |
