from typing import List

import numpy as np
import numpy.typing as npt
import scipy.linalg

# We want to minimize `sum(abs(x - target) for x in positions)`. This has the
# form of an L1 norm, which is minimized at the median.


def part_1(lines: List[str]) -> int:
    positions: npt.NDArray[int] = np.array(lines[0].split(","), dtype=int)
    target = np.median(positions)  # type: ignore
    return int(scipy.linalg.norm(positions - target, 1))
