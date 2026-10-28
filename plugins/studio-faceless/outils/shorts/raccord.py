"""Insère un raccord de voix dans une prise (19/10/2026, short 02 de l'E001 d'AA ; raccord demandé par le propriétaire).
On coupe la prise au milieu du silence qui précède la phrase remplacée (COUPE_A) et au milieu de celui qui la suit (COUPE_B).
On y insère le raccord, débarrassé de ses silences de tête et de queue, avec MARGE secondes de silence de chaque côté (sa
propre respiration). Le gain du raccord est aligné sur la parole des phrases voisines (RMS des trames > −40 dBFS). Fondus de 10 ms.
Usage : python -I -B raccord.py PRISE RACCORD SORTIE.wav COUPE_A COUPE_B [--marge 0.27]
Refuse d'écraser ; écrit aussi SORTIE.json (points de coupe, gain)."""
import argparse, json, os, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'controle'))
import ralentir as R  # noqa: E402

SR = R.SR


def rms_parole(x):
    n = int(0.01 * SR)
    fr = x[: len(x) // n * n].reshape(-1, n).astype(np.float64)
    lv = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-12)
    return float(20 * np.log10(np.sqrt((fr[lv > -40] ** 2).mean()) + 1e-12))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('prise'); ap.add_argument('raccord'); ap.add_argument('sortie')
    ap.add_argument('coupe_a', type=float); ap.add_argument('coupe_b', type=float)
    ap.add_argument('--marge', type=float, default=0.27)
    a = ap.parse_args()
    if os.path.exists(a.sortie):
        raise SystemExit('refus : ' + a.sortie + ' existe déjà')
    x, r = R.f32(['-i', a.prise]), R.f32(['-i', a.raccord])
    sil = R.silences(r)
    on = sil[0][1] if sil and sil[0][0] <= 0.01 else 0.0
    off = sil[-1][0] if sil and sil[-1][1] >= len(r) / SR - 0.01 else len(r) / SR
    r0, r1 = max(0.0, on - a.marge), min(len(r) / SR, off + a.marge)
    piece = r[int(r0 * SR):int(r1 * SR)]
    voisins = np.concatenate([x[int((a.coupe_a - 6) * SR):int(a.coupe_a * SR)], x[int(a.coupe_b * SR):int((a.coupe_b + 6) * SR)]])
    gain = rms_parole(voisins) - rms_parole(piece)
    piece = piece * 10 ** (gain / 20)
    k = int(0.01 * SR)
    avant, apres = x[:int(a.coupe_a * SR)], x[int(a.coupe_b * SR):]
    rampe = np.linspace(0, 1, k, dtype=np.float32)
    y = np.concatenate([avant[:-k], avant[-k:] * (1 - rampe) + piece[:k] * rampe, piece[k:-k],
                        piece[-k:] * (1 - rampe) + apres[:k] * rampe, apres[k:]]).astype(np.float32)
    subprocess.run([R.FF, '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_s24le',
                    a.sortie], input=y.tobytes(), check=True)
    info = {'prise': os.path.basename(a.prise), 'raccord': os.path.basename(a.raccord), 'coupe_a_s': a.coupe_a,
            'coupe_b_s': a.coupe_b, 'raccord_utilise_s': [round(r0, 3), round(r1, 3)], 'gain_raccord_db': round(gain, 2),
            'duree_s': round(len(y) / SR, 3)}
    with open(os.path.splitext(a.sortie)[0] + '.json', 'x', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=1)
    print(json.dumps(info, ensure_ascii=False))


if __name__ == '__main__':
    main()
