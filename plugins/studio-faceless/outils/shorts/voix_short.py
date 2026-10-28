"""Bande voix d'un short de la chaîne (19/10/2026, décisions validées sur AA le même jour).

1. Tête ramenée à 0,05 s avant le premier mot, queue à 0,5 s après le dernier.
2. Option --sans-d DEBUT FIN : retire le bloc D, de l'intérieur du silence qui contient DEBUT à l'intérieur de celui qui
   contient FIN ; la pause qui reste fait --plafond secondes (frontières de phrase).
3. Pauses internes plafonnées à --plafond (0,35 s) : l'excédent est retiré autour du point le plus calme de la pause,
   à 60 ms au moins de la fin du mot et 30 ms du mot suivant (fonction point_calme de ralentir.py). Fondu de 5 ms.
4. Gain unique vers −19 LUFS en mesure mono, crête vraie ≤ −2 dBTP (le plafond de crête l'emporte).
5. Auto-contrôle : aucune recopie (fonction recopies de ralentir.py) ; sinon, rien n'est écrit.
Aucun mot retiré hors du bloc D, aucun ajouté, aucun changement de tempo. Refuse d'écraser.
"""
import argparse, json, os, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'controle'))
import ralentir as R  # noqa: E402

SR = R.SR


def contenant(sil, t):
    for s0, s1 in sil:
        if s0 <= t <= s1:
            return s0, s1
    raise SystemExit(f'aucun silence ne contient {t:.2f} s')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('prise'); ap.add_argument('sortie')
    ap.add_argument('--plafond', type=float, default=0.35)
    ap.add_argument('--sans-d', nargs=2, type=float, metavar=('DEBUT', 'FIN'))
    ap.add_argument('--cible', type=float, default=-19.0)
    a = ap.parse_args()
    if os.path.exists(a.sortie):
        raise SystemExit('refus : ' + a.sortie + ' existe déjà')
    x = R.f32(['-i', a.prise])
    d = len(x) / SR
    sil = R.silences(x)
    retraits = []                                   # intervalles retirés, en secondes de la prise
    onset = sil[0][1] if sil and sil[0][0] <= 0.01 else 0.0
    if onset > 0.05:
        retraits.append((0.0, onset - 0.05, 'tête'))
    offset = sil[-1][0] if sil and sil[-1][1] >= d - 0.01 else d
    if d - offset > 0.5:
        retraits.append((offset + 0.5, d, 'queue'))
    pris = set()
    if a.sans_d:
        sa, sb = contenant(sil, a.sans_d[0]), contenant(sil, a.sans_d[1])
        retraits.append((sa[0] + a.plafond / 2, sb[1] - a.plafond / 2, 'bloc D'))
        pris |= {sa, sb}
        dans_d = lambda s: sa[1] <= s[0] and s[1] <= sb[0]
    else:
        dans_d = lambda s: False
    for s0, s1 in sil:
        if (s0, s1) in pris or dans_d((s0, s1)) or s0 <= 0.01 or s1 >= d - 0.01:
            continue
        exces = (s1 - s0) - a.plafond
        if exces <= 0:
            continue
        pos, _, _ = R.point_calme(x, s0, s1)
        lo, hi = s0 + 0.06, s1 - 0.03
        exces = min(exces, hi - lo)
        r0 = min(max(pos / SR - exces / 2, lo), hi - exces)
        retraits.append((r0, r0 + exces, f'pause {s1 - s0:.2f} s'))
    retraits.sort()
    k = int(0.005 * SR)
    morceaux, t = [], 0.0
    for r0, r1, _ in retraits:
        morceaux.append(x[int(t * SR):int(r0 * SR)]); t = r1
    morceaux.append(x[int(t * SR):])
    y = morceaux[0]
    for m in morceaux[1:]:
        if len(y) > k and len(m) > k:
            rampe = np.linspace(0, 1, k, dtype=np.float32)
            y = np.concatenate([y[:-k], y[-k:] * (1 - rampe) + m[:k] * rampe, m[k:]])
        else:
            y = np.concatenate([y, m])
    tmp = a.sortie + '.tmp.f32'
    i0, p0 = R.ebur128(y, tmp)
    gain = a.cible - i0
    if p0 + gain > -2.0:
        gain = -2.0 - p0
    y = (y * 10 ** (gain / 20)).astype(np.float32)
    i1, p1 = R.ebur128(y, tmp)
    rec = R.recopies(y)
    if rec:
        raise SystemExit(f'refus : {len(rec)} recopie(s) détectée(s), rien n\'est écrit')
    subprocess.run([R.FF, '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_s24le',
                    a.sortie], input=y.tobytes(), check=True)
    info = {'prise': os.path.basename(a.prise), 'duree_prise_s': round(d, 3), 'duree_bande_s': round(len(y) / SR, 3),
            'plafond_pauses_s': a.plafond, 'gain_db': round(gain, 2), 'niveau_lufs_mono': round(i1, 1),
            'crete_vraie_dbtp': round(p1, 1), 'recopies': 0,
            'retraits': [{'debut_s': round(r0, 3), 'fin_s': round(r1, 3), 'motif': m} for r0, r1, m in retraits]}
    with open(os.path.splitext(a.sortie)[0] + '.positions.json', 'x', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=1)
    print(f"{os.path.basename(a.sortie)} : {d:.2f} s -> {len(y) / SR:.2f} s ; {len(retraits)} retraits ; "
          f"gain {gain:+.1f} dB ; {i1:.1f} LUFS mono ; crête {p1:.1f} dBTP ; recopies 0")


if __name__ == '__main__':
    main()
