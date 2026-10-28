# Contrat de mission : modèle

À recopier dans le message de délégation à un sous-agent. Les neuf champs sont définis dans les règles communes du studio (`${CLAUDE_PLUGIN_ROOT}/REGLES_STUDIO.md`, « Sous-agents ») ; un champ sans objet vaut « aucun ». Les règles par défaut citées ci-dessous sont dans `${CLAUDE_PLUGIN_ROOT}/referentiels/` ; les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent.

```text
episode_id : <episode-00N | studio>
objectif : <une phrase>
brief : <chemin ou texte court>
fichiers autorisés en lecture : <chemins exacts>
fichiers autorisés en écriture : <dossier exact, ou « aucun »>
sources communes : <direction/…, marque/…, ou « aucune »>
livrables : <liste>
décisions validées : <décision, date et référence, ou « aucune »>
restrictions : <interdits propres à la mission>
```

**Selon l'agent** :
- `studio-faceless:research` : écriture toujours « aucun ».
- `studio-faceless:art-director` : écriture limitée au dossier des images extraites.
- `studio-faceless:motion-producer` (parcours raccourci, validé sur AA, 16/10/2026) : il faut aussi le chemin du **kit de l'épisode** (`episodes/<id>/kit/`), un **brief de séquence court** (modèle ci-dessous) et un dossier d'écriture exact (`episodes/<id>/production/<séquence>-vN/`).
  - Le producteur fait la mise en scène, sans images clés soumises au propriétaire ; il vérifie une planche, écrit `render.sh` et **s'arrête**. Le Studio Director lance le rendu et les contrôles.
  - Les restrictions rappellent l'interdiction de l'effet diaporama, avec sa définition (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2).
  - Une correction après visionnage se confie à un **nouvel** agent, avec un brief de quelques lignes (ce qui change, fichiers et version de départ).
- `studio-faceless:shorts-producer` (validé sur AA, 19/10/2026) : il faut le **kit shorts** (`episodes/<id>/kit/shorts/`), un **brief de short** (modèle : skill `studio-faceless:shorts`, `references/brief-short.md`) et un dossier d'écriture exact (`episodes/<id>/production/short-0N-vM/`). Mêmes règles que le producteur de séquences : il s'arrête à `render.sh`, et chaque correction est confiée à un nouvel agent.
- `studio-faceless:studio-maintainer` : `episode_id` vaut « studio » ; sans écriture autorisée, il constate seulement.

## Brief de séquence court (producteur)
Une page au plus, **3 Ko au plus** (validé sur AA, 18/10/2026). Le producteur ne lit rien d'autre que ce brief, le kit et le `CLAUDE.md` de l'épisode : les règles de `direction/` y sont recopiées en extraits de quelques lignes, jamais renvoyées à un fichier entier.

```text
séquence : <n°, titre, durée de la bande voix>
voix : <kit/voix/…wav> ; repères : <kit/voix/…> (recalés)
narration minutée : <phrase → début–fin (s)>, une ligne par phrase
plan de plans : <moment (s) → média du kit → mouvement voulu → raison d'être>
son : <musique du kit et gain relatif ; effets au moment exact, ou « aucun »>
gabarit : <kit/gabarit/> ; éléments à réutiliser (fond, fiche, étiquettes…)
règles utiles : <extraits courts de direction/ et des consignes de l'épisode : palette, typographie, vibration, photos répétées…>
fiches du catalogue : <identifiants suggérés, ou « aucune »> ; le producteur lit l'index de ${CLAUDE_PLUGIN_ROOT}/referentiels/MOTION_CATALOG.md (lignes 1 à 90) et choisit lui-même, dans sa fiche d'effets écrite avant toute scène
épisode précédent : <retours du propriétaire à appliquer ; techniques déjà employées, à améliorer et non à recopier>
sortie : <dossier d'écriture exact> ; nom du MP4 prévu
```
