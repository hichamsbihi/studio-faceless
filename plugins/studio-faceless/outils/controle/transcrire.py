"""Transcrit une prise localement et la compare au texte de référence — 15/10/2026.

Méthode de ${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md § 2–3 : filtre `whisper` de FFmpeg 9.0.2 (whisper.cpp) et un modèle ggml
(par exemple ggml-base.en.bin, licence MIT, 148 Mo). Le modèle est gardé HORS du projet ; tout téléchargement se fait
avec l'accord du propriétaire de la chaîne. Le filtre a besoin de chemins relatifs (les « : » des lecteurs Windows cassent ses
arguments) : le script travaille donc depuis le dossier du modèle, puis déplace ses sorties.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/transcrire.py PRISE.mp3 --modele CHEMIN/ggml-base.en.bin --sortie DOSSIER [--texte TEXTE.txt]
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/transcrire.py PRISE.mp3 --modele … --isoler 37.5 4.5     (vérifie un passage douteux)
Sorties (dossier --sortie, refuse d'écraser) : <nom>-texte.txt, <nom>-mots.json (mots horodatés ±0,1 s), <nom>-phrases.txt.
Avec --texte : liste des écarts mot à mot. Un mot doublé ou étrange se vérifie TOUJOURS avec --isoler avant d'être
signalé au propriétaire : c'est souvent un artefact de Whisper (constaté plusieurs fois sur l'épisode 003 d'AA). Les nombres écrits
en chiffres par Whisper (« 113 » pour « hundred and thirteenth ») ne sont pas des écarts.
"""
import argparse, difflib, glob, json, os, re, shutil, subprocess, sys

FF_DEFAUT = next(iter(sorted(glob.glob(os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'WinGet', 'Packages', 'Gyan.FFmpeg*', '*', 'bin')))), '')  # FFmpeg de WinGet s'il existe ; aucun chemin propre à une machine
FF = os.environ.get('HYPERFRAMES_FFMPEG_PATH') or shutil.which('ffmpeg') or os.path.join(FF_DEFAUT, 'ffmpeg.exe')


def sec(x):
    h, m, r = x.split(':'); s, ms = r.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def whisper(audio, modele, mot_a_mot, debut=None, duree=None):
    dossier, nom = os.path.split(os.path.abspath(modele))
    tmp = f'_transcrire_{os.getpid()}_{int(mot_a_mot)}.srt'
    filtre = f'whisper=model={nom}:language=en:queue=20:use_gpu=false:destination={tmp}:format=srt' + (':max_len=1' if mot_a_mot else '')
    cmd = [FF, '-v', 'error', '-y'] + (['-ss', str(debut), '-t', str(duree)] if debut is not None else []) + \
          ['-i', os.path.abspath(audio), '-ar', '16000', '-ac', '1', '-af', filtre, '-f', 'null', '-']
    r = subprocess.run(cmd, cwd=dossier, capture_output=True, text=True, encoding='utf-8', errors='replace')
    chemin = os.path.join(dossier, tmp)
    if r.returncode or not os.path.exists(chemin):
        sys.exit('Transcription impossible : ' + r.stderr[-400:])
    srt = open(chemin, encoding='utf-8', errors='replace').read()
    os.remove(chemin)  # fichier temporaire créé par ce script
    return [(sec(a), sec(b), w.strip()) for a, b, w in re.findall(r'(\d\d:\d\d:\d\d,\d+) --> (\d\d:\d\d:\d\d,\d+)\n(.*?)\n', srt) if w.strip()]


def norm(w):
    return re.sub(r"[^\w']", '', w.lower().replace('’', "'"))


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser()
    ap.add_argument('prise'); ap.add_argument('--modele', required=True)
    ap.add_argument('--sortie'); ap.add_argument('--texte')
    ap.add_argument('--isoler', nargs=2, type=float, metavar=('DEBUT', 'DUREE'))
    a = ap.parse_args()
    if not os.path.isfile(a.modele):
        sys.exit('Modèle introuvable : ' + a.modele + ' (à garder hors du projet ; téléchargement avec l\'accord du propriétaire)')
    if a.isoler:
        segs = whisper(a.prise, a.modele, False, *a.isoler)
        print(f'[{a.isoler[0]:.2f} s + {a.isoler[1]:.2f} s] ' + ' '.join(w for _, _, w in segs))
        return
    if not a.sortie:
        sys.exit('--sortie est obligatoire (sauf avec --isoler)')
    base = os.path.join(a.sortie, os.path.splitext(os.path.basename(a.prise))[0])
    outs = [base + s for s in ('-texte.txt', '-mots.json', '-phrases.txt')]
    for p in outs:
        if os.path.exists(p):
            sys.exit('Sortie existante, aucun écrasement : ' + p)
    os.makedirs(a.sortie, exist_ok=True)
    segs = whisper(a.prise, a.modele, False)
    mots = whisper(a.prise, a.modele, True)
    texte = ' '.join(w for _, _, w in segs)
    open(outs[0], 'x', encoding='utf-8').write(texte + '\n')
    json.dump({'source': 'Whisper (filtre whisper de FFmpeg, max_len=1) ; ±0,1 s ; orthographe des noms propres approximative',
               'mots': [{'w': w, 'start': round(t0, 2), 'end': round(t1, 2)} for t0, t1, w in mots]},
              open(outs[1], 'x', encoding='utf-8'), ensure_ascii=False, indent=0)
    phrases, cur, t_deb = [], [], None
    for i, (t0, t1, w) in enumerate(mots):
        t_deb = t0 if t_deb is None else t_deb
        cur.append(w)
        if re.search(r'[.?!]["”]?$', w) or i == len(mots) - 1:
            phrases.append(f'{t_deb:7.2f} – {t1:7.2f}  {" ".join(cur)}'); cur, t_deb = [], None
    open(outs[2], 'x', encoding='utf-8').write('Début – fin (s) · texte selon Whisper, ±0,1 s\n' + '\n'.join(phrases) + '\n')
    print(f'Transcription : {len(mots)} mots, {len(phrases)} phrases → {a.sortie}')
    print(texte)
    if a.texte:
        ref = re.sub(r'\[[^\]]*\]', ' ', open(a.texte, encoding='utf-8').read())  # retire les balises ElevenLabs
        r = [norm(w) for w in ref.split() if norm(w)]
        h = [norm(w) for _, _, w in mots if norm(w)]
        th = [t0 for t0, _, w in mots if norm(w)]
        ecarts = [op for op in difflib.SequenceMatcher(None, r, h, autojunk=False).get_opcodes() if op[0] != 'equal']
        print(f'\nComparaison au texte ({len(r)} mots attendus, {len(h)} entendus) : {len(ecarts)} écart(s)')
        for tag, i1, i2, j1, j2 in ecarts:
            t = th[j1] if j1 < len(th) else (th[-1] if th else 0)
            print(f'  ≈ {t:6.2f} s · {tag} · texte « {" ".join(r[i1:i2])} » → entendu « {" ".join(h[j1:j2])} »')
        print('  Vérifier chaque écart avec --isoler avant de le signaler (artefacts de Whisper fréquents).')


if __name__ == '__main__':
    main()
