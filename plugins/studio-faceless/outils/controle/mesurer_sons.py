"""Contrôle des sons de bibliothèque avant leur emploi : format, canaux, durée, niveau intégré, crête vraie, part 1-4 kHz, raccord de boucle,
et parole éventuelle (Whisper). Validé sur AA, 02/11/2026 (sons Soundza de l'E011, S21 de l'audit du même jour).

Généralisé de `mesurer_sons.py` de l'E011 d'AA. Règle : `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 4 bis. Les mesures ne valent jamais une écoute :
elles écartent un son avant que le propriétaire l'écoute ; elles ne le valident pas.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/mesurer_sons.py FICHIER [FICHIER …] [--whisper CHEMIN/ggml-base.en.bin] [--crete-max 0] [--boucle]
Sorties, par fichier : codec, fréquence d'échantillonnage, canaux, durée, niveau intégré (LUFS), crête vraie (dBTP), part de l'énergie entre 1 et 4 kHz
(dB sous le total ; à comparer à celle de la voix), écart début/fin pour une boucle ; puis la liste « À VOIR » :
  - codage 8 bits (μ-law, A-law) ou fréquence d'échantillonnage sous 32 kHz ;
  - crête vraie au-dessus de --crete-max (0 dBTP par défaut : écrêtage possible ; un son à +0,7 dBTP a été écarté sur AA) ;
  - avec --boucle : écart d'énergie début/fin au-delà de 1,5 dB (nappes en boucle, `DIRECTION_AUDIO.md` § 4) ;
  - avec --whisper : parole possible (voir ci-dessous).
Parole : le filtre `whisper` de FFmpeg (modèle ggml gardé hors du projet, par exemple ggml-base.en.bin ; tout téléchargement avec l'accord du propriétaire)
transcrit chaque fichier ; les étiquettes de bruit qu'il invente ([Music], (crowd cheering), [Applause]) sont retirées. S'il reste des mots, le fichier est
signalé « parole possible » : à écouter par le propriétaire (souvent un artefact sur de la musique). Un modèle anglais ne reconnaît pas un chant dans une
autre langue : l'absence de mot ne prouve pas l'absence de parole.
Aucun fichier n'est écrit. Code de sortie : 0 = rien à voir ; 1 = au moins un fichier à voir ou illisible ; 2 = usage. Python, numpy, FFmpeg et ffprobe.
"""
import argparse, glob, importlib.util, json, os, re, shutil, subprocess, sys

SR = 44100
FF_DEFAUT = next(iter(sorted(glob.glob(os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'WinGet', 'Packages', 'Gyan.FFmpeg*', '*', 'bin')))), '')
FF = os.environ.get('HYPERFRAMES_FFMPEG_PATH') or shutil.which('ffmpeg') or os.path.join(FF_DEFAUT, 'ffmpeg.exe')
FP = os.environ.get('HYPERFRAMES_FFPROBE_PATH') or shutil.which('ffprobe') or os.path.join(FF_DEFAUT, 'ffprobe.exe')
ETIQUETTE = re.compile(r'\[[^\]]*\]|\([^)]*\)|\*[^*]*\*|♪[^♪]*♪|♪')
CODECS_8_BITS = ('pcm_mulaw', 'pcm_alaw', 'pcm_u8')


def mots_de_parole(texte):
    """Mots restant d'une transcription Whisper une fois retirées les étiquettes de bruit ([Music], (crowd cheering)…)."""
    sans = ETIQUETTE.sub(' ', texte or '')
    return [m for m in re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)*|\d+", sans)]


def points_a_voir(info, crete_max=0.0, boucle=False, parole=None):
    """Liste des raisons de relire un son (chaînes). `info` : dictionnaire des mesures ; `parole` : liste de mots ou None si non mesurée."""
    pts = []
    if info.get('codec') in CODECS_8_BITS or (info.get('bits') and info['bits'] <= 8):
        pts.append(f"codage 8 bits ({info.get('codec')})")
    if info.get('sr') and info['sr'] < 32000:
        pts.append(f"fréquence d'échantillonnage basse ({info['sr']} Hz)")
    if isinstance(info.get('tp'), float) and info['tp'] > crete_max:
        pts.append(f"crête vraie {info['tp']:+.1f} dBTP au-dessus de {crete_max:+.1f}")
    if boucle and info.get('ecart_boucle') is not None and info['ecart_boucle'] > 1.5:
        pts.append(f"raccord de boucle : écart d'énergie début/fin de {info['ecart_boucle']:.1f} dB (plus de 1,5)")
    if parole:
        pts.append(f"parole possible : « {' '.join(parole[:12])}{' …' if len(parole) > 12 else ''} » ({len(parole)} mot(s))")
    return pts


def sonde(chemin):
    r = subprocess.run([FP, '-v', 'error', '-select_streams', 'a:0', '-show_entries',
                        'stream=codec_name,sample_rate,channels,bits_per_sample,bits_per_raw_sample,sample_fmt,duration:format=duration',
                        '-of', 'json', chemin], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        raise RuntimeError('ffprobe : ' + r.stderr.strip()[-200:])
    d = json.loads(r.stdout or '{}')
    s = (d.get('streams') or [{}])[0]
    bits = int(s.get('bits_per_raw_sample') or s.get('bits_per_sample') or 0) or None
    duree = s.get('duration') or (d.get('format') or {}).get('duration')
    return {'codec': s.get('codec_name'), 'sr': int(s['sample_rate']) if s.get('sample_rate') else None, 'canaux': s.get('channels'),
            'bits': bits, 'duree_fichier': float(duree) if duree else None}


def decoder(chemin, filtre=None):
    import numpy as np
    cmd = [FF, '-v', 'error', '-i', chemin, '-ac', '1', '-ar', str(SR)]
    if filtre:
        cmd += ['-af', filtre]
    cmd += ['-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)


def niveau(chemin):
    r = subprocess.run([FF, '-hide_banner', '-nostats', '-i', chemin, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace').stderr
    i = re.findall(r'I:\s+(-?[\d.]+|-inf) LUFS', r)
    tp = re.findall(r'Peak:\s+(-?[\d.]+|-inf) dBFS', r)
    return (float(i[-1]) if i and i[-1] != '-inf' else None), (float(tp[-1]) if tp and tp[-1] != '-inf' else None)


def db(x):
    import numpy as np
    return 20 * np.log10(max(float(np.sqrt(np.mean(np.square(x)))), 1e-9))


def parole(chemin, modele):
    """Mots restants d'une transcription Whisper (après retrait des étiquettes). Lève RuntimeError si la transcription échoue."""
    spec = importlib.util.spec_from_file_location('transcrire', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'transcrire.py'))
    t = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(t)
    try:
        segments = t.whisper(chemin, modele, False)
    except SystemExit as e:
        raise RuntimeError(str(e.code))
    return mots_de_parole(' '.join(w for _, _, w in segments))


def mesurer(chemin, modele=None):
    info = sonde(chemin)
    tout = decoder(chemin)
    info['duree'] = len(tout) / SR
    bande = decoder(chemin, 'highpass=f=1000:poles=2,lowpass=f=4000:poles=2')
    info['lufs'], info['tp'] = niveau(chemin)
    info['bande_1_4k'] = db(bande) - db(tout)
    n = int(0.1 * SR)
    info['debut_db'], info['fin_db'] = db(tout[:n]), db(tout[-n:])
    info['ecart_boucle'] = abs(info['fin_db'] - info['debut_db'])
    info['saut'] = abs(float(tout[-1]) - float(tout[0]))
    info['mots'] = parole(chemin, modele) if modele else None
    return info


def ligne(chemin, i):
    f = lambda v, fmt: ('?' if v is None else format(v, fmt))
    return (f"{os.path.basename(chemin):44s} {i['codec'] or '?':>10} {f(i['sr'], '')} Hz {i['canaux'] or '?'} can. {i['bits'] or '?'} bits {i['duree']:7.2f} s  "
            f"I {f(i['lufs'], '6.1f')} LUFS  TP {f(i['tp'], '+5.1f')} dBTP  1-4 kHz {i['bande_1_4k']:6.1f} dB  "
            f"boucle : fin {i['fin_db']:6.1f} / début {i['debut_db']:6.1f} dB, saut {i['saut']:.3f}")


def main(argv=None):
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, 'reconfigure'):
            flux.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('fichiers', nargs='+')
    ap.add_argument('--whisper', metavar='MODELE', help='modèle ggml (hors du projet) pour repérer une parole')
    ap.add_argument('--crete-max', type=float, default=0.0, help='crête vraie (dBTP) au-dessus de laquelle un son est signalé')
    ap.add_argument('--boucle', action='store_true', help='signaler un raccord de boucle (écart début/fin au-delà de 1,5 dB)')
    a = ap.parse_args(argv)
    if a.whisper and not os.path.isfile(a.whisper):
        print('Modèle introuvable : ' + a.whisper + ' (gardé hors du projet ; téléchargement avec l\'accord du propriétaire)', file=sys.stderr)
        return 2
    voir = 0
    for chemin in a.fichiers:
        try:
            info = mesurer(chemin, a.whisper)
        except (RuntimeError, OSError, subprocess.CalledProcessError, ValueError) as e:
            print(f'{os.path.basename(chemin)} : ILLISIBLE ({e})')
            voir += 1
            continue
        print(ligne(chemin, info))
        pts = points_a_voir(info, a.crete_max, a.boucle, info['mots'])
        if info['mots'] is not None and not info['mots']:
            print('    parole : aucune (étiquettes de bruit seulement, ou rien)')
        for p in pts:
            print('    À VOIR : ' + p)
        voir += bool(pts)
    print(f'{len(a.fichiers)} fichier(s) mesuré(s), {voir} à voir. Les mesures ne valent pas une écoute.')
    return 1 if voir else 0


if __name__ == '__main__':
    sys.exit(main())
