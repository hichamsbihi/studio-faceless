# Documentation du plugin studio-faceless

Cette documentation décrit chaque fichier du plugin et chaque parcours de travail (workflow). Les fichiers du plugin font foi : en cas d'écart, c'est le fichier décrit qui a raison, et la documentation se corrige.

## Par où commencer
| Vous voulez… | Lire |
|---|---|
| Comprendre le plugin en cinq minutes | [`../README.md`](../README.md), puis [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| Tout faire pas à pas, de la machine vide à la première vidéo | [`../DEMARRAGE.md`](../DEMARRAGE.md) |
| Installer une machine ou brancher une chaîne | [`workflows/installation-et-mise-a-jour.md`](workflows/installation-et-mise-a-jour.md) |
| Créer une nouvelle chaîne | [`workflows/nouvelle-chaine.md`](workflows/nouvelle-chaine.md) |
| Fabriquer un épisode de bout en bout | [`workflows/episode.md`](workflows/episode.md) |
| Savoir ce que fait un fichier précis | la **référence** ci-dessous |
| Voir ce qui reste à décider ou à vérifier | [`POINTS_OUVERTS.md`](POINTS_OUVERTS.md) |

## Workflows
Chaque workflow donne son déclencheur, ses acteurs, ses prérequis, ses étapes (fichiers lus et écrits, commandes, portes de validation), un diagramme et les erreurs fréquentes.

| Workflow | Ce qu'il couvre |
|---|---|
| [`episode.md`](workflows/episode.md) | Le parcours complet d'un épisode, du sujet à l'archivage, porte par porte |
| [`recherche.md`](workflows/recherche.md) | Une mission de l'agent `research` : faits, sources, médias candidats, licences |
| [`voix-off.md`](workflows/voix-off.md) | Du script validé aux bandes voix : prises, transcription, ralentissement, repères |
| [`sons.md`](workflows/sons.md) | Bibliothèque de sons, génération ElevenLabs avec accord, repérage sonore |
| [`sequence.md`](workflows/sequence.md) | Mise en scène d'une séquence par `motion-producer`, jusqu'à `render.sh`, et corrections |
| [`critique-da.md`](workflows/critique-da.md) | Critique indépendante et storyboard par `art-director`, à la demande |
| [`rendu-et-controle.md`](workflows/rendu-et-controle.md) | Un rendu à la fois, contrôles techniques, planche, Chrome |
| [`collage-et-mix.md`](workflows/collage-et-mix.md) | Collage du film en voix seule, signature et outro, mix du film, SRT |
| [`miniature.md`](workflows/miniature.md) | Concepts, fabrication HTML/CSS, contrôles, test A/B |
| [`dossier-youtube.md`](workflows/dossier-youtube.md) | Dossier de publication, contrôle, soumission, bilans J+2/J+7/J+28 |
| [`shorts.md`](workflows/shorts.md) | Du film publié au short vertical |
| [`analyse-video.md`](workflows/analyse-video.md) | Faire « regarder » une vidéo YouTube publique par Gemini |
| [`archivage-et-sauvegarde.md`](workflows/archivage-et-sauvegarde.md) | Archivage d'un épisode publié, sauvegarde datée de la chaîne |
| [`session-et-garde-fou.md`](workflows/session-et-garde-fou.md) | Début de session, règles injectées, garde-fou à chaque commande, tokens |
| [`depot-git.md`](workflows/depot-git.md) | Dépôt d'une chaîne : ce qui entre, contrôle avant commit, envoi |
| [`nouvelle-chaine.md`](workflows/nouvelle-chaine.md) | Créer une chaîne à partir du squelette |
| [`installation-et-mise-a-jour.md`](workflows/installation-et-mise-a-jour.md) | Installer une machine, brancher une chaîne, mettre à jour le plugin |
| [`faire-evoluer-le-plugin.md`](workflows/faire-evoluer-le-plugin.md) | Modifier le plugin, version, envoi, mise à jour des chaînes |

## Référence (une fiche par fichier)
| Document | Fichiers décrits |
|---|---|
| [`skill-episode.md`](reference/skill-episode.md) | `skills/episode/` : le skill et ses neuf références |
| [`agents.md`](reference/agents.md) | `agents/` : les cinq agents, avec leurs outils, skills et limites |
| [`templates.md`](reference/templates.md) | `templates/` : contrat de mission, modèles d'épisode, gabarit de séquence v3 |
| [`son.md`](reference/son.md) | `skills/direction-sonore/`, `referentiels/DIRECTION_AUDIO.md`, `outils/montage/`, `transcrire.py`, `ralentir.py` |
| [`publication.md`](reference/publication.md) | `skills/thumbnail-strategist/`, `youtube-seo/`, `shorts/`, `regarder/`, `outils/shorts/`, `publication.py`, `outils/gemini/` |
| [`outils-et-garde.md`](reference/outils-et-garde.md) | `outils/controle/controle.py`, `cartes/`, `rendu/`, archivage, contrôle du dépôt, tokens, sauvegarde, `hooks/`, `REGLES_STUDIO.md` |
| [`referentiels.md`](reference/referentiels.md) | `referentiels/` : méthode de récit, qualité de réalisation, catalogue d'animations |
| [`starter-et-depot.md`](reference/starter-et-depot.md) | `starter/` (squelette de chaîne) et les fichiers de la racine du dépôt |
| [`skills-annexes.md`](reference/skills-annexes.md) | `grilling`, `grill-me`, `humanizer`, `javascript-animation`, `soundtrack`, `find-skills`, `elevenlabs-sound-effects`, `elevenlabs-music`, `frontend-design` |
| [`vendor.md`](reference/vendor.md) | `vendor/claude-skills/` : les skills HyperFrames 0.8.149 figés, skill par skill |

## Vocabulaire
| Terme | Sens |
|---|---|
| **Propriétaire** | La personne qui décide et valide pour une chaîne, nommée dans son `CLAUDE.md` |
| **Studio Director** | Claude principal : il reçoit les demandes, délègue, coordonne, contrôle et soumet |
| **Chaîne** (espace de chaîne) | Le dossier et le dépôt d'une chaîne : `CLAUDE.md`, `direction/`, `marque/`, `episodes/` |
| **Règles par défaut** | `REGLES_STUDIO.md` et `referentiels/` du plugin |
| **Écart** | Une règle de la chaîne qui remplace une règle par défaut, écrite dans `direction/ECARTS.md` |
| **Porte** | Un moment où le propriétaire répond à des questions numérotées avant l'étape suivante |
| **Socle** (kit) | Ce qui est prêt avant le premier producteur : voix, médias, cartes, sons, raccords, briefs |
| **Séquence témoin** | La première séquence, rendue et validée avant les lots de trois |
| **Contrat de mission** | Le message de délégation à un agent : objectif, fichiers permis, livrables, interdits |
| **`${CLAUDE_PLUGIN_ROOT}`** | Le dossier du plugin installé ; remplacé automatiquement dans les skills, les agents et les hooks, pas dans Bash |
