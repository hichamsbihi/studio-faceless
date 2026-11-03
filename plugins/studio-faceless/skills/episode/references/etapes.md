# Les étapes en détail

Chaque étape commence par sa porte de questions (`grilles.md`) et finit par la décision au `BRIEF.md` (statut et date), le `STATE.md` de l'épisode réécrit en entier (2,5 Ko au plus), la ligne de l'épisode mise à jour dans `episodes/INDEX.md`, puis un `/compact` proposé au propriétaire (`tokens-contexte.md`). Après une coupure, la reprise lit seulement `INDEX.md` et ce `STATE.md`.

Les règles par défaut citées ici (`REFERENTIEL`, `DIRECTION_AUDIO`, `METHODE_RECIT`) sont dans `${CLAUDE_PLUGIN_ROOT}/referentiels/`. Les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent sur ces règles.

## 0. Sujet
- **Entrées** : le registre (`direction/LIGNE_EDITORIALE.md`), la veille (`docs/veille/`) et les bilans des épisodes publiés.
- **Méthode** : 5 à 8 candidats, notés selon `choix-sujet.md`. Vérifier la saturation, sauf écart de la chaîne dans `direction/ECARTS.md` : la même question a-t-elle été un succès récent d'une grande chaîne ? Écrire la promesse en une phrase, et le titre en 60 caractères au plus.
- **Sujet qui surperforme ailleurs** : `choix-sujet.md` § 4 (vidIQ seulement sur demande du propriétaire ; on reprend le principe, jamais la vidéo). Étude d'une chaîne de référence : skill `studio-faceless:regarder`.
- **Sortie** : `episodes/<id>/` créé depuis `${CLAUDE_PLUGIN_ROOT}/templates/` (`CLAUDE.episode`, `BRIEF.episode`, `STATE`) ; la ligne de l'épisode ajoutée à `episodes/INDEX.md` (créé depuis `INDEX.template.md` s'il n'existe pas) ; le sujet inscrit au registre.

## 1. Recherche
- **Éclaireur Perplexity** (validé sur AA, 02/11/2026, essai de son E011) : si la session a le serveur MCP `perplexity` (`DEMARRAGE.md`, B6), un agent général (`general-purpose`) par partie, limité par son contrat aux outils Perplexity et à l'écriture de son rapport, lance un `perplexity_research` (réglage `high`). Les parties partent ensemble, sans appels `perplexity_ask` en parallèle (erreurs 429). Rapports : `research/perplexity/R-*.md`, des pistes et des sources primaires, aucun fait vérifié (l'outil n'ouvre ni les pages ni les licences). Les appels sont payants : leur nombre se décide à la porte. Sans serveur, on passe à `research` seul, et la porte le dit.
- **Vérification** : `studio-faceless:research`, une mission par grande partie (faits, précédents, médias), avec un contrat de mission qui lui donne le rapport de l'éclaireur. Il ouvre chaque source avant de retenir un fait et fait seul les médias (page du fichier, licence, empreinte). Les rapports vont dans `research/`.
- Médias candidats : la règle de `REFERENTIEL` § 2 bis s'applique (gratuits, sans filigrane, source notée, extraits de 6 s au plus ; vraies vidéos d'événements et fichiers tirés de YouTube permis, validé sur AA, 28/10/2026 ; compétitions et instances admises : `direction/ECARTS.md`). **Aucun téléchargement** à cette étape.
- Les points de vigilance de l'épisode (procédure en cours, personnes à protéger, chiffres de presse) vont dans son `CLAUDE.md`.

## 2. Angle et découpage
- La question d'une phrase, la promesse, les couches et leurs révélations, le renversement vers 75 %, les séquences et la question qui finit chacune (`recit-retention.md`).
- La signature de la chaîne vient après l'accroche (règle gardée) ; le raccord par défaut y est un noircissement en dégradé (`REFERENTIEL` § 2 ter).
- **Page de structure** (validé sur MM, 23/10/2026, bloc B de son audit stratégique ; proposé au plugin 0.3.0, PROPOSÉ) : la structure s'écrit en une page `script/STRUCTURE-vN.md` (question d'une phrase, promesse, couches et révélations, renversement, fin, séquences et durée de chacune), validée par le propriétaire avant le script.
- Le rappel d'abonnement : sa place par défaut est vers 2:00, juste après l'ouverture d'une question (`METHODE_RECIT.md` § 1, validé sur AA, 26/10/2026) ; la porte la confirme ou l'écarte.

## 3. Script
- Narration en anglais, chaque phrase avec sa source. Fiche d'ouverture en tête : phrase, image prévue et temps estimé pour chaque repère de 0 à 2:00.
- Contrôles avant la voix (`recit-retention.md` § 5). Script ElevenLabs **sans balise** par défaut. Avant de montrer le script au propriétaire : contrôle par `studio-faceless:reviewer`.
- Phrases d'actualité marquées [MAJ], à revoir la veille de la sortie. La narration évite d'abord tout ce qui dépend du jour de l'enregistrement (`METHODE_RECIT.md` § 6, evergreen).
- **Revérification des chiffres la veille de la voix** : chaque chiffre est contrôlé de nouveau sur son lien direct, avec sa date de valeur (`REFERENTIEL` § 2) .

## 4. Voix
- **Agent** (0.7.0, validé sur AA, 03/11/2026) : `studio-faceless:sound-manager` fait cette étape ; Claude principal lance l'appel payant et soumet au propriétaire.
- **Les prises se génèrent par l'API ElevenLabs** (validé sur AA, 02/11/2026, Q35 de son E011) avec `${CLAUDE_PLUGIN_ROOT}/outils/voix/generer_voix.py` :
  - `sound-manager` le lance d'abord à blanc (découpage et coût annoncé), puis s'arrête ;
  - **après l'accord du propriétaire sur le coût**, Claude principal lance `--executer --confirme-credits N` (`DIRECTION_AUDIO.md` § 4) ;
  - le propriétaire peut aussi fournir lui-même les prises.
- `sound-manager`, relancé, vérifie les prises (`${CLAUDE_PLUGIN_ROOT}/outils/controle/transcrire.py`) contre le texte validé, puis les ralentit (`ralentir.py`). Enfin, il recale les repères mot à mot sur les vrais départs de la voix, après avoir coupé la bande sur ses silences.
- Les pauses de révélation sont prévues dès le script et mesurées sur les bandes avant de figer la voix (`pieges.md`, Son).
- Bandes montage (silences S1…, pauses de respiration) dans `kit/voix/`.
- **La voix se fige ici.** Toute nouvelle prise après cette étape oblige à recaler toutes les séquences.

## 5. Socle
Voir `socle.md`. Le résultat, c'est le kit complet : direction artistique, médias vérifiés, cartes, logos, sons, raccords, consignes communes, briefs.

## 5 bis. Maquette et test de décrochage (validé sur MM, 23/10/2026, bloc B de son audit stratégique ; proposé au plugin 0.3.0, PROPOSÉ)
- **Porte** : la faire ou non ; le propriétaire peut s'en passer pour un épisode.
- **Si oui** : la voix posée sur des cartes et des images sommaires, sans finition, un seul rendu ; le propriétaire note la première minute où il a envie de passer. On corrige la structure ou le script avant de lancer les producteurs.

## 6. Séquence témoin
- Le choix se fait en porte : la séquence qui porte le plus de techniques nouvelles, ou la plus difficile, et qui ne dépend d'aucune autre séquence pour ses raccords.
- Elle passe par production, contrôles et rendu, puis le propriétaire la regarde.
- Ce qu'il dit devient la recette des autres séquences (consignes communes, version suivante). Exemple AA : sur l'E007, seq5 v3 a servi de témoin.

## 7. Production
Voir `production.md` : des lots de trois producteurs au plus, des raccords qui ne dépendent pas d'une séquence du même lot, et la vérification de chaque livrable. Corrections sur place.

## 8. Rendus
Voir `rendu-collage.md` § 1–2 : un rendu à la fois, en file suivie, puis les contrôles standard et la planche regardée. Avant de montrer une séquence au propriétaire, `studio-faceless:reviewer` peut la contrôler sur les fichiers (minutage, plan, planche, mesures).

## 9. Collage en voix seule
Voir `rendu-collage.md` § 3 : assembleur commun, journal du master, jonctions mesurées et fondus courts.

## 10. Mix du film
Voir `rendu-collage.md` § 4. La porte de questions fixe d'abord :
- les effets retenus ;
- les niveaux par type ;
- les jonctions musicales ;
- les silences voulus ;
- la place du rappel d'abonnement.

Le mix fait, et avant de montrer le film au propriétaire : contrôle par `studio-faceless:reviewer`.

**Répartition** (0.7.0, validé sur AA, 03/11/2026) :
1. `studio-faceless:sound-manager` fait le repérage, le plan de cues, le choix et le téléchargement des sons de la liste validée, puis le plan son. Méthode par défaut : skill `studio-faceless:direction-sonore`, `references/musique-par-cues.md`, d'abord sur une séquence témoin en deux variantes. Il écrit la commande du mix et s'arrête.
2. Claude principal lance `mix_film.py` en tâche de fond (environ 6 min), puis relit et lance le script de mesure de `sound-manager` (l'agent ne lance pas ses scripts ; décision du 03/11/2026).
3. `sound-manager`, relancé, lit les mesures : écart voix − musique par cue, hausse des marques.

## 11. Retours du propriétaire
- Une correction d'image se fait sur place dans la séquence, puis on la rend et on recolle.
- Une correction de son se fait par un remix, sans rendu : nouveau plan par `sound-manager`, remix lancé par Claude principal, nouvelles mesures.
- Seul le propriétaire donne `APPROUVE_PAR_<PROPRIETAIRE>`.

## 12. Publication
- **Agent** (0.7.0, validé sur AA, 03/11/2026) : `studio-faceless:publisher`.
  - D'abord la miniature (`studio-faceless:thumbnail-strategist`, méthode en trois calques, au moins 2 variantes pour Test & Compare) ; l'agent s'arrête après l'écriture du script de masque, que Claude principal relit et lance, avec le contrôle sur fond vert, avant de le relancer pour le rendu ;
  - puis le dossier YouTube (`studio-faceless:youtube-seo`), avec le titre venu de `studio-faceless:strategist` et validé par le propriétaire.
  - Le SRT se fait avec `${CLAUDE_PLUGIN_ROOT}/outils/montage/srt.py`, par `publisher` si son contrat le demande, sinon par Claude principal.
- Claude principal reporte l'hypothèse du test au `JOURNAL_MINIATURES.md` et soumet au propriétaire.
- Avant la sortie, une passe d'actualité sur les phrases [MAJ].
- **Titre** (validé sur MM, 21/10/2026, audit de son pilote ; proposé au plugin 0.3.0, PROPOSÉ) : la concurrence se contrôle avant de le fixer, par une recherche YouTube des titres proches ; un titre trop proche d'une vidéo existante se change. Un titre changé tard donne une nouvelle version du dossier de publication (`PUBLICATION_vN+1`).
- **Miniature fournie par le propriétaire** (même validation) : Claude en note la source et la licence ; avec une seule miniature, il n'y a pas de Test & Compare.
- Claude ne publie jamais.

## 13. Après la sortie
- Bilans J+2, J+7 et J+28 (`studio-faceless:youtube-seo`) : rétention à 0:30, 1:00 et 2:00, et taux de clic au-delà d'environ 1 000 impressions. Un épisode écrit en essai (par exemple la méthode « Illusion of Novelty », `recit-retention.md` § 8) a en plus son bilan de J+7 selon le protocole de l'essai.
- **Relevé de la première minute** (validé sur MM, 23/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ) : la rétention dans la première minute est relevée et comparée à celle des épisodes précédents.
- Les leçons s'ajoutent à `pieges.md`, et les tokens par étape sont notés (`${CLAUDE_PLUGIN_ROOT}/outils/suivi_tokens.py`).
- L'archivage se fait avec l'accord du propriétaire (ci-dessous).

### Nettoyage et archivage (`VALIDÉ` sur AA, 28/10/2026, Q76 à Q82 de l'E009)
Sur demande du propriétaire, une fois le master approuvé, même avant la mise en ligne. D'abord l'aperçu de `${CLAUDE_PLUGIN_ROOT}/outils/archiver_episode.py`, puis `--executer` avec son accord. La corbeille est `_A_SUPPRIMER/<épisode>/` : Claude ne supprime rien, le propriétaire vide ce dossier.
- **Corbeille** (un `--essai` par chemin) :
  - les médias : `inputs/media`, `kit/media`, les copies `media/` des séquences, du gabarit et des miniatures, son des extraits compris ;
  - les voix : `inputs/voix` (prises), `kit/voix` (bandes et repères), les `pistes/` des séquences, les `.wav` intermédiaires de `outputs/` (`*.mix.wav`, `*.voix.wav`) ;
  - les séquences ratées et les essais : rendus refusés (`_rendu-N`), `_etude`, `_reperage`, `_gabarit-exemples`, `_essai-*`, `da-test-*` ;
  - les captures de contrôle : `planche-*`, `controle-planche`, `outputs/controle-*`, planches de contrôle des miniatures.
- **Zip** : les projets des séquences sans leurs médias et leurs rendus ; le master et le film en voix seule (seul moyen de refaire le son sans refaire l'image) ; `montage/` ; `research/` et les `PROVENANCE.md` (corrections promises dans le commentaire épinglé, réponse à une réclamation) ; le kit écrit (briefs, consignes, raccords) ; les miniatures et leur HTML.
- **SFX générés pour l'épisode** : versés dans `marque/son/` avant l'archivage, avec le préfixe de la chaîne et une ligne au README de la bibliothèque. Aucun si le mix n'a puisé que dans la bibliothèque (cas de l'E009 d'AA).
- **Hors du zip** : les fichiers de la racine (`BRIEF`, `CLAUDE`, `PUBLICATION`, SRT, `JOURNAL_MINIATURES`, script, narration…), pour le statut `PUBLIE` et les bilans.
- **Commande** : `--master` vers le master mixé, sinon l'outil peut prendre le film en voix seule de même version ; puis un `--essai` par chemin de la corbeille, car l'outil ne reconnaît seul ni `_etude`, ni `_rendu-N`, ni `planche-1`, ni `controle-planche`, ni les médias et les voix. La commande se note dans l'`ARCHIVE.md` de l'épisode (exemple AA : E009).
