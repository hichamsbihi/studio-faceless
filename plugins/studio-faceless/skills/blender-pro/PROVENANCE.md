# Skill `blender-pro` : provenance

**Statut** : règle générale du plugin depuis la version 0.3.0 (VALIDÉ, Hicham, 30/10/2026, décision 7 du passage MM). Skill écrit sur Maps & Means (`mm-blender-pro`, 20/10/2026, accord de Hicham : Q6 et Q18 du brainstorming, « ok pour tout »), généralisé le 30/10/2026. Le binaire Blender n'est pas dans le plugin.

| Fichiers | Source exacte | Licence |
|---|---|---|
| `references/scenario-lighting-rendering/*`, `references/scenario-expert/*` | `github.com/scenario-labs/skills`, commit `ccc6c5c623a4f96423df0d157b8ef174f14edfd8`, `skills/dcc/blender/…` (les `SKILL.md` d'origine sont renommés `lighting-rendering.md` et `expert.md`) | MIT, © 2026 Scenario Inc., `licences/LICENSE-scenario-labs-MIT` |
| `references/roble3/*` | `github.com/RobLe3/cc-blender-skill`, commit `a2634b588e80265e796aa53f8ab178d75105c2af`, `plugin/skills/blender-materials` et `blender-cameras` (`SKILL.md` renommés) | MIT, © 2026 RobLe3, `licences/LICENSE-RobLe3-MIT` |

Copiés sans modification le 20/10/2026 par Claude avec l'accord de Hicham, recopiés tels quels le 30/10/2026 (les 8 fichiers de `references/` et les 2 de `licences/` sont identiques à ceux de `mm-blender-pro`). Examen complet par un agent ; vérification par Claude que les deux scripts (`bx_light.py`, `bx_review.py`) ne font ni appel réseau, ni commande système, ni suppression de fichier (seul `cycles_gpu()` touche aux préférences de la session).

Blender 4.5.14 LTS : GPL, `https://download.blender.org/release/Blender4.5/` ; SHA-256 de l'archive Windows x64 relevée le 20/10/2026 dans `SKILL.md`.
