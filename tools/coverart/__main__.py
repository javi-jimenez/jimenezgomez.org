"""Genera las portadas de los artículos.

Uso:
  python3 -m coverart --all                 # todas las que tengan spec
  python3 -m coverart <slug> [<slug> ...]   # sólo esas
  python3 -m coverart --all --no-png        # sólo el SVG
  python3 -m coverart --list                # ver el reparto motivo/paleta
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

from .compose import build_svg, slugify, title_of, year_of
from .motifs import MOTIFS
from .palettes import PALETTES
from .specs import SPECS

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "content" / "posts"

SIZES = [(1200, 630), (600, 315)]


def set_frontmatter_image(post_dir: Path, image: str):
    idx = post_dir / "index.md"
    if not idx.exists():
        return False
    s = idx.read_text(encoding="utf-8")
    if not s.startswith("---"):
        return False
    parts = s.split("---", 2)
    if len(parts) < 3:
        return False
    fm = parts[1]
    for key in ("image", "og_image"):
        line = f'{key}: "{image}"'
        if re.search(rf"^{key}\s*:", fm, re.M):
            fm = re.sub(rf"^{key}\s*:.*$", line, fm, flags=re.M)
        else:
            fm = fm.rstrip("\n") + "\n" + line + "\n"
    parts[1] = fm
    idx.write_text("---".join(parts), encoding="utf-8")
    return True


def rasterize(svg_path: Path, quantize=True):
    """SVG → PNG en los dos tamaños del sitio.

    El grano de la portada es ruido, y el ruido no comprime: un PNG directo de
    rsvg sale a ~300 KB. Se cuantiza a 256 colores (PNG8), que baja a ~100 KB
    sin diferencia visible — el propio grano hace de tramado. Si no hay
    ImageMagick se deja el PNG directo: lo importante es que exista.
    """
    outs = []
    for w, h in SIZES:
        out = svg_path.parent / f"og-image-{w}x{h}.png"
        subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h),
                        "-o", str(out), str(svg_path)], check=True)
        if quantize and shutil.which("convert"):
            tmp = out.with_suffix(".q.png")
            r = subprocess.run(["convert", str(out), "-strip", "-dither",
                                "FloydSteinberg", "-colors", "256",
                                "-depth", "8", f"PNG8:{tmp}"],
                               capture_output=True)
            if r.returncode == 0 and tmp.exists():
                tmp.replace(out)
            else:
                tmp.unlink(missing_ok=True)
        outs.append(out)
    return outs


def build_one(slug, make_png=True, set_fm=True):
    spec = SPECS.get(slug)
    if not spec:
        print(f"  · {slug}: sin spec, se deja como está")
        return False
    post_dir = POSTS / slug
    if not post_dir.is_dir():
        print(f"  ✗ {slug}: no existe la carpeta")
        return False

    meta = dict(slug=slug, title=title_of(post_dir),
                year=year_of(post_dir), **spec)
    if meta["motif"] not in MOTIFS:
        raise SystemExit(f"motivo desconocido: {meta['motif']} ({slug})")
    if meta["palette"] not in PALETTES:
        raise SystemExit(f"paleta desconocida: {meta['palette']} ({slug})")

    svg_path = post_dir / "og-image.svg"
    svg_path.write_text(build_svg(meta), encoding="utf-8")
    extra = ""
    if make_png:
        rasterize(svg_path)
        if set_fm:
            set_frontmatter_image(post_dir, "og-image-1200x630.png")
        extra = " + png"
    print(f"  ✓ {slug}  [{meta['motif']}/{meta['palette']}]{extra}")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(prog="coverart")
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--all", action="store_true", help="todos los de specs.py")
    ap.add_argument("--no-png", action="store_true", help="no rasterizar")
    ap.add_argument("--no-frontmatter", action="store_true")
    ap.add_argument("--list", action="store_true", help="mostrar el reparto")
    args = ap.parse_args(argv)

    if args.list:
        for slug, s in SPECS.items():
            print(f"{s['palette']:<12} {s['motif']:<10} {slug}")
        return 0

    targets = list(SPECS) if args.all else args.slugs
    if not targets:
        ap.error("indica slugs o usa --all")

    print(f"Generando {len(targets)} portada(s)...")
    ok = sum(build_one(s, not args.no_png, not args.no_frontmatter)
             for s in targets)
    print(f"\n{ok}/{len(targets)} generadas.")
    return 0 if ok == len(targets) else 1


if __name__ == "__main__":
    sys.exit(main())
