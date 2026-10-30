# Domaines

Un domaine regroupe ce que toutes les chaînes d'un même sujet partagent : sources primaires, droits des images, risques juridiques et pièges de faits, son, veille. Il se place entre les règles par défaut du plugin et la chaîne (plugin 0.2.0, VALIDÉ, Hicham, 30/10/2026, recommandation 4 du passage de StudioV1).

```
referentiels/ du plugin (défaut)  <  domaines/<domaine>/DOMAINE.md  <  direction/ECARTS.md et CLAUDE.md de la chaîne
```
Le plus précis l'emporte : une règle du domaine remplace la règle par défaut ; un écart de la chaîne remplace la règle du domaine.

## Brancher une chaîne sur un domaine
Le `CLAUDE.md` de la chaîne porte, dans son Identité, la ligne `- **Domaine** : <domaine>` (nom du dossier, par exemple `sport`). Au début de chaque session, le hook des règles communes lit cette ligne et donne le chemin du profil. Une chaîne sans ligne « Domaine » suit seulement les règles par défaut et ses écarts.

## Créer un domaine
1. Copier `_modele/` sous le nom du domaine (minuscules, tirets : `true-crime`, `geo-economie`).
2. Remplir chaque section à partir des règles **déjà validées** d'une chaîne du domaine, avec leur tampon d'origine (« validé sur <chaîne>, date ») ; ce qui n'a été vu que sur une chaîne reste `PROPOSÉ` pour les suivantes.
3. Retirer ces règles du `ECARTS.md` de la chaîne d'origine, qui garde seulement ses vrais écarts au domaine.
4. Nouvelle version du plugin (`CHANGELOG.md`).

Une règle propre à l'identité d'une chaîne (nom, voix, palette, ton, concurrents à ne pas copier) n'entre jamais dans un domaine.

| Domaine | Chaînes | Depuis |
|---|---|---|
| `sport` | Apparently Athletic (StudioV1) | 0.2.0, 30/10/2026 |
