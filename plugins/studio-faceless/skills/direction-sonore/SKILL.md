---
name: direction-sonore
description: Méthode de direction sonore des documentaires de la chaîne — contrat audio, repérage sonore (spotting) et feuille de repérage, couches, perspective et distance, ambiances sourcées, bruitages motivés, silences et respirations, J-cut, L-cut et ponts sonores, musique qui porte l'immersion et journal de cues (cue sheet), contrôle du mix livré (LUFS, true peak, mono, bande 1–4 kHz) et passes d'écoute. Use when planning, reviewing or checking the sound of a sequence, prototype or episode of the channel. Complète DIRECTION_AUDIO.md du plugin (règles par défaut, qui font foi sauf écart de la chaîne dans direction/ECARTS.md) et hyperframes-audio (mécanique HyperFrames) sans les remplacer.
---

# Direction sonore

Méthode et gabarits pour décider **ce que le son doit faire** dans un documentaire de la chaîne, puis le vérifier sur le fichier livré.

## Ordre de préséance
0. **Les écarts de la chaîne** (`direction/ECARTS.md`) l'emportent sur les règles par défaut du plugin ci-dessous.
1. **`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` fait foi** : décisions du propriétaire, voix, prise approuvée intouchable, dépenses, cibles de livraison (environ −16 LUFS, true peak ≤ −1,5 dBTP), constats HyperFrames 0.8.149, règles ElevenLabs. En cas d'écart avec ce skill, il l'emporte. Ne jamais recopier ses chiffres ailleurs que dans une mesure : y renvoyer.
2. **`hyperframes-audio`** : mise en œuvre dans la composition (pistes, automation, effets, groupes). Rappel du projet : les valeurs d'automation sont **absolues** et remplacent `data-volume`.
3. **Ce skill** : la méthode de conception et de contrôle, et les gabarits.
4. `media-use` n'est pas une source de sons pour la chaîne : ses effets fournis (whoosh, riser, glitch…) n'ont ni la provenance ni le registre voulus.

## Quand l'utiliser
- Préparer le son d'une séquence, d'un prototype ou d'un épisode (avant fabrication).
- Revoir un mix, diagnostiquer un défaut, préparer la note de contrôle d'un MP4.
- Ne pas l'utiliser pour générer de la musique ou des sons : toute génération passe par les règles de dépense de `DIRECTION_AUDIO.md` et l'accord du propriétaire.

## Méthode, dans l'ordre
1. **Contrat audio** de la séquence : rôle du son, hiérarchie d'écoute, sources disponibles et leurs droits, livrables, conditions d'écoute réellement disponibles. Gabarit : `references/gabarits.md`.
2. **Repérage** avant tout son : une ligne par événement ou lit sonore, avec sa fonction, son statut et sa source. On ne sonorise pas chaque action visible. Voir `references/reperage-et-couches.md`.
3. **Couches et perspective** : peu de couches sous la voix, une distance et un point d'écoute cohérents avec l'image et le récit. Voir `references/reperage-et-couches.md`.
4. **Relations son-image et transitions** : J-cut, L-cut, ponts, révélation par retrait, silences. Voir `references/transitions-et-silences.md`.
5. **Musique** : depuis le 15/10/2026 (validé sur AA), elle porte l'immersion de chaque séquence. Elle est choisie selon la situation, s'entend vraiment, et on repère ses entrées, retraits et silences voulus. Les niveaux sont dans `DIRECTION_AUDIO.md` § 2 et 3. Voir aussi `references/musique-a-l-image.md`.
6. **Mise en œuvre** dans HyperFrames : `hyperframes-audio` et la section HyperFrames de `DIRECTION_AUDIO.md` ; constats complémentaires dans `references/transitions-et-silences.md`. Depuis le 24/10/2026 (validé sur AA), la séquence ne porte que la voix : ces techniques s'appliquent au mix du film (`DIRECTION_AUDIO.md` § 3, `outils/montage/mix_film.py`), pas dans la composition de la séquence.
7. **Contrôle** du MP4 livré (mesures), puis passes d'écoute. Les mesures ne valident jamais l'écoute. Voir `references/controle-et-mesure.md`.

## Refus permanents (validés sur AA)
- Whoosh à chaque raccord, riser, impact ou « sting » de bande-annonce, musique décorative sans fonction de situation, battement de cœur.
- Foule en fond continu, ou effet sans image qui le justifie (validé sur AA, 15/10/2026 : « les SFX doivent être utilisés que si besoin »).
- Acouphène, effet « tunnel » ou audition intérieure attribués à une personne réelle.
- Voix, pas, souffle ou respiration d'une personne réelle fabriqués et présentés comme captés ; faux commentaire ; parole intelligible non authentifiée.
- Ambiance contextuelle (autre lieu, autre événement) ou son généré présentés comme le son de l'événement : toujours consigner « enregistrement contextuel » ou « génération illustrative ».
- Carve fréquentiel par défaut : seulement si un masquage est constaté. La musique, elle, est atténuée de 3 à 5 dB sous la voix (ducking doux, validé sur AA, 15/10/2026).
- Musique « à la manière de » un artiste ou d'un morceau existant ; nouvelle recherche musicale sans demande du propriétaire.

## Livrables types
- Contrat audio et feuille de repérage (dans le dossier de la séquence ou dans son storyboard).
- Registre des sons : provenance, licence et statut de chaque fichier, dans le `PROVENANCE.md` du projet.
- Journal de cues, si de la musique est utilisée.
- Note de contrôle audio : mesures d'un côté, écoute de l'autre, avec les statuts du `CLAUDE.md` racine.

Sources et licences des méthodes reprises : `SOURCES_ET_LICENCES.md`.
