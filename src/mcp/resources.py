from typing import Any

from src.skills import retailops_skills


def get_platform_info() -> dict[str, Any]:
    """Return metadata describing the RetailOps AI platform."""

    return {
        "name": "RetailOps AI",
        "description": (
            "AI-powered retail operations analytics, "
            "customer intelligence, and risk platform."
        ),
        "domains": [
            "business",
            "operations",
            "customer",
            "risk",
        ],
        "skill_count": len(
            retailops_skills
        ),
    }


def get_skill_catalog() -> list[dict[str, str]]:
    """Return discoverable metadata for registered skills."""

    return [
        {
            "name": skill.name,
            "description": skill.description,
            "domain": skill.domain,
        }
        for skill in retailops_skills.list_skills()
    ]


def get_domain_catalog() -> dict[str, list[str]]:
    """Return skills grouped by domain."""

    domains = {}

    for domain in [
        "business",
        "operations",
        "customer",
        "risk",
    ]:
        domains[domain] = [
            skill.name
            for skill in retailops_skills.list_skills(
                domain=domain
            )
        ]

    return domains