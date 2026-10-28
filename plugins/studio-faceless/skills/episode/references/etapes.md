# Les étapes en détail

Chaque étape commence par sa porte de questions (`grilles.md`) et finit par un état écrit dans le `CLAUDE.md` de l'épisode et une décision au `BRIEF.md`, avec son statut et sa date. Compacter le contexte à la fin de chaque grande étape (`tokens-contexte.md`).

Les règles par défaut citées ici (`REFERENTIEL`, `DIRECTION_AUDIO`, `METHODE_RECIT`) sont dans `${CLAUDE_PLUGIN_ROOT}/referentiels/`. Les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent sur ces règles.

## 0. Sujet
- **Entrées** : le registre (`direction/LIGNE_EDITORIALE.md`), la veille (`docs/veille/`) et les bilans des épisodes publiés.
- **Méthode** : 5 à 8 candidats, notés selon `choix-sujet.md`. Vérifier la saturation : la même question a-t-elle été un succès récent d'une grande chaîne ? Écrire la promesse en une phrase, et le titre en 60 caractères au plus.
- **Sujet qui surperforme ailleurs** : `choix-sujet.md` § 4 (vidIQ seulement sur demande du propriétaire ; on reprend le principe, jamais la vidéo). Étude d'une chaîne de référence : skill `studio-faceless:regarder`.
- **Sortie** : `episodes/<id>/` créé depuis `${CLAUDE_PLUGIN_ROOT}/templates/` (`CLAUDE.episode`, `BRIEF.episode`) ; le sujet inscrit au registre.

## 1. Recherche
- `studio-faceless:research`, une mission par grande partie (faits, précédents, médias), avec un contrat de mission. Les rapports vont dans `research/`.
- Médias candidats : la règle de `REFERENTIEL` § 2 bis s'applique (gratuits, sans filigrane, source notée, extraits de 6 s au plus ; vraies vidéos d'événements et fichiers tirés de YouTube permis, validé sur AA, 28/10/2026 ; compétitions et instances admises : `direction/ECARTS.md`). **Aucun téléchargement** à cette étape.
- Les points de vigilance de l'épisode (procédure en cours, personnes à protéger, chiffres de presse) vont dans son `CLAUDE.md`.

## 2. Angle et découpage
- La question d'une phrase, la promesse, les couches et leurs révélations, le renversement vers 75 %, les séquences et la question qui finit chacune (`recit-retention.md`).
- La signature de la chaîne vient après l'accroche (règle gardée).
- Le rappel d'abonnement : sa place se décide ici. C'est une `QUESTION OUVERTE` de la Méthode (étude AA), bloc 5.

## 3. Script
- Narration en anglais, chaque phrase avec sa source. Fiche d'ouverture en tête : phrase, image prévue et temps estimé pour chaque repère de 0 à 2:00.
- Contrôles avant la voix (`recit-retention.md` § 5). Script ElevenLabs **sans balise** par défaut.
- Phrases d'actualité marquées [MAJ], à revoir la veille de la sortie.

## 4. Voix
- Le propriétaire génère les prises. Claude les vérifie (`${CLAUDE_PLUGIN_ROOT}/outils/controle/transcrire.py`) contre le texte validé, les ralentit (`ralentir.py`) et recale les repères mot à mot sur les vrais départs de la voix.
- Bandes montage (silences S1…, pauses de respiration) dans `kit/voix/`.
- **La voix se fige ici.** Toute nouvelle prise après cette étape oblige à recaler toutes les séquences.

## 5. Socle
Voir `socle.md`. Le résultat, c'est le kit complet : direction artistique, médias vérifiés, cartes, logos, sons, raccords, consignes communes, briefs.

## 6. Séquence témoin
- Le choix se fait en porte : la séquence qui porte le plus de techniques nouvelles, ou la plus difficile, et qui ne dépend d'aucune autre séquence pour ses raccords.
- Elle passe par production, contrôles et rendu, puis le propriétaire la regarde.
- Ce qu'il dit devient la recette des autres séquences (consignes communes, version suivante). Exemple AA : sur l'E007, seq5 v3 a servi de témoin.

## 7. Production
Voir `production.md` : des lots de trois producteurs au plus, des raccords qui ne dépendent pas d'une séquence du même lot, et la vérification de chaque livrable. Corrections sur place.

## 8. Rendus
Voir `rendu-collage.md` § 1–2 : un rendu à la fois, en file suivie, puis les contrôles standard et la planche regardée.

## 9. Collage en voix seule
Voir `rendu-collage.md` § 3 : assembleur commun, journal du master, jonctions mesurées et fondus courts.

## 10. Mix du film
Voir `rendu-collage.md` § 4. La porte de questions fixe d'abord :
- les effets retenus ;
- les niveaux par type ;
- les jonctions musicales ;
- les silences voulus ;
- la place du rappel d'abonnement.

## 11. Retours du propriétaire
- Une correction d'image se fait sur place dans la séquence, puis on la rend et on recolle. Une correction de son se fait par un remix, sans rendu.
- Seul le propriétaire donne `APPROUVE_PAR_<PROPRIETAIRE>`.

## 12. Publication
- La miniature se fait avec `studio-faceless:thumbnail-strategist`, le dossier YouTube avec `studio-faceless:youtube-seo`, et le SRT avec `${CLAUDE_PLUGIN_ROOT}/outils/montage/srt.py`.
- Avant la sortie, une passe d'actualité sur les phrases [MAJ].
- Claude ne publie jamais.

## 13. Après la sortie
- Bilans J+2, J+7 et J+28 (`studio-faceless:youtube-seo`) : rétention à 0:30, 1:00 et 2:00, et taux de clic au-delà d'environ 1 000 impressions.
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
