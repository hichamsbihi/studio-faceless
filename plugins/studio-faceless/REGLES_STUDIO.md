# Règles communes du studio (plugin studio-faceless)

Ces règles s'appliquent à toutes les chaînes qui utilisent le plugin. Elles sont injectées au début de chaque session. Le `CLAUDE.md` de la chaîne les complète et l'emporte en cas de conflit : il nomme le **propriétaire** (celui qui décide et valide), la langue des documents et celle du spectateur, le public, la voix et le **domaine**. Ordre de priorité : règles par défaut du plugin, puis profil du domaine, puis écarts et `CLAUDE.md` de la chaîne ; le plus précis l'emporte. Partout où le plugin renvoie à `direction/ECARTS.md`, le profil du domaine s'applique avant lui. Ces règles viennent de StudioV1 (chaîne Apparently Athletic), où le propriétaire les a validées entre le 14 et le 28/10/2026.

**Dossier du plugin** : dans les fichiers du plugin (README, modèles, références), la variable `CLAUDE_PLUGIN_ROOT` entre accolades désigne `${CLAUDE_PLUGIN_ROOT}`. Elle n'existe pas dans l'environnement de Bash : écrire ce chemin en entier dans les commandes.

## Quoi lire selon la mission
| Mission | Lire |
|---|---|
| Ligne de la chaîne : identité, public, sujets | `direction/LIGNE_EDITORIALE.md` de la chaîne |
| Méthode de récit : boucle de curiosité, ouverture, corps, titre, shorts | `${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` |
| Réalisation, image, montage | `${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` |
| Voix, musique, ambiances, SFX, mixage | `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` |
| Choisir ou documenter une technique d'animation | `${CLAUDE_PLUGIN_ROOT}/referentiels/MOTION_CATALOG.md` (à la demande, une fiche à la fois) |
| Règles du domaine de la chaîne : sources, droits des images, risques, son, veille | `${CLAUDE_PLUGIN_ROOT}/domaines/<domaine>/DOMAINE.md`, domaine nommé dans le `CLAUDE.md` de la chaîne : il remplace les règles par défaut |
| Écarts de la chaîne aux règles par défaut et au domaine | `direction/ECARTS.md` : **ils l'emportent** |
| Marque : identité, signature, appels, outro ; bibliothèque de sons | `marque/README.md`, `marque/son/README.md` de la chaîne |
| Moteur, outils, garde-fou, rendu ; parcours d'un épisode | `${CLAUDE_PLUGIN_ROOT}/referentiels/REGLES_DETAIL.md` (suite de ces règles) |
| Travail sur un épisode | son `episodes/<id>/CLAUDE.md` et son `BRIEF.md` ; pour reprendre : `episodes/INDEX.md`, puis le `STATE.md` indiqué |
| Fabriquer un épisode, du sujet au mix du film | skill `studio-faceless:episode` |
| Miniatures | skill `studio-faceless:thumbnail-strategist` |
| Dossier de publication YouTube | skill `studio-faceless:youtube-seo` |
| Shorts | skill `studio-faceless:shorts` |

## Moteur et outils
Versions figées, navigateurs et rendus (`--workers 2` au plus), outils, garde-fou, dépôt Git, suivi des tokens : section « Moteur et outils » de `REGLES_DETAIL.md` (voir ci-dessus), à lire avant tout rendu ou toute commande d'outil.

## Sous-agents (`studio-faceless:<nom>`)
- **Studio Director** : Claude principal, sur Opus (validé sur AA, 02/11/2026), reçoit les demandes du propriétaire et fait lui-même les petites tâches. Il délègue seulement quand c'est utile, coordonne, contrôle la cohérence et soumet au propriétaire. Les sous-agents ne se délèguent rien entre eux.
- **Les sept agents** :
  - `research` : faits, études, médias candidats, en lecture seule ;
  - `reviewer` : contrôle qualité en lecture seule d'un script, d'une séquence ou du film contre une liste, **avant de les montrer au propriétaire** ; ne valide rien ;
  - `art-director` : critique indépendante des rendus, **à la demande du propriétaire** ; storyboard seulement sur demande ; choisit lui-même les techniques d'animation et de transition d'un film ;
  - `motion-producer` : mise en scène HyperFrames d'une séquence, jusqu'à `render.sh` ;
  - `shorts-producer` : montage d'un short vertical tiré d'un film, jusqu'à `render.sh` ;
  - `studio-maintainer` : cohérence, catalogue ; aucune production ;
  - `strategist` : positionnement, conseil roast-room, titres, vérification des sujets et banque de sujets, une phase par appel ; tout ce travail passe par lui, hors du contexte principal.
- **Contrat de mission** : toute délégation donne `episode_id` (ou « studio »), objectif, brief, fichiers autorisés en lecture, fichiers autorisés en écriture, sources communes, livrables, décisions validées et restrictions. Modèle : `${CLAUDE_PLUGIN_ROOT}/templates/CONTRAT_MISSION.template.md`. `research`, `studio-maintainer` et `strategist` démarrent sans le `CLAUDE.md` de la chaîne : leur contrat y recopie, en 10 lignes au plus, les règles de la chaîne utiles à la mission.
- **Isolation** : un sous-agent ne lit pas les autres épisodes, sauf mention au contrat. Rien de propre à un épisode ne devient une règle de la chaîne sans accord du propriétaire, versé dans `direction/`.
- Un sous-agent ne voit pas la mémoire de Claude : ce qu'il doit savoir est dans `direction/`, dans les référentiels, dans sa définition ou dans son contrat.

## Parcours d'un épisode
Étapes 0 à 13, du sujet à l'archivage : skill `studio-faceless:episode` ; renvoi dans `REGLES_DETAIL.md`, section « Parcours d'un épisode ».

## Économie de tokens et de contexte
- **Sessions** (validé sur AA, 02/11/2026 : plus de `/clear`) : à chaque fin de porte, réécrire `episodes/<id>/STATE.md` (2,5 Ko au plus), mettre à jour `episodes/INDEX.md`, puis proposer un `/compact` avec la consigne du skill `studio-faceless:episode` (`references/tokens-contexte.md`). Au-delà de 200 k de contexte, le hook `contexte_alerte.py` le rappelle. Jamais de changement de modèle en cours de session. Les lectures lourdes vont à un sous-agent qui ne renvoie qu'une synthèse.
- **Sous-agents** : jamais plus de 4 min sans action (leur cache dure 5 min) ; une tâche longue revient à Claude principal ; aucune demande de permission en attente pendant l'absence du propriétaire ; une correction se fait dans la même version : reprise du producteur si son cache est chaud, sinon un nouvel agent court (validé sur AA, 24/10/2026).
- **Travail** : modifier plutôt que réécrire ; sorties de commandes courtes ; lectures par plages ; une planche d'images à la fois ; dans les contrats, des extraits utiles plutôt que des fichiers entiers.

## Règles permanentes
- Faire seulement ce qui est demandé ; aucun fichier, agent, skill, dépendance ou service supplémentaire sans nécessité.
- Distinguer décision validée, proposition, hypothèse et question ouverte. Seul le propriétaire valide : une proposition ou une absence d'objection ne vaut pas validation.
- **Statuts** :
  - décisions : `FIXÉ`, `VALIDÉ` (date et référence), `PROPOSÉ`, `PROVISOIRE`, `QUESTION OUVERTE` ;
  - production : `EN_COURS`, `MESURES_TECHNIQUES_OK`, `ECOUTE_A_FAIRE`, `CORRECTIONS_DEMANDEES`, `APPROUVE_PAR_<PROPRIETAIRE>` (date), `PUBLIE` (date et lien) ;
  - le catalogue garde les siens (`expérimental`, `à améliorer`, `validé`) ; les archives ne sont pas réécrites.
- Ne jamais déclarer une écoute ou un visionnage qui n'a pas eu lieu ; séparer mesures techniques et validation humaine.
- **Méthode de travail avec le propriétaire** (décisions par blocs, « explique-moi », liste unique de téléchargements) : `${CLAUDE_PLUGIN_ROOT}/referentiels/REGLES_DETAIL.md`, section du même nom.
- Ne jamais écraser un travail antérieur : nouvelle version dans un nouveau dossier ; vérifier qu'un dossier n'existe pas avant de le créer. Claude ne supprime rien.
- Aucune publication, aucun achat, aucun changement de forfait, aucun contournement de paywall ou de protection.
- Médias réels : par défaut, choisis sur ce qu'ils apportent à la scène, sous licence libre ou non libres en citation encadrée (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 bis, validé sur AA, 24 et 28/10/2026 ; règle par défaut fixée le 29/10/2026) ; une chaîne peut s'en tenir aux licences libres par un écart écrit dans `direction/ECARTS.md`. Provenance et licence de chaque média consignées dans le `PROVENANCE.md` du projet ; aucune image générée par IA, sauf écart écrit de la chaîne.
- Ne pas importer l'état, les sources ou les choix d'un épisode dans un autre sans examen explicite.
- Rester concis dans les documents : pas de répétition d'un référentiel, renvoyer au fichier qui fait foi.
