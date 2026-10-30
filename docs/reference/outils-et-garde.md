# Outils, garde-fou et règles communes : référence

Une fiche par fichier pour : les contrôles techniques (`outils/controle/controle.py` et son mode d'emploi), les cartes, le rendu, l'archivage, la sauvegarde, le contrôle du dépôt, le suivi des tokens, les hooks (`hooks/`) et les règles communes (`REGLES_STUDIO.md`).

Les fichiers du plugin font foi : en cas d'écart, la fiche se corrige. Les chemins `${CLAUDE_PLUGIN_ROOT}/…` sont relatifs au dossier du plugin installé ; les chemins `direction/`, `marque/`, `episodes/<id>/` sont relatifs à la chaîne.

## Table des matières
- [Conventions de lancement](#conventions-de-lancement)
- [Contrôles techniques](#contrôles-techniques) : `outils/controle/README.md`, `outils/controle/controle.py`
- [Cartes](#cartes) : `outils/cartes/README.md`, `outils/cartes/cartes.py`
- [Rendu](#rendu) : `outils/rendu/rendre_si_libre.sh`
- [Archivage, sauvegarde et dépôt](#archivage-sauvegarde-et-dépôt) : `outils/archiver_episode.py`, `outils/sauvegarde-chaine.ps1`, `outils/verifier_depot.py`
- [Suivi des tokens](#suivi-des-tokens) : `outils/suivi_tokens.py`
- [Garde-fou et injection des règles](#garde-fou-et-injection-des-règles) : `hooks/hooks.json`, `hooks/garde_commandes.py`, `hooks/regles_studio.py`
- [Règles communes](#règles-communes) : `REGLES_STUDIO.md`
- [Workflows liés](#workflows-liés)

Les autres outils sont décrits ailleurs : `ralentir.py` et `transcrire.py` dans [`son.md`](son.md), `publication.py` dans [`publication.md`](publication.md), `outils/montage/` dans [`son.md`](son.md), `outils/shorts/` et `outils/gemini/` dans [`publication.md`](publication.md).

---

## Conventions de lancement
- **Où** : tous les outils se lancent **depuis la racine de la chaîne**. Ils lisent la variable d'environnement `CLAUDE_PROJECT_DIR` (dossier de la chaîne), sinon le dossier courant. Aucun ne travaille dans le dossier du plugin, qui est en lecture seule.
- **Comment** : `python -I -B "<chemin du script>" …`. `-I` isole Python des variables et des modules de l'utilisateur ; `-B` interdit d'écrire du bytecode (`__pycache__`) dans le projet. Exception documentée : `suivi_tokens.py` se lance avec `python -B` (voir sa fiche).
- **Chemin du plugin** : `${CLAUDE_PLUGIN_ROOT}` est remplacé par Claude Code dans les skills, les agents et les hooks, **pas dans l'environnement de Bash**. Dans une commande Bash, on écrit donc le chemin complet (`~/.claude/plugins/cache/studio-faceless/studio-faceless/<version>/outils/…`), tel que le skill l'a déjà reçu remplacé.
- **Windows** : le studio tourne sous Windows avec Git Bash. Plusieurs outils s'appuient sur Windows (voir « À savoir » de chaque fiche : `tasklist`, PowerShell, police Arial).
- **FFmpeg** : trouvé par `HYPERFRAMES_FFMPEG_PATH` (et `HYPERFRAMES_FFPROBE_PATH`), puis le `PATH`, puis l'installation WinGet (`%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*`).
- **Garde-fous des outils** : aucun outil du dossier `outils/` n'écrase un fichier ; ils refusent si la sortie existe.
- **Une mesure n'est pas une écoute** : tous les contrôles se terminent par ce rappel ; les statuts de validation humaine restent au propriétaire.

---

## Contrôles techniques

### outils/controle/README.md
**Rôle** : mode d'emploi des contrôles du studio : `controle.py` (onze contrôles), `ralentir.py`, `transcrire.py`, `publication.py`, avec l'ordre conseillé pour une séquence et l'explication du contrôle « tremblement ».

**Quand il sert** : lu par Claude principal (Studio Director) avant de contrôler un rendu, une prise voix ou un dossier de publication ; relu quand un contrôle signale un écart.

**Contenu**
- **En-tête** : les écarts de la chaîne (`direction/ECARTS.md`) l'emportent sur les règles par défaut citées ; aucun script n'écrase un fichier ; les mesures ne valent jamais une écoute ni un visionnage.
- **`controle.py` : une commande, onze contrôles** : tableau (contrôle, commande, ce qu'on attend, référence) ; codes de sortie 0 / 1 / 2.
- **`ralentir.py`** : tempo ×0,97 par défaut depuis le 26/10/2026 (×0,94 jusqu'à l'E008 v1 d'AA), pauses allongées par un silence au plancher (plus de recopie depuis le 17/10/2026), −19 LUFS mono, fichier `SORTIE.positions.txt`.
- **`transcrire.py`** : prise contre texte, `--isoler DEBUT DUREE`, sorties (texte, mots horodatés, phrases, écarts), faux écarts attendus, modèle `ggml-base.en.bin` gardé hors du projet.
- **`publication.py`** : `verifier`, `chapitres`, `mot` (bibliothèque standard seule ; il lit et affiche, n'écrit rien).
- **Ordre conseillé pour une séquence** : à réception de la prise (`transcrire.py --texte`, puis `--isoler`) ; `ralentir.py` puis `transcrire.py` sur la bande ; après chaque rendu (`tout`, `planche`, `tremblement`, `son`, `voix-reste`) ; avant le collage (`doublons`) ; écoute et visionnage par le propriétaire.
- **Pourquoi `tremblement`** : `vibration` ne voit pas un tremblement d'un pixel ; tableau de calibrage sur vidéo de test, puis résultats sur rendus réels (E004 d'AA).

**Liens** : cite [`REFERENTIEL_QUALITE_REALISATION.md`](../../plugins/studio-faceless/referentiels/REFERENTIEL_QUALITE_REALISATION.md) (§ 2 ter), [`DIRECTION_AUDIO.md`](../../plugins/studio-faceless/referentiels/DIRECTION_AUDIO.md) (§ 3 et § 5), le skill `youtube-seo`. Cité par `rendu-collage.md` du skill `episode` (§ 2), par `DIRECTION_AUDIO.md` § 5 et par [`rendu-et-controle.md`](../workflows/rendu-et-controle.md).

**À savoir**
- Le tableau d'usage ne mentionne pas deux options qui existent dans le code : `planche --colonnes` et `tremblement --seuil` (voir la fiche de `controle.py`).
- Plusieurs exemples sont ceux d'AA (chaîne d'origine : grain de l'E001, corail/charbon/ivoire, domaine public argentin) ; les valeurs propres à une chaîne vivent dans son `marque/` et sa `direction/ECARTS.md`.
- Mode d'emploi source : [`outils/controle/README.md`](../../plugins/studio-faceless/outils/controle/README.md).

### outils/controle/controle.py
**Rôle** : une seule commande, onze contrôles techniques sur un film MP4, des fichiers de composition, des dossiers de médias ou des pistes audio. Aucun contrôle ne modifie un fichier existant.

**Quand il sert** : lancé par Claude principal après chaque rendu de séquence (étape 8 du parcours), après le collage et le mix du film, et avant le collage pour les photos répétées. Le propriétaire ne le lance pas lui-même ; il lit le bilan que Claude lui donne, avec l'écoute et le visionnage qui restent à lui.

**Usage** (depuis la racine de la chaîne, `python -I -B`)
```text
controle.py niveau      FILM.mp4
controle.py planche     FILM.mp4 --sortie DOSSIER [--pas 2] [--colonnes 5]
controle.py vibration   FILM.mp4 --zone L:H:X:Y [--debut S] [--duree S] [--extraire T]
controle.py tremblement FILM.mp4 [--debut S] [--duree S] [--seuil 0.3] [--brut F.npz | --depuis F.npz]
controle.py son         FILM.mp4 [--reference PISTE_MIXEE.wav] [--voix PISTE_VOIX.wav]
controle.py couleurs    index.html [autres fichiers…]
controle.py doublons    DOSSIER_SEQ1 DOSSIER_SEQ2 … [--seuil 6]
controle.py licences    DOSSIER [autres dossiers…]
controle.py voix-reste  VOIX.wav RESTE.wav
controle.py chrome
controle.py tout        FILM.mp4 --projet DOSSIER_DU_PROJET
```
Chaque ligne se préfixe de `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/`.

**Sous-commandes**

| Sous-commande | Ce qu'elle fait | Seuils et options | Écrit |
|---|---|---|---|
| `niveau FILM` | Mesure l'intensité intégrée (LUFS), la crête vraie (dBTP) et la LRA par `ebur128` de FFmpeg ; donne aussi la durée | Cible −16 LUFS ±1 ; crête vraie ≤ −1,5 dBTP ; sortie 1 si l'un des deux est hors plage | rien |
| `planche FILM --sortie DOSSIER` | Planche contact : une image toutes les `--pas` secondes (défaut 2), 480 px de large, temps réel de l'image écrit en jaune, grille `--colonnes` × `--colonnes` (défaut 5 × 5 = 25 images par planche) | Échantillonne par numéro d'image (`pas × fps`) pour que l'étiquette soit le vrai temps de l'image | `DOSSIER/<film>-planche-1.jpg`, `-2.jpg`… ; refuse si une planche du même nom existe |
| `vibration FILM --zone L:H:X:Y` | Sur une zone censée être immobile (largeur:hauteur:x:y en px) : réduction ×4, flou, différence image à image, luminance moyenne ; compte les alternances nettes | Sortie 1 au-delà de 30 % d'alternances nettes ; liste les 8 plus fortes différences ; `--debut`, `--duree` limitent la fenêtre ; `--extraire T` | `--extraire T` : 10 PNG consécutifs dans `<film sans extension>-images-T.TTs/` ; refuse si le dossier existe |
| `tremblement FILM` | Mesure le déplacement réel de l'image, image par image, par corrélation croisée sous-pixel sur 28 tuiles de 256 px (7 × 4, film ramené à 1920 × 1080 en gris) ; signale deux signatures par seconde, tuile et axe | **Marches** : ≥ 90 % des déplacements à 0 ou ±1 px, au moins 2 pas de 1 px de même signe, ≥ 40 % d'images immobiles. **Allers-retours** : ≥ 60 % de paires consécutives de signes opposés, chacune au-dessus de `--seuil` (0,3 px), qui s'annulent à 30 % près. Mesure retenue si pic de corrélation > 0,6, texture suffisante, déplacement < 24 px. Environ 10 min pour 80 s de film | `--brut F.npz` enregistre les mesures (refuse si le fichier existe) ; `--depuis F.npz` réanalyse sans relire le film |
| `son FILM` | Cherche les **trous** (1 à 15 trames de 10 ms sous −60 dB entre deux passages à plus de −35 dB), l'**écrêtage** (échantillons ≥ 0,999) et les **clics isolés** (salve de 6 ms au plus, 20 dB au-dessus du silence précédent, retombée de 15 dB en 10 ms). Les clics sont cherchés dans `--voix`, sinon `--reference`, sinon le film | Avec `--reference` (piste mixée placée dans la composition) : alignement par corrélation sur 20 s (±0,5 s), gain, fidélité par tranches de 50 ms ; un écart (< 12 dB de rapport) est rangé en « attaque étalée par l'AAC » (pas une faute du rendu) ou en « écart créé au rendu » (sortie 1). Sans `--reference` : nombre de sauts de niveau > 12 dB, à titre d'information | rien |
| `couleurs FICHIER…` | Cherche dans des fichiers texte (HTML de composition) les couleurs retirées des films, en hexadécimal ou `rgb()`/`rgba()` | Liste des couleurs lue dans `marque/couleurs_interdites.json` de la chaîne (`{"corail": "#F17462", …}`, six chiffres hexadécimaux) ; sans ce fichier, aucune couleur n'est interdite. Sortie 1 s'il y a une occurrence | rien |
| `doublons DOSSIER…` | Cherche la même photo dans deux séquences : empreinte SHA-1 identique, ou empreinte perceptive dHash (distance de Hamming ≤ `--seuil`, défaut 6 sur 64) | Ignore les fonds (chemins contenant `matieres`, `fonts`, `logo`, `grain`, `fog`, `paper`) et les photos non citées par leur nom dans un `.html` du projet ; ne compare qu'entre dossiers différents. Sortie 1 si une photo se répète | rien |
| `licences DOSSIER…` | Lit tous les `PROVENANCE.md` et liste les lignes qui citent `BY-SA`, `PD-AR`, `PD-Brazil`, `BY 2.0 BR` ou « domaine public argentin » | Liste fixée dans le code (`LICENCES_EN_ATTENTE`). Une ligne « exclu » ou « non utilisé » est normale. Sortie 1 s'il y a une ligne | rien |
| `voix-reste VOIX RESTE` | Compare la voix seule au reste du mix dans la bande 1–4 kHz, par fenêtres de 0,4 s qui contiennent de la voix | Médiane ≥ 12 dB ; liste les fenêtres sous 12 dB ; la sortie 1 ne dépend que de la médiane | rien |
| `chrome` | Compte les processus `chrome-headless-shell.exe` (Chrome de HyperFrames) par `tasklist` | Attendu : 0 après un rendu ; sortie 1 s'il en reste. Ne jamais arrêter le Chrome d'un rendu parallèle | rien |
| `tout FILM --projet DOSSIER` | `niveau` ; `couleurs` sur `*.html` et `compositions/*.html` du projet (s'il y en a) ; `licences` sur le projet ; `chrome` | Ne lance ni `planche`, ni `vibration`, ni `tremblement`, ni `son`, ni `doublons`, ni `voix-reste` : il le rappelle en fin de sortie | rien |

**Fichiers lus** : le film ou la piste donnés ; `marque/couleurs_interdites.json` (pour `couleurs` et `tout`) ; les `PROVENANCE.md` et les `.html` du projet. **Fichiers écrits** : seulement les sorties du tableau.

**Codes de sortie** : 0 = rien à signaler ; 1 = écart signalé ou erreur d'entrée (film illisible, sortie déjà présente ; message à l'écran) ; 2 = usage (arguments invalides, fichier introuvable). Le README de l'outil le dit ainsi depuis le 28/10/2026.

**Dépendances** : Python, `numpy` (obligatoire à l'import ; installé par le `requirements.txt` du squelette de chaîne, `numpy>=2.4`), FFmpeg et ffprobe. **Variables d'environnement** : `HYPERFRAMES_FFMPEG_PATH`, `HYPERFRAMES_FFPROBE_PATH`, `CLAUDE_PROJECT_DIR`, `LOCALAPPDATA`.

**Liens** : mode d'emploi [`outils/controle/README.md`](../../plugins/studio-faceless/outils/controle/README.md) ; référentiels [`REFERENTIEL_QUALITE_REALISATION.md`](../../plugins/studio-faceless/referentiels/REFERENTIEL_QUALITE_REALISATION.md) (§ 2 ter, porte B) et [`DIRECTION_AUDIO.md`](../../plugins/studio-faceless/referentiels/DIRECTION_AUDIO.md) (§ 3, § 5) ; `marque/README.md` de la chaîne ; workflow [`rendu-et-controle.md`](../workflows/rendu-et-controle.md).

**À savoir**
- **Un code 1 ne veut pas toujours dire « écart »** : les erreurs coupées par message (pas de piste son, planche déjà présente, dossier d'images déjà présent, fichier de mesures déjà présent, aucune mesure, aucune fenêtre avec voix) sortent aussi avec le code 1 (le README de l'outil le dit désormais). Lire le message avant de conclure à un défaut du film.
- **Séquence en voix seule** : avant le mix du film, une séquence n'a pas de cible de sonie (`rendu-collage.md` § 2). `niveau` et `tout` appliquent pourtant −16 LUFS : un « ÉCART : intensité hors plage » y est donc attendu et ne se corrige pas. À vérifier sur un rendu réel.
- **`tremblement`** : une seconde signalée n'est pas un défaut prouvé. Elle se vérifie sur dix images (`vibration --extraire T`) : un cran d'un pixel se voit sur un texte ou une photo nette, presque pas sur un fond flou. Il signale aussi les secondes où une coupe mêle des pas de 0 et de 1 px (`pieges.md`). Les « 0 % d'alternances » de `vibration` ne prouvent pas l'absence de vibration.
- **`planche`** : le filtre `drawtext` utilise la police `C:/Windows/Fonts/arial.ttf`. `pieges.md` (§ Technique, E009) signale qu'un chemin de police Windows a fait échouer `drawtext` : des planches ont dû être faites sans étiquettes. À vérifier avant de s'y fier sur une autre machine.
- **`chrome`** utilise `tasklist` : Windows seulement.
- **`couleurs`** : la signature et l'outro gardent les couleurs de marque ; une occurrence dans leurs fichiers est normale.
- **`licences`** : la liste de licences en attente est celle d'AA (domaine public argentin ou brésilien, CC BY 2.0 BR) ; elle est dans le code, pas dans la chaîne. Une autre chaîne devra la modifier dans le plugin.
- **`doublons`** : un même cliché volontairement rappelé doit être consigné dans le README de la chaîne ou le brief ; l'outil ne sait pas distinguer un rappel voulu d'une répétition.
- **`son`** : sans `--voix`, la musique masque une partie des clics de la voix.
- Calibrages datés de 15 et 16/10/2026 (E003 et E004 d'AA).

---

## Cartes

### outils/cartes/README.md
**Rôle** : mode d'emploi de `cartes.py` : schéma de la spécification JSON, choix de projection, limites, et correction d'une erreur de lecture constatée sur l'E007 d'AA (« la carte du monde étire la latitude d'un facteur 1,43 », fausse).

**Quand il sert** : lu par Claude principal quand il prépare le socle d'un épisode (`socle.md` du skill `episode`, étape 5) pour fabriquer les cartes d'un lieu qui porte l'argument ; relu par un producteur qui hésite sur une projection.

**Contenu**
- **Commande** et remarque : le shapefile Natural Earth n'est pas dans `outils/` ; il se télécharge pour l'épisode avec l'accord du propriétaire (le `.dbf` à côté du `.shp`).
- **Spécification** : une carte, une liste ou `{"cartes": [...]}` ; clés `nom`, `projection`, `emprise`, `lat_ref`, `pays`, `classe_pays`, `voisins`, `villes`, `pas_min` (détail dans la fiche de `cartes.py`).
- **Projections** : `equirectangulaire` (cartes régionales ; même échelle sur les deux axes ; formes justes au centre, à 10 % près aux bords) et `equal-earth` (monde ; cadre 1920 × 840 px pour −58° à 84°).
- **La remarque « 1,43 »** : démonstration chiffrée que le SVG du kit de l'E007 était en plate carrée (5,333 px par degré sur les deux axes) et que la « correction » du producteur (y × 0,70123) a aplati la carte de 30 %.
- **Limites** : polygones seulement, pas de découpe au cadre, antiméridien non recousu avec `equal-earth`, noms de pays de Natural Earth (anglais, champ `ADMIN`).

**Liens** : cité par `socle.md` (§ cartes) et `pieges.md` (carte du monde « corrigée ») du skill `episode`.

**À savoir** : ne jamais redresser une carte du kit d'un facteur ; lire `cadre_px` et l'échelle dans `villes-px.json`. Pour le monde, `equal-earth` ; pour un pays, l'équirectangulaire avec `lat_ref` au milieu de l'emprise. Source : [`outils/cartes/README.md`](../../plugins/studio-faceless/outils/cartes/README.md).

### outils/cartes/cartes.py
**Rôle** : tire une carte au trait SVG de 1920 × 1080 et les positions des villes en pixels à partir d'un shapefile Natural Earth admin 0 (domaine public), selon une spécification JSON. Daté du 24/10/2026, repris de l'outil de l'E007 d'AA.

**Quand il sert** : lancé par Claude principal pendant le socle de l'épisode, avant les producteurs ; les producteurs utilisent ensuite le SVG et `villes-px.json` du kit.

**Usage**
```text
python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/cartes/cartes.py SPEC.json --shp episodes/<id>/kit/donnees/ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp --out episodes/<id>/kit/donnees
```
| Argument | Rôle |
|---|---|
| `SPEC.json` | Spécification (une carte, une liste ou `{"cartes": [...]}`) |
| `--shp` (obligatoire) | Fichier `.shp` Natural Earth admin 0 ; le `.dbf` doit être à côté |
| `--out` (obligatoire) | Dossier où créer un sous-dossier par carte |

**Clés d'une carte**
| Clé | Sens | Défaut |
|---|---|---|
| `nom` | Nom de la carte et du sous-dossier | — (obligatoire) |
| `projection` | `equirectangulaire` ou `equal-earth` | `equirectangulaire` |
| `emprise` | `{"lon": [min, max], "lat": [min, max]}` | — (obligatoire) |
| `lat_ref` | Latitude de référence (équirectangulaire) : x = longitude × cos(`lat_ref`) | milieu de l'emprise |
| `meridien_central` | Méridien central (`equal-earth`) | milieu de l'emprise |
| `pays` | Pays du récit (noms du champ `ADMIN`) | aucun |
| `classe_pays` | Classe CSS des pays du récit | `focus` |
| `voisins` | Liste fermée des autres pays tracés ; absent : tous les pays dont l'emprise touche le cadre à 2° près | absent |
| `classe_voisins` | Classe CSS des voisins | `voisin` |
| `villes` | `{"nom": [longitude, latitude]}` | aucune |
| `pas_min` | Écart minimal entre deux points d'un tracé, en pixels (1,5 pour le monde) | 0 |
| `champ_nom` | Autre champ du `.dbf` que `ADMIN` | `ADMIN` |

**Sorties** (par carte) : `<out>/<nom>/<nom>.svg` (traits en `currentColor`, identifiants `<classe>-<pays>` en minuscules avec tirets, cercles `ville-<nom>` de rayon 7) et `<out>/<nom>/villes-px.json` (source, projection, échelle en pixels par degré, `cadre_px` = rectangle occupé par l'emprise, `villes_px`).

**Fichiers lus** : la spécification, le `.shp` et le `.dbf`. **Écrits** : les deux fichiers par carte ; refuse d'écraser (message, sortie 1). Sort aussi en erreur si un pays de `pays` ou `voisins` n'est pas dans le shapefile, si le champ n'existe pas dans le `.dbf` ou si la projection est inconnue.

**Dépendances** : Python seul (lecture directe du shapefile par `struct`). **Échelle** : la mention « 1:10m », « 1:50m » ou « 1:110m » du commentaire SVG se déduit du nom du fichier (`_10m_`, `_50m_`, `_110m_`).

**Liens** : [`outils/cartes/README.md`](../../plugins/studio-faceless/outils/cartes/README.md) ; `socle.md` du skill `episode`.

**À savoir** : l'emprise est inscrite dans 1920 × 1080 et centrée : si son rapport n'est pas 16:9, il reste des bandes vides (lire `cadre_px`). Seuls les polygones sont lus. Le SVG ne découpe pas au cadre : les tracés qui sortent sont coupés par le `viewBox`.

---

## Rendu

### outils/rendu/rendre_si_libre.sh
**Rôle** : lance un `render.sh` seulement quand aucun autre rendu HyperFrames ne tourne sur la machine (toutes sessions confondues) ; sinon attend et revérifie.

**Quand il sert** : lancé par Claude principal (Studio Director), en **tâche suivie**, pour chaque rendu de séquence (étape 8). Une file de plusieurs séquences s'enchaîne dans une seule tâche suivie, jamais en tâche détachée (aucune notification).

**Usage** (depuis la racine de la chaîne, Git Bash)
```text
bash ${CLAUDE_PLUGIN_ROOT}/outils/rendu/rendre_si_libre.sh episodes/<id>/production/<séquence>-vN/render.sh episodes/<id>/production/<séquence>-vN/rendu.log.txt
```
| Argument | Rôle |
|---|---|
| `<render.sh>` | Script de rendu de la séquence (chemin absolu ou relatif à la racine de la chaîne) |
| `<journal>` | Fichier où le script note ses mesures, son lancement et son code de fin |

**Déroulement**
1. Dossier de travail : `CLAUDE_PROJECT_DIR`, sinon le dossier courant.
2. Jusqu'à 144 passes : mesure par PowerShell (WMI) le processeur (6 relevés à 3 s), la mémoire libre, et le nombre de processus `node.exe` dont la ligne de commande correspond à `hyperframes.mjs … render` ; écrit une ligne au journal.
3. Si ce nombre est **0** : écrit « machine libre : lancement », fait `cd` vers la racine de la chaîne, lance `bash <render.sh>` en ajoutant sa sortie au journal, note le code de fin et l'affiche (`tail -2`).
4. Sinon : attend 300 s (5 min) et recommence.
5. Après 144 passes (environ 12 h) : « Attente de 12 h dépassée, rien n'a été lancé », code 3.

**Code de sortie** : celui du `render.sh` quand il a été lancé ; 3 si l'attente est dépassée.

**Dépendances** : Git Bash, PowerShell (`powershell -NoProfile`, WMI), `sed`, `tr`, `date`, `tail`.

**Liens** : `render.sh` du [gabarit de séquence v3](../../plugins/studio-faceless/templates/sequence-gabarit-v3/render.sh) ; `rendu-collage.md` § 1 et `pieges.md` du skill `episode` ; [`rendu-et-controle.md`](../workflows/rendu-et-controle.md).

**À savoir**
- **Les conditions de processeur et de mémoire sont retirées** (validé sur AA, 24/10/2026) : elles sont seulement relevées au journal. Seul le nombre de rendus en cours décide.
- **Une mesure en échec bloque la file** : si PowerShell ne répond pas, le nombre de rendus est lu comme occupé (valeur par défaut 1) et le script attend. Vérifier le journal avant de conclure que la machine est occupée.
- Le journal et le `render.sh` en chemin relatif se lisent depuis la racine de la chaîne : lancer la commande depuis cette racine.
- Une passe dure environ 18 s de mesure plus 300 s d'attente.
- `TaskStop` sur la tâche ne tue pas le `node` enfant : `taskkill //T //F //PID` (`pieges.md`).
- Un rendu arrêté sans message (code 1) se relance une fois à l'identique, avec un nouveau journal, avant de chercher la cause (`pieges.md`, E009).
- Les premières lignes du fichier contiennent un commentaire d'en-tête dupliqué (cosmétique).

---

## Archivage, sauvegarde et dépôt

### outils/archiver_episode.py
**Rôle** : range un épisode terminé : la vidéo finale et ses composants vont dans un zip vérifié ; les essais et les originaux zippés sont déplacés dans `_A_SUPPRIMER/<épisode>/` ; seuls les fichiers de la racine de l'épisode restent en place. **Rien n'est supprimé.**

**Quand il sert** : étape 11 du parcours, après la publication, ou avant la mise en ligne si le propriétaire le demande une fois le master approuvé (`etapes.md` § 13). Lancé par Claude principal : d'abord l'**aperçu**, puis `--executer` **seulement avec l'accord du propriétaire**. Le propriétaire supprime lui-même `_A_SUPPRIMER/<épisode>/`.

**Usage** (depuis la racine de la chaîne)
```text
python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/archiver_episode.py episodes/<id>                 aperçu : n'écrit et ne déplace rien
python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/archiver_episode.py episodes/<id> --executer      zip, vérification, déplacements, ARCHIVE.md
```
| Argument | Rôle |
|---|---|
| `episode` | Dossier de l'épisode ; doit être **directement** sous `episodes/` de la chaîne |
| `--executer` | Exécute pour de bon (sinon aperçu) |
| `--master CHEMIN` | Master final, si `outputs/` n'en contient pas ou pour choisir entre le film mixé et le film en voix seule |
| `--garder CHEMIN` (répétable) | Retire de la liste des essais un chemin (et ce qui le contient ou qu'il contient) |
| `--essai CHEMIN` (répétable) | Ajoute un chemin aux essais (motif « désigné par --essai ») |

**Ce que les règles classent en essais** (seulement quand c'est certain ; dans le doute, le fichier va dans le zip)
- masters d'une autre version que le master final (`master remplacé`), sauf les fichiers d'un MP4 cité par le journal du master (le film en voix seule `…-voix.*` d'où le master est mixé), qui sont gardés ;
- projets de production d'un groupe `…-vN` dont une autre version entre au master final (`version non retenue`), scripts `montage-*` qui n'ont pas produit le master (`montage non retenu`), dossiers de production commençant par `essai` ou `test` (`essai`) ;
- MP4 d'un projet retenu qui ne figurent pas au master (`rendu non retenu`) ;
- captures de contrôle : sous-dossiers `planche`, `planches`, `controle`, `controles`, `snapshots`, `captures` d'un projet ; `outputs/controle*` ; `controle-planche*` dans un dossier `miniature*` (`captures de contrôle`) ; `pistes/essai*` d'un projet (`essai de mix`) ;
- dossiers de la racine de l'épisode commençant par `da-test`, `essai` ou `test` (`test de direction artistique`) ;
- `PUBLICATION_vN.*` quand une version plus haute existe (`dossier de publication remplacé`).

Les rendus « retenus » sont les MP4 cités par le journal du master (`<master>.log.txt`) et par le montage final : `episodes/<id>/montage/` (parcours v3 : ses scripts et ses `.json`, dont `montage.json`) ou le dossier `production/montage-*` dont un script cite le master (gabarits plus anciens).

**Exécution** (ordre garanti)
1. Refuse si le zip, `essais_<date>` ou `originaux_<date>` existe déjà, si la place libre est inférieure à 1,1 × la taille du zip + 1 Go, ou si un `.partiel` d'une exécution précédente traîne.
2. Écrit `episodes/<id>/<id>_archive_<AAAA-MM-JJ>.zip.partiel` (formats déjà compressés stockés tels quels, le reste en deflate niveau 6).
3. **Relit** le zip en entier : CRC de chaque fichier, liste et tailles identiques à la source. En cas d'échec, rien n'est déplacé et le `.partiel` est laissé pour examen.
4. Renomme le zip, affiche le SHA-256.
5. Déplace les essais vers `_A_SUPPRIMER/<id>/essais_<date>/<chemin relatif>` et chaque dossier restant de l'épisode vers `_A_SUPPRIMER/<id>/originaux_<date>/<dossier>`.
6. Écrit `episodes/<id>/ARCHIVE.md` (zip, SHA-256, master, essais par motif, restauration) et en copie un `LISEZMOI_<date>.md` dans `_A_SUPPRIMER/<id>/`.

**Fichiers lus** : tout l'épisode. **Écrits** : le zip, `ARCHIVE.md`, `_A_SUPPRIMER/<id>/…`. **Dépendances** : bibliothèque standard seule. **Codes de sortie** : 0 en fin normale (aperçu compris) ; 1 sur toute erreur annoncée par message (aucun master, master introuvable, règle incohérente, existe déjà, place insuffisante, zip partiel, zip non conforme).

**Liens** : [`etapes.md`](../../plugins/studio-faceless/skills/episode/references/etapes.md) § 13 (répartition détaillée corbeille / zip / hors du zip, `VALIDÉ` sur AA le 28/10/2026) ; [`sauvegarde-chaine.ps1`](../../plugins/studio-faceless/outils/sauvegarde-chaine.ps1) (conseillé avant la première exécution) ; workflow [`archivage-et-sauvegarde.md`](../workflows/archivage-et-sauvegarde.md).

**À savoir**
- **L'outil ne reconnaît pas seul** `_etude`, `_rendu-N`, `planche-1`, `controle-planche`, ni les médias et les voix de l'épisode : il faut un `--essai` par chemin de la corbeille, et noter la commande dans l'`ARCHIVE.md` (`etapes.md` § 13).
- **Master** : sans `--master`, il prend la plus haute version de `outputs/*master-v*.mp4`. Le film en voix seule de même version porte le même numéro : donner `--master` vers le master mixé pour lever l'ambiguïté.
- **Montage** (réglé le 29/10/2026, D3) : l'outil reconnaît `episodes/<id>/montage/` (parcours v3) comme montage final et lit ses `.json` (`montage.json`) pour trouver les séquences retenues ; il reconnaît aussi un dossier `production/montage-*` qui cite le master. L'aperçu n'affiche « Montage final : non trouvé » que si aucun des deux n'existe. Testé sur l'aperçu de l'E010 d'AA le 29/10/2026 : montage trouvé, séquences retenues trouvées, film en voix seule gardé. Pas encore essayé sur une chaîne neuve.
- **Restauration** : dézipper l'archive dans l'épisode redonne les dossiers à l'identique ; avant que le propriétaire vide `_A_SUPPRIMER/`, tout se restaure en remettant les dossiers à leur place.
- `.gitignore` de la chaîne ignore `_A_SUPPRIMER/`, `*.zip` et `*.partiel` : l'archive reste hors du dépôt Git ; elle est dans `episodes/`, donc dans la sauvegarde datée.
- Le texte de `ARCHIVE.md` cite « validé sur AA, 21/10/2026 » : c'est la date de la règle d'origine.

### outils/sauvegarde-chaine.ps1
**Rôle** : copie datée de la chaîne vers un disque ou un dossier choisi, vérifiée fichier par fichier par empreinte SHA-256, sans rien supprimer ni remplacer.

**Quand il sert** : lancé par Claude principal ou par le propriétaire après chaque livraison validée, et avant toute mise à jour d'outil (Node, HyperFrames, FFmpeg) ; jamais automatiquement. Conseillé avant la première exécution de l'archivage. C'est lui qui garde les médias que le dépôt Git ne contient pas.

**Usage** (depuis la racine de la chaîne, PowerShell 5.1 ou 7)
```text
powershell -File ${CLAUDE_PLUGIN_ROOT}/outils/sauvegarde-chaine.ps1 -Destination E:\Sauvegardes -Simulation
powershell -File ${CLAUDE_PLUGIN_ROOT}/outils/sauvegarde-chaine.ps1 -Destination E:\Sauvegardes
powershell -File ${CLAUDE_PLUGIN_ROOT}/outils/sauvegarde-chaine.ps1 -Destination E:\Sauvegardes -Elements marque,direction
```
| Paramètre | Rôle |
|---|---|
| `-Destination` (obligatoire) | Dossier où créer la sauvegarde ; refusé s'il est dans la chaîne |
| `-Chaine` | Dossier de la chaîne ; défaut : le dossier courant |
| `-Simulation` | Liste les fichiers, le volume par dossier et la destination prévue ; ne copie rien |
| `-Elements` | Liste à copier ; défaut : `episodes`, `marque`, `direction`, `templates`, `.claude`, `CLAUDE.md`, `package.json`, `package-lock.json`, `requirements.txt` |

**Déroulement** : découpe `-Elements` (les virgules d'un appel par `-File` arrivent en une seule chaîne) ; ignore avec un avertissement un élément absent ; exclut `node_modules` et `__pycache__` ; vérifie la place libre (volume × 1,05) ; crée `<nom du dossier de la chaîne>_AAAA-MM-JJ_HHMM` sous la destination (refuse s'il existe) ; pour chaque fichier, copie, calcule le SHA-256 de la source et de la copie, **s'arrête** au premier écart ; écrit `MANIFEST.sha256.txt` (une ligne `empreinte  chemin/relatif` par fichier, avec une ligne d'en-tête) ; affiche l'avancement tous les 200 fichiers.

**Fichiers lus** : les éléments de la chaîne. **Écrits** : le dossier daté et son manifeste, à la destination seulement. **Code de sortie** : non nul sur toute erreur (le script s'arrête à la première).

**Restauration** : à la main, en copiant les fichiers voulus depuis le dossier daté ; le manifeste donne leur empreinte.

**Liens** : [`archiver_episode.py`](../../plugins/studio-faceless/outils/archiver_episode.py) ; workflow [`archivage-et-sauvegarde.md`](../workflows/archivage-et-sauvegarde.md) ; `.gitignore` du squelette (les médias vont dans la sauvegarde externe).

**À savoir**
- **Hors liste par défaut** : `docs/`, `.githooks/`, `.gitignore`, `.gitattributes`, `README.md`, `INSTALLATION.md`, `outils/` de la chaîne. Ce sont des fichiers texte, gardés par Git ; ajouter ces noms à `-Elements` pour les copier aussi. Les zips d'archive sont dans `episodes/` : ils sont dans la sauvegarde par défaut, `_A_SUPPRIMER/` ne l'est pas.
- Un élément absent de la chaîne (par exemple `templates`, qui est dans le plugin pour une chaîne neuve) donne un avertissement, pas une erreur.
- Une destination synchronisée (OneDrive…) envoie les fichiers en ligne : à décider par le propriétaire.
- Le volume de ~3,9 Go donné dans l'en-tête est celui d'AA au 28/10/2026.
- Si un écart d'empreinte arrête la copie, le dossier daté reste partiel : ne pas le prendre pour une sauvegarde valide (absence de `MANIFEST.sha256.txt`).

### outils/verifier_depot.py
**Rôle** : contrôle des fichiers à committer dans le dépôt Git de la chaîne : refuse un gros fichier hors Git LFS, un média d'épisode, un secret probable, un chemin propre à une machine dans un fichier de code actif et, depuis la 0.2.3, un `REGLES_STUDIO.md` de plus de 9 000 caractères.

**Quand il sert** : lancé automatiquement par le crochet `.githooks/pre-commit` de la chaîne avant chaque commit ; lancé à la main par Claude principal avant un envoi (`--tout`) ou pour comprendre un refus.

**Usage** (depuis la racine de la chaîne)
```text
python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/verifier_depot.py          fichiers indexés (git add), comme le crochet
python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/verifier_depot.py --tout   tous les fichiers que Git suivrait (suivis + nouveaux non ignorés)
```
**Contrôles**
| Contrôle | Règle |
|---|---|
| Taille | Plus de 10 Mo (10 × 1024 × 1024 octets) sans le filtre `lfs` (lu par `git check-attr filter`) : refus |
| Média d'épisode | Un fichier sous `episodes/` d'extension vidéo, son, image, police, `.pdf` ou `.zip` : refus (sauvegarde externe, pas dépôt) |
| Secret probable | Clés `sk-…`, `sk_…` (dont `sk_live_…`, `sk_test_…`) en début de jeton, c'est-à-dire non précédées d'une lettre, d'un chiffre, de `_` ou de `-` (« risk-… », « task-… » ou une URL en « dsk-… » ne sont pas des clés), `xi-api-key: …`, `api_key: '…'`, jetons `ghp_…` et `github_pat_…`, `-----BEGIN … PRIVATE KEY-----`, en-tête `Bearer …` ; les valeurs de remplacement (`$`, `<`, `{`, `%`) sont ignorées |
| Chemin de machine | `C:/Users/<nom>` ou `/c/Users/<nom>` dans un fichier `.py .mjs .js .cjs .json .sh .ps1 .html .css` hors `episodes/`, `docs/` et tout dossier `vendor/` ; les marqueurs `<…>`, `{…}`, `nom`, `vous`, `you`, `user` sont tolérés |
| Taille de `REGLES_STUDIO.md` (0.2.3) | Tout fichier nommé `REGLES_STUDIO.md` de plus de 9 000 caractères une fois `${CLAUDE_PLUGIN_ROOT}` remplacé par un chemin de cache type (`C:/Users/<nom>/.claude/plugins/cache/studio-faceless/studio-faceless/0.2.3`) : refus. L'application de bureau coupe tout `additionalContext` du hook `SessionStart` au-delà de 10 000 caractères ; le détail va dans `referentiels/REGLES_DETAIL.md` |

Les médias, les fichiers en LFS et ceux de plus de 3 Mo ne sont pas lus pour les secrets et les chemins.

**Fichiers lus** : la liste d'index de Git (ou tous les fichiers suivis et non ignorés avec `--tout`) et leur contenu texte. **Écrits** : aucun. **Codes de sortie** : 0 = rien à signaler ; 1 = refus (liste « REFUS : n problème(s) » avec le motif de chaque fichier). **Dépendances** : Python standard et `git` ; `git` doit être dans le `PATH`.

**Liens** : crochet `.githooks/pre-commit` du squelette (voir [`starter-et-depot.md`](starter-et-depot.md)) ; `.gitignore` et `.gitattributes` du squelette ; workflow [`depot-git.md`](../workflows/depot-git.md).

**À savoir**
- Un refus ne se contourne pas par `--no-verify` : corriger la cause (déplacer le média vers la sauvegarde, passer le binaire en LFS, retirer le secret ou le chemin).
- Les règles LFS du squelette ne couvrent que `marque/**` et `templates/**` pour quelques extensions ; un binaire de plus de 10 Mo ailleurs ou d'une autre extension sera refusé.
- Les fichiers Markdown ne passent pas le contrôle des chemins de machine (seulement celui des secrets).
- Un secret dans un fichier de plus de 3 Mo n'est pas détecté.
- Un segment d'URL qui commence lui-même par `sk-` suivi de 20 caractères reste signalé (faux positif possible).
- **Test** de la détection des secrets (exemples de faux positifs et de vraies clés), depuis la racine du dépôt du plugin : `python -I -B plugins/studio-faceless/outils/test_verifier_depot.py` (29/10/2026) ; il teste aussi la limite de taille de `REGLES_STUDIO.md` (30/10/2026).

---

## Suivi des tokens

### outils/suivi_tokens.py
**Rôle** : mesure la consommation de tokens des sessions de la chaîne en lisant les journaux de Claude Code, sans en afficher le contenu. Ne modifie aucun fichier.

**Quand il sert** : lancé par Claude principal à chaque fin d'étape d'un épisode (`REGLES_STUDIO.md`), pour décider de la suite (état écrit, puis `/clear`, ou `/compact` au milieu d'une longue porte) ou d'un changement de méthode ; les chiffres par étape se notent dans l'état de l'épisode.

**Usage**
```text
python -B ${CLAUDE_PLUGIN_ROOT}/outils/suivi_tokens.py --depuis AAAA-MM-JJ
```
| Option | Rôle | Défaut |
|---|---|---|
| `--depuis AAAA-MM-JJ` | Date de début ; les sessions commencées avant sont ignorées | `2026-10-16` |

**Sortie**, par session (huit premiers caractères de l'identifiant) : date de début, puis pour la session principale le nombre d'appels, le contexte médian et maximal et celui du départ (en k), les tokens effectifs (Mt) et les écritures de cache (Mt) ; puis une ligne de synthèse pour ses sous-agents (nombre, appels, contexte médian et maximal, Mt effectifs, cache écrit).

**Formule** : tokens effectifs = entrée + 0,1 × lecture de cache + 2 × écriture de cache + 5 × sortie.

**Fichiers lus** : `~/.claude/projects/<chemin de la chaîne encodé>/*.jsonl` et `…/<session>/subagents/*.jsonl` (le chemin encodé remplace tout caractère hors lettres et chiffres par `-`). **Écrits** : aucun. **Dépendances** : bibliothèque standard seule.

**Liens** : `REGLES_STUDIO.md` (« Économie de tokens et de contexte ») ; `tokens-contexte.md` et `etapes.md` § 13 du skill `episode` ; workflow [`session-et-garde-fou.md`](../workflows/session-et-garde-fou.md).

**À savoir**
- Se lance avec `python -B` (sans `-I`), comme l'écrivent son en-tête et `REGLES_STUDIO.md`, alors que les autres outils utilisent `python -I -B`.
- Il faut le lancer depuis la racine de la chaîne (ou avec `CLAUDE_PROJECT_DIR`), sinon le dossier de journaux calculé est faux et rien n'est affiché.
- La date de départ par défaut est celle d'AA (16/10/2026) : toujours passer `--depuis`.

---

## Garde-fou et injection des règles

### hooks/hooks.json
**Rôle** : déclare les deux hooks du plugin : l'injection des règles communes au début de chaque session (`SessionStart`) et le garde-fou des commandes avant chaque appel d'outil (`PreToolUse`).

**Quand il sert** : lu par Claude Code au chargement du plugin ; aucun humain ni agent ne le lance.

**Contenu**
| Événement | Filtre | Commande | Délai |
|---|---|---|---|
| `SessionStart` | aucun (début de session ; la doc du script ajoute : après un `/compact`) | `python -I "${CLAUDE_PLUGIN_ROOT}/hooks/regles_studio.py"` (shell `bash`) | 10 s |
| `PreToolUse` | `Bash\|PowerShell\|Write\|Edit\|NotebookEdit` | `python -I "${CLAUDE_PLUGIN_ROOT}/hooks/garde_commandes.py"` (shell `bash`) | 10 s, message d'état « Garde studio-faceless » |

**Liens** : `regles_studio.py`, `garde_commandes.py` ; [`ARCHITECTURE.md`](../ARCHITECTURE.md).

**À savoir** : le hook s'applique à toute la session, sous-agents compris. Un plugin **ignore** les champs `hooks`, `mcpServers` et `permissionMode` de l'en-tête de ses agents : tout passe par ce fichier. Python doit être dans le `PATH` de Git Bash. Si le script plante, la plupart des erreurs de hook ne bloquent pas l'appel, et le garde-fou ne protège alors plus (comportement de Claude Code, à vérifier dans sa documentation).

### hooks/garde_commandes.py
**Rôle** : lit chaque appel d'outil (JSON sur l'entrée standard) et répond « deny » (refus) ou « ask » (demande de confirmation) ; sans objection, il ne répond rien et l'appel suit le circuit normal des permissions. Les chemins protégés sont relatifs au dossier de la chaîne (`CLAUDE_PROJECT_DIR`).

**Quand il sert** : lancé par Claude Code avant chaque `Bash`, `PowerShell`, `Write`, `Edit` et `NotebookEdit`, pour Claude principal comme pour les sous-agents.

**Entrée et sortie**
- **Entrée** : `tool_name`, `tool_input` (`command`, `file_path` ou `notebook_path`), `agent_type` (absent pour Claude principal), `cwd`.
- **Dossier de la chaîne** : `CLAUDE_PROJECT_DIR`, sinon `cwd` de l'entrée, sinon le dossier courant.
- **Sortie** : `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny"|"ask", "permissionDecisionReason": "Garde studio-faceless : …"}}`, ou rien. **Code de sortie toujours 0** ; une entrée JSON illisible ne bloque rien.
- **Option** : `--role <rôle>` force le rôle (essais) ; `hooks.json` ne l'utilise pas.

**Table `ROLES`** (type d'agent, sans le préfixe `studio-faceless:`, vers rôle du garde-fou) :
| Type d'agent | Rôle |
|---|---|
| `motion-producer` | `producteur` |
| `shorts-producer` | `producteur` |
| `art-director` | `directeur-artistique` |
| `studio-maintainer` | `mainteneur` |
| Claude principal, `research`, tout autre type | aucun rôle : seules les règles pour tous s'appliquent |

Le préfixe de plugin (`studio-faceless:`) est retiré avant la recherche ; un ancien préfixe `aa-` (agents de StudioV1) est aussi retiré (`aa-motion-producer` donne `motion-producer`).

**Ordre d'évaluation d'une commande Bash ou PowerShell** : (1) motifs refusés pour tous ; (2) suppression récursive ; (3) règles du rôle, s'il y en a un ; (4) motif soumis à confirmation (`preview`) ; (5) rendu sans `--workers 1` ou `2`. Le premier qui répond l'emporte.

**1. Pour tous : refusé (`deny`)** (le motif s'applique au texte entier de la commande)
| # | Motif | Exemples | Message |
|---|---|---|---|
| 1 | `hyperframes` (ou `hyperframes.mjs`, avec ou sans `@version`) suivi de `publish`, `cloud`, `cloudrun`, `lambda`, `auth` ou `login` | `npx hyperframes publish`, `node …/hyperframes.mjs auth login` | publication, rendu cloud ou connexion HyperFrames : interdit sans décision du propriétaire |
| 2 | `hyperframes … upgrade` | `npx hyperframes upgrade` | mise à jour de HyperFrames : interdite (0.8.149 figée) |
| 3 | `hyperframes … skills update`, `install` ou `add` | `hyperframes skills update` | mise à jour des skills : interdite sans décision du propriétaire |
| 4 | `npx [-y\|--yes] hyperframes@…` | `npx hyperframes@latest render` | autre version de HyperFrames que la 0.8.149 figée |
| 5 | `npm` suivi de `install`, `i`, `add`, `update`, `up`, `upgrade`, `uninstall`, `remove`, `rm` ou `un` | `npm install gsap` | installation ou mise à jour npm : nouvelle dépendance, à décider par le propriétaire |
| 6 | `Remove-Item` avec `-r` ou `-Recurse…` | `Remove-Item dossier -Recurse` | suppression récursive : passer par la corbeille, avec accord |
| 7 | `rd`, `rmdir`, `del`, `erase` avec `/s` | `rd /s /q dossier` | idem |
| 8 | `find … -delete` ou `find … -exec rm` | `find . -name x -delete` | suppression par find : passer par la corbeille, avec accord |
| 9 | `shutil.rmtree`, `os.removedirs`, `rimraf`, `rmSync`, `rmdirSync` ou `promises.rm` avec `recursive` | `python -c "shutil.rmtree('x')"` | suppression récursive par script : passer par la corbeille, avec accord |
| 10 | `Directory::Delete(…, $true)` (.NET) | `[IO.Directory]::Delete($p,$true)` | suppression récursive (.NET) : passer par la corbeille, avec accord |
| 11 | `DeletePermanently` | appel .NET de suppression définitive | suppression définitive : interdite |
| 12 | `Clear-RecycleBin` | `Clear-RecycleBin -Force` | vidage de la corbeille : interdit |
| 13 | Commande `rm`, `rmdir`, `rd`, `del`, `erase`, `ri` ou `remove-item` (en tête de segment, après `sudo`, `xargs`, `command`, `nohup`, `time`, `exec`, `env`, `cmd /c` et les affectations `VAR=`) avec une option récursive : `-…r…`, `--recursive`, `-recurse` ou `/s` | `rm -rf x`, `rm -fr x`, `rm -r x` | suppression récursive : passer par la corbeille, avec accord |

La commande est découpée en segments (`&&`, `||`, `;`, `|`, retour à la ligne).

**2. Pour tous : refus de l'écriture dans le plugin installé** : un `Write`, `Edit` ou `NotebookEdit` dont le chemin est dans le dossier du plugin (`CLAUDE_PLUGIN_ROOT`) est refusé : « le plugin installé ne se modifie pas depuis une chaîne : modifier son dépôt, puis changer sa version ». Cette règle ne vaut que pour ces trois outils, pas pour Bash.

**3. Pour tous : confirmation (`ask`)**
| Motif | Message |
|---|---|
| `hyperframes … preview` | aperçu HyperFrames : son Chrome reste ouvert jusqu'à l'arrêt ; à lancer seulement sur demande |

**4. Pour tous : rendu direct sans `--workers` (refus, `deny`)** : `hyperframes … render` sans `--workers 1`, `--workers 2`, `--workers=1`, `--workers=2`, `-w 1` ou `-w 2` (ni `-w1`, `-w2`) est refusé : « rendu HyperFrames sans « --workers 1 » ou « 2 » : relancer avec --workers 1 (un Chrome par processus) ». Les `render.sh` du gabarit contiennent `--workers 2` ; le garde ne voit pas l'intérieur d'un script lancé par `bash render.sh`.

**5. Par rôle**

| Rôle | Bash et PowerShell | Write, Edit, NotebookEdit |
|---|---|---|
| **directeur-artistique** | Chaque segment doit commencer par `ffmpeg`, `ffprobe` ou `mkdir` (sinon refus, y compris `cd`). Pas de `-y` pour `ffmpeg`. Toute cible d'écriture (redirection, dernier argument de `ffmpeg`, argument de `mkdir`…) est refusée si elle tombe dans `direction/`, `templates/`, `.claude/`, un `CLAUDE.md`, un dossier existant de `marque/`, `episodes/<id>/inputs/`, `episodes/<id>/production/` ou un MP4 existant | Aucune limite du garde ; l'agent n'a pas ces outils (`tools` : Read, Grep, Glob, Bash, WebFetch, WebSearch, Skill) |
| **producteur** (`motion-producer`, `shorts-producer`) | (a) toute cible d'écriture dans `direction/`, `templates/`, `.claude/` ou un `CLAUDE.md` : refus ; (b) **toute mention**, même en lecture, de `direction/`, `templates/`, `.claude/` ou de `claude.md` dans la commande : refus (« se lisent avec Read ou Grep »), **sauf** les chemins du plugin installé (`CLAUDE_PLUGIN_ROOT`, sans « .. »), que la fonction `sans_plugin` remplace par `PLUGIN` avant ce contrôle : le producteur lance ainsi par Bash les outils du plugin, dont le chemin contient `.claude/` ; (c) toute cible d'écriture dans un dossier existant de `marque/`, dans `episodes/<id>/inputs/` ou sur un MP4 existant : refus ; (d) script en ligne (`python -c`, `node -e`, `powershell -command`…) qui écrit et cite `marque` ou `inputs` : refus | Refus dans `direction/`, `templates/`, `.claude/`, les `CLAUDE.md`, un dossier existant de `marque/`, `episodes/<id>/inputs/` et un MP4 existant |
| **mainteneur** | Aucune écriture : un script en ligne qui écrit est refusé ; tout segment avec une cible d'écriture (redirection, `sed -i`, `tee`, `touch`, `mkdir`…) ou dont la commande est `cp`, `mv`, `install`, `tee`, `touch`, `copy-item`, `move-item`, `rename-item`, `set-content`, `add-content`, `out-file`, `new-item`, `copy`, `move`, `ren`, `rename`, `xcopy`, `robocopy`, `ffmpeg`, `dd` ou `ln` est refusé | Refus dans `.claude/`, un dossier existant de `marque/`, `episodes/<id>/inputs/`, `episodes/<id>/production/<projet>/` et un MP4 existant. Il peut éditer `direction/`, `templates/` et les `CLAUDE.md` si la mission l'autorise |

**Zones protégées**
| Zone | Chemin (relatif à la chaîne) | Raison affichée |
|---|---|---|
| `core` | `direction/…`, `templates/…`, `.claude/…`, tout fichier nommé `CLAUDE.md` | direction/, templates/, .claude/ et les CLAUDE.md sont protégés |
| `.claude` | `.claude/…` | .claude/ est protégé |
| `marque` | `marque/<dossier existant>/…` (au moins deux niveaux) | un dossier existant de marque/ ne se modifie pas ; nouvelle version = nouveau dossier |
| `inputs` | `episodes/<id>/inputs…` | les entrées d'origine d'un épisode sont en lecture seule |
| `production` | `episodes/<id>/production/<projet>…` | les projets de production sont réservés au producteur, sur contrat |
| `mp4` | tout fichier `.mp4` qui existe | un export existant n'est jamais écrasé |

Les chemins sont ramenés à un chemin relatif à la chaîne (`/c/Users/…` de Git Bash converti) ; un chemin hors de la chaîne n'est jamais protégé. Une demande d'un rôle refusée porte le préfixe du rôle dans le message (« producteur : … »).

**Fichiers lus** : l'entrée JSON, l'existence de dossiers et de MP4 dans la chaîne. **Écrits** : aucun. **Dépendances** : Python standard.

**Liens** : [`hooks.json`](../../plugins/studio-faceless/hooks/hooks.json) ; [`ARCHITECTURE.md`](../ARCHITECTURE.md) (§ Garde-fou) ; définitions des agents ([`agents.md`](agents.md)) ; `.claude/settings.json` de la chaîne (permissions) ; workflow [`session-et-garde-fou.md`](../workflows/session-et-garde-fou.md).

**À savoir**
- Le rendu sans `--workers 1` ou `2` est **refusé** (`deny`), non soumis à confirmation : l'en-tête du script et `REGLES_STUDIO.md` le disent désormais (seul `preview` demande confirmation).
- Le motif 13 attrape aussi `Remove-Item … -Force` (l'option contient un `r`) : refus par prudence.
- **Le garde-fou ne bloque pas** : `npm ci` et `npm run` (absents de la liste), un script Python lancé par fichier qui supprime ou écrit (seul `python -c` est examiné), `rmdir` sans option récursive. Le mainteneur peut donc lancer `python script.py`, mais sa mission le lui interdit.
- Le chemin du plugin installé contient `.claude/` : `sans_plugin` le remplace par `PLUGIN` avant la règle (b), sauf s'il contient « .. » (alors il reste refusé). Un producteur peut donc lancer par Bash un outil du plugin (chemin complet, sans « .. »). Le gabarit vient quand même du kit, copié par le Studio Director. Cela ne vaut que si `CLAUDE_PLUGIN_ROOT` est défini dans l'environnement du hook.
- Les comparaisons `claude.md` et les noms de zones s'appuient sur `os.path.normcase`, qui met en minuscules sous Windows seulement : sous un autre système, `CLAUDE.md` ne serait pas reconnu par la zone `core` (à vérifier).
- Les permissions `allow`, `deny` et `ask` du `.claude/settings.json` de la chaîne s'ajoutent à ce garde-fou ; la génération ElevenLabs passe par l'API, avec l'accord du propriétaire en conversation et le coût annoncé avant (`DIRECTION_AUDIO.md` § 4) ; ce script ne la contrôle pas.
- La fonction `decide(command, role=None)` est conservée « pour les tests existants ».

### hooks/regles_studio.py
**Rôle** : injecte les règles communes du studio (`REGLES_STUDIO.md`) dans le contexte de Claude au début de chaque session, avec le chemin réel du plugin à la place de `${CLAUDE_PLUGIN_ROOT}`.

**Quand il sert** : lancé par Claude Code à l'événement `SessionStart` (démarrage ; la doc du script ajoute : après un `/clear` ou un `/compact`). Aucun humain ne le lance.

**Déroulement** : dossier du plugin = `CLAUDE_PLUGIN_ROOT`, sinon le dossier parent du dossier `hooks/` ; lit `REGLES_STUDIO.md` ; remplace chaque `${CLAUDE_PLUGIN_ROOT}` par le chemin (barres obliques normales) ; écrit sur la sortie standard `{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "<texte>"}}` en UTF-8. **Depuis la 0.2.3** : si le texte final (règles, plus la section du domaine) dépasse 9 500 caractères, une première ligne « Texte tronqué par l'app : lire <racine>/REGLES_STUDIO.md en entier. » est ajoutée, car l'application coupe tout `additionalContext` au-delà de 10 000 caractères.

**Fichiers lus** : `REGLES_STUDIO.md`. **Écrits** : aucun. **Dépendances** : Python standard.

**Liens** : [`REGLES_STUDIO.md`](../../plugins/studio-faceless/REGLES_STUDIO.md) ; [`ARCHITECTURE.md`](../ARCHITECTURE.md) (§ Ordre des règles) ; workflow [`session-et-garde-fou.md`](../workflows/session-et-garde-fou.md).

**À savoir** : un plugin ne charge pas de `CLAUDE.md` à sa racine, d'où ce hook. Si `REGLES_STUDIO.md` manque, le script plante (fichier introuvable) et aucune règle n'est injectée.

---

## Règles communes

### REGLES_STUDIO.md
**Rôle** : règles communes à toutes les chaînes qui utilisent le plugin ; le `CLAUDE.md` de la chaîne les complète et l'emporte en cas de conflit. Elles viennent de StudioV1 (chaîne Apparently Athletic), où le propriétaire les a validées entre le 14 et le 28/10/2026.

**Quand il sert** : injecté dans chaque session par `regles_studio.py` ; lu implicitement par Claude principal et par chaque agent qui reçoit le contexte de la session ; cité par les skills (« les règles communes du studio »).

**Contenu, section par section**
| Section | Contenu |
|---|---|
| Introduction | Portée, rapport avec le `CLAUDE.md` de la chaîne (nomme le propriétaire, la langue des documents et celle du spectateur, le public, la voix) |
| Dossier du plugin | Note sur `${CLAUDE_PLUGIN_ROOT}` : écrit entre accolades, remplacé à l'injection ; n'existe pas dans l'environnement de Bash |
| Quoi lire selon la mission | Tableau mission → fichier : ligne éditoriale et écarts de la chaîne, `METHODE_RECIT`, `REFERENTIEL_QUALITE_REALISATION`, `DIRECTION_AUDIO`, `MOTION_CATALOG`, `marque/`, épisode, skills `episode`, `thumbnail-strategist`, `youtube-seo`, `shorts` |
| Moteur et outils | Depuis la 0.2.3, **renvoi** de deux lignes vers `referentiels/REGLES_DETAIL.md`, qui porte le texte d'origine : HyperFrames 0.8.149 figée ; Node 22 ou plus ; skills plus récents que le CLI ; navigateurs (`--workers 2` au plus, `preview` sur demande) ; outils du plugin et `controle/` ; garde-fou (pour tous, par rôle) ; rendu par `rendre_si_libre.sh` ; archivage ; dépôt Git (commits locaux, envoi avec accord) ; suivi des tokens |
| Sous-agents | Studio Director ; les six agents (`research`, `reviewer`, `art-director`, `motion-producer`, `shorts-producer`, `studio-maintainer`) ; contrat de mission (avec la section des règles de la chaîne pour les agents sans `CLAUDE.md`) ; isolation ; un sous-agent ne voit pas la mémoire de Claude |
| Parcours d'un épisode | Depuis la 0.2.3, **renvoi** de deux lignes vers `referentiels/REGLES_DETAIL.md` : les onze étapes, du sujet à l'archivage |
| Économie de tokens et de contexte | Sessions : fin de porte = `STATE.md` réécrit, `INDEX.md` à jour, puis `/clear` (un `/compact` remet dans le contexte skills et fichiers lus : 124,6 k contre 81 à 88 k), `/compact` permis au milieu d'une longue porte, modèle du fil principal changé seulement après un `/clear` ; sous-agents (jamais plus de 4 min sans action, une correction dans la même version : reprise du producteur si son cache est chaud, sinon un nouvel agent court) ; travail (lectures par plages, sorties courtes) |
| Règles permanentes | Faire seulement ce qui est demandé ; décision / proposition / hypothèse / question ouverte ; **statuts** ; pas d'écoute déclarée sans écoute ; ne jamais écraser ; aucune publication, achat ou contournement ; médias réels, sous licence libre ou en citation encadrée par défaut (référentiel § 2 bis), licences libres seules par écart de chaîne ; pas de contamination entre épisodes ; concision |

**Statuts** (section « Règles permanentes »)
- décisions : `FIXÉ`, `VALIDÉ` (date et référence), `PROPOSÉ`, `PROVISOIRE`, `QUESTION OUVERTE` ;
- production : `EN_COURS`, `MESURES_TECHNIQUES_OK`, `ECOUTE_A_FAIRE`, `CORRECTIONS_DEMANDEES`, `APPROUVE_PAR_<PROPRIETAIRE>` (date), `PUBLIE` (date et lien) ;
- le catalogue d'animations garde les siens (`expérimental`, `à améliorer`, `validé`).

**Liens** : [`hooks/regles_studio.py`](../../plugins/studio-faceless/hooks/regles_studio.py) (injection) ; [`ARCHITECTURE.md`](../ARCHITECTURE.md) (ordre des règles) ; [`skill-episode.md`](skill-episode.md) ; [`agents.md`](agents.md) ; [`referentiels.md`](referentiels.md).

**À savoir**
- **Ordre des règles** (la dernière l'emporte) : `REGLES_STUDIO.md` et référentiels du plugin, puis `direction/ECARTS.md`, puis `CLAUDE.md` de la chaîne, puis `CLAUDE.md` de l'épisode.
- La section sur les outils prescrit `python -B "<chemin>"`, alors que la plupart des outils indiquent `python -I -B`.
- Le texte est injecté en entier à chaque session : il pèse sur le contexte. Toute règle ajoutée ici s'ajoute à ce coût ; le détail va dans un référentiel ou un skill.

---

## Workflows liés
- [`rendu-et-controle.md`](../workflows/rendu-et-controle.md) : `rendre_si_libre.sh`, `controle.py`, la planche, Chrome, les statuts.
- [`archivage-et-sauvegarde.md`](../workflows/archivage-et-sauvegarde.md) : `archiver_episode.py`, `sauvegarde-chaine.ps1`.
- [`session-et-garde-fou.md`](../workflows/session-et-garde-fou.md) : `regles_studio.py`, `garde_commandes.py`, permissions, `suivi_tokens.py`, `/compact`.
- [`depot-git.md`](../workflows/depot-git.md) : `verifier_depot.py`, crochet `pre-commit`, LFS, commits et envoi.
- [`cartes` dans le workflow d'épisode](../workflows/episode.md) : étape 5 (socle).
