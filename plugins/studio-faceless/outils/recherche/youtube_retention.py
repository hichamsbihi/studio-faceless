"""Rétention de chaque vidéo de sa propre chaîne (API YouTube Analytics v2, accès OAuth du propriétaire).

Usage : python -I -B youtube_retention.py @handle sortie.json [--courts] [--reautoriser]
Accès : le propriétaire crée un client OAuth « Application de bureau » et dépose son fichier JSON en
~/.studio-faceless/youtube/client_secret.json, hors de tout dépôt. Au premier lancement, le navigateur s'ouvre :
il se connecte et accorde lui-même la lecture seule (yt-analytics.readonly). Le jeton reste dans ce dossier
(jeton-<id de la chaîne>.json), jamais affiché ni écrit ailleurs ; en mode Test, Google le retire au bout de 7 jours
et l'outil redemande l'accord. Lancé par Claude principal, jamais par un sous-agent (accord dans le navigateur).
Liste des vidéos : API Data v3 avec YOUTUBE_API_KEY, comme youtube_chaine.py ; longues seulement, sauf --courts.
Par vidéo : vues, durée moyenne, pourcentage moyen regardé ; courbe de 100 points (audienceWatchRatio,
relativeRetentionPerformance) ; rétention à 0:30 et 1:00, interpolée sur la courbe (part des vues encore là).
Coût : gratuit ; environ 3 unités Data, 2 requêtes Analytics par vidéo. Refuse d'écraser un fichier existant.
Validé sur AA (02/11/2026 : accord donné par le propriétaire, 9 longues, 18 requêtes Analytics).
"""
import base64, hashlib, http.server, json, os, re, secrets, sys, time, urllib.error, urllib.parse, urllib.request, webbrowser
from datetime import datetime, timezone
from pathlib import Path

DATA = "https://www.googleapis.com/youtube/v3/"
ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
PORTEE = "https://www.googleapis.com/auth/yt-analytics.readonly"
DOSSIER = Path.home() / ".studio-faceless" / "youtube"
SEUIL_COURT_S = 180  # un short dure 3 min au plus
DELAI_ACCORD_S = 300
requetes = {"data": 0, "analytics": 0}


def data(endpoint, **params):
    params["key"] = os.environ["YOUTUBE_API_KEY"]
    url = DATA + endpoint + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        requetes["data"] += 1
        return json.load(r)


def duree_s(iso):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def poster(url, champs):
    """POST de formulaire ; renvoie le JSON, ou {"erreur", "detail"} sans rien de secret."""
    req = urllib.request.Request(url, data=urllib.parse.urlencode(champs).encode())
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            err = json.load(e)
        except ValueError:
            err = {}
        return {"erreur": err.get("error", e.code), "detail": err.get("error_description", "")}


def accord(client):
    """Ouvre le navigateur ; le propriétaire se connecte et accorde l'accès (PKCE, retour sur 127.0.0.1)."""
    verifieur = secrets.token_urlsafe(64)
    defi = base64.urlsafe_b64encode(hashlib.sha256(verifieur.encode()).digest()).rstrip(b"=").decode()
    etat = secrets.token_urlsafe(16)
    recu = {}

    class Retour(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if "code" not in q and "error" not in q:
                self.send_response(404)
                self.end_headers()
                return
            recu.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<p>Accord reçu. Vous pouvez fermer cet onglet.</p>".encode())

        def log_message(self, *args):  # rien dans la console : le code d'accord y passerait
            pass

    serveur = http.server.HTTPServer(("127.0.0.1", 0), Retour)
    serveur.timeout = 5
    retour = f"http://127.0.0.1:{serveur.server_port}"
    url = client["auth_uri"] + "?" + urllib.parse.urlencode({
        "client_id": client["client_id"], "redirect_uri": retour, "response_type": "code",
        "scope": PORTEE, "access_type": "offline", "prompt": "consent", "state": etat,
        "code_challenge": defi, "code_challenge_method": "S256"})
    print("Accord à donner dans le navigateur (lecture seule de YouTube Analytics). "
          "S'il ne s'ouvre pas, coller ce lien :\n" + url, flush=True)
    webbrowser.open(url)
    fin = time.monotonic() + DELAI_ACCORD_S
    while not recu and time.monotonic() < fin:
        serveur.handle_request()
    serveur.server_close()
    if not recu:
        sys.exit("aucun accord reçu en 5 min : relancer l'outil")
    if recu.get("state") != etat:
        sys.exit("retour du navigateur refusé : état différent")
    if "error" in recu:
        sys.exit(f"accord refusé : {recu['error']}")
    return poster(client["token_uri"], {
        "code": recu["code"], "client_id": client["client_id"], "client_secret": client["client_secret"],
        "redirect_uri": retour, "grant_type": "authorization_code", "code_verifier": verifieur})


def jeton(nom, reautoriser):
    """Jeton d'accès en mémoire ; seul le jeton d'actualisation est gardé, dans DOSSIER (un fichier par chaîne)."""
    secret = DOSSIER / "client_secret.json"
    if not secret.exists():
        sys.exit(f"{secret} absent : le propriétaire crée un client OAuth « Application de bureau » "
                 "et y dépose son fichier JSON")
    client = json.loads(secret.read_text(encoding="utf-8")).get("installed")
    if not client:
        sys.exit("client_secret.json n'est pas celui d'une « Application de bureau » (clé installed absente)")
    fichier = DOSSIER / ("jeton-" + re.sub(r"[^\w.-]", "_", nom.lstrip("@")) + ".json")
    garde = {} if reautoriser or not fichier.exists() else json.loads(fichier.read_text(encoding="utf-8"))
    if garde.get("refresh_token"):
        r = poster(client["token_uri"], {
            "client_id": client["client_id"], "client_secret": client["client_secret"],
            "refresh_token": garde["refresh_token"], "grant_type": "refresh_token"})
        if "access_token" in r:
            return r["access_token"]
        print("jeton retiré par Google (7 jours en mode Test, ou accès révoqué) : nouvel accord", flush=True)
    r = accord(client)
    if "access_token" not in r:
        sys.exit(f"échange refusé par Google : {r.get('erreur')} {r.get('detail')}")
    if r.get("refresh_token"):
        fichier.write_text(json.dumps({
            "refresh_token": r["refresh_token"],
            "obtenu": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M+00:00")}), encoding="utf-8")
    return r["access_token"]


def rapport(acces, **params):
    url = ANALYTICS + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + acces})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            requetes["analytics"] += 1
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            msg = json.load(e)["error"]["message"]
        except (ValueError, KeyError, TypeError):
            msg = str(e.code)
        if e.code == 403:
            sys.exit(f"accès refusé ({msg}) : API YouTube Analytics à activer dans le projet Google Cloud, "
                     "ou accord donné pour une autre chaîne (relancer avec --reautoriser et choisir la bonne)")
        sys.exit(f"API YouTube Analytics : {msg}")


def a_l_instant(points, t, d, col=1):
    """Valeur de la courbe à t secondes (interpolation linéaire entre les points de elapsedVideoTimeRatio)."""
    if not points or not d or t > d:
        return None
    r = t / d
    if r <= points[0][0]:
        return points[0][col]
    for p, q in zip(points, points[1:]):
        if p[0] <= r <= q[0]:
            if p[col] is None or q[col] is None:
                return None
            return round(p[col] + (q[col] - p[col]) * (r - p[0]) / (q[0] - p[0]), 4)
    return points[-1][col]


def main(handle, sortie, courts, reautoriser):
    if os.path.exists(sortie):
        sys.exit(f"{sortie} existe déjà : rien n'est écrasé")
    if not os.environ.get("YOUTUBE_API_KEY"):
        sys.exit("YOUTUBE_API_KEY absente : le propriétaire la pose dans l'environnement")
    items = data("channels", part="snippet,contentDetails", forHandle=handle).get("items")
    if not items:
        sys.exit(f"aucune chaîne pour {handle}")
    ch = items[0]
    acces = jeton(ch["id"], reautoriser)
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, token = [], None
    while True:
        p = {"part": "contentDetails", "playlistId": uploads, "maxResults": 50}
        if token:
            p["pageToken"] = token
        r = data("playlistItems", **p)
        ids += [it["contentDetails"]["videoId"] for it in r["items"]]
        token = r.get("nextPageToken")
        if not token:
            break
    videos = []
    for i in range(0, len(ids), 50):
        r = data("videos", part="snippet,contentDetails", id=",".join(ids[i:i + 50]))
        for v in r["items"]:
            d = duree_s(v["contentDetails"].get("duration"))
            if d <= SEUIL_COURT_S and not courts:
                continue
            videos.append({"id": v["id"], "titre": v["snippet"]["title"], "publiee": v["snippet"]["publishedAt"][:16],
                           "duree_s": d, "format": "court" if d <= SEUIL_COURT_S else "long"})
    videos.sort(key=lambda x: x["publiee"])
    fin = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for v in videos:
        base = {"ids": f"channel=={ch['id']}", "startDate": v["publiee"][:10], "endDate": fin,
                "filters": f"video=={v['id']}"}
        rows = rapport(acces, metrics="views,averageViewDuration,averageViewPercentage", **base).get("rows")
        vues, moy, pct = rows[0] if rows else (0, None, None)
        courbe = rapport(acces, dimensions="elapsedVideoTimeRatio",
                         metrics="audienceWatchRatio,relativeRetentionPerformance", **base).get("rows") or []
        arrondi = lambda x: round(x, 4) if x is not None else None
        courbe = sorted([round(a, 2), arrondi(b), arrondi(c)] for a, b, c in courbe)
        v.update({
            "vues": int(vues),
            "duree_moyenne_s": round(moy) if moy is not None else None,
            "pourcentage_moyen": round(pct, 1) if pct is not None else None,
            "retention_30s": a_l_instant(courbe, 30, v["duree_s"]),
            "retention_60s": a_l_instant(courbe, 60, v["duree_s"]),
            "perf_relative_30s": a_l_instant(courbe, 30, v["duree_s"], col=2),
            "courbe": courbe,
        })
    out = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M+00:00"),
        "source": "YouTube Analytics API v2 (reports.query) ; liste par YouTube Data API v3",
        "note": "courbe : [part de la durée, audienceWatchRatio, relativeRetentionPerformance] ; "
                "retention_30s = part des vues encore là à 0:30 ; perf relative : 0,5 = médiane des vidéos de même durée",
        "chaine": {"id": ch["id"], "titre": ch["snippet"]["title"]},
        "videos": videos,
    }
    with open(sortie, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    pc = lambda x: f"{x:6.1%}" if x is not None else "     -"
    print(f"{ch['snippet']['title']} : {len(videos)} vidéos, {requetes['data']} unités Data, "
          f"{requetes['analytics']} requêtes Analytics")
    print("publiée       0:30   1:00  moy.   %vu  titre")
    for v in videos:
        print(f"{v['publiee'][:10]} {pc(v['retention_30s'])} {pc(v['retention_60s'])} "
              f"{v['duree_moyenne_s'] if v['duree_moyenne_s'] is not None else '-':>4}s "
              f"{v['pourcentage_moyen'] if v['pourcentage_moyen'] is not None else '-':>5}  {v['titre'][:48]}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    options = {a for a in sys.argv[1:] if a.startswith("--")}
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2 or options - {"--courts", "--reautoriser"}:
        sys.exit(__doc__)
    main(args[0], args[1], "--courts" in options, "--reautoriser" in options)
