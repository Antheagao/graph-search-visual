"""Tests for the five pathfinding algorithms in backend/algorithms/.

All five expose the same signature:
    (grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> dict
returning {found, time_taken, nodes_expanded, path, visited}.

`time_taken` is never asserted on (it's a wall-clock measurement) and
`nodes_expanded` is never compared *across* algorithms (each counts
expansions using different bookkeeping - e.g. bidirectional BFS expands
from two frontiers). We only assert nodes_expanded > 0 when a path is found.
"""

from typing import Callable, Dict, List, Tuple

import pytest

from algorithms import a_star, bfs, bi_bfs, dfs, dijkstra

ALGORITHMS: Dict[str, Callable] = {
    "bfs": bfs.bfs,
    "dfs": dfs.dfs,
    "dijkstra": dijkstra.dijkstra,
    "a_star": a_star.a_star,
    "bi_bfs": bi_bfs.bidirectional_bfs,
}

# bfs, dijkstra, a_star, bi_bfs all guarantee shortest path on a uniform-cost
# grid; dfs explicitly does not.
SHORTEST_PATH_ALGORITHMS = {"bfs", "dijkstra", "a_star", "bi_bfs"}


def assert_contiguous_valid_path(
    path: List[Tuple[int, int]],
    grid: List[List[int]],
    start: Tuple[int, int],
    end: Tuple[int, int],
) -> None:
    """Assert a path starts at start, ends at end, never crosses a wall,
    and each step moves to a 4-directional neighbor."""
    assert path[0] == start
    assert path[-1] == end
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        assert abs(r1 - r2) + abs(c1 - c2) == 1, f"non-adjacent step {(r1, c1)} -> {(r2, c2)}"
        assert grid[r2][c2] == 0, f"path crosses wall at {(r2, c2)}"


@pytest.mark.parametrize("name", ALGORITHMS)
def test_empty_1x1_grid_start_equals_end(name):
    """A 1x1 open grid where start == end should be solved immediately.

    KNOWN BUG: bidirectional_bfs (backend/algorithms/bi_bfs.py) returns
    found=False here. It seeds start_visited={start: None} and
    end_visited={end: None} but never checks for that overlap before
    entering the main loop - it only checks for a meeting point when a
    *newly expanded neighbor* lands in the other side's visited set. Since
    a 1x1 grid has no neighbors to expand, the pre-existing overlap between
    start and end is never detected. This test pins current (buggy)
    behavior rather than fixing the algorithm - see final report.
    """
    grid = [[0]]
    start = end = (0, 0)
    fn = ALGORITHMS[name]
    result = fn(grid, start, end)

    assert result["visited"][0] == start

    if name == "bi_bfs":
        assert result["found"] is False
        assert result["path"] == []
    else:
        assert result["found"] is True
        assert result["path"] == [start]
        assert result["nodes_expanded"] > 0


@pytest.mark.parametrize("name", ALGORITHMS)
def test_simple_open_grid_finds_valid_path(name):
    grid = [[0] * 5 for _ in range(5)]
    start, end = (0, 0), (4, 4)
    fn = ALGORITHMS[name]
    result = fn(grid, start, end)

    assert result["found"] is True
    assert result["nodes_expanded"] > 0
    assert result["visited"][0] == start
    assert_contiguous_valid_path(result["path"], grid, start, end)


@pytest.mark.parametrize("name", ALGORITHMS)
def test_unreachable_end_walled_off(name):
    """End cell is open but fully enclosed by walls - no path exists."""
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    start, end = (0, 0), (2, 2)
    fn = ALGORITHMS[name]
    result = fn(grid, start, end)

    assert result["found"] is False
    assert result["path"] == []
    assert result["visited"][0] == start


@pytest.mark.parametrize("name", ALGORITHMS)
def test_start_on_a_wall_is_still_searched_from(name):
    """None of the algorithms validate the start cell against the grid -
    that validation lives in main.py (solve_graph rejects a walled start
    before calling the algorithm). Called directly, a walled start is
    still expanded from as if it were open. This pins that actual
    behavior, not an ideal one."""
    grid = [
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    start, end = (0, 0), (2, 2)
    fn = ALGORITHMS[name]
    result = fn(grid, start, end)

    assert result["found"] is True
    assert result["path"][0] == start
    assert result["path"][-1] == end


@pytest.mark.parametrize("name", ["bfs", "dfs", "dijkstra", "a_star"])
def test_end_on_a_wall_is_unreachable(name):
    """Unlike start, a walled end can never be reached: neighbor expansion
    always checks is_valid() (grid == 0) before a cell is queued, so a
    walled end is never added to the frontier via normal expansion."""
    grid = [
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    start, end = (0, 1), (0, 0)  # end sits on a wall
    fn = ALGORITHMS[name]
    result = fn(grid, start, end)

    assert result["found"] is False
    assert result["path"] == []


def test_bi_bfs_end_on_a_wall_is_reachable_unlike_the_others():
    """KNOWN QUIRK: bi_bfs seeds end_visited={end: None} directly, the
    same way it seeds start, so a walled end (like a walled start) is
    still treated as reachable - inconsistent with bfs/dfs/dijkstra/a_star
    above. This pins that actual, inconsistent behavior."""
    grid = [
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    start, end = (0, 1), (0, 0)
    result = bi_bfs.bidirectional_bfs(grid, start, end)

    assert result["found"] is True
    assert result["path"][0] == start
    assert result["path"][-1] == end


@pytest.mark.parametrize("name", sorted(SHORTEST_PATH_ALGORITHMS))
def test_shortest_path_length_with_forced_detour(name):
    """A wall column with a single gap at the bottom row forces a known
    6-step (7-node) detour from (0,0) to (0,2):

        0 1 0
        0 1 0
        0 0 0
    """
    grid = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    start, end = (0, 0), (0, 2)
    fn = ALGORITHMS[name]
    result = fn(grid, start, end)

    assert result["found"] is True
    assert len(result["path"]) == 7
    assert_contiguous_valid_path(result["path"], grid, start, end)


def test_dfs_finds_a_valid_but_not_necessarily_shortest_path():
    """DFS makes no shortest-path guarantee - only assert it finds *a*
    valid path through the same forced-detour grid used above."""
    grid = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    start, end = (0, 0), (0, 2)
    result = dfs.dfs(grid, start, end)

    assert result["found"] is True
    assert_contiguous_valid_path(result["path"], grid, start, end)
