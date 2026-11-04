# Règles communes du studio : détail

Suite des règles communes du studio (`REGLES_STUDIO.md`), à lire selon la mission, avec la même autorité. Depuis la 1.1.0 (point 6 du conseil, validé sur AA, 04/11/2026), chaque règle n'a qu'une source : ce fichier porte le moteur, le parcours d'une vidéo, la table des décideurs, les arrêts et le rendu ; les valeurs chiffrées sont dans `seuils.json` (ici, on cite la clé) ; la priorité et le vocabulaire sont dans `REGLES_STUDIO.md`. Dans ce fichier comme dans les autres fichiers du plugin, `${CLAUDE_PLUGIN_ROOT}` désigne le dossier du plugin installé, dont le chemin est donné par les règles communes injectées au début de la session ; dans une commande Bash, écrire ce chemin en entier.

## Moteur et outils
- **HyperFrames 0.8.149**, figée dans le `package.json` de la chaîne. Aucune mise à jour (`upgrade`, `skills update`, `npm install` d'une autre version) sans décision du propriétaire.
- **Node 22 ou plus** est obligatoire. Sous Windows, passer par Git Bash (nvm, Node 22).
- **Skills plus récents que le CLI** : `hyperframes usage` et `hyperframes figma` n'existent pas en 0.8.149, donc ignorer les consignes qui les appellent ; `play` se remplace par `preview`. En cas de doute : `hyperframes <commande> --help`.
- **Navigateurs** : `check`, `snapshot`, `render` et `preview` lancent un Chrome sans fenêtre, un par processus de rendu. Rendre avec `--workers 2` au plus ; ne lancer `preview` que sur demande et l'arrêter juste après ; vérifier ensuite qu'aucun Chrome de HyperFrames ne reste ouvert.
- **Installations et envois cachés** (validé sur MM, 14/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ) : `remove-background` installe `onnxruntime-node` et télécharge un modèle de 168 Mo ; `catalog` télécharge et met en cache ; `init` rafraîchit les skills depuis GitHub (seule `HYPERFRAMES_SKIP_SKILLS=1` l'empêche, `--skip-skills` est ignoré) ; `tts`, `transcribe` et `models` téléchargent des modèles. Ces installations passent par Node : un garde sur Bash ne les voit pas, donc aucune sans l'accord du propriétaire, et les projets se créent à la main. `snapshot --describe` envoie les images à Gemini si `GEMINI_API_KEY` existe : toujours `--describe false`. Les scripts de media-use envoient de la télémétrie. Le gel de version tient parce que l'installation est locale : une installation globale ou `npx hyperframes@latest` déclencherait la mise à jour.
- **Poste de travail** (validé sur MM, 28/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ ; constaté sur le poste du propriétaire, commun à ses chaînes) : pas de carte graphique NVIDIA, donc les outils d'IA locaux qui reposent sur CUDA (voix, conversion de voix, gros modèles) ne tournent pas ou très lentement : le signaler avant d'en proposer un. Pillow installé le 03/11/2026 (VALIDÉ, Hicham) pour composer le masque de détourage des miniatures (`skills/thumbnail-strategist/references/fabrication.md` § 3) ; pour le reste, planches par `ffmpeg` (`tile`) et mesure de pixels par sortie `-f rawvideo -pix_fmt rgb24` lue par Python. Rien ne s'installe sans décision du propriétaire. L'heure d'un statut ou d'un journal se lit avec `date` avant d'être écrite : des statuts portaient des heures estimées, fausses.
- **Outils du plugin** : `${CLAUDE_PLUGIN_ROOT}/outils/`, lancés depuis le dossier de la chaîne (`python -B "<chemin>"`). Ils lisent leurs cibles dans `seuils.json` par `outils/seuils.py` (1.1.0). Contrôles : `outils/controle/` (mode d'emploi dans son `README.md`) :
  - `transcrire.py` : la prise contre le texte ;
  - `ralentir.py` : la narration ;
  - `controle.py` : niveau, planche, vibration, tremblement, son, couleurs, photos répétées, licences, voix / reste, Chrome ;
  - `mesurer_sons.py` : sons de bibliothèque avant emploi (format, niveau, crête vraie, boucle, parole).
- **Médias et voix** (0.6.0, validé sur AA, 02/11/2026) : `outils/medias/telecharger_medias.py` (liste validée : aperçu, puis `--executer`) et `outils/voix/generer_voix.py` (appel payant : coût annoncé, `--executer --confirme-credits N` après l'accord du propriétaire) ; modes d'emploi dans les `README.md` de leurs dossiers. Depuis la 0.7.0 (validé sur AA, 03/11/2026), `studio-faceless:sound-manager` prépare et chiffre l'appel, puis s'arrête ; Claude principal le lance après l'accord, comme le mix du film (`mix_film.py`, environ 6 min). Les clés (`ELEVENLABS_API_KEY`, `SOUNDZA_API_KEY`) restent dans l'environnement : Claude ne les lit, ne les écrit et ne les affiche jamais.
- **Garde-fou** (hook du plugin, `${CLAUDE_PLUGIN_ROOT}/hooks/garde_commandes.py`) :
  - pour tous, il refuse la publication, le cloud, la connexion, la mise à jour de HyperFrames ou des skills, l'installation npm, la suppression récursive ou définitive, le vidage de la corbeille et la modification du plugin installé ;
  - pour tous, depuis la 1.0.1 (validé sur AA, 04/11/2026) : Modal (sauf `modal run` d'un script du plugin, sur confirmation), `aws`, `sam`, `pip install`, l'affichage de l'environnement (`printenv`, `env` ou `set` seuls…), toute commande qui nomme une clé ou un jeton, et `claude -p` ;
  - il demande confirmation pour `preview`, et refuse un rendu sans `--workers 1` ou `2` ;
  - par rôle, reconnu au type d'agent : la table `ROLES` de `${CLAUDE_PLUGIN_ROOT}/hooks/garde_commandes.py` fait foi (rôles et limites de chaque agent) ; un sous-agent d'un type inconnu ou sans type reçoit le rôle `lecteur` (1.0.1 ; vérifié dans une session, 04/11/2026) ;
  - Les permissions (allow, deny, ask) sont dans le `.claude/settings.json` de la chaîne.
- **Archivage** : `${CLAUDE_PLUGIN_ROOT}/outils/archiver_episode.py`. Un aperçu d'abord ; `--executer` seulement avec l'accord du propriétaire.
- **Dépôt Git de la chaîne** : `verifier_depot.py` contrôle chaque commit (crochet `.githooks/pre-commit`). Claude fait les commits locaux et **ne pousse qu'avec l'accord du propriétaire, donné à chaque fois** ; il ne se connecte jamais au compte GitHub.
- **Cohérence du plugin** (1.1.0) : `outils/verifier_coherence.py`, bloquant dans le dépôt du plugin sur une base gelée qui ne peut que décroître ; dans une chaîne, il rapporte seulement (écarts « Remplace : <id> » orphelins, écarts qui visent une ligne D). Chaque contradiction corrigée y ajoute un motif interdit.
- **Suivi des tokens** à chaque fin d'étape : `python -B "${CLAUDE_PLUGIN_ROOT}/outils/suivi_tokens.py" --depuis AAAA-MM-JJ`.

## Parcours d'une vidéo
Décision du propriétaire, validé sur AA, 04/11/2026 (point 4, « Oui aux 11 ») ; le skill `studio-faceless:episode` en donne les étapes et fait foi pour leur détail.
- **Trois temps** :
  1. **Préparer**, sans question : la recherche ; l'angle et le script v1, passé par `script.py`, par le `reviewer` et par un tableau des affirmations (chaque chiffre et chaque nom liés à une source relue) ; la fiche de style (`art-director`, `STYLES.md`) ; la liste unique des médias et des sons (`medias.candidats_par_moment` candidats par moment, licence et dimensions vérifiées d'avance, exceptions en tête) ; la fiche son ; les titres et une idée de miniature ; les scripts et accroches des shorts ; le devis de la voix, la liste des noms propres et des chiffres, la fiche des droits.
  2. **Le socle** : une séance du propriétaire, après le script v1 relu et avant la première dépense irréversible, et son fichier `SOCLE.md` (`${CLAUDE_PLUGIN_ROOT}/templates/SOCLE.template.md`). Chaque bloc porte sa réponse recommandée ; le propriétaire répond « oui à tout » ou par numéros, et un bloc refusé fait recalculer les suivants dans la séance. La séance finit par l'appel de voix du film et des shorts, confirmé sur le devis ; le lexique de voix (chaque nom propre et chaque chiffre, `voix.lexique_s_min` à `voix.lexique_s_max` s) est coupé dans la vraie prise et écouté par le propriétaire avant le gel. La marge plafonnée accordée aux phrases que la transcription rejette vaut pour cette version du script, jusqu'au visionnage.
  3. **Fabriquer**, sans question : image, son, shorts et publication partent dès la voix figée ; la fabrication finit par un paquet au statut `ECOUTE_A_FAIRE`. Aucune étape n'écrit `APPROUVE_PAR_<PROPRIETAIRE>`.
- **Les cinq portes** (seul sens du mot : `REGLES_STUDIO.md` § Vocabulaire) :
  1. le sujet, choisi d'un mot dans `direction/BANQUE_SUJETS.md` de la chaîne ;
  2. le socle, lexique de voix compris ;
  3. l'épreuve, seulement si le film porte un style neuf : l'accroche, la signature et le début de S2 en image et en mix définitifs (`styles.epreuve_style_neuf_s` s), rendus avant les producteurs ; seule question permise en cours de ligne ;
  4. le visionnage du master et des shorts : les retours tiennent en une seule liste minutée, appliquée en un passage, et le propriétaire ne revoit que les passages changés ;
  5. la publication, avec la miniature et la case de déclaration.
- **Témoin par style**, hors épisode : vue une fois par le propriétaire au premier emploi d'un style (`STYLES.md`). Il n'y a plus de séquence témoin par épisode.
- **En route** : le directeur tranche les questions nées en route dans le cadre des accords (D07) et les inscrit au journal remis avec le master : situation, choix, règle appliquée, réversible ou non. Un choix irréversible n'entre jamais au journal : c'est un arrêt. Les contrôles chiffrés (`seuils.json`) écartent des défauts, ils ne valident rien ; les corrections se font sur place.
- **Le son pendant la ligne** : tant que `mesurer_mix.py` n'existe pas, une écoute de la bande radio (voix et musique, sans images), facultative et non bloquante, pendant que la piste image travaille ; sans écoute, le mix se reprend après le master, en un passage.
- **Le script** : le propriétaire le lit en entier au socle ; une lecture ciblée (ouverture, renversement, fin, note du `reviewer`) ne se décide qu'après le pilote.
- **Questions de chaîne** : méthode de recherche, règles des shorts, styles, licences, déclaration de contenu modifié se tranchent une fois dans `direction/` de la chaîne et sortent du socle.
- **À l'essai** veut dire qu'on peut revenir à l'étiquette Git précédente du plugin, pas que deux textes coexistent.

## Qui décide
Décision du propriétaire, validé sur AA, 04/11/2026 (option A du point 3 ; table du point 6). Une seule ligne par choix. « Décide » : celui qui choisit dans le cadre d'une porte ; seul le propriétaire accorde une porte. Chaque agent cite ses lignes dans sa définition ; un écart de chaîne qui vise une ligne D est signalé par `verifier_coherence.py`. Le catalogue, la bibliothèque lemo-opuscar et `hyperframes-animation` sont des sources, pas des décideurs.

| Ligne | Choix | Propose | Décide | Porte |
|---|---|---|---|---|
| D01 | sujet, titre | strategist | — | sujet ; socle, bloc 4 |
| D02 | style du film, technique de chaque temps fort | — | art-director | socle, bloc 6 (fiche de style) |
| D03 | détail d'exécution (durées, courbes, son) d'une séquence (`motion-producer`) ou d'un short (`shorts-producer`), dans le cadre de la fiche | — | producteur | — |
| D04 | changement de technique en route | — | aucun (arrêt n° 2) | socle |
| D05 | médias et sons | research, media-fetcher, sound-manager | — | socle, bloc 7 |
| D06 | cues, dans le cadre de la fiche son | — | sound-manager | socle, bloc 8 |
| D07 | questions nées en route, repli, voie de rendu (une par film), cohérence | — | directeur (au journal) | — |
| D08 | miniature | publisher | — | publication |

## Arrêts
Décision du propriétaire, validé sur AA, 04/11/2026 (point 4, questions 3 et 7) : une liste fermée, à l'essai sur l'E012, à la place de l'ancienne règle « une porte à chaque étape ». S'arrêter : écrire l'état, poser un seul paquet de questions, ne rien livrer de dégradé. Seule la piste en cause s'arrête ; les autres continuent.
1. un fait faux qui change une phrase dite ou qui contredit la promesse ;
2. une correction qui toucherait une décision du socle, ou un fichier hors de la liste accordée ;
3. le plafond de crédits ElevenLabs accordé au socle atteint ;
4. un contrôle qui échoue encore après `controles.corrections_sur_place_max` corrections sur place ;
5. le même défaut sur `controles.defaut_repete_sequences` séquences : c'est la recette qui est en cause ;
6. une personne réelle exposée, ou un refus du garde-fou ;
7. un choix irréversible ;
8. le plafond de dépense du paquet dépassé (alerte au journal, puis arrêt dur : valeurs dans `direction/seuils.json` de la chaîne).

**Repli** : permis seulement avec du matériel accordé (le second candidat, une carte, un dessin du kit) **et** une technique que la fiche de style prévoit pour ce genre de moment ; il est noté au journal. Sinon, la séquence s'arrête et sa question part dans le paquet (cas 2).

## Rendu
Décision du propriétaire, validé sur AA, 04/11/2026 (point 5, « Oui aux 12 »).
- **La file de nuit locale est la voie par défaut** : un rendu à la fois, en tâche suivie, par `bash "${CLAUDE_PLUGIN_ROOT}/outils/rendu/rendre_si_libre.sh" <render.sh> <journal>`, qui attend la fin des rendus des autres sessions. Aucun agent n'attend un rendu. Poste branché, sans mise en veille ; le lanceur de la file se décide avec le workflow `fabriquer` (1.2.0).
- **Modal sert au débordement, seulement après un essai réussi** (R1 à R3 en local d'abord, avant tout compte ; essai reporté le 04/11/2026) : une image figée par nos soins et notée par son empreinte (HyperFrames 0.8.149 par `npm ci`, Chrome et FFmpeg figés), un plafond de dépense dur, une app écrite dans le plugin (`outils/rendu/`) et lancée par `modal run` seulement, sans point d'entrée web ; jamais le gabarit de HeyGen. Le jeton se pose en variables utilisateur de Windows, jamais par `modal setup`. Si l'essai local en GL logiciel diffère du master à l'œil, aucune voie cloud n'est ouverte.
- **Règle de débordement**, à l'essai : au-delà de `rendu.debordement_nuit_h` heures prévues pour la nuit, ou une file non finie au matin, le reste part sur Modal ; recalée après deux semaines de nuits mesurées.
- **Une seule voie par film**, reprises comprises (D07).
- **Styles en WebGL** : la fiche de rendu de chaque style porté consigne un rendu local `--no-browser-gpu` de son témoin ; seuls ceux qui le passent vont au cloud.
- **Pas de Lambda pour l'instant** : seulement si Modal échoue sur un critère que Lambda ne partage pas, ou pour une pièce d'un seul tenant qui doit sortir en quelques minutes, et si le propriétaire accepte l'absence de plafond dur ; il resterait en 0.8.149. Pas de montée en 0.9.12 pour le rendu.

## Méthode de travail avec le propriétaire
- **Méthode de travail avec le propriétaire** (validé sur MM, 21/10/2026, bloc 8 de l'audit de son pilote ; proposé au plugin 0.3.0, PROPOSÉ) : une décision se présente par blocs, un à la fois (repris, changé, douteux, puis une recommandation) ; « explique-moi » ne modifie rien ; les téléchargements d'un lot tiennent en une liste unique (nom, source, taille) et un seul accord du propriétaire avant tout téléchargement (par Claude ou par `studio-faceless:media-fetcher`, validé sur AA, 02/11/2026 : `REFERENTIEL_QUALITE_REALISATION.md` § 2 bis ; les sons, aussi par `studio-faceless:sound-manager`, 0.7.0) ; un fichier hors de la liste attend un nouvel accord.

## Délégation aux agents
Décision du propriétaire, validé sur AA, 03/11/2026 (0.7.1) : la voix d'un short, faite par Claude principal, relevait de `sound-manager`.
- **Une tâche du périmètre d'un agent lui est confiée, même petite** : le son à `sound-manager` (voix et son des shorts compris), les miniatures et le dossier de publication à `publisher`, le montage d'une séquence ou d'un short à son producteur, les téléchargements de la liste validée à `media-fetcher`, la stratégie à `strategist`.
- Claude principal ne fait lui-même que les petites tâches hors de tout périmètre, et ce que le garde-fou lui réserve : appels payants, mix long, rendus, masters, scripts d'agent relus puis lancés.
- **Un refus du garde-fou ne se contourne pas.** Si le garde-fou refuse à un agent une tâche de son périmètre, Claude principal ne la fait pas à sa place sans l'accord du propriétaire. Il la lui signale, avec la correction du plugin à décider : zone, outil, ou texte qui se contredit.
