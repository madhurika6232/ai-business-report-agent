from fastapi.testclient import TestClient

from src.api.app import app
from src.api.security import (
    API_KEY_ENV,
)


client = TestClient(app)


def test_security_disabled_without_config(
    monkeypatch,
):
    monkeypatch.delenv(
        API_KEY_ENV,
        raising=False,
    )

    # Validation occurs after authentication.
    response = client.post(
        "/api/v1/query",
        json={},
    )

    assert response.status_code == 422


def test_missing_api_key_rejected(
    monkeypatch,
):
    monkeypatch.setenv(
        API_KEY_ENV,
        "test-secret-key",
    )

    response = client.post(
        "/api/v1/query",
        json={
            "query": "How is revenue?"
        },
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid or missing API key."
    }


def test_invalid_api_key_rejected(
    monkeypatch,
):
    monkeypatch.setenv(
        API_KEY_ENV,
        "test-secret-key",
    )

    response = client.post(
        "/api/v1/query",
        headers={
            "X-API-Key": "wrong-key",
        },
        json={
            "query": "How is revenue?"
        },
    )

    assert response.status_code == 401


def test_valid_key_reaches_endpoint_validation(
    monkeypatch,
):
    monkeypatch.setenv(
        API_KEY_ENV,
        "test-secret-key",
    )

    response = client.post(
        "/api/v1/query",
        headers={
            "X-API-Key": "test-secret-key",
        },
        json={},
    )

    # Authentication passed; request-body validation
    # then rejects the missing query.
    assert response.status_code == 422


def test_public_health_requires_no_key(
    monkeypatch,
):
    monkeypatch.setenv(
        API_KEY_ENV,
        "test-secret-key",
    )

    response = client.get(
        "/health"
    )

    assert response.status_code == 200


def test_public_skill_catalog_requires_no_key(
    monkeypatch,
):
    monkeypatch.setenv(
        API_KEY_ENV,
        "test-secret-key",
    )

    response = client.get(
        "/api/v1/skills"
    )

    assert response.status_code == 200