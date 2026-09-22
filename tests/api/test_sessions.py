from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_conversation_endpoint(
    monkeypatch,
):
    def fake_answer_with_memory(
        user_query,
        session_id,
        store,
    ):
        return {
            "original_query": user_query,
            "resolved_query": user_query,
            "session_id": session_id,
            "final_answer": (
                "Revenue performance was stable."
            ),
            "selected_agents": [
                "business"
            ],
        }

    monkeypatch.setattr(
        "src.api.routes.sessions.answer_with_memory",
        fake_answer_with_memory,
    )

    response = client.post(
        "/api/v1/conversation",
        json={
            "query": (
                "How was revenue in March 2018?"
            ),
            "session_id": "test-session",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["session_id"]
        == "test-session"
    )

    assert (
        data["original_query"]
        == "How was revenue in March 2018?"
    )

    assert (
        data["resolved_query"]
        == "How was revenue in March 2018?"
    )

    assert data[
        "selected_agents"
    ] == [
        "business"
    ]


def test_followup_resolution_exposed(
    monkeypatch,
):
    def fake_answer_with_memory(
        user_query,
        session_id,
        store,
    ):
        return {
            "original_query": user_query,
            "resolved_query": (
                "What was revenue in February 2018?"
            ),
            "session_id": session_id,
            "final_answer": (
                "February revenue is shown "
                "in the verified evidence."
            ),
            "selected_agents": [
                "business"
            ],
        }

    monkeypatch.setattr(
        "src.api.routes.sessions.answer_with_memory",
        fake_answer_with_memory,
    )

    response = client.post(
        "/api/v1/conversation",
        json={
            "query": (
                "What about the previous month?"
            ),
            "session_id": "test-session",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["original_query"]
        == "What about the previous month?"
    )

    assert (
        data["resolved_query"]
        == "What was revenue in February 2018?"
    )


def test_empty_session_id_rejected():
    response = client.post(
        "/api/v1/conversation",
        json={
            "query": "How is revenue?",
            "session_id": "",
        },
    )

    assert response.status_code == 422


def test_missing_session_id_rejected():
    response = client.post(
        "/api/v1/conversation",
        json={
            "query": "How is revenue?",
        },
    )

    assert response.status_code == 422


def test_empty_conversation_query_rejected():
    response = client.post(
        "/api/v1/conversation",
        json={
            "query": "",
            "session_id": "test-session",
        },
    )

    assert response.status_code == 422


from src.memory.store import (
    memory_store,
)


def test_get_session_summary():
    memory_store.clear()

    memory = memory_store.get_or_create(
        "summary-session"
    )

    memory.add_user_turn(
        "How was revenue?"
    )

    memory.add_assistant_turn(
        "Revenue was stable."
    )

    memory.last_selected_agents = [
        "business"
    ]

    response = client.get(
        "/api/v1/sessions/summary-session"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["session_id"]
        == "summary-session"
    )

    assert data["turn_count"] == 2

    assert (
        data["last_query"]
        == "How was revenue?"
    )

    assert (
        data["last_selected_agents"]
        == ["business"]
    )

    memory_store.clear()


def test_get_missing_session_returns_404():
    memory_store.clear()

    response = client.get(
        "/api/v1/sessions/does-not-exist"
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Session not found."
    )


def test_delete_session():
    memory_store.clear()

    memory_store.get_or_create(
        "delete-session"
    )

    response = client.delete(
        "/api/v1/sessions/delete-session"
    )

    assert response.status_code == 200

    assert response.json() == {
        "session_id": "delete-session",
        "deleted": True,
    }

    assert (
        memory_store.get(
            "delete-session"
        )
        is None
    )


def test_delete_missing_session_returns_404():
    memory_store.clear()

    response = client.delete(
        "/api/v1/sessions/missing-session"
    )

    assert response.status_code == 404