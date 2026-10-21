"""Portadas generativas para los artículos de jimenezgomez.org.

Cada artículo tiene un motivo (dibujo) y una paleta propios, definidos en
`specs.py`. El resultado es un SVG de 1200×630 que se rasteriza a PNG, porque
las redes sociales no renderizan SVG en `og:image`.
"""

from .compose import build_svg
from .palettes import PALETTES
from .specs import SPECS

__all__ = ["build_svg", "PALETTES", "SPECS"]
