from fastapi.testclient import TestClient

from src.api.app import app
from src.api.rate_limit import (
    rate_limiter,
)


client = TestClient(app)


def test_query_rate_limit():
    rate_limiter.clear()

    # Invalid request bodies avoid Groq execution,
    # but still exercise router-level dependencies.
    for _ in range(10):
        response = client.post(
            "/api/v1/query",
            json={},
        )

        assert response.status_code == 422

    response = client.post(
        "/api/v1/query",
        json={},
    )

    assert response.status_code == 429

    assert response.json() == {
        "detail": (
            "Too many requests. "
            "Please try again later."
        )
    }

    rate_limiter.clear()


def test_rate_limit_can_be_cleared():
    rate_limiter.clear()

    for _ in range(10):
        client.post(
            "/api/v1/query",
            json={},
        )

    rate_limiter.clear()

    response = client.post(
        "/api/v1/query",
        json={},
    )

    assert response.status_code == 422

    rate_limiter.clear()


def test_health_not_rate_limited():
    rate_limiter.clear()

    for _ in range(20):
        response = client.get(
            "/health"
        )

        assert response.status_code == 200

    rate_limiter.clear()


def test_skills_not_rate_limited():
    rate_limiter.clear()

    for _ in range(20):
        response = client.get(
            "/api/v1/skills"
        )

        assert response.status_code == 200

    rate_limiter.clear()