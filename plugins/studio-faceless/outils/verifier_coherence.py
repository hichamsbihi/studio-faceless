"""Contrôle de cohérence du texte du plugin studio-faceless (1.1.0 ; point 6 du conseil du 04/11/2026, VALIDÉ par le propriétaire).

Une seule source par règle : ce contrôle refuse ce qui ferait revenir une contradiction (§ 7 du compte rendu) :
- le vocabulaire fixé (`REGLES_STUDIO.md` § Vocabulaire) : « socle » hors de ses fichiers (citer `SOCLE.md` ailleurs),
  « portes A à E », « orchestrateur », « conseil » hors du skill conseil ;
- une formule de préséance (« l'emporte », « prime sur »…) hors du § Priorité de `REGLES_STUDIO.md` ;
- une valeur en LUFS, LU ou dBTP dans la prose : les valeurs vivent dans `referentiels/seuils.json` ;
- un `PROPOSÉ` dans `referentiels/`, `skills/` ou `agents/`, sauf le statut d'un livrable (`LIVRABLE`, 1.1.1) ;
- un renvoi mort (fichier du plugin cité et absent, `DEMARRAGE.md` ou `docs/` hors du plugin installé, « dix agents ») ;
- une ligne D à deux décideurs, une ligne D non déclarée par son agent (`REGLES_DETAIL.md` § Qui décide) ;
- un agent qui a Bash, Write ou Edit sans rôle dans `ROLES` (garde-fou) ; un appel `agent(` d'un workflow sans `agentType` ;
- un texte injecté (`REGLES_STUDIO.md`, chemin du cache et ligne du domaine compris) au-delà de la limite de `seuils.json`.

Base gelée (`outils/coherence_base.json`) : les occurrences connues à la création ; elle ne peut que décroître. Dans le dépôt du
plugin, toute occurrence absente de la base est refusée (code 1), et une occurrence de la base qui a disparu doit en être retirée
(`--geler`) dans le même commit. Une ligne de la base que l'on réécrit sort de la base : la nouvelle ligne est contrôlée strictement.
Dans une chaîne, le contrôle ne fait que rapporter (code 0) : écarts « Remplace : <id> » orphelins, écarts qui visent une ligne D.
Ses limites : il travaille par motifs, ne voit pas une contradiction de sens, et peut refuser à tort (corriger le motif, pas la base).

Usage :
  python -I -B plugins/studio-faceless/outils/verifier_coherence.py              dépôt du plugin : bloquant (crochet pre-commit)
  python -I -B <plugin>/outils/verifier_coherence.py                             depuis une chaîne : rapport
  ... --rapport                    n'échoue jamais ; compte par motif, base comprise, et mesure des lignes normatives
  ... --geler                      crée la base si elle n'existe pas ; sinon retire les occurrences disparues (n'ajoute jamais)
  ... --registre FICHIER.json      écrit le registre des tampons (statuts, chaîne, dates, versions) du texte du plugin
  ... --renomme ANCIEN NOUVEAU     reporte les occurrences de la base d'un fichier renommé (chemins relatifs au plugin)
Bibliothèque standard seule.
"""
import ast, json, os, re, subprocess, sys
from collections import Counter

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPOT = os.path.abspath(os.path.join(PLUGIN, '..', '..'))
BASE = os.path.join(PLUGIN, 'outils', 'coherence_base.json')
SEUILS = os.path.join(PLUGIN, 'referentiels', 'seuils.json')
RACINE_TYPE = 'C:/Users/<nom>/.claude/plugins/cache/studio-faceless/studio-faceless/1.1.0'
LIMITE_DEFAUT = 8000             # repli si seuils.json manque ; la valeur fait foi dans seuils.json
DOSSIERS = ('agents', 'domaines', 'hooks', 'outils', 'referentiels', 'skills', 'starter', 'templates', 'vendor', 'workflows')
EXCLUS = ('vendor/',)            # données de tiers
FICHIERS_TIERS = ('PROVENANCE.md', 'SOURCES_ET_LICENCES.md', 'LICENSE', 'LICENSE.md', 'NOTICE.md')

# (identifiant, motif, fichiers ou dossiers où il est permis, message)
MOTIFS = [
    ('socle', re.compile(r'(?i)\bsocles?\b'),
     ('REGLES_STUDIO.md', 'referentiels/REGLES_DETAIL.md', 'templates/SOCLE.template.md', 'skills/episode/'),
     "« socle » = la séance du propriétaire et son fichier : hors de ses fichiers, citer `SOCLE.md` ; l'étape 5 est le « kit »"),
    ('portes-a-e', re.compile(r'\bportes? [A-E]\b(?:\s*(?:à|-|–)\s*[A-E]\b)?'), (),
     "« porte » = un accord du propriétaire ; une mesure est un « contrôle » (seuils.json)"),
    ('orchestrateur', re.compile(r'(?i)\borchestrat(?:eur|rice|ion)s?\b'), (),
     "« directeur » (Claude principal)"),
    ('conseil', re.compile(r'(?i)\bconseils?\b'),
     ('skills/conseil/', 'agents/conseiller.md', 'REGLES_STUDIO.md', 'referentiels/REGLES_DETAIL.md'),
     "« conseil » = le skill studio-faceless:conseil seul ; la séance de strategist est la « revue de positionnement »"),
    ('preseance', re.compile(r"(?i)l['’]emport(?:e|ent)\b|\bprévau[tx]\b|\bprévalent\b|\bprim(?:e|ent) sur\b|\bprioritaires? sur\b"), (),
     "un seul énoncé de la priorité : citer `REGLES_STUDIO.md` § Priorité"),
    ('unite', re.compile(r'(?<![\w.])[-−–+]?\d+(?:[.,]\d+)?\s?(?:LUFS|LU|dBTP|dB TP)\b'), (),
     "valeur chiffrée : dans `referentiels/seuils.json` (ou `direction/seuils.json` de la chaîne), citée par sa clé"),
    ('propose', re.compile(r'\bPROPOSÉ\b'), (),
     "un `PROPOSÉ` n'est pas une règle en vigueur : le propriétaire le valide, sinon il sort du texte actif"),
    ('renvoi-mort', re.compile(r'\bDEMARRAGE\.md\b|\bsocle\.md\b|(?i:\bdix agents\b)'), (),
     "renvoi mort : fichier absent du plugin installé, ou compte faux"),
]
# Statut d'un livrable (1.1.1) : « statut `PROPOSÉ` », « `fichier.md`, `PROPOSÉ` », « `PROPOSÉ`, puis … »,
# « `PROPOSÉ` partout », « dossier / recommandations / tout reste `PROPOSÉ` » : le livrable attend le propriétaire,
# ce n'est pas une règle en attente. Un `PROPOSÉ` hors de ces formes reste compté.
LIVRABLE = re.compile(r"(?i:\bstatut|\bdossier|\brecommandations|\btout reste)\s+`PROPOSÉ`|\.md`,\s+`PROPOSÉ`"
                      r"|`PROPOSÉ`,?\s+puis\b|`PROPOSÉ`\s+partout")
SECTION_PRIORITE = re.compile(r'^#+\s*Priorit', re.I)
# Chemins cités : `${CLAUDE_PLUGIN_ROOT}/…` (tout dossier) ; sans préfixe, seulement les dossiers propres au plugin
# (`outils/` et `vendor/` existent aussi dans les chaînes) et `references/…`, relatif au skill qui le cite.
PROPRES = ('agents', 'domaines', 'hooks', 'referentiels', 'skills', 'starter', 'templates', 'workflows', 'references')
CHEMIN_CITE = re.compile(r'`(?:\$\{CLAUDE_PLUGIN_ROOT\}/((?:' + '|'.join(DOSSIERS) + r')/[^`\s]+)|((?:'
                         + '|'.join(PROPRES) + r')/[^`\s]+))`')


def rel(p):
    return os.path.relpath(p, PLUGIN).replace(os.sep, '/')


def permis(fichier, ou):
    return any(fichier == o or (o.endswith('/') and fichier.startswith(o)) for o in ou)


def perimetre():
    """Fichiers Markdown du texte du plugin (hors données de tiers)."""
    out = []
    for d, sous, fichiers in os.walk(PLUGIN):
        sous[:] = sorted(s for s in sous if s not in ('__pycache__', 'node_modules', '.git'))
        for f in sorted(fichiers):
            r = rel(os.path.join(d, f))
            if f.endswith('.md') and not r.startswith(EXCLUS) and f not in FICHIERS_TIERS:
                out.append(r)
    return out


def lire(r):
    with open(os.path.join(PLUGIN, r), encoding='utf-8', errors='replace') as f:
        return f.read()


def lignes_utiles(texte):
    """(numéro, ligne, titre courant) hors blocs de code."""
    code, titre = False, ''
    for n, ligne in enumerate(texte.splitlines(), 1):
        if ligne.lstrip().startswith('```'):
            code = not code
            continue
        if code:
            continue
        if ligne.startswith('#'):
            titre = ligne
        yield n, ligne, titre


def seuils():
    try:
        with open(SEUILS, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def cles(d, prefixe=''):
    out = set()
    for k, v in (d.items() if isinstance(d, dict) else []):
        if k.startswith('_'):
            continue
        cle = prefixe + k
        out.add(cle)
        out |= cles(v, cle + '.')
    return out


def table_decideurs():
    """Lignes de `REGLES_DETAIL.md` § Qui décide : {id: {colonne: cellule}} ; None si la section manque."""
    try:
        texte = lire('referentiels/REGLES_DETAIL.md')
    except OSError:
        return None
    m = re.search(r'^#+\s*Qui décide.*?$(.*?)(?=^#+\s|\Z)', texte, re.M | re.S)
    if not m:
        return None
    entetes, lignes = None, {}
    for ligne in m.group(1).splitlines():
        if not ligne.startswith('|') or re.match(r'^\|\s*-', ligne):
            continue
        cellules = [c.strip() for c in ligne.strip().strip('|').split('|')]
        if entetes is None:
            entetes = [c.lower() for c in cellules]
            continue
        if re.fullmatch(r'D\d{2}', cellules[0]):
            lignes.setdefault(cellules[0], []).append(dict(zip(entetes, cellules)))
    return lignes


def roles_garde():
    try:
        arbre = ast.parse(lire('hooks/garde_commandes.py'))
    except (OSError, SyntaxError):
        return {}
    for n in arbre.body:
        if isinstance(n, ast.Assign) and any(getattr(t, 'id', '') == 'ROLES' for t in n.targets):
            return ast.literal_eval(n.value)
    return {}


def appels_sans_type(texte):
    """Appels agent(...) dont les options ne portent pas agentType, ni par une fonction qui le pose."""
    poseuses = set()
    for m in re.finditer(r'(?:function\s+(\w+)\s*\(|const\s+(\w+)\s*=\s*(?:\([^)]*\)|\w+)\s*=>)', texte):
        nom = m.group(1) or m.group(2)
        if 'agentType' in texte[m.end():m.end() + 800].split('\nfunction ')[0]:
            poseuses.add(nom)
    out = []
    for m in re.finditer(r'(?<![\w.])agent\(', texte):
        i, prof = m.end(), 1
        while i < len(texte) and prof:
            prof += {'(': 1, ')': -1}.get(texte[i], 0)
            i += 1
        appel = texte[m.start():i]
        if 'agentType' in appel or any(re.search(r'\b' + re.escape(p) + r'\(', appel) for p in poseuses):
            continue
        out.append((texte.count('\n', 0, m.start()) + 1, appel.split('\n')[0][:120]))
    return out


def taille_injectee():
    """Longueur du texte que hooks/regles_studio.py injecte, pour le plus long des domaines du plugin."""
    texte = lire('REGLES_STUDIO.md').replace('${CLAUDE_PLUGIN_ROOT}', RACINE_TYPE)
    plus = 0
    for dom in sorted(os.listdir(os.path.join(PLUGIN, 'domaines'))):
        if dom.startswith('_') or not os.path.isfile(os.path.join(PLUGIN, 'domaines', dom, 'DOMAINE.md')):
            continue
        ligne = ('\n\n## Domaine de la chaîne : ' + dom + '\nProfil : `' + RACINE_TYPE + '/domaines/' + dom
                 + '/DOMAINE.md` (sources, droits des images, risques, son, veille). Il remplace les règles par défaut ;'
                 ' les écarts de la chaîne le remplacent. À lire selon la mission, comme `direction/ECARTS.md`.\n')
        plus = max(plus, len(ligne))
    return len(texte) + plus


def statut_livrable(ligne, x):
    """Vrai si le `PROPOSÉ` trouvé en x est le statut d'un livrable (motif `LIVRABLE`)."""
    return any(s.start() <= x.start() and x.end() <= s.end() for s in LIVRABLE.finditer(ligne))


def occurrences():
    """Liste de (motif, fichier, numéro, texte de la ligne, message)."""
    out = []
    for r in perimetre():
        texte = lire(r)
        skill = '/'.join(r.split('/')[:2]) + '/' if r.startswith('skills/') else ''
        for n, ligne, titre in lignes_utiles(texte):
            for ident, motif, ou, msg in MOTIFS:
                if permis(r, ou):
                    continue
                if ident == 'preseance' and r == 'REGLES_STUDIO.md' and SECTION_PRIORITE.match(titre):
                    continue
                if ident == 'propose' and not r.startswith(('referentiels/', 'skills/', 'agents/')):
                    continue
                trouve = [x for x in motif.finditer(ligne)
                          if not (ident == 'socle' and x.group(0) == 'SOCLE' and ligne[x.end():x.end() + 1] == '.')
                          and not (ident == 'propose' and statut_livrable(ligne, x))]
                if trouve:
                    out.append((ident, r, n, ligne.strip(), msg))
            for m in CHEMIN_CITE.finditer(ligne):
                cible = re.split(r'[§#:]', m.group(1) or m.group(2))[0].rstrip('/.,;)')
                if re.search(r'[<>*{}]|\.\.\.|…', cible) or '/' not in cible:
                    continue
                base = skill if cible.startswith('references/') else ''
                if not base and cible.startswith('references/'):
                    continue
                if not os.path.exists(os.path.join(PLUGIN, base + cible)):
                    out.append(('renvoi-mort', r, n, ligne.strip(), f'renvoi mort : `{base + cible}` absent du plugin'))
    table = table_decideurs()
    if table is None:
        out.append(('qui-decide', 'referentiels/REGLES_DETAIL.md', 0, '§ Qui décide absent',
                    'la table unique des décideurs (lignes D) manque'))
    else:
        agents = {f[:-3] for f in os.listdir(os.path.join(PLUGIN, 'agents')) if f.endswith('.md')}
        for ident, rangs in sorted(table.items()):
            if len(rangs) > 1:
                out.append(('qui-decide', 'referentiels/REGLES_DETAIL.md', 0, ident, f'{ident} : ligne en double'))
            decide = rangs[0].get('décide', '')
            if re.search(r',| et | ou |/|;|\+', decide):
                out.append(('qui-decide', 'referentiels/REGLES_DETAIL.md', 0, ident, f'{ident} : deux décideurs (« {decide} »)'))
            for col in ('propose', 'décide'):
                for nom in re.findall(r'[a-z][a-z-]+', rangs[0].get(col, '')):
                    if nom in agents and not re.search(r'\b' + ident + r'\b', lire(f'agents/{nom}.md')):
                        out.append(('qui-decide', f'agents/{nom}.md', 0, ident, f'{ident} non déclarée par l\'agent {nom}'))
    roles = roles_garde()
    for f in sorted(os.listdir(os.path.join(PLUGIN, 'agents'))):
        if not f.endswith('.md'):
            continue
        m = re.search(r'^tools:\s*(.*)$', lire('agents/' + f), re.M)
        outils = {t.strip() for t in (m.group(1).split(',') if m else [])}
        if outils & {'Bash', 'Write', 'Edit', 'NotebookEdit'} and f[:-3] not in roles:
            out.append(('agent-sans-role', 'agents/' + f, 0, f[:-3], f'{f[:-3]} a Bash, Write ou Edit sans rôle dans ROLES'))
    for d in ('skills', 'workflows'):
        for racine, _, fichiers in os.walk(os.path.join(PLUGIN, d)):
            for f in fichiers:
                if f.endswith(('.js', '.mjs')):
                    r = rel(os.path.join(racine, f))
                    for n, debut in appels_sans_type(lire(r)):
                        out.append(('agent-sans-type', r, n, debut, 'appel agent( sans agentType'))
    taille = taille_injectee()
    limite = seuils().get('injection', {}).get('regles_studio_caracteres_max', LIMITE_DEFAUT)
    if taille > limite:
        out.append(('taille', 'REGLES_STUDIO.md', 0, 'texte injecté trop long',
                    f'{taille} caractères injectés (chemin du cache et ligne du domaine compris), limite {limite}'))
    return out


def cle(o):
    return (o[0], o[1], o[3])


def charger_base():
    try:
        with open(BASE, encoding='utf-8') as f:
            return Counter(tuple(x) for x in json.load(f)['occurrences'])
    except (OSError, ValueError, KeyError):
        return None


def ecrire_base(compte):
    donnees = {'_note': 'Base gelée de verifier_coherence.py : elle ne peut que décroître (--geler retire, n\'ajoute jamais).',
               'occurrences': sorted([list(k) for k, n in compte.items() for _ in range(n)])}
    with open(BASE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1)
        f.write('\n')


STATUTS = re.compile(r"\bFIXÉ\b|\bVALIDÉE?S?\b|\bPROPOSÉE?S?\b|\bPROVISOIRE\b|\bQUESTION OUVERTE\b|\bAPPROUVE_PAR_\w+"
                     r"|(?i:\bvalidée?s? sur [A-Z]{2,3}\b|\bproposée? au plugin\b|\bà l['’]essai\b)")


def registre():
    entrees = []
    for r in perimetre():
        for n, ligne, _ in lignes_utiles(lire(r)):
            st = STATUTS.findall(ligne)
            if not st:
                continue
            entrees.append({'fichier': r, 'ligne': n,
                            'statuts': sorted({s.split()[0].upper() if s.lower().startswith(('validé', 'proposé'))
                                               and ' ' in s else s for s in st}),
                            'chaines': sorted(set(re.findall(r'\bsur ([A-Z]{2,3})\b', ligne))),
                            'dates': re.findall(r'\b\d{1,2}/\d{2}/\d{4}\b', ligne),
                            'versions': sorted(set(re.findall(r'\b\d\.\d{1,2}\.\d{1,2}\b', ligne))),
                            'extrait': ligne.strip()[:200]})
    return entrees


def lignes_normatives():
    compte = Counter()
    for r in perimetre():
        for _, ligne, _ in lignes_utiles(lire(r)):
            s = ligne.strip()
            if s and not s.startswith('#') and not re.match(r'^\|?\s*:?-{3,}', s):
                compte[r.split('/')[0]] += 1
    return compte


def mode_chaine(chaine):
    """Rapport seulement : écarts orphelins et écarts qui visent une ligne D."""
    table = table_decideurs() or {}
    connus = set(table) | cles(seuils())
    try:
        ecarts = open(os.path.join(chaine, 'direction', 'ECARTS.md'), encoding='utf-8').read()
    except OSError:
        print('Chaîne : pas de direction/ECARTS.md.')
        return 0
    tous = re.findall(r'Remplace\s*:\s*`?([^\s`,;)]+)', ecarts)
    vus = [i for i in tous if re.fullmatch(r'[A-Z]\d{2}|[a-z_]+(?:\.[a-z0-9_]+)+', i)]
    print(f'Chaîne {chaine} : {len(vus)} écart(s) « Remplace : <id> », {len(tous) - len(vus)} sans identifiant'
          ' (à migrer) ; rapport seulement, rien ne bloque.')
    for i in vus:
        if i not in connus:
            print(f'  - orphelin : « Remplace : {i} » ne vise rien dans la version installée')
        elif i in table:
            print(f'  - à signaler : l\'écart vise la ligne {i} (un seul décideur par choix)')
    return 0


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    args = sys.argv[1:]
    if '--registre' in args:
        chemin = args[args.index('--registre') + 1]
        entrees = registre()
        with open(chemin, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(entrees, f, ensure_ascii=False, indent=1)
        par = Counter(s for e in entrees for s in e['statuts'])
        print(f'Registre des tampons : {len(entrees)} ligne(s) dans {len({e["fichier"] for e in entrees})} fichier(s) → {chemin}')
        for s, n in par.most_common():
            print(f'  {s:<22} {n}')
        return 0
    try:
        top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    except OSError:
        top = ''
    dans_depot = (os.path.isfile(os.path.join(DEPOT, '.claude-plugin', 'marketplace.json'))
                  and os.path.exists(os.path.join(DEPOT, '.git'))
                  and top and os.path.normcase(os.path.abspath(top)) == os.path.normcase(DEPOT))
    if not dans_depot and '--rapport' not in args and '--geler' not in args:
        return mode_chaine(os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd())
    if '--renomme' in args:
        # Un fichier renommé (git mv) garde ses occurrences connues : on les reporte sur le nouveau nom, sans rien ajouter.
        ancien, nouveau = args[args.index('--renomme') + 1:args.index('--renomme') + 3]
        base = charger_base() or Counter()
        reporte = Counter({(m, nouveau if f == ancien else f, t): n for (m, f, t), n in base.items()})
        ecrire_base(reporte)
        print(f'Base gelée : {sum(n for (m, f, t), n in base.items() if f == ancien)} occurrence(s) reportée(s) de {ancien} sur {nouveau}.')
        return 0
    occ = occurrences()
    actuel = Counter(cle(o) for o in occ)
    base = charger_base()
    if '--geler' in args:
        if base is None:
            ecrire_base(actuel)
            print(f'Base gelée créée : {sum(actuel.values())} occurrence(s) → {rel(BASE)}')
            return 0
        reste = base & actuel
        retire = base - reste
        nouvelles = actuel - base
        ecrire_base(reste)
        print(f'Base gelée : {sum(retire.values())} occurrence(s) retirée(s), {sum(reste.values())} restante(s) ; rien d\'ajouté.')
        if nouvelles:
            print(f'{sum(nouvelles.values())} occurrence(s) nouvelle(s) non ajoutée(s) : à corriger.')
        return 0
    base = base or Counter()
    nouvelles = actuel - base
    disparues = base - actuel
    if '--rapport' in args:
        par = Counter(o[0] for o in occ)
        print(f'Cohérence du plugin (rapport) : {len(occ)} occurrence(s), dont {sum(nouvelles.values())} hors de la base gelée.')
        for ident, n in sorted(par.items(), key=lambda x: -x[1]):
            fich = len({o[1] for o in occ if o[0] == ident})
            print(f'  {ident:<16} {n:>4} dans {fich} fichier(s)')
        norm = lignes_normatives()
        print(f'Lignes normatives (Markdown du plugin hors vendor/) : {sum(norm.values())} ; ' +
              ', '.join(f'{k} {v}' for k, v in sorted(norm.items())))
        print(f'Texte injecté : {taille_injectee()} caractères.')
        return 0
    print(f'Cohérence du plugin : {len(occ)} occurrence(s) connues, base gelée de {sum(base.values())}.')
    echec = False
    if nouvelles:
        echec = True
        print(f'REFUS : {sum(nouvelles.values())} occurrence(s) nouvelle(s) :')
        for o in occ:
            if nouvelles[cle(o)] > 0:
                nouvelles[cle(o)] -= 1
                print(f'  - {o[1]}:{o[2]} [{o[0]}] {o[4]}\n      « {o[3][:140]} »')
    if disparues:
        echec = True
        print(f'REFUS : {sum(disparues.values())} occurrence(s) corrigée(s) encore dans la base : lancer --geler, puis l\'ajouter au commit.')
    if not echec:
        print('OK : aucune contradiction nouvelle.')
    return 1 if echec else 0


if __name__ == '__main__':
    sys.exit(main())
