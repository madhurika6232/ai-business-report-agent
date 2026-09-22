from unittest.mock import patch

from src.agents.graph import (
    error_node,
    route_after_specialists,
    specialist_node,
)


def make_state():
    return {
        "user_query": "Test question",
        "selected_agents": [],
        "agent_results": {},
        "evidence": [],
        "final_answer": None,
        "errors": [],
    }


def test_route_to_synthesis_when_no_errors():
    state = make_state()

    assert (
        route_after_specialists(state)
        == "synthesis"
    )


def test_route_to_error_when_errors_exist():
    state = make_state()

    state["errors"] = [
        "operations: test failure"
    ]

    assert (
        route_after_specialists(state)
        == "error"
    )


def test_error_node():
    state = make_state()

    state["errors"] = [
        "operations: test failure"
    ]

    result = error_node(state)

    assert (
        "could not complete"
        in result["final_answer"].lower()
    )

    assert (
        "operations: test failure"
        in result["final_answer"]
    )


def test_single_specialist_execution():
    state = make_state()

    state["selected_agents"] = [
        "business"
    ]

    fake_result = {
        "agent": "business",
        "query": "Test question",
        "results": {
            "business_summary": {
                "total_orders": 100,
            }
        },
    }

    with patch.dict(
        "src.agents.graph.AGENT_RUNNERS",
        {
            "business": lambda query: fake_result,
        },
        clear=True,
    ):
        result = specialist_node(state)

    assert (
        "business"
        in result["agent_results"]
    )

    assert len(
        result["evidence"]
    ) == 1

    assert result["errors"] == []


def test_multiple_specialist_execution():
    state = make_state()

    state["selected_agents"] = [
        "customer",
        "operations",
    ]

    customer_result = {
        "agent": "customer",
        "query": "Test question",
        "results": {
            "review_summary": {}
        },
    }

    operations_result = {
        "agent": "operations",
        "query": "Test question",
        "results": {
            "delivery_summary": {}
        },
    }

    with patch.dict(
        "src.agents.graph.AGENT_RUNNERS",
        {
            "customer": (
                lambda query:
                customer_result
            ),
            "operations": (
                lambda query:
                operations_result
            ),
        },
        clear=True,
    ):
        result = specialist_node(state)

    assert set(
        result["agent_results"]
    ) == {
        "customer",
        "operations",
    }

    assert len(
        result["evidence"]
    ) == 2

    assert result["errors"] == []


def test_specialist_failure_is_captured():
    state = make_state()

    state["selected_agents"] = [
        "operations"
    ]

    def failing_agent(query):
        raise RuntimeError(
            "Simulated tool failure"
        )

    with patch.dict(
        "src.agents.graph.AGENT_RUNNERS",
        {
            "operations": failing_agent,
        },
        clear=True,
    ):
        result = specialist_node(state)

    assert result["agent_results"] == {}

    assert len(
        result["errors"]
    ) == 1

    assert (
        "Simulated tool failure"
        in result["errors"][0]
    )


def test_unknown_agent_is_captured():
    state = make_state()

    state["selected_agents"] = [
        "unknown"
    ]

    result = specialist_node(state)

    assert result["agent_results"] == {}

    assert len(
        result["errors"]
    ) == 1

    assert (
        "Unknown agent"
        in result["errors"][0]
    )

    # ============================================================
# GUARDRAIL / FAILURE TESTS
# ============================================================

def test_empty_query_rejected():
    from src.agents.router import route_query

    import pytest

    with pytest.raises(
        ValueError,
        match="user_query cannot be empty",
    ):
        route_query("")


def test_whitespace_query_rejected():
    from src.agents.router import route_query

    import pytest

    with pytest.raises(
        ValueError,
        match="user_query cannot be empty",
    ):
        route_query("   ")


def test_multiple_agent_failure_is_captured():
    state = make_state()

    state["selected_agents"] = [
        "customer",
        "operations",
    ]

    def failing_customer(query):
        raise RuntimeError(
            "Customer failure"
        )

    def failing_operations(query):
        raise RuntimeError(
            "Operations failure"
        )

    with patch.dict(
        "src.agents.graph.AGENT_RUNNERS",
        {
            "customer": failing_customer,
            "operations": failing_operations,
        },
        clear=True,
    ):
        result = specialist_node(state)

    assert result["agent_results"] == {}

    assert len(result["errors"]) == 2

    assert any(
        "Customer failure" in error
        for error in result["errors"]
    )

    assert any(
        "Operations failure" in error
        for error in result["errors"]
    )


def test_partial_agent_failure_routes_to_error():
    state = make_state()

    state["errors"] = [
        "operations: simulated failure"
    ]

    assert (
        route_after_specialists(state)
        == "error"
    )


def test_error_response_does_not_expose_traceback():
    state = make_state()

    state["errors"] = [
        "operations: simulated failure"
    ]

    result = error_node(state)

    answer = result[
        "final_answer"
    ].lower()

    assert "traceback" not in answer
    assert "file \"" not in answer
    assert "line " not in answer


def test_unknown_agent_does_not_crash():
    state = make_state()

    state["selected_agents"] = [
        "not_a_real_agent"
    ]

    result = specialist_node(state)

    assert result["agent_results"] == {}
    assert len(result["errors"]) == 1

    assert (
        "Unknown agent"
        in result["errors"][0]
    )