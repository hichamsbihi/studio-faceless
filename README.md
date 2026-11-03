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
| `skills/` | `episode` (fabrication d'un épisode, du sujet au mix), `shorts`, `thumbnail-strategist`, `youtube-seo`, `direction-sonore`, `regarder` (analyse d'une vidéo par Gemini), `grilling` (portes de questions), `humanizer` (surcouche de relecture des scripts, appelée par le propriétaire), `find-skills` (recherche de skills), `elevenlabs-sound-effects`, `elevenlabs-music` (effets sonores et musique générés), `frontend-design` (conception visuelle et critique des planches et compositions), `remove-background` (détourage avec l'outil de HyperFrames), `blender-pro` (3D avec Blender installé dans la chaîne) |
| `agents/` | dix agents : `research`, `reviewer` (contrôle qualité en lecture seule), `art-director`, `motion-producer`, `shorts-producer`, `studio-maintainer`, `strategist` (positionnement, titres et banque de sujets d'une chaîne, une phase par appel), `media-fetcher` (téléchargement d'une liste de médias validée par le propriétaire), `sound-manager` (tout le son d'un épisode : voix, sons, plan son, mesures ; ni appel payant ni mix long), `publisher` (miniatures, puis dossier de publication ; aucun titre créé, aucune publication) |
| `hooks/` | garde-fou des commandes (par rôle) et injection des règles communes au début de chaque session |
| `REGLES_STUDIO.md` | règles communes injectées à chaque session (moins de 9 000 caractères) : quoi lire, sous-agents, économie de tokens et de contexte, statuts et règles permanentes |
| `referentiels/` | règles par défaut : `METHODE_RECIT`, `REFERENTIEL_QUALITE_REALISATION`, `DIRECTION_AUDIO`, `MOTION_CATALOG`, et `REGLES_DETAIL` (suite des règles communes : moteur et outils, parcours d'un épisode) |
| `outils/` | contrôles (`controle/`, dont `mesurer_sons.py`), montage et mix du film (`montage/`), médias (`medias/`, dont `telecharger_medias.py`), voix par l'API ElevenLabs (`voix/`), recherche, cartes, shorts, rendu, archivage, contrôle du dépôt, suivi des tokens |
| `templates/` | gabarit de séquence v3, modèles de `CLAUDE.md`, de `BRIEF.md` et de `STATE.md` d'épisode, modèle d'`INDEX.md` des épisodes, contrat de mission |
| `domaines/` | profils de domaine (`sport`, `geo-economie`) : règles communes aux chaînes d'un même sujet, entre les règles par défaut et la chaîne |
| `starter/` | squelette d'une nouvelle chaîne |
| `vendor/claude-skills/` | skills HyperFrames de la version 0.8.149, figés |
| `vendor/roast-room/` | copie figée du protocole de conseil roast-room (commit `e40f406`, licence MIT), lue par `strategist` seulement ; ni skill ni agent |

Une fois installés, les skills et les agents portent le préfixe du plugin : `studio-faceless:episode`, `studio-faceless:motion-producer`. Quatre skills (`humanizer`, `find-skills`, `elevenlabs-music` et `elevenlabs-sound-effects`) portent `disable-model-invocation: true` : ils ne sont pas proposés à Claude au démarrage, le propriétaire les appelle avec `/nom`.

## Démarrer
- **Commencer ici, pas à pas** : [`DEMARRAGE.md`](DEMARRAGE.md), de la machine vide à la première vidéo d'une nouvelle chaîne (installation, création de la chaîne, identité, fabrication, publication, archivage).
- Installer une machine et brancher une chaîne existante : [`INSTALLATION.md`](INSTALLATION.md).
- Créer une nouvelle chaîne : [`NOUVELLE_CHAINE.md`](NOUVELLE_CHAINE.md).
- Fonctionnement interne et contraintes des plugins : [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
- **Documentation complète**, fichier par fichier et workflow par workflow : [`docs/README.md`](docs/README.md).

## Règles d'or
1. **Seul le propriétaire valide.** Une proposition n'est pas une décision ; chaque décision est datée.
2. **Claude ne publie, n'achète ni ne supprime rien.** Les essais retirés à l'archivage vont dans `_A_SUPPRIMER/`, que le propriétaire vide lui-même. Aucun envoi vers GitHub sans son accord, donné à chaque fois.
3. **On n'écrase jamais un travail** : une nouvelle version va dans un nouveau dossier.
4. **Médias réels**, choisis sur ce qu'ils apportent à la scène : sous licence libre ou non libres en citation encadrée (`REFERENTIEL_QUALITE_REALISATION.md` § 2 bis) ; une chaîne peut s'en tenir aux licences libres par un écart. Téléchargement par Claude (ou `media-fetcher`) d'une liste validée par le propriétaire, sans contournement. Provenance consignée dans un `PROVENANCE.md`. Aucune image générée par IA, sauf écart écrit de la chaîne.
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
- `vendor/roast-room/` : MIT, © 2026 AI Automation Society (son `LICENSE` et sa provenance sont dans le dossier) ;
- `humanizer`, `find-skills`, `elevenlabs-sound-effects`, `elevenlabs-music` : MIT (leur `LICENSE` et leur provenance sont dans leur dossier) ;
- `blender-pro` : références MIT (scenario-labs/skills, RobLe3/cc-blender-skill ; leurs `LICENSE` sont dans `skills/blender-pro/licences/`) ;
- `frontend-design` : Apache 2.0, © Anthropic (son `LICENSE.txt` et sa provenance sont dans son dossier) ;
- `skills/regarder/references/claude-video/` : MIT, © Bradley Bonanno (son `LICENSE` est dans le dossier) ;
- polices du gabarit : SIL OFL.
