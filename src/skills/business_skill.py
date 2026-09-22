from src.skills.registry import (
    Skill,
    SkillRegistry,
)

from src.tools.business_tools import (
    business_summary_tool,
    monthly_performance_tool,
    category_performance_tool,
    state_performance_tool,
)


def register_business_skills(
    registry: SkillRegistry,
) -> None:
    """Register business analytics skills."""

    registry.register(
        Skill(
            name="business_summary",
            description=(
                "Return core marketplace KPIs including "
                "revenue, orders, AOV, items, and customers."
            ),
            domain="business",
            handler=business_summary_tool,
        )
    )

    registry.register(
        Skill(
            name="monthly_performance",
            description=(
                "Return monthly revenue, orders, AOV, "
                "and revenue-growth performance."
            ),
            domain="business",
            handler=monthly_performance_tool,
        )
    )

    registry.register(
        Skill(
            name="category_performance",
            description=(
                "Return product-category performance "
                "ranked by revenue."
            ),
            domain="business",
            handler=category_performance_tool,
        )
    )

    registry.register(
        Skill(
            name="state_performance",
            description=(
                "Return customer-state business performance "
                "ranked by revenue."
            ),
            domain="business",
            handler=state_performance_tool,
        )
    )