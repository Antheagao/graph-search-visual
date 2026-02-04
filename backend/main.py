"""FastAPI backend for graph search visualization.

This module provides a REST API endpoint for running pathfinding algorithms
on a grid-based graph and returning visualization data.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal, List, Dict

from algorithms import bfs, dfs, dijkstra, a_star, bi_bfs


app = FastAPI(title="Graph Search Visualizer API", version="1.0.0")


# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://graph-search-visual.vercel.app"],
    allow_origin_regex=r"^https://graph-search-visual.*\.vercel\.app$",
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Map algorithm names to their implementation functions
algorithm_map = {
    "BFS": bfs.bfs,
    "DFS": dfs.dfs,
    "Dijkstra": dijkstra.dijkstra,
    "A*": a_star.a_star,
    "Bidirectional BFS": bi_bfs.bidirectional_bfs,
}


class GridRequest(BaseModel):
    """Request model for pathfinding algorithm execution."""
    algorithm: Literal["BFS", "DFS", "Dijkstra", "A*", "Bidirectional BFS"] = Field(
        description="Algorithm to use for pathfinding"
    )
    rows: int = Field(gt=0, description="Number of rows in the grid")
    cols: int = Field(gt=0, description="Number of columns in the grid")
    start: Dict[str, int] = Field(description="Starting position {row, col}")
    end: Dict[str, int] = Field(description="Ending position {row, col}")
    grid: List[List[int]] = Field(
        description="Grid representation where 0=open, 1=wall"
    )


@app.post("/solve")
def solve_graph(request: GridRequest) -> Dict:
    """Solve a pathfinding problem using the specified algorithm.
    
    Args:
        request: GridRequest containing algorithm, grid, and start/end positions
        
    Returns:
        Dictionary containing:
        - stats: Performance metrics (solved, time, nodesExpanded, pathLength)
        - path: List of (row, col) tuples representing the solution path
        - visited: List of (row, col) tuples representing visited nodes in order
        
    Raises:
        HTTPException: If the algorithm execution fails or input is invalid
    """
    # Validate grid dimensions match request
    if len(request.grid) != request.rows or any(
        len(row) != request.cols for row in request.grid
    ):
        raise HTTPException(
            status_code=400,
            detail="Grid dimensions do not match specified rows and cols"
        )
    
    # Extract and validate start/end positions
    try:
        start = (request.start["row"], request.start["col"])
        end = (request.end["row"], request.end["col"])
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required position field: {e}"
        )
    
    # Validate positions are within grid bounds
    if not (0 <= start[0] < request.rows and 0 <= start[1] < request.cols):
        raise HTTPException(status_code=400, detail="Start position out of bounds")
    if not (0 <= end[0] < request.rows and 0 <= end[1] < request.cols):
        raise HTTPException(status_code=400, detail="End position out of bounds")
    
    # Validate start and end are not walls
    if request.grid[start[0]][start[1]] == 1:
        raise HTTPException(status_code=400, detail="Start position is a wall")
    if request.grid[end[0]][end[1]] == 1:
        raise HTTPException(status_code=400, detail="End position is a wall")
    
    # Execute the selected algorithm
    try:
        result = algorithm_map[request.algorithm](
            request.grid,
            start,
            end
        )
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown algorithm: {request.algorithm}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Algorithm execution failed: {str(e)}"
        )
    
    return {
        "stats": {
            "solved": result.get("found", False),
            "time": result.get("time_taken", 0),
            "nodesExpanded": result.get("nodes_expanded", 0),
            "pathLength": len(result.get("path", [])),
        },
        "path": result.get("path", []),
        "visited": result.get("visited", []),
    }

