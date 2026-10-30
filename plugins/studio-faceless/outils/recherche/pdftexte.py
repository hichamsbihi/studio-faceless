"""Extraction de texte d'un PDF, bibliothèque standard seulement (pas de poppler).

Validé sur MM (Maps & Means), 28/10/2026 (épisode 005 ; leçon « lire ce que l'agent ne lit pas »). Versé au plugin le
30/10/2026.

Mode d'emploi, depuis la racine de la chaîne :
    1. Le PDF est un fichier local (téléchargé avec l'accord du propriétaire, ou enregistré par WebFetch dans les résultats
       d'outils de la session).
    2. python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/recherche/pdftexte.py <fichier.pdf> > texte.txt
       python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/recherche/pdftexte.py <fichier.pdf> "mot clé" ["autre mot"...]
       Sans mot clé : tout le texte. Avec mots clés : les deux premiers passages de chacun, avec leur contexte.
       Un scan JBIG2 (image) : ${CLAUDE_PLUGIN_ROOT}/outils/medias/jbig2_page.py, puis lecture de l'image.

Méthode : décompresse les flux FlateDecode qui contiennent du texte, les lit à la suite (le contenu
d'une page peut être coupé en plusieurs flux), puis lit les opérateurs Tj et TJ. Les échappements
octaux (\\374 = ü) sont décodés en latin-1. Limites : polices à encodage personnalisé et scans
(images) restent illisibles ; l'ordre de lecture suit celui du fichier.
"""
import re
import sys
import zlib


def extraire(chemin):
    data = open(chemin, "rb").read()
    flux = []
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        try:
            f = zlib.decompress(m.group(1))
        except zlib.error:
            continue
        if len(f) < 200_000 and (b"TJ" in f or b"Tj" in f):
            flux.append(f)
    contenu = b"\n".join(flux)
    morceaux = []
    for tok in re.finditer(rb"\[(.*?)\]\s*TJ|\((.*?)(?<!\\)\)\s*Tj|(T\*|Td|TD|')", contenu, re.S):
        if tok.group(1) is not None:
            for s in re.finditer(rb"\((.*?)(?<!\\)\)|(-?\d+\.?\d*)", tok.group(1), re.S):
                if s.group(1) is not None:
                    morceaux.append(s.group(1))
                elif float(s.group(2)) < -200:
                    morceaux.append(b" ")
        elif tok.group(2) is not None:
            morceaux.append(tok.group(2))
        else:
            morceaux.append(b" ")
    texte = b"".join(morceaux).replace(b"\\(", b"(").replace(b"\\)", b")").decode("latin-1")
    texte = re.sub(r"\\(\d{3})", lambda m: chr(int(m.group(1), 8)), texte)
    return re.sub(r"[ \t]+", " ", texte)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) > 1 else 2)
    texte = extraire(sys.argv[1])
    if len(sys.argv) == 2:
        print(texte)
    for mot in sys.argv[2:]:
        for m in list(re.finditer(re.escape(mot), texte))[:2]:
            print("==", mot, "::", texte[max(0, m.start() - 500):m.end() + 400].replace("\n", " "))
