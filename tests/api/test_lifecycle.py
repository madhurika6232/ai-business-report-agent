from fastapi.testclient import TestClient

from src.api.app import create_app

from src.memory.store import (
    memory_store,
)


def test_application_starts():
    app = create_app()

    with TestClient(app) as client:
        response = client.get(
            "/health"
        )

        assert response.status_code == 200


def test_memory_cleared_on_shutdown():
    memory_store.clear()

    app = create_app()

    with TestClient(app):
        memory_store.get_or_create(
            "lifecycle-test"
        )

        assert (
            memory_store.get(
                "lifecycle-test"
            )
            is not None
        )

    assert (
        memory_store.get(
            "lifecycle-test"
        )
        is None
    )


def test_lifecycle_preserves_request_handling():
    app = create_app()

    with TestClient(app) as client:
        health = client.get(
            "/health"
        )

        ready = client.get(
            "/ready"
        )

        assert health.status_code == 200
        assert ready.status_code == 200