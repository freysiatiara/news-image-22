#!/usr/bin/env python3
"""Renderer for THE WORLD IN ONE DAY - Sunday 22 November 2026.

Draws a one-image broadsheet (1024x1024) with Pillow: masthead, region
counts, a numbers strip, 13 illustrated cards, a 19-item second list, a
world locator map and a DATE CHECK box. Every story on the page happened,
or was first reported, on Sunday 22 November 2026; Saturday's big stories
are listed in DATE CHECK instead. All art is flat shapes drawn here.
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
def scene_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    r = min(30, h // 2 - 4)
    cx, cy = x + w // 2, y + h // 2 - 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 238, 225))
    d.ellipse([cx - r + 6, cy - r + 6, cx - 2, cy - 2], fill=GREEN)
    d.ellipse([cx, cy + 2, cx + r - 6, cy + r - 6], fill=GREEN)
    d.ellipse([x + 12, y + 8, x + 28, y + 24], fill=(240, 200, 90))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(30, 56, 92))
    for i in range(5):
        d.rectangle([x + 12 + i * 16, y + h - 7, x + 20 + i * 16, y + h - 2],
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


def scene_stage(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 32, 56))
    d.polygon([(x + 10, y + 10), (x + 30, y + 10), (x + w // 2, y + 40)], fill=(250, 220, 90))
    d.polygon([(x + w - 10, y + 10), (x + w - 30, y + 10), (x + w // 2, y + 40)],
              fill=(250, 220, 90))
    d.rectangle([x + 12, y + h - 18, x + w - 12, y + h - 8], fill=(120, 96, 60))
    d.ellipse([x + w // 2 - 7, y + 34, x + w // 2 + 7, y + 48], fill=(240, 238, 225))
    d.rectangle([x + w // 2 - 2, y + 48, x + w // 2 + 2, max(y + 49, y + h - 18)],
                fill=(200, 200, 200))
    d.ellipse([x + 18, y + 16, x + 26, y + 24], fill=(240, 120, 120))
    d.ellipse([x + w - 26, y + 22, x + w - 18, y + 30], fill=(120, 200, 240))


def scene_camera(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 170, 140))
    d.rectangle([x + 16, y + 18, x + w - 16, y + h - 10], fill=(52, 52, 52))
    r = min(16, h // 2 - 12)
    d.ellipse([x + w // 2 - r, y + h // 2 - r, x + w // 2 + r, y + h // 2 + r],
              fill=(120, 150, 180))
    d.ellipse([x + w // 2 - r // 2, y + h // 2 - r // 2,
               x + w // 2 + r // 2, y + h // 2 + r // 2], fill=(30, 40, 60))
    d.rectangle([x + 20, y + 10, x + 34, y + 18], fill=(240, 238, 225))
    d.polygon([(x + w - 34, y + 10), (x + w - 22, y + 16), (x + w - 34, y + 22)],
              fill=(250, 200, 60))


def scene_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
    d.rectangle([x + 14, y + h - 16, x + w - 14, y + h - 8], fill=(120, 96, 60))
    d.rectangle([x + w // 2 - 26, y + 22, x + w // 2 + 26, y + 36], fill=(90, 60, 30))
    d.rectangle([x + w // 2 - 4, y + 36, x + w // 2 + 4, y + h - 16], fill=(140, 100, 50))
    d.rectangle([x + 16, y + 16, x + 44, y + 30], fill=(240, 238, 225))
    d.text((x + 18, y + 18), "$4,000", font=font(SANS_B, 10), fill=RED)


def scene_turtle(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 180))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(214, 196, 150))
    d.ellipse([x + w // 2 - 34, y + 18, x + w // 2 + 34, y + 58], fill=GREEN)
    d.ellipse([x + w // 2 - 22, y + 26, x + w // 2 + 22, y + 50], fill=(110, 160, 90))
    d.ellipse([x + w // 2 + 30, y + 30, x + w // 2 + 46, y + 46], fill=GREEN)
    d.ellipse([x + w // 2 - 46, y + 30, x + w // 2 - 30, y + 46], fill=GREEN)
    d.polygon([(x + w // 2 - 30, y + 52), (x + w // 2 - 12, y + 58),
               (x + w // 2 - 28, y + h - 12)], fill=GREEN)
    d.polygon([(x + w // 2 + 30, y + 52), (x + w // 2 + 12, y + 58),
               (x + w // 2 + 28, y + h - 12)], fill=GREEN)
    d.ellipse([x + w // 2 + 34, y + 24, x + w // 2 + 44, y + 34], fill=GREEN)


def scene_ball(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 222, 190))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=GREEN)
    d.ellipse([x + w // 2 - 24, y + 10, x + w // 2 + 24, y + h - 4], fill=RED)
    d.arc([x + w // 2 - 24, y + 10, x + w // 2 + 24, y + h - 4], 40, 140,
          fill=(240, 238, 225), width=3)
    d.arc([x + w // 2 - 24, y + 10, x + w // 2 + 24, y + h - 4], 220, 320,
          fill=(240, 238, 225), width=3)
    d.polygon([(x + 16, y + 20), (x + 34, y + 34), (x + 26, y + 52), (x + 12, y + 40)],
              fill=(214, 178, 120))


def scene_pad(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 44, 72))
    d.rounded_rectangle([x + 16, y + 20, x + w - 16, y + 52], radius=10, fill=(240, 238, 225))
    d.ellipse([x + 26, y + 28, x + 40, y + 42], fill=RED)
    d.ellipse([x + w - 40, y + 28, x + w - 26, y + 42], fill=NAVY)
    d.rectangle([x + w // 2 - 3, y + 28, x + w // 2 + 3, y + 44], fill=INK)
    d.rectangle([x + w // 2 - 8, y + 33, x + w // 2 + 8, y + 39], fill=INK)
    d.ellipse([x + w - 30, y + h - 22, x + w - 16, y + h - 8], fill=(250, 120, 120))
    d.polygon([(x + 18, y + h - 8), (x + 34, y + h - 24), (x + 44, y + h - 8)], fill=GREEN)


SCENES = {1: scene_globe, 2: scene_cricket, 3: scene_talks, 4: scene_flags,
          5: scene_river, 6: scene_fire, 7: scene_book, 8: scene_stage,
          9: scene_camera, 10: scene_gavel, 11: scene_turtle, 12: scene_ball,
          13: scene_pad}

CARDS = [
    (1, "ANTALYA · CLIMATE", "COP31 nears a deal at dawn",
     "New text tabled overnight after talks ran past Friday's deadline; an approval session is set for Sunday morning."),
    (2, "WELLINGTON · CRICKET", "Pant's 128 puts India 629/6 on day four",
     "Rahul's 136 and Pant's century build a 261-run lead over New Zealand at lunch in the first Test."),
    (3, "JERUSALEM · POLITICS", "Eisenkot–Likud marathon talks open today",
     "Yashar invites Netanyahu's party to intensive talks after Saturday's invite; the mandate ends on 6 December."),
    (4, "NEW DELHI · DIPLOMACY", "Jaishankar meets Bulgaria on EU trade deal",
     "The foreign minister discusses the India-EU free trade pact and Black Sea ties with Sofia."),
    (5, "DHAKA · RIVERS", "Ganges treaty talks open today",
     "Bangladesh and India meet on the shared-river treaty as the 1996 pact nears its end."),
    (6, "DHAKA · POLITICS", "30 Awami League houses torched",
     "At least 30 houses of Awami League members are set on fire in Bangladesh."),
    (7, "CHENNAI · BOOKS", "Chennai book fair set for 16–18 January",
     "The Chennai International Book Fair returns in January, with the dates announced today."),
    (8, "AHMEDABAD · MUSIC", "Diljit show faces calls to drop four songs",
     "Objections are raised over four songs ahead of the singer's Ahmedabad concert."),
    (9, "CHENNAI · FILM", "Vijay greets Anirudh and Kavya at reception",
     "The actor-politician meets Rajinikanth at the couple's wedding reception in Chennai."),
    (10, "WASHINGTON · HISTORY", "Washington's lock of hair sells for $4,000",
     "A lock of George Washington's hair goes under the hammer for $4,000."),
    (11, "WORLD · NATURE", "Green sea turtles move to Least Concern",
     "A conservation success as green turtles are reclassified from Endangered."),
    (12, "BLIND CRICKET · SPORT", "Asia Cup final washed out; Pakistan champions",
     "India's blind team boycotts the presentation after Pakistan are declared champions."),
    (13, "WORLD · RESCUE", "Teen gamer helps rescue a missing girl",
     "A teenager and his mother help find a missing girl after spotting clues in a game."),
]

ALSO = [
    (14, "NEW DELHI", "UP holds a voter-list correction drive today."),
    (15, "HYDERABAD", "40 MGD more Godavari water as a pipeline nears its finish."),
    (16, "RAJOURI", "J&K clears a Rs 7.97-crore tourism resort."),
    (17, "NEW DELHI", "Three Godara gang men held in a Pitampura shooting."),
    (18, "NEW DELHI", "US panel: China's backing for Pakistan in Op Sindoor hit Indian planning."),
    (19, "NEW DELHI", "Google gives $5m to IIT Kharagpur for AI research."),
    (20, "NEW DELHI", "Woman dead, two hurt in a Raghubir Nagar house fire."),
    (21, "NEW DELHI", "Hospital chief gets a day in jail for contempt."),
    (22, "MUMBAI", "India beat South Korea 2-1 in the Women's Asian Champions Trophy."),
    (23, "MANILA", "Philippines DOJ banks on an ASEAN treaty to end fugitive havens."),
    (24, "INDIANA", "Purdue professor's family found dead after a teen's 911 call."),
    (25, "NEW DELHI", "Trump hails India's 7% growth; BJP needles Rahul."),
    (26, "NIGERIA", "Boat carrying mourners capsizes; at least 24 killed."),
    (27, "ABUJA", "Nigeria's youth: powerful before, quiet now as an election nears."),
    (28, "COPENHAGEN", "Denmark accuses Russia of a plot to kill a US-Ukrainian rapper."),
    (29, "MUMBAI", "Suniel Shetty hails son-in-law Rahul after his century."),
    (30, "WORLD", "Eva Longoria to be godmother of cruise ship Seven Seas Prestige."),
    (31, "LONDON", "Boxer Anthony Joshua welcomes a second child."),
    (32, "NEW DELHI", "U-Special buses start for two Delhi colleges."),
]

NUMBERS = [
    ("629/6", "India's day-four total"),
    ("128", "Pant's runs at Wellington"),
    ("200", "nations in the COP31 talks"),
    ("24", "killed as a Nigeria boat capsizes"),
    ("30", "houses torched in Bangladesh"),
    ("40 MGD", "more water for Hyderabad"),
]

DATE_CHECK = ("Russia's 400-drone, 110-missile barrage — 20 Nov · Missiles land in "
              "Poland — 20 Nov · Peru quake — 21 Nov · Mexico captures 'El Chapo "
              "Isidro' — 21 Nov · Gupta sentenced in the Pannun plot — 21 Nov · "
              "Anthropic's Riemann claim — 20 Nov, verified 21 Nov · Australia beat "
              "England, 1st T20I — 21 Nov · Modi opens Nitish Setu — 21 Nov · "
              "Basra power plant fire — 21 Nov · Voyager 1 one light-day out — "
              "20–21 Nov · Wall Street tech sell-off — 20 Nov · GTA VI first-day "
              "sales — 21 Nov")

# (card no, lat, lon)
PINS = [(1, 36.9, 30.7), (2, -41.3, 174.8), (3, 31.8, 35.2), (4, 28.6, 77.2),
        (5, 23.8, 90.4), (6, 24.6, 91.4), (7, 13.1, 80.3), (8, 23.0, 72.6),
        (9, 13.9, 79.6), (10, 38.9, -77.0)]

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
    d.text((W - 12 - d.textlength("SUNDAY'S NEWS · ONE PAGE · 32 STORIES",
                                  font=font(SANS_B, 11)), 11),
           "SUNDAY'S NEWS · ONE PAGE · 32 STORIES", font=font(SANS_B, 11), fill=INK)
    d.text((12, 28), "Sunday 22 November 2026", font=font(SERIF_B, 54), fill=INK)
    d.text((12, 96), "COP31 nears a deal at dawn · Pant's 128 puts India 629/6 · "
                      "Eisenkot–Likud talks open today.",
           font=font(SERIF_I, 15), fill=(60, 57, 48))
    d.rectangle([12, 122, W - 12, 125], fill=RED)
    # ---- region strip
    d.text((12, 132), "EUROPE 3  ·  THE AMERICAS 3  ·  ASIA-PACIFIC 20  ·  MIDEAST 1  ·  "
                      "AFRICA 2  ·  OCEANIA 1  ·  WORLD 2",
           font=font(SANS_B, 12), fill=INK)
    d.line([12, 152, W - 12, 152], fill=RULE, width=1)

    # ---- numbers strip
    bw = (W - 24 - 5 * 6) // 6
    for i, (num, label) in enumerate(NUMBERS):
        bx = 12 + i * (bw + 6)
        d.rectangle([bx, 160, bx + bw, 200], outline=RULE, width=1, fill=CARD)
        nf = font(SERIF_B, 21)
        d.text((bx + bw // 2 - d.textlength(num, font=nf) // 2, 163), num,
               font=nf, fill=RED)
        lf = font(SANS, 9)
        d.text((bx + bw // 2 - d.textlength(label, font=lf) // 2, 187), label,
               font=lf, fill=MUTED)

    # ---- cards row 1: 3 big
    cw = (W - 24 - 2 * 8) // 3
    for i, card in enumerate(CARDS[:3]):
        draw_card(d, 12 + i * (cw + 8), 208, cw, 158, *card, big=True)
    # ---- cards rows 2-3: 5 medium each
    mw = (W - 24 - 4 * 8) // 5
    for i, card in enumerate(CARDS[3:8]):
        draw_card(d, 12 + i * (mw + 8), 374, mw, 138, *card, big=False)
    for i, card in enumerate(CARDS[8:13]):
        draw_card(d, 12 + i * (mw + 8), 520, mw, 138, *card, big=False)

    # ---- also list
    d.text((12, 668), "ALSO ON SUNDAY 22 NOVEMBER — 19 MORE STORIES",
           font=font(SANS_B, 13), fill=RED)
    d.line([12, 686, W - 12, 686], fill=RULE, width=1)
    colw = (W - 24 - 24) // 2
    af = font(SANS, 11)
    for j, (num, city, text) in enumerate(ALSO):
        col = j // 10
        row = j % 10
        ax = 12 + col * (colw + 24)
        ay = 694 + row * 11
        if row == 9 and col == 1:
            ay = 694 + 9 * 11
        line = f"{num}. {city} — {text}"
        d.text((ax, ay), line, font=af, fill=INK)

    # ---- bottom row: map + date check
    d.text((12, 812), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    draw_map(d, 12, 830, 488, 128)
    d.text((12, 962), "Each number is its story on this page.",
           font=font(SANS, 9), fill=MUTED)
    bx = 524
    d.rectangle([bx, 830, W - 12, 958], outline=RED, width=2, fill=CARD)
    d.text((bx + 10, 838), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    d.text((bx + 10, 854),
           "First reported Saturday 21 November (or earlier),",
           font=font(SANS_B, 10), fill=INK)
    d.text((bx + 10, 866),
           "so NOT on this page as news:",
           font=font(SANS_B, 10), fill=INK)
    df = font(SANS, 10)
    ty = 882
    for ln in wrap(d, DATE_CHECK, df, W - 12 - bx - 20):
        d.text((bx + 10, ty), ln, font=df, fill=(60, 57, 48))
        ty += 13

    # ---- footer
    d.line([12, 978, W - 12, 978], fill=RULE, width=1)
    d.text((12, 984),
           "Every story here happened, or was first reported, on Sunday 22 November 2026.",
           font=font(SERIF_I, 12), fill=INK)
    d.text((12, 1002),
           "Sources: Reuters, BBC, AP, The Times of India, India Today, NDTV, The Hindu.  Original drawings.",
           font=font(SANS, 9), fill=MUTED)

    img.save(os.path.join(HERE, "entry.png"))


if __name__ == "__main__":
    main()
