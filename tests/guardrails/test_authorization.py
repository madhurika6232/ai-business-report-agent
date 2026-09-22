import pytest

from src.guardrails.authorization import (
    AGENT_SKILL_PERMISSIONS,
    authorize_skill,
    require_skill_authorization,
    execute_authorized_skill,
)


def test_operations_skill_authorized():
    result = authorize_skill(
        "operations",
        "delivery_summary",
    )

    assert result.allowed is True
    assert result.reason == "Authorized."


def test_customer_risk_skill_blocked():
    result = authorize_skill(
        "customer",
        "delivery_risk_screening",
    )

    assert result.allowed is False

    assert (
        result.reason
        == "Skill is not authorized for this agent."
    )


def test_unknown_agent_blocked():
    result = authorize_skill(
        "finance",
        "business_summary",
    )

    assert result.allowed is False
    assert result.reason == "Unknown agent."


def test_require_authorized_skill():
    require_skill_authorization(
        "business",
        "business_summary",
    )


def test_require_unauthorized_skill_raises():
    with pytest.raises(
        PermissionError,
        match="cannot execute",
    ):
        require_skill_authorization(
            "customer",
            "delivery_risk_screening",
        )


def test_authorized_execution():
    result = execute_authorized_skill(
        agent="operations",
        skill="delivery_summary",
    )

    assert result["delivered_orders"] == 96204
    assert result["late_orders"] == 7823
    assert result["late_rate"] == pytest.approx(
        8.13
    )


def test_unauthorized_execution_blocked():
    with pytest.raises(
        PermissionError,
        match="cannot execute",
    ):
        execute_authorized_skill(
            agent="customer",
            skill="delivery_risk_screening",
        )


def test_all_registered_permissions():
    assert len(
        AGENT_SKILL_PERMISSIONS["business"]
    ) == 4

    assert len(
        AGENT_SKILL_PERMISSIONS["operations"]
    ) == 5

    assert len(
        AGENT_SKILL_PERMISSIONS["customer"]
    ) == 6

    assert len(
        AGENT_SKILL_PERMISSIONS["risk"]
    ) == 4