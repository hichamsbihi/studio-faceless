"""Serveur local du globe de l'épisode 004 (127.0.0.1 seulement), arrêté juste après les captures.
Repris de episodes/episode-003-german-gold/kit/cartes/serve.py (relu le 26/10/2026), seul le chemin des polices change.
  /fonts/… → ../../gabarit/media/fonts/ ; le reste → ce dossier (vendor/ : MapLibre 6.13.0, licence BSD-3, vendor/.../LICENSE.txt)."""
import functools, http.server, sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINES = {'/fonts/': ICI.parent.parent / 'gabarit' / 'media' / 'fonts'}


class Gestion(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        chemin = path.split('?', 1)[0]
        for prefixe, racine in RACINES.items():
            if chemin.startswith(prefixe):
                return str(racine / chemin[len(prefixe):])
        return super().translate_path(path)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, *a):
        pass


Gestion.extensions_map.update({'.mjs': 'text/javascript', '.js': 'text/javascript', '.geojson': 'application/json'})
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8766
http.server.ThreadingHTTPServer(('127.0.0.1', port), functools.partial(Gestion, directory=str(ICI))).serve_forever()
