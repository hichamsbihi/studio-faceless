"""Cartes papier de l'épisode 004 (« la feuille pour compter ») : l'Alaska (2.8, rappel en 7.7) et le monde (7.7).
Round « fonds des cartes » (Q1, Q3, Q6, Q9) et round « globe et cinématique » (Q1, Q5), `VALIDÉ` par Hicham le 26/10/2026.
Allure de la marque, comme en 002 : mer réglée `#DCE5D3` (posée en CSS), terre `#ECF0E6`, relief teinté doux (ombre `#C4CEC0`,
lumière `#F8FAF4`), traits d'encre `#1F2B24`.
  python -I -B kit/cartes/outils/preparer_papier.py alaska | monde
Sorties dans `kit/cartes/papier/` (jamais d'écrasement) :
- `<nom>-relief.png` : 2400 × 1350 px, soit le cadre 1920 × 1080 agrandi de 25 %, même centre, même échelle, posé en (−240, −135).
  Relief SR_HR teinté sur les terres ; mer transparente.
- `<nom>.json` et `<nom>.js` (`window.CARTES['<nom>']`) : le cadre, puis les chemins SVG en px du cadre.
  - `terres` : remplissage ; `cotes` et `frontieres` : traits séparés.
  - `pays` : chaque pays, avec son centre visible.
  - `oleoduc` : tracé, avec sa longueur en px pour un tracé progressif.
  - `lieux` : positions en px."""
import json, math, sys, zipfile
from pathlib import Path

import numpy as np
from scipy.ndimage import binary_dilation, gaussian_filter, map_coordinates

ICI = Path(__file__).resolve().parent
KIT = ICI.parent.parent
P = KIT / 'cartes' / 'papier'
sys.path.insert(0, str(ICI))
from proj import Albers, equal_earth, equal_earth_inv  # noqa: E402
from shp import lire  # noqa: E402

BASE, OMBRE, LUMIERE = np.array((236, 240, 230.)), np.array((196, 206, 192.)), np.array((248, 250, 244.))
W, H, X0, Y0 = 2400, 1350, -240, -135             # fond : cadre + 25 %, posé en (X0, Y0) dans le cadre 1920 × 1080
CLIP = (X0 - 60, Y0 - 60, X0 + W + 60, Y0 + H + 60)
DONNEES = KIT / 'donnees'
G = KIT / 'cartes' / 'globe' / 'donnees'


# --- cadres ---------------------------------------------------------------------------------------------------------------
class CadreAlaska:
    """Albers d'Alaska (EPSG:3338) à 1,5 km/px, centre (250 km ; 1 620 km) au centre du cadre (Q3)."""
    nom, kmpp = 'alaska', 1.5

    def __init__(self): self.A = Albers()

    def px(self, lon, lat):
        x, y = self.A.avant(np.asarray(lon, float), np.asarray(lat, float))
        return 960 + (x - 250000) / 1500, 540 - (y - 1620000) / 1500

    def inverse(self, X, Y):
        return self.A.arriere((X - 960) * 1500 + 250000, (540 - Y) * 1500 + 1620000)

    def info(self):
        return {'projection': 'Albers conique équivalente, EPSG:3338 (parallèles 55° et 65° N, origine 50° N, 154° O, GRS80)',
                'km_par_px': 1.5, 'centre_m': [250000, 1620000], 'centre_lonlat': [round(float(v), 5) for v in self.inverse(960, 540)]}


class CadreMonde:
    """Equal Earth, méridien central 0° (Q6) ; Antarctique hors cadre ; largeur des terres 1 840 px."""
    nom = 'monde'

    def __init__(self):
        self.k = 1840 / (2 * 2.7066299837)
        _, yh = equal_earth(0, 83.7); _, yb = equal_earth(0, -56.0)
        self.cy = 540 + self.k * (yh + yb) / 2
        self.kmpp = 6371.0088 / self.k

    def px(self, lon, lat):
        x, y = equal_earth(lon, lat); return 960 + self.k * x, self.cy - self.k * y

    def inverse(self, X, Y): return equal_earth_inv((X - 960) / self.k, (self.cy - Y) / self.k)

    def info(self):
        return {'projection': 'Equal Earth, méridien central 0°, sphère', 'px_par_rayon': round(self.k, 3),
                'km_par_px_equateur': round(self.kmpp, 2), 'centre_y_px': round(self.cy, 2)}


# --- géométrie ------------------------------------------------------------------------------------------------------------
def decouper(anneau, x0, y0, x1, y1):
    """Sutherland–Hodgman : un anneau (liste de (x, y)) coupé au rectangle."""
    pts = anneau
    for k in range(4):
        if not pts: return []
        dedans = [lambda p: p[0] >= x0, lambda p: p[0] <= x1, lambda p: p[1] >= y0, lambda p: p[1] <= y1][k]
        def inter(p, q):
            if k < 2: c = x0 if k == 0 else x1; u = (c - p[0]) / (q[0] - p[0]); return (c, p[1] + u * (q[1] - p[1]))
            c = y0 if k == 2 else y1; u = (c - p[1]) / (q[1] - p[1]); return (p[0] + u * (q[0] - p[0]), c)
        sortie, prec = [], pts[-1]
        for p in pts:
            if dedans(p):
                if not dedans(prec): sortie.append(inter(prec, p))
                sortie.append(p)
            elif dedans(prec): sortie.append(inter(prec, p))
            prec = p
        pts = sortie
    return pts


def remplir(anneaux, w, h, ox=0.0, oy=0.0):
    """Masque (h, w) des anneaux (px), règle pair-impair ; pixel (i, j) de centre (ox + j + 0,5 ; oy + i + 0,5)."""
    lignes, xs = [], []
    for r in anneaux:
        a = np.asarray(r, float) - (ox, oy)
        if len(a) < 3: continue
        b = np.roll(a, -1, 0); m = a[:, 1] != b[:, 1]
        x1, y1, x2, y2 = a[m, 0], a[m, 1], b[m, 0], b[m, 1]
        r0 = np.clip(np.ceil(np.minimum(y1, y2) - 0.5), 0, h).astype(np.int64)
        r1 = np.clip(np.ceil(np.maximum(y1, y2) - 0.5), 0, h).astype(np.int64)
        n = r1 - r0
        if n.sum() == 0: continue
        idx = np.repeat(np.arange(len(n)), n); off = np.cumsum(n) - n
        rows = r0[idx] + (np.arange(n.sum()) - off[idx]); yc = rows + 0.5
        lignes.append(rows); xs.append(x1[idx] + (yc - y1[idx]) * (x2[idx] - x1[idx]) / (y2[idx] - y1[idx]))
    masque = np.zeros((h, w), bool)
    if not lignes: return masque
    rows, x = np.concatenate(lignes), np.concatenate(xs)
    o = np.lexsort((x, rows)); rows, x = rows[o], x[o]
    debut = np.r_[0, np.flatnonzero(np.diff(rows)) + 1]; rang = np.arange(len(rows)) - np.repeat(debut, np.diff(np.r_[debut, len(rows)]))
    a, b = rang % 2 == 0, np.r_[rang[1:] % 2 == 1, False]
    pa = np.flatnonzero(a & b)
    diff = np.zeros((h, w + 1), np.int32)
    ca = np.clip(np.ceil(x[pa] - 0.5), 0, w).astype(np.int64); cb = np.clip(np.ceil(x[pa + 1] - 0.5), 0, w).astype(np.int64)
    np.add.at(diff, (rows[pa], ca), 1); np.add.at(diff, (rows[pa], cb), -1)
    return np.cumsum(diff, 1)[:, :w] > 0


def simplifier(pts, tol):
    if len(pts) < 3: return pts
    xy = np.asarray(pts, float); garde = np.zeros(len(xy), bool); garde[0] = garde[-1] = True; pile = [(0, len(xy) - 1)]
    while pile:
        i, j = pile.pop()
        if j <= i + 1: continue
        d = xy[j] - xy[i]; L = math.hypot(*d)
        r = xy[i + 1:j] - xy[i]
        e = np.abs(d[0] * r[:, 1] - d[1] * r[:, 0]) / L if L > 1e-9 else np.hypot(r[:, 0], r[:, 1])
        k = int(np.argmax(e))
        if e[k] > tol: garde[i + 1 + k] = True; pile += [(i, i + 1 + k), (i + 1 + k, j)]
    return [tuple(p) for p in xy[garde]]


def chemin(lignes, ferme):
    out = []
    for l in lignes:
        if len(l) < 2: continue
        out.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in l) + ('Z' if ferme else ''))
    return ''.join(out)


def dans(p, r):
    return r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3]


def morceaux(l, r):
    """Coupe une polyligne (px) en morceaux qui touchent le rectangle (segments entièrement dehors retirés)."""
    out, cur = [], []
    for i in range(len(l)):
        p = l[i]; q = l[i + 1] if i + 1 < len(l) else None
        if dans(p, r) or (q and dans(q, r)) or (cur and dans(cur[-1], r)): cur.append(p)
        else:
            if len(cur) > 1: out.append(cur)
            cur = []
    if len(cur) > 1: out.append(cur)
    return out


# --- données -------------------------------------------------------------------------------------------------------------
def pays_ne(fichier, nom, garder):
    """[(attributs, anneaux lon/lat)] des pays retenus par garder(attributs, anneau)."""
    out = []
    for a, f in lire(fichier, nom):
        anneaux = [r for r in f if garder(a, r)]
        if anneaux: out.append((a, anneaux))
    return out


def cotes_frontieres(pays):
    """Sépare les arêtes des anneaux en côtes et frontières (arêtes dont les deux sommets appartiennent à deux pays au moins)."""
    proprio = {}
    for k, (_, anneaux) in enumerate(pays):
        for r in anneaux:
            for p in r: proprio.setdefault((round(p[0], 6), round(p[1], 6)), set()).add(k)
    cotes, front, vu = [], [], set()
    for k, (_, anneaux) in enumerate(pays):
        for r in anneaux:
            courant, type_c = [r[0]], None
            for i in range(1, len(r)):
                p, q = r[i - 1], r[i]
                kp, kq = (round(p[0], 6), round(p[1], 6)), (round(q[0], 6), round(q[1], 6))
                f = len(proprio[kp]) > 1 and len(proprio[kq]) > 1 and len(proprio[kp] & proprio[kq]) > 1
                t = 'f' if f else 'c'
                if type_c not in (None, t):
                    (front if type_c == 'f' else cotes).append(courant); courant = [p]
                type_c = t; courant.append(q)
            if len(courant) > 1: (front if type_c == 'f' else cotes).append(courant)
    # une frontière est partagée par deux pays : ne la garder qu'une fois
    uniques = []
    for l in front:
        cle = frozenset((round(p[0], 5), round(p[1], 5)) for p in l)
        if cle not in vu: vu.add(cle); uniques.append(l)
    return cotes, uniques


def sr_hr():
    with zipfile.ZipFile(DONNEES / 'repris-002' / 'SR_HR.zip') as z: b = z.read('SR_HR.tif')
    return np.frombuffer(b, np.uint8, count=10800 * 21600, offset=18798).reshape(10800, 21600)


def relief(cadre, anneaux_px):
    X, Y = np.meshgrid(np.arange(W) + X0 + 0.5, np.arange(H) + Y0 + 0.5)
    lon, lat = cadre.inverse(X, Y); lon = np.asarray(lon, float); lat = np.asarray(lat, float)
    ok = np.isfinite(lon) & np.isfinite(lat)
    col = np.where(ok, (np.nan_to_num(lon) + 180) * 60 - 0.5, 0); lig = np.where(ok, (90 - np.nan_to_num(lat)) * 60 - 0.5, 0)
    sr = sr_hr()
    agr = 1.853 / cadre.kmpp
    if agr < 1:                                               # réduction : par blocs, pour la mémoire, après préfiltre
        f = int(round(1 / agr)); s = sr[:10800 // f * f, :21600 // f * f].reshape(10800 // f, f, 21600 // f, f).mean((1, 3))
        col, lig = (col + 0.5) / f - 0.5, (lig + 0.5) / f - 0.5
        g = map_coordinates(gaussian_filter(s.astype(np.float32), 0.6), [lig, col], order=3, mode='wrap')
    else:
        c0, c1 = int(col[ok].min()) - 8, int(col[ok].max()) + 9; l0, l1 = max(0, int(lig[ok].min()) - 8), min(10800, int(lig[ok].max()) + 9)
        if c0 < 0:          # la zone passe l'antiméridien (longitudes < −180° à l'ouest de l'Alaska) : on recolle les deux bouts
            bloc = np.concatenate([sr[l0:l1, 21600 + c0:], sr[l0:l1, :c1]], axis=1)
        else:
            bloc = sr[l0:l1, c0:c1]
        g = map_coordinates(bloc.astype(np.float32), [lig - l0, col - c0], order=3, mode='nearest')
    s = np.clip((g - 206.0) / 42.0, -1, 1)[..., None]
    rgb = np.where(s < 0, BASE + (BASE - OMBRE) * s, BASE + (LUMIERE - BASE) * s)
    terre = binary_dilation(remplir(anneaux_px, W, H, X0, Y0), iterations=1) & ok
    return np.dstack([np.clip(rgb + 0.5, 0, 255).astype(np.uint8), (terre * 255).astype(np.uint8)]), agr


def ecrire_png(chemin_png, rgba):
    import subprocess
    h, w = rgba.shape[:2]
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{w}x{h}', '-i', '-', '-frames:v', '1',
                    '-compression_level', '9', str(chemin_png)], input=rgba.tobytes(), check=True)


def fabriquer(cadre, pays, lieux, oleoduc=None, retenir=None):
    nom = cadre.nom
    for f in (f'{nom}-relief.png', f'{nom}.json', f'{nom}.js'):
        if (P / f).exists(): sys.exit('existe déjà : ' + str(P / f))
    P.mkdir(parents=True, exist_ok=True)
    proj = lambda r: list(zip(*[np.round(v, 2).tolist() for v in cadre.px([p[0] for p in r], [p[1] for p in r])]))
    vue = (0, 0, 1920, 1080)
    anneaux_px, liste_pays = [], []
    for a, anneaux in pays:
        rs = [decouper(proj(r), *CLIP) for r in anneaux]
        rs = [simplifier(r, 0.35) for r in rs if len(r) > 2]
        rs = [r for r in rs if len(r) > 2]
        if not rs: continue
        anneaux_px += rs
        # centre visible : moyenne des pixels de terre du pays dans le cadre
        m = remplir(rs, 1920, 1080)
        cx = cy = None
        if m.any(): yy, xx = np.nonzero(m); cx, cy = round(float(xx.mean()), 1), round(float(yy.mean()), 1)
        liste_pays.append({'iso': a.get('ADM0_A3') or a.get('adm0_a3'), 'nom': a.get('NAME') or a.get('name'), 'd': chemin(rs, True),
                           'cx': cx, 'cy': cy, 'aire_visible_px': int(m.sum())})
    cotes, front = cotes_frontieres(pays)
    trait = lambda ls: chemin([s for l in ls for m in morceaux(proj(l), CLIP) for s in [simplifier(m, 0.35)]], False)
    rgba, agr = relief(cadre, anneaux_px)
    ecrire_png(P / f'{nom}-relief.png', rgba)
    sortie = {'nom': nom, 'cadre': dict(cadre.info(), w=1920, h=1080),
              'relief': {'fichier': f'{nom}-relief.png', 'w': W, 'h': H, 'x': X0, 'y': Y0,
                         'source': "Natural Earth SR_HR 1:10m (une minute d'arc), domaine public", 'agrandissement': round(agr, 2),
                         'regle_1_3_respectee': bool(agr <= 1.3)},
              'couleurs': {'mer': '#DCE5D3', 'reglure': '#AFC5A8', 'terre': '#ECF0E6', 'encre': '#1F2B24'},
              'terres': chemin(anneaux_px, True), 'cotes': trait(cotes), 'frontieres': trait(front), 'pays': liste_pays,
              'lieux': {l['id']: [round(float(v), 1) for v in cadre.px(*l['lonlat'])] for l in lieux}}
    if oleoduc:
        l = simplifier(proj(oleoduc), 0.3)
        sortie['oleoduc'] = {'d': chemin([l], False), 'longueur_px': round(sum(math.dist(l[i], l[i + 1]) for i in range(len(l) - 1)), 1),
                             'km': 1281.1, 'debut': list(l[0]), 'fin': list(l[-1]),
                             'source': 'OpenStreetMap (D21), © OpenStreetMap contributors, ODbL'}
    if retenir: sortie.update(retenir(cadre))
    (P / f'{nom}.json').write_text(json.dumps(sortie, ensure_ascii=False), encoding='utf-8')
    (P / f'{nom}.js').write_text(f"window.CARTES = window.CARTES || {{}};\nwindow.CARTES['{nom}'] = " + json.dumps(sortie, ensure_ascii=False) + ';\n', encoding='utf-8')
    print(nom, ': pays', len(liste_pays), '; relief', W, 'x', H, 'agrandissement', round(agr, 2), '; terres', len(sortie['terres']) // 1000, 'k car. ;',
          'lieux', sortie['lieux'])


def alaska():
    cadre = CadreAlaska()
    garder = lambda a, r: a['ADM0_A3'] in ('USA', 'CAN', 'RUS') and any(-180 <= p[0] <= -110 and p[1] >= 45 for p in r[::max(1, len(r) // 200)] + [r[0]])
    pays = pays_ne(DONNEES / 'lot-2' / 'D16-ne_10m_admin_0_countries.zip', 'ne_10m_admin_0_countries', garder)
    lieux = json.loads((G / 'lieux.json').read_text(encoding='utf-8'))
    ol = json.loads((G / 'oleoduc.geojson').read_text(encoding='utf-8'))['geometry']['coordinates']
    fabriquer(cadre, pays, [l for l in lieux if l['id'] in ('station-1', 'terminal-valdez', 'prudhoe-bay', 'valdez', 'fairbanks', 'anchorage', 'juneau')], ol)


def monde():
    cadre = CadreMonde()
    def garder(a, r):
        if a['ADM0_A3'] == 'ATA': return False
        if a['ADM0_A3'] == 'USA' and min(p[0] for p in r) > 0: return False      # Aléoutiennes au-delà de 180° (Q6)
        return True
    pays = pays_ne(DONNEES / 'lot-2' / 'D15-ne_50m_admin_0_countries.zip', 'ne_50m_admin_0_countries', garder)
    lieux = json.loads((G / 'lieux.json').read_text(encoding='utf-8'))

    def alaska_info(c):
        ak = [r for a, rs in pays if a['ADM0_A3'] == 'USA' for r in rs if max(p[0] for p in r) < -129 and min(p[1] for p in r) > 50]
        pts = [p for r in ak for p in r]
        xs, ys = c.px([p[0] for p in pts], [p[1] for p in pts])
        anneaux = [simplifier(list(zip(*[np.round(v, 2).tolist() for v in c.px([p[0] for p in r], [p[1] for p in r])])), 0.35) for r in ak]
        m = remplir([r for r in anneaux if len(r) > 2], 1920, 1080); yy, xx = np.nonzero(m)
        return {'alaska': {'d': chemin([r for r in anneaux if len(r) > 2], True), 'cx': round(float(xx.mean()), 1), 'cy': round(float(yy.mean()), 1),
                           'boite': [round(float(xs.min()), 1), round(float(ys.min()), 1), round(float(xs.max()), 1), round(float(ys.max()), 1)]}}
    fabriquer(cadre, pays, [l for l in lieux if l['id'] in ('station-1', 'terminal-valdez', 'anchorage', 'juneau', 'fairbanks')], None, alaska_info)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    {'alaska': alaska, 'monde': monde}[sys.argv[1]]()
