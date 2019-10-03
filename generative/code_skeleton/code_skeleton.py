#!/usr/bin/python

#handy imports  
import re
from keyword import iskeyword

#parameters
w, h = 900, 1500
code_start = 30
code_size = 6 #code line thickness
code_lines = 70
code_sep = 15
indent_size = 45
letter_spacing, word_spacing = 5, 10

#define colors
bg_color = (25, 25, 25)
palette = {
    "text": (120, 120, 120),
    "string": (229, 115, 118),
    "comment": (60, 60, 60), 
    "keyword": (235, 167, 114),
    "builtin": (116, 178, 208),
    "symbols": (180, 190, 180)   
}

QUOTE, STAR, HASH, BANG, DOT = list(map(chr, [34, 42, 35, 33, 46]))
ADJUST_SPACE = [QUOTE, STAR] + list(map(chr, [40, 91, 92, 63, 46, 47]))

def set_color(rgb):
    stroke(*rgb)
    fill(*rgb)
    
def setup():
    pixelDensity(2)
    
    with open(__file__, "r") as f:
        content = f.readlines()
    
    #size and background
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
        comment_mode = code_line[0] == HASH
        num_spaces = 0
        while code_line[num_spaces] == " " and num_spaces < len(code_line) - 1:
            num_spaces += 1
        line_x = indent_size  + num_spaces * letter_spacing
        for word in re.findall("{}.*?{}|[\w']+|[\x20-\x7E]".format(QUOTE, QUOTE), code_line.strip()):
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
                if  c == " ":
                    line_x +=  word_spacing
                else: 
                    if c == QUOTE and not comment_mode:
                        string_mode = not string_mode
                        if string_mode:
                            set_color(palette["string"])
                    elif c == HASH and not string_mode:
                        comment_mode = True
                        set_color(palette["comment"])
                    if c.isalnum() or c in "_'":
                        if not any([keyword_mode, comment_mode, builtin_mode, string_mode]):
                            set_color(palette["text"])
                        line(line_x, line_y, line_x + letter_spacing, line_y)
                        line_x += letter_spacing
                    else: 
                        offset = -4 if (line_x == indent_size or c in [STAR, HASH, BANG]) else 4
                        if not any([keyword_mode, comment_mode, builtin_mode, string_mode, c == QUOTE]):
                            set_color(palette["symbols"])
                        text(c, line_x + offset, line_y + 0.3*code_sep)
                        line_x += letter_spacing + (word_spacing if c in ADJUST_SPACE else letter_spacing)
        line_y += code_sep
    
    save("skeleton_quine.png")
