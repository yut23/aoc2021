from collections import defaultdict
from typing import Counter, Dict, Iterator, List

Node = int
START = 0
END = 1
FIRST_BIG = START - 1
FIRST_SMALL = END + 1

node_ids = {"start": START, "end": END}
next_big = FIRST_BIG
next_small = FIRST_SMALL


def lookup(name: str) -> Node:
    global next_big, next_small  # pylint: disable=global-statement
    if name not in node_ids:
        if name.isupper():
            node_ids[name] = next_big
            next_big -= 1
        else:
            node_ids[name] = next_small
            next_small += 1
    return node_ids[name]


def is_big(node: Node) -> bool:
    return node <= FIRST_BIG


# Node = str
# START = "start"
# END = "end"

# def lookup(name: str) -> Node:
#     return name


# def is_big(node: Node) -> bool:
#     return node.isupper()


class Graph:
    """Just an adjacency list."""

    def __init__(self) -> None:
        self._adj: Dict[Node, List[Node]] = defaultdict(list)

    def add_edge(self, a: str, b: str) -> None:
        u = lookup(a)
        v = lookup(b)
        # don't allow backtracking to start
        if v != START:
            self._adj[u].append(v)
        if u != START:
            self._adj[v].append(u)

    def __getitem__(self, u: Node) -> Iterator[Node]:
        return iter(self._adj[u])

    def __iter__(self) -> Iterator[Node]:
        return iter(self._adj)


def parse(lines: List[str]) -> Graph:
    G = Graph()
    for line in lines:
        u, v = line.split("-")
        G.add_edge(u, v)
    return G


def dfs_step(G: Graph, path: List[Node], can_visit_twice: bool = False) -> int:
    """Recursive DFS to count all paths through the graph."""
    count = 0
    node = path[-1]
    for u in G[node]:
        if u == END:
            count += 1
        elif is_big(u) or u not in path:
            count += dfs_step(G, [*path, u], can_visit_twice)
        elif can_visit_twice:
            count += dfs_step(G, [*path, u], False)
    return count


def dfs_iter(G: Graph, can_visit_twice: bool) -> int:
    """Iterative DFS to count all paths through the graph."""
    count = 0
    path = [START]
    iter_stack = [G[path[0]]]
    seen_count = Counter(path)
    while iter_stack:
        neighbors = iter_stack[-1]
        u = next(neighbors, None)
        if u is None:
            # out of neighbors
            iter_stack.pop(-1)
            prev = path.pop(-1)
            if seen_count[prev] == 2 and not is_big(prev):
                can_visit_twice = True
            seen_count[prev] -= 1
        elif u == END:
            count += 1
        else:
            valid = False
            if is_big(u) or seen_count[u] == 0:
                valid = True
            elif can_visit_twice:
                valid = True
                can_visit_twice = False
            if valid:
                seen_count[u] += 1
                path.append(u)
                iter_stack.append(G[u])
    return count


def part_1(lines: List[str]) -> int:
    G = parse(lines)
    # return dfs_step(G, [START])
    return dfs_iter(G, False)


def part_2(lines: List[str]) -> int:
    G = parse(lines)
    # return dfs_step(G, [START], True)
    return dfs_iter(G, True)
