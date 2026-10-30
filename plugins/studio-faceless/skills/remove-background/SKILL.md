---
name: remove-background
description: Détourage pour les séquences HyperFrames des chaînes du plugin studio-faceless — séparer un sujet réel de son fond pour le poser sur un autre fond, une carte, un dessin ou devant un texte. Deux voies — `hyperframes remove-background` (modèle local u2net_human_seg) pour une personne, un sujet vivant ou un détourage vu en petit, avec la méthode en quatre étapes ; un masque déterministe pour un objet sur fond uni vu de près, dont le bord doit rester net. Use when a producer or Claude needs a cutout, a transparent PNG or a transparent WebM for a sequence. Not for thumbnails (studio-faceless:thumbnail-strategist keeps its polygon cutout).
---

# remove-background : le détourage dans HyperFrames

**Statut** : règle générale du plugin depuis la version 0.2.1 (VALIDÉ, Hicham, 30/10/2026 : « rend remove-background général pour tout le plugin »). Skill écrit sur Maps & Means (StudioV2) le 28/10/2026, d'après la référence `media-use/audio/references/remove-background.md` des skills HyperFrames (HeyGen ; HyperFrames sous licence Apache-2.0), puis généralisé ; méthode en quatre étapes pour les personnes validée sur AA le 28/10/2026 (Q117 de l'E010). La commande est celle de HyperFrames 0.8.149 (`node_modules/hyperframes/dist/remove-background-*.js`) ; elle s'appelle avec `npx hyperframes` ou `node node_modules/hyperframes/bin/hyperframes.mjs`.

## 1. Installation (une fois par machine, avec l'accord du propriétaire)
- La première commande télécharge `onnxruntime-node` (environ 214 Mo) dans `~/.cache/hyperframes/optional/` et le modèle `u2net_human_seg.onnx` (environ 168 Mo, projet rembg) dans `~/.cache/hyperframes/background-removal/models/`. Rien n'entre dans `node_modules/` : HyperFrames reste en 0.8.149. Demander l'accord du propriétaire avant ce premier téléchargement.
- `--info` dit le matériel employé. Sur un poste sans GPU NVIDIA : toujours `--device cpu` (mémoire de pointe ≈ 1,5 Go) ; une seule commande à la fois, jamais pendant un rendu.
- Limite constatée (MM, 28/10/2026, lingot de 6 250 px sur blanc, 26 s) : le masque est calculé en basse définition puis agrandi, d'où un liseré clair d'environ 15 px au bord à pleine définition.
- Jamais un autre outil de détourage ni un service en ligne.

## 2. Choisir la voie
| Sujet | Voie | Pourquoi |
|---|---|---|
| Personne ou sujet vivant, photo ou vidéo | `hyperframes remove-background` et méthode du § 4 bis | c'est l'usage du modèle, entraîné sur des silhouettes humaines |
| Objet sur fond uni vu en petit (moins d'un tiers de l'image) | `hyperframes remove-background` (§ 4) | le liseré ne se voit pas à cette taille |
| Objet sur fond uni vu de près (poinçon d'un lingot, page sur fond clair) | masque déterministe (§ 3), ou masque du modèle recoupé par le seuil du fond | le bord reste net au pixel, sans liseré |
| Montrer un lieu « sans » la personne (fond rebouché) | aucune : interdit | il faudrait inventer des pixels (inpainting), donc une image générée |

D'abord, prendre les détourages déjà faits du kit de l'épisode (`kit/media/detourages-vN/` et son README).

## 3. Objet sur fond uni : masque déterministe
- Fait par le producteur dans son dossier de version, avec ffmpeg ou numpy (Python lancé avec `-I`) ; la source n'est jamais modifiée.
- Le masque vient du fond seulement : seuil sur la couleur du fond (blanc pur ou quasi pur), bord adouci de 1 à 2 px, aucun pixel de l'objet repeint, déplacé ni recoloré.
- Sortie : PNG avec alpha, à la définition d'origine ; vérifier l'alpha sur une planche, l'objet posé sur noir et sur blanc, avec un recadrage d'un coin à pleine définition (aucun liseré clair sur le noir).
- Les ombres et la lumière rasante se font sur le fond de la scène, jamais peintes sur l'objet.

## 4. `hyperframes remove-background`
```bash
npx hyperframes remove-background sujet.jpg -o detoure_brut.png --device cpu
npx hyperframes remove-background sujet.mp4 -o detoure.webm --quality best --device cpu
npx hyperframes remove-background --info
```
- **Sorties** : `.png` pour une image ; `.webm` (VP9 avec alpha) pour une vidéo, lu tel quel par `<video>` ; `.mov` (ProRes 4444) seulement pour un logiciel de montage.
- **Qualité** : `--quality best` pour tout ce qui part au rendu (le réglage ne change que l'encodage, pas la découpe).
- **Calque inverse** : `--background-output fond.webm` donne le fond troué à la place du sujet, pour glisser un texte entre le fond et le sujet ; le trou reste vide (rien n'est rebouché).
- **Vidéo source** : la ramener d'abord en SDR et en extrait de moins de 6 s (outil de préparation des médias de la chaîne s'il existe, sinon ffmpeg), puis détourer l'extrait.

## 4 bis. Personnes : méthode en quatre étapes (validé sur AA, 28/10/2026, Q117 de l'E010)
1. Recadrer d'abord la photo autour de la personne : le modèle détoure tous les humains de l'image.
2. Resserrer le masque de 2 px : `ffmpeg -i <nom>_brut.png -filter_complex "[0]format=rgba,split[c][a];[a]alphaextract,erosion,erosion,gblur=sigma=0.7[m];[c][m]alphamerge" <nom>.png`.
3. Une personne collée à une autre s'écarte par un polygone **multiplié** au masque du modèle ; jamais un détourage tracé seulement à la main en polygone.
4. Contrôle sur fond vert vif, en pleine taille : cheveux, mains, vêtements de la couleur du fond. Un membre perdu se coupe au cadre (aux hanches, par exemple) ; jamais de morceau flottant.

Emploi dans le film : quelques personnes clés, en couleurs réelles, posées dans les dessins, cartes et graphiques, à 45 % de la hauteur au moins (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 ter, fiche CUTOUT-FIGURE du `MOTION_CATALOG.md`).

## 5. Dans la composition
- Envelopper la vidéo détourée dans un `<div>` sans attribut `data-*` et animer l'opacité de ce conteneur, jamais celle de la vidéo : HyperFrames force `opacity: 1` sur un clip actif.
- Vidéo de fond et vidéo détourée commencent toutes deux à `data-start="0"` avec `data-media-start="0"`, et le conteneur reste caché tant que `render(t)` ne le montre pas : un départ tardif décale d'une image.
- Jamais deux prises du même sujet l'une sur l'autre.

## 6. Ce qui ne change pas
- Aucune image générée par IA : le détourage sépare des pixels réels, il n'en crée pas.
- Le détourage est un traitement : il se note dans le README de la séquence (source, voie, réglages) ; la provenance du média reste celle de `PROVENANCE.md`.
- La charte de la chaîne (`direction/ECARTS.md`, `marque/README.md`) et celle de l'épisode s'appliquent au sujet détouré comme au reste de l'image.
