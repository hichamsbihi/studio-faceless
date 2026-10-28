# Gabarit du dossier, liste de contrôle, fiche de conformité

## Gabarit `episodes/<id>/PUBLICATION_vN.md`
Le script lit les blocs ``` placés sous les titres « Titres », « Description », « Tags », « Commentaire épinglé », « Réponse … » et « Playlist » : garder ces mots dans les titres Markdown. Une information inconnue s'écrit « à vérifier », jamais une valeur supposée.

````text
# Épisode NNN · Dossier de publication YouTube, vN (JJ/MM/AAAA)

**Demande du propriétaire** : …
**Statut** : `PROPOSÉ` (sauf : … `VALIDÉ`, le propriétaire, JJ/MM/AAAA). Rien n'est publié : le propriétaire met en ligne.
**Entrées** : journal du master, fiches de narration vérifiées, synthèse des PROVENANCE (studio-faceless:research, JJ/MM), BRIEF.

## Promesse et requêtes — `PROPOSÉ`
- Promesse (une phrase) ; miniature associée :
- Requête principale :
- Longue traîne (3 à 5) :
- Indices relevés (source, date, ce qu'on a vu ; aucun volume) :
- Mots exclus (décision du propriétaire) :

## Titres — `PROPOSÉ`
```
Title A
Title B
Title C
```
Pour chacun : longueur, angle (A question, B requête, C cas concret), lien avec la miniature.

## Description — `PROPOSÉ`
```
(texte complet, chapitres et hashtags compris)
```

## Tags — `PROPOSÉ`
```
tag one, tag two, …
```

## Commentaire épinglé — `PROPOSÉ`
```
…
```
### Réponse 1 au commentaire épinglé (crédits complets)
```
…
```

## Playlist — `PROPOSÉ`
```
Playlist title (seul dans le bloc)
```
Description de la playlist : …

## Sous-titres
`PUBLICATION_vN.en.srt` : nombre de sous-titres, source du texte, date du contrôle.

## Réglages à la mise en ligne (rappels, aucune action de Claude)
…

## Contrôle (JJ/MM/AAAA)
Bilan de `publication.py verifier` (une ligne) et fiche de conformité.
````

## Liste de contrôle
**Promesse et titres**
- [ ] Une promesse, la même que la miniature ; tenue avant 30 s dans la narration de l'accroche.
- [ ] 3 titres vrais et différents ; ≤ 100 caractères, essentiel dans les 60–70 premiers ; ni chevron ni hashtag.

**Requêtes**
- [ ] Une requête principale dans la langue naturelle de la chaîne et 3 à 5 de longue traîne ; aucune requête très populaire.
- [ ] Indices datés ; aucun volume annoncé.

**Description**
- [ ] Les 2 premières lignes portent la promesse et la requête principale (ou sa formulation naturelle).
- [ ] ≤ 5 000 octets, aucun chevron, pas de liste de mots-clés.
- [ ] Chapitres calculés depuis le journal : `0:00`, ≥ 3, ≥ 10 s, titres dans la langue de la chaîne.
- [ ] Note sur les limites des études, si le film les rapproche d'une scène qu'elles n'ont pas mesurée.
- [ ] Aucune synthèse des sources (validé sur AA, 19/10/2026, pour tous les épisodes).
- [ ] Crédits CC BY complets (auteur, source, licence, « adapted »), sauf écart de la chaîne (`direction/ECARTS.md`) ; photo de la miniature créditée ; aucune licence en attente.
- [ ] Voix, musique et effets générés déclarés ; ambiances illustratives signalées.
- [ ] Ligne de chaîne ; 1 à 3 hashtags.

**Tags** : ≤ 500 caractères au compte de YouTube ; mots exclus absents ; aucun mot très disputé seul ; aucun nom absent du film.

**Commentaire épinglé** : question honnête, renvoi aux crédits, appel aux corrections ; réponse 1 (crédits complets).

**Playlist, SRT, réglages**
- [ ] Playlist proposée (titre ≤ 150 caractères).
- [ ] SRT (langue de la chaîne) tiré du texte vérifié, noms propres exacts, contrôlé par `--srt`.
- [ ] Réglages rappelés : contenu modifié ou synthétique, langue, licence des générations, audience.

**Statuts** : `PROPOSÉ` partout, sauf ce que le propriétaire a `VALIDÉ` (date).

## Fiche de conformité (à joindre au dossier ou au rapport)
| Point | Résultat | Remarque |
|---|---|---|
| Limites (script) | N écart(s), N avis | ligne de bilan du script |
| Promesse et titres | conforme / écart | … |
| Requêtes et indices | … | … |
| Description et chapitres | … | … |
| Crédits | … | … |
| Tags et hashtags | … | … |
| Commentaire et réponses | … | … |
| Playlist, SRT, réglages | … | … |

Les mesures du script ne valent pas une relecture : la fiche distingue ce qui est mesuré de ce qui est relu.
