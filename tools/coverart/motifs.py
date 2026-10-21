"""Motivos geométricos para las portadas.

Cada motivo es una función `m_<nombre>(p, rng, W, H, o)` que devuelve un trozo
de SVG. `p` es la paleta, `rng` un `random.Random` ya sembrado (misma portada,
mismo dibujo) y `o` un dict con opciones puntuales del artículo.

Reglas de estilo, para que 39 portadas distintas parezcan de la misma casa:
  · trazos finos (1–2 px) con extremos redondeados;
  · como mucho un elemento relleno con el acento, a baja opacidad;
  · nada de degradados dentro del motivo: el color plano hace que se lea;
  · el motivo vive a la derecha; la izquierda es para el texto.
"""

import math

CX, CY = 830, 315          # centro del área de dibujo
AW, AH = 700, 560          # ancho/alto de referencia del área


def _s(color, w=1.4, op=0.6, dash=None, cap="round", fill="none"):
    """Atributos de trazo. Lleva espacio inicial: se concatena tras otro atributo.

    `fill` es "none" por defecto; si el motivo necesita un relleno, se pasa aquí
    en vez de escribir un `fill=` suelto (que duplicaría el atributo en el XML).
    """
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f' stroke="{color}" stroke-width="{w}" stroke-opacity="{op}" '
            f'fill="{fill}" stroke-linecap="{cap}" stroke-linejoin="round"{d}')


def _poly(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


# --------------------------------------------------------------------------
# Redes y sistemas
# --------------------------------------------------------------------------
def m_mesh(p, rng, W, H, o):
    """Malla de nodos. Para artículos de redes y colaboración."""
    out = []
    cols, rows = 4, 3
    x0, y0, dx, dy = 600, 150, 165, 165
    pts = []
    for j in range(rows):
        for i in range(cols):
            jitter = 18
            pts.append((x0 + i * dx + rng.uniform(-jitter, jitter),
                        y0 + j * dy + rng.uniform(-jitter, jitter)))
    # enlaces
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            d = math.dist(pts[a], pts[b])
            if d < dx * 1.15:
                out.append(f'<line x1="{pts[a][0]:.1f}" y1="{pts[a][1]:.1f}" '
                           f'x2="{pts[b][0]:.1f}" y2="{pts[b][1]:.1f}"'
                           f'{_s(p["line"], 1.3, 0.45)}/>')
    # nodos
    for i, (x, y) in enumerate(pts):
        if i == 5:  # el nodo que importa
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="26" '
                       f'fill="{p["accent"]}" fill-opacity="0.14"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" '
                       f'fill="{p["accent"]}"/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" '
                       f'{_s(p["accent2"], 1.5, 0.75)}/>')
    return "".join(out)


def m_neural(p, rng, W, H, o):
    """Capas de nodos con conexiones. Para IA / desarrollo con IA."""
    out = []
    layers = [3, 5, 5, 2]
    xs = [640, 780, 920, 1060]
    nodes = []
    for li, n in enumerate(layers):
        col = []
        for k in range(n):
            y = CY + (k - (n - 1) / 2) * 78
            col.append((xs[li], y))
        nodes.append(col)
    for li in range(len(nodes) - 1):
        for a in nodes[li]:
            for b in nodes[li + 1]:
                out.append(f'<line x1="{a[0]}" y1="{a[1]:.1f}" '
                           f'x2="{b[0]}" y2="{b[1]:.1f}"'
                           f'{_s(p["line"], 0.9, 0.22)}/>')
    for li, col in enumerate(nodes):
        for x, y in col:
            fill = p["accent"] if li in (0, 3) else "none"
            if fill == "none":
                out.append(f'<circle cx="{x}" cy="{y:.1f}" r="7" '
                           f'{_s(p["accent2"], 1.6, 0.85)}/>')
            else:
                out.append(f'<circle cx="{x}" cy="{y:.1f}" r="8" '
                           f'fill="{fill}" fill-opacity="0.9"/>')
    return "".join(out)


def m_circuit(p, rng, W, H, o):
    """Pistas ortogonales saliendo de un chip. Para tecnología base."""
    out = []
    cw, ch = 150, 150
    out.append(f'<rect x="{CX-cw/2}" y="{CY-ch/2}" width="{cw}" height="{ch}" '
               f'rx="8" fill="{p["accent"]}" fill-opacity="0.10"/>')
    out.append(f'<rect x="{CX-cw/2}" y="{CY-ch/2}" width="{cw}" height="{ch}" '
               f'rx="8"{_s(p["accent"], 2, 0.9)}/>')
    for i in range(5):
        yy = CY - ch / 2 + 22 + i * 27
        out.append(f'<line x1="{CX-cw/2+18}" y1="{yy:.1f}" '
                   f'x2="{CX+cw/2-18}" y2="{yy:.1f}"{_s(p["accent2"], 1, 0.35)}/>')
    # pines y pistas en los cuatro lados
    for side in range(4):
        for i in range(5):
            t = -0.3 + i * 0.15
            if side == 0:
                x0, y0, x1, y1 = CX + cw / 2, CY + t * ch, CX + cw / 2 + 90, CY + t * ch * 2
            elif side == 1:
                x0, y0, x1, y1 = CX - cw / 2, CY + t * ch, CX - cw / 2 - 90, CY + t * ch * 2
            elif side == 2:
                x0, y0, x1, y1 = CX + t * cw, CY - ch / 2, CX + t * cw * 2, CY - ch / 2 - 70
            else:
                x0, y0, x1, y1 = CX + t * cw, CY + ch / 2, CX + t * cw * 2, CY + ch / 2 + 70
            out.append(f'<polyline points="{_poly([(x0,y0),(x1,y0),(x1,y1)])}"'
                       f'{_s(p["line"], 1.2, 0.42)}/>')
            out.append(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="3.5" '
                       f'fill="{p["accent2"]}" fill-opacity="0.7"/>')
    return "".join(out)


def m_mesh_ring(p, rng, W, H, o):
    """Anillo de nodos. Para sistemas operativos de red."""
    out = []
    n = 16
    ring = [(CX + 190 * math.cos(2 * math.pi * i / n),
             CY + 190 * math.sin(2 * math.pi * i / n)) for i in range(n)]
    for i in range(n):
        a, b = ring[i], ring[(i + 1) % n]
        out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" '
                   f'y2="{b[1]:.1f}"{_s(p["line"], 1.2, 0.35)}/>')
        out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{CX}" y2="{CY}"'
                   f'{_s(p["line"], 0.8, 0.16)}/>')
    for i, (x, y) in enumerate(ring):
        r = 7 if i % 4 == 0 else 4
        fill = p["accent"] if i % 4 == 0 else "none"
        if fill == "none":
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" '
                       f'{_s(p["accent2"], 1.4, 0.7)}/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" '
                       f'fill="{fill}" fill-opacity="0.95"/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="46" fill="{p["accent"]}" '
               f'fill-opacity="0.12"/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="46"{_s(p["accent"], 1.8, 0.9)}/>')
    return "".join(out)


# --------------------------------------------------------------------------
# Arquitectura y capas
# --------------------------------------------------------------------------
def m_layers(p, rng, W, H, o):
    """Planos isométricos apilados."""
    out = []
    n = o.get("n", 4)
    w, h = 250, 74
    for i in range(n):
        y = 140 + i * 92
        top = [(CX, y - h / 2), (CX + w / 2, y), (CX, y + h / 2), (CX - w / 2, y)]
        op = 0.9 if i == o.get("hi", 1) else 0.4
        col = p["accent"] if i == o.get("hi", 1) else p["line"]
        out.append(f'<polygon points="{_poly(top)}" fill="{col}" '
                   f'fill-opacity="{0.12 if i == o.get("hi", 1) else 0.04}"/>')
        out.append(f'<polygon points="{_poly(top)}"{_s(col, 1.6, op)}/>')
    # eje vertical
    out.append(f'<line x1="{CX}" y1="90" x2="{CX}" y2="540"'
               f'{_s(p["accent2"], 1, 0.2, dash="3 7")}/>')
    return "".join(out)


def m_strata(p, rng, W, H, o):
    """Estratos ondulados: materiales, capas de conocimiento."""
    out = []
    bands = o.get("bands", 7)
    for i in range(bands):
        y = 110 + i * (400 / (bands - 1))
        amp = 12 + rng.uniform(0, 16)
        ph = rng.uniform(0, 6.2)
        pts = [(550 + k * 14,
                y + amp * math.sin(ph + k * 0.16)) for k in range(48)]
        hi = (i == o.get("hi", 3))
        col = p["accent"] if hi else p["line"]
        op = 0.95 if hi else 0.34
        if hi:
            out.append(f'<polygon points="{_poly(pts + [(1220, 700), (550, 700)])}" '
                       f'fill="{p["accent"]}" fill-opacity="0.09"/>')
        out.append(f'<polyline points="{_poly(pts)}"{_s(col, 1.7 if hi else 1.2, op)}/>')
    return "".join(out)


def m_fractal(p, rng, W, H, o):
    """Cuadrados anidados desplazados: arquitectura fractal (VBD)."""
    out = []
    levels = o.get("levels", 5)
    x, y, s = CX - 200, CY - 190, 380
    off = [(0, 0), (0.42, 0), (0.42, 0.42), (0, 0.42)]
    for lv in range(levels):
        cx, cy = x + s / 2, y + s / 2
        hi = (lv == 1)
        col = p["accent"] if hi else p["line"]
        op = 0.95 if hi else max(0.18, 0.55 - lv * 0.1)
        fill = (f' fill="{p["accent"]}" fill-opacity="0.08"' if hi else "")
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" '
                   f'height="{s:.1f}" rx="{s*0.04:.1f}"{fill}'
                   f'{_s(col, 1.6 if hi else 1.2, op)}/>')
        s *= 0.58
        dx, dy = off[min(lv + 1, 3)]
        x, y = cx - s / 2 + dx * s * 0.35, cy - s / 2 + dy * s * 0.35
    return "".join(out)


def m_blueprint(p, rng, W, H, o):
    """Dibujo técnico: cotas, círculos, retícula."""
    out = []
    out.append(f'<line x1="560" y1="{CY}" x2="1180" y2="{CY}"'
               f'{_s(p["line"], 1, 0.3, dash="2 6")}/>')
    out.append(f'<line x1="{CX}" y1="80" x2="{CX}" y2="550"'
               f'{_s(p["line"], 1, 0.3, dash="2 6")}/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="140" fill="none"'
               f'{_s(p["accent2"], 1.2, 0.45)}/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="92" fill="{p["accent"]}" '
               f'fill-opacity="0.08"{_s(p["accent"], 1.8, 0.9)}/>')
    for a in range(0, 360, 15):
        r1, r2 = (140, 156) if a % 45 == 0 else (140, 148)
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        out.append(f'<line x1="{CX+r1*ca:.1f}" y1="{CY+r1*sa:.1f}" '
                   f'x2="{CX+r2*ca:.1f}" y2="{CY+r2*sa:.1f}"'
                   f'{_s(p["accent2"], 1.1, 0.5)}/>')
    # cotas
    for dx in (-140, 140):
        out.append(f'<line x1="{CX+dx}" y1="{CY+170}" x2="{CX+dx}" y2="{CY+210}"'
                   f'{_s(p["line"], 1, 0.4)}/>')
    out.append(f'<line x1="{CX-140}" y1="{CY+196}" x2="{CX+140}" y2="{CY+196}"'
               f'{_s(p["accent"], 1.2, 0.7)}/>')
    return "".join(out)


def m_lattice(p, rng, W, H, o):
    """Celosía diagonal: estructura, espacio, retícula."""
    out = []
    step = 46
    for k in range(-8, 16):
        x0 = CX - 300 + k * step
        out.append(f'<line x1="{x0}" y1="60" x2="{x0+380}" y2="570"'
                   f'{_s(p["line"], 1, 0.26)}/>')
        out.append(f'<line x1="{x0}" y1="570" x2="{x0+380}" y2="60"'
                   f'{_s(p["line"], 1, 0.14)}/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="86" fill="{p["bg1"]}" '
               f'fill-opacity="0.85"/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="86"{_s(p["accent"], 2, 0.95)}/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="14" fill="{p["accent"]}"/>')
    return "".join(out)


def m_steps(p, rng, W, H, o):
    """Escalera ascendente: mejorar, subir de nivel."""
    out = []
    n = o.get("n", 5)
    bw, bh = 88, 52
    for i in range(n):
        x = 600 + i * (bw + 12)
        h = bh * (i + 1)
        y = 520 - h
        hi = (i == n - 1)
        col = p["accent"] if hi else p["line"]
        out.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" rx="6" '
                   f'fill="{col}" fill-opacity="{0.16 if hi else 0.05}"/>')
        out.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" rx="6"'
                   f'{_s(col, 1.5, 0.9 if hi else 0.4)}/>')
    # flecha
    out.append(f'<path d="M 590 500 C 760 480, 960 420, 1105 190" '
               f'{_s(p["accent2"], 2, 0.85)}/>')
    out.append(f'<polygon points="{_poly([(1105,190),(1078,205),(1092,228)])}" '
               f'fill="{p["accent2"]}" fill-opacity="0.9"/>')
    return "".join(out)


def m_bars(p, rng, W, H, o):
    """Barras de alturas variables: métricas, rendimiento."""
    out = []
    n = o.get("n", 14)
    for i in range(n):
        x = 580 + i * 44
        h = 60 + abs(math.sin(i * 0.7 + rng.uniform(0, 0.5))) * 320
        hi = (i == o.get("hi", 9))
        col = p["accent"] if hi else p["line"]
        out.append(f'<rect x="{x}" y="{520-h:.1f}" width="22" height="{h:.1f}" '
                   f'rx="11" fill="{col}" fill-opacity="{0.85 if hi else 0.16}"/>')
    return "".join(out)


# --------------------------------------------------------------------------
# Símbolos y abstracción
# --------------------------------------------------------------------------
def m_symbols(p, rng, W, H, o):
    """Retícula de símbolos formales: la serie LAIA."""
    out = []
    glyphs = o.get("glyphs", ["∑", "⊢", "∎", "ƒ", "∴", "Θ"])
    cx0, cy0 = 660, 150
    for j in range(2):
        for i in range(3):
            x = cx0 + i * 190
            y = cy0 + j * 190
            g = glyphs[(j * 3 + i) % len(glyphs)]
            hi = (j * 3 + i) == o.get("hi", 2)
            out.append(f'<rect x="{x-70}" y="{y-70}" width="140" height="140" '
                       f'rx="10" fill="{p["accent"]}" '
                       f'fill-opacity="{0.14 if hi else 0.04}"'
                       f'{_s(p["accent"] if hi else p["line"], 1.4, 0.95 if hi else 0.45)}/>')
            out.append(f'<text x="{x}" y="{y+22}" text-anchor="middle" '
                       f'font-family="EB Garamond, DejaVu Serif, serif" '
                       f'font-size="64" fill="{p["accent"] if hi else p["accent2"]}" '
                       f'fill-opacity="{1 if hi else 0.85}">{g}</text>')
    return "".join(out)


def m_star(p, rng, W, H, o):
    """Estrella geométrica de 8 puntas: identidad de marca."""
    out = []
    R, r = o.get("R", 190), o.get("r", 74)
    for rot, w, op in ((0, 2, 0.95), (22.5, 1.1, 0.4)):
        pts = []
        for i in range(16):
            ang = math.radians(-90 + rot + i * 22.5)
            rad = R if i % 2 == 0 else r
            pts.append((CX + rad * math.cos(ang), CY + rad * math.sin(ang)))
        out.append(f'<polygon points="{_poly(pts)}" fill="{p["accent"]}" '
                   f'fill-opacity="{0.10 if op > 0.5 else 0.0}"{_s(p["accent"], w, op)}/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="16" fill="{p["accent"]}"/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="{R+34}" fill="none"'
               f'{_s(p["line"], 1, 0.35, dash="4 8")}/>')
    return "".join(out)


def m_orbits(p, rng, W, H, o):
    """Órbitas concéntricas: DNS universal, escala planetaria."""
    out = []
    for i, (rx, ry) in enumerate([(90, 44), (150, 74), (215, 106), (280, 138)]):
        rot = -18 + i * 8
        out.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{ry}" '
                   f'transform="rotate({rot} {CX} {CY})" fill="none"'
                   f'{_s(p["line"] if i else p["accent"], 1.4 if i == 0 else 1.1, 0.8 if i == 0 else 0.32)}/>')
        a = math.radians(rot + 40 + i * 30)
        px = CX + rx * math.cos(a)
        py = CY + ry * math.sin(a)
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{6-i*0.8}" '
                   f'fill="{p["accent"] if i % 2 == 0 else p["accent2"]}" '
                   f'fill-opacity="0.9"/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="22" fill="{p["accent"]}" '
               f'fill-opacity="0.9"/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="44" fill="none"'
               f'{_s(p["accent"], 1, 0.35)}/>')
    return "".join(out)


def m_duality(p, rng, W, H, o):
    """Orden a la izquierda, dispersión a la derecha: formal vs ML."""
    out = []
    mid = CX
    # izquierda: retícula exacta
    for j in range(9):
        for i in range(5):
            x, y = mid - 250 + i * 40, 130 + j * 44
            out.append(f'<rect x="{x}" y="{y}" width="16" height="16" rx="2" '
                       f'fill="{p["accent"]}" fill-opacity="0.75"/>')
    # derecha: puntos dispersos
    for _ in range(90):
        x = mid + 40 + rng.uniform(0, 250)
        y = 120 + rng.uniform(0, 400)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rng.uniform(1.5,5):.1f}" '
                   f'fill="{p["accent2"]}" fill-opacity="{rng.uniform(0.25,0.85):.2f}"/>')
    out.append(f'<line x1="{mid}" y1="100" x2="{mid}" y2="525"'
               f'{_s(p["line"], 1.2, 0.55, dash="4 8")}/>')
    return "".join(out)


def m_flow(p, rng, W, H, o):
    """Trazos que convergen en uno: callbacks, contratos, interfaces."""
    out = []
    ys = [175, 240, 315, 390, 455]
    for i, y in enumerate(ys):
        out.append(f'<path d="M 600 {y} C 780 {y}, 860 {CY}, 1000 {CY}" '
                   f'{_s(p["line"], 1.3, 0.4)}/>')
        out.append(f'<circle cx="600" cy="{y}" r="5" fill="{p["accent2"]}" '
                   f'fill-opacity="0.55"/>')
    out.append(f'<path d="M 1000 {CY} L 1130 {CY}" fill="none"'
               f'{_s(p["accent"], 2.6, 0.95)}/>')
    out.append(f'<polygon points="{_poly([(1150,CY),(1120,CY-13),(1120,CY+13)])}" '
               f'fill="{p["accent"]}"/>')
    out.append(f'<circle cx="1000" cy="{CY}" r="26" fill="{p["accent"]}" '
               f'fill-opacity="0.14"{_s(p["accent"], 1.6, 0.9)}/>')
    return "".join(out)


def m_dots(p, rng, W, H, o):
    """Trama de puntos con densidad creciente: datos, ruido, señal."""
    out = []
    step = 30
    for j in range(15):
        for i in range(20):
            x = 570 + i * step
            y = 100 + j * step
            d = math.dist((x, y), (CX + 60, CY))
            r = max(0.8, 7.5 - d / 55)
            op = max(0.06, min(0.85, 1.1 - d / 420))
            out.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" '
                       f'fill="{p["accent2"]}" fill-opacity="{op:.2f}"/>')
    return "".join(out)


def m_waves(p, rng, W, H, o):
    """Ondas de señal: conectividad, resiliencia."""
    out = []
    for i in range(9):
        y0 = 150 + i * 44
        amp = 18 + i * 2.5
        pts = [(570 + k * 16, y0 + amp * math.sin(k * 0.28 + i * 0.5))
               for k in range(38)]
        col = p["accent"] if i == 4 else p["line"]
        out.append(f'<polyline points="{_poly(pts)}"'
                   f'{_s(col, 2.1 if i == 4 else 1.4, 0.95 if i == 4 else 0.45)}/>')
    return "".join(out)


def m_rays(p, rng, W, H, o):
    """Rayos radiales: luz, fe, convicción."""
    out = []
    ox, oy = CX + 150, CY + 210
    for a in range(0, 360, 9):
        rad = math.radians(a)
        r1, r2 = 60, 60 + rng.uniform(220, 420)
        out.append(f'<line x1="{ox+r1*math.cos(rad):.1f}" '
                   f'y1="{oy+r1*math.sin(rad):.1f}" '
                   f'x2="{ox+r2*math.cos(rad):.1f}" '
                   f'y2="{oy+r2*math.sin(rad):.1f}"'
                   f'{_s(p["accent2"], 1, 0.16)}/>')
    out.append(f'<circle cx="{ox}" cy="{oy}" r="58" fill="{p["accent"]}" '
               f'fill-opacity="0.16"{_s(p["accent"], 2, 0.95)}/>')
    return "".join(out)


def m_dunes(p, rng, W, H, o):
    """Dunas y brillo: espejismo."""
    out = []
    for i in range(6):
        y = 300 + i * 48
        amp = 26 + i * 6
        pts = [(560 + k * 18, y + amp * math.sin(k * 0.11 + i * 1.3))
               for k in range(36)]
        col = p["accent"] if i == 0 else p["line"]
        out.append(f'<polyline points="{_poly(pts)}"'
                   f'{_s(col, 2 if i == 0 else 1.2, 0.9 if i == 0 else 0.3)}/>')
    for i in range(5):
        y = 250 + i * 12
        out.append(f'<line x1="{700+i*20}" y1="{y}" x2="{1080-i*30}" y2="{y}"'
                   f'{_s(p["accent2"], 1, 0.10)}/>')
    return "".join(out)


def m_mask(p, rng, W, H, o):
    """Círculo mitad iluminado: lo encubierto."""
    out = []
    out.append(f'<circle cx="{CX}" cy="{CY}" r="170" fill="{p["accent"]}" '
               f'fill-opacity="0.10"/>')
    out.append(f'<path d="M {CX} {CY-170} A 170 170 0 0 1 {CX} {CY+170} Z" '
               f'fill="{p["bg1"]}" fill-opacity="0.55"/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="170"{_s(p["accent"], 2, 0.95)}/>')
    out.append(f'<line x1="{CX}" y1="{CY-200}" x2="{CX}" y2="{CY+200}"'
               f'{_s(p["accent2"], 1.2, 0.5, dash="4 8")}/>')
    return "".join(out)


def m_chaos(p, rng, W, H, o):
    """Caos que se ordena: domar la IA."""
    out = []
    for i in range(120):
        x = 570 + rng.uniform(0, 240)
        y = 100 + rng.uniform(0, 420)
        a = rng.uniform(0, 360)
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" '
                   f'x2="{x+16*math.cos(math.radians(a)):.1f}" '
                   f'y2="{y+16*math.sin(math.radians(a)):.1f}"'
                   f'{_s(p["accent2"], 1.2, 0.45)}/>')
    step = 26
    for j in range(16):
        for i in range(10):
            x, y = 860 + i * step, 130 + j * step
            out.append(f'<rect x="{x}" y="{y}" width="14" height="14" rx="2" '
                       f'fill="{p["accent"]}" fill-opacity="{0.10+0.03*((i+j)%4):.2f}"/>')
    return "".join(out)


def m_seal(p, rng, W, H, o):
    """Sello circular con marcas: contratos, garantías."""
    out = []
    out.append(f'<circle cx="{CX}" cy="{CY}" r="150" fill="{p["accent"]}" '
               f'fill-opacity="0.07"{_s(p["accent"], 2.2, 0.95)}/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="126" fill="none"'
               f'{_s(p["accent2"], 1, 0.4)}/>')
    for a in range(0, 360, 6):
        r1, r2 = (150, 168) if a % 30 == 0 else (150, 158)
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        out.append(f'<line x1="{CX+r1*ca:.1f}" y1="{CY+r1*sa:.1f}" '
                   f'x2="{CX+r2*ca:.1f}" y2="{CY+r2*sa:.1f}"'
                   f'{_s(p["accent2"], 1, 0.45)}/>')
    for i, yy in enumerate((-34, 0, 34)):
        out.append(f'<line x1="{CX-62}" y1="{CY+yy}" x2="{CX+62}" y2="{CY+yy}"'
                   f'{_s(p["accent"], 3, 0.75)}/>')
    return "".join(out)


def m_tiles(p, rng, W, H, o):
    """Cuadrícula de baldosas redondeadas: apps, lanzadores."""
    out = []
    s, gap = 88, 22
    for j in range(3):
        for i in range(3):
            x = 640 + i * (s + gap)
            y = 145 + j * (s + gap)
            hi = (i, j) == (1, 1)
            col = p["accent"] if hi else p["accent2"]
            out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="20" '
                       f'fill="{col}" fill-opacity="{0.22 if hi else 0.06}"'
                       f'{_s(col, 1.6, 0.95 if hi else 0.32)}/>')
            # glifo mínimo dentro
            out.append(f'<circle cx="{x+s/2}" cy="{y+s/2}" r="{20 if hi else 12}" '
                       f'{_s(col, 1.6, 0.8 if hi else 0.35)}/>')
    return "".join(out)


def m_container(p, rng, W, H, o):
    """Caja isométrica abierta con contenido: el contenedor universal."""
    out = []
    w, h, d = 210, 130, 60
    top = [(CX, CY - h / 2 - d), (CX + w, CY - h / 2), (CX, CY - h / 2 + d),
           (CX - w, CY - h / 2)]
    left = [(CX - w, CY - h / 2), (CX, CY - h / 2 + d), (CX, CY + h + d / 2),
            (CX - w, CY + h / 2)]
    right = [(CX + w, CY - h / 2), (CX, CY - h / 2 + d), (CX, CY + h + d / 2),
             (CX + w, CY + h / 2)]
    out.append(f'<polygon points="{_poly(left)}" fill="{p["accent"]}" fill-opacity="0.10"/>')
    out.append(f'<polygon points="{_poly(right)}" fill="{p["accent"]}" fill-opacity="0.05"/>')
    out.append(f'<polygon points="{_poly(top)}" fill="{p["accent2"]}" fill-opacity="0.14"/>')
    for poly in (top, left, right):
        out.append(f'<polygon points="{_poly(poly)}"{_s(p["accent"], 1.7, 0.9)}/>')
    # registros dentro
    for i in range(4):
        yy = CY - 20 + i * 30
        out.append(f'<line x1="{CX-w+34}" y1="{yy}" x2="{CX-34}" y2="{yy+d/2}"'
                   f'{_s(p["accent2"], 1.1, 0.45)}/>')
    return "".join(out)


def m_telescope(p, rng, W, H, o):
    """Rectángulos que se hunden: contexto, sesiones, memoria."""
    out = []
    n = o.get("n", 6)
    for i in range(n):
        k = i / (n - 1)
        w, h = 420 * (1 - 0.62 * k), 260 * (1 - 0.62 * k)
        x, y = CX - w / 2 + k * 60, CY - h / 2 - k * 20
        op = 0.85 - k * 0.6
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
                   f'height="{h:.1f}" rx="8" fill="{p["accent"]}" '
                   f'fill-opacity="{0.12*(1-k):.3f}"'
                   f'{_s(p["accent"] if i == 0 else p["accent2"], 1.6 - k, op)}/>')
    return "".join(out)


def m_quote(p, rng, W, H, o):
    """Comillas tipográficas de gran tamaño, como lámina de cuaderno."""
    out = []
    out.append(f'<text x="{CX - 60}" y="{CY + 60}" text-anchor="middle" '
               f'font-family="EB Garamond, DejaVu Serif, serif" font-size="300" '
               f'fill="{p["accent"]}" fill-opacity="0.9">&#8220;</text>')
    # renglones de texto sugeridos
    for i, w in enumerate((300, 268, 292, 210)):
        y = 400 + i * 34
        out.append(f'<line x1="{CX - 130}" y1="{y}" x2="{CX - 130 + w}" y2="{y}"'
                   f'{_s(p["accent2"], 3, 0.22)}/>')
    out.append(f'<line x1="{CX}" y1="110" x2="{CX}" y2="250"'
               f'{_s(p["line"], 1.2, 0.5)}/>')
    return "".join(out)


def m_bricks(p, rng, W, H, o):
    """Muro que se descompone en bloques pequeños: monolito → microservicios."""
    out = []
    bw, bh = 84, 42
    for j in range(9):
        off = 0 if j % 2 == 0 else bw / 2
        for i in range(7):
            x = 590 + i * (bw + 6) + off
            y = 130 + j * (bh + 6)
            if x > 1150:
                continue
            solid = i < o.get("split", 3)
            if solid:
                out.append(f'<rect x="{x:.1f}" y="{y}" width="{bw}" height="{bh}" '
                           f'rx="3" fill="{p["line"]}" fill-opacity="0.10"'
                           f'{_s(p["line"], 1.1, 0.45)}/>')
            else:
                out.append(f'<rect x="{x+18:.1f}" y="{y+8}" width="48" height="26" '
                           f'rx="3" fill="{p["accent"]}" fill-opacity="0.10"'
                           f'{_s(p["accent"], 1.2, 0.65)}/>')
    return "".join(out)


def m_arrow(p, rng, W, H, o):
    """Flecha diagonal de progreso."""
    out = []
    out.append(f'<path d="M 600 500 L 1080 160" {_s(p["line"], 10, 0.10)}/>')
    out.append(f'<path d="M 600 500 L 1080 160" {_s(p["accent"], 2.4, 0.95)}/>')
    out.append(f'<polygon points="{_poly([(1105,142),(1050,170),(1078,200)])}" '
               f'fill="{p["accent"]}" fill-opacity="0.95"/>')
    for i in range(4):
        out.append(f'<circle cx="{620+i*120}" cy="{490-i*82}" r="6" '
                   f'{_s(p["accent2"], 1.4, 0.5)}/>')
    return "".join(out)


def m_plinth(p, rng, W, H, o):
    """Placa sobre una pila hueca vs cimiento bajo la pila: ética como adorno
    frente a ética como infraestructura. Es la tesis del artículo que la usa.
    """
    out = []
    x0, x1 = CX - 235, CX + 235

    # --- izquierda: placa decorativa encima de bloques que no la tocan ---
    out.append(f'<rect x="{x0}" y="120" width="210" height="44" rx="6" '
               f'fill="{p["accent2"]}" fill-opacity="0.06"')
    out.append(f'<rect x="{x0}" y="120" width="210" height="44" rx="6"'
               f'{_s(p["line"], 1.4, 0.8, dash="6 5")}/>')
    for i in range(3):
        y = 210 + i * 66
        out.append(f'<rect x="{x0}" y="{y}" width="210" height="52" rx="5" '
                   f'fill="{p["accent2"]}" fill-opacity="0.04"'
                   f'{_s(p["line"], 1.2, 0.32)}/>')
    # el hueco: la placa flota
    out.append(f'<line x1="{x0+105}" y1="168" x2="{x0+105}" y2="206"'
               f'{_s(p["line"], 1, 0.35, dash="2 6")}/>')

    # --- derecha: cimiento grueso bajo la pila, con apoyos ---
    for i in range(3):
        y = 150 + i * 66
        out.append(f'<rect x="{x1-210}" y="{y}" width="210" height="52" rx="5" '
                   f'fill="{p["accent"]}" fill-opacity="0.05"'
                   f'{_s(p["accent"], 1.2, 0.45)}/>')
    out.append(f'<rect x="{x1-218}" y="366" width="226" height="58" rx="7" '
               f'fill="{p["accent"]}" fill-opacity="0.16"')
    out.append(f'<rect x="{x1-218}" y="366" width="226" height="58" rx="7"'
               f'{_s(p["accent"], 2.2, 0.95)}/>')
    for dx in (40, 113, 186):
        out.append(f'<line x1="{x1-218+dx}" y1="346" x2="{x1-218+dx}" y2="364"'
                   f'{_s(p["accent"], 1.6, 0.7)}/>')

    # suelo y eje de separación
    out.append(f'<line x1="560" y1="500" x2="1180" y2="500"'
               f'{_s(p["line"], 1, 0.3)}/>')
    out.append(f'<line x1="{CX}" y1="100" x2="{CX}" y2="520"'
               f'{_s(p["line"], 1, 0.22, dash="3 9")}/>')
    return "".join(out)


MOTIFS = {
    "mesh": m_mesh,
    "neural": m_neural,
    "circuit": m_circuit,
    "ring": m_mesh_ring,
    "layers": m_layers,
    "strata": m_strata,
    "fractal": m_fractal,
    "blueprint": m_blueprint,
    "lattice": m_lattice,
    "steps": m_steps,
    "bars": m_bars,
    "symbols": m_symbols,
    "star": m_star,
    "orbits": m_orbits,
    "duality": m_duality,
    "flow": m_flow,
    "dots": m_dots,
    "waves": m_waves,
    "rays": m_rays,
    "dunes": m_dunes,
    "mask": m_mask,
    "chaos": m_chaos,
    "seal": m_seal,
    "tiles": m_tiles,
    "container": m_container,
    "telescope": m_telescope,
    "quote": m_quote,
    "bricks": m_bricks,
    "arrow": m_arrow,
    "plinth": m_plinth,
}
