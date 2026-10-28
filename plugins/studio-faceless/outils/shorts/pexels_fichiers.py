"""Lit une page Pexels enregistrée (données, jamais exécutées) : auteur et fichiers vidéo proposés.
Usage : python -I pexels_fichiers.py PAGE.html"""
import json, re, sys

h = open(sys.argv[1], encoding='utf-8').read()
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S)
if not m:
    raise SystemExit('pas de __NEXT_DATA__ (vérification anti-robot ?)')
s = m.group(1)
urls = sorted(set(re.findall(r'https://videos\.pexels\.com/video-files/[^"\\]+?\.mp4', s)))
auteurs = sorted(set(re.findall(r'"(?:first_name|username)":"([^"]{1,60})"', s)))[:4]
print('auteur(s) :', auteurs)
vid = sys.argv[2] if len(sys.argv) > 2 else None
for u in urls:
    if vid is None or f'/video-files/{vid}/' in u:
        print(u)
