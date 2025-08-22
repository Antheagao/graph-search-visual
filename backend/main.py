from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from utils import create_grid
from algorithms import bfs


app = FastAPI() 


# Enable cors for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

# map each algorithm call
algorithm_map = {
    "bfs": bfs.bfs
}

# Define request model
class GridRequest(BaseModel):
    mode: Literal["random", "custom"]
    algorithm: str
    rows: int | None = None
    cols: int | None = None
    start: tuple[int, int] | None = None
    end: tuple[int, int] | None = None


# Endpoint to generate and solve graph search
@app.post("/solve")
def solve_graph(request: GridRequest):
    # Generate grid
    try:
        grid = create_grid(
            request.mode, 
            request.algorithm, 
            request.rows,
            request.cols,
            request.start,
            request.end
        )
    except ValueError as e: 
            raise HTTPException(status_code=400, detail=str(e))
    
    retult = algorithm_map[request.algorithm](grid, request.start, request.end)
    
    return {
        
    }