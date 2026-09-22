from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_request_id_generated():
    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    request_id = response.headers.get(
        "X-Request-ID"
    )

    assert request_id
    assert len(request_id) > 0


def test_existing_request_id_preserved():
    response = client.get(
        "/health",
        headers={
            "X-Request-ID": (
                "retailops-test-123"
            ),
        },
    )

    assert response.status_code == 200

    assert (
        response.headers[
            "X-Request-ID"
        ]
        == "retailops-test-123"
    )


def test_request_ids_are_unique():
    first = client.get(
        "/health"
    )

    second = client.get(
        "/health"
    )

    assert (
        first.headers[
            "X-Request-ID"
        ]
        != second.headers[
            "X-Request-ID"
        ]
    )