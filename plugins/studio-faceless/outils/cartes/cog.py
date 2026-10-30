"""Lit un niveau (ou une zone) d'un COG RVB 8 bits en tuiles (DEFLATE, prédicteur 1 ou 2), sans bibliothèque SIG.

Validé sur MM (Maps & Means), 26/10/2026 (image Sentinel-2 des cartes de l'épisode 004). Versé au plugin le 30/10/2026.
Écrit un PPM (P6) ; refuse d'écraser. Niveau 0 = pleine définition, 1, 2… = vues réduites du COG.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/cartes/cog.py TIF NIVEAU SORTIE.ppm [x0 y0 l h]
"""
import struct, sys, zlib, os
import numpy as np
def ifds(chemin):
    f = open(chemin, 'rb'); t = f.read(8); bo = '<' if t[:2] == b'II' else '>'
    off = struct.unpack(bo + 'I', t[4:8])[0]; res = []
    T = {3: ('H', 2), 4: ('I', 4)}
    while off:
        f.seek(off); n = struct.unpack(bo + 'H', f.read(2))[0]; d = {}
        for _ in range(n):
            tag, typ, cnt, val = struct.unpack(bo + 'HHI4s', f.read(12))
            if typ not in T: continue
            c, s = T[typ]; sz = s * cnt
            if sz <= 4: brut = val[:sz]
            else:
                p = f.tell(); f.seek(struct.unpack(bo + 'I', val)[0]); brut = f.read(sz); f.seek(p)
            d[tag] = struct.unpack(bo + c * cnt, brut)
        off = struct.unpack(bo + 'I', f.read(4))[0]; res.append(d)
    return f, res
def lire(chemin, niveau, zone=None):
    f, L = ifds(chemin); d = L[niveau]
    w, h, tw, th = d[256][0], d[257][0], d[322][0], d[323][0]
    pred = d.get(317, (1,))[0]
    x0, y0, l, hh = zone or (0, 0, w, h)
    out = np.zeros((hh, l, 3), np.uint8)
    nx = (w + tw - 1) // tw
    for ty in range(y0 // th, (y0 + hh - 1) // th + 1):
        for tx in range(x0 // tw, (x0 + l - 1) // tw + 1):
            i = ty * nx + tx; f.seek(d[324][i]); b = zlib.decompress(f.read(d[325][i]))
            a = np.frombuffer(b, np.uint8).reshape(th, tw, 3)
            if pred == 2: a = np.cumsum(a, axis=1, dtype=np.uint8)
            ax, ay = tx * tw, ty * th
            sx0, sy0 = max(x0, ax), max(y0, ay); sx1, sy1 = min(x0 + l, ax + tw, w), min(y0 + hh, ay + th, h)
            out[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = a[sy0 - ay:sy1 - ay, sx0 - ax:sx1 - ax]
    return out
if __name__ == '__main__':
    if len(sys.argv) < 4 or sys.argv[1] in ('-h', '--help'):
        sys.stdout.reconfigure(encoding='utf-8'); print(__doc__)
        sys.exit(0 if len(sys.argv) > 1 else 2)
    tif, niv, sortie = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    zone = tuple(map(int, sys.argv[4:8])) if len(sys.argv) > 4 else None
    if os.path.exists(sortie): sys.exit('existe déjà')
    a = lire(tif, niv, zone)
    with open(sortie, 'xb') as o: o.write(b'P6\n%d %d\n255\n' % (a.shape[1], a.shape[0])); o.write(a.tobytes())
    print(sortie, a.shape, 'moyenne', a.reshape(-1, 3).mean(0).round(1))
