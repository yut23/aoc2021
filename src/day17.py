r"""
Physics time!

y coordinates as functions of time:
\begin{align}
  v_y(t) &= v_{0y} - t \\
    y(t) &= y(t-1) + v_y(t-1) \\
         &= y(t-2) + v_y(t-2) + v_y(t-1) \\
         &= \sum_{\tau=0}^{t-1} v_y(\tau) \\
         &= \sum_{\tau=0}^{t-1} v_{0y} - \tau \\
         &= v_{0y}t - \sum_{\tau=0}^{t-1} \tau \\
         &= v_{0y}t - \frac{(t-1)t}{2} \\
         &= v_{0y}t - \frac{t^2 - t}{2} \\
\end{align}

x coordinates as functions of time:
\begin{align}
  v_x(t) &= \sign(v_{0x}) \max(|v_{0x}| - t, 0) \\
    x(t) &= x(t-1) + v_x(t-1) \\
         &= \sum_{\tau=0}^{t-1} v_x(\tau) \\
         &= \sum_{\tau=0}^{min(|v_{0x}|, t) - 1} \sign(v_{0x}) (|v_{0x}| - \tau) \\
         \shortintertext{Since $v_x(t >= |v_{0x}|) = 0$}
\end{align}

If $t >= |v_{0x}|$:
\begin{align}
    x(t) &= \sum_{\tau=0}^{|v_{0x}|-1} \sign(v_{0x}) (|v_{0x}| - \tau) \\
         &= \sign(v_{0x}) \sum_{\tau=0}^{|v_{0x}|-1} (|v_{0x}| - \tau) \\
         &= \sign(v_{0x}) |v_{0x}|^2 - \sign(v_{0x}) \sum_{\tau=0}^{|v_{0x}|-1} \tau \\
         &= \frac{v_{0x}}{|v_{0x}|} |v_{0x}|^2 - \frac{v_{0x}}{|v_{0x}|} \frac{|v_{0x}|(|v_{0x}| - 1)}{2} \\
         &= v_{0x} |v_{0x}| - \frac{v_{0x}(|v_{0x}| - 1)}{2} \\
         &= \frac{2 v_{0x} |v_{0x}| - v_{0x} |v_{0x}| + v_{0x})}{2} \\
         &= \frac{v_{0x} |v_{0x}| + v_{0x})}{2} \\
         &= \frac{v_{0x}(|v_{0x}| + 1)}{2} \\
\end{align}

If $t < |v_{0x}|$:
\begin{align}
    x(t) &= \sum_{\tau=0}^{t-1} \sign(v_{0x}) (|v_{0x}| - \tau) \\
         &= \sign(v_{0x}) \sum_{\tau=0}^{t-1} (|v_{0x}| - \tau) \\
         &= \frac{v_{0x}}{|v_{0x}|} |v_{0x}|t - \sign(v_{0x}) \sum_{\tau=0}^{t-1} \tau \\
         &= v_{0x} t - \frac{v_{0x}}{|v_{0x}|} \frac{t(t - 1)}{2} \\
         &= v_{0x} t - \sign{v_{0x}} \frac{t(t - 1)}{2} \\
\end{align}

Notes: $vy(y=0) = -v_0y - 1$, and we can extrapolate from there
"""


import re
from typing import Generator, List, NamedTuple, Optional, Tuple, Union

import numpy as np
import numpy.typing as npt

IntType = np.int64
IntArray = npt.NDArray[IntType]


class Coords(NamedTuple):
    vx: IntArray
    vy: IntArray
    x: IntArray = 0
    y: IntArray = 0

    def __getitem__(self, key: Union[int, slice]) -> "Coords":
        return Coords(self.vx[key], self.vy[key], self.x[key], self.y[key])

    def __iter__(self) -> Generator["Coords", None, None]:
        for i in range(self.vx.shape[0]):
            yield Coords(self.vx[i], self.vy[i], self.x[i], self.y[i])

    def __len__(self) -> int:
        return self.vx.shape[0]


def step(coords: Coords) -> Coords:
    x = coords.x + coords.vx
    y = coords.y + coords.vy
    vy = coords.vy - 1
    vx = coords.vx - np.sign(coords.vx)
    return Coords(vx, vy, x, y)


def solve_vx(init: Coords, t: IntArray) -> IntArray:
    return np.copysign(np.clip(np.abs(init.vx) - t, 0, None), init.vx).astype(IntType)


def solve_vy(init: Coords, t: IntArray) -> IntArray:
    return init.vy - t


def solve_y(init: Coords, t: IntArray) -> IntArray:
    return init.y + init.vy * t - t * (t - 1) // 2


def solve_x(init: Coords, t: IntArray) -> IntArray:
    return init.x + np.where(
        t >= np.abs(init.vx),
        init.vx * (np.abs(init.vx) + 1) // 2,  # x velocity is zero from drag
        init.vx * t - np.copysign(t * (t - 1) // 2, init.vx).astype(IntType),
    )


def solve(init: Coords, t: IntArray) -> Coords:
    x = solve_x(init, t)
    y = solve_y(init, t)
    vx = solve_vx(init, t)
    vy = solve_vy(init, t)
    return Coords(vx, vy, x, y)


def parse(lines: List[str]) -> Tuple[range, range]:
    m = re.match(r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", lines[0])
    assert m is not None
    return range(int(m[1]), int(m[2])), range(int(m[3]), int(m[4]))


def draw(coords: Coords, target: Optional[Tuple[range, range]] = None) -> None:
    start = coords[0]
    x_min = coords.x.min()
    x_max = coords.x.max()
    y_min = coords.y.min()
    y_max = coords.y.max()

    if target is not None:
        x_min = min(x_min, target[0].start)
        x_max = max(x_max, target[0].stop - 1)
        y_min = min(y_min, target[1].start)
        y_max = max(y_max, target[1].stop - 1)

    shape = (y_max - y_min + 1, x_max - x_min + 1)

    field = np.full(shape, ".", dtype="<U1")
    if target is not None:
        for y in target[1]:
            for x in target[0]:
                field[y_max - y, x - x_min] = "T"

    for coord in coords:
        field[y_max - coord.y, coord.x - x_min] = "#"

    field[y_max - start.y, start.x - x_min] = "S"
    print(
        "\n".join(
            l.lstrip(" ").lstrip("[").rstrip("]")
            for l in np.array2string(
                field, separator="", formatter={"numpystr": str}, threshold=field.size
            ).splitlines(keepends=False)
        )
    )


def part_1(lines: List[str]) -> int:
    # FIXME: ignore x for now, as we can probably land that target pretty easily
    _, y_range = parse(lines)
    # init = Coords(6, 3)
    # print(f"Initial velocity: {init.vx},{init.vy}")
    # path = solve(init, np.arange(10))
    # draw(path, (x_range, y_range))

    # We always hit y=0 exactly, so the highest y velocity will have to put us
    # at the bottom edge of the target.
    # Optimal y velocity: vy = y_max at y=0
    # vy(y=0) = -v_0y - 1 = y_max
    # => v_0y = -y_max - 1
    vy = -y_range.start - 1
    t0 = 2 * vy + 1
    path = solve(Coords(vx=0, vy=vy), np.arange(t0 + 3))
    # print(path)
    # draw(path, (x_range, y_range))
    return path.y.max()
