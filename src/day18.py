import ast
from dataclasses import dataclass
from typing import Any, Iterable, Iterator, List, Optional, Tuple, Union


@dataclass
class Pair:
    left: Union[int, "Pair"]
    right: Union[int, "Pair"]

    def __getitem__(self, key):
        if isinstance(key, Iterable):
            idx, *rest = key
        else:
            idx = key
            rest = []
        val = self.right if idx else self.left
        if rest:
            assert isinstance(val, Pair)
            return val[rest]
        return val

    def __setitem__(self, key, val):
        if isinstance(key, Iterable):
            idx, *rest = key
        else:
            idx = key
            rest = []
        side = "right" if idx else "left"
        if rest:
            getattr(self, side)[rest] = val
        else:
            setattr(self, side, val)

    def paths(self) -> Iterator[Tuple[List[int], int]]:
        if isinstance(self.left, Pair):
            yield from (([0, *path], val) for path, val in self.left.paths())
        else:
            yield [0], self.left
        if isinstance(self.right, Pair):
            yield from (([1, *path], val) for path, val in self.right.paths())
        else:
            yield [1], self.right

    def __iter__(self) -> Iterator[int]:
        if isinstance(self.left, Pair):
            yield from self.left
        else:
            yield self.left
        if isinstance(self.right, Pair):
            yield from self.right
        else:
            yield self.right

    def __int__(self) -> int:
        return 3 * int(self.left) + 2 * int(self.right)


class Number:
    def __init__(self, pair: Pair):
        self.pair = pair
        self.reduce()

    def add(self, other: Pair) -> "Number":
        return Number(Pair(self.pair, other))

    def reduce(self) -> None:
        modified = True
        while modified:
            modified = False
            # find pairs nested more than 4 layers deep
            prev_path = None
            it = self.pair.paths()
            for path, _ in it:
                if len(path) > 4:
                    # second number in the pair
                    next(it)
                    # next number, if it exists
                    next_path, _ = next(it, (None, -1))
                    self.explode(path[:4], prev_path, next_path)
                    modified = True
                    break
                prev_path = path
            if modified:
                continue
            # find numbers >= 10
            for path, val in self.pair.paths():
                if val >= 10:
                    self.split(path, val)
                    modified = True
                    break

    def explode(
        self,
        path: List[int],
        prev_path: Optional[List[int]],
        next_path: Optional[List[int]],
    ) -> None:
        # print(f"explode at {path}")
        l, r = self.pair[path]
        if prev_path is not None:
            self.pair[prev_path] += l
        if next_path is not None:
            self.pair[next_path] += r
        self.pair[path] = 0

    def split(self, path: List[int], val: int) -> None:
        # print(f"split at {path}")
        l = val // 2
        r = val - l
        self.pair[path] = Pair(l, r)

    def magnitude(self) -> int:
        return int(self.pair)


def parse(lines: List[str]) -> List[Pair]:
    pairs: List[Pair] = []

    def helper(element: Any) -> Union[int, Pair]:
        if isinstance(element, int):
            return element
        assert isinstance(element, list)
        assert len(element) == 2
        l, r = element
        return Pair(helper(l), helper(r))

    for line in lines:
        lst = ast.literal_eval(line)
        pairs.append(helper(lst))  # type: ignore
    return pairs


def part_1(lines: List[str]) -> int:
    pairs = parse(lines)
    num = Number(pairs[0])
    for pair in pairs[1:]:
        num = num.add(pair)
    return num.magnitude()
