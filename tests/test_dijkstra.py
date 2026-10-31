import math
import random
from pathlib import Path

import networkx as nx
import pytest

from dijkstra import dijkstra, load_graph, reconstruct_path

GRAPH_FILE = Path(__file__).resolve().parent.parent / "graph.txt"


def test_sample_graph_matches_networkx():
    graph = load_graph(GRAPH_FILE)
    for source in graph.nodes:
        distances, _ = dijkstra(graph, source)
        expected = nx.single_source_dijkstra_path_length(graph, source)
        for node in graph.nodes:
            assert distances[node] == pytest.approx(expected.get(node, math.inf))


def test_paths_are_consistent_with_distances():
    graph = load_graph(GRAPH_FILE)
    distances, predecessors = dijkstra(graph, "1")
    for target, distance in distances.items():
        path = reconstruct_path(predecessors, "1", target)
        if math.isinf(distance):
            assert path == []
        else:
            assert path[0] == "1" and path[-1] == target
            assert nx.path_weight(graph, path, "weight") == pytest.approx(distance)


@pytest.mark.parametrize("seed", range(20))
def test_random_graphs_match_networkx(seed):
    rng = random.Random(seed)
    graph = nx.gnp_random_graph(30, 0.15, seed=seed, directed=True)
    for u, v in graph.edges:
        graph[u][v]["weight"] = rng.randint(0, 20)

    distances, _ = dijkstra(graph, 0)
    expected = nx.single_source_dijkstra_path_length(graph, 0)
    for node in graph.nodes:
        assert distances[node] == expected.get(node, math.inf)


def test_unknown_source_raises():
    with pytest.raises(KeyError):
        dijkstra(load_graph(GRAPH_FILE), "99")


def test_negative_weight_raises():
    graph = nx.DiGraph()
    graph.add_edge("a", "b", weight=-1)
    with pytest.raises(ValueError):
        dijkstra(graph, "a")
