# Le socle de l'épisode (étape 5)

Le kit se construit **une seule fois**, dans `episodes/<id>/kit/`, avant le premier producteur. Toute pièce manquante au lancement donne des contre-exemples et des corrections répétées (exemple AA : E007 v1 et v2).

Les règles citées (`REFERENTIEL`, `DIRECTION_AUDIO`) sont les règles par défaut du plugin (`${CLAUDE_PLUGIN_ROOT}/referentiels/`) ; les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent.

## 1. Gabarit
- Le gabarit de séquence v3 (`${CLAUDE_PLUGIN_ROOT}/templates/sequence-gabarit-v3/`) est en voix seule : ni musique ni effets dans la séquence, et un tableau des effets proposés dans son README. Il se copie dans `kit/gabarit/`.
- La palette de l'épisode se règle en variables. La base fixe vient de la marque (`marque/README.md`).

## 2. Voix
Bandes montage et repères mot à mot recalés dans `kit/voix/`, avec leur README (durée de chaque bande, silences S1…). La voix est figée.

## 3. Direction artistique
- Une page courte :
  - un motif matériel tiré des vraies photos (pas une liste) ;
  - un monde et une transition par partie ;
  - trois moments à réussir par séquence ;
  - les quotas des effets rares.
- Planche de test validée par le propriétaire. `studio-faceless:art-director` seulement à sa demande.
- La recette v3 (`production.md` § 1) s'applique d'office.

## 4. Médias
1. **Recherche** (`studio-faceless:research`, sans téléchargement), pour chaque moment de la voix : la meilleure image du moment, gratuite et sans filigrane, avec sa source. Deux candidats au plus par moment. Vraies vidéos d'événements permises (compétitions et instances admises : `direction/ECARTS.md`) et fichiers tirés de YouTube permis en HD quand c'est nécessaire (validé sur AA, 28/10/2026) ; extraits vidéo de 6 s au plus (`REFERENTIEL` § 2 bis).
2. **Liste de téléchargement** validée par le propriétaire (`kit/DEMANDE_TELECHARGEMENTS_vN.md`, et sa forme JSON pour l'outil) :
   - pour chaque fichier, le lien de la page ou du fichier, le nom imposé, la taille et le rôle dans la scène ; une liste unique, **un seul accord** du propriétaire avant tout téléchargement (`REGLES_DETAIL.md`) ;
   - un dossier de dépôt créé à l'avance (`kit/media/source-vN/`, dont `manuel/` pour ce que Claude ne peut pas prendre).
   - **Téléchargement** (validé sur AA, 02/11/2026 ; `REFERENTIEL` § 2 bis) : Claude lance `${CLAUDE_PLUGIN_ROOT}/outils/medias/telecharger_medias.py`, ou en charge `studio-faceless:media-fetcher` par un contrat de mission ; aperçu d'abord, puis `--executer`. L'outil rend un manifeste (réf., fichier, SHA-1, taille, statut). Un fichier refusé (Cloudflare, accès payant, connexion, 429 persistant) va à la liste « à télécharger par le propriétaire » (`manuel/`), sans contournement.
3. **Vérification du dépôt** par Claude (téléchargé par l'outil ou déposé à la main) :
   - les SHA-1, comparés à ceux de Commons quand l'API les donne ;
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
- Puisés dans `marque/son/` (son catalogue et son README), copiés dans `kit/media/audio/musique/` et `sfx/`.
- Aucun appel à ElevenLabs sans demande du propriétaire ; un son neuf approuvé rejoint ensuite la bibliothèque.
- **Sons de Soundza** (bibliothèque en ligne, gratuite ; validé sur AA, 02/11/2026) : sur demande ou accord du propriétaire, après la bibliothèque de la chaîne. Recherche et téléchargement de la liste validée par Claude principal ou, depuis la 0.7.0, par `studio-faceless:sound-manager` (serveur MCP `soundza`, clé `SOUNDZA_API_KEY` dans l'environnement, jamais écrite), dans `kit/media/source-vN/soundza/`, deux candidats au plus par besoin ; **contrôle** par `outils/controle/mesurer_sons.py` (format, canaux, niveau, crête vraie, boucle, parole par Whisper), puis écoute du propriétaire. Licence, sons faits par IA, crédit et **dépôt privé** : `DIRECTION_AUDIO.md` § 4 bis. `generate_sound` jamais sans demande du propriétaire.
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
  - ce qu'on fait, moment par moment, avec la voix (temps, mots, image, transformation) ;
  - les passages d'explication marqués : dessin, carte ou schéma ;
  - les chiffres-cibles ;
  - les effets proposés ;
  - la sortie.
