"""Contrôles techniques des vidéos de la chaîne — 15/10/2026.

Une seule commande, plusieurs contrôles. Aucun contrôle ne modifie un fichier existant ; les sorties (planches,
images extraites) vont dans un dossier qui ne doit pas déjà les contenir. Les mesures ne valent jamais une écoute
ni un visionnage (statuts du CLAUDE.md racine de la chaîne).

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py niveau      FILM.mp4
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py planche     FILM.mp4 --sortie DOSSIER [--pas 2] [--colonnes 5]
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py vibration   FILM.mp4 --zone L:H:X:Y [--debut S] [--duree S] [--extraire T]
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py tremblement FILM.mp4 [--debut S] [--duree S] [--brut F.npz | --depuis F.npz]
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py son         FILM.mp4 [--reference PISTE_MIXEE.wav] [--voix PISTE_VOIX.wav]
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py couleurs    index.html [autres fichiers…]
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py doublons    DOSSIER_SEQ1 DOSSIER_SEQ2 …
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py licences    DOSSIER [autres dossiers…]
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py voix-reste  VOIX.wav RESTE.wav
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py chrome
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py tout        FILM.mp4 --projet DOSSIER_DU_PROJET

Code de sortie : 0 si rien n'est signalé, 1 si un contrôle signale un écart, 2 en cas d'erreur d'usage.
Références : ${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md (§ 2 ter, porte B),
${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md (§ 3, § 5), marque/README.md de la chaîne (couleurs des films) ;
écarts de la chaîne : direction/ECARTS.md. Mode d'emploi : ${CLAUDE_PLUGIN_ROOT}/outils/controle/README.md.
"""
import argparse, glob, hashlib, json, os, re, shutil, subprocess, sys
import numpy as np

FF_DEFAUT = next(iter(sorted(glob.glob(os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'WinGet', 'Packages', 'Gyan.FFmpeg*', '*', 'bin')))), '')  # FFmpeg de WinGet s'il existe ; aucun chemin propre à une machine
FF = os.environ.get('HYPERFRAMES_FFMPEG_PATH') or shutil.which('ffmpeg') or os.path.join(FF_DEFAUT, 'ffmpeg.exe')
FP = os.environ.get('HYPERFRAMES_FFPROBE_PATH') or shutil.which('ffprobe') or os.path.join(FF_DEFAUT, 'ffprobe.exe')
SR = 48000

# Cibles (DIRECTION_AUDIO.md § 3) et couleurs retirées des films : celles de la chaîne, dans marque/couleurs_interdites.json
# ({"corail": "#F17462", …}) ; sans ce fichier, aucune couleur n'est interdite.
CIBLE_LUFS, TOLERANCE_LUFS, MAX_TP = -16.0, 1.0, -1.5
FICHIER_COULEURS = os.path.join(os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd(), 'marque', 'couleurs_interdites.json')


def couleurs_interdites():
    if not os.path.isfile(FICHIER_COULEURS):
        return {}
    motifs = {}
    for nom, hexa in json.load(open(FICHIER_COULEURS, encoding='utf-8')).items():
        h = hexa.lstrip('#').lower()
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        motifs[f'{nom} #{h.upper()}'] = [rf'#{h}\b', rf'rgba?\(\s*{r}\s*,\s*{g}\s*,\s*{b}\b']
    return motifs


COULEURS_INTERDITES = couleurs_interdites()
LICENCES_EN_ATTENTE = [r'BY-SA', r'PD-AR', r'PD-Brazil', r'BY 2\.0 BR', r'domaine public argentin']
IMAGES = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, **kw)


def ebur128(path):
    err = run([FF, '-hide_banner', '-nostats', '-i', path, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'],
              text=True, encoding='utf-8', errors='replace').stderr
    summ = err[err.rfind('Summary:'):]
    if not summ:
        sys.exit('Mesure impossible (pas de piste son ?) : ' + path)
    get = lambda k: float(re.search(k + r':\s+(-?[\d.]+|-inf)', summ).group(1))
    return get('I'), get('LRA'), get('Peak')


def duree(path):
    out = run([FP, '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], text=True).stdout.strip()
    return float(out) if out else 0.0


# ---------------------------------------------------------------- niveau
def c_niveau(a):
    I, lra, tp = ebur128(a.film)
    ok_i = abs(I - CIBLE_LUFS) <= TOLERANCE_LUFS
    ok_tp = tp <= MAX_TP
    print(f'Niveau : {I:.1f} LUFS intégré (cible {CIBLE_LUFS:.0f} ±{TOLERANCE_LUFS:.0f}) · crête vraie {tp:.1f} dBTP '
          f'(≤ {MAX_TP}) · LRA {lra:.1f} LU · durée {duree(a.film):.2f} s')
    print('  ' + ('OK' if ok_i and ok_tp else 'ÉCART : ' + ', '.join(
        x for x, ok in (('intensité hors plage', ok_i), ('crête vraie trop haute', ok_tp)) if not ok)))
    return 0 if ok_i and ok_tp else 1


# ---------------------------------------------------------------- planche
def c_planche(a):
    os.makedirs(a.sortie, exist_ok=True)
    base = os.path.join(a.sortie, os.path.splitext(os.path.basename(a.film))[0] + '-planche')
    if glob.glob(base + '-*.jpg'):
        sys.exit('Des planches existent déjà avec ce nom, aucun écrasement : ' + base + '-*.jpg')
    d = duree(a.film)
    par_planche = a.colonnes * a.colonnes
    n = max(1, int(np.ceil(d / a.pas / par_planche)))
    font = 'C\\:/Windows/Fonts/arial.ttf'
    # Échantillonnage par numéro d'image (et non par le filtre fps, qui décale l'image d'environ une demi-période
    # par rapport à son étiquette : constaté le 15/10/2026). L'étiquette affiche le temps réel de l'image montrée.
    num, den = (int(v) for v in run([FP, '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate',
                                     '-of', 'csv=p=0', a.film], text=True).stdout.strip().split('/'))
    pas_images = max(1, round(a.pas * num / den))
    vf = (f"select='not(mod(n\\,{pas_images}))',scale=480:-1,drawtext=fontfile='{font}':text='%{{pts\\:hms}}':x=6:y=6:"
          f"fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6,tile={a.colonnes}x{a.colonnes}")
    r = run([FF, '-v', 'error', '-n', '-i', a.film, '-vf', vf, '-fps_mode', 'passthrough', '-frames:v', str(n), base + '-%d.jpg'])
    if r.returncode:
        sys.exit(r.stderr.decode(errors='replace'))
    print(f'Planche : {n} fichier(s) {base}-1.jpg…, une image toutes les {a.pas} s ({d:.1f} s de film).')
    print('  À relire contre le contrat de plan : tenue ≤ 2,5 s sans mouvement, photos non répétées, couleurs, lisibilité.')
    return 0


# ---------------------------------------------------------------- vibration
def c_vibration(a):
    w, h, x, y = (int(v) for v in a.zone.split(':'))
    pre = ['-ss', str(a.debut)] if a.debut else []
    dur = ['-t', str(a.duree)] if a.duree else []
    vf = (f'crop={w}:{h}:{x}:{y},scale=iw/4:ih/4,gblur=sigma=2,tblend=all_mode=difference,signalstats,'
          f'metadata=print:key=lavfi.signalstats.YAVG:file=-')
    out = run([FF, '-v', 'error'] + pre + dur + ['-i', a.film, '-vf', vf, '-f', 'null', '-'],
              text=True, encoding='utf-8', errors='replace').stdout
    t = [float(v) for v in re.findall(r'pts_time:([\d.]+)', out)]
    d = np.array([float(v) for v in re.findall(r'YAVG=([\d.]+)', out)])
    if not d.size:
        sys.exit('Aucune mesure : zone hors cadre ou film illisible.')
    t = (np.array(t[:len(d)]) + (a.debut or 0)) if t else np.arange(len(d)) / 30 + (a.debut or 0)
    # Une vibration se lit comme une alternance : la différence monte et descend d'une image à l'autre.
    dd = np.diff(d)
    alt = (dd[:-1] * dd[1:] < 0) & (np.abs(dd[:-1]) > 0.5) & (np.abs(dd[1:]) > 0.5)
    taux = alt.mean() if alt.size else 0.0
    print(f'Vibration, zone {a.zone} : {len(d)} images · différence moyenne {d.mean():.2f} · p95 {np.percentile(d, 95):.2f} · '
          f'max {d.max():.2f} · alternances nettes {taux * 100:.0f} %')
    pics = np.argsort(d)[-8:][::-1]
    print('  Plus fortes différences (coupes, mouvements ou vibration, à vérifier) : ' +
          ', '.join(f'{t[i]:.2f} s ({d[i]:.1f})' for i in pics))
    print("  Repères : le grain et la brume (exemple AA : épisode 001) empêchent un zéro parfait (≈ 1,5–2 mesuré sur E003 d'AA). "
          "Une vibration donne une alternance régulière sur une zone qui devrait être immobile ; confirmer à l'œil.")
    if a.extraire is not None:
        dossier = os.path.splitext(a.film)[0] + f'-images-{a.extraire:.2f}s'
        if os.path.exists(dossier):
            sys.exit('Dossier déjà présent, aucun écrasement : ' + dossier)
        os.makedirs(dossier)
        run([FF, '-v', 'error', '-ss', str(a.extraire), '-i', a.film, '-frames:v', '10', os.path.join(dossier, 'image-%02d.png')])
        print(f'  10 images consécutives en pleine taille : {dossier}')
    return 1 if taux > 0.3 else 0


# ---------------------------------------------------------------- tremblement (16/10/2026)
# Pourquoi : « vibration » compare la luminance moyenne d'une zone après réduction ×4 et flou. Un tremblement d'un
# pixel (0, 1, 0, 1…) y donne la même différence à chaque image, donc aucune « alternance » : éprouvé le 16/10/2026
# sur une vidéo de test aux défauts connus, où il ne voyait ni le tremblement d'un pixel ni celui d'un demi-pixel.
# « tremblement » mesure le DÉPLACEMENT réel de l'image, image par image, par corrélation croisée sous-pixel sur une
# grille de 28 tuiles de 256 px, sans avoir à choisir une zone immobile. Un mouvement régulier (dérive, travelling,
# ralenti) varie lentement ; un tremblement (aller-retour) ou un mouvement par marches d'un pixel (arrondi pendant
# une dérive lente) s'écarte de ses images voisines. Calibrage sur la vidéo de test : image fixe 0,006 px,
# travelling sous-pixel 0,04 px ; tremblement d'1 px 0,89 px, de 0,5 px 0,44 px, marches de 0,3 px/image 0,33 px.
def _tuiles(im, xs, ys, T, win):
    t = np.stack([im[y:y + T, x:x + T] for y in ys for x in xs]).astype(np.float64)
    t -= t.mean(axis=(1, 2), keepdims=True)
    tex = t.std(axis=(1, 2))
    t *= win
    return np.fft.rfft2(t), np.sqrt((t ** 2).sum(axis=(1, 2))), tex


def _deplacements(A, B, T):
    (F1, n1, s1), (F2, n2, s2) = A, B
    r = np.fft.irfft2(F1 * np.conj(F2), s=(T, T))
    k = r.shape[0]
    flat = r.reshape(k, -1).argmax(axis=1)
    iy, ix = np.unravel_index(flat, (T, T))
    q = np.arange(k)
    c = r[q, iy, ix]

    def fin(m, p):
        d = m - 2 * c + p
        return np.where(np.abs(d) < 1e-12, 0.0, 0.5 * (m - p) / np.where(np.abs(d) < 1e-12, 1, d))
    dy = iy + fin(r[q, (iy - 1) % T, ix], r[q, (iy + 1) % T, ix])
    dx = ix + fin(r[q, iy, (ix - 1) % T], r[q, iy, (ix + 1) % T])
    dy = np.where(dy > T / 2, dy - T, dy)
    dx = np.where(dx > T / 2, dx - T, dx)
    pic = c / (n1 * n2 + 1e-9)
    ok = (pic > 0.6) & (np.minimum(s1, s2) > 4) & (np.abs(dx) < 24) & (np.abs(dy) < 24)
    return np.where(ok, dx, np.nan), np.where(ok, dy, np.nan)


def _mesurer_tremblement(a):
    W, H, T = 1920, 1080, 256
    xs = [int(v) for v in np.linspace(48, W - T - 48, 7)]
    ys = [int(v) for v in np.linspace(32, H - T - 32, 4)]
    w1 = np.hanning(T)
    win = np.outer(w1, w1)
    fps = float(eval(run([FP, '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate',
                          '-of', 'csv=p=0', a.film], text=True).stdout.strip() or '30'))
    pre = ['-ss', str(a.debut)] if a.debut else []
    dur = ['-t', str(a.duree)] if a.duree else []
    proc = subprocess.Popen([FF, '-v', 'error'] + pre + dur + ['-i', a.film, '-vf', f'scale={W}:{H},format=gray',
                             '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    prec, DX, DY = None, [], []
    while True:
        raw = proc.stdout.read(W * H)
        if len(raw) < W * H:
            break
        cur = _tuiles(np.frombuffer(raw, np.uint8).reshape(H, W), xs, ys, T, win)
        if prec is not None:
            dx, dy = _deplacements(prec, cur, T)
            DX.append(dx); DY.append(dy)
        prec = cur
    proc.wait()
    if not DX:
        sys.exit('Aucune mesure : film illisible.')
    D = np.stack([np.array(DX), np.array(DY)], axis=2)   # (images-1) × tuiles × 2, en px du film
    if a.brut:
        if os.path.exists(a.brut):
            sys.exit('Fichier de mesures déjà présent, aucun écrasement : ' + a.brut)
        np.savez(a.brut, D=D, fps=fps, debut=a.debut or 0, xs=xs, ys=ys)
    return D, fps, a.debut or 0, xs, ys, T


def c_tremblement(a):
    if a.depuis:
        z = np.load(a.depuis)
        D, fps, t0, xs, ys, T = z['D'], float(z['fps']), float(z['debut']), list(z['xs']), list(z['ys']), 256
    else:
        D, fps, t0, xs, ys, T = _mesurer_tremblement(a)
    n_im, n_t = D.shape[0], D.shape[1]
    # Signature, par tuile, par axe et par seconde (calibrée le 16/10/2026 : séquences 4 et 5 de l'épisode 004 et
    # vidéo de test ; un critère d'amplitude seul signalait 40 à 70 s par film, rendus corrigés compris) :
    #  - MARCHES (arrondi au pixel pendant une dérive lente) : déplacements quantifiés à {0, ±1 px} sur au moins 90 %
    #    des images, au moins 2 pas de 1 px de même signe, au moins 40 % d'images immobiles ;
    #  - ALLERS-RETOURS : au moins 60 % des paires d'images consécutives de signes opposés, chacune > seuil, qui
    #    s'annulent à 30 % près.
    # Le grain qui change à chaque image et les couches de 2,5D qui se croisent dans une tuile donnent des valeurs
    # quelconques : ils ne passent pas ces deux filtres.
    w = int(round(fps))
    retenues = {}
    for s0 in range(0, n_im - w + 1, w):
        sec = int(t0 + (s0 + 1) / fps)
        for k in range(n_t):
            for ax in (0, 1):
                v = D[s0:s0 + w, k, ax]
                v = v[np.isfinite(v)]
                if len(v) < 0.8 * w:
                    continue
                av = np.abs(v)
                zero, un = av < 0.15, np.abs(av - 1) < 0.2
                genre = None
                if (zero | un).mean() >= 0.9 and un.sum() >= 2 and zero.mean() >= 0.4 and len(set(np.sign(v[un]))) == 1:
                    genre = 'marches'
                else:
                    p1, p2 = v[:-1], v[1:]
                    alt = (p1 * p2 < 0) & (np.abs(p1) > a.seuil) & (np.abs(p2) > a.seuil) & \
                          (np.abs(p1 + p2) < 0.3 * np.maximum(np.abs(p1), np.abs(p2)))
                    if alt.mean() >= 0.6:
                        genre = 'allers-retours'
                if genre:
                    retenues.setdefault(sec, set()).add((k, genre))
    valides = np.isfinite(D[..., 0]).mean() * 100
    print(f'Tremblement : {n_im + 1} images à {fps:g} i/s · {n_t} tuiles de {T} px · {valides:.0f} % des mesures utilisables '
          f'(tuiles texturées, sans coupe ni fondu complet)')
    if not retenues:
        print('  Aucune marche d\'un pixel ni aller-retour : OK (une mesure ne vaut pas un visionnage).')
        return 0
    print(f'  ÉCART : {len(retenues)} seconde(s) où une zone avance par crans d\'un pixel ou fait des allers-retours :')
    for s in sorted(retenues):
        ev = sorted(retenues[s])
        genres = sorted({g for _, g in ev})
        zones = ', '.join(f'x{xs[k % len(xs)]}-y{ys[k // len(xs)]}' for k in sorted({k for k, _ in ev})[:5])
        print(f'    {s:4d}–{s + 1} s : {len({k for k, _ in ev})} tuile(s), {" et ".join(genres)} · zones (coin haut gauche, '
              f'tuile de {T} px) {zones}' + (' …' if len({k for k, _ in ev}) > 5 else ''))
    print('  À vérifier à l\'œil sur dix images consécutives en pleine taille (vibration --extraire T) : un cran d\'un pixel '
          'se voit sur un texte ou une photo nette, presque pas sur un fond flou.')
    return 1


# ---------------------------------------------------------------- son (16/10/2026)
# Bugs de son : trous (coupures brèves), écrêtage, clics isolés (bruits de bouche d'une prise, coupe sans fondu),
# et, avec --reference (la piste mixée placée dans la composition), les passages où le MP4 s'écarte de cette piste
# (double lecture, coupure, saut, artefact du rendu). Calibré le 16/10/2026 sur les séquences 2, 3 et 5 de
# l'épisode 004 : le MP4 suit sa piste mixée à ~35 dB près ; les seuls écarts venaient de clics déjà présents
# dans la voix, que l'AAC étale sur 5 à 10 ms.
def _stereo(path):
    x = np.frombuffer(run([FF, '-v', 'error', '-i', path, '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-']).stdout,
                      np.float32).astype(np.float64)
    return x.reshape(-1, 2)


def _clics_isoles(mono):
    """Salve de 6 ms au plus qui sort d'au moins 20 dB du silence des 20 ms précédentes et y retombe d'au moins
    15 dB dans les 10 ms suivantes. Une consonne explosive (p, t, k) est suivie d'une voyelle : elle n'y retombe pas."""
    k = int(0.002 * SR)
    m = len(mono) // k
    db = 20 * np.log10(np.sqrt((mono[:m * k].reshape(m, k) ** 2).mean(axis=1)) + 1e-9)
    out, i = [], 10
    while i < m - 10:
        if db[i] > -45 and db[i] - np.median(db[i - 10:i]) >= 20:
            pic = db[i:i + 3].max()
            if db[i + 3:i + 8].max() <= pic - 15:
                out.append((i * 0.002, float(pic)))
                i += 8
                continue
        i += 1
    return out


def c_son(a):
    x = _stereo(a.film)
    d = len(x) / SR
    mono = x.mean(axis=1)
    n10 = int(0.01 * SR)
    m = len(mono) // n10
    db = 20 * np.log10(np.sqrt(np.mean(mono[:m * n10].reshape(m, n10) ** 2, axis=1)) + 1e-9)
    # trous : une à quinze trames de 10 ms sous −60 dB, entourées de son à plus de −35 dB
    trous, i = [], 0
    while i < m:
        if db[i] < -60:
            j = i
            while j < m and db[j] < -60:
                j += 1
            if 1 <= j - i <= 15 and i >= 10 and j + 10 <= m and db[i - 10:i].mean() > -35 and db[j:j + 10].mean() > -35:
                trous.append((i * 0.01, (j - i) * 10))
            i = j
        else:
            i += 1
    ecretage = int((np.abs(x) >= 0.999).sum())
    source = a.voix or a.reference or a.film
    clics = _clics_isoles(_stereo(source).mean(axis=1) if source != a.film else mono)
    print(f'Son : {d:.2f} s · {len(trous)} trou(s) · {ecretage} échantillon(s) écrêté(s) · {len(clics)} clic(s) isolé(s) '
          f'dans {os.path.basename(source)}')
    code = 1 if (trous or ecretage or clics) else 0
    if trous:
        print('  Trous : ' + ', '.join(f'{t:.2f} s ({ms} ms)' for t, ms in trous[:30]))
    if clics:
        print('  Clics isolés (bruit de bouche ou coupe sans fondu, à écouter puis atténuer) : ' +
              ', '.join(f'{t:.2f} s ({pk:.0f} dBFS)' for t, pk in clics[:40]))
    if not a.voix and not a.reference:
        print('  Sans --voix, la musique masque une partie des clics de la voix : passer la piste voix séparée.')
    if not a.reference:
        # sauts : écart de plus de 12 dB entre deux tranches de 100 ms (les syllabes en font aussi : à écouter)
        n100 = int(0.1 * SR)
        k = len(mono) // n100
        db100 = 20 * np.log10(np.sqrt(np.mean(mono[:k * n100].reshape(k, n100) ** 2, axis=1)) + 1e-9)
        sauts = [i * 0.1 for i in range(1, k) if abs(db100[i] - db100[i - 1]) > 12 and min(db100[i], db100[i - 1]) > -50]
        print(f'  {len(sauts)} saut(s) de niveau > 12 dB entre tranches de 100 ms (syllabes comprises) ; '
              'avec --reference, seuls comptent les écarts à la piste mixée.')
    else:
        r = _stereo(a.reference)
        rm, fm = r.mean(axis=1), mono
        # alignement par corrélation sur les 20 premières secondes (décalage de ±0,5 s au plus)
        L = min(len(rm), len(fm), int(20 * SR))
        lag_max = int(0.5 * SR)
        A = np.fft.rfft(fm[:L], 2 * L); B = np.fft.rfft(rm[:L], 2 * L)
        cc = np.fft.irfft(A * np.conj(B))
        cc = np.concatenate([cc[-lag_max:], cc[:lag_max + 1]])
        lag = int(np.argmax(cc)) - lag_max
        f2, r2 = (fm[lag:], rm) if lag >= 0 else (fm, rm[-lag:])
        n = min(len(f2), len(r2))
        f2, r2 = f2[:n], r2[:n]
        g = np.dot(f2, r2) / (np.dot(r2, r2) + 1e-12)
        res = f2 - g * r2
        n50 = int(0.05 * SR)
        q = n // n50
        er = np.sqrt(np.mean(r2[:q * n50].reshape(q, n50) ** 2, axis=1)) * abs(g) + 1e-9
        ee = np.sqrt(np.mean(res[:q * n50].reshape(q, n50) ** 2, axis=1)) + 1e-9
        snr = 20 * np.log10(er / ee)
        actif = 20 * np.log10(er) > -50
        plages = []
        for i in np.where(actif & (snr < 12))[0]:
            if plages and i - plages[-1][1] <= 2:
                plages[-1][1] = i
            else:
                plages.append([i, i])
        # un écart autour d'une attaque très brusque de la piste mixée vient de l'AAC (pré-écho), pas du rendu
        dr = np.abs(np.diff(r2))
        aac, rendu = [], []
        for p0, p1 in plages:
            s0, s1 = p0 * n50, (p1 + 1) * n50
            loc = dr[max(s0 - n50, 0):s1 + n50]
            (aac if loc.size and loc.max() > 20 * np.median(loc) + 1e-6 else rendu).append((p0, p1))
        fmt = lambda P: ', '.join(f'{(p0 * n50 + max(lag, 0)) / SR:.2f}–{((p1 + 1) * n50 + max(lag, 0)) / SR:.2f} s'
                                  for p0, p1 in P[:30])
        print(f'  Contre la piste mixée : décalage {lag / SR * 1000:+.1f} ms · gain {20 * np.log10(abs(g) + 1e-12):+.2f} dB '
              f'(≈ +6 dB = double lecture) · fidélité médiane {np.median(snr[actif]):.1f} dB · '
              f'{len(rendu)} écart(s) créé(s) au rendu · {len(aac)} attaque(s) de la piste étalée(s) par l\'AAC')
        if rendu:
            print('    Écarts du rendu (à écouter) : ' + fmt(rendu))
            code = 1
        if aac:
            print('    Attaques de la piste mixée (déjà dans la piste ; voir les clics isolés) : ' + fmt(aac))
    print('  Une mesure ne vaut pas une écoute.')
    return code


# ---------------------------------------------------------------- couleurs
def c_couleurs(a):
    trouve = 0
    for f in a.fichiers:
        for n, line in enumerate(open(f, encoding='utf-8', errors='replace'), 1):
            for nom, motifs in COULEURS_INTERDITES.items():
                if any(re.search(m, line, re.I) for m in motifs):
                    trouve += 1
                    print(f'{f}:{n} : {nom} → {line.strip()[:140]}')
    if not COULEURS_INTERDITES:
        print(f'Aucune couleur interdite déclarée ({FICHIER_COULEURS} absent ou vide).')
    print(f'Couleurs retirées des films : {trouve} occurrence(s).' + (' OK' if not trouve else
          ' À corriger, sauf la signature et l\'outro, qui gardent les couleurs de marque.'))
    return 1 if trouve else 0


# ---------------------------------------------------------------- doublons
def ahash(path):
    raw = run([FF, '-v', 'error', '-i', path, '-vf', 'scale=9:8:flags=area,format=gray', '-frames:v', '1',
               '-f', 'rawvideo', '-']).stdout
    if len(raw) < 72:
        return None
    g = np.frombuffer(raw[:72], np.uint8).reshape(8, 9).astype(int)
    return (g[:, 1:] > g[:, :-1]).flatten()  # dHash : robuste au redimensionnement et à la recompression


def projet_de(path, racines):
    """Nom lisible et unique du dossier racine qui contient le fichier (« sequence2-moquerie-v2/media » plutôt que « media »)."""
    for r in racines:
        rr = os.path.abspath(r)
        if os.path.abspath(path).startswith(rr + os.sep):
            parties = os.path.normpath(rr).split(os.sep)
            return '/'.join(parties[-2:]) if parties[-1].lower() in ('media', 'photos', 'images', 'assets') else parties[-1]
    return '?'


MATIERES = ('matieres', 'fonts', 'logo', 'grain', 'fog', 'paper')  # fonds et marque : reviennent par nature


def utilisee(f, racines):
    """La photo est-elle citée dans une composition (.html) du projet ? Présente dans media/ ne veut pas dire utilisée."""
    for r in racines:
        rr = os.path.abspath(r)
        if os.path.abspath(f).startswith(rr + os.sep):
            projet = os.path.dirname(rr) if os.path.basename(rr).lower() in ('media', 'photos', 'images') else rr
            nom = os.path.basename(f)
            return any(nom in open(h, encoding='utf-8', errors='replace').read()
                       for h in glob.glob(os.path.join(projet, '**', '*.html'), recursive=True))
    return True


def c_doublons(a):
    fichiers = [f for r in a.dossiers for f in glob.glob(os.path.join(r, '**', '*'), recursive=True)
                if f.lower().endswith(IMAGES) and os.path.isfile(f)
                and not any(m in os.path.relpath(f, r).lower() for m in MATIERES)]
    data = []
    for f in fichiers:
        if not utilisee(f, a.dossiers):
            continue  # copiée mais absente des compositions
        h = hashlib.sha1(open(f, 'rb').read()).hexdigest()
        data.append((f, projet_de(f, a.dossiers), h, ahash(f)))
    signale = 0
    vus = set()
    for i, (f1, p1, h1, a1) in enumerate(data):
        groupe = [(f1, p1, 'identique')]
        for f2, p2, h2, a2 in data[i + 1:]:
            if f2 in vus or p2 == p1:
                continue
            if h2 == h1:
                groupe.append((f2, p2, 'identique'))
            elif a1 is not None and a2 is not None and int((a1 != a2).sum()) <= a.seuil:
                groupe.append((f2, p2, 'même photo, autre taille'))
        if len(groupe) > 1:
            signale += 1
            vus.update(g[0] for g in groupe)
            print('Même photo dans plusieurs séquences :')
            for f, p, k in groupe:
                print(f'  [{p}] {os.path.relpath(f)} ({k})')
    print(f'{len(fichiers)} images examinées dans {len(a.dossiers)} dossiers · {signale} photo(s) répétée(s).' +
          (' OK' if not signale else ' Chaque répétition doit être un rappel voulu, consigné dans le README.'))
    print('  Les fonds (papier, brume, grain) et le logo reviennent par nature : ne regarder que les photos.')
    return 1 if signale else 0


# ---------------------------------------------------------------- licences
def c_licences(a):
    prov = [f for r in a.dossiers for f in glob.glob(os.path.join(r, '**', 'PROVENANCE.md'), recursive=True)]
    trouve = 0
    for f in prov:
        for n, line in enumerate(open(f, encoding='utf-8', errors='replace'), 1):
            if any(re.search(m, line, re.I) for m in LICENCES_EN_ATTENTE):
                trouve += 1
                print(f'{os.path.relpath(f)}:{n} : {line.strip()[:160]}')
    print(f'{len(prov)} PROVENANCE.md lus · {trouve} ligne(s) citant une licence en attente de décision '
          '(CC BY-SA, domaine public argentin ou brésilien, CC BY 2.0 BR).')
    print("  Une ligne qui dit « exclu » ou « non utilisé » est normale ; un média réellement utilisé sous ces licences ne l'est pas.")
    return 1 if trouve else 0


# ---------------------------------------------------------------- voix / reste
def load(path):
    x = np.frombuffer(run([FF, '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']).stdout,
                      np.float32).astype(np.float64)
    return x


def bande_1_4k(x):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < 1000) | (f > 4000)] = 0
    return np.fft.irfft(X, len(x))


def c_voix_reste(a):
    v, r = load(a.voix), load(a.reste)
    n = min(len(v), len(r))
    vb, rb = bande_1_4k(v[:n]), bande_1_4k(r[:n])
    w = int(0.4 * SR)
    res = []
    for i in range(0, n - w, w):
        ve = np.sqrt(np.mean(vb[i:i + w] ** 2)) + 1e-12
        if 20 * np.log10(ve) < -45:
            continue  # pas de voix dans cette fenêtre
        res.append((i / SR, 20 * np.log10(ve / (np.sqrt(np.mean(rb[i:i + w] ** 2)) + 1e-12))))
    if not res:
        sys.exit('Aucune fenêtre avec voix : vérifier les fichiers.')
    vals = np.array([d for _, d in res])
    bas = [(t, d) for t, d in res if d < 12]
    print(f'Voix / reste, 1–4 kHz, fenêtres de 0,4 s avec voix : médiane {np.median(vals):.1f} dB · minimum {vals.min():.1f} dB · '
          f'{len(bas)} fenêtre(s) sur {len(vals)} sous 12 dB')
    if bas:
        print('  ' + ', '.join(f'{t:.1f} s ({d:.1f} dB)' for t, d in bas[:40]) + (' …' if len(bas) > 40 else ''))
    return 0 if np.median(vals) >= 12 else 1


# ---------------------------------------------------------------- chrome
def c_chrome(a):
    out = run(['tasklist', '/FI', 'IMAGENAME eq chrome-headless-shell.exe'], text=True, encoding='cp850', errors='replace').stdout
    n = sum(1 for l in out.splitlines() if l.lower().startswith('chrome-headless-shell'))
    print(f'Chrome de HyperFrames ouverts : {n}.' + (' OK' if not n else
          ' Normal si un rendu tourne encore (agents en parallèle) ; ne jamais arrêter le Chrome d\'un rendu en cours.'))
    return 1 if n else 0


# ---------------------------------------------------------------- tout
def c_tout(a):
    codes = [c_niveau(a)]
    html = glob.glob(os.path.join(a.projet, '*.html')) + glob.glob(os.path.join(a.projet, 'compositions', '*.html'))
    if html:
        a.fichiers = html
        codes.append(c_couleurs(a))
    a.dossiers = [a.projet]
    codes.append(c_licences(a))
    codes.append(c_chrome(a))
    print('Rappel : planche, vibration, doublons entre séquences et voix / reste se lancent à part ; '
          'l\'écoute et le visionnage restent au propriétaire.')
    return 1 if any(codes) else 0


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description='Contrôles techniques du studio (voir README.md)')
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('niveau'); p.add_argument('film'); p.set_defaults(f=c_niveau)
    p = sp.add_parser('planche'); p.add_argument('film'); p.add_argument('--sortie', required=True)
    p.add_argument('--pas', type=float, default=2); p.add_argument('--colonnes', type=int, default=5); p.set_defaults(f=c_planche)
    p = sp.add_parser('vibration'); p.add_argument('film'); p.add_argument('--zone', required=True, help='L:H:X:Y en pixels')
    p.add_argument('--debut', type=float, default=0); p.add_argument('--duree', type=float, default=0)
    p.add_argument('--extraire', type=float, default=None, help='temps (s) : enregistre 10 images consécutives')
    p.set_defaults(f=c_vibration)
    p = sp.add_parser('tremblement'); p.add_argument('film')
    p.add_argument('--debut', type=float, default=0); p.add_argument('--duree', type=float, default=0)
    p.add_argument('--seuil', type=float, default=0.3, help="amplitude minimale d'un aller-retour, en px du film (0,3 par défaut)")
    p.add_argument('--brut', default=None, help='enregistre les déplacements mesurés (.npz) pour recalibrer sans relire le film')
    p.add_argument('--depuis', default=None, help='analyse un .npz enregistré par --brut au lieu de relire le film')
    p.set_defaults(f=c_tremblement)
    p = sp.add_parser('son'); p.add_argument('film'); p.add_argument('--reference', default=None,
                                                                   help='piste mixée placée dans la composition (wav)')
    p.add_argument('--voix', default=None, help='piste voix seule (bande ralentie ou stem voix) : les clics de bouche y ressortent mieux')
    p.set_defaults(f=c_son)
    p = sp.add_parser('couleurs'); p.add_argument('fichiers', nargs='+'); p.set_defaults(f=c_couleurs)
    p = sp.add_parser('doublons'); p.add_argument('dossiers', nargs='+')
    p.add_argument('--seuil', type=int, default=6, help='distance de Hamming maximale (sur 64) pour « même photo »')
    p.set_defaults(f=c_doublons)
    p = sp.add_parser('licences'); p.add_argument('dossiers', nargs='+'); p.set_defaults(f=c_licences)
    p = sp.add_parser('voix-reste'); p.add_argument('voix'); p.add_argument('reste'); p.set_defaults(f=c_voix_reste)
    p = sp.add_parser('chrome'); p.set_defaults(f=c_chrome)
    p = sp.add_parser('tout'); p.add_argument('film'); p.add_argument('--projet', required=True); p.set_defaults(f=c_tout)
    a = ap.parse_args()
    for k in ('film', 'voix', 'reste', 'reference', 'depuis'):
        if k == 'film' and getattr(a, 'depuis', None):
            continue
        if getattr(a, k, None) and not os.path.isfile(getattr(a, k)):
            print('Fichier introuvable : ' + getattr(a, k)); sys.exit(2)
    sys.exit(a.f(a))


if __name__ == '__main__':
    main()
