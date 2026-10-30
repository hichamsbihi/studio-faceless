"""Contrôle d'un script avant la voix : relances, densité de chiffres, révélations, impact sur le spectateur, evergreen.

Validé sur MM (Maps & Means), 23/10/2026 (audit stratégique, E4 blocs 3 et 5) ; règle « evergreen » validée sur MM le
26/10/2026 ; impact sur le spectateur (balises de mode de récit) PROVISOIRE sur MM depuis le 29/10/2026. Versé au plugin
le 30/10/2026 (décision 6 du passage MM, VALIDÉ, Hicham) : les seuils ci-dessous sont les valeurs de départ de MM, à
régler par chaîne (voir « Seuils »).

Bibliothèque standard seule. Ne modifie et n'écrit aucun fichier : il lit et affiche. Aucun accès au réseau.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/script.py SCRIPT.md [--mpm 140] [--detail] [--seuils direction/script_seuils.json]

Narration lue : les lignes « > » ou les blocs ```text placés sous les titres « ## ».
Les balises d'émotion ([calm], [thoughtful]…) sont retirées. Balises de contrôle, à retirer aussi du texte envoyé à
la synthèse vocale (elles ne se disent pas) :
  [REVEAL]          une révélation ; [REVEAL motif] si c'est un motif récurrent sourcé (exemple MM : un acteur)
  [RENVERSEMENT]    le renversement final
  [INCONNU terme]   première mention d'un lieu ou d'un terme inconnu du spectateur
  [ANCRE terme]     le moment où ce terme est ancré par un repère connu
  [SCENE] [MECANISME] [MIROIR] [PERSONNE] [VOUS]   mode de récit, en tête de paragraphe
Impact sur le spectateur : deux modes de suite identiques sont un écart ; [PERSONNE] ou [VOUS] au moins toutes les 90 s
(avis) ; un [INCONNU …] dans la première minute est un écart ; plus d'un « you » par séquence après l'accroche est un avis.
Mesures par minute estimée (mots cumulés divisés par --mpm, mots par minute de la voix) : mots, nombres, plus longue
suite de phrases chiffrées sans question, noms propres nouveaux (approximation : mot à majuscule hors début de phrase),
questions, révélations. Ce sont des compteurs : ils repèrent des excès, ils ne jugent pas l'intérêt d'une révélation.
Evergreen : toute expression relative au jour de l'enregistrement (« this month », « today », « now », « … ago »…) est
un écart, phrase citée ; le texte entre guillemets (citation) n'est pas lu.

Seuils : les valeurs de départ sont celles de MM. Une chaîne les règle dans `direction/script_seuils.json` (lu s'il
existe, ou donné par --seuils), par exemple :
  {"PREMIERE_QUESTION_MAX_S": 60, "REVEALS": [2, 5], "RENVERSEMENT": [0.6, 0.9], "MOTIFS_MIN": 0}
Clés permises : SUITE_CHIFFRES_MAX, NOMS_PAR_MIN_MAX, QUESTIONS_PAR_MIN, PREMIERE_QUESTION_MAX_S, ECART_QUESTIONS_MAX_S,
REVEALS, RENVERSEMENT, MOTIFS_MIN, ANCRE_MAX_S, PREMIERE_MINUTE_S, ACCROCHE_S, ECART_CONCRET_MAX_S, VOUS_PAR_SEQUENCE_MAX.
(QUESTIONS_PAR_MIN : questions par minute, bas et haut ; RENVERSEMENT : part du film.) Les écarts de la chaîne restent
écrits dans `direction/ECARTS.md`.

Code de sortie : 0 si tout est dans les seuils, 1 si un seuil est dépassé, 2 en cas d'erreur d'usage. Sans seuils de la
chaîne (ni --seuils ni direction/script_seuils.json), chaque écart n'est qu'un avis et le code reste 0.
"""
import argparse, json, os, re, sys

SUITE_CHIFFRES_MAX = 3            # phrases chiffrées d'affilée sans question
NOMS_PAR_MIN_MAX = 3              # noms propres nouveaux par minute
QUESTIONS_PAR_MIN = (8 / 12, 12 / 12)   # 8 à 12 questions pour 12 min
PREMIERE_QUESTION_MAX_S = 45      # valeur MM depuis le 28/10/2026 (60 s avant)
ECART_QUESTIONS_MAX_S = 90        # une relance toutes les 45 à 90 s (valeur MM)
REVEALS = (3, 6)
RENVERSEMENT = (0.60, 0.90)       # part du film (valeur MM)
MOTIFS_MIN = 2
ANCRE_MAX_S = 15
PREMIERE_MINUTE_S = 60            # rien d'inconnu dans la première minute
ACCROCHE_S = 30                   # le « you » est libre dans l'accroche, une fois par séquence ensuite
ECART_CONCRET_MAX_S = 90          # [PERSONNE] ou [VOUS] au moins toutes les 90 s
VOUS_PAR_SEQUENCE_MAX = 1
MODES = ('SCENE', 'MECANISME', 'MIROIR', 'PERSONNE', 'VOUS')
VOUS = re.compile(r"\b(you|your|yours|yourself|you're|you'd|you'll|you've)\b", re.I)
ANNONCES = [r"here'?s (the|a) (first |second |third |real |big )?surprise", r"but that'?s not all", r"you won'?t believe",
            r"here'?s the (crazy|wild) part"]
RELATIFS = re.compile(r"\b(this (week|month|year|spring|summer|fall|autumn|winter|decade|century)|"
                      r"(last|next|coming) (weeks?|months?|years?|spring|summer|fall|autumn|winter|decades?)|"
                      r"today'?s?|tonight|tomorrow|yesterday|now|nowadays|these days|currently|at the moment(?=[,.;:])|"
                      r"recently|lately|so far(?=[,.;:])|in recent (years|months)|upcoming|\w+ (years?|months?|weeks?|days?|decades?) ago)\b",
                      re.I)
CITATION = re.compile(r'"[^"]*"|“[^”]*”')

NOMBRE = re.compile(r"\b(\d[\d,.]*%?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
                    r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|"
                    r"hundred|thousand|million|billion|trillion|half|percent|quarter|quarters|dozen)\b", re.I)
COMMUNS = set("""The A An And But So Yet It Its This That These Those Here There Then When Which What Why How Who Where
One Two Some Most All Every Each Even Only In On At By For From To Of With As If Or Not No Now Today Still Just Over
After Before Because While Since Until Instead Meanwhile Across Many Much More Less First Second Third Fourth Last Next
We Our You Your They Their He She His Her I Let Look Imagine Think Remember Yes Well Back Down Up Out
January February March April May June July August September October November December
Monday Tuesday Wednesday Thursday Friday Saturday Sunday""".split())
EMOTION = re.compile(r"\[(calm|thoughtful|serious|softly|curious|excited|sad|warm|whispers|dramatic|confident|"
                     r"surprised|neutral|reflective|concerned|hopeful|amused)\]", re.I)
BALISE = re.compile(r"\[(REVEAL(?: motif)?|RENVERSEMENT|INCONNU [^\]]+|ANCRE [^\]]+|" + '|'.join(MODES) + r")\]")


def narration(md):
    blocs = []
    for bloc in re.split(r'\n## ', md)[1:]:
        lignes = [l[1:].strip() for l in bloc.splitlines() if l.startswith('>')]
        texte = ' '.join(l for l in lignes if l)
        if not texte:
            texte = ' '.join(re.findall(r'```text\n(.*?)```', bloc, re.S))
        if texte.strip():
            blocs.append((bloc.split('\n', 1)[0].strip(), EMOTION.sub('', texte)))
    return blocs


CLES = ('SUITE_CHIFFRES_MAX', 'NOMS_PAR_MIN_MAX', 'QUESTIONS_PAR_MIN', 'PREMIERE_QUESTION_MAX_S', 'ECART_QUESTIONS_MAX_S',
        'REVEALS', 'RENVERSEMENT', 'MOTIFS_MIN', 'ANCRE_MAX_S', 'PREMIERE_MINUTE_S', 'ACCROCHE_S', 'ECART_CONCRET_MAX_S',
        'VOUS_PAR_SEQUENCE_MAX')


CHAINE_REGLEE = False   # vrai quand la chaîne a donné ses seuils ; sinon les écarts ne sont que des avis


def seuils(chemin):
    """Remplace les valeurs de départ par celles du JSON de la chaîne (le dossier courant est la chaîne)."""
    defaut = os.path.join(os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd(), 'direction', 'script_seuils.json')
    chemin = chemin or (defaut if os.path.isfile(defaut) else None)
    if not chemin:
        return
    try:
        lus = json.load(open(chemin, encoding='utf-8'))
    except (OSError, ValueError) as e:
        print(f'erreur : seuils illisibles ({e})'); sys.exit(2)
    inconnues = [k for k in lus if k not in CLES]
    if inconnues:
        print(f'erreur : clés inconnues dans {chemin} : {", ".join(inconnues)}'); sys.exit(2)
    for k, v in lus.items():
        globals()[k] = tuple(v) if isinstance(v, list) else v
    globals()['CHAINE_REGLEE'] = True
    print(f'Seuils de la chaîne lus dans {chemin} : {", ".join(lus)}')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('script')
    p.add_argument('--mpm', type=float, default=140.0, help='mots par minute de la voix (exemple MM : environ 140)')
    p.add_argument('--detail', action='store_true', help='afficher les phrases chiffrées en suite trop longue')
    p.add_argument('--seuils', help="JSON de seuils de la chaîne (sinon direction/script_seuils.json s'il existe)")
    sys.stdout.reconfigure(encoding='utf-8')
    a = p.parse_args()
    seuils(a.seuils)
    try:
        md = open(a.script, encoding='utf-8').read()
    except OSError as e:
        print(f'erreur : {e}'); sys.exit(2)
    blocs = narration(md)
    if not blocs:
        print('erreur : aucune narration trouvée (lignes « > » ou blocs ```text sous des titres « ## »)'); sys.exit(2)

    s_par_mot = 60.0 / a.mpm
    mots_total = 0
    phrases = []          # (seconde de début, texte nettoyé, séquence)
    balises = []          # (seconde, balise)
    for titre, texte in blocs:
        for ph in re.split(r'(?<=[.!?])\s+', texte.strip()):
            if not ph:
                continue
            pos = mots_total
            for m in BALISE.finditer(ph):
                avant = len(BALISE.sub('', ph[:m.start()]).split())
                balises.append(((pos + avant) * s_par_mot, m.group(1)))
            propre = re.sub(r'\s+', ' ', BALISE.sub('', ph)).strip()
            if not propre:
                continue
            phrases.append((pos * s_par_mot, propre, titre))
            mots_total += len(propre.split())
    duree = mots_total * s_par_mot
    minutes = max(1, int(duree // 60) + (1 if duree % 60 > 5 else 0))   # une minute entamée de moins de 5 s ne fait pas une ligne

    par_min = [dict(mots=0, nombres=0, noms=0, questions=0, reveals=0) for _ in range(minutes)]
    vus, suite, suite_max, suite_pire, suite_cour = set(), 0, 0, [], []
    t_questions = []
    for t, ph, _ in phrases:
        m = min(int(t // 60), minutes - 1)
        par_min[m]['mots'] += len(ph.split())
        n = len(NOMBRE.findall(ph))
        par_min[m]['nombres'] += n
        noms = [x for x in re.findall(r"(?<!^)(?<![.?!:]\s)\b([A-Z][\w'’-]+(?:\s[A-Z][\w'’-]+)*)", ph)
                if x.split()[0] not in COMMUNS]
        nouveaux = [x for x in dict.fromkeys(noms) if x not in vus]
        vus.update(noms)
        par_min[m]['noms'] += len(nouveaux)
        if '?' in ph:
            par_min[m]['questions'] += ph.count('?')
            t_questions.append(t)
            suite, suite_cour = 0, []
        elif n:
            suite += 1
            suite_cour.append(ph)
            if suite > suite_max:
                suite_max, suite_pire = suite, list(suite_cour)
        else:
            suite, suite_cour = 0, []
    reveals = [b for b in balises if b[1].startswith('REVEAL')]
    for t, _ in reveals:
        par_min[min(int(t // 60), minutes - 1)]['reveals'] += 1

    print(f'Script : {a.script}')
    print(f'Narration : {mots_total} mots, environ {int(duree // 60)} min {int(duree % 60):02d} s à {a.mpm:.0f} mots/min ; '
          f'{len(blocs)} séquences ; {len(phrases)} phrases')
    print('\nminute | mots | nombres | noms nouveaux | questions | révélations')
    for i, d in enumerate(par_min):
        print(f'{i:>4}   | {d["mots"]:>4} | {d["nombres"]:>7} | {d["noms"]:>13} | {d["questions"]:>9} | {d["reveals"]:>11}')

    ecarts, nb = [], 0
    def verdict(ok, texte, avis=False):
        nonlocal nb
        avis = avis or not CHAINE_REGLEE
        if not ok and not avis:
            nb += 1
        print(f'  {"ok    " if ok else ("avis  " if avis else "ÉCART ")} {texte}')

    print('\nContrôles (seuils de départ de MM, réglables : voir --help)' + ('' if CHAINE_REGLEE else
          ' : la chaîne n\'a pas de direction/script_seuils.json, les écarts sont donnés comme avis et ne bloquent pas'))
    nq = len(t_questions)
    q_min, q_max = QUESTIONS_PAR_MIN[0] * duree / 60, QUESTIONS_PAR_MIN[1] * duree / 60
    verdict(q_min <= nq, f'questions : {nq} (attendu {q_min:.0f} à {q_max:.0f} pour cette durée)')
    verdict(bool(t_questions) and t_questions[0] <= PREMIERE_QUESTION_MAX_S,
            f'première question : {"aucune" if not t_questions else f"vers {t_questions[0]:.0f} s"} (attendu avant {PREMIERE_QUESTION_MAX_S} s)')
    jalons = [0.0] + t_questions + [duree]
    ecart = max(b - a_ for a_, b in zip(jalons, jalons[1:]))
    verdict(ecart <= ECART_QUESTIONS_MAX_S, f'plus long passage sans question : {ecart:.0f} s (attendu {ECART_QUESTIONS_MAX_S} s au plus)', avis=True)
    verdict(suite_max <= SUITE_CHIFFRES_MAX, f'plus longue suite de phrases chiffrées sans question : {suite_max} (attendu {SUITE_CHIFFRES_MAX} au plus)')
    if a.detail and suite_max > SUITE_CHIFFRES_MAX:
        for ph in suite_pire:
            print(f'           · {ph[:110]}')
    pire_noms = max(d['noms'] for d in par_min)
    verdict(pire_noms <= NOMS_PAR_MIN_MAX, f'noms propres nouveaux : {len(vus)} en tout, jusqu\'à {pire_noms} dans une minute (attendu {NOMS_PAR_MIN_MAX} par minute au plus ; approximation)')
    motifs = sum(1 for _, b in reveals if b == 'REVEAL motif')
    verdict(REVEALS[0] <= len(reveals) <= REVEALS[1], f'révélations marquées : {len(reveals)} (attendu {REVEALS[0]} à {REVEALS[1]})')
    verdict(motifs >= MOTIFS_MIN, f'motifs sourcés marqués : {motifs} (attendu {MOTIFS_MIN} au moins)')
    renv = [t for t, b in balises if b == 'RENVERSEMENT']
    verdict(bool(renv) and RENVERSEMENT[0] * duree <= renv[-1] <= RENVERSEMENT[1] * duree,
            f'renversement : {"absent" if not renv else f"vers {renv[-1]:.0f} s, soit {100 * renv[-1] / duree:.0f} % du film"} '
            f'(attendu entre {100 * RENVERSEMENT[0]:.0f} et {100 * RENVERSEMENT[1]:.0f} %)')
    inconnus = {b[8:]: t for t, b in balises if b.startswith('INCONNU ')}
    ancres = {b[6:]: t for t, b in balises if b.startswith('ANCRE ')}
    if inconnus:
        for terme, t0 in inconnus.items():
            t1 = ancres.get(terme)
            verdict(t1 is not None and t1 - t0 <= ANCRE_MAX_S,
                    f'ancrage de « {terme} » : {"jamais" if t1 is None else f"{t1 - t0:.0f} s après sa mention"} (attendu {ANCRE_MAX_S} s au plus)')
    else:
        verdict(False, 'termes inconnus : aucun marqué [INCONNU …] (à baliser pour mesurer les ancrages)', avis=True)

    print('\nImpact sur le spectateur (provisoire sur MM)')
    tot = [(t, b[8:]) for t, b in balises if b.startswith('INCONNU ') and t < PREMIERE_MINUTE_S]
    verdict(not tot, f'termes inconnus dans la première minute : {len(tot)} (attendu 0)')
    for t, terme in tot:
        print(f'           · « {terme} » vers {t:.0f} s')
    modes = [(t, b) for t, b in balises if b in MODES]
    if modes:
        doubles = [(t, b) for (_, b0), (t, b) in zip(modes, modes[1:]) if b == b0]
        verdict(not doubles, f'modes de récit : {len(modes)} balisés, {len(doubles)} fois deux de suite identiques (attendu 0)')
        for t, b in doubles:
            print(f'           · [{b}] répété vers {t:.0f} s')
        jalons = [0.0] + [t for t, b in modes if b in ('PERSONNE', 'VOUS')] + [duree]
        ecart = max(b - a_ for a_, b in zip(jalons, jalons[1:]))
        verdict(ecart <= ECART_CONCRET_MAX_S, f'plus long passage sans [PERSONNE] ni [VOUS] : {ecart:.0f} s (attendu {ECART_CONCRET_MAX_S} s au plus)', avis=True)
    else:
        verdict(False, 'modes de récit : aucun balisé ([SCENE], [MECANISME], [MIROIR], [PERSONNE], [VOUS])', avis=True)
    vous = {}
    for t, ph, titre in phrases:
        if t >= ACCROCHE_S:
            vous[titre] = vous.get(titre, 0) + len(VOUS.findall(CITATION.sub('', ph)))
    trop = {s: n for s, n in vous.items() if n > VOUS_PAR_SEQUENCE_MAX}
    verdict(not trop, f'« you » après l\'accroche : {sum(vous.values())} en tout, {len(trop)} séquence(s) au-delà de {VOUS_PAR_SEQUENCE_MAX}', avis=True)
    for s, n in trop.items():
        print(f'           · {s[:60]} : {n}')
    texte_bas = ' '.join(ph.lower() for _, ph, _ in phrases)
    annonces = [x for x in ANNONCES if re.search(x, texte_bas)]
    verdict(not annonces, f'surprises annoncées au lieu d\'être montrées : {len(annonces)}')
    relatifs = [(m.group(0), ph) for _, ph, _ in phrases for m in RELATIFS.finditer(CITATION.sub('', ph))]
    verdict(not relatifs, f'expressions relatives au moment (evergreen) : {len(relatifs)} (attendu 0)')
    for expr, ph in relatifs:
        print(f'           · « {expr} » : {ph[:110]}')
    print(f'\nBilan : {nb} écart(s).')
    sys.exit(1 if nb else 0)


if __name__ == '__main__':
    main()
