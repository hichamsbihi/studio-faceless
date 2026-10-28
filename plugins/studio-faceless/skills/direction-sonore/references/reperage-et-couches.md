# Repérage, couches et perspective

## 1. Repérage (spotting) avant tout son
Partir de l'image et de la voix approuvée, jamais d'une banque de sons. Une ligne par événement ou par lit sonore (gabarit : `gabarits.md`, « Feuille de repérage ») :

| Champ | Ce qu'on décide |
|---|---|
| Temps | Entrée et sortie, en secondes ou en images, calées sur la prise réelle. |
| Déclencheur | Ce qui motive le son : action visible, phrase de la voix, changement d'idée, raccord. |
| Famille | Voix off · son d'archive · ambiance / room tone · bruitage motivé · effet éditorial · musique · silence voulu. |
| Statut narratif | Dans le monde montré (diégétique), point d'écoute subjectif déclaré, ou ponctuation éditoriale. |
| Synchro | À l'image près, souple, sur la phrase, de fond, ou hors champ. |
| Perspective | Proche, moyenne, lointaine, occultée (derrière une paroi, à la radio, au téléphone). |
| Matière | Gazon, béton, tribune métallique, filet, cuir du ballon, foule, vent… |
| Fonction | Ce que le spectateur doit sentir, remarquer ou comprendre grâce à ce son. |
| Source et statut | Archive exacte, enregistrement contextuel, génération illustrative ; licence ; « provisoire » ou « retenu ». |
| Priorité | Premier plan, plan moyen, fond, à peine perceptible, ou coupé. |

Règles :
- **Ce n'est pas une liste de courses.** Sous une narration, chaque action visible n'appelle pas un son : on garde ceux qui clarifient une cause, rendent une matière, marquent un changement d'idée ou portent une émotion.
- Pour chaque son important, trois questions : **qu'est-ce qui le produit physiquement ? où est-il par rapport au point d'écoute ? qu'apporte-t-il au récit ?** Sans réponse à la troisième, on l'enlève.
- Le son d'une action visible se cale sur le **contact visible** (exemple AA : pied, ballon, filet), pas sur le début du fichier.
- Un événement réel sans son d'archive autorisé reste silencieux ou porté par une ambiance déclarée contextuelle. On ne fabrique pas son son « comme s'il avait été capté ».

## 2. Familles, adaptées au documentaire de la chaîne
- **Voix off** : conduit la compréhension ; aucune autre couche ne la masque. Ses règles sont dans `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 2 (les écarts de la chaîne, dans `direction/ECARTS.md`, l'emportent sur ces règles par défaut).
- **Son d'archive** : choisir qui est au premier plan quand une archive parle sous la voix ; ne pas la « nettoyer » au point d'en changer le caractère ; consigner la source exacte.
- **Ambiance et room tone** : installent le lieu et évitent le trou numérique. Construire en couches (un lit de base, quelques détails locaux, la perspective) et garder un lit très bas continu sous une scène, sauf silence voulu. Exemple AA : une ambiance de stade enregistrée ailleurs est un **enregistrement contextuel**, jamais « le son du stade X ».
- **Bruitages motivés** : seulement pour une action réellement visible et utile au récit (exemple AA : ballon frappé dans une reconstitution déclarée ; ou page tournée d'un document montré…). Deux ou trois appuis valent mieux qu'un son par geste.
- **Effet éditorial** : rare, sec, lié à un changement de sens (apparition d'un document, d'une donnée). Pas de whoosh de transition.
- **Musique** : elle porte l'immersion, choisie selon la situation (validé sur AA, 15/10/2026) ; voir `musique-a-l-image.md`.
- **Foules** : sur l'image qui les justifie, au moment exact, puis elles s'arrêtent ; jamais en fond continu.
- **Silence** : un choix de mise en scène, avec sa raison écrite ; voir `transitions-et-silences.md`.

## 3. Densité : peu de couches sous la voix
Principe de Walter Murch (« loi des deux et demi », connu par des sources secondaires) : au-delà d'environ trois sons de même nature simultanés, l'oreille cesse de les suivre séparément et perçoit une masse.
- **Pour la clarté** (passage parlé) : deux ou trois couches, par exemple voix + lit d'ambiance + éventuellement un seul autre élément.
- **Pour l'effet de masse** (une foule, une ville) : plusieurs couches de même nature fondues en un seul lit, placé derrière la voix.
- **Transitions** : une ou deux couches.
- Hiérarchie de repli quand ça se dispute : voix, puis sons-clés du récit, puis musique, puis ambiances et bruitages. Réduire d'abord la couche secondaire, puis son arrangement, puis son gain (`DIRECTION_AUDIO.md` § 3).

## 4. Perspective et distance
La perspective suit le point de vue du récit, pas l'envie d'effet.

| Perspective | Ce qu'on entend | Moyens possibles |
|---|---|---|
| Proche | Attaques nettes, détail de matière, peu de pièce | Son sec, gain présent |
| Moyenne | Réflexions naturelles du lieu, moins de micro-détail | Un peu de réverbération (wet bas) |
| Lointaine | Moins d'aigus, plus d'air, attaques adoucies, image plus étroite | Passe-bas ou baisse des aigus, wet plus haut, gain plus bas |
| Occultée | Attaque étouffée, couleur de la paroi ou du haut-parleur | Passe-bas marqué, éventuellement bande étroite (radio, téléphone) |

- Ces traitements s'appliquent aux **ambiances et effets**, jamais à la voix off ni à une parole d'archive (on ne corrige un timbre que pour un défaut identifié).
- Un changement de perspective doit être motivé par un changement de point de vue lisible à l'image (raccord, révélation, passage du détail à l'ensemble).
- Une perspective « subjective » n'est permise que dans une scène fictive ou reconstituée **déclarée**, jamais pour prêter une sensation à une personne réelle.
- Mise en œuvre dans HyperFrames : voir les constats de `transitions-et-silences.md` § 4 (pas de panoramique dans le moteur).

## 5. Matières (aide-mémoire)
- Exemple AA (football) : gazon : appuis mats, peu d'aigus ; béton : attaque sèche, réflexions dures ; tribune métallique : résonance et cliquetis ; filet : frottement bref et souple ; cuir d'un ballon frappé : impact court, médium, sans « boom ».
- Une foule lointaine est une masse sans parole intelligible ; une foule proche fait apparaître des voix. Vérifier qu'aucun mot, nom propre ou chant identifiable n'est audible si la source ne l'autorise pas.
