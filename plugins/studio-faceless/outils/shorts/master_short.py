"""Master d'un short de la chaîne (19/10/2026) : −14 LUFS intégrés, crête vraie ≤ −1 dBTP dans le MP4 livré.
Valeurs PROPOSÉ (${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md, shorts ; propriétaire de la chaîne AA : « un son plus élevé qui capte l'attention »).
Gain unique, puis limiteur de crêtes vraies, plafond −1,5 dBTP sur le WAV (marge de 0,5 dB pour l'AAC). Les fonctions
crete_par_echantillon et limiteur sont recopiées de l'assembleur du montage de l'E005 d'AA (version antérieure de montage/assembler.py).
L'image est copiée sans réencodage ; le son est réencodé en AAC 48 kHz ; index en tête (faststart). Refuse d'écraser.
Usage : python -I -B master_short.py ENTREE.mp4 SORTIE.mp4 [--cible LUFS] [--plafond dBTP]   (défauts : shorts.master_lufs et shorts.limiteur_dbtp de seuils.json)
"""
import argparse, os, re, shutil, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # outils/ : seuils.py (-I retire le dossier du script)
import seuils   # noqa: E402  ; referentiels/seuils.json (1.1.0)
from scipy.signal import resample_poly
from scipy.ndimage import minimum_filter1d

FF = os.environ.get('HYPERFRAMES_FFMPEG_PATH') or shutil.which('ffmpeg')
SR = 48000


def lire(path):
    raw = subprocess.run([FF, '-v', 'error', '-i', path, '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def ebur128(path):
    err = subprocess.run([FF, '-hide_banner', '-nostats', '-i', path, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                         capture_output=True, text=True, encoding='utf-8', errors='replace', check=True).stderr
    s = err[err.rfind('Summary:'):]
    get = lambda k: float(re.search(k + r':\s+(-?[\d.]+|-inf)', s).group(1))
    return get('I'), get('LRA'), get('Peak')


def ecrire_wav(path, x):
    tmp = path + '.f32'
    x.astype(np.float32).tofile(tmp)
    try:
        subprocess.run([FF, '-v', 'error', '-n', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', tmp, '-c:a', 'pcm_f32le',
                        path], check=True)
    finally:
        os.remove(tmp)


def mesurer(x, chemin):
    ecrire_wav(chemin, x)
    try:
        return ebur128(chemin)
    finally:
        os.remove(chemin)


def crete_par_echantillon(x, bloc=10 * SR, bord=64):
    out = np.empty(len(x))
    for i0 in range(0, len(x), bloc):
        a, b = max(0, i0 - bord), min(len(x), i0 + bloc + bord)
        y = np.abs(resample_poly(x[a:b], 4, 1, axis=0)).max(axis=1).reshape(-1, 4).max(axis=1)
        out[i0:min(len(x), i0 + bloc)] = y[i0 - a:i0 - a + min(bloc, len(x) - i0)]
    return np.maximum(out, np.abs(x).max(axis=1))


def limiteur(x, plafond_db, anticipation=0.005, retour_db_s=25.0):
    c = 10 ** (plafond_db / 20)
    r = np.minimum(1.0, c / np.maximum(crete_par_echantillon(x), 1e-12))
    h = int(anticipation * SR)
    m = minimum_filter1d(r, 2 * h + 1, mode='nearest')
    w = np.hanning(2 * h + 1)
    w /= w.sum()
    gs = np.minimum(np.convolve(np.pad(m, h, mode='edge'), w, mode='valid'), 1.0)
    d = -20 * np.log10(np.minimum(gs, r.clip(None, 1)) + 1e-12)
    pente = retour_db_s / SR
    idx = np.arange(len(d))
    e = np.maximum.accumulate(d + pente * idx) - pente * idx
    return np.maximum(e, 0.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('entree'); ap.add_argument('sortie')
    ap.add_argument('--cible', type=float, default=float(seuils.valeur('shorts.master_lufs')))
    ap.add_argument('--plafond', type=float, default=float(seuils.valeur('shorts.limiteur_dbtp')))
    a = ap.parse_args()
    if os.path.exists(a.sortie):
        raise SystemExit('refus : ' + a.sortie + ' existe déjà')
    tmp = a.sortie + '.mesure.wav'
    x = lire(a.entree)
    I0, _, tp0 = mesurer(x, tmp)
    g = a.cible - I0
    for passe in range(3):
        y = x * 10 ** (g / 20)
        red = limiteur(y, a.plafond)
        y = y * (10 ** (-red / 20))[:, None]
        I1, _, _ = mesurer(y, tmp)
        if abs(I1 - a.cible) < 0.1 or passe == 2:
            break
        g += a.cible - I1
    wav = a.sortie + '.son.wav'
    ecrire_wav(wav, y)
    try:
        subprocess.run([FF, '-v', 'error', '-n', '-i', a.entree, '-i', wav, '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy',
                        '-c:a', 'aac', '-b:a', '256k', '-ar', str(SR), '-movflags', '+faststart', a.sortie], check=True)
    finally:
        os.remove(wav)
    I2, lra, tp2 = ebur128(a.sortie)
    print(f'{os.path.basename(a.entree)} : {I0:.1f} LUFS, crête {tp0:.1f} dBTP -> gain {g:+.2f} dB ; limiteur : maximum '
          f'{red.max():.1f} dB, {(red > 0.5).sum() / SR:.1f} s sous plus de 0,5 dB, {(red > 2).sum() / SR:.2f} s sous plus de 2 dB')
    print(f'{os.path.basename(a.sortie)} : {I2:.1f} LUFS, LRA {lra:.1f} LU, crête vraie {tp2:.1f} dBTP')


if __name__ == '__main__':
    main()
