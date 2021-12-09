from typing import Dict, List, Set, Tuple

# 2 segments: 1
# 3 segments: 7
# 4 segments: 4
# 5 segments: 2 3 5
# 6 segments: 0 6 9
# 7 segments: 8

# we know 1 4 7 8
# we can distinguish between [2 3 5] and [0 6 9]

# |4 - 2| = 2 -> 2
# |3 - 1| = 3 -> 3
# other       -> 5

# |6 - 1| = 5 -> 6
# |4 - 9| = 0 -> 9
# other       -> 0


def identify_patterns(patterns: List[Set[str]]) -> Dict[str, int]:
    known = {}
    unknown = list()
    known_sizes = {2: 1, 3: 7, 4: 4, 7: 8}
    for p in patterns:
        size = len(p)
        if size in known_sizes:
            known[known_sizes[size]] = p
        else:
            unknown.append(p)

    for p in unknown:
        four_minus = len(known[4] - p)
        minus_one = len(p - known[1])
        size = len(p)

        # 2, 3, 5:
        if four_minus == 2:
            known[2] = p
        elif minus_one == 3:
            known[3] = p
        elif size == 5:
            known[5] = p

        # 0, 6, 9:
        elif minus_one == 5:
            known[6] = p
        elif four_minus == 0:
            known[9] = p
        elif size == 6:
            known[0] = p

    return {"".join(sorted(v)): k for k, v in known.items()}


def parse(lines: List[str]) -> Tuple[List[List[Set[str]]], List[List[str]]]:
    patterns = []
    digits = []
    for line in lines:
        ps, _, ds = line.partition(" | ")
        patterns.append([set(x) for x in ps.split()])
        # normalize pattern order
        digits.append(["".join(sorted(x)) for x in ds.split()])
    return patterns, digits


def part_1(lines: List[str]) -> int:
    _, all_digits = parse(lines)
    return sum(
        int(len(digit) in {2, 3, 4, 7}) for digits in all_digits for digit in digits
    )


def part_2(lines: List[str]) -> int:
    total = 0
    for patterns, digits in zip(*parse(lines)):
        lookup = identify_patterns(patterns)
        total += sum(lookup[digit] * 10 ** i for i, digit in enumerate(digits[::-1]))
    return total
