from typing import List, Set, Tuple


def parse(lines: List[str]) -> Tuple[List[List[Set[str]]], List[List[str]]]:
    patterns = []
    outputs = []
    for line in lines:
        ps, _, os = line.partition(" | ")
        patterns.append([set(x) for x in ps.split()])
        # normalize pattern order
        outputs.append(["".join(sorted(x)) for x in os.split()])
    return patterns, outputs


def part_1(lines: List[str]) -> int:
    _, all_outputs = parse(lines)
    return sum(
        int(len(output) in {2, 3, 4, 7})
        for outputs in all_outputs
        for output in outputs
    )
