from typing import Generator, List

import networkx as nx


def parse(lines: List[str]) -> nx.Graph:
    G = nx.Graph()
    for line in lines:
        u, v = line.split("-")
        G.add_edge(u, v)
    return G


def dfs_step(
    G: nx.Graph, path: List[str], small_twice: str = ""
) -> Generator[List[str], None, None]:
    """Recursive DFS to find all paths through the graph."""
    node = path[-1]
    for u in G.neighbors(node):
        if u == "end":
            # ensure small_twice appears in the path exactly twice, if it's not empty
            if small_twice and path.count(small_twice) != 2:
                continue
            yield [*path, u]
            continue
        if u.islower() and u in path:
            if u == small_twice and path.count(u) < 2:
                pass
            else:
                continue
        yield from dfs_step(G, [*path, u], small_twice)


def part_1(lines: List[str]) -> int:
    G = parse(lines)
    paths = list(dfs_step(G, ["start"]))
    return len(paths)


def part_2(lines: List[str]) -> int:
    G = parse(lines)
    paths = list(dfs_step(G, ["start"]))
    small_caves = [u for u in G if u.islower() and u not in {"start", "end"}]
    for small in small_caves:
        paths.extend(dfs_step(G, ["start"], small))
    # for path in sorted(paths):
    #     print(",".join(path))
    return len(paths)
