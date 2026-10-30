"""Fait relire un script par Gemini, avec une consigne de spectateur curieux, et écrit l'avis dans un fichier.

Validé sur MM (Maps & Means), 23/10/2026 (consigne v2 du 29/10/2026). Versé au plugin le 30/10/2026 (décision 6). Frère de
`regarder.py` (même dossier : il en reprend `appeler` et `lire_cle`).

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/gemini/relire.py SCRIPT.md --consigne CONSIGNE.md --sortie AVIS.md
         [--modele gemini-3.8-flash]
CONSIGNE.md est la consigne de spectateur de la chaîne (exemple MM : spectateur américain ou européen, curieux, qui
décroche s'il s'ennuie) ; le plugin n'en fournit pas.

Règles (audit stratégique de MM, 22 et 23/10/2026, Q9 ; parcours v2, étape 4) :
- appel réseau vers l'API Gemini : un script inédit ne part chez Google qu'avec la clé payante (palier payant depuis le
  23/10/2026 sur MM : décision du propriétaire, hors plugin) ;
- seule la narration est envoyée (lignes « > » ou blocs ```text), sans les tableaux de sources ;
- clé GEMINI_API_KEY (environnement, sinon variables utilisateur Windows), en en-tête, jamais affichée ni écrite ;
- n'écrase jamais un fichier existant ; l'avis de Gemini est une hypothèse, à confronter à `controle/script.py`
  et au test de décrochage du propriétaire.
"""
import argparse, json, re, sys, time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from regarder import appeler, lire_cle  # noqa: E402


def narration(md):
    parties = []
    for bloc in re.split(r'\n## ', md)[1:]:
        titre = bloc.split('\n', 1)[0].strip()
        lignes = [l[1:].strip() for l in bloc.splitlines() if l.startswith('>')]
        texte = '\n'.join(l for l in lignes if l) or '\n'.join(re.findall(r'```text\n(.*?)```', bloc, re.S))
        if texte.strip():
            parties.append(f'### {titre}\n{texte.strip()}')
    return '\n\n'.join(parties)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('script')
    p.add_argument('--consigne', required=True)
    p.add_argument('--sortie', required=True)
    p.add_argument('--modele', default='gemini-3.8-flash')
    sys.stdout.reconfigure(encoding='utf-8')
    a = p.parse_args()
    sortie = Path(a.sortie)
    if sortie.exists():
        sys.exit(f"refusé : {sortie} existe déjà (jamais d'écrasement)")
    texte = narration(Path(a.script).read_text(encoding='utf-8'))
    if not texte:
        sys.exit('aucune narration trouvée (lignes « > » ou blocs ```text sous des titres « ## »)')
    consigne = Path(a.consigne).read_text(encoding='utf-8')
    corps = {'contents': [{'role': 'user', 'parts': [{'text': consigne + '\n\n--- SCRIPT (data) ---\n\n' + texte}]}],
             'generationConfig': {'temperature': 0.3}}
    debut = time.time()
    rep = appeler(a.modele, corps, lire_cle())
    try:
        avis = '\n'.join(x['text'] for x in rep['candidates'][0]['content']['parts'] if x.get('text'))
    except (KeyError, IndexError, TypeError):
        sys.exit('réponse illisible : ' + json.dumps(rep)[:400])
    u = rep.get('usageMetadata', {})
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(f'<!-- Relecture Gemini d\'un script, à lire comme une hypothèse\nscript : {a.script}\nconsigne : {a.consigne}\n'
                      f'modèle : {a.modele} ; date : {datetime.now():%d/%m/%Y %H:%M} ; durée : {time.time() - debut:.0f} s\n'
                      f'jetons : entrée {u.get("promptTokenCount")}, sortie {u.get("candidatesTokenCount")}\n-->\n\n'
                      + avis.strip() + '\n', encoding='utf-8')
    print(f'écrit : {sortie} ; jetons : {u.get("totalTokenCount")}')


if __name__ == '__main__':
    main()
