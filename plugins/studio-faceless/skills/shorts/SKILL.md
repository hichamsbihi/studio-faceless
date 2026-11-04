---
name: shorts
description: "Shorts method for a faceless documentary channel: vertical 9:16 shorts cut from a published film, hook in the first frame, word-by-word captions, end card to the film, platform rules, checks. Use when planning, writing, editing or reviewing a short. Claude never publishes."
---

# Shorts

Méthode pour choisir, écrire, monter et contrôler les shorts d'un film de la chaîne. Statut du skill : `VALIDÉ` (Hicham, 04/11/2026, après les pilotes et le short A de l'E011 d'AA, Q98 ; rédigé sur AA le 19/10/2026 d'après les décisions de son propriétaire du même jour).

## Ordre de préséance
Les écarts de la chaîne sont dans `direction/ECARTS.md` (priorité : `REGLES_STUDIO.md` § Priorité).
1. **Les décisions du propriétaire** et les règles du `CLAUDE.md` de la chaîne, de `direction/` (`ECARTS.md`, puis `${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` § 1 Boucle de curiosité et § 5 Shorts, `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md`, `${CLAUDE_PLUGIN_ROOT}/referentiels/REFERENTIEL_QUALITE_REALISATION.md`) et de `marque/README.md` § Shorts.
2. **L'aide officielle des plateformes** (`references/plateformes.md`).
3. **Ce skill.**

## Objectifs (validé sur AA, 19/10/2026), dans l'ordre
1. Que le short soit regardé jusqu'au bout.
2. Faire connaître la chaîne.
3. Amener vers le film, sur YouTube.

**Toujours une vraie valeur** : le short apprend quelque chose de vrai et tient seul. La relance vers le film est une invitation, jamais une information retenue pour forcer le clic.

## Qui fait quoi
| Étape | Qui |
|---|---|
| Choisir 3 à 5 boucles par film ; écrire 2 ou 3 hooks par boucle, le script et le pont | Claude principal, puis choix du propriétaire |
| Préparer et chiffrer la prise de voix, à blanc (texte du short mot pour mot, une seule prise, vitesse d'origine) | `studio-faceless:sound-manager` |
| Lancer l'appel payant de la prise | Claude principal, après la confirmation du propriétaire |
| Voix et son du short : prise contrôlée (`transcrire.py`), bandes longue et YouTube (`outils/shorts/voix_short.py` : pauses resserrées, D retiré), repères mot à mot (`outils/shorts/recaler.py`) dans `kit/shorts/voix/` ; musique et effets dans `kit/shorts/son/` | `studio-faceless:sound-manager` (validé sur AA, 03/11/2026) |
| Fiche de style du short, tirée de la bibliothèque `${CLAUDE_PLUGIN_ROOT}/vendor/lemo-opuscar/` (`agents/art-director.md`, phase « fiche de style ») | `studio-faceless:art-director`, puis validation du propriétaire (validé sur AA, 03/11/2026) |
| Préparer le reste du kit shorts (`episodes/<id>/kit/shorts/`) : médias, filigrane, gabarit vertical, un brief par short | Claude principal |
| Monter jusqu'à `render.sh`, un short par mission | `studio-faceless:shorts-producer` |
| Rendu, contrôles, planche | Claude principal |
| Légendes et crédits par plateforme | Claude principal prépare ; le propriétaire publie |

## Méthode, dans l'ordre
1. **Choisir les boucles** dans le film approuvé : des boucles complètes (enjeu, question, retournement), avec une relance précise vers le film. Voir `references/ecriture.md` § 1. En priorité, les boucles sur un objet ou un rituel visible du film, avec un titre « Why… » (validé sur AA, 26/10/2026, `${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` § 5) ; le rythme de publication se décide après le pilote.
2. **Écrire le hook, le script et le pont.** Voir `references/ecriture.md` § 2 à 4.
3. **Fiche de style, puis kit et brief.** La fiche validée par le propriétaire passe dans le brief (ligne `style`). Voir `references/brief-short.md`.
4. **Monter** en 1080×1920 avec HyperFrames : le hook dès la première image, sous-titres mot à mot sans changement d'échelle, recomposition verticale, logo discret de la chaîne, carton final qui sert de pont vers le film, zones de sécurité des plateformes (YouTube Shorts, TikTok, Facebook Reels). Voir `references/montage-vertical.md` et `references/plateformes.md`.
5. **Contrôler** : `references/montage-vertical.md` § Contrôles et `references/ecriture.md` § 5.
6. **Tenir le journal des shorts** de l'épisode (`episodes/<id>/SHORTS_JOURNAL.md`) : hooks retenus, plateformes, et mesures à J+2 et J+7. Les noms des mesures sont dans `references/plateformes.md`.

## Refus permanents
- Hook vague (« You won't believe… ») ou mensonger ; promesse que le short ne tient pas.
- Information retenue pour forcer le clic : un short sans apport réel.
- Retournement fabriqué ; fait sans source ; émotion, pensée ou citation prêtée sans source à une personne réelle.
- Le mot « addiction » ; une affirmation neuroscientifique sans source.
- Noir, fondu, logo ou signature avant le hook.
- Texte animé en échelle ; effet diaporama.
- Média sans licence ni provenance ; image générée par IA.
- Publier, téléverser ou se connecter à un compte.

## Livrables types
- `episodes/<id>/SHORTS_vN.md` : boucles candidates, hooks, scripts et ponts (`PROPOSÉ`, puis choix du propriétaire).
- `episodes/<id>/production/short-0N-vM/` : projet HyperFrames, `render.sh`, `README.md`, `PROVENANCE.md`.
- Deux MP4 1080 × 1920 par short : YouTube (moins de 60 s), TikTok et Facebook (65 à 85 s).
- Une fiche de légendes par plateforme : crédits photo (jamais à l'écran) et mention de la voix IA, déclarée partout.
- `episodes/<id>/SHORTS_JOURNAL.md`.

Origine de la méthode : étude AA de la boucle addictive de Kallaway.
