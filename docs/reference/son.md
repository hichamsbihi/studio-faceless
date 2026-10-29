# Référence : le son (direction sonore, voix off, collage et mix)

Cette fiche décrit, fichier par fichier, tout ce que le plugin contient pour le son : le skill `direction-sonore`, le référentiel `DIRECTION_AUDIO.md`, les outils de montage (`assembler.py`, `mix_film.py`, `srt.py`) et les deux outils de la voix off (`transcrire.py`, `ralentir.py`). Les fichiers du plugin font foi : en cas d'écart, la fiche se corrige.

## Table des matières
- [Comment lire cette fiche](#comment-lire-cette-fiche)
- [Le skill `direction-sonore`](#le-skill-direction-sonore)
- [Le référentiel `DIRECTION_AUDIO.md`](#le-référentiel-direction_audiomd)
- [Les outils de montage](#les-outils-de-montage)
- [Les outils de la voix off](#les-outils-de-la-voix-off)
- [Points à vérifier relevés à la lecture](#points-à-vérifier-relevés-à-la-lecture)

## Comment lire cette fiche
- **Chemins** : tous relatifs au plugin (`plugins/studio-faceless/`). Chaque fiche donne un lien cliquable vers le fichier.
- **Commandes** : elles se lancent depuis la racine de la chaîne, avec `python -I -B`. `${CLAUDE_PLUGIN_ROOT}` est le dossier du plugin installé ; cette variable **n'existe pas dans Bash**, il faut donc écrire le chemin complet dans la commande ([`../ARCHITECTURE.md`](../ARCHITECTURE.md), § Chemins).
- **Dossier de travail des outils** : `CLAUDE_PROJECT_DIR` s'il est défini, sinon le dossier courant. Les chemins relatifs des fichiers de configuration partent de là.
- **Dépendances Python** : `numpy` et `scipy` ([`starter/requirements.txt`](../../plugins/studio-faceless/starter/requirements.txt)). FFmpeg et FFprobe viennent de `HYPERFRAMES_FFMPEG_PATH` / `HYPERFRAMES_FFPROBE_PATH`, sinon du `PATH`, sinon de l'installation WinGet de Gyan.
- **Garantie commune** : aucun de ces outils n'écrase une sortie existante.
- **Statuts** : `VALIDÉ`, `PROPOSÉ`… sont ceux de [`REGLES_STUDIO.md`](../../plugins/studio-faceless/REGLES_STUDIO.md). Les décisions citées sont celles de la chaîne d'origine (Apparently Athletic, « AA »), reprises comme règles par défaut ; les écarts d'une chaîne (`direction/ECARTS.md`) l'emportent.
- **Parcours** : pour savoir dans quel ordre on s'en sert, voir [`../workflows/voix-off.md`](../workflows/voix-off.md), [`../workflows/sons.md`](../workflows/sons.md) et [`../workflows/collage-et-mix.md`](../workflows/collage-et-mix.md).

---

## Le skill `direction-sonore`

Sept fichiers dans [`skills/direction-sonore/`](../../plugins/studio-faceless/skills/direction-sonore/) : le point d'entrée, la page des licences, et cinq références lues à la demande.

### skills/direction-sonore/SKILL.md
Fichier : [`SKILL.md`](../../plugins/studio-faceless/skills/direction-sonore/SKILL.md)

- **Rôle** : méthode pour décider *ce que le son doit faire* dans un documentaire de la chaîne, puis le vérifier sur le fichier livré. Il complète `DIRECTION_AUDIO.md` (règles) et le skill `hyperframes-audio` (mécanique HyperFrames) sans les remplacer.
- **Quand il sert** : le Studio Director (Claude principal) le charge pour préparer ou revoir le son d'une séquence, d'un prototype ou d'un épisode, et pour préparer la note de contrôle d'un MP4. Les agents `motion-producer` et `shorts-producer` le chargent « si le brief ne suffit pas » ; `art-director` quand le son est concerné (outil Skill, aucun préchargement). Étapes de l'épisode : socle (choix des sons, relevé musical), mix du film (porte 10), contrôle du master.
- **Contenu** :
  - *Ordre de préséance* : 0, écarts de la chaîne (`direction/ECARTS.md`) ; 1, `DIRECTION_AUDIO.md` (il fait foi, ses chiffres ne se recopient pas) ; 2, `hyperframes-audio` (valeurs d'automation **absolues**, elles remplacent `data-volume`) ; 3, ce skill ; 4, `media-use` n'est pas une source de sons (provenance et registre inadaptés).
  - *Quand l'utiliser* : préparer le son, revoir un mix, diagnostiquer un défaut. **Jamais pour générer** : toute génération passe par les règles de dépense et l'accord du propriétaire.
  - *Méthode en sept étapes* : contrat audio, repérage avant tout son, couches et perspective, relations son-image et transitions, musique, mise en œuvre HyperFrames, contrôle du MP4 puis passes d'écoute. Chaque étape renvoie à une référence.
  - *Refus permanents* (validés sur AA) : whoosh à chaque raccord, riser, impact ou sting de bande-annonce, musique décorative, battement de cœur ; foule en fond continu ; acouphène ou effet tunnel prêtés à une personne réelle ; voix, pas ou souffle d'une personne réelle fabriqués comme captés ; ambiance contextuelle ou son généré présentés comme le son de l'événement ; carve fréquentiel par défaut ; musique « à la manière de » ; nouvelle recherche musicale sans demande.
  - *Livrables types* : contrat audio et feuille de repérage, registre des sons (dans `PROVENANCE.md`), journal de cues si musique, note de contrôle audio.
- **Liens** : cite `DIRECTION_AUDIO.md`, `references/*.md` et `SOURCES_ET_LICENCES.md`. Cité par `agents/motion-producer.md`, `agents/shorts-producer.md`, `agents/art-director.md` et `skills/soundtrack/SKILL.md`.
- **À savoir** :
  - Le ducking doux de la musique (3 à 5 dB sous la voix) est la règle ; le carve fréquentiel ne vient qu'après un masquage constaté.
  - Depuis le 24/10/2026 les séquences ne portent que la voix et le mix se fait sur le film collé. L'étape 6 du skill (« mise en œuvre dans HyperFrames ») décrit surtout l'ancien mix dans la composition ; le skill précise désormais que ces techniques s'appliquent au mix du film (`DIRECTION_AUDIO.md` § 3, `mix_film.py`), pas dans la composition de la séquence. Reste à voir : [Points à vérifier](#points-à-vérifier-relevés-à-la-lecture).

### skills/direction-sonore/SOURCES_ET_LICENCES.md
Fichier : [`SOURCES_ET_LICENCES.md`](../../plugins/studio-faceless/skills/direction-sonore/SOURCES_ET_LICENCES.md)

- **Rôle** : garder les notices de copyright et d'autorisation (licence MIT) des œuvres dont le skill reformule des méthodes.
- **Quand il sert** : jamais pendant une production. Il se lit pour vérifier la provenance du skill ou avant de redistribuer le plugin.
- **Contenu** :
  - trois œuvres adaptées, avec le texte MIT complet : `calesthio/generative-media-skills` (feuille de repérage, perspective, registre de provenance, relations son-image, journal de cues, contrat audio), `JosiahSiegel/claude-plugin-marketplace` (filtres de mesure FFmpeg `ebur128=peak=true`, `astats`), `guia-matthieu/clawfu-skills` (hiérarchie des couches, « loi des deux et demi » de Murch) ;
  - une source **écartée** : `snowfrost/skill-movie`, sans licence au 14/10/2026, rien n'en est repris ;
  - les références de fond citées mais non relues (ITU-R BS.1770, EBU R 128, essai de Murch, documentation des filtres FFmpeg) ;
  - « ce qui vient de la chaîne d'origine » : décisions, cibles, interdits et constats HyperFrames viennent de `DIRECTION_AUDIO.md` et de l'audit du Motion Lab (étude AA, 14/10/2026).
- **Liens** : cité par `SKILL.md` (dernière ligne).
- **À savoir** : le skill a été rédigé sur AA le 14/10/2026 (option B : une méthode propre plutôt que l'installation de skills tiers). Les notices MIT sont une obligation de la licence : ne pas les retirer.

### skills/direction-sonore/references/gabarits.md
Fichier : [`gabarits.md`](../../plugins/studio-faceless/skills/direction-sonore/references/gabarits.md)

- **Rôle** : cinq gabarits à copier pour documenter le son. Une case sans objet vaut « aucun » ; une information inconnue s'écrit « inconnu / à vérifier », jamais une valeur supposée.
- **Quand il sert** : le Studio Director les remplit au moment du repérage sonore et du contrôle du master.
- **Contenu** :
  - *Contrat audio* : séquence et version, rôle du son (une phrase), hiérarchie d'écoute, voix (prise approuvée, transcription comparée), sources et statut, musique, livrables, cible (renvoi à `DIRECTION_AUDIO.md` § 3), écoute réellement disponible, risques ;
  - *Feuille de repérage* : tableau à 11 colonnes (n°, temps, déclencheur, famille, statut narratif, synchro, perspective, matière, fonction, source et statut, priorité) avec deux lignes d'exemple ;
  - *Registre des sons* (dans `PROVENANCE.md`) : fichier, description, type de source, auteur, licence et lien, attribution exigée, lieu et date réels, modifications, statut documentaire, vérifié le, retenu ou provisoire ;
  - *Journal de cues* (si musique) : cue (M01…), titre, source, auteur, entrée, sortie, durée, fonction, points de synchro, sortie prévue, droits, fichier exact ;
  - *Note de contrôle audio* : fichier contrôlé et statut, **mesures** (format, loudness, repli mono, crêtes, silences, voix contre reste), **écoute** (passes, passages à risque, constats), limites.
- **Liens** : cité par `SKILL.md` (étape 1) et par les trois autres références.
- **À savoir** : le gabarit parle du « dossier de la séquence ». Depuis que les séquences ne portent que la voix, le contrat audio et le journal de cues d'un film concernent le mix du film ; aucun fichier ne dit où les ranger (à vérifier, voir [Points à vérifier](#points-à-vérifier-relevés-à-la-lecture)).

### skills/direction-sonore/references/reperage-et-couches.md
Fichier : [`reperage-et-couches.md`](../../plugins/studio-faceless/skills/direction-sonore/references/reperage-et-couches.md)

- **Rôle** : méthode du repérage sonore (*spotting*), des familles de sons, de la densité des couches et de la perspective.
- **Quand il sert** : avant de choisir des sons ; au moment de lire les tableaux d'effets des producteurs pour écrire le plan son.
- **Contenu** :
  1. *Repérage* : on part de l'image et de la voix approuvée, jamais d'une banque de sons. Dix champs par ligne (temps, déclencheur, famille, statut narratif, synchro, perspective, matière, fonction, source et statut, priorité). Trois questions par son important : qu'est-ce qui le produit, où est-il par rapport au point d'écoute, qu'apporte-t-il au récit (sans réponse à la troisième, on l'enlève). Le son d'une action se cale sur le **contact visible**.
  2. *Familles* : voix off, son d'archive, ambiance et room tone, bruitage motivé (deux ou trois appuis valent mieux qu'un son par geste), effet éditorial (rare, sec, pas de whoosh de transition), musique, foules (sur l'image qui les justifie, jamais en fond continu), silence.
  3. *Densité* : loi des deux et demi de Murch ; deux ou trois couches sous une narration ; une ou deux pour une transition ; hiérarchie de repli voix, sons-clés, musique, ambiances.
  4. *Perspective* : proche, moyenne, lointaine, occultée, avec les moyens possibles. Ces traitements valent pour ambiances et effets, **jamais pour la voix off** ni une parole d'archive. Une perspective « subjective » n'est permise que dans une scène fictive ou reconstituée déclarée.
  5. *Matières* : aide-mémoire (exemple AA, football : gazon, béton, tribune métallique, filet, cuir).
- **Liens** : renvoie à `gabarits.md`, `transitions-et-silences.md` § 4, `musique-a-l-image.md` et `DIRECTION_AUDIO.md` § 2-3.
- **À savoir** : « un événement réel sans son d'archive autorisé reste silencieux ou porté par une ambiance déclarée contextuelle ». Une foule proche fait apparaître des voix : vérifier qu'aucun mot, nom propre ou chant identifiable n'est audible si la source ne l'autorise pas.

### skills/direction-sonore/references/transitions-et-silences.md
Fichier : [`transitions-et-silences.md`](../../plugins/studio-faceless/skills/direction-sonore/references/transitions-et-silences.md)

- **Rôle** : choisir la relation entre le son et l'image à chaque moment, et traiter silences et raccords.
- **Quand il sert** : au repérage des transitions et au réglage des départs de musique et d'effets dans le plan son.
- **Contenu** :
  1. *Relations son-image* : synchrone, anticipation (J-cut), traîne (L-cut), pont, révélation par retrait, substitution, contradiction (à manier rarement). On synchronise sur les phrases et les changements d'idée, pas sur chaque coupe. Un pont ne fabrique pas une continuité fausse.
  2. *J-cut, L-cut, ponts* : méthode et exemples ; décalage habituel de quelques images à une ou deux secondes, calé sur une respiration de la prise, **jamais en déplaçant ou en coupant un mot**.
  3. *Silence et quasi-silence* : à préférer au zéro numérique ; un silence voulu figure à la feuille de repérage avec sa raison ; une respiration sans musique après un moment fort.
  4. *Mise en œuvre dans HyperFrames 0.8.149* : constats tirés de la lecture du code du 14/10/2026 (pas d'attribut J/L, pas de panoramique ni de spatialisation, ce qui est automatisable ou non, premier point d'automation au temps 0, mix refusé ou piste supprimée sans message).
- **Liens** : `controle-et-mesure.md` (mesurer le MP4), `DIRECTION_AUDIO.md` § 2.
- **À savoir** : le § 4 vient d'une **lecture du code sans test de rendu** : « les vérifier sur le MP4 au premier usage ». Il concerne un mix fait *dans* la composition, ce qui n'est plus le parcours normal : la référence précise désormais que ses techniques s'appliquent au mix du film (`DIRECTION_AUDIO.md` § 3, `mix_film.py`), pas dans la composition de la séquence (reste à voir : [Points à vérifier](#points-à-vérifier-relevés-à-la-lecture)).

### skills/direction-sonore/references/musique-a-l-image.md
Fichier : [`musique-a-l-image.md`](../../plugins/studio-faceless/skills/direction-sonore/references/musique-a-l-image.md)

- **Rôle** : placer la musique comme porteuse d'immersion (décision du 15/10/2026, validée sur AA) : la question n'est plus « faut-il de la musique ? » mais « quelle musique pour cette situation ? » (ouverture, tension ou rivalité, analyse et science, émotion et fin).
- **Quand il sert** : au relevé musical du socle, puis au choix des entrées, sorties et silences du plan son.
- **Contenu** :
  1. *Fonctions possibles* (soutenir l'immersion, organiser la progression, marquer un contraste…) et ce qu'elle ne fait jamais (dire quoi penser d'une personne réelle, gonfler une affirmation contestée, remplacer une preuve) ;
  2. *Repérage musical* : identifiant stable par cue (M01…), entrée et sortie sur un **changement d'histoire**, zones sans musique, points de synchro peu nombreux ;
  3. *Architecture d'un cue* : de l'état de départ à la sortie (résoudre avant une phrase, couper net sur un silence, tenue-pont, ambiance qui prend le relais, harmonie non résolue) ;
  4. *Musique et voix* : pas de mélodie principale dans la bande 1-4 kHz ; réduire d'abord l'arrangement, puis le gain ;
  5. *Sources et droits* : aucune nouvelle recherche musicale sans demande ; jamais « comme » un artiste ou un morceau connu ; journal de cues sans donnée inventée ;
  6. *Diagnostic rapide* : tableau symptôme, cause, correction (kitsch, lutte avec la voix, boucle qui claque, droits flous…).
- **Liens** : `gabarits.md` (journal de cues), `DIRECTION_AUDIO.md` § 1-3.
- **À savoir** : le § 5 renvoie à `DIRECTION_AUDIO.md` § 4 pour le connecteur ElevenLabs (connecteur de base sans musique, connecteur complet avec Eleven Music, accord du propriétaire). Suno, Udio et équivalents restent exclus sans décision du propriétaire.

### skills/direction-sonore/references/controle-et-mesure.md
Fichier : [`controle-et-mesure.md`](../../plugins/studio-faceless/skills/direction-sonore/references/controle-et-mesure.md)

- **Rôle** : contrôler **le MP4 exporté** (jamais la composition ni un intermédiaire), d'abord par des mesures, ensuite par des passes d'écoute.
- **Quand il sert** : après le mix du film, pour préparer la note de contrôle ; en diagnostic quand un défaut est signalé.
- **Contenu** :
  1. *Mesures FFmpeg* (testées le 14/10/2026 sur FFmpeg 9.0.2, à lancer dans Git Bash, toujours `-f null -`, aucune sortie écrite) : format et durées ; loudness intégrée, LRA et crête vraie (`ebur128=peak=true`) ; repli mono (`pan=mono|c0=0.5*c0+0.5*c1`) ; crêtes et niveaux par canal (`astats`) ; trous et silences numériques (`silencedetect=noise=-60dB:d=0.4`) ; voix contre reste dans la bande 1-4 kHz (sur deux sources séparées, même fenêtre) ; mesure de contrôle de `loudnorm` sans normaliser ;
  2. *Passes d'écoute* (jugement humain) : image seule, son seul sur écran noir, texte seul, complet puis mono et petit haut-parleur ;
  3. *Diagnostic par symptôme* : voix masquée, son en avance ou en retard, ambiance qui boucle, trou de room tone, mix fatigant, échelle fausse, crête trop haute, droits flous ;
  4. *Note de contrôle* : renvoi au gabarit de `gabarits.md`.
- **Liens** : `DIRECTION_AUDIO.md` § 3 et § 5 (seuils) ; l'outil `outils/controle/controle.py` (`niveau`, `son`, `voix-reste`) fait une partie de ces mesures.
- **À savoir** :
  - **Un agent ne peut pas écouter** : il prépare la note, signale les passages à risque horodatés et laisse le statut à `ECOUTE_A_FAIRE`. Seul le propriétaire pose `APPROUVE_PAR_<PROPRIETAIRE>`.
  - Les valeurs de `loudnorm=I=-16:TP=-1.5` reprennent les cibles de `DIRECTION_AUDIO.md` § 3 : si elles changent là-bas, les changer ici.
  - Sans sources séparées (voix, reste), la mesure voix/reste s'écrit « non mesuré », jamais une valeur estimée.

---

## Le référentiel `DIRECTION_AUDIO.md`

### referentiels/DIRECTION_AUDIO.md
Fichier : [`DIRECTION_AUDIO.md`](../../plugins/studio-faceless/referentiels/DIRECTION_AUDIO.md)

- **Rôle** : règles **par défaut** du plugin pour la voix, la musique, les ambiances, les effets, le mixage, la livraison et le contrôle du son. Le fichier le dit en tête : les écarts de la chaîne (`direction/ECARTS.md`) l'emportent, et les pratiques propres à un épisode vont dans le `CLAUDE.md` de l'épisode.
- **Quand il sert** : injecté dans le travail de tout agent ou skill qui touche au son (voir la table « Quoi lire » de [`REGLES_STUDIO.md`](../../plugins/studio-faceless/REGLES_STUDIO.md)). Le Studio Director s'en sert à chaque étape voix, socle, mix du film et contrôle ; le skill `direction-sonore` s'y réfère pour tout chiffre.
- **Statut** : les contraintes reçues du propriétaire sont des décisions ; les choix artistiques et les chiffres sont des recommandations « à éprouver ». **Aucun mixage n'est validé par ce document.**

#### § 1. Décisions et contraintes
Tableau de sept sujets :

| Sujet | Ce que dit la ligne |
|---|---|
| Voix | Propre à la chaîne (voix retenue, prises, statut) : `direction/ECARTS.md`. |
| Prise approuvée | Ne jamais régénérer, réécrire, accélérer ni couper une prise sans autorisation explicite. **Seule exception** (validée sur AA, 15/10/2026) : toute narration est ralentie « juste un peu » (méthode du § 2). **Les shorts n'y sont pas soumis** (19/10/2026) : script dédié, prise à vitesse d'origine, pauses resserrées, une prise par short, version YouTube = même prise sans le bloc D. Son des shorts plus fort que celui des films (valeurs `PROPOSÉ` : musique dès 0,0 s, environ 8 LU sous la voix, master à −14 LUFS, crête vraie ≤ −1 dBTP après un limiteur passé par Claude). Effets des shorts : un effet court (< 0,4 s) par événement visuel, 12 à 18 dB sous la voix, un riser au plus, environ 0,3 s de silence avant le fait clé. |
| Immersion | L'immersion totale est la ligne directrice du son (slogan d'AA, 15/10/2026). |
| Méthode | **Musique d'abord** ; effets et foules seulement si l'image les justifie ; jamais deux fois le même traitement sur un master. |
| Essais musique | Propres à la chaîne (`direction/ECARTS.md`). |
| Choix des sons | Le propriétaire choisit lui-même les variantes générées ; ne pas superposer une musique non demandée. |
| Dépenses | Aucune génération ni dépense hors du budget explicitement autorisé par la mission ; aucun achat. |

#### § 2. Principes
- *Rôle des couches* : la voix conduit, les ambiances installent les lieux, la musique organise la progression, les effets ponctuent, les silences laissent place à la découverte. Une seule couche peut suffire.
- *Narration* : la prise approuvée est la base temporelle ; proche, centrée, peu ou pas de réverbération ; on corrige un défaut identifié, pas un timbre.
- *Ralentissement de toute narration* (validé sur AA, 15/10/2026, réglage mis à jour le 26/10/2026) : voix seule traitée, voix jouées intactes. (1) Tempo × 0,97 par `atempo` (c'était × 0,94 jusqu'à l'E008 v1) ; le débit global est mesuré et noté à chaque épisode, il vise 130 à 135 mots par minute. (2) Pauses internes allongées : +0,15 s pour une pause de 0,36 à 0,60 s, +0,25 s au-delà, par un silence au plancher placé au point le plus calme, **jamais** par recopie du début de la pause (correctif du 17/10/2026). (3) Gain unique vers −19 LUFS en mesure mono (−16 LUFS en double mono dans un MP4 stéréo), crête vraie ≤ −2 dBTP. Script : `outils/controle/ralentir.py`.
- *Chaîne voix* (méthode de l'E003 d'AA) : (1) script en anglais, chaque phrase vérifiée avec sa source ; **aucune balise par défaut** (validé le 23/10/2026), une balise d'émotion (`[calm]`, `[thoughtful]`, `[serious]`, `[softly]`) seulement pour un passage qui l'exige, **jamais de balise de pause ni de vitesse** (`[pause]`, `[slowly]`…) ; (2) le propriétaire génère la prise ; (3) transcription locale et comparaison mot à mot, un doublon suspect se vérifie sur le passage isolé ; (4) ralentissement ; (5) livraison aux producteurs de la bande, des mots horodatés et des phrases.
- *Images au rythme de la voix* : renvoi à `REFERENTIEL_QUALITE_REALISATION.md` § 2 ter.
- *Vérification de la prise* : toute narration fournie est transcrite mot à mot avant le découpage et comparée au brief ; tout écart est signalé au propriétaire tout de suite, en tête du compte rendu.
- *Voix générées* (citation, dialogue reconstitué) : toujours déclarées à l'écran.
- *Musique* (révisée le 15/10/2026) : elle porte l'immersion et s'entend vraiment (environ 12 à 15 LU sous la voix, ducking doux de 3 à 5 dB, remontée dans les pauses). **Avant une révélation** (26/10/2026) : pause de voix de 0,5 à 1 s au plus, seulement sur une image réelle ; la musique **baisse en creux** (environ 8 dB, rampes de 0,8 s, clé `creux` de `mix_film.py`) sans se couper. Une séquence qui suit la signature démarre sur une musique d'ouverture, jamais sur des voix de foule.
- *Ambiances et effets* : seulement si l'image les justifie, au moment exact, puis ils s'arrêtent. Foules jamais en fond continu. **Son des extraits vidéo** (E008 d'AA, nuance du 28/10/2026) : le vrai son passe sous la voix, après transcription (filtre `whisper`) ; s'il porte un commentaire, on ne l'emploie pas et une ambiance de `marque/son/` le remplace (description : « Crowd sounds are illustrative »). Effets d'appareil seulement pendant le mouvement qui les motive. Pas de whoosh à chaque raccord, pas de bip par chiffre. **Ponctuation des changements** (26/10/2026) : impact grave à chaque changement de bloc (quelques-uns par film), whoosh seulement si un élément traverse le cadre, son de matière sur un volet de matière ; niveaux du § 3. Statut toujours noté (archive exacte, enregistrement contextuel, génération illustrative). Jamais la voix, les pas ou la respiration d'une personne réelle fabriqués comme captés.
- *Raccords* : J-cut et L-cut ; jamais déplacer ni rogner un mot pour tomber sur un temps musical.

#### § 3. Mixage et livraison
- *Mix du film à la fin, sur le film collé* (validé sur AA, 24/10/2026) :
  - les séquences ne portent que la voix ; chaque producteur liste ses **effets proposés** dans son README (code, instant local, image qui le justifie, facultatif) ;
  - le film se colle d'abord en voix seule (signature, rappel d'abonnement et écran de fin compris), avec son journal (`<nom>-voix.log.txt`) ;
  - puis **un seul mix** : relevé musical par morceau, musique qui peut continuer d'une séquence à l'autre, effets à niveaux fixes par type, baisse sous la voix active, **un seul gain final** vers −16 LUFS et limiteur à −2,0 dBTP, image copiée telle quelle ;
  - une correction de son se refait par un **remix**, sans nouveau rendu d'image ; Claude n'écoute pas, le film reste `ECOUTE_A_FAIRE` ;
  - niveaux de départ par type, en LU sous la voix (à calibrer à la première écoute) : musique 13, ambiance 16, impact 14, souffle 18, montée 16, papier ou déclic 20 ; le gain final exclut signature et outro ; l'écart de voix entre séquences est mesuré, sans égalisation ;
  - *fin du film en douceur* (validé le 28/10/2026) : dernière séquence fondue en 1,2 s dans 4 s de noir, outro entrant en 0,5 s, morceau de fin calé pour que son accord s'éteigne sur le noir, aucune coupe sèche.
- *Bibliothèque de sons* (`marque/son/`, validé le 24/10/2026) : un épisode puise d'abord ; un nouvel appel ElevenLabs seulement à la demande du propriétaire, puis le son approuvé rejoint la bibliothèque.
- *Familles séparées* : voix, musique, ambiances, effets. *En cas de concurrence* : réduire ou déplacer la couche secondaire, revoir son arrangement, automatiser son gain, et corriger une fréquence seulement si le masquage est établi.
- *Ducking* de 3 à 5 dB sous la voix ; carve fréquentiel seulement si nécessaire.
- *Cibles de travail* : 48 kHz, AAC-LC stéréo, **environ −16 LUFS** (plage −17 à −15), **crête vraie ≤ −1,5 dBTP**, mesurées sur le MP4 livré décodé. Écouter aussi en mono et sur petit haut-parleur.
- *HyperFrames 0.8.149 (constaté)* : médias pilotés par `data-start`, `data-duration`, `data-media-start`, `data-volume`, `data-automation` ; un identifiant unique par audio, aucune double lecture ; AAC fixé à 192 kbit/s ; le moteur abaisse le mix pour rester sous −1 dBTP (régler les gains à la source) ; `carve.mjs` exige un paquet absent (nouvelle dépendance, à décider par le propriétaire), alternative éprouvée : automation de volume écrite à la main, mesurée sur le MP4.
- *Transcription locale* (constaté en octobre 2026) : le FFmpeg installé contient le filtre `whisper` ; il lui faut un modèle `ggml` (par exemple `ggml-base.en.bin`, MIT, 148 Mo) gardé hors du projet, téléchargé avec l'accord du propriétaire ; découper par silences, `max_len=1` donne les mots à ±0,1 s ; chemins relatifs depuis le dossier du modèle (les « : » des lecteurs Windows cassent le filtre) ; échecs connus : l'alignement DTW sur la voix Zira, Scribe d'ElevenLabs (le propriétaire doit envoyer le fichier lui-même).

#### § 4. ElevenLabs
- Deux connecteurs possibles : le **connecteur de base** (voix et effets, **pas de musique**) et le **connecteur complet** (ajoute la musique, Eleven Music v2.5, 3 à 600 s, instrumental possible). Vérifier celui de la session avant de promettre une musique.
- Coûts constatés sur AA : effets environ 3,3 crédits par seconde ; musique environ 27,5 crédits par seconde et par variante (20/10/2026). L'estimation affichée dépasse largement la facturation (35 crédits facturés pour 115,5 estimés) : la lire sans en faire un budget.
- Brief d'un son : action ou matière, proximité, énergie, durée, sec ou réverbéré, début et fin, exclusions, rôle dans la scène ; éléments générés séparément. Une génération par nœud (deux si le propriétaire doit choisir), prompt de 450 caractères au plus, liens de téléchargement valables 2 h.
- Un « clic » généré contient souvent plusieurs attaques : mesurer les transitoires, garder une paire appui/relâchement calée sur l'image de contact.
- Musique : puiser d'abord dans `marque/son/`. Avec le connecteur complet, montrer l'estimation et attendre l'accord. *Solution éprouvée sur AA* (15/10/2026, rechoisie le 20/10/2026, Eleven Music jugé trop cher) : nappes en boucle par le modèle d'effets (`loop: true`, 30 s, 2 variantes) ; le Studio Director garde la variante au raccord de boucle propre (écart d'énergie début/fin ≤ 1,5 dB) et la moins chargée entre 1 et 4 kHz, et nomme l'autre.
- **Garde-fou** : chaque appel au connecteur passe par une règle `ask` du `.claude/settings.json` de la chaîne, sinon accord demandé en conversation avant chaque lot (lots de 20 nœuds au plus). **Aucun sous-agent n'appelle le connecteur** : le Studio Director génère, télécharge et consigne prompts, identifiants, empreintes et crédits.
- Les sons générés sont des illustrations : prompt, identifiant, crédits et licence de l'abonnement vont dans `PROVENANCE.md`.

#### § 5. Contrôles
- *Techniques* (MP4 livré) : pistes, durée, décodage ; calage et gain de la voix, aucun mot coupé ; LUFS, crête vraie, écrêtage ; écart voix/reste de 1 à 4 kHz ; queues de sons, pas de double lecture ; chaque effet et foule sur l'image qui le justifie ; musique au niveau visé.
- *Perceptuels* (le propriétaire, ou un outil qui écoute réellement) : intelligibilité, naturel, raccords et boucles, utilité de chaque couche, confort au casque, en mono et sur petit haut-parleur.
- Une transcription, une forme d'onde ou une mesure ne valident pas une écoute. Outils prêts : `transcrire.py`, `ralentir.py`, `controle.py niveau | voix-reste | tout`.

#### Sources
Huit références consultées le 12/10/2026 : S1 iZotope (superviseur son de *Crip Camp*), S2 iZotope (masquage fréquentiel), S3 Adobe (J et L cuts), S4 FFmpeg `loudnorm`, S5 Adobe (ducking automatique), S6 YouTube (paramètres d'encodage), S7 ElevenLabs (guide des effets), S8 HeyGen (skill `hyperframes-audio`).

- **Liens** : cité par presque tous les fichiers du son ; renvoie à `REFERENTIEL_QUALITE_REALISATION.md` § 2 ter, au skill `episode` (`rendu-collage.md`), à `outils/montage/mix_film.py` (clé `creux`) et aux outils de `outils/controle/`.
- **À savoir** :
  - La cellule « Prise approuvée » du § 1 mêle la règle des films et celle des shorts : lire les deux avant de s'en servir pour un short.
  - Le § 3 contient deux niveaux de plafond qui ne se contredisent pas : la **cible de livraison** est ≤ −1,5 dBTP (mesurée sur le MP4 livré), le **limiteur du mix** travaille à −2,0 dBTP.
  - La règle de dépense (§ 1) et le garde-fou (§ 4) s'ajoutent : aucune génération hors du budget autorisé par la mission, et chaque appel au connecteur passe par un accord du propriétaire.

---

## Les outils de montage

Dossier [`outils/montage/`](../../plugins/studio-faceless/outils/montage/) : un README et trois scripts, tirés de l'E007 d'AA (24/10/2026). Parcours en trois temps : coller (`assembler.py --voix-seule`), mixer (`mix_film.py`), sous-titrer (`srt.py`). Mode d'emploi pas à pas : [`../workflows/collage-et-mix.md`](../workflows/collage-et-mix.md).

### outils/montage/README.md
Fichier : [`README.md`](../../plugins/studio-faceless/outils/montage/README.md)

- **Rôle** : mode d'emploi des trois outils et **schéma officiel** des deux fichiers JSON qu'ils lisent (`montage.json`, `plan-son.json`).
- **Quand il sert** : le Studio Director le lit avant le collage (étape 9 de l'épisode) et avant le mix (étape 10) ; c'est lui qui fait foi pour les noms de clés.
- **Contenu** :
  - tableau des trois outils et de leur rôle ;
  - *Parcours* : les quatre commandes dans l'ordre (film « voix », essai `--son-seul`, master mixé, SRT) ;
  - *`montage.json`* : exemple commenté (épisode, titre, séquences, `marque`, `outro`, `fondus`, `sortie`) ;
  - *`plan-son.json`* : exemple (racine, baisse sous la voix, niveaux par type, silences, musiques, effets, titre, sortie) et les règles de chaque clé, dont les **creux** (ajoutés le 25/10/2026) et les silences voulus ;
  - *Mesures* : la voix est la référence, comment les gains de musique et d'effets sont calculés, gain final unique, contrôles du MP4 mixé ;
  - *Limites* : format fixe, mémoire, effets très courts, pas d'égalisation, etc.
- **Liens** : cite `DIRECTION_AUDIO.md` § 3. Cité par `skills/episode/references/rendu-collage.md` (§ 3 à 5) et par les docstrings des trois scripts.
- **À savoir** :
  - Toujours `python -I -B`, depuis la racine de la chaîne. Aucun outil n'écrase une sortie.
  - `--son-seul` (sur `assembler.py` et `mix_film.py`) mesure et affiche le journal **sans rien écrire**.
  - `assembler.py` sans `--voix-seule` garde le comportement du master E007 v1 d'AA (pistes mixées des séquences) : mode d'archive, pas le parcours actuel.
  - Les essais cités (E007 d'AA : film « voix » de 15 655 images, mix à −16,1 LUFS et −1,9 dBTP, collage 22 min, mix 6,5 min) sont des mesures d'AA, pas des garanties pour une autre chaîne.
  - Les valeurs de `niveaux_par_type` de l'exemple ne sont pas les niveaux de départ de `DIRECTION_AUDIO.md` § 3 (voir [Points à vérifier](#points-à-vérifier-relevés-à-la-lecture)).

### outils/montage/assembler.py
Fichier : [`assembler.py`](../../plugins/studio-faceless/outils/montage/assembler.py)

- **Rôle** : coller les MP4 des séquences, des noirs, la signature et l'outro de la chaîne, avec des fondus enchaînés, en un seul film 1920 × 1080 à 30 i/s. Écrit le MP4, son WAV, le **journal du collage** (`.log.txt`, `<nom>-voix.log.txt` en voix seule : c'est lui que lisent les chapitres et le SRT) et les segments à l'image près (`.journal.json`). Le mode `--voix-seule` prépare le mix du film.
- **Quand il sert** : Studio Director, étape 9 de l'épisode, quand toutes les séquences sont validées (une fois, puis à chaque correction d'image).
- **Usage** :
  ```bash
  python -I -B "${CLAUDE_PLUGIN_ROOT}/outils/montage/assembler.py" --episode <id> --voix-seule
  python -I -B "${CLAUDE_PLUGIN_ROOT}/outils/montage/assembler.py" CONFIG.json [--voix-seule] [--son-seul] [--sans-limiteur] [--nom NOM.mp4] [--out DOSSIER]
  ```
  | Option | Effet |
  |---|---|
  | `CONFIG` (positionnel, facultatif) | Chemin d'un `montage.json`. Sans lui, `--episode` est obligatoire. |
  | `--episode ID` | Lit `episodes/<ID>/montage/montage.json`. |
  | `--voix-seule` | Son = voix seules des séquences (`pistes/stem-voix.wav`) et son propre des pièces de marque ; **aucun gain** ; limiteur seulement si une crête dépasse −2,0 dBTP. Sorties : `NOM.voix.wav`. |
  | (défaut, sans `--voix-seule`) | Son = pistes mixées des séquences (clé `mix` obligatoire) ; gain unique vers −16 LUFS sur les séquences ; limiteur à −2,0 dBTP. Sortie : `NOM.mix.wav`. Comportement du master E007 v1 d'AA. |
  | `--son-seul` | Mesure le son et le limiteur, **n'écrit rien**. |
  | `--sans-limiteur` | Pas de limiteur. En mode mixé : gain unique plafonné par la crête vraie ; en voix seule : aucun limiteur. |
  | `--nom NOM.mp4` | Nom du MP4 (doit finir par `.mp4`). Défaut : en voix seule, `sortie.nom_voix`, à défaut `sortie.nom` suivi de `-voix` ; sans `--voix-seule`, `sortie.nom`. |
  | `--out DOSSIER` | Dossier de sortie (défaut : `sortie.dossier`). |
- **Configuration lue (`montage.json`)** — chemins relatifs à la racine de la chaîne ; `mp4`, `voix` et `mix` sont relatifs au `dossier` de la séquence :

  | Clé | Contenu |
  |---|---|
  | `episode`, `sequences`, `sortie` | **Obligatoires** (sinon arrêt). |
  | `titre` | Étiquette `title` du MP4 (défaut : `episode`) ; « — voix seule » est ajouté en mode voix seule. |
  | `sequences[]` | `id` (unique ; `noir` réservé), `dossier`, `mp4` ; facultatifs : `voix` (défaut `pistes/stem-voix.wav`), `mix` (exigé hors `--voix-seule`). |
  | `marque[]` | Pièces posées **après** une séquence : `apres` (id d'une séquence), `fichier`, `id` (défaut `marque` : à nommer si plusieurs), `noir_avant`, `noir_apres` (secondes). |
  | `outro` | `fichier`, `id` (défaut `outro`), `noir_avant` (secondes). Placé à la fin. |
  | `fondus` | `"A>B": images` entre deux segments qui se suivent (`noir` s'écrit aussi : `"seq9>noir"`, `"noir>outro"`). Un fondu entre deux segments qui ne se suivent pas arrête l'outil. |
  | `sortie` | `dossier`, `nom` (et `nom_voix` facultatif). |
- **Étapes internes** : (1) charge la configuration et refuse les identifiants doublons ; (2) vérifie que chaque entrée existe et que chaque MP4 est en 1920 × 1080, 30 i/s ; (3) calcule le début de chaque segment à l'image près (les fondus sont soustraits) ; (4) lit les voix, **atténue de 20 dB les clics isolés** de la voix (deux passes), cale chaque piste sur la durée d'image ; (5) pour chaque fondu, la fin du segment sortant s'efface en cosinus sous le début du segment entrant, qui garde son niveau ; (6) mesure (sonie, crête vraie) ; (7) en mode mixé, calcule un gain unique vers −16 LUFS et passe le limiteur (jusqu'à trois recalages) ; (8) écrit le WAV 24 bits, encode l'image en une seule fois (`libx264 slow`, CRF 16, BT.709, AAC 320 kbit/s 48 kHz, `faststart`) ; (9) contrôle le MP4 (décodage complet, nombre d'images, sonie, crête) ; (10) écrit journal et segments.
- **Fichiers écrits** : `NOM.mp4`, `NOM.voix.wav` (ou `NOM.mix.wav`), `NOM.log.txt`, `NOM.journal.json` (champs : épisode, titre, mode, configuration, fps, sr, images, son, et par segment `id`, `type`, `debut_image`, `images`, `fondu_images`, `fichier`). Le dossier de sortie est créé au besoin.
- **Journal (`.log.txt`)** : une ligne par segment (`seq1    0.00 s → 45.30 s (1359 images)`), puis le détail du son (clics atténués, fondus), les mesures et la ligne `Contrôles du MP4 : OK` ou `ÉCART : …`. Ce format est celui que lisent `mix_film.py`, `srt.py` et `controle/publication.py`.
- **Codes de sortie** : 0 en cas de succès **même si la ligne « Contrôles du MP4 » annonce un ÉCART** (lire le journal) ; 1 à tout arrêt (`sys.exit` avec message : sortie existante, entrée manquante, format inattendu, configuration incomplète…, ou échec FFmpeg) ; 2 pour une erreur d'arguments.
- **Dépendances** : `numpy`, `scipy` (`minimum_filter1d`, `resample_poly`), FFmpeg et FFprobe. Variables : `CLAUDE_PROJECT_DIR` (racine de la chaîne, sinon dossier courant), `HYPERFRAMES_FFMPEG_PATH`, `HYPERFRAMES_FFPROBE_PATH`, `LOCALAPPDATA` (recherche de l'installation WinGet).
- **Liens** : schéma dans `outils/montage/README.md` ; consommé par `mix_film.py` (via son journal et son WAV) et `srt.py` ; `controle/publication.py` lit son `.log.txt` pour les chapitres.
- **À savoir** :
  - Gros calcul : 22 minutes pour 15 655 images (E007 d'AA), environ 2 à 3 Go de mémoire. À lancer en tâche suivie, pas en avant-plan court.
  - Les identifiants de séquences doivent avoir la forme `seqN` : `srt.py` les associe aux titres `## seqN` du script, et `mix_film.py` ne reconnaît les séquences que par ce motif quand il retombe sur le journal texte (le `.journal.json` donne le type directement).
  - En voix seule, la sonie du film « voix » est **relevée mais pas contrôlée** (environ −17 LUFS à l'E007 d'AA).
  - Le limiteur est un limiteur de crêtes vraies approchées (quatre phases suréchantillonnées, anticipation de 5 ms, retour linéaire de 25 dB/s).
  - Le fichier `.log.txt` d'un film **voix** et celui d'un master **mixé** ont deux contenus différents : seul le premier porte les lignes de segments (`outils/montage/README.md` le dit : `--journal <nom>-voix.log.txt`).

### outils/montage/mix_film.py
Fichier : [`mix_film.py`](../../plugins/studio-faceless/outils/montage/mix_film.py)

- **Rôle** : faire **le** mix du film entier, après le collage en voix seule : musique, effets, baisse sous la voix, silences voulus, creux de musique, gain final unique, limiteur. L'image du film voix est copiée telle quelle (`-c:v copy`).
- **Quand il sert** : Studio Director, étape 10 de l'épisode, une fois le plan son écrit (porte de questions n° 10). Relancé à chaque correction de son : un remix, **sans nouveau rendu d'image**.
- **Usage** :
  ```bash
  python -I -B "${CLAUDE_PLUGIN_ROOT}/outils/montage/mix_film.py" episodes/<id>/outputs/<nom>-voix.mp4 episodes/<id>/montage/plan-son.json --son-seul
  python -I -B "${CLAUDE_PLUGIN_ROOT}/outils/montage/mix_film.py" episodes/<id>/outputs/<nom>-voix.mp4 episodes/<id>/montage/plan-son.json
  ```
  | Argument | Effet |
  |---|---|
  | `film` (positionnel) | MP4 « voix » sorti de `assembler.py --voix-seule`. |
  | `plan` (positionnel) | Plan son JSON. |
  | `--journal FICHIER` | Journal du film voix. Défaut : `FILM.journal.json`, sinon `FILM.log.txt`. |
  | `--nom NOM.mp4` | Nom du MP4 mixé. Défaut : `sortie.nom` du plan, sinon le nom du film avec `-mix` à la place de `-voix`. |
  | `--out DOSSIER` | Dossier de sortie. Défaut : `sortie.dossier` du plan, sinon le dossier du film. |
  | `--son-seul` | Mesure le mix et affiche le journal, **n'écrit rien** (et ne refuse pas une sortie existante). |
- **Fichiers lus** : le film voix `FILM.mp4` ; `FILM.voix.wav` (voix sans perte ; à défaut le son AAC du MP4, avec un AVIS au journal et un second encodage AAC à la fin) ; `FILM.journal.json` ou `FILM.log.txt` ; le plan son ; les fichiers de sons, relatifs à `racine`.
- **Fichiers écrits** : `NOM.mp4`, `NOM.mix.wav`, `NOM.log.txt` (aucun écrasement). Le MP4 est remuxé : image copiée, son AAC 320 kbit/s 48 kHz, étiquette `title`.
- **Clés du plan son (`plan-son.json`)** — un temps s'écrit en secondes du film (`412.5`) ou en temps local d'une séquence (`{"seq": "seq3", "t": 12.5}`, converti par le journal ; `seq` peut aussi nommer `outro` ou une pièce de marque ; pour `noir`, c'est le premier du film) :

  | Clé | Contenu | Défaut |
  |---|---|---|
  | `racine` | Dossier des sons, relatif à la racine de la chaîne (par exemple `marque/son`) | `.` |
  | `baisse_sous_voix_db` | Baisse de la musique sous la voix active | 4,0 |
  | `niveaux_par_type` | Par type d'effet : un nombre en LU, ou `{"lu": …, "baisse_db": …}` | aucun |
  | `silences[]` | `debut`, `fin`, `raison` : musique et effets coupés dans la fenêtre (rampes de 50 ms hors de la fenêtre) ; un effet qui y **commence** est retiré | aucun |
  | `creux[]` | `debut`, `fin`, `baisse_db`, `rampe`, `raison` : la musique **seule** baisse, les effets restent | 8 dB, 0,8 s |
  | `musique[]` | `fichier`, `depart`, `fin` ou `duree`, `niveau_lu` (obligatoire) ; `decalage` (départ dans la source), `boucle` `[début, fin]` en secondes de la source, `fondu_boucle`, `fondu_entree`, `fondu_sortie`, `baisse_db` | décalage 0, fondu de boucle 0,05 s, fondus 1,0 s |
  | `effets[]` | `fichier`, `depart`, `type` (obligatoire, présent dans `niveaux_par_type`) ; `extrait` `[début, fin]`, `fondu_entree`, `fondu_sortie` | extrait entier, 0,008 s, 0,10 s |
  | `titre` | Étiquette `title` du MP4 | titre du film voix sans « — voix seule », plus « — mix du film » |
  | `sortie` | `dossier`, `nom` | voir `--nom`, `--out` |
- **Méthode** :
  1. *Voix de référence* : sonie intégrée (BS.1770, écrite en numpy) mesurée sur les seules séquences ; le journal donne aussi la sonie par séquence, l'écart maximal et le plus grand saut entre voisines (mesuré, non corrigé).
  2. *Musique* : gain = voix + `niveau_lu` − sonie intégrée de l'extrait (fondus compris, avant la baisse). Baisse sous la voix active par l'enveloppe RMS de la voix (fenêtres de 10 ms, seuil −42 dBFS, anticipation de 60 ms, descente 80 ms, remontée 400 ms, pauses de 0,25 s au moins comblées pour la remontée).
  3. *Effets* : gain = voix + niveau du type − sonie momentanée maximale (fenêtre de 400 ms) de l'extrait ; baisse facultative par type (pauses de moins de 0,65 s comblées).
  4. *Silences voulus et creux* : appliqués par masques à rampes en cosinus.
  5. *Gain final unique* vers −16 LUFS mesuré sur les séquences ; **les pièces de marque (signature, outro) gardent leur niveau d'origine** (rampes de 10 ms à leurs bords) ; limiteur de crêtes vraies à −2,0 dBTP (celui de l'assembleur), jusqu'à trois recalages.
  6. *Remux et contrôles* : décodage complet sans erreur ; nombre d'images identique à l'entrée et au journal ; **empreinte MD5 du flux vidéo identique** ; −16 ±1 LUFS ; crête vraie ≤ −1,5 dBTP.
- **Journal (`.log.txt`)** : entête, voix de référence par séquence, une ligne par musique (départ, fondus, gain, baisse, boucles, `COUPÉE` par un silence, `AVIS` si elle chevauche une pièce de marque ou si la source est trop courte), une ligne par effet (ou `RETIRÉ`), silences, creux, sonie de la musique après baisse, gain final et zones de limitation, puis la ligne `Contrôles du MP4`.
- **Codes de sortie** : 0 si l'outil va au bout **même si `Contrôles du MP4` annonce un ÉCART** ; 1 à tout arrêt avec message (sortie existante, fichier de son introuvable, type absent de `niveaux_par_type`, fin avant début, départ hors du film, boucle hors de la source…) ; 2 pour des arguments invalides.
- **Dépendances** : `numpy`, `scipy` (`scipy.signal.lfilter`), FFmpeg, FFprobe ; importe `assembler.py` situé dans le même dossier (les deux fichiers doivent rester côte à côte). Mêmes variables d'environnement que `assembler.py`.
- **Liens** : lit les sorties de `assembler.py --voix-seule` ; son plan est décrit dans `outils/montage/README.md` ; règle : `DIRECTION_AUDIO.md` § 3 ; sons puisés dans `marque/son/`.
- **À savoir** :
  - **Signe des niveaux** : `niveau_lu` et les niveaux par type sont des niveaux **relatifs à la voix**. Pour « 13 LU sous la voix », écrire **−13**. Une valeur positive mettrait le son au-dessus de la voix.
  - Le `type` d'un effet doit être **identique** (accents compris) à une clé de `niveaux_par_type` : `montee` n'est pas `montée`. Les types ne sont pas fermés : c'est la chaîne qui les nomme.
  - Les effets très courts (moins de 0,4 s) ressortent un peu plus fort que leur type ne le dit (sonie momentanée moyennée sur 400 ms).
  - Pas de balance, d'égalisation ni de creux 1-4 kHz dans l'outil.
  - Un temps local hors de la séquence n'arrête pas l'outil : il ajoute un AVIS au journal.
  - Une musique qui traverse une jonction ou chevauche une pièce de marque est seulement signalée ; le gain final ne s'applique pas sous la marque.
  - Mémoire : environ 2 à 3 Go pour un film de 9 min (son en mémoire, limiteur échantillon par échantillon). 6,5 minutes pour le mix de l'E007 d'AA.
  - Le master reste `ECOUTE_A_FAIRE` : l'outil ne produit pas de « reste » (musique et effets sans la voix), donc `controle.py voix-reste` n'a pas de source prête sur le film mixé (à vérifier).

### outils/montage/srt.py
Fichier : [`srt.py`](../../plugins/studio-faceless/outils/montage/srt.py)

- **Rôle** : fabriquer les sous-titres SRT du master : le **texte** vient du script vérifié, les **temps** des mots recalés de chaque séquence, les débuts de séquence du journal.
- **Quand il sert** : Studio Director, étape 12 (publication), une fois le film collé ; le SRT part avec le dossier YouTube (`PUBLICATION_vN.<langue>.srt`) et se contrôle par `publication.py verifier … --srt`.
- **Usage** :
  ```bash
  python -I -B "${CLAUDE_PLUGIN_ROOT}/outils/montage/srt.py" --script episodes/<id>/SCRIPT_v1.md --mots "kit/voix/{seq}-montage-mots-recales.json" \
      --journal episodes/<id>/outputs/<nom>-voix.log.txt --sortie episodes/<id>/PUBLICATION_v1.en.srt
  ```
  | Option | Effet |
  |---|---|
  | `--script` (obligatoire) | Script vérifié : un titre `## seqN` suivi d'un bloc ```` ```text ```` par séquence ; le texte doit être celui de la prise. |
  | `--mots` (obligatoire) | Motif du fichier de mots recalés, avec `{seq}`. Relatif au **dossier du script** (la racine de l'épisode), sauf chemin absolu. |
  | `--journal` (obligatoire) | Journal du film voix : `.log.txt` ou `.journal.json` de `assembler.py`. |
  | `--sortie` (obligatoire) | Fichier SRT à écrire ; refus d'écraser. |
- **Fichiers lus** : le script ; un JSON de mots par séquence (`{"mots": [{"w", "start", "end"}]}`, sortie de `transcrire.py` ou de `recaler.py`) ; le journal. **Écrit** : le SRT (UTF-8, fins de ligne LF). Affiche : nombre de sous-titres, durée la plus courte et la plus longue, nombre de lignes de plus de 42 caractères.
- **Algorithme** : alignement des mots du script sur les mots entendus (`difflib`), mots non reconnus (nombres écrits en lettres…) interpolés entre leurs voisins ; décalage du début de chaque séquence ; une phrase par sous-titre (fin sur `.`, `?` ou `!`), coupée en morceaux de deux lignes de 42 caractères au plus, de préférence après une virgule, sans couper un nom propre (deux mots à majuscule) ; un sous-titre de moins d'1 s rejoint le suivant s'il tient encore sur deux lignes ; durée de 1 à 7 s, 0,3 s de tenue après le dernier mot, 50 ms d'écart, aucun chevauchement.
- **Codes de sortie** : 0 ; 1 si le motif n'a pas `{seq}`, si la sortie existe, si une séquence du script manque au journal ; une erreur de lecture de fichier donne une trace Python.
- **Dépendances** : bibliothèque standard seulement (ni numpy, ni FFmpeg).
- **Liens** : mots de `transcrire.py` / `recaler.py` ; journal de `assembler.py` ; vérifié ensuite par `controle/publication.py` ; cité dans `rendu-collage.md` § 5 et `etapes.md` § 12.
- **À savoir** :
  - Les débuts de séquence sont lus au centième de seconde dans le journal (±5 ms).
  - La règle « 1 à 7 s » cède devant « aucun chevauchement » (un sous-titre de 0,92 s à l'E007 d'AA).
  - Le `--journal` doit être celui du **film voix** (`<nom>-voix.log.txt` ou `.journal.json`) : le `.log.txt` du master mixé ne contient pas les lignes de segments ; `rendu-collage.md` § 5, le README de `controle/` et le skill `youtube-seo` donnent maintenant ce nom.
  - Vérifier par sondage trois phrases contre le film.

---

## Les outils de la voix off

Dossier [`outils/controle/`](../../plugins/studio-faceless/outils/controle/) : deux scripts de la chaîne voix (`transcrire.py`, `ralentir.py`). Les autres contrôles (`controle.py`, `publication.py`) sont décrits dans `outils-et-garde.md` et `publication.md`. Parcours : [`../workflows/voix-off.md`](../workflows/voix-off.md).

### outils/controle/transcrire.py
Fichier : [`transcrire.py`](../../plugins/studio-faceless/outils/controle/transcrire.py)

- **Rôle** : transcrire localement une prise (filtre `whisper` de FFmpeg) et la comparer mot à mot au texte de référence ; donner les mots horodatés (±0,1 s) et les phrases ; vérifier un passage douteux.
- **Quand il sert** : Studio Director, deux fois dans l'étape voix : (1) à réception de chaque prise du propriétaire, avec `--texte` ; (2) sur la bande ralentie, pour obtenir les mots horodatés à recaler.
- **Usage** :
  ```bash
  python -I -B "${CLAUDE_PLUGIN_ROOT}/outils/controle/transcrire.py" PRISE.mp3 --modele CHEMIN/ggml-base.en.bin --sortie DOSSIER [--texte TEXTE.txt]
  python -I -B "${CLAUDE_PLUGIN_ROOT}/outils/controle/transcrire.py" PRISE.mp3 --modele CHEMIN/ggml-base.en.bin --isoler DEBUT DUREE
  ```
  | Option | Effet |
  |---|---|
  | `prise` (positionnel) | Fichier audio lisible par FFmpeg (mp3, wav…). |
  | `--modele` (obligatoire) | Chemin du modèle `ggml` (par exemple `ggml-base.en.bin`, MIT, 148 Mo), **hors du projet**. |
  | `--sortie DOSSIER` | Dossier des trois fichiers de sortie (créé au besoin). Obligatoire, sauf avec `--isoler`. |
  | `--texte TEXTE.txt` | Texte de référence : liste les écarts mot à mot. Les balises entre crochets (`[calm]`…) sont ignorées. |
  | `--isoler DEBUT DUREE` | Transcrit seulement ce passage (secondes de la prise) et l'affiche : `[37.50 s + 4.50 s] texte…`. N'écrit rien. |
- **Fichiers écrits** (dans `--sortie`, nommés d'après la prise ; refus d'écraser) : `<nom>-texte.txt` (texte complet), `<nom>-mots.json` (`source` et `mots` : `{"w", "start", "end"}` arrondis au centième), `<nom>-phrases.txt` (« début – fin  texte » par phrase). Fichier temporaire `_transcrire_<pid>_<0|1>.srt` créé **dans le dossier du modèle**, puis supprimé.
- **Comparaison au texte** : sortie `≈ 12.40 s · replace · texte « a » → entendu « b »`. Les étiquettes sont celles de `difflib` : `delete` = mot du texte non entendu ; `insert` = mot entendu en plus (doublon suspect) ; `replace` = remplacement. Les mots sont normalisés (minuscules, ponctuation retirée).
- **Méthode interne** : deux passes de Whisper sur l'audio rééchantillonné en 16 kHz mono (phrases, puis mot à mot avec `max_len=1`), langue `en`, file `queue=20`, `use_gpu=false`. Le script se place dans le dossier du modèle pour utiliser des chemins relatifs (les « : » des lecteurs Windows cassent les arguments du filtre).
- **Codes de sortie** : 0 en fin normale **même s'il y a des écarts** ; 1 si le modèle est introuvable, si `--sortie` manque, si une sortie existe déjà, ou si Whisper échoue (dernier message de FFmpeg affiché).
- **Dépendances** : FFmpeg 9.x avec le filtre `whisper` (build Gyan de WinGet) ; bibliothèque standard seulement (pas de numpy). Variables : `HYPERFRAMES_FFMPEG_PATH`, `LOCALAPPDATA`.
- **Liens** : règle `DIRECTION_AUDIO.md` § 2-3 ; mode d'emploi `outils/controle/README.md` ; ses mots alimentent `recaler.py` (rangé dans `outils/shorts/`) puis `srt.py`.
- **À savoir** :
  - **Faux écarts attendus** : nombres en chiffres (« 113th »), accents perdus (« Maracana »), noms propres approximatifs.
  - **Un mot doublé ou étrange se vérifie TOUJOURS avec `--isoler`** avant d'être signalé au propriétaire : c'est souvent un artefact de Whisper (exemple d'AA, E003 : « Germany are well-known world champions » était « Germany are world champions »).
  - **Sur une bande ralentie**, les débuts de mots arrivent jusqu'à 1,6 s trop tôt et chaque mot est collé au précédent : les recaler avant de les donner aux producteurs.
  - Le modèle est anglais (`.en`) et la langue codée en dur : pour une chaîne dont le spectateur parle une autre langue, il faudrait un autre modèle et modifier le script (à vérifier avec le propriétaire).
  - Un téléchargement du modèle se fait avec l'accord du propriétaire. À l'origine, il se trouvait dans le dossier temporaire de session de Claude : une nouvelle session doit le retrouver ou le télécharger.
  - Le dossier du modèle doit être inscriptible (fichier temporaire).

### outils/controle/ralentir.py
Fichier : [`ralentir.py`](../../plugins/studio-faceless/outils/controle/ralentir.py)

- **Rôle** : ralentir « juste un peu » une prise de narration selon la méthode validée (`DIRECTION_AUDIO.md` § 2), allonger ses pauses sans rien recopier, caler la bande à −19 LUFS mono, et refuser d'écrire si la bande contient une recopie. Aucune coupe, aucun mot retiré ni ajouté.
- **Quand il sert** : Studio Director, étape voix, après la vérification de la prise. **À n'appliquer qu'à la narration**, jamais aux voix jouées (chants, citations) ni aux shorts (qui ont leur propre outil, `voix_short.py`).
- **Usage** :
  ```bash
  python -I -B "${CLAUDE_PLUGIN_ROOT}/outils/controle/ralentir.py" PRISE.mp3 SORTIE.wav [--tempo 0.97] [--tete 0.6] [--queue 1.2] [--cible -19]
  ```
  | Option | Défaut | Effet |
  |---|---|---|
  | `prise` | — | Prise d'origine (jamais modifiée). |
  | `sortie` | — | WAV à écrire (48 kHz, mono, 24 bits). Son dossier doit exister. |
  | `--tempo` | 0,97 | Facteur de `atempo` (hauteur conservée). × 0,94 jusqu'à l'E008 v1 d'AA. |
  | `--tete` | 0,6 s | Silence ajouté en tête. |
  | `--queue` | 1,2 s | Silence ajouté en queue. |
  | `--cible` | −19 | Sonie visée en LUFS, mesure mono (≈ −16 LUFS en double mono dans un MP4 stéréo). |
- **Étapes** : (1) parole ramenée à −20 dBFS RMS (gain seul, sur les échantillons au-dessus de −45 dBFS) ; (2) `atempo` ; (3) pauses internes de 0,36 à 0,60 s allongées de 0,15 s, au-delà de 0,25 s : le silence ajouté est inséré au milieu du plus long passage au plancher de la pause (à 60 ms au moins de la fin du mot et 30 ms du mot suivant) — silence numérique si le plancher est sous −70 dBFS (cas des prises ElevenLabs, ≈ −86 dBFS), sinon bruit généré au spectre et au niveau de ce passage (graine fixe), **jamais une recopie** ; (4) silences de tête et de queue ; (5) gain unique vers la cible, puis réduction si la crête vraie dépasse −2 dBTP ; (6) **auto-contrôle** : aucun passage ne doit être la copie exacte d'un passage 80 à 600 ms plus tôt (corrélation ≥ 0,995 sur au moins 5 trames de 20 ms) ; sinon rien n'est écrit.
- **Fichiers écrits** : `SORTIE.wav` et `SORTIE.positions.txt` (refus d'écraser l'un ou l'autre). Le fichier de positions donne : prise et **SHA-1**, durées avant/après, tempo, nombre de pauses allongées (et secondes ajoutées), durée de parole et pause médiane avant/après, niveau (LUFS mono, crête vraie, gain total), nature des pauses allongées (silence numérique ou bruit de fond) et « auto-contrôle : 0 recopie exacte ». Un fichier `SORTIE.wav.f32` temporaire est créé puis supprimé.
- **Codes de sortie** : 0 en succès ; 1 si une sortie existe, si l'auto-contrôle trouve une recopie (message avec les instants), ou si FFmpeg échoue.
- **Dépendances** : `numpy`, FFmpeg. Calcul : environ 30 s par minute et demie de voix (auto-contrôle).
- **Liens** : règle `DIRECTION_AUDIO.md` § 2 ; importé par `outils/shorts/voix_short.py`, `recaler.py` et `raccord.py` (qui réutilisent ses fonctions) ; sa bande alimente `transcrire.py`, puis `voix.py` du gabarit de séquence.
- **À savoir** :
  - **Pourquoi pas de recopie** : la version du 15/10/2026 recopiait le début de la pause, qui contient la queue du mot ; la fin du mot revenait 0,15 à 0,46 s plus tard (bandes des E003 et E004 d'AA). Correctif validé le 17/10/2026. Depuis, les mots tombent aux mêmes instants et seul le contenu des pauses change.
  - Le message final de l'outil (« transcrire la bande ralentie pour donner les repères aux producteurs ») ne mentionne pas le **recalage** nécessaire entre-temps (voir [Points à vérifier](#points-à-vérifier-relevés-à-la-lecture)).
  - Le débit global (mots par minute, pauses comprises ; cible 130 à 135) n'est pas calculé par l'outil : il se déduit du nombre de mots du texte et de la durée de la bande (à faire à la main, à vérifier).
  - Le tempo est un réglage de chaîne : un écart de `direction/ECARTS.md` peut le changer sans toucher au script.

---

## Points à vérifier relevés à la lecture

Écarts entre fichiers du plugin repérés pendant la rédaction de cette fiche. Les fichiers du plugin font foi. Ont été retirés ceux que la correction du 28/10/2026 a réglés : connecteur ElevenLabs et musique, journal à donner à `srt.py` et à `publication.py chapitres`.

| # | Constat | Fichiers |
|---|---|---|
| 1 | Le skill et sa référence précisent maintenant que les techniques (J/L-cut, ponts, silences) s'appliquent au mix du film, pas dans la composition de la séquence. Reste : rien ne dit comment un J-cut ou un L-cut s'écrit dans `plan-son.json` (départs de musique et d'effets en temps du film ; la voix ne se déplace jamais). | `skills/direction-sonore/SKILL.md:28` ; `references/transitions-et-silences.md:33-39` ; `referentiels/DIRECTION_AUDIO.md:68-72` |
| 2 | Les niveaux de l'exemple `niveaux_par_type` (souffle −12, impact −8, montée −12, déclic −14, ambiance −20) diffèrent des niveaux de départ validés (impact 14, souffle 18, montée 16, papier ou déclic 20, ambiance 16 LU sous la voix). | `outils/montage/README.md:57-58` ; `referentiels/DIRECTION_AUDIO.md:73` ; `skills/episode/references/rendu-collage.md:33-40` |
| 3 | Le recalage des repères sur les vrais départs de la voix est exigé (E004/E005 d'AA), mais le seul outil qui le fait, `recaler.py`, est rangé dans `outils/shorts/` et décrit comme outil de shorts ; ni le skill `episode` ni le README de `controle/` ne le nomment. Le message de fin de `ralentir.py` enchaîne directement sur `transcrire.py`, sans le recalage. | `outils/shorts/README.md:10` ; `outils/shorts/recaler.py:1` ; `skills/episode/references/etapes.md:29` ; `outils/controle/README.md:46` ; `outils/controle/ralentir.py:200` |
| 4 | Réglé le 29/10/2026 (D2) : le `settings.json` du squelette autorise `assembler.py`, `mix_film.py` et `srt.py` à la place de `mix.py`. Reste : aucune règle n'autorise `ralentir.py` ni `transcrire.py` : leur lancement dépend du mode de permission de la session (à vérifier). | `starter/.claude/settings.json:19-24` |
| 5 | La fiche d'ouverture estime le temps à 125 mots par minute ; `DIRECTION_AUDIO.md` vise 130 à 135 mots par minute (global, pauses comprises). Estimation et cible peuvent être voulues différentes (à vérifier). | `skills/episode/references/recit-retention.md:55` ; `referentiels/DIRECTION_AUDIO.md:25` |
| 6 | « Son catalogue » est cité comme fichier de la bibliothèque, mais le README du squelette n'annonce que des tableaux, des `E00N-PROVENANCE.md` et `SHA1SUMS.txt`. | `skills/episode/references/socle.md:42` ; `templates/sequence-gabarit-v3/README.md:19` ; `starter/marque/son/README.md:7` |
| 7 | La limite « les séquences sorties du gabarit portent encore le gain de leur `mix.py` » décrit le gabarit v2 ; avec la v3, `voix.py` livre `stem-voix.wav` au gain 1. | `outils/montage/README.md:87` ; `templates/sequence-gabarit-v3/voix.py:5` |
| 8 | Aucun fichier ne dit où ranger le contrat audio, la feuille de repérage et le journal de cues d'un film mixé (les gabarits parlent du dossier de la séquence). | `skills/direction-sonore/references/gabarits.md:3` |
| 9 | `transcrire.py` fixe la langue à `en` et la documentation désigne un modèle anglais (`.en`) alors que le plugin sert des chaînes dont la langue du spectateur est un paramètre. | `outils/controle/transcrire.py:30` ; `starter/CLAUDE.md:7` |
