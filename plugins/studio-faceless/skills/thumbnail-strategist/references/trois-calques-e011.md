# Méthode en trois calques (E011 d'AA) : la fabrication du visage et un mot

**Statut** : `VALIDÉ` (Hicham, 03/11/2026), après le choix de la miniature v2-3 de l'E011 d'AA. Depuis le 04/11/2026, c'est la fabrication du gabarit « le visage et un mot » (`gabarits.md` § 2), l'un des trois gabarits par défaut ; elle avait remplacé le fond uni de la grammaire de l'E003 (`grammaire-e003.md`), jugé « pas captivant », qui reste en secours. Le bandeau de contexte ne s'ajoute que si le concept en a besoin (`gabarits.md` § 3). Les écarts de la chaîne sont dans `direction/ECARTS.md` (priorité : `REGLES_STUDIO.md` § Priorité). Elle est appliquée par `studio-faceless:publisher`, et la fabrication suit `fabrication.md`.

## 1. Ce qui a échoué avant
- **Essais du propriétaire dans un outil d'image IA (E011)** :
  - visage redessiné, ou qui a l'air collé ;
  - fautes, et du texte posé sur une tête ;
  - trois points d'attention ;
  - un objet sous la durée, en bas à droite ;
  - des couleurs ternes.
- **Miniatures HTML sur fond uni** : déjà jugées « pas captivantes ».
- **E001** : un fan anonyme fait par IA, avec un texte vague, a donné environ 2 % de CTR (`grammaire-e003.md`, leçons).

## 2. Les trois calques
1. **Fond**
   - Une vraie photo de l'événement, libre ou du domaine public, déjà vibrante (exemple AA : les faisceaux de lumière de la mi-temps).
   - Floutée de 3 px et saturée, avec un voile sombre du côté du texte.
2. **Visage**
   - Un vrai visage célèbre, détouré par `remove-background` (`fabrication.md` § 3, voie A), sans aucun pixel redessiné.
   - Il fait environ 40 % de la hauteur.
   - De profil, son regard va vers le texte ; sa main ouverte peut « présenter » la question.
3. **Texte**, en HTML (Montserrat 900)
   - Une question de 3 mots qui nomme la star, vraie et dite dans le film (exemple AA : « WHO PAYS JAY-Z? »).
   - Le mot clé dans la couleur complémentaire du fond (exemple AA : vert `#2FD27A` sur violet).
   - Un bandeau or, sur une ligne, pour le contexte (exemple AA : « NEXT HALFTIME HEADLINER »).

## 3. Règles
- **Chiffres** : jamais « $0 », ni aucun chiffre, près d'une personne dont le cachet n'est pas public.
- **Scènes** : aucune scène inventée (exemple AA : un bras qui cache un sac d'argent).
- **Un seul point d'attention.** Le regard et la main mènent à la question. Une flèche ne s'ajoute que si elle ne crée pas un second point d'attention.
- **Contraste** : mesuré sur le fond sans les lettres ; sur les 5 % de pixels les plus défavorables, au moins 4,5:1 (`controles.md`, contrôle 4).
- **Aperçus** 168×94 et 320×180 ; coin inférieur droit libre.
- **Bandeau** : un bandeau de deux lignes ne se lit pas sur mobile.
- **Variantes** : au moins deux, pour Test & Compare (`test-et-journal.md`).

## 4. Licences
- Les portraits de Pinterest ou d'une agence ne sont pas libres : prendre Commons (CC BY ou domaine public).
- Une ligne de crédit va dans la description (skill `studio-faceless:youtube-seo`, `${CLAUDE_PLUGIN_ROOT}/skills/youtube-seo/references/description-et-credits.md`), sauf écart de la chaîne.

## 5. Ce qui reste de la grammaire de l'E003
- Un visage célèbre réel, sous licence, qui montre ce que la photo montre.
- 2 à 4 mots en Montserrat 900, loin du coin inférieur droit.
- Un logo discret ; rien de repris d'un concurrent.
- Une flèche, si elle est gardée, ne doit jamais entrer dans le sujet.
