# Montage : collage, mix du film, sous-titres

Outils communs, tirés de l'épisode 007 d'AA (24/10/2026). Règle qui fait foi : `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 3 (mix du film à la fin ; validé sur AA, 24/10/2026), sauf écart de la chaîne dans `direction/ECARTS.md`. Python sans nouvelle dépendance (numpy, scipy) ; FFmpeg et FFprobe du PATH (ou `HYPERFRAMES_FFMPEG_PATH`, `HYPERFRAMES_FFPROBE_PATH`). Toujours `python -I -B`, depuis la racine de la chaîne. Aucun outil n'écrase une sortie.

| Outil | Rôle |
|---|---|
| `assembler.py` | Colle les MP4 des séquences, les noirs, la signature et l'outro de la chaîne, avec les fondus enchaînés ; sort le MP4, son WAV, le journal du master (`.log.txt`) et les segments à l'image près (`.journal.json`) |
| `mix_film.py` | Mixe le film entier sur le film « voix » : musique, effets, baisse sous la voix, silences voulus, gain final unique, limiteur ; l'image est copiée telle quelle |
| `srt.py` | SRT anglais du master : texte du script vérifié, temps des mots recalés, débuts de séquence du journal |

## Parcours
```text
python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/assembler.py --episode <id> --voix-seule          # 1. film « voix » + journal
python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/mix_film.py episodes/<id>/outputs/<nom>-voix.mp4 episodes/<id>/montage/plan-son.json --son-seul   # 2. essai, rien d'écrit
python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/mix_film.py episodes/<id>/outputs/<nom>-voix.mp4 episodes/<id>/montage/plan-son.json             # 3. master mixé
python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/srt.py --script episodes/<id>/SCRIPT_v1.md --mots "kit/voix/{seq}-montage-mots-recales.json" \
    --journal episodes/<id>/outputs/<nom>-voix.log.txt --sortie episodes/<id>/PUBLICATION_v1.en.srt
python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/mesurer_mix.py episodes/<id>/outputs/<nom>.mp4 episodes/<id>/outputs/<nom>-voix.mp4 \
    episodes/<id>/montage/plan-son.json --sortie episodes/<id>/outputs/controle-son-v1/MESURE_MIX_v1.md          # 4. mesure sans écoute
```
- Une correction de son = un nouveau plan (ou une nouvelle sortie) et un nouveau `mix_film.py`, sans nouveau rendu d'image.
- `assembler.py` sans `--voix-seule` garde le comportement du master E007 v1 d'AA (pistes mixées des séquences) ; vérifié le 24/10/2026 : mêmes segments, mêmes 24 clics, gain +1,40 dB, mêmes réductions du limiteur.
- `--son-seul` (les deux outils) : mesure et journal à l'écran, rien n'est écrit.
- Essais sur l'E007 d'AA (24/10/2026, dans le scratchpad) : film « voix » de 15 655 images, flux vidéo identique (MD5) à celui du master v1 approuvé ; mix de démonstration à −16,1 LUFS, −1,9 dBTP, image copiée à l'identique ; SRT régénéré identique à `PUBLICATION_v1.en.srt`. Durées : collage 22 min (encodage), mix 6,5 min.

## `montage.json` (défaut : `episodes/<id>/montage/montage.json`)
Chemins relatifs : depuis la racine de la chaîne ; `mp4`, `voix` et `mix` sont relatifs au `dossier` de la séquence.
```json
{
 "episode": "episode-001",
 "titre": "<Nom de la chaîne> — <Titre du film> (E001 master v2, internal)",
 "sequences": [
  {"id": "seq1", "dossier": "episodes/episode-001/production/seq1-v3", "mp4": "<Chaine>-E001-seq1-v3.mp4",
   "voix": "pistes/stem-voix.wav", "mix": "media/audio/piste-mixee.wav"},
  {"id": "seq2", "dossier": "episodes/episode-001/production/seq2-v3", "mp4": "<Chaine>-E001-seq2-v3.mp4"}
 ],
 "marque": [
  {"id": "logo", "fichier": "marque/<dossier-signature>/<signature-de-la-chaine>.mp4", "apres": "seq1",
   "noir_avant": 0.5, "noir_apres": 0.5}
 ],
 "outro": {"fichier": "marque/<dossier-outro>/<outro-de-la-chaine>.mp4", "noir_avant": 0},
 "fondus": {"seq2>seq3": 6, "seq3>seq4": 4},
 "sortie": {"dossier": "episodes/episode-001/outputs", "nom": "<Chaine>-E001-master-v2.mp4",
            "nom_voix": "<Chaine>-E001-master-v2-voix.mp4"}
}
```
- `voix` vaut `pistes/stem-voix.wav` par défaut ; `mix` est facultatif (exigé seulement hors `--voix-seule`).
- `marque` : pièces placées après une séquence (`apres`), noirs en secondes ; `outro` à la fin. Identifiant `noir` réservé.
- `fondus` : images de chevauchement entre deux segments qui se suivent (`"A>B"`).
- `nom_voix` : facultatif (défaut : `nom` suivi de `-voix`).
- Sorties : `NOM.mp4`, `NOM.mix.wav` ou `NOM.voix.wav`, `NOM.log.txt`, `NOM.journal.json`.

## `plan-son.json`
Un départ s'écrit en temps du film (`412.5`) ou en temps local d'une séquence (`{"seq": "seq3", "t": 12.5}`), converti par le journal (les fondus sont comptés). Chemins des sons : relatifs à `racine` (elle-même relative à la racine de la chaîne).
```json
{
 "racine": "marque/son",
 "baisse_sous_voix_db": 4.0,
 "niveaux_par_type": {"souffle": -12, "impact": -8, "montee": -12, "declic": -14,
                      "ambiance": {"lu": -20, "baisse_db": 10}},
 "silences": [{"debut": {"seq": "seq3", "t": 6.0}, "fin": {"seq": "seq3", "t": 9.0}, "raison": "la phrase seule"}],
 "musique": [
  {"fichier": "musique/<fichier-musique>.mp3", "depart": {"seq": "seq2", "t": 70.0}, "fin": {"seq": "seq3", "t": 20.0},
   "decalage": 0.0, "boucle": [4.0, 28.0], "fondu_boucle": 0.05, "fondu_entree": 2.0, "fondu_sortie": 2.0, "niveau_lu": -8.0}
 ],
 "effets": [
  {"fichier": "effets/<fichier-effet>.mp3", "depart": {"seq": "seq1", "t": 19.57}, "type": "declic",
   "extrait": [0.08, 1.0]}
 ],
 "titre": "…",
 "sortie": {"dossier": "episodes/episode-001/outputs", "nom": "<Chaine>-E001-master-v2.mp4"}
}
```
- Musique : `duree` ou `fin` ; `decalage` = départ dans la source ; `boucle` = [début, fin] dans la source (en secondes, de préférence sur des mesures entières du relevé musical), retour avec un fondu linéaire de `fondu_boucle` pris avant le point de boucle ; `niveau_lu` = sonie intégrée du départ par rapport à celle de la voix (règle par défaut : musique de 7 à 9 LU sous la voix, mesurée, `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 2 ; la valeur s'applique avant la baisse, l'écart réel se mesure : skill `studio-faceless:direction-sonore`, `references/musique-par-cues.md` § 4) ; `baisse_db` facultatif (défaut : `baisse_sous_voix_db`).
- Effets : `type` obligatoire, pris dans `niveaux_par_type` (un nombre en LU, ou `{"lu", "baisse_db"}`) ; `extrait`, `fondu_entree` (0,008 s) et `fondu_sortie` (0,10 s) facultatifs.
- Creux (facultatifs, ajoutés le 25/10/2026 pour l'E008 d'AA, à la demande du propriétaire : « arrêt brutal de son et musique ») : `"creux": [{"debut": …, "fin": …, "baisse_db": 8, "rampe": 0.8, "raison": "…"}]`. La musique seule baisse de `baisse_db` dB sur la fenêtre, avec des rampes en cosinus de `rampe` s au dehors ; les effets restent. Sans cette clé, le mix est identique à avant (vérifié sur le plan E008 v1 d'AA : −16,1 LUFS, −2,0 dBTP, LRA 6,0).
- Silences voulus : musique et effets coupés dans la fenêtre (rampes de 50 ms au dehors) ; un effet qui y commence est retiré. Le journal signale chaque coupe, les musiques qui traversent une jonction et celles qui chevauchent une pièce de marque.

## Mesures
- La voix est la référence : sonie intégrée (BS.1770) des seules séquences. Le journal donne aussi la sonie de la voix par séquence et l'écart entre séquences (mesuré, non corrigé).
- Musique : gain = voix + `niveau_lu` − sonie intégrée du départ ; baisse sous la voix active par l'enveloppe RMS de la voix (10 ms, seuil −42 dBFS, 80 ms / 400 ms, remontée dans les pauses ≥ 0,25 s), comme le gabarit `mix.py`.
- Effets : gain = voix + niveau du type − sonie momentanée maximale (400 ms) de l'extrait.
- Gain final unique vers `mix.film_lufs_cible` (`seuils.json`), mesuré sur les séquences ; signature et outro gardent leur niveau d'origine (comme au master E007 v1 d'AA) ; limiteur de crêtes vraies à `mix.limiteur_dbtp`, repris de l'assembleur.
- Après le mix, `mesurer_mix.py` (1.1.2) mesure le résidu (mix ÷ gain final − voix) : écart voix − musique par cue (fenêtres de 3 s, voix active), hausse de chaque marque (fenêtres de 0,4 s), contrôle de la chaîne de mesure ; méthode : skill `studio-faceless:direction-sonore`, `references/musique-par-cues.md` § 4. Éprouvé sur les mix v1 et v2 de l'E011 d'AA (mêmes médianes et même pire décile que la mesure faite à la main). Il ne valide rien.
- Contrôles du MP4 mixé : images en même nombre et flux vidéo identique (MD5) à l'entrée, `mix.film_lufs_cible` ± `mix.film_lufs_tolerance`, crête vraie ≤ `mix.film_crete_vraie_max_dbtp`, décodage complet. Claude n'écoute pas : le master reste `ECOUTE_A_FAIRE`.

## Limites
- Format fixe : 1920 × 1080, 30 i/s, 48 kHz stéréo. L'image est encodée une seule fois, par l'assembleur (libx264 slow, CRF 16).
- `--voix-seule` n'applique aucun gain : le film « voix » sort au niveau des pistes (un peu sous la cible du film, mesuré à l'E007 d'AA). Limiteur seulement au-delà de `mix.limiteur_dbtp`.
- Les séquences sorties du gabarit portent encore le gain de leur `mix.py` : les voix diffèrent un peu d'une séquence à l'autre (mesuré au journal du mix, non corrigé).
- Effets très courts (< 0,4 s) : la sonie momentanée est moyennée sur 400 ms, donc ils ressortent un peu plus fort que leur type ne le dit.
- Pas de balance, d'égalisation ni de creux 1–4 kHz dans `mix_film.py` (le creux reste « seulement si nécessaire », § 3).
- Une musique qui chevauche une pièce de marque n'est que signalée ; le gain final ne s'applique pas sous la marque.
- Mémoire : environ 2 à 3 Go pour un film de 9 min (son en mémoire, limiteur échantillon par échantillon).
- `srt.py` : titres `## seqN` et blocs ```` ```text ````, texte identique à la prise ; débuts lus au centième de seconde dans le `.log.txt` (±5 ms) ; la règle « 1 à 7 s » cède devant « aucun chevauchement » (un sous-titre de 0,92 s dans l'E007 d'AA).
