# Contrôle du mix livré : mesures, puis écoute

On contrôle **le MP4 exporté**, pas la composition ni un fichier intermédiaire : un codec ou une chaîne d'effets peut changer les crêtes ou supprimer une piste. Les cibles et seuils sont ceux de `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 3 et § 5, sauf écart de la chaîne dans `direction/ECARTS.md` ; ce fichier donne la méthode.

## 1. Mesures (FFmpeg 9.0.2 local, testées le 14/10/2026)
Lancer dans Git Bash. Remplacer `livre.mp4` par le fichier exact livré ; ne jamais écrire de fichier de sortie (`-f null -`).

**Format et durées**
```bash
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,profile,sample_rate,channels,bit_rate -of default=nw=1 livre.mp4
ffprobe -v error -show_entries stream=codec_type,duration -of csv=p=0 livre.mp4
```
Attendu : AAC LC, 48 kHz, stéréo, débit fixé par le moteur ; durées audio et vidéo égales.

**Loudness intégrée, plage et crête vraie**
```bash
ffmpeg -hide_banner -nostats -i livre.mp4 -map 0:a:0 -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary:/,$p'
```
Lire `I` (LUFS), `LRA` et, sous « True peak », la ligne `Peak` (FFmpeg l'affiche en dBFS ; c'est la crête vraie suréchantillonnée).

**Repli mono** (rien d'essentiel ne doit dépendre de la stéréo)
```bash
ffmpeg -hide_banner -nostats -i livre.mp4 -map 0:a:0 -af "pan=mono|c0=0.5*c0+0.5*c1,ebur128=peak=true" -f null - 2>&1 | sed -n '/Summary:/,$p'
```
Une chute de loudness nettement plus forte que celle d'un contenu centré signale des éléments très latéralisés ou en opposition de phase : écouter le passage en mono.

**Crêtes et niveaux par canal** (écrêtage, déséquilibre gauche/droite)
```bash
ffmpeg -hide_banner -nostats -i livre.mp4 -map 0:a:0 -af "astats=measure_perchannel=Peak_level+RMS_level:measure_overall=none" -f null - 2>&1 | grep -E "Channel:|Peak level|RMS level"
```

**Trous et silences numériques** (lit d'ambiance interrompu, piste supprimée sans message)
```bash
ffmpeg -hide_banner -nostats -i livre.mp4 -map 0:a:0 -af silencedetect=noise=-60dB:d=0.4 -f null - 2>&1 | grep silence_
```
Chaque silence trouvé doit correspondre à un silence voulu de la feuille de repérage.

**Voix contre reste dans la bande 1–4 kHz**
Le MP4 mélange tout : la comparaison se fait sur deux sources séparées, sur la **même fenêtre** de narration (`-ss` début, `-t` durée) : (a) la voix seule telle que placée et réglée dans le mix, (b) le reste du mix sans la voix (stem ou rendu de contrôle sans la piste voix).
```bash
ffmpeg -hide_banner -nostats -ss 12.0 -t 6.0 -i source.wav -map 0:a:0 -af "pan=mono|c0=0.5*c0+0.5*c1,highpass=f=1000,lowpass=f=4000,astats=measure_overall=RMS_level:measure_perchannel=none" -f null - 2>&1 | grep "RMS level"
```
L'écart (a − b) se compare au seuil de `DIRECTION_AUDIO.md`. Les filtres d'ordre 2 donnent une **approximation** ; sans sources séparées, écrire « non mesuré » plutôt qu'une valeur estimée.

**Mesure de contrôle de `loudnorm`** (sans normaliser)
```bash
ffmpeg -hide_banner -nostats -i livre.mp4 -map 0:a:0 -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | grep -E '"input_(i|tp|lra)"'
```
Les valeurs `I` et `TP` de cette commande reprennent les cibles de `DIRECTION_AUDIO.md` § 3 ; si elles changent là-bas, les changer ici. Normaliser un master n'est permis qu'en connaissance de cause : corriger d'abord la source, le montage et l'équilibre. Le moteur HyperFrames abaisse déjà tout le mix pour rester sous −1 dBTP.

## 2. Passes d'écoute (jugement humain)
Les mesures disent si le fichier est techniquement conforme ; elles ne disent pas si le son sert le récit. Quatre passes, dans cet ordre :
1. **Image seule, son coupé** : la progression se comprend-elle sans le son ?
2. **Son seul, écran noir** : entend-on où l'on est, quand on change de lieu ou d'idée, sans trou ni clic ? Les J-cuts et L-cuts sont-ils propres ?
3. **Texte seul** : chaque texte à l'écran correspond-il à ce qui est entendu ou sourcé ?
4. **Complet**, à vitesse normale, puis en mono et sur un petit haut-parleur ou un téléphone.

Un agent ne peut pas écouter : il prépare la note, signale les passages à risque (horodatés) et laisse le statut à `ECOUTE_A_FAIRE`. Seul le propriétaire passe un mix en `APPROUVE_PAR_<PROPRIETAIRE>`. Une transcription, une forme d'onde ou une mesure ne valent pas une écoute.

## 3. Diagnostic par symptôme
Couper et isoler les couches pour trouver la fautive avant de toucher au reste.

| Symptôme | Correction, dans l'ordre |
|---|---|
| Voix masquée | Retirer ou alléger la couche concurrente ; puis son arrangement ; puis une automation de gain ; puis un correctif de fréquence si le masquage est établi |
| Son en avance ou en retard | Recaler l'attaque sur le contact visible, à l'image près |
| Ambiance qui boucle | Boucle plus longue, fondu croisé, moins de détails répétés |
| Trou ou saut de room tone | Prolonger le lit, fondu court, vérifier la piste dans le MP4 (supprimée ?) |
| Mix fatigant | Moins de couches, des moments calmes, moins de transitions |
| Échelle fausse (trop proche, trop gros) | Revoir perspective : aigus, réverbération, gain |
| True peak trop haut | Baisser la source fautive ou la transitoire, re-rendre, re-mesurer |
| Droits ou provenance flous | Remplacer avant la version finale ; ne jamais enfouir un son non documenté dans un mix |

## 4. Note de contrôle
Gabarit : `gabarits.md`, « Note de contrôle audio ». Elle sépare toujours les mesures (avec l'outil et la commande) de l'écoute (faite ou à faire, par qui).
