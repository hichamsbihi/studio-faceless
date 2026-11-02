"""Hook UserPromptSubmit du plugin studio-faceless (0.4.1).

Mesure le contexte du fil principal à chaque message du propriétaire : dernier appel du modèle dans le transcript,
entrée + cache lu + cache écrit (même mesure que outils/suivi_tokens.py). Au-delà de 200 k, rappelle à Claude
d'écrire l'état puis de proposer un /compact (Hicham, 02/11/2026 : plus de /clear). Le rappel revient à chaque
palier de 50 k ; sous le seuil, le hook ne dit rien et oublie le dernier palier. Ne bloque jamais un message.
"""
import json
import os
import sys
import tempfile

SEUIL = 200_000
PALIER = 50_000


def dernier_contexte(chemin):
    with open(chemin, 'rb') as f:
        f.seek(0, 2)
        f.seek(max(0, f.tell() - 4_000_000))
        lignes = f.read().splitlines()
    for ligne in reversed(lignes):
        try:
            j = json.loads(ligne)
        except ValueError:
            continue
        if j.get('type') != 'assistant' or j.get('isSidechain'):
            continue
        u = (j.get('message') or {}).get('usage')
        if u:
            return sum(u.get(k, 0) or 0 for k in ('input_tokens', 'cache_read_input_tokens', 'cache_creation_input_tokens'))
    return None


def main():
    data = json.loads(sys.stdin.buffer.read().decode('utf-8') or '{}')
    ctx = dernier_contexte(data['transcript_path'])
    if ctx is None:
        return
    memo = os.path.join(tempfile.gettempdir(), 'studio-faceless-contexte-' + str(data.get('session_id', 'x')) + '.txt')
    if ctx < SEUIL:
        if os.path.exists(memo):
            os.remove(memo)
        return
    palier = ctx // PALIER
    try:
        with open(memo, encoding='utf-8') as f:
            deja = int(f.read().strip() or 0)
    except (OSError, ValueError):
        deja = 0
    if palier <= deja:
        return
    with open(memo, 'w', encoding='utf-8') as f:
        f.write(str(palier))
    texte = ('Contexte du fil principal : ' + str(ctx // 1000) + ' k (seuil ' + str(SEUIL // 1000) + ' k). '
             "À la fin de la tâche en cours : écrire l'état (STATE.md de l'épisode et INDEX.md, ou l'état de la mission), "
             'puis proposer au propriétaire un /compact avec la consigne du skill episode (references/tokens-contexte.md). '
             'Pas de /clear.')
    sys.stdout.buffer.write(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'UserPromptSubmit', 'additionalContext': texte}}, ensure_ascii=False).encode('utf-8'))


if __name__ == '__main__':
    try:
        main()
    except Exception:
        pass
