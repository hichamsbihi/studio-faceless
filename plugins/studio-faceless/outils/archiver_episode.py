"""Archivage d'un épisode publié (validé sur AA, 21/10/2026).

Après la publication d'un épisode : les essais sont retirés, la vidéo finale et ses composants sont rangés dans un zip
vérifié, et seuls les fichiers de la racine de l'épisode (CLAUDE.md, BRIEF.md, fiches, PUBLICATION finale…) restent hors
du zip. Rien n'est supprimé : essais et originaux déjà zippés sont déplacés dans _A_SUPPRIMER/<épisode>/ (à la racine de la chaîne), et
c'est le propriétaire qui supprime ce dossier lui-même, après vérification.

Essais retirés (choix validé sur AA, 21/10/2026), seulement quand c'est certain ; dans le doute, le fichier va dans le zip :
- versions non retenues : masters remplacés ; versions d'un projet de production dont une autre version entre au master
  final (lu dans le journal du master et dans le script de montage final) ; rendus d'un projet retenu qui ne sont pas au
  master ; scripts de montage qui n'ont pas produit le master final ;
- tests de direction artistique : dossiers da-test-*, essai-*, test-* ;
- captures de contrôle : dossiers planche(s), controle(s), snapshots, captures des projets ; outputs/controle-* ;
  pistes/essai-* ; planches de contrôle des miniatures ;
- dossiers de publication remplacés : PUBLICATION_vN.* quand une version plus haute existe.

Usage, depuis la racine de la chaîne (python -I -B) :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/archiver_episode.py episodes/<id>                       aperçu, n'écrit et ne déplace rien
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/archiver_episode.py episodes/<id> --executer            zip, vérification, déplacements, ARCHIVE.md
  Options : --master CHEMIN (master final, si outputs/ n'en contient pas) ; --garder CHEMIN et --essai CHEMIN (répétables)
  pour corriger un cas que les règles classent mal.
Ordre de l'exécution : zip écrit à côté (.partiel), relu en entier (CRC de chaque fichier, nombre et tailles), renommé ;
puis seulement, déplacement des essais et des originaux. En cas d'échec avant ce point, rien n'est déplacé.
Garanties : aucune suppression, aucun écrasement (refus si le zip ou la destination existe). Bibliothèque standard seule.
Conseillé avant la première exécution : une sauvegarde (${CLAUDE_PLUGIN_ROOT}/outils/sauvegarde-chaine.ps1).
"""
import argparse, datetime, hashlib, os, re, shutil, sys, zipfile
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()   # dossier de la chaîne, pas celui du plugin
CORBEILLE = ROOT / '_A_SUPPRIMER'
DEJA_COMPRESSES = {'.mp4', '.mov', '.m4a', '.mp3', '.aac', '.ogg', '.opus', '.jpg', '.jpeg', '.png', '.webp', '.webm',
                   '.zip', '.gz', '.7z', '.woff', '.woff2'}
CAPTURES = {'planche', 'planches', 'controle', 'controles', 'snapshots', 'captures'}
VERSION = re.compile(r'^(.*?)-v(\d+)[a-z]?$')


def taille(p):
    return p.stat().st_size if p.is_file() else sum(f.stat().st_size for f in p.rglob('*') if f.is_file())


def go(n):
    return f'{n / 1e9:.2f} Go' if n >= 1e8 else f'{n / 1e6:.1f} Mo'


def groupe(nom):
    m = VERSION.match(nom)
    return m.group(1) if m else None


def lire(f):
    try:
        return f.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return ''


def planifier(ep, master_opt, garder, ajouts):
    essais = {}
    out, prod = ep / 'outputs', ep / 'production'
    # Master final : la plus haute version de outputs/, sauf --master
    if master_opt:
        master = Path(master_opt).resolve()
    else:
        cands = [p for p in out.glob('*master-v*.mp4')] if out.is_dir() else []
        if not cands:
            sys.exit(f'Aucun master dans {out} : donner --master CHEMIN (le MP4 final publié).')
        master = max(cands, key=lambda p: int(re.search(r'master-v(\d+)', p.name).group(1)))
    if not master.is_file():
        sys.exit(f'Master introuvable : {master}')
    v_final = re.search(r'master-v(\d+)', master.name)
    # Les fichiers d'un MP4 cité par le journal du master restent (v3 : le film en voix seule d'où le master est mixé)
    texte = lire(master.parent / (master.stem + '.log.txt'))
    cites = {Path(n).stem for n in re.findall(r'([\w.()\-]+\.mp4)', texte)}
    for p in master.parent.iterdir():
        m = re.search(r'master-v(\d+)', p.name)
        if v_final and m and m.group(1) != v_final.group(1) and not any(p.name.startswith(s + '.') for s in cites):
            essais[p] = 'master remplacé'
    # Rendus retenus : noms de MP4 cités par le journal du master et par le montage final
    # (production/montage-* jusqu'au gabarit v2 ; episodes/<id>/montage/ et son montage.json depuis le v3)
    montages = [d for d in prod.glob('montage-*') if d.is_dir()] if prod.is_dir() else []
    finals = [d for d in montages if any(master.name in lire(f) for f in d.iterdir()
                                         if f.is_file() and f.suffix in ('.py', '.mjs', '.js', '.sh', '.md', '.txt'))]
    if (ep / 'montage').is_dir():
        finals.append(ep / 'montage')
    for d in finals:
        texte += ''.join(lire(f) for f in d.iterdir() if f.is_file() and f.suffix in ('.py', '.mjs', '.js', '.sh', '.json'))
    gardes = set(re.findall(r'([\w.()\-]+\.mp4)', texte))
    projets = [d for d in prod.iterdir() if d.is_dir()] if prod.is_dir() else []
    retenus = {d for d in projets if any(f.name in gardes for f in d.glob('*.mp4'))} | set(finals)
    groupes = {groupe(d.name) for d in retenus if groupe(d.name)}
    for d in projets:
        if d in retenus:
            continue
        if d.name.startswith('montage-') and finals:
            essais[d] = 'montage non retenu'
        elif groupe(d.name) in groupes:
            essais[d] = 'version non retenue'
        elif d.name.lower().startswith(('essai', 'test')):
            essais[d] = 'essai'
    for d in projets:
        if d in essais:
            continue
        if d in retenus and gardes:
            for f in d.glob('*.mp4'):
                if f.name not in gardes:
                    essais[f] = 'rendu non retenu'
        for sub in d.iterdir():
            if sub.is_dir() and sub.name.lower() in CAPTURES:
                essais[sub] = 'captures de contrôle'
        for sub in (d / 'pistes').glob('essai*'):
            essais[sub] = 'essai de mix'
    if out.is_dir():
        for sub in out.glob('controle*'):
            essais[sub] = 'captures de contrôle'
    for p in ep.iterdir():
        if p.is_dir() and p.name.lower().startswith(('da-test', 'essai', 'test')):
            essais[p] = 'test de direction artistique'
        if p.is_dir() and p.name.lower().startswith('miniature'):
            for f in p.glob('controle-planche*'):
                essais[f] = 'captures de contrôle'
    pubs = {}
    for p in ep.glob('PUBLICATION_v*'):
        pubs.setdefault(int(re.match(r'PUBLICATION_v(\d+)', p.name).group(1)), []).append(p)
    if pubs:
        for v, l in pubs.items():
            if v < max(pubs):
                for p in l:
                    essais[p] = 'dossier de publication remplacé'
    for a in ajouts:
        essais[Path(a).resolve()] = 'désigné par --essai'
    for g in garder:
        g = Path(g).resolve()
        for p in list(essais):
            if p == g or g in p.parents or p in g.parents:
                del essais[p]
    # Ne garder que les essais du plus haut niveau (un essai dans un essai part avec lui)
    essais = {p: m for p, m in essais.items() if not any(a in essais for a in p.parents)}
    if master in essais or any(a in essais for a in master.parents):
        sys.exit('Règle incohérente : le master final serait classé comme essai.')
    dossiers = sorted(p for p in ep.iterdir() if p.is_dir() and p not in essais)
    racine = sorted(p for p in ep.iterdir() if p.is_file() and p not in essais)
    fichiers = [f for d in dossiers for f in sorted(d.rglob('*'))
                if f.is_file() and f not in essais and not any(a in essais for a in f.parents)]
    return master, finals, retenus, essais, dossiers, racine, fichiers


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser()
    ap.add_argument('episode')
    ap.add_argument('--executer', action='store_true')
    ap.add_argument('--master')
    ap.add_argument('--garder', action='append', default=[])
    ap.add_argument('--essai', action='append', default=[])
    a = ap.parse_args()
    ep = Path(a.episode).resolve()
    if ep.parent != ROOT / 'episodes' or not ep.is_dir():
        sys.exit(f'Dossier d\'épisode attendu dans {ROOT / "episodes"} : {ep}')
    master, finals, retenus, essais, dossiers, racine, fichiers = planifier(ep, a.master, a.garder, a.essai)
    date = datetime.date.today().isoformat()
    nom_zip = ep / f'{ep.name}_archive_{date}.zip'
    dest = CORBEILLE / ep.name
    rel = lambda p: p.relative_to(ep).as_posix()
    t_zip = sum(f.stat().st_size for f in fichiers)
    par_motif = {}
    for p, m in essais.items():
        par_motif.setdefault(m, []).append(p)
    print(f'Épisode : {ep.name}\nMaster final : {rel(master) if ep in master.parents else master}')
    print(f'Montage final : {", ".join(d.name for d in finals) or "non trouvé (aucun script de montage ne cite le master)"}')
    print(f'Projets retenus : {", ".join(sorted(d.name for d in retenus if d not in finals)) or "aucun trouvé par les règles"}')
    print(f'\nEssais → {dest.relative_to(ROOT)}/essais_{date}/ :')
    for m, l in sorted(par_motif.items()):
        print(f'  {m} : {len(l)} élément(s), {go(sum(taille(p) for p in l))}')
        for p in sorted(l)[:12]:
            print(f'    {rel(p)}')
        if len(l) > 12:
            print(f'    … et {len(l) - 12} autre(s)')
    print(f'\nRestent hors du zip ({len(racine)} fichier(s) de la racine) : {", ".join(p.name for p in racine)}')
    print(f'\nZip : {nom_zip.name} ← {len(fichiers)} fichier(s), {go(t_zip)}, dossiers : {", ".join(d.name for d in dossiers)}')
    print(f'Puis originaux zippés → {dest.relative_to(ROOT)}/originaux_{date}/')
    if not a.executer:
        print('\nAperçu seulement : rien n\'est écrit ni déplacé. Relancer avec --executer après l\'accord du propriétaire.')
        return
    # --- Exécution
    for p in (nom_zip, dest / f'essais_{date}', dest / f'originaux_{date}'):
        if p.exists():
            sys.exit(f'Existe déjà, aucun écrasement : {p}')
    libre = shutil.disk_usage(ep).free
    if libre < t_zip * 1.1 + 1e9:
        sys.exit(f'Place insuffisante : {go(libre)} libres pour un zip d\'environ {go(t_zip)}.')
    partiel = nom_zip.with_name(nom_zip.name + '.partiel')
    if partiel.exists():
        sys.exit(f'Zip partiel d\'une exécution précédente, à examiner : {partiel}')
    with zipfile.ZipFile(partiel, 'x', allowZip64=True) as z:
        for i, f in enumerate(fichiers, 1):
            stocke = f.suffix.lower() in DEJA_COMPRESSES
            z.write(f, rel(f), compress_type=zipfile.ZIP_STORED if stocke else zipfile.ZIP_DEFLATED,
                    compresslevel=None if stocke else 6)
            if i % 500 == 0:
                print(f'  {i}/{len(fichiers)} fichiers zippés')
    with zipfile.ZipFile(partiel) as z:
        mauvais = z.testzip()
        infos = z.infolist()
    attendu = {rel(f): f.stat().st_size for f in fichiers}
    trouve = {i.filename: i.file_size for i in infos}
    if mauvais or trouve != attendu:
        sys.exit(f'Zip non conforme ({"CRC faux : " + mauvais if mauvais else "liste ou tailles différentes"}). '
                 f'Rien n\'a été déplacé ; zip laissé en {partiel.name} pour examen.')
    os.rename(partiel, nom_zip)
    h = hashlib.sha256()
    with open(nom_zip, 'rb') as fz:
        for bloc in iter(lambda: fz.read(1 << 20), b''):
            h.update(bloc)
    print(f'Zip vérifié : {len(infos)} fichiers, CRC justes, {go(nom_zip.stat().st_size)}, SHA-256 {h.hexdigest()}')
    for p in sorted(essais):
        cible = dest / f'essais_{date}' / rel(p)
        cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(cible))
    for d in dossiers:
        cible = dest / f'originaux_{date}' / d.name
        cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(d), str(cible))
    lignes = [f'# Archive de {ep.name} ({date})', '',
              f'Archivage après publication (validé sur AA, 21/10/2026 ; script `outils/archiver_episode.py` du plugin).', '',
              f'- **Zip** : `{nom_zip.name}`, {go(nom_zip.stat().st_size)}, {len(infos)} fichiers ; SHA-256 `{h.hexdigest()}` ; '
              f'relu en entier (CRC de chaque fichier, liste et tailles) avant tout déplacement.',
              f'- **Master final** : `{rel(master) if ep in master.parents else master}` (dans le zip).',
              f'- **Hors du zip** : les fichiers de la racine de l\'épisode.',
              f'- **Essais retirés** ({len(essais)}) et **originaux zippés** : déplacés dans `_A_SUPPRIMER/{ep.name}/` '
              f'(`essais_{date}/`, `originaux_{date}/`). Le propriétaire les supprime lui-même ; d\'ici là, tout se restaure '
              f'en les remettant à leur place.', '', '## Essais retirés, par motif']
    for m, l in sorted(par_motif.items()):
        lignes.append(f'- {m} ({len(l)}) : ' + ', '.join(f'`{rel(p)}`' for p in sorted(l)))
    lignes += ['', '## Restaurer', f'Dézipper `{nom_zip.name}` dans ce dossier : il redonne les dossiers de l\'épisode à l\'identique.']
    (ep / 'ARCHIVE.md').write_text('\n'.join(lignes) + '\n', encoding='utf-8')
    shutil.copy2(ep / 'ARCHIVE.md', dest / f'LISEZMOI_{date}.md')
    print(f'Fait : essais et originaux dans {dest} ; ARCHIVE.md écrit à la racine de l\'épisode.')


if __name__ == '__main__':
    main()
