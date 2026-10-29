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
- Décisions de Hicham du 28/10/2026, intégrées avant toute installation :
  - crédits CC BY par défaut dans le dossier YouTube, qu'une chaîne peut écarter dans `direction/ECARTS.md` ;
  - fiche `BRAND-SPLIT` (ex-AA-SPLIT) ;
  - § 4 de `DIRECTION_AUDIO.md` réécrit pour les deux connecteurs ElevenLabs ;
  - modèle de miniature : la dernière validée de la chaîne ;
  - statut `APPROUVE_PAR_<PROPRIETAIRE>`.
- Documentation complète (`docs/`) : une fiche par fichier, 18 workflows, index, points ouverts.
- Garde-fou : un producteur peut lancer par Bash les outils du plugin installé (son cache est sous `~/.claude/`) ; une remontée par `..` reste refusée.
- Alignements relevés par la documentation, selon la règle validée la plus récente ou selon le code :
  - corrections dans la même version ;
  - journal du collage en voix seule pour les chapitres et le SRT ;
  - mix du film unique ;
  - pas de balise de synthèse par défaut ;
  - rappel d'abonnement vers 2:00 ;
  - rendu sans `--workers` refusé ;
  - codes de sortie de `controle.py` ;
  - modèle de `CLAUDE.md` d'épisode.
- Décisions de Hicham du 29/10/2026 :
  - D1 : aucune image immobile plus de 1 s, partout (référentiel § 2 ter et porte B, gabarit v3, `controle.py`, méthode de récit) ;
  - D2 : le squelette autorise sans demande `assembler.py`, `mix_film.py` et `srt.py`, à la place des règles `mix.py` du gabarit v2 ;
  - D3 : `archiver_episode.py` reconnaît le dossier `montage/` du parcours v3 et garde le film en voix seule d'où le master est mixé ; testé sur l'aperçu de l'E010 d'AA ;
  - D4 : questions des portes 8, 9, 11 et 13 à écrire au prochain épisode ;
  - D5 : gabarit vertical et journal des shorts à créer au pilote des shorts.
- Guide pas à pas `DEMARRAGE.md` (29/10/2026) : préparer la machine, créer la chaîne et son identité, fabriquer et publier la première vidéo, archiver ; encadrés « Pas encore éprouvé » pour ce qui n'a pas été testé.
