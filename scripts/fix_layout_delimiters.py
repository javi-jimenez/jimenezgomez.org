#!/usr/bin/env python3
"""Fix cases where 'layout: <value>---' appears on a single line (missing newline before closing '---')."""
from pathlib import Path
import re

POSTS = Path('content/posts')
changed = []
pat = re.compile(r"^(layout:\s*.+?)---\s*$")
for path in POSTS.rglob('index.md'):
    lines = path.read_text(encoding='utf-8').splitlines()
    modified = False
    new_lines = []
    i = 0
    while i < len(lines):
        m = pat.match(lines[i])
        if m:
            new_lines.append(m.group(1))
            new_lines.append('---')
            modified = True
            i += 1
            continue
        new_lines.append(lines[i])
        i += 1
    if modified:
        path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
        changed.append(str(path))

if changed:
    print('Fixed layout delimiter issues in:')
    for p in changed:
        print(' -', p)
else:
    print('No layout delimiter issues found.')
