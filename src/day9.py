from typing import List, cast

import numpy as np
import numpy.typing as npt
from scipy import ndimage


def parse(lines: List[str]) -> npt.NDArray[int]:
    return np.array([list(l) for l in lines], dtype=int)


kernel = ndimage.generate_binary_structure(2, 1)


def low_filter(arr: npt.NDArray[int]) -> np.bool_:
    return np.all(arr[2] < arr[[0, 1, 3, 4]])


def part_1(lines: List[str]) -> int:
    heightmap = parse(lines)
    low_points = ndimage.generic_filter(
        heightmap,
        low_filter,
        footprint=kernel,
        output=bool,
        mode="constant",
        cval=np.inf,
    )
    return cast(int, np.sum(heightmap[low_points] + 1))
