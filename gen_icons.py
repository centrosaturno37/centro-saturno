"""Genera los iconos de la PWA Centro Saturno: pentaculo dorado sobre fondo
degradado morado/negro con anillo rojo, siguiendo la paleta de index.html.
Se ejecuta una sola vez para producir los PNG en icons/.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter

OUT_DIR = os.path.join(os.path.dirname(__file__), "icons")
os.makedirs(OUT_DIR, exist_ok=True)

GOLD = (212, 168, 48, 255)
GOLD_L = (240, 200, 96, 255)
RED_D = (96, 0, 16, 255)
RED = (192, 32, 58, 255)
PURPLE = (58, 10, 90, 255)
BG_DARK = (10, 2, 20, 255)
SS = 4  # supersample factor for anti-aliasing


def radial_bg(size):
    """Fondo degradado: morado en el centro -> casi negro en los bordes,
    con un leve halo rojo cerca del borde."""
    img = Image.new("RGBA", (size, size), BG_DARK)
    px = img.load()
    cx = cy = size / 2
    maxd = math.hypot(cx, cy)
    for y in range(size):
        for x in range(size):
            d = math.hypot(x - cx, y - cy) / maxd
            d = min(d, 1.0)
            # interpola morado -> negro
            r = int(PURPLE[0] * (1 - d) + BG_DARK[0] * d)
            g = int(PURPLE[1] * (1 - d) + BG_DARK[1] * d)
            b = int(PURPLE[2] * (1 - d) + BG_DARK[2] * d)
            # halo rojo sutil hacia el borde (anillo entre 0.55 y 0.9)
            ring = max(0.0, 1 - abs(d - 0.72) / 0.28)
            r = int(r * (1 - ring * 0.35) + RED_D[0] * ring * 0.35)
            g = int(g * (1 - ring * 0.35) + RED_D[1] * ring * 0.35)
            b = int(b * (1 - ring * 0.35) + RED_D[2] * ring * 0.35)
            px[x, y] = (r, g, b, 255)
    return img


def pentagram_points(cx, cy, radius, rotation=-90):
    pts = []
    for i in range(5):
        ang = math.radians(rotation + i * 72)
        pts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
    return pts


def draw_pentagram(draw, cx, cy, radius, width, color, glow_layer=None):
    pts = pentagram_points(cx, cy, radius)
    order = [0, 2, 4, 1, 3, 0]
    line = [pts[i] for i in order]
    draw.line(line, fill=color, width=width, joint="curve")
    for p in pts:
        r = width * 0.9
        draw.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)
    if glow_layer is not None:
        gdraw = ImageDraw.Draw(glow_layer)
        gdraw.line(line, fill=color, width=int(width * 2.2), joint="curve")


def make_icon(size, filename, safe_margin_ratio=0.0, circle_border=True):
    big = size * SS
    bg = radial_bg(big)

    cx = cy = big / 2
    content_r = big / 2 * (1 - safe_margin_ratio)

    # anillo dorado exterior
    if circle_border:
        ring = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring)
        rr = content_r * 0.92
        rd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=GOLD, width=int(big * 0.012))
        bg = Image.alpha_composite(bg, ring)

    # halo de brillo detras del pentaculo
    glow = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw_pentagram(ImageDraw.Draw(Image.new("RGBA", (big, big))), cx, cy, content_r * 0.62,
                    int(big * 0.028), GOLD_L, glow_layer=glow)
    glow = glow.filter(ImageFilter.GaussianBlur(big * 0.02))
    bg = Image.alpha_composite(bg, glow)

    # pentaculo nitido
    fg = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(fg)
    draw_pentagram(fdraw, cx, cy, content_r * 0.62, int(big * 0.028), GOLD_L)
    bg = Image.alpha_composite(bg, fg)

    out = bg.resize((size, size), Image.LANCZOS)
    out.save(os.path.join(OUT_DIR, filename))
    print("ok", filename, size)


# Icono estandar (Android/manifest/favicon) - fondo llega al borde
make_icon(512, "icon-512.png", safe_margin_ratio=0.06)
make_icon(192, "icon-192.png", safe_margin_ratio=0.06)

# Icono maskable (Android adaptive icon) - mas margen de seguridad, sin anillo
make_icon(512, "icon-512-maskable.png", safe_margin_ratio=0.20, circle_border=False)

# Apple touch icon (iOS aplica su propio redondeo, fondo debe llegar al borde)
make_icon(180, "apple-touch-icon.png", safe_margin_ratio=0.10)

# Favicon
make_icon(32, "favicon-32.png", safe_margin_ratio=0.08)

print("listo")
