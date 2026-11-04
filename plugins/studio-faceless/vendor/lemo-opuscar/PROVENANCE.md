# lemo-opuscar (copie suivie par paliers)

**Origine** : https://github.com/lemomo-ai/lemo-opuscar, commit `bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00` (31/10/2026), copié le 03/11/2026 (2 083 fichiers, 43,2 Mo). Fichiers copiés tels quels, sans modification ; seul ce `PROVENANCE.md` est ajouté.

**Licence** (`LICENSE` et section « Licence » du `README.md` d'origine) :
- code et documentation, `STYLE.md` et `DEMO.md` compris : MIT, © 2026 LemoLab ;
- films de démo et leurs images, `poster.jpg` compris : CC BY 4.0, crédit « LemoLab » avec un lien vers le dépôt, et mention d'une modification ;
- médias de tiers dans une démo : leur propre licence, dans le `CREDITS` de la démo, à relire avant tout emploi ;
- trois pistes de voix exclues de la licence (Game Show Flat, Paper-cut Lightbox, Broadcast News Package) : elles ne sont pas dans cette copie et ne s'emploient pas.

**Usage dans le studio** (validé sur AA, 03 et 04/11/2026) : une bibliothèque de styles, pas un skill ni un moteur. Ses règles (forme A, portage et fiche de rendu, notice MIT, consignes neutralisées, cadence, familles permises, paliers) sont dans `referentiels/STYLES.md` du plugin, seule source depuis la 1.1.0.

## Contenu
| Ici | Rôle |
|---|---|
| `styles/<style>/STYLE.md` | Le style en clair : intention, palette, typographie, mouvement, règles |
| `styles/<style>/style.json` | Fiche courte du style : nom, catégorie (`category_en`, 11 catégories, par exemple « Edit & Documentary », « Evidence Films », « Information & Keynote »), film de démo, usages (`uses`), durée ; pour le tri |
| `styles/<style>/poster.jpg` | Affiche du style (66 affiches), pour le tri à l'œil |
| `styles/<style>/DEMO.md`, `demo/` | Démo du style : code de dessin, données, polices, `CREDITS`, `SOURCES` ; `demo/tools/` contient des outils de contrôle, dont `briefing-board/demo/tools/rhythm_report.py` (essayé le 03/11/2026 sur un extrait de 30 s en 16:9 et en 9:16 : il suppose 24 i/s, donc des temps d'image faux sur un film à 30 i/s ; il compte une transition rapide comme plusieurs coupes ; il garde tout le film en mémoire et écrit dans son propre dossier, donc jamais lancé d'ici) |
| `styles/_template/` | Gabarit vide d'un style (sans affiche) |
| `styles/README.md` | Index des styles du dépôt d'origine |
| `core/` | Code commun des démos : `render/` (leur moteur d'images, non employé), `post/` et `three/` (effets), `fonts/`, `tts/`, `audio/` (`sampler.py` et `pluck.py` pour composer sur les banques d'instruments, `sfx.py` pour les effets fabriqués en code, `INSTRUMENTS.md`) |
| `README.md`, `TECHNIQUE.md`, `DIRECTOR.md`, `LICENSE` | Présentation, technique et méthode de choix du dépôt d'origine, licence |

**Non copié** :
- les images fixes des démos (`styles/*/demo/stills/`, 33 Mo) ;
- les textures 3D de `core/assets/polyhaven/` (12 Mo ; la 3D n'est pas une famille permise par défaut) ;
- `styleboard/`, `docs/` ;
- leur installeur et leurs outils de dépôt (`tools/`, `setup.sh`, `fetch.sh`, `release.py`) ;
- leur skill et leurs manifestes de plugin (`plugin/`, `.claude-plugin/`) ;
- `AGENTS.md`, `CLAUDE.md`, `MAINTAINING.md`, `MY-STYLES.md` ;
- leurs `package.json` et `requirements*.txt`.

**Banques d'instruments** (`core/audio/instruments/`, 1,42 Go, release `assets` du dépôt) : hors du plugin, trop lourdes. Une chaîne qui les veut les télécharge hors Git, sur décision de son propriétaire, et les consigne dans un `PROVENANCE.md` à côté d'elles (licences : CC0, sauf Salamander en CC BY 3.0 et MuldjordKit en CC BY 4.0, crédits dans la description de la vidéo).

**Mise à jour par paliers** : règle dans `referentiels/STYLES.md` § Bibliothèque. Chaque palier change le commit indiqué en tête de ce fichier.
