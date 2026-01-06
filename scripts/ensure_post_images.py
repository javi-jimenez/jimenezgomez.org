#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / 'content' / 'posts'

front_re = re.compile(r'^---\s*$(.*?)^---\s*$', re.S | re.M)

def read_frontmatter(text):
    m = front_re.search(text)
    if not m:
        return None, text
    fm_raw = m.group(1)
    body = text[m.end():]
    fm = {}
    for line in fm_raw.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            k,v = line.split(':',1)
            v=v.strip()
            # strip quotes
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                v=v[1:-1]
            fm[k.strip()] = v
    return fm, body


def write_frontmatter(fm, body):
    lines = ['---']
    for k,v in fm.items():
        # quote values containing special chars
        if v is None:
            lines.append(f"{k}:")
        elif re.search(r"[\"':#\\]", v):
            lines.append(f'{k}: "{v}"')
        else:
            lines.append(f'{k}: {v}')
    lines.append('---')
    lines.append('')
    lines.append(body.lstrip('\n'))
    return '\n'.join(lines)


def choose_images(postdir):
    # prefer og-image-1200x630.png, og-image.svg, then first png/jpg
    candidates = []
    for name in ['og-image-1200x630.png','og-image.svg','og-image.png','og-image-600x315.png']:
        p=postdir/name
        if os.path.exists(p):
            return name, name
    # find first png/jpg
    for ext in ('*.png','*.jpg','*.jpeg','*.webp'):
        files = list(Path(postdir).glob(ext))
        if files:
            return files[0].name, None
    return None, None


def process_post(postdir):
    idx = Path(postdir)/'index.md'
    if not idx.exists():
        return False, 'no index.md'
    text = idx.read_text(encoding='utf-8')
    fm, body = read_frontmatter(text)
    if fm is None:
        fm = {}
    img, og = choose_images(postdir)
    changed = False
    if og:
        if fm.get('og_image') != og:
            fm['og_image'] = og
            changed = True
        if fm.get('image') != og:
            fm['image'] = og
            changed = True
    elif img:
        # set image if missing
        if 'image' not in fm or not fm.get('image'):
            fm['image'] = img
            changed = True
        # set og_image to image if missing
        if 'og_image' not in fm or not fm.get('og_image'):
            fm['og_image'] = img
            changed = True
    else:
        # no images found; do nothing
        pass
    if changed:
        new = write_frontmatter(fm, body)
        idx.write_text(new, encoding='utf-8')
    return changed, None


def main():
    changed_any = []
    for p in sorted(POSTS.iterdir()):
        if not p.is_dir():
            continue
        changed, reason = process_post(p)
        if changed:
            changed_any.append(str(p))
    if changed_any:
        print('Updated posts:', '\n'.join(changed_any))
    else:
        print('No changes')

if __name__=='__main__':
    main()
