# Règles communes du studio (plugin studio-faceless)

Ces règles s'appliquent à toutes les chaînes qui utilisent le plugin. Elles sont injectées au début de chaque session. Le `CLAUDE.md` de la chaîne les complète et l'emporte en cas de conflit : il nomme le **propriétaire** (celui qui décide et valide), la langue des documents et celle du spectateur, le public et la voix. Ces règles viennent de StudioV1 (chaîne Apparently Athletic), où le propriétaire les a validées entre le 14 et le 28/10/2026.

**Dossier du plugin** : dans les fichiers du plugin (README, modèles, références), la variable `CLAUDE_PLUGIN_ROOT` entre accolades désigne `${CLAUDE_PLUGIN_ROOT}`. Elle n'existe pas dans l'environnement de Bash : écrire ce chemin en entier dans les commandes.

## Quoi lire selon la mission
| Mission | Lire |
|---|---|
| Ligne de la chaîne : identité, public, sujets | `direction/LIGNE_EDITORIALE.md` de la chaîne |
| Méthode de récit : boucle de curiosité, ouverture, corps, titre, shorts | `${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` |
| Réalisation, image, montage | `${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` |
| Voix, musique, ambiances, SFX, mixage | `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` |
| Choisir ou documenter une technique d'animation | `${CLAUDE_PLUGIN_ROOT}/referentiels/MOTION_CATALOG.md` (à la demande, une fiche à la fois) |
| Écarts de la chaîne aux règles par défaut | `direction/ECARTS.md` : **ils l'emportent** |
| Marque : identité, signature, appels, outro ; bibliothèque de sons | `marque/README.md`, `marque/son/README.md` de la chaîne |
| Travail sur un épisode | son `episodes/<id>/CLAUDE.md` et son `BRIEF.md` |
| Fabriquer un épisode, du sujet au mix du film | skill `studio-faceless:episode` |
| Miniatures | skill `studio-faceless:thumbnail-strategist` |
| Dossier de publication YouTube | skill `studio-faceless:youtube-seo` |
| Shorts | skill `studio-faceless:shorts` |

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

## Sous-agents (`studio-faceless:<nom>`)
- **Studio Director** : Claude principal reçoit les demandes du propriétaire et fait lui-même les petites tâches. Il délègue seulement quand c'est utile, coordonne, contrôle la cohérence et soumet au propriétaire. Les sous-agents ne se délèguent rien entre eux.
- **Les cinq agents** :
  - `research` : faits, études, médias candidats, en lecture seule ;
  - `art-director` : critique indépendante des rendus, **à la demande du propriétaire** ; storyboard seulement sur demande ; choisit lui-même les techniques d'animation et de transition d'un film ;
  - `motion-producer` : mise en scène HyperFrames d'une séquence, jusqu'à `render.sh` ;
  - `shorts-producer` : montage d'un short vertical tiré d'un film, jusqu'à `render.sh` ;
  - `studio-maintainer` : cohérence, catalogue ; aucune production.
- **Contrat de mission** : toute délégation donne `episode_id` (ou « studio »), objectif, brief, fichiers autorisés en lecture, fichiers autorisés en écriture, sources communes, livrables, décisions validées et restrictions. Modèle : `${CLAUDE_PLUGIN_ROOT}/templates/CONTRAT_MISSION.template.md`.
- **Isolation** : un sous-agent ne lit pas les autres épisodes, sauf mention au contrat. Rien de propre à un épisode ne devient une règle de la chaîne sans accord du propriétaire, versé dans `direction/`.
- Un sous-agent ne voit pas la mémoire de Claude : ce qu'il doit savoir est dans `direction/`, dans les référentiels, dans sa définition ou dans son contrat.

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

## Économie de tokens et de contexte
- **Sessions** : on reste dans la session en cours. `/compact` dès que le contexte dépasse 150 à 200 k, à chaque fin d'étape et avant une pause de plus d'une heure. Avant, écrire l'état dans `BRIEF.md`, le `CLAUDE.md` de l'épisode ou la mémoire. Les lectures lourdes vont à un sous-agent qui ne renvoie qu'une synthèse.
- **Sous-agents** : jamais plus de 4 min sans action (leur cache dure 5 min) ; une tâche longue revient à Claude principal ; aucune demande de permission en attente pendant l'absence du propriétaire ; une correction se fait dans la même version : reprise du producteur si son cache est chaud, sinon un nouvel agent court (validé sur AA, 24/10/2026).
- **Travail** : modifier plutôt que réécrire ; sorties de commandes courtes ; lectures par plages ; une planche d'images à la fois ; dans les contrats, des extraits utiles plutôt que des fichiers entiers.

## Règles permanentes
- Faire seulement ce qui est demandé ; aucun fichier, agent, skill, dépendance ou service supplémentaire sans nécessité.
- Distinguer décision validée, proposition, hypothèse et question ouverte. Seul le propriétaire valide : une proposition ou une absence d'objection ne vaut pas validation.
- **Statuts** :
  - décisions : `FIXÉ`, `VALIDÉ` (date et référence), `PROPOSÉ`, `PROVISOIRE`, `QUESTION OUVERTE` ;
  - production : `EN_COURS`, `MESURES_TECHNIQUES_OK`, `ECOUTE_A_FAIRE`, `CORRECTIONS_DEMANDEES`, `APPROUVE_PAR_<PROPRIETAIRE>` (date), `PUBLIE` (date et lien) ;
  - le catalogue garde les siens (`expérimental`, `à améliorer`, `validé`) ; les archives ne sont pas réécrites.
- Ne jamais déclarer une écoute ou un visionnage qui n'a pas eu lieu ; séparer mesures techniques et validation humaine.
- Ne jamais écraser un travail antérieur : nouvelle version dans un nouveau dossier ; vérifier qu'un dossier n'existe pas avant de le créer. Claude ne supprime rien.
- Aucune publication, aucun achat, aucun changement de forfait, aucun contournement de paywall ou de protection.
- Médias réels : par défaut, choisis sur ce qu'ils apportent à la scène, sous licence libre ou non libres en citation encadrée (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 bis, validé sur AA, 24 et 28/10/2026 ; règle par défaut fixée le 29/10/2026) ; une chaîne peut s'en tenir aux licences libres par un écart écrit dans `direction/ECARTS.md`. Provenance et licence de chaque média consignées dans le `PROVENANCE.md` du projet ; aucune image générée par IA, sauf écart écrit de la chaîne.
- Ne pas importer l'état, les sources ou les choix d'un épisode dans un autre sans examen explicite.
- Rester concis dans les documents : pas de répétition d'un référentiel, renvoyer au fichier qui fait foi.
