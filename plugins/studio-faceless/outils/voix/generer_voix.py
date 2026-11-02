"""Génère les prises de narration par l'API ElevenLabs (validé sur AA, 02/11/2026, Q35 de son E011 : Claude génère les prises).

Généralisé de `generer_voix.py` de l'E011 d'AA. Règle : `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 4. Chaque appel est PAYANT :
l'outil annonce le coût, et ne génère rien sans `--executer` ET `--confirme-credits N` (N = le coût annoncé, donné par le propriétaire).

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/voix/generer_voix.py SCRIPT.txt --voix VOICE_ID --sortie DOSSIER --nom "E00N_S{n}_voix_v1.mp3" [--prises 2 3]
      → à blanc (défaut) : découpage du script, caractères, mots, début et fin de chaque prise, COÛT ANNONCÉ en crédits.
        Aucun appel, aucune lecture de la clé. À donner au propriétaire avant tout accord.
  … --executer --confirme-credits N     → génère ; refuse si N n'est pas exactement le coût annoncé pour les prises choisies.

Script : un fichier texte, les prises séparées par au moins deux lignes vides (trois sauts de ligne), comme le script ElevenLabs de l'E011.
  --blocs N   refuse si le script n'a pas N prises (garde-fou contre un mauvais découpage).
  --prises    numéros à générer (défaut : toutes) ; une prise déjà générée ne se regénère pas (le fichier existe : refus).
Réglages par défaut = ceux de la voix de la chaîne à lire dans `direction/ECARTS.md` (modèle eleven_v4, stabilité 0,50, similarité 0,75 sur AA) ;
aucune balise n'est ajoutée au texte (règle : aucune balise par défaut).
Coût : caractères × --facteur (1,0 par défaut ; `info_elevenlabs.py` lit le facteur du modèle sur le compte). C'est une estimation : la
facturation réelle se lit sur le compte du propriétaire, après coup (elle peut différer).

Garanties :
- La clé est lue dans la variable d'environnement `ELEVENLABS_API_KEY` seulement avec --executer ; elle n'est ni acceptée en argument, ni écrite,
  ni affichée (les messages d'erreur la masquent).
- Aucun fichier n'est écrasé (`open(…, "xb")`) ; tous les fichiers de sortie sont vérifiés AVANT le premier appel payant.
- Le premier échec arrête tout (on ne dépense pas plus après une erreur) ; le manifeste `MANIFESTE_VOIX_<date>.json` (prises faites, SHA-1,
  crédits annoncés, réglages) est écrit dans tous les cas.
- Le SDK Python `elevenlabs` doit être déjà installé : l'outil n'installe rien.
Code de sortie : 0 = fait (ou aperçu) ; 1 = erreur pendant la génération ; 2 = usage, refus ou confirmation manquante. Bibliothèque standard + SDK.
"""
import argparse, hashlib, json, math, os, re, sys, time

COUPURE = re.compile(r'(?:\r?\n[ \t]*){3,}')
CLE = 'ELEVENLABS_API_KEY'


def decouper(texte):
    return [b.strip() for b in COUPURE.split(texte.strip()) if b.strip()]


def cout(texte, facteur):
    return math.ceil(len(texte) * facteur)


def apercu_prise(n, t, facteur):
    return f"S{n}: {len(t)} car., {len(t.split())} mots, {cout(t, facteur)} crédits | début « {t[:40]} » | fin « {t[-30:]} »"


def choisir(prises, numeros):
    if not numeros:
        return list(range(1, len(prises) + 1))
    inconnus = [n for n in numeros if not 1 <= n <= len(prises)]
    if inconnus:
        raise ValueError(f'prise(s) inexistante(s) : {inconnus} (le script en compte {len(prises)})')
    return list(dict.fromkeys(numeros))


def destination(sortie, nom, n):
    if '{n}' not in nom:
        raise ValueError('--nom doit contenir {n} (numéro de la prise), par exemple E00N_S{n}_voix_v1.mp3')
    base = nom.replace('{n}', str(n))
    if os.path.basename(base) != base or base in ('', '.', '..'):
        raise ValueError('--nom est un nom de fichier, sans dossier')
    return os.path.join(sortie, base)


def masquer(message, cle):
    return message.replace(cle, '***') if cle else message


def nom_libre(chemin):
    base, ext = os.path.splitext(chemin)
    n, essai = 1, chemin
    while os.path.exists(essai):
        n += 1
        essai = f'{base}-{n}{ext}'
    return essai


def client_elevenlabs(cle):
    try:
        from elevenlabs.client import ElevenLabs
    except ImportError:
        raise RuntimeError("le SDK Python `elevenlabs` n'est pas installé ; son installation se décide avec le propriétaire (l'outil n'installe rien)")
    return ElevenLabs(api_key=cle)


def generer(client, texte, a):
    from elevenlabs import VoiceSettings
    flux = client.text_to_speech.convert(voice_id=a.voix, text=texte, model_id=a.modele,
                                         voice_settings=VoiceSettings(stability=a.stabilite, similarity_boost=a.similarite),
                                         output_format=a.format)
    return b''.join(flux)


def lancer(a, env=None, fabrique=None, convertir=None):
    """`env`, `fabrique` (crée le client) et `convertir` (appel payant) sont remplaçables : les tests n'appellent jamais le réseau."""
    env = os.environ if env is None else env
    with open(a.script, encoding='utf-8') as f:
        prises = decouper(f.read())
    if a.blocs and len(prises) != a.blocs:
        raise ValueError(f'le script a {len(prises)} prise(s), {a.blocs} attendue(s) : découpage à vérifier')
    choix = choisir(prises, a.prises)
    cibles = {n: destination(a.sortie, a.nom, n) for n in choix}
    if a.max_caracteres:
        trop = [n for n in choix if len(prises[n - 1]) > a.max_caracteres]
        if trop:
            raise ValueError(f'prise(s) {trop} au-dessus de {a.max_caracteres} caractères (limite d\'une requête) : couper le script')
    total = sum(cout(prises[n - 1], a.facteur) for n in choix)
    for n in choix:
        print(apercu_prise(n, prises[n - 1], a.facteur))
    print(f'COÛT ANNONCÉ : {total} crédits pour {len(choix)} prise(s) ({sum(len(prises[n - 1]) for n in choix)} caractères × {a.facteur}) ; '
          f'modèle {a.modele}, voix {a.voix}. Estimation : la facturation réelle se lit sur le compte.')
    if not a.executer:
        print('Aperçu : aucun appel, aucune clé lue. Après l\'accord du propriétaire : --executer --confirme-credits ' + str(total))
        return 0
    if a.confirme_credits is None:
        raise PermissionError(f'appel payant : annoncer {total} crédits au propriétaire, puis relancer avec --confirme-credits {total}')
    if a.confirme_credits != total:
        raise PermissionError(f'confirmation {a.confirme_credits} différente du coût annoncé {total} : rien n\'est généré')
    deja = [c for c in cibles.values() if os.path.exists(c)]
    if deja:
        raise FileExistsError('fichier(s) déjà présent(s), aucun appel fait : ' + ', '.join(deja))
    cle = env.get(CLE, '')
    if not cle:
        raise PermissionError(f'la variable d\'environnement {CLE} n\'existe pas (posée par le propriétaire ; elle ne se donne jamais en argument)')
    client = (fabrique or client_elevenlabs)(cle)
    os.makedirs(a.sortie, exist_ok=True)
    horodatage = time.strftime('%Y%m%d-%H%M%S')
    manifeste = {'date': horodatage, 'voix': a.voix, 'modele': a.modele, 'stabilite': a.stabilite, 'similarite': a.similarite,
                 'format': a.format, 'facteur': a.facteur, 'credits_annonces': total, 'prises': []}
    code = 0
    try:
        for n in choix:
            texte = prises[n - 1]
            try:
                audio = (convertir or generer)(client, texte, a)
                with open(cibles[n], 'xb') as fh:
                    fh.write(audio)
            except Exception as e:                                  # première erreur : on s'arrête, on ne dépense pas davantage
                manifeste['arret'] = f'prise {n} : {type(e).__name__} : {masquer(str(e), cle)[:300]}'
                print('ARRÊT : ' + manifeste['arret'], file=sys.stderr)
                code = 1
                break
            ligne = {'prise': n, 'fichier': cibles[n].replace('\\', '/'), 'caracteres': len(texte), 'mots': len(texte.split()),
                     'credits_annonces': cout(texte, a.facteur), 'octets': len(audio), 'sha1': hashlib.sha1(audio).hexdigest()}
            manifeste['prises'].append(ligne)
            print(f"   écrit {ligne['fichier']} ({ligne['octets']} octets, SHA-1 {ligne['sha1']})")
    finally:
        chemin = nom_libre(os.path.join(a.sortie, f'MANIFESTE_VOIX_{horodatage}.json'))
        with open(chemin, 'x', encoding='utf-8') as fh:
            json.dump(manifeste, fh, ensure_ascii=False, indent=1)
        print('Manifeste :', chemin)
    return code


def lire_arguments(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('script', help='fichier texte : les prises séparées par au moins deux lignes vides')
    ap.add_argument('--voix', required=True, help='voice_id de la voix de la chaîne')
    ap.add_argument('--sortie', required=True, help='dossier des prises (créé s\'il manque)')
    ap.add_argument('--nom', required=True, help='nom de fichier avec {n}, par exemple "E00N_S{n}_voix_v1.mp3"')
    ap.add_argument('--prises', type=int, nargs='*', default=[], help='numéros à générer (défaut : toutes)')
    ap.add_argument('--blocs', type=int, default=0, help='nombre de prises attendu dans le script')
    ap.add_argument('--modele', default='eleven_v4')
    ap.add_argument('--stabilite', type=float, default=0.5)
    ap.add_argument('--similarite', type=float, default=0.75)
    ap.add_argument('--format', default='mp3_44100_192')
    ap.add_argument('--facteur', type=float, default=1.0, help='crédits par caractère (1,0 par défaut ; voir info_elevenlabs.py)')
    ap.add_argument('--max-caracteres', type=int, default=0, help='refuse une prise plus longue (limite d\'une requête du modèle)')
    ap.add_argument('--executer', action='store_true', help='appel payant (sans cette option : aperçu)')
    ap.add_argument('--confirme-credits', type=int, default=None, help='coût annoncé, confirmé par le propriétaire (obligatoire avec --executer)')
    return ap.parse_args(argv)


def main(argv=None):
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, 'reconfigure'):
            flux.reconfigure(encoding='utf-8', errors='replace')
    try:
        return lancer(lire_arguments(argv))
    except (ValueError, PermissionError, FileExistsError, RuntimeError, OSError) as e:
        print('Refus : ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
