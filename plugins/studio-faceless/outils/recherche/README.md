# Outils de recherche

`pdftexte.py` : versé de Maps & Means (MM) le 30/10/2026, validé sur MM le 28/10/2026 (épisode 005), sans appel réseau. `youtube_chaine.py` et `youtube_resume.py` : versés d'AA le 02/11/2026. Bibliothèque standard seule.

| Outil | Rôle | Commande (depuis la racine de la chaîne) |
|---|---|---|
| `pdftexte.py` | Extrait le texte d'un PDF local (flux FlateDecode, opérateurs Tj et TJ), sans poppler ; avec des mots clés, affiche leurs deux premiers passages avec contexte | `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/recherche/pdftexte.py FICHIER.pdf ["mot clé" …]` |
| `youtube_chaine.py` | Relève toutes les vidéos publiques d'une chaîne par l'API YouTube Data v3 (titre, date, durée, court ou long, vues, ratio = vues ÷ médiane des 30 longues voisines) ; refuse d'écraser ; clé `YOUTUBE_API_KEY` posée par le propriétaire dans l'environnement. Validé sur AA (26/10 et 02/11/2026). Seul outil de ce dossier qui appelle le réseau | `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/recherche/youtube_chaine.py @handle docs/veille/donnees/<chaine>-<date>.json` |
| `youtube_resume.py` | Résume un relevé de `youtube_chaine.py` sans lire le JSON en entier : formats, années, titres, plus forts ratios, territoires par motifs JSON, sponsors. Lecture locale, sans appel réseau. Validé sur AA (02/11/2026) | `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/recherche/youtube_resume.py releve.json [--top N] [--territoires motifs.json] [--liste]` |

Limites de `pdftexte.py` : polices à encodage personnalisé et scans (images) restent illisibles ; l'ordre de lecture suit celui du fichier. Pour un scan JBIG2 : `${CLAUDE_PLUGIN_ROOT}/outils/medias/jbig2_page.py`, puis lecture de l'image. Le PDF est un fichier local : tout téléchargement se fait avec l'accord du propriétaire.
