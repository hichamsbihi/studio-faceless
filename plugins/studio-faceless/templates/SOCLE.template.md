<!-- Modèle du plugin studio-faceless (1.1.0 ; point 4, validé sur AA, 04/11/2026). Copier dans `episodes/<id>/SOCLE.md`
     quand le temps « préparer » est fini (script v1 relu par le reviewer). Une seule séance du propriétaire ; chaque bloc porte
     sa réponse recommandée. Le propriétaire répond « oui à tout » ou par numéros de ligne ; un bloc refusé fait recalculer les
     blocs suivants dans la séance (une correction du script rouvre la liste des médias et le devis de la voix). Valeurs : seuils.json. -->
# Socle : <épisode> (<JJ/MM/AAAA>)

Statut : `PROPOSÉ` jusqu'à la réponse du propriétaire, puis `VALIDÉ` (date, réponse au mot près). Version du script lue : <v1>.

## 1. L'angle
La question en une phrase, la promesse, l'évidence démentie, le renversement, les séquences, et les faits corrigés à la vérification.
- Recommandé : <…>
- Réponse :

## 2. Le script v1
Avec la note du `reviewer` et le tableau des affirmations (chaque chiffre et chaque nom liés à une source relue) ; la durée estimée (`film.duree_min_s` à `film.duree_max_s`) ; les pauses de révélation prévues ; la place du rappel d'abonnement. Lu en entier.
- Recommandé : <…>
- Réponse :

## 3. Les shorts
Scripts et accroches (`film.shorts_par_film` shorts, `film.accroches_par_short` accroches chacun, de mécanismes différents). Jamais de date en ouverture ; un mécanisme absent des derniers shorts (`shorts.mecanisme_accroche_exclu_derniers_shorts`).
- Recommandé : <…>
- Réponse :

## 4. Le titre
Un parmi trois (`strategist`, D01), et l'idée de miniature.
- Recommandé : <…>
- Réponse :

## 5. Les droits
Les personnes réelles (procédures, mineurs, intentions à ne pas prêter), la compétition admise ou non pour la preuve principale, les médias à risque Content ID. Ce bloc vient avant le style, car il le conditionne.
- Recommandé : <…>
- Réponse :

## 6. La fiche de style
La seule validation de style du film (`STYLES.md` § Fiche de style ; D02). Elle signale un style pas encore porté : il appelle l'épreuve.
- Recommandé : <…>
- Réponse :

## 7. La liste unique de téléchargement
Médias et sons (Soundza avec leur champ `ai_content`), exceptions en tête (citations, extraits) : un seul accord (D05).
- Recommandé : <…>
- Réponse :

## 8. La fiche son
Palette, anti-palette, extraits écoutés par le propriétaire (D06).
- Recommandé : <…>
- Réponse :

## 9. La voix
Le devis en caractères et en crédits, un seul appel pour le film et les shorts, et une marge plafonnée pour les phrases que la transcription rejette. L'accord vaut pour cette version du script, jusqu'au visionnage.
- Recommandé : <…>
- Réponse :

## 10. Le contrat d'arrêt et le plafond
Les cas d'arrêt (`REGLES_DETAIL.md` § Arrêts) et le plafond de dépense du paquet (`direction/seuils.json` de la chaîne) ; la maquette (étape 5 bis), faite ou non.
- Recommandé : <…>
- Réponse :

## Fin de séance : la voix
- Appel lancé par le directeur sur le devis accordé (`--confirme-credits N`) : <heure, crédits>.
- Lexique de voix (chaque nom propre et chaque chiffre, `voix.lexique_s_min` à `voix.lexique_s_max` s), coupé dans la vraie prise : écouté par le propriétaire le <date> ; réponse :
- Voix figée : <date>.
