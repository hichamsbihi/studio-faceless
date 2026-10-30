<!-- Modèle du plugin studio-faceless (0.2.3). Copier dans `episodes/<id>/STATE.md` à la création de l'épisode, puis le RÉÉCRIRE EN ENTIER à chaque fin d'étape. 2,5 Ko au plus : un fait par ligne, rien de ce qui est déjà dans BRIEF.md ou CLAUDE.md. Le détail daté va dans `HISTORIQUE_ETAT.md` (journal, lu par grep). Retirer ce commentaire à la copie. -->
# STATE <id-épisode> (manifeste de reprise, réécrit à chaque fin d'étape)

Dernière mise à jour : <JJ/MM/AAAA>, fin de l'étape <n>. Pour reprendre : `episodes/INDEX.md`, puis ce fichier seul ; le détail est dans `CLAUDE.md` (règles) et `HISTORIQUE_ETAT.md` (journal, à lire par `grep`).

## Étape courante
- **Étape <n> (<nom>)** : <non commencée | en fabrication | porte de questions ouverte | en attente du propriétaire>.
- Étapes <0 à n-1> closes.

## Décisions VALIDÉES (<propriétaire>)
- <décision> (<JJ/MM/AAAA>, <référence : porte, question>).
- Voix : <nom de la voix>, `voice_id` `<identifiant>`, réglages <réglages> ; prise <figée le JJ/MM/AAAA | pas encore figée>.
- Film : <durée visée>, minutage `<chemin>`.

## Chemins utiles
- Voix : `<chemin>` ; médias : `<chemin>` ; direction artistique : `<chemin>` ; gabarits : `<chemin>`.
- Rendus : `<chemin>` (statut : <EN_COURS | MESURES_TECHNIQUES_OK | ECOUTE_A_FAIRE | …>).

## Budget
- Épisode : <total> Mt ; consommé : <x> Mt ; reste pour l'étape en cours : <y> Mt (dernière mesure `suivi_tokens.py` : <JJ/MM/AAAA>).

## Prochaine action
1. <action précise>
2. <action précise>
