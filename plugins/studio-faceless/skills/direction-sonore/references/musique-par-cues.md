# Musique par cues, marques et contrôle sans écoute (méthode par défaut)

**Statut** : `VALIDÉ` sur AA, 03/11/2026. Le propriétaire a approuvé à l'écoute le master v3 de l'E011, après avoir refusé les v1 et v2. C'est la règle par défaut de la musique d'un film, pour toutes les chaînes (VALIDÉ, Hicham, 03/11/2026), reprise par `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 2 et § 3. Une chaîne qui veut autre chose l'écrit en écart dans son `direction/ECARTS.md` (priorité : `REGLES_STUDIO.md` § Priorité ; valeurs : `direction/seuils.json`). Le plan et les mesures sont faits par `studio-faceless:sound-manager` ; le mix et les scripts de mesure sont lancés par Claude principal ; l'écoute revient au propriétaire.

## 1. Le constat (E011 d'AA)
- **Refus des v1 et v2** : « la musique de suspense reste trop longtemps en fond », et les révélations n'étaient pas marquées.
- **Demande** : que « l'impact sonore suive l'impact visuel ».

## 2. La recette
- **Des cues de `mix.cue_s_min` à `mix.cue_s_max` s** (`seuils.json`), chacun avec une fonction (installer, enquêter, tendre, respirer). Ils changent aux tournants du récit, pas aux coupes (`musique-a-l-image.md` § 2).
- **Un suspense de `mix.suspense_s_max` s au plus**, qui finit sur sa révélation.
- **Les protagonistes changent la musique à leur entrée.**
- **Une signature courte commune** quand la photo ou le logo d'un autre acteur arrive (exemple AA : un maillet en ré).
- **Révélation simple** : un coup tonal léger (exemple AA : un piano en ré).
- **Révélation majeure** : la musique se retire 0,5 à 1 s avant (creux, § 5), puis vient un coup du thème.
- **Questions de fin de séquence** : un court motif de question.
- **Aucun impact aux entrées de séquence.**
- **Une seule tonalité pour toute la matière.** Chaque marque remplace l'effet déjà posé sur cette image : jamais deux sons pour une même image.
- **Les sauts dans un thème se font par mesures entières** (exemple AA : 92,3 bpm, donc une mesure de 2,6 s). `decalage` et `boucle` tombent sur des multiples de la mesure.
- **Niveau** : musique mesurée entre `mix.musique_sous_voix_lu_min` et `mix.musique_sous_voix_lu_max` LU sous la voix (§ 4).

Ces marques sont tirées de la matière musicale du film, dans sa tonalité. Ce ne sont pas des « stings » de bande-annonce, que `SKILL.md` refuse.

## 3. La méthode de travail
1. **La fiche son, dans `SOCLE.md`** (bloc 8 ; point 4, validé sur AA, 04/11/2026) : palette, anti-palette et deux extraits par rôle, écoutés par le propriétaire ; puis le film entier, sans question. Après le mix, la mesure de `mesurer_mix.py` (§ 4) ; une écoute de la bande radio reste facultative et non bloquante (`REGLES_DETAIL.md` § Parcours). Il n'y a plus de séquence témoin par épisode.
2. **Plan de cues** (`montage/CUES_vN.md`) : une ligne par cue, avec :
   - l'identifiant stable (M01…) ;
   - l'entrée et la sortie (en temps de séquence) ;
   - la fonction ;
   - la source, le décalage et la mesure ;
   - les marques (type, image, son) ;
   - le niveau visé.

   Il se traduit ensuite dans le plan son JSON (`${CLAUDE_PLUGIN_ROOT}/outils/montage/README.md`).
3. **Sources** :
   - bibliothèque de la chaîne d'abord, puis Soundza si le propriétaire l'accepte (`DIRECTION_AUDIO.md` § 4 bis) ;
   - aucune musique des shows ni de l'événement, à cause de Content ID ;
   - Soundza ne garantit ni les droits ni l'absence de réclamation Content ID, et certaines de ses musiques sont générées par IA : le signaler ;
   - les téléchargements se limitent à la liste validée.

## 4. Contrôle sans écoute
Claude n'écoute pas. Ces mesures repèrent des défauts ; elles ne valident rien, et le film reste `ECOUTE_A_FAIRE`.
1. **Résidu = mix ÷ gain final − voix.**
   - Entrées : le son du mix (`NOM.mix.wav`), le gain final lu dans son journal (`NOM.log.txt`) et la voix du film (`FILM.voix.wav`), sur la même ligne de temps.
   - Hors signature et outro : ces pièces gardent leur niveau d'origine.
2. **Intensité en pondération K sur des fenêtres de 3 s** (intensité à court terme de BS.1770, sortie `S` de `ebur128`), pour le résidu et pour la voix. On ne garde que les fenêtres où la voix est active : enveloppe RMS au-dessus de −42 dBFS, seuil de `mix_film.py`.
3. **Écart voix − musique par cue** : la médiane des fenêtres du cue, entre `mix.musique_sous_voix_lu_min` et `mix.musique_sous_voix_lu_max` LU.
4. **Hausse de chaque marque** : la crête momentanée du résidu (fenêtre de 0,4 s, sortie `M`) à la marque, contre celle de la seconde d'avant ; puis son écart à la voix au même instant.
5. **Lecture** : le résidu contient aussi les réductions du limiteur sur les attaques de la voix. Elles existaient avant la musique (comparer au journal du limiteur) : ce n'est pas un défaut de la musique.

**Moyens** : `${CLAUDE_PLUGIN_ROOT}/outils/montage/mesurer_mix.py` (1.1.2) fait ce tableau, à partir du mix, du film voix et du plan son : écart par cue (une fenêtre compte si elle est entièrement en séquence et si la voix y est active une trame de 10 ms sur deux au moins), hausse des marques (effets du plan, et `--marque` pour une marque musicale du plan de cues), contrôle de la chaîne de mesure (résidu sur les passages sans musique ni effet) ; rapport sous `outputs/controle-son-vN/`. `sound-manager` le lance lui-même (rôle `ingenieur-son` du garde-fou). Éprouvé sur les mix v1 et v2 de l'E011 d'AA : il retrouve les médianes et le pire décile mesurés à la main par un script (décision du 03/11/2026) ; ses tests vérifient le résidu nul quand le mix est la voix seule.

**Défauts trouvés au premier tour de l'E011** :
- un motif de question masqué, à 0–2 dB sous la voix ;
- un cue plus fort que la règle (`mix.musique_sous_voix_lu_min` LU sous la voix au moins) ;
- des marques trop faibles.

## 5. Faits de `mix_film.py` (vérifiés sur l'E011 d'AA, 03/11/2026)
- **Gain d'une musique** = intensité de la voix + `niveau_lu` − intensité intégrée de son propre extrait, fondus compris. Un long fondu baisse cette intégrée, donc monte le gain. Le gain s'applique avant la baisse sous la voix (`episode`, `pieges.md`, E010).
- **Fondu de sortie** : il finit à `fin`.
- **Creux** : les rampes sont hors de la fenêtre. Pour un retrait 0,5 à 1 s avant une révélation, la fenêtre commence au retrait, et la rampe le précède.
- **Gain d'un effet** = voix + niveau du type − maximum momentané (400 ms) de l'extrait.
- **Aucun écrasement** : chaque remix a sa sortie neuve.
- **Journal du collage** : le `.journal.json` donne `debut_image`, un nombre d'images (30 i/s), pas des secondes.
