"""Depth-First Search (DFS) pathfinding algorithm implementation.

DFS explores as far as possible along each branch before backtracking.
Note: DFS does not guarantee the shortest path.
"""

from typing import List, Tuple
import time


def dfs(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> dict:
    """Find a path from start to end using DFS algorithm.
    
    Args:
        grid: 2D list where 0 represents an open cell and 1 represents a wall
        start: Starting position as (row, col) tuple
        end: Target position as (row, col) tuple
        
    Returns:
        Dictionary containing:
        - found: Boolean indicating if a path was found
        - time_taken: Execution time in seconds
        - nodes_expanded: Number of nodes explored
        - path: List of (row, col) tuples representing a path (not necessarily shortest)
        - visited: List of (row, col) tuples in order of exploration
    """
    def is_valid(row: int, col: int) -> bool:
        """Check if a position is within grid bounds and not a wall."""
        return 0 <= row < m and 0 <= col < n and grid[row][col] == 0

    m, n = len(grid), len(grid[0])
    stack = [start]
    visited = set([start])
    parent = {start: None}  # Track path reconstruction
    visited_order = []
    nodes_expanded = 0
    start_time = time.time()

    # 4-directional movement: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while stack:
        row, col = stack.pop()
        visited_order.append((row, col))
        nodes_expanded += 1

        # Goal reached - reconstruct and return path
        if (row, col) == end:
            end_time = time.time()
            path = []
            curr = end
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return {
                "found": True,
                "time_taken": end_time - start_time,
                "nodes_expanded": nodes_expanded,
                "path": path,
                "visited": visited_order
            }

        # Explore neighbors (add to stack for later processing)
        for dx, dy in directions:
            next_row, next_col = row + dx, col + dy
            if is_valid(next_row, next_col) and (next_row, next_col) not in visited:
                stack.append((next_row, next_col))
                visited.add((next_row, next_col))
                parent[(next_row, next_col)] = (row, col)

    # No path found
    end_time = time.time()
    return {
        "found": False,
        "time_taken": end_time - start_time,
        "nodes_expanded": nodes_expanded,
        "path": [],
        "visited": visited_order
    }
