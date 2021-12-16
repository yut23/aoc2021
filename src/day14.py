from collections import Counter
from typing import Dict, List, Tuple

Pair = Tuple[str, str]


# We can use a similar trick as day 6, by just tracking the counts for each pair,
# and ignoring the order within the template.
# This is possible because each replacement leaves the outer elements unchanged:
#    ... N C ... => ... N B C ...

# We can get the element counts from the pair counts, since each element will
# show up in exactly two pairs. We just count up all the elements in each pair
# and divide by 2. This works for everything but the elements on the ends of the
# template, since those only appear once. We can store those and add an extra
# occurrence of each to the raw counts, which fixes the total counts.


class Polymer:
    def __init__(self, lines: List[str]):
        # the number of occurrences of each pair of elements in the polymer
        self.pairs: Counter[Pair] = Counter(zip(lines[0], lines[0][1:]))
        # these are needed for calculating the score
        self.ends: Tuple[str, str] = lines[0][0], lines[0][-1]

        self.replacements: Dict[Pair, List[Pair]] = {}
        for line in lines[2:]:
            pair, _, insert = line.partition(" -> ")
            first, second = tuple(pair)
            self.replacements[first, second] = [(first, insert), (insert, second)]

    def update(self) -> None:
        changes: Counter[Pair] = Counter()
        changes.subtract(self.pairs)
        for pair, count in self.pairs.items():
            first, second = self.replacements[pair]
            changes[first] += count
            changes[second] += count
        self.pairs.update(changes)

    def score(self) -> int:
        # add an extra occurence for the ends, so we can cleanly divide by 2
        elements = Counter(self.ends)
        for (first, second), count in self.pairs.items():
            elements[first] += count
            elements[second] += count
        ordered = elements.most_common()
        return (ordered[0][1] - ordered[-1][1]) // 2


def part_1(lines: List[str]) -> int:
    polymer = Polymer(lines)
    for _ in range(10):
        polymer.update()
    return polymer.score()


def part_2(lines: List[str]) -> int:
    polymer = Polymer(lines)
    for _ in range(40):
        polymer.update()
    return polymer.score()
