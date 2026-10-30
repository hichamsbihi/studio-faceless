# Journal des versions

La version installée est celle de `plugins/studio-faceless/.claude-plugin/plugin.json`. Une modification n'arrive dans les chaînes que si ce numéro change.

## 0.2.2 (30/10/2026)
Contexte de départ allégé (VALIDÉ, Hicham, 30/10/2026, après l'audit du contexte de StudioV3 : 85 k tokens au démarrage, dont environ 2,2 k pour le plugin).
- `disable-model-invocation: true` sur six skills qu'aucun autre fichier du plugin n'appelle : `humanizer`, `find-skills`, `javascript-animation`, `soundtrack`, `elevenlabs-music`, `elevenlabs-sound-effects`. Ils restent appelables à la main avec `/nom` et ne pèsent plus au démarrage. Non touchés : `grilling`, `regarder`, `frontend-design` (appelés par d'autres fichiers), `shorts` et `thumbnail-strategist` (préchargés par des agents, ce que ce réglage interdit).
- Descriptions raccourcies de `episode`, `youtube-seo`, `shorts` et `thumbnail-strategist` ; les déclencheurs d'usage sont conservés, le détail reste dans le corps de chaque skill.

## 0.2.1 (30/10/2026)
Nouveau skill `remove-background`, règle générale du plugin (VALIDÉ, Hicham, 30/10/2026 : « rend remove-background général pour tout le plugin »).
- `skills/remove-background/` : skill écrit sur Maps & Means (StudioV2) le 28/10/2026 d'après la référence des skills HyperFrames, généralisé : installation du modèle local avec l'accord du propriétaire, choix de la voie (personne, objet vu en petit, objet sur fond uni vu de près), masque déterministe, commande `hyperframes remove-background`, méthode en quatre étapes pour les personnes (Q117 de l'E010 d'AA), règles de composition. Les miniatures gardent leur détourage par polygone.
- Agent `motion-producer`, `REFERENTIEL_QUALITE_REALISATION.md` § 2 ter et fiche CUTOUT-FIGURE : renvoient au skill au lieu de recopier la méthode.

## 0.2.0 (30/10/2026)
Niveau « domaine » et deux règles de l'E010 d'AA devenues générales, au passage de StudioV1 au plugin (tableau de passage de StudioV1, recommandations 2 et 4, VALIDÉ, Hicham, 30/10/2026).
- `domaines/` : `README.md` (ordre de priorité plugin < domaine < chaîne, brancher et créer un domaine), `_modele/DOMAINE.md` et premier profil `sport/DOMAINE.md` (sources primaires, droits des images dont les compétitions admises pour les vraies vidéos de match, pièges de faits, son, veille), tiré des règles d'AA.
- `hooks/regles_studio.py` : lit la ligne `- **Domaine** : <domaine>` du `CLAUDE.md` de la chaîne et ajoute le chemin du profil aux règles communes ; signale un domaine sans profil. Une chaîne sans cette ligne reçoit les mêmes règles qu'avant.
- `REGLES_STUDIO.md` : ordre de priorité et ligne « Règles du domaine » dans « Quoi lire » ; agents `research` et `art-director`, skill `episode` : lecture du profil du domaine ; `starter/CLAUDE.md` et `NOUVELLE_CHAINE.md` : le domaine est la première question d'une nouvelle chaîne.
- `REFERENTIEL_QUALITE_REALISATION.md` § 2 quater : aucune image fixe tirée d'une vidéo (Q95 de l'E010), à la place de « arrêt sur image : 2 s au plus ».
- `REFERENTIEL_QUALITE_REALISATION.md` § 2 ter, `MOTION_CATALOG.md` (CUTOUT-FIGURE), agent `motion-producer` : personnes détourées avec `remove-background` de HyperFrames en local et méthode en quatre étapes (Q117 de l'E010), à la place du `clip-path` tracé à la main. Les miniatures gardent leur détourage par polygone (`thumbnail-strategist`), Q117 ne visant que les films.

## 0.1.3 (29/10/2026)
Nouveau skill `frontend-design`, ajouté à la demande de Hicham le 29/10/2026 pour des planches et des compositions d'un niveau plus professionnel.
- `skills/frontend-design/` : copie du skill d'anthropics/skills (Apache 2.0, commit `ca45fc4`), avec son `LICENSE.txt` et un `PROVENANCE.md` (source, empreintes). Méthode de directeur artistique : plan de jetons relu contre le brief avant de construire, une seule idée forte, critique sur captures, liste des défauts visuels génériques.
- Une section « Règles du studio » placée sous le titre l'étend aux planches de direction artistique et aux compositions HyperFrames, fait passer la marque validée de la chaîne avant ses préférences et rappelle les règles sur les images et les polices.
- Trouvé avec `find-skills` ; écartés après lecture : `canvas-design` (affiches abstraites, polices à télécharger), `impeccable` (programme téléchargé au premier lancement), `design-taste-frontend` (scripts signalés par les audits, skills de génération d'images dans le même dépôt).
- Listes des skills mises à jour : `README.md`, `DEMARRAGE.md`, `docs/README.md`, `docs/reference/skills-annexes.md`, `docs/reference/starter-et-depot.md`, `docs/workflows/installation-et-mise-a-jour.md`.

## 0.1.2 (29/10/2026)
Trois nouveaux skills, ajoutés à la demande de Hicham le 29/10/2026 : `find-skills`, `elevenlabs-sound-effects` et `elevenlabs-music`.
- `skills/find-skills/` : copie du skill de vercel-labs/skills (MIT, commit `773fb2c`), avec son `LICENSE` et un `PROVENANCE.md` (source, empreintes). Il sert à chercher des skills utiles au studio (premier usage : effets sonores et musique de fond).
- Le texte d'origine lance `npx skills` et installe avec `-g -y` ; une section « Règles du studio » placée sous le titre le remplace par la méthode déjà suivie pour `humanizer` : recherche sur skills.sh et GitHub par le web, vérification (installations, source, étoiles, licences, dépendances), copie à la main sur décision du propriétaire, nouvelle version du plugin.
- `skills/elevenlabs-sound-effects/` et `skills/elevenlabs-music/` : copies des skills `sound-effects` et `music` d'elevenlabs/skills (MIT, commit `503d4e9`), trouvés avec la méthode de `find-skills`, avec `LICENSE` et `PROVENANCE.md`. Une section « Règles du studio » remplace leur mise en route par `npx -y @elevenlabs/cli@latest onboard init` : SDK Python `elevenlabs` figé dans le `requirements.txt` de la chaîne, clé d'API posée par le propriétaire dans `ELEVENLABS_API_KEY` (Claude ne la lit jamais), génération à la demande explicite du propriétaire, forfait payant pour l'usage commercial.
- Listes des skills mises à jour : `README.md`, `DEMARRAGE.md`, `docs/README.md`, `docs/reference/skills-annexes.md`, `docs/reference/starter-et-depot.md`, `docs/workflows/installation-et-mise-a-jour.md`.

## 0.1.1 (29/10/2026)
Trois correctifs relevés en créant une nouvelle chaîne, le 29/10/2026.
- `verifier_depot.py` : la recherche de secrets ne prend plus « sk- » ou « sk_ » au milieu d'un mot pour une clé d'API (« risk-… », « task-… », une URL en « dsk-… ») ; la clé doit commencer le jeton. Les clés `sk_live_…` et `sk_test_…`, que le motif `sk_` manquait, sont désormais détectées. Nouveau test : `outils/test_verifier_depot.py`.
- Licences des médias, décision de Hicham du 29/10/2026 : la citation encadrée (`REFERENTIEL_QUALITE_REALISATION.md` § 2 bis, validée sur AA les 24 et 28/10/2026) est la règle par défaut ; une chaîne peut s'en tenir aux licences libres par un écart. `REGLES_STUDIO.md` (Règles permanentes), le § 2 bis et la règle d'or 4 (`README.md`, `DEMARRAGE.md`) le disent désormais, au lieu de « Médias réels sous licence libre ».
- Installation d'une chaîne : `claude plugin marketplace add hichamsbihi/studio-faceless --scope project` avant `claude plugin install` ; sans elle, Claude Code 2.1.169 répond « Plugin "studio-faceless" not found in marketplace ». Ajouté à `NOUVELLE_CHAINE.md`, `INSTALLATION.md` § 4, `DEMARRAGE.md` (B4) et aux workflows `nouvelle-chaine.md` et `installation-et-mise-a-jour.md`, avec la ligne d'erreur.

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
