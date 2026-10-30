"""Contrôle du dépôt Git de la chaîne avant un commit (validé sur AA, 21/10/2026).

Refuse, dans les fichiers à committer :
- un fichier de plus de 10 Mo qui ne passe pas par Git LFS (GitHub refuse au-delà de 100 Mo) ;
- un média d'épisode (vidéo, son, image, police sous episodes/) : il va dans la sauvegarde externe ;
- un secret probable (clé d'API sk-… ou sk_… en début de jeton, jeton GitHub, clé privée, en-tête Bearer) ;
- un chemin propre à une machine (C:/Users/<nom>, /c/Users/<nom>) dans un fichier de code actif (hors episodes/, docs/ et tout dossier vendor/, copie de tiers) ;
- un REGLES_STUDIO.md de plus de 9 000 caractères une fois ${CLAUDE_PLUGIN_ROOT} remplacé par un chemin de cache type : l'application de bureau
  coupe tout additionalContext du hook SessionStart au-delà de 10 000 caractères (0.2.3, mesure du 30/10/2026). Le détail va dans referentiels/REGLES_DETAIL.md.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/verifier_depot.py            fichiers indexés (git add), comme le crochet pre-commit
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/verifier_depot.py --tout    tous les fichiers que Git suivrait (suivis + nouveaux non ignorés)
Crochet : .githooks/pre-commit, activé par `git config core.hooksPath .githooks` (INSTALLATION.md).
Code de sortie : 0 = rien à signaler ; 1 = refus. Bibliothèque standard seule.
"""
import os, re, subprocess, sys

LIMITE = 10 * 1024 * 1024
LIMITE_REGLES = 9000            # caractères de REGLES_STUDIO.md tel que le hook SessionStart l'injecte
RACINE_TYPE = 'C:/Users/<nom>/.claude/plugins/cache/studio-faceless/studio-faceless/0.2.3'   # longueur type du chemin du plugin installé
MEDIAS = {'.mp4', '.mov', '.webm', '.mkv', '.wav', '.mp3', '.m4a', '.aac', '.flac', '.png', '.jpg', '.jpeg', '.webp', '.gif',
          '.tif', '.tiff', '.pdf', '.ttf', '.otf', '.woff', '.woff2', '.zip'}
CODE = {'.py', '.mjs', '.js', '.cjs', '.json', '.sh', '.ps1', '.html', '.css'}
SECRET = re.compile(r"((?<![A-Za-z0-9_\-])(?:sk-[A-Za-z0-9_\-]{20,}|sk_(?:live_|test_)?[A-Za-z0-9]{24,})|xi-api-key\s*[:=]\s*(?![$<{%])[A-Za-z0-9_\-]{20,}|api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}"
                    r"|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._\-]{24,})")
CHEMIN = re.compile(r"(?i)(?:[A-Z]:[/\\]+Users[/\\]+|/[a-z]/Users/)(?!<|\{|%|\$|nom\b|vous\b|you\b|user\b)[A-Za-z0-9_][\w.\-]*")


def taille_regles(texte):
    """Longueur de REGLES_STUDIO.md une fois ${CLAUDE_PLUGIN_ROOT} remplacé par le chemin du cache (ce que le hook injecte)."""
    return len(texte.replace('${CLAUDE_PLUGIN_ROOT}', RACINE_TYPE))


def git(*a):
    return subprocess.run(['git', *a], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True).stdout


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    tout = '--tout' in sys.argv[1:]
    racine = git('rev-parse', '--show-toplevel').strip()
    os.chdir(racine)
    if tout:
        fichiers = [f for f in git('ls-files', '-co', '--exclude-standard', '-z').split('\0') if f]
    else:
        fichiers = [f for f in git('diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z').split('\0') if f]
    fichiers = [f for f in fichiers if os.path.isfile(f)]
    lfs = {}
    for i in range(0, len(fichiers), 200):
        for ligne in git('check-attr', 'filter', '--', *fichiers[i:i + 200]).splitlines():
            chemin, _, valeur = ligne.rpartition(': ')
            lfs[chemin.rsplit(': filter', 1)[0]] = valeur.strip() == 'lfs'
    refus = []
    for f in fichiers:
        ext = os.path.splitext(f)[1].lower()
        taille = os.path.getsize(f)
        if taille > LIMITE and not lfs.get(f):
            refus.append(f'{f} : {taille / 1e6:.1f} Mo hors Git LFS (limite 10 Mo)')
        if f.startswith('episodes/') and ext in MEDIAS:
            refus.append(f'{f} : média d\'épisode (sauvegarde externe, pas le dépôt)')
        if ext in MEDIAS or lfs.get(f) or taille > 3 * 1024 * 1024:
            continue
        try:
            texte = open(f, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        m = SECRET.search(texte)
        if m:
            refus.append(f'{f} : secret probable (« {m.group(0)[:12]}… »)')
        if os.path.basename(f) == 'REGLES_STUDIO.md' and taille_regles(texte) > LIMITE_REGLES:
            refus.append(f'{f} : {taille_regles(texte)} caractères une fois le chemin du plugin substitué (limite {LIMITE_REGLES} : '
                         "l'application coupe le contexte du hook au-delà de 10 000) ; déplacer du texte dans referentiels/REGLES_DETAIL.md")
        if ext in CODE and not f.startswith(('episodes/', 'docs/', 'vendor/')) and '/vendor/' not in f:
            m = CHEMIN.search(texte)
            if m:
                refus.append(f'{f} : chemin propre à une machine (« {m.group(0)} »)')
    print(f'Dépôt de la chaîne : {len(fichiers)} fichier(s) contrôlé(s) ({"tous" if tout else "indexés"}).')
    if refus:
        print(f'REFUS : {len(refus)} problème(s) à corriger avant le commit :')
        for r in refus:
            print('  - ' + r)
        sys.exit(1)
    print('OK : aucun gros fichier hors LFS, aucun média d\'épisode, aucun secret, aucun chemin de machine.')


if __name__ == '__main__':
    main()
