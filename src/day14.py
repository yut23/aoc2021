from collections import Counter
from typing import Dict, List, Tuple

# (first element, second element) -> inserted element
Rules = Dict[Tuple[str, str], str]


def parse(lines: List[str]) -> Tuple[List[str], Rules]:
    template = list(lines[0])
    rules: Rules = {}
    for line in lines[2:]:
        pair, _, insert = line.partition(" -> ")
        rules[pair[0], pair[1]] = insert
    return template, rules


def part_1(lines: List[str]) -> int:
    template, rules = parse(lines)
    # print(f"Template:     {''.join(template)}")
    for _ in range(10):
        to_insert = []
        for pair in zip(template, template[1:]):
            to_insert.append(rules[pair])
        # interleave to_insert with template
        new_template = template + to_insert
        new_template[::2] = template
        new_template[1::2] = to_insert
        template = new_template
        # print(f"After step {_ + 1}: {''.join(template)}")
    counts = sorted(Counter(template).values())
    return counts[-1] - counts[0]
