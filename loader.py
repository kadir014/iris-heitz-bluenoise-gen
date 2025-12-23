"""

    Project Lyrae
    Copyright (c) 2025 lucysir

    This script is originally written as a part of Lyrae Shaders
    https://modrinth.com/project/lyrae-shaders

    If you use it and find it helpful, I'd appreciate attribution.

"""

# This module parses the sobol sequence, scrambling and ranking data provided by
# Eric Heitz's low-discrepancy sampling paper packed in the 'heitz.data' file.


# Owen-scrambled Sobol sequence of 256 samples of 256 dimensions
SOBOL_256SPP_256D: list[int] = []

# Scrambling tile of 128x128 pixels optimized for 256spp in 8D
SCRAMBLING_256SPP: list[int] = []

# Ranking tile of 128x128 pixels optimzed for all the powers of two spp below 256 in 8D
RANKING_256SPP: list[int] = []

# Scrambling tile of 128x128 pixels optimized for 128spp in 8D
SCRAMBLING_128SPP: list[int] = []

# Ranking tile of 128x128 pixels optimzed for all the powers of two spp below 128 in 8D
RANKING_128SPP: list[int] = []

# Scrambling tile of 128x128 pixels optimized for 64spp in 8D
SCRAMBLING_64SPP: list[int] = []

# Ranking tile of 128x128 pixels optimzed for all the powers of two spp below 64 in 8D
RANKING_64SPP: list[int] = []

# Scrambling tile of 128x128 pixels optimized for 32spp in 8D
SCRAMBLING_32SPP: list[int] = []

# Ranking tile of 128x128 pixels optimzed for all the powers of two spp below 32 in 8D
RANKING_32SPP: list[int] = []

# Scrambling tile of 128x128 pixels optimized for 16spp in 8D
SCRAMBLING_16SPP: list[int] = []

# Ranking tile of 128x128 pixels optimzed for all the powers of two spp below 16 in 8D
RANKING_16SPP: list[int] = []

# Scrambling tile of 128x128 pixels optimized for 8spp in 8D
SCRAMBLING_8SPP: list[int] = []

# Ranking tile of 128x128 pixels optimzed for all the powers of two spp below 8 in 8D
RANKING_8SPP: list[int] = []

# Scrambling tile of 128x128 pixels optimized for 4spp in 8D
SCRAMBLING_4SPP: list[int] = []

# Ranking tile of 128x128 pixels optimzed for all the powers of two spp below 4 in 8D
RANKING_4SPP: list[int] = []

# Scrambling tile of 128x128 pixels optimized for 2spp in 8D
SCRAMBLING_2SPP: list[int] = []

# Ranking tile of 128x128 pixels optimzed for all the powers of two spp below 2 in 8D
RANKING_2SPP: list[int] = []

# Scrambling tile of 128x128 pixels optimized for 1spp in 8D
SCRAMBLING_1SPP: list[int] = []

# Ranking tile of 128x128 pixels optimzed for all the powers of two spp below 1 in 8D
RANKING_1SPP: list[int] = []


with open("bluenoise_packed.data", "rb") as file:
    content = file.read()

    i = 0
    for _ in range(256 * 256):
        byte = content[i]
        SOBOL_256SPP_256D.append(byte)
        i += 1

    tiles = (
        SCRAMBLING_256SPP,
        RANKING_256SPP,
        SCRAMBLING_128SPP,
        RANKING_128SPP,
        SCRAMBLING_64SPP,
        RANKING_64SPP,
        SCRAMBLING_32SPP,
        RANKING_32SPP,
        SCRAMBLING_16SPP,
        RANKING_16SPP,
        SCRAMBLING_8SPP,
        RANKING_8SPP,
        SCRAMBLING_4SPP,
        RANKING_4SPP,
        SCRAMBLING_2SPP,
        RANKING_2SPP,
        SCRAMBLING_1SPP,
        RANKING_1SPP
    )

    for j in range(18):
        tile = tiles[j]

        for _ in range(128 * 128 * 8):
            byte = content[i]

            tile.append(byte)

            i += 1