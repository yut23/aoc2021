import re
from typing import List, NamedTuple, Tuple

import numpy as np
import numpy.typing as npt

AREA_MAX = 50


class Step(NamedTuple):
    turn_on: bool
    x: Tuple[int, int]
    y: Tuple[int, int]
    z: Tuple[int, int]

    def slices(self) -> Tuple[slice, slice, slice]:
        return (
            slice(AREA_MAX + self.x[0], AREA_MAX + self.x[1] + 1),
            slice(AREA_MAX + self.y[0], AREA_MAX + self.y[1] + 1),
            slice(AREA_MAX + self.z[0], AREA_MAX + self.z[1] + 1),
        )

    def within_area(self) -> bool:
        return (
            self.x[0] >= -AREA_MAX
            and self.x[1] <= AREA_MAX
            and self.y[0] >= -AREA_MAX
            and self.y[1] <= AREA_MAX
            and self.z[0] >= -AREA_MAX
            and self.z[1] <= AREA_MAX
        )


def parse(lines: List[str]) -> List[Step]:
    steps = []
    for line in lines:
        action, rest = line.split(" ")
        parts = re.findall(r"[xyz]=(-?\d+)\.\.(-?\d+)", rest)
        coords = []
        for start, end in parts:
            coords.append((int(start), int(end)))
        steps.append(Step(action == "on", *coords))
    return steps


def part_1(lines: List[str]) -> int:
    steps = parse(lines)
    core: npt.NDArray[np.bool_] = np.zeros([AREA_MAX * 2 + 1] * 3, dtype=np.bool_)

    for step in steps:
        if step.within_area():
            core[step.slices()] = step.turn_on

    return np.count_nonzero(core)
