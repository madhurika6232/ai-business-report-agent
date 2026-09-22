import pytest
from pydantic import ValidationError

from src.agents.router import (
    RoutingDecision,
)


def test_single_agent_route():
    decision = RoutingDecision(
        selected_agents=["business"],
        reasoning="Business performance question.",
    )

    assert decision.selected_agents == [
        "business"
    ]


def test_multi_agent_route():
    decision = RoutingDecision(
        selected_agents=[
            "customer",
            "operations",
        ],
        reasoning=(
            "Customer satisfaction and "
            "delivery performance."
        ),
    )

    assert set(
        decision.selected_agents
    ) == {
        "customer",
        "operations",
    }


def test_all_valid_agents():
    decision = RoutingDecision(
        selected_agents=[
            "business",
            "operations",
            "customer",
            "risk",
        ],
        reasoning="Cross-domain analysis.",
    )

    assert len(
        decision.selected_agents
    ) == 4


def test_invalid_agent_rejected():
    with pytest.raises(
        ValidationError
    ):
        RoutingDecision(
            selected_agents=["finance"],
            reasoning="Invalid agent.",
        )