# Plateformes : YouTube Shorts, TikTok, Facebook Reels (état au 19/10/2026)

Synthèse de la recherche `studio-faceless:research` faite sur AA le 19/10/2026.
- **Statuts** : Off. = aide ou documentation de la plateforme ; Obs. = guide ou étude de tiers, daté ; Hyp. = hypothèse.
- **Limite** : les aides TikTok et Facebook n'ont pu être lues que par extraits de moteur de recherche. À reconfirmer avant chaque changement de règle.
- **Sources** : liste en fin de fiche.

## Master unique (Hyp., compatible avec les trois)
- MP4, H.264 High, **1080 × 1920**, **30 i/s constants**, 8 à 12 Mb/s.
- AAC-LC 48 kHz stéréo, 128 kb/s au moins.
- GOP fermé de 2 s, index en tête (`-movflags +faststart`).
- **Deux versions par short** (validé sur AA, 19/10/2026) :
  - **YouTube : moins de 60 s**, de 35 à 50 s. Un Short de plus d'une minute qui porte une revendication Content ID est bloqué partout (Off. [Y2]).
  - **TikTok et Facebook : plus d'une minute**, de 65 à 85 s, pour l'éligibilité à la monétisation. Rester sous 90 s couvre aussi l'ancienne limite des Reels.
- **Conditions des programmes de monétisation** (TikTok Creator Rewards, monétisation Facebook) : abonnés, vues, pays de résidence, durée minimale. Non vérifiées le 19/10/2026 ; à vérifier avant d'y compter, car certains programmes ne sont ouverts que dans certains pays.
- Durées maximales : 3 min pour YouTube (Off.) ; 3 min, voire 10, pour TikTok (Off.) ; Facebook contradictoire, de 3 à 90 s, ou sans limite depuis juin 2025 (Off.).
- Durée conseillée : Facebook dit 10 à 30 s pour la portée (Off. [M6]) ; YouTube n'en donne aucune et renvoie aux courbes de rétention (Off.).
- **Niveau sonore** : plus fort que les films (validé sur AA, 19/10/2026) ; master à `shorts.master_lufs`, crête vraie au plus `shorts.crete_vraie_max_dbtp` (`${CLAUDE_PLUGIN_ROOT}/referentiels/seuils.json` ; VALIDÉ, Hicham, 04/11/2026, à l'écoute du short A de l'E011 d'AA ; `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md`). Aucune source sur la normalisation des trois plateformes n'a été lue : on mesure sur les premiers envois.

## Zones masquées par l'interface (1080 × 1920)
Aucune plateforme ne publie de marges pour la publication non sponsorisée ; les chiffres viennent des gabarits publicitaires (Obs., contradictoires).

| Plateforme | Haut | Bas | Gauche | Droite |
|---|---|---|---|---|
| YouTube Shorts | 288 | 672 | 48 | 192 |
| TikTok | 240 | 660 | 120 | 120 |
| Facebook Reels | 269 | 672 | 65 | 65 |

**Zone sûre commune de départ** (Hyp.) : haut 288, bas 710, gauche 120, droite 240. Soit **x de 120 à 840 et y de 288 à 1210** (environ 720 × 920 px).
- Hook, sous-titres, preuve à l'image et filigrane restent dans cette zone.
- L'image peut déborder ; le texte et les visages, non.
- À vérifier sur un téléphone avec un envoi privé (le propriétaire) : l'interface Shorts a changé en juin 2026 (mode « Clear Screen », Obs.).

## Pont vers le film
| Plateforme | Ce qui marche | Statut |
|---|---|---|
| YouTube Shorts | **« Vidéo associée »** : lien cliquable vers une vidéo de notre chaîne, réglé dans Studio. Il exige les « fonctions avancées » (téléphone vérifié et historique, ou pièce d'identité) : **Le propriétaire vérifie l'éligibilité dans Studio.** | Off. [Y4][Y5] |
| | Les URL de la description et des commentaires d'un Short ne sont **pas cliquables** ; les mentions et les hashtags le sont. | Off. [Y6] |
| TikTok | Lien de profil : 1 000 abonnés ou compte Business. Le compte Business limite la musique de l'appli à la Commercial Music Library, ce qui ne nous gêne pas : notre musique est dans le fichier, avec sa licence. Un lien YouTube via Modifier le profil > Liens serait possible sans seuil. Les liens de légende et de commentaire ne sont pas cliquables. | Obs. [S4][T5] |
| Facebook Reels | Meta conseille des légendes **sans lien** pour la portée ; un lien en premier commentaire est possible. Les liens dans les publications non sponsorisées sont limités en 2026 pour les Pages non abonnées. | Off. [M5], Obs. [S6] |

Le pont repose donc d'abord sur **le nom de la chaîne dans le carton final et la question de la relance**. Les liens viennent en plus, quand la plateforme les permet.

## Mention d'IA (voix off synthétique)
- **Meta** : étiquette « AI info » exigée ; l'exemple officiel est précisément « a reel narrated with a realistic AI-generated voiceover » (Off. [M3]).
- **TikTok** : étiquette obligatoire pour l'audio IA réaliste (Off. [T3][T4]).
- **YouTube** : déclarer le contenu réaliste généré ou modifié (Attributs > « AI use »). La page ne traite pas explicitement d'une voix de synthèse non clonée. La musique générée par IA est citée parmi les cas à déclarer. Déclarer ne réduit ni l'audience ni la monétisation (Off. [Y7]).
- **Décision (validé sur AA, 19/10/2026)** : la voix IA est déclarée sur les trois plateformes, à chaque envoi.

## Crédits et légendes
- **Limites de texte** : YouTube, titre de 100 caractères et description de 5 000 (Off.) ; TikTok, légende de 2 200 caractères (Off., API) ; Facebook, aucune limite officielle trouvée.
- **Crédits CC BY** : **dans les légendes seulement, jamais à l'écran** (validé sur AA, 19/10/2026). Complets dans la description YouTube ; version courte dans les légendes TikTok et Facebook, sous 2 000 caractères.
- **Republication** : le même master est envoyé sur les trois plateformes, **depuis notre rendu**, jamais depuis un fichier téléchargé d'une autre appli (son filigrane ferait classer le short « non original » : Off. [S12][M5][Y11]).

## Mesures (journal de l'épisode, J+2 et J+7)
- **YouTube Studio** (Analytics > Contenu > Shorts ; Off. [Y8][Y9]) :
  - « How many chose to view » (vu ou passé) ;
  - « Stayed to watch » ;
  - « Engaged views » ;
  - « Average view duration » ;
  - « Subscribers » ;
  - « How viewers find your Shorts » ;
  - **« Viewers across formats »** : le chevauchement Shorts / vidéos, notre mesure de conversion.
- **TikTok** (Obs., noms à confirmer dans l'appli) : Average watch time, Watched full video, Retention rate, New followers, Traffic source type.
- **Facebook** : noms de l'interface à confirmer. API : `post_video_avg_time_watched`, `post_video_retention_graph`, `fb_reels_replay_count`, `post_video_followers`.

## Shorts et films longs (pour décider du volume)
- YouTube : publier des Shorts ne pénalise pas la chaîne ; les spectateurs ne passent pas toujours d'un format à l'autre (Off. [Y12]).
- Metricool 2026 (≈ 800 000 vidéos) : un volume **modéré** de Shorts va avec plus de vues longues (+47 %), un volume élevé avec moins (−26 %). C'est une corrélation, sans méthode publiée (Obs. [S8]).
- Aucune donnée publiée de conversion Shorts vers vidéo longue : on mesure la nôtre avec « Viewers across formats ».

## Sources
- **YouTube (aide)** : https://support.google.com/youtube/answer/ suivi du numéro :
  - [Y2] 15424877 ; [Y4] 14075157 ; [Y5] 9890437 ; [Y6] 13748639 ;
  - [Y7] 14328491 ; [Y8] 12942217 ; [Y9] 12220281 ;
  - [Y11] 12504220 ; [Y12] 16559651.
- **TikTok** :
  - [T3] https://newsroom.tiktok.com/en-us/new-labels-for-disclosing-ai-generated-content
  - [T4] https://newsroom.tiktok.com/more-ways-to-spot-shape-and-understand-ai-generated-content?lang=en-GB
  - [T5] https://ads.tiktok.com/business/en-US/blog/audio-library-royalty-free-music
- **Meta** :
  - [M3] https://www.meta.com/en-gb/help/artificial-intelligence/1783222608822690/
  - [M5] https://creators.facebook.com/blog/combating-unoriginal-content
  - [M6] https://creators.facebook.com/blog/making-it-easier-to-create-videos-on-facebook
- **Tiers** :
  - [S4] https://nealschaffer.com/how-to-add-links-to-tiktok-bio/
  - [S6] https://techcrunch.com/2026/09/15/meta-expands-subscription-push-with-new-ai-focused-plans/
  - [S8] https://metricool.com/youtube-shorts-algorithm/
  - [S12] https://www.tiktok.com/safety/en/policies-and-engagement/fyf-standards
- **Gabarits de zones masquées** : https://www.socialync.io/tools/safe-zones/youtube-shorts (relevé le 11/10/2026).
