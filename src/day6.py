from typing import List


def part_1(lines: List[str]) -> int:
    initial_timers = [int(x) for x in lines[0].split(",")]

    # number of fish with each timer value (0 - 8, inclusive)
    fish: List[int] = [0] * 9
    for timer in initial_timers:
        fish[timer] += 1

    for _ in range(80):
        new_fish = [0] * 9
        # handle standard timer decrease
        for t in range(1, 8 + 1):
            new_fish[t - 1] = fish[t]
        # handle new fish being created
        new_fish[8] += fish[0]
        # handle timer roll-over at 0
        new_fish[6] += fish[0]
        fish = new_fish

    return sum(fish)