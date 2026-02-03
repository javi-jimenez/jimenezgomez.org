#!/usr/bin/env python3
"""Fix missing or unclosed YAML frontmatter delimiters in content/posts/*/index.md
Rules:
- If file starts without '---' but contains YAML-like keys in first 5 lines, add opening '---' at top.
- If file starts with '---' but has no closing '---', try to find a reasonable end (after 'layout:' line) and insert closing '---' there.
"""
from pathlib import Path
import re

POSTS = Path('content/posts')
changed = []
for path in POSTS.rglob('index.md'):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    if not lines:
        continue
    if lines[0].strip() == '---':
        # find closing
        try:
            idx = lines.index('---', 1)
        except ValueError:
            # no closing delimiter; attempt to find end after layout: or an empty line
            end_idx = None
            for i, ln in enumerate(lines[1:20], start=1):
                if ln.strip().startswith('layout:'):
                    end_idx = i+1
                    break
                if ln.strip() == '':
                    end_idx = i
                    break
            if end_idx is None:
                # fallback: insert after 20 lines
                end_idx = min(20, len(lines)-1)
            lines.insert(end_idx+1, '---')
            path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            changed.append(str(path))
    else:
        # doesn't start with '---'. if first few lines look like frontmatter keys, add opening delimiter
        look = '\n'.join(lines[:8])
        if re.search(r"^(og_image|image|title|date|draft|layout|tags|categories):", look, re.M):
            # add opening and try to place closing after layout
            insert_open = True
            # find index to insert closing after layout:
            end_idx = None
            for i, ln in enumerate(lines[:40]):
                if ln.strip().startswith('layout:'):
                    end_idx = i+1
                    break
            if end_idx is None:
                # find first blank line
                for i, ln in enumerate(lines[:40]):
                    if ln.strip() == '':
                        end_idx = i
                        break
            if end_idx is None:
                end_idx = min(20, len(lines)-1)
            lines.insert(0, '---')
            lines.insert(end_idx+1, '---')
            path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            changed.append(str(path))

if changed:
    print('Fixed delimiters in:')
    for p in changed:
        print(' -', p)
else:
    print('No delimiter fixes needed.')
