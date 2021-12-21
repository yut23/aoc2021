from itertools import cycle, islice
from typing import Iterator, List, Tuple


def parse(lines: List[str]) -> Tuple[int, int]:
    player_1 = int(lines[0].rpartition(": ")[2])
    player_2 = int(lines[1].rpartition(": ")[2])
    return player_1, player_2


def play(start_1: int, start_2: int, die: Iterator[int]) -> Tuple[int, int, int]:
    "Return the number of die rolls and the winning and losing players' scores."
    positions = [start_1, start_2]
    scores = [0, 0]
    rolls = 0
    curr_player = 0
    while True:
        positions[curr_player] = (
            positions[curr_player] + sum(islice(die, 3)) - 1
        ) % 10 + 1
        rolls += 3
        scores[curr_player] += positions[curr_player]
        if scores[curr_player] >= 1000:
            break
        curr_player = 1 - curr_player
    return rolls, scores[curr_player], scores[1 - curr_player]


def part_1(lines: List[str]) -> int:
    starts = parse(lines)
    die = cycle(range(1, 101))
    rolls, _, loser = play(*starts, die)
    return rolls * loser
