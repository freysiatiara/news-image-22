#!/usr/bin/env python3
"""Renderer for THE WORLD IN ONE DAY - Sunday 22 November 2026. Round 5.

Draws a one-image broadsheet (1024x1024) with Pillow: masthead, region
chips, a numbers strip, 13 illustrated cards, a 22-item second list, a
quote strip, a dotted world locator map with numbered pins, a UTC clock
line and a DATE CHECK box. 35 stories in all, across 6 regions. Every
story on the page happened, was first reported, or was live and developing
on Sunday 22 November 2026; Friday's and Saturday's big stories are listed
in DATE CHECK instead. All art is flat shapes drawn here.

Round 5 vs round 4 (59 stories, dev 0.977797, rank 228): FEWER stories,
sharper ones. Round 3 (48 stories, 0.982336) beat round 4 (59 stories),
so the count drops to 35 -- the 27-38 band the top of the board lives in --
with every story re-verified today: the overnight drone raid is 186, not
400 (that was Friday's barrage); the COP31 text was tabled for a dawn
vote, not adopted; the Bahrain strikes were Saturday night, so the page
leads with Sunday's aftermath (Bahrain's demand for accountability) and
keeps the strike itself honest; Denmark/Estonia and the EU-Indonesia deal
were Friday/Saturday, so they move to DATE CHECK. New this round: a quote
strip (COP31 president Kurum on consensus), a ballot-box card for the Hong
Kong vote, a tennis card for the Turin final, and a bigger, airier second
list.
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


def scene_drones(d, x, y, w, h):
    """Night sky full of drones, air-defence bursts below."""
    d.rectangle([x, y, x + w, y + h], fill=(20, 26, 48))
    for sx, sy in ((18, 10), (60, 22), (110, 8), (160, 18), (40, 34),
                   (140, 30), (190, 12), (90, 26)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(240, 238, 225))
    # drone silhouettes with red running lights
    for dx, dy, s in ((30, 22, 1), (95, 20, 1), (150, 26, 1), (60, 30, 0),
                      (180, 34, 0), (120, 32, 0)):
        k = 10 if s else 7
        d.rectangle([x + dx, y + dy, x + dx + k, y + dy + 3], fill=(200, 200, 200))
        d.rectangle([x + dx - 3, y + dy - 2, x + dx + k + 3, y + dy], fill=(160, 160, 160))
        d.ellipse([x + dx + k // 2 - 1, y + dy + 1, x + dx + k // 2 + 2, y + dy + 4],
                  fill=RED)
    # interception bursts, kept inside the scene
    for bx, by in ((55, 42), (130, 40), (185, 42)):
        d.ellipse([x + bx - 5, y + by - 5, x + bx + 5, y + by + 5], fill=(250, 200, 60))
        d.ellipse([x + bx - 2, y + by - 2, x + bx + 2, y + by + 2], fill=(250, 240, 200))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(52, 44, 40))


def scene_ballot(d, x, y, w, h):
    """Ballot box with a paper slip and a tick."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 222))
    d.rectangle([x + 18, y + h - 30, x + w - 18, y + h - 8], fill=NAVY)
    d.rectangle([x + 18, y + h - 38, x + w - 18, y + h - 30], fill=(240, 238, 225),
                outline=NAVY, width=2)
    d.rectangle([x + w // 2 - 16, y + h - 36, x + w // 2 + 16, y + h - 32], fill=INK)
    # ballot slip, drawn first so the lid overlaps its foot
    d.rectangle([x + w // 2 - 22, y + 4, x + w // 2 + 22, y + h - 36],
                fill=(240, 238, 225), outline=INK, width=1)
    d.line([x + w // 2 - 16, y + 10, x + w // 2 + 16, y + 10], fill=MUTED, width=1)
    d.line([x + w // 2 - 16, y + 16, x + w // 2 + 16, y + 16], fill=MUTED, width=1)
    d.line([x + w - 52, y + h - 26, x + w - 42, y + h - 16, x + w - 22, y + h - 34],
           fill=GREEN, width=4)


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


def scene_tennis(d, x, y, w, h):
    """Indoor hard court at night: net, ball, floodlights."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 92, 120))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(30, 70, 95))
    d.rectangle([x + 14, y + 10, x + w - 14, y + h - 26], fill=(58, 120, 140))
    d.line([x + w // 2, y + 10, x + w // 2, y + h - 26], fill=(240, 238, 225), width=2)
    d.line([x + 14, y + h // 2, x + w - 14, y + h // 2], fill=(240, 238, 225), width=2)
    d.rectangle([x + 10, y + h // 2 - 8, x + w - 10, y + h // 2 + 8],
                fill=(240, 238, 225), outline=INK, width=1)
    d.line([x + 10, y + h // 2 - 4, x + w - 10, y + h // 2 - 4], fill=INK, width=1)
    d.ellipse([x + w // 2 + 26, y + h - 44, x + w // 2 + 40, y + h - 30],
              fill=(200, 230, 60), outline=(240, 238, 225), width=1)
    d.ellipse([x + 22, y + 16, x + 32, y + 26], fill=(250, 240, 200))
    d.ellipse([x + w - 34, y + 18, x + w - 24, y + 28], fill=(250, 240, 200))
    d.text((x + 10, y + h - 22), "TURIN", font=font(SANS_B, 10), fill=(240, 238, 225))


def scene_street(d, x, y, w, h):
    """City street after a firefight: shuttered shops, police tape."""
    d.rectangle([x, y, x + w, y + h], fill=(120, 110, 100))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(70, 66, 60))
    for bx, col in ((x + 10, (150, 120, 90)), (x + w // 2 - 26, (170, 140, 100)),
                    (x + w - 62, (140, 110, 85))):
        d.rectangle([bx, y + 8, bx + 52, y + h - 16], fill=col)
        d.rectangle([bx + 8, y + 18, bx + 20, y + 30], fill=(240, 238, 225))
        d.rectangle([bx + 30, y + 18, bx + 42, y + 30], fill=(240, 238, 225))
        d.rectangle([bx + 14, y + h - 40, bx + 38, y + h - 16], fill=(90, 70, 50))
    d.polygon([(x, y + h - 34), (x + w, y + h - 26), (x + w, y + h - 18),
               (x, y + h - 26)], fill=(250, 200, 60))
    d.text((x + 12, y + h - 33), "POLICE", font=font(SANS_B, 9), fill=INK)


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


def scene_tree(d, x, y, w, h):
    """Spruce in a snowy Norwegian forest, ready for London."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 50, 44))
    for sx, sy in ((16, 12), (60, 8), (120, 14), (170, 10), (40, 30), (150, 28)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(240, 238, 225))
    cx = x + w // 2
    d.polygon([(cx - 34, y + h - 22), (cx, y + 6), (cx + 34, y + h - 22)],
              fill=(40, 110, 60))
    d.polygon([(cx - 24, y + h - 34), (cx, y + 14), (cx + 24, y + h - 34)],
              fill=(52, 130, 70))
    d.rectangle([cx - 5, y + h - 22, cx + 5, y + h - 10], fill=(120, 90, 60))
    d.polygon([(cx - 40, y + h - 22), (cx - 34, y + h - 28), (cx - 28, y + h - 22)],
              fill=(240, 238, 225))
    d.polygon([(cx + 28, y + h - 22), (cx + 34, y + h - 28), (cx + 40, y + h - 22)],
              fill=(240, 238, 225))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(240, 238, 225))
    d.text((x + 10, y + h - 26), "OSLO", font=font(SANS_B, 10), fill=(240, 238, 225))


SCENES = {1: scene_missile, 2: scene_cop31, 3: scene_shipfire, 4: scene_drones,
          5: scene_ballot, 6: scene_fire, 7: scene_river, 8: scene_tennis,
          9: scene_street, 10: scene_talks, 11: scene_cricket, 12: scene_f1,
          13: scene_tree}

CARDS = [
    (1, "BAHRAIN · IRAN WAR", "Iran strikes US bases in Bahrain",
     "IRGC missiles and drones hit Patriot radars at Al-Riffa and Awali; Bahrain says a civilian site burned. (Reuters)"),
    (2, "ANTALYA · CLIMATE", "COP31 tables final text for dawn vote",
     "Ten pages, 94 paragraphs, no mention of fossil fuels; approval session 06:00 GMT, deal in the balance. (Reuters)"),
    (3, "GULF OF FINLAND · UKRAINE WAR", "Russian ship still ablaze in the Baltic",
     "Sparta II burns on at anchor off Finland; 16 crew evacuated, fire may rage for days. (Reuters, Yle)"),
    (4, "UKRAINE · DRONE WAR", "186 drones in one night over Ukraine",
     "Air defences down 161 by 08:00, 56 of 72 jet-powered Shaheds; impacts at 18 sites. (Ukrainian Air Force)"),
    (5, "HONG KONG · VOTE", "Hong Kong votes for its Election Committee",
     "856 candidates chase 723 seats; turnout 95.6% by 3pm, polls open 9am-6pm. (China Daily)"),
    (6, "CIKANDE · DISASTER", "Rescuers hunt 36 missing after factory fire",
     "Three dead at the Milkita candy plant; 15 survived, four in hospital. (Reuters)"),
    (7, "BAYELSA · DISASTER", "Boat toll rises to 24 in Nigeria",
     "Funeral-bound boat capsized Friday; 24 bodies found, 24 survivors rescued. (Reuters, NEMA)"),
    (8, "TURIN · TENNIS", "Alcaraz meets Zverev for the ATP crown",
     "World No. 1 Zverev, twice a champion, faces Alcaraz, on a 13-match win streak. (ATP)"),
    (9, "SINALOA · CARTELS", "11 killed in violence after cartel boss held",
     "'El Chapo Isidro' flown to Mexico City after a firefight; four soldiers among the dead. (AP)"),
    (10, "OTTAWA · ALLIES", "Canada seeks clarity on Hegseth memo",
     "US curbs on military contacts with Ottawa; Pentagon says NORAD untouched. (Washington Post)"),
    (11, "WELLINGTON · CRICKET", "Pant's 128 puts India 629/6 on day four",
     "Rahul's 136 and Pant's century build a 261-run lead over New Zealand at lunch in the first Test."),
    (12, "NEW YORK · GAMES", "GTA 6 launch day put at $3.79bn",
     "Record debut estimate for Rockstar's open-world sequel; players hunt its secrets."),
    (13, "LONDON · TRADITION", "Trafalgar's tree felled in Norway",
     "The 69-foot spruce, 'Jolly Cheery', cut outside Oslo for 80 years of thanks to London."),
]

ALSO = [
    (14, "MANAMA", "Bahrain demands Iran pay for civilian site hit."),
    (15, "ANTALYA", "35% electricity by 2035; $120bn target dropped."),
    (16, "KYIV", "72 jet Shaheds in raid; 56 of them intercepted."),
    (17, "HELSINKI", "Sparta II fire may burn for days, Finns warn."),
    (18, "GUASAVE", "Cartel boss flown to Mexico City after firefight."),
    (19, "HONG KONG", "Turnout 95.6% by 3pm in committee vote."),
    (20, "JAKARTA", "15 survived factory fire; four in hospital."),
    (21, "TURIN", "$5.17m for the undefeated ATP champion."),
    (22, "BEIRUT", "Aoun blames Israel and Iran for threats."),
    (23, "LONDON", "UK opinion turning against Brexit, polls say."),
    (24, "CAMBRIDGE", "Lean certifies AI-built Riemann proof."),
    (25, "WASHINGTON", "Trump: firms must report Congress requests."),
    (26, "FLORIDA", "St. Johns breaks 73-year flood record."),
    (27, "NEW DELHI", "JEE Main 2027 registration closes today."),
    (28, "MANILA", "Quad, ASEAN-India, East Asia summits meet."),
    (29, "NEW DELHI", "India-Japan expand defence pact."),
    (30, "PATNA", "Modi opens Nitish Setu bridge."),
    (31, "NEW DELHI", "India passes 1 crore HPV vaccine doses."),
    (32, "ACCRA", "Ghana launches 'Heritage Series' banknotes."),
    (33, "MOGADISHU", "Al-Shabaab claims hundreds killed in ambush."),
    (34, "MELBOURNE", "70 years since the 1956 Olympics opened."),
    (35, "ABUJA", "Nigeria starts building its own warships."),
]

NUMBERS = [
    ("186", "drones launched at Ukraine"),
    ("161", "drones downed or suppressed"),
    ("24", "dead in Nigeria boat disaster"),
    ("36", "missing in Cikande factory fire"),
    ("06:00", "GMT COP31 approval session"),
    ("35%", "electricity share by 2035"),
]

REGIONS = [
    ("EUROPE 11", NAVY),
    ("ASIA-PACIFIC 9", OCHRE),
    ("AMERICAS 6", PLUM),
    ("AFRICA 4", GREEN),
    ("MIDDLE EAST 3", RUST),
    ("OCEANIA 2", TEAL),
]

QUOTE = ("\u201cWhile no one obtained everything they might have desired, "
         "everyone can find a place for themselves within this text \u2014 "
         "that is the very essence of consensus.\u201d")
QUOTE_BY = "COP31 President Murat Kurum, Antalya, on the final text"

DATE_CHECK = ("400-drone barrage \u2014 20 Nov \u00b7 Missiles in Poland \u2014 "
              "19 Nov \u00b7 Peru quake \u2014 20 Nov \u00b7 \u2018El Chapo "
              "Isidro\u2019 captured \u2014 20 Nov \u00b7 Gaza aid van \u2014 "
              "21 Nov \u00b7 EU\u2013Indonesia deal \u2014 21 Nov \u00b7 "
              "Denmark expels attach\u00e9 \u2014 20 Nov \u00b7 FBI NCIC hack "
              "\u2014 21 Nov \u00b7 Hartha fire \u2014 21 Nov")

CLOCK = ("BY THE CLOCK \u2014 UTC: Sun ~02:00 COP31 final text tabled \u00b7 "
         "03:00 objections close \u00b7 06:00 approval session \u00b7 08:00 "
         "Ukraine: 161 drones downed \u00b7 09:00 Hong Kong polls open \u00b7 "
         "18:00 ATP final in Turin")

# (card no, lat, lon) -- nudged apart so neighbouring pins stay readable
PINS = [(1, 26.0, 50.0), (2, 39.0, 28.0), (3, 62.0, 20.0), (4, 50.0, 31.0),
        (5, 22.3, 114.2), (6, -6.2, 106.2), (7, 4.5, 6.0), (8, 45.1, 7.7),
        (9, 25.6, -108.5), (10, 45.4, -75.7), (11, -41.3, 174.8),
        (12, 40.7, -74.0), (13, 51.5, -0.1)]

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
    d.text((cx + 7, ty), f"{num} \u00b7 {kicker}", font=kf, fill=RED)
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
    d.text((W - 12 - d.textlength("SUNDAY'S NEWS \u00b7 ONE PAGE \u00b7 35 STORIES",
                                  font=font(SANS_B, 11)), 11),
           "SUNDAY'S NEWS \u00b7 ONE PAGE \u00b7 35 STORIES", font=font(SANS_B, 11), fill=INK)
    d.text((12, 28), "Sunday 22 November 2026", font=font(SERIF_B, 54), fill=INK)
    d.text((12, 94), "Iran strikes US bases in Bahrain \u00b7 COP31 tables final text for dawn vote \u00b7 "
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

    # ---- also list: 22 items, 3 columns x 8 rows
    d.text((12, 640), "ALSO ON SUNDAY 22 NOVEMBER \u2014 22 MORE STORIES",
           font=font(SANS_B, 13), fill=RED)
    d.line([12, 656, W - 12, 656], fill=RULE, width=1)
    colw = (W - 24 - 2 * 16) // 3
    af = font(SANS, 11)
    for j, (num, city, text) in enumerate(ALSO):
        col = j // 8
        row = j % 8
        ax = 12 + col * (colw + 16)
        ay = 662 + row * 14
        d.text((ax, ay), f"{num}. {city} \u2014 {text}", font=af, fill=INK)

    # ---- quote strip
    qy = 782
    d.rectangle([12, qy, W - 12, qy + 56], outline=RULE, width=1, fill=CARD)
    d.text((24, qy + 6), "IN THEIR WORDS", font=font(SANS_B, 10), fill=RED)
    qf = font(SERIF_I, 13)
    for i, ln in enumerate(wrap(d, QUOTE, qf, W - 48)):
        d.text((24, qy + 20 + i * 15), ln, font=qf, fill=INK)
    d.text((W - 24 - d.textlength(QUOTE_BY, font=font(SANS, 10)), qy + 40),
           QUOTE_BY, font=font(SANS, 10), fill=MUTED)

    # ---- bottom row: map + date check
    d.text((12, 844), "WHERE IT HAPPENED \u2014 pins match story numbers",
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
    ty = 908
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
           "Sources: Reuters, AP, AFP, China Daily, The Hindu, Yle, Ukrainian Air Force, ATP, Washington Post.  Original drawings.",
           font=font(SANS, 9), fill=MUTED)

    img.save(os.path.join(HERE, "entry.png"))


if __name__ == "__main__":
    main()
