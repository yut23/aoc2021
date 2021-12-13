from typing import Generator, List

import networkx as nx


def parse(lines: List[str]) -> nx.Graph:
    G = nx.Graph()
    for line in lines:
        u, v = line.split("-")
        G.add_edge(u, v)
    return G


def dfs_step(G: nx.Graph, path: List[str]) -> Generator[List[str], None, None]:
    node = path[-1]
    for u in G.neighbors(node):
        if u == "end":
            yield [*path, u]
            continue
        if u.islower() and u in path:
            continue
        yield from dfs_step(G, [*path, u])


def find_paths(G: nx.Graph) -> Generator[List[str], None, None]:
    """Recursive DFS to find all paths through the graph."""
    yield from dfs_step(G, ["start"])


def part_1(lines: List[str]) -> int:
    G = parse(lines)
    paths = list(find_paths(G))
    return len(paths)
