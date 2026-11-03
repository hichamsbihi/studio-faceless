"""Test des ajouts au garde-fou (hooks/garde_commandes.py). 0.6.0 (02/11/2026) : rôle `telechargeur` (agent `media-fetcher`) et
interdiction faite au rôle `stratege` de lancer `youtube_retention.py` (réservé à Claude principal). 0.7.0 (03/11/2026) : rôles
`ingenieur-son` (agent `sound-manager`) et `editeur` (agent `publisher`), éprouvés avec des arguments bizarres (espaces, chemins sans
barre oblique, --option=valeur, options abrégées, sorties au milieu d'une commande ffmpeg, redirections, substitutions) ; un script
écrit par l'agent dans sa zone lui est refusé, sous toutes ses formes d'appel (relu et lancé par Claude principal).

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


class Roles07(Base):
    """Outils du plugin, fichiers existants de la chaîne simulée, et deux listes : commandes permises, commandes refusées."""
    EP = 'episodes/episode-011'

    def setUp(self):
        super().setUp()
        for rel in ('marque/son/musique/theme.mp3', f'{self.EP}/inputs/voix/E011_S1_voix_v1.mp3', f'{self.EP}/SCRIPT_ELEVENLABS_v1.txt',
                    f'{self.EP}/outputs/E011-master-v3-voix.voix.wav', f'{self.EP}/outputs/E011-master-v3.mix.wav',
                    f'{self.EP}/montage/mesures-v3/mesurer_cues.py', f'{self.EP}/kit/media/audio/sfx/maillet-re.wav',
                    f'{self.EP}/kit/media/photos-v1/jayz.jpg', f'{self.EP}/miniatures-v3/travail/masque.py',
                    f'{self.EP}/miniatures-v3/AA-E011-miniature-v3-1.png', 'modeles/ggml-base.en.bin'):
            chemin = os.path.join(self.racine, *rel.split('/'))
            os.makedirs(os.path.dirname(chemin), exist_ok=True)
            open(chemin, 'w').close()

    def py(self, outil, *plus):
        return f'python -I -B "{self.plugin}/{outil}" {" ".join(plus)}'

    def verifier(self, role, permises, refusees):
        for commande in permises:
            with self.subTest(permise=commande[-90:]):
                self.assertIsNone(self.bash(commande, role))
        for commande in refusees:
            with self.subTest(refusee=commande[-90:]):
                verdict = self.bash(commande, role)
                self.assertIsNotNone(verdict)
                self.assertEqual(verdict[0], 'deny')

    def ecrire(self, role, rel):
        return garde.decide_write(os.path.join(self.racine, *rel.split('/')), role, self.racine)

    def test_roles_reconnus(self):
        self.assertEqual(garde.role_of({'agent_type': 'studio-faceless:sound-manager'}), 'ingenieur-son')
        self.assertEqual(garde.role_of({'agent_type': 'studio-faceless:publisher'}), 'editeur')

    def test_ingenieur_son_bash(self):
        ep, gv = self.EP, 'outils/voix/generer_voix.py'
        avant = f'{gv}', f'{ep}/SCRIPT_ELEVENLABS_v1.txt', '--voix', 'AbC123xyz', '--sortie', f'{ep}/inputs/voix', '--nom', '"E011_S{n}_voix_v2.mp3"'
        permises = [
            self.py(*avant),
            self.py(*avant, '--prises', '2', '3', '--facteur=1.0'),
            self.py('outils/voix/info_elevenlabs.py', '--modeles', 'eleven_v4'),
            self.py('outils/controle/ralentir.py', f'{ep}/inputs/voix/E011_S1_voix_v1.mp3', f'{ep}/kit/voix/seq1-ralentie-v2.wav', '--tempo=0.97', '--cible', '-19'),
            self.py('outils/controle/transcrire.py', f'{ep}/inputs/voix/E011_S1_voix_v1.mp3', '--modele', '"C:/Mes Modeles/ggml-base.en.bin"',
                    '--sortie', f'"{ep}/kit/voix/transcription v2"', '--texte', f'{ep}/SCRIPT_ELEVENLABS_v1.txt'),
            self.py('outils/controle/recaler.py', f'{ep}/kit/voix/seq1.wav', f'{ep}/kit/voix/seq1.txt', 'modeles/ggml-base.en.bin', f'{ep}/kit/voix/reperes-v2', 'seq1'),
            self.py('outils/controle/mesurer_sons.py', 'marque/son/musique/theme.mp3', '--whisper', 'modeles/ggml-base.en.bin', '--boucle'),
            self.py('outils/controle/controle.py', 'voix-reste', f'{ep}/outputs/a.wav', f'{ep}/outputs/b.wav'),
            self.py('outils/medias/telecharger_medias.py', f'{ep}/kit/LISTE_SONS_v1.json', '--racine', f'{ep}/kit/media/source-v2/soundza',
                    '--agent-utilisateur', UA, '--executer'),
            f'ffmpeg -hide_banner -nostats -i {ep}/outputs/E011-master-v3.mix.wav -i {ep}/outputs/E011-master-v3-voix.voix.wav -filter_complex '
            f'"[0:a]volume=-2.4dB[m];[m][1:a]amerge=inputs=2,pan=stereo|c0=c0-c2|c1=c1-c3,ebur128=metadata=1,ametadata=mode=print:key=lavfi.r128.S:'
            f'file={ep}/outputs/controle-son-v3/residu-S.txt" -f null - 2>&1 | tail -n 5',
            f'ffmpeg -i marque/son/musique/theme.mp3 -af "atrim=0:3" {ep}/kit/media/audio/musique/theme-3s.wav',
            f'cp -n marque/son/musique/theme.mp3 {ep}/kit/media/audio/musique/',
            f'mkdir -p {ep}/outputs/controle-son-v3 && ls marque/son > {ep}/montage/liste-sons.txt',
            f'ffprobe -v error -show_entries format=duration {ep}/outputs/E011-master-v3.mix.wav', 'date', f'sha1sum {ep}/kit/media/audio/sfx/maillet-re.wav',
        ]
        refusees = [
            self.py(*avant, '--executer', '--confirme-credits', '120'),                       # appel payant : Claude principal
            self.py(*avant, '--exec'), self.py(*avant, '--confirme-credits=120'), self.py(*avant, '--conf', '120'), self.py(*avant, '--e'),
            self.py('outils/montage/mix_film.py', f'{ep}/outputs/a-voix.mp4', f'{ep}/montage/plan-son-v3.json', '--son-seul'),   # mix long
            self.py('outils/montage/assembler.py', '--episode', 'episode-011', '--voix-seule'),
            self.py('outils/controle/ralentir.py', 'a.mp3', 'marque/son/x.wav'),
            self.py('outils/controle/ralentir.py', 'a.mp3', '"marque/son x/y.wav"'),            # chemin avec une espace
            self.py('outils/controle/ralentir.py', 'a.mp3', 'marque'),                          # sans barre oblique
            self.py('outils/controle/ralentir.py', 'a.mp3', f'{ep}/kit/voix/b.wav', '--temp', '0.97'),   # option abrégée
            self.py('outils/controle/transcrire.py', 'a.mp3', '--modele', 'm.bin', '--sortie=direction'),  # --option=valeur
            self.py('outils/controle/transcrire.py', 'a.mp3', '--modele', 'm.bin', '--sort', f'{ep}/kit/voix/t'),
            self.py('outils/controle/ralentir.py', 'a.mp3', f'{ep}/inputs/voix/b.wav'),         # entrées de l'épisode
            self.py('outils/controle/ralentir.py', 'a.mp3', f'{ep}/montage/montage.json'),
            self.py('outils/controle/controle.py', 'planche', 'a.mp4', '--sortie', f'{ep}/outputs/controle-son-v3'),
            self.py('outils/medias/telecharger_medias.py', 'l.json', '--racine', f'{ep}/kit/media/source-v2', '--agent-utilisateur', UA),
            self.py('outils/recherche/youtube_retention.py', '@chaine', 'docs/r.json'),
            self.py('skills/thumbnail-strategist/scripts/miniature.py', 'rendu', 'a.html', f'{ep}/montage/x.png'),
            f'python -I -B "{self.plugin}/../autre/outils/controle/ralentir.py" a.mp3 {ep}/kit/voix/b.wav',
            'python -c "print(1)"', f'python -I -B outils/controle/ralentir.py a.mp3 {ep}/kit/voix/b.wav',
            f'python -I -B {ep}/montage/mesures-v3/mesurer_cues.py {ep}/outputs/E011-master-v3.mix.wav -2.4 {ep}/outputs/controle-son-v3/cues.json',
            f'python -I -B {ep}/montage/mesures-v3/mesurer_cues.py {ep}/outputs/E011-master-v3.mix.wav marque/son/sortie.json',
            f'python -I -B {ep}/montage/mesures-v3/mesurer_cues.py --sortie=marque/son/sortie.json',
            f'python -I -B {ep}/montage/mesures-v3/absent.py', f'python -I -B {ep}/kit/media/audio/x.py',
            f'ffmpeg -y -i a.wav {ep}/kit/media/audio/b.wav', 'ffmpeg -i a.wav marque/son/b.wav',
            'ffmpeg -i a.wav -vn "marque/son x/b.wav"', f'ffmpeg -i a.wav -f wav marque/b.wav -f null -',
            f'ffmpeg -i a.wav -af "ametadata=mode=print:file=direction/x.txt" -f null -',
            f'ffmpeg -i a.wav -c:a pcm_s16le {ep}/outputs/E011-master-v4.mp4',
            f'ffmpeg -i a.wav {ep}/kit/media/audio/sfx/maillet-re.wav',                       # écrasement
            'cp marque/son/musique/theme.mp3 marque/son/musique/theme2.mp3', f'cp -r marque/son {ep}/kit/media/audio/',
            f'cp {ep}/kit/media/audio/sfx/maillet-re.wav {ep}/kit/media/audio/sfx/',        # écrasement
            f'ls marque > direction/x.txt', f'ffprobe a.wav 2> marque/journal.txt', f'ls & cp a.wav marque/x.wav',
            f'ls $(cp a.wav marque/x.wav)', 'cd marque/son && ls', 'curl -o x.mp3 https://exemple.org/x.mp3',
            'node node_modules/hyperframes/bin/hyperframes.mjs remove-background a.jpg -o b.png',
            'rm x.wav', 'mv a.wav b.wav', 'sed -i s/a/b/ x.json',
        ]
        self.verifier('ingenieur-son', permises, refusees)

    def test_ingenieur_son_write(self):
        ep = self.EP
        for rel in (f'{ep}/montage/plan-son-v3.json', f'{ep}/montage/CUES_v3.md', f'{ep}/kit/voix/README.md', f'{ep}/kit/PROVENANCE.md',
                    f'{ep}/kit/media/source-v2/soundza/LISTE.md', f'{ep}/outputs/controle-son-v3/mesures.md', f'{ep}/montage/mesures-v3/m.py'):
            with self.subTest(permis=rel):
                self.assertIsNone(self.ecrire('ingenieur-son', rel))
        for rel in (f'{ep}/montage/montage.json', 'marque/son/README.md', f'{ep}/inputs/voix/x.txt', f'{ep}/production/seq1-v3/README.md',
                    'direction/ECARTS.md', f'{ep}/outputs/film.mp4', f'{ep}/outputs/notes.md', f'{ep}/BRIEF.md', f'{ep}/CLAUDE.md',
                    f'{ep}/kit/media/source-v2/photo.jpg', f'{ep}/kit/media/audio/sfx/maillet-re.wav', '../hors/chaine.txt'):
            with self.subTest(refuse=rel):
                self.assertEqual(self.ecrire('ingenieur-son', rel)[0], 'deny')

    def test_editeur_bash(self):
        ep, mn = self.EP, 'skills/thumbnail-strategist/scripts/miniature.py'
        rb = 'node node_modules/hyperframes/bin/hyperframes.mjs remove-background'
        permises = [
            self.py(mn, 'rendu', f'{ep}/miniatures-v3/miniature-1-who-pays.html', f'{ep}/miniatures-v3/AA-E011-miniature-v3-2-who-pays.png'),
            self.py(mn, 'planche', f'"{ep}/miniatures-v3/planche controle.png"', f'{ep}/miniatures-v3/a.png', f'{ep}/miniatures-v3/b.png'),
            self.py(mn, 'grille', f'{ep}/kit/media/photos-v1/jayz.jpg', f'{ep}/miniatures-v3/travail/grille.png', '--echelle', '0.6', '--zone=10,10,200,200'),
            self.py(mn, 'contraste', '"#2FD27A"', '--image', f'{ep}/miniatures-v3/AA-E011-miniature-v3-1.png', '--zone', '40,60,500,120'),
            self.py('outils/controle/controle.py', 'chrome'),
            self.py('outils/controle/publication.py', 'verifier', f'{ep}/PUBLICATION_v2.md', '--journal', f'{ep}/outputs/a-voix.log.txt'),
            self.py('outils/montage/srt.py', '--script', f'{ep}/SCRIPT_v1.md', '--mots', '"kit/voix/{seq}-montage-mots-recales.json"',
                    '--journal', f'{ep}/outputs/a-voix.log.txt', '--sortie', f'{ep}/PUBLICATION_v2.en.srt'),
            f'{rb} {ep}/miniatures-v3/media/jayz-recadre.jpg -o {ep}/miniatures-v3/media/jayz_brut.png --device cpu',
            f'{rb} {ep}/miniatures-v3/media/jayz-recadre.jpg --output={ep}/miniatures-v3/media/jayz_brut2.png --device cpu', f'{rb} --info',
            f'ffmpeg -i {ep}/kit/media/photos-v1/jayz.jpg -vf "crop=900:1000:300:0" {ep}/miniatures-v3/media/jayz-recadre.jpg',
            f'cp -n {ep}/kit/media/photos-v1/jayz.jpg {ep}/miniatures-v3/media/', 'ls ~/.cache/hyperframes/background-removal/models',
        ]
        refusees = [
            self.py(mn, 'rendu', 'a.html', 'marque/x.png'), self.py(mn, 'rendu', 'a.html', '"marque/logo x/y.png"'),
            self.py(mn, 'rendu', 'a.html', 'marque'), self.py(mn, 'rendu', 'a.html', f'{ep}/miniatures-v3/AA-E011-miniature-v3-1.png'),
            self.py(mn, 'planche', 'docs/planche.png', 'a.png'), self.py(mn, 'grille', 'p.jpg', f'{ep}/miniatures-v3/g.png', '--pol', 'x.html'),
            self.py(mn, 'rendu', 'a.html', f'{ep}/kit/media/photos-v1/y.png'),
            self.py('outils/montage/srt.py', '--script', 's.md', '--mots', 'm', '--journal', 'j', '--sortie', f'{ep}/SCRIPT.srt'),
            self.py('outils/montage/srt.py', '--script', 's.md', '--mots', 'm', '--journal', 'j', '--sort', f'{ep}/PUBLICATION_v2.en.srt'),
            self.py('outils/controle/controle.py', 'planche', 'a.mp4', '--sortie', f'{ep}/miniatures-v3/p'),
            self.py('outils/voix/generer_voix.py', 's.txt', '--voix', 'x', '--sortie', 'd', '--nom', 'n{n}.mp3'),
            self.py('outils/recherche/youtube_retention.py', '@chaine', 'docs/r.json'),
            self.py('outils/medias/telecharger_medias.py', 'l.json', '--racine', f'{ep}/miniatures-v3/media', '--agent-utilisateur', UA),
            f'{rb} a.jpg -o marque/x.png', f'{rb} a.jpg --output=direction/x.png', f'{rb} a.jpg --out {ep}/miniatures-v3/b.png',
            f'{rb} a.jpg -o{ep}/miniatures-v3/b.png', 'node autre.js', 'node node_modules/hyperframes/bin/hyperframes.mjs render --workers 1',
            'npx hyperframes remove-background a.jpg -o b.png',
            f'python -I -B {ep}/miniatures-v3/travail/masque.py {ep}/miniatures-v3/media/jayz_brut.png {ep}/miniatures-v3/media/jayz.png 2',
            f'python -I -B {ep}/miniatures-v3/travail/masque.py a.png {ep}/kit/media/photos-v1/z.png',
            f'ffmpeg -i a.jpg {ep}/kit/media/photos-v1/b.jpg', f'ffmpeg -i a.jpg {ep}/miniatures-v3/AA-E011-miniature-v3-1.png',
            f'cp a.png {ep}/JOURNAL_MINIATURES.md', f'ls > {ep}/PUBLICATION_v2.txt', 'python -c "import PIL"',
        ]
        self.verifier('editeur', permises, refusees)

    def test_script_de_la_zone_refuse(self):
        """03/11/2026 : le garde ne lit pas un script ; celui de l'agent est relu et lancé par Claude principal, jamais par l'agent."""
        ep = self.EP
        for role, rel in (('ingenieur-son', f'{ep}/montage/mesures-v3/mesurer_cues.py'), ('editeur', f'{ep}/miniatures-v3/travail/masque.py')):
            absolu = os.path.join(self.racine, *rel.split('/')).replace('\\', '/')
            for commande in (f'python {rel}', f'python -I -B {rel} 2 {ep}/outputs/controle-son-v3/x.json', f'python3 {rel}', f'py -3 {rel}',
                             f'python "{rel}"', f'python -I -B "{absolu}"', f'python ./{rel}', f'python.exe {rel} -2.4'):
                with self.subTest(role=role, commande=commande[-90:]):
                    verdict = self.bash(commande, role)
                    self.assertIsNotNone(verdict)
                    self.assertEqual(verdict[0], 'deny')
                    self.assertIn('relu et lancé par Claude principal', verdict[1])

    def test_editeur_write(self):
        ep = self.EP
        for rel in (f'{ep}/miniatures-v3/miniature-1-who-pays.html', f'{ep}/miniatures-v3/PROVENANCE.md', f'{ep}/PUBLICATION_v2.md',
                    f'{ep}/PUBLICATION_v2.en.srt', f'{ep}/miniatures-v4/CONCEPTS.md'):
            with self.subTest(permis=rel):
                self.assertIsNone(self.ecrire('editeur', rel))
        for rel in (f'{ep}/JOURNAL_MINIATURES.md', f'{ep}/BRIEF.md', f'{ep}/PUBLICATION_v2.txt', 'marque/logo/x.png', 'direction/BANQUE_SUJETS.md',
                    f'{ep}/miniatures-v3/AA-E011-miniature-v3-1.png', f'{ep}/kit/PROVENANCE.md', f'{ep}/montage/plan-son-v3.json', '../hors.txt'):
            with self.subTest(refuse=rel):
                self.assertEqual(self.ecrire('editeur', rel)[0], 'deny')


if __name__ == '__main__':
    unittest.main()
