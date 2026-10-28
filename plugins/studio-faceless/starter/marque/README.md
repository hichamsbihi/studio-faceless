# Marque de la chaîne

Ce dossier porte l'identité de la chaîne, réemployée telle quelle dans chaque film. Chaque élément vit dans son propre dossier versionné (`<element>-vN/`). Un dossier existant ne se modifie jamais : une nouvelle version va dans un nouveau dossier. Les binaires sont en Git LFS (`.gitattributes`).

## Éléments
| Élément | Dossier | Statut |
|---|---|---|
| Logo et bannière | `identite-chaine-01/` | <statut, date> |
| Signature (après l'intro) | `<signature-vN>/` | <statut, date> |
| Appel Like + Subscribe | `<appel-vN>/` | <statut, date> |
| Outro (écran de fin) | `<outro-vN>/` | <statut, date> |

## Couleurs
- **Marque** : <couleurs du logo, de la signature et de l'outro>.
- **Films** : un socle fixe et une palette propre à chaque histoire, décidée en direction artistique avec une planche d'essai. Couleurs interdites dans les films : `couleurs_interdites.json` (`{"nom": "#RRGGBB"}`), contrôlées par `controle.py couleurs` ; vide = aucune.

## Polices des films
<Polices retenues, avec leur licence (SIL OFL de préférence).>

## Réemploi dans un épisode
On copie l'élément depuis son dossier dans le kit de l'épisode. Sa provenance va dans le `PROVENANCE.md` du kit.
