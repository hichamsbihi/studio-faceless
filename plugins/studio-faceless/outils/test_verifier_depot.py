"""Test de la détection des secrets (29/10/2026) et de la limite de taille de REGLES_STUDIO.md (0.2.3, 30/10/2026) de verifier_depot.py.

Usage, depuis la racine du dépôt du plugin :
  python -I -B plugins/studio-faceless/outils/test_verifier_depot.py
Les clés d'exemple sont assemblées à l'exécution : écrites d'un seul tenant, elles feraient refuser ce fichier par verifier_depot.py.
Code de sortie : 0 = tests passés ; 1 = échec. Bibliothèque standard seule.
"""
import importlib.util, os, unittest

_spec = importlib.util.spec_from_file_location('verifier_depot', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verifier_depot.py'))
verifier_depot = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(verifier_depot)

# « sk- » ou « sk_ » au milieu d'un mot : pas une clé
FAUX_POSITIFS = [
    'https://www.lemondedudroit.fr/decryptages/1576-laffaire-dsk-une-exploitation-mediatique-a-lepreuve-de-la-loi-sur-la-liberte-de-la',
    'risk-assessment-for-the-whole-team',
    'task-runner-configuration-file-name',
    'desk-reference-guide-for-new-editors',
    'mask_abcdefghijklmnopqrstuvwxyz',
]
# clé en début de jeton : détectée
SECRETS = [
    'sk' + '-ant-api03-' + 'Ab3d' * 10,
    'OPENAI_API_KEY=' + 'sk' + '-proj-' + 'Xy9z' * 8,
    'cle = "' + 'sk' + '_' + 'f3a9' * 12 + '"',
    'STRIPE_KEY=' + 'sk' + '_live_' + '51Hx' * 8,
    'token: ' + 'gh' + 'p_' + 'a1B2' * 9,
]


class Secret(unittest.TestCase):
    def test_faux_positifs(self):
        for texte in FAUX_POSITIFS:
            with self.subTest(texte=texte):
                self.assertIsNone(verifier_depot.SECRET.search(texte))

    def test_secrets(self):
        for texte in SECRETS:
            with self.subTest(texte=texte[:18]):
                self.assertIsNotNone(verifier_depot.SECRET.search(texte))


class TailleRegles(unittest.TestCase):
    """REGLES_STUDIO.md est injecté par le hook SessionStart : l'application coupe tout ce qui dépasse 10 000 caractères."""

    def test_le_chemin_est_compte(self):
        # 20 renvois au dossier du plugin : le texte brut est court, le texte injecté est plus long
        brut = '${CLAUDE_PLUGIN_ROOT}/x ' * 20
        self.assertGreater(verifier_depot.taille_regles(brut), len(brut))

    def test_limite(self):
        self.assertLessEqual(verifier_depot.LIMITE_REGLES, 9000)
        self.assertGreater(verifier_depot.taille_regles('a' * 9001), verifier_depot.LIMITE_REGLES)
        self.assertLessEqual(verifier_depot.taille_regles('a' * 9000), verifier_depot.LIMITE_REGLES)

    def test_regles_du_depot(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'REGLES_STUDIO.md')
        if not os.path.isfile(chemin):
            self.skipTest('REGLES_STUDIO.md absent')
        with open(chemin, encoding='utf-8') as f:
            self.assertLessEqual(verifier_depot.taille_regles(f.read()), verifier_depot.LIMITE_REGLES)


if __name__ == '__main__':
    unittest.main()
