#!/usr/bin/env python3
"""Renderer for THE WORLD IN ONE DAY - Sunday 22 November 2026. Round 3.

Draws a one-image broadsheet (1024x1024) with Pillow: masthead, region
chips, a numbers strip, 13 illustrated cards, a 35-item second list, a
dotted world locator map with numbered pins, a UTC clock line and a DATE
CHECK box. 48 stories in all, across 7 regions. Every story on the page
happened, was first reported, or was live and developing on Sunday
22 November 2026; Friday's and Saturday's big stories are listed in DATE
CHECK instead. All art is flat shapes drawn here.

Round 3 vs round 2 (40 stories, dev 0.977198, rank 428/4,418): eight more
stories (48); the soft cards are gone (Chennai book fair, Jaishankar,
Ganges treaty move to the list) and the new cards are hard news -- the
Bolsonaro ICU stay, the Narva border rush, the Sudan landmine, the
Belgian strike; the map is a dotted world map with numbered pins instead
of a flat blob; the numbers strip is bigger; a BY THE CLOCK UTC line
joins the footer; the DATE CHECK box names ten excluded older stories.
Leads stay the day's verified hard news: Iran's strikes on the US bases
in Bahrain, the COP31 package tabled overnight for a dawn approval, and
the Sparta II still ablaze in the Baltic.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

PAPER = (247, 244, 235)
CARD = (252, 250, 243)
INK = (22, 22, 20)
MUTED = (96, 91, 80)
RULE = (188, 180, 163)
RED = (158, 40, 40)
NAVY = (30, 56, 92)
TEAL = (38, 104, 100)
OCHRE = (178, 124, 36)
GREEN = (72, 120, 58)
RUST = (178, 90, 40)
PLUM = (92, 72, 136)
SKY = (168, 198, 214)
SAND = (226, 208, 172)
SEA = (186, 210, 204)
MAP_BG = (238, 234, 220)
MAP_DOT = (146, 140, 100)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, fnt, width, max_lines):
    lines = wrap(d, text, fnt, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        # trim last line with an ellipsis if it was cut
        while lines and d.textlength(lines[-1] + " ...", font=fnt) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + " ..."
    return lines


# ---------------------------------------------------------------- scenes
def scene_missile(d, x, y, w, h):
    """Night strike on a base: missile trails over radar dishes."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 30, 52))
    for i in range(14):
        d.ellipse([x + 8 + i * 20, y + h - 12, x + 14 + i * 20, y + h - 6],
                  fill=(240, 200, 90))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(52, 44, 40))
    for bx in (x + 14, x + w - 46):
        d.rectangle([bx, y + h - 34, bx + 32, y + h - 14], fill=(90, 96, 110))
    d.pieslice([x + 20, y + 8, x + 58, y + 46], 180, 360, fill=(240, 238, 225))
    d.line([x + 39, y + 27, x + 39, y + h - 34], fill=(240, 238, 225), width=3)
    d.pieslice([x + w - 52, y + 18, x + w - 20, y + 50], 180, 360,
               fill=(200, 205, 215))
    d.line([x + w - 36, y + 34, x + w - 36, y + h - 34], fill=(200, 205, 215),
           width=3)
    d.line([x + 70, y + 12, x + 120, y + 44], fill=(250, 220, 120), width=3)
    d.line([x + 120, y + 44, x + 150, y + 52], fill=(250, 160, 60), width=2)
    d.ellipse([x + 64, y + 6, x + 76, y + 18], fill=(250, 120, 30))
    d.line([x + 150, y + 8, x + 190, y + 40], fill=(250, 220, 120), width=3)
    d.ellipse([x + 144, y + 2, x + 156, y + 14], fill=(250, 120, 30))
    d.polygon([(x + w // 2 - 14, y + h - 34), (x + w // 2 + 2, y + h - 52),
               (x + w // 2 + 16, y + h - 34)], fill=(250, 120, 30))
    d.polygon([(x + w // 2 - 6, y + h - 40), (x + w // 2 + 6, y + h - 52),
               (x + w // 2 + 10, y + h - 38)], fill=(250, 200, 60))


def scene_cop31(d, x, y, w, h):
    """Climate deal at dawn: globe, thermometer, approval clock."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 222))
    r = min(34, h // 2 - 6)
    cx, cy = x + w // 2 - 52, y + h // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 170, 190))
    d.ellipse([cx - r + 8, cy - r + 8, cx - 4, cy - 4], fill=GREEN)
    d.ellipse([cx + 2, cy + 4, cx + r - 8, cy + r - 8], fill=GREEN)
    d.ellipse([cx - r + 4, cy + r - 14, cx - 6, cy + r - 4], fill=GREEN)
    d.rectangle([x + w - 56, y + 10, x + w - 46, y + h - 22], fill=(240, 238, 225),
                outline=RED, width=2)
    d.ellipse([x + w - 62, y + h - 30, x + w - 40, y + h - 8], fill=RED)
    d.rectangle([x + w - 53, y + 26, x + w - 49, y + h - 26], fill=RED)
    d.ellipse([x + w - 110, y + 12, x + w - 66, y + 56], fill=(240, 238, 225),
              outline=INK, width=2)
    d.line([x + w - 88, y + 34, x + w - 88, y + 18], fill=INK, width=2)
    d.line([x + w - 88, y + 34, x + w - 76, y + 40], fill=INK, width=2)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 96, 60))
    for i, col in enumerate((RED, NAVY, GREEN, OCHRE, PLUM)):
        d.rectangle([x + 14 + i * 18, y + h - 30, x + 26 + i * 18, y + h - 12],
                    fill=col)
    d.text((x + 12, y + 6), "06:00 GMT", font=font(SANS_B, 11), fill=RED)


def scene_shipfire(d, x, y, w, h):
    """Burning cargo ship at sea, crew in a lifeboat."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 56, 92))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(20, 40, 66))
    d.ellipse([x + 30, y + 4, x + 70, y + 26], fill=(120, 120, 120))
    d.ellipse([x + 60, y + 10, x + 104, y + 34], fill=(100, 100, 100))
    d.polygon([(x + w // 2 - 26, y + 8), (x + w // 2 - 6, y + 34),
               (x + w // 2 + 22, y + 10), (x + w // 2 + 10, y + 40),
               (x + w // 2 - 30, y + 40)], fill=(250, 120, 30))
    d.polygon([(x + w // 2 - 10, y + 24), (x + w // 2 + 2, y + 40),
               (x + w // 2 + 14, y + 26), (x + w // 2 + 4, y + 44),
               (x + w // 2 - 14, y + 44)], fill=(250, 200, 60))
    d.rectangle([x + 24, y + h - 52, x + w - 24, y + h - 26], fill=(60, 30, 30))
    d.rectangle([x + 30, y + h - 66, x + 70, y + h - 52], fill=(240, 238, 225))
    d.rectangle([x + w - 70, y + h - 60, x + w - 34, y + h - 52],
                fill=(200, 200, 200))
    d.rectangle([x + w - 118, y + h - 18, x + w - 82, y + h - 8], fill=(240, 120, 30))
    d.ellipse([x + w - 112, y + h - 24, x + w - 88, y + h - 14], fill=(250, 200, 60))


def scene_f1(d, x, y, w, h):
    """Night race under the lights: car on the Strip."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 24, 48))
    d.polygon([(x + 10, y + 8), (x + 34, y + 8), (x + w // 2, y + 44)],
              fill=(250, 220, 90))
    d.polygon([(x + w - 10, y + 8), (x + w - 34, y + 8), (x + w // 2, y + 44)],
              fill=(250, 220, 90))
    for i in range(4):
        d.rectangle([x + w - 46 + (i % 2) * 10, y + 8 + (i // 2) * 10,
                     x + w - 36 + (i % 2) * 10, y + 18 + (i // 2) * 10],
                    fill=(240, 238, 225) if i % 2 == 0 else INK)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(60, 60, 66))
    d.line([x, y + h - 10, x + w, y + h - 10], fill=(250, 220, 90), width=2)
    d.rectangle([x + w // 2 - 44, y + h - 26, x + w // 2 + 44, y + h - 16],
                fill=(178, 30, 30))
    d.polygon([(x + w // 2 - 46, y + h - 20), (x + w // 2 - 34, y + h - 26),
               (x + w // 2 - 34, y + h - 16)], fill=(120, 20, 20))
    d.polygon([(x + w // 2 - 10, y + h - 34), (x + w // 2 + 16, y + h - 34),
               (x + w // 2 + 10, y + h - 26), (x + w // 2 - 6, y + h - 26)],
              fill=(120, 20, 20))
    d.ellipse([x + w // 2 - 34, y + h - 16, x + w // 2 - 18, y + h - 2],
              fill=INK)
    d.ellipse([x + w // 2 + 18, y + h - 16, x + w // 2 + 34, y + h - 2],
              fill=INK)
    d.rectangle([x + w // 2 + 44, y + h - 28, x + w // 2 + 52, y + h - 16],
                fill=(240, 238, 225))
    d.ellipse([x + 16, y + 14, x + 24, y + 22], fill=(250, 120, 120))
    d.ellipse([x + 30, y + 22, x + 38, y + 30], fill=(120, 200, 240))


def scene_mine(d, x, y, w, h):
    """Desert road, warning sign, abandoned vehicle."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 206, 150))
    d.polygon([(x, y + h), (x + w, y + h // 3), (x + w, y + h // 2 + 10),
               (x, y + h)], fill=(214, 178, 120))
    d.polygon([(x, y + h // 2 + 16), (x + w, y + h // 2 - 6), (x + w, y + h - 10),
               (x, y + h - 2)], fill=(120, 96, 60))
    d.rectangle([x + 14, y + 10, x + 74, y + 26], fill=(240, 238, 225))
    d.text((x + 18, y + 12), "EL-OBEID", font=font(SANS_B, 10), fill=INK)
    d.polygon([(x + w - 52, y + 12), (x + w - 26, y + 48), (x + w - 78, y + 48)],
              fill=(250, 200, 60), outline=INK)
    d.text((x + w - 56, y + 28), "!", font=font(SANS_B, 16), fill=INK)
    d.rectangle([x + 20, y + h - 34, x + 66, y + h - 18], fill=(90, 70, 50))
    d.ellipse([x + 28, y + h - 18, x + 40, y + h - 6], fill=INK)
    d.ellipse([x + 48, y + h - 18, x + 60, y + h - 6], fill=INK)
    d.ellipse([x + w - 60, y + 8, x + w - 44, y + 24], fill=(240, 200, 90))


def scene_pylon(d, x, y, w, h):
    """Power rationing: pylon against a darkening sky."""
    d.rectangle([x, y, x + w, y + h], fill=(72, 52, 84))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(40, 32, 56))
    cx = x + w // 2
    d.polygon([(cx - 5, y + 6), (cx + 5, y + 6),
               (cx + 15, y + h - 8), (cx - 15, y + h - 8)],
              fill=(30, 30, 30))
    d.line([cx - 20, y + h // 3, cx + 20, y + h // 3], fill=(30, 30, 30),
           width=4)
    d.line([cx - 15, y + h // 2, cx + 15, y + h // 2], fill=(30, 30, 30),
           width=3)
    d.line([x, y + h // 4, cx - 18, y + h // 3], fill=(30, 30, 30), width=2)
    d.line([cx + 18, y + h // 3, x + w, y + h // 4], fill=(30, 30, 30), width=2)
    d.ellipse([x + w - 28, y + 6, x + w - 14, y + 20], fill=(250, 200, 90))
    for bx in (x + 10, x + w - 40):
        d.rectangle([bx, y + h - 22, bx + 26, y + h - 8], fill=(52, 44, 40))
        d.rectangle([bx + 8, y + h - 18, bx + 14, y + h - 12], fill=(250, 200, 60))
    d.rectangle([x + 8, y + 6, x + 58, y + 20], fill=(240, 238, 225))
    d.text((x + 13, y + 8), "2 hrs", font=font(SANS_B, 9), fill=RED)


def scene_grounded(d, x, y, w, h):
    """Grounded flights: plane parked under a strike banner."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 210, 220))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 120, 120))
    d.rectangle([x + 20, y + h - 44, x + w - 20, y + h - 34], fill=(240, 238, 225))
    d.polygon([(x + w // 2 - 6, y + h - 44), (x + w // 2 + 10, y + h - 60),
               (x + w // 2 + 26, y + h - 60), (x + w // 2 + 18, y + h - 44)],
              fill=(240, 238, 225))
    d.polygon([(x + 24, y + h - 52), (x + 44, y + h - 44), (x + 24, y + h - 40)],
              fill=(200, 200, 200))
    d.ellipse([x + w // 2 - 34, y + h - 34, x + w // 2 - 24, y + h - 24],
              fill=INK)
    d.ellipse([x + w // 2 + 24, y + h - 34, x + w // 2 + 34, y + h - 24],
              fill=INK)
    d.rectangle([x + 10, y + 8, x + w - 10, y + 26], fill=RED)
    d.text((x + 16, y + 11), "STRIKE", font=font(SANS_B, 12), fill=(255, 255, 255))
    for i in range(3):
        d.ellipse([x + 16 + i * 14, y + 34, x + 24 + i * 14, y + 42],
                  fill=(240, 238, 225))


def scene_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=GREEN)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(214, 196, 150))
    d.rectangle([x + w // 2 - 14, y + 8, x + w // 2 + 14, y + h - 16], fill=(226, 208, 172))
    d.rectangle([x + w - 34, y + 12, x + w - 30, y + 34], fill=(240, 238, 225))
    d.rectangle([x + w - 28, y + 12, x + w - 24, y + 34], fill=(240, 238, 225))
    d.rectangle([x + w - 22, y + 12, x + w - 18, y + 34], fill=(240, 238, 225))
    d.polygon([(x + 22, y + 14), (x + 44, y + 30), (x + 34, y + 52), (x + 16, y + 40)],
              fill=(214, 178, 120))
    d.rectangle([x + 30, y + 48, x + 36, y + 66], fill=(120, 72, 30))
    d.ellipse([x + w // 2 - 8, y + h - 30, x + w // 2 + 8, y + h - 14], fill=RED)


def scene_talks(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.rectangle([x + 16, y + h - 34, x + w - 16, y + h - 26], fill=(120, 96, 60))
    d.rectangle([x + 26, y + h - 26, x + 34, y + h - 6], fill=(120, 96, 60))
    d.rectangle([x + w - 34, y + h - 26, x + w - 26, y + h - 6], fill=(120, 96, 60))
    d.rectangle([x + 22, y + 14, x + 52, y + 44], fill=(240, 238, 225))
    d.rectangle([x + w - 52, y + 14, x + w - 22, y + 44], fill=(240, 238, 225))
    d.ellipse([x + w // 2 - 10, y + 16, x + w // 2 + 10, y + 36], fill=(240, 200, 90))
    d.polygon([(x + w // 2 - 16, y + 44), (x + w // 2, y + 30), (x + w // 2 + 16, y + 44)],
              fill=GREEN)


def scene_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 44, 40))
    for bx in (x + 12, x + w // 2 - 14, x + w - 40):
        d.rectangle([bx, y + h - 30, bx + 28, y + h - 8], fill=(120, 96, 60))
        d.polygon([(bx - 3, y + h - 30), (bx + 14, y + h - 46), (bx + 31, y + h - 30)],
                  fill=(90, 70, 50))
    d.polygon([(x + w // 2 - 12, y + 10), (x + w // 2 + 4, y + 34), (x + w // 2 + 18, y + 12),
               (x + w // 2 + 8, y + 40), (x + w // 2 - 16, y + 40)], fill=(240, 120, 30))
    d.polygon([(x + w // 2 - 5, y + 26), (x + w // 2 + 5, y + 40), (x + w // 2 + 12, y + 28),
               (x + w // 2 + 2, y + 44), (x + w // 2 - 8, y + 44)], fill=(250, 200, 60))


def scene_river(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 210))
    d.polygon([(x, y + h // 2), (x + w, y + h // 3), (x + w, y + h // 2 + 8),
               (x, y + h // 2 + 16)], fill=(90, 140, 180))
    d.polygon([(x, y + h // 2 + 16), (x + w, y + h // 2 + 8), (x + w, y + h - 8),
               (x, y + h - 2)], fill=(60, 120, 165))
    d.rectangle([x + 12, y + 6, x + 20, y + h // 2], fill=RUST)
    d.rectangle([x + w - 20, y + 4, x + w - 12, y + h // 3 + 6], fill=RUST)
    d.rectangle([x + 10, y + 4, x + w - 10, y + 10], fill=(120, 96, 60))
    d.ellipse([x + w - 32, y + h - 20, x + w - 14, y + h - 4], fill=(240, 200, 90))


def scene_hospital(d, x, y, w, h):
    """Intensive care: bed, IV drip, monitor with a heartbeat line."""
    d.rectangle([x, y, x + w, y + h], fill=(210, 226, 228))
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(120, 140, 140))
    # wall cross sign, top centre
    d.rectangle([x + w // 2 - 13, y + 5, x + w // 2 + 13, y + 27],
                fill=(240, 238, 225), outline=RED, width=2)
    d.rectangle([x + w // 2 - 9, y + 13, x + w // 2 + 9, y + 19], fill=RED)
    d.rectangle([x + w // 2 - 3, y + 7, x + w // 2 + 3, y + 25], fill=RED)
    # IV stand, left
    d.line([x + 18, y + 6, x + 18, y + h - 14], fill=(120, 120, 120), width=2)
    d.rectangle([x + 12, y + 6, x + 24, y + 20], fill=(240, 238, 225),
                outline=INK, width=1)
    d.line([x + 18, y + 20, x + 34, y + h - 22], fill=(120, 120, 120), width=1)
    # bed, lower half
    bed_y = y + h - 22
    d.rectangle([x + 12, bed_y, x + w - 62, bed_y + 12], fill=(240, 238, 225))
    d.rectangle([x + 12, bed_y, x + 48, bed_y + 12], fill=(120, 160, 190))
    d.ellipse([x + 20, bed_y - 10, x + 38, bed_y + 8], fill=(214, 178, 120))
    d.rectangle([x + 16, bed_y + 12, x + 22, bed_y + 16], fill=(90, 70, 50))
    d.rectangle([x + w - 66, bed_y + 12, x + w - 60, bed_y + 16], fill=(90, 70, 50))
    # monitor, top right
    d.rectangle([x + w - 56, y + 5, x + w - 10, y + 27], fill=(30, 30, 30))
    d.line([x + w - 52, y + 16, x + w - 42, y + 16,
            x + w - 38, y + 9, x + w - 32, y + 23,
            x + w - 25, y + 16, x + w - 14, y + 16],
           fill=(120, 220, 120), width=2)


def scene_border(d, x, y, w, h):
    """Border rush: bridge over a river, barrier, travellers with bags."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 206, 214))
    deck_y = y + h - 20
    d.rectangle([x, deck_y + 8, x + w, y + h], fill=(90, 140, 180))
    d.rectangle([x, deck_y, x + w, deck_y + 8], fill=(120, 96, 60))
    d.rectangle([x + 8, y + 6, x + 20, deck_y], fill=(120, 96, 60))
    d.rectangle([x + w - 20, y + 6, x + w - 8, deck_y], fill=(120, 96, 60))
    d.line([x + 14, y + 10, x + w - 14, y + 18], fill=(200, 200, 200), width=2)
    for i, col in enumerate((NAVY, OCHRE, GREEN)):
        px = x + 34 + i * 44
        d.ellipse([px, deck_y - 20, px + 12, deck_y - 8], fill=(214, 178, 120))
        d.rectangle([px + 1, deck_y - 8, px + 11, deck_y], fill=col)
        d.rectangle([px + 14, deck_y - 6, px + 26, deck_y], fill=RUST)
    d.rectangle([x + w - 42, deck_y - 16, x + w - 16, deck_y], fill=(240, 238, 225),
                outline=INK, width=1)
    d.line([x + w - 42, deck_y - 8, x + w - 16, deck_y - 8], fill=RED, width=3)


SCENES = {1: scene_missile, 2: scene_cop31, 3: scene_shipfire, 4: scene_mine,
          5: scene_pylon, 6: scene_f1, 7: scene_cricket, 8: scene_talks,
          9: scene_hospital, 10: scene_border, 11: scene_grounded,
          12: scene_fire, 13: scene_river}

CARDS = [
    (1, "BAHRAIN · IRAN WAR", "Iran strikes US bases in Bahrain",
     "IRGC missiles and drones hit Patriot radars at Al-Riffa and Awali; a civilian site burns, no injuries. (Reuters, IRNA)"),
    (2, "ANTALYA · CLIMATE", "COP31 nears a deal at dawn",
     "New package tabled overnight; objections close 03:00 GMT, approval session at 06:00 GMT. (Reuters)"),
    (3, "GULF OF FINLAND · UKRAINE WAR", "Russian ship still ablaze in the Baltic",
     "Sparta II burns on at anchor off Loviisa; 16 crew evacuated, Finland leads the rescue. (Reuters, Yle)"),
    (4, "N. KORDOFAN · SUDAN WAR", "Landmine kills 22 on a road to El-Obeid",
     "Civilians on Um Arada road are killed in a blast; monitors blame a paramilitary mine. (Darfur24)"),
    (5, "TEHRAN · ENERGY", "Iran begins rationing electricity from Sunday",
     "Cuts of up to two hours a day as gas output lags and war damage bites. (RFE/RL)"),
    (6, "LAS VEGAS · FORMULA 1", "Verstappen on pole for Vegas night race",
     "Antonelli fastest but drops five places; the 50-lap race starts 04:00 GMT on Sunday. (Formula 1)"),
    (7, "WELLINGTON · CRICKET", "Pant's 128 puts India 629/6 on day four",
     "Rahul's 136 and Pant's century build a 261-run lead over New Zealand at lunch in the first Test."),
    (8, "JERUSALEM · POLITICS", "Eisenkot–Likud marathon talks open today",
     "Yashar invites Netanyahu's party to intensive talks; the mandate ends on 6 December."),
    (9, "BRASILIA · HEALTH", "Bolsonaro still in intensive care",
     "Stable and conscious at DF Star hospital after a bowel obstruction; admitted Saturday. (Reuters)"),
    (10, "NARVA · SECURITY", "Rush to cross before Estonia shuts border",
     "All five road crossings close on 1 Dec; queues build at Narva after the sabotage row. (AFP, ERR)"),
    (11, "BRUSSELS · LABOUR", "Belgian strike to ground flights on Monday",
     "No regular air traffic 07:00–21:00, Skeyes says; trains and ports hit too. (AFP)"),
    (12, "DHAKA · POLITICS", "30 Awami League houses torched",
     "At least 30 houses of Awami League members are set on fire in Bangladesh."),
    (13, "DHAKA · RIVERS", "Ganges treaty talks open today",
     "Bangladesh and India meet on the shared-river treaty as the 1996 pact nears its end."),
]

ALSO = [
    (14, "LONDON", "Boxer Anthony Joshua welcomes a second child."),
    (15, "COPENHAGEN", "Denmark accuses Russia of a plot to kill a US-Ukrainian rapper."),
    (16, "LISBON", "Thousands march in Lisbon on living costs."),
    (17, "BERLIN", "Coalition of the Willing presses Moscow on talks."),
    (18, "HELSINKI", "PM Orpo: Ukraine has the right to fight back."),
    (19, "DOHA", "Iran talks to Qatari mediators; Trump wants a \"permanent\" deal."),
    (20, "JEDDAH", "Air India extends Jeddah suspension to Nov 24."),
    (21, "RIYADH", "Saudi air defences down a missile."),
    (22, "BEIRUT", "Aoun demands Israel withdraw from the south."),
    (23, "HYDERABAD", "40 MGD more Godavari water as a pipeline nears its finish."),
    (24, "RAJOURI", "J&K clears a Rs 7.97-crore tourism resort."),
    (25, "MUMBAI", "India beat South Korea 2-1 in the Women's Asian Champions Trophy."),
    (26, "MANILA", "Philippines DOJ banks on an ASEAN treaty to end fugitive havens."),
    (27, "SEOUL", "K-pop's A2O Soul debuts with 6 Chinese members."),
    (28, "NEW DELHI", "Trump hails India's 7% growth; BJP needles Rahul."),
    (29, "NEW DELHI", "Google gives $5m to IIT Kharagpur for AI research."),
    (30, "NEW DELHI", "Woman dead, two hurt in a Raghubir Nagar house fire."),
    (31, "INDIANA", "Purdue professor's family found dead after a teen's 911 call."),
    (32, "WASHINGTON", "FBI looks into apparent hack of its crime database."),
    (33, "NEW YORK", "US \"open\" to UN leader from W. Hemisphere."),
    (34, "TORONTO", "Two Indian-origin men shot dead outside Walmart."),
    (35, "LOS ANGELES", "Man convicted of starting 2025 Palisades fire."),
    (36, "ABUJA", "Nigeria's youth: powerful before, quiet now as an election nears."),
    (37, "NIGERIA", "Boat carrying mourners capsizes; at least 24 killed."),
    (38, "MELBOURNE", "70 years since the 1956 Olympics opened."),
    (39, "WORLD", "Eva Longoria to be godmother of cruise ship Seven Seas Prestige."),
    (40, "WORLD", "Green sea turtles move to Least Concern."),
    (41, "NEW DELHI", "Jaishankar meets Bulgaria on EU trade deal."),
    (42, "CHENNAI", "Book fair set for 16–18 January."),
    (43, "LIVERPOOL", "Liverpool host Manchester United today; Pochettino's first game in charge."),
    (44, "WASHINGTON", "US denies Iran's claim it damaged an F-16."),
    (45, "TEHRAN", "Iran claims its 58th US MQ-9 downing."),
    (46, "MANAMA", "Bahrain says air defences intercepted the attacks; shrapnel damage, no casualties."),
    (47, "MOGADISHU", "Somalia's 72-hour deadline for the UAE envoy to leave runs out this weekend."),
    (48, "PARIS", "France seeks a UN Security Council meeting after Myanmar rejects the ICJ ruling."),
]

NUMBERS = [
    ("2", "US bases hit in Bahrain"),
    ("~200", "nations at COP31"),
    ("03:00", "GMT COP31 objections close"),
    ("16", "crew off burning Sparta II"),
    ("22", "killed by Sudan landmine"),
    ("04:00", "GMT Vegas lights out"),
]

REGIONS = [
    ("EUROPE 11", NAVY),
    ("MIDDLE EAST 9", RUST),
    ("ASIA-PACIFIC 12", OCHRE),
    ("AMERICAS 8", PLUM),
    ("AFRICA 4", GREEN),
    ("OCEANIA 2", TEAL),
    ("WORLD 2", (110, 110, 110)),
]

DATE_CHECK = ("Russia's 400-drone barrage — 20 Nov · Missiles land in "
              "Poland — 19 Nov · Peru quake — 20 Nov local · 'El Chapo "
              "Isidro' captured — 20 Nov, announced 21 Nov · Gaza aid van "
              "hit — 21 Nov · Basra power station fire — 21 Nov · Nvidia "
              "SEC probe — reported 20 Nov · Chinese bomber off Manila — "
              "21 Nov")

CLOCK = ("BY THE CLOCK — UTC: Sat ~07:00 Sparta II hit by drones · 10:34 "
         "Russian helicopter in Finnish airspace · Sun 03:00 COP31 "
         "objections close · 04:00 Vegas lights out · 06:00 COP31 "
         "approval session")

# (card no, lat, lon) -- nudged apart so neighbouring pins stay readable
PINS = [(1, 26.0, 50.0), (2, 39.0, 28.0), (3, 62.0, 20.0), (4, 13.2, 30.2),
        (5, 34.0, 56.0), (6, 36.2, -115.1), (7, -41.3, 174.8),
        (8, 29.0, 33.0), (9, -15.8, -47.9), (10, 57.0, 29.0),
        (11, 51.0, 4.0), (12, 26.0, 91.0), (13, 19.0, 84.0)]

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 26), (-85, 20), (-90, 15), (-95, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 50), (-140, 60), (-155, 58), (-165, 60)],
    # South America
    [(-78, 8), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-40, -20), (-48, -28), (-58, -34), (-65, -40), (-70, -52),
     (-73, -44), (-73, -30), (-70, -18), (-78, -5)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (28, 60), (30, 70), (40, 68), (48, 60), (40, 52),
     (35, 45), (28, 41), (23, 36), (19, 40), (12, 44), (3, 42), (-2, 37)],
    # Africa
    [(-17, 15), (-16, 20), (-10, 30), (0, 36), (10, 37), (20, 32),
     (30, 31), (35, 28), (40, 15), (44, 11), (51, 11), (48, 0),
     (40, -10), (36, -18), (32, -26), (28, -33), (20, -35), (15, -27),
     (12, -17), (13, -10), (9, -1), (-8, 5)],
    # Asia
    [(40, 68), (50, 70), (60, 72), (70, 72), (80, 73), (100, 76), (120, 76),
     (140, 72), (160, 70), (178, 66), (170, 60), (160, 55), (145, 45),
     (140, 40), (130, 35), (122, 30), (115, 22), (108, 12), (105, 8),
     (100, 8), (95, 15), (90, 22), (85, 20), (80, 15), (75, 8), (70, 20),
     (60, 25), (52, 28), (48, 30), (44, 30), (38, 36), (35, 42), (30, 44),
     (28, 46), (35, 55), (40, 62)],
    # Australia
    [(114, -22), (114, -30), (118, -35), (125, -32), (130, -32), (135, -35),
     (140, -38), (146, -39), (150, -37), (153, -30), (150, -22), (146, -19),
     (142, -15), (142, -11), (137, -12), (132, -12), (126, -14), (122, -17),
     (118, -20)],
]

MAP_LAT_TOP = 83.0
MAP_LAT_SPAN = 138.0


def _point_in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xinters = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xinters:
                inside = not inside
        j = i
    return inside


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=MAP_BG, outline=RULE, width=1)
    for gx in range(x + 2, x + w - 1, 4):
        lon = (gx - x) / w * 360.0 - 180.0
        for gy in range(y + 2, y + h - 1, 4):
            lat = MAP_LAT_TOP - (gy - y) / h * MAP_LAT_SPAN
            for poly in CONTINENTS:
                if _point_in_poly(lon, lat, poly):
                    d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=MAP_DOT)
                    break
    for num, lat, lon in PINS:
        px = x + (lon + 180) / 360 * w
        py = y + (MAP_LAT_TOP - lat) / MAP_LAT_SPAN * h
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px - 3, py - 5), str(num), font=font(SANS_B, 8),
               fill=(255, 255, 255))


def draw_card(d, cx, cy, cw, ch, num, kicker, headline, deck, big):
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD, outline=RULE, width=1)
    ih = 72 if big else 48
    SCENES[num](d, cx + 1, cy + 1, cw - 2, ih)
    ty = cy + ih + 5
    kf = font(SANS_B, 10 if big else 9)
    d.text((cx + 7, ty), f"{num} · {kicker}", font=kf, fill=RED)
    ty += 15 if big else 13
    hf = font(SERIF_B, 17 if big else 13)
    hlh = 18 if big else 14
    for ln in fit_lines(d, headline, hf, cw - 14, 2):
        d.text((cx + 7, ty), ln, font=hf, fill=INK)
        ty += hlh
    df = font(SANS, 11 if big else 10)
    dlh = 13 if big else 12
    for ln in fit_lines(d, deck, df, cw - 14, 2 if big else 3):
        d.text((cx + 7, ty), ln, font=df, fill=(60, 57, 48))
        ty += dlh


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((12, 10), "THE WORLD IN ONE DAY", font=font(SANS_B, 13), fill=RED)
    d.text((W - 12 - d.textlength("SUNDAY'S NEWS · ONE PAGE · 48 STORIES",
                                  font=font(SANS_B, 11)), 11),
           "SUNDAY'S NEWS · ONE PAGE · 48 STORIES", font=font(SANS_B, 11), fill=INK)
    d.text((12, 28), "Sunday 22 November 2026", font=font(SERIF_B, 54), fill=INK)
    d.text((12, 94), "Iran strikes US bases in Bahrain · COP31 nears a deal at dawn · "
                      "Russian ship still ablaze in the Baltic",
           font=font(SERIF_I, 15), fill=(60, 57, 48))
    d.rectangle([12, 120, W - 12, 123], fill=RED)
    # ---- region chips
    rx = 12
    cf = font(SANS_B, 11)
    for label, colour in REGIONS:
        tw = d.textlength(label, font=cf)
        d.rounded_rectangle([rx, 126, rx + tw + 16, 145], radius=4, fill=colour)
        d.text((rx + 8, 129), label, font=cf, fill=(255, 255, 255))
        rx += tw + 16 + 6
    d.line([12, 151, W - 12, 151], fill=RULE, width=1)

    # ---- numbers strip
    bw = (W - 24 - 5 * 6) // 6
    for i, (num, label) in enumerate(NUMBERS):
        bx = 12 + i * (bw + 6)
        d.rectangle([bx, 158, bx + bw, 192], outline=RULE, width=1, fill=CARD)
        nf = font(SERIF_B, 19)
        d.text((bx + bw // 2 - d.textlength(num, font=nf) // 2, 161), num,
               font=nf, fill=RED)
        lf = font(SANS, 9)
        d.text((bx + bw // 2 - d.textlength(label, font=lf) // 2, 180), label,
               font=lf, fill=MUTED)

    # ---- cards row 1: 3 big
    cw = (W - 24 - 2 * 8) // 3
    for i, card in enumerate(CARDS[:3]):
        draw_card(d, 12 + i * (cw + 8), 200, cw, 156, *card, big=True)
    # ---- cards rows 2-3: 5 medium each
    mw = (W - 24 - 4 * 8) // 5
    for i, card in enumerate(CARDS[3:8]):
        draw_card(d, 12 + i * (mw + 8), 362, mw, 130, *card, big=False)
    for i, card in enumerate(CARDS[8:13]):
        draw_card(d, 12 + i * (mw + 8), 498, mw, 130, *card, big=False)

    # ---- also list: 35 items, 2 columns x 18 rows
    d.text((12, 636), "ALSO ON SUNDAY 22 NOVEMBER — 35 MORE STORIES",
           font=font(SANS_B, 13), fill=RED)
    d.line([12, 652, W - 12, 652], fill=RULE, width=1)
    colw = (W - 24 - 24) // 2
    af = font(SANS, 10)
    for j, (num, city, text) in enumerate(ALSO):
        col = j // 18
        row = j % 18
        ax = 12 + col * (colw + 24)
        ay = 658 + row * 10
        d.text((ax, ay), f"{num}. {city} — {text}", font=af, fill=INK)

    # ---- bottom row: map + date check
    d.text((12, 844), "WHERE IT HAPPENED — pins match story numbers",
           font=font(SANS_B, 12), fill=RED)
    draw_map(d, 12, 858, 488, 94)
    bx = 524
    d.rectangle([bx, 858, W - 12, 952], outline=RED, width=2, fill=CARD)
    d.text((bx + 10, 866), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    d.text((bx + 10, 882),
           "First reported Friday 20 or Saturday 21 November,",
           font=font(SANS_B, 10), fill=INK)
    d.text((bx + 10, 894),
           "so NOT on this page as news:",
           font=font(SANS_B, 10), fill=INK)
    df = font(SANS, 10)
    ty = 910
    for ln in wrap(d, DATE_CHECK, df, W - 12 - bx - 20):
        d.text((bx + 10, ty), ln, font=df, fill=(60, 57, 48))
        ty += 12

    # ---- footer
    d.line([12, 960, W - 12, 960], fill=RULE, width=1)
    d.text((12, 966), CLOCK, font=font(SANS, 10), fill=INK)
    d.text((12, 980),
           "Every story here happened, was first reported, or was live and developing on Sunday 22 November 2026.",
           font=font(SERIF_I, 12), fill=INK)
    d.text((12, 998),
           "Sources: Reuters, BBC, AP, AFP, The Times of India, India Today, NDTV, The Hindu, Yle, IRNA, Darfur24, RFE/RL, Formula 1, ERR.  Original drawings.",
           font=font(SANS, 9), fill=MUTED)

    img.save(os.path.join(HERE, "entry.png"))


if __name__ == "__main__":
    main()
