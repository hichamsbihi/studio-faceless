# Outils des médias

Versés de Maps & Means (MM) le 30/10/2026, validés sur MM. Les réglages de MM sont des valeurs par défaut ou des exemples d'aide. Aucun appel réseau. Lancement depuis la racine de la chaîne, avec `python -I -B` et le chemin du script dans le plugin (`${CLAUDE_PLUGIN_ROOT}/outils/medias/…`). FFmpeg : `HYPERFRAMES_FFMPEG_PATH`, sinon le `PATH`.

| Outil | Rôle | Commande | Validé sur MM |
|---|---|---|---|
| `traiter.py` | Traite une photo ou découpe un extrait vidéo : 1920 × 1080, 30 i/s, GOP 15, sans son, 6 s au plus ; **toute source HDR ramenée en SDR BT.709** (une source HDR fait passer HyperFrames en rendu « en couches » : image figée) ; sans étalonnage, ou avec `--filtre` / `--filtre-fichier` (chaîne de filtres FFmpeg rangée dans `marque/`) | `traiter.py SOURCE SORTIE [--debut S] [--duree D] [--cadre couvrir\|contenir] [--filtre "VF"]` | 24/10/2026 |
| `jbig2_page.py` | Rend en image (PGM) la page d'un scan PDF codé en JBIG2 (Python et numpy) ; écrit d'après ITU-T T.88 et pdf.js (Apache-2.0) | `jbig2_page.py FICHIER.pdf PAGE SORTIE.pgm` | 28/10/2026 |
| `rendre_page_pdf.ps1` | Rend une page de PDF en PNG par le moteur PDF de Windows (Windows seulement) ; ne décode pas le JBIG2 ; le moteur multiplie la définition par l'échelle de l'écran | `powershell -NoProfile -File rendre_page_pdf.ps1 PDF PAGE DPI DOSSIER NOM` | 28/10/2026 |

Les traitements de couleur `present` et `archive` de MM (charte de l'épisode 003) ne sont pas versés : ils sont propres à la chaîne. Une chaîne qui veut un étalonnage écrit sa chaîne de filtres dans `marque/` et la passe à `traiter.py`. `render.sh` du gabarit de séquence refuse une vidéo HDR dans `media/` et renvoie à `traiter.py`.
