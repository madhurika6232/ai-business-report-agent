from src.skills.registry import (
    Skill,
    SkillRegistry,
)

from src.tools.customer_tools import (
    review_summary_tool,
    review_trend_tool,
    delivery_review_impact_tool,
    delay_severity_impact_tool,
)

from src.tools.review_intelligence_tools import (
    complaint_themes_tool,
    delivery_complaint_evidence_tool,
)


def register_customer_skills(
    registry: SkillRegistry,
) -> None:
    """Register customer-experience skills."""

    registry.register(
        Skill(
            name="review_summary",
            description=(
                "Return overall customer review and "
                "satisfaction metrics."
            ),
            domain="customer",
            handler=review_summary_tool,
        )
    )

    registry.register(
        Skill(
            name="review_trend",
            description=(
                "Return monthly customer review and "
                "satisfaction trends."
            ),
            domain="customer",
            handler=review_trend_tool,
        )
    )

    registry.register(
        Skill(
            name="delivery_review_impact",
            description=(
                "Compare customer satisfaction between "
                "on-time and late deliveries."
            ),
            domain="customer",
            handler=delivery_review_impact_tool,
        )
    )

    registry.register(
        Skill(
            name="delay_severity_impact",
            description=(
                "Measure customer satisfaction across "
                "delivery-delay severity levels."
            ),
            domain="customer",
            handler=delay_severity_impact_tool,
        )
    )

    registry.register(
        Skill(
            name="complaint_themes",
            description=(
                "Return customer complaint themes from "
                "cached Groq review classifications."
            ),
            domain="customer",
            handler=complaint_themes_tool,
        )
    )

    registry.register(
        Skill(
            name="delivery_complaint_evidence",
            description=(
                "Compare customer-reported delivery complaints "
                "with structured delivery evidence."
            ),
            domain="customer",
            handler=delivery_complaint_evidence_tool,
        )
    )