# studio-faceless

Plugin Claude Code pour fabriquer des chaînes YouTube documentaires **faceless** avec le moteur vidéo **HyperFrames**. Il couvre tout le parcours : sujet, recherche, script, voix, mise en scène, rendu, contrôles, mix du film, miniature, dossier de publication et shorts. Le propriétaire de chaque chaîne décide, valide et publie.

Il est tiré de StudioV1, le studio de la chaîne Apparently Athletic. Il sert aux chaînes de Hicham ; le dépôt est privé.

## Deux étages
```
studio-faceless (ce dépôt)                       espace d'une chaîne (un dépôt par chaîne)
  le plugin : méthode, agents, outils,      ──►    CLAUDE.md          identité, propriétaire, langues, voix
  garde-fou, gabarits, règles par défaut          direction/         ligne éditoriale + écarts aux règles par défaut
                                                  marque/            logo, signature, outro, sons (Git LFS)
                                                  episodes/          un dossier par épisode
                                                  .claude/settings.json   active le plugin, permissions
```
Le plugin ne dépend d'aucune chaîne : les mentions d'AA ou de StudioV1 n'y servent qu'à dater l'origine d'une règle (« validé sur AA, date »). Ce qui est propre à une chaîne vit dans son espace. Une amélioration du plugin profite à toutes les chaînes dès qu'elles passent à la nouvelle version.

## Contenu du plugin (`plugins/studio-faceless/`)
| Élément | Contenu |
|---|---|
| `skills/` | `episode` (fabrication d'un épisode, du sujet au mix), `shorts`, `thumbnail-strategist`, `youtube-seo`, `direction-sonore`, `regarder` (analyse d'une vidéo par Gemini), `grilling` et `grill-me` (portes de questions), `humanizer`, `javascript-animation`, `soundtrack` |
| `agents/` | `research`, `art-director`, `motion-producer`, `shorts-producer`, `studio-maintainer` |
| `hooks/` | garde-fou des commandes (par rôle) et injection des règles communes au début de chaque session |
| `REGLES_STUDIO.md` | règles communes : outils, sous-agents, parcours d'un épisode, économie de tokens, statuts |
| `referentiels/` | règles par défaut : `METHODE_RECIT`, `REFERENTIEL_QUALITE_REALISATION`, `DIRECTION_AUDIO`, `MOTION_CATALOG` |
| `outils/` | contrôles (`controle/`), montage et mix du film (`montage/`), cartes, shorts, rendu, archivage, contrôle du dépôt, suivi des tokens |
| `templates/` | gabarit de séquence v3, modèles de `CLAUDE.md` et de `BRIEF.md` d'épisode, contrat de mission |
| `starter/` | squelette d'une nouvelle chaîne |
| `vendor/claude-skills/` | skills HyperFrames de la version 0.8.149, figés |

Une fois installés, les skills et les agents portent le préfixe du plugin : `studio-faceless:episode`, `studio-faceless:motion-producer`.

## Démarrer
- Installer une machine et brancher une chaîne existante : [`INSTALLATION.md`](INSTALLATION.md).
- Créer une nouvelle chaîne : [`NOUVELLE_CHAINE.md`](NOUVELLE_CHAINE.md).
- Fonctionnement interne et contraintes des plugins : [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
- **Documentation complète**, fichier par fichier et workflow par workflow : [`docs/README.md`](docs/README.md).

## Règles d'or
1. **Seul le propriétaire valide.** Une proposition n'est pas une décision ; chaque décision est datée.
2. **Claude ne publie, n'achète ni ne supprime rien.** Les essais retirés à l'archivage vont dans `_A_SUPPRIMER/`, que le propriétaire vide lui-même. Aucun envoi vers GitHub sans son accord, donné à chaque fois.
3. **On n'écrase jamais un travail** : une nouvelle version va dans un nouveau dossier.
4. **Médias réels sous licence libre**, provenance consignée dans un `PROVENANCE.md`. Aucune image générée par IA, sauf écart écrit de la chaîne.
5. **HyperFrames reste figé en 0.8.149** : aucune mise à jour sans décision du propriétaire.

## Faire évoluer le plugin
1. Modifier les fichiers **dans ce dépôt**, jamais dans le plugin installé (le garde-fou l'interdit).
2. Augmenter `version` dans `plugins/studio-faceless/.claude-plugin/plugin.json` et noter le changement dans [`CHANGELOG.md`](CHANGELOG.md).
3. Commit, puis envoi sur GitHub avec l'accord du propriétaire.
4. Dans chaque chaîne : `claude plugin update studio-faceless@studio-faceless`, puis `/reload-plugins` dans la session ouverte.

Commits courts, en français, préfixés par la zone : `plugin : …`, `skills : …`, `agents : …`, `outils : …`, `garde : …`, `docs : …`.

## Licence
Dépôt privé, propriété de Hicham, tous droits réservés. Les contenus tiers gardent leur licence :
- HyperFrames et ses skills : Apache-2.0 ;
- `humanizer`, `javascript-animation` et `soundtrack` : MIT (leur `LICENSE` et leur provenance sont dans leur dossier) ;
- `skills/regarder/references/claude-video/` : MIT, © Bradley Bonanno (son `LICENSE` est dans le dossier) ;
- polices du gabarit : SIL OFL.
