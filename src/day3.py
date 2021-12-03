from typing import List

import numpy as np


def part_1(lines: List[str]) -> int:
    bits = np.array([list(l.strip()) for l in lines], dtype=int)
    most_frequent = (np.mean(bits, axis=0) >= 0.5).astype(int)
    least_frequent = 1 - most_frequent
    gamma = sum(2 ** i * bit for i, bit in enumerate(most_frequent[::-1]))
    epsilon = sum(2 ** i * bit for i, bit in enumerate(least_frequent[::-1]))
    return gamma * epsilon
