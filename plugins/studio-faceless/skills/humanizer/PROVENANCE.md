# Skill `humanizer` : provenance

**Statut** : `PROPOSÉ`. Essai sur un script de la chaîne AA (28/10/2026). Il ne devient une règle du studio qu'avec l'accord du propriétaire de la chaîne, après l'épisode, versé dans `direction/` de la chaîne ou dans le skill `studio-faceless:episode`.

## Source
- Dépôt : [blader/humanizer](https://github.com/blader/humanizer), auteur Siqi Chen ; 61 730 étoiles et 10 942 installations sur skills.sh au 28/10/2026.
- Version : 3.1.0, commit `d4b81278e6604e237bf32f0f7ce5c217aee94269` (28/09/2026), le dernier qui modifie `SKILL.md`.
- Trouvé avec la méthode du skill `find-skills` (vercel-labs/skills) : recherche sur skills.sh, puis vérification des installations, de la source et des étoiles. `npx skills` n'a pas été lancé, faute de pouvoir installer un paquet npm.
- Fichiers copiés à la main le 28/10/2026 depuis `raw.githubusercontent.com`, à ce commit :

| Fichier | Octets | Empreinte Git (blob, égale à celle de GitHub) | SHA-256 |
|---|---|---|---|
| `SKILL.md` | 32 348 | `19fc634208e8cc6ae55d4ff287152583216fd244` | `0612f1dfb1672b0ea9b97e139bf1f06cabe98d8b27424fe8ff01e1fb4cc99cad` |
| `LICENSE` | 1 066 | `625297fb778f32eb39d3a5b97e3e3b611b7304d6` | `4ac4810254ab36d45419141aeb8e69bf50652cfafe5b2dab947d06d44e5cbf96` |

- Licence MIT (« Copyright (c) 2025 Siqi Chen ») : le texte de `LICENSE` accompagne la copie, comme la licence l'exige.
- Le reste du dépôt (`scripts/`, `agents/`, extensions) n'est pas copié : le skill tient dans `SKILL.md` seul, sans code.
- `SKILL.md` est gardé **tel quel** ; aucune mise à jour sans décision du propriétaire.

## Usage décidé sur AA (essai, 28/10/2026)
- Une passe sur la **narration anglaise seulement**, après le script v1 et avant les contrôles de densité ; le script est soumis avec la courte liste des tics corrigés.
- Restent intouchables : les « But… » de l'évidence démentie (`${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` § 2, Ouverture), qui relèvent de l'exception du § 1 du skill ; la question de 0:45 ; les citations ; les faits sourcés.
- Échantillon de voix : un script déjà validé de la chaîne, pour le style seulement (longueur des phrases, ponctuation, transitions) ; aucun de ses faits n'est repris.

## Réglage 0.2.2 (30/10/2026)
- `disable-model-invocation: true` ajouté à l'en-tête de `SKILL.md` (valeur du studio, absente de la source) : le skill n'est plus proposé à Claude au démarrage ; le propriétaire l'appelle avec `/humanizer`. Le reste du texte est inchangé.
