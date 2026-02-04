"""Bidirectional Breadth-First Search (Bidirectional BFS) implementation.

Bidirectional BFS searches from both start and end simultaneously, meeting in the middle.
This can be more efficient than standard BFS, especially when the solution path is long.
"""

from typing import List, Tuple
from collections import deque
import time


def bidirectional_bfs(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> dict:
    """Find the shortest path from start to end using Bidirectional BFS algorithm.
    
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
    # 4-directional movement: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Two queues for bidirectional search
    start_queue = deque([start])
    end_queue = deque([end])

    # Track visited nodes and parent pointers for path reconstruction
    start_visited = {start: None}
    end_visited = {end: None}

    visited_order = []
    nodes_expanded = 0
    start_time = time.time()

    def reconstruct_path(meeting_point: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Reconstruct the full path from start to end through the meeting point."""
        path = []
        # Build path from start to meeting point
        curr = meeting_point
        while curr is not None:
            path.append(curr)
            curr = start_visited[curr]
        path.reverse()
        # Build path from meeting point to end
        curr = end_visited[meeting_point]
        while curr is not None:
            path.append(curr)
            curr = end_visited[curr]
        return path

    while start_queue and end_queue:
        # Expand from start side
        row, col = start_queue.popleft()
        nodes_expanded += 1
        visited_order.append((row, col))

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if is_valid(nr, nc) and (nr, nc) not in start_visited:
                start_queue.append((nr, nc))
                start_visited[(nr, nc)] = (row, col)
                # Check if we've met the search from the end
                if (nr, nc) in end_visited:
                    end_time = time.time()
                    return {
                        "found": True,
                        "time_taken": end_time - start_time,
                        "nodes_expanded": nodes_expanded,
                        "path": reconstruct_path((nr, nc)),
                        "visited": visited_order
                    }

        # Expand from end side
        row, col = end_queue.popleft()
        nodes_expanded += 1
        visited_order.append((row, col))

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if is_valid(nr, nc) and (nr, nc) not in end_visited:
                end_queue.append((nr, nc))
                end_visited[(nr, nc)] = (row, col)
                # Check if we've met the search from the start
                if (nr, nc) in start_visited:
                    end_time = time.time()
                    return {
                        "found": True,
                        "time_taken": end_time - start_time,
                        "nodes_expanded": nodes_expanded,
                        "path": reconstruct_path((nr, nc)),
                        "visited": visited_order
                    }

    # No path found
    end_time = time.time()
    return {
        "found": False,
        "time_taken": end_time - start_time,
        "nodes_expanded": nodes_expanded,
        "path": [],
        "visited": visited_order
    }
