from typing import List, cast

import numpy as np
import numpy.typing as npt
from scipy import ndimage


def parse(lines: List[str]) -> npt.NDArray[int]:
    return np.array([list(l) for l in lines], dtype=int)


def display(energy: npt.NDArray[int]) -> None:
    print(np.array2string(energy, separator=""))


def inc_filter(flashes: npt.NDArray[float]) -> int:
    return cast(int, np.sum(flashes, dtype=int))


kernel = ndimage.generate_binary_structure(2, 2)


def calc_step(energy: npt.NDArray[int]) -> npt.NDArray[bool]:
    energy += 1  # type: ignore
    flashed: npt.NDArray[bool] = np.zeros_like(energy, dtype=bool)
    while True:
        new_flashes = (energy > 9) & ~flashed  # type: ignore
        if not np.any(new_flashes):
            break
        to_increment = ndimage.generic_filter(
            new_flashes.astype(np.uint8),
            inc_filter,
            size=3,
            mode="constant",
            cval=0,
        )
        energy += to_increment
        flashed |= new_flashes
    energy[flashed] = 0
    return flashed


def part_1(lines: List[str]) -> int:
    energy = parse(lines)
    flash_count = 0

    # display(energy)
    for _ in range(100):
        flashed = calc_step(energy)
        # display(energy)
        flash_count += np.count_nonzero(flashed)

    return flash_count


def part_2(lines: List[str]) -> int:
    energy = parse(lines)
    step = 0

    while True:
        step += 1
        flashed = calc_step(energy)
        if np.all(flashed):
            return step
