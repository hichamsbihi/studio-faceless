# Gabarit de séquence, v3 (voix seule)

**Statut** : `PROPOSÉ` (Claude, 24/10/2026), à la suite des décisions validées sur AA le 24/10/2026 : mix du film à la fin (Q4) et skill `studio-faceless:episode` (Q1). La v2 (`VALIDÉ` sur AA le 20/10/2026) reste intacte dans les archives de la chaîne AA, avec son `mix.py`.

Les règles par défaut citées ici sont dans `${CLAUDE_PLUGIN_ROOT}/referentiels/` ; les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent.

**Changements par rapport à la v2** :
- **Voix seule** : plus de `mix.py`. `voix.py` fait la piste de la séquence avec la voix seule (`media/audio/piste-voix.wav`) et la référence `pistes/stem-voix.wav`. Musique et effets se mixent sur le film collé (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 3, `${CLAUDE_PLUGIN_ROOT}/outils/montage/`).
- **Effets proposés** : le producteur les liste dans le README de sa séquence (modèle ci-dessous) au lieu de les mixer.
- **Recette d'image v3** (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 ter ; skill `studio-faceless:episode`, `references/production.md` § 1) : vivacité, rien de vide qu'on ne comprend pas, dessins et cartes dans les passages d'explication, logos avec mesure, **aucune grille**.
- **Contrôle de l'en-tête** : aucun texte nu dans `<head>`. Chaque commentaire s'ouvre par `<!--` et se ferme par `-->` (défaut de l'E007 seq2 v3).
- **Inchangés** : le fond, les polices, la palette en variables, les moments d'exemple, `render.sh`, les règles techniques ci-dessous.

## Tableau des effets proposés (à recopier dans le README de la séquence)
| Code | Instant local (s) | Image qui le justifie | Type (souffle, impact, montée, déclic, ambiance…) | Facultatif |
|---|---|---|---|---|
| `T01-fiche-posee` | 12,40 | la fiche touche le mur | déclic | non |

Les sons viennent de `marque/son/` (son catalogue) ou du kit de l'épisode. Le Studio Director décide au mix du film.

Point de départ de chaque séquence du parcours raccourci (skill `studio-faceless:episode`, étapes 6 et 7). Il ne contient aucun média ni texte d'épisode : seulement les matières communes et des textes d'exemple.

**Origine** : séquence 6 v2 de l'E003 d'AA (archives de la chaîne AA). Elle a été préférée à la séquence 4 v3 pour quatre raisons :
- l'arrière-plan de l'E001 y tient en un bloc ;
- les matières et leurs licences sont rangées ensemble (`media/matieres/`) ;
- le mix sort des pistes séparées avec un rapport ;
- la fiche d'étude suit les consignes communes.

La séquence 4 v3 dépend d'une caméra 2,5D maison, et son `check` signalait du texte masqué par la vignette. L'outro de marque et tout ce qui est propre à l'E003 ont été retirés.

## Contenu
| Fichier | Rôle |
|---|---|
| `index.html` | Composition racine 1920 × 1080 (30 i/s au rendu). Elle porte l'arrière-plan commun, la palette (variables CSS), les composants (classes), les outils `window.AA` et l'habillage (étiquette du coin, crédit, noir) |
| `compositions/m01-titre.html` | Moment d'exemple : titre, mot clé surligné, ligne d'appoint |
| `compositions/m02-fiche.html` | Moment d'exemple : fiche « papier » d'étude qui se pose, passage surligné |
| `voix.py` | Piste son de la séquence : la voix seule (−18 LUFS d'écoute) et `pistes/stem-voix.wav` (gain 1) pour le mix du film |
| `render.sh` | Rendu final : `--workers 2`, refuse d'écraser |
| `media/matieres/`, `media/fonts/` | Papier charbon, brumes, grain, Newsreader, avec leurs licences (`PROVENANCE.md`) |
| `media/fonds/fond-exemple.jpg` | Fond de contexte calculé, **à remplacer** |

## Utilisation
1. **Kit (Studio Director)** : vérifier que `episodes/<id>/kit/gabarit/` n'existe pas, puis lancer `cp -r ${CLAUDE_PLUGIN_ROOT}/templates/sequence-gabarit-v3 episodes/<id>/kit/gabarit`. Un épisode ne modifie jamais `${CLAUDE_PLUGIN_ROOT}/templates/`.
2. **Séquence (producteur)** : copier `kit/gabarit/` dans un dossier neuf, `episodes/<id>/production/<séquence>-vN/`. Y copier ensuite depuis le kit ce que la séquence utilise :
   - `media/photos/` ;
   - `media/fonds/` : fonds flous de 2112 × 1188, flou σ 14–18, teints à 55 % de la couleur `--teinte` de l'épisode ;
   - `media/audio/bande-voix.wav` (ni musique ni effets) ;
   - l'extrait de provenance, ajouté à `PROVENANCE.md`.
3. **Remplacer** tout ce que les fichiers marquent « À REMPLACER » :
   - `index.html` :
     - `<title>`, `data-composition-id` ;
     - la palette (`:root`) : celle de la `DIRECTION_ARTISTIQUE` de l'épisode ;
     - `CONTEXTE_SOUS_FICHE` ;
     - `data-duration` : la bande voix arrondie à l'image suivante, la même que celle de la piste son ;
     - les repères `T` ;
     - `CONTEXTES`, `BRUMES`, `PLANS`, `COIN`, `CREDITS` ;
     - les `<img class="contexte">` : le fond d'exemple ne va dans aucun film ;
     - les hôtes des moments.
   - `compositions/` : un fichier par moment, `mNN-nom.html`, avec ses repères locaux `R` et ses textes.
   - lancer `python -I -B <dossier>/voix.py`, puis décommenter `<audio id="voix">` ; écrire le tableau des effets proposés dans le README.
   - `render.sh` : `NOM`.
4. **Vérifier** :
   - lancer `npx hyperframes check <dossier>` : viser 0 remarque ;
   - faire une planche : `npx hyperframes snapshot <dossier> --at t1,…,t16 --no-end --describe false -o <dossier>/planche` ;
   - l'assembler en une image, depuis `<dossier>/planche` :
     ```bash
     ls frame-*.png | sed "s/.*/file '&'/" > liste.txt && ffmpeg -v error -n -f concat -safe 0 -i liste.txt -vf "scale=640:360,tile=4x4:padding=6:color=white" -frames:v 1 planche.jpg
     ```

## Règles techniques (constats d'AA, E003)
- **Animation** : chaque élément est une fonction pure du temps. `render(t)` répond à l'évènement `hf-seek`. Un seul système par séquence : pas de GSAP, aucune horloge, aucun `Math.random`. Seul le grain change à chaque image (`AA.hasard`, positions fixes).
- **Sous-composition** :
  - tout se trouve dans `<template>` ;
  - le même `data-composition-id` sur l'hôte et sur la racine du fichier, et `data-no-timeline` sur les deux ;
  - des identifiants préfixés `mNN-` ;
  - un `data-start` numérique sur l'hôte ;
  - le temps local se calcule avec `AA.debutHote()`.
- **`AA.op()`** met `visibility: inherit`, jamais `visible`. Sinon un enfant reste affiché hors de la fenêtre de son hôte, et l'audit le voit par-dessus les autres moments.
- **Aucune vibration** (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 ter) :
  - **un texte posé reste immobile** : jamais d'échelle, de flou ni de rotation animés sur un texte ou un bloc qui en contient. La brume et le grain (modes de fusion), les flous et `--workers 2` imposent un rendu recalé au pixel : seuls un texte immobile ou un glissement linéaire de 1 à 2 px entiers par image restent réguliers. Le mouvement d'un plan vient du papier, des photos de contexte et des photos en carte ;
  - transformations 2D seulement : jamais `perspective()` ni rotation 3D nulle (tremblement du texte, E003 séquence 4 v2) ;
  - aucun arrondi au pixel pendant un mouvement lent (`AA.f`) ;
  - aucune image immobile plus de 1 s (`REFERENTIEL_QUALITE_REALISATION.md` § 2 quater).
- **Polices** : Newsreader par `@font-face` (fichier local) ; IBM Plex Mono injectée par le compilateur, depuis son cache.
- **Taille** : un fichier de plus de 300 lignes déclenche `composition_file_too_large`. Un moment par fichier.

## Palette (`marque/README.md`, « Films » : socle fixe et palette par épisode, validé sur AA, 20/10/2026)
Le fond (papier charbon, contexte flou, vignette, brume, grain) fait partie du socle fixe. Les couleurs viennent de la palette de l'épisode, dans `:root` :

| Variable | Rôle | Valeur par défaut |
|---|---|---|
| `--teinte`, `--teinte75` | teinte des fonds flous (appliquée au kit), fond des crédits et sous-titres d'étiquette (75 %) | `#0B1622` |
| `--texte` | texte sur fond, titres | `#F1F3F5` |
| `--fiche`, `--encre` | papier et texte des fiches | `#F1F3F5`, `#0B1622` |
| `--surligneur`, `--encre-surligneur` | surligneur, étiquettes, et leur texte | `#FFE600`, `#0B1622` |
| `--accent` | accent qui porte le sens du récit | `#E10600` |

- Couleurs en hexadécimal à 6 chiffres (`AA.melange` les lit) ; `--teinte75` reprend `--teinte` à 75 %.
- Couleurs d'entités réelles (exemple AA : les équipes) : réelles, jamais retouchées.
- **Interdit dans les films** : les couleurs de marque que la chaîne exclut des films (liste dans `marque/README.md`).
- **Exception** : la signature et l'outro de la chaîne gardent leurs couleurs. Elles ne sont pas dans le gabarit et s'ajoutent au collage.
- **Contrôle** : `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py couleurs <dossier>/index.html <dossier>/compositions/*.html`.
