from fastapi.testclient import TestClient

from api import app

client = TestClient(app)
GOAL = {"name": "t", "target": 2_000_000, "years": 8, "sip": 25000, "savings": 0,
        "step_up": 0.05, "inflate": True}


def test_simulate_returns_what_the_frontend_needs():
    r = client.post("/api/simulate", json={"goal": GOAL, "others": [GOAL]})
    assert r.status_code == 200
    d = r.json()
    assert 0 <= d["prob"] <= 1
    assert len(d["bands"]) == 5 and len(d["bands"][0]) == 8 * 12 + 1
    assert d["bands"][0][-1] <= d["bands"][2][-1] <= d["bands"][4][-1]
    assert len(d["others"]) == 1


def test_rejects_bad_input():
    assert client.post("/api/simulate", json={"goal": {**GOAL, "years": 99}}).status_code == 422
    assert client.post("/api/simulate", json={"goal": GOAL, "risk": "wild"}).status_code == 422


def test_serves_the_frontend():
    r = client.get("/")
    assert r.status_code == 200 and "Goal Planner" in r.text
