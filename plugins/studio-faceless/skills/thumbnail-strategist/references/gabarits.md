# Gabarits et planche de la niche

VALIDÉ, Hicham, 04/11/2026 (« tu mets tout ça dans thumbnail-strategist »), après une étude faite sur AA : ses miniatures plafonnaient vers 1,5 % de taux de clic. Ce fichier donne la grammaire par défaut des miniatures (`SKILL.md`, méthode, étapes 3 et 4).

## 1. Ce que la planche a montré (AA, 04/11/2026)
- **Matière** : 81 miniatures.
  - Six chaînes de référence du sport expliqué : Tifo Sports, Tifo Football, Secret Base, Athletic Interest (étudiée, jamais copiée), JxmyHighroller, Thinking Basketball. Pour chacune, les 8 longues au plus fort ratio de vues et les 4 au plus faible.
  - Toutes les longues d'AA.
  - Ratio : vues ÷ médiane des 30 longues voisines. Il mêle sujet, titre et miniature : ce sont des corrélations, pas des preuves.
- **En haut** :
  - **un grand chiffre, souvent en contraste** (« 82,500 < 107,601 », « £116M », « $2,500 / $2,500,000 ») ;
  - **un schéma d'une seule idée** (carte, « EASY → HARD », avant/après, grille) ;
  - **un seul visage**, grand et expressif, quand la star est l'accroche ;
  - un point focal, un fond uni saturé, 1 à 4 mots, plus souvent une affirmation qu'une question.
- **Chez AA aussi** : ses trois meilleurs ratios sont ses seules miniatures menées par un chiffre (« 982/1000 », « 94% », « 6 TITLES / 6th TIER ») ; les autres sont nettement plus bas.
- **En bas** :
  - plusieurs visages ou un collage ;
  - deux animateurs au micro ;
  - un dessin d'action sans idée lisible ;
  - du texte en plusieurs blocs ;
  - un gabarit fixe sans concept : le même gabarit se retrouve en haut et en bas, c'est le mot qui fait la différence.
- **Preuves publiques** :
  - Test & Compare juge le gagnant sur la part du temps de visionnage et demande des variantes très différentes ([aide YouTube](https://support.google.com/youtube/answer/13861714)) ;
  - une émotion forte et vraie va avec plus de vues (16 215 vidéos, *J. Bus. Res.* 2024, [lien](https://scholars.ln.edu.hk/en/publications/clicks-for-money-predicting-video-views-through-a-sentiment-analy/)) ;
  - aucune preuve chiffrée trouvée pour les couleurs, les flèches ou le contraste.

## 2. Les trois gabarits
Vraies photos et dessin en code seulement (cadre du skill) ; un concept de `promesse-et-concepts.md` choisit son gabarit.

1. **Le chiffre qui dément** (à essayer d'abord : c'est le seul motif qui marche aussi chez AA).
   - Un ou deux nombres géants, tirés du script et sourcés : un contraste (« < », « vs »), un avant/après ou une part (« 94% »).
   - Un fond uni pris dans la palette de l'épisode, au plus un petit élément réel (photo détourée ou objet), 1 à 3 mots qui disent ce que le chiffre dément.
2. **Le schéma d'une idée**.
   - Une carte, une comparaison, un avant/après ou une grille, dessinés en code (SVG dans la page), avec de vraies données.
   - 2 à 4 mots ; aucune personne dessinée.
3. **Le visage et un mot** (fabrication : `trois-calques-e011.md`).
   - Un seul visage réel, sur 40 à 50 % du cadre, côté opposé au texte, regard vers le texte ou vers l'objet si la photo le permet.
   - L'expression est choisie parmi plusieurs vraies photos du même moment ; aucune émotion prêtée que la photo ne montre pas.
   - Vrai fond de l'événement, assombri ; 1 à 3 mots, une affirmation ou une question qui nomme la star (E011 d'AA : « WHO PAYS JAY-Z? ») ; le bandeau de contexte de `trois-calques-e011.md` seulement si le concept en a besoin.
   - Seulement quand la star est l'accroche.

**Les 3 variantes de l'étape 3** : une par gabarit quand le sujet le permet. Elles sont alors vraiment différentes, comme Test & Compare le demande.

## 3. Règles communes
- Un seul point focal. Pas de deuxième bloc de texte, de pastille, de drapeau ni de flèche, sauf si le concept en a besoin.
- Au plus 4 mots (refus du skill) ; le texte est vrai et dit dans le film ; il complète le titre sans le répéter.
- Lisible à environ 120 px de large (en plus des aperçus de `controles.md`) ; rien d'important dans les deux coins du bas (durée, chapitres).
- Les règles de style de la chaîne s'appliquent (`direction/ECARTS.md`). Sur AA : rien du style d'Athletic Interest (ni fonds orange et bleu roi, ni texte blanc à contour noir, ni flèches blanches).
- Une question n'est pas interdite, mais la planche penche vers l'affirmation : Test & Compare tranche.

## 4. La planche de la niche
À refaire quand le propriétaire la demande, ou avant de changer de gabarit.
1. **Données** : `strategist` relève 4 à 6 chaînes de référence par `outils/recherche/youtube_chaine.py` (ratio par vidéo), plus la chaîne elle-même.
2. **Planche** : `scripts/planche_niche.py` écrit un court script JavaScript ; le directeur l'exécute dans un onglet du navigateur intégré ouvert sur `https://i.ytimg.com/`, puis fait des captures. Les images s'affichent depuis YouTube et rien n'est enregistré. Un sous-agent ne voit pas ces images : la lecture revient au directeur.
3. **Lecture** : ce qui revient en haut et en bas, chez les autres et chez nous ; rapport dans `docs/rapports/` de la chaîne. Un gabarit nouveau entre ici sur décision du propriétaire.

## 5. Ce qui n'est pas adopté
- Le skill `youtube-thumbnail-design` (`qu-skills/skills`, lu en entier le 04/11/2026) : il génère la miniature par IA (FLUX, Seedream) avec le CLI payant `belt` d'inference.sh. Il demande `npx skills add` et une connexion à un compte, et aucun de ses chiffres n'a de source. Ses règles d'artisanat utiles sont reprises au § 3.
