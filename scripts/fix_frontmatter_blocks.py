#!/usr/bin/env python3
"""Fix malformed frontmatter blocks in posts.

Handles cases like:

---\n...\n---\n---title: "..."\n...

by merging the two frontmatter blocks into one and ensuring proper '---' delimiters.
Also fixes occurrences where frontmatter keys are concatenated to the dashes (e.g. '---title:') and some HTML-entity variants ('&mdash;title:').
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / 'content' / 'posts'

KEYS = [
    'title','date','draft','layout','image','og_image','og-image','og-image','og_image','categories','tags','author'
]

def fix_text(text: str) -> str:
    orig = text
    # Merge consecutive frontmatter delimiters: \n---\n--- -> \n (remove the middle delimiter)
    while '\n---\n---' in text:
        text = text.replace('\n---\n---', '\n', 1)

    # Fix cases like '---title:' -> '---\ntitle:' at start of line
    for k in KEYS:
        text = re.sub(r'(?m)^---\s*' + re.escape(k) + r'\s*:', '---\n' + k + ':', text)
        # also fix HTML entity variants like '&mdash;title:' or '&ndash;title:' or '—title:'
        text = re.sub(r'(?m)^(?:&mdash;|&ndash;|—)\s*' + re.escape(k) + r'\s*:', '---\n' + k + ':', text)

    # If there are multiple opening '---' and closing '---' blocks, ensure only one frontmatter at top
    # Count occurrences of lines that are exactly '---'
    lines = text.splitlines()
    delim_lines = [i for i,l in enumerate(lines) if l.strip() == '---']
    if len(delim_lines) >= 4:
        # Merge sequential frontmatters: remove the delimiter lines between first and last
        # We'll keep the first '---' and the last '---' before content.
        first = delim_lines[0]
        # find the last delimiter that is before non-frontmatter content (heuristic: before a blank line or after keys)
        last = delim_lines[-1]
        # Remove all delimiter lines between first and last (exclusive)
        new_lines = []
        for idx, l in enumerate(lines):
            if first < idx < last and l.strip() == '---':
                continue
            new_lines.append(l)
        text = '\n'.join(new_lines)

    return text if text != orig else orig

def main():
    changed = 0
    for md in POSTS.rglob('index.md'):
        txt = md.read_text(encoding='utf-8')
        new = fix_text(txt)
        if new != txt:
            md.write_text(new, encoding='utf-8')
            changed += 1
    print(f'Fixed frontmatter in {changed} files under {POSTS}')

if __name__ == '__main__':
    main()
