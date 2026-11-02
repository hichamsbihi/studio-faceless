"""Résumé d'un relevé de `youtube_chaine.py`, sans lire le JSON en entier.

Usage : python -I -B youtube_resume.py releve.json [--top N] [--territoires motifs.json] [--liste]
- longues et courts : nombre, vues médianes ; longues par année ;
- titres des longues : médiane de mots, part des « Why », « How », « What », « Every » et des questions ;
- les N longues au plus fort ratio (vues ÷ médiane des 30 voisines), 20 par défaut ;
- --territoires : fichier JSON {"territoire": "motif regex", ...}, testés dans l'ordre sur le titre en minuscules ;
  le premier qui correspond l'emporte, sinon « autre » (classement par mots-clés : une hypothèse, pas un fait) ;
- sponsors probables lus dans le début des descriptions.
Validé sur AA (positionnement, 02/11/2026).
"""
import json, re, statistics as S, sys
from collections import defaultdict

SPONSOR = re.compile(r"(?:sponsored by|thanks to|brought to you by|partnered with|check out|download|sign up for|try)\s+"
                     r"([A-Z][\w.&'-]+(?:\s[A-Z][\w.&'-]+)?)")


def option(nom, defaut=None):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def main(f):
    d = json.load(open(f, encoding="utf-8"))
    videos = d["videos"]
    longues = [v for v in videos if v["format"] == "long"]
    courts = [v for v in videos if v["format"] == "court"]
    med = lambda xs: f"{S.median(xs):,.0f}" if xs else "—"
    print(f"== {d['chaine']['titre']} ({d['date']}) : {d['chaine']['abonnes']:,} abonnés")
    print(f"longues {len(longues)}, vues médianes {med([v['vues'] for v in longues])} ; "
          f"courts {len(courts)}, vues médianes {med([v['vues'] for v in courts])}")
    an = defaultdict(list)
    for v in longues:
        an[v["publiee"][:4]].append(v["vues"])
    print("longues par année (n, vues médianes) : " + " ; ".join(f"{a} {len(x)} {med(x)}" for a, x in sorted(an.items())))
    titres = [v["titre"] for v in longues]
    if titres:
        mots = [len(t.split()) for t in titres]
        parts = {m: sum(bool(re.match(m + r"\b", t, re.I)) for t in titres) / len(titres) for m in ("Why", "How", "What", "Every")}
        parts["questions"] = sum(t.rstrip().endswith("?") for t in titres) / len(titres)
        print(f"titres des longues : {S.median(mots):.0f} mots en médiane ; " + ", ".join(f"{k} {p:.0%}" for k, p in parts.items()))
    n = int(option("--top", 20))
    forts = sorted((v for v in longues if v.get("ratio")), key=lambda v: -v["ratio"])[:n]
    print(f"-- {len(forts)} plus forts ratios (longues) :")
    for v in forts:
        print(f"×{v['ratio']} | {v['vues']:,} | {v['publiee'][:10]} | {v['titre']}")
    chemin = option("--territoires")
    if chemin:
        motifs = list(json.load(open(chemin, encoding="utf-8")).items())
        groupes = defaultdict(list)
        for v in (v for v in longues if v.get("ratio")):
            nom = next((k for k, rx in motifs if re.search(rx, v["titre"].lower())), "autre")
            groupes[nom].append(v)
        print("territoire | n | ratio médian | ×5 et plus | ×2 et plus | vues médianes")
        for nom, vs in sorted(groupes.items(), key=lambda kv: -len(kv[1])):
            r = [v["ratio"] for v in vs]
            print(f"{nom} | {len(vs)} | ×{S.median(r):.2f} | {sum(x >= 5 for x in r)} | {sum(x >= 2 for x in r)} | {med([v['vues'] for v in vs])}")
            if "--liste" in sys.argv:
                print("   " + " ; ".join(f"{v['titre']} ×{v['ratio']}" for v in vs))
    sponsors = defaultdict(int)
    for v in videos:
        for m in SPONSOR.findall(v.get("description_debut", "")):
            sponsors[m] += 1
    print("sponsors probables (descriptions) :", dict(sorted(sponsors.items(), key=lambda kv: -kv[1])[:15]))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
