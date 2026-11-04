"""Hook SessionStart du plugin studio-faceless.

Injecte les règles communes du studio (REGLES_STUDIO.md) au début de chaque session, et après un /clear ou un /compact,
avec les chemins du plugin installé à la place de ${CLAUDE_PLUGIN_ROOT}.
Depuis 0.2.0 : lit la ligne « - **Domaine** : <domaine> » du CLAUDE.md de la chaîne et donne le chemin de son profil.
Depuis 0.2.3 : l'application de bureau coupe tout additionalContext au-delà de 10 000 caractères (seul un aperçu de 2 Ko
arrive au modèle). REGLES_STUDIO.md doit donc rester court (limite : injection.regles_studio_caracteres_max de
referentiels/seuils.json, comptée par outils/verifier_coherence.py avec cette ligne du domaine) ;
si le texte final dépasse tout de même 9 500 caractères, une première ligne dit de lire le fichier en entier.
"""
import json
import os
import re
import sys

root = os.environ.get('CLAUDE_PLUGIN_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
racine = root.replace(chr(92), '/')
with open(os.path.join(root, 'REGLES_STUDIO.md'), encoding='utf-8') as f:
    texte = f.read().replace('${CLAUDE_PLUGIN_ROOT}', racine)

chaine = os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd()
try:
    with open(os.path.join(chaine, 'CLAUDE.md'), encoding='utf-8') as f:
        m = re.search(r'^\s*-\s*\*\*Domaine\*\*\s*:\s*`?([a-z0-9-]+)`?', f.read(), re.M)
except OSError:
    m = None
if m and m.group(1) != 'aucun':
    profil = os.path.join(root, 'domaines', m.group(1), 'DOMAINE.md')
    if os.path.isfile(profil):
        texte += ('\n\n## Domaine de la chaîne : ' + m.group(1) + '\nProfil : `' + racine + '/domaines/' + m.group(1)
                  + '/DOMAINE.md` (sources, droits des images, risques, son, veille). Il remplace les règles par défaut ;'
                  ' les écarts de la chaîne le remplacent. À lire selon la mission, comme `direction/ECARTS.md`.\n')
    else:
        texte += ('\n\n## Domaine de la chaîne : ' + m.group(1) + '\nAucun profil `domaines/' + m.group(1)
                  + '/DOMAINE.md` dans le plugin : le signaler au propriétaire (`domaines/README.md`, « Créer un domaine »).\n')
if len(texte) > 9500:
    texte = "Texte tronqué par l'app : lire " + racine + "/REGLES_STUDIO.md en entier.\n\n" + texte
sys.stdout.buffer.write(json.dumps({'hookSpecificOutput': {
    'hookEventName': 'SessionStart', 'additionalContext': texte}}, ensure_ascii=False).encode('utf-8'))
