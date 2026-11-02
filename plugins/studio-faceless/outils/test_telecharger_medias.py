"""Test hors réseau de medias/telecharger_medias.py (0.6.0, 02/11/2026) : lecture de la liste, nommage, refus d'écraser, refus sans détour.

Usage, depuis la racine du dépôt du plugin :
  python -I -B plugins/studio-faceless/outils/test_telecharger_medias.py
Aucun appel réseau : le téléchargement passe par un faux `urlopen`. Code de sortie : 0 = tests passés ; 1 = échec. Bibliothèque standard seule.
"""
import argparse, hashlib, importlib.util, io, json, os, tempfile, unittest, urllib.error

_spec = importlib.util.spec_from_file_location('telecharger_medias', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'medias', 'telecharger_medias.py'))
tm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tm)

UA = 'ChaineEssai-MediaFetch/1.0 (https://exemple.org/chaine)'


class Reponse:
    def __init__(self, data=b'', ctype='image/jpeg'):
        self._d = io.BytesIO(data)
        self.headers = {'Content-Type': ctype, 'Content-Length': str(len(data))}

    def read(self, n=-1):
        return self._d.read(n)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def erreur(url, code, entetes=None):
    return urllib.error.HTTPError(url, code, 'erreur', entetes or {}, None)


class Faux:
    """Faux urlopen : `scenario` associe un fragment d'adresse à une liste de réponses (objet ou exception) consommées dans l'ordre."""

    def __init__(self, scenario):
        self.scenario, self.appels = scenario, []

    def __call__(self, req, timeout=None):
        url = req.full_url
        self.appels.append((req.get_method(), url, req.get_header('User-agent')))
        for fragment, reponses in self.scenario.items():
            if fragment in url:
                r = reponses.pop(0) if len(reponses) > 1 else reponses[0]
                if isinstance(r, Exception):
                    raise r
                return r
        raise AssertionError('appel inattendu : ' + url)


def ecrire_liste(dossier, medias):
    chemin = os.path.join(dossier, 'liste.json')
    with open(chemin, 'w', encoding='utf-8') as f:
        json.dump({'medias': medias}, f)
    return chemin


def args(liste, racine, **kw):
    base = dict(liste=liste, racine=racine, agent_utilisateur=UA, executer=True, pause=3.5, essais=3, manifeste=None)
    base.update(kw)
    return argparse.Namespace(**base)


class Liste(unittest.TestCase):
    def charger(self, medias):
        with tempfile.TemporaryDirectory() as d:
            return tm.charger_liste(ecrire_liste(d, medias))

    def test_liste_valide(self):
        m = self.charger([
            {'ref': 'M1', 'type': 'commons', 'titre': 'Super Bowl LIX (54361965533).jpg', 'dossier': 'photos'},
            {'ref': 'L2a', 'type': 'commons', 'pageid': 33781934, 'dossier': 'photos'},
            {'ref': 'P1b', 'type': 'direct', 'url': 'https://exemple.org/a/b%20c.jpg', 'dossier': 'photos'},
            {'ref': 'V6b', 'type': 'pexels', 'titre': '13367034', 'dossier': 'videos', 'fps': 60},
            {'ref': 'V7a', 'type': 'pexels', 'url': 'https://www.pexels.com/video/handheld-shot-of-spotlights-8515272/', 'dossier': 'videos'},
        ])
        self.assertEqual([x['ref'] for x in m], ['M1', 'L2a', 'P1b', 'V6b', 'V7a'])
        self.assertEqual(m[0]['titre'], 'Super_Bowl_LIX_(54361965533).jpg')
        self.assertEqual(m[0]['api'], 'commons.wikimedia.org')
        self.assertEqual(m[3]['fps'], [60])
        self.assertEqual(m[4]['id'], 8515272)
        self.assertEqual(m[4]['fps'], tm.FPS_DEFAUT)

    def test_commons_par_adresse(self):
        m = self.charger([{'ref': 'G1', 'type': 'commons', 'url': 'https://en.wikipedia.org/wiki/File:Logo_test.svg', 'dossier': 'logos'}])
        self.assertEqual((m[0]['titre'], m[0]['api']), ('Logo_test.svg', 'en.wikipedia.org'))

    def test_listes_refusees(self):
        mauvaises = [
            [],
            [{'ref': 'M 1', 'type': 'direct', 'url': 'https://exemple.org/a.jpg', 'dossier': 'photos'}],
            [{'ref': 'M1', 'type': 'inconnu', 'dossier': 'photos'}],
            [{'ref': 'M1', 'type': 'direct', 'url': 'https://exemple.org/a.jpg', 'dossier': 'photos'}] * 2,
            [{'ref': 'M1', 'type': 'direct', 'url': 'https://exemple.org/a.jpg', 'dossier': '../dehors'}],
            [{'ref': 'M1', 'type': 'direct', 'url': 'https://exemple.org/a.jpg', 'dossier': '/absolu'}],
            [{'ref': 'M1', 'type': 'direct', 'url': 'http://exemple.org/a.jpg', 'dossier': 'photos'}],
            [{'ref': 'M1', 'type': 'direct', 'url': 'https://www.pexels.com/video/x-1234567/', 'dossier': 'videos'}],
            [{'ref': 'M1', 'type': 'commons', 'titre': 'A.jpg', 'api': 'exemple.org', 'dossier': 'photos'}],
            [{'ref': 'V1', 'type': 'pexels', 'url': 'https://videos.pexels.com/autre/chose.mp4', 'dossier': 'videos'}],
        ]
        for medias in mauvaises:
            with self.subTest(medias=str(medias)[:60]):
                with self.assertRaises(ValueError):
                    self.charger(medias)

    def test_agent_utilisateur(self):
        self.assertEqual(tm.agent_valide(UA), UA)
        self.assertEqual(tm.agent_valide('Robot/1.0 (https://www.youtube.com/@unechaine)'), 'Robot/1.0 (https://www.youtube.com/@unechaine)')
        for mauvais in ('Robot/1.0', 'Robot/1.0 (contact: nom.prenom@exemple.com)', 'Robot (https://exemple.org) mailto:a@b.fr', ''):
            with self.subTest(ua=mauvais):
                with self.assertRaises(ValueError):
                    tm.agent_valide(mauvais)


class Nommage(unittest.TestCase):
    def test_noms(self):
        m = {'ref': 'M1', 'dossier': 'photos'}
        self.assertEqual(tm.nom_final(m, 'Super_Bowl_LIX_(54361965533).jpg'), 'M1__Super_Bowl_LIX_(54361965533).jpg')
        self.assertEqual(tm.nom_final(m, 'Un titre: "avec" ?des* <interdits>.jpg'), 'M1__Un_titre___avec___des___interdits_.jpg')
        self.assertEqual(tm.nom_final({**m, 'nom': 'nom-impose.png'}, 'autre.jpg'), 'M1__nom-impose.png')
        self.assertEqual(tm.nom_final(m, '../../dehors.jpg'), 'M1__dehors.jpg')
        self.assertTrue(len(tm.nom_final(m, 'a' * 300 + '.jpg')) <= 120 + len('M1__'))
        self.assertTrue(tm.nom_final(m, 'a' * 300 + '.jpg').endswith('.jpg'))

    def test_nom_distant(self):
        self.assertEqual(tm.nom_distant_direct('https://exemple.org/dir/b%20c.jpg?x=1'), 'b c.jpg')

    def test_dossier_de_depot(self):
        with tempfile.TemporaryDirectory() as d:
            dest = tm.chemin_dest(d, {'ref': 'P1', 'dossier': 'photos'}, 'x.jpg')
            self.assertEqual(os.path.relpath(dest, d).replace('\\', '/'), 'photos/P1__x.jpg')

    def test_pexels_serveur_de_fichiers(self):
        self.assertEqual(tm.url_pexels(13367034, 60), 'https://videos.pexels.com/video-files/13367034/13367034-hd_1920_1080_60fps.mp4')
        self.assertEqual(tm.url_pexels(6976212, 24, 1080, 1920), 'https://videos.pexels.com/video-files/6976212/6976212-hd_1080_1920_24fps.mp4')


class Telechargement(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.racine = os.path.join(self.tmp.name, 'kit', 'media', 'source-v1')
        self.pauses = []

    def tearDown(self):
        self.tmp.cleanup()

    def client(self, faux):
        return tm.Client(UA, pause=3.5, ouvrir=faux, dormir=self.pauses.append)

    def test_refus_d_ecraser(self):
        m = {'ref': 'P1', 'type': 'direct', 'url': 'https://exemple.org/a.jpg', 'dossier': 'photos', 'nom': None, 'sha1': None}
        dest = tm.chemin_dest(self.racine, m, 'a.jpg')
        tm.ecrire_sans_ecraser(dest, b'ORIGINAL')
        with self.assertRaises(FileExistsError):
            tm.ecrire_sans_ecraser(dest, b'AUTRE')
        faux = Faux({'exemple.org': [Reponse(b'AUTRE')]})
        ligne = tm.traiter(self.client(faux), self.racine, m)
        self.assertEqual(ligne['statut'], 'deja_present')
        self.assertEqual(faux.appels, [])                                    # rien n'est même demandé au site
        with open(dest, 'rb') as f:
            self.assertEqual(f.read(), b'ORIGINAL')
        self.assertEqual(ligne['sha1'], hashlib.sha1(b'ORIGINAL').hexdigest())

    def test_telechargement_et_agent(self):
        m = {'ref': 'P1', 'type': 'direct', 'url': 'https://exemple.org/a.jpg', 'dossier': 'photos', 'nom': None, 'sha1': None}
        faux = Faux({'exemple.org': [Reponse(b'IMAGE')]})
        ligne = tm.traiter(self.client(faux), self.racine, m)
        self.assertEqual((ligne['statut'], ligne['octets']), ('ok', 5))
        self.assertEqual(ligne['sha1'], hashlib.sha1(b'IMAGE').hexdigest())
        self.assertEqual(faux.appels[0][2], UA)                              # le robot est identifié
        self.assertEqual(self.pauses, [3.5])                                 # une pause avant le fichier

    def test_429_double_l_attente(self):
        m = {'ref': 'P1', 'type': 'direct', 'url': 'https://exemple.org/a.jpg', 'dossier': 'photos', 'nom': None, 'sha1': None}
        faux = Faux({'exemple.org': [erreur('https://exemple.org/a.jpg', 429), Reponse(b'IMAGE')]})
        c = self.client(faux)
        ligne = tm.traiter(c, self.racine, m)
        self.assertEqual(ligne['statut'], 'ok')
        self.assertEqual(self.pauses, [3.5, 7.0])                            # pause avant le fichier, puis attente doublée
        self.assertEqual(c.pause, 7.0)                                       # et gardée pour les fichiers suivants

    def test_429_qui_persiste_va_au_proprietaire(self):
        m = {'ref': 'P1', 'type': 'direct', 'url': 'https://exemple.org/a.jpg', 'dossier': 'photos', 'nom': None, 'sha1': None}
        faux = Faux({'exemple.org': [erreur('https://exemple.org/a.jpg', 429)]})
        ligne = tm.traiter(self.client(faux), self.racine, m)
        self.assertEqual(ligne['statut'], 'refuse')
        self.assertEqual(len(faux.appels), 3)                                # trois essais, pas un de plus
        self.assertFalse(os.path.exists(os.path.join(self.racine, 'photos', 'P1__a.jpg')))

    def test_refus_sans_detour(self):
        m = {'ref': 'P1', 'type': 'direct', 'url': 'https://exemple.org/a.jpg', 'dossier': 'photos', 'nom': None, 'sha1': None}
        for code in (401, 403, 451):
            with self.subTest(code=code):
                faux = Faux({'exemple.org': [erreur('https://exemple.org/a.jpg', code)]})
                ligne = tm.traiter(self.client(faux), self.racine, m)
                self.assertEqual(ligne['statut'], 'refuse')
                self.assertEqual(len(faux.appels), 1)                        # aucun nouvel essai, aucune autre adresse
        faux = Faux({'exemple.org': [erreur('https://exemple.org/a.jpg', 503, {'cf-mitigated': 'challenge'})]})
        self.assertEqual(tm.traiter(self.client(faux), self.racine, m)['statut'], 'refuse')
        self.assertEqual(len(faux.appels), 1)

    def test_page_web_a_la_place_du_fichier(self):
        m = {'ref': 'P2', 'type': 'direct', 'url': 'https://exemple.org/b.jpg', 'dossier': 'photos', 'nom': None, 'sha1': None}
        faux = Faux({'exemple.org': [Reponse(b'<html>Just a moment...</html>', 'text/html; charset=utf-8')]})
        ligne = tm.traiter(self.client(faux), self.racine, m)
        self.assertEqual(ligne['statut'], 'refuse')
        self.assertFalse(os.path.exists(os.path.join(self.racine, 'photos', 'P2__b.jpg')))

    def test_pexels_jamais_la_page(self):
        m = tm.charger_liste(self._liste([{'ref': 'V6b', 'type': 'pexels', 'titre': '13367034', 'dossier': 'videos', 'fps': [24, 60]}]))[0]
        faux = Faux({'-hd_1920_1080_24fps': [erreur('x', 404)], '-hd_1920_1080_60fps': [Reponse(b'VIDEO', 'video/mp4')]})
        ligne = tm.traiter(self.client(faux), self.racine, m)
        self.assertEqual(ligne['statut'], 'ok')
        self.assertTrue(all(u.startswith('https://videos.pexels.com/video-files/13367034/') for _, u, _ in faux.appels))
        self.assertTrue(ligne['fichier'].endswith('V6b__13367034-hd_1920_1080_60fps.mp4'))

    def _liste(self, medias):
        os.makedirs(self.tmp.name, exist_ok=True)
        return ecrire_liste(self.tmp.name, medias)

    def test_commons_empreinte_de_l_api(self):
        contenu = b'PHOTO'
        sha = hashlib.sha1(contenu).hexdigest()
        reponse_api = json.dumps({'query': {'normalized': [{'from': 'File:A_b.jpg', 'to': 'File:A b.jpg'}], 'pages': [
            {'pageid': 1, 'title': 'File:A b.jpg', 'imageinfo': [{'url': 'https://upload.exemple.org/A_b.jpg', 'sha1': sha, 'width': 10, 'height': 5,
                                                                   'size': 5, 'mime': 'image/jpeg', 'descriptionurl': 'https://commons.wikimedia.org/wiki/File:A_b.jpg',
                                                                   'extmetadata': {'LicenseShortName': {'value': '<b>CC BY 2.0</b>'}}}]}]}}).encode()
        m = tm.charger_liste(self._liste([{'ref': 'M1', 'type': 'commons', 'titre': 'A b.jpg', 'dossier': 'photos'}]))
        faux = Faux({'commons.wikimedia.org': [Reponse(reponse_api, 'application/json')], 'upload.exemple.org': [Reponse(contenu)]})
        c = self.client(faux)
        infos = tm.interroger_commons(c, m)
        ligne = tm.traiter(c, self.racine, m[0], infos['M1'])
        self.assertEqual(ligne['statut'], 'ok')
        self.assertTrue(ligne['sha1_conforme_api'])
        self.assertEqual(ligne['meta']['LicenseShortName'], 'CC BY 2.0')
        self.assertTrue(ligne['fichier'].endswith('M1__A_b.jpg'))

    def test_commons_empreinte_differente(self):
        reponse_api = json.dumps({'query': {'pages': [{'pageid': 1, 'title': 'File:A.jpg', 'imageinfo': [
            {'url': 'https://upload.exemple.org/A.jpg', 'sha1': '0' * 40, 'extmetadata': {}}]}]}}).encode()
        m = tm.charger_liste(self._liste([{'ref': 'M1', 'type': 'commons', 'titre': 'A.jpg', 'dossier': 'photos'}]))
        faux = Faux({'commons.wikimedia.org': [Reponse(reponse_api, 'application/json')], 'upload.exemple.org': [Reponse(b'PHOTO')]})
        c = self.client(faux)
        ligne = tm.traiter(c, self.racine, m[0], tm.interroger_commons(c, m)['M1'])
        self.assertEqual(ligne['statut'], 'empreinte_differente')

    def test_apercu_sans_reseau(self):
        liste = self._liste([{'ref': 'P1', 'type': 'direct', 'url': 'https://exemple.org/a.jpg', 'dossier': 'photos'}])

        def interdit(*a, **k):
            raise AssertionError('appel réseau pendant l\'aperçu')
        self.assertEqual(tm.lancer(args(liste, self.racine, executer=False), ouvrir=interdit, dormir=interdit), 0)
        self.assertFalse(os.path.exists(self.racine))

    def test_lancer_manifeste_et_liste_du_proprietaire(self):
        liste = self._liste([{'ref': 'P1', 'type': 'direct', 'url': 'https://exemple.org/a.jpg', 'dossier': 'photos'},
                             {'ref': 'P2', 'type': 'direct', 'url': 'https://autre.example/b.jpg', 'dossier': 'photos'}])
        faux = Faux({'exemple.org': [Reponse(b'IMAGE')], 'autre.example': [erreur('https://autre.example/b.jpg', 403)]})
        code = tm.lancer(args(liste, self.racine, manifeste=os.path.join(self.racine, 'manifeste-1.json')), ouvrir=faux, dormir=self.pauses.append)
        self.assertEqual(code, 1)                                            # un refus : sortie 1
        with open(os.path.join(self.racine, 'manifeste-1.json'), encoding='utf-8') as f:
            lignes = {l['ref']: l for l in json.load(f)['medias']}
        self.assertEqual((lignes['P1']['statut'], lignes['P2']['statut']), ('ok', 'refuse'))
        self.assertEqual(lignes['P1']['sha1'], hashlib.sha1(b'IMAGE').hexdigest())
        manuel = [n for n in os.listdir(os.path.join(self.racine, 'manuel')) if n.startswith('A_TELECHARGER_PAR_LE_PROPRIETAIRE')]
        self.assertEqual(len(manuel), 1)
        with open(os.path.join(self.racine, 'manuel', manuel[0]), encoding='utf-8') as f:
            texte = f.read()
        self.assertIn('P2', texte)
        self.assertNotIn('| P1 |', texte)
        # second passage : P1 est déjà là (jamais écrasé), P2 est toujours refusé, un nouveau manifeste est écrit à côté
        faux2 = Faux({'autre.example': [erreur('https://autre.example/b.jpg', 403)]})
        tm.lancer(args(liste, self.racine, manifeste=os.path.join(self.racine, 'manifeste-2.json')), ouvrir=faux2, dormir=self.pauses.append)
        with open(os.path.join(self.racine, 'manifeste-2.json'), encoding='utf-8') as f:
            self.assertEqual({l['ref']: l['statut'] for l in json.load(f)['medias']}, {'P1': 'deja_present', 'P2': 'refuse'})
        # un manifeste existant n'est pas écrasé
        with self.assertRaises(ValueError):
            tm.lancer(args(liste, self.racine, manifeste=os.path.join(self.racine, 'manifeste-1.json')), ouvrir=faux2, dormir=self.pauses.append)

    def test_lien_signe_masque_au_manifeste(self):
        signe = 'https://stockage.exemple.org/sons/a.mp3?X-Amz-Credential=ABCD%2F2026&X-Amz-Date=20261102T163915Z&X-Amz-Signature=deadbeef1234'
        m = {'ref': 'S1', 'type': 'direct', 'url': signe, 'dossier': 'soundza', 'nom': 'soundza-a.mp3', 'sha1': None}
        faux = Faux({'stockage.exemple.org': [Reponse(b'SON', 'audio/mpeg')]})
        ligne = tm.traiter(self.client(faux), self.racine, m)
        self.assertEqual(ligne['statut'], 'ok')
        self.assertTrue(ligne['fichier'].endswith('S1__soundza-a.mp3'))
        brut = json.dumps(ligne)
        self.assertNotIn('deadbeef1234', brut)
        self.assertNotIn('ABCD', brut)
        self.assertIn('X-Amz-Date=20261102T163915Z', ligne['url'])

    def test_pause_minimale(self):
        self.assertEqual(tm.Client(UA, pause=0.5).pause, tm.PAUSE_MIN)


if __name__ == '__main__':
    unittest.main()
