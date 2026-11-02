# Récit et rétention (`PROPOSÉ`, à valider par blocs)

**Base** : la Méthode v1 (étude AA, hors plugin ; Claude, 23/10/2026, `PROPOSÉ`, cinq blocs), tirée d'une étude de rétention (étude AA, 23/10/2026 : 35 analyses, les vraies courbes de la chaîne AA). S'y ajoutent des repères tirés d'une autre chaîne (24/10/2026), transposés. On lit la Méthode par blocs ; ce fichier n'en donne que l'essentiel et les ajouts.

La boucle de curiosité (`${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` § 1, validé sur AA, 19/10/2026) reste la règle. Les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent sur ces règles par défaut.

## 1. La perte est au début
- Mesure AA : 53 à 60 % des spectateurs partent vers 0:30.
- Les repères d'ouverture sont la priorité. De 0:00 à 1:00, ils sont validés sur AA (26/10/2026, `METHODE_RECIT.md` § 2, Ouverture), comme la première réponse avant 1:30 (même fichier, § 3, Corps du film) :

  | Repère | Ce qu'il faut |
  |---|---|
  | 0 à 15 s | soit une personne nommée, vue de face, en image réelle ; soit l'anomalie en image comparée (avant/après, classement rang par rang) ; un nom, un lieu ou un événement célèbre avant 0:15 |
  | 5 à 15 s | la preuve ou le premier état |
  | avant 0:40 | la contradiction complète ; par défaut, une évidence démentie (« But… ») |
  | avant 0:45 | la question d'une phrase, dite par la voix et écrite à l'écran (texte fixe) |
  | après la question | la signature de la chaîne, puis le plan de la réponse : 2 ou 3 pistes dites, chacune avec un pictogramme qui revient en tête de sa séquence, sans la conclusion |
  | avant 1:30 | une première pièce de réponse ; ni histoire ni cours technique avant elle |

## 2. Patron du film (8 à 10 min)
Les repères de l'ouverture, de la première réponse, de l'ordre des couches, du renversement et de la dernière révélation sont validés sur AA (26/10/2026, `METHODE_RECIT.md`) ; le reste du patron est `PROPOSÉ`.

| Part de la durée | Rôle |
|---|---|
| 0 à 45 s | accroche : l'enjeu, l'image de 0:00 à 0:15, l'évidence démentie, la question dite et écrite (§ 1) |
| 45 à 60 s | la signature, puis le plan de la réponse en 2 ou 3 pistes |
| avant 1:30 | première réponse partielle, qui ouvre une question plus précise ; ni histoire ni cours technique avant elle |
| jusqu'à 75 % | deux couches (histoire, technique, cas), chacune ouverte par une contradiction et finie par une révélation ; une relance toutes les 45 à 120 s ; un cas suivi au passage le plus chargé |
| 75 à 90 % | le renversement (vers 75 %), puis une dernière révélation gardée pour le dernier quart |
| 90 à 100 % | réponse et formule courte, sans prédiction ; écran de fin |

Exemple AA : l'E007 suit ce patron :
- ouverture sur Kompany ;
- question à 0:35 ;
- réfutation de « la gravité de la faute » en seq3 ;
- renversement « to no one » en seq5 ;
- formule finale « Taking it out of memory is another matter ».

## 3. Quatre accroches
1. **L'acte inexplicable** : l'acte daté, en image, puis ce qui le rend absurde, puis « pourquoi ? ».
2. **Le chiffre comparé** : un objet ou un montant, comparé à un repère familier, puis la question.
3. **L'état A puis l'état B** d'une entité connue : un titre soulevé, puis le même titre en jeu, puis « qui décide ? ».
4. **L'évidence fausse** : « tout le monde dit X », puis l'image qui contredit X, puis la question. **C'est l'accroche par défaut** (validé sur AA, 26/10/2026) ; une des trois autres se justifie à la porte du script.

## 4. Relances
- **Relancent** : une contradiction (« But… »), une preuve qui dérange, un changement d'échelle, une phrase surprenante d'un acteur (citée), un coût révélé.
- **Ne relancent pas** : un changement de sujet, une annonce (« voici la première surprise »), « mais ce n'est pas tout ».
- **La surprise se montre, elle ne s'annonce jamais.** On ne prête aucune intention sans source.
- On n'ajoute pas de relances : nous en avons déjà plus que le genre (Méthode, bloc 3).

## 5. Densité et contrôles avant la voix
- Au plus trois chiffres d'affilée. Chaque chiffre clé est donné en paire (avant/après, A contre B) ou comparé à un repère familier, toujours sur une infographie qui naît sur la voix. Tout terme, lieu ou personne inconnus sont expliqués en moins de 5 s, par une image et, si possible, un exemple célèbre (validé sur AA, 26/10/2026).
- Au plus trois noms propres nouveaux par minute ; préférer un rôle à un nom inutile.
- Avant une révélation : une pause de voix de 0,5 à 1 s au plus, seulement sur une image réelle, jamais sur une simple animation ; la musique baisse en creux sans se couper (validé sur AA, 26/10/2026, `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 2).
- **Fiche d'ouverture** en tête du script (Méthode, bloc 5) : pour chaque repère de 0 à 2:00, la phrase, l'image et le temps estimé au débit de la voix de la chaîne : à défaut de mesure, la cible de 130 à 135 mots par minute, pauses comprises (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 2). Tout repère manquant ou en retard est signalé.
  - *Note (02/11/2026)* : l'estimation initiale était de 125 mots par minute. Elle sous-estimait le débit : sur AA, la voix a été mesurée à environ 139 puis 144 mots par minute (E010, puis E011 : 7:23 pour un film prévu à 9 min). Chaque chaîne remplace la cible par le débit mesuré de sa voix (`direction/ECARTS.md`), noté à chaque épisode.
- Gemini ne juge pas une ouverture : il ne sert qu'à décrire un film publié.

## 6. Succession des séquences
- Chaque séquence finit sur une question ouverte que la suivante reprend. Exemple AA (E007) : seq4 finit sur « who gets it? », seq5 ouvre sur « You might think the runner-up simply moves up ».
- Raccords visuels exacts (`socle.md` § 7). La musique continue, ou se tait exprès.
- Image : coupes plus serrées à l'ouverture qu'au milieu ; rien d'immobile plus de 1 s ; transitions variées, chacune avec son son ; dessins et schémas dans les passages d'explication.

## 7. Après la sortie
- Rétention à 0:30, 1:00 et 2:00, comparée aux vidéos habituelles. Taux de clic au-delà d'environ 1 000 impressions.
- On ne conclut qu'à partir d'environ 100 spectateurs.
- Appel à s'abonner au milieu du film : plus une question ouverte ; place par défaut vers 2:00 (`METHODE_RECIT.md` § 1, validé sur AA, 26/10/2026), confirmée ou écartée à la porte.

## 8. Essai : « Illusion of Novelty » (essai en cours sur AA, `PROPOSÉ`, 02/11/2026)
**Statut** : essai décidé par le propriétaire d'AA le 02/11/2026 (Q18 de son E011), en cours depuis cet épisode. Ce n'est **ni une règle du plugin ni, pour l'instant, une règle d'AA** : elle ne le devient qu'au bilan de J+7 (ci-dessous). Une autre chaîne qui veut l'essayer l'écrit dans son `direction/ECARTS.md`, avec ses critères.

**Source** : Kallaway, *The Illusion Of Novelty Doc*, un guide d'écriture d'accroche (le PDF est gardé dans `direction/references/` de la chaîne qui l'essaie, jamais copié dans le plugin). Sa formule : « Novelty is an illusion you construct. » Les sous-agents ne lisent pas le PDF : la grille ci-dessous se copie dans leur contrat.

**Le principe, en nos mots** : un sujet connu n'a pas besoin d'un nouveau thème mais d'un **angle** présenté comme une découverte. Quatre composantes bâtissent l'effet, une cinquième l'empêche de fuir :
1. **Nouveauté et bénéfice** : révéler ce qui a changé (ou ce que peu de gens savent) et le relier à ce que le spectateur veut obtenir ou comprendre.
2. **Contraste** : placer l'angle contre la croyance courante, dans la même phrase, et en vrais opposés (sans quoi « nouveau » ne veut rien dire).
3. **Urgence**, la seule facultative : seulement si quelque chose a vraiment changé ou si une fenêtre se ferme, avec sa date. Une urgence fabriquée coûte la confiance.
4. **Preuve au plus près du spectateur** : du chiffre ou de l'étude (le plus bas) à la foule, puis au cas qui lui ressemble (le plus haut).
5. **Protéger l'illusion** : ne pas avouer que l'idée est ancienne, ne pas atténuer ses propres phrases (« ce n'est en fait que… »), et confier plutôt qu'annoncer.

**Adaptations aux règles du plugin** (décidées avec l'essai) : toute phrase garde sa source, et la cinquième composante ne cache jamais une incertitude (elle se dit : `REFERENTIEL_QUALITE_REALISATION.md` § 2) ; dates absolues (« le 4 février », pas « hier ») ; la preuve vient des acteurs du récit et de leurs documents, jamais d'un témoin ou d'un cas inventé ; urgence vraie seulement ; la surprise se montre, elle ne s'annonce pas (§ 4).

**Grille de note** (0 à 2 par ligne, sur 10, pour la fenêtre 0:00 à 0:45) :

| Composante | 0 | 1 | 2 |
|---|---|---|---|
| Nouveauté | sujet présenté tel quel | présenté comme nouveau, mais vague ou tardif | nouvel angle clair dans l'accroche |
| Bénéfice | non relié à ce que veut le spectateur | implicite ou générique | relié à un résultat précis |
| Contraste | aucune croyance citée | croyance citée, mais pas le vrai opposé ou pas dans la même phrase | croyance et angle dans la même phrase, vrais opposés |
| Urgence | fausse (à signaler, pire que rien) | aucune, et aucune n'était vraie | réelle, avec sa date |
| Preuve | aucune | chiffre ou étude seulement | foule, ou cas proche du spectateur |

Contrôle d'intégrité en plus, réussi ou échoué, qui prime sur la note : une phrase qui avoue l'ancienneté de l'idée, qui l'atténue ou qui hausse le ton comme une annonce publicitaire échoue et se réécrit.

**Emploi pendant l'essai** (AA, E011) : la méthode co-écrit l'angle (étape 2) et le script (étape 3) ; la note est donnée par `studio-faceless:reviewer` avant la voix, jamais par l'auteur de l'accroche. Gemini ne juge pas une ouverture (§ 5).

**Protocole de bilan à J+7** (généralisé de l'E011 d'AA ; `PROPOSÉ`) :
1. **Mesure** : rétention à 0:30 et performance relative à 0:30 (`outils/recherche/youtube_retention.py` : 0,5 = médiane des vidéos de même durée, ce qui corrige l'effet de la durée), lues sur les films comparables de la chaîne (durée voisine), jamais sur ceux d'une autre chaîne.
2. **Seuils fixés avant la sortie**, à partir de ces films :
   - *règle de la chaîne* si le film fait mieux que le meilleur des comparables, sur les deux mesures ;
   - *grille à revoir* s'il fait moins bien que le moins bon, sur l'une ou l'autre ;
   - *essai prolongé* entre les deux : les deux épisodes suivants sont écrits à la grille, puis décision.
   Exemple AA (E011) : règle si la performance relative est d'au moins 0,37 **et** la rétention d'au moins 64 % ; à revoir sous 0,29 **ou** 58 % ; entre les deux, essai prolongé sur les E012 et E013.
3. **Conditions de lecture** : au moins 300 vues à J+7, sinon lecture à J+28 ; noter la source du trafic et la part du public visé, qui changent avec le sujet. Lectures d'appoint : la chute entre 0:15 et 0:30, et la rétention à 1:00.
4. **Limites à écrire au bilan** : un seul film, où la grille change en même temps que le sujet, le titre et la miniature : « mieux que nos meilleurs » ne prouve pas que la grille en soit la cause ; une note donnée en connaissant les chiffres est biaisée.
5. **Décision** : le propriétaire. Atteint, le critère fait de la méthode une règle de la chaîne, écrite dans son `direction/ECARTS.md` ; elle ne rejoint les règles par défaut du plugin que par une décision à part (nouvelle version).
