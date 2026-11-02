"""Test hors réseau de voix/generer_voix.py et voix/info_elevenlabs.py (0.6.0, 02/11/2026) : coût annoncé, confirmation obligatoire, aucun écrasement, clé jamais écrite.

Usage, depuis la racine du dépôt du plugin :
  python -I -B plugins/studio-faceless/outils/test_generer_voix.py
Aucun appel à ElevenLabs : le client et l'appel payant sont remplacés par des faux. Code de sortie : 0 = tests passés ; 1 = échec. Bibliothèque standard seule.
"""
import contextlib, hashlib, importlib.util, io, json, os, tempfile, unittest


def charger(nom):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voix', nom + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gv = charger('generer_voix')
info = charger('info_elevenlabs')

FAUSSE_CLE = 'cle-factice-pour-le-test'
SCRIPT = 'Premier texte de la prise une.\n\n\nDeuxième texte, plus long que le premier.\n\n\n\nTroisième.\n'


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.script = os.path.join(self.tmp.name, 'script.txt')
        with open(self.script, 'w', encoding='utf-8') as f:
            f.write(SCRIPT)
        self.sortie = os.path.join(self.tmp.name, 'prises')
        self.appels = []

    def tearDown(self):
        self.tmp.cleanup()

    def args(self, *plus):
        return gv.lire_arguments([self.script, '--voix', 'VOIX_ID', '--sortie', self.sortie, '--nom', 'E00N_S{n}_voix_v1.mp3', *plus])

    def convertir(self, client, texte, a):
        self.appels.append(texte)
        return ('AUDIO:' + texte).encode('utf-8')

    def lancer(self, *plus, env=None, convertir=None):
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            code = gv.lancer(self.args(*plus), env={gv.CLE: FAUSSE_CLE} if env is None else env,
                             fabrique=lambda cle: object(), convertir=convertir or self.convertir)
        return code, sortie.getvalue()


class Cout(Base):
    def test_decoupage(self):
        self.assertEqual(gv.decouper(SCRIPT), ['Premier texte de la prise une.', 'Deuxième texte, plus long que le premier.', 'Troisième.'])
        self.assertEqual(gv.decouper('Un.\n\nDeux sur la même prise.'), ['Un.\n\nDeux sur la même prise.'])

    def test_cout(self):
        self.assertEqual(gv.cout('abcd', 1.0), 4)
        self.assertEqual(gv.cout('abcd', 0.5), 2)
        self.assertEqual(gv.cout('abc', 0.5), 2)                              # arrondi au crédit supérieur

    def test_apercu_annonce_le_cout_sans_appel_ni_cle(self):
        def interdit(*a, **k):
            raise AssertionError('appel pendant l\'aperçu')
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            code = gv.lancer(self.args(), env={}, fabrique=interdit, convertir=interdit)
        texte = sortie.getvalue()
        total = sum(len(t) for t in gv.decouper(SCRIPT))
        self.assertEqual(code, 0)
        self.assertIn(f'COÛT ANNONCÉ : {total} crédits pour 3 prise(s)', texte)
        self.assertIn(f'--confirme-credits {total}', texte)
        self.assertFalse(os.path.exists(self.sortie))                        # rien n'est créé

    def test_prises_choisies(self):
        _, texte = self.lancer('--prises', '2')
        self.assertIn(f"COÛT ANNONCÉ : {len(gv.decouper(SCRIPT)[1])} crédits pour 1 prise(s)", texte)
        with self.assertRaises(ValueError):
            self.lancer('--prises', '9')

    def test_blocs_et_nom(self):
        with self.assertRaises(ValueError):
            self.lancer('--blocs', '4')
        with self.assertRaises(ValueError):
            gv.destination(self.sortie, 'sans-numero.mp3', 1)
        with self.assertRaises(ValueError):
            gv.destination(self.sortie, '../dehors_{n}.mp3', 1)


class Paiement(Base):
    def total(self, *numeros):
        prises = gv.decouper(SCRIPT)
        return sum(len(prises[n - 1]) for n in (numeros or (1, 2, 3)))

    def test_rien_sans_confirmation(self):
        with self.assertRaises(PermissionError):
            self.lancer('--executer')
        with self.assertRaises(PermissionError):
            self.lancer('--executer', '--confirme-credits', str(self.total() - 1))
        with self.assertRaises(PermissionError):
            self.lancer('--executer', '--confirme-credits', str(self.total() + 1))
        self.assertEqual(self.appels, [])
        self.assertFalse(os.path.exists(self.sortie))

    def test_sans_cle(self):
        with self.assertRaises(PermissionError) as c:
            self.lancer('--executer', '--confirme-credits', str(self.total()), env={})
        self.assertIn('ELEVENLABS_API_KEY', str(c.exception))
        self.assertEqual(self.appels, [])

    def test_generation_confirmee(self):
        code, texte = self.lancer('--executer', '--confirme-credits', str(self.total()))
        self.assertEqual(code, 0)
        self.assertEqual(len(self.appels), 3)
        premier = os.path.join(self.sortie, 'E00N_S1_voix_v1.mp3')
        with open(premier, 'rb') as f:
            audio = f.read()
        manifestes = [n for n in os.listdir(self.sortie) if n.startswith('MANIFESTE_VOIX_')]
        self.assertEqual(len(manifestes), 1)
        with open(os.path.join(self.sortie, manifestes[0]), encoding='utf-8') as f:
            brut = f.read()
        manifeste = json.loads(brut)
        self.assertEqual(manifeste['credits_annonces'], self.total())
        self.assertEqual(manifeste['prises'][0]['sha1'], hashlib.sha1(audio).hexdigest())
        self.assertNotIn(FAUSSE_CLE, texte)                                  # la clé n'est jamais écrite ni affichée
        self.assertNotIn(FAUSSE_CLE, brut)

    def test_aucun_ecrasement_avant_le_premier_appel(self):
        os.makedirs(self.sortie)
        existant = os.path.join(self.sortie, 'E00N_S2_voix_v1.mp3')
        with open(existant, 'wb') as f:
            f.write(b'PRISE APPROUVEE')
        with self.assertRaises(FileExistsError):
            self.lancer('--executer', '--confirme-credits', str(self.total()))
        self.assertEqual(self.appels, [])                                    # pas un crédit dépensé pour la prise 1
        with open(existant, 'rb') as f:
            self.assertEqual(f.read(), b'PRISE APPROUVEE')

    def test_premiere_erreur_arrete_tout_et_masque_la_cle(self):
        def casse(client, texte, a):
            self.appels.append(texte)
            if len(self.appels) == 2:
                raise RuntimeError('refus de la clé ' + FAUSSE_CLE)
            return b'AUDIO'
        sortie = io.StringIO()
        erreurs = io.StringIO()
        with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(erreurs):
            code = gv.lancer(self.args('--executer', '--confirme-credits', str(self.total())), env={gv.CLE: FAUSSE_CLE},
                             fabrique=lambda cle: object(), convertir=casse)
        self.assertEqual(code, 1)
        self.assertEqual(len(self.appels), 2)                                # la prise 3 n'est pas lancée
        self.assertNotIn(FAUSSE_CLE, erreurs.getvalue())
        self.assertIn('***', erreurs.getvalue())
        self.assertTrue(os.path.exists(os.path.join(self.sortie, 'E00N_S1_voix_v1.mp3')))
        self.assertFalse(os.path.exists(os.path.join(self.sortie, 'E00N_S2_voix_v1.mp3')))
        manifeste = [n for n in os.listdir(self.sortie) if n.startswith('MANIFESTE_VOIX_')]
        with open(os.path.join(self.sortie, manifeste[0]), encoding='utf-8') as f:
            brut = f.read()
        self.assertNotIn(FAUSSE_CLE, brut)
        self.assertIn('arret', brut)

    def test_main_refuse_proprement(self):
        erreurs = io.StringIO()
        with contextlib.redirect_stderr(erreurs), contextlib.redirect_stdout(io.StringIO()):
            code = gv.main([self.script, '--voix', 'V', '--sortie', self.sortie, '--nom', 'x_{n}.mp3', '--executer'])
        self.assertEqual(code, 2)
        self.assertIn('--confirme-credits', erreurs.getvalue())


class Info(unittest.TestCase):
    def test_refus_sans_cle(self):
        with self.assertRaises(PermissionError):
            info.lire(info.argparse.Namespace(modeles=None, tous=False, voix=None), env={})

    def test_refus_affiches_sans_la_cle(self):
        class Client:
            def __init__(self, cle):
                raise_cle = cle

            @property
            def models(self):
                raise RuntimeError("{'message': 'droit refusé pour " + FAUSSE_CLE + "'}")

            @property
            def voices(self):
                raise RuntimeError('refus')

            @property
            def user(self):
                raise RuntimeError('refus')
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            code = info.lire(info.argparse.Namespace(modeles=None, tous=False, voix='V'), env={info.CLE: FAUSSE_CLE}, fabrique=Client)
        self.assertEqual(code, 0)
        self.assertIn('modèles : refusé', sortie.getvalue())
        self.assertNotIn(FAUSSE_CLE, sortie.getvalue())


if __name__ == '__main__':
    unittest.main()
