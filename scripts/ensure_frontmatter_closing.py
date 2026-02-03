#!/usr/bin/env python3
"""Ensure frontmatter closing '---' is on its own line for content/posts/*/index.md

Behavior:
- If file starts with '---', find closing '---'. If closing delimiter is attached to previous text (e.g. 'layout: post---'), split the line so '---' is its own line.
- If there is no closing '---', attempt to insert it after 'layout:' line or after first blank line within the first 30 lines.
- Preserve other content.
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
    # Only process files that look like they have frontmatter keys at the top
    if not lines[0].strip() == '---':
        look = '\n'.join(lines[:8])
        if not re.search(r"^(og_image|image|title|date|draft|layout|tags|categories):", look, re.M):
            continue
        # add opening delimiter if missing
        lines.insert(0, '---')
    # now lines[0] == '---'
    # find closing delimiter line index
    closing_idx = None
    for i in range(1, min(len(lines), 200)):
        if lines[i].strip() == '---':
            closing_idx = i
            break
    if closing_idx is None:
        # look for a line that contains '---' attached to other text
        for i in range(1, min(len(lines), 200)):
            if '---' in lines[i]:
                # split at first '---'
                before, after = lines[i].split('---', 1)
                before = before.rstrip()
                after = after.lstrip()
                lines[i] = before
                insert_pos = i + 1
                lines.insert(insert_pos, '---')
                if after:
                    lines.insert(insert_pos+1, after)
                closing_idx = insert_pos
                break
    else:
        # closing exists, but check if it's attached to previous content in same physical line
        # (rare, since splitlines() would have separated, but check for cases like 'layout: post---' being a single line earlier)
        pass
    # Also handle cases where closing delimiter is attached at end of a line, e.g. 'layout: post---'
    # Search first 40 lines for a line that endswith '---' but not equal
    if closing_idx is None:
        for i in range(1, min(len(lines), 80)):
            if lines[i].endswith('---') and lines[i].strip() != '---':
                # split
                before = lines[i][: -3].rstrip()
                after = ''
                lines[i] = before
                insert_pos = i + 1
                lines.insert(insert_pos, '---')
                if after:
                    lines.insert(insert_pos+1, after)
                closing_idx = insert_pos
                break
    # final fallback: if still no closing, insert after layout: or after first blank line
    if closing_idx is None:
        end_idx = None
        for i, ln in enumerate(lines[1:40], start=1):
            if ln.strip().startswith('layout:'):
                end_idx = i+1
                break
            if ln.strip() == '':
                end_idx = i
                break
        if end_idx is None:
            end_idx = min(20, len(lines)-1)
        lines.insert(end_idx+1, '---')
        closing_idx = end_idx+1
    new_text = '\n'.join(lines) + '\n'
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        changed.append(str(path))

if changed:
    print('Fixed closing delimiters in:')
    for p in changed:
        print(' -', p)
else:
    print('No closing delimiter issues found.')
