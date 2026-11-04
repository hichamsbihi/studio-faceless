"""Ralentit « juste un peu » une prise de narration — 15/10/2026, pauses corrigées le 17/10/2026.

Méthode validée sur AA (${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md § 2) :
  1. parole ramenée à −20 dBFS RMS (gain seul) ;
  2. tempo × 0,97 (atempo de FFmpeg, hauteur conservée) ; × 0,94 jusqu'à l'E008 v1 d'AA, × 0,97 validé sur AA le 26/10/2026 ;
  3. pauses internes allongées : +0,15 s de 0,36 à 0,60 s, +0,25 s au-delà. Le silence ajouté est inséré au milieu du plus
     long passage au plancher de la pause, à 60 ms au moins de la fin du mot et 30 ms du mot suivant :
     - silence numérique si ce plancher est sous −70 dBFS (cas des prises ElevenLabs, ≈ −86 dBFS) ;
     - sinon, bruit généré au spectre et au niveau de ce passage (graine fixe), jamais une recopie.
     La version du 15/10/2026 recopiait le début de la pause, qui contient encore la queue du mot : la fin du mot
     revenait 0,15 à 0,46 s plus tard (bandes des épisodes 003 et 004 d'AA ; étude AA, 17/10/2026).
     Correctif validé sur AA le 17/10/2026 pour les épisodes suivants. Les mots tombent aux mêmes instants qu'avec
     l'ancienne version : seul le contenu des pauses change ;
  4. 0,6 s de silence en tête, 1,2 s en queue (réglables) ;
  5. gain unique vers −19 LUFS en mesure mono (−16 LUFS en double mono dans un MP4 stéréo), crête vraie ≤ −2 dBTP ;
  6. auto-contrôle : aucun passage de la bande ne doit être la copie exacte d'un passage 80 à 600 ms plus tôt
     (environ 30 s de calcul par minute et demie de voix) ; sinon, rien n'est écrit.
Aucune coupe, aucun mot retiré ni ajouté. À n'appliquer qu'à la narration : jamais aux voix jouées (chants, citations).

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/ralentir.py PRISE.mp3 SORTIE.wav [--tempo 0.97] [--tete 0.6] [--queue 1.2] [--cible LUFS]   (défaut : mix.voix_mono_lufs de seuils.json)
Écrit SORTIE.wav (48 kHz, mono, 24 bits) et SORTIE.positions.txt. Refuse d'écraser. La prise d'origine n'est pas modifiée.
"""
import argparse, glob, hashlib, os, re, shutil, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # outils/ : seuils.py (-I retire le dossier du script)
import seuils   # noqa: E402  ; referentiels/seuils.json (1.1.0)

FF_DEFAUT = next(iter(sorted(glob.glob(os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'WinGet', 'Packages', 'Gyan.FFmpeg*', '*', 'bin')))), '')  # FFmpeg de WinGet s'il existe ; aucun chemin propre à une machine
FF = os.environ.get('HYPERFRAMES_FFMPEG_PATH') or shutil.which('ffmpeg') or os.path.join(FF_DEFAUT, 'ffmpeg.exe')
SR = 48000
REGLES_PAUSES = ((0.36, 0.60, 0.15), (0.60, 99, 0.25))
PLANCHER_NUMERIQUE = -70.0      # dBFS : sous ce plancher, la pause est allongée par un silence numérique


def f32(args, x=None):
    cmd = [FF, '-v', 'error'] + args + ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, input=None if x is None else np.asarray(x, np.float32).tobytes(),
                                        capture_output=True, check=True).stdout, np.float32).copy()


def silences(x, seuil=-40.0, mini=0.12, trame=0.01):
    n = int(trame * SR)
    fr = x[: len(x) // n * n].reshape(-1, n)
    calme = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9) < seuil
    out, debut = [], None
    for i, q in enumerate(calme):
        if q and debut is None:
            debut = i
        if (not q or i == len(calme) - 1) and debut is not None:
            fin = i if not q else i + 1
            if (fin - debut) * trame >= mini:
                out.append((round(debut * trame, 2), round(fin * trame, 2)))
            debut = None
    return out


def point_calme(y, s0, s1, apres_mot=0.06, avant_mot=0.03, marge=6.0, trame=0.01):
    """Milieu du plus long passage au plancher de la pause [s0, s1] (trames ≤ minimum + 6 dB), à 60 ms au moins de la fin
    du mot et 30 ms du mot suivant. Renvoie l'échantillon d'insertion, le plancher (dBFS) et le passage lui-même."""
    n = int(trame * SR)
    a, b = int((s0 + apres_mot) * SR), int((s1 - avant_mot) * SR)
    fr = y[a: a + (b - a) // n * n].astype(np.float64).reshape(-1, n)
    lv = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-12)
    meilleur, debut = (int(np.argmin(lv)), int(np.argmin(lv)) + 1), None
    for i, q in enumerate(np.append(lv <= lv.min() + marge, False)):
        if q and debut is None:
            debut = i
        if not q and debut is not None:
            if i - debut > meilleur[1] - meilleur[0]:
                meilleur = (debut, i)
            debut = None
    r0, r1 = a + meilleur[0] * n, a + meilleur[1] * n
    return (r0 + r1) // 2, float(lv.min()), y[r0:r1]


def bruit_de_fond(src, n, graine):
    """n échantillons de bruit au spectre et au niveau du passage src, phases tirées au hasard : aucune recopie."""
    S = np.abs(np.fft.rfft(src.astype(np.float64) * np.hanning(len(src))))
    mag = np.interp(np.linspace(0, 1, n // 2 + 1), np.linspace(0, 1, len(S)), S)
    b = np.fft.irfft(mag * np.exp(1j * np.random.default_rng(graine).uniform(0, 2 * np.pi, len(mag))), n)
    b *= np.sqrt(np.mean(src.astype(np.float64) ** 2)) / (np.sqrt(np.mean(b ** 2)) + 1e-20)
    k = min(int(0.005 * SR), n // 2)
    b[:k] *= np.linspace(0, 1, k); b[-k:] *= np.linspace(1, 0, k)
    return b.astype(np.float32)


def recopies(x, decal=(0.08, 0.6), trame=0.02, pas=0.01, seuil=0.995, plancher=-75.0, mini=5):
    """Passages copiés à l'identique d'un passage 80 à 600 ms plus tôt : corrélation normalisée ≥ 0,995 sur au moins
    5 trames de 20 ms de suite, au même décalage, au-dessus de −75 dBFS. Une voix naturelle, même après atempo, n'en a
    aucun (étude AA, 17/10/2026). Renvoie [(début en s, décalage en s), …]."""
    x = np.asarray(x, np.float64)
    W, H, L0, L1 = int(trame * SR), int(pas * SR), int(decal[0] * SR), int(decal[1] * SR)
    R = L1 - L0 + W
    nfft = 1 << int(np.ceil(np.log2(R + W)))
    c2 = np.concatenate([[0.0], np.cumsum(x ** 2)])
    ev = []
    for i in range(L1, len(x) - W, H):
        f = x[i:i + W]
        ef = float(f @ f)
        if 10 * np.log10(ef / W + 1e-20) < plancher:
            continue
        r0 = i - L1
        c = np.fft.irfft(np.fft.rfft(x[r0:r0 + R], nfft) * np.conj(np.fft.rfft(f, nfft)), nfft)[:R - W + 1]
        nc = c / np.sqrt(ef * np.maximum(c2[r0 + W:r0 + R + 1] - c2[r0:r0 + R - W + 1], 1e-30))
        k = int(np.argmax(nc))
        if nc[k] < seuil:
            continue
        lag = i - (r0 + k)
        if ev and i - ev[-1][1] <= H and abs(lag - ev[-1][2]) <= 2:
            ev[-1][1] = i; ev[-1][3] += 1
        else:
            ev.append([i, i, lag, 1])
    return [(a / SR, lag / SR) for a, _, lag, n in ev if n >= mini]


def stats(x):
    d = len(x) / SR
    sil = silences(x)
    inner = [s for s in sil if s[0] > 0.05 and s[1] < d - 0.05]
    on = sil[0][1] if sil and sil[0][0] <= 0.01 else 0.0
    off = sil[-1][0] if sil and sil[-1][1] >= d - 0.01 else d
    p = np.array([b - a for a, b in inner]) if inner else np.array([0.0])
    return off - on, float(np.median(p)), len(inner)


def ebur128(sig, tmp):
    np.asarray(sig, np.float32).tofile(tmp)
    try:
        err = subprocess.run([FF, '-hide_banner', '-nostats', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', tmp,
                              '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True,
                             encoding='utf-8', errors='replace', check=True).stderr
    finally:
        os.remove(tmp)
    s = err[err.rfind('Summary:'):]
    get = lambda k: float(re.search(k + r':\s+(-?[\d.]+|-inf)', s).group(1))
    return get('I'), get('Peak')


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser()
    ap.add_argument('prise'); ap.add_argument('sortie')
    ap.add_argument('--tempo', type=float, default=0.97); ap.add_argument('--tete', type=float, default=0.6)
    ap.add_argument('--queue', type=float, default=1.2); ap.add_argument('--cible', type=float, default=float(seuils.valeur('mix.voix_mono_lufs')))
    a = ap.parse_args()
    pos = os.path.splitext(a.sortie)[0] + '.positions.txt'
    for p in (a.sortie, pos):
        if os.path.exists(p):
            sys.exit('Sortie existante, aucun écrasement : ' + p)
    x = f32(['-i', a.prise])
    act = x[np.abs(x) > 10 ** (-45 / 20)]
    g0 = -20 - 20 * np.log10(np.sqrt(np.mean(act ** 2)) + 1e-9)
    x = x * 10 ** (g0 / 20)
    y = f32(['-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', 'pipe:0', '-af', f'atempo={a.tempo}'], x)
    d = len(y) / SR
    morceaux, dernier, ajouts, planchers = [], 0, [], []
    for s0, s1 in silences(y):
        if s0 <= 0.05 or s1 >= d - 0.05:
            continue
        e = next((e for lo, hi, e in REGLES_PAUSES if lo <= s1 - s0 < hi), 0.0)
        if not e:
            continue
        m, plancher, src = point_calme(y, s0, s1)
        n = int(round(e * SR))
        rempl = np.zeros(n, np.float32) if plancher <= PLANCHER_NUMERIQUE else bruit_de_fond(src, n, len(ajouts))
        morceaux += [y[dernier:m], rempl]
        dernier = m
        ajouts.append(e); planchers.append(plancher)
    morceaux.append(y[dernier:])
    z = np.concatenate([np.zeros(int(a.tete * SR), np.float32)] + morceaux + [np.zeros(int(a.queue * SR), np.float32)])
    I0, _ = ebur128(z, a.sortie + '.f32')
    z = z * 10 ** ((a.cible - I0) / 20)
    I1, tp = ebur128(z, a.sortie + '.f32')
    if tp > -2.0:
        z = z * 10 ** ((-2.0 - tp) / 20)
        I1, tp = ebur128(z, a.sortie + '.f32')
    rec = recopies(z)
    if rec:
        sys.exit(f'Auto-contrôle : {len(rec)} recopie(s) exacte(s) dans la bande, aucun fichier écrit : '
                 + ', '.join(f'{t:.2f} s (copie de {dl:.2f} s plus tôt)' for t, dl in rec[:8]))
    tmp = a.sortie + '.f32'
    z.astype(np.float32).tofile(tmp)
    try:
        subprocess.run([FF, '-v', 'error', '-n', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', tmp, '-c:a', 'pcm_s24le', a.sortie], check=True)
    finally:
        os.remove(tmp)
    p0, m0, n0 = stats(x)
    p1, m1, n1 = stats(z)
    sha = hashlib.sha1(open(a.prise, 'rb').read()).hexdigest()
    lignes = [f'Prise : {a.prise} (SHA-1 {sha})',
              f'Durée : {len(x) / SR:.2f} s → {len(z) / SR:.2f} s ; tempo ×{a.tempo} ; {len(ajouts)} pauses allongées (+{sum(ajouts):.2f} s)',
              f'Parole : {p0:.2f} s → {p1 - a.tete:.2f} s ; pause médiane {m0:.2f} → {m1:.2f} s',
              f'Niveau : {I1:.1f} LUFS (mesure mono ; ≈ {I1 + 3:.0f} en double mono), crête vraie {tp:.1f} dBTP, gain total {g0 + a.cible - I0:+.1f} dB',
              f'Pauses allongées (méthode du 17/10/2026) : '
              + (f'plancher le plus haut {max(planchers):.0f} dBFS ; {sum(p <= PLANCHER_NUMERIQUE for p in planchers)} en silence numérique, '
                 f'{sum(p > PLANCHER_NUMERIQUE for p in planchers)} en bruit de fond généré' if planchers else 'aucune')
              + ' ; auto-contrôle : 0 recopie exacte']
    open(pos, 'x', encoding='utf-8').write('\n'.join(lignes) + '\n')
    print('\n'.join(lignes))
    print("Étape suivante : transcrire la bande ralentie (outils/controle/transcrire.py) pour donner les repères aux producteurs.")


if __name__ == '__main__':
    main()
