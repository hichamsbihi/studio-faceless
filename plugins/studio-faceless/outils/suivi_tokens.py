"""Suivi de la consommation de tokens des sessions de la chaîne (mesure validée sur AA, 18/10/2026).

Lit les journaux de Claude Code (*.jsonl) sans en afficher le contenu et donne, par session :
appels, contexte médian et maximal, contexte de départ, tokens effectifs (Mt) et écritures de cache (Mt),
puis le même résumé pour ses sous-agents.
Tokens effectifs = entrée + 0,1 × lecture de cache + 2 × écriture de cache + 5 × sortie.

Usage (Git Bash) :  python -B ${CLAUDE_PLUGIN_ROOT}/outils/suivi_tokens.py [--depuis AAAA-MM-JJ]
À lancer à chaque fin d'étape ; ne modifie aucun fichier.
"""
import argparse
import glob
import json
import os
import re
import statistics
import sys

# Journaux de Claude Code pour le dossier de la chaîne (chemin encodé : tout caractère hors lettres et chiffres devient « - »)
JOURNAUX = os.path.join(os.path.expanduser('~'), '.claude', 'projects',
                        re.sub(r'[^A-Za-z0-9]', '-', os.path.abspath(os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd())))


def mesurer(fichier):
    vus, lignes = set(), []
    for ligne in open(fichier, encoding='utf8', errors='ignore'):
        try:
            j = json.loads(ligne)
        except ValueError:
            continue
        m = j.get('message') if isinstance(j.get('message'), dict) else {}
        u = m.get('usage')
        if not u or j.get('type') != 'assistant':
            continue
        cle = m.get('id') or j.get('uuid')
        if cle in vus:
            continue
        vus.add(cle)
        lignes.append((j.get('timestamp', ''), u))
    if not lignes:
        return None
    g = lambda u, k: u.get(k, 0) or 0
    ctx = [g(u, 'input_tokens') + g(u, 'cache_read_input_tokens') + g(u, 'cache_creation_input_tokens') for _, u in lignes]
    cr = sum(g(u, 'cache_read_input_tokens') for _, u in lignes)
    cw = sum(g(u, 'cache_creation_input_tokens') for _, u in lignes)
    inp = sum(g(u, 'input_tokens') for _, u in lignes)
    out = sum(g(u, 'output_tokens') for _, u in lignes)
    return {'debut': lignes[0][0][:16], 'appels': len(lignes), 'med': int(statistics.median(ctx)),
            'max': max(ctx), 'depart': ctx[0], 'eff': (inp + 0.1 * cr + 2 * cw + 5 * out) / 1e6, 'cw': cw / 1e6}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--depuis', default='2026-10-16', help='date de début (AAAA-MM-JJ)')
    a = p.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    sessions = {}
    for f in glob.glob(os.path.join(JOURNAUX, '*.jsonl')) + glob.glob(os.path.join(JOURNAUX, '*', 'subagents', '*.jsonl')):
        sous = os.path.basename(os.path.dirname(f)) == 'subagents'
        sid = os.path.basename(os.path.dirname(os.path.dirname(f))) if sous else os.path.basename(f)[:-6]
        r = mesurer(f)
        if not r or r['debut'][:10] < a.depuis:
            continue
        s = sessions.setdefault(sid[:8], {'main': None, 'sous': []})
        if sous:
            s['sous'].append(r)
        else:
            s['main'] = r
    k = lambda r: f"{r['appels']} appels, ctx méd {r['med'] // 1000} k / max {r['max'] // 1000} k, départ {r['depart'] // 1000} k, {r['eff']:.1f} Mt eff, cache écrit {r['cw']:.1f} Mt"
    for sid, s in sorted(sessions.items(), key=lambda x: (x[1]['main'] or {'debut': ''})['debut']):
        m = s['main']
        print(f"{sid} {m['debut'] if m else '?'} principale : {k(m) if m else '—'}")
        if s['sous']:
            sb = s['sous']
            print(f"  {len(sb)} sous-agents : {sum(x['appels'] for x in sb)} appels, ctx méd {int(statistics.median(x['med'] for x in sb)) // 1000} k / max {max(x['max'] for x in sb) // 1000} k, "
                  f"{sum(x['eff'] for x in sb):.1f} Mt eff, cache écrit {sum(x['cw'] for x in sb):.1f} Mt")


if __name__ == '__main__':
    main()
