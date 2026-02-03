#!/usr/bin/env python3
"""Remove duplicated 'tags:' keys in YAML frontmatter of content/posts/*/index.md
Keeps the first occurrence of a key and removes subsequent duplicate key lines.
"""
from pathlib import Path
import re

POSTS = Path('content/posts')
changed = []
for path in POSTS.rglob('index.md'):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        continue
    parts = text.split('---', 2)
    if len(parts) < 3:
        continue
    fm = parts[1]
    body = parts[2]
    lines = fm.splitlines()
    seen = set()
    new_lines = []
    modified = False
    key_re = re.compile(r"^([A-Za-z0-9_]+):")
    for line in lines:
        m = key_re.match(line.strip())
        if m:
            key = m.group(1)
            if key in seen:
                # skip duplicate key line
                modified = True
                continue
            seen.add(key)
        new_lines.append(line)
    if modified:
        new_fm = "\n".join(new_lines)
        # Ensure proper YAML delimiters and spacing
        new_body = body.lstrip('\n')
        new_text = '---\n' + new_fm + '\n---\n' + new_body
        path.write_text(new_text, encoding='utf-8')
        changed.append(str(path))

if changed:
    print('Fixed duplicates in:')
    for p in changed:
        print(' -', p)
else:
    print('No duplicated frontmatter keys found.')
