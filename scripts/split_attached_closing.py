#!/usr/bin/env python3
"""Split lines that have the closing '---' attached to other content (e.g. '- layer---' or 'layout: post---').
This focuses on frontmatter (between opening '---' and closing '---' or first 80 lines).
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
    # Only process files that have frontmatter starting at top
    if lines[0].strip() != '---':
        continue
    # find end of frontmatter (search for a line equal to '---')
    end_idx = None
    for i in range(1, min(len(lines), 200)):
        if lines[i].strip() == '---':
            end_idx = i
            break
    scan_until = end_idx if end_idx is not None else min(len(lines), 80)
    modified = False
    i = 1
    while i < scan_until:
        ln = lines[i]
        if '---' in ln and ln.strip() != '---':
            before, after = ln.split('---', 1)
            before = before.rstrip()
            after = after.lstrip()
            lines[i] = before
            insert_pos = i+1
            lines.insert(insert_pos, '---')
            if after:
                lines.insert(insert_pos+1, after)
            modified = True
            # adjust indexes
            if end_idx is not None:
                end_idx += 1
            scan_until = end_idx if end_idx is not None else min(len(lines), 80)
            i = insert_pos + 1
            continue
        i += 1
    if modified:
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        changed.append(str(path))

if changed:
    print('Split attached closings in:')
    for p in changed:
        print(' -', p)
else:
    print('No attached closings found.')
