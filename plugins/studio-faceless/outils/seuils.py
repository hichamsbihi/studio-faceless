"""Valeurs chiffrées du studio (1.1.0) : `referentiels/seuils.json` du plugin, puis `direction/seuils.json` de la chaîne par-dessus.

Une seule source par valeur : un outil lit sa cible ici au lieu de la recopier. Une chaîne remplace une clé dans son
`direction/seuils.json` (même structure), et l'inscrit dans `direction/ECARTS.md` (« Remplace : <clé> »).
Usage dans un outil (lancé par `python -I`, qui retire le dossier du script de sys.path) :
  sys.path.insert(0, <dossier outils/>) ; import seuils ; seuils.valeur('mix.film_lufs_cible')
En ligne de commande : python -I -B <plugin>/outils/seuils.py mix.film_lufs_cible
"""
import json, os, sys

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_cache = {}


def _fusion(base, dessus):
    for k, v in dessus.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _fusion(base[k], v)
        else:
            base[k] = v
    return base


def charger(chaine=None):
    chaine = os.path.normpath(chaine or os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd())
    if chaine not in _cache:
        with open(os.path.join(PLUGIN, 'referentiels', 'seuils.json'), encoding='utf-8') as f:
            donnees = json.load(f)
        propre = os.path.join(chaine, 'direction', 'seuils.json')
        if os.path.isfile(propre):
            with open(propre, encoding='utf-8') as f:
                _fusion(donnees, json.load(f))
        _cache[chaine] = donnees
    return _cache[chaine]


def valeur(cle, chaine=None):
    """Valeur d'une clé pointée (« mix.film_lufs_cible ») ; KeyError si elle n'existe pas : jamais de valeur recopiée en repli."""
    d = charger(chaine)
    for partie in cle.split('.'):
        d = d[partie]
    return d


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    for c in sys.argv[1:]:
        print(f'{c} = {valeur(c)}')
