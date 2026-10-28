"""Hook SessionStart du plugin studio-faceless.

Injecte les règles communes du studio (REGLES_STUDIO.md) au début de chaque session, et après un /compact,
avec les chemins du plugin installé à la place de ${CLAUDE_PLUGIN_ROOT}.
"""
import json
import os
import sys

root = os.environ.get('CLAUDE_PLUGIN_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(root, 'REGLES_STUDIO.md'), encoding='utf-8') as f:
    texte = f.read().replace('${CLAUDE_PLUGIN_ROOT}', root.replace('\\', '/'))
sys.stdout.buffer.write(json.dumps({'hookSpecificOutput': {
    'hookEventName': 'SessionStart', 'additionalContext': texte}}, ensure_ascii=False).encode('utf-8'))
