from typing import List, Tuple
import heapq
import time

def dijkstra(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
    def is_valid(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n and grid[row][col] == 0

    m, n = len(grid), len(grid[0])
    visited_order = []
    nodes_expanded = 0
    start_time = time.time()

    # min-heap: (distance, (row, col))
    heap = [(0, start)]
    distances = {start: 0}
    parent = {start: None}
    visited = set()

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    while heap:
        dist, (row, col) = heapq.heappop(heap)

        if (row, col) in visited:
            continue
        visited.add((row, col))
        visited_order.append((row, col))
        nodes_expanded += 1

        if (row, col) == end:
            end_time = time.time()
            # Reconstruct path
            path = []
            curr = end
            while curr:
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

        # check neighbors
        for dx, dy in directions:
            next_row, next_col = row + dx, col + dy
            if is_valid(next_row, next_col) and (next_row, next_col) not in visited:
                new_dist = dist + 1  # uniform cost of 1 per step
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
