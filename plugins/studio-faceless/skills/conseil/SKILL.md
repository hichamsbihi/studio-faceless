---
name: conseil
description: Conseil de plusieurs agents Claude indépendants qui débattent d'une décision du studio (méthode de fabrication, architecture, outil ou service, stratégie) : avis en aveugle, débat sur les avis anonymes avec classement, contre-hypothèse si l'accord vient trop vite, compte rendu d'un président. Sièges définis pour chaque question et soumis au propriétaire avant le lancement. Appelé par le propriétaire avec /conseil.
argument-hint: "[la question] [--rapide]"
disable-model-invocation: true
---

# Conseil

Ajout au plugin validé sur AA le 04/11/2026 ; nombre de tours, sièges par défaut et coût à confirmer au premier conseil. Adapté de `claude-council` (avis indépendants, revue anonyme, classement) et du protocole de `council-skill` (débat, contre-hypothèse) : `PROVENANCE.md`, licences dans `LICENSE`.

## Quand
- Une décision du studio difficile ou coûteuse à défaire : méthode de fabrication, architecture, outil ou service payant, organisation des chaînes.
- Pas pour une porte d'épisode courante (skill `studio-faceless:episode`). Positionnement d'une chaîne, titres et sujets : `strategist` (conseil roast-room).

## Porte avant le lancement
Le directeur (Claude principal) soumet au propriétaire, en un bloc, et ne lance qu'avec son accord :
1. la question, au mot près ;
2. les sièges : nom, angle en une ou deux phrases, modèle ;
3. les fichiers que les sièges liront d'abord, et le contexte en 3 à 6 lignes (faits mesurés, décisions déjà validées, contraintes) ;
4. le mode (`complet` ou `rapide`), le nombre d'agents et le coût estimé ;
5. le chemin du compte rendu : `docs/rapports/CONSEIL_<SUJET>_<AAAA-MM-JJ>.md` de la chaîne.

## Déroulé (script `conseil-workflow.js`)
| Tour | Qui | Ce qu'il fait |
|---|---|---|
| 1. Avis | chaque siège, en parallèle, sans voir les autres | position, réponse (600 mots au plus), points clés, confiance, ce qui ferait tomber sa position |
| 2. Débat (mode complet) | chaque siège, en parallèle | reçoit les avis anonymes (A, B, C…), critique chacun, nomme son désaccord principal et sa gravité, l'avis qui l'a renforcé, ce qui a changé, sa position finale, classe tous les avis |
| 3. Contre-hypothèse (mode complet) | un agent, toujours (1.0.1) | suppose fausse la position de la majorité : alternative la plus forte, ce qui ferait basculer, preuve qui trancherait |
| 4. Président | un agent Opus, en lecture seule (1.0.1) | rédige le compte rendu et le rend, avec un chemin libre vérifié ; le directeur l'écrit, sans écraser un fichier existant |

- **Agents** : N sièges donnent 2N + 2 agents en mode complet (1.0.1), N + 1 en mode rapide. De 2 à 8 sièges ; 4 à 6 conseillés.
- **Coût** : à mesurer au premier conseil ; estimation de 0,5 à 1 M de tokens pour 6 sièges en mode complet.
- **Lecture seule** : les sièges, la contre-hypothèse et le président sont des agents `studio-faceless:conseiller` (Read, Grep, Glob, WebFetch, WebSearch ; ni écriture ni Bash ; rôle `lecteur` du garde-fou depuis la 1.0.1). Le directeur écrit le compte rendu à partir de `president.contenu`.

## Lancer
```
Workflow({
  scriptPath: "${CLAUDE_PLUGIN_ROOT}/skills/conseil/conseil-workflow.js",
  args: {
    question: "<le texte validé, au mot près>",
    sieges: [ { nom: "...", angle: "...", modele: "opus" } ],
    contexte: "<3 à 6 lignes>",
    fichiers: [ "docs/rapports/<étude>.md" ],
    mode: "complet",
    rapport: "docs/rapports/CONSEIL_<SUJET>_<AAAA-MM-JJ>.md",
    date: "JJ/MM/AAAA"
  }
})
```
- `args` est un objet JSON, pas une chaîne. `question` et `rapport` sont obligatoires.
- `sieges` : sans liste, quatre sièges par défaut (l'architecte, le sceptique, le pragmatique, le chercheur). `modele` : `opus` (par défaut), `sonnet`, `haiku` ou `fable`.
- `mode: "rapide"` : avis puis président, sans débat ; pour une décision réversible.
- `type_agent` : `studio-faceless:conseiller` par défaut ; `""` prend l'agent par défaut du workflow, sans lecture seule imposée, seulement avec l'accord du propriétaire.
- Le script n'a ni horloge ni hasard : la date passe par `args`. Reprise après un arrêt : mêmes `scriptPath` et `args`, avec `resumeFromRunId`.

## Ce que le directeur rend au propriétaire
- Le résumé et la recommandation du président, le tableau des sièges (siège, modèle, position finale, désaccord, rang moyen), le consensus, la dissidence, les questions ouvertes et le lien du compte rendu.
- Il ne recopie pas les avis entiers : ils sont dans le compte rendu et dans le journal du workflow. Il peut donner son propre avis, séparé, et dire où il s'écarte du conseil.
- Tout reste `PROPOSÉ` : une recommandation du conseil n'est pas une décision ; rien ne devient règle sans le propriétaire.
- Un siège n'est jamais présenté comme une autre IA ou une personne réelle : ce sont des agents Claude avec un angle.

## Erreurs
| Erreur | Reprise |
|---|---|
| « Aucun siège n'a répondu » | type `studio-faceless:conseiller` introuvable : `/reload-plugins`, puis relancer |
| Un siège sans réponse | le conseil continue ; le compte rendu compte les sièges vides |
| Président sans réponse | le résultat porte `secours` (tableau, avis, débat) : le directeur écrit le compte rendu |
| Compte rendu déjà présent | le président propose `_v2` ; le directeur vérifie avant d'écrire ; jamais d'écrasement |
