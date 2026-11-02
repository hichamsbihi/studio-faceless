"""Test des deux ajouts de la 0.6.0 au garde-fou (hooks/garde_commandes.py), 02/11/2026 : rôle `telechargeur` (agent `media-fetcher`) et
interdiction faite au rôle `stratege` de lancer `youtube_retention.py` (réservé à Claude principal).

Usage, depuis la racine du dépôt du plugin :
  python -I -B plugins/studio-faceless/outils/test_garde_commandes.py
Le plugin installé et la chaîne sont simulés par des dossiers temporaires. Code de sortie : 0 = tests passés ; 1 = échec. Bibliothèque standard seule.
"""
import importlib.util, os, tempfile, unittest

_spec = importlib.util.spec_from_file_location('garde_commandes', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'hooks', 'garde_commandes.py'))
garde = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(garde)

UA = '"Robot-MediaFetch/1.0 (https://exemple.org/chaine)"'


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.racine = os.path.join(self.tmp.name, 'chaine')
        self.plugin = os.path.join(self.tmp.name, 'cache', 'studio-faceless', '0.6.0').replace('\\', '/')
        os.makedirs(self.racine)
        self.ancien = os.environ.get('CLAUDE_PLUGIN_ROOT')
        os.environ['CLAUDE_PLUGIN_ROOT'] = self.plugin

    def tearDown(self):
        if self.ancien is None:
            os.environ.pop('CLAUDE_PLUGIN_ROOT', None)
        else:
            os.environ['CLAUDE_PLUGIN_ROOT'] = self.ancien
        self.tmp.cleanup()

    def bash(self, commande, role):
        return garde.decide_bash(commande, role, self.racine)


class Stratege(Base):
    def test_ses_outils_restent_permis(self):
        for outil in ('youtube_chaine.py', 'youtube_resume.py'):
            with self.subTest(outil=outil):
                self.assertIsNone(self.bash(f'python -I -B "{self.plugin}/outils/recherche/{outil}" @chaine docs/veille/donnees/x.json', 'stratege'))

    def test_youtube_retention_est_refuse(self):
        verdict = self.bash(f'python -I -B "{self.plugin}/outils/recherche/youtube_retention.py" @chaine docs/veille/donnees/r.json', 'stratege')
        self.assertEqual(verdict[0], 'deny')
        self.assertIn('Claude principal', verdict[1])

    def test_claude_principal_le_lance(self):
        self.assertIsNone(self.bash(f'python -I -B "{self.plugin}/outils/recherche/youtube_retention.py" @chaine docs/veille/donnees/r.json', None))


class Telechargeur(Base):
    LISTE = 'episodes/episode-011/kit/LISTE_TELECHARGEMENT_v1.json'
    RACINE = 'episodes/episode-011/kit/media/source-v1'

    def outil(self, *plus):
        return f'python -I -B "{self.plugin}/outils/medias/telecharger_medias.py" {" ".join(plus)}'

    def test_role_reconnu(self):
        self.assertEqual(garde.role_of({'agent_type': 'studio-faceless:media-fetcher'}), 'telechargeur')
        self.assertEqual(garde.ROLES['media-fetcher'], 'telechargeur')

    def test_commande_permise(self):
        for fin in ('', ' --executer'):
            with self.subTest(fin=fin):
                self.assertIsNone(self.bash(self.outil(self.LISTE, '--racine', self.RACINE, '--agent-utilisateur', UA) + fin, 'telechargeur'))
        self.assertIsNone(self.bash(self.outil(self.LISTE, f'--racine={self.RACINE}', '--agent-utilisateur', UA, '--pause', '4'), 'telechargeur'))
        self.assertIsNone(self.bash(f'ls {self.RACINE}', 'telechargeur'))
        self.assertIsNone(self.bash(f'mkdir {self.RACINE}/manuel', 'telechargeur'))

    def test_commandes_refusees(self):
        refusees = [
            'curl -sS -o x.jpg https://exemple.org/a.jpg',
            'wget https://exemple.org/a.jpg',
            'python -c "print(1)"',
            f'python -I -B "{self.plugin}/outils/recherche/youtube_retention.py" @chaine docs/x.json',
            f'python -I -B "{self.plugin}/outils/medias/traiter.py" a b',
            'python -I -B outils/medias/telecharger_medias.py liste.json',                       # outil copié hors du plugin installé
            f'python -I -B "{self.plugin}/../autre/outils/medias/telecharger_medias.py" liste.json',
            self.outil(self.LISTE, '--racine', 'marque/son', '--agent-utilisateur', UA),         # dépôt hors de source-vN
            self.outil(self.LISTE, '--racine', 'episodes/episode-011/inputs', '--agent-utilisateur', UA),
            self.outil('direction/ECARTS.md', '--racine', self.RACINE, '--agent-utilisateur', UA),   # liste hors du kit
            self.outil(self.LISTE, '--racine', self.RACINE, '--manifeste', 'direction/m.json', '--agent-utilisateur', UA),
            self.outil(self.LISTE, '--racine', '"marque/son x"', '--agent-utilisateur', UA),     # chemin avec une espace
            self.outil(self.LISTE, '--racine', '"D:/autre dossier/x"', '--agent-utilisateur', UA),
            self.outil(self.LISTE, '--racine', 'marque', '--agent-utilisateur', UA),             # chemin sans « / » ni « . »
            self.outil(self.LISTE, '--racine=marque/son', '--agent-utilisateur', UA),            # forme --option=valeur
            self.outil(self.LISTE, '--rac', 'marque/son', '--agent-utilisateur', UA),            # option abrégée
            self.outil(self.LISTE, '--racine', self.RACINE, '--manifeste', '"direction/m x.json"', '--agent-utilisateur', UA),
            f'ls {self.RACINE} > direction/x.txt',
            f'cp {self.LISTE} marque/x.json',
        ]
        for commande in refusees:
            with self.subTest(commande=commande[:70]):
                verdict = self.bash(commande, 'telechargeur')
                self.assertIsNotNone(verdict)
                self.assertEqual(verdict[0], 'deny')

    def test_ecriture_write_edit(self):
        def ecrire(rel):
            return garde.decide_write(os.path.join(self.racine, *rel.split('/')), 'telechargeur', self.racine)
        self.assertIsNone(ecrire('episodes/episode-011/kit/media/source-v1/manuel/A_TELECHARGER.md'))
        self.assertIsNone(ecrire('episodes/episode-011/kit/media/source-v2/MANIFESTE.json'))
        for refuse in ('episodes/episode-011/kit/DEMANDE_TELECHARGEMENTS_v1.md', 'episodes/episode-011/kit/media/photos-v1/x.jpg',
                       'episodes/episode-011/inputs/x.txt', 'direction/ECARTS.md', 'marque/son/x.wav', 'CLAUDE.md', '../hors/chaine.txt'):
            with self.subTest(rel=refuse):
                verdict = ecrire(refuse)
                self.assertIsNotNone(verdict)
                self.assertEqual(verdict[0], 'deny')


if __name__ == '__main__':
    unittest.main()
