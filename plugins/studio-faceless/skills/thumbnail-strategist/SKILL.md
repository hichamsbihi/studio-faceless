---
name: thumbnail-strategist
description: "Thumbnail method for a faceless documentary channel: one promise shared with the title, five truthful concepts, three variants, HTML/CSS 1280x720 render, measurable checks, A/B test protocol. Use when planning, making, critiquing or checking a thumbnail. Real licensed photos only, never AI images."
---

# Miniatures

Méthode pour concevoir, fabriquer, contrôler et tester les miniatures d'un épisode de la chaîne. Statut du skill : `VALIDÉ` (validé sur AA, 17/10/2026 ; rédigé le 16/10/2026 à partir de l'étude AA des skills YouTube).

## Ordre de préséance
Les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent sur les règles par défaut du plugin.
1. **Les décisions du propriétaire** (`BRIEF.md` et `PROVENANCE.md` de l'épisode) et les règles du `CLAUDE.md` de la chaîne et de `direction/`.
2. **L'aide officielle de YouTube** (formats, Test & Compare, CTR) : elle l'emporte sur toute « recette » de miniature.
3. **Ce skill** : la méthode, la grammaire par défaut (trois calques, VALIDÉ, Hicham, 03/11/2026 ; celle de l'E003 en secours), les contrôles et les gabarits.

## Quand l'utiliser
- Trouver les concepts et les variantes d'une miniature, une fois le titre et le montage connus.
- Fabriquer une miniature (HTML/CSS, rendu par le Chrome de HyperFrames) ou la critiquer (`studio-faceless:art-director`, sur demande du propriétaire). Le directeur artistique critique sur les PNG et les planches ; son garde-fou ne lui permet pas de lancer le script, donc les mesures sont faites par `publisher` ou Claude principal.
- **Agent** (0.7.0, validé sur AA, 03/11/2026) : `studio-faceless:publisher` fait les miniatures d'un épisode avec ce skill (mission principale), puis le dossier de publication (`studio-faceless:youtube-seo`). Le titre lui est donné : il vient de `studio-faceless:strategist`, validé par le propriétaire.
- Préparer le test A/B, puis lire et consigner son résultat.
- Ne pas l'utiliser pour générer une image : aucune image générée par IA, ni fond, ni visage, ni retouche de visage.

## Cadre (non négociable)
- **Photos réelles sous licence libre**, chacune consignée dans le `PROVENANCE.md` du dossier de miniatures, crédit compris pour la description YouTube.
- **Personnalités publiques seulement** en sujet ; aucune personne anonyme en sujet (validé sur AA, E003 : « mettre des photos de personnes anonymes ne va pas amener des gens à cliquer »).
- **Aucun média d'un concurrent.** On reprend des principes, jamais leur style ni leurs couleurs.
- **Mise en ligne, choix final et lancement des tests : le propriétaire seul.** Claude ne publie, ne téléverse et ne modifie rien sur la chaîne.

## Méthode, dans l'ordre
1. **Promesse** : une seule promesse, portée à la fois par le titre et la miniature et tenue dès l'accroche de la vidéo. La miniature complète le titre sans le répéter. Voir `references/promesse-et-concepts.md`.
2. **Au moins 5 concepts véridiques**, chacun fondé sur une contradiction vérifiée et sourcée ; aucune émotion ni pensée inventée prêtée à une personne réelle. Voir `references/promesse-et-concepts.md`.
3. **3 variantes très différentes** retenues parmi les concepts (sujet, image, mécanisme du texte) ; au moins 2 pour un Test & Compare (validé sur AA, 03/11/2026).
4. **Grammaire** : par défaut, depuis le 03/11/2026 (VALIDÉ, Hicham, après le choix de la v2-3 de l'E011 d'AA), la **méthode en trois calques** : vraie photo de fond déjà vibrante, floutée et voilée ; vrai visage célèbre détouré par `remove-background` ; question de 3 mots en HTML qui nomme la star, mot clé en couleur complémentaire, bandeau de contexte d'une ligne. Voir `references/trois-calques-e011.md`. La grammaire de la v4 de l'E003 (fond uni, flèche, drapeaux ; `references/grammaire-e003.md`) reste en secours et garde ses leçons, mais son fond uni a été jugé « pas captivant ».
5. **Fabrication** : HTML/CSS 1280×720, détourage par `remove-background` (VALIDÉ, Hicham, 03/11/2026) ou, en secours, par polygone à partir d'une grille de coordonnées, rendu sans fenêtre. Voir `references/fabrication.md` et `scripts/miniature.py`.
6. **Contrôles mesurables** (poids et taille, aperçus 168×94 et 320×180, coin inférieur droit, contraste du texte, fonds clair et sombre), puis planche « flux » (analyse interne). Voir `references/controles.md`. Les mesures ne remplacent pas le regard du propriétaire.
7. **Test & Compare** et **journal de l'épisode**. Voir `references/test-et-journal.md`.

## Refus permanents
- Image générée par IA, visage reconstruit ou « amélioré », montage qui fait croire à une scène qui n'a pas eu lieu.
- Émotion, pensée, citation ou geste prêtés à une personne réelle sans source (exemple AA : « MESSI HATES BRAZIL ») ; la miniature ne montre que ce que la photo montre.
- « $0 » ou tout chiffre près d'une personne dont le cachet n'est pas public ; scène inventée (exemple AA, E011 : un bras qui cache un sac d'argent) ; plus d'un point d'attention (validé sur AA, 03/11/2026).
- Promesse que la vidéo ne tient pas, ou qu'elle ne tient que tard.
- Texte qui recopie le titre ; plus de 4 mots ; texte dans le coin inférieur droit.
- Personne anonyme en sujet ; photo sans licence ou sans provenance.
- Fonds, contours, flèches ou couleurs repris d'un concurrent.
- Modification d'une miniature pendant un test A/B.

## Livrables types
- Fiche de concepts (5 au moins) et choix des 3 variantes, statut `PROPOSÉ`.
- Dossier `episodes/<id>/miniatures-vN/` (jamais écrasé) : sources HTML, PNG 1280×720, `media/`, `PROVENANCE.md`, planche de contrôle.
- Fiche de contrôle (gabarit dans `references/controles.md`).
- Journal des miniatures de l'épisode (gabarit dans `references/test-et-journal.md`).

Sources des méthodes reprises : `SOURCES.md`.
