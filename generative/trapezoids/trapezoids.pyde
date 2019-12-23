from itertools import cycle
from math import sin, cos, radians
import random

# size and colors
w, h = 900, 900
bg_color = (25, 25, 25)
palette = cycle([
    # base
    (60, 60, 60),
    (120, 120, 120),
    (220, 220, 220),
    # original
    (229, 115, 118),  # e57376
    (235, 167, 114),  # eba772
    (116, 178, 208),  # 74b2d0
    (180, 190, 180),  # b4beb4
    # added:
    (102, 133, 134),  # 668586
    (132, 148, 131),  # 849483
    (216, 219, 226),  # d8dbe2
    (141, 161, 185),  # 8da1b9
    (225, 212, 183),  # e2d4b7

])

def trapezoid(x0, y0, tz_height, tz_base, up=True, t=60):
    set_color(next(palette))
    theta = radians(t)
    x_scale = 1 / tan(theta)
    y_scale = 1 / sin(theta)
    dx = x_scale * tz_height
    if up:
        beginShape()
        vertex(x0, y0)
        vertex(x0 - dx, y0 + tz_height)
        vertex(x0 + dx + tz_base, y0 + tz_height)
        vertex(x0 + tz_base, y0)
        vertex(x0, y0)
        endShape()
    else:
        beginShape()
        vertex(x0, y0)
        vertex(x0 + dx, y0 + tz_height)
        vertex(x0 + tz_base, y0 + tz_height)
        vertex(x0 + tz_base + dx, y0)
        vertex(x0, y0)
        endShape()

def slashed_circle(x0, y0, tz_height, tz_base, up=True, t=60):
    for k in (1, 2, 4, 6, 8):
        set_color(next(palette))
        circle(x0 + tz_base / 2, y0 + tz_height / 2, tz_height / k)

def set_color(clr):
    try:
        r, g, b = clr
        stroke(r, g, b)
    except Exception:
        stroke(clr)
    fill(0, 0, 0, 0)

def setup():
    strokeWeight(3)
    strokeJoin(MITER)
    size(w, h)
    background(*bg_color)

    random.seed(112358)

    y0 = -35
    t0 = 55
    t = t0 + 2 * y0 / 15 - y0 ** 2 / 6750
    up = True
    while y0 < h:
        x0 = -random.randint(0, 30)
        dy = random.randint(15, 51)
        while x0 < w:
            xp = x0 + random.randint(15, 81)
            if random.random() > 0.12:
                trapezoid(x0, y0, dy, xp - x0, up, t)
                if random.random() > 0.50:
                    x_off = +1 if random.random() > 0.5 else -1
                    y_off = +1 if random.random() > 0.5 else -1
                    trapezoid(
                        x0 + x_off * 5, y0 + y_off * 5, dy, xp - x0, up, t)
            else:
                slashed_circle(x0, y0, dy, xp - x0, up, t)
            x0 = xp + 30
            up = not up
        y0 += dy + 20
        t = t0 + 2 * y0 / 15 - y0 ** 2 / 6750
    save("trapezoids.png")
