"""Test de controle/mesurer_sons.py (0.6.0, 02/11/2026) : tri des étiquettes de Whisper et des points à voir, sans FFmpeg ni numpy.

Usage, depuis la racine du dépôt du plugin :
  python -I -B plugins/studio-faceless/outils/test_mesurer_sons.py
Code de sortie : 0 = tests passés ; 1 = échec. Bibliothèque standard seule (numpy n'est importé que pour mesurer un vrai fichier).
"""
import importlib.util, os, unittest

_spec = importlib.util.spec_from_file_location('mesurer_sons', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'controle', 'mesurer_sons.py'))
ms = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ms)


class Parole(unittest.TestCase):
    def test_etiquettes_de_bruit_ne_sont_pas_de_la_parole(self):
        for texte in ('[Music] (upbeat music) (upbeat music)', '[APPLAUSE] [APPLAUSE] (buzzing)', '(crowd cheering)', '', '   ', '♪ ♪', '*applause*'):
            with self.subTest(texte=texte):
                self.assertEqual(ms.mots_de_parole(texte), [])

    def test_des_mots_restent(self):
        self.assertEqual(ms.mots_de_parole('[Music] Thank you for watching (applause) everyone'), ['Thank', 'you', 'for', 'watching', 'everyone'])
        self.assertEqual(ms.mots_de_parole("don't stop 3 times"), ["don't", 'stop', '3', 'times'])


class APoint(unittest.TestCase):
    def test_rien_a_voir(self):
        info = {'codec': 'mp3', 'sr': 44100, 'bits': None, 'tp': -3.2, 'ecart_boucle': 0.4}
        self.assertEqual(ms.points_a_voir(info, 0.0, True, []), [])

    def test_points(self):
        info = {'codec': 'pcm_mulaw', 'sr': 8000, 'bits': 8, 'tp': 0.7, 'ecart_boucle': 3.0}
        pts = ms.points_a_voir(info, 0.0, True, ['hello', 'there'])
        self.assertEqual(len(pts), 5)
        self.assertTrue(any('8 bits' in p for p in pts))
        self.assertTrue(any('+0.7' in p for p in pts))
        self.assertTrue(any('boucle' in p for p in pts))
        self.assertTrue(any('parole possible' in p for p in pts))

    def test_boucle_seulement_si_demandee(self):
        info = {'codec': 'mp3', 'sr': 44100, 'bits': None, 'tp': -3.0, 'ecart_boucle': 6.0}
        self.assertEqual(ms.points_a_voir(info, 0.0, False, None), [])


if __name__ == '__main__':
    unittest.main()
