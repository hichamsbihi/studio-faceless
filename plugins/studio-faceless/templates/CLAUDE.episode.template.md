# Instructions de l'épisode — [identifiant et sujet]

Modèle inactif tant qu'il n'est pas utilisé pour un épisode autorisé. À copier ultérieurement dans `episodes/[identifiant]/CLAUDE.md`, puis à compléter sans inventer de validation.

## Cadre applicable
- Respecter le `CLAUDE.md` de la chaîne et consulter les référentiels en vigueur selon la mission : `direction/LIGNE_EDITORIALE.md` (ligne éditoriale de la chaîne) et `${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` pour recherche et storytelling, `${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` pour réalisation et qualité visuelle, `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` pour narration vocale et mixage. Les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent sur ces règles par défaut. Les chemins de la chaîne partent de sa racine.
- Renvoyer à ces documents sans recopier leurs règles ; respecter leurs statuts de décision, proposition ou hypothèse.
- Langues de la chaîne (son `CLAUDE.md`).
- Limiter ces instructions à cet épisode. Ne pas importer les conclusions, sources, décisions ou états d'autres épisodes comme des acquis.

## Périmètre de l'épisode
- Identifiant et sujet : [à renseigner].
- Brief de référence : [chemin du brief propre à cet épisode].
- Travail actuellement autorisé : [à renseigner d'après la demande utilisateur].
- Limites particulières : [à renseigner si nécessaire].

## Structure et périmètre des sous-agents
- **Dossiers de l'épisode** :
  - `BRIEF.md` : brief éditorial (ce n'est pas un BRIEF HyperFrames) ;
  - `inputs/` : briefs et prises d'origine fournis par le propriétaire, en lecture seule ;
  - `research/` : notes et sources ;
  - `assets/` : médias retenus, avec leur `PROVENANCE.md` ;
  - `kit/` : socle préparé une seule fois pour toutes les séquences (médias convertis, voix, gabarit, briefs) ;
  - `production/<séquence>-vN/` : un projet HyperFrames par version, jamais écrasé ;
  - `montage/` : `montage.json` et `plan-son.json` du collage et du mix du film ;
  - `outputs/` : masters livrés ;
  - `miniatures-vN/` : miniatures, une version par dossier, jamais écrasée.
- **Lecture par défaut d'un sous-agent** : ce dossier, les référentiels (ceux du plugin et `direction/` de la chaîne) utiles à sa mission (`references/` seulement pour un besoin précis) et les ressources approuvées du studio listées ici : [à renseigner]. Les autres épisodes sont exclus, sauf mention au contrat de mission.
- **Écriture** : uniquement les chemins nommés dans le contrat de mission (voir `CLAUDE.md` de la chaîne).
- **Constats techniques** (HyperFrames, rendus), consultés par `studio-faceless:motion-producer` : [à renseigner au fil de la production].
- **Mémoire** : rien de propre à cet épisode ne devient une règle globale. Un enseignement durable est proposé au propriétaire, puis versé dans `direction/` (une technique d'animation : `direction/ECARTS.md`, section MOTION_CATALOG). Ce qui servirait à toutes les chaînes se propose pour le plugin.

## Recherche et narration
- Partir de la question et des hypothèses du brief, sans présumer de la conclusion.
- Relier les affirmations factuelles à des sources vérifiables dans les notes de l'épisode ; conserver leurs références et les limites utiles à leur interprétation.
- Distinguer faits, hypothèses et interprétations. Signaler ce qui reste non vérifié ; chercher objections et contre-exemples.
- Faire progresser l'explication et la curiosité sans hooks trompeurs. Les découvertes attendues sont des objectifs d'enquête, pas des résultats garantis.

## Décisions et état
- Consigner les décisions éditoriales propres à l'épisode dans son brief, avec leur statut et la référence à la validation utilisateur ; ne pas les recopier ici.
- Toute modification importante du sujet, de l'angle ou de la promesse nécessite la validation de l'utilisateur. Proposer les changements globaux à la direction sans les appliquer implicitement.
- **État courant : `STATE.md`** (à lire seul pour reprendre, avec `episodes/INDEX.md` ; le réécrire en entier à chaque fin d'étape, 2,5 Ko au plus ; modèle `${CLAUDE_PLUGIN_ROOT}/templates/STATE.template.md`). Journal complet : `HISTORIQUE_ETAT.md`, à lire par `grep`.
- Prochaine action autorisée : [à renseigner dans `STATE.md` ; ne pas supposer une autorisation de production].

Ce fichier définit des instructions ; il ne lance aucune action ni aucun processus autonome.
