# Domaine : geo-economie

Règles communes aux chaînes de géographie de l'argent : routes, détroits, frontières, ressources et flux qui font et défont la richesse des nations. Elles remplacent les règles par défaut du plugin (`${CLAUDE_PLUGIN_ROOT}/referentiels/`) ; un écart de la chaîne (`direction/ECARTS.md`) les remplace. Elles viennent de Maps & Means (StudioV2), versées au plugin 0.3.0 le 30/10/2026 (tableaux de passage de StudioV2, A43 à A49 et B10 à B13 ; VALIDÉ, Hicham, 30/10/2026, décision 1). Ce qui reste propre à l'identité de cette chaîne (nom, voix, palette, durée de 9 à 12 min, concurrents à ne pas copier, une carte par séquence au plus, moteur de carte et direction « plein jour ») est dans ses écarts, pas ici.

## Sources primaires
- **Faits et chiffres** : institut statistique, banque centrale, organisation internationale, texte de traité ou de loi, dépôt officiel (SEC), rapport d'entreprise, presse datée, revue scientifique avec DOI vérifié sur Crossref (validé sur MM, 19/10/2026 ; B22).
- **Données** : Banque mondiale, OCDE, Eurostat, BIS, BCE, Our World in Data, banques centrales ; chaque jeu de données avec sa date de valeur (validé sur MM, 19/10/2026, A45).
- **Chiffre contesté, source partisane ou d'une partie au conflit** : signalés au rapport de recherche, avec les noms concurrents d'un lieu ou d'une frontière (validé sur MM, 19/10/2026, B22).
- **Sources que l'agent de recherche ne lit pas** : PDF, tableaux dynamiques. Le contrat de mission demande le lien et la page, marqués « non lu » ; Claude les lit lui-même (`skills/episode/references/pieges.md`, § Recherche).

## Droits des images (précisent `REFERENTIEL_QUALITE_REALISATION.md` § 2 bis, qui s'applique sans écart)
Liste de bonnes sources, jamais une obligation d'ordre ni de licence (validé sur MM, 19/10/2026 et 24/10/2026, A45) :
- **Œuvres officielles** : œuvres fédérales américaines (Maison-Blanche, Réserve fédérale, DoD/DVIDS, débats en séance du Congrès), Commission et Parlement européens avec le crédit exact demandé, contenus sous licence OGL britannique, kremlin.ru (CC BY 4.0).
- **Cartes et images de la Terre** : Natural Earth, Copernicus Sentinel, Landsat, OpenStreetMap avec sa mention (licence ODbL à signaler).
- **Si ces sources n'ont ni la personne, ni le lieu, ni l'époque** : Wikimedia Commons, Library of Congress, NARA.
- **Stock libre** (Pexels, Pixabay ; Mixkit clip par clip, jamais un clip « Restricted ») : ambiance seulement, **jamais pour montrer une personne identifiable** à propos d'un krach, d'une fraude ou de la pauvreté (validé sur MM, 19/10/2026, A45).
- **Si aucune image ne montre le fait** : motion design (cartes animées, graphiques), document primaire (dépôt SEC, communiqué de banque centrale), titre de presse cité brièvement avec sa source.

## Risques et pièges de faits
- **Aucun conseil d'investissement, aucune prédiction de cours** : jamais « acheter » ni « vendre » ; un prix ou un cours cité est un fait daté et sourcé (validé sur MM, 19/10/2026, Q5 de la feuille de route, A43 et B22).
- **Avertissement obligatoire** dans la description de chaque vidéo, en anglais, mot pour mot, jamais omis ni reformulé :
  « This video is for educational and informational purposes only and is not financial or investment advice. »
  Le contrôle de l'avertissement est dans `${CLAUDE_PLUGIN_ROOT}/outils/controle/publication.py` (validé sur MM, 19/10/2026, B23 ; à tester sur la chaîne avant la première publication).
- **Neutralité géopolitique** (validé sur MM, 19/10/2026, Q6 de la feuille de route, puis 28/10/2026, bloc 2 de l'étude E6 ; A44) :
  - ton explicatif et neutre, sans militantisme ; les intérêts et les contraintes de chaque camp ;
  - **un motif se cite, il ne se prête jamais** : on ne prête sans source ni pensée, ni intention, ni sentiment à une personne réelle, à un dirigeant ou à un État ; chaque camp reçoit son motif, avec la même grammaire ;
  - **contrepoint** : à chaque couche où une puissance agit, une phrase donne l'intérêt du camp d'en face.
- **Réfuter l'évidence par un ratio chiffré** : deux grandeurs comparées, sourcées et datées, avant 2 min. Un montant d'argent n'entre au titre que comparé à un repère connu (validé sur MM, 28/10/2026, blocs 1 et 2 de l'étude E6 ; A49).
- **Mot géographique exact** : chaque mot de la question et du titre (vallée, détroit, île, « le plus grand ») est vérifié par la recherche, sinon on choisit un mot plus juste (validé sur MM, 28/10/2026, B26 ; « valley » est devenu « corner »).
- **Date de valeur** de chaque chiffre, revérifiée la veille de la voix : règle générale, `REFERENTIEL_QUALITE_REALISATION.md` § 2.

## Cartes
Le fond de carte porte un déplacement ou une découverte, jamais un décor : un même fond clair repris d'une séquence à l'autre produit de la monotonie (validé sur MM, 23/10/2026, audit stratégique, Q22 ; B10 : cause de décrochage relevée sur le deuxième épisode).

**Grammaire** (validé sur MM, 23/10/2026, bloc 4 de l'étude E4 et blocs E et F de l'étude E5 ; A46) :
- **un fond unique par film**, qui revient toutes les 1 à 2,5 min avec **une seule couche nouvelle**, celle qui répond à la question précédente ;
- ce qui unifie les cartes : une couleur fixe par acteur, la même du début à la fin du film, une typographie d'étiquettes, une direction de lumière, une atmosphère et un étalonnage communs ;
- les passages d'un type de carte à l'autre se font **par la caméra**, sans coupe (de l'orbite au site en 10 à 15 s ; du plat au relief pour révéler) ;
- ne pas mêler trois familles de cartes dans un même film ;
- **couleurs des acteurs testées en daltonisme** : un écart ΔE minimal supérieur à 20 sous la vision normale et sous les trois simulations (protanopie, deutéranopie, tritanopie) ; au-dessous de 10, la confusion est probable. Le contexte (fond, pays non concernés) est hors du calcul et se distingue par la forme (trait fin, sans halo). Le ΔE vient d'une simulation, pas d'un test avec des spectateurs daltoniens.

**Quel traitement pour quel besoin** (validé sur MM, 23/10/2026 et 28/10/2026, A47) :

| Besoin | Traitement |
|---|---|
| Situer un lieu, montrer un terrain | satellite en relief, étiquette posée sur le lieu |
| Montrer un obstacle ou une route | survol 3D le long du relief ; carte et profil d'altitude côte à côte |
| Faire comprendre une taille | calque d'échelle : l'inconnu posé sur un territoire familier ; dans la première minute, en moins de 10 s, si le lieu central ne se situe pas d'un coup d'œil |
| Montrer un contournement | sur le fond satellite, la route existante, l'obstacle, la route de contournement, puis l'option écartée barrée |
| Réfuter l'évidence par un ratio | coût décomposé en barre ou en diagramme de Sankey, source et date à l'écran |
| Montrer un changement | couches datées, avant et après |
| Montrer l'activité économique | lumières de nuit (mêlées à une texture de jour, c'est une stylisation : la dire par la mention de source et garder la date visible) |
| Comparer des pays | choroplèthe dévoilée par strates |
| Raconter un rapport de force | pions et pastilles posés sur la voix, liens entre acteurs |
| Montrer un commerce | arcs de flux levés au-dessus du sol avec une ombre portée douce, compteurs |
| Expliquer un mécanisme | coupe d'infrastructure enchaînée depuis la carte ; 3D en gros plan |
| Écarter des solutions | options réfutées une à une sur la carte |
| Scénariser | déroulé minute par minute sur la carte |

**Fabrication** (validé sur MM, 23/10/2026, B10 à B12) :
- les fonds sont **calculés à l'avance** (ombrage, teintes, ordre des calques, étiquettes) ; aucune tuile chargée en ligne au rendu, aucun jeton de service de cartes, aucune clé ;
- la licence de chaque source d'image est lue avant usage : une imagerie à usage non commercial (exemple : l'imagerie EOX « s2cloudless 2020 ») est exclue ;
- MapLibre GL n'est pas vérifié dans le Chrome de rendu de HyperFrames (WebGL, tuiles qui arrivent en différé alors que `hf-seek` veut une image immédiate) : un essai technique précède tout emploi en direct ;
- **aucun texte dans une 3D rendue** : exporter les points projetés et poser les étiquettes en 2D ;
- références MapLibre (relief, cartographie, licence MIT) : `${CLAUDE_PLUGIN_ROOT}/domaines/geo-economie/cartes/` ; outils (projections, lecteurs de COG et de shapefile, globe, feuille papier, vols de caméra) : `${CLAUDE_PLUGIN_ROOT}/outils/cartes/`. Ce sont des **modèles issus d'un épisode** : un épisode copie ce qu'il lui faut dans son kit et l'adapte.
- calque 360° (planète et cylindre, numpy et ffmpeg) : `${CLAUDE_PLUGIN_ROOT}/outils/medias/calque360.py`, effet `expérimental` (validé sur MM, 24/10/2026, B12).

## Son
Rien de propre au domaine à ce jour : `DIRECTION_AUDIO.md` et le skill `studio-faceless:direction-sonore` s'appliquent sans changement.

## Veille et analyse
- **Miniature « carte-repère »** (validé sur MM, 28/10/2026, bloc 3 de l'étude E6 ; B13) : l'image plein cadre est la carte satellite du lieu connu, reconnaissable à sa forme, rendu du studio (Sentinel-2 ou NASA), jamais une image générée ; le lieu du paradoxe est rempli de la couleur d'accent et désigné par une flèche ; sur les trois variantes de chaque épisode, au moins une est une « carte-repère » ; elle passe les mêmes contrôles de lisibilité aux petites tailles (168 × 94 et 320 × 180), car une carte se lit moins bien qu'une photo.
- **Accroche « la carte qu'on croit connaître »** et fonds de carte réemployés d'un épisode à l'autre par région : les mosaïques déjà calculées se reprennent (validé sur MM, 28/10/2026, B13).
- **Saturation d'un sujet par vidIQ** : voir `skills/episode/references/choix-sujet.md` (requêtes courtes).
