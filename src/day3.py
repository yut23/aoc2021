from typing import List, Sequence

import numpy as np
import numpy.typing as npt


def bits_to_int(bits: Sequence[int]) -> int:
    return sum(1 << i for i, bit in enumerate(bits[::-1]) if bit)


def part_1(lines: List[str]) -> int:
    bits = np.array([list(l) for l in lines], dtype=int)
    most_frequent = (np.mean(bits, axis=0) >= 0.5).astype(int)
    least_frequent = 1 - most_frequent
    gamma = bits_to_int(most_frequent)
    epsilon = bits_to_int(least_frequent)
    return gamma * epsilon


def filter_at_bit(
    bits: npt.NDArray[int], position: int, most_common: bool
) -> npt.NDArray[int]:
    mean = np.mean(bits[:, position], axis=0)
    if mean == 0.5:
        target = int(most_common)
    elif most_common:
        target = int(mean > 0.5)
    else:
        target = int(mean < 0.5)

    mask = bits[:, position] == target
    return bits[mask]  # type: ignore


def calc_rating(bits: npt.NDArray[int], most_common: bool) -> int:
    position = 0
    while bits.shape[0] > 1:
        bits = filter_at_bit(bits, position, most_common)
        position += 1
    return bits_to_int(bits[0])


def part_2(lines: List[str]) -> int:
    bits = np.array([list(l) for l in lines], dtype=int)
    oxygen = calc_rating(bits, True)
    co2 = calc_rating(bits, False)

    return oxygen * co2
