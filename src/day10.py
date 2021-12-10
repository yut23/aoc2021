from typing import Deque, List, Optional

MARKERS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def check_line(line: str) -> Optional[str]:
    """Return the bad character if the line is corrupted, or None otherwise."""
    marker_stack: Deque[str] = Deque()
    for char in line:
        if char in MARKERS:
            # opener
            marker_stack.append(MARKERS[char])
        else:
            # closer
            if marker_stack.pop() != char:
                return char
    return None


def part_1(lines: List[str]) -> int:
    score = 0
    for line in lines:
        if (bad := check_line(line)) is not None:
            score += SCORES[bad]
    return score
