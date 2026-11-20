#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme from scratch, deterministically (Pillow only).

The scene: a synthwave Vice City sunset. A striped sun sets over the ocean
between two palm silhouettes and a lit skyline, while the white make.fun
ghost (sparkle eyes, magenta star) floats in the sky next to the make.fun
wordmark. The caption is the launch-day joke: thirteen years of waiting,
two delays, GTA 6 finally out — and a sick day to play it.

GTA 6 came out 19 Nov 2026. Everything here is fixed numbers and fixed
drawing calls, so every run writes the same 1200x675 PNG.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# --- sky: purple dusk at the top, gold at the horizon (y = 440) ---
sky_stops = [(0.0, (26, 11, 46)), (0.35, (122, 28, 122)), (0.62, (226, 62, 110)),
             (0.80, (255, 126, 46)), (1.0, (255, 201, 60))]
HORIZON = 440
for y in range(HORIZON):
    t = y / HORIZON
    for i in range(len(sky_stops) - 1):
        t0, c0 = sky_stops[i]
        t1, c1 = sky_stops[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0) if t1 > t0 else 0
            col = tuple(int(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
            break
    d.line([(0, y), (W, y)], fill=col)

# --- sun with a soft halo, then retro slats cut across its lower half ---
sx, sy, sr = 600, 400, 115
for r in range(sr + 60, sr, -4):
    alpha = int(60 * (1 - (r - sr) / 60))
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 150 + alpha // 3, 80))
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 233, 168))
for yy in range(sy + 10, sy + sr, 16):
    half = int(math.sqrt(max(sr * sr - (yy - sy) ** 2, 0)))
    d.rectangle([sx - half, yy, sx + half, yy + 5], fill=(255, 126, 46))

# --- ocean below the horizon, with the sun's reflection shimmering ---
for y in range(HORIZON, 530):
    t = (y - HORIZON) / 90
    col = tuple(int(a + (b - a) * t) for a, b in zip((64, 20, 90), (24, 8, 44)))
    d.line([(0, y), (W, y)], fill=col)
for i in range(24):
    yy = HORIZON + 6 + i * 4
    wob = 26 + (i % 5) * 14
    d.line([(sx - wob, yy), (sx + wob, yy)], fill=(255, 190, 90), width=3)

# --- ground and skyline silhouettes with a few lit windows ---
d.rectangle([0, 530, W, H], fill=(16, 6, 30))
buildings = [(0, 470, 70, 530), (80, 440, 150, 530), (160, 480, 210, 530),
             (220, 420, 300, 530), (310, 470, 360, 530), (880, 460, 950, 530),
             (960, 430, 1040, 530), (1050, 475, 1110, 530), (1120, 445, 1200, 530)]
for x0, y0, x1, y1 in buildings:
    d.rectangle([x0, y0, x1, y1], fill=(24, 8, 42))
    for wy in range(y0 + 12, y1 - 8, 18):
        for wx in range(x0 + 10, x1 - 8, 18):
            if (wx * 7 + wy * 13) % 5 == 0:
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 201, 90))

# --- palm silhouettes: a curved trunk of segments, then arcing fronds ---
def palm(cx, base, h, lean, scale=1.0):
    pts = []
    for i in range(11):
        f = i / 10
        x = cx + lean * f * f * 60 * scale
        y = base - f * h
        pts.append((x, y))
    d.line(pts, fill=(16, 6, 30), width=int(10 * scale), joint="curve")
    tx, ty = pts[-1]
    for ang in range(-160, 21, 28):
        a = math.radians(ang)
        ex = tx + math.cos(a) * 95 * scale
        ey = ty + math.sin(a) * 42 * scale + 26 * scale
        d.line([(tx, ty), (ex, ey)], fill=(16, 6, 30), width=int(7 * scale))
        d.line([(tx, ty), ((tx + ex) / 2, (ty + ey) / 2 + 14 * scale)],
               fill=(16, 6, 30), width=int(4 * scale))

palm(120, 560, 210, -1, 1.0)
palm(1090, 565, 190, 1, 0.9)

# --- make.fun ghost: white body, round top, four-scallop hem ---
gx, gy, gw, gh = 880, 130, 170, 200
ghost = Image.new("RGBA", (W, H), (0, 0, 0, 0))
g = ImageDraw.Draw(ghost)
g.pieslice([gx, gy, gx + gw, gy + gw], 180, 360, fill=(255, 255, 255, 255))
g.rectangle([gx, gy + gw // 2, gx + gw, gy + gh - 30], fill=(255, 255, 255, 255))
sc = gw // 4
for i in range(4):
    x0 = gx + i * sc
    g.pieslice([x0, gy + gh - 30 - sc // 2, x0 + sc, gy + gh - 30 + sc // 2],
               0, 180, fill=(255, 255, 255, 255))
img = Image.alpha_composite(img.convert("RGBA"), ghost).convert("RGB")
d = ImageDraw.Draw(img)


def star4(cx, cy, r, fill):
    pts = [(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy),
           (cx + r * 0.28, cy + r * 0.28), (cx, cy + r), (cx - r * 0.28, cy + r * 0.28),
           (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)]
    d.polygon(pts, fill=fill)


# sparkle eyes and a smile, then the magenta star coin beside the ghost
star4(gx + 58, gy + 78, 17, (26, 11, 46))
star4(gx + 112, gy + 78, 17, (26, 11, 46))
d.arc([gx + 62, gy + 100, gx + 108, gy + 128], 15, 165, fill=(26, 11, 46), width=5)
star4(gx + gw + 42, gy + 30, 26, (255, 0, 110))
star4(gx - 34, gy + 150, 15, (255, 0, 110))


# --- caption text, centred, with a dark outline so it reads over the sky ---
def text_center(y, s, font, fill, outline=(10, 4, 26), ow=4):
    bbox = d.textbbox((0, 0), s, font=font)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2
    for dx in range(-ow, ow + 1):
        for dy in range(-ow, ow + 1):
            if dx * dx + dy * dy <= ow * ow + 2:
                d.text((x + dx, y + dy), s, font=font, fill=outline)
    d.text((x, y), s, font=font, fill=fill)
    return y + (bbox[3] - bbox[1])


f_top = ImageFont.truetype(BOLD, 62)
f_big = ImageFont.truetype(BOLD, 70)
f_sub = ImageFont.truetype(BOLD, 40)
f_tag = ImageFont.truetype(BOLD, 36)

text_center(28, "13 YEARS. 2 DELAYS.", f_top, (255, 255, 255))
text_center(540, "GTA 6 IS OUT.", f_big, (255, 233, 168))
text_center(622, "MY BOSS THINKS I'M SICK.", f_sub, (255, 255, 255))
# make.fun wordmark in the free sky corner, top-left
d.text((28, 34), "make.fun", font=f_tag, fill=(255, 255, 255),
       stroke_width=2, stroke_fill=(255, 0, 110))

img.save("meme.png")
print("saved meme.png", img.size)
