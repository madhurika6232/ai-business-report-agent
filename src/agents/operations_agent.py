from typing import Any

from src.tools.operations_tools import (
    delivery_summary_tool,
    delivery_trend_tool,
    high_risk_sellers_tool,
    cancellation_metrics_tool,
    freight_metrics_tool,
)


def run_operations_agent(
    user_query: str,
) -> dict[str, Any]:
    """Collect trusted operations evidence for the supervisor."""

    query = user_query.lower()

    results = {}

    if any(
        term in query
        for term in [
            "delivery",
            "late",
            "shipping",
        ]
    ):
        results["delivery_summary"] = (
            delivery_summary_tool()
        )

    if any(
        term in query
        for term in [
            "trend",
            "month",
            "worse",
            "decline",
        ]
    ):
        results["delivery_trend"] = (
            delivery_trend_tool()
        )

    if any(
        term in query
        for term in [
            "seller",
            "vendor",
        ]
    ):
        results["high_risk_sellers"] = (
            high_risk_sellers_tool(
                min_orders=30,
                top_n=10,
            )
        )

    if any(
        term in query
        for term in [
            "cancel",
            "cancellation",
        ]
    ):
        results["cancellation_metrics"] = (
            cancellation_metrics_tool()
        )

    if any(
        term in query
        for term in [
            "freight",
            "shipping cost",
        ]
    ):
        results["freight_metrics"] = (
            freight_metrics_tool()
        )

    # Provide a general operations baseline if no
    # specialized tool matched.
    if not results:
        results["delivery_summary"] = (
            delivery_summary_tool()
        )

        results["cancellation_metrics"] = (
            cancellation_metrics_tool()
        )

        results["freight_metrics"] = (
            freight_metrics_tool()
        )

    return {
        "agent": "operations",
        "query": user_query,
        "results": results,
    }