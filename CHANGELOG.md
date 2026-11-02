# Journal des versions

La version installée est celle de `plugins/studio-faceless/.claude-plugin/plugin.json`. Une modification n'arrive dans les chaînes que si ce numéro change.

## 0.5.0 (02/11/2026)
Méthode de recherche de l'étape 1, rendue générale à la demande du propriétaire (« tu consignes ces changements de recherches dans le plugin pour qu'il soit général », 02/11/2026), après l'essai de l'E011 d'AA : deux méthodes lancées sur la même demande puis comparées à la source (habituelle : 1 fait faux sur 40 vérifiés ; Perplexity seule : deux fois plus rapide, 2 faux et 2 introuvables sur 42, aucune licence établie). Choix du propriétaire : « Éclaireur puis habituelle ».
- **Éclaireur Perplexity** (skill `episode` : `SKILL.md`, `etapes.md` § 1, `grilles.md` § 1) : si la session a le serveur MCP `perplexity`, un agent général par partie lance un `perplexity_research` (réglage `high`) et écrit `research/perplexity/R-*.md` ; des pistes et des sources primaires, aucun fait vérifié. Parties lancées ensemble, jamais d'appels `perplexity_ask` en parallèle (429). Nombre d'appels, payants, décidé à la porte ; sans serveur, `research` seul.
- **Agent `research`** : reçoit le rapport de l'éclaireur au contrat, ouvre chaque source avant de retenir un fait, note les pistes écartées et fait seul les médias (page du fichier, licence, empreinte).
- **Installation** (`DEMARRAGE.md`, B6) : clé `PERPLEXITY_API_KEY` dans l'environnement, serveur `@perplexity-ai/mcp-server@1.3.0` déclaré par chaîne en portée `local` (`cmd /c npx`, délai de 15 min), redémarrage complet de l'application.
- **Documentation** : workflows recherche et épisode, fiches skill episode et agents.

## 0.4.1 (02/11/2026)
Contexte du fil principal, demandé par le propriétaire le 02/11/2026 (« on n'utilise plus clear juste compact, opus sera le model de claude directeur ») après une mesure de la session d'AA : 319 appels, contexte médian de 278 k, aucun `/clear` de la journée.
- **Hook `contexte_alerte.py`** (`hooks/`, événement `UserPromptSubmit`) : à chaque message du propriétaire, mesure le contexte du dernier appel du fil principal (entrée + cache lu + cache écrit, comme `outils/suivi_tokens.py`). Dès 200 k, puis à chaque palier de 50 k, il rappelle d'écrire l'état et de proposer un `/compact`. Ne bloque jamais un message ; testé sur un journal de 15,6 Mo (alerte à 264 k, 0,17 s).
- **Plus de `/clear`** (`REGLES_STUDIO.md`, skill `episode` : `SKILL.md`, `etapes.md`, `tokens-contexte.md`) : à chaque fin de porte, l'état écrit, Claude propose un `/compact` avec la consigne de `tokens-contexte.md`. La mesure du 30/10/2026 reste citée comme coût connu.
- **Claude principal sur Opus** (`REGLES_STUDIO.md`, Studio Director) : jamais de changement de modèle en cours de session. Les agents en `model: inherit` le suivent ; `research`, `reviewer` et `studio-maintainer` restent en sonnet.
- **Documentation** : `DEMARRAGE.md`, `docs/` (session et garde-fou, outils et garde, skill episode, modèles, architecture, points ouverts, agents) ; `omitClaudeMd` devrait agir dans l'application de bureau (déduit de la version), qui fait tourner son propre Claude Code (2.1.309 le 02/11/2026).

## 0.4.0 (02/11/2026)
Nouvel agent de stratégie, demandé par le propriétaire le 02/11/2026 après le positionnement d'AA (« le plugin doit avoir un agent spécialiste [...] pour les autres chaînes [...] tout ce travail ne doit plus polluer le contexte principal »).
- **Agent `strategist`** (`agents/strategist.md`) : positionnement et stratégie éditoriale d'une chaîne, une phase par appel (`dossier`, `brief`, `conseil`, `titres`, `sujets`, `banque`). Il rend une synthèse de 300 mots au plus ; ses lectures restent dans son contexte. Contrat : deux champs en plus, `phase` et `session` ; démarre sans le `CLAUDE.md` de la chaîne. Leçons d'AA intégrées (coût d'un conseil, pièges des titres, argent jamais dans la promesse quand la ligne l'interdit).
- **Garde-fou, rôle `stratege`** (`hooks/garde_commandes.py`) : Write et Edit seulement dans `docs/` et `direction/BANQUE_SUJETS.md` ; en Bash, `python` sur les outils du plugin installé, `ls`, `wc`, `grep`, `head`, `tail`, `mkdir`, `cd`, sans script en ligne ni écriture hors de `docs/` ; tout argument d'un outil Python qui ressemble à un chemin doit être dans `docs/` (un outil écrit par son argument de sortie, que le garde ne voyait pas). Essayé le 02/11/2026 sur une entrée simulée du hook : écritures dans `docs/` et la banque permises ; `direction/`, un chemin hors de la chaîne, `cp`, `python -c`, un script hors du plugin refusés.
- **Copie figée de roast-room** (`vendor/roast-room/`, MIT, commit `e40f406`) : protocole du Chair, cerveaux et consignes des 12 sièges, `check_quotes.py` ; ni skill ni agent, lue par `strategist` seulement. Fiche dans `docs/reference/vendor.md`.
- **Outils** (`outils/recherche/`) : `youtube_chaine.py`, relevé de toutes les vidéos publiques d'une chaîne par l'API YouTube Data v3 (ratio sur les 30 longues voisines, refus d'écraser ; clé posée par le propriétaire) ; `youtube_resume.py`, résumé d'un relevé (formats, années, titres, plus forts ratios, territoires par motifs, sponsors) sans lire le JSON en entier. Validés sur AA (26/10 et 02/11/2026).
- **Banque de sujets** : le skill `episode` (`references/choix-sujet.md` § 4) lit d'abord `direction/BANQUE_SUJETS.md` de la chaîne s'il existe, sans refaire la recherche de ses sujets.
- `REGLES_STUDIO.md` : sept agents ; `templates/CONTRAT_MISSION.template.md` : champs de `strategist` et ligne des règles de la chaîne qui lui sont utiles.

**Nettoyage** (audit du 02/11/2026, lots 1 et 2 VALIDÉS par le propriétaire le même jour) :
- **Garde-fou** : le préfixe `aa-` des anciens agents de StudioV1 n'est plus reconnu (aucune chaîne n'a d'agent `aa-*`, vérifié le 02/11/2026).
- **Sauvegarde** (`outils/sauvegarde-chaine.ps1`) : éléments par défaut `docs` et `archives` ajoutés (`docs/` est hors Git, la sauvegarde en est la seule copie), `templates` retiré ; un élément absent reste signalé et ignoré.
- **Doublons retirés** : `REGLES_DETAIL.md` renvoie au skill `episode` pour les étapes (0 à 13) et à la table `ROLES` de `hooks/garde_commandes.py` pour les rôles.
- **Starter** : règles LFS et `.gitignore` sur `templates/` retirées ; `docs/` ajouté au `.gitignore` ; `settings.json` : `render.sh` au lieu de `render.mjs`, outils de `strategist` autorisés.
- **Skills** : descriptions de `remove-background` (641 → 273 caractères) et `blender-pro` (333 → 289) en anglais, sous 300 ; `regarder` renvoie à `youtube_chaine.py` pour le relevé d'une chaîne.
- **Trois skills retirés** (Hicham, 02/11/2026) : `javascript-animation` et `soundtrack` (scripts injouables sans `playwright-core`, jamais utilisés) et `grill-me` (alias de `grilling`, invoqué directement), déplacés dans la corbeille du propriétaire. `humanizer` reste, comme surcouche de relecture des scripts. Le plugin compte 14 skills, dont 4 en appel manuel (`humanizer`, `find-skills`, `elevenlabs-music`, `elevenlabs-sound-effects`) ; la documentation est à jour.
- **Documents retirés** : `docs/CHANTIER_0.3.0_regles.md` et `_outils.md` (chantier clos) vont à la corbeille du propriétaire ; `docs/POINTS_OUVERTS.md` perd ses points résolus.
- **Documentation mise à jour** : `README.md`, `DEMARRAGE.md`, `INSTALLATION.md` (clés `YOUTUBE_API_KEY` et `GEMINI_API_KEY`, Claude Code 2.1.271 ou plus, version 0.4.0), `ARCHITECTURE.md` (niveau domaine dans l'ordre des règles), `docs/README.md`, `docs/reference/agents.md`, `templates.md`, `vendor.md`, `outils-et-garde.md`, `skill-episode.md`, `docs/workflows/session-et-garde-fou.md`, `archivage-et-sauvegarde.md`, `installation-et-mise-a-jour.md`, `outils/recherche/README.md`, `outils/gemini/README.md`, `agents/studio-maintainer.md` (`render.sh`), étiquette de `verifier_depot.py`.
- **Reste pour un commit de documentation séparé** : `docs/reference/starter-et-depot.md`, `referentiels.md`, `docs/workflows/depot-git.md` et le reste de `docs/reference/` décrivent encore l'état 0.2.3 ; descriptions de `find-skills` (303) et `humanizer` (350).

## 0.3.1 (02/11/2026)
Leçons de l'E010 d'AA versées aux pièges du skill `episode` (VALIDÉ, Hicham, 02/11/2026, « oui »). Celles qui étaient déjà dans le plugin depuis la 0.2.0 (aucune image fixe tirée d'une vidéo, détourage avec `remove-background`, `snapshot --describe false`) ne sont pas répétées.
- `skills/episode/references/pieges.md` : rangées d'unités identiques (« tableau périodique »), photo forte devenue motif, passages tout en dessin, ouverture de séquence presque vide, ralentis des résumés de match, règlement lu en entier avant un renversement, nom d'un prix secondaire, identifiant en double, durée sans voix ajoutée, porte du collage qui oublie la fin en douceur, appel à s'abonner hors du collage, `publication.py verifier` sur le journal du film voix, chemins absolus en tâche détachée, enveloppe des musiques, `niveau_lu` appliqué avant la baisse sous la voix.
- Aucune règle par défaut ne change : le niveau de musique plus haut (environ 7 LU sous la voix) et les miniatures retouchées par IA restent des écarts d'AA (`direction/ECARTS.md` de la chaîne).

## 0.3.0 (30/10/2026)
Règles, domaine et outils versés de Maps & Means (StudioV2) au passage de cette chaîne au plugin (relevés A et B du 30/10/2026, dix décisions VALIDÉES par Hicham le 30/10/2026). Les règles venues de MM sont `PROPOSÉ` dans le plugin jusqu'à leur premier emploi sur une autre chaîne. Le suivi détaillé (`docs/CHANTIER_0.3.0_*.md`) a été retiré le 02/11/2026, chantier clos.
- **Domaine `geo-economie`** (`domaines/geo-economie/DOMAINE.md`) : pas de conseil d'investissement (avertissement mot pour mot), neutralité géopolitique, sources de données et de médias, grammaire des cartes ; références et modèles MapLibre dans `domaines/geo-economie/cartes/` (modèles de l'E004 de MM, à adapter : ils supposent l'étalonnage de MM).
- **Règles générales** dans `METHODE_RECIT`, `REFERENTIEL_QUALITE_REALISATION`, `DIRECTION_AUDIO`, `REGLES_DETAIL` et les références du skill `episode` : evergreen et date de valeur, page de structure, test de décrochage, rétention de la première minute, lignes de source relues, aucune clé avant sa valeur, aucun cadre qui naît vide, raccord par noircissement, limiteur par piste, pièges (vidéo HDR cachée, `scale()` animé, une seule composition racine, Wikimedia, Pexels, Mixkit, PDF illisibles). La méthode de travail avec le propriétaire va dans `REGLES_DETAIL.md` (lu à la demande) et non dans les règles injectées.
- **Outils** : `controle/script.py` (relances et densité du script ; sans `direction/script_seuils.json` de la chaîne, ses écarts ne sont que des avis), `controle/pauses.py`, `raccourcir.py`, `recaler.py`, `medias/traiter.py` (SDR, extraits), `medias/calque360.py`, `medias/jbig2_page.py`, `medias/rendre_page_pdf.ps1`, `recherche/pdftexte.py`, `gemini/relire.py` (appel à l'API Gemini, comme `regarder.py`), `cartes/proj.py`, `shp.py`, `cog.py`. `remix.py` de MM n'est pas versé (il suppose un `mix.py` par séquence).
- **`controle.py licences`** : la liste des licences à relire se lit dans `direction/licences.json` de la chaîne s'il existe ; sans lui, rien ne change ; un fichier illisible donne un avertissement et la liste par défaut, sans bloquer les autres contrôles.
- **Gabarit v3, `render.sh`** : garde HDR (refus si une vidéo HLG ou PQ est dans le projet de la séquence, `ffprobe` par `HYPERFRAMES_FFPROBE_PATH`) et rendu `--sdr`. **Changement de comportement** : un projet qui contient une vidéo HDR ne se rend plus ; la refaire en SDR avec `outils/medias/traiter.py`. Les `render.sh` déjà copiés dans les séquences ne changent pas.
- **Skill `blender-pro`** (références MIT, `licences/`, `PROVENANCE.md`) : Blender 4.5 s'installe dans la chaîne (`outils/blender/`, hors dépôt, ajouté au `.gitignore` du starter), avec l'accord du propriétaire.
- **Relecture indépendante** faite avant l'envoi (30/10/2026) ; corrigés : garde HDR muette sans `ffprobe`, `licences.json` faux qui bloquait tout `controle.py`, seuils de MM qui faisaient échouer `script.py` sur les autres chaînes, lien mort vers `calque360.py`, règle de méthode dans le fichier injecté.
- **Agrandissement d'une image à l'écran** : 1,3 fois son pixel natif au plus, partout, recette v3 comprise (1,6 avant ; VALIDÉ, Hicham, 30/10/2026).

## 0.2.3 (30/10/2026)
Suite de la 0.2.2 (commit bd994e5, déjà envoyé sur GitHub) : nouveau numéro pour que `claude plugin update` livre ces changements. Contexte de départ allégé et règles réellement injectées (VALIDÉ, Hicham, 30/10/2026, « Apply all », après l'audit du contexte de StudioV3 du même jour). Constats de l'audit :
- l'application de bureau coupe tout `additionalContext` au-delà de 10 000 caractères ; `REGLES_STUDIO.md` en faisait 12 565 une fois le chemin substitué : seul un aperçu de 2 Ko arrivait au modèle, dans toutes les sessions depuis le 29/10, et les sections « Sous-agents », « Parcours d'un épisode », « Économie de tokens » et « Règles permanentes » n'étaient jamais lues ;
- coût permanent du plugin : environ 2,2 k tokens (`claude plugin details`), et `thumbnail-strategist` et `youtube-seo` apparaissaient sans description dans la liste des skills (budget dépassé) ;
- un `/compact` remet dans le contexte le texte des skills appelés et les fichiers lus récemment : 124,6 k au premier appel après compactage, contre 81 à 88 k pour une session neuve, soit environ 40 k de plus à chaque appel.

Changements :
- **Règles communes** : `REGLES_STUDIO.md` passe de 12 565 à 8 403 caractères (chemin de cache substitué). Les sections « Moteur et outils » et « Parcours d'un épisode » sont déplacées mot pour mot dans `referentiels/REGLES_DETAIL.md` (suite des règles communes, même autorité, lue selon la mission) et remplacées par deux lignes de renvoi ; une ligne du tableau « Quoi lire » y mène. `hooks/regles_studio.py` ajoute en tête « Texte tronqué par l'app : lire <racine>/REGLES_STUDIO.md en entier. » si le texte injecté dépasse 9 500 caractères. `outils/verifier_depot.py` refuse un `REGLES_STUDIO.md` de plus de 9 000 caractères (chemin substitué), avec son test.
- **Descriptions de 300 caractères au plus**, en anglais : `youtube-seo` 960 → 298, `thumbnail-strategist` 853 → 298, `shorts` 851 → 273, `episode` 815 → 293, `direction-sonore` 688 → 292, `regarder` 484 → 295. Ce qui en sortait et manquait au corps du `SKILL.md` y est ajouté. Somme des descriptions des skills proposés au démarrage : 8 902 → 2 746 caractères ; estimation de `claude plugin details` : 2 376 → 1 729 tokens (elle compte encore les six skills bloqués).
- **État et reprise d'un épisode** (skill `episode`, `etapes.md`, `tokens-contexte.md`, `REGLES_STUDIO.md`) : à chaque fin d'étape, `episodes/<id>/STATE.md` réécrit en entier (manifeste de 2,5 Ko au plus) et `episodes/INDEX.md` mis à jour ; à chaque fin de porte, `/clear` au lieu de `/compact` ; la reprise lit seulement `INDEX.md` puis `STATE.md` ; `/compact` reste permis au milieu d'une longue porte ; le modèle du fil principal ne change que juste après un `/clear`. Nouveaux modèles génériques `templates/STATE.template.md` et `templates/INDEX.template.md` (d'après ceux d'une chaîne, sans aucun contenu d'épisode) ; `CLAUDE.episode.template.md` renvoie à `STATE.md`.
- **ElevenLabs par l'API** (`referentiels/DIRECTION_AUDIO.md` § 4, skills `elevenlabs-*`, `musique-a-l-image.md`, installation) : SDK Python `elevenlabs`, clé dans `ELEVENLABS_API_KEY` jamais lue ni affichée ; le connecteur claude.ai est coupé par défaut ; chaque génération demande l'accord du propriétaire, coût annoncé avant ; les skills `elevenlabs-*` sont appelés avec `/nom` ou lus par Claude quand le propriétaire demande une génération. Remplace la règle sur les appels au connecteur.
- **Garde-fou** : rôle `relecteur` pour l'agent `reviewer` (`hooks/garde_commandes.py`) : en Bash, seules `ffprobe`, `ffmpeg` de mesure (`-f null`), `wc`, `ls`, `grep`, `head` et `tail`, sans redirection.
- **Agents** : nouvel agent `reviewer` (contrôle qualité en lecture seule d'un script, d'une séquence ou du film contre une liste : accroche, structure, durée, ton, protection des personnes, sources, règles de la chaîne ; Sonnet ; `Read, Grep, Glob, Bash` ; garde le `CLAUDE.md` de la chaîne ; rapport en tableau de 25 lignes au plus ; ne valide rien) ; le skill `episode` le cite comme contrôle avant de montrer un script, une séquence ou le film. `omitClaudeMd: true` pour `research` et `studio-maintainer` (champ qui demande Claude Code 2.1.271 ou plus) : le modèle de contrat de mission gagne une section « Règles de la chaîne utiles à la mission » (10 lignes au plus), obligatoire pour ces deux agents. Pas d'agents scriptwriter, seo ou producer (doublons du skill `episode`, de `youtube-seo` et des scripts de voix).
- **Documentation** : `README.md`, `DEMARRAGE.md`, `INSTALLATION.md`, `NOUVELLE_CHAINE.md`, `docs/` (agents, templates, référentiels, skill episode, skills annexes, outils et garde-fou, workflows de session, d'épisode, de sons, de dépôt Git et d'installation, points ouverts).

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
