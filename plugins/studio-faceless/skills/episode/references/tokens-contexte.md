# Tokens et contexte

Les règles communes du studio (`${CLAUDE_PLUGIN_ROOT}/REGLES_STUDIO.md`, « Économie de tokens et de contexte ») font foi. Voici ce que l'E007 d'AA a mesuré et ce qu'on en tire.

## Coûts constatés (AA, E007, 24/10/2026)
| Travail | Coût |
|---|---|
| Producteur de séquence | 330 à 460 k |
| Agent court de correction | 170 à 200 k |
| Chercheur de médias | 260 à 340 k |
| Reprise d'un producteur au cache froid | tout son contexte, réécrit |

## Points de compactage
À la fin de chaque grande étape :
- sujet ;
- recherche ;
- angle ;
- script ;
- voix ;
- socle ;
- séquence témoin ;
- chaque lot ;
- collage et mix.

Avant, écrire l'état dans le `CLAUDE.md` de l'épisode et le `BRIEF.md`. Consigne : « garder les décisions VALIDÉES, les chemins et l'état des rendus ; oublier les sorties de commandes et les lectures ».

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
