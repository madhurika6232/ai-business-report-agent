import json
import logging

from fastapi.testclient import TestClient

from src.api.app import app
from src.api.logging_config import (
    JsonFormatter,
    LOGGER_NAME,
)


client = TestClient(app)


def test_json_formatter():
    formatter = JsonFormatter()

    record = logging.LogRecord(
        name=LOGGER_NAME,
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request_completed",
        args=(),
        exc_info=None,
    )

    record.request_id = "test-request-id"
    record.method = "GET"
    record.path = "/health"
    record.status_code = 200
    record.latency_ms = 12.34

    output = formatter.format(
        record
    )

    data = json.loads(
        output
    )

    assert (
        data["message"]
        == "request_completed"
    )

    assert (
        data["request_id"]
        == "test-request-id"
    )

    assert data["method"] == "GET"
    assert data["path"] == "/health"
    assert data["status_code"] == 200
    assert data["latency_ms"] == 12.34

    assert "timestamp" in data
    assert data["level"] == "INFO"


def test_health_request_is_logged(
    caplog,
):
    caplog.set_level(
        logging.INFO,
        logger=LOGGER_NAME,
    )

    response = client.get(
        "/health",
        headers={
            "X-Request-ID": (
                "logging-test-123"
            ),
        },
    )

    assert response.status_code == 200

    records = [
        record
        for record in caplog.records
        if record.name == LOGGER_NAME
    ]

    assert records

    record = records[-1]

    assert (
        record.getMessage()
        == "request_completed"
    )

    assert (
        getattr(
            record,
            "request_id",
            None,
        )
        == "logging-test-123"
    )

    assert (
        getattr(
            record,
            "method",
            None,
        )
        == "GET"
    )

    assert (
        getattr(
            record,
            "path",
            None,
        )
        == "/health"
    )

    assert (
        getattr(
            record,
            "status_code",
            None,
        )
        == 200
    )

    assert (
        getattr(
            record,
            "latency_ms",
            None,
        )
        is not None
    )


def test_query_body_not_logged(
    monkeypatch,
    caplog,
):
    secret_query = (
        "PRIVATE_QUERY_TEXT_DO_NOT_LOG"
    )

    def fake_guarded_query(
        user_query: str,
    ):
        return {
            "user_query": user_query,
            "safe_query": user_query,
            "final_answer": "Safe answer.",
            "selected_agents": [
                "business"
            ],
            "blocked": False,
            "pii_detected": False,
            "guardrail_validation": {
                "output_valid": True,
            },
        }

    monkeypatch.setattr(
        "src.api.routes.query.guarded_agent_query",
        fake_guarded_query,
    )

    caplog.set_level(
        logging.INFO,
        logger=LOGGER_NAME,
    )

    response = client.post(
        "/api/v1/query",
        json={
            "query": secret_query,
        },
    )

    assert response.status_code == 200

    logged_text = " ".join(
        record.getMessage()
        for record in caplog.records
        if record.name == LOGGER_NAME
    )

    assert (
        secret_query
        not in logged_text
    )


def test_api_key_not_logged(
    monkeypatch,
    caplog,
):
    monkeypatch.setenv(
        "RETAILOPS_API_KEY",
        "configured-secret",
    )

    supplied_key = (
        "configured-secret"
    )

    caplog.set_level(
        logging.INFO,
        logger=LOGGER_NAME,
    )

    response = client.post(
        "/api/v1/query",
        headers={
            "X-API-Key": supplied_key,
        },
        json={},
    )

    assert response.status_code == 422

    logged_text = " ".join(
        record.getMessage()
        for record in caplog.records
        if record.name == LOGGER_NAME
    )

    assert (
        supplied_key
        not in logged_text
    )


def test_log_does_not_contain_request_headers(
    caplog,
):
    caplog.set_level(
        logging.INFO,
        logger=LOGGER_NAME,
    )

    response = client.get(
        "/health",
        headers={
            "Authorization": (
                "Bearer secret-token"
            ),
            "X-Custom-Secret": (
                "private-value"
            ),
        },
    )

    assert response.status_code == 200

    logged_text = " ".join(
        record.getMessage()
        for record in caplog.records
        if record.name == LOGGER_NAME
    )

    assert (
        "secret-token"
        not in logged_text
    )

    assert (
        "private-value"
        not in logged_text
    )