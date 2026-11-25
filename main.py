#!/usr/bin/env python3
"""News front page for Wednesday 25 November 2026.

Draws a newspaper front page summing up the day's world news as a
1024x1024 PNG, using only the Python standard library: a hand-rolled
PNG encoder, a small 5x7 bitmap font drawn from my own glyph table,
and simple vector drawing routines. No network, no randomness, so two
runs write byte-identical output.

Writes $MAKEFUN_OUTPUT_DIR/entry.png (default: ./out/entry.png).
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- colours
PAPER = (246, 241, 227)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
NAVY2 = (28, 46, 84)
GOLD = (201, 162, 39)
GOLD_LT = (232, 196, 90)
RED = (185, 28, 28)
RED_DK = (139, 26, 26)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
GREY = (120, 120, 116)
GREY_LT = (226, 222, 210)
GREEN = (118, 185, 0)
GREEN_DK = (84, 138, 0)
BLUE = (58, 110, 180)
BLUE_LT = (178, 208, 235)
BLUE_DK = (34, 68, 112)
SKY = (214, 232, 245)
ORANGE = (240, 130, 30)
YELLOW = (250, 204, 21)
BROWN = (146, 96, 48)
BROWN_DK = (110, 70, 32)
STEEL = (112, 128, 144)
STEEL_DK = (74, 90, 106)

# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 bits, drawn by me for this entry.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "%": ("11001", "11010", "00100", "01000", "01011", "10011", "10011"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    ":": ("00000", "01100", "00000", "00000", "00000", "01100", "00000"),
    ";": ("00000", "01100", "00000", "00000", "01100", "00100", "01000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
}


def text_width(s, scale):
    return len(s) * 6 * scale - scale


def wrap_text(s, max_w, scale):
    """Greedy word wrap; returns a list of lines."""
    words = s.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.rect(0, 0, w, h, bg)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def hline(self, x, y, w, c):
        self.rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.rect(x, y, 1, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def thick_line(self, x0, y0, x1, y1, t, c):
        for ox in range(-t // 2, t // 2 + 1):
            for oy in range(-t // 2, t // 2 + 1):
                self.line(x0 + ox, y0 + oy, x1 + ox, y1 + oy, c)

    def disc(self, cx, cy, r, c):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, c)

    def ring(self, cx, cy, r, c):
        steps = max(24, r * 6)
        for k in range(steps):
            import math
            a = 2 * math.pi * k / steps
            self.set(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)), c)

    def poly(self, pts, c):
        """Scanline fill of a polygon given as [(x, y), ...]."""
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                self.rect(int(xs[j]), y, max(1, int(xs[j + 1]) - int(xs[j])), 1, c)

    def burst(self, cx, cy, r_out, r_in, points, c):
        import math
        pts = []
        for k in range(points * 2):
            r = r_out if k % 2 == 0 else r_in
            a = math.pi * k / points - math.pi / 2
            pts.append((int(cx + r * math.cos(a)), int(cy + r * math.sin(a))))
        self.poly(pts, c)

    def glyph(self, ch, x, y, scale, c):
        g = FONT.get(ch)
        if g is None:
            return
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits[col] == "1":
                    self.rect(x + col * scale, y + row * scale, scale, scale, c)

    def text(self, s, x, y, scale, c, align="left"):
        s = s.upper()  # the bitmap font carries capitals only
        if align == "center":
            x = x - text_width(s, scale) // 2
        elif align == "right":
            x = x - text_width(s, scale)
        for ch in s:
            self.glyph(ch, x, y, scale, c)
            x += 6 * scale

    def text_lines(self, lines, x, y, scale, c, leading=None):
        if leading is None:
            leading = 7 * scale + 3
        for ln in lines:
            self.text(ln, x, y, scale, c)
            y += leading
        return y


# ---------------------------------------------------------------- PNG output
def _chunk(kind, data):
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )


def encode_png(cv):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + _chunk(b"IEND", b"")
    )


# ---------------------------------------------------------------- icons
def icon_nvidia(cv, x, y):
    # chip
    cv.rect(x + 28, y + 34, 94, 94, GREEN)
    cv.rect(x + 28, y + 34, 94, 6, GREEN_DK)
    cv.rect(x + 28, y + 122, 94, 6, GREEN_DK)
    for k in range(4):
        cv.rect(x + 14 + k * 4, y + 52 + k * 18, 14, 8, GREEN_DK)
        cv.rect(x + 122, y + 52 + k * 18, 14, 8, GREEN_DK)
    cv.rect(x + 44, y + 50, 62, 62, (140, 200, 40))
    cv.text("NVDA", x + 75, y + 70, 2, WHITE, align="center")
    cv.text("-7%", x + 75, y + 94, 2, WHITE, align="center")
    # falling arrow
    cv.thick_line(x + 118, y + 138, x + 138, y + 168, 5, RED)
    cv.poly([(x + 138, y + 176), (x + 126, y + 162), (x + 146, y + 160)], RED)
    cv.text("SHARES -7%", x + 75, y + 176, 2, RED, align="center")


def icon_riyadh(cv, x, y):
    cv.rect(x, y, 150, 210, SKY)
    # city skyline behind
    cv.rect(x + 6, y + 130, 26, 66, STEEL)
    cv.rect(x + 118, y + 142, 26, 54, STEEL)
    # tallest tower (KAFD)
    cv.rect(x + 58, y + 44, 34, 152, NAVY2)
    cv.rect(x + 58, y + 44, 34, 8, NAVY)
    for r in range(7):
        for cc in range(3):
            cv.rect(x + 64 + cc * 10, y + 62 + r * 18, 5, 8, GOLD_LT)
    cv.vline(x + 75, y + 28, 16, NAVY2)
    # blast at the top
    cv.burst(x + 75, y + 40, 26, 12, 8, ORANGE)
    cv.burst(x + 75, y + 40, 15, 7, 8, YELLOW)
    cv.disc(x + 60, y + 22, 7, GREY)
    cv.disc(x + 92, y + 18, 9, GREY)
    cv.rect(x, y + 196, 150, 14, (90, 96, 100))


def icon_hormuz(cv, x, y):
    cv.rect(x, y, 150, 210, SKY)
    # sea
    cv.rect(x, y + 128, 150, 82, BLUE)
    cv.hline(x + 8, y + 150, 60, WHITE)
    cv.hline(x + 82, y + 168, 60, WHITE)
    cv.hline(x + 20, y + 186, 50, WHITE)
    # tanker
    cv.poly([(x + 18, y + 128), (x + 132, y + 128), (x + 118, y + 158),
             (x + 30, y + 158)], (40, 44, 52))
    cv.rect(x + 30, y + 100, 22, 28, RED)
    cv.rect(x + 56, y + 108, 22, 20, YELLOW)
    cv.rect(x + 82, y + 100, 22, 28, GREEN_DK)
    cv.rect(x + 108, y + 112, 18, 16, WHITE)
    # mine in the water
    cv.disc(x + 128, y + 176, 9, INK)
    for a in range(8):
        import math
        ang = math.pi * a / 4
        cv.line(int(x + 128 + 8 * math.cos(ang)), int(y + 176 + 8 * math.sin(ang)),
                int(x + 128 + 14 * math.cos(ang)), int(y + 176 + 14 * math.sin(ang)), INK)
    # blast above the deck
    cv.burst(x + 66, y + 92, 22, 10, 8, ORANGE)
    cv.burst(x + 66, y + 92, 12, 6, 8, YELLOW)


def icon_ukraine(cv, x, y):
    cv.rect(x, y, 150, 210, SKY)
    # sea
    cv.rect(x, y + 138, 150, 72, BLUE)
    cv.hline(x + 10, y + 160, 55, WHITE)
    cv.hline(x + 85, y + 180, 55, WHITE)
    # listing warship, bow up, stern down
    cv.poly([(x + 22, y + 118), (x + 128, y + 148), (x + 118, y + 168),
             (x + 34, y + 140)], STEEL_DK)
    cv.poly([(x + 22, y + 118), (x + 128, y + 148), (x + 122, y + 156),
             (x + 28, y + 128)], STEEL)
    cv.thick_line(x + 62, y + 112, x + 66, y + 82, 4, STEEL_DK)
    cv.rect(x + 52, y + 96, 22, 16, STEEL_DK)
    # smoke
    cv.disc(x + 66, y + 66, 12, GREY)
    cv.disc(x + 84, y + 52, 10, GREY)
    cv.disc(x + 100, y + 66, 8, GREY)
    # blast on the deck
    cv.burst(x + 96, y + 132, 18, 8, 8, ORANGE)
    cv.burst(x + 96, y + 132, 10, 5, 8, YELLOW)


def icon_huawei(cv, x, y):
    cv.rect(x, y, 150, 210, (232, 226, 208))
    # courthouse columns
    for k in range(3):
        cx = x + 26 + k * 42
        cv.rect(cx, y + 34, 18, 96, WHITE)
        cv.rect(cx - 4, y + 28, 26, 8, WHITE)
        cv.rect(cx - 4, y + 128, 26, 8, WHITE)
    cv.rect(x + 12, y + 20, 126, 10, NAVY2)
    cv.rect(x + 12, y + 136, 126, 10, NAVY2)
    # gavel
    cv.rect(x + 42, y + 156, 66, 16, BROWN)
    cv.thick_line(x + 118, y + 150, x + 138, y + 178, 6, BROWN_DK)
    cv.rect(x + 30, y + 176, 90, 10, BROWN_DK)
    cv.text("GUILTY", x + 75, y + 192, 2, RED_DK, align="center")


def icon_space(cv, x, y):
    cv.rect(x, y, 150, 210, NAVY)
    # stars
    for sx, sy in [(14, 20), (40, 44), (128, 26), (118, 70), (24, 90),
                   (136, 110), (12, 140), (60, 16), (100, 44)]:
        cv.set(x + sx, y + sy, WHITE)
        cv.set(x + sx + 1, y + sy, WHITE)
        cv.set(x + sx - 1, y + sy, WHITE)
        cv.set(x + sx, y + sy + 1, WHITE)
        cv.set(x + sx, y + sy - 1, WHITE)
    # space station
    cv.rect(x + 96, y + 26, 40, 14, STEEL)
    cv.rect(x + 88, y + 30, 8, 6, BLUE)
    cv.rect(x + 136, y + 30, 8, 6, BLUE)
    cv.rect(x + 108, y + 18, 16, 8, STEEL_DK)
    # rocket
    cv.poly([(x + 52, y + 78), (x + 68, y + 78), (x + 60, y + 52)], RED)
    cv.rect(x + 52, y + 78, 16, 56, WHITE)
    cv.poly([(x + 52, y + 134), (x + 40, y + 152), (x + 52, y + 146)], RED)
    cv.poly([(x + 68, y + 134), (x + 80, y + 152), (x + 68, y + 146)], RED)
    cv.disc(x + 60, y + 92, 5, BLUE)
    # flame
    cv.poly([(x + 54, y + 134), (x + 66, y + 134), (x + 60, y + 168)], ORANGE)
    cv.poly([(x + 56, y + 134), (x + 64, y + 134), (x + 60, y + 152)], YELLOW)
    # horizon band at the bottom of the panel (earth below, kept inside)
    cv.rect(x, y + 196, 150, 14, BLUE)


# ---------------------------------------------------------------- layout
STORIES = [
    ("TECH", "HUANG SAYS SORRY", RED,
     "Nvidia chief apologises to staff and says he is in daily therapy. "
     "Shares fall 7% after a 31% surge on his comeback.",
     icon_nvidia),
    ("MIDDLE EAST", "TOWER HIT AGAIN", RED_DK,
     "Houthis strike Riyadh's tallest tower a second time in a week. "
     "11 people hurt; coalition hits back at Hodeidah.",
     icon_riyadh),
    ("MIDDLE EAST", "MINES IN HORMUZ", BLUE_DK,
     "Two tankers hit mines in the Strait of Hormuz. "
     "Iran's Revolutionary Guards blamed for the blasts.",
     icon_hormuz),
    ("WAR IN EUROPE", "WARSHIP SUNK", STEEL_DK,
     "Ukraine says it sank a Russian warship off Libya in self-defence. "
     "Kyiv also hit a Russian ship in the Gulf of Finland.",
     icon_ukraine),
    ("LAW", "HUAWEI CONVICTED", NAVY2,
     "A US jury convicts China's Huawei over its Iran business "
     "and stealing trade secrets in a criminal trial.",
     icon_huawei),
    ("SPACE", "PAKISTAN IN ORBIT", GREEN_DK,
     "Pakistan's first astronaut reaches China's Tiangong station "
     "aboard Shenzhou-24, the first foreigner on board.",
     icon_space),
]


def draw_card(cv, x, y, w, h, tag, headline, accent, caption, icon_fn):
    cv.rect(x, y, w, h, CARD)
    cv.rect(x, y, w, 10, accent)
    cv.rect(x, y, w, h, INK)  # border via thin rects below
    cv.rect(x + 1, y + 1, w - 2, h - 2, CARD)
    cv.rect(x, y, w, 10, accent)
    # icon panel
    ix, iy = x + 12, y + 22
    icon_fn(cv, ix, iy)
    cv.rect(ix, iy, 150, 1, INK)
    cv.rect(ix, iy + 209, 150, 1, INK)
    cv.rect(ix, iy, 1, 210, INK)
    cv.rect(ix + 149, iy, 1, 210, INK)
    # text column
    tx = x + 178
    tw = w - 178 - 14
    cv.text(tag, tx, y + 24, 2, accent)
    cv.text(headline, tx, y + 52, 3, INK)
    lines = wrap_text(caption, tw, 2)
    cv.text_lines(lines, tx, y + 92, 2, (52, 52, 52), leading=18)


def build():
    cv = Canvas(W, H, PAPER)
    # masthead
    cv.rect(0, 0, W, 150, NAVY)
    cv.rect(0, 146, W, 4, GOLD)
    cv.text("THE WORLD IN ONE DAY", W // 2, 26, 5, WHITE, align="center")
    cv.text("WEDNESDAY 25 NOVEMBER 2026", W // 2, 92, 4, GOLD_LT, align="center")
    # sub-strip
    cv.text("SIX STORIES THAT DEFINED THE DAY", W // 2, 162, 2, RED_DK,
            align="center")
    # story grid: 2 cols x 3 rows
    cw, ch, gx, gy = 496, 242, 16, 8
    for i, (tag, headline, accent, caption, icon_fn) in enumerate(STORIES):
        cx = 8 + (i % 2) * (cw + gx)
        cy = 182 + (i // 2) * (ch + gy)
        draw_card(cv, cx, cy, cw, ch, tag, headline, accent, caption, icon_fn)
    # footer ticker
    cv.rect(0, 938, W, 86, NAVY)
    cv.rect(0, 938, W, 3, GOLD)
    cv.text("MARKETS: NIKKEI -2.76%  S&P 500 -0.5%  BRENT $87.49, DOWN 21% IN NOV",
            W // 2, 954, 2, WHITE, align="center")
    cv.text("ALSO: COP31 COLLAPSES - SENEGAL WIN AFRICA CUP - DEMOCRATS WIN 259 SEATS",
            W // 2, 984, 2, GOLD_LT, align="center")
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    cv = build()
    data = encode_png(cv)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
