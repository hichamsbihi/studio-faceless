# Contrôles mesurables et planche « flux »

Les mesures se font sur le **PNG livré**, jamais sur la source HTML seule. Elles ne valent pas validation : seul le propriétaire valide, et la fiche sépare toujours mesures et regard humain. Script : `scripts/miniature.py` (lancer avec `python -B`).

## 1. Liste de contrôle
| # | Contrôle | Comment | Seuil |
|---|---|---|---|
| 1 | Format | `miniature.py mesure IMAGE` | PNG ou JPEG, au moins 1280×720, 16:9, moins de 2 Mo (aide YouTube 72431) |
| 2 | Aperçus réduits | `miniature.py planche SORTIE.png IMAGE...` : chaque variante en 320×180 et 168×94 | À 168×94 : les mots principaux se lisent, le visage se reconnaît, la contradiction se comprend |
| 3 | Coin inférieur droit | Sur la planche, la durée simulée « 12:34 » ; dans la source, la zone x ≥ 1080 et y ≥ 620 | Ni texte, ni visage, ni pointe de flèche sous la durée |
| 4 | Contraste du texte | `miniature.py contraste #TEXTE #FOND` pour un aplat ; `contraste #TEXTE --image IMAGE --zone x,y,l,h` sur une bande de fond collée aux lettres, sans les lettres | Au moins 4,5:1 pour les mots principaux ; 3:1 minimum (gros texte, WCAG 2.2, critère 1.4.3) ; le script juge sur les 5 % de pixels les plus défavorables |
| 5 | Fonds clair et sombre | La planche montre chaque variante sur le blanc et le noir `#0F0F0F` de YouTube | Les bords de l'image ne se fondent dans aucun des deux fonds |
| 6 | Économie | Compter dans la source | 3 éléments à lire au plus (sujet, texte, flèche) ; 2 à 4 mots |
| 7 | Flèche | Distance entre la pointe et le sujet, à l'œil sur le PNG ou par les coordonnées | Elle désigne sans entrer dans le sujet |
| 8 | Promesse | Fiche de concept | Complète le titre sans le répéter ; tenue dans l'accroche (minutage noté) |
| 9 | Exactitude et droits | `PROVENANCE.md` du dossier | Personnalité publique ; photo réelle, source, licence et crédit YouTube consignés ; rien repris d'un concurrent ; aucune image générée ; aucune émotion inventée |

Après chaque série de captures : `python -B ${CLAUDE_PLUGIN_ROOT}/outils/controle/controle.py chrome` doit répondre 0.

## 2. Planche « flux » (analyse interne)
But : voir si nos variantes ressortent **au milieu des miniatures de la niche**, comme sur l'accueil de YouTube.
- `miniature.py planche SORTIE.png NOS_VARIANTES... --flux DOSSIER_VOISINES` : grille de 4 colonnes en 320×180, sur fond clair puis sombre, nos variantes réparties parmi les voisines, durée simulée et barres de titre grises ; les rangs de nos variantes sont écrits sous la grille.
- **Voisines** : captures d'écran fournies par le propriétaire (sa propre page d'accueil ou une recherche), ou plus tard un rapport de veille de la chaîne. Claude n'en télécharge ni n'en aspire aucune.
- **Usage interne seulement** : la planche ne se publie pas, et aucune miniature voisine n'entre dans une production.
- Questions à se poser, sans conclure à la place du propriétaire : laquelle attire l'œil en premier ? la nôtre se distingue-t-elle par sa couleur et sa composition ? reste-t-elle lisible ? dit-elle le sujet ?

## 3. Fiche de contrôle (gabarit)
```markdown
# Contrôle de la miniature <EPISODE> vN-n « MOTS » (JJ/MM/AAAA)
Fichier : `episodes/<id>/miniatures-vN/<png>` · Titre : « ... » · Statut : PROPOSÉ | VALIDÉ (le propriétaire, date)

## Mesures
| # | Contrôle | Mesure | Verdict |
|---|---|---|---|
| 1 | Format | 1280×720, PNG, 0,76 Mo | OK |
| ... | | | OK / À SURVEILLER / ÉCHEC |

## Observations (Claude, sur la planche)
- ...

## Regard du propriétaire
Non fait (ne jamais le déclarer fait sans sa réponse).
```
