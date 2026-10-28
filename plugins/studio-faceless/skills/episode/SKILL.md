---
name: episode
description: Full making of a documentary episode for a faceless channel, from choosing the subject to the final film mix and master — question gates with the channel owner at every step (studio-faceless:grilling), the episode foundation (voice, kit, media lists the owner downloads by hand, maps, logos, sound library, pixel-exact junctions, short briefs), one test sequence validated before producers run in batches of three, in-place corrections, one render at a time, voice-only assembly then a single film mix, and the checks before showing the owner. Use whenever the channel owner starts, resumes or plans an episode, or asks how an episode is made. Not for shorts (studio-faceless:shorts), thumbnails (studio-faceless:thumbnail-strategist) or the YouTube file (studio-faceless:youtube-seo), which it calls at their step.
---

# Fabriquer un épisode de la chaîne

**Statut** : `VALIDÉ` pour la structure (validé sur AA, 24/10/2026 : dix recommandations, dont ce skill, la règle des médias, le mix du film à la fin, la séquence témoin). Deux références restent `PROPOSÉ` : `recit-retention.md` et `choix-sujet.md`, à valider par blocs (Méthode v1, étude AA, 23/10/2026). Rédigé par Claude le 24/10/2026, d'après un audit de la fabrication (étude AA, 24/10/2026).

**Ce qui fait foi** (le propriétaire est celui que nomme le `CLAUDE.md` de la chaîne) :
- les règles communes du studio (`${CLAUDE_PLUGIN_ROOT}/REGLES_STUDIO.md` : statuts, sous-agents, garde-fou, économie de tokens), injectées au début de chaque session, puis le `CLAUDE.md` de la chaîne (langues, propriétaire, règles propres) ;
- les règles par défaut du plugin, dans `${CLAUDE_PLUGIN_ROOT}/referentiels/` : `REFERENTIEL_QUALITE_REALISATION.md` (médias § 2 bis, rythme § 2 ter), `DIRECTION_AUDIO.md` (mix § 3), `MOTION_CATALOG.md`, `METHODE_RECIT.md` ;
- `direction/LIGNE_EDITORIALE.md` de la chaîne, et ses écarts dans `direction/ECARTS.md`, qui l'emportent sur les règles par défaut ;
- `marque/README.md` et `marque/son/README.md` ;
- le `CLAUDE.md` et le `BRIEF.md` de l'épisode.

Ce skill donne l'ordre, les portes et les listes de contrôle. Il ne recopie pas les règles.

## Huit règles qui évitent les reprises
1. **Une porte de questions avant chaque étape** (skill `studio-faceless:grilling`) : des questions numérotées, chacune avec une réponse recommandée que « oui » accepte. Les faits, Claude les cherche ; les décisions sont au propriétaire. On ne fabrique pas tant qu'une question reste ouverte.
2. **L'image d'abord.** Un brief décrit des transformations d'images (photo réelle, dessin, carte, raccord de matière), jamais des lignes de texte. La recette v3 fait la base : `references/production.md` § 1.
3. **Le socle est fini avant le premier producteur** :
   - la voix figée et ses repères ;
   - les médias déposés et vérifiés ;
   - les cartes, les logos et les sons de la bibliothèque ;
   - les raccords au pixel ;
   - les briefs courts.
4. **Une séquence témoin**, rendue et validée par le propriétaire, avant les lots de trois.
5. **Les corrections se font dans la même version** : on reprend le producteur si son cache est chaud, sinon un agent court ciblé. Une nouvelle version seulement pour un défaut majeur. L'ancien rendu est rangé, jamais écrasé.
6. **Un rendu à la fois**, en tâche suivie, après les contrôles. Claude regarde chaque planche avant de montrer quoi que ce soit.
7. **Les séquences ne portent que la voix.** Le film se colle en voix seule, puis on fait un seul mix du film entier.
8. **Claude n'écoute pas et ne déclare aucun visionnage.** Mesures techniques d'un côté, validation du propriétaire de l'autre.

## Les étapes
| # | Étape | Porte de questions (`references/grilles.md`) | Livrable | Condition de passage |
|---|---|---|---|---|
| 0 | Sujet | candidats, grille, promesse | `episodes/<id>/` créé, sujet au registre | le propriétaire choisit parmi les trois premiers |
| 1 | Recherche | parties à chercher, médias candidats | `research/R-*.md` (`studio-faceless:research`) | faits sourcés ; médias candidats sans téléchargement |
| 2 | Angle et découpage | question, couches, renversement, séquences | `ANGLE_DECOUPAGE_vN.md` | `VALIDÉ` par le propriétaire |
| 3 | Script | fiche d'ouverture, densité, relances | `SEQUENCES_*_NARRATION.md`, script ElevenLabs sans balise | `VALIDÉ` ; contrôles avant la voix (`recit-retention.md`) |
| 4 | Voix | voix, prononciations | prises vérifiées, ralenties, repères recalés (`kit/voix/`) | voix figée : plus aucune régénération sans le propriétaire |
| 5 | Socle | direction artistique, médias, sons, raccords | kit complet (`references/socle.md`) | liste de contrôle « avant un producteur » cochée |
| 6 | Séquence témoin | quelle séquence, ce qu'elle doit prouver | une séquence rendue | le propriétaire valide la recette sur elle |
| 7 | Production | lots, raccords, quotas | séquences jusqu'à `render.sh` (`references/production.md`) | chaque planche regardée ; corrections faites sur place |
| 8 | Rendus | ordre | MP4 contrôlés (`references/rendu-collage.md` § 1–2) | `MESURES_TECHNIQUES_OK` pour chaque séquence |
| 9 | Collage en voix seule | marque, appel, jonctions | master voix et journal (§ 3) | images attendues ; jonctions mesurées |
| 10 | Mix du film | musique, effets, niveaux, silences | plan son, master final (§ 4) | −16 ±1 LUFS, crête vraie ≤ −1,5 dBTP ; `ECOUTE_A_FAIRE` |
| 11 | Retours | ce que le propriétaire a vu et entendu | corrections sur place, puis remix ou rendu ciblé | `APPROUVE_PAR_<PROPRIETAIRE>` (date) |
| 12 | Publication | titre, miniature | skills `studio-faceless:thumbnail-strategist` et `studio-faceless:youtube-seo` | le propriétaire publie |
| 13 | Après la sortie | relevés, leçons | bilans J+2, J+7, J+28 ; `pieges.md` complété ; archivage (`references/etapes.md` § 13) | — |

Le détail de chaque étape est dans `references/etapes.md`.

## Avant de lancer un producteur (liste de contrôle)
- [ ] Voix figée ; repères mot à mot recalés ; durée de chaque bande montage.
- [ ] Médias de la séquence déposés par le propriétaire, vérifiés (empreinte, image regardée) et inscrits au `PROVENANCE.md` du kit avec leur source.
- [ ] Aucune photo prise par une autre séquence, sauf les rappels voulus inscrits au `BRIEF.md`.
- [ ] Image d'entrée et image de sortie écrites au pixel. Chaque séquence d'un même lot a des raccords qui ne dépendent pas d'une autre séquence de ce lot.
- [ ] Cartes, logos et dessins de référence prêts dans le kit (`${CLAUDE_PLUGIN_ROOT}/outils/cartes/`).
- [ ] Sons choisis dans `marque/son/`. Le producteur ne fait **aucun mix** : il propose ses effets dans un tableau.
- [ ] Brief court qui renvoie aux consignes communes de l'épisode. Passages d'explication marqués (dessin, carte, schéma).
- [ ] Gabarit de séquence v3 (`${CLAUDE_PLUGIN_ROOT}/templates/sequence-gabarit-v3/`) ; en-têtes HTML contrôlés.
- [ ] Contrat de mission complet (`references/production.md` § 2).

## Références (à lire à la demande, par plages)
- `references/etapes.md` : chaque étape en détail.
- `references/grilles.md` : les banques de questions des portes, avec leurs réponses recommandées.
- `references/socle.md` : construire le kit.
- `references/production.md` : la recette v3, le contrat du producteur, les lots, les corrections.
- `references/rendu-collage.md` : rendus, contrôles, collage en voix seule, mix du film, master, sous-titres.
- `references/recit-retention.md` (`PROPOSÉ`) : patron du film, ouverture, relances, densité, succession des séquences.
- `references/choix-sujet.md` (`PROPOSÉ`) : grille et promesse.
- `references/pieges.md` : leçons de tous les épisodes, à compléter à chaque épisode.
- `references/tokens-contexte.md` : compactages, lectures, délégations.
