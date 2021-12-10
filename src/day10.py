from typing import Deque, List, Tuple

MARKERS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
CORRUPT_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
COMPLETE_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def check_line(line: str) -> Tuple[bool, str]:
    """Parses a line of the navigation subsystem.

    Returns:
        (False, bad character) if the line is corrupted.
        (True, missing characters) if the line is incomplete.
    """
    marker_stack: Deque[str] = Deque()
    for char in line:
        if char in MARKERS:
            # opener
            marker_stack.appendleft(MARKERS[char])
        else:
            # closer
            if marker_stack.popleft() != char:
                return False, char
    return True, "".join(marker_stack)


def part_1(lines: List[str]) -> int:
    score = 0
    for line in lines:
        valid, bad_char = check_line(line)
        if not valid:
            score += CORRUPT_POINTS[bad_char]
    return score


def part_2(lines: List[str]) -> int:
    scores = []
    for line in lines:
        score = 0
        valid, missing = check_line(line)
        if not valid:
            continue
        for char in missing:
            score *= 5
            score += COMPLETE_POINTS[char]
        scores.append(score)
    scores.sort()
    return scores[len(scores) // 2]
