"""Traitement des photos et des extraits vidéo d'une chaîne : découpe, format, passage en SDR.

Validé sur MM (Maps & Means), 24/10/2026 : outil commun né dans l'épisode 003. Versé au plugin le 30/10/2026 (décision 6)
sous sa forme neutre : les traitements de couleur `present` (couleur, ombres encre) et `archive` (bichromie encre/ivoire)
sont la charte de l'épisode 003 de MM et ne sont pas versés ; une chaîne qui veut un étalonnage le range dans `marque/`
(une chaîne de filtres FFmpeg dans un fichier texte) et le passe par --filtre-fichier, ou par --filtre.

Usage, depuis la racine de la chaîne :
  python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/medias/traiter.py SOURCE SORTIE [--debut S] [--duree D] [--cadre couvrir|contenir]
                                                         [--filtre "VF" | --filtre-fichier marque/traitement.vf]
Photo (jpg, png) -> JPEG 1920 px de large au plus ; vidéo -> MP4 H.264 30 i/s sans son, 6 s au plus (règle par défaut du
plugin, REFERENTIEL_QUALITE_REALISATION.md § 2 bis), GOP 15 (seek-safe), 1920 × 1080. Sans filtre : aucun étalonnage.
Toute source HDR (HLG ou PQ, BT.2020) est ramenée en SDR BT.709 avant le traitement : un extrait qui garde ses balises HDR
fait passer HyperFrames en rendu HDR « en couches », qui ignore une partie de render(t) (MM, 24/10/2026).
Exemple de filtre de MM (bichromie encre -> ivoire, charte de l'épisode 003, `--cadre contenir`) :
  format=gray,eq=contrast=1.12:gamma=0.95,format=rgb24,lutrgb=r='16+val*(242-16)/255':g='24+val*(230-24)/255':b='38+val*(207-38)/255',vignette=PI/4.5
Refuse d'écraser. FFmpeg et ffprobe : dans le PATH (ou HYPERFRAMES_FFMPEG_PATH pour FFmpeg).
"""
import argparse, os, pathlib, shutil, subprocess, sys

FF = os.environ.get('HYPERFRAMES_FFMPEG_PATH') or shutil.which('ffmpeg') or 'ffmpeg'
FP = os.environ.get('HYPERFRAMES_FFPROBE_PATH') or shutil.which('ffprobe') or 'ffprobe'
DUREE_MAX = 6.0  # extraits de moins de six secondes (règle par défaut du plugin ; MM, 24/10/2026)
# Source HDR (HLG ou PQ, BT.2020) : ramenée en SDR BT.709 avant le traitement (S1 v2 de MM, 24/10/2026).
VERS_SDR = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
            "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,")
BALISES_SDR = ['-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709']
VIDEO = {'.mp4', '.mov', '.webm', '.mkv', '.ogv', '.avi', '.mpg', '.mpeg', '.m4v'}


def transfert(src):
    r = subprocess.run([FP, '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                        'stream=color_transfer', '-of', 'csv=p=0', str(src)], capture_output=True, text=True)
    return r.stdout.strip()


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('source'); p.add_argument('sortie')
    p.add_argument('--debut', type=float, default=0.0)
    p.add_argument('--duree', type=float, default=DUREE_MAX)
    p.add_argument('--cadre', choices=['couvrir', 'contenir'], default='couvrir',
                   help="couvrir : recadré en 16:9 plein (défaut) ; contenir : format d'origine gardé")
    g = p.add_mutually_exclusive_group()
    g.add_argument('--filtre', help="chaîne de filtres FFmpeg (-vf) d'étalonnage, appliquée après la découpe")
    g.add_argument('--filtre-fichier', help="fichier texte qui contient cette chaîne (exemple : marque/traitement.vf)")
    a = p.parse_args()
    src, out = pathlib.Path(a.source), pathlib.Path(a.sortie)
    if out.exists():
        sys.exit(f"{out} existe déjà : jamais d'écrasement, choisir un autre nom")
    grade = a.filtre or (pathlib.Path(a.filtre_fichier).read_text(encoding='utf-8').strip() if a.filtre_fichier else '') or 'null'
    if src.suffix.lower() in VIDEO:
        if a.duree > DUREE_MAX:
            sys.exit(f"extrait de {a.duree} s : {DUREE_MAX} s au plus")
        geo = ("scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" if a.cadre == 'couvrir'
               else "scale=-2:1080")
        hdr = transfert(src) in ('arib-std-b67', 'smpte2084')
        cmd = [FF, '-hide_banner', '-loglevel', 'error', '-ss', str(a.debut), '-t', str(a.duree), '-i', str(src),
               '-vf', f"{VERS_SDR if hdr else ''}fps=30,{geo},{grade},format=yuv420p", '-an', '-c:v', 'libx264',
               '-crf', '16', '-preset', 'slow', '-g', '15', *BALISES_SDR, '-movflags', '+faststart', str(out)]
        if hdr:
            print("source HDR : ramenée en SDR BT.709")
    else:
        geo = "scale='min(1920,iw)':-2"
        cmd = [FF, '-hide_banner', '-loglevel', 'error', '-i', str(src), '-vf', f"{geo},{grade}", '-q:v', '2', str(out)]
    subprocess.run(cmd, check=True)
    print(f"{'filtre' if grade != 'null' else 'neutre'} ({a.cadre}) : {out}")


if __name__ == '__main__':
    main()
