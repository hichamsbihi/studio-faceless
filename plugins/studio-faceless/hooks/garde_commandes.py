"""Garde-fou PreToolUse du plugin studio-faceless (Bash, PowerShell, Write, Edit).

Lit l'appel d'outil (JSON) sur l'entrée standard et répond, au besoin, « deny » ou « ask ».
Sans objection, il ne répond rien : l'appel suit le circuit normal des permissions.
Les chemins protégés sont relatifs au dossier de la chaîne (CLAUDE_PROJECT_DIR).

Pour tous :
- deny : publication, cloud, connexion ou mise à jour HyperFrames ; autre version par npx ; installation npm ;
  suppression récursive ou définitive (rm -r où que soit l'option, Remove-Item -Recurse, rd /s, find -delete,
  shutil.rmtree, rmSync récursif, rimraf, Directory.Delete récursif) ; vidage de la corbeille ;
  écriture par Write ou Edit dans le plugin installé (il se modifie dans son dépôt, pas depuis une chaîne) ;
  rendu direct sans `--workers 1` ou `2` ;
  1.0.1 (sécurité, validé sur AA, 04/11/2026, point 6 du conseil) : modal (sauf `modal run` d'un script du plugin installé),
  aws, sam, pip install ; printenv, et env, set, export, declare ou Get-ChildItem env: lancés seuls (env n'est plus un préfixe
  neutre : il n'est retiré que s'il précède une commande) ; toute commande qui nomme une clé ou un jeton (*_API_KEY, *_SECRET,
  *_TOKEN, MODAL_TOKEN_*), $env: compris ; [Environment]::GetEnvironmentVariable ; la lecture de tout l'environnement dans un
  script en ligne ou un here-document (os.environ ou process.env entiers) ; claude -p ;
- ask : aperçu HyperFrames ; `modal run` d'un script du plugin installé (1.0.1).
Par rôle, déduit du type d'agent (`agent_type` de l'entrée du hook, voir ROLES), ou option `--role` :
- lecteur (1.0.1) : research, conseiller, et tout sous-agent (`agent_id` présent) d'un type inconnu ou sans type ; Write et
  Edit seulement sous docs/rapports/ ; en Bash, seules des commandes de lecture (LECTEUR_COMMANDES), sorties seulement sous
  docs/rapports/, sans script en ligne ni substitution de commande ;
- relecteur (reviewer) : seules ffprobe, ffmpeg de mesure (-f null), wc, ls, grep, head et tail ; aucune redirection ;
- directeur-artistique : seules ffmpeg, ffprobe et mkdir ; pas d'écrasement (-y) ; sortie hors zones protégées ;
- producteur : en Bash, aucune mention de direction/, templates/, .claude/ ou d'un CLAUDE.md (sauf les chemins du
  plugin installé, pour lancer ses outils, sans « .. »), et aucune écriture
  vers un dossier existant de marque/, des entrées d'épisode ou un MP4 existant ; mêmes limites pour Write et Edit ;
- mainteneur : n'écrit qu'avec Write et Edit (aucune écriture en Bash), jamais dans .claude/, un projet de
  production, un dossier existant de marque/, des entrées d'épisode ou un MP4 ;
- stratege (strategist) : écrit seulement dans docs/ et direction/BANQUE_SUJETS.md ; en Bash, seules python (outils
  du plugin installé, sauf youtube_retention.py, réservé à Claude principal), ls, wc, grep, head, tail, mkdir et cd,
  sans script en ligne ni écriture hors de docs/.
- telechargeur (media-fetcher, 0.6.0) : écrit seulement sous episodes/<id>/kit/media/source-vN/ ; en Bash, seules python
  (outils/medias/telecharger_medias.py du plugin installé, dont les chemins sont sous ce dossier), ls, wc, grep, head, tail,
  mkdir et cd, sans script en ligne : ni curl ni wget, tout passe par l'outil (pause, agent identifié, aucun écrasement).
- ingenieur-son (sound-manager, 0.7.0 ; shorts depuis la 0.7.1) : écrit seulement dans kit/voix/, kit/shorts/voix/,
  kit/shorts/son/, kit/media/audio/, kit/media/source-vN/soundza/, kit/PROVENANCE.md, montage/ (sauf montage.json) et
  outputs/controle-son*/ de l'épisode ; en Bash, seules python (ses outils du plugin installé, table OUTILS : generer_voix.py
  à blanc seulement, mesurer_mix.py avec son rapport dans la zone, ni mix_film.py, ni assembler.py, ni master_short.py),
  ffmpeg (sans -y,
  sorties dans sa zone), ffprobe, cp (sans écrasement), ls, wc, grep, head, tail, mkdir, date, sha1sum, sha256sum et cd vers
  la racine ; aucun script en ligne ni substitution de commande.
- editeur (publisher, 0.7.0) : écrit seulement dans miniatures-vN/, PUBLICATION_vN.md et PUBLICATION_vN.<langue>.srt de
  l'épisode ; en Bash, les mêmes commandes, avec ses outils (miniature.py, publication.py, srt.py, controle.py chrome) et node
  pour `hyperframes.mjs remove-background` seulement.
  Pour ces deux rôles, chaque option d'un outil est lue dans sa table : une option inconnue ou abrégée est refusée, et un
  chemin où l'outil écrit doit être dans la zone, qu'il ait une espace, aucune barre oblique ou la forme --option=valeur.
  Un script écrit par l'agent (mesures du mix sous montage/mesures-vN/, masque de détourage sous miniatures-vN/travail/) n'est
  jamais lancé par lui : le garde ne lit pas le contenu d'un script ; Claude principal le relit et le lance (décision du
  03/11/2026 ; `mesurer_mix.py` existe depuis la 1.1.2, `miniature.py masque` reste prévu).
"""
import json
import os
import re
import shlex
import sys

I = re.IGNORECASE
HF = r'\bhyperframes(?:\.mjs)?(?:@\S+)?'

DENY_TEXT = [
    (re.compile(HF + r'\s+(publish|cloud|cloudrun|lambda|auth|login)\b', I),
     "publication, rendu cloud ou connexion HyperFrames : interdit sans décision du propriétaire"),
    (re.compile(HF + r'\s+upgrade\b', I), "mise à jour de HyperFrames : interdite sans décision du propriétaire (0.8.149 figée)"),
    (re.compile(HF + r'\s+skills\s+(update|install|add)\b', I), "mise à jour des skills : interdite sans décision du propriétaire"),
    (re.compile(r'\bnpx\s+(?:-y\s+|--yes\s+)?hyperframes@', I), "autre version de HyperFrames que la 0.8.149 figée"),
    (re.compile(r'\bnpm\s+(install|i|add|update|up|upgrade|uninstall|remove|rm|un)\b', I),
     "installation ou mise à jour npm : nouvelle dépendance, à décider par le propriétaire"),
    (re.compile(r'\bremove-item\b[^|;\n]*\s-r(ec\w*)?\b', I), "suppression récursive : passer par la corbeille, avec accord"),
    (re.compile(r'\b(rd|rmdir|del|erase)\s+(/[a-z]\s+)*/s\b', I), "suppression récursive : passer par la corbeille, avec accord"),
    (re.compile(r'\bfind\b[^|;\n]*\s(-delete\b|-exec\s+rm\b)', I), "suppression par find : passer par la corbeille, avec accord"),
    (re.compile(r'shutil\.rmtree|os\.removedirs|\brimraf\b|(rmSync|rmdirSync|promises\.rm)\s*\([^)]*recursive', I),
     "suppression récursive par script : passer par la corbeille, avec accord"),
    (re.compile(r'Directory\]?::Delete\s*\([^)]*\$?true', I), "suppression récursive (.NET) : passer par la corbeille, avec accord"),
    (re.compile(r'DeletePermanently', I), "suppression définitive : interdite"),
    (re.compile(r'\bClear-RecycleBin\b', I), "vidage de la corbeille : interdit"),
]
ASK_TEXT = [(re.compile(HF + r'\s+preview\b', I),
             "aperçu HyperFrames : son Chrome reste ouvert jusqu'à l'arrêt ; à lancer seulement sur demande")]
RENDER = re.compile(HF + r'\s+render\b', I)
WORKERS_OK = re.compile(r'(--workers[ =]|-w[ =]?)[12]\b', I)

WRAPPERS = {'sudo', 'xargs', 'command', 'nohup', 'time', 'exec'}     # env (1.0.1) : voir tokens() et sans_env()
RECURSIVE_FLAG = re.compile(r'^(-[a-z]*r[a-z]*|--recursive|-recurse|/s)$', I)
WRITE_CMDS = {'cp', 'mv', 'install', 'tee', 'touch', 'copy-item', 'move-item', 'rename-item', 'set-content', 'add-content',
              'out-file', 'new-item', 'copy', 'move', 'ren', 'rename', 'xcopy', 'robocopy', 'ffmpeg', 'dd', 'ln'}
REDIRECT = re.compile(r'(?<![0-9&])>>?\s*("[^"]+"|\'[^\']+\'|[^\s|;&]+)')
INLINE_CODE = re.compile(r'\b(python3?|py|node|pwsh|powershell)(\.exe)?\b[^\n]*?\s-(c|e|command)\b', I)
INLINE_WRITE = re.compile(r'(write|open\([^)]*[\'"][wa]|unlink|remove|rename|copy|rmtree|mkdir|makedirs|move)', I)


def segments(command):
    return [s.strip() for s in re.split(r'&&|\|\||;|\||\n', command) if s.strip()]


def tokens(segment):
    try:
        toks = shlex.split(segment, posix=False)
    except ValueError:
        toks = segment.split()
    toks = [t.strip('"\'') for t in toks]
    while toks:
        if toks[0].lower() in WRAPPERS or re.match(r'^\w+=', toks[0]):
            toks = toks[1:]
        elif re.sub(r'\.exe$', '', os.path.basename(toks[0]).lower()) == 'env' and sans_env(toks):
            toks = sans_env(toks)          # env suivi d'une commande : la commande est contrôlée ; env seul reste visible
        elif len(toks) > 1 and toks[0].lower() in ('cmd', 'cmd.exe') and toks[1].lower() in ('/c', '/k'):
            toks = toks[2:]
        else:
            break
    return toks


def sans_env(toks):
    """1.0.1 : ce que lance `env` (sans ses options ni ses affectations) ; [] si env est lancé seul."""
    reste, i = toks[1:], 0
    while i < len(reste):
        t = reste[i]
        if t in ('-S', '--split-string') and i + 1 < len(reste):
            try:
                return shlex.split(reste[i + 1], posix=False) + reste[i + 2:]
            except ValueError:
                return reste[i + 1].split() + reste[i + 2:]
        if t in ('-u', '--unset', '-C', '--chdir'):
            i += 2
        elif t.startswith('-') or re.match(r'^\w+=', t):
            i += 1
        else:
            break
    return reste[i:] if sans_redirections(reste[i:]) else []      # « env > fichier » : env seul, redirigé


def head(toks):
    return re.sub(r'\.(exe|cmd|ps1)$', '', os.path.basename(toks[0]).lower()) if toks else ''


def recursive_rm(command):
    for seg in segments(command):
        toks = tokens(seg)
        if head(toks) in ('rm', 'rmdir', 'rd', 'del', 'erase', 'ri', 'remove-item') and any(RECURSIVE_FLAG.match(t) for t in toks[1:]):
            return True
    return False


def project_rel(path, root):
    """Chemin relatif au dossier de la chaîne (minuscules, « / »), ou None s'il est hors du projet."""
    if not path:
        return None
    p = path.strip('"\'')
    if re.match(r'^/[a-z]/', p, I):            # /c/Users/... (Git Bash)
        p = p[1] + ':' + p[2:]
    full = os.path.normcase(os.path.abspath(os.path.join(root, p)))
    base = os.path.normcase(os.path.abspath(root))
    if not (full == base or full.startswith(base + os.sep)):
        return None
    return os.path.relpath(full, base).replace('\\', '/')


def protected(rel, root, zones):
    """Raison si le chemin relatif tombe dans une zone protégée, sinon None."""
    if rel is None:
        return None
    parts = rel.split('/')
    if 'core' in zones and (parts[0] in ('direction', 'templates', '.claude') or parts[-1] == 'claude.md'):
        return "direction/, templates/, .claude/ et les CLAUDE.md sont protégés"
    if '.claude' in zones and parts[0] == '.claude':
        return ".claude/ est protégé"
    if 'marque' in zones and parts[0] == 'marque' and len(parts) > 2 and os.path.isdir(os.path.join(root, 'marque', parts[1])):
        return "un dossier existant de marque/ ne se modifie pas ; nouvelle version = nouveau dossier"
    if 'inputs' in zones and len(parts) > 2 and parts[0] == 'episodes' and parts[2] == 'inputs':
        return "les entrées d'origine d'un épisode sont en lecture seule"
    if 'production' in zones and len(parts) > 3 and parts[0] == 'episodes' and parts[2] == 'production':
        return "les projets de production sont réservés au producteur, sur contrat"
    if 'mp4' in zones and rel.endswith('.mp4') and os.path.exists(os.path.join(root, rel)):
        return "un export existant n'est jamais écrasé"
    return None


def write_targets(seg):
    """Cibles d'écriture probables d'un segment de commande (heuristique)."""
    targets = [m.strip('"\'') for m in REDIRECT.findall(seg) if m.lower() not in ('/dev/null', 'nul', '$null')]
    toks = tokens(seg)
    h = head(toks)
    args = [t for t in toks[1:] if not t.startswith('-')]
    if h in ('cp', 'mv', 'install', 'copy-item', 'move-item', 'copy', 'move', 'xcopy', 'robocopy', 'ln', 'ffmpeg') and args:
        targets.append(args[-1])
    if h in ('tee', 'touch', 'rename-item', 'set-content', 'add-content', 'out-file', 'new-item', 'ren', 'rename', 'mkdir'):
        targets += args
    if h == 'sed' and any(t.startswith('-i') for t in toks):
        targets += args[-1:]
    return targets


def sans_plugin(command):
    """La commande, chemins du plugin installé remplacés par PLUGIN : un producteur peut lancer les outils du plugin,
    dont le cache est sous ~/.claude/plugins/ (sinon la règle « .claude/ » les bloquerait)."""
    plugin = (os.environ.get('CLAUDE_PLUGIN_ROOT') or '').replace('\\', '/').rstrip('/')
    if not plugin:
        return command
    formes = {plugin, plugin.replace('/', '\\')}
    if re.match(r'^[a-z]:/', plugin, I):
        formes.add('/' + plugin[0].lower() + plugin[2:])          # /c/Users/... (Git Bash)
    for f in formes:
        command = re.sub(re.escape(f) + r'[^\s"\'|;&]*', lambda m: m.group(0) if '..' in m.group(0) else 'PLUGIN', command, flags=I)
    return command


# --- 1.0.1 : clés, cloud, environnement, claude -p ; pour tous, Claude principal compris (validé sur AA, 04/11/2026) ----------
NOM_DE_CLE = re.compile(r'\b[a-z0-9]\w*_(api_key|secret|token)\b|\bmodal_token_\w+', I)
ENV_DOTNET = re.compile(r'Environment\]::GetEnvironmentVariables?\b', I)
HEREDOC = re.compile(r'<<-?\s*[\'"]?\w+')
ENV_ENTIER = re.compile(r'\bos\.environb?\b(?!\s*\[|\s*\.get\s*\()|\bprocess\.env\b(?!\s*\.\w|\s*\[)', I)
SHELLS = {'bash', 'sh', 'zsh', 'dash', 'pwsh', 'powershell'}
PYTHONS = {'python', 'python3', 'py'}
MODAL_INTERDIT = {'setup', 'token', 'deploy', 'serve', 'secret'}
LISTE_ENV_PS = {'get-childitem', 'gci', 'ls', 'dir', 'get-item', 'gi'}


def premier_mot(toks):
    """Premier argument qui n'est pas une option (une sous-commande), en minuscules, ou ''."""
    return next((t.lower() for t in toks if not t.startswith('-')), '')


def verdict_pour_tous(command, profondeur=0):
    """Motifs de la 1.0.1 : ('deny', raison), ('ask', raison) pour `modal run` d'un script du plugin, ou None."""
    if NOM_DE_CLE.search(command):
        return 'deny', ("commande qui nomme une clé ou un jeton (…_API_KEY, …_SECRET, …_TOKEN, MODAL_TOKEN_…) : les clés restent "
                        "dans l'environnement et ne s'écrivent dans aucune commande ; un texte qui les nomme s'écrit avec Write ou Edit")
    if ENV_DOTNET.search(command):
        return 'deny', "lecture des variables d'environnement par [Environment]::GetEnvironmentVariable : interdite"
    if (INLINE_CODE.search(command) or HEREDOC.search(command)) and ENV_ENTIER.search(command):
        return 'deny', "script qui lit tout l'environnement (os.environ ou process.env entiers) : lire une variable nommée, jamais une clé"
    demande = None
    for seg in segments_cites(command):
        toks = sans_redirections(tokens(seg))
        h, args = head(toks), toks[1:]
        if h == 'env':
            return 'deny', "env lancé seul affiche tout l'environnement, clés comprises : interdit"
        if h == 'printenv':
            return 'deny', "printenv affiche l'environnement, clés comprises : interdit"
        if (h == 'set' and not args) or (h == 'export' and all(a == '-p' for a in args)) \
                or (h in ('declare', 'typeset') and all(a.startswith('-') for a in args)) \
                or (h == 'compgen' and any(a in ('-e', '-v') for a in args)):
            return 'deny', h + " sans nom affiche toutes les variables, clés comprises : interdit"
        if h in LISTE_ENV_PS and any(a.lower().replace('\\', '/') in ('env:', 'env:/', 'env:*', 'env:/*') for a in args):
            return 'deny', "liste du lecteur env: de PowerShell (clés comprises) : interdite"
        module, sous = None, []
        if h in PYTHONS and '-m' in args and args.index('-m') + 1 < len(args):
            module, sous = args[args.index('-m') + 1].lower(), args[args.index('-m') + 2:]
        if h in ('aws', 'sam') or module == 'awscli':
            return 'deny', "AWS (aws, sam) : aucun compte ni service de cloud sans décision du propriétaire"
        if (h in ('pip', 'pip3', 'pipx') and premier_mot(args) == 'install') or (module in ('pip', 'pip3') and premier_mot(sous) == 'install') \
                or (h == 'uv' and [a.lower() for a in args[:2]] == ['pip', 'install']):
            return 'deny', "pip install : nouvelle dépendance, à décider par le propriétaire"
        if h == 'modal' or module == 'modal':
            reste = args if h == 'modal' else sous
            sc = premier_mot(reste)
            if sc in MODAL_INTERDIT:
                return 'deny', "Modal : jeton, déploiement, service et secret interdits ; aucun jeton Modal sans décision du propriétaire"
            if sc == 'run':
                apres = reste[[a.lower() for a in reste].index('run') + 1:]
                script = next((a for a in apres if not a.startswith('-')), '').split('::')[0]
                if outil_du_plugin(script) is None:
                    return 'deny', "modal run seulement sur un script du plugin installé (chemin complet, sans « .. »)"
                demande = demande or ('ask', "modal run : rendu dans le cloud, payant ; à confirmer par le propriétaire")
            elif sc:
                return 'deny', "Modal : seul « modal run » d'un script du plugin installé est permis, avec confirmation"
        if (h == 'claude' or (h == 'npx' and any('claude-code' in a for a in args))) \
                and any(a in ('-p', '--print') or a.startswith('--print=') for a in args):
            return 'deny', "claude -p : aucun lancement de Claude sans le propriétaire, dans sa session"
        if h in SHELLS and profondeur < 3:
            i = next((k for k, a in enumerate(args) if a.lower() in ('-c', '-command')), None)
            if i is not None and i + 1 < len(args):
                v = verdict_pour_tous(' '.join(args[i + 1:]), profondeur + 1)
                if v and v[0] == 'deny':
                    return v
                demande = demande or v
    return demande


# --- 1.0.1 : rôle lecteur (research, conseiller, sous-agent d'un type inconnu ou sans type) ---------------------------------
LECTEUR_COMMANDES = {'ls', 'cat', 'head', 'tail', 'wc', 'grep', 'rg', 'find', 'file', 'stat', 'du', 'df', 'pwd', 'cd', 'echo',
                     'printf', 'sort', 'cut', 'tr', 'diff', 'cmp', 'sha1sum', 'sha256sum', 'md5sum', 'ffprobe', 'git', 'date',
                     'basename', 'dirname', 'realpath', 'which', 'true'}
GIT_LECTURE = {'status', 'log', 'diff', 'show', 'ls-files', 'rev-parse', 'blame', 'describe', 'shortlog'}
FIND_ACTIONS = {'-delete', '-exec', '-execdir', '-ok', '-okdir', '-fprint', '-fprint0', '-fprintf', '-fls'}


def ecriture_lecteur(rel):
    """Le lecteur n'écrit que sous docs/rapports/ de la chaîne."""
    return rel is not None and rel.lower().startswith('docs/rapports/')


def refus_lecteur(command, root):
    """Limites du rôle lecteur en Bash ; raison du refus, ou None."""
    if INLINE_CODE.search(command) or re.search(r'\$\(|`|<\(|>\(', command):
        return "aucun script en ligne ni substitution de commande"
    for seg in segments_cites(command):
        toks = sans_redirections(tokens(seg))
        h, bas = head(toks), [t.lower() for t in toks[1:]]
        if h not in LECTEUR_COMMANDES:
            return "seules des commandes de lecture sont permises (refusé : " + seg[:120] + ")"
        for t in REDIRECT_TOUT.findall(seg):
            t = t.strip('"\'')
            if t.lower() not in SANS_FICHIER and not ecriture_lecteur(project_rel(t, root)):
                return "écriture seulement sous docs/rapports/ (refusé : " + t[:120] + ")"
        if h == 'find' and FIND_ACTIONS & set(bas):
            return "find sans action (-delete, -exec, -ok, -fprint, -fls)"
        if h == 'sort' and any(t == '-o' or t.startswith('--output') or re.match(r'^-[a-z]*o', t) for t in bas):
            return "sort sans fichier de sortie (-o)"
        if h == 'ffprobe' and any(t in ('-o', '-output') for t in bas):
            return "ffprobe sans fichier de sortie"
        if h == 'git':
            brut = toks[1:]                                     # « -C » (dossier) et « -c » (réglage) ne diffèrent que par la casse
            if any(t == '-c' or t.lower().startswith(('--output', '--exec-path', '--config-env')) for t in brut):
                return "git sans -c, --output ni --exec-path"
            i = 0
            while i < len(brut) and brut[i].startswith('-'):
                i += 2 if brut[i] == '-C' else 1
            if i >= len(brut) or brut[i].lower() not in GIT_LECTURE:
                return "git en lecture seulement (status, log, diff, show, ls-files, rev-parse, blame, describe, shortlog)"
    return None


def decide_bash(command, role, root):
    for rx, why in DENY_TEXT:
        if rx.search(command):
            return 'deny', why
    if recursive_rm(command):
        return 'deny', "suppression récursive : passer par la corbeille, avec accord"
    demande = verdict_pour_tous(command)
    if demande and demande[0] == 'deny':
        return demande

    if role == 'lecteur':
        why = refus_lecteur(command, root)
        if why:
            return 'deny', "lecteur : " + why

    if role == 'relecteur':
        for seg in segments(command):
            toks = tokens(seg)
            h = head(toks)
            if h not in ('ffprobe', 'ffmpeg', 'wc', 'ls', 'grep', 'head', 'tail'):
                return 'deny', "relecteur : seules ffprobe, ffmpeg de mesure, wc, ls, grep, head et tail sont permises (refusé : " + seg[:120] + ")"
            if h == 'ffmpeg' and not any(a == '-f' and b == 'null' for a, b in zip(toks, toks[1:])):
                return 'deny', "relecteur : ffmpeg seulement pour mesurer (-f null -), sans fichier de sortie"
            if [m for m in REDIRECT.findall(seg) if m.lower() not in ('/dev/null', 'nul', '$null')]:
                return 'deny', "relecteur : aucune écriture (redirection refusée)"

    if role == 'directeur-artistique':
        for seg in segments(command):
            toks = tokens(seg)
            if head(toks) not in ('ffmpeg', 'ffprobe', 'mkdir'):
                return 'deny', "directeur artistique : seules ffmpeg, ffprobe et mkdir sont permises (refusé : " + seg[:120] + ")"
            if head(toks) == 'ffmpeg' and '-y' in toks:
                return 'deny', "directeur artistique : pas d'écrasement (-y) ; écrire dans un dossier neuf"
            for t in write_targets(seg):
                why = protected(project_rel(t, root), root, {'core', 'marque', 'inputs', 'production', 'mp4'})
                if why:
                    return 'deny', "directeur artistique : sortie refusée, " + why

    if role == 'producteur':
        for seg in segments(command):
            for t in write_targets(seg):
                if protected(project_rel(t, root), root, {'core'}):
                    return 'deny', "producteur : écriture interdite dans direction/, templates/, .claude/ et les CLAUDE.md"
        if re.search(r'(^|[\s"\'=/\\])(direction|templates|\.claude)[/\\]|claude\.md', sans_plugin(command), I):
            return 'deny', "producteur : direction/, templates/, .claude/ et les CLAUDE.md se lisent avec Read ou Grep, jamais par Bash"
        for seg in segments(command):
            for t in write_targets(seg):
                why = protected(project_rel(t, root), root, {'marque', 'inputs', 'mp4'})
                if why:
                    return 'deny', "producteur : " + why
        if INLINE_CODE.search(command) and re.search(r'marque|inputs', command, I) and INLINE_WRITE.search(command):
            return 'deny', "producteur : écriture par script en ligne vers marque/ ou inputs/"

    if role == 'mainteneur':
        if INLINE_CODE.search(command) and INLINE_WRITE.search(command):
            return 'deny', "mainteneur : aucune écriture par script en ligne ; utiliser Write ou Edit"
        for seg in segments(command):
            toks = tokens(seg)
            if write_targets(seg) or head(toks) in WRITE_CMDS:
                return 'deny', "mainteneur : aucune écriture par Bash ; utiliser Write ou Edit (refusé : " + seg[:120] + ")"

    if role == 'stratege':
        if INLINE_CODE.search(command):
            return 'deny', "stratège : aucun script en ligne ; seulement les outils du plugin"
        for seg in segments(command):
            toks = tokens(seg)
            h = head(toks)
            if h not in ('python', 'python3', 'py', 'ls', 'wc', 'grep', 'head', 'tail', 'mkdir', 'cd'):
                return 'deny', "stratège : seules python (outils du plugin), ls, wc, grep, head, tail, mkdir et cd sont permises (refusé : " + seg[:120] + ")"
            if h in ('python', 'python3', 'py'):
                if 'PLUGIN' not in sans_plugin(seg):
                    return 'deny', "stratège : python seulement pour les outils du plugin installé"
                if re.search(r'youtube_retention', seg, I):
                    return 'deny', "stratège : youtube_retention.py (accès OAuth à la chaîne) est réservé à Claude principal"
                # Un outil écrit par son argument de sortie, que write_targets ne voit pas : tout chemin hors du plugin reste dans docs/.
                for a in tokens(sans_plugin(seg))[1:]:
                    if a.startswith('-') or a.startswith('@') or a == 'PLUGIN' or a.startswith('PLUGIN/') or a.startswith('PLUGIN\\'):
                        continue
                    if ('/' in a or '\\' in a or '.' in a) and not ecriture_stratege(project_rel(a, root)):
                        return 'deny', "stratège : un outil ne lit et n'écrit que dans docs/ de la chaîne (refusé : " + a[:120] + ")"
            for t in write_targets(seg):
                if not ecriture_stratege(project_rel(t, root)):
                    return 'deny', "stratège : écriture seulement dans docs/ de la chaîne (refusé : " + t[:120] + ")"

    if role == 'telechargeur':
        if INLINE_CODE.search(command):
            return 'deny', "téléchargeur : aucun script en ligne ; seulement telecharger_medias.py"
        for seg in segments(command):
            toks = tokens(seg)
            h = head(toks)
            if h not in ('python', 'python3', 'py', 'ls', 'wc', 'grep', 'head', 'tail', 'mkdir', 'cd'):
                return 'deny', "téléchargeur : seules python (telecharger_medias.py), ls, wc, grep, head, tail, mkdir et cd sont permises (refusé : " + seg[:120] + ")"
            if h in ('python', 'python3', 'py'):
                apres = tokens(seg)[1:]
                script = next((t for t in apres if not t.startswith('-')), '')
                if sans_plugin(script) != 'PLUGIN' or not script.replace('\\', '/').endswith('/outils/medias/telecharger_medias.py'):
                    return 'deny', "téléchargeur : python seulement pour outils/medias/telecharger_medias.py du plugin installé"
                option = None                                                   # option dont la valeur suit
                for a in apres[apres.index(script) + 1:]:
                    if option is None and a.startswith('-'):
                        nom, egal, valeur = a.partition('=')
                        if nom not in OPTIONS_TELECHARGEUR or (egal and OPTIONS_TELECHARGEUR[nom] is None):
                            return 'deny', "téléchargeur : option inconnue ou abrégée de telecharger_medias.py (refusé : " + a[:120] + ")"
                        if OPTIONS_TELECHARGEUR[nom] is None:
                            continue
                        if not egal:
                            option = nom
                            continue
                        a = valeur
                    else:
                        nom, option = option, None
                    if nom is not None and not OPTIONS_TELECHARGEUR[nom]:
                        continue                                                # robot, pause, essais : pas un chemin
                    rel = project_rel(a, root)                                  # tout autre argument est un chemin, même avec une espace
                    if not (ecriture_telechargeur(rel) if nom else lecture_telechargeur(rel)):   # dépôt et manifeste sous source-vN ; la liste sous kit/
                        return 'deny', "téléchargeur : liste sous episodes/<id>/kit/, dépôt et manifeste sous episodes/<id>/kit/media/source-vN/ (refusé : " + a[:120] + ")"
            for t in write_targets(seg):
                if not ecriture_telechargeur(project_rel(t, root)):
                    return 'deny', "téléchargeur : écriture seulement sous episodes/<id>/kit/media/source-vN/ (refusé : " + t[:120] + ")"

    if role in ZONES:
        why = refus_outils(command, role, root)
        if why:
            return 'deny', NOMS_ROLES[role] + " : " + why

    for rx, why in ASK_TEXT:
        if rx.search(command):
            return 'ask', why
    if RENDER.search(command) and not WORKERS_OK.search(command):
        return 'deny', "rendu HyperFrames sans « --workers 1 » ou « 2 » : relancer avec --workers 1 (un Chrome par processus)"
    return demande


def ecriture_stratege(rel):
    """Le stratège écrit dans docs/ et dans la banque de sujets, rien d'autre."""
    return rel is not None and (rel.lower().startswith('docs/') or rel.lower() == 'direction/banque_sujets.md')


# Options de telecharger_medias.py : True, la valeur est un chemin où l'outil écrit ; False, une valeur qui n'est pas un chemin ;
# None, sans valeur. L'outil refuse les abréviations (allow_abbrev=False) : seuls les noms entiers sont connus ici.
OPTIONS_TELECHARGEUR = {'--racine': True, '--manifeste': True, '--agent-utilisateur': False, '--pause': False,
                        '--essais': False, '--executer': None}


DEPOT_TELECHARGEMENT = re.compile(r'^episodes/[^/]+/kit/media/source-v\d+(/|$)', re.IGNORECASE)


LISTE_TELECHARGEMENT = re.compile(r'^episodes/[^/]+/kit/', re.IGNORECASE)


def ecriture_telechargeur(rel):
    """Le téléchargeur dépose dans kit/media/source-vN/ de l'épisode ; rien d'autre."""
    return rel is not None and bool(DEPOT_TELECHARGEMENT.match(rel))


def lecture_telechargeur(rel):
    """Il lit sa liste dans le kit de l'épisode."""
    return rel is not None and bool(LISTE_TELECHARGEMENT.match(rel))


# --- Rôles de la 0.7.0 : ingenieur-son (sound-manager) et editeur (publisher), décidés sur AA le 03/11/2026 -------------
# Une zone d'écriture, une liste de commandes et une table des outils du plugin permis. Dans la table, chaque option et chaque
# argument de position a un genre : 'ecrit' (chemin où l'outil écrit : dans la zone), 'lit' (chemin lu), 'v' (valeur qui
# n'est pas un chemin), 'v*' (plusieurs valeurs), un tuple de genres (nombre fixe de valeurs, comme nargs=2 : la valeur
# suivante redevient un argument de position) ou None (option sans valeur). Une option absente de la table est refusée,
# donc aussi une option abrégée (argparse accepte les préfixes : « --exec » vaut « --executer »).
EPISODE = r'^episodes/[^/]+/'
ZONES = {
    'ingenieur-son': re.compile(EPISODE + r'(kit/voix(/|$)|kit/shorts/(voix|son)(/|$)|kit/media/audio(/|$)|kit/media/source-v\d+/soundza(/|$)'
                                r'|kit/provenance\.md$|montage($|/(?!montage\.json$))|outputs/controle-son[^/]*(/|$))', I),
    'editeur': re.compile(EPISODE + r'(miniatures-v\d+(/|$)|publication_v\d+\.md$|publication_v\d+\.[a-z]{2}(-[a-z]{2})?\.srt$)', I),
}
NOMS_ROLES = {'ingenieur-son': 'ingénieur du son', 'editeur': 'éditeur'}
TEXTE_ZONES = {
    'ingenieur-son': "kit/voix/, kit/shorts/voix/, kit/shorts/son/, kit/media/audio/, kit/media/source-vN/soundza/, "
                     "kit/PROVENANCE.md, montage/ (sauf montage.json) et outputs/controle-son*/ de l'épisode",
    'editeur': "miniatures-vN/, PUBLICATION_vN.md et PUBLICATION_vN.<langue>.srt de l'épisode",
}
_COMMUNES = {'python', 'python3', 'py', 'ffmpeg', 'ffprobe', 'cp', 'ls', 'wc', 'grep', 'head', 'tail', 'mkdir', 'cd', 'date',
             'sha1sum', 'sha256sum'}
COMMANDES = {'ingenieur-son': _COMMUNES, 'editeur': _COMMUNES | {'node'}}
_CONTROLE_SON = {'niveau': {'pos': ['lit']}, 'son': {'pos': ['lit'], 'opts': {'--reference': 'lit', '--voix': 'lit'}},
                 'voix-reste': {'pos': ['lit', 'lit']}}
OUTILS = {
    'ingenieur-son': {
        # À blanc seulement (découpage et coût) : ni --executer ni --confirme-credits ; l'appel payant est lancé par Claude principal.
        'outils/voix/generer_voix.py': {'pos': ['lit'], 'opts': {
            '--voix': 'v', '--sortie': 'v', '--nom': 'v', '--prises': 'v*', '--blocs': 'v', '--modele': 'v', '--stabilite': 'v',
            '--similarite': 'v', '--format': 'v', '--facteur': 'v', '--max-caracteres': 'v'}},
        'outils/voix/info_elevenlabs.py': {'opts': {'--modeles': 'v*', '--tous': None, '--voix': 'v'}},
        'outils/controle/transcrire.py': {'pos': ['lit'], 'opts': {'--modele': 'lit', '--sortie': 'ecrit', '--texte': 'lit', '--isoler': 'v*'}},
        'outils/controle/ralentir.py': {'pos': ['lit', 'ecrit'], 'opts': {'--tempo': 'v', '--tete': 'v', '--queue': 'v', '--cible': 'v'}},
        'outils/controle/pauses.py': {'pos': ['lit', 'ecrit', 'lit', 'v']},
        'outils/controle/raccourcir.py': {'pos': ['lit', 'ecrit'], 'opts': {'--sequences': 'v', '--part': 'v', '--plancher': 'v', '--gardes': 'lit'}},
        'outils/controle/recaler.py': {'pos': ['lit', 'lit', 'lit', 'ecrit', 'v']},
        'outils/controle/mesurer_sons.py': {'pos': ['lit'], 'opts': {'--whisper': 'lit', '--crete-max': 'v', '--boucle': None}},
        # Mesure du mix sans écoute (1.1.2) : lit le mix, le film voix et le plan ; n'écrit que son rapport.
        'outils/montage/mesurer_mix.py': {'pos': ['lit', 'lit', 'lit'], 'opts': {
            '--journal': 'lit', '--log': 'lit', '--marque': 'v', '--sortie': 'ecrit'}},
        'outils/controle/controle.py': {'sous': _CONTROLE_SON},
        'outils/controle/publication.py': {'sous': {'mot': {'pos': ['lit', 'v']}}},
        # Voix des shorts (0.7.1, validé sur AA, 03/11/2026) ; le master du MP4 (master_short.py) reste à Claude principal.
        'outils/shorts/voix_short.py': {'pos': ['lit', 'ecrit'], 'opts': {'--plafond': 'v', '--sans-d': ('v', 'v'), '--cible': 'v'}},
        'outils/shorts/recaler.py': {'pos': ['lit', 'lit', 'ecrit']},
        'outils/shorts/raccord.py': {'pos': ['lit', 'lit', 'ecrit', 'v', 'v'], 'opts': {'--marge': 'v'}},
        'outils/medias/telecharger_medias.py': {'pos': ['lit'], 'opts': {
            '--racine': 'ecrit', '--manifeste': 'ecrit', '--agent-utilisateur': 'v', '--pause': 'v', '--essais': 'v', '--executer': None}},
    },
    'editeur': {
        'skills/thumbnail-strategist/scripts/miniature.py': {'sous': {
            'rendu': {'pos': ['lit', 'ecrit']},
            'mesure': {'pos': ['lit']},
            'planche': {'pos': ['ecrit', 'lit'], 'opts': {'--flux': 'lit'}},
            'grille': {'pos': ['lit', 'ecrit'], 'opts': {'--zone': 'v', '--echelle': 'v', '--pas': 'v', '--polygone': 'lit'}},
            'contraste': {'pos': ['v', 'v'], 'opts': {'--image': 'lit', '--zone': 'v'}}}},
        'outils/controle/controle.py': {'sous': {'chrome': {}}},
        'outils/controle/publication.py': {'sous': {
            'verifier': {'pos': ['lit'], 'opts': {'--journal': 'lit', '--srt': 'lit', '--exclure': 'v*', '--requete': 'v'}},
            'chapitres': {'pos': ['lit'], 'opts': {'--titre': 'v', '--repere': 'v', '--ignorer': 'v*'}},
            'mot': {'pos': ['lit', 'v']}}},
        'outils/montage/srt.py': {'opts': {'--script': 'lit', '--mots': 'v', '--journal': 'lit', '--sortie': 'ecrit'}},
    },
}
# `node node_modules/hyperframes/bin/hyperframes.mjs remove-background` (citty) : options de HyperFrames 0.8.149.
REMOVE_BACKGROUND = {'pos': ['lit'], 'opts': {'-o': 'ecrit', '--output': 'ecrit', '-b': 'ecrit', '--background-output': 'ecrit',
                                              '--device': 'v', '--quality': 'v', '--info': None, '--json': None}}
NOMBRE = re.compile(r'^[+-]?\d+(\.\d+)?$')
REDIRECT_TOUT = re.compile(r'>>?\s*("[^"]+"|\'[^\']+\'|[^\s|;&]+)')     # y compris 2> et &>
SANS_FICHIER = {'-', '/dev/null', 'nul', '$null'}
MEDIAS_ECRITS = {'.mp4', '.mov', '.webm', '.mkv', '.wav', '.mp3', '.flac', '.m4a', '.aac', '.ogg', '.opus', '.png', '.jpg',
                 '.jpeg', '.webp'}
FFMPEG_DRAPEAUX = {'-y', '-n', '-hide_banner', '-nostats', '-stats', '-nostdin', '-vn', '-an', '-sn', '-dn', '-shortest',
                   '-xerror', '-copyts', '-re', '-autorotate', '-noautorotate', '-accurate_seek', '-noaccurate_seek',
                   '-ignore_unknown', '-benchmark', '-report', '-dump', '-hex'}


def chemin_absolu(p, root):
    p = os.path.expanduser(p.strip('"\''))
    if re.match(r'^/[a-z]/', p, I):            # /c/Users/... (Git Bash)
        p = p[1] + ':' + p[2:]
    return os.path.abspath(os.path.join(root, p))


def outil_du_plugin(t):
    """Chemin de l'outil relatif au plugin installé (minuscules, « / »), ou None (hors du plugin, ou « .. »)."""
    plugin = (os.environ.get('CLAUDE_PLUGIN_ROOT') or '').replace('\\', '/').rstrip('/')
    p = t.strip('"\'').replace('\\', '/')
    if not plugin or '..' in p:
        return None
    p = p[1] + ':' + p[2:] if re.match(r'^/[a-z]/', p, I) else p
    plugin = plugin[1] + ':' + plugin[2:] if re.match(r'^/[a-z]/', plugin, I) else plugin
    return p[len(plugin) + 1:].lower() if p.lower().startswith(plugin.lower() + '/') else None


def sortie_refusee(t, role, root):
    """Raison du refus d'une cible d'écriture, ou None si elle est dans la zone du rôle."""
    if t.lower() in SANS_FICHIER:
        return None
    rel = project_rel(t, root)
    if rel is None or not ZONES[role].match(rel):
        return "écriture seulement dans " + TEXTE_ZONES[role] + " (refusé : " + t[:120] + ")"
    if rel.lower().endswith('.mp4'):
        return "aucun MP4 n'est écrit par ce rôle (refusé : " + t[:120] + ")"
    if os.path.splitext(rel)[1].lower() in MEDIAS_ECRITS and os.path.exists(chemin_absolu(t, root)):
        return "un média existant ne s'écrase pas (refusé : " + t[:120] + ")"
    return None


def arguments_refuses(args, spec, role, root):
    """Raison du refus si les arguments d'un outil sortent de sa table (voir OUTILS), sinon None."""
    if 'sous' in spec:
        if not args or args[0] not in spec['sous']:
            return "sous-commande non permise (refusé : " + (args[0] if args else '') + ")"
        spec, args = spec['sous'][args[0]], args[1:]
    pos, opts = spec.get('pos', []), spec.get('opts', {})
    attente, n = None, 0
    for a in args:
        if a.startswith('-') and not NOMBRE.match(a):
            nom, egal, valeur = a.partition('=')
            if nom not in opts:
                return "option inconnue ou abrégée (refusé : " + a[:120] + ")"
            genre, attente = opts[nom], None
            if genre is None:
                if egal:
                    return "option sans valeur (refusé : " + a[:120] + ")"
            elif egal:
                if isinstance(genre, tuple):
                    return "option à plusieurs valeurs écrite avec « = » (refusé : " + a[:120] + ")"
                if genre == 'ecrit' and sortie_refusee(valeur, role, root):
                    return sortie_refusee(valeur, role, root)
            else:
                attente = list(genre) if isinstance(genre, tuple) else genre
            continue
        if isinstance(attente, list):
            genre = attente.pop(0)
            attente = attente or None
        elif attente is not None:
            genre = attente
            if not attente.endswith('*'):
                attente = None
        elif pos:
            genre, n = pos[min(n, len(pos) - 1)], n + 1
        else:
            return "argument inattendu (refusé : " + a[:120] + ")"
        if genre == 'ecrit' and sortie_refusee(a, role, root):
            return sortie_refusee(a, role, root)
    return None


def sorties_ffmpeg(toks):
    """Fichiers écrits par ffmpeg : tout argument qui n'est ni une option, ni sa valeur, ni une entrée (-i), le dernier argument,
    et le `file=` d'un filtre (ametadata…)."""
    sorties, valeur = [], False
    for t in toks[1:]:
        if valeur:
            valeur = False
        elif t.startswith('-') and t != '-':
            valeur = t.lower() not in FFMPEG_DRAPEAUX
        else:
            sorties.append(t)
    if len(toks) > 1 and not toks[-1].startswith('-'):
        sorties.append(toks[-1])
    for t in toks[1:]:
        sorties += re.findall(r'(?:^|[:,;\[=])file=([^:,;\]]+)', t)
    return sorties


def segments_cites(command):
    """Segments d'une commande coupés sur &&, ||, ;, |, & et les fins de ligne hors guillemets (un filtre ffmpeg en contient)."""
    segs, cur, q, i = [], '', None, 0
    while i < len(command):
        c = command[i]
        if q:
            cur += c
            q = None if c == q else q
        elif c in '"\'':
            q, cur = c, cur + c
        elif command.startswith(('&&', '||'), i):
            segs.append(cur)
            cur, i = '', i + 2
            continue
        elif c in ';|\n' or (c == '&' and command[i - 1:i] != '>' and command[i + 1:i + 2] != '>'):
            segs.append(cur)
            cur = ''
        else:
            cur += c
        i += 1
    segs.append(cur)
    return [s.strip() for s in segs if s.strip()]


def sans_redirections(toks):
    """Les arguments sans les redirections (2>&1, > fichier, < entrée), contrôlées à part."""
    out, sauter = [], False
    for t in toks:
        if sauter:
            sauter = False
        elif re.fullmatch(r'\d*>>?|&>>?|<', t):
            sauter = True
        elif not re.match(r'^(\d*>>?|&>>?|<)\S', t):
            out.append(t)
    return out


def refus_outils(command, role, root):
    """Limites des rôles ingenieur-son et editeur en Bash ; raison du refus, ou None."""
    if INLINE_CODE.search(command) or re.search(r'\$\(|`|<\(|>\(', command):
        return "aucun script en ligne ni substitution de commande ; seulement les outils du plugin"
    for seg in segments_cites(command):
        toks = sans_redirections(tokens(seg))
        h = head(toks)
        if h not in COMMANDES[role]:
            return "commande non permise (refusé : " + seg[:120] + ")"
        for t in REDIRECT_TOUT.findall(seg):
            why = sortie_refusee(t.strip('"\''), role, root)
            if why:
                return why
        args = [t for t in toks[1:] if not t.startswith('-')]
        if h == 'cd':
            if args and project_rel(args[0], root) != '.':
                return "cd seulement vers la racine de la chaîne : les chemins se donnent depuis elle (refusé : " + seg[:120] + ")"
        elif h == 'mkdir':
            for t in args:
                why = sortie_refusee(t, role, root)
                if why:
                    return why
        elif h == 'cp':
            if any(t not in ('-n', '-p', '--no-clobber') for t in toks[1:] if t.startswith('-')) or len(args) < 2:
                return "cp seulement avec -n ou -p, une ou plusieurs sources et une destination (refusé : " + seg[:120] + ")"
            why = sortie_refusee(args[-1], role, root)
            if why:
                return why
            dest = chemin_absolu(args[-1], root)
            finaux = [os.path.join(dest, os.path.basename(s.rstrip('/\\'))) for s in args[:-1]] if os.path.isdir(dest) else [dest]
            if any(os.path.exists(f) for f in finaux):
                return "cp : aucun écrasement (refusé : " + seg[:120] + ")"
        elif h == 'ffprobe':
            if any(t in ('-o', '-output') for t in toks):
                return "ffprobe sans fichier de sortie"
        elif h == 'ffmpeg':
            if '-y' in toks:
                return "ffmpeg sans -y : aucun écrasement, une sortie neuve"
            for t in sorties_ffmpeg(toks):
                why = sortie_refusee(t, role, root)
                if why:
                    return why
        elif h == 'node':
            if len(toks) < 3 or (project_rel(toks[1], root) or '').lower() != 'node_modules/hyperframes/bin/hyperframes.mjs' \
                    or toks[2] != 'remove-background':
                return "node seulement pour « node node_modules/hyperframes/bin/hyperframes.mjs remove-background » (refusé : " + seg[:120] + ")"
            why = arguments_refuses(toks[3:], REMOVE_BACKGROUND, role, root)
            if why:
                return why
        elif h in ('python', 'python3', 'py'):
            apres = toks[1:]
            script = next((t for t in apres if not t.startswith('-')), '')
            reste = apres[apres.index(script) + 1:] if script else []
            outil = outil_du_plugin(script) if script else None
            if outil is not None:
                if outil not in OUTILS[role]:
                    return "outil du plugin non permis à ce rôle (refusé : " + outil + ")"
                why = arguments_refuses(reste, OUTILS[role][outil], role, root)
                if why:
                    return why
            elif script and ZONES[role].match(project_rel(script, root) or ''):
                # Le garde ne lit pas le contenu d'un script : celui de l'agent est relu et lancé par Claude principal (03/11/2026).
                return ("un script de l'agent est relu et lancé par Claude principal : l'écrire avec Write dans sa zone, "
                        "s'arrêter et donner la commande exacte dans le rapport (refusé : " + seg[:120] + ")")
            else:
                return ("python seulement pour ses outils du plugin installé (chemin complet) ; un script de l'agent est relu "
                        "et lancé par Claude principal (refusé : " + seg[:120] + ")")
    return None


def decide_write(path, role, root):
    rel = project_rel(path, root)
    if role == 'lecteur':
        return None if ecriture_lecteur(rel) else ('deny', "lecteur : écriture seulement sous docs/rapports/ de la chaîne")
    if role == 'stratege':
        return None if ecriture_stratege(rel) else ('deny', "stratège : écriture seulement dans docs/ et direction/BANQUE_SUJETS.md")
    if role == 'telechargeur':
        return None if ecriture_telechargeur(rel) else ('deny', "téléchargeur : écriture seulement sous episodes/<id>/kit/media/source-vN/")
    if role in ZONES:
        why = sortie_refusee(path, role, root)
        return ('deny', NOMS_ROLES[role] + " : " + why) if why else None
    if role == 'producteur':
        why = protected(rel, root, {'core', 'marque', 'inputs', 'mp4'})
    elif role == 'mainteneur':
        why = protected(rel, root, {'.claude', 'marque', 'inputs', 'production', 'mp4'})
    else:
        why = None
    return ('deny', role + " : " + why) if why else None


# Compatibilité avec les tests existants
def decide(command, role=None):
    return decide_bash(command, role, os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd())


# Type d'agent (sans le préfixe « studio-faceless: ») → rôle du garde-fou ; Claude principal n'a pas de rôle.
ROLES = {'motion-producer': 'producteur', 'shorts-producer': 'producteur',
         'art-director': 'directeur-artistique', 'studio-maintainer': 'mainteneur',
         'reviewer': 'relecteur', 'strategist': 'stratege', 'media-fetcher': 'telechargeur',
         'sound-manager': 'ingenieur-son', 'publisher': 'editeur',
         'research': 'lecteur', 'conseiller': 'lecteur'}          # 1.0.1


def role_of(data):
    if '--role' in sys.argv:
        return sys.argv[sys.argv.index('--role') + 1]
    agent = str(data.get('agent_type') or '').rsplit(':', 1)[-1]
    if agent in ROLES:
        return ROLES[agent]
    # 1.0.1 : un sous-agent (agent_id présent) d'un type inconnu ou sans type reçoit le rôle de lecteur, et non plus les droits
    # du directeur. Sans agent_id (Claude principal, même lancé avec --agent), aucun rôle.
    return 'lecteur' if data.get('agent_id') else None


def in_plugin(path):
    plugin = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if not (path and plugin):
        return False
    def absolu(p):
        p = p.strip('"\'')
        if re.match(r'^/[a-z]/', p, I):            # /c/Users/... (Git Bash)
            p = p[1] + ':' + p[2:]
        return os.path.normcase(os.path.abspath(p))
    full, base = absolu(path), absolu(plugin)
    return full == base or full.startswith(base + os.sep)


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode('utf-8', errors='replace') or '{}')
    except json.JSONDecodeError:
        return 0
    role = role_of(data)
    root = os.environ.get('CLAUDE_PROJECT_DIR') or data.get('cwd') or os.getcwd()
    tool_input = data.get('tool_input') or {}
    if data.get('tool_name') in ('Write', 'Edit', 'NotebookEdit'):
        path = str(tool_input.get('file_path') or tool_input.get('notebook_path') or '')
        if in_plugin(path):
            verdict = ('deny', "le plugin installé ne se modifie pas depuis une chaîne : modifier son dépôt, puis changer sa version")
        else:
            verdict = decide_write(path, role, root) if role else None
    else:
        verdict = decide_bash(str(tool_input.get('command', '')), role, root)
    if verdict:
        decision, why = verdict
        sys.stdout.write(json.dumps({'hookSpecificOutput': {
            'hookEventName': 'PreToolUse', 'permissionDecision': decision,
            'permissionDecisionReason': 'Garde studio-faceless : ' + why}}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
