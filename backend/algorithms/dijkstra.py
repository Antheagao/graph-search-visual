from typing import List, Tuple
from collections import deque
import time

def dijkstra():
    def is_valid(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n and grid[row][col] == 0
    
    # if no path
    end_time = time.time()
    return {
        "found": False,
        "time_taken": end_time - start_time,
        "nodes_expanded": nodes_expanded,
        "path": [],
        "visited": visited_order  
    }
