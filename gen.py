"""

    Project Lyrae
    Copyright (c) 2025 lucysir

    This script is originally written as a part of Lyrae Shaders
    https://modrinth.com/project/lyrae-shaders

    If you use it and find it helpful, I'd appreciate attribution.

"""

import struct
import argparse

import loader


OUT_FILE = "heitz_bluenoise_{0}spp.ssbo"

VALID_SPPS = (1, 2, 4, 8, 16, 32, 64, 128, 256)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "gen",
        description = "Generate Iris-ready SSBO files for bluenoise sampling."
    )
    parser.add_argument("spp", type=int, help="SPP (Samples per pixel) value. It must be an integer in range [1, 256] and a power of two.")

    args = parser.parse_args()
    spp = int(args.spp)

    if not spp in VALID_SPPS:
        raise ValueError(f"spp argument '{spp}' is not a valid value. Use -h to see valid usage.")

    filename = OUT_FILE.format(spp)

    ranking = getattr(loader, f"RANKING_{spp}SPP")
    scrambling = getattr(loader, f"SCRAMBLING_{spp}SPP")

    with open(filename, "wb") as file:
        content = bytearray()

        for el in ranking:
            content += struct.pack("<I", el)

        for el in scrambling:
            content += struct.pack("<I", el)

        for el in loader.SOBOL_256SPP_256D:
            content += struct.pack("<I", el)
        
        file.write(content)

        print(f"Bluenoise sampling SSBO data is successfully written to '{filename}'.")