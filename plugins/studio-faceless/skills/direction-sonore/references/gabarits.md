# Gabarits

À copier dans le dossier de la séquence (storyboard, `PROVENANCE.md`, `README.md`). Une case sans objet vaut « aucun ». Une information inconnue s'écrit « inconnu / à vérifier », jamais une valeur supposée.

## Contrat audio
```text
Séquence / version :
Rôle du son dans la séquence (une phrase) :
Hiérarchie d'écoute : voix off d'abord / archive parlante / ambiance / autre (préciser par passage si elle change)
Voix : prise approuvée (fichier, date) ou « pas encore de prise » ; transcription comparée au texte : oui / non
Sources disponibles et statut : archive exacte / enregistrement contextuel / génération illustrative ; licences
Musique : aucune / prévue (fonction en une phrase) / à décider par le propriétaire
Livrables : MP4 ; pistes séparées (voix, musique, ambiances, effets) ; autre
Cible : voir `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 3, sauf écart dans `direction/ECARTS.md` de la chaîne (ne pas la recopier autrement)
Écoute réellement disponible : le propriétaire au casque / petit haut-parleur / personne (le dire)
Risques connus : masquage, droits, prise modifiée, ambiance trop identifiable, autre
```

## Feuille de repérage
| # | Temps (entrée–sortie) | Déclencheur | Famille | Statut narratif | Synchro | Perspective | Matière | Fonction | Source et statut | Priorité |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 | 0,0–3,2 s | Plan large du lieu | Ambiance | Diégétique (contextuelle) | De fond | Lointaine | Foule, vent | Installer le lieu sans parole intelligible | Enregistrement contextuel, CC0, provisoire | Fond |
| S02 | 3,2 s | Fin de phrase « … » | Silence voulu | Éditorial | Sur la phrase | — | — | Laisser la phrase résonner | — | — |

Familles : voix off · son d'archive · ambiance / room tone · bruitage motivé · effet éditorial · musique · silence.

## Registre des sons (dans `PROVENANCE.md`)
| Fichier | Description | Type de source | Auteur / fournisseur | Licence et lien | Attribution exigée | Lieu et date réels d'enregistrement | Modifications | Statut documentaire | Vérifié le | Retenu ou provisoire |
|---|---|---|---|---|---|---|---|---|---|---|

Type de source : archive exacte · enregistrement contextuel · génération illustrative (prompt, identifiant, crédits) · enregistré par le projet.
Statut documentaire : ce que le son peut prétendre représenter, et ce qu'il ne doit jamais représenter.

## Journal de cues (si musique)
| Cue | Titre / version | Source | Auteur, éditeur | Entrée | Sortie | Durée | Fonction | Points de synchro | Sortie prévue (résolution, coupe, pont, son du monde) | Droits et restrictions | Fichier exact |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M01 |  |  | inconnu / à vérifier |  |  |  |  |  |  |  |  |

## Note de contrôle audio
```text
Fichier contrôlé (chemin exact, date) :
Statut : EN_COURS / MESURES_TECHNIQUES_OK / ECOUTE_A_FAIRE / CORRECTIONS_DEMANDEES / APPROUVE_PAR_<PROPRIETAIRE> (date)

MESURES (outil, commande)
- Format : codec, fréquence, canaux, débit ; durées audio / vidéo
- Loudness intégrée I : … LUFS ; LRA : … LU ; crête vraie : …
- Repli mono : I … LUFS ; écart avec la stéréo : …
- Crêtes par canal : … ; écrêtage : oui / non
- Silences trouvés : … (correspondent-ils aux silences voulus ?)
- Voix contre reste, 1–4 kHz : … dB sur [fenêtre] ou « non mesuré » (raison)

ÉCOUTE
- Passes faites : image seule / son seul / texte seul / complet / mono / petit haut-parleur — par qui
- Passages à risque à écouter (horodatés) :
- Constats d'écoute (seulement si une écoute a réellement eu lieu) :

Limites et points ouverts :
```
