import functools
from collections import Counter
from itertools import cycle, islice, product
from typing import List, Tuple


def parse(lines: List[str]) -> Tuple[int, int]:
    player_1 = int(lines[0].rpartition(": ")[2])
    player_2 = int(lines[1].rpartition(": ")[2])
    return player_1, player_2


def play_deterministic(start_1: int, start_2: int) -> Tuple[int, int, int]:
    "Return the number of die rolls and the winning and losing players' scores."
    positions = [start_1, start_2]
    scores = [0, 0]
    die = cycle(range(1, 101))
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
    rolls, _, loser = play_deterministic(*starts)
    return rolls * loser


dirac_frequencies: List[Tuple[int, int]] = list(
    Counter(map(sum, product(range(1, 4), repeat=3))).items()  # type: ignore
)


@functools.lru_cache(maxsize=None)
def step_dirac(
    pos_curr: int,
    pos_other: int,
    score_curr: int = 0,
    score_other: int = 0,
    curr_player: int = 0,
) -> List[int]:
    wins = [0, 0]
    for roll, count in dirac_frequencies:
        new_pos = (pos_curr + roll) % 10
        new_score = score_curr + new_pos + 1
        if new_score >= 21:
            wins[curr_player] += count
            continue
        new_wins = step_dirac(
            pos_other,
            new_pos,
            score_other,
            new_score,
            1 - curr_player,
        )
        wins[0] += new_wins[0] * count
        wins[1] += new_wins[1] * count
    return wins


def play_dirac(start_1: int, start_2: int) -> List[int]:
    "Return the win counts for each player."
    # clear the cache for timing measurements
    step_dirac.cache_clear()
    return step_dirac(start_1 - 1, start_2 - 1)


def part_2(lines: List[str]) -> int:
    starts = parse(lines)
    wins = play_dirac(*starts)
    return max(wins)
