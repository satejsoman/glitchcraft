from types import SimpleNamespace

import numpy as np
import glitchcraft.colorspace as cspace

class SummaryStat:
    def __init__(self, operations):
        self.operations = operations
    
    def __call__(self, pixels):
        return self.operation()

    def __lmul__(self, val):
        self.operations

class PixelProperty: 
    def __init__(self, operations):
        pass 

    def __call__(self, pixel):
        pass 

brightness = PixelProperty(sum)
hue = PixelProperty(cspace.hue)
median = SummaryStat(np.median)
mean   = SummaryStat(np.average)

def from_transparent(img):
    pass 
    
def from_grayscale(img, keep):
    pass 

brightness > 1.2 * median(brightness)
hue < 0.9 * mean(hue)
