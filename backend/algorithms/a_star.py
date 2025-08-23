from typing import List, Tuple
import heapq
import time

def a_star(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
    def is_valid(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n and grid[row][col] == 0

    def heuristic(r: int, c: int) -> int:
        # Manhattan distance
        return abs(r - end[0]) + abs(c - end[1])

    m, n = len(grid), len(grid[0])
    visited_order = []
    nodes_expanded = 0
    start_time = time.time()

    open_set = []
    heapq.heappush(open_set, (heuristic(*start), 0, start))  # (f_score, g_score, position)
    came_from = {start: None}
    g_score = {start: 0}
    visited = set()

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        nodes_expanded += 1
        visited_order.append(current)

        if current == end:
            # Reconstruct path
            path = []
            node = end
            while node:
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

        visited.add(current)

        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)
            if not is_valid(nr, nc) or neighbor in visited:
                continue

            tentative_g = current_g + 1
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
