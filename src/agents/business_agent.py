from typing import Any

from src.tools.business_tools import (
    business_summary_tool,
    monthly_performance_tool,
    category_performance_tool,
    state_performance_tool,
)


def run_business_agent(
    user_query: str,
) -> dict[str, Any]:
    """Collect trusted business evidence for the supervisor."""

    query = user_query.lower()

    results = {}

    # Overall business KPIs
    results["business_summary"] = (
        business_summary_tool()
    )

    # Add relevant detailed evidence
    if any(
        term in query
        for term in [
            "trend",
            "month",
            "growth",
            "performance",
        ]
    ):
        results["monthly_performance"] = (
            monthly_performance_tool()
        )

    if "categor" in query:
        results["category_performance"] = (
            category_performance_tool(
                top_n=10
            )
        )

    if any(
        term in query
        for term in [
            "state",
            "region",
            "geograph",
        ]
    ):
        results["state_performance"] = (
            state_performance_tool(
                top_n=10
            )
        )

    return {
        "agent": "business",
        "query": user_query,
        "results": results,
    }