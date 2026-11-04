# Domaine : sport

Règles communes aux chaînes de sport. Elles remplacent les règles par défaut du plugin (`${CLAUDE_PLUGIN_ROOT}/referentiels/`) ; un écart de la chaîne (`direction/ECARTS.md`) les remplace. Elles viennent d'Apparently Athletic (StudioV1), versées au plugin 0.2.0 le 30/10/2026 (tableau de passage de StudioV1, M05 et M49 à M57 ; VALIDÉ, Hicham, 30/10/2026). Les dix fiches au vocabulaire sportif du `MOTION_CATALOG.md` restent dans le catalogue du plugin (décision 1 du 28/10/2026, reconfirmée le 30/10/2026).

## Sources primaires
- Pour les faits : club, ligue, instance, presse datée, revue scientifique avec DOI vérifié sur Crossref. Pour les médias : sites de club et Wikimedia Commons (validé sur AA).

## Droits des images (remplacent ou précisent `REFERENTIEL_QUALITE_REALISATION.md` § 2 bis)
- **Vraies vidéos de match** : un vrai moment de match se montre en vraie vidéo, jamais en animation ; l'animation sert à expliquer. Compétitions admises par défaut : Mondial (FIFA), CAN (CAF), compétitions de l'UEFA, Premier League (validé sur AA, 28/10/2026, Q23 et Q24 de l'E010, après les exceptions de l'E008 et de l'E009). Le risque de réclamation Content ID est assumé par le propriétaire ; chaque chaîne confirme ou réduit cette liste dans ses écarts.
- **Vraie photo d'un moment de match** (validé sur AA, 04/11/2026) : seules la caméra et les annotations qui expliquent (anneaux, flèches) bougent, et aucun athlète n'est détouré ni décollé de la photo. Le détourage en calque sert aux portraits et aux lieux. Jamais un corps qui bouge.
- **Logos** : clubs, instances, compétitions, trophées (Ballon d'Or), médias cités, avec mesure : un ou deux par passage, seulement s'ils aident (validé sur AA, 28/10/2026, Q69 de l'E010).
- **Vidéos libres génériques** : permises, jamais présentées comme le match ou le club précis ; aucune vidéo générée par IA (validé sur AA, 19/10/2026).
- **Licences à signaler au contrôle** : `BY-SA`, `PD-AR`, `PD-Brazil`, `BY 2.0 BR`, domaine public argentin (liste `LICENCES_EN_ATTENTE` de `outils/controle/controle.py`, constituée sur AA).

## Risques et pièges de faits
- Ne pas confondre les objets : la Ligue des champions n'est pas un titre de champion national, la Coupe d'Italie n'est pas le scudetto, une demi-finale n'est pas une finale ; la légende dit exactement ce que montre la photo (validé sur AA).

## Son (complète `DIRECTION_AUDIO.md` et le skill `studio-faceless:direction-sonore`)
- **Son des extraits de match** : le vrai son d'un extrait passe sous la voix plutôt qu'une foule de bibliothèque ; on le transcrit d'abord. S'il porte un commentaire, fréquent sur les vidéos de la FIFA, de l'UEFA ou des chaînes de compétition, on ne l'emploie pas : une ambiance de stade de `marque/son/` le remplace, et la description dit « Crowd sounds are illustrative » (validé sur AA, 26/10/2026 ; nuance du 28/10/2026, Q70 de l'E009).
- **Matières** : gazon : appuis mats, peu d'aigus ; béton : attaque sèche, réflexions dures ; tribune métallique : résonance et cliquetis ; filet : frottement bref et souple ; cuir d'un ballon frappé : impact court, médium, sans « boom » ; le son d'une action se cale sur le contact visible (pied, ballon, filet).
- **Refus** : jamais de faux commentaire sportif ; jamais l'ambiance d'un autre stade ou d'un autre match présentée comme le son de l'événement (toujours « enregistrement contextuel » ou « génération illustrative »).

## Veille et analyse
- Grilles Gemini du skill `studio-faceless:regarder` : `grille-sport-v1` (fiche, promesse et emballage, accroche, personnages, structure, relances, émotion, image, son, fin) et `grille-sport-v2-retention` (étude de rétention du 23/10/2026, mesures finales comparables).
