import re
from typing import List, NamedTuple, Optional, Set, Tuple


class Dot(NamedTuple):
    x: int
    y: int


class Fold(NamedTuple):
    axis: str
    position: int

    def apply(self, dot: Dot) -> Dot:
        if self.axis == "x":
            assert dot.x != self.position
            if dot.x < self.position:
                return dot
            return Dot(2 * self.position - dot.x, dot.y)
        elif self.axis == "y":
            assert dot.y != self.position
            if dot.y < self.position:
                return dot
            return Dot(dot.x, 2 * self.position - dot.y)
        assert False


def parse(lines: List[str]) -> Tuple[Set[Dot], List[Fold]]:
    dots = set()
    folds = []
    for line in lines:
        if m := re.match(r"fold along (x|y)=(\d+)", line):
            folds.append(Fold(m[1], int(m[2])))
        elif line:
            x, y = line.split(",")
            dots.add(Dot(int(x), int(y)))
    return dots, folds


def apply_fold(dots: Set[Dot], fold: Fold) -> Set[Dot]:
    new_dots = set()
    for dot in dots:
        new_dots.add(fold.apply(dot))
    return new_dots


def pretty(dots: Set[Dot], fold: Optional[Fold] = None, bg_char: str = ".") -> str:
    width = max(dot.x for dot in dots) + 1
    height = max(dot.y for dot in dots) + 1
    lines = [[bg_char] * width for _ in range(height)]
    for dot in dots:
        lines[dot.y][dot.x] = "#"
    if fold is not None:
        if fold.axis == "y":
            lines[fold.position] = ["-"] * width
        elif fold.axis == "x":
            for y in range(height):
                lines[y][fold.position] = "|"
    return "\n".join("".join(line) for line in lines)


def part_1(lines: List[str]) -> int:
    dots, folds = parse(lines)
    # print(",\n".join(map(str, sorted(dots))))
    # print("\n" + pretty(dots, folds[0]) + "\n")
    dots = apply_fold(dots, folds[0])
    # print(",\n".join(map(str, sorted(dots))))
    # print("\n" + pretty(dots, folds[1]) + "\n")
    return len(dots)


def part_2(lines: List[str]) -> str:
    dots, folds = parse(lines)
    for fold in folds:
        dots = apply_fold(dots, fold)
    return "\n" + pretty(dots, bg_char=" ")
