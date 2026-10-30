---
name: youtube-seo
description: "YouTube publication file for an episode of a faceless documentary channel: titles, description, chapters, CC BY credits, AI-voice disclosure, tags, pinned comment, upload settings, limit checks, J+2/7/28 reviews. Use when preparing or checking an episode's YouTube metadata. Claude never publishes."
---

# Dossier de publication YouTube

Méthode pour rédiger et contrôler le **dossier de publication** d'un épisode : `episodes/<id>/PUBLICATION_vN.md`, statut `PROPOSÉ`. Le propriétaire valide et met en ligne lui-même ; Claude ne publie jamais. Skill rédigé sur AA le 16/10/2026 d'après l'étude AA des skills YouTube (§ 2 et § 3.2) et le dossier fait à la main pour l'E003 d'AA. Statut du skill : `VALIDÉ` (validé sur AA, 17/10/2026).

## Ordre de préséance
Les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent sur les règles par défaut du plugin.
1. **Décisions du propriétaire** : `BRIEF.md` de l'épisode, éléments `VALIDÉ` d'un dossier précédent, mots exclus de l'épisode.
2. **`CLAUDE.md` de la chaîne et `direction/`** : langues, statuts, provenance, ligne éditoriale (accroche fidèle au titre).
3. **Aide officielle de YouTube** : elle l'emporte sur toute « recette » SEO.
4. **Ce skill** : méthode, gabarit et contrôles.

## Étiquettes de preuve (sur chaque règle des références)
`[Officiel]` aide YouTube, doc de l'API ou blog YouTube · `[Observé]` constaté, vérifiable, sans garantie officielle · `[Hypothèse]` raisonnement à tester sur nos chiffres · `[Folklore écarté]` affirmation répandue sans source, qu'on n'applique pas. Sources et limites : `references/signaux-et-limites.md`.

## Méthode, dans l'ordre
1. **Lire par plages** : `BRIEF.md`, les fiches de narration vérifiées, le journal du collage en voix seule (`outputs/<nom>-voix.log.txt`, écrit par `assembler.py`), la décision de miniature, et les `PROVENANCE.md` des séquences et du kit pour les crédits, sauf écart de la chaîne (`direction/ECARTS.md`).
2. **Une promesse** en une phrase, partagée par le titre et la miniature (`studio-faceless:thumbnail-strategist`) et tenue dès l'accroche du film.
3. **Requêtes** : une principale dans la langue naturelle de la chaîne (anglais sur AA), 3 à 5 de longue traîne, indices gratuits datés, jamais de volume. Voir `references/requetes-titres-tags.md`.
4. **Trois titres**, puis tags de longue traîne, 1 à 3 hashtags pour une chaîne neuve et playlist : même référence.
5. **Description** (la promesse et la requête principale dans ses deux premières lignes), **chapitres** calculés depuis le journal du master, **crédits**, **déclaration des voix et sons générés**, **commentaire épinglé** et réponse de crédits complets, **SRT**, **réglages d'envoi** (contenu modifié ou synthétique, langue) : `references/description-et-credits.md`. **Pas de synthèse des sources** (validé sur AA, 19/10/2026, pour tous les épisodes).
6. **Contrôle** : script de limites, puis liste de contrôle et fiche de conformité (`references/gabarit-et-controle.md`).
   ```
   python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/publication.py chapitres episodes/<id>/outputs/<nom>-voix.log.txt --titre seq1="…" …
   python -I -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/publication.py verifier episodes/<id>/PUBLICATION_vN.md --journal <nom>-voix.log.txt --srt <fichier>.srt [--exclure MOT …] [--requete "…"]
   ```
7. **Soumission au propriétaire** : dossier `PROPOSÉ` + fiche de conformité. Il choisit le titre, valide, publie.
8. **Après publication** : bilans J+2, J+7, J+28, sans toucher un titre qui marche (`references/apres-publication.md`).

## Refus permanents
- Publier, programmer, modifier une vidéo en ligne, se connecter à la chaîne ou à un outil capable d'y écrire (vidIQ, MCP tiers) : jamais par Claude.
- Annoncer, estimer ou recopier un volume de recherche, ou un gain de CTR sans source officielle.
- Titre, miniature, tag ou hashtag qui promet ce que le film ne montre pas, nom de personne ou de marque absent du film, liste de mots-clés dans la description (`[Officiel]` aide 146402 : contraire au règlement sur le spam).
- **Omettre un crédit CC BY sans écart écrit de la chaîne.** Par défaut, chaque média CC BY est crédité (auteur, source, licence, mention « adapted ») dans le bloc PHOTO CREDITS et la réponse 1 au commentaire épinglé, à partir des `PROVENANCE.md` (validé sur AA, 19/10/2026 ; règle par défaut du plugin, Hicham, 28/10/2026). Une chaîne peut s'en écarter dans `direction/ECARTS.md` (exemple AA : aucun crédit dans le dossier depuis le 24/10/2026). La déclaration des voix et sons générés reste toujours dans la description.
- Écraser un dossier : toute reprise devient `PUBLICATION_vN+1.md`.

## Livrable
`episodes/<id>/PUBLICATION_vN.md` (gabarit : `references/gabarit-et-controle.md`) et `episodes/<id>/PUBLICATION_vN.en.srt` (le suffixe de langue suit la langue de la chaîne). Texte destiné au spectateur dans la langue de la chaîne (anglais sur AA) ; tout le reste en français.
