"""Télécharge les médias d'une liste validée par le propriétaire (validé sur AA, 02/11/2026, Q56 et Q57 de son E011).

Généralisé des trois scripts de l'E011 d'AA (Commons et Wikipédia par l'API, liens directs, serveur de fichiers de Pexels).
Règle : `${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 bis (« téléchargement des médias »). Le propriétaire a validé
la LISTE ; l'outil ne télécharge rien d'autre, et rien du tout sans `--executer`.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/medias/telecharger_medias.py LISTE.json --racine episodes/<id>/kit/media/source-vN \\
      --agent-utilisateur "NomDeLaChaine-MediaFetch/1.0 (https://adresse-de-la-chaine)"            aperçu : aucun appel réseau
  … même commande avec --executer                                                                   télécharge, écrit le manifeste

Liste (JSON) : un tableau, ou {"medias": [...]}. Chaque média :
  ref      identifiant court de la liste du propriétaire (M1, P3a, V6b…) ; lettres, chiffres, « _ » et « - » seulement ;
  type     "commons" | "direct" | "pexels" ;
  titre    commons : titre du fichier (sans « File: ») ; pexels : identifiant numérique de la vidéo ;
  url      à la place de `titre` : commons, l'adresse de la page « File: » ; direct, l'adresse du fichier ; pexels, l'adresse du
           fichier sur videos.pexels.com/video-files/ (ou celle de la page de la vidéo, dont on ne lit que l'identifiant) ;
  dossier  sous-dossier de --racine (photos, logos, videos…) ; jamais absolu, jamais « .. » ;
  Facultatifs : nom (nom imposé du fichier, sans la réf.), pageid (commons, à la place du titre), api (commons : « commons.wikimedia.org »
  par défaut, ou « en.wikipedia.org » pour une image de Wikipédia), sha1 (empreinte attendue), fps (pexels : un nombre ou une liste,
  sinon 24, 25, 30, 50, 60, 29), largeur et hauteur (pexels, 1920 × 1080 par défaut).

Garanties :
- Fichier écrit sous le nom `<réf>__<nom>`, par `open(…, "xb")` : aucun fichier n'est jamais écrasé (un fichier présent est signalé « deja_present »).
- Commons : fichier original (`imageinfo`), SHA-1 comparé à celui de l'API ; Pexels : serveur de fichiers seulement, jamais la page (Cloudflare).
- Robot identifié par `--agent-utilisateur` : une adresse de la chaîne ou d'un projet, JAMAIS une adresse e-mail (refusé).
- Entre deux fichiers, 3,5 s au moins (--pause, 3 s au minimum) ; après un 429, l'attente est doublée (nouvel essai et fichiers suivants) ; 3 essais.
- Aucun contournement : accès refusé (401, 402, 403, 451, vérification anti-robot, page web à la place du fichier, 429 qui persiste) =
  « refuse » ; le fichier va à la liste « à télécharger par le propriétaire » (`manuel/` sous --racine). Aucun autre chemin n'est tenté.
- Sorties (refusent d'écraser) : `MANIFESTE_TELECHARGEMENT_<date>.json` sous --racine (réf., type, statut, fichier, SHA-1, taille, adresses,
  empreintes de l'API, métadonnées de licence de Commons) et, s'il y a des refus, `manuel/A_TELECHARGER_PAR_LE_PROPRIETAIRE_<date>.md`.
Code de sortie : 0 = tout est présent ; 1 = refus ou échec (manifeste écrit) ; 2 = usage ou liste invalide. Bibliothèque standard seule.
"""
import argparse, hashlib, html, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

REF = re.compile(r'^[A-Za-z0-9_-]{1,24}$')
EMAIL = re.compile(r'(?i)mailto:|[\w.+-]+@[\w-]+(?:\.[\w-]+)+')
API_OK = re.compile(r'^(commons\.wikimedia|[a-z]{2,3}\.wikipedia)\.org$')
HOTES_PEXELS = ('www.pexels.com', 'pexels.com')
FPS_DEFAUT = [24, 25, 30, 50, 60, 29]
META = ['Artist', 'Credit', 'LicenseShortName', 'LicenseUrl', 'UsageTerms', 'DateTimeOriginal', 'ImageDescription']
EXT_HTML = {'.html', '.htm'}
PAUSE_MIN = 3.0
CODES_REFUS = (401, 402, 403, 451)


class Refus(Exception):
    """Accès refusé par le site : le fichier passe à la liste du propriétaire, on ne cherche aucun détour."""


class Echec(Exception):
    """Erreur technique ou fichier introuvable."""


# ------------------------------------------------------------------ liste et noms

def agent_valide(ua):
    ua = (ua or '').strip()
    if not re.search(r'https?://', ua):
        raise ValueError("--agent-utilisateur doit contenir l'adresse (https://…) de la chaîne ou d'un projet")
    if EMAIL.search(ua):
        raise ValueError("--agent-utilisateur ne doit jamais contenir une adresse e-mail (l'adresse du propriétaire n'est pas à donner à un site)")
    return ua


def sous_dossier_sur(dossier):
    d = (dossier or '').replace('\\', '/')
    if not d or d.startswith('/') or re.match(r'^[A-Za-z]:', d) or any(p in ('', '.', '..') for p in d.rstrip('/').split('/')):
        raise ValueError(f'dossier invalide : « {dossier} » (un sous-dossier de --racine, jamais absolu, sans « .. »)')
    return d.rstrip('/')


def nettoyer_nom(nom):
    """Nom de fichier sûr (Windows compris) : sans séparateur, sans caractère interdit, 120 caractères au plus (extension gardée)."""
    n = re.sub(r'[\x00-\x1f<>:"/\\|?*]', '_', nom.replace(' ', '_')).strip('._ ')
    if len(n) > 120:
        base, ext = os.path.splitext(n)
        n = base[:120 - len(ext)] + ext
    if not n:
        raise ValueError('nom de fichier vide')
    return n


def titre_depuis_url_commons(url):
    p = urllib.parse.urlparse(url)
    m = re.search(r'/wiki/(?:File|Fichier):(.+)$', urllib.parse.unquote(p.path))
    if not m or not API_OK.match(p.hostname or ''):
        raise ValueError(f"adresse commons non reconnue : {url} (attendu : https://commons.wikimedia.org/wiki/File:…)")
    return m.group(1).replace(' ', '_'), p.hostname


def id_pexels(valeur):
    """Identifiant numérique d'une vidéo Pexels, depuis un nombre, un titre numérique ou l'adresse de sa page (jamais ouverte)."""
    v = str(valeur or '').strip()
    if v.isdigit():
        return int(v)
    m = re.search(r'-(\d{4,})/?$', urllib.parse.urlparse(v).path)
    if m:
        return int(m.group(1))
    raise ValueError(f'identifiant Pexels introuvable dans « {valeur} »')


def liste_fps(valeur):
    if valeur is None:
        return list(FPS_DEFAUT)
    return [int(x) for x in (valeur if isinstance(valeur, list) else [valeur])]


def url_pexels(vid, fps, largeur=1920, hauteur=1080):
    return f'https://videos.pexels.com/video-files/{vid}/{vid}-hd_{largeur}_{hauteur}_{fps}fps.mp4'


def charger_liste(chemin):
    """Lit la liste et la valide. Retourne des médias normalisés ; lève ValueError au premier défaut (rien n'est téléchargé)."""
    with open(chemin, encoding='utf-8') as f:
        brut = json.load(f)
    medias = brut.get('medias') if isinstance(brut, dict) else brut
    if not isinstance(medias, list) or not medias:
        raise ValueError('la liste est vide ou n\'est pas un tableau')
    vus, sortie = set(), []
    for i, m in enumerate(medias, 1):
        if not isinstance(m, dict):
            raise ValueError(f'média {i} : objet attendu')
        ref = str(m.get('ref', ''))
        if not REF.match(ref):
            raise ValueError(f'média {i} : réf. invalide « {ref} » (lettres, chiffres, _ et - ; 24 caractères au plus)')
        if ref in vus:
            raise ValueError(f'réf. en double : {ref}')
        vus.add(ref)
        t = m.get('type')
        if t not in ('commons', 'direct', 'pexels'):
            raise ValueError(f'{ref} : type « {t} » inconnu (commons, direct ou pexels)')
        n = {'ref': ref, 'type': t, 'dossier': sous_dossier_sur(m.get('dossier')), 'nom': m.get('nom'), 'sha1': (m.get('sha1') or '').lower() or None}
        titre, url = m.get('titre'), m.get('url')
        if t == 'commons':
            api = m.get('api') or 'commons.wikimedia.org'
            if m.get('pageid'):
                n['pageid'] = int(m['pageid'])
            elif url:
                titre, api = titre_depuis_url_commons(url)
            if not API_OK.match(api):
                raise ValueError(f'{ref} : api « {api} » refusée (commons.wikimedia.org ou xx.wikipedia.org)')
            if not titre and 'pageid' not in n:
                raise ValueError(f'{ref} : titre, adresse « File: » ou pageid attendu')
            n.update(titre=(titre or '').replace(' ', '_') or None, api=api)
        elif t == 'direct':
            p = urllib.parse.urlparse(url or '')
            if p.scheme != 'https' or not p.hostname:
                raise ValueError(f'{ref} : adresse https attendue')
            if p.hostname in HOTES_PEXELS:
                raise ValueError(f'{ref} : une page de Pexels ne se télécharge pas ; type « pexels »')
            n['url'] = url
        else:
            if url and (urllib.parse.urlparse(url).hostname or '') == 'videos.pexels.com':
                if not urllib.parse.urlparse(url).path.startswith('/video-files/'):
                    raise ValueError(f'{ref} : seul le serveur de fichiers /video-files/ de Pexels est permis')
                n['url'] = url
                n['id'] = id_pexels(re.search(r'/video-files/(\d+)/', url).group(1)) if re.search(r'/video-files/(\d+)/', url) else None
            else:
                n['id'] = id_pexels(titre if titre is not None else url)
                n['fps'] = liste_fps(m.get('fps'))
                n['largeur'], n['hauteur'] = int(m.get('largeur', 1920)), int(m.get('hauteur', 1080))
        sortie.append(n)
    return sortie


def nom_final(m, nom_distant):
    """`<réf>__<nom>` : le nom imposé de la liste s'il existe, sinon le nom du fichier d'origine."""
    base = m.get('nom') or nom_distant
    return f"{m['ref']}__{nettoyer_nom(str(base))}"


def chemin_dest(racine, m, nom_distant):
    dest = os.path.join(racine, m['dossier'], nom_final(m, nom_distant))
    rel = os.path.relpath(os.path.abspath(dest), os.path.abspath(racine))
    if rel.startswith('..') or os.path.isabs(rel):
        raise ValueError(f"{m['ref']} : chemin hors de --racine")
    return dest


def nom_distant_direct(url):
    return urllib.parse.unquote(urllib.parse.urlparse(url).path.rsplit('/', 1)[-1]) or 'fichier'


def ecrire_sans_ecraser(dest, data):
    """Écrit un fichier neuf ; FileExistsError si le chemin existe (jamais d'écrasement)."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'xb') as fh:
        fh.write(data)


def sha1_fichier(chemin):
    h = hashlib.sha1()
    with open(chemin, 'rb') as f:
        for bloc in iter(lambda: f.read(1 << 20), b''):
            h.update(bloc)
    return h.hexdigest()


SECRET_URL = re.compile(r'(?i)sig|credential|token|secret|key|auth|policy')


def url_publique(url):
    """L'adresse sans les valeurs secrètes de sa requête (lien signé à durée limitée, comme ceux de Soundza) : c'est elle qui va au manifeste."""
    p = urllib.parse.urlparse(url)
    if not p.query:
        return url
    q = [(k, '***' if SECRET_URL.search(k) else v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True)]
    return urllib.parse.urlunparse(p._replace(query=urllib.parse.urlencode(q, safe='*')))


def propre(v):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', v or ''))).strip()


# ------------------------------------------------------------------ réseau

class Client:
    """Requêtes polies : User-Agent imposé, pause entre fichiers, attente doublée après un 429, aucun détour après un refus."""

    def __init__(self, agent, pause=3.5, essais=3, taille_max=500 * 1024 * 1024, ouvrir=None, dormir=time.sleep):
        self.agent, self.pause, self.essais, self.taille_max = agent, max(pause, PAUSE_MIN), essais, taille_max
        self.ouvrir = ouvrir or urllib.request.urlopen
        self.dormir = dormir
        self.dernier = None

    def attendre(self, secondes=None):
        self.dormir(self.pause if secondes is None else secondes)

    def lire(self, url, methode='GET'):
        """(octets, type de contenu). Refus si l'accès est refusé ; Echec si le fichier manque ou après les essais (hors 429)."""
        for essai in range(1, self.essais + 1):
            req = urllib.request.Request(url, headers={'User-Agent': self.agent}, method=methode)
            try:
                with self.ouvrir(req, timeout=180) as r:
                    ctype = r.headers.get('Content-Type', '') or ''
                    if methode == 'HEAD':
                        return b'', ctype
                    data = bytearray()
                    while True:
                        bloc = r.read(1 << 20)
                        if not bloc:
                            break
                        data += bloc
                        if len(data) > self.taille_max:
                            raise Refus(f'fichier de plus de {self.taille_max // (1024 * 1024)} Mo : à confirmer avec le propriétaire')
                    attendu = r.headers.get('Content-Length')
                    if attendu and attendu.isdigit() and int(attendu) != len(data):
                        raise Echec(f'fichier incomplet ({len(data)} octets sur {attendu})')
                    return bytes(data), ctype
            except urllib.error.HTTPError as e:
                en_tete = {k.lower(): v for k, v in (e.headers or {}).items()}
                e.close()
                if e.code in CODES_REFUS or en_tete.get('cf-mitigated') == 'challenge':
                    raise Refus(f'HTTP {e.code} (accès refusé ou vérification anti-robot ; aucun contournement)')
                if e.code == 404:
                    raise Echec('HTTP 404 (introuvable)')
                if e.code == 429:
                    self.pause = min(self.pause * 2, 120.0)           # attente doublée, pour la suite aussi
                    if essai < self.essais:
                        self.dormir(self.pause)
                        continue
                    raise Refus(f'HTTP 429 après {essai} essais (site saturé : à télécharger plus tard par le propriétaire)')
                if e.code in (500, 502, 503, 504) and essai < self.essais:
                    self.dormir(self.pause * 2 ** (essai - 1))
                    continue
                raise Echec(f'HTTP {e.code}')
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                if essai < self.essais:
                    self.dormir(self.pause * 2 ** (essai - 1))
                    continue
                raise Echec(f'réseau : {e}')
        raise Echec('essais épuisés')

    def json_api(self, api, **params):
        params.update(action='query', format='json', formatversion='2', prop='imageinfo', iiprop='url|sha1|size|mime|timestamp|user|extmetadata')
        data, _ = self.lire(f'https://{api}/w/api.php?' + urllib.parse.urlencode(params))
        return json.loads(data)


def interroger_commons(client, medias):
    """imageinfo de chaque média commons, par lots (un lot par API). Retourne {réf: page ou None}."""
    infos = {}
    par_api = {}
    for m in medias:
        if m['type'] == 'commons':
            par_api.setdefault(m['api'], []).append(m)
    premier = True
    for api, groupe in par_api.items():
        for debut in range(0, len(groupe), 20):
            lot = groupe[debut:debut + 20]
            if not premier:
                client.attendre()
            premier = False
            par_id = [m for m in lot if m.get('pageid')]
            par_titre = [m for m in lot if not m.get('pageid')]
            if par_titre:
                q = client.json_api(api, titles='|'.join('File:' + m['titre'] for m in par_titre))
                norm = {n['from']: n['to'] for n in q['query'].get('normalized', [])}
                pages = {p['title']: p for p in q['query']['pages']}
                for m in par_titre:
                    cle = 'File:' + m['titre'].replace('_', ' ')
                    infos[m['ref']] = pages.get(norm.get('File:' + m['titre'], norm.get(cle, cle)))
            if par_id:
                if par_titre:
                    client.attendre()
                q = client.json_api(api, pageids='|'.join(str(m['pageid']) for m in par_id))
                pages = {p['pageid']: p for p in q['query']['pages']}
                for m in par_id:
                    infos[m['ref']] = pages.get(m['pageid'])
    return infos


def trouver_pexels(client, m):
    """URL du fichier Pexels (HEAD sur le serveur de fichiers, jamais sur la page)."""
    if m.get('url'):
        return m['url']
    for fps in m['fps']:
        u = url_pexels(m['id'], fps, m['largeur'], m['hauteur'])
        try:
            client.lire(u, 'HEAD')
            return u
        except Echec:
            client.dormir(1.0)
    raise Echec(f"aucun fichier {m['largeur']} × {m['hauteur']} au serveur de fichiers pour l'identifiant {m['id']} (vérifier la taille proposée par la page, à lire par le propriétaire)")


# ------------------------------------------------------------------ exécution

def verifier_type(nom, ctype):
    """Une page web à la place d'un fichier média (blocage, vérification) est un refus, jamais un fichier."""
    if ctype.lower().startswith('text/html') and os.path.splitext(nom)[1].lower() not in EXT_HTML:
        raise Refus('le site renvoie une page web (blocage ou vérification) à la place du fichier')


def traiter(client, racine, m, page=None):
    """Télécharge un média. Retourne sa ligne de manifeste."""
    ligne = {'ref': m['ref'], 'type': m['type'], 'dossier': m['dossier']}
    try:
        if m['type'] == 'commons':
            if not page or 'imageinfo' not in page:
                raise Echec('introuvable au serveur (titre ou identifiant inexact)')
            ii = page['imageinfo'][0]
            titre = page['title'].split(':', 1)[1]
            dest = chemin_dest(racine, m, titre)
            ligne.update(titre=page['title'], url=ii['url'], page=ii.get('descriptionurl'), sha1_api=ii['sha1'], largeur=ii.get('width'),
                         hauteur=ii.get('height'), mime=ii.get('mime'), depose_le=ii.get('timestamp'), televerse_par=ii.get('user'),
                         meta={k: propre(ii.get('extmetadata', {}).get(k, {}).get('value')) for k in META})
            url = ii['url']
        elif m['type'] == 'pexels':
            url = trouver_pexels(client, m)
            dest = chemin_dest(racine, m, nom_distant_direct(url))
            ligne['url'] = url_publique(url)
        else:
            url = m['url']
            dest = chemin_dest(racine, m, nom_distant_direct(url))
            ligne['url'] = url_publique(url)
        ligne['fichier'] = dest.replace('\\', '/')
        if os.path.exists(dest):
            ligne['statut'] = 'deja_present'
        else:
            client.attendre()
            data, ctype = client.lire(url)
            verifier_type(dest, ctype)
            ecrire_sans_ecraser(dest, data)
            ligne.update(statut='ok', type_contenu=ctype)
    except Refus as e:
        ligne.update(statut='refuse', motif=str(e))
    except Echec as e:
        ligne.update(statut='introuvable' if 'introuvable' in str(e) or 'aucun fichier' in str(e) else 'echec', motif=str(e))
    except FileExistsError:
        ligne['statut'] = 'deja_present'
    if ligne.get('fichier') and os.path.exists(ligne['fichier']):
        ligne['sha1'] = sha1_fichier(ligne['fichier'])
        ligne['octets'] = os.path.getsize(ligne['fichier'])
        if ligne.get('sha1_api'):
            ligne['sha1_conforme_api'] = ligne['sha1'] == ligne['sha1_api']
        if m.get('sha1'):
            ligne['sha1_conforme_attendu'] = ligne['sha1'] == m['sha1']
        if ligne.get('sha1_conforme_api') is False or ligne.get('sha1_conforme_attendu') is False:
            ligne['statut'] = 'empreinte_differente' if ligne['statut'] == 'ok' else ligne['statut']
    return ligne


def nom_libre(chemin):
    """Le chemin, ou le chemin suivi de -2, -3… si un fichier existe déjà (aucun écrasement)."""
    base, ext = os.path.splitext(chemin)
    n, essai = 1, chemin
    while os.path.exists(essai):
        n += 1
        essai = f'{base}-{n}{ext}'
    return essai


def ecrire_nouveau(chemin, texte):
    os.makedirs(os.path.dirname(chemin) or '.', exist_ok=True)
    with open(chemin, 'x', encoding='utf-8') as f:
        f.write(texte)


def liste_manuelle(lignes, horodatage):
    """Texte de la liste « à télécharger par le propriétaire » : fichiers refusés ou introuvables."""
    sortie = [f'# À télécharger par le propriétaire ({horodatage})', '',
              'Fichiers que l\'outil n\'a pas pu ou pas dû télécharger (aucun contournement n\'a été tenté). Déposer chacun ici, sous le nom imposé.', '',
              '| Réf. | Nom imposé | Adresse | Motif |', '|---|---|---|---|']
    for l in lignes:
        nom = os.path.basename(l.get('fichier') or '') or f"{l['ref']}__(nom d'origine)"
        adresse = l.get('page') or l.get('url') or l.get('titre') or ''
        sortie.append(f"| {l['ref']} | {nom} | {adresse} | {l.get('statut')} : {l.get('motif', '')} |".replace('\n', ' '))
    return '\n'.join(sortie) + '\n'


def apercu(racine, medias):
    print(f'Aperçu (aucun appel réseau) : {len(medias)} média(s) vers {racine}')
    for m in medias:
        cible = m.get('url') or m.get('titre') or m.get('pageid') or m.get('id')
        print(f"  {m['ref']:<8} {m['type']:<8} {m['dossier']}/ {m['ref']}__…  <- {cible}")
    print('Relancer avec --executer pour télécharger (liste validée par le propriétaire).')


def lancer(args, ouvrir=None, dormir=time.sleep):
    medias = charger_liste(args.liste)
    ua = agent_valide(args.agent_utilisateur)
    racine = args.racine
    if not re.search(r'source-v\d+', racine.replace('\\', '/')):
        print('Attention : --racine n\'est pas un dossier kit/media/source-vN.', file=sys.stderr)
    for m in medias:                                         # noms et collisions vérifiés avant tout réseau
        if m['type'] == 'direct':
            chemin_dest(racine, m, nom_distant_direct(m['url']))
    if not args.executer:
        apercu(racine, medias)
        return 0
    horodatage = time.strftime('%Y%m%d-%H%M%S')
    manifeste = args.manifeste or nom_libre(os.path.join(racine, f'MANIFESTE_TELECHARGEMENT_{horodatage}.json'))
    if os.path.exists(manifeste):
        raise ValueError(f'le manifeste existe déjà : {manifeste} (aucun écrasement)')
    client = Client(ua, pause=args.pause, essais=args.essais, ouvrir=ouvrir, dormir=dormir)
    infos = interroger_commons(client, medias) if any(m['type'] == 'commons' for m in medias) else {}
    lignes = []
    for m in medias:
        ligne = traiter(client, racine, m, infos.get(m['ref']))
        lignes.append(ligne)
        print(m['ref'], ligne['statut'], ligne.get('motif', ''), flush=True)
    ecrire_nouveau(manifeste, json.dumps({'agent_utilisateur': ua, 'date': horodatage, 'medias': lignes}, ensure_ascii=False, indent=1))
    manuels = [l for l in lignes if l['statut'] in ('refuse', 'introuvable', 'echec')]
    if manuels:
        ecrire_nouveau(nom_libre(os.path.join(racine, 'manuel', f'A_TELECHARGER_PAR_LE_PROPRIETAIRE_{horodatage}.md')), liste_manuelle(manuels, horodatage))
    comptes = {}
    for l in lignes:
        comptes[l['statut']] = comptes.get(l['statut'], 0) + 1
    print('Bilan :', ', '.join(f'{k} {v}' for k, v in sorted(comptes.items())), '| manifeste :', manifeste)
    return 1 if manuels or comptes.get('empreinte_differente') else 0


def main(argv=None):
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, 'reconfigure'):
            flux.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0], allow_abbrev=False)   # noms entiers : le garde-fou les lit
    ap.add_argument('liste', help='liste JSON validée par le propriétaire')
    ap.add_argument('--racine', required=True, help='dossier de dépôt, par exemple episodes/<id>/kit/media/source-vN')
    ap.add_argument('--agent-utilisateur', required=True, help='nom du robot et adresse de la chaîne ; jamais une adresse e-mail')
    ap.add_argument('--executer', action='store_true', help='télécharger (sans cette option : aperçu, aucun appel réseau)')
    ap.add_argument('--pause', type=float, default=3.5, help='secondes entre deux fichiers (3 au minimum)')
    ap.add_argument('--essais', type=int, default=3)
    ap.add_argument('--manifeste', help='chemin du manifeste JSON (sinon sous --racine)')
    args = ap.parse_args(argv)
    try:
        return lancer(args)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print('Erreur : ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
