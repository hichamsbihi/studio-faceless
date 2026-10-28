"""Contrôle du dossier de publication YouTube d'un épisode de la chaîne — 16/10/2026.

Bibliothèque standard seule. Ne modifie et n'écrit aucun fichier : il lit et affiche. Aucun accès au réseau.
Méthode et règles : skill `studio-faceless:youtube-seo` (limites officielles : references/signaux-et-limites.md).

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/publication.py verifier  PUBLICATION_vN.md [--journal MASTER.log.txt] [--srt FICHIER.srt]
                                                        [--exclure MOT …] [--requete "requête principale"]
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/publication.py chapitres MASTER.log.txt [--titre seq1="Titre" …] [--repere seq4:66.5="Titre" …]
                                                        [--ignorer NOM …]
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/publication.py mot       MOTS.json "quelques mots dits"

`verifier` lit les blocs ``` placés sous les titres Markdown du dossier : « Titres » (un titre par ligne),
« Description », « Tags » (séparés par des virgules), « Commentaire épinglé » et « Réponse … », « Playlist ».
Un bloc sous « Sous-titres » ou « SRT » est ignoré (le SRT se contrôle avec --srt).

Code de sortie : 0 si rien n'est signalé, 1 si une limite est dépassée, 2 en cas d'erreur d'usage.
"""
import argparse, json, math, re, sys, unicodedata

# Limites officielles (doc de l'API YouTube Data, ressources videos et playlists ; aide 9884579 et 6390658)
MAX_TITRE, MAX_DESC_OCTETS, MAX_TAGS = 100, 5000, 500
MAX_PLAYLIST = 150
CHAP_MIN, CHAP_DUREE_MIN = 3, 10
HASHTAGS_IGNORES = 60
# Repères observés ou choix du studio (avertissements, pas des erreurs)
TITRE_LISIBLE = 70           # [Observé] troncature fréquente vers 60–70 caractères
HASHTAGS_STUDIO = (1, 3)     # choix du studio ; YouTube en affiche 3
MAX_COMMENTAIRE = 10000      # [Observé] limite d'un commentaire, non vérifiée dans l'aide
SRT_LIGNE, SRT_LIGNES = 42, 2  # convention de sous-titrage courante
SEGMENTS_HORS_CHAPITRE = {'noir', 'logo', 'signature', 'outro', 'appel', 'fondu'}

ecarts, avis = [], []


def ecart(msg):
    ecarts.append(msg)
    print(f'  ÉCART  {msg}')


def note(msg):
    avis.append(msg)
    print(f'  avis   {msg}')


def ok(msg):
    print(f'  ok     {msg}')


def hms(s):
    s = int(s)
    h, m, sec = s // 3600, s % 3600 // 60, s % 60
    return f'{h}:{m:02d}:{sec:02d}' if h else f'{m}:{sec:02d}'


def sans_accents(t):
    return ''.join(c for c in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(c) != 'Mn')


def normaliser(t):
    return re.sub(r"[^a-z0-9 ]", ' ', sans_accents(t).replace('’', "'").replace("'", '')).split()


# ---------- lecture des fichiers ----------

def lire(chemin):
    with open(chemin, encoding='utf-8-sig') as f:
        return f.read()


def lire_journal(chemin):
    """Segments (nom, début, fin) et durée du MP4 d'après le journal du master."""
    segs, duree = [], None
    for ligne in lire(chemin).splitlines():
        m = re.match(r'^(\S+)\s+([\d.]+)\s*s\s*(?:→|->)\s*([\d.]+)\s*s', ligne)
        if m:
            segs.append((m.group(1), float(m.group(2)), float(m.group(3))))
        m = re.search(r'MP4\s*:\s*\d+\s*images\s*\(([\d.]+)\s*s', ligne)
        if m:
            duree = float(m.group(1))
    if not segs:
        raise ValueError(f'aucun segment « nom début s → fin s » dans {chemin}')
    return segs, duree or segs[-1][2]


def sections(md):
    """Blocs ``` du dossier, rangés par rubrique d'après le titre Markdown qui les précède."""
    out = {'titres': [], 'description': [], 'tags': [], 'commentaires': [], 'playlist': []}
    rubrique, dans_bloc, bloc, entete = None, False, [], ''
    for ligne in md.splitlines():
        if ligne.lstrip().startswith('```'):
            if dans_bloc:
                if rubrique:
                    out[rubrique].append(('\n'.join(bloc), entete))
                dans_bloc, bloc = False, []
            else:
                dans_bloc = True
            continue
        if dans_bloc:
            bloc.append(ligne)
            continue
        m = re.match(r'^#{1,6}\s+(.*)', ligne)
        if m:
            entete = m.group(1).strip()
            h = sans_accents(entete)
            if 'sous-titre' in h or 'srt' in h:
                rubrique = None
            elif 'playlist' in h:
                rubrique = 'playlist'
            elif 'commentaire' in h or 'reponse' in h:
                rubrique = 'commentaires'
            elif 'titre' in h:
                rubrique = 'titres'
            elif 'description' in h:
                rubrique = 'description'
            elif 'tag' in h:
                rubrique = 'tags'
            else:
                rubrique = None
    return out


def compte_tags(tags):
    """Compte de YouTube : virgules comprises, et 2 guillemets pour un tag qui contient une espace."""
    return sum(len(t) + (2 if ' ' in t else 0) for t in tags) + max(len(tags) - 1, 0)


def chapitres_description(desc):
    chap = []
    for ligne in desc.splitlines():
        m = re.match(r'^\s*\(?(\d{1,2}(?::\d{2}){1,2})\)?\s+\S', ligne)
        if m:
            parties = [int(p) for p in m.group(1).split(':')]
            t = parties[0] * 60 + parties[1] if len(parties) == 2 else parties[0] * 3600 + parties[1] * 60 + parties[2]
            chap.append((t, ligne.strip()))
    return chap


def controle_chapitres(chap, duree):
    """chap : liste (secondes, libellé). Règles de l'aide 9884579."""
    n0 = len(ecarts)
    if not chap:
        ecart('aucun chapitre (il en faut au moins 3, le premier à 0:00)')
        return
    if chap[0][0] != 0:
        ecart(f'le premier chapitre doit être 0:00 (trouvé {hms(chap[0][0])})')
    if len(chap) < CHAP_MIN:
        ecart(f'{len(chap)} chapitre(s) ; il en faut au moins {CHAP_MIN}')
    fins = [c[0] for c in chap[1:]] + ([duree] if duree else [])
    for (t, lib), fin in zip(chap, fins):
        if fin <= t:
            ecart(f'chapitres hors d\'ordre : {lib}')
        elif fin - t < CHAP_DUREE_MIN:
            ecart(f'chapitre de {fin - t:.1f} s (< {CHAP_DUREE_MIN} s) : {lib}')
    if duree and chap[-1][0] >= duree:
        ecart(f'dernier chapitre ({hms(chap[-1][0])}) après la fin du film ({duree:.2f} s)')
    if len(ecarts) == n0:
        ok(f'{len(chap)} chapitres, premier à 0:00, tous ≥ {CHAP_DUREE_MIN} s' + (f' (film : {duree:.2f} s)' if duree else ''))


def controle_chevrons(nom, texte):
    if re.search(r'[<>]', texte):
        ecart(f'{nom} : chevron < ou > (refusé par YouTube)')
        return False
    return True


def controle_srt(chemin, duree):
    print(f'\nSous-titres : {chemin}')
    try:
        txt = lire(chemin)
    except UnicodeDecodeError:
        ecart('SRT : encodage non UTF-8')
        return
    blocs = [b for b in re.split(r'\n\s*\n', txt.replace('\r\n', '\n').strip()) if b.strip()]
    prec_fin, n_longues, n_lignes, n0, debut = 0.0, 0, 0, len(ecarts), None
    for i, b in enumerate(blocs, 1):
        lignes = b.split('\n')
        if lignes[0].strip() != str(i):
            ecart(f'SRT : bloc {i} numéroté « {lignes[0].strip()} »')
            return
        m = re.match(r'(\d\d):(\d\d):(\d\d),(\d{3}) --> (\d\d):(\d\d):(\d\d),(\d{3})\s*$', lignes[1] if len(lignes) > 1 else '')
        if not m:
            ecart(f'SRT : bloc {i}, ligne de temps invalide')
            return
        v = [int(x) for x in m.groups()]
        t0 = v[0] * 3600 + v[1] * 60 + v[2] + v[3] / 1000
        t1 = v[4] * 3600 + v[5] * 60 + v[6] + v[7] / 1000
        texte = [l for l in lignes[2:] if l.strip()]
        debut = t0 if debut is None else debut
        if t1 <= t0:
            ecart(f'SRT : bloc {i}, fin avant le début')
        if t0 < prec_fin - 0.001:
            ecart(f'SRT : bloc {i} chevauche le précédent')
        if not texte:
            ecart(f'SRT : bloc {i} vide')
        n_longues += sum(len(l) > SRT_LIGNE for l in texte)
        n_lignes += len(texte) > SRT_LIGNES
        prec_fin = t1
    if duree and prec_fin > duree + 0.001:
        ecart(f'SRT : dernier sous-titre ({prec_fin:.2f} s) après la fin du film ({duree:.2f} s)')
    if n_longues:
        note(f'SRT : {n_longues} ligne(s) de plus de {SRT_LIGNE} caractères (convention courante)')
    if n_lignes:
        note(f'SRT : {n_lignes} bloc(s) de plus de {SRT_LIGNES} lignes')
    if len(ecarts) == n0:
        ok(f'SRT : {len(blocs)} sous-titres, de {debut or 0:.2f} à {prec_fin:.2f} s')


# ---------- commandes ----------

def verifier(a):
    md = lire(a.dossier)
    s = sections(md)
    duree, segs = None, []
    if a.journal:
        segs, duree = lire_journal(a.journal)
    tout_texte = []

    print('Titres')
    titres = [l.strip() for bloc, _ in s['titres'] for l in bloc.splitlines() if l.strip()]
    if not titres:
        ecart('aucun titre trouvé (bloc ``` sous un titre Markdown « Titres »)')
    elif len(titres) != 3:
        note(f'{len(titres)} titre(s) ; le skill en propose 3')
    for t in titres:
        n = len(t)
        if n > MAX_TITRE:
            ecart(f'{n} caractères (> {MAX_TITRE}) : {t}')
        elif controle_chevrons('titre', t):
            (note if n > TITRE_LISIBLE else ok)(f'{n} caractères{" (au-delà de ~70, fin souvent coupée)" if n > TITRE_LISIBLE else ""} : {t}')
        if re.search(r'(?<!\S)#\w', t):
            note(f'hashtag dans le titre (il remplace ceux de la description au-dessus du titre) : {t}')
    tout_texte += titres

    print('\nDescription')
    desc = s['description'][0][0] if s['description'] else ''
    if not desc:
        ecart('aucune description trouvée')
    else:
        if len(s['description']) > 1:
            note(f'{len(s["description"])} blocs sous « Description » ; seul le premier est contrôlé')
        octets = len(desc.encode('utf-8'))
        (ecart if octets > MAX_DESC_OCTETS else ok)(f'{len(desc)} caractères, {octets} octets UTF-8 (limite {MAX_DESC_OCTETS} octets)')
        if controle_chevrons('description', desc):
            ok('aucun chevron')
        lignes = [l for l in desc.splitlines() if l.strip()]
        for i, l in enumerate(lignes[:2], 1):
            print(f'  ligne {i} ({len(l)} car.) : {l[:160]}{"…" if len(l) > 160 else ""}')
        chap = chapitres_description(desc)
        print('  chapitres :')
        controle_chapitres(chap, duree)
        if segs:
            attendus = {math.ceil(round(d, 3)) for n, d, _ in segs if n.lower() not in SEGMENTS_HORS_CHAPITRE} | {0}
            hors = [lib for t, lib in chap if t not in attendus]
            if hors:
                note('chapitre(s) qui ne tombent pas sur un début de séquence du journal (repère interne ? à vérifier) : '
                     + ' | '.join(hors))
            else:
                ok('chaque chapitre tombe sur un début de séquence du journal (arrondi à la seconde supérieure)')
        hashtags = re.findall(r'(?<!\S)#(\w+)', desc)
        if len(hashtags) > HASHTAGS_IGNORES:
            ecart(f'{len(hashtags)} hashtags (> {HASHTAGS_IGNORES} : YouTube les ignore tous)')
        elif not HASHTAGS_STUDIO[0] <= len(hashtags) <= HASHTAGS_STUDIO[1]:
            note(f'{len(hashtags)} hashtag(s) ; le studio en met 1 à 3 (YouTube affiche les 3 premiers)')
        else:
            ok(f'{len(hashtags)} hashtag(s) : ' + ' '.join('#' + h for h in hashtags))
    tout_texte.append(desc)

    print('\nTags')
    brut = ' '.join(b for b, _ in s['tags'])
    tags = [t.strip() for t in brut.replace('\n', ' ').split(',') if t.strip()]
    if not tags:
        note('aucun tag (leur rôle est minime, aide 146402)')
    else:
        n = compte_tags(tags)
        (ecart if n > MAX_TAGS else ok)(f'{len(tags)} tags, {n} caractères au compte de YouTube (limite {MAX_TAGS})')
        controle_chevrons('tags', brut)
        doublons = {t for t in tags if [x.lower() for x in tags].count(t.lower()) > 1}
        if doublons:
            note('tags en double : ' + ', '.join(sorted(doublons)))
    tout_texte += tags

    print('\nCommentaire épinglé et réponses')
    if not s['commentaires']:
        note('aucun commentaire épinglé')
    for bloc, entete in s['commentaires']:
        n = len(bloc)
        (note if n > MAX_COMMENTAIRE else ok)(f'{n} caractères — {entete[:70]}')
        tout_texte.append(bloc)

    print('\nPlaylist')
    if not s['playlist']:
        note('aucune playlist proposée')
    for bloc, _ in s['playlist']:
        nom = bloc.strip().splitlines()[0] if bloc.strip() else ''
        (ecart if len(nom) > MAX_PLAYLIST else ok)(f'{len(nom)} caractères : {nom}')
        controle_chevrons('playlist', bloc)
        tout_texte.append(bloc)

    if a.exclure:
        print('\nMots exclus')
        corpus = sans_accents('\n'.join(tout_texte))
        for mot in a.exclure:
            k = len(re.findall(r'\b' + re.escape(sans_accents(mot)) + r'\b', corpus))
            (ecart if k else ok)(f'« {mot} » : {k} occurrence(s)')

    if a.requete:
        print('\nRequête principale (information)')
        q = ' '.join(normaliser(a.requete))
        lieux = [f'titre {i}' for i, t in enumerate(titres, 1) if q in ' '.join(normaliser(t))]
        debut = [l for l in desc.splitlines() if l.strip()][:2]
        if q in ' '.join(normaliser(' '.join(debut))):
            lieux.append('2 premières lignes de la description')
        if any(q == ' '.join(normaliser(t)) for t in tags):
            lieux.append('tags')
        (ok if lieux else note)(f'« {a.requete} » : ' + (', '.join(lieux) if lieux else 'absente des titres et des 2 premières lignes'))

    if a.srt:
        controle_srt(a.srt, duree)

    print(f'\nBilan : {len(ecarts)} écart(s), {len(avis)} avis.')
    return 1 if ecarts else 0


def chapitres(a):
    segs, duree = lire_journal(a.journal)
    ignorer = SEGMENTS_HORS_CHAPITRE | {n.lower() for n in a.ignorer or []}
    titres = dict(x.split('=', 1) for x in a.titre or [])
    debuts = {n: d for n, d, _ in segs}
    chap = []
    for n, d, _ in segs:
        if n.lower() not in ignorer:
            chap.append((0 if not chap else math.ceil(round(d, 3)), titres.get(n, f'[TITRE {n}]'), f'{n} à {d:.2f} s'))
    for r in a.repere or []:
        m = re.match(r'^([^:]+):([\d.]+)=(.+)$', r)
        if not m or m.group(1) not in debuts:
            raise ValueError(f'repère invalide : {r} (forme seq4:66.5="Titre", segment du journal)')
        t = debuts[m.group(1)] + float(m.group(2))
        chap.append((math.ceil(round(t, 3)), m.group(3), f'{m.group(1)} + {float(m.group(2)):.2f} s = {t:.2f} s'))
    chap.sort(key=lambda c: c[0])
    print(f'Chapitres tirés de {a.journal} (début arrondi à la seconde supérieure, premier forcé à 0:00) :\n')
    for t, titre, origine in chap:
        print(f'{hms(t)} {titre}')
    print('\nOrigine :')
    for t, titre, origine in chap:
        print(f'  {hms(t):>7}  ←  {origine}')
    print('\nContrôle :')
    controle_chapitres([(t, f'{hms(t)} {ti}') for t, ti, _ in chap], duree)
    if any(ti.startswith('[TITRE') for _, ti, _ in chap):
        note('titres de chapitre à écrire (--titre seqN="…")')
    return 1 if ecarts else 0


def mot(a):
    d = json.loads(lire(a.mots))
    mots = d['mots'] if isinstance(d, dict) else d
    cible = normaliser(a.phrase)
    norm = [' '.join(normaliser(m['w'])) for m in mots]
    trouve = 0
    for i in range(len(mots) - len(cible) + 1):
        if norm[i:i + len(cible)] == cible:
            trouve += 1
            contexte = ' '.join(m['w'] for m in mots[i:i + len(cible) + 6])
            print(f'{mots[i]["start"]:.2f} s dans la bande  —  {contexte}')
    if not trouve:
        print(f'« {a.phrase} » introuvable dans {a.mots}')
        return 1
    print('\nTemps dans la bande voix : ajouter le décalage de la bande dans la séquence (data-start de la piste voix '
          'dans index.html) ; vérifier que les repères ont été recalés sur les vrais départs de la voix.')
    return 0


def main():
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding='utf-8', errors='replace')
        except AttributeError:
            pass
    p = argparse.ArgumentParser(description='Contrôle du dossier de publication YouTube (studio-faceless).')
    sp = p.add_subparsers(dest='cmd', required=True)
    v = sp.add_parser('verifier', help='limites et règles du dossier PUBLICATION_vN.md')
    v.add_argument('dossier')
    v.add_argument('--journal', help='journal du master (outputs/*.log.txt) : durée et débuts de séquence')
    v.add_argument('--srt', help='sous-titres anglais à contrôler')
    v.add_argument('--exclure', nargs='+', help='mots qui ne doivent apparaître nulle part')
    v.add_argument('--requete', help='requête principale : où apparaît-elle ?')
    c = sp.add_parser('chapitres', help='chapitres calculés depuis le journal du master')
    c.add_argument('journal')
    c.add_argument('--titre', action='append', help='seqN="Titre du chapitre"')
    c.add_argument('--repere', action='append', help='chapitre interne : seqN:SECONDES="Titre" (temps dans la séquence)')
    c.add_argument('--ignorer', nargs='+', help='segments du journal à ne pas compter comme chapitres')
    m = sp.add_parser('mot', help='temps d\'une phrase dans un fichier de mots horodatés (mots-*.json)')
    m.add_argument('mots')
    m.add_argument('phrase')
    a = p.parse_args()
    try:
        return {'verifier': verifier, 'chapitres': chapitres, 'mot': mot}[a.cmd](a)
    except (OSError, ValueError, KeyError) as e:
        print(f'Erreur : {e}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
