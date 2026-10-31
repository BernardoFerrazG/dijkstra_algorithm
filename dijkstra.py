"""Single-source shortest paths with Dijkstra's algorithm.

The graph is read from a weighted edge list (``source target weight`` per line)
and the algorithm itself is implemented from scratch with a binary heap;
NetworkX is used only as the graph container and for drawing.
"""

from __future__ import annotations

import argparse
import heapq
import math
from collections.abc import Hashable

import networkx as nx

Node = Hashable


def load_graph(path: str) -> nx.DiGraph:
    """Read a directed, weighted graph from an edge-list file."""
    return nx.read_weighted_edgelist(path, create_using=nx.DiGraph)


def dijkstra(graph: nx.DiGraph, source: Node) -> tuple[dict[Node, float], dict[Node, Node | None]]:
    """Compute shortest distances from ``source`` to every node.

    Returns ``(distances, predecessors)``. Unreachable nodes have distance
    ``math.inf`` and predecessor ``None``.

    Runs in O((V + E) log V) using a min-heap with lazy deletion.
    """
    if source not in graph:
        raise KeyError(f"source node {source!r} is not in the graph")

    distances: dict[Node, float] = {node: math.inf for node in graph.nodes}
    predecessors: dict[Node, Node | None] = {node: None for node in graph.nodes}
    distances[source] = 0.0

    heap: list[tuple[float, int, Node]] = [(0.0, 0, source)]
    counter = 1  # tie-breaker so nodes themselves never need to be comparable
    visited: set[Node] = set()

    while heap:
        distance, _, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)

        for neighbor, data in graph[node].items():
            weight = data.get("weight", 1.0)
            if weight < 0:
                raise ValueError("Dijkstra's algorithm requires non-negative edge weights")
            candidate = distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                predecessors[neighbor] = node
                heapq.heappush(heap, (candidate, counter, neighbor))
                counter += 1

    return distances, predecessors


def reconstruct_path(predecessors: dict[Node, Node | None], source: Node, target: Node) -> list[Node]:
    """Rebuild the path ``source -> target`` from the predecessor map (empty if unreachable)."""
    path = [target]
    while path[-1] != source:
        previous = predecessors[path[-1]]
        if previous is None:
            return []
        path.append(previous)
    return path[::-1]


def plot_graph(graph: nx.DiGraph) -> None:
    import matplotlib.pyplot as plt

    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=600)
    weights = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights, font_size=8)
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Shortest paths from a source vertex (Dijkstra).")
    parser.add_argument("source", nargs="?", help="source vertex (asked interactively if omitted)")
    parser.add_argument("-g", "--graph", default="graph.txt", help="edge-list file (default: graph.txt)")
    parser.add_argument("--no-plot", action="store_true", help="do not open the graph window")
    args = parser.parse_args()

    graph = load_graph(args.graph)
    source = args.source or input("Enter the source vertex: ").strip()
    if source not in graph:
        parser.error(f"vertex {source!r} not found; available: {', '.join(sorted(graph.nodes))}")

    distances, predecessors = dijkstra(graph, source)
    for target in sorted(graph.nodes, key=str):
        if math.isinf(distances[target]):
            print(f"{source} -> {target}: unreachable")
        else:
            path = " -> ".join(reconstruct_path(predecessors, source, target))
            print(f"{source} -> {target}: {path} (distance {distances[target]:g})")

    if not args.no_plot:
        plot_graph(graph)


if __name__ == "__main__":
    main()
