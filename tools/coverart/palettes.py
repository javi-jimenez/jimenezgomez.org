"""Paletas para las portadas.

Cada portada usa una paleta completa (fondo, tinta, acento, línea). La regla es
que **ninguna portada repita la combinación de otra**: el color es lo primero
que distingue un artículo de otro en una lista.
"""

PALETTES = {
    # --- oscuras ---------------------------------------------------------
    "ember": {
        "bg1": "#170f0a", "bg2": "#3b1d13", "ink": "#fdf1e7",
        "accent": "#ff8f4d", "accent2": "#ffd8a8", "line": "#b9825f",
    },
    "forest": {
        "bg1": "#07120c", "bg2": "#123121", "ink": "#eaf7ef",
        "accent": "#6fe3a3", "accent2": "#c9f2d8", "line": "#6f9f86",
    },
    "plum": {
        "bg1": "#140a19", "bg2": "#2f1137", "ink": "#f8ecff",
        "accent": "#d98cff", "accent2": "#f3c9ff", "line": "#a37bb4",
    },
    "golds": {
        "bg1": "#0b1016", "bg2": "#1b2432", "ink": "#f6f3ec",
        "accent": "#e2b552", "accent2": "#f3e0b6", "line": "#8496ab",
    },
    "teal": {
        "bg1": "#031518", "bg2": "#0a3339", "ink": "#e6fbf8",
        "accent": "#4fe3d1", "accent2": "#b7f5ec", "line": "#5f9d9b",
    },
    "burgundy": {
        "bg1": "#160507", "bg2": "#3b0d17", "ink": "#fdecef",
        "accent": "#ff6b8a", "accent2": "#ffd0cf", "line": "#a5626f",
    },
    "indigo": {
        "bg1": "#08091b", "bg2": "#181b4c", "ink": "#eef0ff",
        "accent": "#8b9dff", "accent2": "#cdd5ff", "line": "#757ead",
    },
    "amber": {
        "bg1": "#130f09", "bg2": "#2f2414", "ink": "#fdf4dd",
        "accent": "#ffb703", "accent2": "#ffe4a3", "line": "#a08a62",
    },
    "ice": {
        "bg1": "#07111f", "bg2": "#123145", "ink": "#eaf6fd",
        "accent": "#7dd3fc", "accent2": "#d3ecf9", "line": "#7494a8",
    },
    "sand": {
        "bg1": "#140f09", "bg2": "#302716", "ink": "#f8f1e2",
        "accent": "#cfa36b", "accent2": "#f0e2c8", "line": "#9a8768",
    },
    "moss": {
        "bg1": "#0b1008", "bg2": "#1e2b12", "ink": "#f1f7e4",
        "accent": "#b5d96b", "accent2": "#e6f4c4", "line": "#849463",
    },
    "rust": {
        "bg1": "#190c07", "bg2": "#3c1b10", "ink": "#fdeee6",
        "accent": "#ff7043", "accent2": "#ffcbb4", "line": "#ab7a63",
    },
    "violet": {
        "bg1": "#0a091d", "bg2": "#231a47", "ink": "#f0ebff",
        "accent": "#b39dff", "accent2": "#ded3ff", "line": "#847ba5",
    },
    "graphite": {
        "bg1": "#0b0b0d", "bg2": "#23232b", "ink": "#f2f2f5",
        "accent": "#f2f2f5", "accent2": "#b9b9c4", "line": "#85858f",
    },
    "cobalt": {
        "bg1": "#040b18", "bg2": "#0f2c53", "ink": "#eaf5ff",
        "accent": "#38bdf8", "accent2": "#c2ecff", "line": "#6d90b3",
    },
    "copper": {
        "bg1": "#110c0a", "bg2": "#2c1a12", "ink": "#faf0e6",
        "accent": "#e07a5f", "accent2": "#f2cc8f", "line": "#a08273",
    },
    "ink": {
        "bg1": "#050608", "bg2": "#14161c", "ink": "#f7f8fa",
        "accent": "#d9e2ec", "accent2": "#9fb3c8", "line": "#5c6b7a",
    },
    "wine": {
        "bg1": "#120611", "bg2": "#31132c", "ink": "#fbeef8",
        "accent": "#f472b6", "accent2": "#fbcfe8", "line": "#9d6b8e",
    },
    "ocean": {
        "bg1": "#02101c", "bg2": "#07304a", "ink": "#e8fbff",
        "accent": "#5eead4", "accent2": "#b8f5ea", "line": "#5f92a8",
    },
    "sepia": {
        "bg1": "#0f0b06", "bg2": "#2c2013", "ink": "#fbf3e4",
        "accent": "#d9a066", "accent2": "#efd9b8", "line": "#9b8365",
    },
    "midnight": {
        "bg1": "#060812", "bg2": "#131a33", "ink": "#f2f5ff",
        "accent": "#a5b4fc", "accent2": "#dbe2ff", "line": "#6b7398",
    },
    # --- claras (editorial) ---------------------------------------------
    "paper": {
        "bg1": "#f5f2ea", "bg2": "#e4ddcf", "ink": "#1a1712",
        "accent": "#b4472b", "accent2": "#7a6a55", "line": "#c2b8a4",
    },
    "papercool": {
        "bg1": "#f2f4f7", "bg2": "#dde4ec", "ink": "#111720",
        "accent": "#1f4e79", "accent2": "#5b7086", "line": "#b9c4d1",
    },
    "paperwarm": {
        "bg1": "#fbf6ec", "bg2": "#efe3cd", "ink": "#20190f",
        "accent": "#b5651d", "accent2": "#7d6a4e", "line": "#d3c3a5",
    },
}

# Nombres de fuente que existen en el sistema (comprobados con fc-list).
FONT_DISPLAY = "Inter Display, Inter, DejaVu Sans, sans-serif"
FONT_MONO = "IBM Plex Mono, DejaVu Sans Mono, monospace"
FONT_SERIF = "EB Garamond, DejaVu Serif, serif"

# Rutas TTF/OTF para medir texto con PIL (wrapping exacto).
FONT_FILES = {
    "display": "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf",
    "display-semibold": "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf",
    "mono": "/usr/share/fonts/truetype/ibm-plex/IBMPlexMono-Regular.ttf",
    "mono-bold": "/usr/share/fonts/truetype/ibm-plex/IBMPlexMono-Medium.ttf",
    "serif": "/usr/share/fonts/truetype/ebgaramond/EBGaramond08-Regular.ttf",
}
