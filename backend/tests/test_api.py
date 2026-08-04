"""Smoke test for the POST /solve endpoint (backend/main.py)."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_solve_happy_path():
    payload = {
        "algorithm": "BFS",
        "rows": 3,
        "cols": 3,
        "start": {"row": 0, "col": 0},
        "end": {"row": 2, "col": 2},
        "grid": [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
    }
    response = client.post("/solve", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["stats"]["solved"] is True
    assert body["path"][0] == [0, 0]
    assert body["path"][-1] == [2, 2]


def test_solve_rejects_mismatched_grid_dimensions():
    payload = {
        "algorithm": "BFS",
        "rows": 3,
        "cols": 3,
        "start": {"row": 0, "col": 0},
        "end": {"row": 1, "col": 1},
        "grid": [
            [0, 0],
            [0, 0],
        ],
    }
    response = client.post("/solve", json=payload)

    assert response.status_code == 400
    assert "dimensions" in response.json()["detail"].lower()
