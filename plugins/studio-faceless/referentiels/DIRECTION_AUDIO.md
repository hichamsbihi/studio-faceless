# Direction audio et sound design

> Règles par défaut du plugin studio-faceless.
> Les écarts de la chaîne (`direction/ECARTS.md`) l'emportent.

**Statut.** Les contraintes reçues du propriétaire sont des décisions. Les choix artistiques et les chiffres ci-dessous sont des recommandations à éprouver. Aucun mixage n'est validé par ce document.

Les pratiques propres à un épisode vont dans son `CLAUDE.md`.

## 1. Décisions et contraintes
| Sujet | Statut |
|---|---|
| Voix | Propre à la chaîne (voix retenue, prises, statut) : `direction/ECARTS.md`. |
| Prise approuvée | Ne jamais régénérer, réécrire, accélérer ni couper une prise sans autorisation explicite. **Seule exception, validée sur AA le 15/10/2026** : toute narration est ralentie « juste un peu » selon la méthode du § 2 (« le principe de ralentir juste un peu doit être pris dans toutes les séquences »). **Les shorts n'y sont pas soumis** (validé sur AA, 19/10/2026) : script dédié, prise à vitesse d'origine, pauses resserrées au montage. Une seule prise par short ; la version YouTube est la même prise **sans le bloc D**, coupée à des frontières de phrase (script en blocs, accord du 19/10/2026 sur AA ; skill `studio-faceless:shorts`). **Son des shorts plus fort que celui des films** (validé sur AA, 19/10/2026 : « un son plus élevé qui capte l'attention »). Valeurs `PROPOSÉ`, à confirmer à l'écoute : musique dès 0,0 s, environ 8 LU sous la voix (`MUS_REL` −6, `MUS_DUCK` 2), contre 12 à 15 LU dans les films ; master final à −14 LUFS, crête vraie ≤ −1 dBTP, avec un limiteur passé par Claude après le rendu. **Effets dans les shorts** (validé sur AA, 19/10/2026, formule des shorts) : un effet court (moins de 0,4 s : whoosh, impact, clic) sur chaque événement visuel, à 12 à 18 dB sous la voix ; un riser au plus avant la révélation ; environ 0,3 s de silence avant le fait clé ; coupes calées sur le tempo de la musique. La règle « effets rares » reste celle des films. |
| Immersion | L'immersion totale du spectateur est la ligne directrice du son (slogan d'AA, 15/10/2026). |
| Méthode | **Musique d'abord** (validé sur AA, 15/10/2026) : une musique de documentaire, choisie selon la situation, porte l'immersion de chaque séquence. Les effets et les foules ne s'emploient que si l'image les justifie (« les SFX doivent être utilisés que si besoin »). Niveaux décidés au mixage ; jamais deux fois le même traitement sur un master. |
| Essais musique | Propres à la chaîne : `direction/ECARTS.md`. |
| Choix des sons | Le propriétaire choisit lui-même les variantes générées ; ne pas superposer une musique non demandée. |
| Dépenses | Aucune génération ni dépense hors du budget explicitement autorisé par la mission ; aucun achat. |

## 2. Principes
- La voix conduit la compréhension ; les ambiances installent les lieux ; la musique organise la progression ; les effets ponctuent une action ou un changement d'idée ; les silences laissent place à la découverte. Une seule couche peut suffire.
- **Narration** : la prise approuvée est la base temporelle (pauses et diction réelles). Proche, centrée, peu ou pas de réverbération. On corrige un défaut identifié, pas un timbre ; aucun traitement systématique. Si une archive parle, choisir qui est au premier plan.
- **Ralentissement de toute narration** (validé sur AA le 15/10/2026, après « la narration fait vite »). La voix seule est traitée ; les voix jouées (chants, citations) restent intactes.
  1. Tempo × 0,97 avec `atempo` (hauteur conservée) : `ralentir.py --tempo 0.97`, réglage par défaut depuis le 26/10/2026 (validé sur AA, 26/10/2026, d'après l'E008 v2, approuvé à l'écoute ; étude AA, 26/10/2026). C'était × 0,94 jusqu'à l'E008 v1, jugé lent. Le débit global (mots par minute, pauses comprises) est mesuré et noté à chaque épisode ; il vise 130 à 135, et on mesure avant d'aller plus vite.
  2. Pauses internes allongées : +0,15 s pour une pause de 0,36 à 0,60 s, +0,25 s au-delà.
     - Le silence ajouté est au plancher de la prise et se place au point le plus calme de la pause.
     - Jamais de recopie du début de la pause : il contient la queue du mot, qu'on entendrait deux fois.
     - Correctif validé sur AA le 17/10/2026 (« ok inclu ce correctif pour les prochaines episodes »).
  3. Gain unique vers −19 LUFS en mesure mono, soit −16 LUFS une fois en double mono dans un MP4 stéréo. Crête vraie ≤ −2 dBTP.

  Résultat constaté sur AA : environ 183 → 172 mots/min hors pauses, 144 → 128 mots/min au global. Script de référence : `${CLAUDE_PLUGIN_ROOT}/outils/controle/ralentir.py`, qui refuse d'écrire une bande contenant une recopie.
- **Chaîne voix** (méthode de l'épisode 003 d'AA, à reprendre) :
  1. Le script est rédigé en anglais. Chaque phrase est vérifiée, avec sa source, dans une note de narration.
     - **Aucune balise par défaut** (validé sur AA, 23/10/2026, « aucune balise ElevenLabs par défaut, seulement là où un passage l'exige vraiment ») : le ton naturel de la voix porte le texte. Une balise peut changer le ton de la narration ; elle ne s'emploie que pour un passage qui l'exige vraiment, placée sur ce passage et pour une raison qu'on peut dire, jamais en tête de prise par habitude.
     - Les balises possibles restent les balises d'émotion d'eleven_v4 : `[calm]`, `[thoughtful]`, `[serious]`, `[softly]`.
     - **Aucune balise de pause ni de vitesse** (`[pause]`, `[short pause]`, `[long pause]`, `[slowly]`), décision du 15/10/2026 validée sur AA : les pauses et le rythme se font au montage (ralentissement ci-dessus).
  2. Le propriétaire génère la prise.
  3. Transcription locale et comparaison mot à mot ; un doublon suspect se vérifie sur le passage isolé (souvent un artefact de Whisper).
  4. Ralentissement.
  5. Livraison aux producteurs de la bande, des mots horodatés et des phrases.
- **Images au rythme de la voix** : voir `${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 ter.
- **Vérification de la prise** : toute narration fournie est transcrite mot à mot avant le découpage, puis comparée au texte du brief. Tout écart est signalé au propriétaire tout de suite, et en tête du compte rendu. On construit sur l'audio réel ; le texte à l'écran ne reprend que ce qui est entendu ou sourcé.
- **Voix générées** (citation, dialogue reconstitué) : toujours déclarées à l'écran.
- **Musique**, révisée le 15/10/2026 : elle **porte l'immersion**. On la choisit selon la situation : ouverture, tension ou rivalité, analyse et science, émotion et fin.
  - Elle s'entend vraiment : environ 12 à 15 LU sous la voix, avec un ducking doux de 3 à 5 dB quand la voix parle, et elle remonte dans les pauses. Elle ne s'arrête que sur un silence voulu.
  - **Avant une révélation** (validé sur AA, 26/10/2026, étude AA et retours sur l'E008) :
    - la voix peut marquer une pause de 0,5 à 1 s au plus, seulement sur une image réelle (photo, vidéo), jamais sur une simple animation ;
    - la musique ne se coupe pas : elle baisse, avec un creux d'environ 8 dB et des rampes de 0,8 s (clé `creux` de `${CLAUDE_PLUGIN_ROOT}/outils/montage/mix_film.py`).
  - Une séquence qui suit la signature de la chaîne démarre sur une musique d'ouverture de documentaire, jamais sur des voix de foule.
  - Peu d'éléments dans la zone de la voix ; prévoir entrées, retraits et fin au découpage. Ni pathos imposé, ni riser automatique, ni changement de morceau à chaque décor.
- **Ambiances et effets** : seulement si l'image les justifie (« un mouvement ne rend pas un son nécessaire »), au moment exact, puis ils s'arrêtent.
  - **Foules** : une foule ne reste jamais en fond tout au long d'une séquence (exemple AA : dans l'ouverture de l'épisode 003, les voix de supporters n'apparaissent qu'après le nom du stade et s'arrêtent quelques secondes après).
  - **Son des extraits vidéo** (demande du propriétaire sur l'E008 d'AA, 26/10/2026 ; nuance validée sur AA, 28/10/2026) : le vrai son d'un extrait passe sous la voix plutôt qu'une foule de bibliothèque. Avant de le prévoir, on le transcrit (filtre `whisper`, § 3). S'il porte un commentaire, fréquent sur les vidéos d'instances ou de chaînes de diffusion, on ne l'emploie pas : une ambiance de la bibliothèque de la chaîne (`marque/son/`) le remplace, et la description dit « Crowd sounds are illustrative » quand il s'agit d'une foule.
  - **Effets d'appareil** (scanner, tiques…) : ils ne jouent que pendant le mouvement qui les motive.
  - **Accent et interdits** : l'accent tombe sur l'action perçue. Pas de whoosh à chaque raccord, ni de bip par chiffre.
  - **Ponctuation des changements** (validé sur AA, 26/10/2026, étude AA) :
    - un impact grave à chaque changement de bloc ou de chapitre, soit quelques-uns par film ;
    - un whoosh seulement quand un élément traverse vraiment le cadre ;
    - un son de matière sur un volet de matière.

    Niveaux du § 3 : impact 14 LU, souffle 18, papier 20.
  - **Statut** toujours noté : archive exacte / enregistrement contextuel / génération illustrative.
  - Ne jamais fabriquer la voix, les pas ou la respiration d'une personne réelle comme s'ils avaient été captés.
- **Raccords** : J-cut et L-cut pour la continuité. Ne jamais déplacer ou rogner un mot pour tomber sur un temps musical.

## 3. Mixage et livraison
- **Mix du film à la fin, sur le film collé** (validé sur AA, 24/10/2026, pour tous les épisodes à venir ; méthode : skill `studio-faceless:episode`, référence `rendu-collage.md`) :
  - les séquences ne portent que la voix : chaque producteur laisse musique et effets vides et liste dans son README un tableau des **effets proposés** (code, instant local, image qui le justifie ; facultatifs marqués) ;
  - le film se colle d'abord en voix seule (signature, rappel d'abonnement et écran de fin compris), avec le journal du master ;
  - puis **un seul mix** sur le film entier : relevé musical par morceau (tempo, boucles sur mesures entières, silences voulus), musique qui peut continuer d'une séquence à l'autre, effets repris des tableaux à **niveaux fixes par type** (en LU sous la voix), baisse sous la voix active, **un seul gain final** vers −16 LUFS et limiteur à −2,0 dBTP ; l'image est copiée telle quelle ;
  - une correction de son se refait par un **remix**, sans nouveau rendu d'image ; Claude n'écoute pas : le film reste `ECOUTE_A_FAIRE` jusqu'à l'écoute du propriétaire.
  - niveaux de départ par type, en LU sous la voix (validé sur AA, 24/10/2026, à calibrer à sa première écoute) : musique 13, ambiance 16, impact 14, souffle 18, montée 16, papier ou déclic 20 ; gain final hors signature et outro ; écart de voix entre séquences mesuré, sans égalisation.
  - **fin du film en douceur** (validé sur AA, 28/10/2026 ; demande du 26/10 : « finir la vidéo en douceur comme un vrai film ») : la dernière séquence se fond en 1,2 s dans 4 s de noir, puis l'outro entre en 0,5 s ; le morceau de fin est calé dans sa source pour que son accord final s'éteigne sur le noir, et il s'arrête en fondu juste après l'entrée de l'outro ; aucune coupe sèche. Réglages : skill `studio-faceless:episode`, `rendu-collage.md` § 4.
- **Bibliothèque de sons** de la chaîne (`marque/son/`, validé sur AA, 24/10/2026) : un épisode puise d'abord dans les musiques et effets déjà générés ; un nouvel appel ElevenLabs seulement à la demande du propriétaire, puis le son approuvé rejoint la bibliothèque.
- Familles séparées : voix, musique, ambiances, effets.
- En cas de concurrence : réduire ou déplacer la couche secondaire, puis revoir son arrangement, puis automatiser son gain. Corriger une fréquence seulement si le masquage est établi.
- Sous la voix, la musique est atténuée de 3 à 5 dB (ducking doux, décision du 15/10/2026). Le carve fréquentiel reste **seulement si nécessaire** : la consigne du propriétaire prime sur le « carve by default » du skill.
- Cibles de travail : 48 kHz, AAC-LC stéréo 48 kHz, **environ −16 LUFS** (plage −17 à −15), **true peak ≤ −1,5 dBTP**, mesurés sur le MP4 livré décodé.
- Écouter aussi en mono et sur un petit haut-parleur : aucune information essentielle ne doit dépendre de la stéréo ou du grave.

**HyperFrames 0.8.149 (constaté)**
- Les médias sont pilotés par le moteur via `data-start`, `data-duration`, `data-media-start`, `data-volume`, `data-automation` et les fondus.
- Un identifiant unique par audio. Aucune lecture manuelle, aucune double lecture d'une vidéo dont le son est séparé.
- L'AAC est fixé à 192 kbit/s (384 non disponible).
- Le moteur abaisse tout le mix pour rester sous −1 dBTP : régler les gains à la source pour qu'il n'ait pas à le faire.
- `scripts/carve.mjs` du skill exige le paquet `@hyperframes/core`, absent ici ; l'ajouter serait une nouvelle dépendance, à décider par le propriétaire. Alternative éprouvée sur l'épisode 001 d'AA : une automation de volume (`data-automation`, valeurs absolues) écrite à la main sous les passages de voix, puis mesurée sur le MP4 livré (voix ≥ 12 dB au-dessus du reste entre 1 et 4 kHz).

**Transcription locale (constaté le 12 octobre 2026, filtre revérifié le 14 octobre)**
- Le FFmpeg 9.0.2 installé (build WinGet Gyan) contient le filtre `whisper` (whisper.cpp). Il lui faut un modèle `ggml`, par exemple `ggml-base.en.bin` (licence MIT, 148 Mo), gardé hors du projet ; tout téléchargement se fait avec l'accord du propriétaire.
- Découper par silences ; `max_len=1` donne les mots à ±0,1 s environ. Lancer depuis le dossier du modèle, avec des chemins relatifs : les « : » des lecteurs Windows cassent les arguments du filtre.
- Échecs connus : l'alignement DTW sur la voix Windows (Zira) dérive ; Scribe d'ElevenLabs demande que le propriétaire envoie le fichier lui-même.

## 4. ElevenLabs
- **Deux connecteurs possibles**, selon ce que le propriétaire a ajouté à son compte claude.ai :
  - le connecteur de base fait voix et effets sonores, **pas de musique** ;
  - le connecteur ElevenLabs complet ajoute la musique (Eleven Music v2.5 : durée de 3 à 600 s, instrumental possible ; prompt = genre, humeur, instruments, tempo, courbe d'énergie, sans visuel) ;
  - vérifier celui de la session avant de promettre une musique.
- **Coûts constatés sur AA** : effets, environ 3,3 crédits par seconde ; musique, estimation d'environ 27,5 crédits par seconde et par variante (20/10/2026).
- Brief d'un son : action ou matière, proximité, énergie, durée, sec ou réverbéré, début et fin, éléments exclus, rôle dans la scène. Générer les éléments séparément.
- **Coût réel** : l'estimation affichée avant une génération dépasse largement la facturation (constaté : 35 crédits facturés pour 115,5 estimés). La lire, sans s'en servir comme budget réel.
- **Une génération par nœud** (`generations_count: 1` ; quatre par défaut), ou deux quand le propriétaire doit choisir entre variantes (exemple AA : épisode 003). Prompt de 450 caractères au plus. Les liens de téléchargement expirent au bout de 2 h.
- **Clics et attaques** : un « clic » généré contient souvent plusieurs attaques. Mesurer les transitoires et ne garder qu'une paire appui/relâchement, calée sur l'image de contact.
- **Musique** : puiser d'abord dans `marque/son/`. Eleven Music demande le connecteur complet, que seul le propriétaire peut ajouter : sans lui, le dire et proposer une autre solution. Avec lui, montrer l'estimation et attendre l'accord du propriétaire, puisque la musique coûte cher.
  - **Solution éprouvée sur AA (15/10/2026, choisie de nouveau le 20/10/2026 parce qu'Eleven Music y était jugé trop cher)** : des nappes en boucle générées par le modèle d'effets (`loop: true`, 30 s, 2 variantes). Le Studio Director garde la variante dont le raccord de boucle est propre (écart d'énergie début/fin ≤ 1,5 dB) et la moins chargée entre 1 et 4 kHz. Il nomme l'autre pour que le propriétaire puisse l'échanger à l'écoute.
- **Garde-fou** : chaque appel au connecteur passe par une règle « ask » du `.claude/settings.json` de la chaîne (identifiant du connecteur, `INSTALLATION.md` du plugin) ; à défaut, Claude demande l'accord du propriétaire en conversation avant chaque lot. Regrouper les générations (tous les nœuds, puis un lancement par lot de 20 au plus) quand il est présent. **Aucun sous-agent n'appelle le connecteur** : le Studio Director génère et télécharge, puis consigne prompts, identifiants, empreintes et crédits.
- Les sons générés sont des illustrations. Consigner le prompt, l'identifiant, les crédits et la licence de l'abonnement dans `PROVENANCE.md`.

## 5. Contrôles
- **Techniques** (MP4 livré) :
  - pistes présentes, durée, décodage complet ;
  - calage et gain de la voix, aucun mot coupé ;
  - LUFS, true peak, écrêtage ;
  - écart voix / reste dans la bande 1–4 kHz ;
  - queues de sons, absence de double lecture ;
  - chaque effet et chaque foule placés sur l'image qui les justifie, sans fond de foule continu ; musique présente au niveau visé.
- **Perceptuels** (le propriétaire, ou un outil qui écoute réellement) :
  - intelligibilité, noms propres compris ;
  - naturel de la voix ;
  - raccords et boucles ;
  - utilité de chaque couche ;
  - confort au casque, en mono et sur petit haut-parleur.
- Une transcription, une forme d'onde ou une mesure LUFS ne valident pas une écoute.
- **Outils prêts** dans `${CLAUDE_PLUGIN_ROOT}/outils/controle/` (mode d'emploi : `${CLAUDE_PLUGIN_ROOT}/outils/controle/README.md`) :
  - `transcrire.py` : prise contre texte, passages isolés ;
  - `ralentir.py` : la méthode du § 2 ;
  - `controle.py niveau | voix-reste | tout`.
- Statuts : voir les règles communes du studio (`${CLAUDE_PLUGIN_ROOT}/REGLES_STUDIO.md`, « Règles permanentes »). Mesures techniques et écoute restent toujours séparées.

## Sources (consultées le 12 octobre 2026)
- [S1] iZotope, entretien avec le superviseur son de *Crip Camp* (archives) : https://www.izotope.com/en/learn/interview-with-jacob-bloomfield-misrach.html
- [S2] iZotope, *What is frequency masking?* : https://www.izotope.com/community/blog/what-is-frequency-masking
- [S3] Adobe, *J cuts and L cuts* : https://www.adobe.com/uk/creativecloud/video/discover/j-cut-and-l-cut.html
- [S4] FFmpeg, `loudnorm` : https://www.ffmpeg.org/ffmpeg-filters.html#loudnorm
- [S5] Adobe, *Automatically duck audio* : https://helpx.adobe.com/premiere/desktop/add-audio-effects/adjust-volume-and-levels/automatically-duck-audio.html
- [S6] YouTube, paramètres d'encodage recommandés : https://support.google.com/youtube/answer/1722171?hl=en
- [S7] ElevenLabs, guide des effets sonores : https://elevenlabs.io/docs/eleven-creative/playground/sound-effects
- [S8] HeyGen, skill officiel `hyperframes-audio` : https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes-audio/SKILL.md
