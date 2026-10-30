"""Recale les repères mot à mot d'une bande voix ralentie.

Validé sur MM (Maps & Means), 19/10/2026 (leçon technique « horodatage des mots », 16/10/2026, venue d'AA). Versé au
plugin le 30/10/2026. Complète `transcrire.py` (même dossier, qui fournit `whisper`, `norm` et le chemin de FFmpeg).

Méthode :
1. silencedetect (-50 dB, ≥ 0,25 s) : les vrais départs de la voix ;
2. Whisper mot à mot sur des morceaux découpés aux silences (≥ 4 s), et non sur la bande entière ;
3. chaque mot qui tombe dans un silence est poussé à sa fin ; le premier mot après un silence part à la fin de ce silence ;
4. alignement sur le texte validé (balises retirées) ; les mots que Whisper écrit autrement (nombres, noms) reçoivent
   le temps du passage correspondant, réparti au prorata des lettres.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/recaler.py BANDE.wav TEXTE.txt MODELE SORTIE_DOSSIER NOM
Écrit SORTIE_DOSSIER/NOM-mots.json et NOM-phrases.txt ; refuse d'écraser. MODELE : le modèle ggml de `transcrire.py`
(hors du projet). Voir aussi `${CLAUDE_PLUGIN_ROOT}/outils/shorts/recaler.py` (autre outil : repères d'un short).
"""
import difflib, json, os, re, subprocess, sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transcrire import whisper, FF, norm  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if len(sys.argv) != 6 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0 if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help') else 2)
    bande, texte, modele, sortie, nom = sys.argv[1:6]
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    mots_json = os.path.join(sortie, f"{nom}-mots.json")
    phrases_txt = os.path.join(sortie, f"{nom}-phrases.txt")
    for p in (mots_json, phrases_txt):
        if os.path.exists(p):
            sys.exit("existe, aucun écrasement : " + p)

    # 1. silences
    r = subprocess.run([FF, "-hide_banner", "-i", bande, "-af", "silencedetect=noise=-50dB:d=0.25", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    duree = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).group(3)) + \
        60 * int(re.search(r"Duration: (\d+):(\d+)", r.stderr).group(2))
    debuts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    fins = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    silences = list(zip(debuts, fins + [duree] * (len(debuts) - len(fins))))
    # parole = complément des silences
    parole, t = [], 0.0
    for s0, s1 in silences:
        if s0 - t > 0.05:
            parole.append((t, s0))
        t = s1
    if duree - t > 0.05:
        parole.append((t, duree))

    # 2. morceaux de 4 s au moins, coupés aux silences
    morceaux, cur = [], None
    for a, b in parole:
        cur = (a, b) if cur is None else (cur[0], b)
        if cur[1] - cur[0] >= 4.0:
            morceaux.append(cur); cur = None
    if cur:
        if morceaux and cur[1] - cur[0] < 1.5:
            morceaux[-1] = (morceaux[-1][0], cur[1])
        else:
            morceaux.append(cur)

    hyp = []  # (start, end, mot)
    for a, b in morceaux:
        d0 = max(0.0, a - 0.05)
        for t0, t1, w in whisper(bande, modele, True, d0, (b + 0.05) - d0):
            hyp.append([min(b, d0 + t0), min(b, d0 + t1), w])

    # 3. mots tombés dans un silence → fin du silence ; premier départ après un silence
    def dans_silence(t):
        for s0, s1 in silences:
            if s0 <= t < s1:
                return s1
        return None
    for h in hyp:
        s1 = dans_silence(h[0])
        if s1 is not None:
            h[0] = s1; h[1] = max(h[1], s1 + 0.05)
    for s0, s1 in silences:
        apres = [h for h in hyp if h[0] >= s1 - 0.3]
        if apres:
            apres[0][0] = s1
        for h in hyp:  # un mot ne déborde pas dans le silence qui le suit
            if h[0] < s0 < h[1]:
                h[1] = s0

    # 4. alignement sur le texte validé
    ref_brut = re.sub(r"\[[^\]]*\]", " ", open(texte, encoding="utf-8").read()).split()
    ref = [norm(w) for w in ref_brut]
    hn = [norm(w) for _, _, w in hyp]
    temps = [None] * len(ref)
    sm = difflib.SequenceMatcher(None, ref, hn, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                temps[i1 + k] = (hyp[j1 + k][0], hyp[j1 + k][1])
        elif tag == "replace" and j2 > j1:
            t0, t1 = hyp[j1][0], hyp[j2 - 1][1]
            poids = [max(1, len(ref[i])) for i in range(i1, i2)]
            tot, acc = sum(poids), 0
            for k, i in enumerate(range(i1, i2)):
                a = t0 + (t1 - t0) * acc / tot; acc += poids[k]
                temps[i] = (a, t0 + (t1 - t0) * acc / tot)
    # trous (mots non entendus) : interpolation entre voisins
    for i in range(len(temps)):
        if temps[i] is None:
            g = next((temps[k][1] for k in range(i - 1, -1, -1) if temps[k]), 0.0)
            d = next((temps[k][0] for k in range(i + 1, len(temps)) if temps[k]), g)
            temps[i] = (g, max(g, d))
    mots = [{"w": w, "start": round(a, 2), "end": round(b, 2)} for w, (a, b) in zip(ref_brut, temps)]
    non_alignes = sum(1 for op in sm.get_opcodes() if op[0] != "equal")

    os.makedirs(sortie, exist_ok=True)
    json.dump({"source": f"Recalé le {date.today():%d/%m/%Y} : silencedetect -50 dB ≥ 0,25 s, Whisper base.en par morceaux ({len(morceaux)}), "
                         f"texte {os.path.basename(texte)} ; {non_alignes} passages écrits autrement par Whisper, répartis au prorata",
               "bande": os.path.basename(bande), "duree": round(duree, 2),
               "silences": [[round(a, 2), round(b, 2)] for a, b in silences], "mots": mots},
              open(mots_json, "x", encoding="utf-8"), ensure_ascii=False, indent=0)
    lignes, cur, deb = [], [], None
    for m in mots:
        deb = m["start"] if deb is None else deb
        cur.append(m["w"])
        if re.search(r'[.?!]["”]?$', m["w"]):
            lignes.append(f"{deb:7.2f} – {m['end']:7.2f}  {' '.join(cur)}"); cur, deb = [], None
    if cur:
        lignes.append(f"{deb:7.2f} – {mots[-1]['end']:7.2f}  {' '.join(cur)}")
    open(phrases_txt, "x", encoding="utf-8").write(
        f"Début – fin (s) · texte {os.path.basename(texte)}, recalé sur les départs réels ({os.path.basename(bande)}, {duree:.2f} s)\n" + "\n".join(lignes) + "\n")
    print(f"{nom} : {len(morceaux)} morceaux, {len(silences)} silences, {len(hyp)} mots entendus / {len(ref)} attendus, "
          f"{non_alignes} passages non identiques")


if __name__ == "__main__":
    main()
