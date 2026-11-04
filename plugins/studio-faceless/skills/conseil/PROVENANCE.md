# Skill `conseil` : provenance

**Statut** : `VALIDÉ`, Hicham, 04/11/2026. Recherche par `find-skills` (web seulement, sans `npx`) d'un skill où plusieurs agents débattent d'une décision ; parmi six candidats, choix du propriétaire : « claude-council + débat ». Réglages (tours, sièges par défaut, coût) à confirmer au premier conseil.

## Sources
1. **claude-council** : [amgadelgamal/claude-council](https://github.com/amgadelgamal/claude-council), 29 étoiles au 04/11/2026 (API GitHub), licence MIT « Copyright (c) 2026 Amgad El Gamal ». Commit `819c1d07aace94b4bd0c43ccc316e864ec62962a` (12/06/2026), le seul du dépôt. Repris : la structure du script de workflow (avis parallèles en contextes isolés, revue anonyme par lettres, classement moyen, sièges libres avec un modèle par siège, lecture des `args`).
2. **council-skill** : [tsenart/council-skill](https://github.com/tsenart/council-skill), 7 étoiles au 04/11/2026, licence MIT « Copyright (c) 2026 ». Commit `2040ee1bfb1c7b4c4d42f0924265c36b443681f9` (17/04/2026). Repris : le protocole du débat (désaccord principal, avis qui renforce, ce qui a changé, position finale) et la passe de contre-hypothèse quand l'accord vient trop vite. Ses personnages (Socrate, Feynman…) ne sont pas repris.
- Fichiers lus en entier sur `raw.githubusercontent.com` le 04/11/2026, sans `npx` ni clone. Aucune consigne douteuse : ni réseau, ni installation, ni clé. Les deux textes MIT sont dans `LICENSE`.

| Fichier d'origine | Octets | Empreinte Git (blob) | SHA-256 |
|---|---|---|---|
| claude-council `SKILL.md` | 6 028 | `e31caa07abfeea1bc7078f877a19347f47cc5673` | `8193edf768779f5751cb6c91fd0fd56782ef2adc3e34863b58db4d788f081a3c` |
| claude-council `council-workflow.js` | 8 998 | `7f064308f5b71dcd4a0734a2179a5b0e42b95090` | `038aa812a557f46a0780f430889f21b336e94b975c26a4060bb1b439a04b89b5` |
| claude-council `LICENSE` | 1 072 | `080b2cf17e668b5cd2db4e2d6bbc3b17d4836576` | `6086cdd57fb66cb5d02c51ccda096636508459e4de6f993b5c5bf739a73873f7` |
| council-skill `skills/council/SKILL.md` | 4 246 | `abbc1228f518b97fd7ea0493651b3487f7327521` | `c4c760de2863fcf5465946054a97e2a99429c1d862f0944c1ffbcd67682e56f8` |
| council-skill `skills/council/references/protocol.md` | 2 705 | `d94379e7c95e70ea5d788a2cf0294e1a64d4c97c` | `daafe5c2d2cbe3a5cd9d621072722f84143d6b65af7da425e20773a1efdae153` |
| council-skill `LICENSE` | 1 056 | `14fac913ccf80234b1848540089a3bbcb6e5283d` | `1126322e2cc8d165adc4c792eeb195717de2bcc7b39be1ce77959d78e87ef685` |

## Œuvre du studio (04/11/2026)
| Fichier | Octets | Empreinte Git (blob) | SHA-256 |
|---|---|---|---|
| `SKILL.md` | 5 342 | `83fee8691c666b6cc128d1ed8285fe8956dcd874` | `d258140a5137c5f429a9bcd4968eb12b7b1b7075b101efcb4df379a6d3b8ef6c` |
| `conseil-workflow.js` | 19 098 | `7e4ca91533ffcdd3e84d43e9f42187d225e72a03` | `6d20cd41aa3f2d6ca07f6f6734765d2149116977ae36b289e9afc2ae71d5bb93` |
| `LICENSE` | 2 930 | `e01aa36218423dd83f986c3348fd499b77838fc0` | `aebafc4c8796cd62ba866fc848777e5f40575e1af7c591a58dd2d6906a5a383e` |
| `../../agents/conseiller.md` | 1 815 | `7d187a377753d495f4f238f36197c885ad420457` | `aed13577ebc27da4ebfc593caeea512614ba82ad5de52861940512ab9465e34b` |

## Ce que le studio a changé
- **Textes réécrits en français** ; `SKILL.md` aux règles du studio : porte du propriétaire avant tout lancement, statut `PROPOSÉ` du verdict, compte rendu dans `docs/rapports/` de la chaîne, `disable-model-invocation: true` (appel par le propriétaire avec `/conseil`).
- **Un tour de débat ajouté** entre l'avis et le président : la revue anonyme de claude-council et le contre-interrogatoire de council-skill tiennent dans le même appel (critiques, désaccord principal et sa gravité, avis qui renforce, ce qui a changé, position finale, classement).
- **Contre-hypothèse** : un agent de plus, seulement si aucun siège ne garde de désaccord majeur.
- **Président en agent** (claude-council le laisse à la session principale) : il écrit le compte rendu sans écraser de fichier et ne rend qu'une synthèse, pour garder léger le contexte du directeur.
- **Sièges en lecture seule** : agent `studio-faceless:conseiller` du plugin (Read, Grep, Glob, WebFetch, WebSearch), au lieu de l'agent par défaut qui peut écrire.
- **Sièges par défaut** : les quatre de claude-council, traduits ; la note de claude-council sur Fable (non vérifiée) n'est pas reprise.
- Essai à sec le 04/11/2026 : script lancé dans Node avec de faux agents (9 cas : avec et sans désaccord majeur, siège vide, mode rapide, président vide, `args` en texte, `rapport` absent, type par défaut, aucun siège) ; résultats conformes. Aucun conseil réel encore lancé.
- Aucune mise à jour depuis les sources sans décision du propriétaire.
