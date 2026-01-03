#!/usr/bin/env python3
"""
Generate a simple OG SVG for a Hugo post.
Usage:
  ./generate-og-image.py /path/to/post
Options:
  --set-frontmatter  : update `image: "og-image.svg"` in the post frontmatter
  --title "Text"     : override title to render

The script writes `og-image.svg` into the post folder.
"""
import sys
import re
from pathlib import Path

TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="g" x1="0" x2="1">
      <stop offset="0" stop-color="#0f172a"/>
      <stop offset="1" stop-color="#0b6f84"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#g)" />
  <g transform="translate(80,80)">
    <rect x="0" y="0" width="1040" height="470" rx="18" fill-opacity="0.06" fill="#ffffff"/>
    <text x="40" y="120" font-family="Inter, Arial, Helvetica, sans-serif" font-size="52" fill="#ffffff" font-weight="700">{title}</text>
    <text x="40" y="190" font-family="Inter, Arial, Helvetica, sans-serif" font-size="28" fill="#e6f7fb">{subtitle}</text>
    <text x="40" y="360" font-family="Inter, Arial, Helvetica, sans-serif" font-size="18" fill="#bdeef7">Documento — jimenezgomez.org — {year}</text>
  </g>
</svg>'''


def read_title_from_index(post_dir: Path):
    idx = post_dir / 'index.md'
    if not idx.exists():
        return post_dir.name.replace('-', ' ').title()
    text = idx.read_text(encoding='utf-8')
    # try YAML frontmatter between --- and ---
    m = re.search(r"^---\n(.*?)\n---\n", text, re.S | re.M)
    if not m:
        # try toml +++
        m = re.search(r"^\+\+\+\n(.*?)\n\+\+\+\n", text, re.S | re.M)
    if m:
        fm = m.group(1)
        # look for title: "..."
        tm = re.search(r"^title\s*:\s*\"?(.*?)\"?$", fm, re.M)
        if tm:
            return tm.group(1).strip()
        # toml: title = '...'
        tm = re.search(r"^title\s*=\s*\"?(.*?)\"?\s*$", fm, re.M)
        if tm:
            return tm.group(1).strip()
    # fallback: first H1
    h1 = re.search(r"^#\s+(.*)$", text, re.M)
    if h1:
        return h1.group(1).strip()
    return post_dir.name.replace('-', ' ').title()


def set_frontmatter_image(post_dir: Path, image_name='og-image.svg'):
    idx = post_dir / 'index.md'
    if not idx.exists():
        return False
    s = idx.read_text(encoding='utf-8')
    if s.startswith('---'):
        # YAML frontmatter
        parts = s.split('---')
        # parts[1] is fm
        fm = parts[1]
        if re.search(r"^image\s*:\s*", fm, re.M):
            # replace existing
            fm = re.sub(r"^image\s*:\s*.*$", f'image: "{image_name}"', fm, flags=re.M)
        else:
            fm = fm.strip() + '\nimage: "' + image_name + '"\n'
        parts[1] = fm
        new = '---'.join(parts)
        idx.write_text(new, encoding='utf-8')
        return True
    if s.startswith('+++'):
        # TOML frontmatter
        parts = s.split('+++')
        fm = parts[1]
        if re.search(r"^image\s*=", fm, re.M):
            fm = re.sub(r"^image\s*=\s*.*$", f'image = "{image_name}"', fm, flags=re.M)
        else:
            fm = fm.strip() + '\nimage = "' + image_name + '"\n'
        parts[1] = fm
        new = '+++'.join(parts)
        idx.write_text(new, encoding='utf-8')
        return True
    return False


def main(argv):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('post', help='Path to post folder (e.g. content/posts/2026-01-03-slug)')
    parser.add_argument('--set-frontmatter', action='store_true', help='Update frontmatter to reference generated og-image.svg')
    parser.add_argument('--title', help='Override title text')
    args = parser.parse_args(argv)
    post = Path(args.post)
    if not post.exists() or not post.is_dir():
        print('Post folder not found:', post)
        return 2
    title = args.title or read_title_from_index(post)
    subtitle = ''
    year = '2026'
    try:
        year = read_title_from_index(post)
    except Exception:
        pass
    # craft svg
    svg = TEMPLATE.format(title=title.replace('"',''), subtitle=subtitle, year='2026')
    out = post / 'og-image.svg'
    out.write_text(svg, encoding='utf-8')
    print('Wrote', out)
    if args.set_frontmatter:
        ok = set_frontmatter_image(post)
        print('Frontmatter updated' if ok else 'Frontmatter not updated (no frontmatter found)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
