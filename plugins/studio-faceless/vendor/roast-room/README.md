# roast-room (copie figée)

**Origine** : https://github.com/nateherkai/roast-room, commit `e40f406`, copié le 02/11/2026. **Licence** : MIT (`LICENSE`, © 2026 AI Automation Society). Fichiers copiés tels quels, sans modification.

**Usage dans le studio** : seul l'agent `strategist` s'en sert (`agents/strategist.md`, phase « conseil »). Ce n'est pas un skill du plugin : le `SKILL.md` ici est le protocole d'origine, lu comme référence, et ne se charge pas au démarrage.

## Contenu
| Ici | Dans le dépôt d'origine | Rôle |
|---|---|---|
| `SKILL.md` | `.claude/skills/roast-room/SKILL.md` | Protocole du Chair : brief, trois tours, résolution, vérification des citations, verdict |
| `roster.json` | `.claude/skills/roast-room/roster.json` | Les 12 sièges, leur pilier, leur question et le conseil par défaut |
| `references/` | `.claude/skills/roast-room/references/` | `seats.md` (choix du conseil, poids), `round-prompts.md`, `scoring.md` (calcul, plafonds), `report-template.md`, `live-room.md` (salle visuelle, non copiée) |
| `brains/<slug>/` | `.claude/skills/roast-room/brains/` | Le « cerveau » de chaque siège, tiré des travaux publics de l'expert, avec identifiants de source |
| `seats/council-<clé>.md` | `.claude/agents/council-<clé>.md` | La consigne de chaque siège (lentille, voix, débat, interdits) |
| `scripts/check_quotes.py` | `.claude/skills/roast-room/scripts/check_quotes.py` | Vérifie chaque citation d'une session contre les cerveaux (`brains/` se trouve à côté de `scripts/`) |

**Correspondance des chemins** : les fichiers d'origine parlent de `.claude/skills/roast-room/` et de `.claude/agents/council-<clé>.md` ; ici ce sont `vendor/roast-room/` et `vendor/roast-room/seats/council-<clé>.md`. Les sessions ne vont pas dans `sessions/` à la racine mais dans `docs/strategie/<date>-<sujet>/` de la chaîne.

**Non copié** : la salle visuelle (`app/`, fichiers `council.json` et `verdict.json`), le skill `newroaster` (il télécharge des vidéos pour bâtir un siège ; à demander au propriétaire si un siège YouTube devient nécessaire), la session d'exemple.

**Aucun siège n'est un spécialiste de YouTube** : le dossier de faits de la chaîne (phase « dossier » de `strategist`) apporte les chiffres de YouTube aux sièges.

**Mise à jour** : une nouvelle copie se fait dans un nouveau commit du plugin, avec le nouveau numéro de commit ici et dans `CHANGELOG.md`.
