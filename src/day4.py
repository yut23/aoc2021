from typing import List, Tuple, cast

import numpy as np
import numpy.typing as npt


class Board:
    def __init__(self, lines: List[str]):
        assert len(lines) == 5
        self.numbers: npt.NDArray[int] = np.array([l.split() for l in lines], dtype=int)
        self.marked: npt.NDArray[bool] = np.zeros_like(self.numbers, dtype=bool)

    def mark(self, number: int) -> bool:
        """Returns True if the board wins."""
        self.marked |= self.numbers == number
        return self.check_win()

    def check_win(self) -> bool:
        return any(self.marked.prod(axis=0)) or any(self.marked.prod(axis=1))

    def calc_score(self, last_number: int) -> int:
        return cast(int, self.numbers[~self.marked].sum()) * last_number


def read_boards(lines: List[str]) -> Tuple[List[int], List[Board]]:
    order = [int(n) for n in lines[0].split(",")]
    boards = []
    for i in range(2, len(lines) - 1, 6):
        boards.append(Board(lines[i : i + 5]))
    return order, boards


def part_1(lines: List[str]) -> int:
    order, boards = read_boards(lines)
    for num in order:
        for board in boards:
            if board.mark(num):
                return board.calc_score(num)
    return -1
