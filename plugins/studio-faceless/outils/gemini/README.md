# Outils Gemini

Appels réseau vers l'API Gemini de Google : seuls outils du plugin dans ce cas. Clé `GEMINI_API_KEY` (environnement, sinon variables utilisateur Windows), jamais affichée ni écrite. Un contenu inédit ne part chez Google qu'avec la clé du palier payant : décision du propriétaire, hors plugin. Ne jamais écraser un fichier existant.

| Outil | Rôle | Commande (depuis la racine de la chaîne) | Validé sur MM |
|---|---|---|---|
| `regarder.py` | Fait « regarder » une vidéo YouTube publique (skill `studio-faceless:regarder`) | voir le skill | 23/10/2026 |
| `relire.py` | Fait relire un script (narration seule) par Gemini avec une consigne de spectateur curieux ; écrit l'avis, à lire comme une hypothèse | `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/gemini/relire.py SCRIPT.md --consigne CONSIGNE.md --sortie AVIS.md [--modele gemini-3.8-flash]` | 23/10/2026, consigne v2 du 29/10/2026 |

`relire.py` versé de MM le 30/10/2026. La consigne de spectateur est celle de la chaîne (le plugin n'en fournit pas) ; l'avis se confronte à `outils/controle/script.py` et au test de décrochage du propriétaire.
