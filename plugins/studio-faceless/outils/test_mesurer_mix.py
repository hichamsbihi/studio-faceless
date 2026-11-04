"""Tests de outils/montage/mesurer_mix.py (1.1.2) : chaîne de mesure sur des signaux synthétiques, sans fichier.

Cas connu demandé par `musique-par-cues.md` § 4 : résidu nul quand le mix est la voix seule ; puis une musique posée à un écart
connu sous la voix, une musique trop forte, une marque qui monte, une pièce de marque exclue.
Lancer : python -I -B outils/test_mesurer_mix.py
"""
import importlib.util, os, sys, tempfile, unittest

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, 'montage'))
_spec = importlib.util.spec_from_file_location('mesurer_mix', os.path.join(ICI, 'montage', 'mesurer_mix.py'))
mm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mm)
np = mm.np
SR, FPS = mm.SR, mm.FPS


def bruit(n, db, graine):
    """Bruit blanc stéréo identique sur les deux canaux, RMS de db dBFS."""
    x = np.random.default_rng(graine).standard_normal(n).astype(np.float32) * np.float32(10 ** (db / 20))
    return np.stack([x, x], axis=1)


class MesurerMix(unittest.TestCase):
    D = 20                                     # secondes
    G = 4.0                                    # gain final (dB)

    def setUp(self):
        self.N = self.D * SR
        self.segs = [{'id': 'seq1', 'type': 'sequence', 'debut': 0, 'images': self.D * FPS}]
        self.voix = bruit(self.N, -20, 1)
        self.g = np.float32(10 ** (self.G / 20))

    def mesure(self, musique_db, plan_musique=True, effets=(), marques=(), segs=None, mix=None):
        mus = bruit(self.N, musique_db, 2) if musique_db is not None else np.zeros_like(self.voix)
        if mix is None:
            mix = (self.voix + mus) * self.g
        plan = {'musique': [{'id': 'M01', 'fichier': 'm.mp3', 'depart': 0.0, 'fin': float(self.D), 'niveau_lu': -8}]
                if plan_musique else [], 'effets': list(effets), 'niveaux_par_type': {'impact': -8}}
        return mm.mesurer(mix, self.voix.copy(), segs or self.segs, self.D * FPS, plan, '.', list(marques), 7, 9, self.G)

    def test_residu_nul_voix_seule(self):
        r = mm.residu(self.voix * self.g, self.voix, self.segs, self.G)
        self.assertLess(float(np.abs(r).max()), 1e-5)
        tete, corps, hors = self.mesure(None, plan_musique=False)
        self.assertIn('chaîne de mesure', tete[0])
        self.assertTrue('-200' in tete[0] or 'inf' in tete[0] or float(tete[0].split('soit ')[1].split(' LU')[0]) > 60, tete[0])

    def test_ecart_connu(self):
        tete, corps, hors = self.mesure(-28)            # musique 8 dB sous la voix, même spectre
        ligne = next(l for l in corps if l.startswith('| M01'))
        med = float(ligne.split('|')[6])
        self.assertAlmostEqual(med, 8.0, delta=0.2)
        self.assertIn('| OK |', ligne)
        self.assertEqual(hors, 0)

    def test_musique_trop_forte(self):
        tete, corps, hors = self.mesure(-24)            # 4 LU sous la voix
        ligne = next(l for l in corps if l.startswith('| M01'))
        self.assertIn('TROP FORTE', ligne)
        self.assertEqual(hors, 1)

    def test_marque_qui_monte(self):
        mus = bruit(self.N, -30, 2)
        t = 10.0
        i = int(t * SR)
        mus[i:i + SR // 2] += bruit(SR // 2, -16, 3)   # impact de 0,5 s au-dessus de la musique
        mix = (self.voix + mus) * self.g
        effet = {'fichier': 'i.mp3', 'depart': t, 'type': 'impact', 'extrait': [0.0, 0.5]}
        tete, corps, hors = self.mesure(None, effets=[effet], marques=['15.0:repere'], mix=mix)
        l_i = next(l for l in corps if l.startswith('| 0:10.0'))
        hausse = float(l_i.split('|')[5])
        self.assertGreater(hausse, 8.0)
        self.assertIn('| 8 |', l_i)                     # écart prévu par le niveau du type
        l_r = next(l for l in corps if l.startswith('| 0:15.0'))
        self.assertLess(abs(float(l_r.split('|')[5])), 1.0)   # pas de hausse sans événement

    def test_piece_de_marque_exclue(self):
        segs = [{'id': 'seq1', 'type': 'sequence', 'debut': 0, 'images': 10 * FPS},
                {'id': 'logo', 'type': 'marque', 'debut': 10 * FPS, 'images': 10 * FPS}]
        mus = bruit(self.N, -28, 2)
        mix = (self.voix + mus) * self.g
        mix[10 * SR:] = (self.voix + bruit(self.N, -10, 4))[10 * SR:]   # sous la marque : pas de gain final, son fort
        tete, corps, hors = self.mesure(None, segs=segs, mix=mix)
        ligne = next(l for l in corps if l.startswith('| M01'))
        self.assertAlmostEqual(float(ligne.split('|')[6]), 8.0, delta=0.3)

    def test_gain_du_journal(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'a.log.txt')
            with open(p, 'w', encoding='utf-8') as f:
                f.write('Mix du film\nGain final unique +5.10 dB (pièces de marque exclues), limiteur à -2.0 dBTP : 3 réductions\n')
            g, l = mm.gain_du_journal(p)
            self.assertAlmostEqual(g, 5.10)
            self.assertTrue(l.startswith('Gain final unique'))


if __name__ == '__main__':
    unittest.main()
