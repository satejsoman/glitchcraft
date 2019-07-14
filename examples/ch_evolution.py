from pathlib import Path

from PIL import Image
import matplotlib.pyplot as plt

from glitchcraft.cahn_hillard import integrate


def main(input_path, output_dir):
    src = Image.open(input_path).convert('L')
    output_dir.mkdir(exist_ok=True)
    filename_pattern = str(output_dir/"frame_{0:03d}.png")
    for (i, image) in enumerate(integrate(src)):
        plt.imsave(filename_pattern.format(i), image, cmap="Greys")


if __name__ == "__main__":
    base = Path(__file__).parent
    input_path = base/"../artifacts/input/stream_square.png"
    output_dir = base/"../artifacts/output/ch_evolution_test"
    main(input_path, output_dir)
