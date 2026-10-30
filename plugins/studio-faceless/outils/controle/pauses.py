"""Pauses ajoutées à une narration, voix intacte.

Validé sur MM (Maps & Means), 21/10/2026 (méthode du pilote, voix v4 de l'épisode 001 ; règle générale du studio :
« on clone les décisions de cet épisode pour les pauses »). Versé au plugin le 30/10/2026.

On ajoute du silence numérique au milieu de silences déjà présents dans la bande (contrôlés sous −60 dBFS), puis on
décale les repères mot à mot (`seqN-mots.json`) et par phrase (`seqN-phrases.txt`). Aucun mot n'est coupé ni retouché.
Réglages par défaut et choix des instants : `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 2 ; les valeurs de
la voix de la chaîne sont dans sa `direction/ECARTS.md`.

Fichier de pauses (JSON), une liste par séquence ; chaque pause est [instant dans la bande source en s, silence ajouté
en s], ou ["fin", s] pour une queue :
  {"1": [[0.30, 1.8], [9.53, 0.3], ["fin", 2.0]], "2": [[0.36, 0.5], ["fin", 0.6]]}

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/pauses.py SOURCE SORTIE PAUSES.json N [N...]
SOURCE contient seqN-voix.wav et reperes/seqN-mots.json, reperes/seqN-phrases.txt (sortie de ralentir.py, puis des
repères). Écrit SORTIE/seqN-voix.wav et SORTIE/reperes/. Refuse d'écraser ; le dossier SORTIE doit déjà exister.
"""
import json, os, shutil, subprocess, sys
import numpy as np

FF = os.environ.get('HYPERFRAMES_FFMPEG_PATH') or shutil.which('ffmpeg') or 'ffmpeg'
SR = 48000
SILENCE_MAX = 10 ** (-60 / 20)      # crête tolérée autour du point d'insertion


def lire(path):
    r = subprocess.run([FF, '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).copy()


def ecrire(x, path):
    subprocess.run([FF, '-v', 'error', '-n', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-i', '-', '-c:a', 'pcm_s24le', path],
                   input=x.astype(np.float32).tobytes(), check=True)


def sequence(source, sortie, pauses, n):
    src = os.path.join(source, f'seq{n}-voix.wav')
    out = os.path.join(sortie, f'seq{n}-voix.wav')
    rep = os.path.join(sortie, 'reperes')
    for p in (out, os.path.join(rep, f'seq{n}-mots.json'), os.path.join(rep, f'seq{n}-phrases.txt')):
        if os.path.exists(p):
            sys.exit(f'refus : {p} existe déjà')
    x = lire(src)
    mots = json.load(open(os.path.join(source, 'reperes', f'seq{n}-mots.json'), encoding='utf-8'))
    sil = mots['silences']
    points = []
    for t, d in pauses:
        if t == 'fin':
            points.append((len(x) / SR, d)); continue
        s = next(((a, b) for a, b in sil if a <= t <= b), None)    # le silence qui contient l'instant voulu
        if s is None:
            sys.exit(f'séquence {n} : aucun silence à {t} s')
        m = (s[0] + s[1]) / 2
        i0, i1 = int((m - 0.05) * SR), int((m + 0.05) * SR)
        crete = float(np.abs(x[max(0, i0):i1]).max()) if i1 > i0 else 0.0
        if crete >= SILENCE_MAX:
            sys.exit(f'séquence {n} : pas de vrai silence à {t} s (crête {crete:.2e})')
        points.append((m, d))
    points.sort()
    morceaux, dernier = [], 0
    for t, d in points:
        i = min(len(x), int(round(t * SR)))
        morceaux += [x[dernier:i], np.zeros(int(round(d * SR)), np.float32)]; dernier = i
    morceaux.append(x[dernier:])
    y = np.concatenate(morceaux)

    def decale(t):
        return round(t + sum(d for p, d in points if p <= t + 1e-9 and p < len(x) / SR), 3)

    os.makedirs(rep, exist_ok=True)
    ecrire(y, out)
    m2 = dict(mots)
    m2['source'] = f'Bande {src} + pauses (studio-faceless, outils/controle/pauses.py) ; repères décalés. ' + mots.get('source', '')
    m2['bande'] = f'seq{n}-voix.wav'; m2['duree'] = round(len(y) / SR, 3)
    m2['pauses_ajoutees'] = [[round(t, 3), d] for t, d in points]
    m2['silences'] = [[decale(a), decale(b) if b < len(x) / SR - 1e-6 else round(len(y) / SR, 3)] for a, b in sil]
    m2['mots'] = [dict(w, start=decale(w['start']), end=decale(w['end'])) for w in mots['mots']]
    json.dump(m2, open(os.path.join(rep, f'seq{n}-mots.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    lignes = open(os.path.join(source, 'reperes', f'seq{n}-phrases.txt'), encoding='utf-8').read().splitlines()
    res = [lignes[0] + f' ; avec pauses : {len(y) / SR:.2f} s']
    for l in lignes[1:]:
        if '–' in l and l.strip():
            a, reste = l.split('–', 1); b, texte = reste.strip().split(' ', 1)
            res.append(f'{decale(float(a)):7.2f} – {decale(float(b)):7.2f}  {texte.strip()}')
        else:
            res.append(l)
    open(os.path.join(rep, f'seq{n}-phrases.txt'), 'w', encoding='utf-8').write('\n'.join(res) + '\n')
    print(f'séquence {n} : {len(x) / SR:.2f} s -> {len(y) / SR:.2f} s ; {len(points)} pauses (+{sum(d for _, d in points):.2f} s)')


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if '-h' in sys.argv[1:] or '--help' in sys.argv[1:]:
        print(__doc__); return
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    source, sortie, fichier = sys.argv[1:4]
    if not os.path.isdir(sortie):
        sys.exit(f'refus : le dossier {sortie} n\'existe pas (le créer d\'abord, après vérification)')
    toutes = json.load(open(fichier, encoding='utf-8'))
    for n in sys.argv[4:]:
        sequence(source, sortie, [tuple(p) for p in toutes[str(n)]], int(n))


if __name__ == '__main__':
    main()
