# Skill `lemo-layers` : provenance

**Statut** : `EXPÉRIMENTAL` (adapté, jamais employé sur un épisode). Copie du 04/11/2026.

**Décision du propriétaire** (Hicham, 04/11/2026) : « tu prends les skills tu les adaptes à notre environnement point final ». La licence est tranchée par le propriétaire ; elle est seulement consignée ici.

## Source
- Dépôt : [lemomo-ai/lemo-wake](https://github.com/lemomo-ai/lemo-wake), dossier `skills/layers/` ; version 1.1.0.
- Commit figé : `f070df8bdf891d792012aabc054582b16e04f759`. Fichiers bruts téléchargés à ce commit, tailles comparées à l'arbre de l'API ; rien n'a été exécuté.
- Licence : CC BY-NC 4.0 (`LICENSE` de la racine du dépôt, copié ici). Crédit : « Lemomo, lemo-wake », https://github.com/lemomo-ai/lemo-wake.
- Skill compagnon : `lemo-wake` (voir son `PROVENANCE.md`) ; le texte d'origine renvoie à `../wake/scripts`.

## Fichiers (octets, empreinte Git du blob, SHA-256 d'origine)
| Fichier | Octets | Blob Git | SHA-256 |
|---|---|---|---|
| `LICENSE` | 19 805 | `4a084cc3ae357d0c3cc7bc623f427feb224acb9a` | `dca60ea4e526ed8dbbaee970793c3421b114754aa54323d4d00b50ab06d268b6` |
| `SKILL.md (origine)` | 12 716 | `e16ff577d2e95d5dc007cad70b8a868d817153c3` | `8bdb50ab5d5c8d788e988dd9cf449a676df67e059910df05f7f30fa35c5b5dbf` |
| `scripts/layers.py` | 19 453 | `034e7db98a5f277e1f91b7ffb9fc43b1cca71708` | `aa19c1852ae1b9940e1b64f31bdf33137fc623706df97eed25bc6fc7fe8f3075` |

`SKILL.md (studio)` : SHA-256 `0b4f81d79b473f15e3d62e3e8335d180c621589dfcee20062db2ff5a20868e32` (relu par le Studio Director, 04/11/2026). `layers.py` et `LICENSE` sont identiques à l'origine.

## Modifications du studio
- `SKILL.md` seul :
  - front matter : `name: lemo-layers` ajouté ; `description` réécrite en français, sans le chinois ; `when_to_use` supprimé ; `argument-hint`, `license`, `metadata` conservés ;
  - section « Règles du studio studio-faceless (prioritaires sur la suite) » (7 points) insérée sous le titre ; le reste est inchangé et sert de donnée.
- Raison : l'original détoure par des modèles téléchargés, remplit le fond par LaMa, calcule une profondeur par modèle et écrit un PSD par `psd-tools`.

## Tableau des scripts
| Script | Statut | Raison |
|---|---|---|
| `layers.py` (`scan`, `prep`, `build --no-psd`) | utilisable | numpy et PIL ; lancé par `python -I`, jamais par son shebang `uv` ; sortie PNG et `layers.json` |
| `layers.py` écriture du PSD (sans `--no-psd`) | jamais lancé | paquet `psd-tools` à installer |
| `layers.py` recherche d'une pièce rognée (`locate`) | jamais lancé | OpenCV ; donner `nom=fichier@x,y` |
| scripts de `lemo-wake` cités (`segment.py`, `inpaint.py`, `depth.py`) | jamais lancé | voir le `PROVENANCE.md` de `lemo-wake` ; seul `sheet.py` (PIL) y est utilisable |

Consignes douteuses : modèles à télécharger (600 Mo) ; `claude plugin install lemo-wake@lemo-wake` ; fond rempli et formes « complétées en code » (pixels créés).
