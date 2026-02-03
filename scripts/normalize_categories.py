#!/usr/bin/env python3
"""Normalize categories frontmatter across content/posts/*/index.md
- Converts `categories: [a, b]` plus following `- item` lines into a single
  YAML list under `categories:` with unique items preserved.
"""
from pathlib import Path
import re

POSTS = Path('content/posts')
changed = []
cat_re = re.compile(r"^categories:\s*\[(.*)\]\s*$")
for path in POSTS.rglob('index.md'):
    lines = path.read_text(encoding='utf-8').splitlines()
    i = 0
    modified = False
    new_lines = []
    while i < len(lines):
        m = cat_re.match(lines[i])
        if m:
            inline = m.group(1)
            items = [it.strip() for it in inline.split(',') if it.strip()]
            j = i+1
            extra = []
            while j < len(lines) and re.match(r"^\s*-\s+", lines[j]):
                extra_item = re.sub(r"^\s*-\s+", '', lines[j]).strip()
                if extra_item:
                    extra.append(extra_item)
                j += 1
            # merge preserving order and uniqueness
            merged = []
            for it in items + extra:
                if it not in merged:
                    merged.append(it)
            # write normalized block
            new_lines.append('categories:')
            for it in merged:
                new_lines.append('  - ' + it)
            i = j
            modified = True
            continue
        else:
            new_lines.append(lines[i])
            i += 1
    if modified:
        path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
        changed.append(str(path))

if changed:
    print('Normalized categories in:')
    for p in changed:
        print(' -', p)
else:
    print('No categories normalization needed.')
