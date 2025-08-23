from typing import List, Tuple
from collections import deque
import time

def bidirectional_bfs(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
    def is_valid(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n and grid[row][col] == 0

    m, n = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    start_queue = deque([start])
    end_queue = deque([end])

    start_visited = {start: None}
    end_visited = {end: None}

    visited_order = []
    nodes_expanded = 0
    start_time = time.time()

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
                if (nr, nc) in end_visited:
                    # Meeting point found, reconstruct path
                    path = []
                    # From start to meeting
                    curr = (nr, nc)
                    while curr:
                        path.append(curr)
                        curr = start_visited[curr]
                    path = path[::-1]
                    # From meeting to end
                    curr = end_visited[(nr, nc)]
                    while curr:
                        path.append(curr)
                        curr = end_visited[curr]
                    end_time = time.time()
                    return {
                        "found": True,
                        "time_taken": end_time - start_time,
                        "nodes_expanded": nodes_expanded,
                        "path": path,
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
                if (nr, nc) in start_visited:
                    # Meeting point found, reconstruct path
                    path = []
                    curr = (nr, nc)
                    while curr:
                        path.append(curr)
                        curr = start_visited[curr]
                    path = path[::-1]
                    curr = end_visited[(nr, nc)]
                    while curr:
                        path.append(curr)
                        curr = end_visited[curr]
                    end_time = time.time()
                    return {
                        "found": True,
                        "time_taken": end_time - start_time,
                        "nodes_expanded": nodes_expanded,
                        "path": path,
                        "visited": visited_order
                    }

    end_time = time.time()
    return {
        "found": False,
        "time_taken": end_time - start_time,
        "nodes_expanded": nodes_expanded,
        "path": [],
        "visited": visited_order
    }
