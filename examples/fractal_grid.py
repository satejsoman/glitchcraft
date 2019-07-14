from pathlib import Path

from PIL import Image

from glitchcraft.fractal import colorshift

output_dir = Path("../artifacts/output/fractals")
output_dir.mkdir(exist_ok=True)

src = Image.open("../artifacts/input/stream_square.png")

# draw basic fractal
colorshift(Image.new("RGB", src.size, color="white"), normalization=3).save(output_dir/"julia.png")

# parameter grid 
for (cx, cy) in [
    (-1, 1),         # default
    (-0.7, 0.27015), # julia  
    (-0.5, 0.5)       
]: 
    for normalization in [3, 6, 9]:
        print(normalization, cx, cy)
        colorshift(src, normalization=normalization, cx=cx, cy=cy).save(output_dir/("stream_shifted_{}_{}_{}.png".format(normalization, cx, cy)))
