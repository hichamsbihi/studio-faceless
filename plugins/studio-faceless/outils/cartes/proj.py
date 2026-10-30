"""Projections pour les cartes d'une chaîne : Albers, UTM, Equal Earth, Web Mercator (numpy).

Validé sur MM (Maps & Means), 26/10/2026 (cartes de l'épisode 004, Alaska) ; versé au plugin le 30/10/2026 (décision 1 :
code général dans `outils/cartes/`, modèles dans `domaines/geo-economie/cartes/`). D'après Snyder (1987) ; Šavrič, Patterson
et Jenny (2018) pour Equal Earth.
- Albers conique équivalente, ellipsoïde GRS80. Les paramètres par défaut sont ceux d'Alaska Albers (EPSG:3338 : parallèles
  55° et 65° N, origine 50° N, méridien -154°), l'exemple de MM : une chaîne les passe explicitement pour sa région.
- UTM (WGS84, hémisphère nord), pour lire les tuiles Sentinel-2 ; `zone` à passer.
- Equal Earth (sphère), pour le monde ; `lon0` pour le méridien central.
- Web Mercator, pour les tuiles et les images du globe MapLibre.
Coordonnées projetées en mètres (Albers, UTM, Mercator) ou en rayons terrestres (Equal Earth). `km(a, b)` : distance
orthodromique. Bibliothèque : numpy. Voir `${CLAUDE_PLUGIN_ROOT}/outils/cartes/README.md`.
"""
import math

import numpy as np

R_MERC = 6378137.0


class Albers:
    def __init__(self, lat1=55, lat2=65, lat0=50, lon0=-154, a=6378137.0, f=1 / 298.257222101):
        self.a = a; self.e2 = 2 * f - f * f; self.e = math.sqrt(self.e2); self.lon0 = math.radians(lon0)
        m = lambda p: math.cos(p) / math.sqrt(1 - self.e2 * math.sin(p) ** 2)
        p1, p2, p0 = map(math.radians, (lat1, lat2, lat0))
        self.n = (m(p1) ** 2 - m(p2) ** 2) / (self.q(p2) - self.q(p1))
        self.C = m(p1) ** 2 + self.n * self.q(p1)
        self.r0 = a * math.sqrt(self.C - self.n * self.q(p0)) / self.n

    def q(self, p):
        s = np.sin(p); e = self.e
        return (1 - self.e2) * (s / (1 - self.e2 * s * s) - np.log((1 - e * s) / (1 + e * s)) / (2 * e))

    def avant(self, lon, lat):
        """lon, lat en degrés (nombres ou tableaux numpy) → x, y en mètres."""
        r = self.a * np.sqrt(self.C - self.n * self.q(np.radians(lat))) / self.n
        t = self.n * (np.radians(lon) - self.lon0)
        return r * np.sin(t), self.r0 - r * np.cos(t)

    def arriere(self, x, y):
        x, y = np.asarray(x, float), np.asarray(y, float)
        r = np.hypot(x, self.r0 - y); t = np.arctan2(x, self.r0 - y)
        q = (self.C - (r * self.n / self.a) ** 2) / self.n; e = self.e
        p = np.arcsin(np.clip(q / 2, -1, 1))
        for _ in range(12):
            s = np.sin(p)
            p = p + (1 - self.e2 * s * s) ** 2 / (2 * np.cos(p)) * (q / (1 - self.e2) - s / (1 - self.e2 * s * s)
                                                                    + np.log((1 - e * s) / (1 + e * s)) / (2 * e))
        return np.degrees(self.lon0 + t / self.n), np.degrees(p)


def utm(lon, lat, zone, a=6378137.0, f=1 / 298.257223563):
    """Coordonnées UTM (hémisphère nord) en mètres ; lon, lat en degrés, nombres ou tableaux."""
    e2 = 2 * f - f * f; ep2 = e2 / (1 - e2); k0 = 0.9996
    p = np.radians(lat); l0 = math.radians(-183 + 6 * zone)
    N = a / np.sqrt(1 - e2 * np.sin(p) ** 2); T = np.tan(p) ** 2; C = ep2 * np.cos(p) ** 2
    A = (np.radians(lon) - l0) * np.cos(p)
    M = a * ((1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256) * p - (3 * e2 / 8 + 3 * e2 ** 2 / 32 + 45 * e2 ** 3 / 1024) * np.sin(2 * p)
             + (15 * e2 ** 2 / 256 + 45 * e2 ** 3 / 1024) * np.sin(4 * p) - 35 * e2 ** 3 / 3072 * np.sin(6 * p))
    x = k0 * N * (A + (1 - T + C) * A ** 3 / 6 + (5 - 18 * T + T * T + 72 * C - 58 * ep2) * A ** 5 / 120) + 500000
    y = k0 * (M + N * np.tan(p) * (A * A / 2 + (5 - T + 9 * C + 4 * C * C) * A ** 4 / 24
                                   + (61 - 58 * T + T * T + 600 * C - 330 * ep2) * A ** 6 / 720))
    return x, y


A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
M_EE = math.sqrt(3) / 2


def equal_earth(lon, lat, lon0=0.0):
    """Equal Earth sur la sphère unité : lon, lat en degrés → x, y (y vers le nord)."""
    d = np.asarray(lon, float) - lon0
    l = np.radians(np.where(np.abs(d) <= 180, d, (d + 180) % 360 - 180))   # ±180 gardés tels quels (bord des anneaux)
    t = np.arcsin(M_EE * np.sin(np.radians(lat))); t2 = t * t; t6 = t2 ** 3
    x = 2 * math.sqrt(3) * l * np.cos(t) / (3 * (9 * A4 * t6 * t2 + 7 * A3 * t6 + 3 * A2 * t2 + A1))
    y = t * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))
    return x, y


def equal_earth_inv(x, y, lon0=0.0):
    """Inverse d'Equal Earth (sphère unité), par Newton sur θ ; NaN hors de la carte."""
    x, y = np.asarray(x, float), np.asarray(y, float); t = y.copy()
    for _ in range(12):
        t2 = t * t; t6 = t2 ** 3
        f = t * (A1 + A2 * t2 + t6 * (A3 + A4 * t2)) - y
        t = t - f / (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2))
    t2 = t * t; t6 = t2 ** 3
    lat = np.degrees(np.arcsin(np.clip(np.sin(t) / M_EE, -1, 1)))
    lon = np.degrees(3 * x * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)) / (2 * math.sqrt(3) * np.cos(t))) + lon0
    dehors = (np.abs(np.sin(t) / M_EE) > 1) | (np.abs(lon - lon0) > 180)
    return np.where(dehors, np.nan, lon), np.where(dehors, np.nan, lat)


def mercator(lon, lat):
    """Web Mercator en mètres."""
    return R_MERC * np.radians(lon), R_MERC * np.log(np.tan(math.pi / 4 + np.radians(lat) / 2))


def mercator_inv(x, y):
    return np.degrees(np.asarray(x) / R_MERC), np.degrees(2 * np.arctan(np.exp(np.asarray(y) / R_MERC)) - math.pi / 2)


def km(a, b):
    """Distance orthodromique en km entre deux points (lon, lat)."""
    R = 6371.0088; lo1, la1, lo2, la2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))
