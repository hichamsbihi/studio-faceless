# Musique à l'image

Depuis le 15/10/2026 (validé sur AA), la musique **porte l'immersion** de chaque séquence (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 1-2 ; les écarts de la chaîne sont dans `direction/ECARTS.md` et l'emportent sur les règles par défaut). La question n'est plus « faut-il de la musique ? » mais « quelle musique pour cette situation ? » : ouverture, tension ou rivalité, analyse et science, émotion et fin. Écrire sa fonction pour chaque passage, ainsi que ses entrées, retraits et silences voulus.

## 1. Fonctions possibles
Soutenir l'immersion, organiser la progression d'une enquête, marquer un contraste, accompagner une résolution, relier un montage, laisser entendre un sous-texte. Jamais : dire au spectateur quoi penser d'une personne réelle, gonfler une affirmation contestée, remplacer une preuve.

## 2. Repérage musical
Pour chaque cue (gabarit : `gabarits.md`, « Journal de cues ») :
- **identifiant stable** (M01, M02…) qu'on ne renumérote pas à chaque révision ;
- **entrée et sortie** : les placer sur un **changement d'histoire** (nouvelle idée, révélation, conséquence), pas seulement sur une coupe ;
- **fonction** et **état émotionnel** au début, au tournant et à la fin, plutôt qu'une humeur unique sur une scène qui évolue ;
- **zones sans musique** voulues : le silence se repère aussi ; une musique qui démarre à la première image par défaut fait perdre le contraste ;
- **points de synchro** choisis (une révélation, un document), peu nombreux : laisser certains événements passer sous une phrase musicale continue ;
- **à éviter** : clichés de bande-annonce, emphase, imitation d'un morceau ou d'un artiste.

Accompagner le sous-texte plutôt que l'action littérale quand la scène dit déjà son émotion de surface.

## 3. Architecture d'un cue
État de départ → question musicale → développement → tournant → conséquence → **sortie**. La sortie compte autant que l'entrée :
- résoudre avant une phrase importante ;
- couper net sur un silence voulu ;
- laisser une tenue faire le pont vers la scène suivante ;
- finir sur un son du monde montré (une ambiance prend le relais) ;
- laisser une harmonie non résolue quand l'enquête n'est pas close.

## 4. Musique et voix
- Peu d'éléments dans la zone de la voix ; pas de mélodie principale dans la bande 1–4 kHz pendant la narration.
- Sous une narration dense : peu de surprises harmoniques ; le mouvement peut venir de la pulsation et de l'arrangement.
- Réduire d'abord l'arrangement (instruments, densité, registre), puis le gain ; carve ou ducking seulement si un masquage est mesuré ou entendu (`DIRECTION_AUDIO.md` § 3).

## 5. Sources et droits
- Aucune nouvelle recherche musicale sans demande du propriétaire ; il choisit lui-même les variantes.
- Connecteur ElevenLabs : le connecteur de base ne fait pas de musique, le connecteur complet ajoute Eleven Music, avec l'accord du propriétaire (`${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` § 4) ; Suno, Udio et services équivalents sont exclus sans décision du propriétaire.
- Ne jamais demander une musique « comme » un artiste vivant ou un morceau connu : décrire des attributs (tempo, instrumentation, densité, registre, dynamique).
- Le journal de cues ne contient **aucune donnée inventée** : compositeur, éditeur ou identifiants inconnus s'écrivent « inconnu / à vérifier ».

## 6. Diagnostic rapide
| Symptôme | Cause probable | Correction |
|---|---|---|
| Sonne « kitsch » ou emphatique | Émotion trop explicite, harmonie générique, procédés de bande-annonce | Alléger l'arrangement, accompagner le sous-texte, laisser un silence |
| Lutte avec la voix | Mélodie ou voix chantée dans la bande de la parole | Retirer la mélodie, baisser la densité, déplacer le cue |
| Rate le montage | Aucun repérage, sorties sur les coupes | Placer entrées et sorties sur les changements d'histoire |
| Ressemble à un morceau connu | Référence trop précise | Repartir d'attributs neutres |
| Boucle qui claque | Boucle hors mesure, queue de réverbération coupée | Boucle sur une limite de mesure, fondu, queue séparée |
| Droits flous | Source ou licence manquante | Bloquer l'usage final ; documenter ou remplacer |
