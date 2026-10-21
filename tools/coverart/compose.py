"""Composición de la portada: fondo, textura, motivo y tipografía."""

import hashlib
import math
import random
import re
from pathlib import Path

from PIL import ImageFont

from .motifs import MOTIFS
from .palettes import (FONT_DISPLAY, FONT_FILES, FONT_MONO, FONT_SERIF,
                       PALETTES)

W, H = 1200, 630
PAD = 72                      # margen
TEXT_W = 520                  # ancho de la columna de texto


# --------------------------------------------------------------------------
# Texto
# --------------------------------------------------------------------------
_font_cache = {}


def _font(kind, size):
    key = (kind, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_FILES[kind], size)
    return _font_cache[key]


def measure(text, kind, size, tracking=0.0):
    f = _font(kind, size)
    w = f.getlength(text)
    return w + tracking * max(0, len(text) - 1)


def wrap(text, kind, size, max_width, tracking=0.0):
    """Parte el texto en líneas que quepan en `max_width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        probe = f"{cur} {word}".strip()
        if measure(probe, kind, size, tracking) <= max_width or not cur:
            cur = probe
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(text, kind, max_width, sizes, max_lines, tracking=0.0):
    """Busca el mayor tamaño que quepa en `max_lines` líneas."""
    for size in sizes:
        lines = wrap(text, kind, size, max_width, tracking)
        if len(lines) <= max_lines:
            return size, lines
    size = sizes[-1]
    return size, wrap(text, kind, size, max_width, tracking)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


_ATTR = re.compile(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)="([^"]*)"')


def dedupe_attrs(svg):
    """Deja un solo valor por atributo en cada etiqueta.

    Un motivo puede escribir `fill="#fff" fill-opacity=".1"` y luego cerrar con
    `_s(...)`, que aporta un `fill="none"` de reserva. XML no permite atributos
    duplicados, así que se colapsan aquí. **Gana la primera aparición**: lo
    escrito a propósito tiene prioridad sobre el valor por defecto del helper.
    """
    def fix(m):
        tag = m.group(0)
        head = re.match(r"<[a-zA-Z_:][-a-zA-Z0-9_:.]*", tag).group(0)
        seen, keep = set(), []
        for name, value in _ATTR.findall(tag):
            if name in seen:
                continue
            seen.add(name)
            keep.append(f'{name}="{value}"')
        closing = "/>" if tag.endswith("/>") else ">"
        return f"{head} {' '.join(keep)}{closing}"
    return re.sub(r"<[a-zA-Z_:][^>]*>", fix, svg)


# --------------------------------------------------------------------------
# Fondo
# --------------------------------------------------------------------------
def background(p, seed):
    """Degradado + retícula tenue + grano + viñeta."""
    g = math.radians(20 + (seed % 5) * 30)
    x2, y2 = math.cos(g), math.sin(g)
    return f'''<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="{x2:.2f}" y2="{y2:.2f}">
    <stop offset="0%" stop-color="{p['bg1']}"/>
    <stop offset="100%" stop-color="{p['bg2']}"/>
  </linearGradient>
  <radialGradient id="vig" cx="50%" cy="45%" r="78%">
    <stop offset="58%" stop-color="#000000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.26"/>
  </radialGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="3"
                  seed="{seed % 97}" result="n"/>
    <feColorMatrix in="n" type="saturate" values="0"/>
    <feComponentTransfer><feFuncA type="linear" slope="0.5"/></feComponentTransfer>
  </filter>
  <linearGradient id="scrim" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{p['bg1']}" stop-opacity="0.97"/>
    <stop offset="40%" stop-color="{p['bg1']}" stop-opacity="0.90"/>
    <stop offset="55%" stop-color="{p['bg1']}" stop-opacity="0.55"/>
    <stop offset="66%" stop-color="{p['bg1']}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#vig)"/>
<g opacity="0.045" stroke="{p['ink']}" stroke-width="1">
  {"".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H, 90))}
</g>
<rect width="{W}" height="{H}" filter="url(#grain)" opacity="0.028"/>'''


# --------------------------------------------------------------------------
# Portada completa
# --------------------------------------------------------------------------
def seed_of(slug):
    """Semilla estable a partir del slug.

    No se usa `hash()`: el hash de las cadenas en Python está aleatorizado por
    proceso (PYTHONHASHSEED), así que dos ejecuciones darían portadas distintas
    y el fichero cambiaría en cada commit sin motivo.
    """
    return int.from_bytes(hashlib.sha256(slug.encode()).digest()[:4], "big")


def build_svg(meta, seed=None):
    """`meta` necesita: slug, title, eyebrow, motif, palette y opcionalmente
    kicker, sub, year, opts."""
    palette = PALETTES[meta["palette"]]
    p = palette
    motif = MOTIFS[meta["motif"]]
    seed = seed if seed is not None else seed_of(meta["slug"])
    rng = random.Random(seed)

    art = dedupe_attrs(motif(p, rng, W, H, meta.get("opts", {})))

    title = meta["title"]
    # Tamaño del título: 3 líneas como mucho, 62 → 34 px.
    size, lines = fit(title, "display", TEXT_W,
                      [62, 56, 50, 46, 42, 38, 34], 3, tracking=-0.5)
    leading = size * 1.08
    block_h = leading * len(lines)
    top = PAD + 118
    if block_h > 300:                     # títulos muy largos: subir el bloque
        top = PAD + 96

    text = []
    # eyebrow
    eyebrow = meta.get("eyebrow", "")
    if eyebrow:
        text.append(
            f'<text x="{PAD}" y="{PAD+24}" font-family="{FONT_MONO}" '
            f'font-size="15" letter-spacing="3.4" fill="{p["accent"]}" '
            f'font-weight="500">{esc(eyebrow.upper())}</text>')
    # regla corta bajo el eyebrow
    text.append(f'<rect x="{PAD}" y="{PAD+42}" width="56" height="3" rx="1.5" '
                f'fill="{p["accent"]}" fill-opacity="0.9"/>')

    # título
    for i, line in enumerate(lines):
        y = top + i * leading
        text.append(f'<text x="{PAD}" y="{y:.1f}" font-family="{FONT_DISPLAY}" '
                    f'font-size="{size}" font-weight="900" '
                    f'letter-spacing="-0.5" fill="{p["ink"]}">{esc(line)}</text>')

    # línea fina + subtítulo
    y_rule = top + block_h + 16
    text.append(f'<line x1="{PAD}" y1="{y_rule:.1f}" x2="{PAD+64}" '
                f'y2="{y_rule:.1f}" stroke="{p["accent2"]}" '
                f'stroke-width="1.6" stroke-opacity="0.8"/>')
    sub = meta.get("sub", "")
    if sub:
        ssize = 19
        slines = wrap(sub, "serif", ssize, TEXT_W)[:3]
        for i, line in enumerate(slines):
            text.append(f'<text x="{PAD}" y="{y_rule+34+i*(ssize*1.35):.1f}" '
                        f'font-family="{FONT_SERIF}" font-size="{ssize}" '
                        f'font-style="italic" fill="{p["accent2"]}" '
                        f'fill-opacity="0.85">{esc(line)}</text>')

    # pie
    k = meta.get("kicker", "")
    text.append(f'<line x1="{PAD}" y1="{H-72}" x2="{PAD+40}" y2="{H-72}" '
                f'stroke="{p["line"]}" stroke-width="1" stroke-opacity="0.7"/>')
    foot = " · ".join(x for x in (k, "jimenezgomez.org", meta.get("year", "2026")) if x)
    text.append(f'<text x="{PAD}" y="{H-46}" font-family="{FONT_MONO}" '
                f'font-size="14" letter-spacing="1.8" fill="{p["line"]}" '
                f'fill-opacity="0.95">{esc(foot.upper())}</text>')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">\n{background(p, seed)}\n'
           f'<g opacity="1">{art}</g>\n'
           f'<rect width="{W}" height="{H}" fill="url(#scrim)"/>\n'
           f'{"".join(text)}\n</svg>\n')
    return dedupe_attrs(svg)


# --------------------------------------------------------------------------
# Lectura del artículo
# --------------------------------------------------------------------------
def read_frontmatter(post_dir: Path):
    idx = post_dir / "index.md"
    if not idx.exists():
        return {}
    text = idx.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        m = re.match(r"^\+\+\+\n(.*?)\n\+\+\+\n", text, re.S)
    if not m:
        return {}
    fm, out = m.group(1), {}
    for line in fm.splitlines():
        mm = re.match(r'^(title|date|description)\s*:\s*"?(.*?)"?\s*$', line)
        if mm:
            out[mm.group(1)] = mm.group(2)
    return out


def title_of(post_dir: Path):
    fm = read_frontmatter(post_dir)
    t = fm.get("title")
    if t:
        return t
    return post_dir.name.split("-", 3)[-1].replace("-", " ").title()


def year_of(post_dir: Path):
    fm = read_frontmatter(post_dir)
    d = fm.get("date", "")
    m = re.match(r"(\d{4})", d)
    if m:
        return m.group(1)
    return post_dir.name[:4]


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower())
    return s.strip("-")
