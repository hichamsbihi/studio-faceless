# Chantier 0.3.0, partie « règles » : suivi du versement (PROPOSÉ)

Source : relevés validés de StudioV2 (Maps & Means, MM), `direction/migration/MIGRATION_A_direction_2026-10-30.md` (A01 à A70) et `MIGRATION_B_outils_2026-10-30.md` (B01 à B46) ; décisions VALIDÉES par Hicham le 30/10/2026. Les règles versées portent le tampon « (validé sur MM, date ; proposé au plugin 0.3.0, PROPOSÉ) ». Plugin : `plugins/studio-faceless/` (P). Version et `CHANGELOG.md` : au Studio Director. Rien n'est commité.

Format : n° du relevé → fichier § du plugin → nouveau / complété / déjà présent.

## Domaine `geo-economie` (nouveau, décision 1)
| Relevé | Destination | Statut |
|---|---|---|
| A43 (aucun conseil d'investissement, avertissement mot pour mot) | `domaines/geo-economie/DOMAINE.md` § Risques et pièges de faits | nouveau |
| A44 (neutralité géopolitique) | idem | nouveau |
| A45 (sources de données et de médias) | idem § Sources primaires, § Droits des images | nouveau |
| A46 (grammaire des cartes) | idem § Cartes | nouveau |
| A47 (quel traitement pour quel besoin) | idem § Cartes | nouveau |
| A49 (pièges de chiffres : ratio avant 2 min, montant au titre) | idem § Risques et pièges de faits | nouveau |
| B10 (cartes comme décor, fonds calculés à l'avance, tuiles jamais en ligne, imagerie non commerciale exclue, MapLibre non vérifié au rendu) | idem § Cartes, Fabrication | nouveau |
| B11 (chaîne des cartes : renvoi aux modèles) | idem § Cartes, Fabrication (renvoi à `outils/cartes/` et `domaines/geo-economie/cartes/`) | nouveau |
| B12 (calque 360°) | idem § Cartes, Fabrication (renvoi à `outils/medias/calque360.py`) | nouveau |
| B13 (miniature « carte-repère », accroche « carte qu'on croit connaître », fonds réemployés) | idem § Veille et analyse | nouveau |
| B22 (neutralité : chiffres contestés, sources partisanes, noms concurrents) | idem § Sources primaires | nouveau |
| B23 (avertissement mot pour mot) | idem § Risques et pièges de faits | nouveau |
| B26 (mot géographique exact) | idem § Risques et pièges de faits | nouveau |
| — | `domaines/README.md` : ligne `geo-economie` au tableau | nouveau |

## Règles générales
| Relevé | Destination | Statut |
|---|---|---|
| A22 evergreen | `referentiels/METHODE_RECIT.md` § 6 ; renvoi `skills/episode/references/etapes.md` § 3 | nouveau |
| A23 date de valeur, revérification la veille de la voix, incertitude à l'écran | `referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2 ; `etapes.md` § 3 | complété (le plugin disait « source » seulement) |
| A24 page `STRUCTURE-vN` validée | `etapes.md` § 2 | nouveau |
| A24 maquette et test de décrochage | `etapes.md` § 5 bis ; `grilles.md` § 5 bis ; `skills/episode/SKILL.md` (ligne 5 bis du tableau) | nouveau |
| A24 relevé de rétention de la 1re minute | `etapes.md` § 13 | complété (le plugin relevait 0:30, 1:00, 2:00) |
| A25 validation par blocs, « explique-moi » | `REGLES_STUDIO.md` § Règles permanentes | nouveau |
| A25 liste unique de téléchargements | `REGLES_STUDIO.md` § Règles permanentes | complété (`socle.md` § 4 avait la liste par lot, sans le principe) |
| A51 lignes de source relues avant `render.sh` | `REFERENTIEL_QUALITE_REALISATION.md` § 4 A | nouveau |
| A51 aucune clé avant sa valeur | idem § 4 B | nouveau |
| A51 aucun cadre ne naît vide | idem § 4 B | complété (recette v3, `production.md` § 1 et `pieges.md` § Image avaient les cadres vides) |
| A52 raccord par noircissement vers la signature | idem § 2 ter ; renvoi `etapes.md` § 2 | nouveau |
| A53 agrandissement limité à 1,3 fois | `pieges.md` § Image | complété (conflit signalé avec 1,6 de `production.md` § 1) |
| A54 limiteur propre à une piste remontée seule | `referentiels/DIRECTION_AUDIO.md` § 3 ; renvoi `rendu-collage.md` § 4 | nouveau |
| A55 vidéo HDR cachée, `--sdr` | `pieges.md` § Technique | nouveau |
| A56 `scale()` animé et mode de capture | `pieges.md` § Technique | complété (`REFERENTIEL` § 2 ter avait « texte posé immobile » et la cause du flou et de `--workers 2`) |
| A56 une seule composition racine, polices système remplacées, TIFF, faux « occluded », `mask` animé | `pieges.md` § Technique | nouveau |
| A57 planches de repérage, instant de coupe | `pieges.md` § Médias | nouveau |
| A58 Wikimedia (API 50 pages, vignettes, User-Agent, backoff, SHA-1) | `pieges.md` § Médias | complété (le plugin avait « 429 » et les 50 pages dans `agents/research.md`) |
| A58 Pexels (Cloudflare), Mixkit (`videoRestricted`) | `agents/research.md` (déjà là) ; renvoi `pieges.md` § Médias | déjà présent |
| A59 envois cachés, installations par Node, `--describe false`, télémétrie | `referentiels/REGLES_DETAIL.md` § Moteur et outils | nouveau (le hook refuse déjà les installations npm) |
| A60 vidIQ en lecture seule, 5 crédits, `channel_stats`, requêtes courtes, formats mêlés | `skills/episode/references/choix-sujet.md` § 4 | complété |
| A61 PDF illisibles par l'agent, `pdftexte.py` | `pieges.md` § Recherche (nouvelle section) | nouveau |
| A62 poste sans GPU NVIDIA, sans Pillow, heure lue avec `date` | `REGLES_DETAIL.md` § Moteur et outils | nouveau |
| A63 concurrence du titre, titre tardif, miniature fournie | `etapes.md` § 12 | nouveau |
| B28 objet `RACCORD` unique pour les objets qui reviennent | `skills/episode/references/socle.md` § 7 | complété |
| B03 perspective isométrique CSS à 26,57° | `pieges.md` § Technique | nouveau |
| B40 `--sdr` et garde HDR (gabarit v4) | règle dans `pieges.md` (A55) ; gabarit : hors périmètre (`templates/`) | règle nouvelle, gabarit à l'autre agent |
| B22 Wikimedia (SHA-1, FlickreviewR), Openverse, légendes Flickr | `agents/research.md` (déjà là) | déjà présent |
| A66 (leçons de V2 déjà au plugin : automation de volume absolue, `-g 15`, horodatage des mots, cache des sous-agents, vérification d'un sous-agent, suppression récursive) | `REGLES_DETAIL.md`, `pieges.md`, `DIRECTION_AUDIO.md`, `tokens-contexte.md` | déjà présent |
| A64, A65 (DA, REF de V2 déjà au plugin) | référentiels | déjà présent |
| B01 `remove-background` | `skills/remove-background/` | déjà présent (0.2.1) |

## Lignes « pour toutes les chaînes » non versées, avec la raison
- **A63, partie `skills/youtube-seo` et `skills/thumbnail-strategist`** : ces skills sont hors du périmètre de cette passe ; la règle est écrite dans `etapes.md` § 12, à reporter dans les deux skills si le Studio Director le veut.
- **A55, gabarit `--sdr`** (B40) : `templates/sequence-gabarit-v3/` est à l'autre agent (il porte déjà une garde HDR dans `render.sh`).
- **A61, côté `agents/research.md`** : la règle est dans `pieges.md` § Recherche ; l'agent n'a pas été modifié (hors périmètre).
- **A59, côté garde-fou** : `hooks/` hors périmètre ; seule la règle écrite est versée.
- **B44 `relire.py`** (consigne de relecture par Gemini) : outil, à l'autre agent ; la consigne de `mm-regarder` n'est pas versée au skill `regarder` (hors périmètre).
- **B03 `skills/dessin-pro`** (références de dessin et règles générales du `SKILL.md`) : hors périmètre ; seule la règle isométrique est versée à `pieges.md`.
- **AP 8.2 « trois propositions pour toute décision créative »** : n'est pas dans A25 du relevé ; elle reste seulement dans `grilles.md` § 12.
- **A38 (fiche POSE-REPRISE, parade aux crans d'un pixel)** et **B12 (fiche `calque360` au `MOTION_CATALOG.md`)** : décision de catalogue non demandée ; non versées.

## Non versé par décision (propre à la chaîne)
Conflits et écarts gardés par la décision 3 : voix 1,00 et pauses (A31, A32), flou interdit (A27), sans GSAP (B33), liberté de style (A33), durée de 9 à 12 min (A19), miniature « grand texte » (B29), archivage MM (B46). Médias : la décision 4 aligne la chaîne sur `REFERENTIEL_QUALITE_REALISATION.md` § 2 bis, sans changement. A50 (sources de données propres à la Suisse et aux États-Unis) reste en chaîne (recommandation de la Q1).
