"""Mix du film entier, sur le film collé en voix seule. Outil commun du studio (24/10/2026).

Règle : ${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md § 3 (validé sur AA, 24/10/2026) : un seul mix sur le film entier, après le collage en
voix seule ; une correction de son se refait par un remix, sans nouveau rendu d'image. Claude n'écoute pas : le master
reste ECOUTE_A_FAIRE jusqu'à l'écoute du propriétaire.

Entrées :
  - FILM.mp4, sorti de ${CLAUDE_PLUGIN_ROOT}/outils/montage/assembler.py --voix-seule, avec à côté FILM.voix.wav (son sans perte ; à défaut, le son
    AAC du MP4, avec un avis au journal) et FILM.journal.json (à défaut FILM.log.txt, le journal texte du master) ;
  - un plan son JSON : musique, effets, niveaux par type, baisse sous la voix, silences voulus (schéma : README.md).
Méthode :
  - la voix est la référence : sa sonie intégrée (BS.1770, mesurée sur les seules séquences) fixe tous les niveaux ;
  - musique : gain = voix + niveau_lu − sonie intégrée du départ (fondus compris, avant la baisse) ; baisse sous la voix
    active, par l'enveloppe RMS de la voix (fenêtres de 10 ms, seuil −42 dBFS, descente 80 ms, remontée 400 ms, remontée
    dans les pauses ≥ 0,25 s : mêmes règles que le gabarit mix.py) ;
  - effets : gain = voix + niveau du type − sonie momentanée maximale (fenêtre de 400 ms) de l'extrait ; baisse facultative
    par type (pauses < 0,65 s comblées) ;
  - creux (facultatifs, E008 d'AA) : la musique seule baisse de baisse_db dB sur la fenêtre, rampes de « rampe » s ;
  - silences voulus : musique et effets y sont coupés (rampes de 50 ms hors de la fenêtre) ; un effet qui y commence est
    retiré ; le journal signale chaque coupe ;
  - un seul gain final vers −16 LUFS, mesuré sur les séquences (les pièces de marque gardent leur niveau d'origine, comme au
    master E007 v1 d'AA), limiteur de crêtes vraies à −2,0 dBTP (celui de l'assembleur), image copiée telle quelle (-c:v copy).
Contrôles : images identiques à l'entrée (nombre et empreinte MD5 du flux vidéo), −16 ±1 LUFS, crête vraie ≤ −1,5 dBTP,
décodage complet sans erreur. Sorties : NOM.mp4, NOM.mix.wav, NOM.log.txt ; aucun écrasement. --son-seul : rien n'est écrit.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/mix_film.py FILM-voix.mp4 PLAN-SON.json [--journal FICHIER] [--nom NOM.mp4] [--out DOSSIER]
                                         [--son-seul]
"""
import argparse, json, os, re, subprocess, sys
import numpy as np
from scipy.signal import lfilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I retire le dossier du script de sys.path
from assembler import (FF, FP, SR, FPS, TARGET_I, TOLERANCE_I, MAX_TP, PLAFOND_WAV, chemin, rel, probe, lire, ebur128, mesurer,   # noqa: E402
                       write_wav, limiteur, lieu, ecrire_journal)

RAMPE_SILENCE, RAMPE_GAIN = 0.05, 0.01


# --- Journal du film voix ----------------------------------------------------------------------------------------------

def lire_journal(mp4, pj=None):
    base = mp4[:-4]
    pj = pj or (base + '.journal.json' if os.path.isfile(base + '.journal.json') else base + '.log.txt')
    if not os.path.isfile(pj):
        sys.exit('Journal du film introuvable : ' + pj)
    if pj.endswith('.json'):
        with open(pj, encoding='utf-8') as f:
            j = json.load(f)
        segs = [{'id': s['id'], 'type': s['type'], 'debut': s['debut_image'], 'images': s['images']} for s in j['segments']]
        return segs, j['images'], pj
    segs = []
    with open(pj, encoding='utf-8') as f:
        for l in f:
            m = re.match(r'^(\S+)\s+([\d.]+) s →\s*([\d.]+) s \((\d+) images\)', l)
            if m:
                k = m.group(1)
                typ = 'noir' if k == 'noir' else 'sequence' if re.fullmatch(r'seq\d+', k) else 'marque'
                segs.append({'id': k, 'type': typ, 'debut': int(round(float(m.group(2)) * FPS)), 'images': int(m.group(4))})
    if not segs:
        sys.exit('Aucun segment dans le journal : ' + pj)
    return segs, segs[-1]['debut'] + segs[-1]['images'], pj


def temps(d, segs, quoi, avis):
    """Temps du film (s) : un nombre, ou {"seq": "seq3", "t": 12.5} (temps local de la séquence, converti par le journal)."""
    if isinstance(d, (int, float)) and not isinstance(d, bool):
        return float(d)
    if isinstance(d, dict) and 'seq' in d:
        s = next((s for s in segs if s['id'] == d['seq']), None)
        if s is None:
            sys.exit(f'{quoi} : segment « {d["seq"]} » absent du journal')
        t = float(d.get('t', 0.0))
        if not 0 <= t <= s['images'] / FPS:
            avis.append(f'  AVIS : {quoi} : {t:.2f} s hors de {s["id"]} (0 → {s["images"] / FPS:.2f} s)')
        return s['debut'] / FPS + t
    sys.exit(f'{quoi} : temps illisible ({d!r}) ; attendu un nombre ou {{"seq": "seqN", "t": secondes}}')


def segments_touches(t0, t1, segs, types):
    return [s['id'] for s in segs if s['type'] in types and s['debut'] / FPS < t1 and (s['debut'] + s['images']) / FPS > t0]


# --- Sonie BS.1770 en numpy (niveaux relatifs) ---------------------------------------------------------------------------

_K1 = ([1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585])
_K2 = ([1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621])


def lk(z):
    return -0.691 + 10 * np.log10(np.maximum(z, 1e-20))


def energies(x, pas=0.1):
    """Énergies pondérées K des blocs de 400 ms au pas donné (s), canaux sommés (BS.1770, 48 kHz)."""
    y = lfilter(*_K2, lfilter(*_K1, np.asarray(x, np.float64), axis=0), axis=0)
    p = (y ** 2).sum(axis=1)
    n, h = int(0.4 * SR), max(1, int(pas * SR))
    if len(p) < n:
        return np.array([p.sum() / n])
    c = np.concatenate([[0.0], np.cumsum(p)])
    d = np.arange(0, len(p) - n + 1, h)
    return (c[d + n] - c[d]) / n


def integree(z):
    """Sonie intégrée (LUFS) d'énergies de blocs : portes absolue (−70) et relative (−10 LU)."""
    z = z[lk(z) > -70]
    if not len(z):
        return -np.inf
    z = z[lk(z) > lk(z.mean()) - 10]
    return float(lk(z.mean()))


# --- Enveloppe de la voix et baisse ------------------------------------------------------------------------------------

def activite(v, comble):
    """Voix active par fenêtres de 10 ms (RMS > −42 dBFS) ; pauses < comble × 10 ms comblées ; anticipation de 60 ms."""
    h = SR // 100
    n = len(v) // h
    d = 20 * np.log10(np.sqrt((v[:n * h].reshape(n, h).astype(np.float64) ** 2).mean(1)) + 1e-9)
    act = d > -42.0
    i = 0
    while i < n:
        if not act[i]:
            j = i
            while j < n and not act[j]:
                j += 1
            if 0 < i and j < n and j - i < comble:
                act[i:j] = True
            i = j
        else:
            i += 1
    return act | np.concatenate([act[6:], np.zeros(6, bool)])


def courbe_db(act, prof):
    """Gain en dB par fenêtre de 10 ms : −prof sous la voix, descente en 80 ms, remontée en 400 ms."""
    cur, out = 0.0, np.zeros(len(act))
    for i, a in enumerate(act):
        tgt = -prof if a else 0.0
        cur = max(tgt, cur - prof / 8) if tgt < cur else min(tgt, cur + prof / 40)
        out[i] = cur
    return out


def gain_lin(cdb, s0, s1):
    tf = (np.arange(len(cdb)) + 0.5) / 100
    return (10 ** (np.interp(np.arange(s0, s1) / SR, tf, cdb) / 20)).astype(np.float32)


def fondus(x, fi, fo, forme='sin'):
    ni, no = min(len(x), max(1, int(fi * SR))), min(len(x), max(1, int(fo * SR)))
    if forme == 'sin':
        up, dn = np.sin(np.linspace(0, np.pi / 2, ni)), np.cos(np.linspace(0, np.pi / 2, no))
    else:
        up, dn = np.linspace(0, 1, ni), np.linspace(1, 0, no)
    x[:ni] *= up[:, None].astype(x.dtype)
    x[-no:] *= dn[:, None].astype(x.dtype)
    return x


def extrait_musique(m, off, n, boucle, xf_s):
    """n échantillons de la source à partir de off (s) ; avec boucle [a, b] (s), retour de b à a avec un fondu enchaîné
    linéaire de xf_s pris avant a (le point de boucle tombe juste). Rend (signal, nombre de retours, secondes manquantes)."""
    i0 = int(round(off * SR))
    if i0 >= len(m):
        sys.exit(f'Décalage {off:.2f} s au-delà de la source ({len(m) / SR:.2f} s)')
    if not boucle:
        x = m[i0:i0 + n]
        manque = n - len(x)
        return (np.vstack([x, np.zeros((manque, 2), np.float32)]) if manque > 0 else x.copy()), 0, max(0, manque) / SR
    a, b = int(round(boucle[0] * SR)), int(round(boucle[1] * SR))
    if not (0 <= a < b <= len(m) and i0 < b):
        sys.exit(f'Boucle {boucle} hors de la source ({len(m) / SR:.2f} s) ou après le décalage {off:.2f} s')
    out, xf = np.zeros((n, 2), np.float32), int(xf_s * SR)
    k = min(n, b - i0)
    out[:k] = m[i0:i0 + k]
    pos, retours = k, 0
    while pos < n:
        k = min(n - pos, b - a)
        out[pos:pos + k] = m[a:a + k]
        j = min(xf, a, pos)
        if j:
            r = np.linspace(0, 1, j, dtype=np.float32)[:, None]
            out[pos - j:pos] = out[pos - j:pos] * (1 - r) + m[a - j:a] * r
        pos += k
        retours += 1
    return out, retours, 0.0


def masque_rampes(N, fenetres, r):
    """1 partout, 0 dans chaque fenêtre (i0, i1), rampes en cosinus de r échantillons hors de la fenêtre."""
    g = np.ones(N, np.float32)
    rd = (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, r))).astype(np.float32)        # 1 → 0
    for i0, i1 in fenetres:
        i0, i1 = max(0, i0), min(N, i1)
        g[i0:i1] = 0
        a = max(0, i0 - r)
        g[a:i0] = np.minimum(g[a:i0], rd[r - (i0 - a):])
        b = min(N, i1 + r)
        g[i1:b] = np.minimum(g[i1:b], rd[::-1][:b - i1])
    return g


def masque_creux(N, fenetres):
    """1 partout ; dans chaque fenêtre (i0, i1, db, r), la musique baisse de db dB, rampes en cosinus de r échantillons
    hors de la fenêtre (E008 d'AA, 25/10/2026 : un silence voulu sans coupure brutale)."""
    g = np.ones(N, np.float32)
    for i0, i1, db, r in fenetres:
        lo, r = np.float32(10 ** (-db / 20)), max(1, r)
        i0, i1 = max(0, i0), min(N, i1)
        g[i0:i1] = np.minimum(g[i0:i1], lo)
        u = (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, r))).astype(np.float32)       # 0 → 1
        a = max(0, i0 - r)
        g[a:i0] = np.minimum(g[a:i0], 1 - (1 - lo) * u[r - (i0 - a):])
        b = min(N, i1 + r)
        g[i1:b] = np.minimum(g[i1:b], 1 - (1 - lo) * u[::-1][:b - i1])
    return g


def empreinte_video(p):
    return subprocess.run([FF, '-v', 'error', '-i', p, '-map', '0:v:0', '-c', 'copy', '-f', 'md5', '-'],
                          capture_output=True, text=True, check=True).stdout.strip()


def titre_de(p):
    out = subprocess.run([FP, '-v', 'error', '-show_entries', 'format_tags=title', '-of', 'default=nw=1:nk=1', p],
                         capture_output=True, text=True, encoding='utf-8', errors='replace').stdout.strip()
    return out


# --- Mix ----------------------------------------------------------------------------------------------------------------

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description='Mix du film entier sur le film collé en voix seule (outils/montage/README.md).')
    ap.add_argument('film', help='MP4 « voix » sorti de assembler.py --voix-seule')
    ap.add_argument('plan', help='plan son JSON')
    ap.add_argument('--journal', help='journal du film (défaut : FILM.journal.json, sinon FILM.log.txt)')
    ap.add_argument('--nom', help='nom du MP4 mixé (défaut : sortie.nom du plan, sinon FILM avec -mix au lieu de -voix)')
    ap.add_argument('--out', help='dossier de sortie (défaut : sortie.dossier du plan, sinon celui du film)')
    ap.add_argument('--son-seul', action='store_true', help='mesure le mix sans rien écrire')
    a = ap.parse_args()
    film, plan_path = os.path.abspath(a.film), os.path.abspath(a.plan)
    with open(plan_path, encoding='utf-8') as f:
        plan = json.load(f)
    so = plan.get('sortie', {})
    base_film = os.path.basename(film)[:-4]
    nom = a.nom or so.get('nom') or (base_film.replace('-voix', '-mix') if '-voix' in base_film else base_film + '-mix') + '.mp4'
    out = os.path.join(os.path.abspath(a.out) if a.out else (chemin(so['dossier']) if so.get('dossier') else os.path.dirname(film)), nom)
    wav, logp = out[:-4] + '.mix.wav', out[:-4] + '.log.txt'
    if not a.son_seul:
        for p in (out, wav, logp):
            if os.path.exists(p):
                sys.exit('Sortie existante, aucun écrasement : ' + p)
    segs, total, pj = lire_journal(film, a.journal)
    racine = chemin(plan.get('racine', '.'))
    log, avis = [f'Mix du film (outils/montage/mix_film.py) ; film voix {rel(film)} ; journal {rel(pj)} ; plan {rel(plan_path)}'], []

    # --- Voix (référence)
    vw = film[:-4] + '.voix.wav'
    if os.path.isfile(vw):
        voix = lire(vw, np.float32)
        log.append(f'Voix : {rel(vw)} (sans perte)')
    else:
        voix = lire(film, np.float32)
        log.append(f'Voix : son AAC du film (AVIS : {rel(vw)} absent ; un second encodage AAC suivra)')
    N = total * SR // FPS
    if abs(len(voix) - N) > SR // FPS:
        avis.append(f'  AVIS : son du film voix de {len(voix) / SR:.3f} s pour {total / FPS:.3f} s d\'image (calé à l\'image)')
    voix = voix[:N] if len(voix) >= N else np.vstack([voix, np.zeros((N - len(voix), 2), np.float32)])
    sq = np.zeros(N, bool)
    blocs, par_seq = [], []
    for s in segs:
        i0, i1 = s['debut'] * SR // FPS, (s['debut'] + s['images']) * SR // FPS
        if s['type'] == 'sequence':
            sq[i0:i1] = True
            z = energies(voix[i0:i1])
            blocs.append(z)
            par_seq.append((s['id'], integree(z)))
    if not par_seq:
        sys.exit('Aucune séquence dans le journal : la voix de référence manque')
    Iv = integree(np.concatenate(blocs))
    vals = [v for _, v in par_seq]
    imin, imax = int(np.argmin(vals)), int(np.argmax(vals))
    sauts = [(abs(par_seq[i + 1][1] - par_seq[i][1]), par_seq[i][0], par_seq[i + 1][0]) for i in range(len(par_seq) - 1)]
    log.append(f'Voix (référence) : {Iv:.1f} LUFS intégrés sur les séquences ; par séquence : '
               + ', '.join(f'{k} {v:.1f}' for k, v in par_seq))
    log.append(f'  écart de niveau de la voix entre séquences : {vals[imax] - vals[imin]:.1f} LU au plus '
               f'({par_seq[imin][0]} {vals[imin]:.1f} → {par_seq[imax][0]} {vals[imax]:.1f})'
               + (f' ; plus grand saut entre voisines {max(sauts)[0]:.1f} LU ({max(sauts)[1]} → {max(sauts)[2]})' if sauts else ''))
    vm = voix.mean(axis=1)
    vm[~sq] = 0
    act_mu, act_fx = activite(vm, 25), activite(vm, 65)
    del vm
    cache_db = {}

    def baisse(act_k, prof, s0, s1):
        if not prof:
            return None
        k = (act_k, prof)
        if k not in cache_db:
            cache_db[k] = courbe_db(act_mu if act_k == 'mu' else act_fx, prof)
        return gain_lin(cache_db[k], s0, s1)

    # --- Silences voulus
    sil = []
    for i, s in enumerate(plan.get('silences', [])):
        t0, t1 = temps(s['debut'], segs, f'silence {i + 1}', avis), temps(s['fin'], segs, f'silence {i + 1}', avis)
        if t1 <= t0:
            sys.exit(f'Silence {i + 1} : fin avant le début')
        sil.append((t0, t1, s.get('raison', '')))
    r_sil = int(RAMPE_SILENCE * SR)
    masque = masque_rampes(N, [(int(round(t0 * SR)), int(round(t1 * SR))) for t0, t1, _ in sil], r_sil)

    def coupes(t0, t1):
        return [(max(t0, a0), min(t1, a1)) for a0, a1, _ in sil if a0 - RAMPE_SILENCE < t1 and a1 + RAMPE_SILENCE > t0]

    # --- Creux de musique (facultatif) : la musique seule baisse de baisse_db dB sur la fenêtre, rampes de « rampe » s
    creux = []
    for i, c in enumerate(plan.get('creux', [])):
        t0, t1 = temps(c['debut'], segs, f'creux {i + 1}', avis), temps(c['fin'], segs, f'creux {i + 1}', avis)
        if t1 <= t0:
            sys.exit(f'Creux {i + 1} : fin avant le début')
        creux.append((t0, t1, float(c.get('baisse_db', 8.0)), float(c.get('rampe', 0.8)), c.get('raison', '')))
    masque_mu = masque_creux(N, [(int(round(t0 * SR)), int(round(t1 * SR)), db, int(r * SR)) for t0, t1, db, r, _ in creux])

    # --- Musique
    mus = np.zeros((N, 2), np.float32)
    prof_mu = float(plan.get('baisse_sous_voix_db', 4.0))
    log.append(f'Musique (niveaux en LU sous la voix, avant la baisse de {prof_mu:.1f} dB sous la voix active, '
               f'80 ms / 400 ms, remontée dans les pauses ≥ 0,25 s) :')
    sources = {}
    for i, c in enumerate(plan.get('musique', [])):
        q = f'musique {i + 1}'
        fp = chemin(c['fichier'], racine)
        if not os.path.isfile(fp):
            sys.exit(f'{q} : fichier introuvable : {fp}')
        if fp not in sources:
            sources[fp] = lire(fp, np.float32)
        t0 = temps(c['depart'], segs, q, avis)
        dur = temps(c['fin'], segs, q, avis) - t0 if 'fin' in c else float(c['duree'])
        if dur <= 0:
            sys.exit(f'{q} : durée nulle ou négative')
        n = int(round(dur * SR))
        x, retours, manque = extrait_musique(sources[fp], float(c.get('decalage', 0.0)), n, c.get('boucle'),
                                             float(c.get('fondu_boucle', 0.05)))
        x = fondus(x, float(c.get('fondu_entree', 1.0)), float(c.get('fondu_sortie', 1.0)))
        Ic = integree(energies(x))
        if not np.isfinite(Ic):
            sys.exit(f'{q} : extrait muet')
        g = Iv + float(c['niveau_lu']) - Ic
        x *= np.float32(10 ** (g / 20))
        s0 = int(round(t0 * SR))
        s1 = min(N, s0 + n)
        if s0 >= N or s0 < 0:
            sys.exit(f'{q} : départ {t0:.2f} s hors du film')
        prof = float(c.get('baisse_db', prof_mu))
        x = x[:s1 - s0]
        gb = baisse('mu', prof, s0, s1)
        if gb is not None:
            x *= gb[:, None]
        mus[s0:s1] += x
        t1 = s1 / SR
        trav = segments_touches(t0, t1, segs, ('sequence',))
        notes = []
        if len(trav) > 1:
            notes.append('traverse ' + ' → '.join(trav))
        if retours:
            notes.append(f'{retours} retour(s) de boucle {c["boucle"][0]:.2f} → {c["boucle"][1]:.2f} s')
        if manque:
            notes.append(f'AVIS : source trop courte, {manque:.2f} s de silence à la fin')
        for a0, a1 in coupes(t0, t1):
            notes.append(f'COUPÉE par le silence voulu de {a0:.2f} à {a1:.2f} s')
        for k in segments_touches(t0, t1, segs, ('marque',)):
            notes.append(f'AVIS : chevauche la pièce de marque « {k} »')
        log.append(f'  {rel(fp)} : {t0:.2f} → {t1:.2f} s du film ({lieu(s0, segs)}), source à partir de '
                   f'{float(c.get("decalage", 0.0)):.2f} s, fondus {float(c.get("fondu_entree", 1.0)):.2f} / '
                   f'{float(c.get("fondu_sortie", 1.0)):.2f} s, {float(c["niveau_lu"]):+.1f} LU, gain {g:+.1f} dB, baisse {prof:.1f} dB'
                   + (' ; ' + ' ; '.join(notes) if notes else ''))
    sources.clear()

    # --- Effets
    types = {}
    for k, v in plan.get('niveaux_par_type', {}).items():
        types[k] = {'lu': float(v), 'baisse_db': 0.0} if isinstance(v, (int, float)) else \
                   {'lu': float(v['lu']), 'baisse_db': float(v.get('baisse_db', 0.0))}
    fx = np.zeros((N, 2), np.float32)
    log.append('Effets (niveau fixe par type : sonie momentanée maximale, en LU sous la voix) : '
               + ', '.join(f'{k} {v["lu"]:+.1f} LU' + (f' (baisse {v["baisse_db"]:.0f} dB)' if v['baisse_db'] else '')
                           for k, v in types.items()))
    cache = {}
    for i, e in enumerate(plan.get('effets', [])):
        q = f'effet {i + 1}'
        if e.get('type') not in types:
            sys.exit(f'{q} : type « {e.get("type")} » absent de niveaux_par_type')
        fp = chemin(e['fichier'], racine)
        if not os.path.isfile(fp):
            sys.exit(f'{q} : fichier introuvable : {fp}')
        if fp not in cache:
            cache[fp] = lire(fp, np.float32)
        ea, eb = e.get('extrait', [0.0, len(cache[fp]) / SR])
        x = cache[fp][int(round(ea * SR)):int(round(eb * SR))].copy()
        x = fondus(x, float(e.get('fondu_entree', 0.008)), float(e.get('fondu_sortie', 0.10)), 'lin')
        t0 = temps(e['depart'], segs, q, avis)
        t1 = t0 + len(x) / SR
        Lm = float(lk(energies(x, 0.01).max()))
        ty = types[e['type']]
        g = Iv + ty['lu'] - Lm
        dans = [(a0, a1) for a0, a1, _ in sil if a0 <= t0 < a1]
        if dans:
            log.append(f'  {rel(fp)} ({e["type"]}) à {t0:.2f} s : RETIRÉ, il tombe dans le silence voulu de '
                       f'{dans[0][0]:.2f} à {dans[0][1]:.2f} s')
            continue
        x *= np.float32(10 ** (g / 20))
        s0 = int(round(t0 * SR))
        if s0 >= N or s0 < 0:
            sys.exit(f'{q} : départ {t0:.2f} s hors du film')
        s1 = min(N, s0 + len(x))
        x = x[:s1 - s0]
        gb = baisse('fx', ty['baisse_db'], s0, s1)
        if gb is not None:
            x *= gb[:, None]
        fx[s0:s1] += x
        notes = [f'COUPÉ en partie par le silence voulu de {a0:.2f} à {a1:.2f} s' for a0, a1 in coupes(t0, t1)]
        notes += [f'AVIS : chevauche la pièce de marque « {k} »' for k in segments_touches(t0, t1, segs, ('marque',))]
        log.append(f'  {rel(fp)} [{ea:.2f}–{eb:.2f} s] ({e["type"]}) à {t0:.2f} s ({lieu(s0, segs)}), '
                   f'crête momentanée {Lm:.1f} LUFS, gain {g:+.1f} dB' + (' ; ' + ' ; '.join(notes) if notes else ''))
    cache.clear()
    if sil:
        log.append('Silences voulus (musique et effets coupés, rampes de 50 ms hors de la fenêtre) :')
        log += [f'  {t0:.2f} → {t1:.2f} s ({lieu(int(t0 * SR), segs)})' + (f' : {r}' if r else '') for t0, t1, r in sil]
    if creux:
        log.append('Creux de musique (la musique seule baisse ; les effets restent) :')
        log += [f'  {t0:.2f} → {t1:.2f} s ({lieu(int(t0 * SR), segs)}), −{db:.1f} dB, rampes de {r:.2f} s'
                + (f' : {raison}' if raison else '') for t0, t1, db, r, raison in creux]
    mus *= (masque * masque_mu)[:, None]
    fx *= masque[:, None]
    del masque, masque_mu
    reste = mus + fx
    act_lit = np.abs(mus).max(axis=1) > 1e-6
    if act_lit.any():
        Im = integree(energies(mus[act_lit]))
        log.append(f'Musique mesurée après la baisse, sur ses passages : {Im:.1f} LUFS, soit {Iv - Im:.1f} LU sous la voix')
    del mus, fx, act_lit
    mix = voix + reste
    del reste, voix

    # --- Gain final unique (séquences et noirs ; pièces de marque à leur niveau), limiteur, mesures
    gm = np.ones(N, np.float32)          # 1 : le gain final s'applique ; 0 : pièce de marque, rampes de 10 ms à ses bords
    r = int(RAMPE_GAIN * SR)
    for s in segs:
        if s['type'] == 'marque':
            i0, i1 = s['debut'] * SR // FPS, (s['debut'] + s['images']) * SR // FPS
            gm[i0:i1] = 0
            gm[i0:i0 + r] = np.linspace(1, 0, r)
            gm[i1 - r:i1] = np.linspace(0, 1, r)
    I0, _, tp0 = mesurer(mix[sq])
    log.append(f'Film mixé avant le gain final (séquences) : {I0:.1f} LUFS, crête vraie {tp0:.1f} dBTP')
    g = TARGET_I - I0
    for passe in range(3):
        y = mix * (1 + gm * np.float32(10 ** (g / 20) - 1))[:, None]
        red = limiteur(y, PLAFOND_WAV)
        y *= (10 ** (-red / 20))[:, None]
        I1, _, _ = mesurer(y[sq])
        if abs(I1 - TARGET_I) < 0.1 or passe == 2:
            break
        g += TARGET_I - I1
        del y, red
    del mix, gm
    act = red > 0.1
    bords = np.flatnonzero(np.diff(np.concatenate([[0], act.astype(np.int8), [0]])))
    zones = list(zip(bords[::2], bords[1::2]))
    log.append(f'Gain final unique {g:+.2f} dB (pièces de marque exclues), limiteur à {PLAFOND_WAV} dBTP : {len(zones)} réductions '
               f'de plus de 0,1 dB, maximum {red.max():.1f} dB ; temps sous réduction > 0,5 dB : {(red > 0.5).sum() / SR:.1f} s, '
               f'> 2 dB : {(red > 2).sum() / SR:.2f} s')
    for z0, z1 in sorted(zones, key=lambda z: -red[z[0]:z[1]].max())[:6]:
        log.append(f'  {red[z0:z1].max():.1f} dB à {lieu(z0 + int(np.argmax(red[z0:z1])), segs)}')
    del red, act
    log += avis
    if a.son_seul:
        I2, lra2, tp2 = mesurer(y)
        log.append(f'Essai son seul (rien n\'est écrit) : {I2:.1f} LUFS, crête vraie {tp2:.1f} dBTP, LRA {lra2:.1f} LU')
        print('\n'.join(log))
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    write_wav(wav, y)
    del y
    I2, lra2, tp2 = ebur128(wav)
    log.append(f'Son du film (WAV) : {I2:.1f} LUFS, crête vraie {tp2:.1f} dBTP, LRA {lra2:.1f} LU')

    # --- Remux : image copiée telle quelle, son AAC
    titre = plan.get('titre') or (titre_de(film).replace(' — voix seule', '') + ' — mix du film').strip(' —')
    subprocess.run([FF, '-v', 'error', '-n', '-i', film, '-i', wav, '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '320k', '-ar', str(SR), '-movflags', '+faststart', '-metadata', 'title=' + titre, out],
                   check=True)

    # --- Contrôles
    subprocess.run([FF, '-v', 'error', '-xerror', '-i', out, '-f', 'null', '-'], check=True)
    n_in, n_out = probe(film), probe(out)
    md_in, md_out = empreinte_video(film), empreinte_video(out)
    I3, lra3, tp3 = ebur128(out)
    log.append(f'MP4 : {n_out} images (entrée {n_in}, journal {total}) ; flux vidéo {"identique" if md_in == md_out else "DIFFÉRENT"} '
               f'(MD5 {md_out[-12:]}) ; {I3:.1f} LUFS intégré, crête vraie {tp3:.1f} dBTP, LRA {lra3:.1f} LU ; '
               f'décodage complet sans erreur')
    ecarts = [x for x, bad in (('nombre d\'images', n_out != n_in or n_in != total), ('flux vidéo modifié', md_in != md_out),
                               (f'intensité hors {TARGET_I:g} ±{TOLERANCE_I:g} LUFS', abs(I3 - TARGET_I) > TOLERANCE_I),
                               ('crête vraie > −1,5 dBTP', tp3 > MAX_TP)) if bad]
    log.append('Contrôles du MP4 : ' + ('OK' if not ecarts else 'ÉCART : ' + ', '.join(ecarts))
               + ' ; écoute à faire par le propriétaire (ECOUTE_A_FAIRE)')
    ecrire_journal(logp, log)
    print('\n'.join(log))


if __name__ == '__main__':
    main()
