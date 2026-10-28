# Description, chapitres, crédits, commentaire épinglé, SRT, réglages

Modèle réel : le dossier de publication de l'E003 d'AA (description de 3 964 caractères, deux réponses au commentaire épinglé), gardé dans les archives AA. Depuis le 19/10/2026 (validé sur AA), sans ses sources : voir le point 6.

## Description, dans cet ordre
1. **Ligne 1** : la scène concrète (lieu, date) et la question du film. Elle porte la promesse et la requête principale, dite naturellement (exemple AA : « Why does a rival's defeat feel this good? »). `[Observé]` Ce sont les lignes visibles avant « …more ».
2. **Ligne 2** : le parcours du film, avec 2 ou 3 mots de la longue traîne, sans liste de mots-clés (`[Officiel]` aide 146402 : spam).
3. Si utile, une ligne sur le phénomène nommé (exemple AA, E003 : « GORFing »).
4. **CHAPTERS** (ci-dessous).
5. **Note sur la science**, si le film rapproche des études d'une scène qu'elles n'ont pas mesurée : petites études, autres pays, analogie et non preuve (`direction/LIGNE_EDITORIALE.md`).
6. **Pas de synthèse des sources** (validé sur AA, 19/10/2026, pour tous les épisodes). Ni section SOURCES dans la description, ni réponse de sources au commentaire épinglé, ni mission `studio-faceless:research` pour les compiler. Les sources restent dans `research/` et les fiches de narration de l'épisode.
7. **PHOTO CREDITS**, regroupés par auteur et licence, puis la ligne des licences, le crédit de la photo de la miniature, et le renvoi à la réponse 1.
8. **AUDIO** : voix off, voix jouées, musique et effets générés (outil nommé) ; ambiances et foules « illustrative, not recordings of the events shown » ; musique de l'outro ; textures.
9. Ligne de chaîne (texte fixe de la chaîne, dans `marque/README.md`), puis 1 à 3 hashtags (ceux de la chaîne : `direction/ECARTS.md` ou `marque/README.md`).

Contrôles : 5 000 octets, aucun chevron (`publication.py verifier`). Pas de lien raccourci ni d'appel à un autre réseau sans demande du propriétaire.

## Chapitres
- `[Officiel]` Aide 9884579 : `0:00` d'abord, au moins 3 chapitres, chacun d'au moins 10 s, dans l'ordre.
- **Calcul** : `publication.py chapitres <master>.log.txt --titre seq1="…" …`. Une séquence du journal = un chapitre ; noir, logo, signature, outro et appel sont exclus (`--ignorer` pour un autre nom). Le début est arrondi à la **seconde supérieure** pour que le clic tombe dans la séquence, pas dans le noir ou la signature qui la précède (exemple AA, E003 : séquence 2 à 92,63 s → `1:33`).
- **Chapitre interne** (vrai changement de sujet dans une longue séquence) : temps du mot dans la bande voix (`publication.py mot mots-seqN.json "premiers mots"`), plus le `data-start` de la piste voix dans l'`index.html` de la séquence, puis `--repere seqN:SECONDES="Titre"`. N'utiliser que des repères recalés sur les vrais départs de la voix (`${CLAUDE_PLUGIN_ROOT}/outils/controle/README.md`, `transcrire.py`).
- **Titres** dans la langue de la chaîne, courts, concrets ; une citation du film entre guillemets est possible (exemple AA, E003 : « "Brazil, tell me how it feels" »).

## Crédits
- **Entrée** : les `PROVENANCE.md` des séquences du master, de la signature, de l'outro et de l'appel. Lecture lourde : la confier à `studio-faceless:research` avec un contrat de mission ; il renvoie la liste regroupée et la liste complète.
- **CC BY** (2.0, 3.0, 3.0 BR, 4.0) : auteur tel qu'il demande à être crédité, source (Wikimedia Commons, Flickr…), licence avec son lien, et la mention des modifications (« adapted: cropped, blurred, tinted, animated »). Domaine public et CC0 : crédités par courtoisie.
- Aucune licence en attente ni exclue (`controle.py licences`).
- La photo de la miniature est créditée à part.

## Commentaire épinglé et réponses
- **Commentaire** : une question honnête, liée au film, à laquelle chacun peut répondre ; le renvoi aux crédits ; l'invitation à signaler une erreur (« we'll pin the correction »). `[Hypothèse]` Il ouvre la discussion ; aucun effet de classement promis.
- **Réponse 1** : liste complète des photos (auteur, licence, ce que montre la photo, date, nombre).
- Pas de réponse de sources (validé sur AA, 19/10/2026, ci-dessus).
- Publiés par le propriétaire après la mise en ligne, dans cet ordre.

## Sous-titres (SRT)
- Écrits depuis le **texte vérifié** des fiches de narration, jamais depuis une transcription automatique ; noms propres exacts (exemple AA : Maracanã, Götze).
- Temps : repères mot à mot recalés de chaque bande voix, plus le `data-start` de la voix dans la séquence, plus le début de la séquence dans le journal du master.
- `[Observé]` Conventions courantes : 42 caractères par ligne et 2 lignes au plus, 1 à 7 s par sous-titre, aucun chevauchement. Les voix jouées sont sous-titrées comme dites.
- Fichier `PUBLICATION_vN.en.srt` (le suffixe de langue suit la langue de la chaîne), UTF-8 ; contrôle `publication.py verifier … --srt`.
- `[Folklore écarté]` Effet sur le classement : on les fait pour l'accessibilité et le public non natif.

## Réglages à la mise en ligne (rappels pour le propriétaire, aucune action de Claude)
- **Contenu modifié ou synthétique** (case de YouTube Studio, `[Officiel]`) : la recommander quand le film contient des voix jouées sur des paroles réelles, des foules ou sons générés sur des photos réelles, ou toute scène réaliste modifiée. Relire la formulation de Studio au moment de cocher ; la décision est au propriétaire.
- **Langue** : vidéo, titre et description dans la langue de la chaîne (`[Officiel]` aide 4792576 pour la langue et les traductions) ; sous-titres : le SRT, dans la même langue.
- **Générations ElevenLabs** : sous forfait payant (selon l'aide d'ElevenLabs, le plan gratuit n'a pas de licence commerciale).
- **Audience** (« conçu pour les enfants » ou non) et catégorie : choix du propriétaire.
- **Miniature** : la version validée ; test éventuel selon `studio-faceless:thumbnail-strategist`.
