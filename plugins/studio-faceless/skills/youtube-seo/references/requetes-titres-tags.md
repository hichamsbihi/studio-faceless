# Requêtes, titres, tags, hashtags, playlist

## Requêtes d'une nouvelle chaîne
- **Une requête principale**, dans la langue naturelle de la chaîne, telle qu'une personne la taperait (exemples AA : « why do fans celebrate rival losses », « how does a club go bankrupt »). Elle décrit le sujet du film, pas un mot-clé générique.
- **3 à 5 requêtes de longue traîne** : plus longues et plus précises (lieu, date, phénomène nommé, étude). Exemple AA, E003 : « glory out of reflected failure », « brazilians celebrated argentina loss ».
- **Éviter les requêtes et tags très populaires** (exemples AA : « football », « World Cup », un nom de star seul) : choix validé sur AA pour l'E003 (15/10/2026), repris ici par défaut. `[Hypothèse]` Une chaîne nouvelle a plus de chances sur des requêtes précises où peu de vidéos répondent vraiment (« content gaps ») que sur des requêtes tenues par les grosses chaînes.
- **Indices gratuits, tous datés dans le dossier** (« relevé le JJ/MM/AAAA ») ; aucun ne donne un volume :
  - `[Officiel]` onglet **Research** (Recherche) de YouTube Studio : recherches de notre audience et sur YouTube, « content gaps », sur 28 jours ; souvent vide pour une petite chaîne. Relevé par le propriétaire (connexion requise) ;
  - `[Observé]` **autocomplétion** de la barre de recherche YouTube : les suggestions montrent des formulations réelles, sans ordre de grandeur fiable ;
  - `[Officiel]` **Google Trends**, filtre « YouTube Search » : indice relatif (0–100) entre requêtes et dans le temps, jamais un volume ;
  - après publication : les vrais termes de recherche de nos vidéos dans Analytics (`apres-publication.md`).

  Claude ne consulte l'autocomplétion ou Trends que si le propriétaire le demande, en lecture seule et sans compte ; sinon le propriétaire fournit ses relevés.
- **Jamais de volume** : ni chiffre, ni « forte demande », ni score d'un outil tiers. On écrit « indice : la formulation apparaît dans l'autocomplétion (16/10/2026) ».

## Trois titres
- Une seule promesse, celle de la miniature, tenue avant 30 s. Pas de fait que le film ne montre pas.
- **Trois variantes vraiment différentes**, un titre par ligne dans le bloc :
  - A, la forme par défaut (validé sur AA, 26/10/2026, `${CLAUDE_PLUGIN_ROOT}/referentiels/METHODE_RECIT.md` § 4 Sujet et titre ; les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent) : « Why… » sur un fait observable (un lieu, une règle, un record, un objet), jamais sur un sentiment ; environ 7 mots, aucun montant. Les « Why » de sentiment de l'E001, de l'E003 et de l'E004 d'AA ont eu peu de vues `[Observé]`, sur une chaîne naissante : la part du titre n'est pas isolée ;
  - B, proche de la requête principale ;
  - C, le cas concret (lieu, date, personne publique au cœur du film).
- `[Officiel]` 100 caractères au plus. `[Observé]` L'essentiel dans les 60 à 70 premiers, souvent coupés au-delà. `[Folklore écarté]` Position obligatoire du mot-clé.
- Majuscules de titre selon la langue de la chaîne (anglaises sur AA), pas de capitales entières ni de ponctuation en rafale. Aucun hashtag dans le titre (il remplacerait ceux de la description au-dessus du titre `[Observé]`).
- Le propriétaire choisit. `[Officiel]` Les titres peuvent aussi passer en Test & Compare (aide 13861714), jugé au temps de visionnage.

## Tags (en dernier)
- `[Officiel]` Rôle minime (aide 146402) : y consacrer peu de temps.
- Contenu : la requête principale, les requêtes de longue traîne, le phénomène nommé, les variantes d'orthographe courantes (exemple AA : « Maracana » sans accent). Tous dans le sujet du film.
- Exclus : les mots très disputés seuls, les noms que le propriétaire a exclus pour l'épisode (contrôle `--exclure`), les noms ou marques absents du film, les tags de concurrents.
- `[Folklore écarté]` Nombre optimal. Seule limite : 500 caractères au compte de YouTube.

## Hashtags
- 1 à 3, en dernière ligne de la description, en `CamelCase` lisible (les hashtags de la chaîne sont dans `direction/ECARTS.md` ou `marque/README.md`). `[Officiel]` 3 affichés, plus de 60 = tous ignorés, hors sujet = retiré (aide 6390658).
- Plus larges que les tags mais jamais trompeurs. `[Hypothèse]` Leur effet sur la découverte est faible pour une chaîne nouvelle.

## Playlist
- Une playlist thématique de la chaîne (titre dans la langue naturelle de la chaîne, 150 caractères au plus, et une description d'une ou deux phrases) : la série dont l'épisode fait partie (les playlists de la chaîne sont dans `direction/ECARTS.md` ou `marque/README.md`).
- `[Hypothèse]` Elle aide le spectateur satisfait à enchaîner un autre épisode ; aucun effet de classement promis.
- Création et classement de la playlist : par le propriétaire dans Studio.
