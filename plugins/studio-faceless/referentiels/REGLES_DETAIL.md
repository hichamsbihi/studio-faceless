# Règles communes du studio : détail

Suite des règles communes du studio (`REGLES_STUDIO.md`), à lire selon la mission, avec la même autorité. Les deux sections ci-dessous ont été déplacées mot pour mot depuis `REGLES_STUDIO.md` (0.2.2, 30/10/2026), qui est injecté au début de chaque session et que l'application tronque au-delà de 10 000 caractères. Dans ce fichier comme dans les autres fichiers du plugin, `${CLAUDE_PLUGIN_ROOT}` désigne le dossier du plugin installé, dont le chemin est donné par les règles communes injectées au début de la session ; dans une commande Bash, écrire ce chemin en entier.

## Moteur et outils
- **HyperFrames 0.8.149**, figée dans le `package.json` de la chaîne. Aucune mise à jour (`upgrade`, `skills update`, `npm install` d'une autre version) sans décision du propriétaire.
- **Node 22 ou plus** est obligatoire. Sous Windows, passer par Git Bash (nvm, Node 22).
- **Skills plus récents que le CLI** : `hyperframes usage` et `hyperframes figma` n'existent pas en 0.8.149, donc ignorer les consignes qui les appellent ; `play` se remplace par `preview`. En cas de doute : `hyperframes <commande> --help`.
- **Navigateurs** : `check`, `snapshot`, `render` et `preview` lancent un Chrome sans fenêtre, un par processus de rendu. Rendre avec `--workers 2` au plus ; ne lancer `preview` que sur demande et l'arrêter juste après ; vérifier ensuite qu'aucun Chrome de HyperFrames ne reste ouvert.
- **Outils du plugin** : `${CLAUDE_PLUGIN_ROOT}/outils/`, lancés depuis le dossier de la chaîne (`python -B "<chemin>"`). Contrôles : `outils/controle/` (mode d'emploi dans son `README.md`) :
  - `transcrire.py` : la prise contre le texte ;
  - `ralentir.py` : la narration ;
  - `controle.py` : niveau, planche, vibration, tremblement, son, couleurs, photos répétées, licences, voix / reste, Chrome.
- **Garde-fou** (hook du plugin, `${CLAUDE_PLUGIN_ROOT}/hooks/garde_commandes.py`) :
  - pour tous, il refuse la publication, le cloud, la connexion, la mise à jour de HyperFrames ou des skills, l'installation npm, la suppression récursive ou définitive, le vidage de la corbeille et la modification du plugin installé ;
  - il demande confirmation pour `preview`, et refuse un rendu sans `--workers 1` ou `2` ;
  - par rôle, reconnu au type d'agent :
    - le directeur artistique n'a droit qu'à `ffmpeg`, `ffprobe` et `mkdir`, sans écrasement ni sortie dans une zone protégée ;
    - les producteurs ne touchent ni à `direction/`, `templates/`, `.claude/` et aux `CLAUDE.md` (ils peuvent lancer les outils du plugin), ni à un dossier existant de `marque/`, aux entrées d'un épisode ou à un MP4 existant ;
    - le mainteneur n'écrit qu'avec Write ou Edit, jamais dans `.claude/`, un projet de production, un dossier existant de `marque/`, les entrées d'un épisode ou un MP4.
  - Les permissions (allow, deny, ask) sont dans le `.claude/settings.json` de la chaîne.
- **Rendu** : un à la fois, en tâche suivie, par `bash "${CLAUDE_PLUGIN_ROOT}/outils/rendu/rendre_si_libre.sh" <render.sh> <journal>`, qui attend la fin des rendus des autres sessions.
- **Archivage** : `${CLAUDE_PLUGIN_ROOT}/outils/archiver_episode.py`. Un aperçu d'abord ; `--executer` seulement avec l'accord du propriétaire.
- **Dépôt Git de la chaîne** : `verifier_depot.py` contrôle chaque commit (crochet `.githooks/pre-commit`). Claude fait les commits locaux et **ne pousse qu'avec l'accord du propriétaire, donné à chaque fois** ; il ne se connecte jamais au compte GitHub.
- **Suivi des tokens** à chaque fin d'étape : `python -B "${CLAUDE_PLUGIN_ROOT}/outils/suivi_tokens.py" --depuis AAAA-MM-JJ`.

## Parcours d'un épisode
La fabrication suit le skill `studio-faceless:episode`, du choix du sujet au mix du film : questions au propriétaire à chaque porte (skill `studio-faceless:grilling`), séquence témoin validée avant les lots de trois, corrections dans la même version, mix du film à la fin sur le film collé. Les étapes :
1. **Sujet**, choisi avec le propriétaire, inscrit au registre de `direction/LIGNE_EDITORIALE.md` ; dossier `episodes/<id>/` créé à partir des modèles du plugin.
2. **Recherche** par `research`, rapports dans `research/`.
3. **Validation** de l'angle et du découpage par le propriétaire.
4. **Fiches et scripts** : narration vérifiée phrase par phrase avec sa source, plan de plans, son. Le script part **sans balise de synthèse vocale par défaut**.
5. **Voix off** : le propriétaire génère les prises ; Claude les vérifie (`transcrire.py`), les ralentit (`ralentir.py`) et prépare les repères mot à mot.
6. **Kit de l'épisode**, préparé une seule fois : médias convertis avec leur provenance, bandes voix et repères, sons puisés dans `marque/son/`, gabarit de séquence v3, un brief court par séquence.
7. **Mise en scène** : un `motion-producer` par séquence, avec un contrat de mission ; une séquence témoin d'abord, puis des lots de trois au plus. L'effet diaporama est interdit (`REFERENTIEL_QUALITE_REALISATION.md` § 2).
8. **Rendu et contrôle**, sans agent : un rendu à la fois (`--workers 2`), puis `controle.py` (`tout`, `planche`, `tremblement`, `son`) ; Claude regarde la planche avant de montrer la séquence.
9. **Retours** : corrections dans la même version ; une nouvelle version seulement pour un défaut majeur ; un rendu déjà fait est rangé dans `_rendu-N/`.
10. **Collage** quand toutes les séquences sont validées : signature de la chaîne après l'intro, outro à la fin ; collage en voix seule, puis un seul mix du film (`${CLAUDE_PLUGIN_ROOT}/outils/montage/`).
11. **Archivage** après la publication, avec l'accord du propriétaire : la vidéo finale et ses composants dans un zip vérifié ; les essais dans `_A_SUPPRIMER/<épisode>/`, que le propriétaire vide lui-même.
