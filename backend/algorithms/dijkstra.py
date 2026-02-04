"""Dijkstra's pathfinding algorithm implementation.

Dijkstra's algorithm finds the shortest path in weighted graphs. For uniform
edge weights (as in this grid), it behaves similarly to BFS but uses a priority queue.
"""

from typing import List, Tuple
import heapq
import time


def dijkstra(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> dict:
    """Find the shortest path from start to end using Dijkstra's algorithm.
    
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

    m, n = len(grid), len(grid[0])
    visited_order = []
    nodes_expanded = 0
    start_time = time.time()

    # Min-heap: (distance, (row, col))
    heap = [(0, start)]
    distances = {start: 0}  # Shortest distance from start to each node
    parent = {start: None}  # Track path reconstruction
    visited = set()  # Closed set - nodes already processed

    # 4-directional movement: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while heap:
        dist, (row, col) = heapq.heappop(heap)

        # Skip if already processed (can happen with duplicate entries in heap)
        if (row, col) in visited:
            continue
        visited.add((row, col))
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

        # Explore neighbors
        for dx, dy in directions:
            next_row, next_col = row + dx, col + dy
            if is_valid(next_row, next_col) and (next_row, next_col) not in visited:
                new_dist = dist + 1  # Uniform cost of 1 per step
                # Update if we found a shorter path to this neighbor
                if (next_row, next_col) not in distances or new_dist < distances[(next_row, next_col)]:
                    distances[(next_row, next_col)] = new_dist
                    heapq.heappush(heap, (new_dist, (next_row, next_col)))
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
