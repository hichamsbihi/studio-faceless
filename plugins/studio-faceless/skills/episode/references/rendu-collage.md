# Rendus, collage, mix du film, master (étapes 8 à 10)

## 1. Rendus
- **Un rendu à la fois.** D'abord attendre la fin des rendus des autres sessions (processus `node … hyperframes.mjs … render`). Il n'y a plus de condition sur le processeur ni sur la mémoire (validé sur AA, 24/10/2026). On vérifie toutes les 5 min, 12 h au plus. Script de garde : `bash ${CLAUDE_PLUGIN_ROOT}/outils/rendu/rendre_si_libre.sh <render.sh> <journal>` (depuis la racine de la chaîne).
- **Une seule tâche suivie qui enchaîne la file**, par exemple `for q in seq6 seq2 seq7; do garde …; done` en arrière-plan suivi. Une tâche détachée (`( … &)`) ne prévient jamais.
- Arrêter un rendu : `TaskStop` ne tue pas l'enfant `node` ; il faut `taskkill //T //F //PID`.
- **Durées constatées** sur une machine libre : 7 à 16 min par séquence d'une à deux minutes. Plus de 5 h quand la machine est chargée.
- **Rendu à refaire** : on range l'ancien MP4 et sa planche de contrôle dans `_rendu-N/`, car `render.sh` refuse d'écraser.

## 2. Contrôles d'une séquence rendue
- `${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py` :
  - `tout --projet <dossier> <mp4>` : niveau, couleurs, licences, Chrome ;
  - `son --voix pistes/stem-voix.wav <mp4>` : trous, écrêtage, clics ;
  - `tremblement <mp4>` ;
  - `planche --sortie <dossier>/controle-planche --pas 4 <mp4>`.
- **Lire le tremblement** : des crans d'un pixel sur une photo qui dérive sont tolérés. Sur du texte, non. L'outil signale aussi les secondes où une coupe mêle des pas de 0 et de 1 px, même sur un glissement exact : en cas de doute, prendre 10 images de suite en snapshot.
- **La planche est regardée avant de montrer.** Statut `MESURES_TECHNIQUES_OK` ou correction sur place.
- Le son d'une séquence en voix seule n'a pas de cible de sonie. Le niveau se règle au mix du film.

## 3. Collage en voix seule
- **Outil** : `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/assembler.py --episode <id> --voix-seule` (ou un `montage.json` ; `--son-seul` mesure sans rien écrire), avec la configuration `episodes/<id>/montage/montage.json`. Testé sur AA (E007) le 24/10/2026 : 15 655 images, image identique au master v1 (même MD5 du flux), 22 min. Le README de l'outil donne le schéma : séquences, signature de la chaîne après l'accroche avec 0,5 s de noir de part et d'autre, rappel d'abonnement, outro de la chaîne (`marque/`), fondus par jonction.
- **Jonctions** : comparer la dernière image de chaque séquence à la première de la suivante (PSNR et planche des paires). Si seuls des crédits ou une plaque changent, un fondu de 4 à 6 images suffit. Si l'image saute, on corrige la séquence.
- **Contrôles** : nombre d'images attendu, journal du master (début de chaque séquence), décodage complet.

## 4. Mix du film
- **Outil** : `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/mix_film.py <film>-voix.mp4 plan-son.json [--son-seul]` (schéma du plan : `${CLAUDE_PLUGIN_ROOT}/outils/montage/README.md`). Testé sur AA (E007) : −16,1 LUFS, −1,9 dBTP, image identique, 6,5 min, environ 2 à 3 Go de mémoire. Entrées : le master voix, son journal et `episodes/<id>/montage/plan-son.json`. La sortie est le master final, dont l'image est copiée telle quelle.
- **Le plan son** (porte de questions d'abord, `grilles.md` § 10) :
  - **musique** : les départs en temps de séquence (convertis par le journal) ou en temps du film, le décalage dans la source, les boucles sur des mesures entières (relevé musical), les fondus. Une musique peut traverser une jonction. Elle se tait exprès avant une révélation ;
  - **effets** : repris des tableaux des producteurs, sans les facultatifs sauf décision, chacun avec son type ;
  - **silences voulus** : une musique ou un effet qui y tombe est coupé, et le journal le signale.
- **Niveaux de départ par type**, en LU sous la voix (validé sur AA comme départ, 24/10/2026, Q12 ; à calibrer à la première écoute du propriétaire) :

  | Type | Niveau |
  |---|---|
  | musique | 13 (plage 12 à 15) |
  | ambiance en boucle (foule, pluie) | 16 |
  | impact ou battement | 14 |
  | souffle, whoosh | 18 |
  | montée | 16, coupée avant la phrase |
  | papier, craie, surligneur, déclic | 20 |

  La baisse sous la voix active est de 3 à 5 dB (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 3 ; les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent).
- **Fin du mix** : un seul gain final vers −16 LUFS intégrés, mesuré sur les séquences ; **la signature et l'outro gardent leur niveau d'origine** (Q13, validé sur AA, 24/10/2026) ; puis un limiteur à −2,0 dBTP. Une piste remontée seule passe d'abord dans son propre limiteur (`DIRECTION_AUDIO.md` § 3). Les clics de voix sont atténués. L'écart de voix entre séquences se **mesure** et se rapporte, sans égalisation (Q14, validé sur AA, 24/10/2026).
- **Fin du film en douceur** (validé sur AA, 28/10/2026, Q71 de l'E009 ; `DIRECTION_AUDIO` § 3). Exemple AA : le dossier `montage/` de l'E009.
  - `montage.json` : fondu `"seqN>noir"` de 36 images (1,2 s), outro avec `noir_avant` 4,0, fondu `"noir>outro"` de 15 images (0,5 s).
  - `plan-son.json` : le morceau de fin part dans la dernière séquence, avec un `decalage` dans la source choisi pour que l'accord final tombe sur le noir ; `fin` `{"seq": "outro", "t": 0.5}` ; fondu d'entrée de 2 s, fondu de sortie de 0,8 s.
- **Contrôles du master** :
  - images identiques au master voix ;
  - −16 ±1 LUFS ;
  - crête vraie ≤ −1,5 dBTP ;
  - décodage complet ;
  - jointures musicales mesurées (pas de saut de niveau à une jonction) ;
  - planche du film toutes les 8 s, regardée.

  Statut : `MESURES_TECHNIQUES_OK`, puis `ECOUTE_A_FAIRE` jusqu'à ce que le propriétaire écoute.
- **Une correction de son se fait par un remix** : on modifie le plan, puis on relance `mix_film.py` vers une nouvelle sortie, sans rendu de l'image.

## 5. Sous-titres et publication
- **SRT** : `python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/montage/srt.py --script SCRIPT.md --mots "kit/voix/{seq}-montage-mots-recales.json" --journal <nom>-voix.log.txt --sortie X.srt`. Il les tire du script vérifié (blocs ```text sous `## seqN`), des mots recalés des bandes montage et du journal du collage en voix seule (celui d'`assembler.py`, dans `outputs/` ; le `.log.txt` de `mix_film.py` ne convient pas). Deux lignes de 42 caractères au plus, 1 à 7 s. Vérifier par sondage trois phrases contre le film.
- **Dossier YouTube** : skill `studio-faceless:youtube-seo` ; chapitres par `${CLAUDE_PLUGIN_ROOT}/outils/controle/publication.py chapitres`.
