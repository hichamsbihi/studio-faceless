# Sources

Skill rédigé sur AA (StudioV1) le 16/10/2026, à la demande de son propriétaire, d'après l'étude AA des skills YouTube du 16/10/2026 (§ 2, § 3.1 et annexe). Aucun skill tiers n'a été installé ni copié : les candidats ont été lus par la recherche du 16/10/2026, et seules leurs **idées** sont reprises, réécrites et adaptées. Aucun texte ni code n'en est reproduit, d'où l'absence de notice de licence.

## Idées reprises (dépôts GitHub sous licence MIT)
- **higgsfield-ai/skills** (`higgsfield-youtube-thumbnail`) : au moins 5 concepts véridiques, écart d'information, contrôle à petite taille. Écarté pour le reste : génération par IA, installation par `curl | sh`, ressemblance de vraies personnes.
- **charlie947/social-media-skills** : garde-fous, ne pas inventer de résultat, aucun visage non fourni.
- **smitmartijn/claude-skills** (`thumbnail-video`) : chaîne HTML/CSS et Chrome sans fenêtre.

## Faits officiels
- Aide YouTube (support.google.com/youtube/answer/…) : 72431 (miniatures), 7628154 et 16767369 (impressions et CTR), 13861714 et 16391400 (Test & Compare).
- WCAG 2.2, critère 1.4.3 « Contrast (Minimum) » : seuils 4,5:1 et 3:1 (gros texte), formule de luminance relative.

## Décisions et leçons venues d'AA
- E001 : CTR d'environ 2 % de la miniature générée par IA (AA, 15/10/2026).
- E003 : miniatures v1, v3 et v4, avec leurs `PROVENANCE.md`, gardées dans les archives AA, hors du plugin (refus des v1, consigne de s'inspirer d'une chaîne concurrente sans reprendre son style, correction de la flèche, validation de la v4 le 15/10/2026).
