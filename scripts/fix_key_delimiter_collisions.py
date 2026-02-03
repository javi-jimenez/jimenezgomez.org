#!/usr/bin/env python3
"""Fix lines where a YAML key is immediately followed by the closing delimiter, e.g. 'tags:---'.
Replaces 'key:---' with 'key:' newline '---'.
"""
from pathlib import Path
import re

POSTS = Path('content/posts')
pat = re.compile(r"^(\s*[A-Za-z0-9_+-]+:)\s*---\s*$")
changed = []
for path in POSTS.rglob('index.md'):
    lines = path.read_text(encoding='utf-8').splitlines()
    modified = False
    for i, ln in enumerate(lines[:30]):
        m = pat.match(ln)
        if m:
            lines[i] = m.group(1)
            # insert closing delimiter after this line
            lines.insert(i+1, '---')
            modified = True
            break
    if modified:
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        changed.append(str(path))

if changed:
    print('Fixed key+delimiter collisions in:')
    for p in changed:
        print(' -', p)
else:
    print('No collisions found.')
