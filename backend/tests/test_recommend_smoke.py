"""Smoke tests for recommendation endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_recommendation_smoke():
    r = client.get("/api/v1/recommend/?risk=balanced&amount=10000")
    assert r.status_code == 200
    data = r.json()
    assert "allocation_weights" in data
    assert "signals" in data
