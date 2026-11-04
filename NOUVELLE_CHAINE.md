# Créer une nouvelle chaîne

Une chaîne est un dossier (et un dépôt Git privé) créé à partir du squelette `plugins/studio-faceless/starter/`. La machine doit d'abord être installée ([`INSTALLATION.md`](INSTALLATION.md), sections 1 à 3).

## 1. Créer l'espace (propriétaire, ou Claude avec son accord)
1. Créer un dossier vide pour la chaîne, par exemple `Desktop\<NomDeLaChaine>`.
2. Y copier tout le contenu de `plugins/studio-faceless/starter/`, fichiers cachés compris (`.claude/`, `.githooks/`, `.gitignore`, `.gitattributes`).
3. Dans ce dossier :
   ```bash
   git init -b main
   ```
   ```bash
   git lfs install
   ```
   ```bash
   git config core.hooksPath .githooks
   ```
4. Dépendances : `npm ci` ne marche qu'avec un `package-lock.json` à jour. Le squelette fournit celui de HyperFrames 0.8.149 ; le propriétaire décide de l'installation. Suivre ensuite [`INSTALLATION.md`](INSTALLATION.md) § 4, points 4 à 7 : `pip install -r requirements.txt`, clé `ELEVENLABS_API_KEY` posée par le propriétaire (pas de connecteur), modèle Whisper.
5. Ouvrir le dossier dans Claude Code, accepter la confiance du dossier, puis, dans un terminal Git Bash ouvert dans ce dossier, déclarer le catalogue du plugin et installer le plugin :
   ```bash
   claude plugin marketplace add hichamsbihi/studio-faceless --scope project
   ```
   ```bash
   claude plugin install studio-faceless@studio-faceless --scope project
   ```
   Sans la première commande, l'installation échoue avec « Plugin "studio-faceless" not found in marketplace » : le CLI ne lit pas le catalogue déclaré dans `.claude/settings.json` (`extraKnownMarketplaces`) d'un dossier qui ne lui a pas encore été confié (Claude Code 2.1.169, constaté le 29/10/2026).

## 2. Remplir l'identité (avec Claude, des questions par blocs)
À donner à Claude dans la nouvelle chaîne :
> Nouvelle chaîne. Avec le skill `studio-faceless:grilling`, pose-moi les questions de départ, un bloc à la fois : domaine (un profil de `plugins/studio-faceless/domaines/`, ou un nouveau domaine à créer selon `domaines/README.md`), nom et promesse, public et langues, propriétaire, voix, territoires, principes, personnalité narrative, ce qui s'écarte des règles par défaut du plugin. Puis remplis `CLAUDE.md`, `direction/LIGNE_EDITORIALE.md` et `direction/ECARTS.md`, tout en `PROPOSÉ`, sans rien valider à ma place.

Ensuite viennent la marque (`marque/README.md` : logo, signature, appel, outro, couleurs, polices) et la bibliothèque de sons (`marque/son/README.md`), puis le premier épisode avec le skill `studio-faceless:episode`.

## 3. Ce qui se décide par chaîne
| Où | Quoi |
|---|---|
| `CLAUDE.md` | propriétaire, langues, public, voix, domaine, règles propres, état |
| `direction/LIGNE_EDITORIALE.md` | identité, promesse, territoires, principes, personnalité narrative, sujets et registre des décisions |
| `direction/ECARTS.md` | ce qui remplace une règle par défaut du plugin (référentiels, méthode de récit) ; chaque écart porte « Remplace : <id> » (priorité : `REGLES_STUDIO.md` § Priorité du plugin) |
| `marque/` | identité visuelle et sonore |

Une règle commune à toutes les chaînes ne s'écrit pas dans une chaîne : elle se propose pour le plugin (nouvelle version, [`README.md`](README.md), « Faire évoluer le plugin »).
