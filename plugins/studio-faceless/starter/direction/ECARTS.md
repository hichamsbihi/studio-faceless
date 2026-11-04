# Écarts de la chaîne aux règles par défaut

Les règles par défaut sont dans `${CLAUDE_PLUGIN_ROOT}/referentiels/`. Ce fichier ne liste que ce que la chaîne fait autrement, ajoute ou précise. **Un écart ici remplace la règle par défaut** (priorité : `REGLES_STUDIO.md` § Priorité du plugin). Ce qui n'y figure pas suit la règle par défaut.

**Format d'une ligne d'écart** : `§ visé : règle de la chaîne (statut, date)`.
- `§ visé` : le numéro de section du référentiel, ou « Ajout » pour une règle que le référentiel ne contient pas ;
- `règle de la chaîne` : ce qui s'applique ici, en une ou deux phrases ;
- `statut` : `FIXÉ`, `VALIDÉ` (propriétaire), `PROPOSÉ`, `PROVISOIRE` ou `QUESTION OUVERTE` ;
- `date` : le jour de la décision, avec la référence si elle existe (brief, rapport) ;
- depuis la 1.1.0, `Remplace : <id>` quand l'écart vise une ligne D (`REGLES_DETAIL.md` § Qui décide : un tel écart est signalé) ou une valeur de `seuils.json` (la valeur elle-même va dans `direction/seuils.json`). `verifier_coherence.py` signale un identifiant qui n'existe plus dans la version installée.

## METHODE_RECIT
Écarts à `${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` (boucle de curiosité § 1, ouverture § 2, corps du film § 3, sujet et titre § 4, shorts § 5).

## REFERENTIEL_QUALITE_REALISATION
Écarts à `${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md`. Ici aussi : le contenu des § 5 (référence d'étude de la chaîne) et § 6 (décisions ouvertes), qui sont propres à chaque chaîne.

## DIRECTION_AUDIO
Écarts à `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md`. Ici aussi : la voix retenue (§ 1), ses réglages, les essais de musique et la bibliothèque de sons.

## MOTION_CATALOG
Écarts à `${CLAUDE_PLUGIN_ROOT}/referentiels/MOTION_CATALOG.md`. Ici aussi : les techniques que la chaîne ajoute (une ligne d'index et une fiche de deux ou trois phrases), et les épisodes qui ont repris une technique existante.
