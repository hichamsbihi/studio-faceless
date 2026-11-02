"""Relevé de toutes les vidéos publiques d'une chaîne YouTube (API Data v3).

Usage : python -I -B youtube_chaine.py @handle sortie.json
Clé : variable d'environnement YOUTUBE_API_KEY, posée par le propriétaire ; jamais écrite dans un fichier.
Ratio = vues ÷ médiane des 30 longues voisines (15 avant, 15 après), longues seulement ; un court dure 180 s au plus.
Coût : environ 1 unité d'API par appel (playlistItems et videos par 50). Refuse d'écraser un fichier existant.
Validé sur AA (études de Tifo Sports, 26/10/2026, et du positionnement, 02/11/2026).
"""
import json, os, re, sys, statistics, urllib.parse, urllib.request
from datetime import datetime, timezone

API = "https://www.googleapis.com/youtube/v3/"
SEUIL_COURT_S = 180  # un short dure 3 min au plus
unites = 0


def get(endpoint, **params):
    global unites
    params["key"] = os.environ["YOUTUBE_API_KEY"]
    url = API + endpoint + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        unites += 1
        return json.load(r)


def duree_s(iso):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def main(handle, sortie):
    if os.path.exists(sortie):
        sys.exit(f"{sortie} existe déjà : rien n'est écrasé")
    if not os.environ.get("YOUTUBE_API_KEY"):
        sys.exit("YOUTUBE_API_KEY absente : le propriétaire la pose dans l'environnement")
    ch = get("channels", part="snippet,statistics,contentDetails", forHandle=handle)["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, token = [], None
    while True:
        p = {"part": "contentDetails", "playlistId": uploads, "maxResults": 50}
        if token:
            p["pageToken"] = token
        r = get("playlistItems", **p)
        ids += [it["contentDetails"]["videoId"] for it in r["items"]]
        token = r.get("nextPageToken")
        if not token:
            break
    videos = []
    for i in range(0, len(ids), 50):
        r = get("videos", part="snippet,contentDetails,statistics", id=",".join(ids[i:i + 50]))
        for v in r["items"]:
            sn, st = v["snippet"], v.get("statistics", {})
            d = duree_s(v["contentDetails"].get("duration"))
            videos.append({
                "id": v["id"],
                "titre": sn["title"],
                "publiee": sn["publishedAt"][:16],
                "duree_s": d,
                "format": "court" if d <= SEUIL_COURT_S else "long",
                "vues": int(st.get("viewCount", 0)),
                "likes": int(st.get("likeCount", 0)),
                "commentaires": int(st.get("commentCount", 0)),
                "tags": sn.get("tags", []),
                "description_debut": sn.get("description", "")[:600],
            })
    videos.sort(key=lambda x: x["publiee"])
    longues = [v for v in videos if v["format"] == "long"]
    for i, v in enumerate(longues):
        voisines = [w["vues"] for w in longues[max(0, i - 15):i] + longues[i + 1:i + 16]]
        med = statistics.median(voisines) if voisines else 0
        v["ratio"] = round(v["vues"] / med, 2) if med else None
    sn, st = ch["snippet"], ch["statistics"]
    out = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M+00:00"),
        "source": "YouTube Data API v3",
        "chaine": {
            "id": ch["id"], "titre": sn["title"], "creee": sn["publishedAt"][:10],
            "pays": sn.get("country"), "description": sn.get("description", ""),
            "abonnes": int(st.get("subscriberCount", 0)), "vues": int(st.get("viewCount", 0)),
            "nb_videos": int(st.get("videoCount", 0)),
        },
        "videos": videos,
    }
    with open(sortie, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"{sn['title']} : {len(videos)} vidéos ({len(longues)} longues), "
          f"{out['chaine']['abonnes']} abonnés, {unites} unités d'API")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
