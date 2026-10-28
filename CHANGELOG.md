# Journal des versions

La version installée est celle de `plugins/studio-faceless/.claude-plugin/plugin.json`. Une modification n'arrive dans les chaînes que si ce numéro change.

## 0.1.0 (28/10/2026)
Première version, tirée de StudioV1 (chaîne Apparently Athletic) dans son état du 28/10/2026.
- Skills : episode, shorts, thumbnail-strategist, youtube-seo, direction-sonore, regarder, grilling, grill-me, humanizer, javascript-animation, soundtrack.
- Agents : research, art-director, motion-producer, shorts-producer, studio-maintainer.
- Garde-fou : le rôle se déduit du type d'agent, puisqu'un plugin ignore les hooks déclarés dans l'en-tête d'un agent. Il refuse aussi toute écriture dans le plugin installé.
- Règles communes injectées au début de chaque session (`REGLES_STUDIO.md`).
- Référentiels par défaut : qualité de réalisation, direction audio, catalogue d'animations, méthode de récit.
- Outils : contrôles, montage, cartes, shorts, rendu, archivage, contrôle du dépôt, suivi des tokens. Ils travaillent dans le dossier de la chaîne (`CLAUDE_PROJECT_DIR`, sinon le dossier courant).
- Gabarit de séquence v3, modèles d'épisode et de contrat de mission, squelette de chaîne (`starter/`), skills HyperFrames 0.8.149 figés (`vendor/`).
