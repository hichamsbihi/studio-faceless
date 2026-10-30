# Outils de recherche

Versé de Maps & Means (MM) le 30/10/2026, validé sur MM le 28/10/2026 (épisode 005). Bibliothèque standard seule, aucun appel réseau.

| Outil | Rôle | Commande (depuis la racine de la chaîne) |
|---|---|---|
| `pdftexte.py` | Extrait le texte d'un PDF local (flux FlateDecode, opérateurs Tj et TJ), sans poppler ; avec des mots clés, affiche leurs deux premiers passages avec contexte | `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/recherche/pdftexte.py FICHIER.pdf ["mot clé" …]` |

Limites : polices à encodage personnalisé et scans (images) restent illisibles ; l'ordre de lecture suit celui du fichier. Pour un scan JBIG2 : `${CLAUDE_PLUGIN_ROOT}/outils/medias/jbig2_page.py`, puis lecture de l'image. Le PDF est un fichier local : tout téléchargement se fait avec l'accord du propriétaire.
