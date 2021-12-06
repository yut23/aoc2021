from typing import List


def simulate(initial_timers: List[int], days: int) -> int:
    # number of fish with each timer value (0 - 8, inclusive)
    fish: List[int] = [0] * 9
    for timer in initial_timers:
        fish[timer] += 1

    for _ in range(days):
        new_fish = [0] * 9
        # handle standard timer decrease
        for t in range(1, 8 + 1):
            new_fish[t - 1] = fish[t]
        # handle new fish being created
        new_fish[8] = fish[0]
        # handle timer roll-over at 0
        new_fish[6] += fish[0]
        fish = new_fish

    return sum(fish)


def simulate_inplace(initial_timers: List[int], days: int) -> int:
    # number of fish with each timer value (0 - 8, inclusive)
    fish: List[int] = [0] * 9
    for timer in initial_timers:
        fish[timer] += 1

    for _ in range(days):
        fish[0:8], fish[8] = fish[1:9], fish[0]
        fish[6] += fish[8]

    return sum(fish)


def part_1(lines: List[str]) -> int:
    initial_timers = [int(x) for x in lines[0].split(",")]
    return simulate_inplace(initial_timers, 80)


def part_2(lines: List[str]) -> int:
    initial_timers = [int(x) for x in lines[0].split(",")]
    return simulate_inplace(initial_timers, 256)
