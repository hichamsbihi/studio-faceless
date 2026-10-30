# Points ouverts

Ce qui reste à décider ou à vérifier dans le plugin, relevé pendant l'écriture de la documentation (28/10/2026). Un point réglé sort de cette liste et entre dans le [`CHANGELOG`](../CHANGELOG.md).

## Décisions et tâches
| # | Point | Fichiers | Recommandation |
|---|---|---|---|
| D4 | **Portes sans banque de questions** : `episode` prévoit une porte aux étapes 8, 9, 11 et 13, mais `grilles.md` n'a pas de questions pour elles | `skills/episode/SKILL.md`, `references/grilles.md` | Décidé (Hicham, 29/10/2026) : à faire au prochain épisode |
| D5 | **Shorts** : le skill (`PROPOSÉ`) suppose un gabarit vertical et un modèle de `SHORTS_JOURNAL.md`, absents du plugin | `skills/shorts/`, `agents/shorts-producer.md` | Décidé (Hicham, 29/10/2026) : à faire au pilote des shorts |

## Vérifications (Claude)
| Point | Fichiers |
|---|---|
| Unité des niveaux de l'exemple `montage.json` (impact −8, souffle −12…) face aux niveaux validés en LU sous la voix (impact 14, souffle 18…) | `outils/montage/README.md` l. 55-59, `referentiels/DIRECTION_AUDIO.md` § 3 |
| `controle.py planche` écrit ses étiquettes avec une police Windows échappée (`C\:/Windows/Fonts/arial.ttf`) ; un piège dit qu'un chemin Windows a fait échouer `drawtext` | `outils/controle/controle.py` l. 95, `skills/episode/references/pieges.md` l. 49 |
| Instants de la planche du producteur : 16 à 20, 16 ou 24 selon le fichier | `agents/motion-producer.md` l. 50, `templates/sequence-gabarit-v3/README.md` l. 64, `skills/episode/references/production.md` l. 65 |
| Seuil des bilans : 1 000 impressions ou « quelques centaines de vues » | `skills/episode/references/etapes.md` l. 68, `skills/youtube-seo/references/apres-publication.md` l. 15 |
| Recalage des repères mot à mot pour un épisode : seul `outils/shorts/recaler.py` le fait | `skills/episode/references/etapes.md` l. 29, `outils/controle/README.md` l. 46 |
| « Journal du master » encore employé là où les chapitres et le SRT demandent le journal du collage en voix seule (`<nom>-voix.log.txt`) ; certains emplois visent bien le master mixé | `skills/youtube-seo/references/description-et-credits.md` l. 20 et 38, `gabarit-et-controle.md` l. 11, `skills/episode/references/etapes.md` l. 48, `rendu-collage.md` l. 23, `referentiels/DIRECTION_AUDIO.md` l. 70, docstrings de `publication.py`, `srt.py`, `assembler.py` |
| Corrections des shorts : « nouvelle version, nouvel agent », alors que les épisodes corrigent dans la même version depuis le 24/10 | `templates/CONTRAT_MISSION.template.md` l. 24, `agents/shorts-producer.md` l. 101 |
| `mix.py` encore cité | `skills/shorts/references/montage-vertical.md` l. 67-68, `referentiels/DIRECTION_AUDIO.md` l. 14 |
| Texte de la licence Apache-2.0 absent de `vendor/` (le paquet `hyperframes` n'en fournit pas) | `vendor/claude-skills/README.md` |
| `javascript-animation` : `playwright-core` demande une installation npm, que le garde-fou refuse ; `outils/capture.sh` n'existe pas | `skills/javascript-animation/SKILL.md` l. 14 et 84 |
| `regarder.py` : Windows seulement sans variable d'environnement ; liens `/shorts/` refusés ; deux nouvelles tentatives automatiques après une erreur 429 | `outils/gemini/regarder.py`, `skills/regarder/SKILL.md` l. 23 |
| Étude d'une chaîne de référence : l'API YouTube Data est citée, sans outil ni clé dans le plugin | `skills/thumbnail-strategist/`, `skills/youtube-seo/` |

## Non testé (le CLI `claude` de la machine n'est connecté à aucun compte)
- l'arrivée de `REGLES_STUDIO.md` dans le contexte au début d'une vraie session, et après `/clear`, `/compact` ou `/reload-plugins` (depuis la 0.2.2, le texte injecté fait moins de 9 500 caractères ; à confirmer en session que l'aperçu de 2 Ko n'apparaît plus) ;
- l'effet de `omitClaudeMd: true` sur `research` et `studio-maintainer` : le champ demande Claude Code 2.1.271 ou plus (2.1.169 sur la machine de mise au point) ;
- l'effet réel de `disable-model-invocation` sur la liste des skills d'une session (`claude plugin details` ne le déduit pas de son estimation) ;
- le `agent_type` reçu par le garde-fou dans un vrai sous-agent ;
- le préchargement de `studio-faceless:thumbnail-strategist` et `studio-faceless:shorts` par les agents ;
- le chemin du cache cherché par le crochet `pre-commit` d'une chaîne ;
- l'effet de `claude plugin install --scope project` sur `.claude/settings.json`.

Ces tests se font à la bascule de StudioV1.
