# Signaux, limites et sources

« Aide NNN » = `support.google.com/youtube/answer/NNN`. « Blog 2021 » = « On YouTube's recommendation system », C. Goodrow, blog YouTube, 15/09/2021. « API » = documentation de l'API YouTube Data v3, ressources `videos` et `playlists`. Faits relevés le 16/10/2026 par l'étude AA des skills YouTube (§ 2) ; les relire à la source si une règle semble avoir changé.

## Hiérarchie des signaux, du plus fort au plus faible
1. **Satisfaction et temps de visionnage.**
   - `[Officiel]` Blog 2021 : des enquêtes notent les vidéos de 1 à 5 étoiles ; seules les notes 4 et 5 comptent comme « valued watchtime ». Le clic seul ne suffit pas.
   - `[Officiel]` Aide 141805 : l'accueil et les suggestions montrent une vidéo qui a intéressé et satisfait des spectateurs semblables ; une vidéo faible ne pénalise pas directement la chaîne.
   - `[Officiel]` Aide 16090438 et 141805 : la recherche combine pertinence (titre, tags, description, contenu), engagement (temps de visionnage) et qualité, avec de la personnalisation ; pas un classement par vues.
   - Conséquence : le film lui-même fait l'essentiel. Le dossier ne doit jamais attirer un public que le film décevra.
2. **Promesse du titre et de la miniature.**
   - `[Officiel]` Aide 7628154 et 16767369 : la moitié des chaînes et des vidéos ont un CTR entre 2 % et 10 % ; il baisse quand les impressions montent ; il se lit par source de trafic.
   - `[Officiel]` Aide 13861714 et 16391400 : Test & Compare montre jusqu'à 3 miniatures ou titres et désigne le gagnant au **temps de visionnage**, pas au CTR.
   - `[Officiel]` Aide 9314415 : l'« intro » est la part des spectateurs encore là à 30 s. La promesse doit être tenue avant.
3. **Description.**
   - `[Officiel]` Aide 16090438 : la description fait partie de la pertinence. Aide 12948449 : conseils de rédaction de la description.
   - `[Observé]` Seules les premières lignes s'affichent avant « …more » (page de lecture, résultats de recherche) : elles portent la promesse et la requête principale.
4. **Chapitres.**
   - `[Officiel]` Aide 9884579 : navigation dans la vidéo ; règles de format ci-dessous.
   - `[Observé]` Google peut afficher les chapitres comme « moments clés » dans sa recherche.
5. **Tags, en dernier.**
   - `[Officiel]` Aide 146402 : rôle « minimal » dans la découverte, sauf pour les fautes d'orthographe courantes. Mettre trop de tags dans la description est contraire au règlement sur le spam.
6. **Hashtags.**
   - `[Officiel]` Aide 6390658 : YouTube affiche les 3 premiers hashtags de la description ; au-delà de 60, tous sont ignorés ; un hashtag sans rapport avec la vidéo peut être retiré.

## Limites officielles (contrôlées par `${CLAUDE_PLUGIN_ROOT}/outils/controle/publication.py`)
| Champ | Limite | Source |
|---|---|---|
| Titre | 100 caractères, ni `<` ni `>` | API `videos` |
| Description | 5 000 octets UTF-8 (un « — » ou un « ã » compte plusieurs octets), ni `<` ni `>` | API `videos` |
| Tags | 500 caractères au compte de YouTube : virgules comprises, et 2 guillemets ajoutés à chaque tag qui contient une espace | API `videos` (le script retrouve les 417 caractères calculés pour l'E003 d'AA ; jamais comparé à l'affichage de Studio) |
| Chapitres | premier à `0:00`, au moins 3, chacun d'au moins 10 s, dans l'ordre | Aide 9884579 |
| Hashtags | 3 affichés ; plus de 60 = tous ignorés | Aide 6390658 |
| Titre de playlist | 150 caractères | API `playlists` |

Repères qui ne sont pas des limites : titre lisible en entier vers 60 à 70 caractères selon l'écran `[Observé]` ; commentaire limité à 10 000 caractères `[Observé]`, non vérifié dans l'aide.

## Folklore écarté
- `[Folklore écarté]` Mot-clé obligatoire dans les 40 premiers caractères du titre.
- `[Folklore écarté]` Nombre « optimal » de tags ; densité de mots-clés dans la description.
- `[Folklore écarté]` Meilleure heure ou fréquence de publication : aide 141805, aucun lien établi avec la croissance.
- `[Folklore écarté]` « +20 à 50 % de CTR » avec telle formule de titre : aucun chiffre sans source.
- `[Folklore écarté]` Les sous-titres font monter dans le classement : non confirmé par YouTube. On les fait pour l'accessibilité et le public non natif.
- `[Folklore écarté]` Volumes de recherche des outils tiers : estimations en boîte noire, jamais annoncées.

## À surveiller dans Studio (étude AA, 16/10/2026)
- Depuis le 24/08/2026, une vue publique compte dès le lancement ; CTR, durée moyenne et rétention restent calculés sur les **vues engagées** : on compare nos épisodes en vues engagées.
- Remplacement automatique d'une miniature peu performante annoncé « later this year » (TechCrunch, 23/09/2026, non vérifié à la source) : vérifier qu'aucune miniature n'est remplacée sans nous.

Idée des étiquettes de preuve : TubeAlfred (`tubealfred/youtube-skills`, MIT), reformulée ; aucun texte repris.
