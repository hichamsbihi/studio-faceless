# Installer le studio sur une machine

Le studio tourne sous **Windows**, avec **Git Bash** pour les commandes de Claude. Les versions sont celles de la machine de référence au 28/10/2026.

## 1. Prérequis (installés par le propriétaire)
| Outil | Version de référence | Rôle | Installation suggérée (PowerShell) |
|---|---|---|---|
| Git pour Windows, avec Git LFS | Git 2.49, LFS 3.6.1 | dépôts, binaires de la marque, Git Bash | `winget install Git.Git` |
| GitHub CLI | récente | identifiants Git pour le dépôt privé du plugin | `winget install GitHub.cli` |
| nvm pour Windows, puis Node | Node **22.0.0** | HyperFrames (Node 22 ou plus obligatoire) | `winget install CoreyButler.NVMforWindows`, puis `nvm install 22.0.0` et `nvm use 22.0.0` |
| Python | 3.14 (3.12 au moins) | outils, garde-fou, mix | `winget install Python.Python.3.14` |
| FFmpeg | 9.0 | tout le son et l'image | `winget install Gyan.FFmpeg` |
| Claude Code | 2.1.271 ou plus | Claude, plugin, agents (le champ `omitClaudeMd` de `research`, `studio-maintainer` et `strategist` demande cette version) | application de bureau ou `claude` en terminal |

- **Compte GitHub** du propriétaire, avec l'authentification à deux facteurs et l'accès aux dépôts privés.
- **Compte ElevenLabs** et sa clé d'API (voix, musique et effets passent par l'API, pas par le connecteur claude.ai, coupé par défaut) ; **clé d'API YouTube Data** (relevés de chaînes de `strategist`) et **clé d'API Gemini** (`regarder`, `relire`), voir § 4, point 6 ; **compte claude.ai** pour les autres connecteurs de la chaîne (vidIQ en lecture seule, sur demande).
- **Chrome sans fenêtre** : HyperFrames télécharge `chrome-headless-shell` (environ 270 Mo) dans `~/.cache/hyperframes/` au premier contrôle ou rendu, avec l'accord du propriétaire.

## 2. Identifiants Git (une fois par machine)
Claude Code installe le plugin avec les identifiants Git de la machine, sans jamais en demander.
```bash
gh auth login
```
```bash
gh auth setup-git
```

## 3. Skills HyperFrames figés (une fois par machine)
Les agents préchargent les skills HyperFrames 0.8.149. Le plus simple est de cloner ce dépôt une fois, puis de copier chaque dossier de `plugins/studio-faceless/vendor/claude-skills/` dans `~/.claude/skills/`, sans écraser un dossier existant.

## 4. Brancher une chaîne existante
1. Cloner le dépôt de la chaîne, puis récupérer ses binaires :
   ```bash
   git lfs install
   ```
   ```bash
   git clone https://github.com/<compte>/<depot-de-la-chaine>.git
   ```
2. Ouvrir le dossier dans Claude Code et **accepter la confiance du dossier** : sans elle, Claude Code ignore le catalogue déclaré dans `.claude/settings.json`.
3. Dans un terminal Git Bash ouvert dans le dossier de la chaîne, déclarer le catalogue du plugin, puis installer le plugin pour ce projet :
   ```bash
   claude plugin marketplace add hichamsbihi/studio-faceless --scope project
   ```
   ```bash
   claude plugin install studio-faceless@studio-faceless --scope project
   ```
   Sans la première commande, l'installation échoue avec « Plugin "studio-faceless" not found in marketplace » : le CLI ne lit pas le catalogue déclaré dans `.claude/settings.json` (`extraKnownMarketplaces`) d'un dossier qui ne lui a pas encore été confié (Claude Code 2.1.169, constaté le 29/10/2026).
4. Dépendances de la chaîne : `npm ci` (HyperFrames 0.8.149, figé par `package-lock.json`), puis `pip install -r requirements.txt`.
5. Contrôle avant commit : `git config core.hooksPath .githooks`.
6. ElevenLabs : poser la clé d'API dans la variable d'environnement `ELEVENLABS_API_KEY` (le propriétaire la crée sur elevenlabs.io et la pose lui-même ; Claude ne la lit ni ne l'affiche jamais) ; le SDK Python `elevenlabs` s'installe seulement sur décision du propriétaire, à la version figée dans le `requirements.txt` de la chaîne (règle des skills `elevenlabs-*`; le squelette ne le contient pas). Aucune règle `ask` à ajouter : le connecteur est coupé, et chaque génération demande l'accord du propriétaire.
   Les deux autres clés se posent de la même façon, par le propriétaire, dans l'environnement ; Claude ne les lit ni ne les affiche, et aucune n'est écrite dans un fichier :
   - `YOUTUBE_API_KEY` (API YouTube Data v3, clé créée par le propriétaire) : `outils/recherche/youtube_chaine.py` et l'agent `strategist` ; sans elle, l'outil s'arrête ;
   - `GEMINI_API_KEY` : skill `regarder` (`regarder.py`) et `relire.py` ; un contenu inédit ne part chez Google qu'avec la clé du palier payant, décision du propriétaire.
7. Modèle Whisper pour le contrôle des prises : `ggml-base.en.bin`, hors du projet, téléchargé avec l'accord du propriétaire.

## 5. Vérifier
À donner à Claude dans la chaîne, en lisant le bilan avant de continuer :
> Vérifie l'installation : liste les skills et agents `studio-faceless`, vérifie que les règles communes du studio sont arrivées au début de la session, lance `hyperframes check` sur le gabarit de séquence v3 du plugin copié dans un dossier temporaire, un rendu test de 3 secondes avec `--workers 1`, un contrôle `controle.py niveau` sur ce rendu et `controle.py chrome`. Vérifie à la fin qu'aucun Chrome ne reste ouvert.

## 6. Mettre à jour le plugin
La mise à jour automatique est désactivée pour un dépôt privé : rien ne change sans action du propriétaire.
```bash
claude plugin update studio-faceless@studio-faceless
```
Puis `/reload-plugins` dans une session déjà ouverte.
