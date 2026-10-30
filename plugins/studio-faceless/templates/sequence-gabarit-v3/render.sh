#!/usr/bin/env bash
# Gabarit de séquence — rendu final d'une séquence (render.sh du gabarit v2, 20/10/2026, repris tel quel en v3).
# Écrit par le producteur, lancé par le Studio Director en arrière-plan, depuis Git Bash (Node ≥ 22) :
#   bash episodes/<id>/production/<séquence>-vN/render.sh
# MP4 1920 × 1080, 30 i/s, H.264 + AAC 48 kHz ; --workers 2 au plus ; refuse d'écraser une sortie existante.
# Aucun chemin absolu : FFmpeg par HYPERFRAMES_FFMPEG_PATH (sinon le PATH) ; Chrome de HyperFrames
# (~/.cache/hyperframes/chrome) sauf si HYPERFRAMES_BROWSER_PATH est défini.
# Garde HDR et rendu forcé en SDR (`--sdr`) : repris du gabarit v4 de Maps & Means (validé sur MM, 24/10/2026, épisode 003).
# Une source HLG ou PQ dans media/ faisait passer HyperFrames en rendu HDR « en couches » : image figée, rendu de 70 min.
set -euo pipefail

NOM="Chaine-EXXX-sequenceN-nom-v1"     # À REMPLACER : chaîne, épisode, séquence, nom court, version

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$DIR"                                          # racine de la chaîne : premier parent qui contient HyperFrames
while [ ! -f "$ROOT/node_modules/hyperframes/package.json" ]; do
  [ "$ROOT" = "/" ] && { echo "HyperFrames introuvable au-dessus de $DIR" >&2; exit 2; }
  ROOT="$(dirname "$ROOT")"
done
FF="${HYPERFRAMES_FFMPEG_PATH:-ffmpeg}"
SORTIE="$DIR/$NOM.mp4"

node -e 'process.exit(+process.versions.node.split(".")[0] >= 22 ? 0 : 1)' \
  || { echo "Node 22 ou plus requis (Git Bash, nvm)." >&2; exit 2; }
node -e 'process.exit(require(process.argv[1]).version === "0.8.149" ? 0 : 1)' "$ROOT/node_modules/hyperframes/package.json" \
  || { echo "HyperFrames 0.8.149 requis (version figée)." >&2; exit 2; }
[ -e "$SORTIE" ] && { echo "Export existant, aucun écrasement : $SORTIE" >&2; exit 1; }
grep -qE '^[[:space:]]*<audio id="(voix|mix)"' "$DIR/index.html" || echo "Attention : aucune piste <audio id=\"voix\"> active dans index.html (film muet)." >&2
# Aucune vidéo HDR (HLG ou PQ) dans le projet de la séquence (media/, compositions/) : la refaire en SDR par ${CLAUDE_PLUGIN_ROOT}/outils/medias/traiter.py
HDR=""
FFPROBE="${HYPERFRAMES_FFPROBE_PATH:-ffprobe}"
command -v "$FFPROBE" >/dev/null 2>&1 || { echo "ffprobe introuvable ($FFPROBE) : garde HDR impossible ; poser HYPERFRAMES_FFPROBE_PATH" >&2; exit 1; }
while IFS= read -r -d '' V; do
  T="$("$FFPROBE" -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$V" 2>/dev/null || true)"
  case "$T" in *arib-std-b67*|*smpte2084*) HDR="$HDR $V";; esac
done < <(find "$DIR" -path "$DIR/renders" -prune -o -type f \( -iname '*.mp4' -o -iname '*.webm' -o -iname '*.mov' -o -iname '*.mkv' \) -print0)
[ -z "$HDR" ] || { echo "Vidéo HDR dans media/ (à refaire en SDR par outils/medias/traiter.py) :$HDR" >&2; exit 1; }

cd "$ROOT"
node node_modules/hyperframes/bin/hyperframes.mjs render "$DIR" --output "$SORTIE" --fps 30 --workers 2 --quality delivery --sdr
"$FF" -v error -xerror -i "$SORTIE" -f null -                       # décodage complet : aucune erreur
echo "Rendu terminé : $SORTIE"
