# Choisir le sujet (`PROPOSÉ`, Méthode v1, étude AA, bloc 1)

Les règles citées (`REFERENTIEL`, `METHODE_RECIT`) sont les règles par défaut du plugin (`${CLAUDE_PLUGIN_ROOT}/referentiels/`) ; les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent.

## 1. Grille (celle de l'audit E007 d'AA)
Six critères notés de 1 à 5. Trois comptent double : demande, nom connu, médias. Maximum 45.

| Critère | Ce qu'on regarde |
|---|---|
| Demande (double) | la question se pose en ce moment, ou revient sans cesse |
| Nom connu (double) | une entité que le spectateur reconnaît en cinq mots (exemple AA : un club, un joueur ou une compétition) |
| Contradiction | deux états opposés de la même entité, ou un fait qui semble ne pas avoir de sens |
| Médias (double) | des images réelles gratuites et sans filigrane du moment clé (`REFERENTIEL` § 2 bis), dont de la vidéo réelle |
| Place libre | aucune grande chaîne n'a traité la même question avec succès dans les 12 derniers mois, ou on a un angle nettement différent |
| Accroche et durée | la question tient 8 à 10 min, en couches, avec un renversement |

**Seuil** : 33/45 au moins, et aucun critère double sous 3. Le propriétaire choisit parmi les trois premiers. Exemple AA : l'E007 avait 38/45 (audit du 23/10/2026).

**Une chaîne peut écarter ce contrôle dans `direction/ECARTS.md`** (critère « place libre » et recherche de concurrence du § 4, point 3) : un sujet déjà traité ailleurs n'est alors jamais exclu, et l'écart dit comment le critère se note. `studio-faceless:strategist` fait de même : il ne recoupe avec d'autres chaînes que si `ECARTS.md` le demande (exemple AA : jamais, validé le 02/11/2026).

## 2. Vérifications en plus (prompt d'une autre chaîne, transposé)
- **Compris par un non-initié** (éliminatoire, validé sur AA, 26/10/2026, `METHODE_RECIT.md` § 4, Sujet et titre) : la question se comprend sans connaître le milieu (exemple AA : ni le club ni la ligue), et l'anomalie se montre en une image ; sinon, on reformule l'angle ou on écarte le sujet.
- **Un motif écrit** par l'acteur lui-même : règle, contrat, décision, déclaration. C'est ce qui permet une révélation neutre.
- **Au moins trois révélations et un renversement** possibles.
- **Le moment** : l'actualité rend la question brûlante, et le mécanisme restera vrai dans six mois. Les phrases d'actualité sont marquées [MAJ].
- **Personnes** : on ne prête aucun motif sans source. Une procédure en cours s'attribue (« the commission found », « X deny… and are appealing »).

## 3. La promesse
- Le titre pose la question, ou le pourquoi caché, en 60 caractères au plus.
- Une entité connue ou un objet concret ; aucun montant d'argent au titre. Une question au titre seulement si l'objet est fort.
- **Forme par défaut** (validé sur AA, 26/10/2026) : « Why… » sur un fait observable (lieu, règle, record, objet), jamais sur un sentiment ; environ 7 mots ; aucun mot tout en majuscules.
- **Format guide** (essai validé sur AA le 26/10/2026) : un épisode au titre « Every [x] explained », porté par une question centrale et une enquête, jugé sur ses chiffres avant toute série.
- La miniature montre la contradiction sans répéter le titre, et n'affirme que ce que le film montre (`studio-faceless:thumbnail-strategist`).
- La promesse est tenue dans les 30 premières secondes. Le sujet du titre est à l'écran ou nommé dans les 5 premières.
- **Essai en cours sur AA** (`PROPOSÉ`, 02/11/2026) : l'angle d'un sujet connu se formule comme une nouveauté posée contre la croyance courante (méthode « Illusion of Novelty », protocole de bilan : `recit-retention.md` § 8).
- Trois titres et trois miniatures peuvent passer en Test & Compare avant de juger un sujet.

## 4. Repérer un sujet qui surperforme et en reprendre le principe (`PROPOSÉ`)
Écrit sur AA le 28/10/2026 à la demande du propriétaire (Q74), d'après la recherche du 26/10 pour l'E009. Exemple complet AA : la veille du 26/10/2026 (étude AA).
1. **Vivier** : d'abord la banque de sujets de la chaîne (`direction/BANQUE_SUJETS.md`, s'il existe ; tenue par l'agent `strategist`) : ses sujets sont déjà vérifiés, avec faits et liens, et on ne refait pas leur recherche, on recoupe seulement ce qui est marqué « résumé » ou « secondaire » (validé sur AA, 02/11/2026). Puis la veille (`docs/veille/`), les candidats non retenus des propositions de sujets précédentes, les bilans des épisodes publiés.
2. **vidIQ, seulement sur demande du propriétaire** (environ 60 crédits pour une recherche complète) :
   - les chaînes de la niche : `similar_channels` à partir des chaînes de référence de la chaîne (`direction/LIGNE_EDITORIALE.md`) et par description de la niche, plus les chaînes de `docs/veille/donnees/`. Jamais à partir de la nôtre : vidIQ peut la classer dans une autre niche (exemple AA : entraînement et science du sport) ;
   - les vidéos qui surperforment (`outliers`) : sur la liste des chaînes, puis par thème (format long, 6 mois, 500 k abonnés au plus, 50 000 vues au moins). Les recherches par thème ramènent du bruit ;
   - le ratio ×N mesure la portée, ni le taux de clic ni la rétention, et grimpe vite sur les petites chaînes : regarder aussi les vues et la tendance.
   - **garde-fous** (validé sur MM, 28/10/2026 ; proposé au plugin 0.3.0, PROPOSÉ) : vidIQ en lecture seule, aucune connexion de chaîne, aucune action sur YouTube ; chaque appel coûte 5 crédits et `vidiq_balance` est gratuit, donc vérifier le solde avant un lot et annoncer le coût du lot ; éviter `vidiq_channel_stats`, dont la sortie (statistiques quotidiennes) est très lourde pour le contexte, `vidiq_channel_videos` suffisant pour les médianes et les percées ;
   - **saturation en requêtes courtes** : des requêtes longues et précises (« why Iceland produces aluminium without bauxite ») sont revenues vides ; la contre-épreuve en 3 ou 4 mots a changé deux verdicts. Toujours doubler une requête vide ou mince par une requête courte ;
   - **formats mêlés** : Shorts, extraits de journal télévisé et directs comptent dans les vues ; lire la durée avant de conclure (le verdict d'un sujet tenait à un extrait de 50 s).
3. **Concurrence** de chaque candidat : une recherche triée par vues (`youtube_search` de vidIQ, ou l'API YouTube Data sur les vidéos de plus de 3 min). Un sujet déjà gagné par une grande chaîne demande un angle nettement différent (critère « place libre »), sauf si la chaîne a écarté ce contrôle dans `direction/ECARTS.md` (§ 1).
4. **Reprendre le principe, jamais la vidéo** :
   - on garde ce qui a fait le succès : la question, l'anomalie, l'objet concret, la forme du titre ;
   - l'angle, la question précise, les faits (vérifiés par `studio-faceless:research`), le récit et la mise en scène sont les nôtres ;
   - on ne reprend ni leur texte, ni leurs images, ni leur découpage ; 12 mots cités au plus (`studio-faceless:regarder`).
5. **Au besoin, faire regarder la vidéo de référence** par `studio-faceless:regarder` (Gemini) pour isoler le principe : promesse, ouverture, relances.
6. **Noter** les 5 à 8 candidats (grille du § 1, test du non-initié du § 2, promesse du § 3), puis donner les trois premiers au propriétaire.
