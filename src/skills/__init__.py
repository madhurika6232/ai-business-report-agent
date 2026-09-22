from src.skills.registry import (
    Skill,
    SkillRegistry,
)

from src.skills.business_skill import (
    register_business_skills,
)

from src.skills.operations_skill import (
    register_operations_skills,
)

from src.skills.customer_skill import (
    register_customer_skills,
)

from src.skills.risk_skill import (
    register_risk_skills,
)


def build_skill_registry() -> SkillRegistry:
    """Build the complete RetailOps skill registry."""

    registry = SkillRegistry()

    register_business_skills(
        registry
    )

    register_operations_skills(
        registry
    )

    register_customer_skills(
        registry
    )

    register_risk_skills(
        registry
    )

    return registry


retailops_skills = build_skill_registry()