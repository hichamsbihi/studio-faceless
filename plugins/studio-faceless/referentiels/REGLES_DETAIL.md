# Règles communes du studio : détail

Suite des règles communes du studio (`REGLES_STUDIO.md`), à lire selon la mission, avec la même autorité. Les deux sections ci-dessous ont été déplacées mot pour mot depuis `REGLES_STUDIO.md` (0.2.3, 30/10/2026), qui est injecté au début de chaque session et que l'application tronque au-delà de 10 000 caractères. Dans ce fichier comme dans les autres fichiers du plugin, `${CLAUDE_PLUGIN_ROOT}` désigne le dossier du plugin installé, dont le chemin est donné par les règles communes injectées au début de la session ; dans une commande Bash, écrire ce chemin en entier.

## Moteur et outils
- **HyperFrames 0.8.149**, figée dans le `package.json` de la chaîne. Aucune mise à jour (`upgrade`, `skills update`, `npm install` d'une autre version) sans décision du propriétaire.
- **Node 22 ou plus** est obligatoire. Sous Windows, passer par Git Bash (nvm, Node 22).
- **Skills plus récents que le CLI** : `hyperframes usage` et `hyperframes figma` n'existent pas en 0.8.149, donc ignorer les consignes qui les appellent ; `play` se remplace par `preview`. En cas de doute : `hyperframes <commande> --help`.
- **Navigateurs** : `check`, `snapshot`, `render` et `preview` lancent un Chrome sans fenêtre, un par processus de rendu. Rendre avec `--workers 2` au plus ; ne lancer `preview` que sur demande et l'arrêter juste après ; vérifier ensuite qu'aucun Chrome de HyperFrames ne reste ouvert.
- **Installations et envois cachés** (validé sur MM, 14/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ) : `remove-background` installe `onnxruntime-node` et télécharge un modèle de 168 Mo ; `catalog` télécharge et met en cache ; `init` rafraîchit les skills depuis GitHub (seule `HYPERFRAMES_SKIP_SKILLS=1` l'empêche, `--skip-skills` est ignoré) ; `tts`, `transcribe` et `models` téléchargent des modèles. Ces installations passent par Node : un garde sur Bash ne les voit pas, donc aucune sans l'accord du propriétaire, et les projets se créent à la main. `snapshot --describe` envoie les images à Gemini si `GEMINI_API_KEY` existe : toujours `--describe false`. Les scripts de media-use envoient de la télémétrie. Le gel de version tient parce que l'installation est locale : une installation globale ou `npx hyperframes@latest` déclencherait la mise à jour.
- **Poste de travail** (validé sur MM, 28/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ ; constaté sur le poste du propriétaire, commun à ses chaînes) : pas de carte graphique NVIDIA, donc les outils d'IA locaux qui reposent sur CUDA (voix, conversion de voix, gros modèles) ne tournent pas ou très lentement : le signaler avant d'en proposer un. Pas de Pillow : planches par `ffmpeg` (`tile`) ; pour mesurer des pixels, sortie `-f rawvideo -pix_fmt rgb24` lue par Python. Rien ne s'installe sans décision du propriétaire. L'heure d'un statut ou d'un journal se lit avec `date` avant d'être écrite : des statuts portaient des heures estimées, fausses.
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

## Méthode de travail avec le propriétaire
- **Méthode de travail avec le propriétaire** (validé sur MM, 21/10/2026, bloc 8 de l'audit de son pilote ; proposé au plugin 0.3.0, PROPOSÉ) : une décision se présente par blocs, un à la fois (repris, changé, douteux, puis une recommandation) ; « explique-moi » ne modifie rien ; les téléchargements d'un lot tiennent en une liste unique (nom, source, taille) et un seul accord.
