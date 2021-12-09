from typing import List, Tuple, cast

import numpy as np
import numpy.typing as npt
from scipy import ndimage


def parse(lines: List[str]) -> Tuple[npt.NDArray[int], npt.NDArray[int], int]:
    heightmap: npt.NDArray[int] = np.array([list(l) for l in lines], dtype=int)
    basins, num_basins = ndimage.label((heightmap != 9).astype(np.uint8))
    return heightmap, basins, num_basins


def part_1(lines: List[str]) -> int:
    heightmap, basins, num_basins = parse(lines)
    # every low point has a basin, and it will be the minimum value in that basin
    mins = ndimage.minimum(heightmap, basins, index=np.arange(1, num_basins + 1))
    return cast(int, np.sum(mins + 1))


def part_2(lines: List[str]) -> int:
    _, basins, num_basins = parse(lines)
    basin_sizes = [
        np.count_nonzero(basins == label) for label in range(1, num_basins + 1)
    ]
    basin_sizes.sort(reverse=True)
    return cast(int, np.prod(basin_sizes[:3]))
