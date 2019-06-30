#!python3

# convenience wrapper over colorsys functions in  standard library to provide a nicer API 

import colorsys
from typing import Tuple

from .utils import Pixel

ColorspacePoint = Tuple[float, float, float]

def normalize(pixel: Pixel) -> ColorspacePoint:
    """ scales RGB pixel channel values to [0, 1] """
    return tuple(channel/255.0 for channel in pixel)

# basic colorspace conversions

def hsv(pixel: Pixel) -> ColorspacePoint:
    """ HSV representation of RGB pixel """
    return colorsys.rgb_to_hsv(*normalize(pixel))

def hls(pixel: Pixel) -> ColorspacePoint:
    """ HLS representation of RGB pixel """
    return colorsys.rgb_to_hls(*normalize(pixel))

def yiq(pixel: Pixel) -> ColorspacePoint:
    """ YIQ representation of RGB pixel """
    return colorsys.rgb_to_yiq(*normalize(pixel))

# single dimensions

def hue(pixel: Pixel) -> float:
    """ get pixel hue """
    return hsv(pixel)[0]

def saturation(pixel: Pixel) -> float:
    """ get pixel saturation """
    return hsv(pixel)[1]

def luminance(pixel: Pixel) -> float:
    """ get pixel luminance """
    return hls(pixel)[1]

# "reverse" conversions: get an RGB value by pretending normalized input pixel is from another colorspace
# not guaranteed to generate valid RGBs

def rev_hsv(pixel: Pixel) -> ColorspacePoint:
    """ apply HSV conversion to a point actually in RGB space """
    return colorsys.hsv_to_rgb(*normalize(pixel))

def rev_hls(pixel: Pixel) -> ColorspacePoint:
    """ apply HLS conversion to a point actually in RGB space """
    return colorsys.hls_to_rgb(*normalize(pixel))

def rev_yiq(pixel: Pixel) -> ColorspacePoint:
    """ apply YIQ conversion to a point actually in RGB space """
    return colorsys.yiq_to_rgb(*normalize(pixel))

# technically undefined but we have fun here 

def uhsv(pixel: Pixel) -> Tuple[float]:
    """ attempt at HSV representation *without* normalizing RGB channel values """
    return colorsys.rgb_to_hsv(*pixel)
