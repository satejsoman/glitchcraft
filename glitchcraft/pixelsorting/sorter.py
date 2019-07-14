

class PixelSorter(): 


    def __init__(self):
        pass 


def radial(*params):
    r, t, *_ = params
    return (r*cos(t), r*sin(t))

for param_coord in product(*params.values):
    img_coord = coordinates(*param_coord)
