# Montage vertical d'un short (1080 × 1920)

Pour `studio-faceless:shorts-producer`, et pour Claude principal au contrôle. Chiffres propres aux plateformes (marges masquées, durée, niveau sonore) : `plateformes.md`. Les règles de `${CLAUDE_PLUGIN_ROOT}/referentiels/` sont des règles par défaut : les écarts de la chaîne sont dans `direction/ECARTS.md` (priorité : `REGLES_STUDIO.md` § Priorité).

## Format
MP4 1080 × 1920, 30 i/s constants, H.264, AAC 48 kHz, sauf indication contraire du brief. Détail de l'encodage : `plateformes.md` § Master unique.

**Deux exports par short, depuis un même projet** (validé sur AA, 19/10/2026) :
- **version TikTok et Facebook** : tous les blocs, de 65 à 85 s ;
- **version YouTube** : sans le bloc D, de 35 à 50 s, **toujours sous 60 s**.

Le projet ne garde qu'**une composition racine**, la version longue. La version YouTube va dans `compositions/` (chemins en `../`) et se rend avec `-c`, en réutilisant les mêmes scènes. Le raccord C → E doit être aussi soigné qu'un raccord de film. `render.sh` produit les deux MP4.

**Aucun crédit photo à l'écran** : ils vont dans les légendes (validé sur AA, 19/10/2026).

**Zone sûre commune** : x de 120 à 840, y de 288 à 1210. Hook, sous-titres, preuve et filigrane y restent ; l'image peut déborder.

## L'image 0
- **L'image la plus forte du short, la ligne du hook et la voix démarrent à 0,0 s.**
- Ni noir, ni fondu d'entrée, ni logo animé, ni signature de la chaîne avant le hook.
- Du mouvement dès la première seconde, coupé sur la voix.

## Effet diaporama : interdit, comme dans les films
**Définition** (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2) : une suite d'images fixes traitées de la même façon (une photo ou un fond, un zoom ou un titre, un fondu, puis la même chose) pendant que la voix avance. En 9:16, on garde :
- un espace continu où les médias se posent ;
- une grammaire qui change avec le contenu ;
- jamais deux fois de suite le même traitement.

**Formule** (validé sur AA, 19/10/2026, d'après l'étude AA de la formule des shorts)  ; résumé ci-dessous des 10 règles de l'étude et de ses valeurs de caméra.
- Image 0 en mouvement.
- Un événement visuel toutes les 1,5 à 3 s, à rythme irrégulier : coupe, punch-in, whip, compteur, flèche, surlignage, écran partagé, cascade de photos.
- Poussée de 1,0 à 1,12 en 2 à 3 s ; tremblé sur les impacts ; on anime un conteneur « caméra », jamais le clip.
- Vraie vidéo quand elle illustre la phrase.
- Mot actif surligné par la couleur.
- Un effet sonore court sur chaque événement.

**Rythme** (retours du propriétaire sur la v1 du pilote AA, 19/10/2026) :
- **une image par phrase**, et jamais plus de 2,5 s sans changement d'image ;
- **pas d'écran sombre presque vide**, ni de bloc de typographie seule : les fiches et les mots clés se posent sur des photos ;
- **toutes les photos en plein cadre** (1080 × 1920, cover), pas en bandeaux ; l'image 0 aussi.

Le kit doit donc fournir assez de médias pour chaque phrase (le brief les attribue phrase par phrase).

## Recomposer pour le vertical
Un média horizontal recadré au centre perd souvent l'essentiel. Moyens, à choisir selon l'image :
- **sujet détouré** posé sur un fond aux couleurs de l'histoire ;
- **deux cadres superposés** (haut et bas) qui se répondent : avant et après, cause et effet ;
- **traversée latérale** d'une photo large, en translation ;
- **document ou donnée** recomposés en hauteur (typographie, chiffres) ;
- jamais de fond flouté du même média par facilité ;
- jamais deux fois de suite le même moyen.

## Sous-titres
- **Mot à mot**, depuis les repères du kit, par groupes de 2 ou 3 mots, **80 à 88 px** (58 px était trop petit, validé sur AA, 19/10/2026), avec une ombre ou une bande sombre pour rester lisibles sur photo.
- **Mouvement** : apparition en opacité ; **un texte posé reste immobile**. Jamais d'échelle animée ni de `filter: blur` sur un texte ou un bloc qui en contient. L'échelle fait sauter les lettres, et le flou impose une capture qui recale au pixel : même un glissement lent saccade (mesures de l'E005, 19/10/2026).
- **Lisibles sur un téléphone** : police du gabarit, fort contraste, palette de l'histoire (pas de palette « style Claude » corail, ivoire et charbon pour les titres).
- **Placement** : dans la zone visible des trois plateformes, sans couvrir un visage ni la preuve à l'image.
- La ligne du hook et les sous-titres ne se superposent pas.

## Marque
- **Filigrane discret de la chaîne** pendant tout le short (fichier, coin, taille et opacité donnés au brief, depuis `marque/README.md` § Shorts), dans une zone visible.
- **Carton final de 2 à 3 s** : logo de la chaîne, nom de la chaîne (72 px au moins), titre du film (60 px au moins) et la ligne du pont (52 px au moins), dans les couleurs de marque.

## Son
- Voix au premier plan ; bande fournie par le kit, prête (seul le gain change).
- Effets : un effet court sur chaque événement visuel, à 12 à 18 dB sous la voix ; coupes calées sur le tempo (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md`, shorts).
- Musique dès 0,0 s, **plus présente que dans les films** (validé sur AA, 19/10/2026) : dans `mix.py`, `MUS_REL` −6 et `MUS_DUCK` 2, soit environ 8 LU sous la voix (`PROPOSÉ`). Effets seulement sur un repère du brief.
- Le son du short se mixe à `shorts.mix_sequence_lufs` ; le directeur fait ensuite le master avec `${CLAUDE_PLUGIN_ROOT}/outils/shorts/master_short.py` : `shorts.master_lufs`, crête vraie ≤ `shorts.crete_vraie_max_dbtp`, limiteur à `shorts.limiteur_dbtp` (`seuils.json`).

## Contrôles
Par l'agent, avant `render.sh` :
- `check` ;
- une capture de l'image 0 en pleine taille ;
- une planche de 12 à 16 instants avec le tracé des zones masquées ; deux planches au plus.

Par Claude principal, après le rendu :
- `${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py` : `tout`, `planche`, `tremblement`, et `son` quand la voix séparée existe ;
- la capture de l'image 0 vue à la taille d'un téléphone : le hook se lit-il en moins de 1,5 s ?
- aucun texte ni visage dans les zones masquées.
