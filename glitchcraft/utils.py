#!python3

# common utilities for image manipulation

from math import sqrt
from typing import Iterable, Sequence, Tuple, Union
from xml.dom import minidom
import numpy as  np

from tqdm import tqdm, trange

# type definition for an RGB pixel
Pixel = Tuple[int, int, int]

# progress bars

def progress(iterator: Union[Iterable, int]) -> tqdm:
    """ wrapper over tqdm, kept to simplify legacy code using progressbar2 """
    if type(iterator) == int:
        return trange(iterator)
    return tqdm(iterator)

def penumerate(iterator: Iterable) -> tqdm:
    """ ensures tqdm wraps the underlying iterator to prevent enumerate object hiding sequence length """
    return enumerate(tqdm(iterator))

def pzip(iterator1: Iterable, iterator2: Iterable, wrap_both=False) -> tqdm:
    """ ensures tqdm wraps the underlying iterator to prevent zip from interfering with tqdm optimizations """
    return zip(tqdm(iterator1), tqdm(iterator2) if wrap_both else iterator2)

# pixel/channel operations

def blend(alpha: float, px1: Pixel, px2: Pixel) -> Pixel:
    """ affine combination of each pixel's channel intensities"""
    return tuple(int((1 - alpha) * c1 + alpha * c2) for (c1, c2) in zip(px1, px2))

def shift(pixel: Pixel, factor: float) -> Pixel:
    """ brightness shifting for RGB pixels """
    return tuple(min(int(factor*channel), 255) for channel in pixel)

def mean_pixel(pixels: Sequence[Pixel]) -> Pixel:
    """ quadratic luminance averaging for RGB pixels """
    n = float(len(pixels))
    return tuple(int(sqrt(sum(pixel[channel]**2 for pixel in pixels)/n)) for channel in (0, 1, 2))

# misc 

def const(value):
    return lambda *args: value 

def import_svg_path(filename):
    doc = minidom.parse(filename)
    path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    coords = set(tuple(map(float, coord.split(","))) for coord in path_strings[0].split("C")[1].split())
    doc.unlink()

    return coords

def fit_x(coords: List[Tuple[float, float]], deg: Optional[int] = None) -> np.polynomial.Polynomial:
    if not deg: 
        deg = int(0.75 * len(coords))

    xs, ys = list(zip(*coords))
    return np.polynomial.Polynomial.fit(xs, ys, deg=deg)

def fit_y(coords: List[Tuple[float, float]], deg: Optional[int] = None) -> np.polynomial.Polynomial:
    if not deg: 
        deg = int(0.75 * len(coords))

    xs, ys = list(zip(*coords))
    return np.polynomial.Polynomial.fit(ys, xs, deg=deg)