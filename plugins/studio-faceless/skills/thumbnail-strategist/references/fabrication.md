# Fabrication : HTML/CSS 1280×720, détourage, rendu

Aucun outil nouveau : une page HTML/CSS par miniature, rendue par le Chrome sans fenêtre que HyperFrames a déjà téléchargé (`~/.cache/hyperframes/chrome/chrome-headless-shell/`). Pas d'image générée par IA (le détourage sépare des pixels réels, il n'en crée pas), pas de Photoshop. Le sujet se détoure avec `remove-background` de HyperFrames (§ 3, voie A) ou, en secours, par un polygone tracé à la main (voie B).

## 1. Dossier
- `episodes/<id>/miniatures-vN/` : vérifier qu'il n'existe pas, puis le créer. Une version ne s'écrase jamais ; une correction du propriétaire fait une `vN+1` (exemple AA, E003 : v4 = v3-1 avec la flèche raccourcie).
- Contenu : `miniature-<n>-<mots>.html` (source), `media/` (copies : photo en 1920 px, drapeaux SVG, le logo de la chaîne pris dans `marque/`, `Montserrat-VariableFont.ttf` et `Montserrat-OFL.txt`), `PROVENANCE.md`, les PNG rendus et la planche de contrôle.
- Nom du PNG livré : `<NomChaine>-<EPISODE>-miniature-vN-<n>-<mots>.png`.

## 2. Page source
Modèle à copier puis adapter : la page de la dernière miniature validée de la chaîne (exemple AA : la v4 de l'E003, 38 lignes). Pour la première miniature d'une chaîne, partir des extraits de CSS ci-dessous. La police Montserrat (SIL OFL) se télécharge une fois depuis Google Fonts, avec l'accord du propriétaire, et se range dans `marque/` avec sa licence ; chaque miniature en copie ensuite les deux fichiers dans son `media/`.
- `html, body` : 1280×720, `overflow: hidden`, fond de secours foncé ; tout en `position: absolute` dans un conteneur 1280×720.
- Police : `@font-face` local sur `media/Montserrat-VariableFont.ttf`, graisse 900 pour les mots, 800 pour les pastilles.
- Commentaire en tête : version, mots, épisode, date, photo et licence, ce qui change depuis la version précédente.
- Couches dans l'ordre : fond, symbole de fond (losange, bande, chiffre), sujet détouré, logo, texte, flèche, pastille.
- Flèche : un `path` SVG en courbe, `stroke-linecap: round`, pointe en `marker`, doublé d'un même tracé plus épais, foncé, à 35 % pour l'ombre. **Sa pointe s'arrête avant le sujet** (≈ 30 px dans la v4).

## 3. Détourage du sujet
Décision du propriétaire (VALIDÉ, Hicham, 03/11/2026 : « tu utilises le modele remove-background de hyperframes ») : une miniature peut détourer une personne avec `hyperframes remove-background` (modèle local `u2net_human_seg`) au lieu du seul polygone. Méthode appliquée et vérifiée le 03/11/2026 (exemple AA : miniatures-v2 de l'E011). Le polygone seul reste possible en secours (voie B). Le refus d'image générée par IA ne change pas.

### Voie A : modèle local `remove-background`
Commande, installation du modèle et limites : skill `studio-faceless:remove-background` (§ 1 pour l'accord du propriétaire au premier téléchargement, § 4 bis pour le masque).
1. **Recadrer** la photo autour de la personne.
2. **Détourer** depuis la racine de la chaîne : `node node_modules/hyperframes/bin/hyperframes.mjs remove-background <recadrage.jpg> -o <brut.png> --device cpu` (1,5 s pour 1600×1400, modèle déjà en cache).
3. **Masque** : resserré de 2 px puis flou de 0,7 (méthode du § 4 bis du skill), multiplié par un **polygone séparateur** (tracé avec la grille de la voie B) qui écarte les autres personnes et les objets que le modèle garde (fauteuil, main d'une voisine). Fait ici avec Pillow : `MinFilter(5)`, `GaussianBlur(0.7)`, polygone flouté de 1 px. Les couleurs viennent telles quelles de la photo d'origine : aucun pixel redessiné.
4. **Contrôler** sur fond vert vif, en pleine taille : cheveux, mains, bords. Puis la page HTML/CSS et le rendu (§ 4) restent inchangés.

Pillow sert seulement à composer ce masque (installé sur le poste du propriétaire le 03/11/2026 ; ailleurs, rien ne s'installe sans son accord).

### Voie B : polygone tracé à la main (secours)
Principe de la v4 : la photo est affichée **à sa taille naturelle** (`width` et `height` = dimensions du fichier), donc les coordonnées du polygone sont celles des pixels de la photo ; on place et on réduit ensuite le conteneur (`transform: scale(...)`, `transform-origin: 0 0`).

```css
#sujet{position:absolute;left:430px;top:-6px;transform:scale(.73);transform-origin:0 0;
  filter:drop-shadow(0 14px 28px rgba(0,0,0,.5)) drop-shadow(0 0 2px rgba(0,0,0,.6))}
#sujet img{display:block;width:1920px;height:1205px;clip-path:polygon(970px 20px, 985px 22px, ...)}
```

Méthode :
1. **Grille de coordonnées** de la photo entière, pour repérer le contour :
   `python -B ${CLAUDE_PLUGIN_ROOT}/skills/thumbnail-strategist/scripts/miniature.py grille media/photo.jpg <travail>/grille.png --echelle 0.6`
   (lignes tous les 50 px, valeurs tous les 100 px, en pixels de la photo).
2. **Zooms** sur les bords difficiles (cheveux, mains, épaules) : `--zone x,y,largeur,hauteur --echelle 2 --pas 10`.
3. **Tracer** le polygone dans le CSS, dans le sens des aiguilles d'une montre, un point tous les 15 à 40 px selon la courbure (82 points pour Messi dans la v4). Le bas du sujet sort du cadre : le polygone descend jusqu'au bord de la photo.
4. **Vérifier** en superposant le polygone : `grille ... --polygone miniature.html` lit le premier `clip-path: polygon(...)` de la page (ou une liste `x y, x y` dans un fichier). Hors du polygone, la photo est assombrie ; les sommets sont numérotés tous les 5 pour corriger un point précis. Rogner un peu dans le sujet plutôt que de laisser du fond.
5. Les grilles et captures de travail vont dans le dossier temporaire de la session, pas dans le dossier de l'épisode.

## 4. Rendu
```bash
python -B ${CLAUDE_PLUGIN_ROOT}/skills/thumbnail-strategist/scripts/miniature.py rendu episodes/<id>/miniatures-vN/miniature-1-<mots>.html episodes/<id>/miniatures-vN/<NomChaine>-<EPISODE>-miniature-vN-1-<mots>.png
```
- Chrome sans fenêtre, fenêtre 1280×720, échelle 1, polices chargées (budget de temps virtuel de 10 s), puis mesure automatique (format, taille, 16:9, poids).
- Refus d'écraser un fichier existant ; le dossier de sortie doit exister.
- Un seul Chrome à la fois ; après la série, vérifier qu'aucun `chrome-headless-shell` ne reste ouvert (`python -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py chrome`, voir `${CLAUDE_PLUGIN_ROOT}/outils/controle/README.md`).
- Si un PNG dépasse 2 Mo (photo très détaillée), en faire une copie JPEG de qualité haute dans un nouveau fichier avec ffmpeg, puis la mesurer.
