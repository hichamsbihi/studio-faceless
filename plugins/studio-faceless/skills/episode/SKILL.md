---
name: episode
description: "Full making of a documentary episode for a faceless channel, from subject to the final film mix: prepare without questions, one owner session (the socle) once the script v1 is reviewed, then build without questions up to the master, with a closed list of stop cases. Use when the owner starts, resumes or plans an episode. Not for shorts (shorts), thumbnails (thumbnail-strategist) or the YouTube file (youtube-seo)."
---

# Fabriquer un épisode de la chaîne

**Statut** : `VALIDÉ` pour la structure (validé sur AA, 24/10/2026) ; ossature récrite par la 1.1.0 sur le parcours du point 4 (socle, kit, fabrication, arrêts ; validé sur AA, 04/11/2026, à l'essai sur l'E012). Deux références restent à valider par blocs (ci-dessous).

**Ce qui fait foi** : le parcours, les portes, les décideurs, les arrêts et le rendu sont dans `${CLAUDE_PLUGIN_ROOT}/referentiels/REGLES_DETAIL.md` ; les valeurs dans `seuils.json` ; la priorité et le vocabulaire dans `REGLES_STUDIO.md`. Ce skill donne l'ordre des étapes et les listes de contrôle ; il ne recopie pas les règles. Le propriétaire est celui que nomme le `CLAUDE.md` de la chaîne.

## Six règles qui évitent les reprises
1. **Toutes les questions en une seule séance, le socle**, au premier moment où elles ont un objet : après le script v1 relu, avant la voix. Ensuite, on ne pose plus de question : on tranche dans le cadre des accords (au journal) ou on s'arrête (`REGLES_DETAIL.md` § Arrêts).
2. **L'image d'abord.** Un brief décrit des transformations d'images (photo réelle, dessin, carte, raccord de matière), jamais des lignes de texte. La recette v3 fait la base : `references/production.md` § 1.
3. **Le kit est fini avant le premier producteur** (`references/kit.md`) : la voix figée et ses repères ; les médias de la liste accordée, téléchargés par Claude ou par `studio-faceless:media-fetcher` et vérifiés ; les cartes, les logos et les sons ; les raccords au pixel ; les briefs courts.
4. **Les corrections se font dans la même version** : on reprend le producteur si son cache est chaud, sinon un agent court ciblé. Une nouvelle version seulement pour un défaut majeur. L'ancien rendu est rangé, jamais écrasé.
5. **Les séquences ne portent que la voix.** Le film se colle en voix seule, puis on fait un seul mix du film entier. Un rendu à la fois, en tâche suivie, après les contrôles ; Claude regarde chaque planche avant de montrer quoi que ce soit.
6. **Claude n'écoute pas et ne déclare aucun visionnage.** Mesures techniques d'un côté, portes du propriétaire de l'autre ; la fabrication s'arrête à `ECOUTE_A_FAIRE`.

## État, reprise et contexte
- **À chaque fin d'étape** : réécrire en entier `episodes/<id>/STATE.md`, un manifeste court (`sessions.state_ko_max` Ko : étape courante, décisions `VALIDÉ`, chemins des médias, voix et `voice_id`, budget restant, prochaine action ; modèle `${CLAUDE_PLUGIN_ROOT}/templates/STATE.template.md`), mettre à jour `episodes/INDEX.md` (modèle `INDEX.template.md`), puis proposer au propriétaire un `/compact` avec la consigne de `references/tokens-contexte.md` (validé sur AA, 02/11/2026 : plus de `/clear`). Le détail daté va dans `HISTORIQUE_ETAT.md` ; le journal des choix faits en route, dans `JOURNAL.md` de l'épisode.
- **Reprise** : lire seulement `episodes/INDEX.md`, puis le `STATE.md` de l'épisode. Le `CLAUDE.md`, le `BRIEF.md`, le `SOCLE.md` et `HISTORIQUE_ETAT.md` se lisent à la demande, par plages ou par `grep`.
- Le hook `contexte_alerte.py` rappelle le `/compact` au-delà du seuil de contexte (`seuils.json`). Le directeur tourne sur Opus ; jamais de changement de modèle en cours de session.
- **Avant de montrer** un script, une séquence ou le film au propriétaire : un contrôle par `studio-faceless:reviewer` (lecture seule ; il ne valide rien et n'a rien vu ni écouté).

## Les étapes
| # | Temps | Étape | Livrable | Condition de passage |
|---|---|---|---|---|
| 0 | porte 1 | Sujet | `episodes/<id>/` créé, sujet au registre | le propriétaire choisit d'un mot dans `direction/BANQUE_SUJETS.md` |
| 1 | préparer | Recherche | `research/perplexity/R-*.md` (éclaireur), puis `research/R-*.md` (`studio-faceless:research`) | faits relus à la source ; médias candidats sans téléchargement |
| 2 | préparer | Angle et découpage | `ANGLE_DECOUPAGE_vN.md`, page de structure | prêts pour le socle (bloc 1) |
| 3 | préparer | Script v1 et le reste du temps « préparer » | script, tableau des affirmations, fiche de style, liste unique, fiche son, titres, shorts, devis de la voix, fiche des droits | `script.py` et `reviewer` sans point bloquant |
| 4 | porte 2 | Socle et voix | `SOCLE.md` (`templates/SOCLE.template.md`) ; prises vérifiées, ralenties, repères recalés (`kit/voix/`) | socle `VALIDÉ` ; lexique écouté ; voix figée |
| 5 | fabriquer | Kit | kit complet (`references/kit.md`) | liste de contrôle « avant un producteur » cochée |
| 5 bis | fabriquer | Maquette et test de décrochage (si le socle l'a retenue) | une voix sur images sommaires, un rendu | la première minute de décrochage est corrigée avant les producteurs |
| 6 | porte 3 | Épreuve (seulement un style neuf) | accroche, signature et début de S2 définitifs | vue par le propriétaire |
| 7 | fabriquer | Production | séquences jusqu'à `render.sh` (`references/production.md`) | chaque planche regardée ; corrections faites sur place |
| 8 | fabriquer | Rendus | MP4 contrôlés (`references/rendu-collage.md` § 1–2) | `MESURES_TECHNIQUES_OK` pour chaque séquence |
| 9 | fabriquer | Collage en voix seule | master voix et journal (§ 3) | images attendues ; jonctions mesurées |
| 10 | fabriquer | Mix du film | `sound-manager` : plan de cues, sons, plan son ; mix lancé par le directeur ; mesures (§ 4) | cibles de `seuils.json` (`mix.*`) ; `ECOUTE_A_FAIRE` |
| 11 | porte 4 | Visionnage du master et des shorts | une seule liste minutée ; corrections sur place ; pour le son, nouveau plan et remix | `APPROUVE_PAR_<PROPRIETAIRE>` (date), donné par le propriétaire |
| 12 | porte 5 | Publication | `studio-faceless:publisher` : miniatures, puis dossier (skills `thumbnail-strategist`, `youtube-seo`) | le propriétaire choisit et publie |
| 13 | — | Après la sortie | bilans J+2, J+7, J+28 ; `pieges.md` complété ; archivage (`references/etapes.md` § 13) | — |

Le détail de chaque étape est dans `references/etapes.md` ; les shorts du paquet suivent le skill `studio-faceless:shorts`.

**Agents** (0.7.0, validé sur AA, 03/11/2026) : `studio-faceless:sound-manager` fait tout le son (voix, sons, plan son, mesures), et `studio-faceless:publisher` les miniatures puis le dossier de publication. Le directeur coordonne. Il lance les tâches longues (rendus, mix), les appels payants confirmés et, après relecture, les scripts que ces agents écrivent (mesures, masque ; décision du 03/11/2026), puis soumet au propriétaire. Aucun agent n'écoute ni ne publie.

## Avant de lancer un producteur (liste de contrôle)
- [ ] Voix figée ; repères mot à mot recalés ; durée de chaque bande montage.
- [ ] Médias de la séquence déposés (téléchargés ou remis par le propriétaire), vérifiés (empreinte, image regardée) et inscrits au `PROVENANCE.md` du kit avec leur source.
- [ ] Aucune photo prise par une autre séquence, sauf les rappels voulus inscrits au `BRIEF.md`.
- [ ] Image d'entrée et image de sortie écrites au pixel. Chaque séquence d'un même lot a des raccords qui ne dépendent pas d'une autre séquence de ce lot.
- [ ] Fiche de style accordée au socle ; les démos qu'elle reprend et les techniques de chaque temps fort sont citées au brief.
- [ ] Cartes, logos et dessins de référence prêts dans le kit (`${CLAUDE_PLUGIN_ROOT}/outils/cartes/`).
- [ ] Sons choisis dans `marque/son/`. Le producteur ne fait **aucun mix** : il propose ses effets dans un tableau.
- [ ] Brief court qui renvoie aux consignes communes de l'épisode. Passages d'explication marqués (dessin, carte, schéma).
- [ ] Gabarit de séquence v3 (`${CLAUDE_PLUGIN_ROOT}/templates/sequence-gabarit-v3/`) ; en-têtes HTML contrôlés.
- [ ] Contrat de mission complet (`references/production.md` § 2).

## Références (à lire à la demande, par plages)
- `references/etapes.md` : chaque étape en détail.
- `references/kit.md` : construire le kit (étape 5).
- `references/production.md` : la recette v3, le contrat du producteur, les lots, les corrections.
- `references/rendu-collage.md` : rendus, contrôles, collage en voix seule, mix du film, master, sous-titres.
- `references/recit-retention.md` (`PROPOSÉ`) : patron du film, ouverture, relances, densité, succession des séquences.
- `references/choix-sujet.md` (`PROPOSÉ`) : grille et promesse.
- `references/pieges.md` : leçons de tous les épisodes, à compléter à chaque épisode (son et miniature de l'E011 compris).
- `references/tokens-contexte.md` : fin d'étape (`/compact`), état, lectures, délégations.
