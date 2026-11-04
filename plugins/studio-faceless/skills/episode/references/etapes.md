# Les étapes en détail

Le parcours a trois temps (`REGLES_DETAIL.md` § Parcours, validé sur AA, 04/11/2026) : **préparer** (étapes 0 à 3, sans question après le choix du sujet), **le socle** (étape 4, une séance du propriétaire, puis la voix), **fabriquer** (étapes 5 à 10, sans question, jusqu'au master `ECOUTE_A_FAIRE`), puis le visionnage et la publication. Une question née en route se tranche dans le cadre des accords (D07, au journal) ou devient un arrêt (`REGLES_DETAIL.md` § Arrêts). Chaque étape finit par le `STATE.md` de l'épisode réécrit en entier (court : `seuils.json`), la ligne de l'épisode mise à jour dans `episodes/INDEX.md`, puis un `/compact` proposé au propriétaire (`tokens-contexte.md`). Après une coupure, la reprise lit seulement `INDEX.md` et ce `STATE.md`.

Les règles par défaut citées ici (`REFERENTIEL`, `DIRECTION_AUDIO`, `METHODE_RECIT`, `STYLES`) sont dans `${CLAUDE_PLUGIN_ROOT}/referentiels/` ; priorité : `REGLES_STUDIO.md` § Priorité.

## 0. Sujet (porte 1)
- **Entrée** : le propriétaire choisit d'un mot dans `direction/BANQUE_SUJETS.md` de la chaîne, dont les sujets et l'ordre sont déjà validés.
- **Banque vide** : les candidats viennent du registre (`direction/LIGNE_EDITORIALE.md`), de la veille et des bilans des épisodes publiés, notés selon `choix-sujet.md` ; la promesse en une phrase. Sujet qui surperforme ailleurs : `choix-sujet.md` § 4 (vidIQ seulement sur demande du propriétaire ; on reprend le principe, jamais la vidéo). Étude d'une chaîne de référence : skill `studio-faceless:regarder`. La banque se remplit par `strategist`.
- **Sortie** : `episodes/<id>/` créé depuis `${CLAUDE_PLUGIN_ROOT}/templates/` (`CLAUDE.episode`, `BRIEF.episode`, `STATE`) ; la ligne de l'épisode ajoutée à `episodes/INDEX.md` (créé depuis `INDEX.template.md` s'il n'existe pas) ; le sujet inscrit au registre.

## 1. Recherche
- **Méthode** : celle de la chaîne (`direction/`), tranchée une fois ; par défaut, l'éclaireur puis la vérification.
- **Éclaireur Perplexity** (validé sur AA, 02/11/2026, essai de son E011) : si la session a le serveur MCP `perplexity`, un agent général (`general-purpose`) par partie, limité par son contrat aux outils Perplexity, lance un `perplexity_research` (réglage `high`) et rend son rapport au directeur, qui l'écrit (un agent sans type est en lecture seule). Les parties partent ensemble, sans appels `perplexity_ask` en parallèle (erreurs 429). Rapports : `research/perplexity/R-*.md`, des pistes et des sources primaires, aucun fait vérifié (l'outil n'ouvre ni les pages ni les licences). Les appels sont payants : leur nombre suit la méthode de la chaîne. Sans serveur, on passe à `research` seul.
- **Vérification** : `studio-faceless:research`, une mission par grande partie (faits, précédents, médias), avec un contrat de mission qui lui donne le rapport de l'éclaireur. Il ouvre chaque source avant de retenir un fait et fait seul les médias (page du fichier, licence, empreinte). Les rapports vont dans `research/`.
- Médias candidats : la règle de `REFERENTIEL` § 2 bis s'applique (gratuits, sans filigrane, source notée, extraits de `medias.extrait_non_libre_s_max` s au plus ; vraies vidéos d'événements et fichiers tirés de YouTube permis, validé sur AA, 28/10/2026 ; compétitions et instances admises : `direction/ECARTS.md`). **Aucun téléchargement** avant le socle.
- Les points de vigilance de l'épisode (procédure en cours, personnes à protéger, chiffres de presse) vont dans son `CLAUDE.md`.

## 2. Angle et découpage
- La question d'une phrase, la promesse, les couches et leurs révélations, le renversement vers 75 %, les séquences et la question qui finit chacune (`recit-retention.md`).
- La signature de la chaîne vient après l'accroche (règle gardée) ; le raccord par défaut y est un noircissement en dégradé (`REFERENTIEL` § 2 ter).
- **Page de structure** (validé sur MM, 23/10/2026, bloc B de son audit stratégique ; place fixée par le point 4, validé sur AA, 04/11/2026) : la structure s'écrit en une page `script/STRUCTURE-vN.md` (question d'une phrase, promesse, couches et révélations, renversement, fin, séquences et durée de chacune) ; elle est lue au socle, bloc 1.
- Le rappel d'abonnement : sa place par défaut est vers 2:00, juste après l'ouverture d'une question (`METHODE_RECIT.md` § 1, validé sur AA, 26/10/2026) ; le socle la confirme (bloc 2).

## 3. Script v1, et le reste du temps « préparer »
- Narration dans la langue du spectateur, chaque phrase avec sa source. Fiche d'ouverture en tête : phrase, image prévue et temps estimé pour chaque repère de 0 à 2:00.
- Contrôles (`recit-retention.md` § 5) et `script.py` ; puis `studio-faceless:reviewer`, et le tableau des affirmations. Script ElevenLabs **sans balise** par défaut.
- Phrases d'actualité marquées [MAJ], à revoir la veille de la sortie. La narration évite d'abord tout ce qui dépend du jour de l'enregistrement (`METHODE_RECIT.md` § 6, evergreen).
- **En parallèle**, sans question : la fiche de style (`art-director`, `STYLES.md`) ; la liste unique des médias et des sons (`kit.md` § 4) ; la fiche son (palette, anti-palette, extraits par rôle) ; trois titres (`strategist`) et une idée de miniature ; les scripts et accroches des shorts (skill `studio-faceless:shorts`) ; le devis de la voix (`sound-manager`, passage à blanc), la liste des noms propres et des chiffres ; la fiche des droits.
- **Revérification des chiffres avant l'appel de voix** : chaque chiffre est contrôlé de nouveau sur son lien direct, avec sa date de valeur (`REFERENTIEL` § 2).

## 4. Socle et voix (porte 2)
- **La séance** : `SOCLE.md`, depuis `${CLAUDE_PLUGIN_ROOT}/templates/SOCLE.template.md` (dix blocs, une réponse recommandée chacun). Le propriétaire répond « oui à tout » ou par numéros ; un bloc refusé fait recalculer les suivants.
- **La voix, en fin de séance** (agent : `studio-faceless:sound-manager`, 0.7.0) : les prises se génèrent par l'API ElevenLabs (validé sur AA, 02/11/2026) avec `${CLAUDE_PLUGIN_ROOT}/outils/voix/generer_voix.py`. `sound-manager` l'a lancé à blanc avant le socle (découpage et coût) ; le propriétaire confirme le devis au bloc 9, et le directeur lance `--executer --confirme-credits N` (`DIRECTION_AUDIO.md` § 4), un seul appel pour le film et les shorts. Le propriétaire peut aussi fournir lui-même les prises.
- `sound-manager`, relancé, vérifie les prises (`${CLAUDE_PLUGIN_ROOT}/outils/controle/transcrire.py`) contre le texte accordé, les ralentit (`ralentir.py`), puis recale les repères mot à mot sur les vrais départs de la voix, après avoir coupé la bande sur ses silences. Les phrases rejetées se reprennent dans la marge accordée ; au-delà, c'est l'arrêt n° 3.
- **Lexique de voix** : coupé dans la vraie prise, écouté par le propriétaire avant le gel (porte 2). Les pauses de révélation sont mesurées sur les bandes avant de figer la voix (`pieges.md`, Son ; `voix.pause_revelation_s_min`).
- Bandes montage (silences S1…, pauses de respiration) dans `kit/voix/`.
- **La voix se fige ici.** Toute nouvelle prise après cette étape oblige à recaler toutes les séquences.

## 5. Kit
Voir `kit.md` : direction artistique, médias téléchargés et vérifiés, cartes, logos, sons, raccords, consignes communes, briefs.

## 5 bis. Maquette et test de décrochage (validé sur MM, 23/10/2026, bloc B de son audit stratégique ; adopté au plugin, VALIDÉ, Hicham, 04/11/2026)
- **Décision** : au socle (bloc 10) ; le propriétaire peut s'en passer pour un épisode.
- **Si oui** : la voix posée sur des cartes et des images sommaires, sans finition, un seul rendu ; le propriétaire note la première minute où il a envie de passer. On corrige la structure ou le script avant de lancer les producteurs.

## 6. Épreuve (porte 3, seulement si le film porte un style neuf)
- Un style s'essaie de préférence hors épisode, sur sa témoin (`STYLES.md` § Témoin par style). Il n'y a plus de séquence témoin par épisode.
- Si la fiche de style porte un style pas encore porté : l'accroche, la signature et le début de S2, en image et en mix définitifs (`styles.epreuve_style_neuf_s` s), rendus avant les producteurs, puis vus par le propriétaire. C'est la seule question permise en cours de ligne.

## 7. Production
Voir `production.md` : des lots de trois producteurs au plus, des raccords qui ne dépendent pas d'une séquence du même lot, et la vérification de chaque livrable. Corrections sur place, au plus `controles.corrections_sur_place_max` tours ; au-delà, l'arrêt n° 4.

## 8. Rendus
Voir `rendu-collage.md` § 1–2 et `REGLES_DETAIL.md` § Rendu : un rendu à la fois, en file suivie, puis les contrôles standard et la planche regardée. `studio-faceless:reviewer` peut contrôler une séquence sur les fichiers (minutage, plan, planche, mesures).

## 9. Collage en voix seule
Voir `rendu-collage.md` § 3 : assembleur commun, journal du master, jonctions mesurées et fondus courts.

## 10. Mix du film
Voir `rendu-collage.md` § 4. La fiche son accordée au socle (bloc 8) fixe le cadre : effets, niveaux par type, jonctions musicales, silences voulus ; `sound-manager` y décide les cues (D06). Tant que `mesurer_mix.py` n'existe pas, une écoute de la bande radio par le propriétaire, facultative et non bloquante, pendant que la piste image travaille (`REGLES_DETAIL.md` § Parcours).

Le mix fait : contrôle par `studio-faceless:reviewer`, puis le paquet au statut `ECOUTE_A_FAIRE`.

**Répartition** (0.7.0, validé sur AA, 03/11/2026) :
1. `studio-faceless:sound-manager` fait le repérage, le plan de cues, le choix et le téléchargement des sons de la liste accordée, puis le plan son. Méthode par défaut : `${CLAUDE_PLUGIN_ROOT}/skills/direction-sonore/references/musique-par-cues.md`. Il écrit la commande du mix et s'arrête.
2. Le directeur lance `mix_film.py` en tâche de fond (environ 6 min), puis relit et lance le script de mesure de `sound-manager` (l'agent ne lance pas ses scripts ; décision du 03/11/2026).
3. `sound-manager`, relancé, lit les mesures : écart voix − musique par cue, hausse des marques.

## 11. Visionnage du master et des shorts (porte 4)
- Les retours tiennent en une seule liste minutée, appliquée en un passage ; le propriétaire ne revoit que les passages changés.
- Une correction d'image se fait sur place dans la séquence, puis on la rend et on recolle.
- Une correction de son se fait par un remix, sans rendu : nouveau plan par `sound-manager`, remix lancé par le directeur, nouvelles mesures.
- Seul le propriétaire donne `APPROUVE_PAR_<PROPRIETAIRE>` ; aucune étape de la fabrication ne l'écrit.

## 12. Publication (porte 5)
- **Agent** (0.7.0, validé sur AA, 03/11/2026) : `studio-faceless:publisher`.
  - D'abord la miniature (`studio-faceless:thumbnail-strategist`, méthode en trois calques, au moins 2 variantes pour Test & Compare ; D08) ; l'agent s'arrête après l'écriture du script de masque, que le directeur relit et lance, avec le contrôle sur fond vert, avant de le relancer pour le rendu ;
  - puis le dossier YouTube (`studio-faceless:youtube-seo`), avec le titre accordé au socle (D01).
  - Le SRT se fait avec `${CLAUDE_PLUGIN_ROOT}/outils/montage/srt.py`, par `publisher` si son contrat le demande, sinon par le directeur.
- Le directeur reporte l'hypothèse du test au `JOURNAL_MINIATURES.md` et soumet au propriétaire : miniature, publication et case de déclaration.
- Avant la sortie, une passe d'actualité sur les phrases [MAJ].
- **Titre** (validé sur MM, 21/10/2026, audit de son pilote ; adopté au plugin, VALIDÉ, Hicham, 04/11/2026) : la concurrence se contrôle avant de le fixer, par une recherche YouTube des titres proches ; un titre trop proche d'une vidéo existante se change. Un titre changé tard donne une nouvelle version du dossier de publication (`PUBLICATION_vN+1`).
- **Miniature fournie par le propriétaire** (même validation) : Claude en note la source et la licence ; avec une seule miniature, il n'y a pas de Test & Compare.
- Claude ne publie jamais.

## 13. Après la sortie
- Bilans J+2, J+7 et J+28 (`studio-faceless:youtube-seo`) : rétention à 0:30, 1:00 et 2:00, et taux de clic au-delà d'environ 1 000 impressions. Un épisode écrit en essai (par exemple la méthode « Illusion of Novelty », `recit-retention.md` § 8) a en plus son bilan de J+7 selon le protocole de l'essai.
- **Relevé de la première minute** (validé sur MM, 23/10/2026 ; adopté au plugin, VALIDÉ, Hicham, 04/11/2026) : la rétention dans la première minute est relevée et comparée à celle des épisodes précédents.
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
