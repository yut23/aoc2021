import itertools
from typing import List

import numpy as np
import numpy.typing as npt


def parse(lines: List[str]) -> npt.NDArray[int]:
    return np.array([list(l) for l in lines], dtype=int)


def display(energy: npt.NDArray[int]) -> None:
    print(np.array2string(energy, separator=""))


def calc_step(energy: npt.NDArray[int]) -> npt.NDArray[bool]:
    energy += 1  # type: ignore
    flashed: npt.NDArray[bool] = np.zeros_like(energy, dtype=bool)
    while True:
        new_flashes = (energy > 9) & ~flashed  # type: ignore
        if not np.any(new_flashes):
            break
        slices = {
            (None, -1): slice(1, None),
            (None,): slice(None),
            (1, None): slice(None, -1),
        }
        for x, y in itertools.product(slices, repeat=2):
            energy[slice(*x), slice(*y)] += new_flashes[slices[x], slices[y]]
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
