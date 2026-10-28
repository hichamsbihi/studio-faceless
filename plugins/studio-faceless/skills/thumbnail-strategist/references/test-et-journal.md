# Test & Compare, lecture du CTR et journal de l'épisode

**Tout ce qui se passe sur la chaîne est fait par le propriétaire** : mise en ligne, lancement et arrêt du test, choix final. Claude prépare les variantes, l'hypothèse et le journal, puis lit les chiffres que le propriétaire lui transmet.

## 1. Ce que dit YouTube (aide 13861714 et 16391400, résumées par l'étude AA du 16/10/2026)
- Jusqu'à **3 miniatures** (ou 3 titres) montrées **en même temps** à des spectateurs différents.
- Le gagnant est désigné au **temps de visionnage**, pas au CTR.
- Le test se termine en **2 semaines au plus**.
- Il faut les fonctions avancées de la chaîne et un ordinateur.

## 2. Protocole (validé sur AA, 17/10/2026)
1. **Avant** :
   - 3 variantes très différentes (`references/promesse-et-concepts.md` § 3), toutes passées par la liste de contrôle ;
   - une **hypothèse écrite** dans le journal (laquelle gagnera, et pourquoi) ;
   - le propriétaire vérifie dans Studio qu'aucun remplacement automatique de miniature n'est activé (annonce de YouTube rapportée par la recherche, non vérifiée à la source).
2. **Pendant** : **aucune modification** de miniature ni de titre ; on n'interprète pas les chiffres partiels.
3. **Verdict** : celui de YouTube, au temps de visionnage. S'il ne se dégage pas de gagnant, on garde la miniature validée par le propriétaire et on le note. Un CTR plus haut ne fait pas un gagnant à lui seul.
4. **Après** : le rapport note qu'un nouveau test est possible 72 h après la sortie, à confirmer dans Studio le moment venu. Un nouveau test se justifie par une nouvelle hypothèse, pas par impatience.

## 3. Lire le CTR (aide 7628154 et 16767369)
- **Par source de trafic** : la recherche a un CTR plus élevé que l'accueil ; un CTR global mélange des publics différents.
- **Dans la durée** : le CTR baisse quand les impressions montent, car la vidéo est montrée plus largement. On compare aux mêmes échéances (J+2, J+7, J+28) et à nos autres épisodes, jamais à un chiffre de « bon CTR » trouvé en ligne.
- **Repère** : la moitié des chaînes et des vidéos sont entre 2 % et 10 %.
- **Toujours avec la durée moyenne de visionnage** : une miniature qui attire sans tenir sa promesse fait monter le CTR et baisser la rétention.
- Depuis le 24/08/2026, CTR, durée moyenne et rétention sont calculés sur les **vues engagées** : c'est dans cette unité qu'on compare les épisodes.

## 4. Journal des miniatures (un par épisode)
Fichier proposé : `episodes/<id>/JOURNAL_MINIATURES.md`. On y ajoute des lignes, on ne réécrit pas les anciennes.

```markdown
# Journal des miniatures — <EPISODE> « titre de la vidéo »

## Hypothèse (écrite avant le test, JJ/MM/AAAA)
- ... Statut : PROPOSÉ

## Variantes
| Variante | Fichier | Mots | Mécanisme | Statut |
|---|---|---|---|---|
| A | `miniatures-vN/...png` | ... | visage et affirmation | VALIDÉ (le propriétaire, date) |
| B | ... | ... | chiffre et comparaison | PROPOSÉ |
| C | ... | ... | moment clé | PROPOSÉ |

## Test & Compare
- Lancé par le propriétaire le ... ; terminé le ... ; aucune modification pendant le test : oui / non
- Résultat donné par YouTube : ... (part du temps de visionnage par variante, si Studio l'affiche)

## Chiffres transmis par le propriétaire
| Échéance | Impressions | CTR accueil | CTR recherche | CTR suggestions | Durée moyenne (vues engagées) |
|---|---|---|---|---|---|
| J+2 | | | | | |

## Leçon proposée
- ... Statut : PROPOSÉ. Elle ne devient une règle de chaîne, versée dans `direction/`, qu'avec l'accord du propriétaire (date et citation).
```

## 5. Statuts
- Concepts, variantes, hypothèses, leçons : `PROPOSÉ`, puis `VALIDÉ` (le propriétaire, date, référence).
- Une leçon d'un épisode reste dans son journal ; elle ne s'applique pas aux autres épisodes sans examen explicite.
- Ne jamais écrire qu'un test, un chiffre ou un regard a eu lieu sans la réponse du propriétaire.
