# Contrôles techniques du studio

Créés le 15/10/2026 (validé sur AA) et testés sur les rendus de l'épisode 003 d'AA. Les écarts de la chaîne, dans `direction/ECARTS.md`, l'emportent sur les règles par défaut citées ci-dessous.
- **Garanties** : aucun script n'écrase un fichier ; tous refusent si la sortie existe.
- **Limite** : les mesures ne valent jamais une écoute ni un visionnage (statuts du `CLAUDE.md` racine de la chaîne).
- **Lancement** : depuis la racine de la chaîne, avec `python -I -B` et le chemin du script dans le plugin (`${CLAUDE_PLUGIN_ROOT}/outils/controle/…`). FFmpeg est trouvé dans `HYPERFRAMES_FFMPEG_PATH`, le `PATH` ou l'installation WinGet.

## `controle.py` : une commande, onze contrôles
| Contrôle | Commande | Ce qu'on attend | Référence |
|---|---|---|---|
| Niveau du MP4 livré | `controle.py niveau FILM.mp4` | −16 LUFS ±1, crête vraie ≤ −1,5 dBTP | `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 3 |
| Planche contact | `controle.py planche FILM.mp4 --sortie DOSSIER [--pas 2]` | À relire : aucune image immobile plus de 1 s, lisibilité, couleurs, photos. L'étiquette donne le temps exact de chaque image (échantillonnage par numéro d'image, corrigé le 15/10/2026) | `${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 ter |
| Vibration (zone fixe) | `controle.py vibration FILM.mp4 --zone L:H:X:Y [--debut S --duree S] [--extraire T]` | Sur une zone censée être immobile : pas d'alternance régulière (exemple AA : le grain de l'E001 donne une moyenne de 1,5 à 2). Le contrôle signale un écart au-delà de 30 % d'alternances nettes ; `--extraire` enregistre 10 images consécutives à regarder | Porte B |
| **Tremblement** (16/10/2026) | `controle.py tremblement FILM.mp4 [--debut S --duree S]` (`--brut F.npz` enregistre les mesures, `--depuis F.npz` les réanalyse sans relire le film) | Aucune seconde signalée. Le contrôle mesure le déplacement réel de l'image sur 28 tuiles de 256 px, par corrélation sous-pixel. Il signale deux signatures : les **marches** (déplacements de 0 ou 1 px de même sens : arrondi au pixel pendant une dérive lente) et les **allers-retours** (tremblement). Chaque seconde signalée se vérifie sur dix images (`vibration --extraire T`) : un cran se voit sur un texte ou une photo nette, presque pas sur un fond flou. Environ 10 min par film de 80 s | `REFERENTIEL_QUALITE_REALISATION.md` § 2 ter |
| **Son** (16/10/2026) | `controle.py son FILM.mp4 --reference PISTE_MIXEE.wav --voix STEM_VOIX.wav` | Aucun trou ni écrêtage ; aucun écart créé au rendu (gain MP4 / piste ≈ 0 dB ; +6 dB = double lecture) ; aucun clic isolé dans la voix. Un écart autour d'une attaque très brusque de la piste vient de l'AAC (pré-écho) et renvoie aux clics isolés | `DIRECTION_AUDIO.md` § 5 |
| Couleurs retirées des films | `controle.py couleurs index.html [autres…]` | Aucune des couleurs retirées des films par `marque/README.md` de la chaîne (hex ou rgb), sauf la signature et l'outro (exemple AA : corail, charbon, ivoire) | `marque/README.md` |
| Photos répétées | `controle.py doublons DOSSIER_SEQ1/media DOSSIER_SEQ2/media …` | Aucune photo, même redimensionnée (empreinte perceptive), dans deux séquences. Les fonds (`matieres/`, papier, brume, grain, logo, polices) et les photos copiées mais non citées dans un `.html` sont ignorés | § 2 ter |
| Licences en attente | `controle.py licences DOSSIER […]` | Liste les lignes des `PROVENANCE.md` qui citent CC BY-SA ou une licence à vérifier (défaut, celui d'AA : CC BY-SA, domaine public argentin ou brésilien, CC BY 2.0 BR). Une chaîne écrit sa propre liste dans `direction/licences.json` (`{"en_attente": ["regex", …]}`, qui remplace le défaut ; ajouté le 30/10/2026). C'est un signal à relire, pas une exclusion : la règle par défaut (§ 2 bis) admet les médias non libres en citation encadrée. Une ligne « exclu » est normale | Brief de l'épisode |
| Voix / reste (1–4 kHz) | `controle.py voix-reste VOIX.wav RESTE.wav` | Médiane ≥ 12 dB ; fenêtres sous 12 dB listées | `DIRECTION_AUDIO.md` § 5 |
| Chrome de HyperFrames | `controle.py chrome` | 0 après un rendu ; ne jamais arrêter le Chrome d'un rendu parallèle | `CLAUDE.md` racine de la chaîne |
| Bilan rapide | `controle.py tout FILM.mp4 --projet DOSSIER_DU_PROJET` | Niveau, couleurs, licences et Chrome d'un coup | — |

Code de sortie : 0 = rien à signaler ; 1 = écart signalé ou erreur d'entrée (film illisible, sortie déjà présente) ; 2 = usage (arguments invalides, fichier introuvable).

## `ralentir.py` : ralentir une narration
`python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/ralentir.py PRISE.mp3 SORTIE.wav`

C'est la méthode validée sur AA le 15/10/2026 (`DIRECTION_AUDIO.md` § 2) :
- tempo ×0,97 par défaut depuis le 26/10/2026 (×0,94 jusqu'à l'E008 v1 d'AA) ;
- pauses allongées de 0,15 ou 0,25 s :
  - par un silence au plancher, placé au point le plus calme de la pause ;
  - plus de recopie depuis le 17/10/2026 : elle doublait la fin des mots dans les bandes des E003 et E004 d'AA (étude AA, 17/10/2026) ;
- auto-contrôle : aucune recopie exacte dans la bande, sinon rien n'est écrit ;
- −19 LUFS mono ;
- un fichier `SORTIE.positions.txt`.

Sa version du 15/10/2026 redonnait exactement la bande de la séquence 6 de l'E003 d'AA (61,31 s → 71,17 s). Depuis le 17/10/2026, la durée et la place des mots sont les mêmes, et seul le contenu des pauses change. Ne jamais l'appliquer aux voix jouées (chants, citations).

## `transcrire.py` : la prise colle-t-elle au texte ?
`python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/transcrire.py PRISE.mp3 --modele CHEMIN/ggml-base.en.bin --sortie DOSSIER [--texte TEXTE.txt]`

`… --isoler DEBUT DUREE` vérifie un passage douteux.

**Sorties** :
- le texte ;
- les mots horodatés. **Attention (16/10/2026)** : sur une bande ralentie, les débuts arrivent jusqu'à 1,6 s trop tôt, et chaque mot est collé au précédent. Recaler sur les vrais départs de la voix avant de les donner aux producteurs (exemple AA : la bande voix de l'E004) ;
- les phrases ;
- avec `--texte`, la liste des écarts. Les balises ElevenLabs du texte sont ignorées.

**Limites** :
- **Faux écarts attendus** : nombres en chiffres (« 113th »), accents perdus (« Maracana »), noms approximatifs.
- **Doublons et mots étranges** : à vérifier par `--isoler`. Exemple AA, sur l'E003 : « Germany are well-known world champions » était en réalité « Germany are world champions ».
- **Modèle** : le modèle `ggml` est gardé hors du projet ; tout téléchargement se fait avec l'accord du propriétaire. En octobre 2026, sur AA, il se trouvait dans le dossier temporaire de session de Claude : une nouvelle session devra le retrouver ou le retélécharger (148 Mo, licence MIT).

## `publication.py` : le dossier de publication YouTube (16/10/2026)
Bibliothèque standard seule ; il lit et affiche, n'écrit rien. Méthode : skill `studio-faceless:youtube-seo`.
- `publication.py verifier PUBLICATION_vN.md [--journal <nom>-voix.log.txt] [--srt F.srt] [--exclure MOT …] [--requete "…"]` : titres ≤ 100 caractères, description ≤ 5 000 octets, tags ≤ 500 caractères au compte de YouTube, chevrons, chapitres (`0:00`, ≥ 3, ≥ 10 s), hashtags, mots exclus, SRT.
- `publication.py chapitres <nom>-voix.log.txt --titre seq1="…" [--repere seq4:66.5="…"]` : chapitres prêts à coller, depuis le journal du collage en voix seule (écrit par `assembler.py`, lignes « seqN t s → », pas celui de `mix_film.py`).
- `publication.py mot mots-seqN.json "premiers mots"` : temps d'une phrase dans une bande voix.

Testé sur l'E003 d'AA le 16/10/2026 : 0 écart ; il retrouve les chapitres et les 417 caractères de tags du dossier fait à la main.

## Outils versés de Maps & Means le 30/10/2026 (validés sur MM)
Tous : bibliothèque standard, numpy ou FFmpeg, aucun appel réseau ; refusent d'écraser. Les réglages de MM sont des valeurs par défaut, à régler par chaîne (`direction/ECARTS.md`).

| Outil | Rôle | Commande (depuis la racine de la chaîne) | Validé sur MM |
|---|---|---|---|
| `script.py` | Contrôle d'un script avant la voix : relances, chiffres, noms nouveaux, révélations, renversement, ancrages, modes de récit, « you », expressions relatives au jour (evergreen). Seuils de MM par défaut, réglables par `direction/script_seuils.json` de la chaîne ou `--seuils` | `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/script.py SCRIPT.md [--mpm 140] [--detail] [--seuils F.json]` | 23/10/2026 (evergreen 26/10, modes de récit 29/10, provisoire) |
| `pauses.py` | Ajoute du silence dans les silences d'une narration (voix intacte), décale les repères | `… pauses.py SOURCE SORTIE PAUSES.json N [N…]` | 21/10/2026 |
| `raccourcir.py` | Pendant inverse : ramène les pauses à une part de leur longueur (défaut 60 %, plancher 0,25 s), fenêtres gardées en option | `… raccourcir.py SOURCE SORTIE [--sequences 1-7] [--part 0.6] [--plancher 0.25] [--gardes G.json]` | 26/10/2026 |
| `recaler.py` | Recale les repères mot à mot d'une bande ralentie (Whisper par morceaux, silences, alignement sur le texte) ; utilise `transcrire.py` | `… recaler.py BANDE.wav TEXTE.txt MODELE SORTIE_DOSSIER NOM` | 19/10/2026 |

`remix.py` de MM n'est pas versé : il suppose un `mix.py` par séquence, que le gabarit v3 du plugin n'a pas (le son du film se mixe à la fin avec `montage/mix_film.py`). `recaler.py` ne se confond pas avec `outils/shorts/recaler.py` (repères d'un short). `pauses.py`, `raccourcir.py` et `recaler.py` lisent et écrivent les repères `seqN-mots.json` et `seqN-phrases.txt`.

## `mesurer_sons.py` : un son de bibliothèque avant emploi (0.6.0, validé sur AA le 02/11/2026)
`python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/mesurer_sons.py FICHIER [FICHIER …] [--whisper CHEMIN/ggml-base.en.bin] [--crete-max 0] [--boucle]`

Généralisé de `mesurer_sons.py` de l'E011 d'AA (sons Soundza). Par fichier : codec, fréquence d'échantillonnage, canaux, profondeur, durée, niveau intégré (LUFS), crête vraie (dBTP), part de l'énergie entre 1 et 4 kHz, raccord de boucle (énergie des 100 premières et dernières ms), puis une liste « À VOIR » : codage 8 bits (μ-law), fréquence sous 32 kHz, crête vraie au-dessus de `--crete-max` (0 dBTP par défaut ; un son à +0,7 dBTP a été écarté sur AA), écart de boucle au-delà de 1,5 dB avec `--boucle`, **parole possible** avec `--whisper`.
- **Parole** : le filtre `whisper` de FFmpeg transcrit le fichier (modèle ggml gardé hors du projet, comme pour `transcrire.py` ; tout téléchargement avec l'accord du propriétaire). Les étiquettes de bruit de Whisper (« [Music] », « (crowd cheering) », « [Applause] ») sont retirées ; s'il reste des mots, le fichier est signalé et le propriétaire l'écoute. Un modèle anglais ne reconnaît pas un chant dans une autre langue : l'absence de mot ne prouve pas l'absence de parole.
- Aucun fichier écrit. Les mesures écartent un son ; elles ne le valident jamais (`DIRECTION_AUDIO.md` § 4 bis et § 5). Python, numpy, FFmpeg et ffprobe (`HYPERFRAMES_FFMPEG_PATH` / `HYPERFRAMES_FFPROBE_PATH`, sinon le `PATH`). Essai : `outils/test_mesurer_sons.py`.

## Ordre conseillé pour une séquence
1. **À réception de la prise** : `transcrire.py --texte`, puis `--isoler` sur chaque écart douteux.
2. `ralentir.py`, puis `transcrire.py` sur la bande ralentie, pour les repères.
3. **Après chaque rendu** : `controle.py tout`, `planche`, `tremblement` sur tout le film, `son --reference --voix`, et `voix-reste` si les pistes séparées existent.
4. **Avant le collage** : `doublons` sur les dossiers `media/` de toutes les séquences.
5. **Écoute et visionnage** : le propriétaire.

## Pourquoi `tremblement` (16/10/2026)
`vibration` compare la luminance moyenne d'une zone, après réduction ×4 et flou. Un tremblement d'un pixel (0, 1, 0, 1…) y donne la même différence à chaque image, donc aucune « alternance ».

Sur une vidéo de test aux défauts connus :

| Défaut du test | `vibration` | `tremblement` |
|---|---|---|
| Tremblement d'1 px | 0 % d'alternances | signalé, 0,89 px |
| Tremblement de 0,5 px | 0 % d'alternances | signalé, 0,44 px |
| Marches de 0,3 px par image | signalé | signalé, 0,33 px |
| Image fixe | rien | rien, 0,006 px |
| Travelling sous-pixel | rien | rien, 0,04 px |

**Sur des rendus réels** (épisode 004 d'AA, 16/10/2026), un simple seuil d'amplitude signalait 40 à 70 s par film, rendus corrigés compris. En cause : le grain qui change à chaque image, et les plans de 2,5D qui se croisent dans une tuile. Seules les signatures font la différence :

| Rendu | Défaut connu | Secondes signalées |
|---|---|---|
| Séquence 4, premier rendu | Texte du panneau « 1,661 » par crans d'1 px (mesuré par le producteur) | 28, dont 48–53 s sur le panneau |
| Séquence 4, `-r2` (rotation de 0,3° des textes) | Corrigé | 9, toutes déjà présentes dans le premier rendu (autres plans, à vérifier) |
| Séquence 5, v1 | En-tête Risen par crans (critique, 68–70 s) | 49, dont 68–76 s sur l'en-tête : beaucoup de dérives lentes y avancent au pixel près |

Les « 0 % d'alternances » des rendus antérieurs ne prouvent donc pas l'absence de vibration.
