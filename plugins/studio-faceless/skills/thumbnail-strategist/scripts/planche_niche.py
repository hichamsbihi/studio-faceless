"""Planche des miniatures de la niche, par ratio de vues (references/gabarits.md § 4 ; 1.1.3, VALIDÉ, propriétaire d'AA, 04/11/2026).

Entrées : des relevés de outils/recherche/youtube_chaine.py (un JSON par chaîne, champ `ratio` par vidéo).
Sortie : un court script JavaScript que le directeur exécute dans un onglet du navigateur intégré ouvert sur
https://i.ytimg.com/ (les miniatures s'affichent depuis YouTube, rien n'est enregistré), puis il fait des captures ;
et SORTIE.index.txt (numéro, chaîne, haut ou bas, ratio, vues, titre) pour relire sans images.
Par chaîne de référence : les --haut longues au plus fort ratio et les --bas au plus faible, publiées entre --depuis et
--avant (prendre --avant au moins 30 jours avant le relevé, pour des vues installées) ; la chaîne passée par --notre est
montrée en entier, par date. Une longue dont le titre contient un mot de --exclure est écartée (podcasts, par exemple).

Usage :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/skills/thumbnail-strategist/scripts/planche_niche.py SORTIE.js RELEVE.json [...]
         [--notre RELEVE.json] [--depuis AAAA-MM-JJ] [--avant AAAA-MM-JJ] [--haut 8] [--bas 4] [--exclure MOT]...
Aucun écrasement. Bibliothèque standard seule.
"""
import argparse, json, os, sys


def choisir(videos, depuis, avant, haut, bas, exclure):
    longues = [v for v in videos if v.get('format') == 'long' and not any(m in v.get('titre', '').lower() for m in exclure)]
    ok = sorted([v for v in longues if v.get('ratio') is not None and depuis <= v.get('publiee', '')[:10] <= avant],
                key=lambda v: -v['ratio'])
    if len(ok) < haut + bas:
        return [('toutes', ok)]
    return [('haut', ok[:haut]), ('bas', ok[-bas:][::-1])] if bas else [('haut', ok[:haut])]


def nom_de(d, f):
    c = d.get('chaine')
    return c.get('titre') if isinstance(c, dict) else (c or os.path.basename(f))


def script(blocs):
    return ('const B=' + json.dumps(blocs, ensure_ascii=False, separators=(',', ':')) + ';'
            "document.head.innerHTML='<style>body{background:#0f0f0f;color:#eee;font:12px Arial;margin:8px}h2{font-size:14px;margin:10px 0 4px}"
            ".g{display:grid;grid-template-columns:repeat(4,320px);gap:8px}img{display:block;border-radius:8px}b{color:#ffd54a}</style>';"
            "document.body.innerHTML=B.map(([t,it])=>'<h2>'+t+'</h2><div class=g>'+it.map(([i,n,r,k])=>"
            "'<div><img src=https://i.ytimg.com/vi/'+i+'/mqdefault.jpg width=320 height=180><div><b>#'+n+' · '+r+'</b> · '+k+' k</div></div>')"
            ".join('')+'</div>').join('');document.images.length")


def main():
    ap = argparse.ArgumentParser(description='Planche des miniatures de la niche, par ratio de vues.')
    ap.add_argument('sortie', help='script JavaScript à écrire (aucun écrasement)')
    ap.add_argument('releves', nargs='+', help='relevés youtube_chaine.py des chaînes de référence')
    ap.add_argument('--notre', help='relevé de la chaîne elle-même, montrée en entier')
    ap.add_argument('--depuis', default='0000-00-00')
    ap.add_argument('--avant', default='9999-99-99')
    ap.add_argument('--haut', type=int, default=8)
    ap.add_argument('--bas', type=int, default=4)
    ap.add_argument('--exclure', action='append', default=[], help='mot du titre qui écarte une longue (répétable)')
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    index_p = a.sortie + '.index.txt'
    for p in (a.sortie, index_p):
        if os.path.exists(p):
            sys.exit('Sortie existante, aucun écrasement : ' + p)
    exclure = [m.lower() for m in a.exclure]
    blocs, index, n = [], [], 0
    entrees = [(f, False) for f in a.releves] + ([(a.notre, True)] if a.notre else [])
    for f, notre in entrees:
        with open(f, encoding='utf-8') as fi:
            d = json.load(fi)
        nom = nom_de(d, f)
        if notre:
            choix = [('toutes', sorted([v for v in d['videos'] if v.get('format') == 'long'], key=lambda v: v.get('publiee', '')))]
        else:
            choix = choisir(d['videos'], a.depuis, a.avant, a.haut, a.bas, exclure)
        for t, vs in choix:
            items = []
            for v in vs:
                n += 1
                r = v.get('ratio')
                rt = '—' if r is None else round(r, 2)
                items.append([v['id'], n, rt, round(v.get('vues', 0) / 1000)])
                index.append(f'{n}\t{nom}\t{t}\t{rt}\t{v.get("vues", 0)}\t{v.get("titre", "")}')
            blocs.append([f'{nom[:28]} : {t}', items])
    os.makedirs(os.path.dirname(os.path.abspath(a.sortie)), exist_ok=True)
    with open(a.sortie, 'x', encoding='utf-8') as fo:
        fo.write(script(blocs))
    with open(index_p, 'x', encoding='utf-8') as fo:
        fo.write('\n'.join(index) + '\n')
    print(f'{n} miniatures, {len(blocs)} blocs : {a.sortie} (à exécuter dans un onglet ouvert sur https://i.ytimg.com/) ; index : {index_p}')


if __name__ == '__main__':
    main()
