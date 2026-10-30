# Skill `elevenlabs-music` : provenance

**Statut** : `VALIDÉ`, Hicham, 29/10/2026. Ajout demandé par le propriétaire depuis la chaîne Cracked Alibi (« utilise le skill elevenlabs et télécharge le nécessaire »), après une recherche par la méthode de `find-skills`.

## Source
- Dépôt : [elevenlabs/skills](https://github.com/elevenlabs/skills) (ElevenLabs), dossier `music/` ; 519 étoiles au 29/10/2026 ; licence MIT, « Copyright (c) 2024 ElevenLabs » (le `LICENSE` accompagne la copie).
- Commit : `503d4e9fda0190ab9357142f44e51de626f97f90` (`main` le 29/10/2026). Fichiers copiés à la main depuis `raw.githubusercontent.com` ; aucune commande `npx` ni CLI lancée.
- Sur skills.sh au 29/10/2026 : 11 500 installations.
- Dépendance : SDK Python `elevenlabs` 2.75.0 (PyPI, MIT), installé le 29/10/2026 et figé dans le `requirements.txt` de la chaîne.

| Fichier | Octets | Empreinte Git (blob) | SHA-256 |
|---|---|---|---|
| `SKILL.md (origine)` | 14 225 | `4126f7fb1b99d3bd42d12a9a888f5766ba59be4b` | `7d868f6f5a09131c11bbeccf9142cbb3cbdc27b5c47cd788c57cb5f35392763d` |
| `SKILL.md (studio)` | 16 259 | `7b0094ad6fc392cd2a445d546bf539d84769a8f5` | `f03d1866ae9d0b270185d12db7a6cf105ac9c6acb9ebe7a71124d97072e52aa0` |
| `references/installation.md (origine)` | 2 284 | `e3ccd5eee7ec28ee7f7810fc0460ff1eff0412e3` | `bc434123987153fc0eb96409f503cee37c84b53a6ae95873ae85b368b2986bb9` |
| `references/installation.md (studio)` | 2 612 | `0fea4381f5ec5bffca8fdf859c8ee9366d145b00` | `8951190d9792a14633208955071e533cb0e36c2e093b45f1b26ade44a6702498` |
| `references/api_reference.md (origine)` | 18 526 | `e9cf120056879d859a381ed9e55c718be363a19d` | `98ea9a58aa989a1812747283ef16b629d5af434e301f0c8040b4b9b010075861` |
| `LICENSE` | 1 067 | `61c1c47ce5964af14a44759b75bd61e5925a898c` | `4ab5e9af2296f748eefa6c0696667f83aa9c0edda7b6972785966b60644b3da6` |

## Modifications du studio
- `SKILL.md` : champ `name` renommé de `music` en `elevenlabs-music` (nom explicite dans le plugin) ; section « Règles du studio studio-faceless » insérée sous le titre ; encadré « Setup » d'origine (qui lançait `npx -y @elevenlabs/cli@latest onboard init`, version non figée et sans confirmation) remplacé par un renvoi à cette section.
- `references/installation.md` : encadré du studio en tête (seule la section Python s'applique).
- `references/api_reference.md` : inchangé.
- Raison : la mise en route d'origine installe une CLI par `npx` sans version ni confirmation et connecte un compte ; le studio garde le SDK Python figé et une clé posée par le propriétaire lui-même.
- Aucune mise à jour sans décision du propriétaire.

## Réglage 0.2.3 (30/10/2026)
- `disable-model-invocation: true` ajouté à l'en-tête de `SKILL.md` (valeur du studio, absente de la source) : le skill n'est plus proposé à Claude au démarrage ; le propriétaire l'appelle avec `/elevenlabs-music`. Le reste du texte est inchangé.
