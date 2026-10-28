"""Cartes au trait SVG 1920 × 1080 et positions des villes, tirées de Natural Earth admin 0. Outil commun du studio (24/10/2026).

Repris de l'outil de cartes de l'E007 d'AA (cartes-v3.py, non modifié) et de sa carte d'Italie. Lecture directe
du shapefile (.shp et .dbf voisins), sans dépendance. Spécification JSON (une carte, une liste, ou {"cartes": [...]}) :
schéma et choix de projection dans ${CLAUDE_PLUGIN_ROOT}/outils/cartes/README.md.

Chaque carte : DOSSIER/<nom>/<nom>.svg (traits en currentColor, pays du récit en classe « focus » ou classe_pays, voisins en
« voisin ») et DOSSIER/<nom>/villes-px.json (positions des villes en pixels, projection, cadre de l'emprise et échelle).
Projections :
  - « equirectangulaire » (celle des cartes de l'E007 d'AA) : x = longitude × cos(lat_ref), y = latitude, même échelle sur les
    deux axes ; l'emprise est inscrite dans 1920 × 1080 et centrée (bandes vides si son rapport n'est pas 16:9) ;
  - « equal-earth » (Šavrič, Patterson et Jenny, 2018) : à aires égales, formes naturelles ; pour le monde.
Refuse d'écraser.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/cartes/cartes.py SPEC.json --shp CHEMIN/ne_50m_admin_0_countries.shp --out DOSSIER
"""
import argparse, json, math, os, struct, sys

W, H = 1920, 1080
A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796       # Equal Earth
M = math.sqrt(3) / 2


def lire(shp, champ='ADMIN'):
    """Noms (champ du .dbf) et polygones (liste d'anneaux de (lon, lat)) d'un shapefile de polygones."""
    base = shp[:-4] if shp.lower().endswith('.shp') else shp
    with open(base + '.dbf', 'rb') as f:
        h = f.read(32)
        n, hl, rl = struct.unpack('<IHH', h[4:12])
        champs = []
        while True:
            d = f.read(32)
            if d[0] == 0x0D:
                break
            champs.append((d[:11].split(b'\0')[0].decode(), d[16]))
        if champ not in [c for c, _ in champs]:
            sys.exit(f'Champ « {champ} » absent du .dbf ({", ".join(c for c, _ in champs[:12])}…)')
        f.seek(hl)
        noms = []
        for _ in range(n):
            r = f.read(rl)
            off, rec = 1, {}
            for nm, ln in champs:
                rec[nm] = r[off:off + ln].decode('utf-8', 'replace').replace('\x00', '').strip()
                off += ln
            noms.append(rec[champ])
    with open(base + '.shp', 'rb') as f:
        s = f.read()
    pos, polys = 100, []
    while pos < len(s):
        _, clen = struct.unpack('>ii', s[pos:pos + 8])
        c = s[pos + 8:pos + 8 + clen * 2]
        pos += 8 + clen * 2
        if struct.unpack('<i', c[:4])[0] != 5:
            polys.append([])
            continue
        np_, npt = struct.unpack('<ii', c[36:44])
        parts = list(struct.unpack('<%di' % np_, c[44:44 + 4 * np_]))
        p = struct.unpack('<%dd' % (2 * npt), c[44 + 4 * np_:44 + 4 * np_ + 16 * npt])
        p = [(p[2 * k], p[2 * k + 1]) for k in range(npt)]
        parts.append(npt)
        polys.append([p[parts[k]:parts[k + 1]] for k in range(np_)])
    return noms, polys


def equal_earth(lon, lat, lon0):
    lam, th = math.radians(lon - lon0), math.asin(M * math.sin(math.radians(lat)))
    t2 = th * th
    t6 = t2 * t2 * t2
    return lam * math.cos(th) / (M * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2))), th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))


def projection(sp):
    """Rend (P, description, infos) : P(lon, lat) → (x, y) en pixels arrondis au dixième, emprise inscrite et centrée."""
    (lon0, lon1), (lat1, lat2) = sp['emprise']['lon'], sp['emprise']['lat']
    pr = sp.get('projection', 'equirectangulaire')
    if pr == 'equirectangulaire':
        latref = float(sp.get('lat_ref', (lat1 + lat2) / 2))
        kx = math.cos(math.radians(latref))
        sc = min(W / ((lon1 - lon0) * kx), H / (lat2 - lat1))      # même calcul que cartes-v3.py (E007 d'AA)
        ox = (W - (lon1 - lon0) * kx * sc) / 2
        oy = (H - (lat2 - lat1) * sc) / 2
        P = lambda lo, la: (round(ox + (lo - lon0) * kx * sc, 1), round(oy + (lat2 - la) * sc, 1))
        desc = f'équirectangulaire cos({latref}°)'
        infos = {'px_par_degre': {'longitude': round(kx * sc, 3), 'latitude': round(sc, 3)}}
    elif pr == 'equal-earth':
        lc = float(sp.get('meridien_central', (lon0 + lon1) / 2))
        bord = [(lon0 + (lon1 - lon0) * i / 200, la) for i in range(201) for la in (lat1, lat2)] + \
               [(lo, lat1 + (lat2 - lat1) * i / 200) for i in range(201) for lo in (lon0, lon1)]
        xy = [equal_earth(lo, la, lc) for lo, la in bord]
        xmin, xmax = min(x for x, _ in xy), max(x for x, _ in xy)
        ymin, ymax = min(y for _, y in xy), max(y for _, y in xy)
        sc = min(W / (xmax - xmin), H / (ymax - ymin))
        ox, oy = (W - (xmax - xmin) * sc) / 2, (H - (ymax - ymin) * sc) / 2

        def P(lo, la):
            x, y = equal_earth(lo, la, lc)
            return round(ox + (x - xmin) * sc, 1), round(oy + (ymax - y) * sc, 1)
        desc = f'Equal Earth, méridien central {lc}°'
        infos = {'px_par_degre_au_centre': {'latitude': round(abs(P(lc, 0.5)[1] - P(lc, -0.5)[1]), 3)}}
    else:
        sys.exit(f'Projection inconnue : {pr} (equirectangulaire ou equal-earth)')
    infos['cadre_px'] = [round(ox, 1), round(oy, 1), round(W - ox, 1), round(H - oy, 1)]
    return P, desc, infos


def carte(sp, noms, polys, out, echelle):
    nom = sp['nom']
    (lon0, lon1), (lat1, lat2) = sp['emprise']['lon'], sp['emprise']['lat']
    focus, voisins = set(sp.get('pays', [])), sp.get('voisins')
    cf, cv = sp.get('classe_pays', 'focus'), sp.get('classe_voisins', 'voisin')
    pas_min = float(sp.get('pas_min', 0.0))
    for n in focus | set(voisins or []):
        if n not in noms:
            sys.exit(f'{nom} : pays « {n} » absent du shapefile')
    d_out = os.path.join(out, nom)
    svg_p, json_p = os.path.join(d_out, nom + '.svg'), os.path.join(d_out, 'villes-px.json')
    for p in (svg_p, json_p):
        if os.path.exists(p):
            sys.exit('Sortie existante, aucun écrasement : ' + p)
    P, desc, infos = projection(sp)
    lignes = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
              f'<!-- Natural Earth {echelle} admin 0 (domaine public) ; {desc}, lon {lon0}–{lon1}, lat {lat1}–{lat2} ; '
              f'outils/cartes/cartes.py. -->']
    n_pays = 0
    for nm, rings in zip(noms, polys):
        if not rings:
            continue
        if voisins is not None:              # liste fermée : le récit et ses voisins nommés
            if nm not in focus and nm not in voisins:
                continue
        else:                                # tous les pays dont l'emprise touche le cadre (marge de 2°)
            xs = [x for r in rings for x, _ in r]
            ys = [y for r in rings for _, y in r]
            if max(xs) < lon0 - 2 or min(xs) > lon1 + 2 or max(ys) < lat1 - 2 or min(ys) > lat2 + 2:
                continue
        cls = cf if nm in focus else cv
        d = []
        for r in rings:
            pts, last = [], None
            for lo, la in r:
                q = P(lo, la)
                if last is None or abs(q[0] - last[0]) + abs(q[1] - last[1]) >= pas_min:
                    pts.append(q)
                    last = q
            if len(pts) >= 3:
                d.append('M' + ' L'.join('%s %s' % q for q in pts) + ' Z')
        if d:
            n_pays += 1
            lignes.append(f'<path id="{cls}-{nm.lower().replace(" ", "-")}" class="{cls}" d="{" ".join(d)}" fill="none" '
                          f'stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>')
    px = {k: P(*v) for k, v in sp.get('villes', {}).items()}
    lignes += [f'<circle id="ville-{k}" cx="{x}" cy="{y}" r="7" fill="currentColor"/>' for k, (x, y) in px.items()]
    lignes.append('</svg>')
    os.makedirs(d_out, exist_ok=True)
    with open(svg_p, 'x', encoding='utf-8') as f:
        f.write('\n'.join(lignes))
    with open(json_p, 'x', encoding='utf-8') as f:
        json.dump({'source': f'Natural Earth {echelle} admin 0 countries (domaine public)',
                   'projection': f'{desc}, lon {lon0}–{lon1}, lat {lat1}–{lat2}, {W}×{H}', **infos, 'villes_px': px},
                  f, ensure_ascii=False, indent=1)
    print(nom, f'{n_pays} pays,', os.path.getsize(svg_p) // 1024, 'Ko,', 'cadre', infos['cadre_px'], px)


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description='Cartes au trait SVG depuis Natural Earth (outils/cartes/README.md).')
    ap.add_argument('spec', help='spécification JSON (une carte, une liste, ou {"cartes": [...]})')
    ap.add_argument('--shp', required=True, help='shapefile Natural Earth admin 0 (.shp ; le .dbf est à côté)')
    ap.add_argument('--out', required=True, help='dossier où créer un sous-dossier par carte')
    a = ap.parse_args()
    with open(a.spec, encoding='utf-8') as f:
        spec = json.load(f)
    cartes = spec if isinstance(spec, list) else spec.get('cartes', [spec])
    champs = {sp.get('champ_nom', 'ADMIN') for sp in cartes}
    b = os.path.basename(a.shp).lower()
    echelle = next((f'1:{e}m' for e in ('10', '50', '110') if f'_{e}m_' in b), '')
    donnees = {c: lire(a.shp, c) for c in champs}
    for sp in cartes:
        carte(sp, *donnees[sp.get('champ_nom', 'ADMIN')], a.out, echelle)


if __name__ == '__main__':
    main()
