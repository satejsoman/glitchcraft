from math import cos, pi, sin

import numpy as np
from PIL import Image, ImageDraw

from glitchcraft.utils import progress, shift

white = (255,) * 3

src_img = Image.open('00100dPORTRAIT_00100_BURST20180803190225629_COVER.jpg')
src = src_img.load()
(w, h) = src_img.size

dst_img = src_img.copy()
dst = dst_img.load()

draw = ImageDraw.Draw(dst_img)

pts = [int(x) for x in np.linspace(0, w-1, 14)[1:]]
dx = pts[0]
r = 3 * dx // 4
a = h // 4
v_offset1 = 0.6
v_offset2 = 1.4

R0 = 20
q1, R1, R2 = 0.3, 40, 30
q2, R3 = 0.5, 12

f = lambda x: h/2 + a * sin((x - w/2)/(128*pi))

for x0 in progress(pts):
    Y = f(x0)
    dy = h - Y
    for x in range(x0 - dx, x0 + dx):
        for y in range(h):
            try:
                dst[x, y] = src[x, (y + dy) % h]
            except Exception:
                pass
    try:
        fill = dst[x0 - dx/2, y]
        draw.ellipse((x0 - dx/2 - (r/2 + R0), Y - (r/2 + R0), x0 - dx/2 + (r/2 + R0), Y + (r/2 + R0)), fill=white)
        draw.ellipse((x0 - dx/2 - r/2, Y - r/2, x0 - dx/2 + r/2, Y + r/2), fill=fill)

        draw.ellipse((x0 - dx/2 - R1, Y + q1 * a - R1, x0 - dx/2 + R1, Y + q1 * a + R1), fill=src[x0 - dx/2 - R1/2, Y + q1 * a])
        draw.ellipse((x0 - dx/2 - R2, Y + q1 * a - R2, x0 - dx/2 + R2, Y + q1 * a + R2), fill=white)

        draw.ellipse((x0 - dx/2 - R3, Y + q2 * a - R3, x0 - dx/2 + R3, Y + q2 * a + R3), fill=white)

        linefill = dst[x0 - dx/2, Y + v_offset1 * a]
        draw.line((x0 - dx/2, Y + v_offset1 * a, x0 - dx/2, Y + v_offset2 * a), fill=white,    width = 15)
        draw.line((x0 - dx/2, Y + v_offset1 * a, x0 - dx/2, Y + v_offset2 * a), fill=linefill, width = 9)
    except Exception:
        print(x0)
        pass

    up_cols = sorted([
        sorted([dst[x, y] for y in range(int(Y - v_offset2*a), int(Y - v_offset1*a))])
        for x in range(int(x0 - dx/2 - r/2), int(x0 - dx/2 + r/2))
    ], key=lambda col: np.mean([sum(px) for px in col]))

    for (i, x) in enumerate(range(int(x0 - dx/2 - r/2), int(x0 - dx/2 + r/2))):
        for (j, y) in enumerate(range(int(Y - v_offset2*a), int(Y - v_offset1*a))):
            try: 
                dst[x, y] = shift(up_cols[i][j], 0.8)
            except Exception as e:
                print(x, y, i, j, e)
                pass

dst_img.save('pl9_circles.png')
dst_img.show()
