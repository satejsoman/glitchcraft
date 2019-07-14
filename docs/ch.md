# cahn-hillard phase separation

the [cahn-hillard equation](https://en.wikipedia.org/wiki/Cahn%E2%80%93Hilliard_equation) is a model of phase separation from theoretical materials science. 

<div align="center"><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/b7a860f6b6857c5eefafb72a81c8fc1d25964edc"></div>

generally, given an initial concentration field, it describes how particles will diffuse along a free energy gradient. this library implements a solver that takes a single-channel or grayscale image as an initial concentration gradient and simulates the system evolution.

[david eyre](http://www.math.utah.edu/~eyre/research/methods/papers.html) developed a stable numerical integration scheme to solve the cahn-hillard partial differential equation.

# example: 

## take this initial sample image:
<div align="center">
<img src=../artifacts/input/stream_square_greyscale.png width="256">
</div>

## run the [solver](../examples/ch_evolution.py): 
```python
from glitchcraft.cahn_hillard import integrate
from pathlib import Path
from PIL import Image

def main(input_path, output_dir):
    src = Image.open(input_path).convert('L')
    output_dir.mkdir(exist_ok=True)
    integrate(src, str(output_dir/"frame_{0:03d}.png"))


if __name__ == "__main__":
    base = Path(__file__).parent
    input_path = base/"../artifacts/input/stream_square.png"
    output_dir = base/"../artifacts/output/ch_evolution"
    main(input_path, output_dir)
```

## merge the individual frames into a gif: 
```
ffmpeg -t 5 -pattern_type glob -i "*.png" -vf "scale=512:512:flags=lanczos" ch_evolution.gif
```

## _voilà_
<div align="center">
<img src=../artifacts/output/ch_evolution/ch_evolution.gif width="256">
</div>
