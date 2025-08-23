from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal, List
from algorithms import bfs, dfs, dijkstra, a_star


app = FastAPI() 


# Enable cors for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# map each algorithm call
algorithm_map = {
    "BFS": bfs.bfs,
    "DFS": dfs.dfs,
    "Dijkstra": dijkstra.dijkstra,
    "A*": a_star.a_star,
}

# Define request model
class GridRequest(BaseModel):
    algorithm: Literal["BFS", "DFS", "Dijkstra", "A*"]
    rows: int
    cols: int
    start: dict
    end: dict 
    grid: List[List[int]]


# Endpoint to generate and solve graph search
@app.post("/solve")
def solve_graph(request: GridRequest):
    start = (request.start["row"], request.start["col"])
    end = (request.end["row"], request.end["col"])
    
    try:
        result = algorithm_map[request.algorithm](
            request.grid,
            start,
            end
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
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

