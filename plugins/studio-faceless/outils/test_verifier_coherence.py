"""Tests de verifier_coherence.py (1.1.0, 04/11/2026) : un test par motif, des faux positifs, la base gelée et un plugin factice.

Usage, depuis la racine du dépôt du plugin :
  python -I -B plugins/studio-faceless/outils/test_verifier_coherence.py
Code de sortie : 0 = tests passés ; 1 = échec. Bibliothèque standard seule.
"""
import importlib.util, json, os, shutil, tempfile, unittest
from collections import Counter

_spec = importlib.util.spec_from_file_location('verifier_coherence', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verifier_coherence.py'))
v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v)
MOTIF = {i: m for i, m, _, _ in v.MOTIFS}


class Motifs(unittest.TestCase):
    def oui(self, ident, ligne):
        self.assertTrue(MOTIF[ident].search(ligne), f'{ident} devrait voir : {ligne}')

    def non(self, ident, ligne):
        self.assertFalse(MOTIF[ident].search(ligne), f'{ident} ne devrait pas voir : {ligne}')

    def test_socle(self):
        self.oui('socle', 'Le kit est le socle des séquences.')
        self.oui('socle', 'Socle : direction artistique')
        self.non('socle', 'Les socleries')            # mot différent

    def test_portes(self):
        self.oui('portes-a-e', 'Contrôle : porte B.')
        self.oui('portes-a-e', 'les portes A à C (§4)')
        self.non('portes-a-e', 'la porte du sujet')
        self.non('portes-a-e', 'Porte : accord de Hicham')

    def test_orchestrateur(self):
        self.oui('orchestrateur', "recopiée par l'orchestrateur")
        self.non('orchestrateur', 'le directeur coordonne')

    def test_conseil(self):
        self.oui('conseil', 'le conseil roast-room')
        self.oui('conseil', 'Conseils de rédaction')
        self.non('conseil', '4 à 6 conseillés')
        self.non('conseil', 'agent conseiller')

    def test_preseance(self):
        for l in ("les écarts l'emportent", 'ses écarts l’emportent', 'la règle prime sur le skill',
                  'Règles du studio (prioritaires sur la suite)', 'le domaine prévaut'):
            self.oui('preseance', l)
        self.non('preseance', 'il emporte le kit')
        self.non('preseance', 'priorité : voir REGLES_STUDIO.md § Priorité')

    def test_unite(self):
        for l in ('−14 LUFS', 'master à -14 LUFS', 'environ 7 LU sous la voix', 'crête ≤ −1 dBTP', '-1,5 dB TP', '+6 LU'):
            self.oui('unite', l)
        for l in ('seuil −42 dBFS', 'LUFS intégrés (seuils.json)', 'v1.14 LU', 'gain de 6 dB'):
            self.non('unite', l)

    def test_propose(self):
        self.oui('propose', 'Statut : `PROPOSÉ` (Claude)')
        self.non('propose', 'proposé par le producteur')

    def test_renvoi_mort(self):
        self.oui('renvoi-mort', 'voir `DEMARRAGE.md`, B6')
        self.oui('renvoi-mort', 'Voir `socle.md`.')
        self.oui('renvoi-mort', 'Les dix agents délégués')
        self.non('renvoi-mort', '`SOCLE.md` bloc 6')
        self.non('renvoi-mort', '`mix_film.py`')


class Workflow(unittest.TestCase):
    def test_agent_type(self):
        js = ("const opts = (s, extra) => Object.assign({}, t ? { agentType: t } : {}, extra)\n"
              "agent(p, opts(s, { label: 'a' }))\n"
              "agent(p, { label: 'b', agentType: 'x' })\n"
              "agent(p, { label: 'c' })\n"
              "x.agent(p)\n")
        trouves = v.appels_sans_type(js)
        self.assertEqual([n for n, _ in trouves], [4])


class PluginFactice(unittest.TestCase):
    def setUp(self):
        self.dossier = tempfile.mkdtemp()
        self.ancien = (v.PLUGIN, v.BASE, v.SEUILS)
        v.PLUGIN = self.dossier
        v.BASE = os.path.join(self.dossier, 'outils', 'coherence_base.json')
        v.SEUILS = os.path.join(self.dossier, 'referentiels', 'seuils.json')
        self.ecrire('REGLES_STUDIO.md', "# Règles\nIntro.\n\n## Priorité\nLe plus précis l'emporte.\n\n## Suite\nLes écarts l'emportent.\n")
        self.ecrire('referentiels/seuils.json', json.dumps({'injection': {'regles_studio_caracteres_max': 8000},
                                                            'mix': {'film': {'lufs': -14}}}))
        self.ecrire('referentiels/REGLES_DETAIL.md', '# Détail\n\n## Qui décide\n| Ligne | Choix | Propose | Décide | Porte |\n|---|---|---|---|---|\n'
                    '| D01 | sujet | strategist | — | sujet |\n| D02 | style | — | art-director et producteur | socle |\n\n## Suite\n')
        self.ecrire('agents/strategist.md', '---\nname: strategist\ntools: Read, Write\n---\nTu proposes : D01.\n')
        self.ecrire('agents/art-director.md', '---\nname: art-director\ntools: Read, Bash\n---\nTu décides le style.\n')
        self.ecrire('hooks/garde_commandes.py', "ROLES = {'strategist': 'stratege'}\n")
        self.ecrire('domaines/sport/DOMAINE.md', '# Sport\n')
        self.ecrire('skills/s/w.js', "agent(p, { label: 'c' })\n")
        os.makedirs(os.path.join(self.dossier, 'outils'))
        self.ecrire('skills/s/SKILL.md', "Voir `references/absent.md` et `referentiels/REGLES_DETAIL.md`.\n```\nl'emporte dans du code\n```\n")

    def tearDown(self):
        v.PLUGIN, v.BASE, v.SEUILS = self.ancien
        shutil.rmtree(self.dossier)

    def ecrire(self, r, texte):
        p = os.path.join(self.dossier, r)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(texte)

    def test_occurrences(self):
        occ = v.occurrences()
        vus = Counter((o[0], o[1]) for o in occ)
        self.assertEqual(vus[('preseance', 'REGLES_STUDIO.md')], 1)          # § Priorité permis, § Suite refusé
        self.assertEqual(vus[('renvoi-mort', 'skills/s/SKILL.md')], 1)       # references/absent.md ; REGLES_DETAIL existe
        self.assertEqual(vus[('preseance', 'skills/s/SKILL.md')], 0)         # bloc de code ignoré
        self.assertEqual(vus[('agent-sans-type', 'skills/s/w.js')], 1)
        self.assertEqual(vus[('agent-sans-role', 'agents/art-director.md')], 1)
        self.assertEqual(vus[('agent-sans-role', 'agents/strategist.md')], 0)
        textes = [o[4] for o in occ if o[0] == 'qui-decide']
        self.assertTrue(any('deux décideurs' in t for t in textes))
        self.assertTrue(any('D02 non déclarée' in t for t in textes))       # art-director ne cite pas D02
        self.assertFalse(any('D01 non déclarée' in t for t in textes))      # strategist cite D01
        self.assertEqual(vus[('taille', 'REGLES_STUDIO.md')], 0)

    def test_taille(self):
        self.ecrire('referentiels/seuils.json', json.dumps({'injection': {'regles_studio_caracteres_max': 100}}))
        self.assertTrue(any(o[0] == 'taille' for o in v.occurrences()))

    def test_qui_decide_absent(self):
        self.ecrire('referentiels/REGLES_DETAIL.md', '# Détail\n')
        self.assertTrue(any(o[0] == 'qui-decide' and 'manque' in o[4] for o in v.occurrences()))

    def test_base_ne_fait_que_decroitre(self):
        actuel = Counter(v.cle(o) for o in v.occurrences())
        v.ecrire_base(actuel)
        self.assertEqual(v.charger_base(), actuel)
        self.ecrire('REGLES_STUDIO.md', "# Règles\n\n## Priorité\nLe plus précis l'emporte.\n\n## Suite\nRien.\n")  # une corrigée
        apres = Counter(v.cle(o) for o in v.occurrences())
        self.assertEqual(sum((v.charger_base() - apres).values()), 1)       # disparue : à retirer
        self.assertEqual(sum((apres - v.charger_base()).values()), 0)
        self.ecrire('REGLES_STUDIO.md', "# Règles\n\n## Priorité\nok\n\n## Suite\nLes écarts l'emportent, encore.\n")  # réécrite
        apres = Counter(v.cle(o) for o in v.occurrences())
        self.assertEqual(sum((apres - v.charger_base()).values()), 1)       # ligne réécrite : contrôlée strictement

    def test_cles_seuils(self):
        self.assertIn('mix.film.lufs', v.cles(v.seuils()))


if __name__ == '__main__':
    unittest.main(verbosity=1)
