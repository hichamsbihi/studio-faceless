# Points ouverts

> **Historique, non normatif** (bandeau posé par la 1.1.0, 04/11/2026) : cette page décrit le plugin tel qu'il était quand elle a été écrite. Les règles en vigueur sont dans `plugins/studio-faceless/` (`REGLES_STUDIO.md`, `referentiels/`, skills, agents) ; là où elle s'en écarte, ce sont elles qui s'appliquent.

Ce qui reste à décider ou à vérifier dans le plugin, relevé pendant l'écriture de la documentation (28/10/2026), mis à jour le 02/11/2026 (points réglés retirés, numéros de ligne recalés). Un point réglé sort de cette liste et entre dans le [`CHANGELOG`](../CHANGELOG.md).

## Décisions et tâches
| # | Point | Fichiers | Recommandation |
|---|---|---|---|
| D5 | **Shorts** : le skill (`PROPOSÉ`) suppose un gabarit vertical et un modèle de `SHORTS_JOURNAL.md`, absents du plugin | `skills/shorts/`, `agents/shorts-producer.md` | Décidé (Hicham, 29/10/2026) : à faire au pilote des shorts |

## Vérifications (Claude)
| Point | Fichiers |
|---|---|
| Unité des niveaux de l'exemple `montage.json` (impact −8, souffle −12…) face aux niveaux validés en LU sous la voix (impact 14, souffle 18…) | `outils/montage/README.md` l. 55-59, `referentiels/DIRECTION_AUDIO.md` § 3 |
| `controle.py planche` écrit ses étiquettes avec une police Windows échappée (`C\:/Windows/Fonts/arial.ttf`) ; un piège dit qu'un chemin Windows a fait échouer `drawtext` | `outils/controle/controle.py` l. 120, `skills/episode/references/pieges.md` l. 80 |
| Instants de la planche du producteur : 16 à 20, 16 ou 24 selon le fichier | `agents/motion-producer.md` l. 50, `templates/sequence-gabarit-v3/README.md` l. 64, `skills/episode/references/production.md` l. 65 |
| Seuil des bilans : 1 000 impressions ou « quelques centaines de vues » | `skills/episode/references/etapes.md` l. 78, `skills/youtube-seo/references/apres-publication.md` l. 15 |
| « Journal du master » encore employé là où les chapitres et le SRT demandent le journal du collage en voix seule (`<nom>-voix.log.txt`) ; certains emplois visent bien le master mixé | `skills/youtube-seo/references/description-et-credits.md` l. 20 et 38, `gabarit-et-controle.md` l. 11, `skills/episode/references/etapes.md` l. 54, `rendu-collage.md` l. 23, `referentiels/DIRECTION_AUDIO.md` l. 70, docstrings de `publication.py`, `srt.py`, `assembler.py` |
| Corrections des shorts : « nouvelle version, nouvel agent », alors que les épisodes corrigent dans la même version depuis le 24/10 | `templates/CONTRAT_MISSION.template.md` l. 35-36, `agents/shorts-producer.md` l. 101 |
| `mix.py` encore cité | `skills/shorts/references/montage-vertical.md` l. 67-68 |
| Texte de la licence Apache-2.0 absent de `vendor/` (le paquet `hyperframes` n'en fournit pas) | `vendor/claude-skills/README.md` |
| `regarder.py` : Windows seulement sans variable d'environnement ; liens `/shorts/` refusés ; deux nouvelles tentatives automatiques après une erreur 429 | `outils/gemini/regarder.py`, `skills/regarder/SKILL.md` l. 26-27 |

## Ouvert depuis la 0.6.0 (02/11/2026)
| Point | Fichiers |
|---|---|
| **Jamais lancés en vrai** (essais hors réseau seulement) : `telecharger_medias.py` (Commons, Pexels, liens directs), `generer_voix.py --executer` et `info_elevenlabs.py` (appels payants ou de compte), `mesurer_sons.py --whisper`. Le premier emploi sur une chaîne les éprouve | `outils/medias/`, `outils/voix/`, `outils/controle/mesurer_sons.py`, `outils/test_*.py` |
| **Le rôle `telechargeur` et l'agent `media-fetcher`** : le garde-fou est essayé sur des entrées simulées (`outils/test_garde_commandes.py`), pas dans une vraie session ; `agent_type` reçu dans un vrai sous-agent : même point non testé que ci-dessous | `hooks/garde_commandes.py`, `agents/media-fetcher.md` |
| **Soundza par un sous-agent** : un plugin ignore `mcpServers`, `media-fetcher` n'a donc pas les outils du serveur ; le téléchargement d'un son est fait par Claude principal ou, depuis la 0.7.0, par `sound-manager` (outils nommés dans son en-tête ; lien signé de 15 minutes). À vérifier en vraie session que ces outils lui parviennent | `agents/media-fetcher.md`, `referentiels/DIRECTION_AUDIO.md` § 4 bis |
| **Déclaration du serveur MCP `soundza`** : adresse relevée sur la page développeurs de Soundza (02/11/2026) ; la commande exacte (OAuth ou en-tête avec la clé en variable d'environnement) n'est pas figée dans le plugin, pour qu'aucune clé ne soit écrite en clair | `DEMARRAGE.md` B6 |
| **Licence de Soundza** : relevée le 02/11/2026 sur le serveur et la page développeurs ; à relire avant un nouvel usage (elle peut changer) | `referentiels/DIRECTION_AUDIO.md` § 4 bis |
| **Essai « Illusion of Novelty »** : `PROPOSÉ` jusqu'au bilan de J+7 de l'E011 d'AA (seuils de la chaîne) ; la grille de note est une paraphrase du document de Kallaway, jamais une copie ; version du PDF non datée dans la chaîne | `skills/episode/references/recit-retention.md` § 8 |
| **`CLAUDE_CODE_EXECPATH`** : le piège des copies de Claude Code est repris de l'audit du 02/11/2026 ; la lecture de la version à partir de cette variable n'a pas été refaite pour la 0.6.0 | `skills/episode/references/pieges.md` |
| Shorts : les docs `docs/reference/publication.md` et `docs/workflows/shorts.md` disent encore que le propriétaire génère la prise du short ; les voix de shorts n'ont pas été reprises dans la décision Q35 (film) | `docs/workflows/shorts.md`, `docs/reference/publication.md` |

## Ouvert depuis la 0.7.2 (03/11/2026)
| Point | Fichiers |
|---|---|
| **Branchement `hf-seek`** du code d'une démo de `vendor/lemo-opuscar/` : lu dans le moteur HyperFrames 0.8.149 (l'adaptateur `three` émet `hf-seek` à chaque image, sans exiger Three.js), pas encore éprouvé par un rendu ; première preuve prévue sur un short (`expérimental`) | `agents/shorts-producer.md`, `agents/motion-producer.md`, `vendor/lemo-opuscar/PROVENANCE.md` |
| **`rhythm_report.py`** (lemo-opuscar) : lit bien le 9:16, mais suppose 24 i/s, compte une transition rapide comme plusieurs coupes, garde tout le film en mémoire et écrit dans son propre dossier ; son seuil de « plat » (1,0) classe presque tout plan lent sur photo comme plat. Adaptation en outil du plugin à décider par le propriétaire | `vendor/lemo-opuscar/PROVENANCE.md` |

## Ouvert depuis la 0.7.0 (03/11/2026)
| Point | Fichiers |
|---|---|
| **Suite proposée en 0.7.3** (à confirmer par le propriétaire) : outils du plugin `miniature.py masque` et `mesurer_mix.py`, pour rendre aux agents le masque de détourage (`publisher`) et les mesures du mix (`sound-manager`). D'ici là, l'agent écrit son script et s'arrête ; Claude principal le relit et le lance (VALIDÉ, Hicham, 03/11/2026) | `hooks/garde_commandes.py`, `agents/publisher.md`, `agents/sound-manager.md`, `skills/thumbnail-strategist/references/fabrication.md` § 3, `skills/direction-sonore/references/musique-par-cues.md` § 4 |
| Shorts : musique « plus présente que dans les films » (environ 8 LU), alors que les films sont à 7 à 9 LU depuis le 03/11/2026 ; l'écart des shorts tient désormais au master (−14 LUFS) | `skills/shorts/references/montage-vertical.md` l. 67, `referentiels/DIRECTION_AUDIO.md` § 1 |

## Non testé (le CLI `claude` de la machine n'est connecté à aucun compte)
- l'arrivée de `REGLES_STUDIO.md` dans le contexte au début d'une vraie session, et après `/clear`, `/compact` ou `/reload-plugins` (depuis la 0.2.3, le texte injecté fait moins de 9 500 caractères ; à confirmer en session que l'aperçu de 2 Ko n'apparaît plus) ;
- `omitClaudeMd: true` sur `research`, `studio-maintainer`, `strategist` et `media-fetcher` : le champ demande Claude Code 2.1.271 ou plus. L'application de bureau fait tourner son propre Claude Code (2.1.309 le 02/11/2026) : il devrait y agir (déduit de la version, pas encore observé sur un sous-agent). Une copie du terminal plus ancienne l'ignore : sur la machine de mise au point, le `claude` du terminal est un 2.1.76 depuis le 02/11/2026, la copie winget un 2.1.292 ;
- l'effet réel de `disable-model-invocation` sur la liste des skills d'une session (`claude plugin details` ne le déduit pas de son estimation) ;
- le `agent_type` reçu par le garde-fou dans un vrai sous-agent ;
- le préchargement de `studio-faceless:thumbnail-strategist` et `studio-faceless:shorts` par les agents ;
- le chemin du cache cherché par le crochet `pre-commit` d'une chaîne ;
- l'effet de `claude plugin install --scope project` sur `.claude/settings.json`.
