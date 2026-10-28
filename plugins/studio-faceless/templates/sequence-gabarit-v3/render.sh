#!/usr/bin/env bash
# Gabarit de séquence — rendu final d'une séquence (render.sh du gabarit v2, 20/10/2026, repris tel quel en v3).
# Écrit par le producteur, lancé par le Studio Director en arrière-plan, depuis Git Bash (Node ≥ 22) :
#   bash episodes/<id>/production/<séquence>-vN/render.sh
# MP4 1920 × 1080, 30 i/s, H.264 + AAC 48 kHz ; --workers 2 au plus ; refuse d'écraser une sortie existante.
# Aucun chemin absolu : FFmpeg par HYPERFRAMES_FFMPEG_PATH (sinon le PATH) ; Chrome de HyperFrames
# (~/.cache/hyperframes/chrome) sauf si HYPERFRAMES_BROWSER_PATH est défini.
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

cd "$ROOT"
node node_modules/hyperframes/bin/hyperframes.mjs render "$DIR" --output "$SORTIE" --fps 30 --workers 2 --quality delivery
"$FF" -v error -xerror -i "$SORTIE" -f null -                       # décodage complet : aucune erreur
echo "Rendu terminé : $SORTIE"
