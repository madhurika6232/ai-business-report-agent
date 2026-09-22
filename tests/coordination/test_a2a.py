import pytest

from src.coordination.messages import (
    AgentMessage,
    AgentResponse,
)

from src.coordination.a2a import (
    dispatch_message,
    dispatch_to_agents,
)


def test_agent_message():
    message = AgentMessage(
        sender="supervisor",
        recipient="operations",
        message_type="request",
        task="Analyze delivery performance.",
    )

    assert message.sender == "supervisor"
    assert message.recipient == "operations"
    assert message.message_type == "request"


def test_single_agent_dispatch():
    message = AgentMessage(
        sender="supervisor",
        recipient="operations",
        message_type="request",
        task="Analyze seller delivery performance.",
        context={
            "user_query": (
                "Which sellers have the worst "
                "delivery performance?"
            )
        },
    )

    response = dispatch_message(
        message
    )

    assert isinstance(
        response,
        AgentResponse,
    )

    assert response.agent == "operations"
    assert response.success is True
    assert response.error is None

    assert (
        "delivery_summary"
        in response.evidence
    )

    assert (
        "high_risk_sellers"
        in response.evidence
    )


def test_multi_agent_dispatch():
    responses = dispatch_to_agents(
        user_query=(
            "Why did customer satisfaction decline "
            "when delivery performance got worse?"
        ),
        agent_names=[
            "customer",
            "operations",
        ],
    )

    assert set(
        responses.keys()
    ) == {
        "customer",
        "operations",
    }

    assert responses[
        "customer"
    ].success is True

    assert responses[
        "operations"
    ].success is True


def test_customer_a2a_evidence():
    responses = dispatch_to_agents(
        user_query=(
            "How does late delivery affect "
            "customer satisfaction?"
        ),
        agent_names=[
            "customer",
        ],
    )

    evidence = responses[
        "customer"
    ].evidence

    assert (
        "delivery_review_impact"
        in evidence
    )

    assert (
        "delay_severity_impact"
        in evidence
    )


def test_non_request_message_rejected():
    message = AgentMessage(
        sender="business",
        recipient="operations",
        message_type="response",
        task="Test",
    )

    response = dispatch_message(
        message
    )

    assert response.success is False

    assert (
        "Only request messages"
        in response.error
    )


def test_supervisor_not_dispatch_target():
    message = AgentMessage(
        sender="business",
        recipient="supervisor",
        message_type="request",
        task="Test",
    )

    response = dispatch_message(
        message
    )

    assert response.success is False

    assert (
        "not a specialist"
        in response.error
    )


def test_empty_multi_agent_query():
    with pytest.raises(
        ValueError,
        match="user_query cannot be empty",
    ):
        dispatch_to_agents(
            user_query="",
            agent_names=[
                "operations",
            ],
        )


def test_empty_agent_list():
    with pytest.raises(
        ValueError,
        match="agent_names cannot be empty",
    ):
        dispatch_to_agents(
            user_query="Test question",
            agent_names=[],
        )