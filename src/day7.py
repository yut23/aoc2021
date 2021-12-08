from typing import Callable, List, Tuple, Union, overload

import numpy as np
import numpy.typing as npt


@overload
def total_fuel(
    positions: npt.NDArray[int],
    target: int,
    calc_fuel: Callable[[npt.NDArray[int]], npt.NDArray[int]],
) -> int:
    ...


@overload
def total_fuel(
    positions: npt.NDArray[int],
    target: Union[List[int], npt.NDArray[int]],
    calc_fuel: Callable[[npt.NDArray[int]], npt.NDArray[int]],
) -> npt.NDArray[int]:
    ...


def total_fuel(
    positions: npt.NDArray[int],
    target: Union[int, List[int], npt.NDArray[int]],
    calc_fuel: Callable[[npt.NDArray[int]], npt.NDArray[int]],
) -> Union[int, npt.NDArray[int]]:
    targets: npt.NDArray[int] = np.array(target, dtype=int)
    # if targets is not a scalar, then this will broadcast positions into the
    # last axis, which we then sum over
    steps: npt.NDArray[int] = np.abs(positions - targets[..., np.newaxis], dtype=int)
    return np.sum(calc_fuel(steps), axis=-1, dtype=int)  # type: ignore  # np.sum() just returns Any :(


def minimize_fuel(
    positions: npt.NDArray[int],
    approx_target: float,
    calc_fuel: Callable[[npt.NDArray[int]], npt.NDArray[int]],
) -> Tuple[int, int]:
    """Returns the minimum (fuel, target) of `floor(target)` and `ceil(target)`."""
    targets = [int(np.floor(approx_target)), int(np.ceil(approx_target))]
    fuels = total_fuel(positions, targets, calc_fuel)
    index = np.argmin(fuels)
    return fuels[index], targets[index]


def part_1(lines: List[str]) -> int:
    # We want to minimize `sum(abs(x - target) for x in positions)`. This has the
    # form of an L1 norm, which is minimized at the median.
    positions: npt.NDArray[int] = np.array(lines[0].split(","), dtype=int)

    def fuel(steps: npt.NDArray[int]) -> npt.NDArray[int]:
        return steps

    approx_target: float = np.median(positions)  # type: ignore  # TODO: fixed in numpy 1.22
    return minimize_fuel(positions, approx_target, fuel)[0]


def part_2(lines: List[str]) -> int:
    # fuel cost is now n*(n+1)/2, which is proportional to n^2 => L2 norm
    # this is minimized by the mean, instead of the median
    positions: npt.NDArray[int] = np.array(lines[0].split(","), dtype=int)

    def fuel(steps: npt.NDArray[int]) -> npt.NDArray[int]:
        return steps * (steps + 1) // 2

    return minimize_fuel(positions, np.mean(positions), fuel)[0]
