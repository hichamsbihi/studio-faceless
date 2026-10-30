# Chantier 0.3.0, partie « outils » : suivi (30/10/2026)

Source : `V2/direction/migration/MIGRATION_B_outils_2026-10-30.md` (section « Décisions », VALIDÉ, Hicham, 30/10/2026). V2 = `StudioV2` (Maps & Means, MM) ; P = `plugins/studio-faceless/`. Version et `CHANGELOG.md` non touchés. Aucun commit. Tous les outils portent « validé sur MM, date » dans leur docstring.

## Fait : une ligne par élément
| Réf. | Source V2 | Destination P | Ce qui a été généralisé |
|---|---|---|---|
| B04 | `outils/controle/script.py` | `outils/controle/script.py` | Docstring et statuts datés ; seuils de MM gardés comme valeurs de départ, réglables par `direction/script_seuils.json` de la chaîne ou `--seuils` (13 clés permises, clés inconnues refusées) ; références MM (E4, LIGNE_EDITORIALE) retirées ; `--help` complet |
| B05 | `controle/pauses.py` | `outils/controle/pauses.py` | Usage depuis la racine de la chaîne ; renvoi à `referentiels/DIRECTION_AUDIO.md` et à `direction/ECARTS.md` ; `--help` ajouté |
| B05 | `controle/raccourcir.py` | `outils/controle/raccourcir.py` | Réécrit en outil à arguments : SOURCE, SORTIE, `--sequences` (1-7), `--part` (0,6), `--plancher` (0,25), `--gardes` (JSON). Plus de dossiers `finale-v2/v3`, plus de fenêtres gardées de l'E004 en dur ; `coupes_v3` renommé `coupes` dans le JSON de sortie |
| B05 | `controle/recaler.py` | `outils/controle/recaler.py` | Chemin `C:\Users\…\StudioV2` remplacé par le dossier du script (importe `transcrire.py` du plugin) ; code mis dans `main()` ; date et nom du texte ne sont plus écrits en dur (« SCRIPT-v1 », 19/10/2026) ; `--help` |
| B05 | `controle/remix.py` | `outils/controle/remix.py` | Docstring (prérequis : un `mix.py` dans le dossier de la séquence) ; aide argparse |
| B06 | `medias/traiter.py` | `outils/medias/traiter.py` | Modes `present` et `archive` retirés (charte de l'E003 de MM) ; remplacés par `--filtre` / `--filtre-fichier` (chaîne FFmpeg rangée dans `marque/`), la valeur d'`archive` en exemple dans l'aide ; SDR, 6 s au plus, GOP 15 gardés ; `ffmpeg`/`ffprobe` via `HYPERFRAMES_FFMPEG_PATH` / `HYPERFRAMES_FFPROBE_PATH` ou le PATH. Essai réel : extrait de 1 s traité |
| B07 | `medias/jbig2_page.py` | `outils/medias/jbig2_page.py` | Crédit pdf.js (Apache-2.0) et ITU-T T.88 dans l'en-tête ; `--help` |
| B07 | `medias/rendre_page_pdf.ps1` | `outils/medias/rendre_page_pdf.ps1` | Tampon d'origine, chemin du plugin dans l'usage, « poste de MM » pour l'échelle 1,5 ; Windows seulement (non exécuté ici) |
| B07 | `recherche/pdftexte.py` | `outils/recherche/pdftexte.py` | Mode d'emploi sans WebFetch obligatoire ni chemin de V2 ; `--help` |
| B44 | `gemini/relire.py` | `outils/gemini/relire.py` | Exemple de consigne `mm-regarder` retiré (consigne à fournir par la chaîne) ; aide argparse. **Appel réseau** (API Gemini), comme `regarder.py` : seule exception à « aucun appel réseau » |
| B11 | `cartes/proj.py`, `shp.py`, `cog.py` | `outils/cartes/` (à côté de `cartes.py`, inchangé) | Docstrings sans « épisode 004 » ni « D22 » ; Albers : défaut Alaska gardé comme exemple dit, à passer explicitement ; `cog.py` : `--help`. Essai : Equal Earth aller-retour exact, `km` juste |
| B10, B11 | `cartes/preparer_globe.py`, `preparer_papier.py`, `vols.py`, `globe/*`, `papier/index.html`, `vendor/maplibre-6.13.0/` | `domaines/geo-economie/cartes/modeles-e004/` | Copies sans retouche, sauf le titre de `papier/index.html` (nom de la chaîne retiré) ; README : « modèles de l'E004 », à adapter |
| B10 | `.claude/skills/mm-dessin-pro/references/maplibre/` (4 fichiers, MIT) | `domaines/geo-economie/cartes/references/maplibre/` | Sans modification, `LICENSE.md` et `NOTICE` gardés |
| B10, B11 | README de V2 + docstrings | `domaines/geo-economie/cartes/README.md` | Nouveau : contenu, modèles à adapter, règles de cartographie, projections, limites |
| B02 | `skills/mm-blender-pro/` (12 fichiers) | `skills/blender-pro/` | `references/` (8 fichiers) et `licences/` (2) identiques à V2 (vérifié par `diff -r`) ; `SKILL.md` réécrit : prérequis en tête (Blender 4.5.14 dans `outils/blender/blender-4.5.14-windows-x64/`, hors Git, accord du propriétaire, arrêt si absent), procédure d'installation avec empreinte SHA-256, « poste sans GPU », règles MM (pas de flou, aucun rouge) ramenées à des exemples renvoyant à `marque/` et `direction/ECARTS.md`, style et scènes de MM retirés ; `PROVENANCE.md` nouveau ; `name: blender-pro` |
| B40 | `templates/sequence-gabarit-v4/render.sh` | `templates/sequence-gabarit-v3/render.sh` (+ une ligne du `README.md`) | Seulement la garde HDR (refus d'une vidéo HLG/PQ dans `media/`) et `--sdr`, commentaire d'origine ; garde « provisoire », `mix.py`, `<audio id="mix">` non portés. `bash -n` ok |
| Licences | `outils/controle/controle.py` du plugin | même fichier + README | Voir ci-dessous |

## Décision 5, licences : constat
- Le contrôle `licences` du plugin **ne refuse rien** : il liste les lignes des `PROVENANCE.md` qui citent `BY-SA`, `PD-AR`, `PD-Brazil`, `BY 2.0 BR`, « domaine public argentin » (liste en dur, propre à AA) et rend le code 1. Il ne cible ni NC ni ND (ceux que `controle.py` de V2 excluait).
- Écart avec la règle par défaut du plugin (`REFERENTIEL_QUALITE_REALISATION.md` § 2 bis : médias libres ou non libres admis en citation encadrée) : `BY-SA` y est admissible, donc le signal du plugin est plus strict que la règle. Non changé quant à son défaut.
- Fait (simple) : `controle.py` lit le fichier facultatif `direction/licences.json` de la chaîne (`{"en_attente": ["regex", …]}`), dont la liste **remplace** celle du défaut ; sans fichier, comportement identique. Fichier illisible : arrêt avec message. README du contrôle mis à jour (signal à relire, pas exclusion). Essais : défaut, liste de la chaîne.
- Pour MM, le fichier peut être `{"en_attente": []}` (même souplesse qu'AA, règle par défaut sans écart, aucune exclusion).

## Pas porté, avec la raison
- `medias/calque360.py` (B12, domaine geo-economie, effet de la charte E003 de MM, à cataloguer `expérimental` dans MOTION_CATALOG) : sa destination (`domaines/geo-economie/outils/`) est hors de mon périmètre, et le catalogue est un référentiel (autre agent). À faire.
- Modes `present` et `archive` de `traiter.py` (B06/B30), `film-mix` (B30), `miniature-grand-texte` (B29), `atelier.py` et `corbeille.ps1` (B46, archivage MM : écart de la chaîne, décision 10), `sauvegarde-studiov2.ps1`, `controle.py`, `assembler.py`, `publication.py`, `ralentir.py`, `transcrire.py`, `suivi_tokens.py`, `regarder.py` de V2 (équivalents dans P, ou propres à MM : B30, B34, B45, B46).
- `outils/blender/` de V2 (binaire, archive, `scenes/`, README) : reste dans la chaîne, jamais dans le plugin. Le README de V2 n'est repris que par la procédure d'installation du skill.
- Skills `dessin-pro` (B03), `find-skills` et `humanizer` (B08, B09), gabarits `*.template.md` (B41) : hors de ma tâche (skills et gabarits d'un autre agent).
- Consignes de relecture de script (`consigne-script-v1/v2.md` de `mm-regarder`) : fichiers de skill, hors périmètre ; `relire.py` exige `--consigne`.
- `starter/requirements.txt` : inchangé. Aucun outil porté n'a de dépendance nouvelle (numpy et scipy y sont déjà ; les autres outils n'importent que la bibliothèque standard).

## À faire par d'autres
- `README.md` racine (§ Licence : ajouter `blender-pro`, sources MIT, et les composants MapLibre BSD-3 / MIT du domaine) et liste des skills ; `CHANGELOG.md` et version.
- `referentiels/MOTION_CATALOG.md` : `calque360` (expérimental, domaine geo-economie).
- Un `.gitignore` de chaîne qui exclut `outils/blender/` (le skill le dit, le squelette `starter/` est à vérifier).

## Doutes
- `remix.py` a besoin d'un `mix.py` dans le dossier de la séquence ; le gabarit de séquence du plugin (v3) n'en a pas (V2 en a un dans son v4, que la décision n'a pas versé).
- `script.py` : les balises `[SCENE]`, `[MECANISME]`, `[MIROIR]`, `[PERSONNE]`, `[VOUS]` et les contrôles qui en découlent sont PROVISOIRES sur MM ; seuils par défaut = MM. Une chaîne sans ces balises reçoit des « avis » (pas des écarts).
- `modeles-e004/` : modèles non exécutables sans les données et l'étalonnage de MM ; seule la compilation Python a été vérifiée, pas leur exécution.
- Les `ECARTS` de MM sur la souplesse des licences sont à écrire par l'autre agent / la session de MM.
