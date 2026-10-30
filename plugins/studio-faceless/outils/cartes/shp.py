"""Lecteur minimal de shapefile (polygones et lignes) et de sa table DBF, lus dans l'archive zip de Natural Earth.

Validé sur MM (Maps & Means), 26/10/2026 (cartes de l'épisode 004). Versé au plugin le 30/10/2026. Aucune bibliothèque SIG :
struct et zipfile seulement. Complète `cartes.py`, qui lit un .shp posé à côté de son .dbf (polygones seuls).
  lire(zip, 'ne_10m_admin_0_countries') -> [(attributs, [anneaux ou lignes : liste de (lon, lat)])]
Le nom est celui des fichiers dans l'archive, sans extension. Natural Earth est du domaine public ; le téléchargement
d'une archive se fait avec l'accord du propriétaire.
"""
import struct
import zipfile


def _dbf(b, encodage):
    n, lh, lr = struct.unpack('<IHH', b[4:12])
    champs, i = [], 32
    while b[i] != 0x0D:
        nom = b[i:i + 11].split(b'\0')[0].decode('ascii'); typ = chr(b[i + 11]); lg = b[i + 16]
        champs.append((nom, typ, lg)); i += 32
    lignes = []
    for k in range(n):
        o = lh + k * lr + 1; d = {}
        for nom, typ, lg in champs:
            v = b[o:o + lg].decode(encodage, 'replace').replace('\0', '').strip(); o += lg
            if typ in 'NF':
                try: v = float(v) if ('.' in v or 'e' in v.lower()) else int(v)
                except ValueError: v = None
            d[nom] = v
        lignes.append(d)
    return lignes


def _shp(b):
    formes, i = [], 100
    while i + 8 <= len(b):
        _, lg = struct.unpack('>II', b[i:i + 8]); c = b[i + 8:i + 8 + 2 * lg]; i += 8 + 2 * lg
        typ = struct.unpack('<i', c[:4])[0]
        if typ == 0: formes.append([]); continue
        if typ in (1, 11, 21): formes.append([[struct.unpack('<dd', c[4:20])]]); continue
        if typ not in (3, 5, 13, 15, 23, 25): raise ValueError('forme %d non prise en charge' % typ)
        np_, npt = struct.unpack('<ii', c[36:44])
        parts = list(struct.unpack('<%di' % np_, c[44:44 + 4 * np_])) + [npt]
        pts = struct.unpack('<%dd' % (2 * npt), c[44 + 4 * np_:44 + 4 * np_ + 16 * npt])
        xy = list(zip(pts[0::2], pts[1::2]))
        formes.append([xy[parts[k]:parts[k + 1]] for k in range(np_)])
    return formes


def lire(chemin_zip, nom):
    with zipfile.ZipFile(chemin_zip) as z:
        enc = 'utf-8'
        if nom + '.cpg' in z.namelist():
            enc = z.read(nom + '.cpg').decode('ascii').strip().lower().replace('utf8', 'utf-8') or 'utf-8'
        attrs = _dbf(z.read(nom + '.dbf'), enc)
        formes = _shp(z.read(nom + '.shp'))
    if len(attrs) != len(formes): raise ValueError('DBF et SHP de tailles différentes')
    return list(zip(attrs, formes))
