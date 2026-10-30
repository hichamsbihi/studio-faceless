"""Pauses ramenées à une part de leur longueur, voix intacte.

Validé sur MM (Maps & Means), 26/10/2026 : « 60 %, plancher 0,25 s » (round reprise de S1, Q1, voix v3 de l'épisode 004).
Versé au plugin le 30/10/2026 ; les réglages de MM sont les valeurs par défaut de l'aide ci-dessous, à régler par chaîne
(les valeurs de la voix de la chaîne sont dans sa `direction/ECARTS.md`).

Pendant inverse de `pauses.py` : dans chaque silence de `seqN-mots.json` (silencedetect −50 dB, 0,25 s au moins)
compris entre le premier et le dernier mot, on retire du milieu ce qui dépasse max(PLANCHER, PART × longueur), avec un
fondu de 10 ms. Les silences gardés (fenêtres protégées) ne bougent pas. Les repères (`seqN-mots.json`,
`seqN-phrases.txt`) sont décalés d'autant ; `decalage.json` donne, par séquence, les coupes [instant de début dans la
bande source, durée retirée] pour recaler briefs, raccords et relevé musical.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/raccourcir.py SOURCE SORTIE [--sequences 1-7 | 1,3,5]
         [--part 0.6] [--plancher 0.25] [--gardes GARDES.json]
SOURCE contient seqN-voix.wav et reperes/seqN-mots.json, reperes/seqN-phrases.txt. SORTIE doit exister et être vide.
Fenêtres gardées (JSON, en s de la bande source ; un silence qui les touche ne bouge pas), exemple MM :
  {"2": [[50.60, 53.80]], "3": [[78.60, 82.70]]}
(MM : un vol de caméra de 3,2 s en séquence 2 ; le rappel « Like + Subscribe » en séquence 3.)
"""
import argparse, json, os, shutil, subprocess, sys
import numpy as np

FF = os.environ.get('HYPERFRAMES_FFMPEG_PATH') or shutil.which('ffmpeg') or 'ffmpeg'
SR, FONDU = 48000, 0.010
CRETE_MAX = 10 ** (-50 / 20)          # le passage retiré doit rester sous −50 dBFS


def lire(path):
    r = subprocess.run([FF, '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).copy()


def ecrire(x, path):
    subprocess.run([FF, '-v', 'error', '-n', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-i', '-', '-c:a', 'pcm_s24le', path],
                   input=x.astype(np.float32).tobytes(), check=True)


def sequence(n, source, sortie, part, plancher, gardes):
    x = lire(os.path.join(source, f'seq{n}-voix.wav'))
    mots = json.load(open(os.path.join(source, 'reperes', f'seq{n}-mots.json'), encoding='utf-8'))
    debut, fin = mots['mots'][0]['start'], mots['mots'][-1]['end']
    coupes = []                        # [début de la coupe, durée retirée], en s de la bande source
    for a, b in mots['silences']:
        if a < debut or b > fin:
            continue                   # ouverture et fin de séquence gardées
        if any(a < g1 and b > g0 for g0, g1 in gardes.get(str(n), [])):
            continue
        retire = (b - a) - max(plancher, part * (b - a))
        if retire < 0.02:
            continue
        m = (a + b) / 2
        i0, i1 = int(round((m - retire / 2) * SR)), int(round((m + retire / 2) * SR))
        crete = float(np.abs(x[i0 - int(FONDU * SR):i1 + int(FONDU * SR)]).max())
        if crete >= CRETE_MAX:
            sys.exit(f'séquence {n} : pas de vrai silence à {m:.2f} s (crête {20 * np.log10(crete):.1f} dBFS)')
        coupes.append((i0, i1))
    f = int(FONDU * SR); rampe = np.linspace(1, 0, f, dtype=np.float32)
    morceaux, dernier = [], 0
    for i0, i1 in coupes:
        a = x[dernier:i0].copy()
        b = x[i1 - f:i1] * (1 - rampe)
        a[-f:] = a[-f:] * rampe + b            # fondu enchaîné de 10 ms dans le silence ; retrait exact de i1 − i0
        morceaux.append(a); dernier = i1
    morceaux.append(x[dernier:])
    y = np.concatenate(morceaux)
    cs = [(i0 / SR, (i1 - i0) / SR) for i0, i1 in coupes]

    def decale(t):
        d = 0.0
        for c, r in cs:
            if t >= c + r - 1e-9:
                d += r
            elif t > c:
                d += t - c                     # instant pris dans une coupe : ramené à son début
        return round(t - d, 3)

    os.makedirs(os.path.join(sortie, 'reperes'), exist_ok=True)
    ecrire(y, os.path.join(sortie, f'seq{n}-voix.wav'))
    m2 = dict(mots)
    m2['source'] = (f'Bande {source}/seq{n}-voix.wav, pauses ramenées à {part:.0%} (plancher {plancher} s) par raccourcir.py '
                    '(studio-faceless) ; repères décalés. ' + mots.get('source', ''))
    m2['duree'] = round(len(y) / SR, 3)
    m2['coupes'] = [[round(c, 3), round(r, 3)] for c, r in cs]
    m2['silences'] = [[decale(a), decale(b)] for a, b in mots['silences']]
    m2['mots'] = [dict(w, start=decale(w['start']), end=decale(w['end'])) for w in mots['mots']]
    json.dump(m2, open(os.path.join(sortie, 'reperes', f'seq{n}-mots.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    lignes = open(os.path.join(source, 'reperes', f'seq{n}-phrases.txt'), encoding='utf-8').read().splitlines()
    res = [lignes[0] + f' ; pauses à {part:.0%} : {len(y) / SR:.2f} s']
    for l in lignes[1:]:
        if '–' in l and l.strip():
            a, reste = l.split('–', 1); b, texte = reste.strip().split(' ', 1)
            res.append(f'{decale(float(a)):7.2f} – {decale(float(b)):7.2f}  {texte.strip()}')
        else:
            res.append(l)
    open(os.path.join(sortie, 'reperes', f'seq{n}-phrases.txt'), 'w', encoding='utf-8').write('\n'.join(res) + '\n')
    print(f'séquence {n} : {len(x) / SR:.2f} s -> {len(y) / SR:.2f} s ; {len(cs)} pauses raccourcies (−{sum(r for _, r in cs):.2f} s)')
    return [[round(c, 3), round(r, 3)] for c, r in cs]


def liste(texte):
    """« 1-7 » ou « 1,3,5 » ou « 2-4,6 »."""
    out = []
    for p in texte.split(','):
        a, _, b = p.partition('-')
        out += list(range(int(a), int(b or a) + 1))
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source'); ap.add_argument('sortie')
    ap.add_argument('--sequences', default='1-7', help='séquences à traiter, ex. 1-7 ou 1,3,5 (défaut 1-7)')
    ap.add_argument('--part', type=float, default=0.6, help='part de la pause gardée (défaut 0.6 = valeur MM)')
    ap.add_argument('--plancher', type=float, default=0.25, help='durée minimale gardée, en s (défaut 0.25 = valeur MM)')
    ap.add_argument('--gardes', help="JSON des fenêtres gardées par séquence (voir l'exemple ci-dessus)")
    a = ap.parse_args()
    if not os.path.isdir(a.sortie) or os.listdir(a.sortie):
        sys.exit(f'refus : {a.sortie} doit exister et être vide')
    gardes = json.load(open(a.gardes, encoding='utf-8')) if a.gardes else {}
    dec = {str(n): sequence(n, a.source, a.sortie, a.part, a.plancher, gardes) for n in liste(a.sequences)}
    json.dump({'regle': f'pauses à {a.part:.0%}, plancher {a.plancher} s ; coupes [début dans la bande source (s), durée retirée (s)]',
               'coupes': dec}, open(os.path.join(a.sortie, 'decalage.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
