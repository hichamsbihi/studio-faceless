# Transitions, relations son-image et silences

## 1. Relations son-image
Choisir une relation par moment, en fonction de ce que le spectateur doit comprendre :

| Relation | Effet | Usage typique |
|---|---|---|
| Synchrone | Le son tombe avec l'image | Contact visible, document qui apparaît |
| Anticipation (J-cut) | Le son du plan suivant arrive avant l'image | Faire entrer dans un lieu ou une époque avant de le montrer |
| Traîne (L-cut) | Le son du plan précédent déborde sur la nouvelle image | Garder une phrase ou une émotion pendant que l'image apporte la preuve |
| Pont | Un même son relie deux images qui ne se raccordent pas | Ambiance ou souffle continu entre deux archives d'origines différentes |
| Révélation par retrait | L'ambiance baisse et laisse entendre un petit son | Isoler un détail ou un instant décisif |
| Substitution | Le son attendu est remplacé par du silence ou un détail | Après un événement fort, sans dramatiser |
| Contradiction | Le son contredit l'image | À manier rarement, jamais pour orienter le jugement sur une personne réelle |

- **Synchroniser sur les phrases et les changements d'idée, pas sur chaque coupe.** Trop de points de synchro rendent le son mécanique.
- Un raccord porté par le son ne doit pas fabriquer une continuité fausse : un pont relie deux images, il n'affirme pas qu'elles viennent du même lieu ou du même moment. Le statut de chaque ambiance reste consigné.

## 2. J-cut, L-cut, ponts : méthode
- **J-cut** : faire entrer la prochaine idée, le prochain lieu ou la prochaine énergie avant l'image. Exemple AA : l'ambiance d'une tribune (enregistrement contextuel) monte sous la fin d'un plan calme, puis l'image du stade arrive.
- **L-cut** : prolonger une voix, une citation ou une ambiance sur les images qui en apportent la preuve. Exemple : une citation sourcée continue pendant que l'image passe au document qui l'atteste.
- **Pont sonore** : ambiance, souffle, room tone ou motif sonore répété pour relier deux plans sans rapport visuel.
- **Continuité** : pas de trou d'ambiance ni de saut brusque de room tone. Un trou sonore se remarque souvent plus qu'un raccord image imparfait. Chaque lit a une entrée et une sortie propres (fondus courts, sans clic).
- Décalage habituel d'un J-cut ou d'un L-cut : de quelques images à une ou deux secondes selon le débit de la voix. Le caler sur une respiration de la prise, jamais en déplaçant ou en coupant un mot (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 2 ; écarts de la chaîne : `direction/ECARTS.md`).

## 3. Silence et quasi-silence
Le silence sert à : créer l'attente, isoler une phrase, agrandir un événement par contraste, marquer un choc, laisser respirer une matière difficile, finir sans fausse résolution.
- Préférer un **quasi-silence** (room tone, résidu d'ambiance) au zéro numérique, qui sonne comme une panne.
- Un silence voulu figure dans la feuille de repérage avec sa raison.
- Après un moment fort ou une citation difficile, laisser une respiration sans musique avant de relancer.
- Contraste avant un moment fort : réduire les couches concurrentes juste avant, plutôt qu'ajouter un impact.

## 4. Mise en œuvre dans HyperFrames 0.8.149 : constats complémentaires
Ces points complètent `hyperframes-audio` et la section HyperFrames de `DIRECTION_AUDIO.md`. Ils viennent d'une lecture du code installé le 14/10/2026, sans test de rendu : les vérifier sur le MP4 au premier usage. Depuis le 24/10/2026 (validé sur AA), la séquence ne porte que la voix : les techniques de cette référence s'appliquent au mix du film (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 3, `outils/montage/mix_film.py`), pas dans la composition de la séquence.
- **J-cut et L-cut** : il n'y a pas d'attribut dédié. Placer des `<audio>` distincts, chacun avec un `id`, son `data-start` et son `data-media-start`, sous des `<video>` en `muted`. Les fondus croisés se font par chevauchement et automation de volume, en valeurs absolues.
- **Pas de panoramique ni de spatialisation dans le moteur** (aucun nœud stéréo ni effet « pan »). Une position gauche/droite ou un élargissement se prépare **avant**, dans FFmpeg (`pan`, `stereotools`, `adelay` par canal), en stems séparés.
- **Automatisable** : volume, fréquences des filtres passe-bas et passe-haut, `wet`/`dry` de la réverbération, débit (`rate`). **Non automatisables** : compresseur, limiteur, true peak, gate, bitcrush ; automatiser un gain placé avant eux.
- La première valeur d'une automation s'applique aussi avant son premier point : poser un point explicite au temps 0 du clip.
- Une chaîne d'effets illisible fait refuser le mix au rendu, et une piste qui vise un nœud absent est supprimée sans message : **mesurer le MP4 livré** à chaque fois (`controle-et-mesure.md`).
