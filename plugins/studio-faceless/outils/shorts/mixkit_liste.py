"""Liste les clips d'une page de recherche Mixkit enregistrée (données lues, jamais exécutées) : id, titre, lien de page.
La licence se lit sur la page de chaque clip (data-license). Usage : python -I mixkit_liste.py PAGE.html"""
import re, sys, html
h = open(sys.argv[1], encoding='utf-8', errors='replace').read()
for b in h.split('class="item-grid-card"')[1:]:
    i = re.search(r'/videos/(\d+)/', b)
    t = re.search(r'item-grid-card__title[^>]*>(?:\s*<a[^>]*>)?\s*([^<]+)', b)
    u = re.search(r'href="(/free-stock-video/[^"]+)"', b)
    print(i.group(1) if i else '?', '|', html.unescape(t.group(1).strip()) if t else '?', '|', u.group(1) if u else '')
