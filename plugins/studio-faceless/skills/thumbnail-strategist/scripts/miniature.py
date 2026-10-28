#!/usr/bin/env python3
"""Miniatures de la chaîne : rendu, mesure, planche, grille de détourage, contraste.

Bibliothèque standard Python seulement. Les captures passent par le Chrome sans fenêtre déjà
téléchargé par HyperFrames (rien n'est installé ni téléchargé) ; `contraste --image` lit les
pixels avec ffmpeg. Aucun écrasement : chaque fichier de sortie doit être nouveau et son dossier
doit déjà exister. Lancer avec `python -B`. Mode d'emploi : references/fabrication.md et
references/controles.md.

  python -B miniature.py rendu SOURCE.html SORTIE.png
  python -B miniature.py mesure IMAGE [IMAGE...]
  python -B miniature.py planche SORTIE.png IMAGE [IMAGE...] [--flux DOSSIER]
  python -B miniature.py grille PHOTO SORTIE.png [--zone x,y,l,h] [--echelle 1] [--pas 50] [--polygone P]
  python -B miniature.py contraste #TEXTE #FOND
  python -B miniature.py contraste #TEXTE --image IMAGE --zone x,y,l,h
"""
import argparse
import html
import math
import os
import re
import statistics
import struct
import subprocess
import sys
from pathlib import Path

LARGEUR, HAUTEUR = 1280, 720
POIDS_MAX = 2_000_000  # « under 2MB » (aide YouTube 72431), compté en octets décimaux par prudence
FONDS = (('Fond clair', '#FFFFFF', '#0F0F0F'), ('Fond sombre', '#0F0F0F', '#F1F1F1'))  # fonds de YouTube


def sortir(msg, code=1):
    print(msg)
    sys.exit(code)


def nouveau(p):
    p = Path(p).resolve()
    if p.exists():
        sortir(f'refus : {p} existe déjà (aucun écrasement)')
    if not p.parent.is_dir():
        sortir(f'refus : le dossier {p.parent} n\'existe pas (le créer d\'abord, après vérification)')
    return p


def chrome():
    env = os.environ.get('HYPERFRAMES_BROWSER_PATH')
    if env and os.path.isfile(env):
        return env
    base = Path.home() / '.cache' / 'hyperframes' / 'chrome' / 'chrome-headless-shell'
    exe = sorted(p for p in base.glob('*/chrome-headless-shell-*/chrome-headless-shell*') if p.suffix.lower() in ('.exe', ''))
    if not exe:
        sortir(f'Chrome de HyperFrames introuvable sous {base} : ne rien télécharger sans accord du propriétaire')
    return str(exe[-1])


def capturer(page, sortie, l, h):
    cmd = [chrome(), '--headless', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
           '--allow-file-access-from-files', f'--window-size={l},{h}', '--virtual-time-budget=10000',
           f'--screenshot={sortie}', Path(page).resolve().as_uri()]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    except subprocess.TimeoutExpired:
        sortir('échec : Chrome a dépassé 120 s (vérifier qu\'aucun chrome-headless-shell ne reste ouvert)')
    if not Path(sortie).is_file():
        sortir('échec de capture')


def dimensions(p):
    b = Path(p).read_bytes()
    if b[:8] == b'\x89PNG\r\n\x1a\n':
        return ('PNG',) + struct.unpack('>II', b[16:24])
    if b[:6] in (b'GIF87a', b'GIF89a'):
        return ('GIF',) + struct.unpack('<HH', b[6:10])
    if b[:2] == b'\xff\xd8':
        i = 2
        while i + 9 < len(b):
            if b[i] != 0xFF:
                i += 1
                continue
            m = b[i + 1]
            if m == 0xFF:
                i += 1
            elif m in (0x01, 0xD8) or 0xD0 <= m <= 0xD7:
                i += 2
            elif 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                h, l = struct.unpack('>HH', b[i + 5:i + 9])
                return ('JPEG', l, h)
            else:
                i += 2 + struct.unpack('>H', b[i + 2:i + 4])[0]
    return (None, 0, 0)


def mesurer(images):
    ok_tout = True
    for img in images:
        p = Path(img)
        if not p.is_file():
            print(f'{img} : introuvable')
            ok_tout = False
            continue
        fmt, l, h = dimensions(p)
        poids = p.stat().st_size
        tests = [
            ('format', fmt in ('PNG', 'JPEG'), fmt or 'inconnu'),
            ('taille', l >= LARGEUR and h >= HAUTEUR, f'{l}x{h}'),
            ('16:9', h > 0 and abs(l / h - 16 / 9) < 0.01, f'{l / h:.3f}' if h else '-'),
            ('poids < 2 Mo', poids < POIDS_MAX, f'{poids / 1e6:.2f} Mo'),
        ]
        ok = all(t[1] for t in tests)
        ok_tout &= ok
        detail = ' ; '.join(f'{n} {"OK" if v else "ÉCHEC"} ({x})' for n, v, x in tests)
        print(f'{p.name} : {"OK" if ok else "ÉCHEC"} — {detail}')
    return ok_tout


def vignette(uri, l, h, rayon):
    return (f'<div class="v" style="width:{l}px;height:{h}px;border-radius:{rayon}px">'
            f'<img src="{uri}" alt=""><span class="d">12:34</span></div>')


STYLE = ('body{margin:0;font:13px/1.3 Arial,sans-serif}'
         '.p{padding:20px 24px}.t{font-weight:700;margin:0 0 12px}'
         '.r{display:flex;gap:24px;flex-wrap:nowrap}.c{display:flex;flex-direction:column;gap:6px}'
         '.s{display:flex;gap:12px;align-items:flex-start}'
         '.v{position:relative;overflow:hidden;flex:none;background:#777}'
         '.v img{width:100%;height:100%;object-fit:cover;display:block}'
         '.d{position:absolute;right:4px;bottom:4px;background:rgba(0,0,0,.8);color:#fff;'
         'font:500 12px/1 Arial,sans-serif;padding:3px 4px;border-radius:4px}'
         '.g{display:grid;grid-template-columns:repeat(4,320px);gap:16px 16px}'
         '.b{height:10px;border-radius:5px;margin-top:8px;opacity:.25}')


def planche(sortie, images, flux):
    sortie = nouveau(sortie)
    page = nouveau(sortie.with_suffix('.html'))
    nos = [Path(i).resolve() for i in images]
    for p in nos:
        if not p.is_file():
            sortir(f'{p} : introuvable')
    corps, l_page, h_page = [], 0, 0
    if flux:
        voisines = sorted(p.resolve() for p in Path(flux).iterdir()
                          if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp'))
        if not voisines:
            sortir(f'{flux} : aucune miniature de la niche (jpg, png, webp)')
        total = len(voisines) + len(nos)
        rangs = [int((k + 0.5) * total / len(nos)) for k in range(len(nos))]  # distincts : pas >= 1
        it_nos, it_vois = iter(nos), iter(voisines)
        liste = [next(it_nos) if i in rangs else next(it_vois) for i in range(total)]
        lignes = math.ceil(total / 4)
        for titre, fond, texte in FONDS:
            cases = ''.join(f'<div>{vignette(p.as_uri(), 320, 180, 10)}'
                            f'<div class="b" style="background:{texte};width:92%"></div>'
                            f'<div class="b" style="background:{texte};width:55%"></div></div>' for p in liste)
            corps.append(f'<div class="p" style="background:{fond};color:{texte}"><p class="t">{titre} — flux '
                         f'(analyse interne)</p><div class="g">{cases}</div><p>Nos variantes : n° '
                         f'{", ".join(str(r + 1) for r in rangs)} (de gauche à droite, de haut en bas)</p></div>')
        l_page, h_page = 48 + 4 * 320 + 3 * 16, 2 * (40 + lignes * (180 + 52) + 56)
        print(f'flux : {len(voisines)} voisines, nos variantes aux rangs {[r + 1 for r in rangs]}')
    else:
        for titre, fond, texte in FONDS:
            cellules = ''.join(f'<div class="c"><div class="s">{vignette(p.as_uri(), 320, 180, 10)}'
                               f'{vignette(p.as_uri(), 168, 94, 8)}</div><span>{html.escape(p.name[:70])}</span></div>'
                               for p in nos)
            corps.append(f'<div class="p" style="background:{fond};color:{texte}"><p class="t">{titre} — '
                         f'320×180 et 168×94, durée simulée en bas à droite</p><div class="r">{cellules}</div></div>')
        l_page, h_page = 48 + len(nos) * 500 + (len(nos) - 1) * 24, 2 * (40 + 180 + 30 + 40)
    page.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{STYLE}</style></head>'
                    f'<body>{"".join(corps)}</body></html>', encoding='utf-8')
    capturer(page, sortie, l_page, h_page)
    print(f'planche : {sortie} ({l_page}x{h_page}) ; source : {page.name}')


def lire_polygone(arg):
    p = Path(arg)
    texte = p.read_text(encoding='utf-8') if p.is_file() else arg
    if p.suffix.lower() in ('.html', '.htm'):
        trouves = re.findall(r'clip-path\s*:\s*polygon\(([^)]*)\)', texte)
        if not trouves:
            sortir(f'{arg} : aucun clip-path: polygon(...)')
        if len(trouves) > 1:
            print(f'{len(trouves)} polygones trouvés : le premier est utilisé')
        texte = trouves[0]
    if '%' in texte:
        sortir('polygone en % non pris en charge : coordonnées en px, photo affichée à sa taille naturelle')
    pts = [(float(a), float(b)) for a, b in re.findall(r'(-?\d+(?:\.\d+)?)(?:px)?\s+(-?\d+(?:\.\d+)?)(?:px)?', texte)]
    if len(pts) < 3:
        sortir('polygone : moins de 3 points lus')
    return pts


def grille(photo, sortie, zone, echelle, pas, polygone):
    sortie = nouveau(sortie)
    page = nouveau(sortie.with_suffix('.html'))
    photo = Path(photo).resolve()
    fmt, L, H = dimensions(photo)
    if not fmt:
        sortir(f'{photo} : format non reconnu (PNG, JPEG)')
    x, y, l, h = [int(v) for v in zone.split(',')] if zone else (0, 0, L, H)
    s = echelle
    lp, hp = round(l * s), round(h * s)
    if max(lp, hp) > 4000:
        sortir(f'capture trop grande ({lp}x{hp}) : réduire --zone ou --echelle')
    uri = photo.as_uri()
    pts = lire_polygone(polygone) if polygone else None
    el = []
    if pts:
        liste = ' '.join(f'{a:g},{b:g}' for a, b in pts)
        el.append(f'<defs><clipPath id="cp"><polygon points="{liste}"/></clipPath></defs>'
                  f'<image href="{uri}" width="{L}" height="{H}" opacity=".3"/>'
                  f'<image href="{uri}" width="{L}" height="{H}" clip-path="url(#cp)"/>')
    else:
        el.append(f'<image href="{uri}" width="{L}" height="{H}"/>')
    ecr = f'font-size="{11 / s:g}" fill="#fff" stroke="#000" stroke-width="{3 / s:g}" paint-order="stroke"'
    for gx in range(math.ceil(x / pas) * pas, x + l + 1, pas):
        fort = gx % (2 * pas) == 0
        el.append(f'<line x1="{gx}" y1="{y}" x2="{gx}" y2="{y + h}" stroke="#00E5FF" stroke-width="{1.5 if fort else 1}" '
                  f'opacity="{.9 if fort else .45}" vector-effect="non-scaling-stroke"/>')
        if fort:
            el.append(f'<text x="{gx + 2 / s:g}" y="{y + 12 / s:g}" {ecr}>{gx}</text>')
    for gy in range(math.ceil(y / pas) * pas, y + h + 1, pas):
        fort = gy % (2 * pas) == 0
        el.append(f'<line x1="{x}" y1="{gy}" x2="{x + l}" y2="{gy}" stroke="#00E5FF" stroke-width="{1.5 if fort else 1}" '
                  f'opacity="{.9 if fort else .45}" vector-effect="non-scaling-stroke"/>')
        if fort:
            el.append(f'<text x="{x + 2 / s:g}" y="{gy - 2 / s:g}" {ecr}>{gy}</text>')
    if pts:
        el.append(f'<polygon points="{liste}" fill="none" stroke="#FF2D2D" stroke-width="2" vector-effect="non-scaling-stroke"/>')
        for i, (a, b) in enumerate(pts):
            el.append(f'<circle cx="{a:g}" cy="{b:g}" r="{3 / s:g}" fill="#FF2D2D"/>')
            if i % 5 == 0:
                el.append(f'<text x="{a + 5 / s:g}" y="{b - 5 / s:g}" font-size="{10 / s:g}" fill="#FFE600" '
                          f'stroke="#000" stroke-width="{3 / s:g}" paint-order="stroke">{i}</text>')
    page.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0;background:#808080;'
                    f'font-family:Arial,sans-serif}}svg{{display:block}}</style></head><body>'
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="{lp}" height="{hp}" viewBox="{x} {y} {l} {h}">'
                    f'{"".join(el)}</svg></body></html>', encoding='utf-8')
    capturer(page, sortie, lp, hp)
    extra = f' ; polygone de {len(pts)} points' if pts else ''
    print(f'grille : {sortie} ; photo {L}x{H}, zone {x},{y},{l},{h}, échelle {s:g}, pas {pas}{extra}')


def luminance(rgb):
    c = [v / 255 for v in rgb]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def rapport(l1, l2):
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def hexa(v):
    m = re.fullmatch(r'#?([0-9a-fA-F]{6})', v)
    if not m:
        sortir(f'couleur illisible : {v} (format #RRGGBB)')
    return tuple(int(m.group(1)[i:i + 2], 16) for i in (0, 2, 4))


def verdict(r):
    return 'bon' if r >= 4.5 else ('limite : gros texte seulement' if r >= 3 else 'insuffisant')


def contraste(texte, fond, image, zone):
    lt = luminance(hexa(texte))
    if fond:
        r = rapport(lt, luminance(hexa(fond)))
        print(f'contraste {texte} / {fond} : {r:.2f}:1 ({verdict(r)})')
        return
    if not (image and zone):
        sortir('donner une couleur de fond, ou --image et --zone')
    x, y, l, h = [int(v) for v in zone.split(',')]
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(image), '-vf', f'crop={l}:{h}:{x}:{y}', '-frames:v', '1',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
    px = out.stdout
    if out.returncode or len(px) < 3:
        sortir('ffmpeg : lecture de la zone impossible')
    rs = sorted(rapport(lt, luminance(px[i:i + 3])) for i in range(0, len(px) - 2, 3))
    pire = rs[int(0.05 * (len(rs) - 1))]
    print(f'contraste {texte} sur la zone {zone} : médiane {statistics.median(rs):.2f}:1, '
          f'5 % les plus faibles {pire:.2f}:1 ({verdict(pire)})')


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description='Miniatures de la chaîne (voir references/fabrication.md)')
    sp = ap.add_subparsers(dest='cmd', required=True)
    a = sp.add_parser('rendu')
    a.add_argument('source')
    a.add_argument('sortie')
    a = sp.add_parser('mesure')
    a.add_argument('images', nargs='+')
    a = sp.add_parser('planche')
    a.add_argument('sortie')
    a.add_argument('images', nargs='+')
    a.add_argument('--flux')
    a = sp.add_parser('grille')
    a.add_argument('photo')
    a.add_argument('sortie')
    a.add_argument('--zone')
    a.add_argument('--echelle', type=float, default=1.0)
    a.add_argument('--pas', type=int, default=50)
    a.add_argument('--polygone')
    a = sp.add_parser('contraste')
    a.add_argument('texte')
    a.add_argument('fond', nargs='?')
    a.add_argument('--image')
    a.add_argument('--zone')
    o = ap.parse_args()
    if o.cmd == 'rendu':
        sortie = nouveau(o.sortie)
        if not Path(o.source).is_file():
            sortir(f'{o.source} : introuvable')
        capturer(o.source, sortie, LARGEUR, HAUTEUR)
        sys.exit(0 if mesurer([sortie]) else 1)
    if o.cmd == 'mesure':
        sys.exit(0 if mesurer(o.images) else 1)
    if o.cmd == 'planche':
        planche(o.sortie, o.images, o.flux)
    elif o.cmd == 'grille':
        grille(o.photo, o.sortie, o.zone, o.echelle, o.pas, o.polygone)
    else:
        contraste(o.texte, o.fond, o.image, o.zone)


if __name__ == '__main__':
    main()
