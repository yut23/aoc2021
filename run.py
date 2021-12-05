#!/usr/bin/env python3

import argparse
import datetime
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
TODAY = datetime.datetime.now().day

# add the source directory to the beginning of Python's search path
sys.path.insert(0, str(ROOT / "src"))


def main() -> None:
    parser = argparse.ArgumentParser()
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "-e",
        "--example",
        action="store_const",
        dest="input_dir",
        const="example",
        default="input",
        help="use the example input from the instructions",
    )
    input_group.add_argument(
        "-i",
        "--input",
        metavar="file",
        type=argparse.FileType("r"),
        help="override the input file",
    )
    parser.add_argument(
        "day",
        nargs=argparse.ZERO_OR_MORE,
        help="a day number to run (defaults to today)",
    )
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
        file = args.input
        if file is None:
            file = open(ROOT / args.input_dir / f"day{n}.txt")
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

        if i != len(days) - 1:
            print()


if __name__ == "__main__":
    main()
