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
