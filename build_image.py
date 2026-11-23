#!/usr/bin/env python3
"""Build entry.png for news-image-20261123 (Monday 23 November 2026).

Draws a one-page newspaper front page with Pillow. This script runs only
on the builder's machine; the graded entry point is main.py, which is
standard-library only and copies the finished entry.png to the output dir.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (200, 16, 46)
DARKRED = (139, 26, 26)
NAVY = (31, 56, 100)
TEAL = (14, 124, 123)
GREEN = (46, 125, 50)
GREY = (85, 85, 85)
LIGHTGREY = (238, 238, 236)
MIDGREY = (200, 200, 200)
CREAM = (250, 246, 236)
SKY = (183, 214, 232)
SEA = (52, 120, 178)
SAND = (226, 205, 158)
PALE = (245, 245, 240)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def chip(draw, x, y, text, fnt, bg, fg, pad_x=5, pad_y=2, outline=None):
    w = int(draw.textlength(text, font=fnt)) + pad_x * 2
    h = fnt.size + pad_y * 2
    if outline is not None:
        draw.rectangle([x, y, x + w, y + h], outline=outline, width=1)
        draw.text((x + pad_x, y + pad_y), text, font=fnt, fill=fg)
    else:
        draw.rectangle([x, y, x + w, y + h], fill=bg)
        draw.text((x + pad_x, y + pad_y), text, font=fnt, fill=fg)
    return w, h


def certainty_chip(draw, x, y, tag):
    fnt = font(SANS_B, 9)
    if tag == "OFFICIAL":
        return chip(draw, x, y, "OFFICIAL", fnt, BLACK, WHITE)
    if tag == "CONFIRMED":
        return chip(draw, x, y, "CONFIRMED", fnt, RED, WHITE)
    if tag == "CLAIM":
        return chip(draw, x, y, "CLAIM", fnt, WHITE, RED, outline=RED)
    return chip(draw, x, y, "REPORTED", fnt, GREY, WHITE)


def chip_width(draw, tag):
    fnt = font(SANS_B, 9)
    return int(draw.textlength(tag, font=fnt)) + 10


def num_circle(draw, cx, cy, n, r=10):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    size = 9 if r <= 8 else 11
    fnt = font(SANS_B, size)
    t = str(n)
    tw = draw.textlength(t, font=fnt)
    draw.text((cx - tw / 2, cy - size / 2 - 1), t, font=fnt, fill=WHITE)


# ---------------------------------------------------------------- pictures

def pic_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=SEA)
    d.polygon([(x, y + h), (x + w * 0.45, y + h * 0.55),
               (x + w * 0.75, y + h * 0.62), (x + w, y + h * 0.7),
               (x + w, y + h)], fill=SAND)
    d.ellipse([x + w - 52, y + 8, x + w - 12, y + 48], fill=(240, 180, 60))
    # conference hall
    d.rectangle([x + 18, y + h - 58, x + 118, y + h - 12], fill=WHITE)
    d.rectangle([x + 18, y + h - 66, x + 118, y + h - 58], fill=NAVY)
    for i in range(4):
        d.rectangle([x + 28 + i * 24, y + h - 50, x + 40 + i * 24, y + h - 20],
                    fill=NAVY)
    # broken pact paper
    d.polygon([(x + 150, y + 30), (x + 250, y + 22), (x + 262, y + 78),
               (x + 158, y + 86)], fill=WHITE)
    d.line([x + 205, y + 26, x + 198, y + 82], fill=RED, width=4)
    d.line([x + 162, y + 40, x + 246, y + 36], fill=BLACK, width=2)
    d.line([x + 164, y + 52, x + 244, y + 48], fill=BLACK, width=2)
    d.line([x + 166, y + 64, x + 230, y + 60], fill=BLACK, width=2)


def pic_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
    # rough Poland shape
    d.polygon([(x + 40, y + 30), (x + 150, y + 18), (x + 260, y + 34),
               (x + 300, y + 62), (x + 270, y + 96), (x + 170, y + 108),
               (x + 70, y + 96), (x + 30, y + 62)], fill=(232, 222, 170))
    for px, py in ((250, 78), (272, 88), (292, 70)):
        ax, ay = x + px, y + py
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([ax, ay, ax + 12 * math.cos(a), ay + 12 * math.sin(a)],
                   fill=RED, width=3)
        d.ellipse([ax - 4, ay - 4, ax + 4, ay + 4], fill=RED)
    # NATO compass star
    cx, cy = x + 52, y + 92
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(0, 90, 160))
    d.polygon([(cx, cy - 14), (cx + 4, cy), (cx, cy + 14), (cx - 4, cy)],
              fill=WHITE)
    d.polygon([(cx - 14, cy), (cx, cy - 4), (cx + 14, cy), (cx, cy + 4)],
              fill=WHITE)


def pic_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 16, 16))
    for gy in range(1, 4):
        yy = y + h * gy / 4
        d.line([x + 8, yy, x + w - 8, yy], fill=(60, 60, 60), width=1)
    pts = [(x + 16, y + 22), (x + 70, y + 34), (x + 120, y + 30),
           (x + 170, y + 52), (x + 220, y + 48), (x + 262, y + 78),
           (x + 300, y + 96)]
    d.line(pts, fill=RED, width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    d.polygon([(x + 268, y + 78), (x + 300, y + 78), (x + 284, y + 108)],
              fill=RED)


def pic_libya(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 60, 110))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(18, 40, 80))
    d.rectangle([x + 30, y + 34, x + 150, y + 52], fill=(90, 90, 90))
    d.rectangle([x + 60, y + 18, x + 78, y + 34], fill=(70, 70, 70))
    d.rectangle([x + 110, y + 24, x + 122, y + 34], fill=(70, 70, 70))
    d.polygon([(x + 150, y + 30), (x + 168, y + 22), (x + 168, y + 40)],
              fill=(255, 120, 40))
    d.ellipse([x + 158, y + 8, x + 182, y + 28], fill=(255, 160, 40))
    d.ellipse([x + 60, y + 4, x + 92, y + 26], fill=(120, 120, 120))
    d.line([x + 8, y + h - 8, x + w - 8, y + h - 8], fill=(120, 160, 210),
           width=2)


def pic_refinery(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(64, 32, 24))
    d.rectangle([x, y + h * 0.6, x + w, y + h], fill=(30, 20, 16))
    for bx, bw in ((18, 26), (52, 20), (80, 30), (118, 22), (150, 26)):
        d.rectangle([x + bx, y + 22, x + bx + bw, y + h - 6], fill=(20, 20, 20))
    d.polygon([(x + 150, y + 12), (x + 162, y + 26), (x + 150, y + 30),
               (x + 172, y + 34), (x + 158, y + 44), (x + 176, y + 48),
               (x + 160, y + 58)], fill=(255, 140, 30))
    d.ellipse([x + 120, y + 8, x + 150, y + 30], fill=(255, 190, 60))


def pic_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 32, 48))
    d.rectangle([x + 26, y + 16, x + 96, y + h - 6], fill=(120, 118, 110))
    d.rectangle([x + 110, y + 26, x + 168, y + h - 6], fill=(100, 98, 92))
    for wx in (34, 52, 70):
        for wy in (22, 36, 50):
            d.rectangle([x + wx, y + wy, x + wx + 12, y + wy + 10],
                        fill=(255, 210, 90))
    d.polygon([(x + 96, y + 16), (x + 110, y + 26), (x + 110, y + 60),
               (x + 96, y + 52)], fill=(40, 40, 40))
    d.polygon([(x + 140, y + 26), (x + 152, y + 12), (x + 162, y + 26)],
              fill=(255, 120, 30))
    d.rectangle([x + 12, y + h - 10, x + w - 12, y + h - 6], fill=(70, 70, 70))


def pic_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.polygon([(x, y), (x + 60, y), (x + 30, y + h), (x, y + h)], fill=SAND)
    d.polygon([(x + w, y + h * 0.4), (x + w, y), (x + w - 50, y),
               (x + w - 20, y + h * 0.4)], fill=SAND)
    d.rectangle([x + 70, y + 26, x + 150, y + 44], fill=(40, 40, 40))
    d.rectangle([x + 96, y + 12, x + 110, y + 26], fill=(30, 30, 30))
    for px, py in ((160, 22), (176, 34)):
        ax, ay = x + px, y + py
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([ax, ay, ax + 9 * math.cos(a), ay + 9 * math.sin(a)],
                   fill=(255, 90, 30), width=2)
    for mx, my in ((80, 52), (130, 54), (105, 56)):
        d.ellipse([x + mx - 3, y + my - 3, x + mx + 3, y + my + 3],
                  fill=BLACK)
        d.line([x + mx - 5, y + my - 5, x + mx + 5, y + my + 5], fill=BLACK,
               width=1)


def pic_seattle(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(110, 110, 110))
    d.rectangle([x + 20, y + 22, x + 130, y + h - 8], fill=(200, 200, 198))
    d.rectangle([x + 20, y + 16, x + 130, y + 22], fill=NAVY)
    for wx in (28, 52, 76, 100):
        d.rectangle([x + wx, y + 30, x + wx + 16, y + 44], fill=NAVY)
    d.polygon([(x + 138, y + 30), (x + 188, y + 24), (x + 188, y + 32),
               (x + 138, y + 38)], fill=WHITE)
    d.polygon([(x + 176, y + 24), (x + 188, y + 12), (x + 188, y + 24)],
              fill=WHITE)
    d.line([x + 8, y + h - 14, x + w - 8, y + h - 14], fill=RED, width=3)


def pic_fifa(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(34, 139, 64))
    d.rectangle([x, y + 8, x + w, y + h - 8], outline=WHITE, width=2)
    d.line([x + w / 2, y + 8, x + w / 2, y + h - 8], fill=WHITE, width=2)
    d.ellipse([x + w / 2 - 14, y + h / 2 - 14, x + w / 2 + 14, y + h / 2 + 14],
              outline=WHITE, width=2)
    d.ellipse([x + 22, y + h - 34, x + 48, y + h - 8], fill=WHITE)
    d.polygon([(x + 35, y + h - 34), (x + 30, y + h - 22),
               (x + 40, y + h - 22)], fill=BLACK)
    d.rectangle([x + w - 52, y + 10, x + w - 20, y + 30], fill=(212, 175, 55))
    d.rectangle([x + w - 46, y + 4, x + w - 26, y + 10], fill=(212, 175, 55))


def pic_seoul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 205, 230))
    d.rectangle([x + 24, y + 26, x + 150, y + h - 6], fill=(225, 225, 220))
    d.rectangle([x + 24, y + 20, x + 150, y + 26], fill=(120, 30, 30))
    for cx in (36, 62, 88, 114):
        d.rectangle([x + cx, y + 32, x + cx + 12, y + h - 6], fill=(90, 90, 90))
    d.rectangle([x + 158, y + 12, x + 186, y + 34], fill=(30, 30, 30))
    d.text((x + 162, y + 17), "AI", font=font(SANS_B, 11), fill=WHITE)
    d.line([x + 158, y + 34, x + 172, y + 48], fill=RED, width=3)
    d.line([x + 186, y + 34, x + 172, y + 48], fill=RED, width=3)


def pic_cikande(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 90, 95))
    d.rectangle([x + 16, y + 30, x + 120, y + h - 6], fill=(150, 148, 140))
    d.rectangle([x + 128, y + 10, x + 142, y + h - 6], fill=(110, 108, 100))
    d.ellipse([x + 124, y + 2, x + 160, y + 22], fill=(160, 160, 160))
    d.polygon([(x + 40, y + 30), (x + 56, y + 12), (x + 66, y + 30)],
              fill=(255, 130, 30))
    d.polygon([(x + 80, y + 30), (x + 92, y + 16), (x + 102, y + 30)],
              fill=(255, 170, 40))
    d.rectangle([x + 16, y + 44, x + 120, y + 50], fill=(70, 70, 70))


def pic_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 125, 50))
    d.rectangle([x + 14, y + h * 0.35, x + w - 14, y + h * 0.72],
                fill=(205, 178, 120))
    for sx in (30, 38, 46):
        d.rectangle([x + sx, y + 12, x + sx + 3, y + 26], fill=(245, 230, 180))
    d.rectangle([x + 28, y + 10, x + 52, y + 13], fill=(160, 110, 50))
    d.line([x + 90, y + 40, x + 150, y + 26], fill=(120, 70, 30), width=5)
    d.ellipse([x + 160, y + 18, x + 172, y + 30], fill=RED)


def pic_shuri(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 195, 225))
    d.ellipse([x + w - 46, y + 8, x + w - 14, y + 40], fill=(245, 200, 80))
    d.rectangle([x + 30, y + 30, x + 150, y + h - 6], fill=(178, 34, 34))
    d.polygon([(x + 22, y + 30), (x + 90, y + 8), (x + 158, y + 30)],
              fill=(120, 20, 20))
    for wx in (44, 76, 108, 132):
        d.rectangle([x + wx, y + 40, x + wx + 12, y + 56], fill=(255, 220, 180))
    d.rectangle([x + 78, y + h - 26, x + 102, y + h - 6], fill=(90, 30, 30))
    d.rectangle([x + 10, y + h - 8, x + w - 10, y + h - 4], fill=(90, 130, 70))


# ---------------------------------------------------------------- layout

HEROES = [
    dict(n=1, pic=pic_cop31, tag="COP31: NO DEAL", tag_bg=RED,
         cert="CONFIRMED", kicker="1 ANTALYA · CLIMATE",
         head="COP31 collapses with no fossil-fuel deal",
         body="Talks collapse on Sunday in Antalya: no consensus, and the "
              "'Antalya Pact' never mentions fossil fuels. (CNN, WSJ)"),
    dict(n=2, pic=pic_poland, tag="POLAND", tag_bg=NAVY, cert="CONFIRMED",
         kicker="2 WARSAW · SECURITY",
         head="Poland: the three objects were Russian missiles",
         body="Prosecutors confirm the three objects that fell on Friday "
              "were Russian Kh-101 cruise missiles. NATO meets Monday. "
              "(Reuters)"),
    dict(n=3, pic=pic_markets, tag="MARKETS", tag_bg=BLACK, cert="CONFIRMED",
         kicker="3 TAIPEI · SEOUL · MARKETS",
         head="Asia on alert after Friday's market rout",
         body="Taiwan bans short-selling from Monday after shares fell "
              "17.5% in a week. Seoul eases buyback limits. (Reports)"),
]

SECONDARY = [
    dict(n=4, pic=pic_libya, tag="LIBYA · WAR", tag_bg=NAVY, cert="REPORTED",
         kicker="4 BENGHAZI · WAR",
         head="Russian warship sunk in Libyan port",
         body="Merkury capsized after sea drones hit Benghazi base "
              "Sunday. 10 hurt. (Reuters)"),
    dict(n=5, pic=pic_refinery, tag="ROSTOV · ENERGY", tag_bg=DARKRED,
         cert="REPORTED", kicker="5 ROSTOV · ENERGY",
         head="Drones hit Russian oil refinery overnight",
         body="Drones hit Novoshakhtinsk refinery early Monday; fire "
              "broke out. (Reports)"),
    dict(n=6, pic=pic_kyiv, tag="KYIV · WAR", tag_bg=NAVY, cert="CONFIRMED",
         kicker="6 DYMER · WAR",
         head="Kyiv-region toll rises to at least 12",
         body="More dead found after Sunday's strike on a block in "
              "Dymer. (Reports)"),
    dict(n=7, pic=pic_hormuz, tag="HORMUZ · SHIPPING", tag_bg=TEAL,
         cert="REPORTED", kicker="7 STRAIT OF HORMUZ · SHIPPING",
         head="More tankers hit as Hormuz attacks mount",
         body="Two more tankers caught fire Sunday after hitting "
              "mines, Iran says. (AP)"),
    dict(n=8, pic=pic_seattle, tag="SEATTLE · AMERICAS", tag_bg=NAVY,
         cert="REPORTED", kicker="8 SEATTLE · IMMIGRATION",
         head="Father and daughter held by ICE at airport",
         body="Pair bound for a family baptism when held at Seattle "
              "airport. (The Hindu)"),
    dict(n=9, pic=pic_fifa, tag="FOOTBALL", tag_bg=GREEN, cert="REPORTED",
         kicker="9 LONDON · SPORT",
         head="UK to host the 2035 Women's World Cup",
         body="FIFA to name UK as hosts of the 2035 Women's World Cup "
              "on Monday. (Reports)"),
    dict(n=10, pic=pic_seoul, tag="SEOUL · POLITICS", tag_bg=NAVY,
         cert="REPORTED", kicker="10 SEOUL · POLITICS",
         head="Minister quits over AI exam-cheating scandal",
         body="Seoul's education minister quits over AI cheating in "
              "the exams. (Reports)"),
    dict(n=11, pic=pic_cikande, tag="BANTEN · DISASTER", tag_bg=DARKRED,
         cert="CONFIRMED", kicker="11 CIKANDE · DISASTER",
         head="24 body bags after factory fire",
         body="24 body bags found after Sunday's fire; search resumes "
              "Monday. (Reports)"),
    dict(n=12, pic=pic_cricket, tag="CRICKET", tag_bg=GREEN, cert="CONFIRMED",
         kicker="12 INDIA · CRICKET",
         head="India push for victory on Day 5 in NZ Test",
         body="NZ are 157 for 4 at lunch on Day 5 as India press for "
              "the win. (Reports)"),
    dict(n=13, pic=pic_shuri, tag="OKINAWA · CULTURE", tag_bg=TEAL,
         cert="CONFIRMED", kicker="13 OKINAWA · CULTURE",
         head="Shuri Castle's great hall opens again",
         body="Restored main hall opens Monday, seven years after "
              "the 2019 fire. (Reports)"),
]

ALSO = [
    "UK to build Ukrainian drones in a new deal",
    "Lahore most polluted city again (Sun)",
    "Settlers torch 12 vehicles near Ramallah",
    "Sudan strikes hit Khartoum, UN site hit (Sun)",
    "Houthis claim Saudi refinery strike (CLAIM)",
    "Hegseth memo curbs US–Canada defence ties",
    "Democrats flip N. Carolina seat in House",
    "Trump reposts 'TrumpCare' health pitch",
    "Oracle says its AI funding is secured (Sun)",
    "Taiwan export orders rise for a 21st month",
    "FIDE title Game 1: Sindarov gets White",
    "Marquez wins 8th MotoGP title (Sun)",
    "Liverpool beat 10-man Man Utd (Sun)",
    "Thitikul wins third straight LPGA title (Sun)",
    "Alcaraz wins first ATP Finals title (Sun)",
    "BepiColombo enters orbit around Mercury (Sat)",
    "Brent $92.58; WTI $83.56 (Fri close)",
    "Bitcoin $58,970, down 5.2% (Sat)",
    "UK, France, China block UN top-job bid",
    "Trump: working with Schumer 'difficult'",
    "US hawks urge Iran strike; Trump: no rush",
    "Youth Congress protests Meta in India",
    "Price wins Grand Slam darts (Sun)",
]

REGIONS = [
    ("Europe 9", NAVY), ("Asia-Pacific 9", RED), ("Middle East 3", TEAL),
    ("Africa 2", GREEN), ("Americas 7", DARKRED), ("Global 6", GREY),
]

NUMBERS = [
    ("3", "missiles in Poland"),
    ("17.5%", "Taiwan weekly fall"),
    ("12", "dead, Kyiv region"),
    ("24", "body bags, Cikande"),
    ("35%", "COP31 power goal"),
    ("538", "Lahore air index"),
]

TIMELINE = [
    ("02:22", "Refinery hit, Rostov"),
    ("MORNING", "Taiwan bans short sales"),
    ("MORNING", "Asian markets on alert"),
    ("MIDDAY", "NATO Council meets"),
    ("AFTERNOON", "FIFA confirms UK 2035"),
    ("EVENING", "Search resumes, Cikande"),
    ("NIGHT", "India press on, Day 5"),
]


def build():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # top line
    d.text((16, 6), "THE WORLD IN ONE DAY", font=font(SANS_B, 13), fill=RED)
    right = "36 STORIES · 6 REGIONS · MONDAY 23 NOVEMBER 2026"
    rw = d.textlength(right, font=font(SANS_B, 11))
    d.text((W - 16 - rw, 8), right, font=font(SANS_B, 11), fill=BLACK)
    d.line([16, 26, W - 16, 26], fill=BLACK, width=2)

    # masthead
    title = "Monday 23 November 2026"
    tf = font(SERIF_B, 56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 30), title, font=tf, fill=BLACK)
    sub = "COP31 collapses · NATO meets on Poland · Asia's markets on alert after Friday's rout"
    sf = font(SERIF, 15)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 94), sub, font=sf, fill=BLACK)
    d.line([16, 116, W - 16, 116], fill=BLACK, width=1)

    # timeline strip
    y = 122
    d.rectangle([16, y, 126, y + 26], fill=RED)
    d.text((22, y + 4), "THE DAY", font=font(SANS_B, 10), fill=WHITE)
    d.text((22, y + 14), "IN UTC", font=font(SANS_B, 10), fill=WHITE)
    d.line([16, y + 26, W - 16, y + 26], fill=BLACK, width=1)
    slots = 7
    slot_w = (W - 32 - 126) / slots
    for i, (tm, ev) in enumerate(TIMELINE):
        cx = 126 + 16 + slot_w * i + slot_w / 2
        d.text((cx - d.textlength(tm, font=font(SANS_B, 10)) / 2, y + 2),
               tm, font=font(SANS_B, 10), fill=RED)
        lines = wrap(d, ev, font(SANS, 9), slot_w - 8)
        ly = y + 14
        for ln in lines[:2]:
            d.text((cx - d.textlength(ln, font=font(SANS, 9)) / 2, ly),
                   ln, font=font(SANS, 9), fill=BLACK)
            ly += 10

    # numbers strip
    y = 154
    d.rectangle([16, y, 126, y + 36], fill=RED)
    d.text((22, y + 6), "THE DAY", font=font(SANS_B, 11), fill=WHITE)
    d.text((22, y + 18), "IN NUMBERS", font=font(SANS_B, 10), fill=WHITE)
    d.line([16, y + 36, W - 16, y + 36], fill=BLACK, width=1)
    n_w = (W - 32 - 126) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = 126 + 16 + n_w * i + n_w / 2
        nf = font(SANS_B, 21)
        d.text((cx - d.textlength(num, font=nf) / 2, y + 2), num,
               font=nf, fill=BLACK)
        lines = wrap(d, lab, font(SANS, 9), n_w - 6)
        ly = y + 26
        for ln in lines[:1]:
            d.text((cx - d.textlength(ln, font=font(SANS, 9)) / 2, ly),
                   ln, font=font(SANS, 9), fill=RED)
            ly += 10

    # region strip
    y = 194
    x = 16
    total_w = W - 32
    each = total_w / len(REGIONS)
    for name, col in REGIONS:
        d.rectangle([x, y, x + each - 2, y + 18], fill=col)
        tw2 = d.textlength(name, font=font(SANS_B, 11))
        d.text((x + (each - 2 - tw2) / 2, y + 3), name,
               font=font(SANS_B, 11), fill=WHITE)
        x += each

    # heroes
    hy, hh = 218, 236
    hw = (W - 32 - 2 * 10) / 3
    for i, s in enumerate(HEROES):
        hx = 16 + i * (hw + 10)
        s["pic"](d, hx, hy, hw, 118)
        chip(d, hx + 4, hy + 118 - 20, s["tag"], font(SANS_B, 10),
             s["tag_bg"], WHITE)
        cw = chip_width(d, s["cert"])
        certainty_chip(d, hx + hw - cw - 4, hy + 4, s["cert"])
        d.text((hx, hy + 122), s["kicker"], font=font(SANS_B, 11), fill=RED)
        yy = draw_wrapped(d, hx, hy + 138, s["head"], font(SERIF_B, 21),
                          BLACK, hw, 25)
        draw_wrapped(d, hx, yy + 2, s["body"], font(SANS, 13), BLACK, hw, 16)

    # secondary grid: 5 columns x 2 rows
    sy = 456
    sw_ = (W - 32 - 4 * 8) / 5
    sh_ = 140
    for i, s in enumerate(SECONDARY):
        r, c = divmod(i, 5)
        sx = 16 + c * (sw_ + 8)
        syy = sy + r * (sh_ + 6)
        s["pic"](d, sx, syy, sw_, 46)
        chip(d, sx + 3, syy + 46 - 16, s["tag"], font(SANS_B, 8),
             s["tag_bg"], WHITE)
        cw2 = chip_width(d, s["cert"])
        certainty_chip(d, sx + sw_ - cw2 - 3, syy + 3, s["cert"])
        d.text((sx, syy + 49), s["kicker"], font=font(SANS_B, 10), fill=RED)
        yy = draw_wrapped(d, sx, syy + 61, s["head"], font(SERIF_B, 14),
                          BLACK, sw_, 16)
        draw_wrapped(d, sx, yy + 1, s["body"], font(SANS, 12), BLACK, sw_,
                     13)

    # bottom: map left, also list right
    by = 750
    # map panel
    d.text((16, by), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=RED)
    d.rectangle([16, by + 20, 340, by + 196], outline=MIDGREY, width=1)
    mx0, my0, mx1, my1 = 16, by + 20, 340, by + 196
    d.rectangle([mx0, my0, mx1, my1], fill=(226, 236, 242))
    # rough continents, panel-local coords offset by (mx0, my0)
    land = (214, 200, 160)

    def poly(pts):
        d.polygon([(mx0 + px, my0 + py) for px, py in pts], fill=land)

    poly([(24, 50), (104, 34), (154, 50), (134, 100), (74, 108),
          (34, 82)])                                       # N America
    poly([(104, 112), (144, 108), (156, 140), (134, 166),
          (112, 140)])                                     # S America
    poly([(194, 36), (234, 28), (252, 46), (230, 64),
          (198, 56)])                                      # Europe
    poly([(204, 70), (246, 66), (260, 100), (242, 140), (216, 128),
          (200, 98)])                                      # Africa
    poly([(256, 30), (314, 24), (320, 60), (294, 90), (266, 74),
          (252, 50)])                                      # Asia
    poly([(284, 140), (314, 138), (318, 152), (290, 154)])  # Australia
    pins = [(268, 58, 1), (216, 34, 2), (294, 82, 3), (222, 84, 4),
            (248, 40, 5), (230, 46, 6), (276, 74, 7), (34, 60, 8),
            (194, 30, 9), (304, 52, 10), (288, 110, 11), (278, 94, 12),
            (314, 72, 13)]
    for px, py, n in pins:
        num_circle(d, mx0 + px, my0 + py, n, r=7)
    d.text((22, by + 178), "Tags: OFFICIAL black · CONFIRMED red · "
           "REPORTED grey · CLAIM outline", font=font(SANS, 9), fill=GREY)

    # also list, two columns
    ax = 356
    d.text((ax, by), "ALSO ON MONDAY 23 NOVEMBER — 23 MORE STORIES",
           font=font(SANS_B, 12), fill=RED)
    col_w = (W - 16 - ax - 12) / 2
    af = font(SANS, 12)
    nf2 = font(SANS_B, 12)
    for i, item in enumerate(ALSO):
        col, row = divmod(i, 12)
        lx = ax + col * (col_w + 12)
        ly = by + 20 + row * 15
        num = str(14 + i)
        d.text((lx, ly), num, font=nf2, fill=RED)
        nw = d.textlength(num + " ", font=nf2)
        txt = item
        while d.textlength(txt, font=af) > col_w - nw - 2 and len(txt) > 10:
            txt = txt[:-1]
        if txt != item:
            txt = txt[:-3].rstrip() + "…"
        d.text((lx + nw, ly), txt, font=af, fill=BLACK)

    # date check
    dy = 962
    d.rectangle([16, dy, W - 16, dy + 40], fill=RED)
    d.text((22, dy + 4), "DATE CHECK", font=font(SANS_B, 12), fill=WHITE)
    dc = ("Left out as not Monday's news: the '400 drones, 110 missiles' "
          "attack on Ukraine (Fri 20–Sat 21 Nov); Sparta and Kryvyi Rih "
          "strikes (Sat); 'Chapo Isidro' captured Fri 20 Nov; the "
          "killer-robot deal (Sat 21 Nov); the Shenzhen summit, Anthropic "
          "IPO and GTA VI launch (19 Nov); COP31 drafts before Sunday.")
    draw_wrapped(d, 108, dy + 3, dc, font(SANS, 11), WHITE, W - 16 - 108 - 8,
                 13)
    d.text((16, 1006), "Sunday events are dated as Sunday in their cards. "
           "Claims are labelled as claims. "
           "Sources named beside each story · original drawings",
           font=font(SANS, 10), fill=GREY)

    img.save(os.path.join(HERE, "entry.png"), "PNG")
    print("wrote", os.path.join(HERE, "entry.png"))


if __name__ == "__main__":
    build()
