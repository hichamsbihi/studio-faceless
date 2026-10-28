# Skills HyperFrames figés (copie du 21/10/2026)

Copie des skills de Claude Code utilisés avec le moteur **HyperFrames 0.8.149** (figé dans le `package.json` de chaque chaîne), prise dans `~/.claude/skills/` de la machine de référence le 21/10/2026. Une nouvelle machine reçoit exactement ces versions, pas les plus récentes (validé sur AA, 21/10/2026).

- **Contenu** : `hyperframes`, `hyperframes-animation`, `hyperframes-audio`, `hyperframes-cli`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-registry`, `hyperframes-studio`, `media-use`.
- **Licence** : Apache License 2.0, celle du paquet `hyperframes` 0.8.149 (champ `license` de son `package.json`) ; © HeyGen et les auteurs de HyperFrames. Copie sans modification.
- **Installation** : recopier chaque dossier dans `~/.claude/skills/` (`INSTALLATION.md` du dépôt, section 3). Ils restent des skills d'utilisateur, sans préfixe : les agents du plugin les préchargent sous ces noms. Les skills du studio arrivent par le plugin (`studio-faceless:…`).
- **À savoir** : ces skills sont parfois plus récents que le CLI 0.8.149 et demandent de mettre HyperFrames à jour (`upgrade`, `skills update`). Les règles du studio l'interdisent sans décision du propriétaire, et le garde-fou le refuse. Les commandes `hyperframes usage` et `hyperframes figma` n'existent pas en 0.8.149 ; `play` se remplace par `preview`.
- **Mise à jour de cette copie** : seulement avec une montée de version de HyperFrames décidée par le propriétaire ; nouvelle copie datée, ce fichier mis à jour, nouvelle version du plugin.
