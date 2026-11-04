"""Mesure du mix d'un film sans écoute : écart voix − musique par cue, hausse de chaque marque. Outil commun du studio (1.1.2, 04/11/2026).

Méthode : skill `studio-faceless:direction-sonore`, `references/musique-par-cues.md` § 4 (contrôle sans écoute, décision du
03/11/2026 ; demandé par le propriétaire d'AA avant l'E012, 04/11/2026). Ces mesures repèrent des défauts ; elles ne valident
rien : le film reste ECOUTE_A_FAIRE jusqu'à l'écoute du propriétaire.

Entrées (celles de mix_film.py, sur la même ligne de temps) :
  - le mix : NOM.mp4 ou NOM.mix.wav sorti de mix_film.py, avec à côté NOM.mix.wav et NOM.log.txt (gain final unique) ;
  - le film voix : FILM-voix.mp4, avec FILM-voix.voix.wav (son sans perte, obligatoire) et son journal (FILM-voix.journal.json,
    à défaut FILM-voix.log.txt) ;
  - le plan son JSON du mix (cues : `musique` ; marques : `effets`, plus les --marque).
Calcul :
  1. résidu = mix ÷ gain final − voix, sur les seules séquences (signature, outro et autres pièces de marque exclues) ;
  2. intensité pondérée K (BS.1770) par trames de 10 ms, puis fenêtres de 3 s (court terme, sortie S d'ebur128) et de 0,4 s
     (momentanée, sortie M), pour le résidu et pour la voix ;
  3. par cue : fenêtres de 3 s dont le centre est dans le cue, entièrement en séquence, où la voix est active au moins une
     trame sur deux (activité de mix_film.py : RMS > −42 dBFS, pauses de moins de 250 ms comblées) et où le résidu passe la
     porte absolue de −70 LUFS ; médiane et pire décile de l'écart voix − résidu, contre mix.musique_sous_voix_lu_min et
     mix.musique_sous_voix_lu_max (seuils.json, avec direction/seuils.json de la chaîne) ;
  4. par marque : crête momentanée du résidu (départ entre t − 0,2 s et t + 0,4 s) contre la crête de la seconde d'avant
     (hausse), puis écart de la voix au résidu dans la même fenêtre, à côté de l'écart prévu par le plan (niveau du type) ;
  5. contrôle de la chaîne de mesure : résidu sur les passages en séquence sans musique ni effet prévus (il doit être très bas ;
     sinon gain, voix ou journal ne correspondent pas au mix).
Lecture : le résidu contient aussi les réductions du limiteur sur les attaques de la voix (journal du mix) et les effets qui
tombent dans un cue : un écart bas sur un cue chargé d'effets n'est pas forcément un défaut de la musique.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/mesurer_mix.py NOM.mp4 FILM-voix.mp4 PLAN-SON.json
         [--journal FICHIER] [--log NOM.log.txt] [--marque T[:nom]]... [--sortie RAPPORT.md]
  T : temps du film en secondes, ou seqN@t (temps local d'une séquence). --sortie : rapport Markdown, sans écrasement.
"""
import argparse, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I retire le dossier du script de sys.path
import numpy as np                                               # noqa: E402
from scipy.signal import lfilter                                 # noqa: E402
from mix_film import _K1, _K2, lk, activite, lire_journal, temps  # noqa: E402
from assembler import FP, SR, FPS, chemin, rel, lire              # noqa: E402
import seuils                                                    # noqa: E402  (outils/, mis sur sys.path par assembler)

TRAME = SR // 100          # 10 ms
COURT, MOMENT = 300, 40    # fenêtres de 3 s et de 0,4 s, en trames (définitions de BS.1770)
PORTE_ABSOLUE = -70.0      # porte absolue de BS.1770 (LUFS)


def puissance_trames(x):
    """Puissance pondérée K par trame de 10 ms, canaux sommés ; filtre en morceaux de 10 s (mémoire bornée)."""
    n = len(x) // TRAME
    out = np.empty(n)
    z1 = np.zeros((2, x.shape[1]))
    z2 = np.zeros((2, x.shape[1]))
    pas = TRAME * 1000
    for i in range(0, n * TRAME, pas):
        c = np.asarray(x[i:min(i + pas, n * TRAME)], np.float64)
        y, z1 = lfilter(*_K1, c, axis=0, zi=z1)
        y, z2 = lfilter(*_K2, y, axis=0, zi=z2)
        p = (y ** 2).sum(axis=1)
        out[i // TRAME:i // TRAME + len(p) // TRAME] = p.reshape(-1, TRAME).mean(1)
    return out


def fenetres(p, w):
    """Énergie moyenne des fenêtres de w trames, au pas d'une trame (fenêtre k : trames k à k + w − 1)."""
    if len(p) < w:
        return np.zeros(0)
    c = np.concatenate([[0.0], np.cumsum(p)])
    return (c[w:] - c[:-w]) / w


def part(b, w):
    """Part des trames vraies dans chaque fenêtre de w trames."""
    return fenetres(b.astype(np.float64), w)


def residu(mix, voix, segs, g):
    """mix ÷ gain final − voix : gain final sur les séquences et les noirs, pièces de marque à leur niveau (comme mix_film.py)."""
    gm = np.ones(len(mix), np.float32)
    r = int(0.01 * SR)
    for s in segs:
        if s['type'] == 'marque':
            i0, i1 = s['debut'] * SR // FPS, (s['debut'] + s['images']) * SR // FPS
            gm[i0:i1] = 0
            gm[i0:i0 + r] = np.linspace(1, 0, r)
            gm[i1 - r:i1] = np.linspace(0, 1, r)
    return mix / (1 + gm * np.float32(10 ** (g / 20) - 1))[:, None] - voix


def gain_du_journal(logp):
    with open(logp, encoding='utf-8') as f:
        lignes = f.read().splitlines()
    for l in lignes:
        m = re.match(r'^Gain final unique ([+-]?\d+(?:\.\d+)?) dB', l)
        if m:
            return float(m.group(1)), l
    sys.exit('Gain final introuvable dans le journal du mix : ' + logp)


def duree_fichier(p):
    r = subprocess.run([FP, '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def temps_marque(txt, segs, avis):
    t, _, nom = txt.partition(':')
    if '@' in t:
        s, _, loc = t.partition('@')
        return temps({'seq': s, 't': float(loc)}, segs, 'marque ' + txt, avis), nom or txt
    return float(t), nom or txt


def mmss(t):
    return f'{int(t // 60)}:{t % 60:04.1f}'


def mesurer(mix, voix, segs, total, plan, racine, marques_cli, lu_min, lu_max, g):
    """Tableaux des cues et des marques ; renvoie (lignes du rapport, nombre de cues hors plage)."""
    avis = []
    N = total * SR // FPS
    sq = np.zeros(N, bool)
    for s in segs:
        if s['type'] == 'sequence':
            sq[s['debut'] * SR // FPS:(s['debut'] + s['images']) * SR // FPS] = True
    res = residu(mix, voix, segs, g)
    pv, pr = puissance_trames(voix), puissance_trames(res)
    n = len(pv)
    sq_t = sq[:n * TRAME].reshape(n, TRAME).all(1)
    vm = voix.mean(axis=1)
    vm[~sq] = 0
    act = activite(vm, 25)[:n]
    del vm, res

    Sv, Sr = lk(fenetres(pv, COURT)), lk(fenetres(pr, COURT))
    ok = (part(sq_t, COURT) > 0.999) & (part(act, COURT) >= 0.5) & (Sr > PORTE_ABSOLUE)
    centre = (np.arange(len(Sv)) + COURT / 2) * 0.01
    Mv, Mr = lk(fenetres(pv, MOMENT)), lk(fenetres(pr, MOMENT))
    sq_m = part(sq_t, MOMENT) > 0.999
    Iv = float(lk(pv[sq_t & act].mean())) if (sq_t & act).any() else float('-inf')

    # --- Cues
    out = ['## Cues (écart voix − musique, fenêtres de 3 s, voix active)', '',
           f'Plage : de {lu_min:g} à {lu_max:g} LU sous la voix (`mix.musique_sous_voix_lu_min`, `mix.musique_sous_voix_lu_max`).', '',
           '| Cue | Fichier | Début → fin | Niveau du plan | Voix mesurée (s) | Médiane | Pire décile | Verdict |', '|---|---|---|---|---|---|---|---|']
    hors, couvert = 0, np.zeros(n, bool)
    for i, m in enumerate(plan.get('musique', [])):
        t0 = temps(m['depart'], segs, f'musique {i + 1}', avis)
        t1 = temps(m['fin'], segs, f'musique {i + 1}', avis) if 'fin' in m else t0 + float(m.get('duree', 0))
        couvert[max(0, int(t0 * 100)):max(0, int(t1 * 100) + 1)] = True
        sel = ok & (centre >= t0) & (centre <= t1)
        e = (Sv - Sr)[sel]
        ident = m.get('id') or f'M{i + 1:02d}'
        if len(e):
            med, p10 = float(np.median(e)), float(np.percentile(e, 10))
            verdict = 'OK' if lu_min <= med <= lu_max else ('TROP FORTE' if med < lu_min else 'TROP FAIBLE')
            hors += verdict != 'OK'
            mes = f'{len(e) / 100:.1f} | {med:.1f} | {p10:.1f} | {verdict}'
        else:
            mes = '0 | — | — | non mesuré (voix absente, pièce de marque ou cue trop court)'
        out.append(f'| {ident} | {os.path.basename(m["fichier"])} | {mmss(t0)} → {mmss(t1)} | {m.get("niveau_lu", "—")} | {mes} |')

    # --- Marques
    niveaux = plan.get('niveaux_par_type', {})
    marques = []
    for i, e in enumerate(plan.get('effets', [])):
        t = temps(e['depart'], segs, f'effet {i + 1}', avis)
        if 'extrait' in e:
            d = float(e['extrait'][1]) - float(e['extrait'][0])
        else:
            d = duree_fichier(os.path.join(racine, e['fichier']))
        couvert[max(0, int(t * 100)):max(0, int((t + d) * 100) + 1)] = True
        niv = niveaux.get(e.get('type'))
        niv = niv.get('lu') if isinstance(niv, dict) else niv
        marques.append((t, f'{e.get("type", "?")} · {os.path.basename(e["fichier"])}', niv))
    for txt in marques_cli:
        t, nom = temps_marque(txt, segs, avis)
        marques.append((t, 'marque · ' + nom, None))
    lignes_m, hausses = [], []
    for t, nom, niv in sorted(marques):
        k0, k1 = int(round((t - 0.2) * 100)), int(round((t + 0.4) * 100))
        a0, a1 = int(round((t - 1.0) * 100)), int(round((t - 0.4) * 100))
        if a0 < 0 or k1 >= len(Mr) or not sq_m[a0:k1 + 1].all():
            lignes_m.append(f'| {mmss(t)} | {nom} | — | — | — | {"—" if niv is None else f"{-niv:g}"} | hors séquence ou bord du film |')
            continue
        kp = k0 + int(np.argmax(Mr[k0:k1 + 1]))
        crete, avant = float(Mr[kp]), float(Mr[a0:a1 + 1].max())
        hausse, ecart = crete - avant, float(Mv[kp]) - crete
        hausses.append((hausse, t, nom))
        prevu = '—' if niv is None else f'{-niv:g}'
        lignes_m.append(f'| {mmss(t)} | {nom} | {crete:.1f} | {avant:.1f} | {hausse:+.1f} | {prevu} | {ecart:.1f} |')
    out += ['', '## Marques (crête momentanée du résidu, fenêtres de 0,4 s)', '',
            'Hausse : crête à la marque moins crête de la seconde d\'avant. Écart : voix moins résidu dans la fenêtre de la crête ; '
            'prévu : écart visé par le plan (niveau du type, en LU sous la voix).', '',
            '| Temps | Marque | Crête (LUFS) | Avant | Hausse (LU) | Écart prévu | Écart mesuré |', '|---|---|---|---|---|---|---|']
    out += lignes_m
    if hausses:
        faibles = sorted(hausses)[:10]
        out += ['', 'Les plus faibles hausses : ' + ' ; '.join(f'{mmss(t)} {nom} {h:+.1f} LU' for h, t, nom in faibles) + '.']

    # --- Contrôle de la chaîne de mesure
    libre = sq_t & ~couvert
    if libre.sum() >= MOMENT:
        Il = float(lk(pr[libre].mean()))
        ctrl = f'résidu sur {libre.sum() / 100:.1f} s en séquence sans musique ni effet : {Il:.1f} LUFS, soit {Iv - Il:.1f} LU sous la voix'
    else:
        ctrl = 'aucun passage en séquence sans musique ni effet : chaîne de mesure non contrôlée sur ce film'
    tete = [f'Voix active sur les séquences : {Iv:.1f} LUFS. Contrôle de la chaîne de mesure : {ctrl}.']
    return tete + avis, out, hors


def main():
    ap = argparse.ArgumentParser(description='Mesure du mix sans écoute (musique-par-cues.md § 4).')
    ap.add_argument('mix', help='NOM.mp4 ou NOM.mix.wav sorti de mix_film.py')
    ap.add_argument('film', help='FILM-voix.mp4 (avec FILM-voix.voix.wav et son journal)')
    ap.add_argument('plan', help='plan son JSON du mix')
    ap.add_argument('--journal', help='journal du film voix (défaut : FILM.journal.json, sinon FILM.log.txt)')
    ap.add_argument('--log', help='journal du mix (défaut : NOM.log.txt)')
    ap.add_argument('--marque', action='append', default=[], help='marque à mesurer : T[:nom] ou seqN@t[:nom]')
    ap.add_argument('--sortie', help='rapport Markdown (aucun écrasement)')
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    m = os.path.abspath(a.mix)
    base = m[:-8] if m.endswith('.mix.wav') else m[:-4]
    wav, logp = base + '.mix.wav', os.path.abspath(a.log) if a.log else base + '.log.txt'
    film = os.path.abspath(a.film)
    vw = film[:-4] + '.voix.wav'
    for p in (wav, logp, vw, os.path.abspath(a.plan)):
        if not os.path.isfile(p):
            sys.exit('Fichier introuvable : ' + p)
    if a.sortie and os.path.exists(a.sortie):
        sys.exit('Rapport existant, aucun écrasement : ' + a.sortie)
    with open(a.plan, encoding='utf-8') as f:
        plan = json.load(f)
    segs, total, pj = lire_journal(film, a.journal)
    g, ligne_gain = gain_du_journal(logp)
    N = total * SR // FPS

    def caler(x):
        return x[:N] if len(x) >= N else np.vstack([x, np.zeros((N - len(x), 2), x.dtype)])
    mix, voix = caler(lire(wav, np.float32)), caler(lire(vw, np.float32))
    lu_min, lu_max = seuils.valeur('mix.musique_sous_voix_lu_min'), seuils.valeur('mix.musique_sous_voix_lu_max')
    tete, corps, hors = mesurer(mix, voix, segs, total, plan, chemin(plan.get('racine', '.')), a.marque, lu_min, lu_max, g)
    rapport = [f'# Mesure du mix sans écoute : {os.path.basename(base)}', '',
               f'Outil `outils/montage/mesurer_mix.py` ; mix {rel(wav)} ; journal du mix {rel(logp)} ; film voix {rel(vw)} ; '
               f'journal {rel(pj)} ; plan {rel(os.path.abspath(a.plan))}.', '',
               f'Journal du mix : {ligne_gain}', ''] + tete + [''] + corps + [
               '', '## Lecture',
               f'- Cues hors plage : {hors}. Ces mesures repèrent des défauts ; elles ne valident rien : le film reste '
               '`ECOUTE_A_FAIRE` jusqu\'à l\'écoute du propriétaire.',
               '- Le résidu contient aussi les réductions du limiteur (journal du mix) et les effets qui tombent dans un cue.']
    texte = '\n'.join(rapport) + '\n'
    if a.sortie:
        os.makedirs(os.path.dirname(os.path.abspath(a.sortie)) or '.', exist_ok=True)
        with open(a.sortie, 'x', encoding='utf-8') as f:
            f.write(texte)
    print(texte)


if __name__ == '__main__':
    main()
