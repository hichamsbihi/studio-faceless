# Après la publication : bilans J+2, J+7, J+28

Les données viennent de YouTube Studio, relevées par le propriétaire (export « Exporter la vue » en mode avancé, ou captures). Claude les lit ; il ne se connecte jamais à la chaîne. Chaque bilan est une section datée ajoutée à `episodes/<id>/BILANS_PUBLICATION.md`, sans réécrire les précédentes.

## Ce qu'on relève
| Quand | Quoi |
|---|---|
| J+2 | Impressions et CTR **par source de trafic** (recherche, accueil, suggestions) ; vues engagées ; durée moyenne et pourcentage regardé ; part encore présente à 30 s. Miniature toujours la nôtre ; état de Test & Compare s'il tourne |
| J+7 | Les mêmes, plus les **termes de recherche YouTube** (source « YouTube search ») comparés à notre requête principale et à la longue traîne ; premiers commentaires (questions, erreurs signalées : correction épinglée si besoin). Sur la capture Studio : la **perte au moment de l'appel à s'abonner**, comparée à la pente des secondes voisines (validé sur AA, 26/10/2026) ; pour un essai de durée différente, la comparaison avec les films de durée habituelle de la chaîne (`direction/LIGNE_EDITORIALE.md`) |
| J+28 | Post-mortem complet par le futur skill `video-postmortem` (étude AA du 16/10/2026, § 3.4 ; pas encore écrit). En attendant : les mêmes relevés, et 3 leçons au plus pour le dossier de l'épisode suivant |

## Comment lire
- `[Officiel]` Le CTR se lit par source et dans le temps ; il baisse quand les impressions montent (aide 7628154, 16767369). La moitié des chaînes sont entre 2 % et 10 %.
- `[Officiel]` On compare nos épisodes en **vues engagées** (définition de la vue changée le 24/08/2026, étude AA § 2).
- `[Observé]` Sous quelques centaines de vues, CTR et courbe sont surtout du bruit : on note, on ne conclut pas.
- Chaque phrase du bilan porte « mesuré », « calculé » ou « hypothèse ».

## Ne pas toucher un titre qui marche
- `[Hypothèse]` Changer le titre change la promesse et la pertinence, et brouille la lecture des bilans suivants. Si le CTR de la recherche et de l'accueil reste dans la plage habituelle de la chaîne et que la durée moyenne tient, on ne change rien.
- Un changement n'est proposé qu'à partir de J+7, sur un écart net et prouvé (beaucoup d'impressions et un CTR faible dans toutes les sources, ou des termes de recherche sans rapport avec le titre), avec l'accord du propriétaire, de préférence par Test & Compare (`[Officiel]` jugé au temps de visionnage, aide 13861714).
- Tout changement fait en ligne est consigné dans un nouveau `PUBLICATION_vN+1.md` daté.
- Les vrais termes de recherche nourrissent les requêtes de l'épisode suivant ; une leçon n'entre dans `direction/` de la chaîne qu'avec l'accord du propriétaire.
