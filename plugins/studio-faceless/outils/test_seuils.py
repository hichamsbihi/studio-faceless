"""Tests de seuils.py et de referentiels/seuils.json (1.1.0, 04/11/2026).

Usage, depuis la racine du dépôt du plugin :
  python -I -B plugins/studio-faceless/outils/test_seuils.py
Code de sortie : 0 = tests passés ; 1 = échec. Bibliothèque standard seule.
"""
import importlib.util, json, os, re, shutil, tempfile, unittest

ICI = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.dirname(ICI)
_spec = importlib.util.spec_from_file_location('seuils', os.path.join(ICI, 'seuils.py'))
seuils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(seuils)


class Lecture(unittest.TestCase):
    def setUp(self):
        self.chaine = tempfile.mkdtemp()
        seuils._cache.clear()

    def tearDown(self):
        shutil.rmtree(self.chaine)
        seuils._cache.clear()

    def test_valeur_du_plugin(self):
        self.assertEqual(seuils.valeur('mix.film_lufs_cible', self.chaine), -16)
        self.assertEqual(seuils.valeur('injection.regles_studio_caracteres_max', self.chaine), 8000)

    def test_ecart_de_chaine(self):
        os.makedirs(os.path.join(self.chaine, 'direction'))
        with open(os.path.join(self.chaine, 'direction', 'seuils.json'), 'w', encoding='utf-8') as f:
            json.dump({'mix': {'film_lufs_cible': -14}, 'paquet': {'alerte_usd': 120}}, f)
        self.assertEqual(seuils.valeur('mix.film_lufs_cible', self.chaine), -14)     # remplacée
        self.assertEqual(seuils.valeur('mix.film_lufs_tolerance', self.chaine), 1)   # gardée
        self.assertEqual(seuils.valeur('paquet.alerte_usd', self.chaine), 120)       # ajoutée par la chaîne

    def test_cle_absente(self):
        with self.assertRaises(KeyError):
            seuils.valeur('mix.inconnue', self.chaine)


class Citations(unittest.TestCase):
    def test_cles_citees_existent(self):
        """Chaque `section.cle` citée dans le texte du plugin existe dans seuils.json (une clé fausse est un renvoi mort)."""
        with open(os.path.join(PLUGIN, 'referentiels', 'seuils.json'), encoding='utf-8') as f:
            donnees = json.load(f)
        sections = {k for k in donnees if not k.startswith('_')}
        cles = {f'{s}.{k}' for s in sections for k in donnees[s] if not k.startswith('_')}
        motif = re.compile(r'`(?:seuils\.json` \()?((?:' + '|'.join(sorted(sections)) + r')\.[a-z0-9_*]+)`')
        manquantes = []
        for d, sous, fichiers in os.walk(PLUGIN):
            sous[:] = [s for s in sous if s not in ('vendor', '__pycache__')]
            for f in fichiers:
                if f.endswith('.md'):
                    with open(os.path.join(d, f), encoding='utf-8') as fichier:
                        texte = fichier.read()
                    for m in motif.finditer(texte):
                        c = m.group(1)
                        if c.rsplit('.', 1)[1] in ('py', 'md', 'json', 'js', 'mjs', 'sh', 'html', 'txt', 'wav', 'mp4', 'srt'):
                            continue                        # un fichier (`mix.py`, `voix.py`), pas une clé
                        if '*' in c:
                            if not any(re.fullmatch(c.replace('*', '[a-z0-9_]+'), x) for x in cles):
                                manquantes.append((f, c))
                        elif c not in cles:
                            manquantes.append((f, c))
        self.assertEqual(manquantes, [])


if __name__ == '__main__':
    unittest.main(verbosity=1)
