import bisect
import builtins
import copy
import itertools
import re
from functools import cached_property
from typing import Any, Iterator, List, NamedTuple, Tuple, TypeVar, Union, cast

PROFILING = "profile" in dir(builtins)
if not PROFILING:
    # for line profiler
    T = TypeVar("T")

    def profile(func: T) -> T:
        return func


class Range(NamedTuple):
    lo: int
    hi: int

    def __iter__(self) -> Iterator[int]:
        yield self.lo
        yield self.hi

    def __contains__(self, point: Any) -> bool:
        return bool(self.lo <= point <= self.hi)

    @cached_property
    def length(self) -> int:
        assert self.hi >= self.lo
        return self.hi - self.lo + 1


class Cuboid(NamedTuple):
    x: Range
    y: Range
    z: Range

    @cached_property
    def bounds(self) -> Tuple[Range, Range, Range]:
        return self.x, self.y, self.z

    def __iter__(self) -> Iterator[Range]:
        return iter(self.bounds)

    def slices(self, bounding_box: "Cuboid") -> Tuple[slice, slice, slice]:
        return tuple(  # type: ignore
            slice(bb.lo + rng.lo, bb.lo + rng.hi + 1)
            for rng, bb in zip(self, bounding_box)
        )

    def volume(self) -> int:
        return self.x.length * self.y.length * self.z.length


class ITree:
    "Holds axis-aligned planes that split the contained space into multiple sections."

    def __init__(self, axis: int = 0):
        self.axis = axis
        self.splits: List[int] = []
        self.values: List[Union[ITree, bool]] = [
            ITree(self.axis + 1) if self.axis < 2 else False
        ]

    def count_on(self) -> int:
        total = 0
        for i in range(1, len(self.values) - 1):
            length = self.splits[i] - self.splits[i - 1]
            if self.axis == 2:
                val = int(cast(bool, self.values[i]))
            else:
                val = cast(ITree, self.values[i]).count_on()
            total += val * length
        return total

    def __str__(self) -> str:
        out = []
        for pos, value in zip(itertools.chain([None], self.splits), self.values):
            if pos is not None:
                out.append("xyz"[self.axis] + f"={pos}")
            out.extend("  |  " + l for l in str(value).splitlines())
        return "\n".join(out)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ITree):
            return NotImplemented
        return (
            self.axis == other.axis
            and self.splits == other.splits
            and self.values == other.values
        )

    @profile
    def update(self, state: bool, cuboid: Cuboid) -> None:
        lo, hi = cuboid[self.axis]
        lo_idx = self._split(lo)
        hi_idx = self._split(hi + 1)

        # update the contained values with `state`
        for i in range(lo_idx + 1, hi_idx + 1):
            if self.axis == 2:
                self.values[i] = state
            else:
                cast(ITree, self.values[i]).update(state, cuboid)

        # merge identical sections
        for i in range(len(self.splits))[::-1]:
            if self.values[i + 1] == self.values[i]:
                del self.splits[i]
                del self.values[i]

    @profile
    def _split(self, pos: int) -> int:
        index = bisect.bisect(self.splits, pos)
        if index >= len(self.splits) or self.splits[index] != pos:
            self.splits.insert(index, pos)
            # insert a copy of the indexed value right after it
            value = copy.deepcopy(self.values[index])
            self.values.insert(index + 1, value)
        return index


def parse(lines: List[str]) -> List[Tuple[bool, Cuboid]]:
    steps = []
    for line in lines:
        action, rest = line.split(" ")
        parts = re.findall(r"[xyz]=(-?\d+)\.\.(-?\d+)", rest)
        coords = []
        for start, end in parts:
            coords.append(Range(int(start), int(end)))
        # pylint: disable-next=no-value-for-parameter
        steps.append((action == "on", Cuboid(*coords)))
    return steps


def part_1(lines: List[str]) -> int:
    steps = parse(lines)
    init_range = Range(-50, 50)

    itree = ITree()
    for state, cuboid in steps:
        if all(
            cuboid[i].lo in init_range and cuboid[i].hi in init_range for i in range(3)
        ):
            itree.update(state, cuboid)

    return itree.count_on()


def part_2(lines: List[str]) -> int:
    steps = parse(lines)

    itree = ITree()
    for state, cuboid in steps:
        itree.update(state, cuboid)

    return itree.count_on()
