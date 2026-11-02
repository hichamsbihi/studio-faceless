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

**Règles de la chaîne utiles à la mission** (0.2.3) : une section de **10 lignes au plus**, recopiée par l'orchestrateur depuis le `CLAUDE.md` de la chaîne, à la suite des neuf champs. **Obligatoire pour `studio-faceless:research`, `studio-faceless:studio-maintainer`, `studio-faceless:strategist` et `studio-faceless:media-fetcher`**, qui démarrent sans le `CLAUDE.md` de la chaîne (`omitClaudeMd`) ; facultative pour les autres agents, qui le lisent.

```text
Règles de la chaîne utiles à la mission (10 lignes au plus, recopiées du CLAUDE.md de la chaîne)
protection des personnes : <flou, bip, noms, adresses, plaques, mineurs, victimes, témoins : ce qui concerne la mission>
sources admises : <ordre et exclusions utiles à la mission>
langues : <langue des documents, langue de ce que voit ou entend le spectateur>
autres : <exclusions, statuts, mentions obligatoires utiles à la mission, ou « aucune »>
pour strategist : <propriétaire, domaine, chaînes sœurs, chaînes de référence>
```

**Selon l'agent** :
- `studio-faceless:research` : écriture toujours « aucun » ; section « Règles de la chaîne utiles à la mission » obligatoire.
- `studio-faceless:reviewer` : écriture toujours « aucun » ; le contrat nomme l'objet à contrôler (script, séquence ou film), ses fichiers (script, minutage, plan, transcriptions, planches, mesures) et la durée visée si elle ne vient pas du `BRIEF.md` ; il garde le `CLAUDE.md` de la chaîne.
- `studio-faceless:art-director` : écriture limitée au dossier des images extraites.
- `studio-faceless:motion-producer` (parcours raccourci, validé sur AA, 16/10/2026) : il faut aussi le chemin du **kit de l'épisode** (`episodes/<id>/kit/`), un **brief de séquence court** (modèle ci-dessous) et un dossier d'écriture exact (`episodes/<id>/production/<séquence>-vN/`).
  - Le producteur fait la mise en scène, sans images clés soumises au propriétaire ; il vérifie une planche, écrit `render.sh` et **s'arrête**. Le Studio Director lance le rendu et les contrôles.
  - Les restrictions rappellent l'interdiction de l'effet diaporama, avec sa définition (`${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md` § 2).
  - Une correction après visionnage se fait dans la même version (validé sur AA, 24/10/2026) : reprise du producteur si son cache est chaud, sinon un agent court, avec un brief de quelques lignes (ce qui change, fichiers et version de départ) ; une nouvelle version seulement pour un défaut majeur.
- `studio-faceless:shorts-producer` (validé sur AA, 19/10/2026) : il faut le **kit shorts** (`episodes/<id>/kit/shorts/`), un **brief de short** (modèle : skill `studio-faceless:shorts`, `references/brief-short.md`) et un dossier d'écriture exact (`episodes/<id>/production/short-0N-vM/`). Mêmes règles que le producteur de séquences : il s'arrête à `render.sh`, et chaque correction est confiée à un nouvel agent.
- `studio-faceless:studio-maintainer` : `episode_id` vaut « studio » ; sans écriture autorisée, il constate seulement ; section « Règles de la chaîne utiles à la mission » obligatoire.
- `studio-faceless:strategist` (0.4.0) : `episode_id` vaut « studio » ; deux champs en plus, `phase` (`dossier`, `brief`, `conseil`, `titres`, `sujets` ou `banque`) et `session` (`docs/strategie/<AAAA-MM-JJ>-<sujet>/`) ; écriture dans `docs/`, et dans `direction/BANQUE_SUJETS.md` seulement si « décisions validées » cite l'accord daté du propriétaire ; section « Règles de la chaîne utiles à la mission » obligatoire (propriétaire, langues, domaine, chaînes sœurs, chaînes de référence).
- `studio-faceless:media-fetcher` (0.6.0) : `episode_id` de l'épisode ; écriture limitée à `episodes/<id>/kit/media/source-vN/` ; le contrat donne la **liste JSON** à télécharger (dans `episodes/<id>/kit/`), la décision datée du propriétaire qui la valide (« décisions validées »), le dossier de dépôt et le **robot** (`--agent-utilisateur` : un nom et l'adresse de la chaîne, jamais une adresse e-mail) ; section « Règles de la chaîne utiles à la mission » obligatoire (sources admises, exclusions, langues).

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
fiches du catalogue : <identifiants suggérés, ou « aucune »> ; le producteur lit l'index de ${CLAUDE_PLUGIN_ROOT}/referentiels/MOTION_CATALOG.md (début du fichier, jusqu'à la première fiche `###`) et choisit lui-même, dans sa fiche d'effets écrite avant toute scène
épisode précédent : <retours du propriétaire à appliquer ; techniques déjà employées, à améliorer et non à recopier>
sortie : <dossier d'écriture exact> ; nom du MP4 prévu
```
