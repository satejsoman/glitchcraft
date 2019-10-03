#!/usr/bin/python

#handy imports  
from keyword import iskeyword

#parameters
w, h = 900, 1500
code_start = 24
code_size = 7 #code line thickness
code_lines = 70
code_sep = 15
indent_size = 32
letter_spacing, word_spacing = 6, 12

#define colors
bg_color = (25, 25, 25)
palette = {
    "string": (229, 115, 118), 
    "keyword": (235, 167, 114),
    "text": (120, 120, 120),
    "comment": (60, 60, 60), 
    "builtin": (116, 178, 208),
    "symbols": (180, 180, 180)   
}

QUOTE = chr(34)

def set_color(rgb):
    stroke(*rgb)
    fill(*rgb)
    
def setup():
    pixelDensity(2)
    
    with open(__file__, "r") as f:
        content = f.readlines()
        num_lines = len(content) 
    
    #size and background
    h = (num_lines + 2) * code_sep/2
    size(w, h)
    background(*bg_color)
    
    #line, text, color options
    strokeCap(ROUND)
    strokeWeight(code_size)
    textSize(15)
    textFont(createFont("Monospaced", 14))
    set_color(palette["text"])

    line_y = code_start
    for code_line in content:
        comment_mode = code_line[0] == "#"
        num_spaces = 0
        while code_line[num_spaces] == " " and num_spaces < len(code_line) - 1:
            num_spaces += 1
        line_x = indent_size  + num_spaces * letter_spacing
        for word in code_line.split():
            keyword_mode = False
            builtin_mode = False
            if iskeyword(word) and not comment_mode:
                keyword_mode = True
                set_color(palette["keyword"])
            
            if word in dir(__builtin__) and not comment_mode:
                builtin_mode= True
                set_color(palette["builtin"])
                
            if not (comment_mode or keyword_mode or builtin_mode):
                set_color(palette["text"])
            string_mode = False
            for c in word:
                if c == QUOTE and not comment_mode:
                    string_mode = not string_mode
                    if string_mode:
                        set_color(palette["string"])
                elif c == "#" and not string_mode:
                    comment_mode = True
                    set_color(palette["comment"])
                if c.isalnum() or c in "_'":
                    if not any([keyword_mode, comment_mode, builtin_mode, string_mode]):
                        set_color(palette["text"])
                    line(line_x, line_y, line_x + letter_spacing, line_y)
                    line_x += letter_spacing
                else: 
                    offset = -2 if (line_x == indent_size or c in "*#!") else 4
                    if not any([keyword_mode, comment_mode, builtin_mode, string_mode, c == QUOTE]):
                        set_color(palette["symbols"])
                    text(c, line_x + offset, line_y + 0.3*code_sep)
                    line_x += 15
            line_x += word_spacing
        line_y += code_sep 
    save("skeleton_quine.png")
