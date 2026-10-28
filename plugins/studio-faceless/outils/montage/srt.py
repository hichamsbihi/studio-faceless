"""Sous-titres SRT anglais du master d'un film de la chaîne. Outil commun du studio (24/10/2026).

Repris du script qui a fait le SRT de l'E007 d'AA (scratchpad, faire_srt_e007.py), même algorithme :
  - texte = le script vérifié (blocs ```text sous des titres « ## seqN ») ; temps = les mots recalés de chaque séquence
    (JSON {"mots": [{"w", "start", "end"}]}), alignés au texte par difflib ; mots non reconnus (nombres écrits en lettres…)
    interpolés entre leurs voisins ; décalés du début de chaque séquence lu dans le journal du master ;
  - une phrase par sous-titre, coupée en morceaux qui tiennent sur deux lignes de 42 caractères au plus (de préférence
    après une virgule), sans couper un nom propre (deux mots à majuscule) ; deux lignes équilibrées ;
  - un sous-titre de moins d'1 s rejoint le suivant s'il tient encore sur deux lignes ; durée de 1 à 7 s, aucun
    chevauchement (50 ms d'écart), 0,3 s de tenue après le dernier mot.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/srt.py --script episodes/<id>/SCRIPT_v1.md --mots "kit/voix/{seq}-montage-mots-recales.json"
                                     --journal episodes/<id>/outputs/<master>.log.txt --sortie episodes/<id>/PUBLICATION_vN.en.srt
Le motif {seq} des mots recalés est relatif au dossier du script (la racine de l'épisode), sauf chemin absolu.
Le journal peut être le .log.txt du master ou le .journal.json de ${CLAUDE_PLUGIN_ROOT}/outils/montage/assembler.py. Refuse d'écraser.
"""
import argparse, difflib, json, os, re, sys, unicodedata


def norm(w):
    w = unicodedata.normalize('NFKD', w.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(ch for ch in w if not unicodedata.combining(ch)))


def tient(texte):                       # tient sur deux lignes de 42 caractères au plus
    if len(texte) <= 42:
        return True
    mm = texte.split()
    return any(len(' '.join(mm[:c])) <= 42 and len(' '.join(mm[c:])) <= 42 for c in range(1, len(mm)))


def lignes(texte):                      # deux lignes équilibrées de 42 caractères au plus
    if len(texte) <= 42:
        return texte
    mm = texte.split()
    best = None
    for c in range(1, len(mm)):
        l1, l2 = ' '.join(mm[:c]), ' '.join(mm[c:])
        if len(l1) <= 42 and len(l2) <= 42 and (best is None or abs(len(l1) - len(l2)) < best[0]):
            best = (abs(len(l1) - len(l2)), l1 + '\n' + l2)
    return best[1] if best else texte


def debuts(journal):
    """Début de chaque séquence (s), tel qu'écrit dans le journal du master."""
    if journal.endswith('.json'):
        with open(journal, encoding='utf-8') as f:
            j = json.load(f)
        return {s['id']: s['debut_image'] / j['fps'] for s in j['segments'] if s['type'] == 'sequence'}
    with open(journal, encoding='utf-8') as f:
        return {k: float(v) for k, v in re.findall(r'^(seq\d+)\s+([\d.]+) s', f.read(), re.M)}


def sous_titres(vw, mots, debut):
    sm = difflib.SequenceMatcher(None, [norm(w) for w in vw], [norm(m['w']) for m in mots], autojunk=False)
    t = [None] * len(vw)
    for a, b, n in sm.get_matching_blocks():
        for i in range(n):
            t[a + i] = (mots[b + i]['start'], mots[b + i]['end'])
    known = [i for i, x in enumerate(t) if x]
    for i in range(len(vw)):          # interpolation des mots non reconnus (nombres écrits en lettres, etc.)
        if t[i] is None:
            p = max([j for j in known if j < i], default=None)
            q = min([j for j in known if j > i], default=None)
            s0 = t[p][1] if p is not None else 0.0
            s1 = t[q][0] if q is not None else s0 + 1.0
            a = p if p is not None else -1
            b = q if q is not None else len(vw)
            f0, f1 = (i - a) / (b - a), (i + 1 - a) / (b - a)
            t[i] = (s0 + (s1 - s0) * f0, s0 + (s1 - s0) * f1)
    phrases, cur = [], []             # phrases, puis morceaux de deux lignes au plus (coupure de préférence après une virgule)
    for i, w in enumerate(vw):
        cur.append(i)
        if re.search(r'[.?!]["”]?$', w):
            phrases.append(cur)
            cur = []
    if cur:
        phrases.append(cur)
    subs = []
    for ph in phrases:
        morceaux, m = [], []
        for i in ph:
            if m and not tient(' '.join(vw[j] for j in m + [i])):
                cut = max([x for x in range(1, len(m)) if vw[m[x - 1]].endswith(',')
                           and len(' '.join(vw[j] for j in m[:x])) >= 35], default=len(m))
                while cut == len(m) and cut > 1 and vw[m[cut - 1]][:1].isupper() and vw[i][:1].isupper():
                    cut -= 1                    # ne pas couper un nom propre (« Premier / League »)
                morceaux.append(m[:cut])
                m = m[cut:]
            m.append(i)
        morceaux.append(m)
        for m in morceaux:
            subs.append([debut + t[m[0]][0], debut + t[m[-1]][1] + 0.3, lignes(' '.join(vw[j] for j in m))])
    return subs


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description='SRT anglais du master d\'un film de la chaîne (outils/montage/README.md du plugin).')
    ap.add_argument('--script', required=True, help='script vérifié (blocs ```text sous « ## seqN »)')
    ap.add_argument('--mots', required=True, help='motif des mots recalés, avec {seq} (relatif au dossier du script)')
    ap.add_argument('--journal', required=True, help='journal du master (.log.txt) ou .journal.json de l\'assembleur')
    ap.add_argument('--sortie', required=True, help='fichier SRT à écrire (refus d\'écraser)')
    a = ap.parse_args()
    if '{seq}' not in a.mots:
        sys.exit('Le motif --mots doit contenir {seq}')
    if os.path.exists(a.sortie):
        sys.exit('Sortie existante, aucun écrasement : ' + a.sortie)
    racine = os.path.dirname(os.path.abspath(a.script))
    with open(a.script, encoding='utf-8') as f:
        blocs = dict(re.findall(r'## (seq\d+)\b.*?```text\n(.*?)```', f.read(), re.S))
    debut = debuts(a.journal)
    manque = sorted(set(blocs) - set(debut))
    if manque:
        sys.exit('Séquences du script absentes du journal : ' + ', '.join(manque))
    subs = []
    for k in sorted(blocs, key=lambda s: int(s[3:])):
        p = a.mots.format(seq=k)
        p = p if os.path.isabs(p) else os.path.join(racine, p)
        with open(p, encoding='utf-8') as f:
            subs += sous_titres(blocs[k].split(), json.load(f)['mots'], debut[k])
    subs.sort(key=lambda s: s[0])
    i = 0
    while i < len(subs) - 1:                        # un sous-titre de moins d'1 s rejoint le suivant s'il reste sur deux lignes
        a_, b_ = subs[i], subs[i + 1]
        joint = lignes((a_[2] + ' ' + b_[2]).replace('\n', ' '))
        if a_[1] - a_[0] < 1.0 and b_[0] - a_[0] < 2.0 and joint.count('\n') <= 1 and all(len(l) <= 42 for l in joint.split('\n')):
            subs[i] = [a_[0], b_[1], joint]
            del subs[i + 1]
        else:
            i += 1
    for i, s in enumerate(subs):                    # pas de chevauchement, 1 à 7 s
        nxt = subs[i + 1][0] - 0.05 if i + 1 < len(subs) else s[1] + 2
        s[1] = min(max(s[1], s[0] + 1.0), nxt, s[0] + 7.0)
    fmt = lambda x: f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round((x % 1) * 1000)) % 1000:03d}'
    with open(a.sortie, 'x', encoding='utf-8', newline='\n') as f:
        for i, (t0, t1, txt) in enumerate(subs, 1):
            f.write(f'{i}\n{fmt(t0)} --> {fmt(t1)}\n{txt}\n\n')
    longues = sum(1 for _, _, txt in subs for l in txt.split('\n') if len(l) > 42)
    print(len(subs), 'sous-titres ; plus court', round(min(b - a for a, b, _ in subs), 2), 's ; plus long',
          round(max(b - a for a, b, _ in subs), 2), 's ; lignes de plus de 42 caractères :', longues)


if __name__ == '__main__':
    main()
