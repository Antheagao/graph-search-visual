"""Breadth-First Search (BFS) pathfinding algorithm implementation.

BFS explores all nodes at the current depth level before moving to the next level,
guaranteeing the shortest path in unweighted graphs.
"""

from typing import List, Tuple
from collections import deque
import time


def bfs(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> dict:
    """Find the shortest path from start to end using BFS algorithm.
    
    Args:
        grid: 2D list where 0 represents an open cell and 1 represents a wall
        start: Starting position as (row, col) tuple
        end: Target position as (row, col) tuple
        
    Returns:
        Dictionary containing:
        - found: Boolean indicating if a path was found
        - time_taken: Execution time in seconds
        - nodes_expanded: Number of nodes explored
        - path: List of (row, col) tuples representing the shortest path
        - visited: List of (row, col) tuples in order of exploration
    """
    def is_valid(row: int, col: int) -> bool:
        """Check if a position is within grid bounds and not a wall."""
        return 0 <= row < m and 0 <= col < n and grid[row][col] == 0
    
    m = len(grid)
    n = len(grid[0])
    # 4-directional movement: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    queue = deque([start])
    visited = set([start])
    parent = {start: None}  # Track path reconstruction
    
    nodes_expanded = 0
    visited_order = []  # Track the order of node expansion for visualization
    start_time = time.time()
    
    while queue:
        row, col = queue.popleft()
        nodes_expanded += 1
        visited_order.append((row, col))
        
        # Goal reached - reconstruct and return path
        if (row, col) == end:
            end_time = time.time()
            path = []
            curr = end
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            return {
                "found": True,
                "time_taken": end_time - start_time,
                "nodes_expanded": nodes_expanded,
                "path": path[::-1],
                "visited": visited_order
            }
        
        # Explore neighbors
        for dx, dy in directions:
            next_row, next_col = row + dx, col + dy
            if is_valid(next_row, next_col) and (next_row, next_col) not in visited:
                queue.append((next_row, next_col))
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
