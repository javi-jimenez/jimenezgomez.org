#!/usr/bin/env python3
"""Normalize frontmatter in content/posts:
- convert tags from bracket-strings to YAML lists
- quote author values
- add default image if none
- unescape HTML entities in body
"""
import re
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / 'content' / 'posts'
DEFAULT_IMAGE = '/img/default-post.svg'

def normalize_file(path: Path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        return
    parts = text.split('---', 2)
    if len(parts) < 3:
        return
    _, fm, body = parts
    fm_lines = fm.strip().splitlines()
    new_fm_lines = []
    has_image = False
    has_tags = False
    for line in fm_lines:
        # tags: "[... ]" or tags: '[...]' -> convert
        m = re.match(r'^tags:\s*["\']?\s*\[(.*)\]\s*["\']?\s*$', line)
        if m:
            has_tags = True
            items = [i.strip().strip('\"\'') for i in m.group(1).split(',') if i.strip()]
            new_fm_lines.append('tags:')
            for it in items:
                # remove surrounding quotes
                it = it.strip()
                it = it.strip('"').strip("'")
                new_fm_lines.append(f'  - {it}')
            continue

        # author: Gemini (AI Model) -> quote if unquoted
        m2 = re.match(r'^(author:\s*)(.+)$', line)
        if m2:
            val = m2.group(2).strip()
            if not (val.startswith('"') or val.startswith("'")):
                val = f'"{val}"'
            new_fm_lines.append(f'author: {val}')
            continue

        # image or og_image presence
        if re.match(r'^image:\s*', line) or re.match(r'^og_image:\s*', line) or re.match(r'^og-image:\s*', line):
            has_image = True

        # Unescape HTML entities in frontmatter values and normalize smart quotes
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0]
            val = parts[1].lstrip()
            if val:
                # remove surrounding whitespace, then unescape HTML entities
                v = html.unescape(val)
                # normalize smart quotes to straight quotes
                v = v.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
                new_fm_lines.append(f"{key}: {v}")
                continue
        new_fm_lines.append(line)

    if not has_tags:
        # ensure tags exists as empty list if missing
        new_fm_lines.append('tags: []')

    if not has_image:
        # add default image
        new_fm_lines.append(f'image: "{DEFAULT_IMAGE}"')

    # Unescape HTML entities in body
    new_body = html.unescape(body)

    new_text = '---\n' + '\n'.join(new_fm_lines).rstrip() + '\n---\n' + new_body.lstrip()
    path.write_text(new_text, encoding='utf-8')

def main():
    count = 0
    for md in POSTS.rglob('index.md'):
        normalize_file(md)
        count += 1
    print(f'Normalized {count} post files under {POSTS}')

if __name__ == '__main__':
    main()
