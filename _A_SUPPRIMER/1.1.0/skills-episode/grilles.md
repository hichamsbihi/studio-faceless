# Portes de questions (banques par étape)

**Forme** (skill `studio-faceless:grilling`) :
- une série regroupe toutes les questions dont les prérequis sont tranchés ;
- chaque question est numérotée, et sa réponse recommandée est formulée pour que « oui » l'accepte ;
- les faits se cherchent (sous-agent si besoin), les décisions sont au propriétaire ;
- la porte se ferme quand plus aucune question n'est ouverte ;
- les réponses sont écrites au `BRIEF.md`, avec leur date.

Les réponses par défaut ci-dessous sont des points de départ, à adapter au sujet. Les règles citées sont les règles par défaut du plugin (`${CLAUDE_PLUGIN_ROOT}/referentiels/`) ; les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent.

## 0. Sujet
- Le spectateur résume-t-il le sujet en cinq mots avant de cliquer ? Défaut : oui, sinon on écarte le sujet.
- Un non-initié comprend-il la question sans connaître le milieu (exemple AA : ni le club ni la ligue), et l'anomalie se montre-t-elle en une image ? Défaut : oui, sinon on reformule ou on écarte (`${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` § 4, Sujet et titre).
- Qui est l'acteur connu, quel est l'acte intrigant, où est le motif écrit (règle, contrat, décision) ? Défaut : les trois sont nommés, sources à l'appui.
- Quel est le renversement vers 75 % ? Défaut : un fait sourcé qui change le sens de la question.
- Y a-t-il une personne ou un cas à suivre ? Défaut : un cas par couche, pas forcément une personne pour tout le film (Méthode, étude AA, bloc 3).
- Faut-il une carte ? Défaut : seulement si un lieu porte l'argument.
- Le sujet est-il saturé ? Défaut : si une grande chaîne a eu un succès sur la même question dans les 12 derniers mois, on écrit un angle nettement différent avant de commencer (sauf écart de la chaîne dans `direction/ECARTS.md`, `choix-sujet.md` § 1).
- Durée et nombre de séquences ? Défaut : 8 à 10 min, 6 ou 7 séquences. Le premier sujet « Why » qui s'y prête est l'essai de 6 à 7 min, environ 5 séquences (validé sur AA, 26/10/2026, `METHODE_RECIT.md` § 4).

## 1. Recherche
- Quelles parties méritent une mission chacune ? Défaut : le cas central, les précédents ou le mécanisme, puis les médias.
- Éclaireur Perplexity : combien d'appels ? Défaut : un `perplexity_research` par partie, lancés ensemble, aucun `perplexity_ask` (`etapes.md` § 1) ; sans serveur `perplexity` dans la session, `research` seul.
- Quels points de vigilance (procédure en cours, personnes à protéger, chiffres de presse non officiels) ? Défaut : écrits dans le `CLAUDE.md` de l'épisode.

## 2. Angle et découpage
- La question d'une phrase est-elle posée avant 0:45, dite et écrite ? Défaut : oui.
- Quelle accroche, et quelle image de 0:00 à 0:15 (visage nommé ou image comparée) ? Défaut : l'évidence démentie, contradiction complète avant 0:40 (`METHODE_RECIT.md` § 2, Ouverture).
- Quelles 2 ou 3 pistes pour le plan de la réponse après la signature, avec quels pictogrammes ? Défaut : des pistes, jamais la conclusion.
- La première pièce de réponse arrive-t-elle avant 1:30, sans histoire ni cours technique avant elle ? Défaut : oui (`METHODE_RECIT.md` § 3, Corps du film).
- Chaque séquence finit-elle sur la question que la suivante reprend ? Défaut : oui.
- Où va le rappel d'abonnement ? Défaut : juste après l'ouverture d'une question, vers 2:00 (exemple AA : E007), sur un plan calme, plus l'écran de fin. La perte au moment de l'appel est mesurée à J+7 ; si elle dépasse la pente voisine, la question est rouverte (validé sur AA, 26/10/2026, `METHODE_RECIT.md` § 1, Boucle de curiosité).

## 3. Script
- Densité : au plus trois chiffres d'affilée, chaque chiffre clé en paire ou comparé à un repère, chaque inconnu expliqué en moins de 5 s. Défaut : contrôlé et signalé avant la voix.
- Une balise d'émotion est-elle vraiment nécessaire ? Défaut : non.
- Où tombent les pauses de révélation ? Défaut : prévues dès le script, une phrase courte avant chaque révélation sur image réelle (0,5 à 1 s au plus), puis ajoutées aux bandes avec `outils/controle/pauses.py` (validé sur AA, 02/11/2026 ; `pieges.md`, Son).
- Le script suit-il l'essai « Illusion of Novelty » de la chaîne ? Défaut : non, sauf essai écrit dans `direction/ECARTS.md` ; sinon note de l'ouverture par `reviewer` avant la voix (`recit-retention.md` § 8).

## 4. Voix
- Quelle voix ElevenLabs ? Défaut : celle validée pour la chaîne, ou proposée par Claude puis validée.
- Quels mots faut-il réécouter (noms propres, nombres) ? Défaut : la liste est jointe au script.

## 5. Socle
- Quelle direction artistique : palette de l'épisode, motif matériel, mondes par séquence ? Défaut : la base fixe de la marque, plus une palette propre au sujet, testée sur une planche.
- Quels médias télécharger ? Défaut : une liste unique de liens, chacun avec le nom imposé, la taille et le rôle, validée en un seul accord ; Claude la télécharge (outil ou `media-fetcher`) dans `kit/media/source-vN/`, et le propriétaire ne prend que ce qui est refusé (`manuel/`) (validé sur AA, 02/11/2026).
- Quels sons ? Défaut : puisés dans `marque/son/` ; aucune génération sans demande ; Soundza seulement si le propriétaire l'accepte (`DIRECTION_AUDIO.md` § 4 bis).
- Quels raccords ? Défaut : écrits au pixel avant les lots ; les séquences d'un même lot ne dépendent pas l'une de l'autre.
- Quels effets rares, avec leur quota ? Défaut : un WHIP-JUMP par film ; un surligneur deux fois au plus.

## 5 bis. Maquette et test de décrochage
- La faire ou non ? Défaut : la proposer ; le propriétaire décide, et note la première minute où il a envie de passer.

## 6. Séquence témoin
- Quelle séquence ? Défaut : la plus riche en techniques nouvelles, avec des raccords indépendants.
- Que doit-elle prouver ? Défaut : la recette d'image (vivacité, aucun vide incompris, dessins, cartes) et sa grammaire de transitions.

## 7. Production
- Composition des lots ? Défaut : trois producteurs au plus, ordonnés par raccords.
- Que faire d'un défaut trouvé sur une planche ? Défaut : correction sur place, sans nouvelle version.

## 10. Mix du film
- Quels effets retenir ? Défaut : ceux des tableaux des producteurs, sans les facultatifs.
- Niveaux par type, en LU sous la voix ? Défaut : ceux de `rendu-collage.md` § 4.
- Où la musique continue-t-elle, et où se tait-elle exprès ? Défaut : elle continue aux jonctions ; avant une révélation, elle baisse en creux sans se couper (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 2).
- Le rappel d'abonnement reste-t-il à sa place ? Défaut : oui.

## 12. Publication
- Quel titre ? Défaut : trois propositions vraies et différentes, puis le choix du propriétaire.
- Des crédits dans la description ? Défaut : selon la décision du propriétaire pour l'épisode (exemple AA : l'E007 est sans crédits, 24/10/2026).
