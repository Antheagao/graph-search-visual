"""A* pathfinding algorithm implementation.

A* is an informed search algorithm that uses both the actual cost from start (g-score)
and an estimated cost to the goal (h-score) to find the optimal path efficiently.
"""

from typing import List, Tuple
import heapq
import time


def a_star(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> dict:
    """Find the shortest path from start to end using A* algorithm.
    
    Args:
        grid: 2D list where 0 represents an open cell and 1 represents a wall
        start: Starting position as (row, col) tuple
        end: Target position as (row, col) tuple
        
    Returns:
        Dictionary containing:
        - found: Boolean indicating if a path was found
        - time_taken: Execution time in seconds
        - nodes_expanded: Number of nodes explored
        - path: List of (row, col) tuples representing the optimal path
        - visited: List of (row, col) tuples in order of exploration
    """
    def is_valid(row: int, col: int) -> bool:
        """Check if a position is within grid bounds and not a wall."""
        return 0 <= row < m and 0 <= col < n and grid[row][col] == 0

    def heuristic(r: int, c: int) -> int:
        """Calculate Manhattan distance heuristic (admissible for grid movement)."""
        return abs(r - end[0]) + abs(c - end[1])

    m, n = len(grid), len(grid[0])
    visited_order = []
    nodes_expanded = 0
    start_time = time.time()

    # Priority queue: (f_score, g_score, position)
    # f_score = g_score + heuristic (total estimated cost)
    open_set = []
    heapq.heappush(open_set, (heuristic(*start), 0, start))
    came_from = {start: None}  # Track path reconstruction
    g_score = {start: 0}  # Actual cost from start to each node
    visited = set()  # Closed set - nodes already explored

    # 4-directional movement: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        
        # Skip if already processed (can happen with duplicate entries in heap)
        if current in visited:
            continue
            
        nodes_expanded += 1
        visited_order.append(current)
        visited.add(current)

        # Goal reached - reconstruct and return path
        if current == end:
            path = []
            node = end
            while node is not None:
                path.append(node)
                node = came_from[node]
            path.reverse()
            end_time = time.time()
            return {
                "found": True,
                "time_taken": end_time - start_time,
                "nodes_expanded": nodes_expanded,
                "path": path,
                "visited": visited_order
            }

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)
            
            # Skip invalid positions or already visited nodes
            if not is_valid(nr, nc) or neighbor in visited:
                continue

            # Calculate new g_score (cost from start to neighbor)
            tentative_g = current_g + 1
            
            # If we found a better path to this neighbor, update it
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(nr, nc)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    # No path found
    end_time = time.time()
    return {
        "found": False,
        "time_taken": end_time - start_time,
        "nodes_expanded": nodes_expanded,
        "path": [],
        "visited": visited_order
    }
