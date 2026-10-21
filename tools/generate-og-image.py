#!/usr/bin/env python3
"""Portada de un artículo.

Punto de entrada estable (lo invoca el hook `pre-commit`), pero el dibujo lo
hace `tools/coverart`. Si el artículo no tiene entrada en `coverart/specs.py`
se usa una plantilla sobria y se avisa, para que el hueco se note.

Uso:
  ./tools/generate-og-image.py content/posts/2026-01-01-slug --set-frontmatter
  ./tools/generate-og-image.py --all
"""
import argparse
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from coverart.compose import title_of, year_of  # noqa: E402
from coverart.specs import SPECS               # noqa: E402

FALLBACK = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="g" x1="0" x2="1">
      <stop offset="0" stop-color="#0d1017"/>
      <stop offset="1" stop-color="#1b2432"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#g)"/>
  <g transform="translate(76,86)">
    <rect x="0" y="0" width="56" height="3" rx="1.5" fill="#e2b552"/>
    <text x="0" y="96" font-family="Inter Display, Inter, DejaVu Sans, sans-serif"
          font-size="50" font-weight="900" fill="#f6f3ec">{title}</text>
    <text x="0" y="470" font-family="IBM Plex Mono, monospace" font-size="14"
          letter-spacing="1.8" fill="#8496ab">JIMENEZGOMEZ.ORG · {year}</text>
  </g>
</svg>
'''


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("post", nargs="?", help="carpeta del artículo")
    ap.add_argument("--all", action="store_true", help="todos los de specs.py")
    ap.add_argument("--set-frontmatter", action="store_true")
    ap.add_argument("--title", help="sobrescribe el título")
    args = ap.parse_args(argv)

    if args.all:
        return subprocess.call([sys.executable, "-m", "coverart", "--all"],
                               cwd=TOOLS)

    if not args.post:
        ap.error("indica la carpeta del artículo o usa --all")

    post = Path(args.post).resolve()
    if not post.is_dir():
        print("No existe la carpeta:", post)
        return 2
    slug = post.name

    if slug in SPECS:
        cmd = [sys.executable, "-m", "coverart", slug]
        if not args.set_frontmatter:
            cmd.append("--no-frontmatter")
        return subprocess.call(cmd, cwd=TOOLS)

    print(f"  ! {slug}: sin portada propia en coverart/specs.py "
          f"(se usa la plantilla sobria)")
    (post / "og-image.svg").write_text(
        FALLBACK.format(title=(args.title or title_of(post)).replace('"', ""),
                        year=year_of(post)), encoding="utf-8")
    for w, h in ((1200, 630), (600, 315)):
        subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h),
                        "-o", str(post / f"og-image-{w}x{h}.png"),
                        str(post / "og-image.svg")], check=False)
    if args.set_frontmatter:
        from coverart.__main__ import set_frontmatter_image
        set_frontmatter_image(post, "og-image-1200x630.png")
        print("Frontmatter updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
