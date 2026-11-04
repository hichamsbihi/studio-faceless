# Journal des versions

La version installée est celle de `plugins/studio-faceless/.claude-plugin/plugin.json`. Une modification n'arrive dans les chaînes que si ce numéro change.

## 0.8.0 (04/11/2026)
Skill `conseil` et agent `conseiller`, à la demande du propriétaire (04/11/2026 : « me trouver un skill dont l'idée est de créer un council, un conseil avec plusieurs agents pour en débattre », puis le choix « claude-council + débat »).
- **`skills/conseil/`** : plusieurs agents Claude indépendants débattent d'une décision du studio : avis en aveugle, débat sur les avis anonymes avec classement, contre-hypothèse si aucun désaccord majeur, compte rendu d'un président dans `docs/rapports/` de la chaîne. Script `conseil-workflow.js` pour l'outil Workflow ; porte du propriétaire avant tout lancement ; `disable-model-invocation: true`.
  - Adapté de amgadelgamal/claude-council (commit `819c1d0`) et de tsenart/council-skill (commit `2040ee1`), tous deux MIT : `LICENSE` et `PROVENANCE.md` du dossier.
  - Essai à sec dans Node avec de faux agents (9 cas) ; aucun conseil réel encore lancé : tours, sièges par défaut et coût à confirmer au premier conseil.
- **`agents/conseiller.md`** : siège du conseil, en lecture seule (Read, Grep, Glob, WebFetch, WebSearch), lancé par le script, jamais délégué directement. `REGLES_STUDIO.md` (8 984 caractères sur 9 000) ne le liste pas : sa liste devient « les dix agents délégués ».
- Documentation : `README.md`, `DEMARRAGE.md`, `docs/README.md`, `docs/reference/agents.md`, `skills-annexes.md`, `outils-et-garde.md`, `starter-et-depot.md`, `docs/workflows/installation-et-mise-a-jour.md`.
- Les outils `miniature.py masque` et `mesurer_mix.py`, proposés pour la 0.7.3, passent à une version suivante.

## 0.7.2 (03/11/2026)
Bibliothèque de styles lemo-opuscar, figée, et fiche de style par l'`art-director`, à la demande du propriétaire (03/11/2026 : « pourquoi refaire le travail à zéro alors qu'il est déjà servi […] on essaie de déléguer à un agent les différents styles et à chaque vidéo il fera son analyse et donnera les styles ou mix de styles qui conviendra avec bien sûr notre ligne artistique »). Décisions Q84 à Q88 de l'E011 d'AA, `VALIDÉ` (Hicham, 03/11/2026).
- **`vendor/lemo-opuscar/`** : copie figée du dépôt https://github.com/lemomo-ai/lemo-opuscar au commit `bebbbe1` (31/10/2026), sans modification.
  - Contenu : 2 083 fichiers, 43,2 Mo (66 styles avec `STYLE.md`, `style.json`, affiche et code de démo ; `core/` ; `LICENSE`), plus un `PROVENANCE.md`.
  - Licences : code et textes MIT ; images des démos CC BY 4.0 ; médias de tiers sous leur `CREDITS`.
  - Non copiés : leur installeur, leur skill, leurs manifestes de plugin, les images fixes des démos, les textures 3D, les banques d'instruments (1,42 Go, hors plugin).
  - Ni skill ni moteur : HyperFrames reste le seul moteur ; leurs scripts ne se lancent jamais.
- **`art-director`** : nouvelle phase « fiche de style » pour chaque film et chaque short, validée par le propriétaire avant tout producteur.
  - Démarche : tri par l'index et les `style.json`, affiches des seuls candidats, 2 ou 3 `STYLE.md` au plus ; puis, par temps fort, la technique, le fichier de démo et les adaptations.
  - Familles permises par défaut : styles documentaires et graphismes dessinés en code pour expliquer ; ni anime, ni jeux, ni peinture, ni 3D. Une chaîne peut faire autrement dans `direction/ECARTS.md`.
  - `REGLES_STUDIO.md` (ligne de l'agent, à longueur constante : 8 984 caractères), `docs/reference/agents.md`.
- **Skills** :
  - `shorts` : une ligne « fiche de style » dans « Qui fait quoi » ; étape 3 de la méthode ; ligne `style` dans le brief de short ;
  - `episode` : `socle.md` § 3 et la liste « avant un producteur ».
- **`shorts-producer` et `motion-producer`** : reprise du code d'une démo citée au brief.
  - Son `window.render(t)` devient un écouteur de `hf-seek` (horloge de l'adaptateur `three`, sans charger Three.js).
  - `expérimental` jusqu'à une première preuve par un rendu.
- **Essai de `rhythm_report.py`** (Q88), sur un extrait de 30 s d'un film de la chaîne, en 16:9 et en 9:16.
  - Le 9:16 se lit bien : corrélation de 0,96 entre les deux courbes de mouvement.
  - Mais le script suppose 24 i/s, compte une transition rapide comme plusieurs coupes, garde tout le film en mémoire et écrit dans son propre dossier.
  - Adaptation à décider (`docs/POINTS_OUVERTS.md`).
- Documentation : `README.md`, `docs/README.md`, `docs/reference/vendor.md`, `docs/POINTS_OUVERTS.md`.
- Les outils `miniature.py masque` et `mesurer_mix.py` sont proposés pour la 0.7.3 : aucun des deux ne sert au premier short, et chacun demande une table du garde-fou et des essais.

## 0.7.1 (03/11/2026)
Le travail d'un agent lui revient, voix des shorts comprise, à la demande du propriétaire (03/11/2026 : « ce travail est dans le périmètre du sound manager, pourquoi ne pas lui assigner cette tâche, consigne ça dans les règles générales du plugin »). Constat sur l'E011 d'AA : le garde-fou refusait `kit/shorts/` à `sound-manager`, et le skill `shorts` (19/10) confiait encore la voix du short à Claude principal ; Claude principal l'a donc faite lui-même.
- **Règle générale** : `REGLES_STUDIO.md` (Studio Director) confie à l'agent concerné toute tâche de son périmètre, même petite. Le détail est dans `referentiels/REGLES_DETAIL.md`, nouvelle section « Délégation aux agents », car `REGLES_STUDIO.md` était à 22 caractères de sa limite de 9 000 : Claude principal ne garde que les petites tâches hors de tout périmètre et ce que le garde-fou lui réserve ; un refus du garde-fou ne se contourne pas sans l'accord du propriétaire, il se signale avec la correction du plugin à décider.
- **`sound-manager`** : tout le son de l'épisode **et de ses shorts**. Nouvelle méthode « A bis. Voix d'un short » : préparation et chiffrage à blanc, contrôle, bandes longue et YouTube (`voix_short.py`), repères (`outils/shorts/recaler.py`), README ; musique et effets du short dans `kit/shorts/son/`. Le master du MP4 (`master_short.py`) reste à Claude principal.
- **Skill `shorts`** (« Qui fait quoi ») : voix et son du short à `sound-manager` ; l'appel payant à Claude principal, après la confirmation du propriétaire (la ligne « Générer la prise : le propriétaire » datait d'avant l'API) ; le reste du kit (médias, filigrane, gabarit, briefs) à Claude principal.
- **Garde-fou** (`hooks/garde_commandes.py`), rôle `ingenieur-son` :
  - zone élargie à `kit/shorts/voix/` et `kit/shorts/son/` ;
  - outils `outils/shorts/voix_short.py`, `recaler.py` et `raccord.py` ajoutés à sa table ;
  - nouveau genre d'option à nombre fixe de valeurs (tuple, comme `nargs=2`) pour `--sans-d DEBUT FIN`. Avec `v*`, `--sans-d 40 62 PRISE SORTIE` aurait avalé la sortie sans la contrôler ; `--sans-d=…` est refusé.
  - Tests (`outils/test_garde_commandes.py`) : commandes permises et refusées des shorts, dont ce cas.
- Les outils `miniature.py masque` et `mesurer_mix.py`, annoncés pour la 0.7.1, passent à la 0.7.2.

## 0.7.0 (03/11/2026)
Deux agents et les leçons de l'E011 d'AA, à la demande du propriétaire (03/11/2026 : « tu crées le skill pour un agent de sound manager […] tout le travail sonore sera dédié à cet agent ; un agent de publication avec la mission principale est la thumbnail […] et consigne-le dans le skill général avec les leçons apprises »). Leçons `VALIDÉ` sur AA le 03/11/2026 : le master v3 de l'E011, approuvé à l'écoute, et la miniature v2-3, choisie par le propriétaire.
- **Agent `sound-manager`** (`agents/sound-manager.md`, `opus`, skill `direction-sonore` préchargé, outils du serveur `soundza` sauf `generate_sound`) : tout le son d'un épisode.
  - Voix : prépare et chiffre l'appel puis s'arrête ; Claude principal le lance après l'accord du propriétaire. Ensuite : contrôle du texte, ralentissement ×0,97, repères après coupe sur les silences.
  - Sons de la liste validée (`marque/son/`, Soundza).
  - Plan de cues, plan son, mesures.
  - Aucun mix long : il écrit la commande, Claude principal lance `mix_film.py`, puis l'agent, relancé, mesure. Il n'écoute pas.
  - Il ne lance pas son script de mesure (`montage/mesures-vN/`) : il l'écrit, s'arrête et donne la commande ; Claude principal le relit et le lance, puis le relance (VALIDÉ, Hicham, 03/11/2026).
- **Agent `publisher`** (`agents/publisher.md`, `opus`, skills `thumbnail-strategist` et `youtube-seo` préchargés) : la miniature d'abord, puis le dossier de publication.
  - Miniature : concepts, trois calques, détourage voie A, `miniature.py`, contrôles et planche, au moins 2 variantes.
  - Détourage : recadrage, `remove-background`, écriture du script de masque, puis arrêt ; Claude principal relit et lance le masque, regarde le contrôle sur fond vert et relance l'agent pour le rendu (VALIDÉ, Hicham, 03/11/2026).
  - Dossier : avec le titre venu de `strategist` et validé ; aucun titre créé, aucune publication. Le SRT (`PUBLICATION_vN.<langue>.srt`, par `srt.py`) si le contrat le demande (VALIDÉ, Hicham, 03/11/2026).
- **Garde-fou** (`hooks/garde_commandes.py`) : rôles `ingenieur-son` et `editeur`.
  - Chacun a sa zone d'écriture, sa liste de commandes et une table de ses outils (`OUTILS`, `REMOVE_BACKGROUND`) : une option inconnue ou abrégée est refusée, et tout chemin d'écriture est contrôlé (espace, sans barre oblique, `--option=valeur`, sortie au milieu d'une commande ffmpeg, `file=` d'un filtre, `2>`).
  - Les segments se coupent hors des guillemets ; scripts en ligne, substitutions de commande et `cd` hors de la racine sont refusés.
  - Pour `ingenieur-son`, refusés aussi : `generer_voix.py --executer`, `mix_film.py` et `assembler.py`.
  - Aucun des deux ne lance ses propres scripts (VALIDÉ, Hicham, 03/11/2026) : le garde ne lit pas le contenu d'un script, qui pourrait écrire n'importe où. `python` sur un script de la zone est refusé sous toutes ses formes (`python3`, `py`, guillemets, chemin absolu, `./`), avec le message « un script de l'agent est relu et lancé par Claude principal ».
  - Essais : `outils/test_garde_commandes.py` (classe `Roles07`, dont `test_script_de_la_zone_refuse`).
- **Skill `episode`** :
  - `SKILL.md` (étapes 4, 10 à 12 et paragraphe des agents) et `etapes.md` (§ 4, 10, 11, 12) : `sound-manager` et `publisher` ; Claude principal coordonne, lance les tâches longues et payantes, soumet au propriétaire ;
  - `pieges.md` : leçons de l'E011 (Son, et nouvelle section « Miniatures et publication ») ;
  - `socle.md` § 6 (Soundza aussi par `sound-manager`) et `rendu-collage.md` § 4 (qui fait quoi au mix).
- **Skill `direction-sonore`** : `references/musique-par-cues.md`, méthode par défaut, renvoyée depuis `SKILL.md`. Elle contient :
  - la recette (cues de 15 à 40 s, marques, une tonalité, sauts par mesures entières, 7 à 9 LU sous la voix) ;
  - la séquence témoin en deux variantes ;
  - le contrôle sans écoute (résidu, écart par cue, hausse des marques) ;
  - les faits de `mix_film.py`.

  Elle devient la règle par défaut de toutes les chaînes (VALIDÉ, Hicham, 03/11/2026) ; une chaîne qui veut autre chose l'écrit en écart.
- **`referentiels/DIRECTION_AUDIO.md`** aligné sur la recette (validé sur AA, 03/11/2026, master v3 de l'E011) : musique de 7 à 9 LU sous la voix (§ 2), départ à 8 (§ 3) ; les marques de la recette remplacent l'impact grave à chaque bloc ou chapitre (§ 2) ; Soundza téléchargé par `sound-manager` ou Claude principal, liste validée seulement, toujours sans `generate_sound` pour un sous-agent (§ 4 bis). Alignés aussi : `REFERENTIEL_QUALITE_REALISATION.md` (changement de bloc), `rendu-collage.md` § 4 (tableau des niveaux), `outils/montage/README.md` (exemple `niveau_lu` −8). `mix_film.py` n'a pas changé (aucun niveau de musique par défaut).
- **Skill `thumbnail-strategist`** :
  - `references/trois-calques-e011.md`, grammaire par défaut (VALIDÉ, Hicham, 03/11/2026) ;
  - `SKILL.md` (variantes, grammaire, agent, refus « $0 » et scène inventée) ;
  - `grammaire-e003.md` (en secours), `fabrication.md` (trois calques ; dossier `travail/` de `publisher` ; masque lancé par Claude principal), `controles.md` (un seul point d'attention, bandeau d'une ligne).
- **Skill `youtube-seo`** : renvoi à `publisher` (titres reçus, jamais créés).
- `REGLES_STUDIO.md` : dix agents ; phrase sur les agents sans `CLAUDE.md` rendue générale ; deux phrases raccourcies pour rester sous 9 000 caractères (8 978). `REGLES_DETAIL.md` : qui prépare et qui lance l'appel payant ; les sons aussi par `sound-manager`.
- Documentation : `README.md`, `DEMARRAGE.md` (dix agents), `docs/README.md`, `docs/ARCHITECTURE.md`, `docs/reference/agents.md` (deux fiches), `docs/reference/outils-et-garde.md` (table `ROLES`, scripts des agents), `docs/workflows/installation-et-mise-a-jour.md` ; niveaux et marques dans `docs/reference/son.md`, `docs/reference/skill-episode.md`, `docs/workflows/sons.md`, `episode.md` et `collage-et-mix.md`.
- **Suite prévue en 0.7.1** : outils du plugin `miniature.py masque` et `mesurer_mix.py`, pour rendre ces deux étapes aux agents (`docs/POINTS_OUVERTS.md`).

## 0.6.1 (03/11/2026)
Détourage des miniatures par `remove-background` (VALIDÉ, Hicham, 03/11/2026 : « tu utilises le modele remove-background de hyperframes et tu le consigne dans le plugin et install pillow »). Méthode appliquée et vérifiée le 03/11/2026 sur la v2 des miniatures de l'E011 d'AA.
- `skills/thumbnail-strategist/references/fabrication.md` : intro et § 3 « Détourage du sujet » en deux voies. Voie A : recadrage, `hyperframes remove-background --device cpu`, masque resserré de 2 px et flou 0,7 multiplié par un polygone séparateur (Pillow), contrôle sur fond vert vif, page et rendu inchangés. Voie B : le polygone tracé à la main, gardé en secours. Le refus d'image générée par IA ne change pas.
- `skills/thumbnail-strategist/SKILL.md` (étapes 4 et 5), `skills/remove-background/SKILL.md` (« Pas pour les miniatures » retiré ; la miniature suit le § 4 bis) : alignés.
- `referentiels/REGLES_DETAIL.md` (Poste de travail) : « Pas de Pillow » remplacé par Pillow installé le 03/11/2026, pour le masque des miniatures.
- `docs/workflows/miniature.md` (étape 7, précisions, diagramme, commandes) et `docs/reference/publication.md` (fiches `fabrication.md`, `grammaire-e003.md` et `miniature.py`) : la voie A `remove-background` et le polygone en secours (voie B), avec renvoi à `fabrication.md` § 3. `grammaire-e003.md` (historique de la v4), `starter/requirements.txt` et `DEMARRAGE.md` sont laissés tels quels.

## 0.6.0 (02/11/2026)
Quatre ajouts demandés par le propriétaire d'AA le 02/11/2026 (« kalalway api elevenlabs et api soundza avec telechargemnt mene par un agent claude sont a ajoute dans le plugin ; applique aussi les propositions de l'agent »), tous validés sur AA à cette date, plus les corrections de l'audit des décisions du même jour. Chaque ajout vient d'une décision de l'E011 d'AA (Q18 et Q25, Q35, Q45, Q56 et Q57).
- **Téléchargement des médias mené par Claude ou un agent** (remplace « le propriétaire télécharge à la main, aucun téléchargement en lot », 24/10/2026) :
  - règle : `REFERENTIEL_QUALITE_REALISATION.md` § 2 bis ; une liste validée par le propriétaire, un seul accord, dépôt `kit/media/source-vN/`, aucun contournement (Cloudflare, accès payant, connexion, CAPTCHA, filigrane), un fichier refusé reste au propriétaire (`manuel/`) ; reprise dans le skill `episode` (`SKILL.md` règle 3 et liste de contrôle, `socle.md` § 4 à 6, `grilles.md` § 5, `pieges.md`), `REGLES_DETAIL.md`, `agents/research.md` ;
  - **agent `media-fetcher`** (`agents/media-fetcher.md`, Read, Write, Bash, Glob, Grep) : télécharge la liste, rend un manifeste, ne choisit ni ne cherche rien ; huit agents dans `REGLES_STUDIO.md` ; contrat de mission complété ;
  - **outil `outils/medias/telecharger_medias.py`**, généralisé des trois scripts de l'E011 : types `commons` (API, original, SHA-1 de l'API), `direct`, `pexels` (serveur de fichiers, jamais la page) ; aperçu par défaut, `--executer` pour télécharger ; robot identifié par une adresse de la chaîne (adresse e-mail refusée) ; 3,5 s entre deux fichiers, attente doublée après un 429, trois essais ; aucun écrasement ; manifeste JSON et liste du propriétaire ; liens signés masqués. Essai hors réseau : `outils/test_telecharger_medias.py` ;
  - **garde-fou, rôle `telechargeur`** (`hooks/garde_commandes.py`) : l'agent n'écrit que sous `episodes/<id>/kit/media/source-vN/` et ne lance que `telecharger_medias.py` ; ni `curl` ni `wget` ; les options de l'outil sont lues par leur nom entier (forme `--option=valeur` comprise ; l'outil refuse les abréviations), toute option inconnue est refusée et tout autre argument est contrôlé comme un chemin, même avec une espace. Essai : `outils/test_garde_commandes.py`.
- **ElevenLabs par l'API** (corrige C2 de l'audit) : Claude génère les prises, chaque appel payant annoncé avec son coût et confirmé par le propriétaire (`DIRECTION_AUDIO.md` § 2 et § 4, `etapes.md` § 4). **Outils `outils/voix/`** : `generer_voix.py` (à blanc par défaut, coût annoncé, `--executer --confirme-credits N` seulement avec le coût exact, aucun écrasement, premier échec = arrêt, manifeste) et `info_elevenlabs.py` (facteur de coût, voix, solde, lecture seule). Clé jamais écrite ni affichée. Essai hors réseau : `outils/test_generer_voix.py`.
- **Soundza** (`DIRECTION_AUDIO.md` § 4 bis, `socle.md` § 6, skill `direction-sonore`) : serveur MCP ou API, clé `SOUNDZA_API_KEY` dans l'environnement ; licence annoncée par Soundza (libre, sans crédit obligatoire ; interdits : revendre ou redistribuer un son seul et non modifié, entraîner une IA ; aucune garantie de droits ni de Content ID) ; sons faits par IA (`ai_content`) dits au propriétaire ; **dépôt privé** pour une chaîne qui garde des sons Soundza ; crédit demandé, facultatif, écarté par un écart ; téléchargement dans `kit/media/source-vN/soundza/` ; `generate_sound` jamais sans demande. **Contrôle des sons de bibliothèque** (S21 de l'audit) : `outils/controle/mesurer_sons.py` (format, canaux, niveau, crête vraie, boucle, Whisper pour une parole). Essai : `outils/test_mesurer_sons.py`.
- **Kallaway, « Illusion of Novelty »** (`recit-retention.md` § 8, `choix-sujet.md` § 3, `grilles.md` § 3) : le principe en nos mots, une citation de six mots, jamais le PDF ; statut « essai en cours sur AA » (`PROPOSÉ`) ; grille de note sur 10 et protocole de bilan à J+7 généralisé (seuils fixés avant la sortie sur les films comparables, 300 vues, essai prolongé, limites).
- **Corrections de l'audit du 02/11/2026** :
  - C3 : l'accès OAuth en lecture seule de la 0.5.1 est dit comme seule exception aux « refus permanents » (`youtube-seo` : `SKILL.md`, `apres-publication.md` ; `docs/reference/publication.md`, `docs/workflows/dossier-youtube.md`) ; le garde-fou refuse `youtube_retention.py` au rôle `strategist` (réservé à Claude principal) ;
  - Claude Code 2.1.271 ou plus dans `docs/workflows/installation-et-mise-a-jour.md` et `docs/reference/starter-et-depot.md` (comme `INSTALLATION.md`) ;
  - `choix-sujet.md` § 1 et § 4, `grilles.md`, `etapes.md` : une chaîne peut écarter le contrôle de concurrence dans `direction/ECARTS.md` (comme `strategist.md`) ;
  - `recit-retention.md` § 5 : la fiche d'ouverture estime le temps à la cible de 130 à 135 mots par minute, ou au débit mesuré de la voix de la chaîne (139 à 144 sur AA), non plus à 125 ;
  - `pieges.md` : pauses de révélation prévues dès le script (S26), sons de bibliothèque à mesurer, plusieurs copies de Claude Code sur le poste (S23).
- **Documentation** : `README.md`, `INSTALLATION.md`, `DEMARRAGE.md`, `docs/` (agents, outils et garde-fou, skill episode, son, workflows épisode, recherche, voix, sons, session et garde-fou, points ouverts).

## 0.5.1 (02/11/2026)
Rétention de sa propre chaîne par l'API, demandée par le propriétaire (« tu utilise youtube api pour voir les duree de retention pour chaque videp », 02/11/2026) pour l'analyse des ouvertures de l'E011 d'AA ; rangée dans le plugin à sa demande (décision Q22 de l'E011).
- **Outil `youtube_retention.py`** (`outils/recherche/`) : API YouTube Analytics v2 (`reports.query`) ; par vidéo : vues, durée moyenne, pourcentage regardé, courbe de 100 points (`audienceWatchRatio`, `relativeRetentionPerformance`), rétention à 0:30 et 1:00 interpolée. Bibliothèque standard seule. Accès OAuth « Application de bureau » (PKCE, retour sur 127.0.0.1), accordé par le propriétaire dans son navigateur ; client et jeton dans `~/.studio-faceless/youtube/`, hors de tout dépôt ; seul le jeton d'actualisation est gardé, jamais affiché. La chaîne est cherchée avant l'accord et demandée par son identifiant : un accord donné pour une autre chaîne est refusé par l'API. Essai hors ligne (19 contrôles) ; validé sur AA (9 longues, 18 requêtes, gratuit).
- **Documentation** : `outils/recherche/README.md` ; skill `youtube-seo` (`references/apres-publication.md` : source possible des bilans, à recouper une fois avec Studio) ; `DEMARRAGE.md` A6 et B6 (client OAuth, accord, 7 jours en mode Test).

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
