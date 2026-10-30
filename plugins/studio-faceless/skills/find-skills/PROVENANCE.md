# Skill `find-skills` : provenance

**Statut** : `VALIDÉ`, Hicham, 29/10/2026. Ajout au plugin demandé par le propriétaire depuis la chaîne Cracked Alibi (« tu télécharges /find-skills et tu l'ajoutes dans le plugin »), pour chercher des skills d'effets sonores et de musique de fond.

## Source
- Dépôt : [vercel-labs/skills](https://github.com/vercel-labs/skills) (Vercel), qui porte aussi le CLI `skills` ; 37 111 étoiles au 29/10/2026 (API GitHub).
- `SKILL.md` : `skills/find-skills/SKILL.md`, commit `773fb2c7bbf16781670a3520affc4abd0c6151ae` (06/07/2026), le dernier qui le modifie ; identique sur `main` le 29/10/2026 (`92a9a34ac3bf88e695e468b90c7bf32f163d32c8`).
- `LICENSE` : racine du dépôt, sur `main` le 29/10/2026 (dernier commit qui le modifie : `e173b8c88f2581cfdaa1b6767c6519a08155790e`, 22/07/2026). Licence MIT, « Copyright (c) 2026 Vercel, Inc. » : le texte accompagne la copie, comme la licence l'exige.
- Fichiers copiés à la main le 29/10/2026 depuis `raw.githubusercontent.com` ; `npx skills` n'a pas été lancé. Le reste du dépôt (le CLI) n'est pas copié : le skill tient dans `SKILL.md` seul, sans code.

| Fichier | Octets | Empreinte Git (blob) | SHA-256 |
|---|---|---|---|
| `SKILL.md` d'origine | 5 472 | `a41bdd074bb587afd861332cf2f473f3154de4d7` | `c00eeea0e13e74fe4a9d84ba0a8542205a1b736d65f13134fe1a6647eb14976f` |
| `SKILL.md` du studio | 6 840 | `536ce3575c10917d547b97f8a46e9d3623beb98f` | `f053108930df61d5f379bdc1595c336afbc16994a4017ae423b6c3270ee96875` |
| `LICENSE` | 1 069 | `eabe3008f6c0275929faa8b07d406e82717648cc` | `661142e53c313d2bb5e1b055f5c0a39001450ff1b5e27b89dc4bc7de9a6352ca` |

## Modification du studio
- Une section « Règles du studio studio-faceless (prioritaires sur la suite) » est insérée sous le titre ; le reste du texte est inchangé. La licence MIT permet la modification.
- Raison : le texte d'origine lance `npx skills find` et installe par `npx skills add <skill> -g -y` (installation globale, sans confirmation). Le garde-fou refuse les installations npm, et aucun skill ne s'ajoute sans décision du propriétaire. La section reprend la méthode déjà suivie pour `humanizer` le 28/10/2026 : recherche sur skills.sh et GitHub par le web, vérification, copie à la main avec `LICENSE` et `PROVENANCE.md`, nouvelle version du plugin.
- Aucune mise à jour sans décision du propriétaire.

## Réglage 0.2.2 (30/10/2026)
- `disable-model-invocation: true` ajouté à l'en-tête de `SKILL.md` (valeur du studio, absente de la source) : le skill n'est plus proposé à Claude au démarrage ; le propriétaire l'appelle avec `/find-skills`. Le reste du texte est inchangé.
