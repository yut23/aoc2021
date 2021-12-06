import math
from typing import Counter, Generator, List, Tuple


class Line:
    def __init__(self, desc: str):
        p1, _, p2 = desc.partition(" -> ")
        self.x1, self.y1 = map(int, p1.split(","))
        self.x2, self.y2 = map(int, p2.split(","))

    def __str__(self) -> str:
        return f"{self.x1},{self.y1} -> {self.x2},{self.y2}"

    def get_points(self) -> Generator[Tuple[int, int], None, None]:
        if self.is_vertical():
            yield from (
                (self.x1, y)
                for y in range(min(self.y1, self.y2), max(self.y1, self.y2) + 1)
            )
            return
        if self.is_horizontal():
            yield from (
                (x, self.y1)
                for x in range(min(self.x1, self.x2), max(self.x1, self.x2) + 1)
            )
            return

        # diagonal line
        dx = int(math.copysign(1, self.x2 - self.x1))
        dy = int(math.copysign(1, self.y2 - self.y1))

        yield from (
            (self.x1 + i * dx, self.y1 + i * dy)
            for i in range(abs(self.x2 - self.x1) + 1)
        )

    def is_horizontal(self) -> bool:
        return self.y1 == self.y2

    def is_vertical(self) -> bool:
        return self.x1 == self.x2


def part_1(input_lines: List[str]) -> int:
    line_counts: Counter[Tuple[int, int]] = Counter()

    for line in map(Line, input_lines):
        if line.is_horizontal() or line.is_vertical():
            for point in line.get_points():
                line_counts[point] += 1

    return sum(int(c > 1) for c in line_counts.values())


def part_2(input_lines: List[str]) -> int:
    line_counts: Counter[Tuple[int, int]] = Counter()

    for line in map(Line, input_lines):
        for point in line.get_points():
            line_counts[point] += 1

    return sum(int(c > 1) for c in line_counts.values())
