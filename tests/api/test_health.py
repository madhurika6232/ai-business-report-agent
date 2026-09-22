from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": "RetailOps AI",
    }


def test_readiness_endpoint():
    response = client.get(
        "/ready"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ready",
        "service": "RetailOps AI",
    }


def test_openapi_available():
    response = client.get(
        "/openapi.json"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["info"]["title"]
        == "RetailOps AI API"
    )

    assert (
        data["info"]["version"]
        == "1.0.0"
    )


def test_swagger_docs_available():
    response = client.get(
        "/docs"
    )

    assert response.status_code == 200

    assert (
        "swagger"
        in response.text.lower()
    )

import pytest

from src.api.config import (
    validate_production_config,
)


def test_readiness_validation_allows_development():
    validate_production_config()


def test_readiness_validation_rejects_invalid_environment(
    monkeypatch,
):
    monkeypatch.setenv(
        "RETAILOPS_ENV",
        "invalid",
    )

    with pytest.raises(
        ValueError,
        match="RETAILOPS_ENV",
    ):
        validate_production_config()