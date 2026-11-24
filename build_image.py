"""Draw the 23 November 2026 front page (picture-led V2) and save entry.png.

Run:  python3 build_image.py
Writes entry.png (1024x1024) next to this file. PIL is used at build time only;
the entrypoint main.py is standard library only and just copies the picture.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 12
CW = W - 2 * MARGIN  # 1000

INK = (17, 17, 17)
RED = (178, 18, 28)
GREY = (102, 102, 102)
LINE = (205, 205, 205)
PAPER = (255, 255, 255)
NAVY = (31, 56, 100)
TEAL = (14, 116, 144)
GREEN = (21, 128, 61)
WINE = (157, 23, 77)
SLATE = (71, 85, 105)

DJ = "/usr/share/fonts/truetype/dejavu/"


def _font(name, size):
    try:
        return ImageFont.truetype(DJ + name, size)
    except OSError:
        return ImageFont.load_default()


F_TOP = _font("DejaVuSans-Bold.ttf", 14)
F_TOP_R = _font("DejaVuSans-Bold.ttf", 12)
F_MAST = _font("DejaVuSerif-Bold.ttf", 50)
F_SUB = _font("DejaVuSans.ttf", 15)
F_STRIP = _font("DejaVuSans-Bold.ttf", 12)
F_SLOT_T = _font("DejaVuSans-Bold.ttf", 10)
F_SLOT = _font("DejaVuSans.ttf", 10)
F_NUM = _font("DejaVuSerif-Bold.ttf", 21)
F_NUM_L = _font("DejaVuSans.ttf", 9)
F_TAB = _font("DejaVuSans-Bold.ttf", 11)
F_KICK_H = _font("DejaVuSans-Bold.ttf", 12)
F_HEAD_H = _font("DejaVuSerif-Bold.ttf", 20)
F_BODY_H = _font("DejaVuSans.ttf", 11)
F_KICK_W = _font("DejaVuSans-Bold.ttf", 12)
F_HEAD_W = _font("DejaVuSerif-Bold.ttf", 19)
F_BODY_W = _font("DejaVuSans.ttf", 12)
F_KICK_G = _font("DejaVuSans-Bold.ttf", 10)
F_HEAD_G = _font("DejaVuSerif-Bold.ttf", 14)
F_BODY_G = _font("DejaVuSans.ttf", 10)
F_TAG = _font("DejaVuSans-Bold.ttf", 10)
F_TAG_S = _font("DejaVuSans-Bold.ttf", 8)
F_LIST_H = _font("DejaVuSans-Bold.ttf", 12)
F_LIST = _font("DejaVuSans.ttf", 9)
F_DATE_H = _font("DejaVuSans-Bold.ttf", 11)
F_DATE = _font("DejaVuSans.ttf", 11)
F_FOOT = _font("DejaVuSans.ttf", 10)
F_PIN = _font("DejaVuSans-Bold.ttf", 9)
F_LEG = _font("DejaVuSans.ttf", 8)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(d, x, y, w, h, text, fnt, bg, fg, outline=None):
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg,
                        outline=outline, width=1 if outline else 0)
    tw = d.textlength(text, font=fnt)
    th = fnt.size
    d.text((x + (w - tw) / 2, y + (h - th) / 2 - 1), text, font=fnt, fill=fg)


def cert_colors(cert):
    if cert == "CONFIRMED":
        return RED, PAPER, None
    if cert == "REPORTED":
        return (110, 110, 110), PAPER, None
    return PAPER, RED, RED  # CLAIM


def _bands(d, x, y, w, h, colors):
    n = len(colors)
    for i, c in enumerate(colors):
        d.rectangle([x, y + i * h / n, x + w, y + (i + 1) * h / n], fill=c)


def draw_flag(d, x, y, w, h, kind):
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(40, 40, 40))
    if kind == "globe":
        d.ellipse([x + 1, y + 1, x + w - 2, y + h - 2], fill=(41, 98, 168))
        d.ellipse([x + 4, y + 3, x + 11, y + 9], fill=(46, 139, 87))
        d.ellipse([x + 14, y + 9, x + 24, y + 15], fill=(46, 139, 87))
        d.ellipse([x + 7, y + 12, x + 13, y + 16], fill=(46, 139, 87))
        return
    if kind == "poland":
        _bands(d, x, y, w, h, [PAPER, (220, 20, 40)])
    elif kind == "russia":
        _bands(d, x, y, w, h, [PAPER, (0, 70, 160), (220, 20, 40)])
    elif kind == "ukraine":
        _bands(d, x, y, w, h, [(0, 90, 180), (255, 210, 0)])
    elif kind == "indonesia":
        _bands(d, x, y, w, h, [(220, 20, 40), PAPER])
    elif kind == "iran":
        _bands(d, x, y, w, h, [(0, 140, 70), PAPER, (220, 20, 40)])
    elif kind == "libya":
        _bands(d, x, y, w, h, [(220, 20, 40), (20, 20, 20), (0, 140, 70)])
        d.ellipse([x + w * 0.44, y + h * 0.38, x + w * 0.56, y + h * 0.62],
                  fill=PAPER)
    elif kind == "india":
        _bands(d, x, y, w, h, [(255, 153, 51), PAPER, (0, 130, 60)])
        d.ellipse([x + w * 0.44, y + h * 0.30, x + w * 0.56, y + h * 0.70],
                  outline=(0, 40, 120), width=1)
        d.ellipse([x + w * 0.48, y + h * 0.44, x + w * 0.52, y + h * 0.56],
                  fill=(0, 40, 120))
    elif kind == "japan":
        d.rectangle([x, y, x + w, y + h], fill=PAPER)
        d.ellipse([x + w * 0.38, y + h * 0.22, x + w * 0.62, y + h * 0.78],
                  fill=(190, 0, 30))
    elif kind == "taiwan":
        d.rectangle([x, y, x + w, y + h], fill=(200, 0, 30))
        d.rectangle([x, y, x + w * 0.55, y + h * 0.52], fill=(0, 40, 120))
        d.ellipse([x + w * 0.16, y + h * 0.12, x + w * 0.38, y + h * 0.40],
                  fill=PAPER)
    elif kind == "korea":
        d.rectangle([x, y, x + w, y + h], fill=PAPER)
        d.pieslice([x + w * 0.36, y + h * 0.22, x + w * 0.64, y + h * 0.78],
                   180, 360, fill=(205, 40, 50))
        d.pieslice([x + w * 0.36, y + h * 0.22, x + w * 0.64, y + h * 0.78],
                   0, 180, fill=(0, 70, 160))
        d.rectangle([x + 2, y + 2, x + 7, y + 5], fill=INK)
        d.rectangle([x + w - 7, y + h - 5, x + w - 2, y + h - 2], fill=INK)
    elif kind == "usa":
        for i in range(7):
            c = (190, 0, 30) if i % 2 == 0 else PAPER
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7], fill=c)
        d.rectangle([x, y, x + w * 0.42, y + h * 0.57], fill=(0, 40, 100))
        for r in range(2):
            for c in range(3):
                d.ellipse([x + 2 + c * 4, y + 2 + r * 5,
                           x + 4 + c * 4, y + 4 + r * 5], fill=PAPER)
    elif kind == "uk":
        d.rectangle([x, y, x + w, y + h], fill=(0, 40, 110))
        d.line([x, y, x + w, y + h], fill=PAPER, width=4)
        d.line([x + w, y, x, y + h], fill=PAPER, width=4)
        d.rectangle([x + w * 0.44, y, x + w * 0.56, y + h], fill=PAPER)
        d.rectangle([x, y + h * 0.42, x + w, y + h * 0.58], fill=PAPER)
        d.rectangle([x + w * 0.47, y, x + w * 0.53, y + h], fill=(200, 0, 30))
        d.rectangle([x, y + h * 0.46, x + w, y + h * 0.54], fill=(200, 0, 30))


def _starburst(d, cx, cy, r, color):
    import math
    for a in range(0, 360, 30):
        x2 = cx + r * math.cos(math.radians(a))
        y2 = cy + r * math.sin(math.radians(a))
        d.line([cx, cy, x2, y2], fill=color, width=2)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=color)


def draw_picture(d, x, y, w, h, pid):
    if pid == 1:  # COP31, Antalya: hall, document, sun, sand
        d.rectangle([x, y, x + w, y + h], fill=(191, 227, 242))
        d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(233, 217, 166))
        d.ellipse([x + w * 0.68, y + h * 0.06, x + w * 0.80, y + h * 0.30],
                  fill=(240, 150, 40))
        d.rectangle([x + w * 0.06, y + h * 0.34, x + w * 0.46, y + h * 0.78],
                    fill=PAPER, outline=(120, 120, 120))
        d.rectangle([x + w * 0.04, y + h * 0.30, x + w * 0.48, y + h * 0.36],
                    fill=(230, 230, 230))
        for i in range(4):
            cx = x + w * (0.11 + i * 0.09)
            d.rectangle([cx, y + h * 0.40, cx + 5, y + h * 0.74],
                        fill=(90, 90, 90))
        d.rectangle([x + w * 0.56, y + h * 0.42, x + w * 0.92, y + h * 0.82],
                    fill=PAPER, outline=(120, 120, 120))
        for i in range(3):
            ly = y + h * (0.50 + i * 0.09)
            d.line([x + w * 0.60, ly, x + w * 0.88, ly], fill=(80, 80, 80),
                   width=2)
        d.line([x + w * 0.58, y + h * 0.80, x + w * 0.90, y + h * 0.46],
               fill=RED, width=4)
    elif pid == 2:  # Poland: map, starbursts, plane
        d.rectangle([x, y, x + w, y + h], fill=(22, 35, 61))
        poly = [(x + w * 0.30, y + h * 0.30), (x + w * 0.48, y + h * 0.22),
                (x + w * 0.68, y + h * 0.26), (x + w * 0.74, y + h * 0.44),
                (x + w * 0.62, y + h * 0.60), (x + w * 0.44, y + h * 0.66),
                (x + w * 0.30, y + h * 0.52), (x + w * 0.26, y + h * 0.40)]
        d.polygon(poly, fill=(242, 227, 179))
        _starburst(d, x + w * 0.44, y + h * 0.40, 12, (220, 30, 40))
        _starburst(d, x + w * 0.62, y + h * 0.52, 10, (220, 30, 40))
        _starburst(d, x + w * 0.36, y + h * 0.56, 9, (220, 30, 40))
        d.polygon([(x + w * 0.24, y + h * 0.14), (x + w * 0.34, y + h * 0.10),
                   (x + w * 0.36, y + h * 0.16), (x + w * 0.26, y + h * 0.18)],
                  fill=PAPER)
    elif pid == 3:  # Markets: falling chart
        d.rectangle([x, y, x + w, y + h], fill=(16, 20, 24))
        for i in range(1, 4):
            ly = y + i * h / 4
            d.line([x, ly, x + w, ly], fill=(42, 47, 54), width=1)
        pts = []
        for i, f in enumerate([0.18, 0.30, 0.26, 0.44, 0.40, 0.58, 0.70]):
            pts.append((x + w * (0.06 + i * 0.14), y + h * f))
        d.line(pts, fill=(230, 40, 50), width=3, joint="curve")
        d.polygon([(pts[-1][0], pts[-1][1]),
                   (pts[-1][0] - 14, pts[-1][1] - 4),
                   (pts[-1][0] - 14, pts[-1][1] + 10)], fill=(230, 40, 50))
        for cx, cy, col in [(0.20, 0.30, (40, 160, 80)),
                            (0.34, 0.44, (220, 40, 50)),
                            (0.48, 0.40, (40, 160, 80)),
                            (0.62, 0.58, (220, 40, 50)),
                            (0.76, 0.70, (220, 40, 50))]:
            bx, by = x + w * cx, y + h * cy
            d.rectangle([bx - 4, by - 8, bx + 4, by + 8], fill=col)
            d.line([bx, by - 13, bx, by + 13], fill=col, width=1)
    elif pid == 4:  # Libya: capsized warship at sea
        d.rectangle([x, y, x + w, y + h], fill=(11, 61, 102))
        for i in range(3):
            ly = y + h * (0.30 + i * 0.22)
            d.arc([x + 6, ly - 8, x + w - 6, ly + 8], 0, 180, fill=PAPER,
                  width=2)
        d.polygon([(x + w * 0.18, y + h * 0.62), (x + w * 0.62, y + h * 0.44),
                   (x + w * 0.72, y + h * 0.58), (x + w * 0.30, y + h * 0.76)],
                  fill=(40, 44, 50))
        d.rectangle([x + w * 0.34, y + h * 0.44, x + w * 0.44, y + h * 0.56],
                    fill=(70, 74, 80))
        _starburst(d, x + w * 0.78, y + h * 0.30, 14, (240, 140, 30))
        d.ellipse([x + w * 0.72, y + h * 0.20, x + w * 0.84, y + h * 0.34],
                  fill=(240, 170, 60))
    elif pid == 5:  # Rostov refinery at night, on fire
        d.rectangle([x, y, x + w, y + h], fill=(27, 27, 46))
        d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(15, 15, 25))
        for cx in (0.18, 0.38, 0.58):
            d.rectangle([x + w * cx, y + h * 0.42, x + w * (cx + 0.12),
                         y + h * 0.74], fill=(120, 120, 125))
            d.ellipse([x + w * cx, y + h * 0.38, x + w * (cx + 0.12),
                       y + h * 0.46], fill=(150, 150, 155))
        d.rectangle([x + w * 0.76, y + h * 0.30, x + w * 0.80, y + h * 0.74],
                    fill=(120, 120, 125))
        d.line([x + w * 0.76, y + h * 0.40, x + w * 0.80, y + h * 0.60],
               fill=(80, 80, 85), width=2)
        d.line([x + w * 0.80, y + h * 0.40, x + w * 0.76, y + h * 0.60],
               fill=(80, 80, 85), width=2)
        for cx, s in [(0.24, 16), (0.52, 20), (0.78, 14)]:
            fx, fy = x + w * cx, y + h * 0.62
            d.polygon([(fx - s, fy), (fx, fy - s * 1.4), (fx + s, fy)],
                      fill=(240, 120, 20))
            d.polygon([(fx - s * 0.5, fy), (fx, fy - s * 0.8),
                       (fx + s * 0.5, fy)], fill=(250, 200, 60))
        d.ellipse([x + w * 0.60, y + h * 0.12, x + w * 0.72, y + h * 0.30],
                  fill=(90, 90, 100))
    elif pid == 6:  # Dymer: damaged block, smoke, ambulance
        d.rectangle([x, y, x + w, y + h], fill=(201, 205, 211))
        d.polygon([(x + w * 0.12, y + h * 0.78), (x + w * 0.12, y + h * 0.30),
                   (x + w * 0.58, y + h * 0.30), (x + w * 0.58, y + h * 0.44),
                   (x + w * 0.46, y + h * 0.52), (x + w * 0.46, y + h * 0.78)],
                  fill=(110, 112, 118))
        for r in range(3):
            for c in range(3):
                wx = x + w * (0.18 + c * 0.13)
                wy = y + h * (0.38 + r * 0.12)
                d.rectangle([wx, wy, wx + 10, wy + 8], fill=(40, 42, 48))
        d.ellipse([x + w * 0.58, y + h * 0.10, x + w * 0.72, y + h * 0.28],
                  fill=(150, 150, 155))
        d.ellipse([x + w * 0.66, y + h * 0.04, x + w * 0.80, y + h * 0.20],
                  fill=(170, 170, 175))
        d.rectangle([x + w * 0.62, y + h * 0.72, x + w * 0.90, y + h * 0.86],
                    fill=PAPER, outline=(150, 150, 150))
        d.rectangle([x + w * 0.74, y + h * 0.74, x + w * 0.78, y + h * 0.84],
                    fill=RED)
        d.rectangle([x + w * 0.70, y + h * 0.77, x + w * 0.82, y + h * 0.81],
                    fill=RED)
    elif pid == 7:  # Hormuz: tanker, fire, mine
        d.rectangle([x, y, x + w, y + h * 0.28], fill=(242, 232, 201))
        d.rectangle([x, y + h * 0.28, x + w, y + h], fill=(14, 90, 110))
        d.rectangle([x + w * 0.08, y + h * 0.52, x + w * 0.86, y + h * 0.66],
                    fill=(25, 25, 30))
        d.rectangle([x + w * 0.08, y + h * 0.62, x + w * 0.86, y + h * 0.66],
                    fill=(150, 30, 30))
        d.rectangle([x + w * 0.62, y + h * 0.36, x + w * 0.74, y + h * 0.54],
                    fill=PAPER)
        d.rectangle([x + w * 0.30, y + h * 0.44, x + w * 0.36, y + h * 0.54],
                    fill=(200, 200, 200))
        d.polygon([(x + w * 0.42, y + h * 0.52), (x + w * 0.46, y + h * 0.34),
                   (x + w * 0.50, y + h * 0.52)], fill=(240, 120, 20))
        d.polygon([(x + w * 0.46, y + h * 0.52), (x + w * 0.50, y + h * 0.40),
                   (x + w * 0.54, y + h * 0.52)], fill=(250, 200, 60))
        import math
        mx, my = x + w * 0.16, y + h * 0.78
        d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(20, 20, 20))
        for a in range(0, 360, 45):
            d.line([mx, my, mx + 11 * math.cos(math.radians(a)),
                    my + 11 * math.sin(math.radians(a))], fill=(20, 20, 20),
                   width=2)
    elif pid == 8:  # Seattle airport: tower, plane, two figures
        d.rectangle([x, y, x + w, y + h], fill=(207, 227, 242))
        d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(90, 95, 100))
        d.rectangle([x + w * 0.12, y + h * 0.30, x + w * 0.20, y + h * 0.80],
                    fill=(120, 125, 130))
        d.rectangle([x + w * 0.09, y + h * 0.22, x + w * 0.23, y + h * 0.32],
                    fill=(70, 75, 80))
        d.polygon([(x + w * 0.52, y + h * 0.30), (x + w * 0.88, y + h * 0.26),
                   (x + w * 0.90, y + h * 0.34), (x + w * 0.54, y + h * 0.38)],
                  fill=(200, 205, 210))
        d.polygon([(x + w * 0.66, y + h * 0.22), (x + w * 0.72, y + h * 0.34),
                   (x + w * 0.64, y + h * 0.34)], fill=(180, 185, 190))
        for fx in (0.34, 0.46):
            cx = x + w * fx
            d.ellipse([cx - 4, y + h * 0.66, cx + 4, y + h * 0.74], fill=INK)
            d.polygon([(cx - 6, y + h * 0.98), (cx - 3, y + h * 0.74),
                       (cx + 3, y + h * 0.74), (cx + 6, y + h * 0.98)],
                      fill=INK)
    elif pid == 9:  # London: football pitch, ball, trophy
        d.rectangle([x, y, x + w, y + h], fill=(46, 139, 87))
        d.rectangle([x + 6, y + 6, x + w - 6, y + h - 6], outline=PAPER,
                    width=2)
        d.line([x + w / 2, y + 6, x + w / 2, y + h - 6], fill=PAPER, width=2)
        d.ellipse([x + w * 0.38, y + h * 0.28, x + w * 0.62, y + h * 0.72],
                  outline=PAPER, width=2)
        d.rectangle([x + w * 0.78, y + h * 0.28, x + w - 6, y + h * 0.72],
                    outline=PAPER, width=2)
        bx, by = x + w * 0.30, y + h * 0.60
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=PAPER,
                  outline=INK, width=1)
        d.polygon([(bx, by - 4), (bx + 4, by - 1), (bx + 2, by + 4),
                   (bx - 2, by + 4), (bx - 4, by - 1)], fill=INK)
        tx, ty = x + w * 0.84, y + h * 0.80
        d.polygon([(tx - 8, ty), (tx + 8, ty), (tx + 5, ty + 12),
                   (tx - 5, ty + 12)], fill=(220, 180, 60))
        d.arc([tx - 12, ty + 2, tx - 4, ty + 10], 90, 270, fill=(220, 180, 60),
              width=2)
        d.arc([tx + 4, ty + 2, tx + 12, ty + 10], -90, 90, fill=(220, 180, 60),
              width=2)
    elif pid == 10:  # Seoul: exam hall, phone with red ban
        d.rectangle([x, y, x + w, y + h], fill=(232, 226, 213))
        d.rectangle([x + w * 0.08, y + h * 0.58, x + w * 0.44, y + h * 0.72],
                    fill=(150, 110, 70))
        d.rectangle([x + w * 0.56, y + h * 0.58, x + w * 0.92, y + h * 0.72],
                    fill=(150, 110, 70))
        d.rectangle([x + w * 0.14, y + h * 0.50, x + w * 0.38, y + h * 0.60],
                    fill=PAPER)
        d.rectangle([x + w * 0.62, y + h * 0.50, x + w * 0.86, y + h * 0.60],
                    fill=PAPER)
        d.rectangle([x + w * 0.36, y + h * 0.14, x + w * 0.64, y + h * 0.52],
                    fill=(30, 30, 40), outline=(150, 150, 150))
        d.line([x + w * 0.40, y + h * 0.24, x + w * 0.60, y + h * 0.24],
               fill=(80, 160, 255), width=2)
        d.line([x + w * 0.40, y + h * 0.32, x + w * 0.52, y + h * 0.32],
               fill=(80, 160, 255), width=2)
        d.line([x + w * 0.40, y + h * 0.40, x + w * 0.56, y + h * 0.40],
               fill=(80, 160, 255), width=2)
        cx, cy, r = x + w * 0.50, y + h * 0.33, 26
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=4)
        d.line([cx - r * 0.7, cy + r * 0.7, cx + r * 0.7, cy - r * 0.7],
               fill=RED, width=4)
    elif pid == 11:  # Cikande: factory on fire
        d.rectangle([x, y, x + w, y + h], fill=(200, 205, 210))
        d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(90, 90, 95))
        d.polygon([(x + w * 0.10, y + h * 0.72), (x + w * 0.10, y + h * 0.42),
                   (x + w * 0.26, y + h * 0.30), (x + w * 0.42, y + h * 0.42),
                   (x + w * 0.58, y + h * 0.30), (x + w * 0.74, y + h * 0.42),
                   (x + w * 0.90, y + h * 0.30), (x + w * 0.90, y + h * 0.72)],
                  fill=(130, 130, 135))
        for i in range(4):
            wx = x + w * (0.16 + i * 0.18)
            d.rectangle([wx, y + h * 0.52, wx + 12, y + h * 0.64],
                        fill=(60, 60, 65))
        for cx, s in [(0.30, 18), (0.55, 22), (0.78, 16)]:
            fx, fy = x + w * cx, y + h * 0.34
            d.polygon([(fx - s, fy), (fx, fy - s * 1.5), (fx + s, fy)],
                      fill=(240, 120, 20))
            d.polygon([(fx - s * 0.5, fy), (fx, fy - s * 0.9),
                       (fx + s * 0.5, fy)], fill=(250, 200, 60))
        d.ellipse([x + w * 0.62, y + h * 0.04, x + w * 0.76, y + h * 0.20],
                  fill=(80, 80, 85))
    elif pid == 12:  # India cricket: pitch, stumps, bat, ball
        d.rectangle([x, y, x + w, y + h], fill=(58, 155, 79))
        d.rectangle([x + w * 0.40, y, x + w * 0.60, y + h], fill=(190, 160, 110))
        d.line([x + w * 0.40, y, x + w * 0.40, y + h], fill=PAPER, width=2)
        d.line([x + w * 0.60, y, x + w * 0.60, y + h], fill=PAPER, width=2)
        for sx in (0.44, 0.47, 0.50):
            d.rectangle([x + w * sx, y + h * 0.12, x + w * sx + 3,
                         y + h * 0.24], fill=(240, 220, 150))
        d.polygon([(x + w * 0.66, y + h * 0.55), (x + w * 0.72, y + h * 0.50),
                   (x + w * 0.78, y + h * 0.78), (x + w * 0.72, y + h * 0.82)],
                  fill=(210, 180, 130), outline=(120, 90, 50))
        bx, by = x + w * 0.30, y + h * 0.70
        d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(180, 20, 30))
        d.arc([bx - 7, by - 7, bx + 7, by + 7], 200, 340, fill=PAPER, width=1)
    elif pid == 13:  # Shuri Castle: tiered red roofs on a hill
        d.rectangle([x, y, x + w, y + h], fill=(191, 224, 242))
        d.ellipse([x + w * 0.80, y + h * 0.08, x + w * 0.92, y + h * 0.26],
                  fill=(245, 180, 60))
        d.polygon([(x, y + h), (x, y + h * 0.78), (x + w * 0.35, y + h * 0.62),
                   (x + w * 0.65, y + h * 0.62), (x + w, y + h * 0.78),
                   (x + w, y + h)], fill=(111, 160, 90))
        d.rectangle([x + w * 0.30, y + h * 0.62, x + w * 0.70, y + h * 0.78],
                    fill=(150, 150, 150))
        d.rectangle([x + w * 0.36, y + h * 0.46, x + w * 0.64, y + h * 0.64],
                    fill=(245, 245, 245))
        d.polygon([(x + w * 0.32, y + h * 0.48), (x + w * 0.68, y + h * 0.48),
                   (x + w * 0.62, y + h * 0.38), (x + w * 0.38, y + h * 0.38)],
                  fill=(178, 40, 35))
        d.rectangle([x + w * 0.41, y + h * 0.24, x + w * 0.59, y + h * 0.40],
                    fill=(245, 245, 245))
        d.polygon([(x + w * 0.38, y + h * 0.26), (x + w * 0.62, y + h * 0.26),
                   (x + w * 0.57, y + h * 0.16), (x + w * 0.43, y + h * 0.16)],
                  fill=(178, 40, 35))
        d.rectangle([x + w * 0.47, y + h * 0.06, x + w * 0.53, y + h * 0.18],
                    fill=(245, 245, 245))
        d.polygon([(x + w * 0.45, y + h * 0.08), (x + w * 0.55, y + h * 0.08),
                   (x + w * 0.52, y + h * 0.02), (x + w * 0.48, y + h * 0.02)],
                  fill=(178, 40, 35))


STORIES = [
    {"n": 1, "kicker": "1 ANTALYA \u00b7 CLIMATE", "tag": "COP31: NO DEAL",
     "cert": "CONFIRMED", "flag": "globe", "pic": 1,
     "head": "COP31 collapses with no fossil-fuel deal",
     "body": "Talks collapse on Sunday in Antalya: no consensus, and the "
             "Antalya Pact never mentions fossil fuels. (CNN, WSJ)"},
    {"n": 2, "kicker": "2 WARSAW \u00b7 SECURITY", "tag": "POLAND",
     "cert": "CONFIRMED", "flag": "poland", "pic": 2,
     "head": "Poland: the three objects were Russian missiles",
     "body": "Prosecutors confirm the three objects that fell on Friday were "
             "Russian Kh-101 cruise missiles. NATO meets Monday. (Reuters)"},
    {"n": 3, "kicker": "3 TAIPEI \u00b7 SEOUL \u00b7 MARKETS", "tag": "MARKETS",
     "cert": "CONFIRMED", "flag": "taiwan+korea", "pic": 3,
     "head": "Asia on alert after Friday's market rout",
     "body": "Taiwan bans short-selling from Monday after shares fell 17.5% "
             "in a week. Seoul eases buyback limits. (Reports)"},
    {"n": 4, "kicker": "4 BENGHAZI \u00b7 WAR", "tag": "LIBYA \u00b7 WAR",
     "cert": "REPORTED", "flag": "libya", "pic": 4,
     "head": "Russian warship sunk in Libyan port",
     "body": "Merkury capsized after sea drones hit Benghazi base Sunday, "
             "10 hurt. (Reuters)"},
    {"n": 5, "kicker": "5 ROSTOV \u00b7 ENERGY", "tag": "ROSTOV \u00b7 ENERGY",
     "cert": "REPORTED", "flag": "russia", "pic": 5,
     "head": "Drones hit Russian oil refinery overnight",
     "body": "Drones hit Novoshakhtinsk refinery early Monday; fire broke "
             "out. (Reports)"},
    {"n": 6, "kicker": "6 DYMER \u00b7 WAR", "tag": "KYIV \u00b7 WAR",
     "cert": "CONFIRMED", "flag": "ukraine", "pic": 6,
     "head": "Kyiv-region toll rises to at least 12",
     "body": "More dead found after Sunday's strike on a block in Dymer. "
             "(Reports)"},
    {"n": 7, "kicker": "7 STRAIT OF HORMUZ \u00b7 SHIPPING",
     "tag": "HORMUZ \u00b7 SHIPPING", "cert": "REPORTED", "flag": "iran",
     "pic": 7,
     "head": "More tankers hit as Hormuz attacks mount",
     "body": "Two more tankers caught fire Sunday after hitting mines, Iran "
             "says. (AP)"},
    {"n": 8, "kicker": "8 SEATTLE \u00b7 IMMIGRATION", "tag": "SEATTLE \u00b7 AMERICAS",
     "cert": "REPORTED", "flag": "usa", "pic": 8,
     "head": "Father and daughter held by ICE at airport",
     "body": "Pair bound for a family baptism when held at Seattle airport. "
             "(The Hindu)"},
    {"n": 9, "kicker": "9 LONDON \u00b7 SPORT", "tag": "FOOTBALL",
     "cert": "REPORTED", "flag": "uk", "pic": 9,
     "head": "UK to host the 2035 Women's World Cup",
     "body": "FIFA to name UK as hosts of the 2035 Women's World Cup on "
             "Monday. (Reports)"},
    {"n": 10, "kicker": "10 SEOUL \u00b7 POLITICS", "tag": "SEOUL \u00b7 POLITICS",
     "cert": "REPORTED", "flag": "korea", "pic": 10,
     "head": "Minister quits over AI exam-cheating scandal",
     "body": "Seoul's education minister quits over AI cheating in the "
             "exams. (Reports)"},
    {"n": 11, "kicker": "11 CIKANDE \u00b7 DISASTER", "tag": "BANTEN \u00b7 DISASTER",
     "cert": "CONFIRMED", "flag": "indonesia", "pic": 11,
     "head": "24 body bags after factory fire",
     "body": "24 body bags found after Sunday's fire; search resumes Monday. "
             "(Reports)"},
    {"n": 12, "kicker": "12 INDIA \u00b7 CRICKET", "tag": "CRICKET",
     "cert": "CONFIRMED", "flag": "india", "pic": 12,
     "head": "India push for victory on Day 5 in NZ Test",
     "body": "NZ are 157 for 4 at lunch on Day 5 as India press for the win. "
             "(Reports)"},
    {"n": 13, "kicker": "13 OKINAWA \u00b7 CULTURE", "tag": "OKINAWA \u00b7 CULTURE",
     "cert": "CONFIRMED", "flag": "japan", "pic": 13,
     "head": "Shuri Castle's great hall opens again",
     "body": "Restored main hall opens Monday, seven years after the 2019 "
             "fire. (Reports)"},
]

ALSO = [
    (14, "UK to build Ukrainian drones in a new deal"),
    (15, "Lahore most polluted city again (Sun)"),
    (16, "Settlers torch 12 vehicles near Ramallah"),
    (17, "Sudan strikes hit Khartoum, UN site hit (Sun)"),
    (18, "Houthis claim Saudi refinery strike (CLAIM)"),
    (19, "Hegseth memo curbs US-Canada defence ties"),
    (20, "Democrats flip N. Carolina seat in House"),
    (21, "Trump reports 'TrumpCare' health pitch"),
    (22, "Oracle says its AI funding is secured (Sun)"),
    (23, "Taiwan export orders rise for a 21st month"),
    (24, "FIDE title Game 1: Sindarov gets White"),
    (25, "Marquez wins 8th MotoGP title (Sun)"),
    (26, "Liverpool beat 10-man Man Utd (Sun)"),
    (27, "Thitikul wins third straight LPGA title (Sun)"),
    (28, "Alcaraz wins first ATP Finals title (Sun)"),
    (29, "BepiColombo enters orbit around Mercury (Sat)"),
    (30, "Brent $92.58; WTI $83.56 (Fri close)"),
    (31, "Bitcoin $58,970, down 5.2% (Sat)"),
    (32, "UK, France, China block UN top-job bid"),
    (33, "Trump: working with Schumer 'difficult'"),
    (34, "US hawks urge Iran strike; Trump: no rush"),
    (35, "Youth Congress protests Meta in India"),
    (36, "Price wins Grand Slam darts (Sun)"),
]

REGIONS = [("Europe 9", NAVY), ("Asia-Pacific 9", RED), ("Middle East 3", TEAL),
           ("Africa 2", GREEN), ("Americas 7", WINE), ("Global 6", SLATE)]

UTC_SLOTS = [
    ("02:22", "Refinery hit, Rostov"),
    ("MORNING", "Taiwan bans short sales"),
    ("MORNING", "Asian markets on alert"),
    ("MIDDAY", "NATO Council meets"),
    ("AFTERNOON", "FIFA confirms UK 2035"),
    ("EVENING", "Search resumes, Cikande"),
    ("NIGHT", "India press on, Day 5"),
]

NUMBERS = [
    ("3", "missiles in Poland"),
    ("17.5%", "Taiwan weekly fall"),
    ("12", "dead, Kyiv region"),
    ("24", "body bags, Cikande"),
    ("35%", "COP31 power goal"),
    ("538", "Lahore air index"),
]

DATE_CHECK = ("Left out as not Monday's news: the '400 drones, 110 missiles' "
              "attack on Ukraine (Fri 20\u2013Sat 21 Nov); Sparta and Kryvyi "
              "Rih strikes (Sat); 'Chapo Isidro' captured Fri 20 Nov; the "
              "killer-robot deal (Sat 21 Nov); the Shenzhen summit, "
              "Anthropic IPO and GTA VI launch (19 Nov); COP31 drafts "
              "before Sunday.")

FOOTER = ("Sunday events are dated as Sunday in their cards. Claims are "
          "labelled as claims. Sources named beside each story \u00b7 "
          "original drawings")

MAP_PINS = [(1, 0.56, 0.33), (2, 0.53, 0.15), (3, 0.90, 0.35),
            (4, 0.52, 0.44), (5, 0.585, 0.23), (6, 0.50, 0.28),
            (7, 0.63, 0.40), (8, 0.10, 0.22), (9, 0.44, 0.13),
            (10, 0.86, 0.22), (11, 0.815, 0.58), (12, 0.685, 0.44),
            (13, 0.94, 0.48)]


def draw_flag_chip(d, x, y, kind, fw=30, fh=20):
    if kind == "taiwan+korea":
        draw_flag(d, x, y, 28, 18, "taiwan")
        draw_flag(d, x + 30, y, 28, 18, "korea")
        return 58
    draw_flag(d, x, y, fw, fh, kind)
    return fw


def draw_cert_chip(d, x, y, cert, fnt, h=17):
    bg, fg, ol = cert_colors(cert)
    w = d.textlength(cert, font=fnt) + 14
    chip(d, x, y, w, h, cert, fnt, bg, fg, ol)
    return w


def draw_tag_chip(d, x, y, tag, fnt, h=17):
    w = d.textlength(tag, font=fnt) + 14
    chip(d, x, y, w, h, tag, fnt, INK, PAPER)
    return w


def hero_card(d, x, y, w, pic_h, s):
    draw_picture(d, x, y, w, pic_h, s["pic"])
    draw_flag_chip(d, x + 8, y + 8, s["flag"])
    cw = d.textlength(s["cert"], font=F_TAG) + 14
    draw_cert_chip(d, x + w - 8 - cw, y + 8, s["cert"], F_TAG)
    draw_tag_chip(d, x + 8, y + pic_h - 25, s["tag"], F_TAG)
    d.text((x, y + pic_h + 6), s["kicker"], font=F_KICK_H, fill=RED)
    yy = y + pic_h + 22
    lines = wrap(d, s["head"], F_HEAD_H, w)
    yy = draw_lines(d, x, yy, lines[:2], F_HEAD_H, INK, 22)
    blines = wrap(d, s["body"], F_BODY_H, w)
    draw_lines(d, x, yy + 2, blines[:2], F_BODY_H, INK, 14)


def wide_card(d, x, y, w, pic_h, s):
    draw_picture(d, x, y, w, pic_h, s["pic"])
    draw_flag_chip(d, x + 8, y + 8, s["flag"])
    cw = d.textlength(s["cert"], font=F_TAG) + 14
    draw_cert_chip(d, x + w - 8 - cw, y + 8, s["cert"], F_TAG)
    draw_tag_chip(d, x + 8, y + pic_h - 25, s["tag"], F_TAG)
    d.text((x, y + pic_h + 6), s["kicker"], font=F_KICK_W, fill=RED)
    yy = y + pic_h + 22
    d.text((x, yy), s["head"], font=F_HEAD_W, fill=INK)
    d.text((x, yy + 22), s["body"], font=F_BODY_W, fill=INK)


def grid_card(d, x, y, w, pic_h, s):
    draw_picture(d, x, y, w, pic_h, s["pic"])
    draw_flag_chip(d, x + 6, y + 6, s["flag"], fw=26, fh=17)
    cw = d.textlength(s["cert"], font=F_TAG_S) + 10
    draw_cert_chip(d, x + w - 6 - cw, y + 6, s["cert"], F_TAG_S, h=14)
    draw_tag_chip(d, x + 6, y + pic_h - 20, s["tag"], F_TAG_S, h=14)
    d.text((x, y + pic_h + 5), s["kicker"], font=F_KICK_G, fill=RED)
    yy = y + pic_h + 17
    lines = wrap(d, s["head"], F_HEAD_G, w)
    yy = draw_lines(d, x, yy, lines[:2], F_HEAD_G, INK, 15)
    blines = wrap(d, s["body"], F_BODY_G, w)
    draw_lines(d, x, yy + 1, blines[:3], F_BODY_G, INK, 12)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(234, 242, 248))
    land = (229, 217, 184)
    conts = [
        [(0.06, 0.18), (0.16, 0.10), (0.30, 0.12), (0.32, 0.22),
         (0.24, 0.30), (0.26, 0.42), (0.16, 0.44), (0.10, 0.32)],
        [(0.24, 0.48), (0.30, 0.46), (0.34, 0.56), (0.30, 0.72),
         (0.25, 0.66)],
        [(0.46, 0.14), (0.52, 0.10), (0.57, 0.16), (0.55, 0.26),
         (0.48, 0.26), (0.45, 0.20)],
        [(0.47, 0.36), (0.55, 0.34), (0.59, 0.44), (0.56, 0.60),
         (0.51, 0.66), (0.47, 0.52)],
        [(0.57, 0.12), (0.70, 0.08), (0.88, 0.12), (0.94, 0.24),
         (0.88, 0.38), (0.78, 0.44), (0.66, 0.40), (0.58, 0.28)],
        [(0.82, 0.62), (0.90, 0.60), (0.93, 0.66), (0.88, 0.72),
         (0.83, 0.68)],
    ]
    for poly in conts:
        d.polygon([(x + fx * w, y + fy * h) for fx, fy in poly], fill=land)
    for n, fx, fy in MAP_PINS:
        cx, cy = x + fx * w, y + fy * h
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=PAPER, width=1)
        t = str(n)
        tw = d.textlength(t, font=F_PIN)
        d.text((cx - tw / 2, cy - 5), t, font=F_PIN, fill=PAPER)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 8
    # Top line
    d.text((MARGIN, y), "THE WORLD IN ONE DAY", font=F_TOP, fill=RED)
    right = "36 STORIES \u00b7 6 REGIONS \u00b7 MONDAY 23 NOVEMBER 2026"
    d.text((W - MARGIN - d.textlength(right, font=F_TOP_R), y + 1), right,
           font=F_TOP_R, fill=INK)
    y += 20
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 6
    # Masthead
    mast = "Monday 23 November 2026"
    d.text(((W - d.textlength(mast, font=F_MAST)) / 2, y), mast, font=F_MAST,
           fill=INK)
    y += 54
    sub = ("COP31 collapses \u00b7 NATO meets on Poland \u00b7 Asia's markets "
           "on alert after Friday's rout")
    d.text(((W - d.textlength(sub, font=F_SUB)) / 2, y), sub, font=F_SUB,
           fill=INK)
    y += 18
    # UTC strip
    y0 = y
    d.rectangle([MARGIN, y0, MARGIN + 130, y0 + 38], fill=RED)
    d.text((MARGIN + 10, y0 + 4), "THE DAY", font=F_STRIP, fill=PAPER)
    d.text((MARGIN + 10, y0 + 20), "IN UTC", font=F_STRIP, fill=PAPER)
    slot_w = (CW - 130) / 7
    for i, (t, txt) in enumerate(UTC_SLOTS):
        sx = MARGIN + 130 + i * slot_w
        if i:
            d.line([sx - 2, y0 + 4, sx - 2, y0 + 34], fill=LINE, width=1)
        d.text((sx + 6, y0 + 3), t, font=F_SLOT_T, fill=RED)
        lines = wrap(d, txt, F_SLOT, slot_w - 12)
        draw_lines(d, sx + 6, y0 + 16, lines[:2], F_SLOT, INK, 11)
    y = y0 + 40
    # Numbers strip (small)
    y0 = y
    d.rectangle([MARGIN, y0, MARGIN + 130, y0 + 32], fill=RED)
    d.text((MARGIN + 10, y0 + 2), "THE DAY", font=F_STRIP, fill=PAPER)
    d.text((MARGIN + 10, y0 + 16), "IN NUMBERS", font=F_STRIP, fill=PAPER)
    num_w = (CW - 130) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        nx = MARGIN + 130 + i * num_w
        d.text((nx + 8, y0 + 1), num, font=F_NUM, fill=INK)
        d.text((nx + 8, y0 + 22), lab, font=F_NUM_L, fill=RED)
    y = y0 + 34
    # Region tabs
    y0 = y
    tab_w = CW / 6
    for i, (label, col) in enumerate(REGIONS):
        tx = MARGIN + i * tab_w
        d.rectangle([tx, y0, tx + tab_w - 4, y0 + 20], fill=col)
        tw = d.textlength(label, font=F_TAB)
        d.text((tx + (tab_w - 4 - tw) / 2, y0 + 3), label, font=F_TAB,
               fill=PAPER)
    y = y0 + 22
    # Heroes 1-2 side by side
    hero_w = (CW - 8) // 2
    hero_pic = 106
    hero_card(d, MARGIN, y, hero_w, hero_pic, STORIES[0])
    hero_card(d, MARGIN + hero_w + 8, y, hero_w, hero_pic, STORIES[1])
    y += 196
    # Story 3 wide row
    wide_card(d, MARGIN, y, CW, 66, STORIES[2])
    y += 112
    # Grid 4-13: 2 rows of 5
    gw = (CW - 4 * 8) // 5
    row_h = 160
    for r in range(2):
        for c in range(5):
            s = STORIES[3 + r * 5 + c]
            grid_card(d, MARGIN + c * (gw + 8), y + r * row_h, gw, 76, s)
    y += 2 * row_h
    # Map + also-on list
    y0 = y + 4
    map_w = 300
    d.text((MARGIN, y0), "WHERE IT HAPPENED", font=F_LIST_H, fill=RED)
    draw_map(d, MARGIN, y0 + 16, map_w, 94)
    d.text((MARGIN, y0 + 112),
           "Tags: OFFICIAL black \u00b7 CONFIRMED red \u00b7 REPORTED grey "
           "\u00b7 CLAIM outline", font=F_LEG, fill=GREY)
    lx = MARGIN + map_w + 12
    lw = W - MARGIN - lx
    d.text((lx, y0), "ALSO ON MONDAY 23 NOVEMBER \u2014 23 MORE STORIES",
           font=F_LIST_H, fill=RED)
    col_w = lw / 3
    for ci in range(3):
        chunk = ALSO[ci * 8:(ci + 1) * 8]
        cy = y0 + 18
        for n, txt in chunk:
            d.text((lx + ci * col_w, cy), str(n), font=F_LIST, fill=RED)
            lines = wrap(d, txt, F_LIST, col_w - 26)
            draw_lines(d, lx + ci * col_w + 22, cy, lines[:2], F_LIST, INK,
                       11)
            cy += 11 * max(1, len(lines[:2]))
    y = y0 + 140
    # DATE CHECK box
    d.rectangle([MARGIN, y, W - MARGIN, y + 30], fill=RED)
    head = "DATE CHECK  "
    hw = d.textlength(head, font=F_DATE_H)
    d.text((MARGIN + 8, y + 3), head, font=F_DATE_H, fill=PAPER)
    lines = wrap(d, DATE_CHECK, F_DATE, CW - hw - 24)
    draw_lines(d, MARGIN + 8 + hw, y + 3, lines[:2], F_DATE, PAPER, 12)
    y += 32
    # Footer
    d.text(((W - d.textlength(FOOTER, font=F_FOOT)) / 2, y), FOOTER,
           font=F_FOOT, fill=GREY)
    y += 10
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG")
    print("wrote %s (%d bytes), final y=%d" % (out, os.path.getsize(out), y))


if __name__ == "__main__":
    main()
