"""Rend en image la page d'un scan PDF codé en JBIG2, sans rien installer (Python + numpy).

Validé sur MM (Maps & Means), 28/10/2026 (épisode 005 ; sorti de l'épisode 004 le même jour). Versé au plugin le 30/10/2026.

Décodeur JBIG2 minimal, codage arithmétique seulement : dictionnaires de symboles (avec raffinement
et agrégation), régions de texte, régions génériques. Écrit d'après la norme ITU-T T.88 et le
décodeur de pdf.js (Apache-2.0, https://github.com/mozilla/pdf.js : crédit à garder). Ni Huffman, ni MMR, ni
prédiction typique : le script s'arrête s'il les rencontre.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/medias/jbig2_page.py FICHIER.pdf PAGE(1..n) SORTIE.pgm
Le PGM est en niveaux de gris, 0 = noir (encre), 255 = blanc (papier). Jamais d'écrasement.
"""
import math, os, re, sys
import numpy as np

QE = [(0x5601, 1, 1, 1), (0x3401, 2, 6, 0), (0x1801, 3, 9, 0), (0x0AC1, 4, 12, 0), (0x0521, 5, 29, 0),
      (0x0221, 38, 33, 0), (0x5601, 7, 6, 1), (0x5401, 8, 14, 0), (0x4801, 9, 14, 0), (0x3801, 10, 14, 0),
      (0x3001, 11, 17, 0), (0x2401, 12, 18, 0), (0x1C01, 13, 20, 0), (0x1601, 29, 21, 0), (0x5601, 15, 14, 1),
      (0x5401, 16, 14, 0), (0x5101, 17, 15, 0), (0x4801, 18, 16, 0), (0x3801, 19, 17, 0), (0x3401, 20, 18, 0),
      (0x3001, 21, 19, 0), (0x2801, 22, 19, 0), (0x2401, 23, 20, 0), (0x2201, 24, 21, 0), (0x1C01, 25, 22, 0),
      (0x1801, 26, 23, 0), (0x1601, 27, 24, 0), (0x1401, 28, 25, 0), (0x1201, 29, 26, 0), (0x1101, 30, 27, 0),
      (0x0AC1, 31, 28, 0), (0x09C1, 32, 29, 0), (0x08A1, 33, 30, 0), (0x0521, 34, 31, 0), (0x0441, 35, 32, 0),
      (0x02A1, 36, 33, 0), (0x0221, 37, 34, 0), (0x0141, 38, 35, 0), (0x0111, 39, 36, 0), (0x0085, 40, 37, 0),
      (0x0049, 41, 38, 0), (0x0025, 42, 39, 0), (0x0015, 43, 40, 0), (0x0009, 44, 41, 0), (0x0005, 45, 42, 0),
      (0x0001, 45, 43, 0), (0x5601, 46, 46, 0)]


class Arith:
    """Décodeur arithmétique MQ (annexe E de T.88), comme celui de pdf.js."""
    __slots__ = ('d', 'bp', 'end', 'chigh', 'clow', 'ct', 'a')

    def __init__(self, d, start):
        self.d = d; self.bp = start; self.end = len(d)
        self.chigh = d[start]; self.clow = 0; self.ct = 0
        self.byte_in()
        self.chigh = ((self.chigh << 7) & 0xffff) | ((self.clow >> 9) & 0x7f)
        self.clow = (self.clow << 7) & 0xffff
        self.ct -= 7
        self.a = 0x8000

    def byte_in(self):
        d = self.d; bp = self.bp
        if bp < self.end and d[bp] == 0xff:
            if (d[bp + 1] if bp + 1 < self.end else 0xff) > 0x8f:
                self.clow += 0xff00; self.ct = 8
            else:
                bp += 1; self.clow += d[bp] << 9; self.ct = 7; self.bp = bp
        else:
            bp += 1
            self.clow += (d[bp] << 8) if bp < self.end else 0xff00
            self.ct = 8; self.bp = bp
        if self.clow > 0xffff:
            self.chigh += self.clow >> 16; self.clow &= 0xffff

    def bit(self, cx, pos):
        v = cx[pos]; idx = v >> 1; mps = v & 1
        qe, nmps, nlps, sw = QE[idx]
        a = self.a - qe
        if self.chigh < qe:
            if a < qe:
                a = qe; d = mps; idx = nmps
            else:
                a = qe; d = 1 ^ mps
                if sw: mps = d
                idx = nlps
        else:
            self.chigh -= qe
            if a & 0x8000:
                self.a = a
                return mps
            if a < qe:
                d = 1 ^ mps
                if sw: mps = d
                idx = nlps
            else:
                d = mps; idx = nmps
        while True:
            if self.ct == 0: self.byte_in()
            a <<= 1
            self.chigh = ((self.chigh << 1) & 0xffff) | ((self.clow >> 15) & 1)
            self.clow = (self.clow << 1) & 0xffff
            self.ct -= 1
            if a & 0x8000: break
        self.a = a
        cx[pos] = (idx << 1) | mps
        return d


class Contextes(dict):
    """Contextes d'un segment, par procédure (IADT, IAID, GB, GR…)."""
    def __missing__(self, nom):
        taille = {'GB': 1 << 16, 'GR': 1 << 13}.get(nom, 512)
        self[nom] = v = [0] * taille
        return v

    def iaid(self, n):
        cle = 'IAID%d' % n
        if cle not in self: self[cle] = [0] * (1 << (n + 1))
        return self[cle]


def lire_bits(ar, cx, n, prev):
    v = 0
    for _ in range(n):
        b = ar.bit(cx, prev)
        prev = ((prev << 1) | b) if prev < 256 else ((((prev << 1) | b) & 511) | 256)
        v = (v << 1) | b
    return v, prev


def entier(ar, cx):
    """Entier codé (annexe A.2) ; None pour OOB."""
    s, p = lire_bits(ar, cx, 1, 1)
    b, p = lire_bits(ar, cx, 1, p)
    if not b:
        v, p = lire_bits(ar, cx, 2, p)
    else:
        b, p = lire_bits(ar, cx, 1, p)
        if not b:
            v, p = lire_bits(ar, cx, 4, p); v += 4
        else:
            b, p = lire_bits(ar, cx, 1, p)
            if not b:
                v, p = lire_bits(ar, cx, 6, p); v += 20
            else:
                b, p = lire_bits(ar, cx, 1, p)
                if not b:
                    v, p = lire_bits(ar, cx, 8, p); v += 84
                else:
                    b, p = lire_bits(ar, cx, 1, p)
                    if not b:
                        v, p = lire_bits(ar, cx, 12, p); v += 340
                    else:
                        v, p = lire_bits(ar, cx, 32, p); v += 4436
    if s == 0: return v
    return -v if v > 0 else None


def iaid(ar, cx, n):
    prev = 1
    for _ in range(n): prev = (prev << 1) | ar.bit(cx, prev)
    return prev & ((1 << n) - 1)


GABARITS = [
    [(-1, -2), (0, -2), (1, -2), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (-4, 0), (-3, 0), (-2, 0), (-1, 0)],
    [(-1, -2), (0, -2), (1, -2), (2, -2), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (-3, 0), (-2, 0), (-1, 0)],
    [(-1, -2), (0, -2), (1, -2), (-2, -1), (-1, -1), (0, -1), (1, -1), (-2, 0), (-1, 0)],
    [(-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (-4, 0), (-3, 0), (-2, 0), (-1, 0)]]
AT_DEFAUT = [(3, -1), (-3, -1), (2, -2), (-2, -2)]
RAFFINE = [([(0, -1), (1, -1), (-1, 0)], [(0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]),
           ([(-1, -1), (0, -1), (1, -1), (-1, 0)], [(0, -1), (-1, 0), (0, 0), (1, 0), (0, 1), (1, 1)])]


def generique(ar, cx, w, h, gab, at):
    """Région générique (6.2), sans prédiction typique. Rend une liste de lignes (bytearray, 1 = noir).
    L'ordre des bits du contexte est libre tant qu'il est constant : sans prédiction, aucun contexte
    n'est partagé avec un pseudo-pixel."""
    lignes = []; vide = bytes(w); bit = ar.bit
    if gab == 0 and list(at) == AT_DEFAUT:
        for y in range(h):
            P2 = b'\0\0' + bytes(lignes[y - 2] if y >= 2 else vide) + b'\0\0\0'
            P1 = b'\0\0\0' + bytes(lignes[y - 1] if y >= 1 else vide) + b'\0\0\0\0'
            w2 = (P2[0] << 4) | (P2[1] << 3) | (P2[2] << 2) | (P2[3] << 1) | P2[4]
            w1 = 0
            for k in range(7): w1 = (w1 << 1) | P1[k]
            w0 = 0; ligne = bytearray(w)
            for x in range(w):
                p = bit(cx, (w2 << 11) | (w1 << 4) | w0)
                ligne[x] = p
                w0 = ((w0 << 1) | p) & 15
                w2 = ((w2 << 1) & 31) | P2[x + 5]
                w1 = ((w1 << 1) & 127) | P1[x + 7]
            lignes.append(ligne)
        return lignes
    pos = GABARITS[gab] + list(at[:4] if gab == 0 else at[:1])
    for y in range(h):
        ligne = bytearray(w)
        for x in range(w):
            c = 0
            for dx, dy in pos:
                xx = x + dx; yy = y + dy; b = 0
                if 0 <= xx < w and yy >= 0:
                    b = ligne[xx] if yy == y else lignes[yy][xx]
                c = (c << 1) | b
            ligne[x] = bit(cx, c)
        lignes.append(ligne)
    return lignes


def raffinement(ar, cx, w, h, gab, ref, dx, dy, rat):
    """Région de raffinement générique (6.3), sans prédiction typique."""
    cod, rfp = RAFFINE[gab]
    if gab == 0: cod = cod + [rat[0]]; rfp = rfp + [rat[1]]
    rh = len(ref); rw = len(ref[0]) if rh else 0
    lignes = []; bit = ar.bit
    for y in range(h):
        ligne = bytearray(w)
        for x in range(w):
            c = 0
            for ex, ey in cod:
                yy = y + ey; xx = x + ex; b = 0
                if yy >= 0 and 0 <= xx < w:
                    b = ligne[xx] if yy == y else lignes[yy][xx]
                c = (c << 1) | b
            for ex, ey in rfp:
                yy = y + ey - dy; xx = x + ex - dx
                c = (c << 1) | (ref[yy][xx] if (0 <= yy < rh and 0 <= xx < rw) else 0)
            ligne[x] = bit(cx, c)
        lignes.append(ligne)
    return lignes


def tableau(lignes):
    h = len(lignes); w = len(lignes[0]) if h else 0
    return np.frombuffer(b''.join(bytes(l) for l in lignes), np.uint8).reshape(h, w) if h and w else np.zeros((h, w), np.uint8)


def poser(fond, motif, x0, y0, op):
    """Combine motif (0/1) dans fond à (x0, y0), découpé au bord. op : 0 OU, 1 ET, 2 OUX, 3 NON-OUX, 4 remplace."""
    H, W = fond.shape; h, w = motif.shape
    ys, ye = max(0, y0), min(H, y0 + h); xs, xe = max(0, x0), min(W, x0 + w)
    if ys >= ye or xs >= xe: return
    m = motif[ys - y0:ye - y0, xs - x0:xe - x0]; f = fond[ys:ye, xs:xe]
    if op == 0: f |= m
    elif op == 1: f &= m
    elif op == 2: f ^= m
    elif op == 3: f[...] = 1 - (f ^ m)
    else: f[...] = m


def region_texte(ar, ctx, W, H, n, syms, lcode, rgab, rat, raffine, bandes, defpix, comb, dsoff, coin):
    """Région de texte (6.4), codage arithmétique, non transposée. Rend un tableau numpy 0/1."""
    reg = np.full((H, W), defpix, np.uint8)
    cache = {}
    bandet = -entier(ar, ctx['IADT'])
    premiers = 0; i = 0
    while i < n:
        bandet += entier(ar, ctx['IADT'])
        premiers += entier(ar, ctx['IAFS'])
        s = premiers
        while True:
            ct = entier(ar, ctx['IAIT']) if bandes > 1 else 0
            t = bandes * bandet + ct
            sid = iaid(ar, ctx.iaid(lcode), lcode)
            ri = entier(ar, ctx['IARI']) if raffine else 0
            sym = syms[sid]
            sh = len(sym); sw = len(sym[0]) if sh else 0
            if ri:
                rdw = entier(ar, ctx['IARDW']); rdh = entier(ar, ctx['IARDH'])
                rdx = entier(ar, ctx['IARDX']); rdy = entier(ar, ctx['IARDY'])
                sw += rdw; sh += rdh
                sym = raffinement(ar, ctx['GR'], sw, sh, rgab, sym, (rdw >> 1) + rdx, (rdh >> 1) + rdy, rat)
                m = tableau(sym)
            else:
                m = cache.get(sid)
                if m is None: m = cache[sid] = tableau(sym)
            inc = 0
            if coin > 1: s += sw - 1
            else: inc = sw - 1
            ot = t - (0 if coin & 1 else sh - 1)
            os_ = s - (sw - 1 if coin & 2 else 0)
            if sw and sh: poser(reg, m, os_, ot, comb)
            i += 1
            ds = entier(ar, ctx['IADS'])
            if ds is None: break
            s += inc + ds + dsoff
    return reg


def s8(b): return b - 256 if b > 127 else b
def u32(d, i): return int.from_bytes(d[i:i + 4], 'big')


def dictionnaire(d, entree):
    fl = int.from_bytes(d[0:2], 'big')
    huff, refagg = fl & 1, (fl >> 1) & 1
    gab, rgab = (fl >> 10) & 3, (fl >> 12) & 1
    if huff or (fl >> 8) & 1: sys.exit('dictionnaire Huffman ou contextes repris : non pris en charge')
    i = 2; at = []
    for _ in range(4 if gab == 0 else 1): at.append((s8(d[i]), s8(d[i + 1]))); i += 2
    rat = []
    if refagg and rgab == 0:
        rat = [(s8(d[i]), s8(d[i + 1])), (s8(d[i + 2]), s8(d[i + 3]))]; i += 4
    nexp, nnew = u32(d, i), u32(d, i + 4); i += 8
    ar = Arith(d, i); ctx = Contextes()
    nouveaux = []; lcode = math.ceil(math.log2(len(entree) + nnew)) if len(entree) + nnew > 1 else 0
    hc = 0
    while len(nouveaux) < nnew:
        hc += entier(ar, ctx['IADH'])
        sw = 0
        while True:
            dw = entier(ar, ctx['IADW'])
            if dw is None: break
            sw += dw
            if refagg:
                ninst = entier(ar, ctx['IAAI'])
                if ninst > 1:
                    reg = region_texte(ar, ctx, sw, hc, ninst, entree + nouveaux, lcode, rgab, rat, 1, 1, 0, 0, 0, 1)
                    bm = [bytearray(r.tobytes()) for r in reg]
                else:
                    sid = iaid(ar, ctx.iaid(lcode), lcode)
                    rdx = entier(ar, ctx['IARDX']); rdy = entier(ar, ctx['IARDY'])
                    bm = raffinement(ar, ctx['GR'], sw, hc, rgab, (entree + nouveaux)[sid], rdx, rdy, rat)
            else:
                bm = generique(ar, ctx['GB'], sw, hc, gab, at)
            nouveaux.append(bm)
    drapeaux = []; cur = 0; tot = len(entree) + nnew
    while len(drapeaux) < tot:
        drapeaux += [cur] * entier(ar, ctx['IAEX']); cur ^= 1
    tous = entree + nouveaux
    sortie = [tous[k] for k in range(tot) if drapeaux[k]]
    if len(sortie) != nexp: print('attention : %d symboles exportés, %d annoncés' % (len(sortie), nexp))
    return sortie


def info_region(d):
    return u32(d, 0), u32(d, 4), u32(d, 8), u32(d, 12), d[16] & 7


def texte(d, syms):
    w, h, x, y, op = info_region(d); i = 17
    fl = int.from_bytes(d[i:i + 2], 'big'); i += 2
    huff, raff, logb, coin = fl & 1, (fl >> 1) & 1, (fl >> 2) & 3, (fl >> 4) & 3
    transp, comb, defpix, dsoff, rgab = (fl >> 6) & 1, (fl >> 7) & 3, (fl >> 9) & 1, (fl >> 10) & 31, (fl >> 15) & 1
    if dsoff > 15: dsoff -= 32
    if huff or transp: sys.exit('région de texte Huffman ou transposée : non pris en charge')
    rat = []
    if raff and rgab == 0:
        rat = [(s8(d[i]), s8(d[i + 1])), (s8(d[i + 2]), s8(d[i + 3]))]; i += 4
    n = u32(d, i); i += 4
    lcode = math.ceil(math.log2(len(syms))) if len(syms) > 1 else 0
    reg = region_texte(Arith(d, i), Contextes(), w, h, n, syms, lcode, rgab, rat, raff, 1 << logb, defpix, comb, dsoff, coin)
    return reg, x, y, op


def generique_seg(d):
    w, h, x, y, op = info_region(d); i = 17
    g = d[i]; i += 1
    if g & 1 or (g >> 3) & 1: sys.exit('région générique MMR ou à prédiction typique : non pris en charge')
    gab = (g >> 1) & 3; at = []
    for _ in range(4 if gab == 0 else 1): at.append((s8(d[i]), s8(d[i + 1]))); i += 2
    return tableau(generique(Arith(d, i), [0] * (1 << 16), w, h, gab, at)), x, y, op


def segments(data):
    i = 0
    while i + 11 <= len(data):
        num = u32(data, i); fl = data[i + 4]; typ = fl & 63; grand = fl & 64
        c = data[i + 5]; nref = c >> 5; j = i + 6
        if nref == 7: sys.exit('en-tête de segment long : non pris en charge')
        taille = 1 if num <= 256 else 2 if num <= 65536 else 4
        refs = [int.from_bytes(data[j + k * taille:j + (k + 1) * taille], 'big') for k in range(nref)]
        j += nref * taille + (4 if grand else 1)
        ln = u32(data, j); j += 4
        if ln == 0xffffffff: sys.exit('segment de longueur inconnue : non pris en charge')
        yield num, typ, refs, data[j:j + ln]
        i = j + ln


def image_de_page(pdf, page):
    d = open(pdf, 'rb').read()
    objs = {int(m.group(1)): m.end() for m in re.finditer(rb'(\d+)\s+0\s+obj\b', d)}
    def corps(n): i = objs[n]; return d[i:d.find(b'endobj', i)]
    def dico(n): b = corps(n); k = b.find(b'stream'); return b if k < 0 else b[:k]
    def flux(n):
        b = corps(n); h = dico(n); k = b.find(b'stream'); k = b.find(b'\n', k) + 1
        L = re.search(rb'/Length\s+(\d+)(\s+0\s+R)?', h)
        return b[k:k + int(L.group(1))] if L and not L.group(2) else b[k:b.rfind(b'endstream')]
    def enfants(n):
        h = dico(n)
        if re.search(rb'/Type\s*/Pages', h):
            r = []
            for x in re.findall(rb'(\d+)\s+0\s+R', re.search(rb'/Kids\s*\[(.*?)\]', h, re.S).group(1)): r += enfants(int(x))
            return r
        return [n]
    racine = int(re.search(rb'/Root\s+(\d+)\s+0\s+R', d).group(1))
    pages = enfants(int(re.search(rb'/Pages\s+(\d+)\s+0\s+R', dico(racine)).group(1)))
    h = dico(pages[page - 1])
    xr = re.search(rb'/XObject\s+(\d+)\s+0\s+R', h)
    xd = dico(int(xr.group(1))) if xr else re.search(rb'/XObject\s*(<<.*?>>)', h, re.S).group(1)
    for _, n in re.findall(rb'/(\w+)\s+(\d+)\s+0\s+R', xd):
        ih = dico(int(n))
        if b'JBIG2Decode' in ih:
            g = re.search(rb'/JBIG2Globals\s+(\d+)\s+0\s+R', ih)
            w = int(re.search(rb'/Width\s+(\d+)', ih).group(1)); hh = int(re.search(rb'/Height\s+(\d+)', ih).group(1))
            return (flux(int(g.group(1))) if g else b'') + flux(int(n)), w, hh
    sys.exit('pas d\'image JBIG2 sur cette page')


def main():
    if len(sys.argv) != 4 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0 if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help') else 2)
    pdf, page, sortie = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    if os.path.exists(sortie): sys.exit('existe déjà : ' + sortie)
    data, w, h = image_de_page(pdf, page)
    exportes = {}; page_img = np.zeros((h, w), np.uint8)
    for num, typ, refs, d in segments(data):
        if typ == 48:
            print('page', u32(d, 0), 'x', u32(d, 4))
        elif typ == 0:
            entree = [s for r in refs for s in exportes.get(r, [])]
            exportes[num] = dictionnaire(d, entree)
            print('dictionnaire', num, ':', len(exportes[num]), 'symboles')
        elif typ in (6, 7):
            syms = [s for r in refs for s in exportes.get(r, [])]
            reg, x, y, op = texte(d, syms); poser(page_img, reg, x, y, op)
            print('région de texte', num, reg.shape, 'op', op)
        elif typ in (38, 39):
            reg, x, y, op = generique_seg(d); poser(page_img, reg, x, y, op)
            print('région générique', num, reg.shape, 'op', op)
        elif typ in (49, 50, 51, 62):
            pass
        else:
            sys.exit('segment de type %d : non pris en charge' % typ)
    with open(sortie, 'xb') as f:
        f.write(b'P5\n%d %d\n255\n' % (w, h)); f.write(((1 - page_img) * 255).astype(np.uint8).tobytes())
    print('écrit', sortie, ': encre', round(float(page_img.mean()) * 100, 2), '%')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
