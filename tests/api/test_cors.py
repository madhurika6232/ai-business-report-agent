from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_allowed_cors_origin():
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200

    assert (
        response.headers.get(
            "access-control-allow-origin"
        )
        == "http://localhost:3000"
    )


def test_second_allowed_cors_origin():
    response = client.options(
        "/health",
        headers={
            "Origin": "http://127.0.0.1:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200

    assert (
        response.headers.get(
            "access-control-allow-origin"
        )
        == "http://127.0.0.1:3000"
    )


def test_disallowed_cors_origin():
    response = client.options(
        "/health",
        headers={
            "Origin": "http://evil.example.com",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert (
        response.headers.get(
            "access-control-allow-origin"
        )
        is None
    )


def test_cors_allowed_methods():
    response = client.options(
        "/api/v1/query",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200

    allowed_methods = (
        response.headers.get(
            "access-control-allow-methods",
            "",
        )
    )

    assert "GET" in allowed_methods
    assert "POST" in allowed_methods
    assert "DELETE" in allowed_methods