# Outils des shorts

Scripts de préparation et de finition des shorts, écrits par Claude du 19 au 20/10/2026 (shorts des E001, E003 et E004 d'AA), copiés ici le 21/10/2026 à la demande du propriétaire. Méthode : skill `studio-faceless:shorts` ; règles par défaut : `${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` § 5 (Shorts), sauf écart de la chaîne dans `direction/ECARTS.md`.

Tous se lancent avec `python -I -B` et refusent d'écraser une sortie existante. `voix_short.py`, `recaler.py` et `raccord.py` importent `../controle/ralentir.py` (chemin relatif au script).

| Script | Rôle | Usage |
|---|---|---|
| `voix_short.py` | Bande voix d'un short : tête et queue resserrées, pauses plafonnées, bloc D retiré pour la version YouTube (DEBUT et FIN dans des silences), −19 LUFS, crête −2 dBTP, contrôle des recopies | `voix_short.py PRISE SORTIE.wav [--sans-d DEBUT FIN] [--plafond 0.35]` |
| `recaler.py` | Repères mot à mot recalés sur les vrais départs de la voix, à partir des mots de `controle/transcrire.py` | `recaler.py BANDE.wav MOTS_WHISPER.json PREFIXE` |
| `raccord.py` | Insère une phrase régénérée dans une prise, entre deux coupes prises au milieu des silences | `raccord.py PRISE RACCORD SORTIE.wav COUPE_A COUPE_B [--marge 0.27]` |
| `master_short.py` | Master du MP4 rendu : `shorts.master_lufs`, limiteur à `shorts.limiteur_dbtp`, crête vraie ≤ `shorts.crete_vraie_max_dbtp` dans le MP4 livré (`seuils.json`) ; image copiée sans réencodage | `master_short.py ENTREE.mp4 SORTIE.mp4 [--cible LUFS] [--plafond dBTP]` |
| `mixkit_liste.py` | Liste id, titre et lien des clips d'une page de recherche Mixkit enregistrée | `mixkit_liste.py PAGE.html` |
| `pexels_fichiers.py` | Lit l'auteur et les fichiers vidéo d'une page Pexels enregistrée (`__NEXT_DATA__`) | `pexels_fichiers.py PAGE.html` |

**Après `recaler.py`**, chercher les phrases qui se chevauchent ou les mots de durée nulle : un mot mal entendu par Whisper peut décaler toute une phrase. Corriger à la main et noter la correction dans le JSON (champ `correction`). Une correction de la bande longue ne vaut pas forcément pour la bande YouTube.
