# Provenance des matières du gabarit de séquence

Toutes sont des copies non modifiées des matières de l'E001 d'AA (registre : provenance de l'E003 d'AA, dossier `matieres-e001/`), sauf la licence du papier (copie de celle de la séquence 6 v2 de l'E003 d'AA) et le fond d'exemple (calcul). Empreintes SHA-1, vérifiées le 16/10/2026 contre le registre de l'E003 d'AA.

**Resource Boy** : usage personnel et commercial, sans attribution ; **pas de revente, de sous-licence ni de redistribution des fichiers seuls**, même gratuite. Ces fichiers restent dans les projets de la chaîne ; ils ne sortent que fondus dans un film.

| Fichier | Origine | Licence | SHA-1 |
|---|---|---|---|
| `media/matieres/paper-charcoal-rb09.jpg` (2560 × 1440) | Épisode 001 d'AA, séquence 4 (`episode001-sequence04/media/`) | Resource Boy, `media/matieres/resourceboy-License.txt` | `afa59b2d16dc6879f2355b8ef3239e695f7199bc` |
| `media/matieres/fog-08_resourceboy.jpg` | Épisode 001 d'AA, intro cinématique v4 (`aa-cinematic-intro-v4/media/`) ; pack « 200 Fog Textures » | Resource Boy, `media/matieres/resourceboy-fog-License.txt` | `c07dbd79a4a8d9e426a9bd2440d66373d566d080` |
| `media/matieres/fog-65_resourceboy.jpg` | idem | idem | `9aa290dff3b2383b2bab8620418550963073da63` |
| `media/matieres/grain-512.png` (512 × 512) | Épisode 001 d'AA, intro cinématique v4 (`aa-cinematic-intro-v4/generate.py`), fonction `grain()` : bruit gaussien, graine 20261012, flou σ 0,9 raccordable (`wrap`), moyenne 128, écart-type 30 | Calcul, aucun tiers | `05625d7978efcc0723e253f0e06b2383fdd34ee2` |
| `media/fonts/Newsreader-VariableFont.ttf` (graisses 200–800) | Production Type, Google Fonts | SIL OFL 1.1, `media/fonts/Newsreader-OFL.txt` | `1f3f33594af32d544aaaad15490f86dbc176da7c` |
| IBM Plex Mono (aucun fichier) | Injectée par le compilateur HyperFrames depuis Google Fonts ; cache local `~/.cache/hyperframes/fonts/ibm-plex-mono` (déjà présent : aucun téléchargement au `check`) | SIL OFL 1.1 (IBM) | — |
| `media/fonds/fond-exemple.jpg` (2112 × 1188) | Calcul de Claude, 16/10/2026 : dégradé, quatre halos, bande texturée (graine 20261016), puis la recette des fonds du kit (flou gaussien σ 14, teinte `#0B1622` à 55 %, FFmpeg). Aucune photo | Calcul, aucun tiers. **À remplacer** : il ne montre rien du récit | `9c6137c97eafcd7b6f8392d8dca2b4eaa3ee559f` |

Licences jointes : `resourceboy-License.txt` (`717e5083…`), `resourceboy-fog-License.txt` (`f9e3bee5…`), `Newsreader-OFL.txt` (`b05a591a…`).

Dans un projet de séquence, ce fichier devient la provenance de la séquence : le producteur y ajoute l'extrait de provenance du kit (photos, fonds, voix, musiques, effets).
