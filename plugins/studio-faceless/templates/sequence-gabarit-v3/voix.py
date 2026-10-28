"""Gabarit v3 — piste son d'une séquence : la voix seule (24/10/2026, skill studio-faceless:episode).

Depuis le 24/10/2026, une séquence ne porte que la voix : musique et effets se mixent sur le film collé
(DIRECTION_AUDIO.md § 3 du plugin ; outils/montage/mix_film.py du plugin). Ce script ne fait que :
  - pistes/stem-voix.wav : la bande voix du kit en double mono, gain 1, sans coupe ni recalage (référence du mix du film) ;
  - media/audio/piste-voix.wav : la même voix, gain unique vers −18 LUFS, crête d'échantillon ≤ −3 dBFS (écoute de travail) ;
  - pistes/voix-rapport.txt.
FFmpeg par HYPERFRAMES_FFMPEG_PATH, sinon celui du PATH ; aucun chemin absolu ; refus d'écraser.
Usage, depuis la racine de la chaîne : python -I -B episodes/<id>/production/<séquence>-vN/voix.py
"""
import os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FF = os.environ.get('HYPERFRAMES_FFMPEG_PATH') or shutil.which('ffmpeg')
VOIX = os.path.join(HERE, 'media', 'audio', 'bande-voix.wav')       # bande ralentie et vérifiée du kit
STEM = os.path.join(HERE, 'pistes', 'stem-voix.wav')
PISTE = os.path.join(HERE, 'media', 'audio', 'piste-voix.wav')
RAPPORT = os.path.join(HERE, 'pistes', 'voix-rapport.txt')
CIBLE_I, PLAFOND_ECH = -18.0, -3.0


def mesure(path):
    out = subprocess.run([FF, '-hide_banner', '-nostats', '-i', path, '-af', 'ebur128=peak=sample', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    i = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1])
    crete = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', out)[-1])
    return i, crete


def main():
    if not FF:
        sys.exit('FFmpeg introuvable (HYPERFRAMES_FFMPEG_PATH ou PATH)')
    if not os.path.isfile(VOIX):
        sys.exit('Bande voix manquante : ' + VOIX)
    for p in (STEM, PISTE, RAPPORT):
        if os.path.exists(p):
            sys.exit('Sortie existante, aucun écrasement : ' + p)
    os.makedirs(os.path.dirname(STEM), exist_ok=True)
    subprocess.run([FF, '-v', 'error', '-n', '-i', VOIX, '-af', 'pan=stereo|c0=c0|c1=c0', '-ar', '48000',
                    '-c:a', 'pcm_f32le', STEM], check=True)
    i, crete = mesure(STEM)
    gain = min(CIBLE_I - i, PLAFOND_ECH - crete)
    subprocess.run([FF, '-v', 'error', '-n', '-i', STEM, '-af', f'volume={gain:.2f}dB', '-c:a', 'pcm_s24le', PISTE], check=True)
    i2, crete2 = mesure(PISTE)
    texte = (f'Voix seule (gabarit v3)\nbande : {os.path.relpath(VOIX, HERE)}\n'
             f'stem-voix.wav : {i:.1f} LUFS, crête {crete:.1f} dBFS (gain 1)\n'
             f'piste-voix.wav : gain {gain:+.2f} dB, soit {i2:.1f} LUFS, crête {crete2:.1f} dBFS\n'
             'Musique et effets : aucun (mix du film). Effets proposés : tableau du README.\n')
    open(RAPPORT, 'w', encoding='utf-8').write(texte)
    print(texte, end='')


if __name__ == '__main__':
    main()
