import numpy as np


def part_1(lines):
    data = np.array(lines, dtype=int)
    return np.sum(np.diff(data) > 0)  # type: ignore


def part_2(lines):
    data = np.array(lines, dtype=int)
    windowed = data[:-2] + data[1:-1] + data[2:]
    return np.sum(np.diff(windowed) > 0)  # type: ignore
