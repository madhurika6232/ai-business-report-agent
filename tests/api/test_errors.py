from fastapi import APIRouter
from fastapi.testclient import TestClient

from src.api.app import create_app


def build_error_test_client():
    app = create_app()

    test_router = APIRouter()

    @test_router.get(
        "/test/internal-error"
    )
    def internal_error():
        raise RuntimeError(
            r"Failed reading "
            r"C:\Users\madhu\secret\data.csv "
            r"api_key=super-secret-value"
        )

    app.include_router(
        test_router
    )

    return TestClient(
        app,
        raise_server_exceptions=False,
    )


def test_internal_error_is_sanitized():
    client = build_error_test_client()

    response = client.get(
        "/test/internal-error"
    )

    assert response.status_code == 500

    data = response.json()

    assert (
        data["error"]
        == "internal_error"
    )

    assert (
        "super-secret-value"
        not in data["detail"]
    )

    assert (
        "api_key"
        not in data["detail"]
    )

    assert (
        "C:\\Users"
        not in data["detail"]
    )


def test_internal_error_does_not_expose_traceback():
    client = build_error_test_client()

    response = client.get(
        "/test/internal-error"
    )

    body = response.text.lower()

    assert "traceback" not in body

    assert (
        "runtimeerror"
        not in body
    )


def test_known_http_errors_remain_404():
    client = TestClient(
        create_app()
    )

    response = client.get(
        "/api/v1/sessions/not-found"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Session not found."
    }