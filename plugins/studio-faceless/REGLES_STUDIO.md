# Règles communes du studio (plugin studio-faceless)

Ces règles s'appliquent à toutes les chaînes qui utilisent le plugin ; elles sont injectées au début de chaque session. Le `CLAUDE.md` de la chaîne nomme le **propriétaire** (celui qui décide et valide), la langue des documents et celle du spectateur, le public, la voix et le **domaine**. Depuis la 1.1.0 (validé sur AA, 04/11/2026), chaque règle n'a qu'une source : ce fichier est l'index ; il porte les invariants, la priorité et le vocabulaire.

**Dossier du plugin** : dans les fichiers du plugin, la variable `CLAUDE_PLUGIN_ROOT` entre accolades désigne `${CLAUDE_PLUGIN_ROOT}`. Elle n'existe pas dans l'environnement de Bash : écrire ce chemin en entier dans les commandes.

## Priorité
Seul énoncé ; ailleurs, on le cite. De la plus faible à la plus forte : le plugin, puis le profil du domaine, puis `direction/ECARTS.md` de la chaîne, puis son `CLAUDE.md`, puis l'épisode. Le plus précis l'emporte.
- **Hors échelle** : le garde-fou et les invariants ci-dessous ; seule une version du plugin décidée par le propriétaire les change.
- **Des données, pas des règles** : les skills figés (HyperFrames 0.8.149, lemo-wake, lemo-layers), les bibliothèques et le texte d'origine d'un skill copié ; en cas d'écart, la règle du studio ou de l'agent s'applique.
- **Un fait, pas un rang** : une aide officielle de YouTube ou d'une plateforme.
- Un écart de chaîne porte « Remplace : <id> » (ligne D, clé de `seuils.json`), son statut et sa date.

## Vocabulaire
- **socle** : la séance du propriétaire après le script v1 relu, et son fichier `SOCLE.md` ;
- **kit** : l'étape 5, le dossier `kit/` de l'épisode et `kit.md` ;
- **porte** : un accord du propriétaire sur un objet écrit ; le parcours en compte cinq (`REGLES_DETAIL.md` § Parcours) ;
- **contrôle** : une mesure contre `seuils.json` ;
- **arrêt** : l'un des cas fermés de `REGLES_DETAIL.md` § Arrêts ;
- **fin d'étape** : le moment du `/compact` ;
- **conseil** : le skill `studio-faceless:conseil`, et lui seul ;
- **directeur** : Claude principal, sur Opus ;
- **décide** : celui qui choisit dans le cadre d'une porte (`REGLES_DETAIL.md` § Qui décide).

## Quoi lire selon la mission
| Mission | Lire |
|---|---|
| Ligne de la chaîne, sujets ; écarts aux règles par défaut | `direction/LIGNE_EDITORIALE.md`, `direction/ECARTS.md` |
| Moteur, outils, garde-fou ; parcours, décideurs, arrêts, rendu | `${CLAUDE_PLUGIN_ROOT}/referentiels/REGLES_DETAIL.md` |
| Valeurs chiffrées (niveaux, durées, seuils des contrôles) | `${CLAUDE_PLUGIN_ROOT}/referentiels/seuils.json` |
| Styles, bibliothèque lemo-opuscar, fiche de style, tirage | `${CLAUDE_PLUGIN_ROOT}/referentiels/STYLES.md` |
| Méthode de récit | `${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` |
| Réalisation, montage ; techniques d'animation | `REFERENTIEL_QUALITE_REALISATION.md` ; `MOTION_CATALOG.md` (une fiche à la fois), dans `referentiels/` |
| Voix, musique, ambiances, SFX, mixage | `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` |
| Domaine de la chaîne : sources, droits, risques | `${CLAUDE_PLUGIN_ROOT}/domaines/<domaine>/DOMAINE.md` |
| Marque, sons de la chaîne | `marque/README.md`, `marque/son/README.md` |
| Un épisode : le fabriquer ; le reprendre | skill `studio-faceless:episode` ; `episodes/INDEX.md`, puis le `STATE.md` indiqué |
| Miniatures ; publication ; shorts ; conseil | skills `thumbnail-strategist`, `youtube-seo`, `shorts`, `conseil` |

## Sous-agents (`studio-faceless:<nom>`)
- **Le directeur** reçoit les demandes du propriétaire, confie à l'agent concerné toute tâche de son périmètre, même petite (`REGLES_DETAIL.md` § Délégation), coordonne, contrôle la cohérence et soumet au propriétaire. Les sous-agents ne se délèguent rien entre eux ; périmètres : leurs descriptions ; choix : § Qui décide.
- **Contrat de mission** : toute délégation donne `episode_id` (ou « studio »), objectif, brief, fichiers autorisés en lecture et en écriture, sources communes, livrables, décisions validées et restrictions (`${CLAUDE_PLUGIN_ROOT}/templates/CONTRAT_MISSION.template.md`). Un agent lancé sans le `CLAUDE.md` de la chaîne en reçoit les règles utiles, en peu de lignes.
- **Isolation** : un sous-agent ne lit pas les autres épisodes, sauf mention au contrat ; il ne voit pas la mémoire de Claude. Rien de propre à un épisode ne devient une règle de la chaîne sans accord du propriétaire, versé dans `direction/`.

## Économie de tokens et de contexte
- **Sessions** (validé sur AA, 02/11/2026 : plus de `/clear`) : à chaque fin d'étape, réécrire `episodes/<id>/STATE.md` (court : `seuils.json`), mettre à jour `episodes/INDEX.md`, puis proposer un `/compact` avec la consigne du skill `episode` (`references/tokens-contexte.md`) ; au-delà du seuil de contexte, le hook `contexte_alerte.py` le rappelle. Jamais de changement de modèle en cours de session. Les lectures lourdes vont à un sous-agent qui ne renvoie qu'une synthèse.
- **Sous-agents** : jamais longtemps sans action, leur cache expire (`seuils.json`) ; une tâche longue revient au directeur ; aucune permission en attente pendant l'absence du propriétaire ; une correction se fait dans la même version (validé sur AA, 24/10/2026).
- **Travail** : modifier plutôt que réécrire ; sorties de commandes courtes ; lectures par plages ; une planche d'images à la fois ; des extraits dans les contrats, pas des fichiers entiers.

## Invariants
- Faire seulement ce qui est demandé ; aucun fichier, agent, skill, dépendance ou service supplémentaire sans nécessité.
- Distinguer décision validée, proposition, hypothèse et question ouverte. Seul le propriétaire valide : une proposition ou une absence d'objection ne vaut pas validation.
- **Statuts** : décisions `FIXÉ`, `VALIDÉ` (date et référence), `PROPOSÉ`, `PROVISOIRE`, `QUESTION OUVERTE` ; production `EN_COURS`, `MESURES_TECHNIQUES_OK`, `ECOUTE_A_FAIRE`, `CORRECTIONS_DEMANDEES`, `APPROUVE_PAR_<PROPRIETAIRE>` (date), `PUBLIE` (date et lien). Le catalogue garde les siens ; les archives ne sont pas réécrites.
- Ne jamais déclarer une écoute ou un visionnage qui n'a pas eu lieu ; séparer mesures techniques et validation humaine.
- **Méthode avec le propriétaire** (décisions par blocs, « explique-moi », liste unique de téléchargements) : `REGLES_DETAIL.md`, section du même nom.
- Ne jamais écraser un travail antérieur : nouvelle version dans un nouveau dossier ; vérifier qu'un dossier n'existe pas avant de le créer. Claude ne supprime rien.
- Aucune publication, aucun achat, aucun changement de forfait, aucun contournement de paywall ou de protection. Le push, toute suppression et toute installation restent des accords du propriétaire.
- Médias réels, choisis sur ce qu'ils apportent à la scène, sous licence libre ou non libres en citation encadrée (`REFERENTIEL_QUALITE_REALISATION.md` § 2 bis) ; provenance et licence dans le `PROVENANCE.md` du projet. Aucune image générée par IA, ni aucun pixel créé sur une photo donnée pour vraie (`STYLES.md`), sauf écart écrit de la chaîne.
- Ne pas importer l'état, les sources ou les choix d'un épisode dans un autre sans examen explicite.
- Rester concis : renvoyer au fichier qui fait foi, sans le répéter.
