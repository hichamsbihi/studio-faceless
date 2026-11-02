# Tokens et contexte

Les règles communes du studio (`${CLAUDE_PLUGIN_ROOT}/REGLES_STUDIO.md`, « Économie de tokens et de contexte ») font foi. Voici ce que l'E007 d'AA a mesuré et ce qu'on en tire.

## Coûts constatés (AA, E007, 24/10/2026)
| Travail | Coût |
|---|---|
| Producteur de séquence | 330 à 460 k |
| Agent court de correction | 170 à 200 k |
| Chercheur de médias | 260 à 340 k |
| Reprise d'un producteur au cache froid | tout son contexte, réécrit |

## Fin de porte : écrire l'état, puis `/compact` (validé sur AA, 02/11/2026 : plus de `/clear`)
À la fin de chaque grande étape (sujet, recherche, angle, script, voix, socle, séquence témoin, chaque lot, collage et mix) :
1. Réécrire en entier `episodes/<id>/STATE.md` (2,5 Ko au plus ; modèle `${CLAUDE_PLUGIN_ROOT}/templates/STATE.template.md`) et mettre à jour la ligne de l'épisode dans `episodes/INDEX.md` (`INDEX.template.md`). Le détail daté va dans `HISTORIQUE_ETAT.md`.
2. Proposer au propriétaire un `/compact` avec la consigne : « garder les décisions VALIDÉES, les chemins et l'état des rendus ; oublier les sorties de commandes et les lectures ». Après une coupure, reprendre en lisant seulement `INDEX.md` et ce `STATE.md` ; le `CLAUDE.md` de l'épisode, le `BRIEF.md` et l'historique se lisent à la demande.

**Coût connu** (mesure du 30/10/2026, sur une chaîne en production) : un `/compact` remet dans le contexte le texte des skills appelés et les fichiers lus récemment ; premier appel après compactage : 124,6 k, contre 81 à 88 k pour une session neuve. D'où l'état écrit avant, et une consigne courte.

- Au milieu d'une longue porte, un `/compact` reste permis après avoir écrit l'état. Le hook `contexte_alerte.py` (événement `UserPromptSubmit`) le rappelle dès 200 k de contexte, puis à chaque palier de 50 k.
- Claude principal tourne sur Opus (validé sur AA, 02/11/2026). Jamais de changement de modèle en cours de session : il recalcule tout le contexte.

## Lire peu
- Lire par plages. Une planche à la fois. Des sorties de commandes courtes (`tail`, `grep`).
- Confier les lectures lourdes à un sous-agent qui ne renvoie qu'une synthèse : provenances de tout un film, audits de vidéos, archives.
- Ne jamais relire le fichier `.output` d'un agent : son rapport arrive dans le message de fin. Si un fichier doit garder ce rapport, l'extraire par script du transcript `subagents/agent-<id>.jsonl`.

## Déléguer juste
- Préparer les faits avant de déléguer (cartes, logos, raccords, photos prises) : un producteur ne doit rien chercher hors de son contrat.
- Des briefs courts, qui renvoient aux consignes communes ; des contrats sans fichiers entiers recopiés.
- Les corrections dans la même version (`production.md` § 4).
- Les attentes de rendu se font en tâche suivie, jamais dans un sous-agent : son cache ne dure que 5 min.

## Écrire court
- Rapports d'agents de 12 lignes au plus.
- États d'épisode d'une ligne par fait.
- Pas de répétition d'un référentiel : renvoyer au fichier qui fait foi.
