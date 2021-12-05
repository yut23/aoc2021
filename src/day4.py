from typing import List, Tuple

import numpy as np
import numpy.typing as npt


class Bingo:
    def __init__(self, boards: List[List[str]]):
        self.numbers: npt.NDArray[int] = np.array(
            [[l.split() for l in lines] for lines in boards], dtype=int
        )
        self.marked: npt.NDArray[bool] = np.zeros_like(self.numbers, dtype=bool)
        self.won: npt.NDArray[bool] = np.zeros(self.numbers.shape[0], dtype=bool)

    def mark(self, number: int) -> List[int]:
        """Returns the scores of all winning boards."""
        self.marked[~self.won] |= self.numbers[~self.won] == number
        new_wins: npt.NDArray[bool] = ~self.won & (
            self.marked.prod(axis=1).any(axis=-1)
            | self.marked.prod(axis=2).any(axis=-1)
        )
        if new_wins.any():
            self.won[new_wins] = True
            mask = ~self.marked[new_wins]
            scores = self.numbers[new_wins].sum(axis=(1, 2), where=mask) * number
            return list(scores)
        return []


def read_boards(lines: List[str]) -> Tuple[List[int], Bingo]:
    order = [int(n) for n in lines[0].split(",")]
    boards = []
    for i in range(2, len(lines) - 1, 6):
        boards.append(lines[i : i + 5])
    return order, Bingo(boards)


def part_1(lines: List[str]) -> int:
    order, bingo = read_boards(lines)
    for num in order:
        new_wins = bingo.mark(num)
        if new_wins:
            return new_wins[0]
    return -1


def part_2(lines: List[str]) -> int:
    order, bingo = read_boards(lines)
    for num in order:
        new_wins = bingo.mark(num)
        if bingo.won.all():
            return new_wins[0]
    return -1
