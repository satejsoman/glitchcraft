from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image

from glitchcraft.cahn_hillard import integrate
from glitchcraft.utils import progress


def main(input_path, output_dir):
    src = Image.open(input_path).convert('L')
    output_dir.mkdir(exist_ok=True)
    
    filename_pattern = str(output_dir/"frame_{0:03d}.png")
    state = integrate(src)
    
    for i in progress(250):
        plt.imsave(filename_pattern.format(i), next(state), cmap="Greys")


if __name__ == "__main__":
    base = Path(__file__).parent
    input_path = base/"../artifacts/input/stream_square.png"
    output_dir = base/"../artifacts/output/ch_evolution_test"
    main(input_path, output_dir)
