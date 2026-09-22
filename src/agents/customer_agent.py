from typing import Any

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


def run_customer_agent(
    user_query: str,
) -> dict[str, Any]:
    """Collect trusted customer-experience evidence."""

    query = user_query.lower()

    results = {}

    # Overall satisfaction
    if any(
        term in query
        for term in [
            "rating",
            "review",
            "satisfaction",
            "customer experience",
        ]
    ):
        results["review_summary"] = (
            review_summary_tool()
        )

    # Satisfaction trends
    if any(
        term in query
        for term in [
            "trend",
            "month",
            "decline",
            "drop",
            "worse",
        ]
    ):
        results["review_trend"] = (
            review_trend_tool()
        )

    # Complaint themes
    if any(
        term in query
        for term in [
            "complain",
            "complaint",
            "issue",
            "problem",
        ]
    ):
        results["complaint_themes"] = (
            complaint_themes_tool(
                negative_only=True
            )
        )

    # Delivery impact on satisfaction
    if any(
        term in query
        for term in [
            "delivery",
            "late",
            "delay",
        ]
    ):
        results["delivery_review_impact"] = (
            delivery_review_impact_tool()
        )

        results["delay_severity_impact"] = (
            delay_severity_impact_tool()
        )

    # Compare customer complaints with structured evidence
    if (
        any(
            term in query
            for term in [
                "complain",
                "complaint",
            ]
        )
        and
        any(
            term in query
            for term in [
                "delivery",
                "late",
                "evidence",
            ]
        )
    ):
        results["delivery_complaint_evidence"] = (
            delivery_complaint_evidence_tool()
        )

    # General customer baseline
    if not results:
        results["review_summary"] = (
            review_summary_tool()
        )

    return {
        "agent": "customer",
        "query": user_query,
        "results": results,
    }