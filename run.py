#!/usr/bin/env python3

import argparse
import datetime
import importlib
import sys
from pathlib import Path
from typing import Optional, TextIO

ROOT = Path(__file__).parent.resolve()
TODAY = datetime.datetime.now().day

# add the source directory to the beginning of Python's search path
sys.path.insert(0, str(ROOT / "src"))


def run_day(n: int, file: Optional[TextIO] = None) -> None:
    if file is None:
        file = open(ROOT / f"input/day{n}.txt")  # pylint: disable=consider-using-with
    try:
        lines = file.read().splitlines(keepends=False)
    finally:
        file.close()

    day = importlib.import_module(f"day{n}")

    print(f"Day {n}")
    if hasattr(day, "part_1"):
        answer = day.part_1(lines)  # type: ignore
        print(f"Part 1: {answer}")

    if hasattr(day, "part_2"):
        answer = day.part_2(lines)  # type: ignore
        print(f"Part 2: {answer}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=argparse.FileType("r"), help="Override the input file"
    )
    parser.add_argument("day", nargs=argparse.ZERO_OR_MORE, help="What days to run")
    args = parser.parse_args()

    if args.day:
        if args.day[0] == "all":
            days = list(range(1, TODAY + 1))
        else:
            days = [int(x) for x in args.day]
    else:
        days = [TODAY]

    if len(days) > 1 and args.input is not None:
        parser.error("-i/--input cannot be used if multiple days are specified")

    for i, n in enumerate(days):
        run_day(n, args.input)
        if i != len(days) - 1:
            print()


if __name__ == "__main__":
    main()
