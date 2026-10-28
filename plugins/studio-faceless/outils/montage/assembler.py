"""Collage d'un film de la chaîne à partir des MP4 de ses séquences. Outil commun du studio (24/10/2026).

Repris de l'assembleur du montage de l'E007 d'AA (master E007 v1, approuvé par le propriétaire d'AA le 24/10/2026),
qui n'est pas modifié : mêmes segments, noirs, fondus enchaînés, déclic de la voix, gain unique, limiteur et contrôles.
Ce qui change : la configuration vient d'un fichier JSON (schéma : ${CLAUDE_PLUGIN_ROOT}/outils/montage/README.md), et le mode --voix-seule
prépare le mix du film à la fin (${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md § 3 ; ${CLAUDE_PLUGIN_ROOT}/outils/montage/mix_film.py).

Modes :
  (défaut)      son = pistes mixées des séquences (voix déclinquée) et son propre des pièces de marque ; gain unique vers
                −16 LUFS sur les séquences, limiteur de crêtes vraies à −2,0 dBTP (comportement du master E007 v1 d'AA) ;
  --voix-seule  son = voix seules des séquences (pistes/stem-voix.wav, déclinquées) et son propre des pièces de marque ;
                aucun gain (la voix garde son niveau pour le mix du film), limiteur seulement si une crête dépasse −2,0 dBTP ;
  --son-seul    mesure le son et le limiteur sans rien écrire (se combine avec --voix-seule).
Sorties : NOM.mp4, NOM.mix.wav (ou NOM.voix.wav), NOM.log.txt (journal du master, même format que l'E007 d'AA)
et NOM.journal.json (segments à l'image près, lu par mix_film.py). Refuse toujours d'écraser.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/assembler.py [CONFIG.json | --episode ID] [--voix-seule] [--son-seul] [--sans-limiteur]
                                           [--nom NOM.mp4] [--out DOSSIER]
Sans CONFIG : episodes/<ID>/montage/montage.json. Les chemins relatifs du JSON partent de la racine de la chaîne.
"""
import argparse, glob, json, os, re, shutil, subprocess, sys
import numpy as np
from scipy.ndimage import minimum_filter1d
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd())   # dossier de la chaîne, pas celui du plugin
FF_DEFAUT = next(iter(sorted(glob.glob(os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'WinGet', 'Packages', 'Gyan.FFmpeg*', '*', 'bin')))), '')
FF = os.environ.get('HYPERFRAMES_FFMPEG_PATH') or shutil.which('ffmpeg') or os.path.join(FF_DEFAUT, 'ffmpeg.exe')
FP = os.environ.get('HYPERFRAMES_FFPROBE_PATH') or shutil.which('ffprobe') or os.path.join(FF_DEFAUT, 'ffprobe.exe')
SR, FPS, W, H = 48000, 30, 1920, 1080
TARGET_I, MAX_TP, PLAFOND_WAV = -16.0, -1.5, -2.0
BT709 = 'setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv'


# --- Chemins et configuration ------------------------------------------------------------------------------------------

def chemin(p, base=ROOT):
    return os.path.normpath(p if os.path.isabs(p) else os.path.join(base, p))


def rel(p):
    p = os.path.abspath(p)
    return os.path.relpath(p, ROOT) if p.lower().startswith(ROOT.lower() + os.sep) else p


def charger_config(path):
    with open(path, encoding='utf-8') as f:
        c = json.load(f)
    for k in ('episode', 'sequences', 'sortie'):
        if k not in c:
            sys.exit(f'Configuration incomplète, « {k} » manque : {path}')
    seqs = []
    for s in c['sequences']:
        d = chemin(s['dossier'])
        seqs.append({'id': s['id'], 'mp4': chemin(s['mp4'], d), 'voix': chemin(s.get('voix', 'pistes/stem-voix.wav'), d),
                     'mix': chemin(s['mix'], d) if s.get('mix') else None})
    ids = [s['id'] for s in seqs]
    if len(set(ids)) != len(ids) or 'noir' in ids:
        sys.exit('Identifiants de séquence en double ou réservés (« noir ») : ' + ', '.join(ids))
    c['sequences'] = seqs
    return c


def plan_segments(c):
    """Ordre du film : chaque séquence, puis les pièces de marque placées après elle (noirs autour), puis l'outro."""
    ids = [s['id'] for s in c['sequences']]
    noir = lambda s: {'id': 'noir', 'type': 'noir', 'fichier': None, 'images': int(round(s * FPS))}
    plan = []
    for m in c.get('marque', []):
        if m.get('apres') not in ids:
            sys.exit(f'Pièce de marque placée après une séquence inconnue : {m}')
    for s in c['sequences']:
        plan.append({'id': s['id'], 'type': 'sequence', 'fichier': s['mp4'], 'seq': s})
        for m in c.get('marque', []):
            if m['apres'] == s['id']:
                if m.get('noir_avant', 0):
                    plan.append(noir(m['noir_avant']))
                plan.append({'id': m.get('id', 'marque'), 'type': 'marque', 'fichier': chemin(m['fichier'])})
                if m.get('noir_apres', 0):
                    plan.append(noir(m['noir_apres']))
    o = c.get('outro')
    if o:
        if o.get('noir_avant', 0):
            plan.append(noir(o['noir_avant']))
        plan.append({'id': o.get('id', 'outro'), 'type': 'marque', 'fichier': chemin(o['fichier'])})
    autres = [p['id'] for p in plan if p['type'] != 'noir']
    if len(set(autres)) != len(autres):
        sys.exit('Identifiants de segment en double : ' + ', '.join(autres))
    fondus = {}
    for k, f in c.get('fondus', {}).items():
        a, _, b = k.partition('>')
        if not any(p['id'] == a.strip() and q['id'] == b.strip() for p, q in zip(plan, plan[1:])):
            sys.exit(f'Fondu « {k} » : les deux segments ne se suivent pas dans le film')
        fondus[(a.strip(), b.strip())] = int(f)
    return plan, fondus


# --- Son : lecture, mesures, déclic, limiteur ----------------------------------------------------------------------------

def probe(path):
    out = subprocess.run([FP, '-v', 'error', '-count_frames', '-show_entries',
                          'stream=codec_type,width,height,r_frame_rate,nb_read_frames',
                          '-of', 'json', path], capture_output=True, text=True, check=True).stdout
    v = next(s for s in json.loads(out)['streams'] if s['codec_type'] == 'video')
    if (v['width'], v['height'], v['r_frame_rate']) != (W, H, f'{FPS}/1'):
        sys.exit(f'Format inattendu ({v["width"]}×{v["height"]}, {v["r_frame_rate"]}) : {path}')
    return int(v['nb_read_frames'])


def lire(path, dtype=np.float64):
    return np.frombuffer(subprocess.run([FF, '-v', 'error', '-i', path, '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                                        capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).astype(dtype)


def caler(x, n):
    x = x[:n] if len(x) >= n else np.vstack([x, np.zeros((n - len(x), 2), x.dtype)])
    k = int(0.005 * SR)
    x = x.copy()
    x[:k] *= np.linspace(0, 1, k)[:, None]
    x[-k:] *= np.linspace(1, 0, k)[:, None]
    return x


def db(x):
    return 20 * np.log10(np.sqrt(np.mean(np.asarray(x) ** 2)) + 1e-12)


def clics_isoles(mono):
    """Même règle que outils/controle/controle.py (_clics_isoles), recopiée pour que l'outil reste autonome."""
    k = int(0.002 * SR)
    m = len(mono) // k
    d = 20 * np.log10(np.sqrt((mono[:m * k].reshape(m, k) ** 2).mean(axis=1)) + 1e-9)
    out, i = [], 10
    while i < m - 10:
        if d[i] > -45 and d[i] - np.median(d[i - 10:i]) >= 20:
            pic = d[i:i + 3].max()
            if d[i + 3:i + 8].max() <= pic - 15:
                out.append((i * 0.002, float(pic)))
                i += 8
                continue
        i += 1
    return out


def _poser(cl, env, r):
    for t, pk in cl:
        i0, i1 = int(t * SR) - int(0.002 * SR), int(t * SR) + int(0.008 * SR)
        seg = np.full(i1 - i0, 0.1)
        seg[:r] = np.linspace(1, 0.1, r)
        seg[-r:] = np.linspace(0.1, 1, r)
        env[i0:i1] = np.minimum(env[i0:i1], seg)


def declic(mix, voix, nom, log, passes=2, voix_seule=False):
    """Clics isolés de la voix atténués de 20 dB (la voix est retirée du mix sous l'enveloppe) ; mix = voix en voix seule."""
    env = np.ones(len(mix))
    r = int(0.001 * SR)
    cl = []
    for _ in range(passes):  # une salve longue peut laisser un reste qui ressort au second passage
        cl += clics_isoles((voix * env[:, None]).mean(axis=1))
        _poser(cl, env, r)
    for t, pk in sorted(cl):
        i0, i1 = int(t * SR) - int(0.002 * SR), int(t * SR) + int(0.008 * SR)
        reste = '' if voix_seule else f' ; reste du mix {db(mix[i0:i1] - voix[i0:i1]):.0f} dBFS'
        log.append(f'  {nom} : clic à {t:.3f} s ({pk:.0f} dBFS dans la voix{reste}) → −20 dB sur la voix')
    out = mix - voix * (1 - env)[:, None]
    apres = clics_isoles((voix * env[:, None]).mean(axis=1))
    log.append(f'  {nom} : {len(cl)} clic(s) atténué(s) ; il en reste {len(apres)} au contrôle')
    return out


def crete_par_echantillon(x, bloc=10 * SR, bord=64):
    """Crête vraie approchée de chaque échantillon : max |x| des quatre phases suréchantillonnées, deux canaux liés."""
    out = np.empty(len(x))
    for i0 in range(0, len(x), bloc):
        a, b = max(0, i0 - bord), min(len(x), i0 + bloc + bord)
        y = np.abs(resample_poly(x[a:b], 4, 1, axis=0)).max(axis=1).reshape(-1, 4).max(axis=1)
        out[i0:min(len(x), i0 + bloc)] = y[i0 - a:i0 - a + min(bloc, len(x) - i0)]
    return np.maximum(out, np.abs(x).max(axis=1))


def limiteur(x, plafond_db, anticipation=0.005, retour_db_s=25.0):
    """Réduction de gain en dB par échantillon : sous le plafond partout, anticipée en cosinus, retour linéaire en dB."""
    c = 10 ** (plafond_db / 20)
    r = np.minimum(1.0, c / np.maximum(crete_par_echantillon(x), 1e-12))
    h = int(anticipation * SR)
    m = minimum_filter1d(r, 2 * h + 1, mode='nearest')            # tenue ±h autour de chaque crête
    w = np.hanning(2 * h + 1)
    w /= w.sum()
    gs = np.minimum(np.convolve(np.pad(m, h, mode='edge'), w, mode='valid'), 1.0)   # lissage ±h : à chaque crête, gs ≤ r
    del m
    d = -20 * np.log10(np.minimum(gs, r.clip(None, 1)) + 1e-12)    # sécurité : jamais au-dessus de r
    del gs, r
    pente = retour_db_s / SR
    idx = np.arange(len(d))
    e = np.maximum.accumulate(d + pente * idx) - pente * idx       # retour linéaire en dB après chaque réduction
    return np.maximum(e, 0.0)


def _resume_ebur128(err):
    summ = err[err.rfind('Summary:'):]
    get = lambda k: float(re.search(k + r':\s+(-?[\d.]+|-inf)', summ).group(1))
    return get('I'), get('LRA'), get('Peak')


def ebur128(path):
    """(LUFS intégrés, LRA, crête vraie dBTP) d'un fichier, par le filtre ebur128 de FFmpeg."""
    err = subprocess.run([FF, '-hide_banner', '-nostats', '-i', path, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                         capture_output=True, text=True, encoding='utf-8', errors='replace', check=True).stderr
    return _resume_ebur128(err)


def mesurer(x):
    """Même mesure sur un signal en mémoire (stéréo, 48 kHz), passé par un tube : rien n'est écrit."""
    r = subprocess.run([FF, '-hide_banner', '-nostats', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', 'pipe:0',
                        '-af', 'ebur128=peak=true', '-f', 'null', '-'], input=np.ascontiguousarray(x, np.float32).tobytes(),
                       capture_output=True, check=True)
    return _resume_ebur128(r.stderr.decode('utf-8', 'replace'))


def write_wav(path, x, codec='pcm_s24le'):
    subprocess.run([FF, '-v', 'error', '-n', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', 'pipe:0', '-c:a', codec, path],
                   input=np.ascontiguousarray(x, np.float32).tobytes(), check=True)


def ecrire_journal(path, lignes):
    with open(path, 'x', encoding='utf-8') as f:
        f.writelines(l + '\n' for l in lignes)


def lieu(i, segs):
    """« seqN t s (film m:ss.ss) » pour l'échantillon i du film."""
    s = next(s for s in segs[::-1] if s['debut'] * SR // FPS <= i)
    return f'{s["id"]} {i / SR - s["debut"] / FPS:.2f} s (film {int(i / SR // 60)}:{i / SR % 60:05.2f})'


# --- Collage --------------------------------------------------------------------------------------------------------------

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description='Collage d\'un film de la chaîne (outils/montage/README.md du plugin).')
    ap.add_argument('config', nargs='?', help='montage.json (défaut : episodes/<ID>/montage/montage.json)')
    ap.add_argument('--episode', help='identifiant de l\'épisode, si CONFIG est omis')
    ap.add_argument('--voix-seule', action='store_true', help='son = voix seules des séquences et son des pièces de marque')
    ap.add_argument('--sans-limiteur', action='store_true')
    ap.add_argument('--son-seul', action='store_true', help='mesure le son et le limiteur, sans rien écrire')
    ap.add_argument('--nom', help='nom du MP4 de sortie (défaut : sortie.nom, ou sortie.nom_voix en voix seule)')
    ap.add_argument('--out', help='dossier de sortie (défaut : sortie.dossier)')
    a = ap.parse_args()
    if not a.config and not a.episode:
        ap.error('donner CONFIG.json ou --episode ID')
    cfg_path = os.path.abspath(a.config) if a.config else chemin(f'episodes/{a.episode}/montage/montage.json')
    c = charger_config(cfg_path)
    sortie = c['sortie']
    nom = a.nom or (sortie.get('nom_voix') or sortie['nom'][:-4] + '-voix.mp4' if a.voix_seule else sortie['nom'])
    out = os.path.join(os.path.abspath(a.out) if a.out else chemin(sortie['dossier']), nom)
    titre = c.get('titre', c['episode']) + (' — voix seule' if a.voix_seule else '')
    base = out[:-4]
    wav, logp, jsonp = base + ('.voix.wav' if a.voix_seule else '.mix.wav'), base + '.log.txt', base + '.journal.json'
    if not out.lower().endswith('.mp4'):
        sys.exit('Le nom de sortie doit finir par .mp4 : ' + out)
    if not a.son_seul:
        for p in (out, wav, logp, jsonp):
            if os.path.exists(p):
                sys.exit('Sortie existante, aucun écrasement : ' + p)
    plan, fondus = plan_segments(c)
    entrees = [(p['id'], p['fichier']) for p in plan if p['fichier']]
    for s in c['sequences']:
        entrees.append((s['id'] + ' voix', s['voix']))
        if not a.voix_seule:
            if not s['mix']:
                sys.exit(f'{s["id"]} : piste mixée non déclarée ; utiliser --voix-seule ou ajouter « mix » à la configuration')
            entrees.append((s['id'] + ' mix', s['mix']))
    for k, p in entrees:
        if not os.path.isfile(p):
            sys.exit(f'Entrée manquante ({k}) : {p}')

    # --- Segments (image et son de même durée, à l'image près)
    log = [f'Collage (outils/montage/assembler.py), mode {"voix seule" if a.voix_seule else "pistes mixées"} ; '
           f'configuration {rel(cfg_path)}']
    segs, t, prec = [], 0, None
    for p in plan:
        n = p['images'] if p['type'] == 'noir' else probe(p['fichier'])
        f = fondus.get((prec, p['id']), 0)
        t -= f
        segs.append(dict(p, images=n, fondu=f, debut=t))
        log.append(f'{p["id"]:5s} {t / FPS:7.2f} s → {(t + n) / FPS:7.2f} s ({n} images)'
                   + ('' if p['fichier'] is None else '  ' + rel(p['fichier']))
                   + (f'  ← fondu enchaîné de {f} images ({f / FPS:.2f} s)' if f else ''))
        t += n
        prec = p['id']
    total = t

    # --- Son : voix seules ou pistes mixées (voix déclinquée), son des MP4 de marque, noir muet
    log.append('Son :')
    blocs, est_seq = [], []
    for s in segs:
        n, f = s['images'], s['fondu']
        ns = n * SR // FPS
        if s['type'] == 'noir':
            x = np.zeros((ns, 2))
        elif s['type'] == 'sequence':
            voix = lire(s['seq']['voix'])
            if a.voix_seule:
                src = voix
                x = caler(declic(voix, voix, s['id'], log, voix_seule=True), ns)
            else:
                src = lire(s['seq']['mix'])
                m = min(len(src), len(voix))
                x = caler(declic(src[:m], voix[:m], s['id'], log), ns)
            if abs(len(src) - ns) > SR // FPS:
                log.append(f'  {s["id"]} : piste de {len(src) / SR:.3f} s pour {n / FPS:.3f} s d\'image (calée à l\'image)')
        else:
            x = caler(lire(s['fichier']), ns)
        if f:   # fondu enchaîné : la fin du segment précédent s'efface sous le début de celui-ci
            nf = f * SR // FPS
            a_fin = blocs[-1][-nf:]
            log.append(f'  fondu vers {s["id"]} : fin sortante à {db(a_fin):.0f} dBFS, effacée en {f / FPS:.2f} s')
            blocs[-1][-nf:] = a_fin * (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, nf)))[:, None] + x[:nf]
            x = x[nf:]
        blocs.append(x)
        est_seq.append(np.full(len(x), s['type'] == 'sequence'))
    mix = np.vstack(blocs)
    del blocs
    sq = np.concatenate(est_seq)
    I0, _, tp0 = mesurer(mix[sq])
    log.append(f'Séquences assemblées (sans la marque) : {I0:.1f} LUFS, crête vraie {tp0:.1f} dBTP')

    def journal_limiteur(red, g):
        act = red > 0.1
        bords = np.flatnonzero(np.diff(np.concatenate([[0], act.astype(np.int8), [0]])))
        zones = list(zip(bords[::2], bords[1::2]))
        pires = sorted(zones, key=lambda z: -red[z[0]:z[1]].max())[:6]
        log.append(f'Limiteur : gain {g:+.2f} dB sur les séquences, plafond {PLAFOND_WAV} dBTP ; {len(zones)} réductions de plus de '
                   f'0,1 dB, maximum {red.max():.1f} dB ; temps sous réduction > 0,5 dB : {(red > 0.5).sum() / SR:.1f} s, '
                   f'> 2 dB : {(red > 2).sum() / SR:.2f} s, sur {sq.sum() / SR:.0f} s de séquences')
        for z0, z1 in pires:
            log.append(f'  {red[z0:z1].max():.1f} dB à {lieu(z0 + int(np.argmax(red[z0:z1])), segs)}')

    # --- Niveau
    if a.voix_seule:
        # aucun gain : la voix garde le niveau de ses pistes pour le mix du film ; limiteur seulement au-delà du plafond
        Ia, _, tpa = mesurer(mix)
        if tpa > PLAFOND_WAV and not a.sans_limiteur:
            red = limiteur(mix, PLAFOND_WAV)
            mix = mix * (10 ** (-red / 20))[:, None]
            journal_limiteur(red, 0.0)
        else:
            log.append(f'Voix seule : aucun gain ; crête vraie {tpa:.1f} dBTP, limiteur inutile')
    elif a.sans_limiteur:
        g = min(TARGET_I - I0, PLAFOND_WAV - tp0)
        mix = mix * (1 + np.where(sq, 10 ** (g / 20) - 1, 0.0))[:, None]
        log.append(f'Sans limiteur : gain unique {g:+.2f} dB sur les séquences (plafonné par la crête vraie)')
    else:
        g = TARGET_I - I0
        for passe in range(3):            # la limitation retire un peu d'intensité : on recale le gain (deux passes suffisent)
            y = mix * (1 + np.where(sq, 10 ** (g / 20) - 1, 0.0))[:, None]
            red = limiteur(y, PLAFOND_WAV)
            y *= (10 ** (-red / 20))[:, None]
            I1, _, _ = mesurer(y[sq])
            if abs(I1 - TARGET_I) < 0.1 or passe == 2:
                break
            g += TARGET_I - I1
            del y
        mix = y
        journal_limiteur(red, g)
    if a.son_seul:
        I2, lra2, tp2 = mesurer(mix)
        log.append(f'Essai son seul (rien n\'est écrit) : {I2:.1f} LUFS, crête vraie {tp2:.1f} dBTP, LRA {lra2:.1f} LU')
        print('\n'.join(log))
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    write_wav(wav, mix)
    del mix
    I2, lra2, tp2 = ebur128(wav)
    log.append(f'Son du film (WAV{", voix seule" if a.voix_seule else ""}) : {I2:.1f} LUFS, crête vraie {tp2:.1f} dBTP, LRA {lra2:.1f} LU')

    # --- Image : segments enchaînés deux à deux (coupe franche ou fondu enchaîné), noir généré, multiplexage
    args, fc, idx, cur, cur_n = [FF, '-v', 'error', '-n'], [], 0, None, 0
    for j, s in enumerate(segs):
        n, f, lab = s['images'], s['fondu'], f'[s{j}]'
        if s['fichier'] is None:
            fc.append(f'color=c=black:s={W}x{H}:r={FPS}:d={n / FPS},format=yuv420p,setsar=1,{BT709},settb=1/{FPS}{lab}')
        else:
            args += ['-i', s['fichier']]
            fc.append(f'[{idx}:v]trim=end_frame={n},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p,setsar=1,{BT709},settb=1/{FPS}{lab}')
            idx += 1
        if cur is None:
            cur, cur_n = lab, n
            continue
        if f:
            fc.append(f'{cur}{lab}xfade=transition=fade:duration={f / FPS:.6f}:offset={(cur_n - f) / FPS:.6f}[c{j}]')
        else:
            fc.append(f'{cur}{lab}concat=n=2:v=1:a=0,settb=1/{FPS}[c{j}]')
        cur, cur_n = f'[c{j}]', cur_n + n - f
    fc.append(f'{cur}{BT709}[v]')
    args += ['-i', wav, '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', f'{idx}:a',
             '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(FPS),
             '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
             '-c:a', 'aac', '-b:a', '320k', '-ar', str(SR), '-movflags', '+faststart',
             '-metadata', 'title=' + titre, out]
    subprocess.run(args, check=True)

    # --- Contrôles du MP4 livré
    subprocess.run([FF, '-v', 'error', '-xerror', '-i', out, '-f', 'null', '-'], check=True)
    n_out = probe(out)
    I3, lra3, tp3 = ebur128(out)
    log.append(f'MP4 : {n_out} images ({n_out / FPS:.2f} s ; attendu {total} images) ; {I3:.1f} LUFS intégré, '
               f'crête vraie {tp3:.1f} dBTP, LRA {lra3:.1f} LU ; décodage complet sans erreur')
    ecarts = [x for x, bad in (('nombre d\'images', n_out != total),
                               ('intensité hors −16 ±1 LUFS', not (a.sans_limiteur or a.voix_seule) and abs(I3 - TARGET_I) > 1),
                               ('crête vraie > −1,5 dBTP', tp3 > MAX_TP)) if bad]
    log.append('Contrôles du MP4 : ' + ('OK' if not ecarts else 'ÉCART : ' + ', '.join(ecarts))
               + (' (voix seule : intensité relevée, non contrôlée)' if a.voix_seule else ''))
    ecrire_journal(logp, log)
    with open(jsonp, 'x', encoding='utf-8') as fj:
        json.dump({'episode': c['episode'], 'titre': titre, 'mode': 'voix-seule' if a.voix_seule else 'pistes-mixees',
                   'configuration': rel(cfg_path), 'fps': FPS, 'sr': SR, 'images': total, 'son': rel(wav),
                   'segments': [{'id': s['id'], 'type': s['type'], 'debut_image': s['debut'], 'images': s['images'],
                                 'fondu_images': s['fondu'], 'fichier': rel(s['fichier']) if s['fichier'] else None}
                                for s in segs]}, fj, ensure_ascii=False, indent=1)
    print('\n'.join(log))


if __name__ == '__main__':
    main()
