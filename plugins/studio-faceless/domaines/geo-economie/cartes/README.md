# Cartes du domaine geo-economie

Versé de Maps & Means (MM) le 30/10/2026 (décision 1 du passage MM, VALIDÉ, Hicham). Cartes MapLibre (globe, relief, vols de caméra) et feuilles papier pour les films qui racontent un lieu. Le code général (projections, lecteurs de shapefile et de COG, cartes au trait) est dans `${CLAUDE_PLUGIN_ROOT}/outils/cartes/` : `proj.py`, `shp.py`, `cog.py`, `cartes.py`.

## Ce que contient ce dossier
| Chemin | Contenu | Validé sur MM |
|---|---|---|
| `references/maplibre/` | Références MapLibre GL JS : `maplibre-cartography.md` (lisibilité des symboles et des étiquettes sur imagerie, hiérarchie visuelle, ordre des calques) et `maplibre-terrain-rendering.md` (relief, ombrage). Sources MIT, `LICENSE.md` et `NOTICE` dans le dossier (projet MapLibre Agent Skills, commit `6149b9b4…` du 22/10/2026, inspiré de mapbox-agent-skills, © Mapbox, MIT) | audit stratégique de MM, 23/10/2026 (Q22) |
| `modeles-e004/` | **Modèles de l'épisode 004 de MM (Alaska)**, copies sans retouche (hors le titre de `papier/index.html`) : `preparer_globe.py`, `preparer_papier.py`, `vols.py`, `globe/` (`carte.html`, `serve.py`, `capturer.mjs`, `vendor/maplibre-6.13.0/`), `papier/index.html` | 26/10/2026 (globe et cinématique), 28/10/2026 (versés) |

## Modèles de l'E004 : à adapter, pas à lancer tels quels
- Les chemins, les vues (Alaska, Alberta, Prudhoe), les vols, les emprises Sentinel-2 et les couleurs (papier, encre, terre, mer de la palette « Ledger » de MM) sont écrits pour l'épisode 004. Un épisode copie ce qu'il lui faut dans son `kit/cartes/` et l'adapte ; les couleurs se lisent dans `marque/` de la chaîne.
- `preparer_globe.py` importe `present` de `traiter.py` : c'est l'étalonnage « present » de MM, non versé (le `traiter.py` du plugin est neutre, voir `${CLAUDE_PLUGIN_ROOT}/outils/medias/README.md`). La chaîne fournit son propre étalonnage.
- `preparer_*.py` importent `proj` et `shp` : les copier à côté, ou ajouter `${CLAUDE_PLUGIN_ROOT}/outils/cartes/` au chemin de recherche. Ils demandent scipy (déjà dans `starter/requirements.txt`).
- `globe/serve.py` : serveur local sur 127.0.0.1 seulement, arrêté juste après les captures ; le chemin des polices est à adapter. `globe/capturer.mjs` : captures par le Chrome sans fenêtre de HyperFrames (puppeteer-core du projet, Node 22), MP4 direct et ancres. Jamais pendant un rendu.
- `vendor/maplibre-6.13.0/` : MapLibre GL 6.13.0 en copie locale, licence BSD-3 (`LICENSE.txt`). **Tuiles jamais en ligne** : aucun réseau extérieur, tout est servi par `serve.py`.
- Les données (Blue Marble NASA, Sentinel-2, Natural Earth, relief SR_HR) ne sont pas dans le plugin : à télécharger avec l'accord du propriétaire, licences dans le `PROVENANCE.md` de l'épisode. L'imagerie EOX non commerciale est exclue.

## Règles de cartographie retenues sur MM
- **La carte est un décor**, pas une diapositive : fonds calculés à l'avance (relief teinté, imagerie étalonnée), caméra qui voyage, étiquettes et crédits posés en 2D par le producteur, jamais incrustés dans la page MapLibre.
- **Le globe pour voyager, la feuille papier pour compter** (MM, 26/10/2026) : le globe MapLibre sert aux vols de caméra (un seul mouvement par moment de carte, adouci, inclinaison 45° au plus, aucun zoom suivi d'un dézoom) ; la feuille papier (projection à aires justes, relief teinté, traits d'encre) sert aux quantités et aux comparaisons.
- **Projections** (`outils/cartes/proj.py`) : Albers conique équivalente pour une région de moyenne latitude (paramètres propres à la région : Alaska Albers EPSG:3338 en exemple), UTM pour lire des tuiles Sentinel-2, **Equal Earth pour le monde**, Web Mercator pour les tuiles du globe. Jamais de plate carrée pour un monde dont on compare des surfaces. Ne jamais redresser une carte d'un facteur : lire le cadre et l'échelle dans la sortie (voir `outils/cartes/README.md`).
- **Limite à dire** : MapLibre GL n'a pas été vérifié dans le Chrome de rendu de toutes les configurations (MM, Q23) ; capturer une vue d'essai avant de bâtir une séquence dessus.
- **Part de la carte** : sur MM, 20 % au plus d'une séquence (règle de la chaîne, dans son `direction/ECARTS.md`, pas une règle du plugin).
- Miniature « carte-repère » et accroche « la carte qu'on croit connaître » : propres à MM (voir le `DOMAINE.md` du domaine si le propriétaire les y a versées).
