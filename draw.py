#!/usr/bin/env python3
"""Renderer for THE WORLD IN ONE DAY - Sunday 22 November 2026. Round 2.

Draws a one-image broadsheet (1024x1024) with Pillow: masthead, region
chips, a numbers strip, 13 illustrated cards, a 27-item second list, a
world locator map and a DATE CHECK box. 40 stories in all, across 7
regions. Every story on the page happened, or was first reported, on
Sunday 22 November 2026; Friday's and Saturday's big stories are listed
in DATE CHECK instead. All art is flat shapes drawn here.

Round 2 vs round 1: the leads are the day's hard news, verified this
morning -- Iran's strikes on the US bases in Bahrain, the COP31 text
tabled overnight for a dawn approval, the burning Sparta II still
ablaze in the Baltic -- instead of round 1's cricket-led page; the
India-heavy skew is gone (Asia-Pacific 12 of 40, not 20 of 32); seven
new illustrated scenes; 40 stories, up from 32.
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
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(60, 60, 66))
    d.line([x, y + h - 22, x + w, y + h - 22], fill=(250, 220, 90), width=2)
    d.rectangle([x + w // 2 - 44, y + h - 40, x + w // 2 + 44, y + h - 30],
                fill=(178, 30, 30))
    d.polygon([(x + w // 2 - 46, y + h - 34), (x + w // 2 - 34, y + h - 40),
               (x + w // 2 - 34, y + h - 30)], fill=(120, 20, 20))
    d.polygon([(x + w // 2 - 10, y + h - 48), (x + w // 2 + 16, y + h - 48),
               (x + w // 2 + 10, y + h - 40), (x + w // 2 - 6, y + h - 40)],
              fill=(120, 20, 20))
    d.ellipse([x + w // 2 - 34, y + h - 30, x + w // 2 - 18, y + h - 14],
              fill=INK)
    d.ellipse([x + w // 2 + 18, y + h - 30, x + w // 2 + 34, y + h - 14],
              fill=INK)
    d.rectangle([x + w // 2 + 44, y + h - 42, x + w // 2 + 52, y + h - 30],
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
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(40, 32, 56))
    d.polygon([(x + w // 2 - 6, y + 8), (x + w // 2 + 6, y + 8),
               (x + w // 2 + 16, y + h - 18), (x + w // 2 - 16, y + h - 18)],
              fill=(30, 30, 30))
    d.line([x + w // 2 - 22, y + 22, x + w // 2 + 22, y + 22], fill=(30, 30, 30),
           width=4)
    d.line([x + w // 2 - 16, y + 36, x + w // 2 + 16, y + 36], fill=(30, 30, 30),
           width=3)
    d.line([x, y + 26, x + w // 2 - 20, y + 34], fill=(30, 30, 30), width=2)
    d.line([x + w // 2 + 20, y + 34, x + w, y + 26], fill=(30, 30, 30), width=2)
    d.ellipse([x + w - 30, y + 8, x + w - 14, y + 24], fill=(250, 200, 90))
    for bx in (x + 12, x + w - 44):
        d.rectangle([bx, y + h - 34, bx + 26, y + h - 18], fill=(52, 44, 40))
        d.rectangle([bx + 8, y + h - 28, bx + 14, y + h - 22], fill=(250, 200, 60))
    d.rectangle([x + w // 2 - 30, y + h - 40, x + w // 2 + 30, y + h - 30],
                fill=(240, 238, 225))
    d.text((x + w // 2 - 26, y + h - 39), "2 hrs", font=font(SANS_B, 9), fill=RED)


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


def scene_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    b1, b2, b3 = h // 4, h // 2, 3 * h // 4
    d.rectangle([x + 14, y + 10, x + w // 2 - 6, y + h - 10], fill=(255, 255, 255))
    d.rectangle([x + 14, y + 10, x + w // 2 - 6, y + 10 + b1], fill=(255, 153, 51))
    d.rectangle([x + 14, y + h - 10 - b1, x + w // 2 - 6, y + h - 10], fill=(19, 136, 8))
    d.ellipse([x + w // 4 - 6, y + h // 2 - 6, x + w // 4 + 6, y + h // 2 + 6],
              outline=(0, 0, 128), width=2)
    d.rectangle([x + w // 2 + 6, y + 10, x + w - 14, y + h - 10], fill=(255, 255, 255))
    d.rectangle([x + w // 2 + 6, y + 10 + b1, x + w - 14, y + 10 + b2], fill=(0, 122, 90))
    d.rectangle([x + w // 2 + 6, y + 10 + b2, x + w - 14, y + h - 10], fill=(214, 40, 40))


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


def scene_book(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 222, 190))
    d.polygon([(x + 14, y + 14), (x + w // 2, y + 24), (x + w // 2, y + h - 14),
               (x + 14, y + h - 14)], fill=(252, 250, 243))
    d.polygon([(x + w - 14, y + 14), (x + w // 2, y + 24), (x + w // 2, y + h - 14),
               (x + w - 14, y + h - 14)], fill=(240, 236, 222))
    for i, yy in enumerate((y + 30, y + 42, y + 54)):
        d.line([x + 22, yy, x + w // 2 - 8, yy + 3], fill=MUTED, width=2)
        d.line([x + w // 2 + 8, yy + 3, x + w - 22, yy], fill=MUTED, width=2)
    d.rectangle([x + w // 2 - 2, y + 22, x + w // 2 + 2, y + h - 14], fill=RED)


SCENES = {1: scene_missile, 2: scene_cop31, 3: scene_shipfire, 4: scene_f1,
          5: scene_mine, 6: scene_pylon, 7: scene_cricket, 8: scene_talks,
          9: scene_grounded, 10: scene_fire, 11: scene_river, 12: scene_flags,
          13: scene_book}

CARDS = [
    (1, "BAHRAIN · IRAN WAR", "Iran strikes US bases in Bahrain",
     "IRGC missiles and drones hit Patriot radars at Al-Riffa and Awali; a civilian site burns, no injuries. (Reuters, IRNA)"),
    (2, "ANTALYA · CLIMATE", "COP31 nears a deal at dawn",
     "New text tabled overnight; objections close 03:00 GMT, approval session at 06:00 GMT. (Reuters)"),
    (3, "GULF OF FINLAND · UKRAINE WAR", "Russian ship ablaze in the Baltic",
     "Sparta II, a sanctioned military-linked cargo ship, burns after a drone strike; 16 crew evacuated. (Reuters, Yle)"),
    (4, "LAS VEGAS · FORMULA 1", "Verstappen on pole as Vegas races under the lights",
     "Antonelli drops five places; the 50-lap race starts 04:00 GMT on Sunday. (Formula 1)"),
    (5, "N. KORDOFAN · SUDAN WAR", "Landmine kills 22 on a road to El-Obeid",
     "Civilians travelling to the city are killed in a blast on Um Arada road; monitors blame a paramilitary mine. (Darfur24)"),
    (6, "TEHRAN · ENERGY", "Iran begins rationing electricity from Sunday",
     "Cuts of up to two hours a day as gas output lags and war damage bites. (RFE/RL)"),
    (7, "WELLINGTON · CRICKET", "Pant's 128 puts India 629/6 on day four",
     "Rahul's 136 and Pant's century build a 261-run lead over New Zealand at lunch in the first Test."),
    (8, "JERUSALEM · POLITICS", "Eisenkot–Likud marathon talks open today",
     "Yashar invites Netanyahu's party to intensive talks after Saturday's invite; the mandate ends on 6 December."),
    (9, "BRUSSELS · LABOUR", "Belgian national strike to ground flights on Monday",
     "No regular air traffic 07:00–21:00, Skeyes says; trains and ports hit too. (AFP)"),
    (10, "DHAKA · POLITICS", "30 Awami League houses torched",
     "At least 30 houses of Awami League members are set on fire in Bangladesh."),
    (11, "DHAKA · RIVERS", "Ganges treaty talks open today",
     "Bangladesh and India meet on the shared-river treaty as the 1996 pact nears its end."),
    (12, "NEW DELHI · DIPLOMACY", "Jaishankar meets Bulgaria on EU trade deal",
     "The foreign minister discusses the India-EU free trade pact and Black Sea ties with Sofia."),
    (13, "CHENNAI · BOOKS", "Chennai book fair set for 16–18 January",
     "The Chennai International Book Fair returns in January, with the dates announced today."),
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
]

NUMBERS = [
    ("2", "US bases hit in Bahrain"),
    ("200", "nations at COP31"),
    ("16", "crew off burning Sparta II"),
    ("22", "killed by Sudan landmine"),
    ("06:00", "GMT COP31 approval session"),
    ("04:00", "GMT Vegas lights out"),
]

REGIONS = [
    ("EUROPE 8", NAVY),
    ("MIDDLE EAST 7", RUST),
    ("ASIA-PACIFIC 12", OCHRE),
    ("AMERICAS 6", PLUM),
    ("AFRICA 3", GREEN),
    ("OCEANIA 2", TEAL),
    ("WORLD 2", (110, 110, 110)),
]

DATE_CHECK = ("Russia's 400-drone, 110-missile barrage — 20 Nov · Missiles land in "
              "Poland — 20 Nov · Peru quake — 20 Nov · 'El Chapo Isidro' captured "
              "— 20 Nov, announced 21 Nov · Gaza aid van hit — 21 Nov · Rutte in "
              "Warsaw — 21 Nov · Kuwait base hit — 19 Nov · Hormuz tanker hit — "
              "20 Nov")

# (card no, lat, lon)
PINS = [(1, 26.2, 50.6), (2, 36.9, 30.7), (3, 60.0, 27.5), (4, 36.2, -115.1),
        (5, 13.2, 30.2), (6, 35.7, 51.4), (7, -41.3, 174.8), (8, 31.8, 35.2),
        (9, 50.8, 4.4), (10, 23.8, 90.4), (11, 23.3, 89.9), (12, 28.6, 77.2),
        (13, 13.1, 80.3)]

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


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h) for lon, lat in poly]
        d.polygon(pts, fill=SAND)
    for num, lat, lon in PINS:
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px - 3, py - 6), str(num), font=font(SANS_B, 9), fill=(255, 255, 255))


def draw_card(d, cx, cy, cw, ch, num, kicker, headline, deck, big):
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD, outline=RULE, width=1)
    ih = 82 if big else 54
    SCENES[num](d, cx + 1, cy + 1, cw - 2, ih)
    ty = cy + ih + 5
    kf = font(SANS_B, 10 if big else 9)
    d.text((cx + 7, ty), f"{num} · {kicker}", font=kf, fill=RED)
    ty += 15 if big else 13
    hf = font(SERIF_B, 17 if big else 13)
    hlh = 19 if big else 14
    for ln in fit_lines(d, headline, hf, cw - 14, 2):
        d.text((cx + 7, ty), ln, font=hf, fill=INK)
        ty += hlh
    df = font(SANS, 11 if big else 10)
    dlh = 14 if big else 12
    for ln in fit_lines(d, deck, df, cw - 14, 3 if not big else 2):
        d.text((cx + 7, ty), ln, font=df, fill=(60, 57, 48))
        ty += dlh


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((12, 10), "THE WORLD IN ONE DAY", font=font(SANS_B, 13), fill=RED)
    d.text((W - 12 - d.textlength("SUNDAY'S NEWS · ONE PAGE · 40 STORIES",
                                  font=font(SANS_B, 11)), 11),
           "SUNDAY'S NEWS · ONE PAGE · 40 STORIES", font=font(SANS_B, 11), fill=INK)
    d.text((12, 28), "Sunday 22 November 2026", font=font(SERIF_B, 54), fill=INK)
    d.text((12, 96), "Iran strikes US bases in Bahrain · COP31 nears a deal at dawn · "
                      "Burning Russian ship still ablaze in the Baltic",
           font=font(SERIF_I, 15), fill=(60, 57, 48))
    d.rectangle([12, 122, W - 12, 125], fill=RED)
    # ---- region chips
    rx = 12
    cf = font(SANS_B, 11)
    for label, colour in REGIONS:
        tw = d.textlength(label, font=cf)
        d.rounded_rectangle([rx, 131, rx + tw + 16, 150], radius=4, fill=colour)
        d.text((rx + 8, 134), label, font=cf, fill=(255, 255, 255))
        rx += tw + 16 + 6
    d.line([12, 156, W - 12, 156], fill=RULE, width=1)

    # ---- numbers strip
    bw = (W - 24 - 5 * 6) // 6
    for i, (num, label) in enumerate(NUMBERS):
        bx = 12 + i * (bw + 6)
        d.rectangle([bx, 164, bx + bw, 204], outline=RULE, width=1, fill=CARD)
        nf = font(SERIF_B, 21)
        d.text((bx + bw // 2 - d.textlength(num, font=nf) // 2, 167), num,
               font=nf, fill=RED)
        lf = font(SANS, 9)
        d.text((bx + bw // 2 - d.textlength(label, font=lf) // 2, 191), label,
               font=lf, fill=MUTED)

    # ---- cards row 1: 3 big
    cw = (W - 24 - 2 * 8) // 3
    for i, card in enumerate(CARDS[:3]):
        draw_card(d, 12 + i * (cw + 8), 212, cw, 158, *card, big=True)
    # ---- cards rows 2-3: 5 medium each
    mw = (W - 24 - 4 * 8) // 5
    for i, card in enumerate(CARDS[3:8]):
        draw_card(d, 12 + i * (mw + 8), 378, mw, 138, *card, big=False)
    for i, card in enumerate(CARDS[8:13]):
        draw_card(d, 12 + i * (mw + 8), 524, mw, 138, *card, big=False)

    # ---- also list: 27 items, 2 columns x 14 rows
    d.text((12, 670), "ALSO ON SUNDAY 22 NOVEMBER — 27 MORE STORIES",
           font=font(SANS_B, 13), fill=RED)
    d.line([12, 688, W - 12, 688], fill=RULE, width=1)
    colw = (W - 24 - 24) // 2
    af = font(SANS, 10)
    for j, (num, city, text) in enumerate(ALSO):
        col = j // 14
        row = j % 14
        ax = 12 + col * (colw + 24)
        ay = 694 + row * 10
        d.text((ax, ay), f"{num}. {city} — {text}", font=af, fill=INK)

    # ---- bottom row: map + date check
    d.text((12, 838), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    draw_map(d, 12, 854, 488, 100)
    d.text((12, 958), "Each number is its story on this page.",
           font=font(SANS, 9), fill=MUTED)
    bx = 524
    d.rectangle([bx, 854, W - 12, 962], outline=RED, width=2, fill=CARD)
    d.text((bx + 10, 862), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    d.text((bx + 10, 878),
           "First reported Saturday 21 November (or earlier),",
           font=font(SANS_B, 10), fill=INK)
    d.text((bx + 10, 890),
           "so NOT on this page as news:",
           font=font(SANS_B, 10), fill=INK)
    df = font(SANS, 10)
    ty = 906
    for ln in wrap(d, DATE_CHECK, df, W - 12 - bx - 20):
        d.text((bx + 10, ty), ln, font=df, fill=(60, 57, 48))
        ty += 12

    # ---- footer
    d.line([12, 972, W - 12, 972], fill=RULE, width=1)
    d.text((12, 978),
           "Every story here happened, or was first reported, on Sunday 22 November 2026.",
           font=font(SERIF_I, 12), fill=INK)
    d.text((12, 996),
           "Sources: Reuters, BBC, AP, AFP, The Times of India, India Today, NDTV, The Hindu, Yle, IRNA.  Original drawings.",
           font=font(SANS, 9), fill=MUTED)

    img.save(os.path.join(HERE, "entry.png"))


if __name__ == "__main__":
    main()
