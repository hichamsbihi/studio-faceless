# Calque 360° (charte v1 de l'épisode 003, 24/10/2026) : deux lectures, précalculées et déterministes (numpy + ffmpeg).
#   planete  : le calque de l'image A s'enroule sur 360° (projection polaire, petite planète, moitié image et moitié miroir,
#              donc sans couture), la planète tourne d'un tour, A cède à B au sommet, puis B se déroule à plat.
#   cylindre : le calque de A est posé sur un cylindre de 360° autour de la caméra (face avant = l'image, face arrière =
#              miroirs de A et de B fondus, donc sans couture) ; la caméra fait un tour complet ; A cède à B quand la face
#              avant est hors champ ; puis le calque revient à plat sur B.
# Outil du plugin depuis 0.3.0, validé sur MM (outils/medias/, 24/10/2026). Lecture retenue sur MM : cylindre (24/10/2026) ; « planète » écartée,
# gardée pour mémoire. Source vidéo : la passer d'abord par outils/medias/traiter.py (SDR).
# Usage, depuis le dossier de la chaîne :
#   python -I -B outils/medias/calque360.py cylindre SORTIE --a SRC [--a-debut S] --b SRC [--b-debut S] --duree D [--profil demo|court]
# SRC : image (recadrée en 1920 × 1080, centre) ou vidéo (lue à 30 i/s à partir de --x-debut). Sortie MP4 H.264, 30 i/s,
# GOP 15, sans son ; refuse d'écraser. Flou de mouvement : moyenne de sous-images seulement pendant la rotation rapide.
import argparse, math, pathlib, subprocess, sys
import numpy as np

W, H, FPS = 1920, 1080, 30
ENCRE = np.array([14, 20, 28], np.float32)          # #0E141C (encre de MM ; à adapter à la charte de la chaîne)
FF = 'ffmpeg'


def SIO(u):
    u = min(max(u, 0.0), 1.0); return 0.5 - 0.5 * math.cos(math.pi * u)


def L(t, a, b):
    return min(max((t - a) / (b - a), 0.0), 1.0)


class Source:
    """Image fixe ou vidéo lue en séquence (images 1920 × 1080, rgb float32)."""
    def __init__(self, path, debut):
        self.path, self.vid = path, path.suffix.lower() in ('.mp4', '.webm', '.mov', '.mkv')
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
        if self.vid:
            self.p = subprocess.Popen([FF, '-v', 'error', '-ss', str(debut), '-i', str(path), '-vf', f"fps={FPS},{vf}",
                                       '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
            self.n, self.img = -1, None
        else:
            raw = subprocess.run([FF, '-v', 'error', '-i', str(path), '-vf', vf, '-frames:v', '1', '-f', 'rawvideo',
                                  '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, check=True).stdout
            self.img = np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float32)

    def image(self, i):
        if not self.vid:
            return self.img
        while self.n < i:                                   # avance jusqu'à l'image i ; garde la dernière à la fin du fichier
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            self.img, self.n = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32), self.n + 1
        return self.img


def echantillon(img, sx, sy):
    """Lecture bilinéaire ; hors de l'image : encre."""
    dedans = (sx >= 0) & (sx <= W - 1) & (sy >= 0) & (sy <= H - 1)
    x = np.clip(sx, 0, W - 1.001); y = np.clip(sy, 0, H - 1.001)
    x0 = x.astype(np.int32); y0 = y.astype(np.int32); fx = (x - x0)[..., None]; fy = (y - y0)[..., None]
    a = img[y0, x0]; b = img[y0, x0 + 1]; c = img[y0 + 1, x0]; d = img[y0 + 1, x0 + 1]
    out = (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy
    return np.where(dedans[..., None], out, ENCRE)


YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
DX, DY = XX - (W - 1) / 2, YY - (H - 1) / 2


def miroir(u):
    """u normalisé (0..1 dans l'image) : au-delà, reflet (calque continu, sans couture)."""
    u = np.mod(u, 2.0)
    return np.where(u > 1.0, 2.0 - u, u)


def planete(img, beta, z, rho):
    """beta : angle couvert par l'image (0 → plat, π → planète complète, l'autre moitié en miroir) ; z : zoom ; rho : rotation."""
    if beta < 1e-3:
        dx, dy = DX / z, DY / z
        c, s = math.cos(-rho), math.sin(-rho)
        return echantillon(img, (W - 1) / 2 + c * dx - s * dy, (H - 1) / 2 + s * dx + c * dy)
    R0 = W / beta - (W / math.pi) * (beta / math.pi)       # rayon du sol : ≈ W/β à plat, 0 en planète complète (sol au centre)
    m = SIO(beta / math.pi)                                # le centre de la planète vient au centre de l'écran
    dx, dy = DX / z, DY / z
    c, s = math.cos(-rho), math.sin(-rho)
    dx, dy = c * dx - s * dy, s * dx + c * dy
    dy = dy + m * (R0 + H / 2)
    vx, vy = dx, dy - (R0 + H / 2)                         # vecteur depuis le centre de courbure (sous l'image)
    r = np.sqrt(vx * vx + vy * vy); phi = np.arctan2(vx, -vy)
    u = miroir(phi / beta + 0.5)
    return echantillon(img, u * (W - 1), (H - 1) - (r - R0))


def cylindre(face, dosA, dosB, theta, k):
    """Caméra au centre d'un cylindre de 360° ; face avant (−90°..90°) = image courante ; dos = miroirs de A et B fondus.
    k : 0 = image à plat, 1 = projection cylindrique ; theta : lacet de la caméra (rad)."""
    f = W / math.pi                                        # 180° de calque = 1920 px : échelle 1 au centre
    psi = theta + np.arctan2(DX, f)                        # angle vu par chaque colonne
    psi = np.mod(psi + math.pi, 2 * math.pi) - math.pi     # −π..π
    sy_c = (H - 1) / 2 + DY * f / np.sqrt(DX * DX + f * f)
    avant = np.abs(psi) <= math.pi / 2
    u_av = psi / math.pi + 0.5
    if k < 1:                                              # passage à plat : la caméra regarde la face (theta = 0 mod 2π)
        return echantillon(face, (1 - k) * XX + k * u_av * (W - 1), (1 - k) * YY + k * sy_c)
    a = echantillon(face, u_av * (W - 1), sy_c)
    if (~avant).any():
        # dos (π/2 → 3π/2) : miroir de l'image sur tout le dos, son bord droit contre le bord droit de la face (côté A,
        # vu avant la bascule) et son bord gauche contre le bord gauche de la face (côté B, vu après) ; fondu de A vers B
        p2 = np.where(psi < 0, psi + 2 * math.pi, psi)
        ud = (1 - (p2 - math.pi / 2) / math.pi).clip(0, 1) * (W - 1)
        wB = np.clip((p2 - (math.pi - 0.45)) / 0.9, 0, 1); wB = (0.5 - 0.5 * np.cos(math.pi * wB))[..., None]
        dos = echantillon(dosA, ud, sy_c) * (1 - wB) + echantillon(dosB, ud, sy_c) * wB
        a = np.where(avant[..., None], a, dos)
    return a


PROFILS = {   # fractions de la durée
    'demo':  dict(k_in=(0.08, 0.24), spin=(0.24, 0.76), k_out=(0.76, 0.92), roll=(0.10, 0.47), fondu=(0.45, 0.55), unroll=(0.53, 0.90)),
    'court': dict(k_in=(0.00, 0.17), spin=(0.17, 0.83), k_out=(0.83, 1.00), roll=(0.00, 0.44), fondu=(0.42, 0.58), unroll=(0.56, 1.00)),
}


def image_planete(t, T, P, A, B, ia, ib):
    r0, r1 = P['roll'][0] * T, P['roll'][1] * T; u0, u1 = P['unroll'][0] * T, P['unroll'][1] * T
    rho = 2 * math.pi * SIO(L(t, r0, u1))
    out = []
    for img, p in ((A.image(ia), SIO(L(t, r0, r1))), (B.image(ib), 1 - SIO(L(t, u0, u1)))):
        out.append(planete(img, math.pi * p, 1 - 0.6 * p, rho))
    w = SIO(L(t, P['fondu'][0] * T, P['fondu'][1] * T))
    return out[0] * (1 - w) + out[1] * w


def image_cylindre(t, T, P, A, B, ia, ib):
    s0, s1 = P['spin'][0] * T, P['spin'][1] * T
    theta = 2 * math.pi * SIO(L(t, s0, s1))
    k = SIO(L(t, P['k_in'][0] * T, P['k_in'][1] * T)) * (1 - SIO(L(t, P['k_out'][0] * T, P['k_out'][1] * T)))
    face = A.image(ia) if theta < math.pi else B.image(ib)     # la face change quand elle est hors champ (dos à 180°)
    if k <= 0:
        return face.copy()
    return cylindre(face, A.image(ia), B.image(ib), theta, k)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['planete', 'cylindre']); p.add_argument('sortie')
    p.add_argument('--a', required=True); p.add_argument('--a-debut', type=float, default=0.0)
    p.add_argument('--b', required=True); p.add_argument('--b-debut', type=float, default=0.0)
    p.add_argument('--duree', type=float, default=3.0); p.add_argument('--profil', choices=list(PROFILS), default='demo')
    p.add_argument('--sous', type=int, default=3, help='sous-images par image pendant la rotation rapide')
    a = p.parse_args()
    out = pathlib.Path(a.sortie)
    if out.exists():
        sys.exit(f"{out} existe déjà : jamais d'écrasement")
    A, B = Source(pathlib.Path(a.a), a.a_debut), Source(pathlib.Path(a.b), a.b_debut)
    P, T, n = PROFILS[a.profil], a.duree, int(round(a.duree * FPS))
    enc = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-g', '15', '-pix_fmt', 'yuv420p',
                            '-movflags', '+faststart', str(out)], stdin=subprocess.PIPE)
    fn = image_planete if a.mode == 'planete' else image_cylindre
    s0, s1 = (P['roll'][0], P['unroll'][1]) if a.mode == 'planete' else P['spin']
    for i in range(n):
        t = i / FPS
        rapide = s0 * T + 0.15 * (s1 - s0) * T < t < s1 * T - 0.15 * (s1 - s0) * T
        ns = a.sous if rapide else 1
        acc = np.zeros((H, W, 3), np.float32)
        for j in range(ns):                                 # obturateur à 180° : sous-images sur une demi-image
            acc += fn(t + (j / ns - 0.25) * 0.5 / FPS if ns > 1 else t, T, P, A, B, i, i)
        enc.stdin.write(np.clip(acc / ns + 0.5, 0, 255).astype(np.uint8).tobytes())
        if i % 15 == 0:
            print(f'{a.mode} {i}/{n}', flush=True)
    enc.stdin.close(); enc.wait()
    for s_ in (A, B):
        if s_.vid: s_.p.kill()
    print(f'{a.mode} : {out}')


if __name__ == '__main__':
    main()
