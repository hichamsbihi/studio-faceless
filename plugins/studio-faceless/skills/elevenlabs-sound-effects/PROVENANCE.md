# Skill `elevenlabs-sound-effects` : provenance

**Statut** : `VALIDÉ`, Hicham, 29/10/2026. Ajout demandé par le propriétaire depuis la chaîne Cracked Alibi (« utilise le skill elevenlabs et télécharge le nécessaire »), après une recherche par la méthode de `find-skills`.

## Source
- Dépôt : [elevenlabs/skills](https://github.com/elevenlabs/skills) (ElevenLabs), dossier `sound-effects/` ; 519 étoiles au 29/10/2026 ; licence MIT, « Copyright (c) 2024 ElevenLabs » (le `LICENSE` accompagne la copie).
- Commit : `503d4e9fda0190ab9357142f44e51de626f97f90` (`main` le 29/10/2026). Fichiers copiés à la main depuis `raw.githubusercontent.com` ; aucune commande `npx` ni CLI lancée.
- Sur skills.sh au 29/10/2026 : 12 000 installations, trois audits réussis (Gen Agent Trust Hub, Socket, Snyk).
- Dépendance : SDK Python `elevenlabs` 2.75.0 (PyPI, MIT), installé le 29/10/2026 et figé dans le `requirements.txt` de la chaîne.

| Fichier | Octets | Empreinte Git (blob) | SHA-256 |
|---|---|---|---|
| `SKILL.md (origine)` | 4 229 | `5fb3e8772b42bee2401199d9b6b136aa80ef700e` | `f032efd853426b15568a3e1f135f9c6ad8dd983e8c4f265aad58675d78e72ae3` |
| `SKILL.md (studio)` | 6 099 | `44315adf041b93759c978bb81ec98e3dd749b1e5` | `d65a6fc60e57a7ac494f42740b568a714d1d310ff3cc8f6a1c16e31aaab5e657` |
| `references/installation.md (origine)` | 2 239 | `fa9bc9b62bddc98d2158a676b2252089bbcf185a` | `40e28b7366308d7e22130b4688d1b9194b31567563e6cf0ecf6cd8cc5d957f0e` |
| `references/installation.md (studio)` | 2 567 | `5c22982ea14046a8411cb0dabfe305bf6923a9b6` | `6411812604ec7952c02321a219581b85f21c5a9d378dedda28955e314d1c1416` |
| `LICENSE` | 1 067 | `61c1c47ce5964af14a44759b75bd61e5925a898c` | `4ab5e9af2296f748eefa6c0696667f83aa9c0edda7b6972785966b60644b3da6` |

## Modifications du studio
- `SKILL.md` : champ `name` renommé de `sound-effects` en `elevenlabs-sound-effects` (nom explicite dans le plugin) ; section « Règles du studio studio-faceless » insérée sous le titre ; encadré « Setup » d'origine (qui lançait `npx -y @elevenlabs/cli@latest onboard init`, version non figée et sans confirmation) remplacé par un renvoi à cette section.
- `references/installation.md` : encadré du studio en tête (seule la section Python s'applique).
- Raison : la mise en route d'origine installe une CLI par `npx` sans version ni confirmation et connecte un compte ; le studio garde le SDK Python figé et une clé posée par le propriétaire lui-même.
- Aucune mise à jour sans décision du propriétaire.
