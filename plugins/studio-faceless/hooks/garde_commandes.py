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
- ask : aperçu HyperFrames.
Par rôle, déduit du type d'agent (`agent_type` de l'entrée du hook, voir ROLES), ou option `--role` :
- relecteur (reviewer) : seules ffprobe, ffmpeg de mesure (-f null), wc, ls, grep, head et tail ; aucune redirection ;
- directeur-artistique : seules ffmpeg, ffprobe et mkdir ; pas d'écrasement (-y) ; sortie hors zones protégées ;
- producteur : en Bash, aucune mention de direction/, templates/, .claude/ ou d'un CLAUDE.md (sauf les chemins du
  plugin installé, pour lancer ses outils, sans « .. »), et aucune écriture
  vers un dossier existant de marque/, des entrées d'épisode ou un MP4 existant ; mêmes limites pour Write et Edit ;
- mainteneur : n'écrit qu'avec Write et Edit (aucune écriture en Bash), jamais dans .claude/, un projet de
  production, un dossier existant de marque/, des entrées d'épisode ou un MP4.
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

WRAPPERS = {'sudo', 'xargs', 'command', 'nohup', 'time', 'exec', 'env'}
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
    while toks and (toks[0].lower() in WRAPPERS or re.match(r'^\w+=', toks[0])):
        toks = toks[1:]
    if len(toks) > 1 and toks[0].lower() in ('cmd', 'cmd.exe') and toks[1].lower() in ('/c', '/k'):
        toks = toks[2:]
    return toks


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


def decide_bash(command, role, root):
    for rx, why in DENY_TEXT:
        if rx.search(command):
            return 'deny', why
    if recursive_rm(command):
        return 'deny', "suppression récursive : passer par la corbeille, avec accord"

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

    for rx, why in ASK_TEXT:
        if rx.search(command):
            return 'ask', why
    if RENDER.search(command) and not WORKERS_OK.search(command):
        return 'deny', "rendu HyperFrames sans « --workers 1 » ou « 2 » : relancer avec --workers 1 (un Chrome par processus)"
    return None


def decide_write(path, role, root):
    rel = project_rel(path, root)
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
         'reviewer': 'relecteur'}


def role_of(data):
    if '--role' in sys.argv:
        return sys.argv[sys.argv.index('--role') + 1]
    agent = str(data.get('agent_type') or '').rsplit(':', 1)[-1]
    return ROLES.get(agent[3:] if agent.startswith('aa-') else agent)


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
