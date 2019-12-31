from itertools import cycle
import random
from math import sin, cos, radians

random.seed(11235813)

# size and colors
w, h = 1200, 1200
bg_color = (25, 25, 25)
Rs = list(range(0, 500, 75)) 

silvers = cycle([
    (243/2, 243/2, 243/2),
    (233/2, 233/2, 233/2),
    (227/2, 227/2, 227/2)
])


colors = [
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

]
random.shuffle(colors)
palette = cycle(colors)

def set_color(clr):
    try:
        r, g, b = clr
        stroke(r, g, b)
    except Exception:
        stroke(clr)
    fill(0, 0, 0, 0)

def setup():
    hint(ENABLE_STROKE_PURE)
    smooth() 
    
    size(w, h)
    background(*bg_color)
    n = 45
    strokeJoin(ROUND)
    
    x0 = w/2
    y0 = h/2

    strokeWeight(0.1)
    spacing = 50
    hatch_length = 1
    for x in range(0, w, spacing):
        for y in range(0, h, spacing):
            set_color(next(silvers))
            line(x - hatch_length, y - hatch_length, x + hatch_length, y + hatch_length)
            set_color(next(silvers))
            line(x + spacing/2 - hatch_length, y + spacing/2 + hatch_length, x + spacing/2 + hatch_length, y + spacing/2 - hatch_length)

    for i in range(len(Rs)):
        for j in range(n):
            bezier(
                width / 2.  + width  * cos(TWO_PI * i  * j / n), 
                height / 2. + height * sin(TWO_PI * i * j / n), 
                width, height / 2., width, 
                height / 2., 2. * width, 
                height / 2.);

    for (i, (clr, R)) in enumerate(zip(silvers, Rs), start = 3):
        stroke(255, 255, 255)
        fill(255, 255, 255)
        
        for j in range(12):
            a1_x = x0 + R * cos(TWO_PI/i * j)
            a1_y = y0 + R * sin(TWO_PI/i * j)
            
            c1_x = x0 + R * cos(TWO_PI/i * (j + 1.05))
            c1_y = y0 + R * sin(TWO_PI/i * (j + 1))
            
            c2_x = x0 + R * cos(TWO_PI/i * (j + 2.1))
            c2_y = y0 + R * sin(TWO_PI/i * (j + 2))
            
            a2_x = x0 + R * cos(TWO_PI/i * (j + 3.15))
            a2_y = y0 + R * sin(TWO_PI/i * (j + 3))
            
            b2_x = x0 + R * cos(TWO_PI/i * (j + 4.2))
            b2_y = y0 + R * sin(TWO_PI/i * (j + 4))
            
            b3_x = x0 + R * cos(TWO_PI/i * (j + 5.25))
            b3_y = y0 + R * sin(TWO_PI/i * (j + 5))            
            
            strokeWeight(0.75)
            set_color(next(palette))
            bezier(a1_x, a1_y, c1_x, c1_y, c2_x, c2_y, a2_x, a2_y)
            bezier(a2_x, a2_y, c1_x, c1_y, c2_x, c2_y, b2_x, b2_y)
            bezier(b2_x, b2_y, c1_x, c1_y, c2_x, c2_y, b3_x, b3_y)
        
    save("warp5.png")
