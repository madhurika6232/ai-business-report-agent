from dataclasses import dataclass


AGENT_SKILL_PERMISSIONS = {
    "business": {
        "business_summary",
        "monthly_performance",
        "category_performance",
        "state_performance",
    },

    "operations": {
        "delivery_summary",
        "delivery_trend",
        "high_risk_sellers",
        "cancellation_metrics",
        "freight_metrics",
    },

    "customer": {
        "review_summary",
        "review_trend",
        "delivery_review_impact",
        "delay_severity_impact",
        "complaint_themes",
        "delivery_complaint_evidence",
    },

    "risk": {
        "delivery_anomaly_detection",
        "delivery_risk_screening",
        "forecast_history",
        "forecast_method",
    },
}


@dataclass(frozen=True)
class AuthorizationDecision:
    """Result of an agent skill authorization check."""

    allowed: bool
    agent: str
    skill: str
    reason: str


def authorize_skill(
    agent: str,
    skill: str,
) -> AuthorizationDecision:
    """Check whether an agent may execute a skill."""

    if agent not in AGENT_SKILL_PERMISSIONS:
        return AuthorizationDecision(
            allowed=False,
            agent=agent,
            skill=skill,
            reason="Unknown agent.",
        )

    allowed_skills = (
        AGENT_SKILL_PERMISSIONS[
            agent
        ]
    )

    if skill not in allowed_skills:
        return AuthorizationDecision(
            allowed=False,
            agent=agent,
            skill=skill,
            reason=(
                "Skill is not authorized "
                "for this agent."
            ),
        )

    return AuthorizationDecision(
        allowed=True,
        agent=agent,
        skill=skill,
        reason="Authorized.",
    )


def require_skill_authorization(
    agent: str,
    skill: str,
) -> None:
    """Raise an error when an agent is not authorized."""

    decision = authorize_skill(
        agent,
        skill,
    )

    if not decision.allowed:
        raise PermissionError(
            f"{agent} cannot execute {skill}: "
            f"{decision.reason}"
        )


def execute_authorized_skill(
    agent: str,
    skill: str,
    **kwargs,
):
    """Execute a RetailOps skill only when the agent is authorized."""

    require_skill_authorization(
        agent,
        skill,
    )

    from src.skills import retailops_skills

    return retailops_skills.execute(
        skill,
        **kwargs,
    )