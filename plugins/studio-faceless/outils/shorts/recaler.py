"""Repères mot à mot recalés sur les vrais départs de la voix (méthode de l'E004 et de l'E005 d'AA) :
1. départs réels = fins des silences (−40 dB, au moins 0,25 s), plus le premier son de la bande ;
2. chaque phrase de Whisper prend le premier départ réel entre −0,3 et +1,8 s autour de son repère ;
3. ses mots gardent ce décalage, puis se posent sur le départ réel le plus proche (−0,3 / +0,4 s).
Usage : python -I -B recaler.py BANDE.wav MOTS_WHISPER.json SORTIE_PREFIXE
Écrit SORTIE_PREFIXE-mots-recales.json et SORTIE_PREFIXE-phrases-recalees.txt ; refuse d'écraser.
"""
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'controle'))
import ralentir as R  # noqa: E402


def main():
    bande, mots_json, pref = sys.argv[1:4]
    out_m, out_p = pref + '-mots-recales.json', pref + '-phrases-recalees.txt'
    for f in (out_m, out_p):
        if os.path.exists(f):
            raise SystemExit('refus : ' + f + ' existe déjà')
    x = R.f32(['-i', bande])
    sil = R.silences(x, mini=0.25)
    departs = sorted({round(s1, 2) for s0, s1 in sil if s1 < len(x) / R.SR - 0.05})
    n = int(0.01 * R.SR)
    fr = x[: len(x) // n * n].reshape(-1, n)
    son = np.nonzero(20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9) >= -40)[0]
    if len(son):
        departs = sorted(set(departs) | {round(son[0] * 0.01, 2)})
    mots = json.load(open(mots_json, encoding='utf-8'))['mots']
    phrases, cur = [], []
    for m in mots:
        cur.append(m)
        if m['w'].rstrip('"\'”').endswith(('.', '?', '!')):
            phrases.append(cur); cur = []
    if cur:
        phrases.append(cur)
    sortie_m, lignes, non = [], [], 0
    for ph in phrases:
        t = ph[0]['start']
        cand = [d for d in departs if t - 0.3 <= d <= t + 1.8]
        delta = (cand[0] - t) if cand else 0.0
        non += 0 if cand else 1
        for m in ph:
            s = m['start'] + delta
            proche = [d for d in departs if s - 0.3 <= d <= s + 0.4]
            if proche:
                s = min(proche, key=lambda d: abs(d - s))
            sortie_m.append({'w': m['w'], 'start': round(s, 2), 'end': round(m['end'] + delta, 2),
                             'start_whisper': m['start']})
        debut = sortie_m[-len(ph)]['start']
        lignes.append(f"{debut:7.2f} – {sortie_m[-1]['end']:7.2f}  {' '.join(m['w'] for m in ph)}"
                      + ('' if cand else '   [non recalée]'))
    for a, b in zip(sortie_m, sortie_m[1:]):
        if a['end'] > b['start']:
            a['end'] = b['start']
    with open(out_m, 'x', encoding='utf-8') as f:
        json.dump({'source': 'Whisper (FFmpeg, max_len=1), recalé sur les départs réels (silencedetect −40 dB, 0,25 s)',
                   'mots': sortie_m}, f, ensure_ascii=False, indent=1)
    with open(out_p, 'x', encoding='utf-8') as f:
        f.write('Début – fin (s), recalés sur les départs réels de la voix\n' + '\n'.join(lignes) + '\n')
    print(f'{os.path.basename(pref)} : {len(phrases)} phrases, {len(sortie_m)} mots, {non} phrase(s) non recalée(s)')


if __name__ == '__main__':
    main()
