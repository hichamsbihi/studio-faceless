# Sources et licences

Ce skill a été rédigé sur AA le 14 octobre 2026, à la demande du propriétaire (option B : une méthode propre plutôt que l'installation de skills tiers). Il reformule et adapte au documentaire de la chaîne des méthodes et structures publiées sous licence MIT. Le texte est réécrit ; les notices de copyright et d'autorisation des œuvres adaptées sont reproduites ci-dessous, comme la licence MIT le demande.

## Œuvres adaptées

1. **calesthio/generative-media-skills** — https://github.com/calesthio/generative-media-skills
   - Skills lus en entier le 14/10/2026 : `skills/production/audio-craft/sound-design-foley`, `skills/production/post-production/editing-montage` (section J-cuts, L-cuts, ponts sonores ; passes de contrôle), `skills/production/audio-craft/music-supervision-scoring` (repérage musical, journal de cues), `skills/production/audio-craft/audio-mixing-mastering` (contrat audio, contrôle après encodage, repli mono), `skills/production/content-formats/documentary-montage-production` (retenue musicale documentaire).
   - Repris sous une forme adaptée : champs de la feuille de repérage, modèle de perspective, registre de provenance par son, relations son-image, architecture et sorties de cue, journal de cues sans donnée inventée, diagnostic par symptôme, contrat audio.

   ```text
   MIT License

   Copyright (c) 2026 generative-media-skills contributors

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
   ```

2. **JosiahSiegel/claude-plugin-marketplace** — https://github.com/JosiahSiegel/claude-plugin-marketplace
   - Fichier lu le 14/10/2026 : `plugins/ffmpeg-core/skills/ffmpeg-audio-processing/references/audio-analysis-measurement.md`.
   - Repris sous une forme adaptée : choix des filtres de mesure (`ebur128=peak=true`, `astats`). Les commandes de `controle-et-mesure.md` ont été réécrites et testées sur FFmpeg 9.0.2.

   ```text
   MIT License

   Copyright (c) 2025 Josiah Siegel

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
   ```

3. **guia-matthieu/clawfu-skills** — https://github.com/guia-matthieu/clawfu-skills
   - Fichier lu le 14/10/2026 : `skills/audio/sound-design-film/SKILL.md`.
   - Repris sous une forme adaptée : hiérarchie des couches et « loi des deux et demi » de Walter Murch, telles que présentées par ce skill.

   ```text
   MIT License

   Copyright (c) 2026 Guia

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
   ```

## Écarté
- **snowfrost/skill-movie**, « cinematic-music-sound-design » : aucune licence dans le dépôt au 14/10/2026 ; rien n'en est repris.

## Références de fond citées par ces sources (non relues ici)
- ITU-R BS.1770 (mesure de loudness et de crête vraie) ; EBU R 128.
- Walter Murch, « Dense Clarity – Clear Density » (essai connu ici par des sources secondaires).
- Documentation des filtres FFmpeg : https://ffmpeg.org/ffmpeg-filters.html

## Ce qui vient de la chaîne d'origine
- Les décisions, cibles, interdits et constats HyperFrames viennent de `${CLAUDE_PLUGIN_ROOT}/referentiels/DIRECTION_AUDIO.md` (règles par défaut du plugin ; validées sur AA), du `CLAUDE.md` de la chaîne et de l'audit du Motion Lab (étude AA, 14/10/2026). En cas d'écart, `DIRECTION_AUDIO.md` fait foi, sauf écart de la chaîne dans `direction/ECARTS.md`.
