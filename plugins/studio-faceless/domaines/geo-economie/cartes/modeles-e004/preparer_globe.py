"""Prépare les fonds et les données du globe de l'épisode 004 (kit/cartes/globe/).
Round « globe et cinématique », Q2 et Q3 (`VALIDÉ`, Hicham, 26/10/2026).
  python -I -B kit/cartes/outils/preparer_globe.py bm | s2 | s2v2 | donnees
Jamais d'écrasement : chaque étape s'arrête si sa sortie existe déjà.

Sorties :
- `globe/fonds/bm-v2/{z}/{x}/{y}.jpg` : Blue Marble NG d'août 2004 (NASA, domaine public), image du studio
  `direction/strategie/essais/systeme-cartes-v1/donnees/blue-marble/`.
  - Tuiles Web Mercator 256 px : z0–4 sur le monde, z5–6 sur l'Alaska et l'Alberta (−172 à −100° ; 45 à 73° N).
  - v2 (26/10/2026) : la région découpée dans Blue Marble couvre l'union exacte des tuiles z5–6. La v1 (`fonds/bm/`) prenait
    seulement la zone voulue, et les bords des tuiles qui en débordaient étaient recopiés en traînées (vues d'essai).
  - Étirement 0–0,92 comme le système de cartes du studio, puis étalonnage PRÉSENT de `kit/medias/traiter.py`.
- `globe/fonds/s2/prudhoe-40m.webp` et `prudhoe-10m.webp` : D22 (Sentinel-2 L2A, 01/08/2025) reprojetée en Web Mercator.
  - Bords fondus en alpha, sur le pourtour et le long du triangle sans données.
  - Étirement des niveaux sur les pixels valides, puis PRÉSENT.
  - Les emprises sont dans `globe/donnees/emprises.json`.
- `globe/donnees/oleoduc.geojson` : D21, la ligne du pétrole de la station 1 au terminal de Valdez, ordonnée et simplifiée à 15 m.
- `globe/donnees/alberta.geojson` (D17, 1:10 m) et `globe/donnees/lieux.json` (Natural Earth et D21)."""
import heapq, json, math, subprocess, sys
from pathlib import Path

import numpy as np
from scipy.ndimage import distance_transform_edt, map_coordinates

ICI = Path(__file__).resolve().parent
KIT = ICI.parent.parent
G = KIT / 'cartes' / 'globe'
sys.path.insert(0, str(ICI)); sys.path.insert(0, str(KIT / 'medias'))
from proj import km, mercator, mercator_inv, utm  # noqa: E402
from shp import lire  # noqa: E402
from traiter import present  # noqa: E402

BM = KIT.parent.parent.parent / 'direction' / 'strategie' / 'essais' / 'systeme-cartes-v1' / 'donnees' / 'blue-marble' / 'world.topo.bathy.200408.3x21600x10800.jpg'
D22 = KIT / 'donnees' / 'lot-2' / 'D22-sentinel2-prudhoe-2025-08-01-TCI.tif'
D21 = KIT / 'donnees' / 'lot-2' / 'D21-oleoduc-osm.json'
D17 = KIT / 'donnees' / 'lot-2' / 'D17-ne_10m_admin_1_states_provinces.zip'
NE_LIEUX = KIT / 'donnees' / 'repris-002' / 'ne_10m_populated_places.zip'
REGION = (-172.0, 45.0, -100.0, 73.0)
# D22 : UTM 6 N, origine (399960, 7800000), 10 m ; niveau 2 du COG = 40 m
D22_X0, D22_Y0 = 399960.0, 7800000.0
EMPRISES = {'prudhoe-40m': ((-149.72, 69.55, -146.55, 70.288), 40.0, 40),    # lon0, lat0, lon1, lat1 ; m/px ; fondu en px
            'prudhoe-10m': ((-149.10, 69.93, -147.55, 70.284), 10.0, 120)}


def decoder(chemin, filtre=None):
    sonde = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(chemin)] + (['-vf', filtre] if filtre else []) +
                           ['-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True).stdout
    w, h = int.from_bytes(sonde[16:20], 'big'), int.from_bytes(sonde[20:24], 'big')
    brut = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(chemin)] + (['-vf', filtre] if filtre else []) +
                          ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(brut, np.uint8).reshape(h, w, 3)


def echantillon(img, bbox, lon, lat):
    h, w = img.shape[:2]
    col = (lon - bbox[0]) / (bbox[2] - bbox[0]) * w - 0.5
    lig = (bbox[3] - lat) / (bbox[3] - bbox[1]) * h - 0.5
    return np.stack([map_coordinates(img[..., k], [lig, col], order=1, mode='nearest') for k in range(img.shape[2])], -1)


def tuile_lonlat(z, x, y, n=256):
    px = (np.arange(n) + 0.5) / n
    gx, gy = np.meshgrid(x + px, y + px)
    return gx / 2 ** z * 360 - 180, np.degrees(np.arctan(np.sinh(math.pi * (1 - 2 * gy / 2 ** z))))


def tuiles_xy(z, bbox):
    n = 2 ** z
    xy = lambda lon, lat: ((lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(max(-85.05, min(85.05, lat))))) / math.pi) / 2 * n)
    x0, y0 = xy(bbox[0], bbox[3]); x1, y1 = xy(bbox[2], bbox[1])
    return range(max(0, int(x0)), min(n, int(x1) + 1)), range(max(0, int(y0)), min(n, int(y1) + 1))


def bm():
    sortie = G / 'fonds' / 'bm-v2'
    if sortie.exists(): sys.exit('existe déjà : ' + str(sortie))
    monde = decoder(BM, 'scale=5400:2700').astype(np.float32) / 255            # 7,4 km/px, assez pour z0–4
    # union exacte des tuiles z5–6 de la région (z5 la contient) : aucun pixel de tuile hors de la découpe
    xs, ys = tuiles_xy(5, REGION)
    tlon0 = xs[0] / 32 * 360 - 180; tlon1 = (xs[-1] + 1) / 32 * 360 - 180
    tlat1 = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * ys[0] / 32)))); tlat0 = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (ys[-1] + 1) / 32))))
    c0, c1 = max(0, int(math.floor((tlon0 + 180) * 60)) - 2), min(21600, int(math.ceil((tlon1 + 180) * 60)) + 2)
    r0, r1 = max(0, int(math.floor((90 - tlat1) * 60)) - 2), min(10800, int(math.ceil((90 - tlat0) * 60)) + 2)
    print('découpe Blue Marble : lon', round(c0 / 60 - 180, 2), round(c1 / 60 - 180, 2), 'lat', round(90 - r1 / 60, 2), round(90 - r0 / 60, 2))
    region = decoder(BM, f'crop={c1 - c0}:{r1 - r0}:{c0}:{r0}').astype(np.float32) / 255
    rb = (c0 / 60 - 180, 90 - r1 / 60, c1 / 60 - 180, 90 - r0 / 60)
    etal = lambda a: present(np.clip(a / 0.92, 0, 1))
    jobs = [(z, x, y) for z in range(5) for x in range(2 ** z) for y in range(2 ** z)]
    for z in (5, 6):
        xs, ys = tuiles_xy(z, REGION); jobs += [(z, x, y) for x in xs for y in ys]
    tuiles = []
    for z, x, y in jobs:
        lon, lat = tuile_lonlat(z, x, y)
        a = echantillon(monde, (-180, -90, 180, 90), lon, lat) if z <= 4 else echantillon(region, rb, lon, lat)
        tuiles.append((z, x, y, (etal(a) * 255 + 0.5).astype(np.uint8)))
    tmp = sortie / '_seq'; tmp.mkdir(parents=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '256x256', '-i', '-', '-q:v', '3',
                    str(tmp / '%05d.jpg')], input=b''.join(t[3].tobytes() for t in tuiles), check=True)
    for k, (z, x, y, _) in enumerate(tuiles, 1):
        d = sortie / str(z) / str(x) / f'{y}.jpg'; d.parent.mkdir(parents=True, exist_ok=True); (tmp / f'{k:05d}.jpg').rename(d)
    tmp.rmdir()
    print('Blue Marble :', len(tuiles), 'tuiles')


def lire_d22(niveau):
    sys.path.insert(0, str(ICI))
    from cog import lire as lire_cog
    return lire_cog(str(D22), niveau)


def s2():
    sortie = G / 'fonds' / 's2'
    if sortie.exists(): sys.exit('existe déjà : ' + str(sortie))
    sources = {40.0: lire_d22(2), 10.0: lire_d22(0)}
    valide40 = sources[40.0].max(2) > 0
    # bornes d'étirement communes aux deux produits, sur les pixels valides du 40 m (centiles 0,5–99,5, communs aux bandes)
    v = sources[40.0][valide40].astype(np.float32) / 255
    bas, haut = np.percentile(v, 0.5), np.percentile(v, 99.5)
    sortie.mkdir(parents=True); emprises = {}
    for nom, (bb, res, fondu) in EMPRISES.items():
        src = sources[res]; valide = (src.max(2) > 0).astype(np.float32)
        lat_m = (bb[1] + bb[3]) / 2; pas = res / math.cos(math.radians(lat_m))       # pas en mètres Mercator
        (mx0, my0), (mx1, my1) = mercator(bb[0], bb[1]), mercator(bb[2], bb[3])
        w, h = int(round((mx1 - mx0) / pas)), int(round((my1 - my0) / pas))
        gx, gy = np.meshgrid(mx0 + (np.arange(w) + 0.5) * (mx1 - mx0) / w, my1 - (np.arange(h) + 0.5) * (my1 - my0) / h)
        lon, lat = mercator_inv(gx, gy)
        ux, uy = utm(lon, lat, 6)
        col, lig = (ux - D22_X0) / res - 0.5, (D22_Y0 - uy) / res - 0.5
        rgb = np.stack([map_coordinates(src[..., k], [lig, col], order=1, mode='constant', cval=0) for k in range(3)], -1)
        a = map_coordinates(valide, [lig, col], order=1, mode='constant', cval=0) > 0.99
        a[0, :] = a[-1, :] = a[:, 0] = a[:, -1] = False
        alpha = np.clip(distance_transform_edt(a) / fondu, 0, 1); alpha = alpha * alpha * (3 - 2 * alpha)
        x = present(np.clip((rgb.astype(np.float32) / 255 - bas) / (haut - bas), 0, 1) ** 0.92)
        rgba = np.dstack([(x * 255 + 0.5).astype(np.uint8), (alpha * 255 + 0.5).astype(np.uint8)])
        f = sortie / f'{nom}.webp'
        subprocess.run(['ffmpeg', '-v', 'error', '-n', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{w}x{h}', '-i', '-',
                        '-c:v', 'libwebp', '-quality', '90', '-pix_fmt', 'yuva420p', '-frames:v', '1', str(f)], input=rgba.tobytes(), check=True)
        emprises[nom] = {'fichier': f'fonds/s2/{nom}.webp', 'lonlat': [bb[0], bb[1], bb[2], bb[3]], 'taille': [w, h], 'm_par_px': res,
                         'fondu_px': fondu, 'valide_pct': round(float(a.mean()) * 100, 1)}
        print(nom, w, 'x', h, 'valide', emprises[nom]['valide_pct'], '%', round(f.stat().st_size / 1e6, 1), 'Mo')
    emprises['_etirement'] = {'bas': float(bas), 'haut': float(haut), 'gamma': 0.92}
    (G / 'donnees').mkdir(exist_ok=True)
    (G / 'donnees' / 'emprises.json').write_text(json.dumps(emprises, indent=1), encoding='utf-8')


def simplifier(pts, tol_km):
    """Douglas–Peucker en plan local (km), itératif."""
    if len(pts) < 3: return pts
    la0 = math.radians(sum(p[1] for p in pts) / len(pts))
    xy = np.array([[p[0] * 111.32 * math.cos(la0), p[1] * 110.57] for p in pts])
    garde = np.zeros(len(pts), bool); garde[0] = garde[-1] = True; pile = [(0, len(pts) - 1)]
    while pile:
        i, j = pile.pop()
        if j <= i + 1: continue
        a, b = xy[i], xy[j]; d = b - a; L = np.hypot(*d) or 1e-9
        r = xy[i + 1:j] - a; e = np.abs(d[0] * r[:, 1] - d[1] * r[:, 0]) / L; k = int(np.argmax(e))
        if e[k] > tol_km: garde[i + 1 + k] = True; pile += [(i, i + 1 + k), (i + 1 + k, j)]
    return [pts[k] for k in range(len(pts)) if garde[k]]


def donnees():
    D = G / 'donnees'; D.mkdir(exist_ok=True)
    for f in ('oleoduc.geojson', 'alberta.geojson', 'lieux.json'):
        if (D / f).exists(): sys.exit('existe déjà : ' + str(D / f))
    # oléoduc : plus court chemin dans le réseau du pétrole, de la station 1 (bout le plus au nord) au terminal (le plus au sud)
    el = [e for e in json.load(open(D21, encoding='utf-8'))['elements'] if e.get('tags', {}).get('substance') == 'oil']
    cle = lambda p: (round(p['lon'], 7), round(p['lat'], 7))
    adj = {}
    for k, e in enumerate(el):
        g = [cle(p) for p in e['geometry']]; L = sum(km(g[i], g[i + 1]) for i in range(len(g) - 1))
        adj.setdefault(g[0], []).append((g[-1], L, k, 1)); adj.setdefault(g[-1], []).append((g[0], L, k, -1))
    deg = {p: len(v) for p, v in adj.items()}
    bouts = [p for p, n in deg.items() if n == 1]
    src, dst = max(bouts, key=lambda p: p[1]), min(bouts, key=lambda p: p[1])
    dist, prec, q = {src: 0.0}, {}, [(0.0, src)]
    while q:
        c, u = heapq.heappop(q)
        if c > dist[u]: continue
        for v, L, k, s in adj[u]:
            if c + L < dist.get(v, 1e18): dist[v] = c + L; prec[v] = (u, k, s); heapq.heappush(q, (c + L, v))
    chemin, u = [], dst
    while u != src:
        p, k, s = prec[u]; g = [cle(x) for x in el[k]['geometry']][::s]
        chemin = g[1:] + chemin if chemin else g; u = p
    chemin = [src] + chemin[1:] if chemin[0] != src else chemin
    simple = simplifier(chemin, 0.015)
    tot = sum(km(simple[i], simple[i + 1]) for i in range(len(simple) - 1))
    (D / 'oleoduc.geojson').write_text(json.dumps({'type': 'Feature', 'properties': {
        'nom': 'Trans-Alaska Pipeline System', 'de': 'station de pompage 1', 'vers': 'terminal de Valdez',
        'km_reseau': round(dist[dst], 1), 'km_simplifie': round(tot, 1), 'points': len(simple),
        'source': 'OpenStreetMap (D21, Overpass du 26/10/2026), © OpenStreetMap contributors, ODbL ; simplifié à 15 m'},
        'geometry': {'type': 'LineString', 'coordinates': [[round(a, 6), round(b, 6)] for a, b in simple]}}), encoding='utf-8')
    print('oléoduc', len(chemin), '→', len(simple), 'points ;', round(dist[dst], 1), 'km (réseau),', round(tot, 1), 'km (simplifié)')
    # Alberta
    ab = next(f for a, f in lire(D17, 'ne_10m_admin_1_states_provinces') if a.get('iso_3166_2') == 'CA-AB')
    (D / 'alberta.geojson').write_text(json.dumps({'type': 'Feature', 'properties': {'nom': 'Alberta', 'source': 'Natural Earth 1:10m (D17), domaine public'},
        'geometry': {'type': 'Polygon', 'coordinates': [[[round(x, 5), round(y, 5)] for x, y in r] for r in ab]}}), encoding='utf-8')
    # lieux
    voulus = {('Prudhoe Bay', 'Alaska'): 'prudhoe-bay', ('Valdez', 'Alaska'): 'valdez', ('Fairbanks', 'Alaska'): 'fairbanks',
              ('Anchorage', 'Alaska'): 'anchorage', ('Juneau', 'Alaska'): 'juneau', ('Edmonton', 'Alberta'): 'edmonton',
              ('Calgary', 'Alberta'): 'calgary', ('Fort McMurray', 'Alberta'): 'fort-mcmurray'}
    lieux = [{'id': 'station-1', 'nom': 'Pump Station 1', 'lonlat': list(src), 'source': 'D21 (OSM), début de la ligne'},
             {'id': 'terminal-valdez', 'nom': 'Valdez Marine Terminal', 'lonlat': list(dst), 'source': 'D21 (OSM), fin de la ligne'}]
    for a, f in lire(NE_LIEUX, 'ne_10m_populated_places'):
        i = voulus.get((a.get('NAME'), a.get('ADM1NAME')))
        if i: lieux.append({'id': i, 'nom': a['NAME'], 'lonlat': [round(f[0][0][0], 5), round(f[0][0][1], 5)], 'source': 'Natural Earth 10m populated places'})
    (D / 'lieux.json').write_text(json.dumps(lieux, indent=1, ensure_ascii=False), encoding='utf-8')
    print('lieux', [l['id'] for l in lieux])


def s2v2():
    """v2 de la vue 10 m (26/10/2026), seule employée par le globe. Sur la planche du vol 7.7 v1, la vue 40 m montrait le bord
    en diagonale de sa zone sans données dès le zoom 9,3, et la vue Sentinel était deux fois plus claire que le Blue Marble
    (luminance de la terre 0,39 contre 0,18) : un rectangle clair au recul. La v2 rapproche la teinte de la vue 10 m de celle du
    Blue Marble, à mi-chemin en échelle logarithmique et par bande, avec un contraste à 0,9. Le globe la fond pendant qu'elle couvre
    encore tout le cadre. La vue 40 m n'est plus employée."""
    f = G / 'fonds' / 's2' / 'prudhoe-10m-v2.webp'; fe = G / 'donnees' / 'emprises-v2.json'
    if f.exists() or fe.exists(): sys.exit('existe déjà : ' + str(f))
    E = json.loads((G / 'donnees' / 'emprises.json').read_text(encoding='utf-8'))['prudhoe-10m']; bb = E['lonlat']
    acc = []
    xs, ys = tuiles_xy(6, bb)
    for x in xs:
        for y in ys:
            a = decoder(G / 'fonds' / 'bm-v2' / '6' / str(x) / f'{y}.jpg').astype(np.float32) / 255
            lon, lat = tuile_lonlat(6, x, y)
            acc.append(a[(lon >= bb[0]) & (lon <= bb[2]) & (lat >= bb[1]) & (lat <= bb[3])])
    bmv = np.concatenate(acc); bm_terre = bmv[bmv[:, 2] < bmv[:, 1] * 1.05].mean(0)
    brut = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(G / E['fichier']), '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], capture_output=True, check=True).stdout
    w, h = E['taille']; s = np.frombuffer(brut, np.uint8).reshape(h, w, 4).astype(np.float32) / 255
    rgb, alpha = s[..., :3], s[..., 3]
    v = rgb[alpha > 0.99]; s_terre = v[v[:, 2] < v[:, 1] * 1.05].mean(0)
    cible = np.sqrt(s_terre * bm_terre)                                 # mi-chemin en échelle logarithmique, par bande
    x = np.clip((rgb - s_terre) * 0.9 * (cible / s_terre) + cible, 0, 1)
    rgba = np.dstack([(x * 255 + 0.5).astype(np.uint8), (alpha * 255 + 0.5).astype(np.uint8)])
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{w}x{h}', '-i', '-',
                    '-c:v', 'libwebp', '-quality', '90', '-pix_fmt', 'yuva420p', '-frames:v', '1', str(f)], input=rgba.tobytes(), check=True)
    E2 = dict(E, fichier='fonds/s2/prudhoe-10m-v2.webp', ton={'bm_terre': bm_terre.round(4).tolist(), 's2_terre': s_terre.round(4).tolist(),
              'cible': cible.round(4).tolist(), 'contraste': 0.9})
    fe.write_text(json.dumps({'prudhoe-10m-v2': E2}, indent=1), encoding='utf-8')
    print('prudhoe-10m-v2', w, 'x', h, 'BM', bm_terre.round(3), 'S2', s_terre.round(3), '→', cible.round(3), round(f.stat().st_size / 1e6, 1), 'Mo')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    {'bm': bm, 's2': s2, 's2v2': s2v2, 'donnees': donnees}[sys.argv[1]]()
