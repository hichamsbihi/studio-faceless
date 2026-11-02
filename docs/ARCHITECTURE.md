# Architecture du plugin

## Ordre des règles
Au début de chaque session (et après un `/compact`, ainsi qu'après un `/clear`), le hook `SessionStart` injecte `REGLES_STUDIO.md` en remplaçant `${CLAUDE_PLUGIN_ROOT}` par le chemin du plugin installé. L'application de bureau coupe tout `additionalContext` au-delà de 10 000 caractères (constat du 30/10/2026 : seul un aperçu de 2 Ko arrivait au modèle) : `REGLES_STUDIO.md` reste donc sous 9 000 caractères une fois le chemin substitué (`verifier_depot.py` refuse un fichier plus long) et sa suite, `referentiels/REGLES_DETAIL.md`, se lit à la demande. Les règles s'appliquent ensuite dans cet ordre, la dernière l'emportant :
1. `REGLES_STUDIO.md` et les référentiels du plugin (`referentiels/`) : règles par défaut ;
2. profil du domaine de la chaîne (`domaines/<domaine>/DOMAINE.md`, quand le `CLAUDE.md` de la chaîne nomme un domaine) : règles communes aux chaînes d'un même sujet ;
3. `direction/ECARTS.md` de la chaîne : écarts écrits, statut et date ;
4. `CLAUDE.md` de la chaîne : identité et règles propres ;
5. `CLAUDE.md` de l'épisode.

Un plugin ne charge pas de `CLAUDE.md` à sa racine. C'est pourquoi les règles communes passent par ce hook.

## Garde-fou
`hooks/hooks.json` déclare trois hooks : `regles_studio.py` sur `SessionStart` (injection des règles), `contexte_alerte.py` sur `UserPromptSubmit` (0.4.1 : à chaque message du propriétaire, mesure du contexte du fil principal et, dès 200 k, rappel d'écrire l'état puis de proposer un `/compact` ; [fiche](reference/outils-et-garde.md#hookscontexte_alertepy)) et `garde_commandes.py` sur `PreToolUse` (Bash, PowerShell, Write, Edit, NotebookEdit). Le garde-fou s'applique à toute la session, sous-agents compris.

Un plugin **ignore** les champs `hooks`, `mcpServers` et `permissionMode` dans l'en-tête de ses agents. Le rôle se déduit donc du champ `agent_type` que Claude Code fournit au hook (table `ROLES` du script) :
| Agent | Rôle |
|---|---|
| `motion-producer`, `shorts-producer` | producteur |
| `art-director` | directeur-artistique |
| `studio-maintainer` | mainteneur |
| `research`, Claude principal | aucun rôle : seules les règles communes s'appliquent |
| `reviewer` | relecteur |
| `strategist` | stratege : écrit dans `docs/` et `direction/BANQUE_SUJETS.md` seulement ; en Bash, outils Python du plugin (sauf `youtube_retention.py`), `ls`, `wc`, `grep`, `head`, `tail`, `mkdir`, `cd` |
| `media-fetcher` | telechargeur (0.6.0) : écrit sous `episodes/<id>/kit/media/source-vN/` seulement ; en Bash, `telecharger_medias.py` du plugin, `ls`, `wc`, `grep`, `head`, `tail`, `mkdir`, `cd` |

Les chemins protégés sont relatifs au dossier de la chaîne (`CLAUDE_PROJECT_DIR`). Toute écriture par Write ou Edit dans le plugin installé est refusée.

## Ce qu'un plugin ne peut pas faire
- **Fournir des permissions** (allow, deny, ask) : elles sont dans le `.claude/settings.json` de chaque chaîne, fourni par le squelette.
- **Contenir des fichiers en Git LFS** : ils arriveraient sous forme de pointeurs. Ce dépôt n'a donc aucune règle LFS. Les binaires lourds (marque, sons) restent dans les chaînes.
- **Lire hors de son dossier** : seul `plugins/studio-faceless/` est copié à l'installation. Ce qui sert à l'exécution doit y être.

## Chemins
- Dans les skills, les agents et les hooks, `${CLAUDE_PLUGIN_ROOT}` est remplacé par le dossier du plugin installé (`~/.claude/plugins/cache/…/<version>/`). Ce dossier change à chaque version : rien ne s'y écrit.
- Cette variable n'existe pas dans l'environnement des commandes Bash. Les skills écrivent donc le chemin complet dans la commande, déjà remplacé à la lecture.
- Les outils travaillent dans le dossier de la chaîne : `CLAUDE_PROJECT_DIR`, sinon le dossier courant. On les lance depuis la racine de la chaîne.
- Le crochet Git `pre-commit` de la chaîne cherche `verifier_depot.py` dans le cache du plugin ; la variable `STUDIO_FACELESS_OUTILS` peut désigner un autre dossier `outils/`.

## Noms
Les skills et les agents prennent le préfixe du plugin : `studio-faceless:episode`, `studio-faceless:motion-producer`. Le champ `name:` de leur en-tête garde le nom court. Les skills HyperFrames (`hyperframes-*`, `media-use`) restent des skills d'utilisateur (`~/.claude/skills/`), sans préfixe.

## Versions
- `version` dans `plugin.json` fige la version installée. Le catalogue (`.claude-plugin/marketplace.json`) n'en porte pas.
- La mise à jour automatique est désactivée pour un catalogue privé.
- **Ne jamais renommer le plugin** : un renommage casse les installations.
