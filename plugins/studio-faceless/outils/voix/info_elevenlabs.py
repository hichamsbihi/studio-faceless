"""Lit ce que le compte ElevenLabs permet de savoir avant une génération : facteur de coût et limite des modèles, voix, solde (0.6.0, 02/11/2026).

Généralisé de `el_info.py` de l'E011 d'AA. Lecture seule : aucun de ces appels ne génère de son ni ne consomme de crédits. Une clé à droits
restreints (c'était le cas sur AA) refuse souvent les modèles, la voix ou le solde : chaque refus est affiché sans arrêter les autres lectures,
et on garde alors le facteur par défaut de `generer_voix.py` (1,0), à confirmer sur le compte du propriétaire.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/voix/info_elevenlabs.py [--modeles eleven_v4 eleven_v3 …] [--voix VOICE_ID] [--tous]
La clé est lue dans la variable d'environnement `ELEVENLABS_API_KEY` ; elle n'est ni acceptée en argument, ni écrite, ni affichée.
Le SDK Python `elevenlabs` doit être déjà installé (l'outil n'installe rien). Code de sortie : 0 = lu (même avec des refus) ; 2 = usage ou clé absente.
"""
import argparse, os, sys

CLE = 'ELEVENLABS_API_KEY'
MODELES_DEFAUT = ['eleven_v4', 'eleven_v3', 'eleven_multilingual_v2']


def court(e, cle):
    message = str(e).split("'message': ")[-1]
    return message.replace(cle, '***')[:140] if cle else message[:140]


def lire(a, env=None, fabrique=None):
    env = os.environ if env is None else env
    cle = env.get(CLE, '')
    if not cle:
        raise PermissionError(f'la variable d\'environnement {CLE} n\'existe pas (posée par le propriétaire)')
    if fabrique is None:
        try:
            from elevenlabs.client import ElevenLabs
        except ImportError:
            raise RuntimeError("le SDK Python `elevenlabs` n'est pas installé (l'outil n'installe rien)")
        fabrique = lambda k: ElevenLabs(api_key=k)
    c = fabrique(cle)
    try:
        modeles = list(c.models.list())
        voulus = None if a.tous else (a.modeles or MODELES_DEFAUT)
        for m in modeles:
            if voulus is None or m.model_id in voulus:
                print(f"modèle : {m.model_id} | facteur de coût : {getattr(m, 'token_cost_factor', None)} | "
                      f"caractères max par requête : {getattr(m, 'maximum_text_length_per_request', None)}")
    except Exception as e:
        print('modèles : refusé,', court(e, cle))
    if a.voix:
        try:
            v = c.voices.get(a.voix)
            print(f"voix : {v.name} | catégorie : {v.category}")
        except Exception as e:
            print('voix : refusé,', court(e, cle))
    try:
        s = c.user.subscription.get()
        print(f"solde : {s.character_count} crédits utilisés sur {s.character_limit} | formule : {s.tier}")
    except Exception as e:
        print('solde : refusé,', court(e, cle))
    return 0


def main(argv=None):
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, 'reconfigure'):
            flux.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--modeles', nargs='*', help='identifiants de modèles à afficher')
    ap.add_argument('--tous', action='store_true', help='tous les modèles')
    ap.add_argument('--voix', help='voice_id à lire')
    try:
        return lire(ap.parse_args(argv))
    except (PermissionError, RuntimeError) as e:
        print('Refus : ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
