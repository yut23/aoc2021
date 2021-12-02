#!/usr/bin/env python3

import datetime
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

today = datetime.datetime.now().day

if len(sys.argv) >= 2:
    if sys.argv[1] == "all":
        days = list(range(1, today + 1))
    else:
        days = [int(x) for x in sys.argv[1:]]
else:
    days = [today]

# add the source directory to the beginning of Python's search path
sys.path.insert(0, str(ROOT / "src"))

for i, n in enumerate(days):
    with open(ROOT / f"input/day{n}.txt") as f:
        lines = list(f)

    day = importlib.import_module(f"day{n}")

    print(f"Day {n}")
    if hasattr(day, "part_1"):
        answer = day.part_1(lines)  # type: ignore
        print(f"Part 1: {answer}")

    if hasattr(day, "part_2"):
        answer = day.part_2(lines)  # type: ignore
        print(f"Part 2: {answer}")

    if i != len(days) - 1:
        print()
