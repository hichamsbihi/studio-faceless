# Cartes au trait

`cartes.py` (24/10/2026) tire une carte au trait SVG 1920 × 1080 et les positions des villes en pixels d'un shapefile Natural Earth admin 0 (domaine public), selon une spécification JSON. Repris de l'outil de cartes de l'E007 d'AA et de sa carte d'Italie : avec les mêmes paramètres, les cartes d'Italie et du monde de l'E007 sortent identiques (traits et villes ; seul le commentaire d'en-tête change). Python seul, sans dépendance. Refuse d'écraser.

```text
python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/cartes/cartes.py SPEC.json --shp episodes/<id>/kit/donnees/ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp --out episodes/<id>/kit/donnees
```
Le shapefile n'est pas dans `outils/` : il se télécharge pour l'épisode, avec l'accord du propriétaire (le `.dbf` doit être à côté du `.shp`).

## Spécification
Une carte, une liste, ou `{"cartes": [...]}` :
```json
{"cartes": [
 {"nom": "carte-italie", "projection": "equirectangulaire",
  "emprise": {"lon": [4.0, 20.0], "lat": [36.2, 47.6]}, "lat_ref": 42.5,
  "pays": ["Italy"], "classe_pays": "italie",
  "voisins": ["France", "Switzerland", "Austria", "Slovenia"],
  "villes": {"turin": [7.6869, 45.0703], "rome": [12.4964, 41.9028]}},
 {"nom": "carte-monde", "projection": "equal-earth",
  "emprise": {"lon": [-180, 180], "lat": [-58, 84]}, "pas_min": 1.5,
  "villes": {"manchester": [-2.2426, 53.4808]}}
]}
```
- `pays` : pays du récit (classe `classe_pays`, défaut `focus`) ; noms du champ `ADMIN` (`champ_nom` pour un autre champ).
- `voisins` : facultatif. Donné, seuls ces pays sont tracés (carte légère) ; absent, tous les pays dont l'emprise touche le cadre à 2° près (classe `classe_voisins`, défaut `voisin`).
- `villes` : `[longitude, latitude]` ; cercles `ville-<nom>` dans le SVG, positions dans `villes-px.json`.
- `pas_min` : écart minimal entre deux points d'un tracé, en pixels (1,5 pour le monde).
- Sorties : `<out>/<nom>/<nom>.svg` (traits en `currentColor`, identifiants `<classe>-<pays>`) et `villes-px.json` (projection, `cadre_px` = rectangle occupé par l'emprise, échelle en pixels par degré, villes).

## Projections
- **`equirectangulaire`** (cartes de l'E007 d'AA) : x = longitude × cos(`lat_ref`), y = latitude, **même échelle en pixels sur les deux axes**. L'emprise est inscrite dans 1920 × 1080 et centrée : si son rapport n'est pas 16:9, il reste des bandes vides (voir `cadre_px`). Pour un pays ou une région, avec `lat_ref` au milieu de l'emprise, les formes sont justes au centre et à 10 % près aux bords (Italie de l'E007 : 8,5 % à 47,6° N). **À prendre pour les cartes régionales.**
- **`equal-earth`** (Šavrič, Patterson et Jenny, 2018) : projection à aires égales aux formes naturelles, pensée pour les cartes du monde ; `meridien_central` facultatif (défaut : milieu de l'emprise). **À prendre pour le monde.** Monde de −58° à 84° : cadre 1920 × 840 px (bandes de 120 px).

## La remarque « la carte du monde du kit étire la latitude d'un facteur 1,43 » (seq4 v3 de l'E007 d'AA)
Vérifiée le 24/10/2026 (étude AA) : **elle est fausse**.
- Le SVG de la carte du monde du kit de l'E007 d'AA est en équirectangulaire cos(0°) (plate carrée) : 5,333 px par degré en longitude **et** en latitude. L'emprise de 142° de latitude n'occupe que 757 px de haut, centrés (terres de y = 163,5 à 907,4 ; bandes vides de 161 px en haut et en bas).
- Le 1,43 est le rapport (1080 / 142) / (1920 / 360) = 7,606 / 5,333 = 1,426 : l'échelle qu'aurait la latitude si la carte remplissait toute la hauteur. Ce n'est pas le cas du fichier.
- La « correction » du producteur (y × 0,70123 dans la composition de la carte de la séquence 4 v3) a donc **écrasé** la carte : 3,74 px par degré de latitude contre 5,33 en longitude (terres de y = 114,7 à 636,3), soit les formes aplaties de 30 % en hauteur, en plus de l'élargissement propre à la plate carrée aux hautes latitudes (déjà × 1,68 à Manchester). Les villes, corrigées de la même façon, restent sur leurs côtes : le défaut est de forme, pas de position.
- Pour le monde, prendre `equal-earth` (formes naturelles, aucune échelle à « corriger ») ; pour un pays, l'équirectangulaire avec `lat_ref` au milieu. Ne jamais redresser une carte du kit d'un facteur : lire `cadre_px` et l'échelle dans `villes-px.json`.

## Limites
- Polygones seulement (pas de lignes ni de points du shapefile) ; pas de découpe au cadre : les tracés qui sortent du cadre sont coupés par le `viewBox` du SVG.
- `equal-earth` avec un `meridien_central` éloigné de 0 : les pays qui traversent l'antiméridien ne sont pas recousus.
- Les noms des pays sont ceux de Natural Earth (anglais, champ `ADMIN`).

## Lecteurs et projections (versés de Maps & Means le 30/10/2026, validés sur MM)
Trois modules complètent `cartes.py` sans le modifier. Ils servent aux cartes de relief, d'imagerie et de globe décrites dans `${CLAUDE_PLUGIN_ROOT}/domaines/geo-economie/cartes/README.md`. Python et numpy ; aucun appel réseau.

| Module | Rôle | Validé sur MM |
|---|---|---|
| `proj.py` | Projections : Albers conique équivalente (paramètres à passer ; défaut = Alaska Albers EPSG:3338, exemple de MM), UTM (WGS84, zone à passer), Equal Earth et son inverse (Šavrič et al. 2018), Web Mercator et son inverse, `km(a, b)` | 26/10/2026 |
| `shp.py` | Lit polygones, lignes et table DBF d'un shapefile dans le zip de Natural Earth (domaine public), sans bibliothèque SIG : `lire(zip, 'ne_10m_admin_0_countries')` | 26/10/2026 |
| `cog.py` | Lit un niveau ou une zone d'un COG RVB 8 bits (Sentinel-2), écrit un PPM : `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/cartes/cog.py TIF NIVEAU SORTIE.ppm [x0 y0 l h]` | 26/10/2026 |

`cartes.py` lit un `.shp` à côté de son `.dbf` (polygones, cartes au trait SVG) ; `shp.py` lit l'archive zip telle que Natural Earth la publie (polygones et lignes, attributs). Les deux coexistent. Pour le monde, `equal_earth` de `proj.py` donne les mêmes formes que la projection `equal-earth` de `cartes.py`. Les données (Natural Earth, Sentinel-2, relief) ne sont pas dans le plugin : à télécharger pour l'épisode, avec l'accord du propriétaire.
