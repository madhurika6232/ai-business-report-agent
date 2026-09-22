from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_openapi_contains_expected_routes():
    response = client.get(
        "/openapi.json"
    )

    assert response.status_code == 200

    paths = response.json()[
        "paths"
    ]

    expected_paths = {
        "/health",
        "/ready",
        "/api/v1/query",
        "/api/v1/conversation",
        "/api/v1/sessions/{session_id}",
        "/api/v1/skills",
        "/api/v1/evaluation",
    }

    assert expected_paths.issubset(
        set(paths)
    )


def test_openapi_query_method():
    schema = app.openapi()

    assert (
        "post"
        in schema["paths"][
            "/api/v1/query"
        ]
    )


def test_openapi_conversation_method():
    schema = app.openapi()

    assert (
        "post"
        in schema["paths"][
            "/api/v1/conversation"
        ]
    )


def test_session_methods():
    schema = app.openapi()

    session_path = schema[
        "paths"
    ][
        "/api/v1/sessions/{session_id}"
    ]

    assert "get" in session_path
    assert "delete" in session_path


def test_query_security_header_documented():
    schema = app.openapi()

    parameters = schema[
        "paths"
    ][
        "/api/v1/query"
    ][
        "post"
    ].get(
        "parameters",
        [],
    )

    names = {
        parameter["name"]
        for parameter in parameters
    }

    assert "X-API-Key" in names


def test_openapi_metadata():
    schema = app.openapi()

    assert (
        schema["info"]["title"]
        == "RetailOps AI API"
    )

    assert (
        schema["info"]["version"]
        == "1.0.0"
    )