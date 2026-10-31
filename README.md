# Dijkstra's Shortest Paths

[![CI](https://github.com/BernardoFerrazG/dijkstra_algorithm/actions/workflows/ci.yml/badge.svg)](https://github.com/BernardoFerrazG/dijkstra_algorithm/actions/workflows/ci.yml)

A from-scratch implementation of **Dijkstra's algorithm** for single-source shortest paths in a directed, weighted graph, with path reconstruction, a small CLI and graph visualisation.

NetworkX is used only as the graph container and for drawing — the algorithm itself is implemented by hand and validated against NetworkX's reference implementation in the test suite.

## How it works

1. Every vertex starts at distance `∞`, except the source (`0`).
2. A **min-heap** always yields the closest vertex not yet finalised.
3. Each outgoing edge `(u, v, w)` is *relaxed*: if `dist[u] + w < dist[v]`, the distance and predecessor of `v` are updated and `v` is pushed back onto the heap.
4. Stale heap entries are skipped (lazy deletion), so no decrease-key operation is needed.

| | |
| --- | --- |
| Time | `O((V + E) log V)` |
| Space | `O(V + E)` |
| Requirement | Non-negative edge weights (negative weights raise `ValueError`) |

## Usage

```bash
pip install -r requirements.txt
python dijkstra.py 1             # shortest paths from vertex 1
python dijkstra.py 1 --no-plot   # text output only
python dijkstra.py -g my_graph.txt A
```

The input is a whitespace-separated edge list, one `source target weight` per line (see [`graph.txt`](graph.txt)).

Example output:

```
1 -> 2: 1 -> 2 (distance 5)
1 -> 3: 1 -> 3 (distance 2)
1 -> 4: 1 -> 3 -> 4 (distance 5)
1 -> 5: 1 -> 2 -> 6 -> 5 (distance 20)
1 -> 6: 1 -> 2 -> 6 (distance 13)
1 -> 7: unreachable
1 -> 8: unreachable
```

## Tests

```bash
pip install pytest
pytest
```

The suite compares distances against `networkx.single_source_dijkstra_path_length` on the sample graph and on 20 random graphs, checks that every reconstructed path has exactly the reported weight, and covers invalid input. CI runs it on every push.

## Project structure

```
dijkstra.py          # algorithm, path reconstruction, CLI and plotting
graph.txt            # sample graph
tests/               # pytest suite
```
