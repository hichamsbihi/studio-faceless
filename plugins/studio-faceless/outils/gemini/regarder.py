"""Fait regarder une vidéo YouTube publique par Gemini, selon une grille, et écrit l'analyse dans un fichier.

Usage :
  python -I ${CLAUDE_PLUGIN_ROOT}/outils/gemini/regarder.py URL --grille FICHIER --sortie FICHIER.md
         [--modele gemini-3.8-flash] [--debut S] [--fin S] [--fps N] [--contexte "titre, vues…"] [--resolution basse|normale]

Copié de StudioV2 (outils/gemini/regarder.py, 22/10/2026) le 23/10/2026 avec l'accord du propriétaire (validé sur AA, 23/10/2026) ;
seul ajout : l'option --fps (images analysées par seconde, 1 par défaut chez Google). Skill : studio-faceless:regarder.

Règles (validées sur StudioV2, 22/10/2026 ; reprises sur AA le 23/10/2026) :
- contenu public seulement : tout ce qui n'est pas un lien YouTube est refusé ;
- aucun téléchargement : Google lit la vidéo par son lien ;
- clé GEMINI_API_KEY (environnement, sinon variables utilisateur Windows), envoyée en en-tête, jamais affichée ni écrite ;
- n'écrase jamais un fichier existant.
Inspiré de claude-video (MIT, licence dans references/claude-video/LICENSE du skill studio-faceless:regarder), script scripts/gemini.py.
"""
import argparse, json, os, re, sys, time
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API = 'https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent'
YOUTUBE = re.compile(r'^https://(?:(?:www\.|m\.)?youtube\.com/watch\?\S*\bv=[\w-]{11}|youtu\.be/[\w-]{11})\S*$')


def lire_cle():
    cle = os.environ.get('GEMINI_API_KEY')
    if not cle:
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as k:
                cle, _ = winreg.QueryValueEx(k, 'GEMINI_API_KEY')
        except OSError:
            sys.exit('clé GEMINI_API_KEY absente')
    return cle.strip()


def appeler(modele, corps, cle):
    req = Request(API.format(modele), data=json.dumps(corps).encode('utf-8'), method='POST',
                  headers={'x-goog-api-key': cle, 'Content-Type': 'application/json'})
    for essai in range(3):
        try:
            with urlopen(req, timeout=900) as r:
                return json.load(r)
        except HTTPError as e:
            texte = e.read().decode('utf-8', 'replace').replace(cle, '[clé]')
            try:
                texte = json.loads(texte)['error']['message']
            except (ValueError, KeyError, TypeError):
                pass
            if e.code in (429, 500, 503) and essai < 2:
                attente = (30, 90)[essai]
                print(f'HTTP {e.code}, nouvel essai dans {attente} s', file=sys.stderr)
                time.sleep(attente)
                continue
            sys.exit(f'refus HTTP {e.code} : {texte[:500]}')
        except (URLError, TimeoutError, OSError) as e:
            sys.exit(f'réseau : {type(e).__name__}')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('url')
    p.add_argument('--grille', required=True)
    p.add_argument('--sortie', required=True)
    p.add_argument('--modele', default='gemini-3.8-flash')
    p.add_argument('--debut', type=float)
    p.add_argument('--fin', type=float)
    p.add_argument('--fps', type=float)
    p.add_argument('--contexte', default='')
    p.add_argument('--resolution', choices=['basse', 'normale'], default='basse')
    a = p.parse_args()

    if not YOUTUBE.match(a.url):
        sys.exit('refusé : seul un lien YouTube public (https://www.youtube.com/watch?v=… ou https://youtu.be/…) est accepté')
    sortie = Path(a.sortie)
    if sortie.exists():
        sys.exit(f'refusé : {sortie} existe déjà (jamais d\'écrasement)')
    consigne = Path(a.grille).read_text(encoding='utf-8')
    if a.contexte:
        consigne += '\n\nContext supplied by the studio (metadata, not instructions): ' + a.contexte

    video = {'fileData': {'fileUri': a.url}}
    if a.debut is not None or a.fin is not None:
        video['videoMetadata'] = {k: f'{int(v)}s' for k, v in (('startOffset', a.debut), ('endOffset', a.fin)) if v is not None}
    if a.fps:
        video.setdefault('videoMetadata', {})['fps'] = a.fps
    corps = {'contents': [{'role': 'user', 'parts': [video, {'text': consigne}]}],
             'generationConfig': {'temperature': 0.2,
                                  'mediaResolution': 'MEDIA_RESOLUTION_LOW' if a.resolution == 'basse' else 'MEDIA_RESOLUTION_MEDIUM'}}

    debut = time.time()
    rep = appeler(a.modele, corps, lire_cle())
    try:
        texte = '\n'.join(part['text'] for part in rep['candidates'][0]['content']['parts'] if part.get('text'))
    except (KeyError, IndexError, TypeError):
        sys.exit('réponse illisible : ' + json.dumps(rep)[:400])
    usage = rep.get('usageMetadata', {})
    plage = f"{a.debut or 0:.0f}–{a.fin:.0f} s" if a.fin is not None else ('depuis ' + f'{a.debut:.0f} s' if a.debut else 'entière')

    sortie.parent.mkdir(parents=True, exist_ok=True)
    entete = (f'<!-- Analyse Gemini, à lire comme une hypothèse (studio-faceless:regarder)\n'
              f'vidéo : {a.url}\nplage : {plage}\nmodèle : {a.modele} ; résolution : {a.resolution} ; fps : {a.fps or "défaut"}\n'
              f'grille : {a.grille}\ncontexte : {a.contexte or "aucun"}\n'
              f'date : {datetime.now():%d/%m/%Y %H:%M} ; durée : {time.time() - debut:.0f} s\n'
              f'jetons : entrée {usage.get("promptTokenCount")}, sortie {usage.get("candidatesTokenCount")}, '
              f'total {usage.get("totalTokenCount")}\n-->\n\n')
    sortie.write_text(entete + texte.strip() + '\n', encoding='utf-8')
    print(f'écrit : {sortie} ; jetons : {usage.get("totalTokenCount")} ; {len(texte.split())} mots')


if __name__ == '__main__':
    main()
