import heapq
from typing import Dict, Generator, List, Tuple

import numpy as np
import numpy.typing as npt

Coord = Tuple[int, int]


def parse(lines: List[str]) -> npt.NDArray[int]:
    return np.array([list(l) for l in lines], dtype=int)


class PriorityQueue:
    def __init__(self) -> None:
        self.pq: List[Tuple[int, Coord]] = []

    def add(self, coord: Coord, distance: int = 0) -> None:
        heapq.heappush(self.pq, (distance, coord))

    def pop_min(self) -> Tuple[int, Coord]:
        return heapq.heappop(self.pq)

    def __bool__(self) -> bool:
        return bool(self.pq)


def dijkstra(cave: npt.NDArray[int]) -> int:
    start = (0, 0)
    dest = (cave.shape[0] - 1, cave.shape[1] - 1)

    distances: Dict[Coord, int] = {}
    distances[start] = 0

    queue = PriorityQueue()
    queue.add(start, 0)

    def neighbors(coord: Coord) -> Generator[Coord, None, None]:
        y, x = coord
        if x - 1 >= 0:
            yield y, x - 1
        if y - 1 >= 0:
            yield y - 1, x
        if x + 1 < cave.shape[1]:
            yield y, x + 1
        if y + 1 < cave.shape[0]:
            yield y + 1, x

    while queue:
        dist, current = queue.pop_min()
        if dist != distances[current]:
            continue
        for n in neighbors(current):
            tentative_distance = distances[current] + cave[n]
            if n not in distances or tentative_distance < distances[n]:
                distances[n] = tentative_distance
                queue.add(n, tentative_distance)
        if current == dest:
            break

    return distances[dest]


def part_1(lines: List[str]) -> int:
    cave = parse(lines)
    return dijkstra(cave)
