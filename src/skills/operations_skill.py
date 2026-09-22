from src.skills.registry import (
    Skill,
    SkillRegistry,
)

from src.tools.operations_tools import (
    delivery_summary_tool,
    delivery_trend_tool,
    high_risk_sellers_tool,
    cancellation_metrics_tool,
    freight_metrics_tool,
)


def register_operations_skills(
    registry: SkillRegistry,
) -> None:
    """Register operations analytics skills."""

    registry.register(
        Skill(
            name="delivery_summary",
            description=(
                "Return overall delivery performance including "
                "late-delivery rate and average delivery time."
            ),
            domain="operations",
            handler=delivery_summary_tool,
        )
    )

    registry.register(
        Skill(
            name="delivery_trend",
            description=(
                "Return monthly delivery performance and "
                "late-delivery trends."
            ),
            domain="operations",
            handler=delivery_trend_tool,
        )
    )

    registry.register(
        Skill(
            name="high_risk_sellers",
            description=(
                "Return sellers with elevated "
                "late-delivery rates."
            ),
            domain="operations",
            handler=high_risk_sellers_tool,
        )
    )

    registry.register(
        Skill(
            name="cancellation_metrics",
            description=(
                "Return canceled-order volume "
                "and cancellation rate."
            ),
            domain="operations",
            handler=cancellation_metrics_tool,
        )
    )

    registry.register(
        Skill(
            name="freight_metrics",
            description=(
                "Return freight costs and "
                "freight-to-revenue metrics."
            ),
            domain="operations",
            handler=freight_metrics_tool,
        )
    )