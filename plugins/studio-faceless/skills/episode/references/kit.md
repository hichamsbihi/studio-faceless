# Le kit de l'épisode (étape 5)

Depuis la 1.1.0 (point 4, validé sur AA, 04/11/2026), l'étape 5 s'appelle « kit » ; « socle » ne désigne plus que la séance du propriétaire (`SOCLE.md`). Le kit se construit **une seule fois**, dans `episodes/<id>/kit/`, après le socle et avant le premier producteur, sur les seuls accords du socle. Toute pièce manquante au lancement donne des contre-exemples et des corrections répétées (exemple AA : E007 v1 et v2).

Les règles citées (`REFERENTIEL`, `DIRECTION_AUDIO`, `STYLES`) sont dans `${CLAUDE_PLUGIN_ROOT}/referentiels/` ; priorité : `REGLES_STUDIO.md` § Priorité ; valeurs chiffrées : `seuils.json`.

## 1. Gabarit
- Le gabarit de séquence v3 (`${CLAUDE_PLUGIN_ROOT}/templates/sequence-gabarit-v3/`) est en voix seule : ni musique ni effets dans la séquence, et un tableau des effets proposés dans son README. Il se copie dans `kit/gabarit/`.
- La palette de l'épisode se règle en variables. La base fixe vient de la marque (`marque/README.md`).

## 2. Voix
Bandes montage et repères mot à mot recalés dans `kit/voix/`, avec leur README (durée de chaque bande, silences S1…). La voix est figée à la fin du socle.

## 3. Direction artistique
- Une page courte :
  - un motif matériel tiré des vraies photos (pas une liste) ;
  - un monde et une transition par partie ;
  - trois moments à réussir par séquence ;
  - les quotas des effets rares.
- La fiche de style du film, accordée au socle (bloc 6 ; `STYLES.md` § Fiche de style) : l'`art-director` y a décidé le style et la technique de chaque temps fort (D02).
- La planche de test est un contrôle : les chiffres-cibles de `production.md` § 1 (`seuils.json`, clés `image.*`), mesurés dès le storyboard. `studio-faceless:art-director` la critique à la demande du propriétaire.
- La recette v3 (`production.md` § 1) s'applique d'office.

## 4. Médias
1. **Recherche** (temps « préparer », avant le socle ; `studio-faceless:research`, sans téléchargement), pour chaque moment de la voix : la meilleure image du moment, gratuite et sans filigrane, avec sa source, au plus `medias.candidats_par_moment` candidats par moment, licence et dimensions vérifiées d'avance. Vraies vidéos d'événements permises (compétitions et instances admises : `direction/ECARTS.md`) et fichiers tirés de YouTube permis en HD quand c'est nécessaire (validé sur AA, 28/10/2026) ; extraits vidéo de `medias.extrait_non_libre_s_max` s au plus (`REFERENTIEL` § 2 bis).
2. **Liste unique de téléchargement**, accordée au socle (bloc 7 ; `kit/DEMANDE_TELECHARGEMENTS_vN.md`, et sa forme JSON pour l'outil) :
   - pour chaque fichier, le lien de la page ou du fichier, le nom imposé, la taille et le rôle dans la scène ; **un seul accord** du propriétaire avant tout téléchargement (`REGLES_DETAIL.md`) ; un fichier hors de la liste est un arrêt (n° 2) ;
   - un dossier de dépôt créé à l'avance (`kit/media/source-vN/`, dont `manuel/` pour ce que Claude ne peut pas prendre).
   - **Téléchargement** (validé sur AA, 02/11/2026 ; `REFERENTIEL` § 2 bis) : Claude lance `${CLAUDE_PLUGIN_ROOT}/outils/medias/telecharger_medias.py`, ou en charge `studio-faceless:media-fetcher` par un contrat de mission ; aperçu d'abord, puis `--executer`. L'outil rend un manifeste (réf., fichier, SHA-1, taille, statut). Un fichier refusé (Cloudflare, accès payant, connexion, 429 persistant) va à la liste « à télécharger par le propriétaire » (`manuel/`), sans contournement ; s'il manque, le repli suit `REGLES_DETAIL.md` § Arrêts.
3. **Vérification du dépôt** par Claude (téléchargé par l'outil ou déposé à la main) :
   - les SHA-1, comparés à ceux de Commons quand l'API les donne, et au manifeste de la liste accordée ;
   - les dimensions ;
   - une planche de tous les fichiers, regardée : on écarte filigrane, mauvais sujet, date fausse, mineur identifiable ;
   - les conversions sans agrandissement (1920 px au plus) dans `kit/media/photos-vN/` et `logos-vN/` ;
   - une section au `kit/PROVENANCE.md` (source, auteur, licence ou « citation », SHA-1, date et lieu, remarque).
4. **Répartition** : une photo appartient à une seule séquence, sauf les rappels voulus inscrits au `BRIEF.md`. La liste des photos prises est donnée à chaque producteur.

## 5. Cartes, logos, dessins
- **Cartes** au trait : `${CLAUDE_PLUGIN_ROOT}/outils/cartes/cartes.py` (Natural Earth 1:50m, téléchargé avec l'accord du propriétaire) produit le SVG en 1920 × 1080, en `currentColor`, et les positions des villes en pixels. Une carte par lieu qui porte l'argument ; jamais de carte en décor répété.
- **Logos** : de Wikipédia ou Commons, sur la liste de téléchargement (§ 4) ; ils arrivent souvent en WebP et se convertissent en PNG. Avec mesure : un ou deux par passage, seulement s'ils aident.
- **Dessins de référence** pour les passages d'explication : extraits de compositions passées, rangés dans `kit/references-vN/` avec un README qui donne les lignes utiles. Exemple AA : le schéma de Turin de l'E003, rangé dans les archives de la chaîne.

## 6. Sons
- La fiche son est accordée au socle (bloc 8 : palette, anti-palette, extraits écoutés par le propriétaire) ; `sound-manager` y choisit les cues (D06).
- Puisés dans `marque/son/` (son catalogue et son README), copiés dans `kit/media/audio/musique/` et `sfx/`.
- Aucun appel à ElevenLabs sans demande du propriétaire ; un son neuf approuvé rejoint ensuite la bibliothèque.
- **Sons de Soundza** (bibliothèque en ligne, gratuite ; validé sur AA, 02/11/2026) : après la bibliothèque de la chaîne, sur la liste accordée au socle. Recherche et téléchargement par `studio-faceless:sound-manager` (serveur MCP `soundza`, clé dans l'environnement, jamais écrite), dans `kit/media/source-vN/soundza/`, au plus `medias.candidats_par_moment` candidats par besoin ; **contrôle** par `outils/controle/mesurer_sons.py` (format, canaux, niveau, crête vraie, boucle, parole par Whisper). Licence, sons faits par IA, crédit et **dépôt privé** : `DIRECTION_AUDIO.md` § 4 bis. `generate_sound` jamais sans demande du propriétaire.
- **Relevé musical** par morceau : tempo, boucles sur des mesures entières, silences voulus, rôle par séquence. Il servira au mix du film (`rendu-collage.md` § 4).

## 7. Raccords
- Une fiche `kit/RACCORDS.md` donne, pour chaque jonction, l'image de sortie et l'image d'entrée **au pixel** : cadre, objet, position, lumière. Elle dit aussi ce qui change exprès.
- Les lots de producteurs se composent pour qu'aucune séquence n'attende la sortie d'une autre du même lot. Sinon, on fixe d'avance l'image de jonction dans la fiche.
- **Objets qui reviennent** (validé sur MM, 28/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ) : tout objet repris d'une séquence à l'autre (un chèque, une fiche) est fixé dans le kit, position et contenu compris, avant les producteurs. Une séquence produite avant sa voisine garde ses paramètres de raccord dans un seul objet `RACCORD`. Sur le film d'origine, un chèque portait un montant alors que celui de la séquence d'avant était vierge.
- Après un rendu, on réextrait l'image de raccord, car un élément retiré (exemple AA : la grille de l'E007) a pu changer.

## 8. Consignes communes et briefs
- **Consignes communes** (`kit/CONSIGNES_COMMUNES_vN.md`) : la recette v3 adaptée au sujet, les règles de l'épisode (personnes, interdits, couleurs), les médias déjà pris, les cartes et les logos disponibles, la méthode de sortie.
- **Brief par séquence**, court (environ 3 Ko) :
  - le point de départ (gabarit, ou version précédente) ;
  - les raccords ;
  - ce qu'on garde ;
  - ce qu'on fait, moment par moment, avec la voix (temps, mots, image, transformation), dans le cadre de la fiche de style ;
  - les passages d'explication marqués : dessin, carte ou schéma ;
  - les chiffres-cibles ;
  - les effets proposés ;
  - la sortie.
