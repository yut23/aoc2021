from typing import List


def part_1(commands: List[str]) -> int:
    pos = 0
    depth = 0
    for cmd in commands:
        direction, count_ = cmd.split()
        count = int(count_)
        if direction == "down":
            depth += count
        if direction == "up":
            depth -= count
        if direction == "forward":
            pos += count
    return pos * depth


def part_2(commands: List[str]) -> int:
    pos = 0
    depth = 0
    aim = 0
    for cmd in commands:
        direction, count_ = cmd.split()
        count = int(count_)
        if direction == "down":
            aim += count
        if direction == "up":
            aim -= count
        if direction == "forward":
            pos += count
            depth += aim * count
    return pos * depth
