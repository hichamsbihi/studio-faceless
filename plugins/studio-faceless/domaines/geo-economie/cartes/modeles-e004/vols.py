"""Vols de caméra du globe de l'épisode 004, réglés sur la voix figée (kit/voix/finale-v2/reperes/).
Round « globe et cinématique » (`VALIDÉ`, Hicham, 26/10/2026) : un seul mouvement par moment de carte, adouci, sans zoom suivi
d'un dézoom ; inclinaison 45° au plus.
  python -I -B kit/cartes/outils/vols.py      → kit/cartes/globe/vols/<nom>.json (jamais d'écrasement)
Chaque vol a une clé par image (« lineaire ») : le mouvement est calculé ici, d'un seul tenant, et capturer.mjs ne fait que le suivre.
`debut_sequence` : l'instant de la séquence où le producteur pose le MP4 (temps local de la séquence, en secondes)."""
import json, math, sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
G = ICI.parent / 'globe'
sys.path.insert(0, str(ICI))
from proj import km  # noqa: E402

FPS = 30


def lisse(u):
    u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)


def cos_ease(u):
    u = min(1.0, max(0.0, u)); return 0.5 - 0.5 * math.cos(math.pi * u)


def slerp(a, b, s):
    r = math.pi / 180
    v = lambda p: (math.cos(p[1] * r) * math.cos(p[0] * r), math.cos(p[1] * r) * math.sin(p[0] * r), math.sin(p[1] * r))
    p, q = v(a), v(b); w = math.acos(max(-1.0, min(1.0, sum(x * y for x, y in zip(p, q)))))
    if w < 1e-9: return list(a)
    s1, s2 = math.sin((1 - s) * w) / math.sin(w), math.sin(s * w) / math.sin(w)
    x, y, z = (s1 * p[i] + s2 * q[i] for i in range(3))
    return [math.atan2(y, x) / r, math.atan2(z, math.hypot(x, y)) / r]


def cam(c, z, p, b):
    return {'center': [round(c[0], 6), round(c[1], 6)], 'zoom': round(z, 5), 'pitch': round(p, 4), 'bearing': round(b, 4)}


# --- 2.8 : plongée du Pacifique Nord sur l'Alaska, arrivée calée au pixel sur la carte papier (Q3) ----------------------------
# S2 : « The oil only reached the port of Valdez, » 50,79–53,3 ; « eight hundred miles » dès 53,34. Le fondu vers la feuille
# (0,6 s, Q5) se fait sur l'arrivée tenue, de 53,2 à 53,8.
FIN_2_8 = ([-148.79629, 64.45442], 4.507, 0.0, 4.44)     # réglée sur captures : station 1 et terminal à 0,3 px de la carte papier


def vol_2_8():
    cles = []
    for f in range(int(round(3.2 * FPS))):
        t = f / FPS; u = min(1.0, t / 2.5); s = 1 - (1 - u) ** 3            # départ déjà lancé (coupe franche depuis P15), arrivée douce
        c = slerp([-170.0, 40.0], FIN_2_8[0], s)
        cles.append({'t': t, 'ease': 'lineaire', 'camera': cam(c, 2.0 + (FIN_2_8[1] - 2.0) * s, 22 * math.sin(math.pi * s), -20 + (FIN_2_8[3] + 20) * s)})
    return {'nom': 's2-plongee', 'sequence': 'S2', 'plan': '2.8', 'debut_sequence': 50.60, 'vue': 'alaska', 'fps': FPS, 'duree': 3.2, 'cles': cles,
            'note': 'arrivée tenue de 2,5 à 3,2 s : image identique à la carte papier pour le fondu de 0,6 s'}


# --- 5.3 : au-dessus de l'Alaska, puis montée, rotation vers l'est, descente sur l'Alberta ------------------------------------
# S5 : « Can a check really protect a fund? » 29,71–32,0 ; « Look east, » 32,62 ; « Alberta, » 33,39 ; « province. » 35,51 ; 5.4 à 36,62.
def vol_5_3():
    cles, D = [], 29.60
    for f in range(int(round(6.9 * FPS))):
        t = f / FPS
        d1 = min(1.0, t / 2.9); s = lisse((t - 2.9) / 3.0); d2 = min(1.0, max(0.0, (t - 5.9) / 1.0))
        a = [-150.5 + 1.2 * d1, 63.8 - 0.2 * d1]; b = [-114.4 + 0.25 * d2, 54.4 + 0.05 * d2]
        z = (4.40 - 0.12 * d1) * (1 - s) + (4.95 + 0.05 * d2) * s - 0.75 * math.sin(math.pi * s)
        p = (10 + 4 * d1) * (1 - s) + 38 * s; br = 2 * (1 - s) + (12 + 1 * d2) * s
        cles.append({'t': t, 'ease': 'lineaire', 'camera': cam(slerp(a, b, s), z, p, br), 'calques': ['alberta'],
                     'alberta': round(lisse((t + D - 33.39 - 0.2) / 1.0), 4)})
    return {'nom': 's5-vers-alberta', 'sequence': 'S5', 'plan': '5.3', 'debut_sequence': D, 'vue': 'alaska', 'fps': FPS, 'duree': 6.9, 'cles': cles,
            'note': "dérive lente sur la question, voyage de 2,9 à 5,9 s (« Look east »), l'Alberta s'allume sur son nom"}


# --- 7.7 : vue Sentinel de Prudhoe Bay, recul, l'oléoduc s'allume vers le sud, orbite --------------------------------------
# S7 : « Look at the map one last time. » 51,29–53,69 ; « Oil flows south through eight hundred miles of pipe. » 53,82–56,8 ;
# « Money » 57,43 : fondu vers le monde papier (Q1, Q6), fait par le producteur pendant la fin du vol.
def vol_7_7():
    ligne = json.load(open(G / 'donnees' / 'oleoduc.geojson', encoding='utf-8'))['geometry']['coordinates']
    cum = [0.0]
    for i in range(1, len(ligne)): cum.append(cum[-1] + km(ligne[i - 1], ligne[i]))
    L = cum[-1]
    # même mesure que couper() de carte.html (degrés, latitude × 2,2), pour passer d'une distance en km à la fraction tracée
    deg = [0.0]
    for i in range(1, len(ligne)): deg.append(deg[-1] + math.hypot(ligne[i][0] - ligne[i - 1][0], (ligne[i][1] - ligne[i - 1][1]) * 2.2))

    def point_a(dkm):
        i = next((k for k in range(1, len(cum)) if cum[k] >= dkm), len(cum) - 1)
        u = (dkm - cum[i - 1]) / ((cum[i] - cum[i - 1]) or 1)
        return [ligne[i - 1][0] + (ligne[i][0] - ligne[i - 1][0]) * u, ligne[i - 1][1] + (ligne[i][1] - ligne[i - 1][1]) * u], deg[i - 1] + (deg[i] - deg[i - 1]) * u

    cles, D = [], 51.10
    P0, ORB = [-148.30, 70.138], [-141.0, 57.0]
    for f in range(int(round(7.0 * FPS))):
        t = f / FPS
        d = min(1.0, t / 2.7); p0 = [P0[0] + 0.03 * d, P0[1] - 0.004 * d]            # dérive latérale, sans zoom
        e = cos_ease((t - 2.7) / 4.3)
        z = 10.57 * (1 - e) + 2.35 * e
        H = 1.08 * 19.8 * 2 ** (10.57 - z)                                        # hauteur du cadre, en km (approchée)
        dist = min(L, 0.85 * H * lisse((t - 2.72) / 0.6)) if t >= 2.72 else 0.0
        m, _ = point_a(dist / 2); _, dtrace = point_a(dist)
        c = slerp(slerp(p0, m, lisse((t - 2.7) / 1.0)), ORB, lisse((t - 5.4) / 1.6))
        cles.append({'t': t, 'ease': 'lineaire', 'camera': cam(c, z, 30 * (1 - lisse((t - 2.7) / 2.8)), 2 * d * (1 - lisse((t - 2.7) / 3.1))),
                     'traces': {'oleoduc': round(dtrace / deg[-1], 6) if dist > 0 else 0.0}})
    return {'nom': 's7-prudhoe-orbite', 'sequence': 'S7', 'plan': '7.7', 'debut_sequence': D, 'vue': 'prudhoe', 'fps': FPS, 'duree': 7.0, 'cles': cles,
            'note': "Sentinel-2 de 0 à environ 3,4 s (crédit 2D « Contains modified Copernicus Sentinel data 2025 » tant que la vue D22 se voit, puis « NASA Blue Marble ») ; oléoduc tracé de 2,7 à environ 5,9 s"}


def vol_7_7_v2():
    """v2 (26/10/2026) : sur la planche de la v1, le centre remontait vers le nord-ouest au début du recul (vers la station 1),
    et le haut du cadre sortait de la vue Sentinel (bande sombre). Ici, le centre ne suit le tracé qu'au sud de sa latitude de
    départ ; il glisse donc vers l'ouest, sur l'oléoduc, puis descend avec lui. Le reste est identique à la v1."""
    v = vol_7_7()
    ligne = json.load(open(G / 'donnees' / 'oleoduc.geojson', encoding='utf-8'))['geometry']['coordinates']
    cum = [0.0]
    for i in range(1, len(ligne)): cum.append(cum[-1] + km(ligne[i - 1], ligne[i]))
    d0 = next(cum[k] for k in range(len(ligne)) if ligne[k][1] <= 70.138)          # point du tracé à la latitude de départ
    def point_a(dkm):
        i = next((k for k in range(1, len(cum)) if cum[k] >= dkm), len(cum) - 1)
        u = (dkm - cum[i - 1]) / ((cum[i] - cum[i - 1]) or 1)
        return [ligne[i - 1][0] + (ligne[i][0] - ligne[i - 1][0]) * u, ligne[i - 1][1] + (ligne[i][1] - ligne[i - 1][1]) * u]
    P0, ORB, L = [-148.30, 70.138], [-141.0, 57.0], cum[-1]
    for k in v['cles']:
        t = k['t']; d = min(1.0, t / 2.7); p0 = [P0[0] + 0.03 * d, P0[1] - 0.004 * d]
        e = cos_ease((t - 2.7) / 4.3); z = 10.57 * (1 - e) + 2.35 * e
        H = 1.08 * 19.8 * 2 ** (10.57 - z)
        dist = min(L, 0.85 * H * lisse((t - 2.72) / 0.6)) if t >= 2.72 else 0.0
        m = point_a(max(dist / 2, d0))
        c = slerp(slerp(p0, m, lisse((t - 2.7) / 1.0)), ORB, lisse((t - 5.4) / 1.6))
        k['camera']['center'] = [round(c[0], 6), round(c[1], 6)]
    v['nom'] = 's7-prudhoe-orbite-v2'
    v['note'] = ("Sentinel-2 (vue 10 m v2) de 0 à environ 3,7 s, fondue entre 3,36 et 3,71 s (crédit 2D « Contains modified Copernicus "
                 "Sentinel data 2025 » jusqu'à 3,7 s, puis « NASA Blue Marble ») ; oléoduc tracé de 2,7 à environ 5,9 s")
    return v


# --- 1.1 v2 : de la Terre entière à l'Alaska, puis plongée vers la côte sud (S1 v2, proposition B « Vu d'en haut »,
# VALIDÉE par Hicham le 26/10/2026, sans globe final). Voix v3 (kit/voix/finale-v3/reperes/seq1-mots.json) : « Every » 2,46 ;
# « Alaskans » 5,09 (« ALASKA » posé en 2D à 4,96) ; la coupe en zoom traversant vers V21 se fait de 5,1 à 5,6 s.
# Un seul mouvement : le zoom ne fait qu'accélérer (u²), le centre tourne plus tôt (lisse), l'inclinaison vient à la fin.
def vol_1_1():
    cles = []
    for f in range(int(round(5.6 * FPS))):
        t = f / FPS; u = t / 5.6
        c = slerp([-128.0, 32.0], [-150.8, 60.6], lisse(u / 0.85))
        z = 1.05 + (6.2 - 1.05) * u * u
        cles.append({'t': t, 'ease': 'lineaire', 'camera': cam(c, z, 32 * lisse((t - 3.8) / 1.8), 0.0)})
    return {'nom': 's1-approche', 'sequence': 'S1', 'plan': '1.1 (v2)', 'debut_sequence': 0.0, 'vue': 'pacifique', 'fps': FPS, 'duree': 5.6,
            'cles': cles, 'note': "Terre entière à 0 s ; l'Alaska remplit le cadre vers 4,9 s ; plongée accélérée jusqu'à la coupe vers V21 (5,1–5,6 s)"}


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    (G / 'vols').mkdir(exist_ok=True)
    tous = (vol_2_8(), vol_5_3(), vol_7_7(), vol_7_7_v2(), vol_1_1())
    voulus = sys.argv[1:]                     # noms à écrire (par défaut, tous ceux qui manquent)
    for v in tous:
        if voulus and v['nom'] not in voulus: continue
        f = G / 'vols' / f"{v['nom']}.json"
        if f.exists(): print('existe déjà, gardé :', f.name); continue
        f.write_text(json.dumps(v), encoding='utf-8')
        c0, c1 = v['cles'][0]['camera'], v['cles'][-1]['camera']
        print(f"{v['nom']} : {len(v['cles'])} images ; zoom {c0['zoom']} → {c1['zoom']} ; pose à {v['debut_sequence']} s de {v['sequence']}")
