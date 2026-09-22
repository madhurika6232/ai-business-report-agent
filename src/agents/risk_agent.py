from typing import Any

from src.tools.ml_tools import (
    anomaly_detection_tool,
    delivery_risk_summary_tool,
)

from src.tools.business_tools import (
    monthly_performance_tool,
)


def run_risk_agent(
    user_query: str,
) -> dict[str, Any]:
    """Collect trusted ML and risk evidence."""

    query = user_query.lower()

    results = {}

    # Anomaly detection
    if any(
        term in query
        for term in [
            "anomaly",
            "anomalies",
            "unusual",
            "abnormal",
            "spike",
        ]
    ):
        results["delivery_anomalies"] = (
            anomaly_detection_tool(
                metric="late_rate",
                higher_is_bad=True,
            )
        )

    # Delivery-risk screening
    if any(
        term in query
        for term in [
            "risk",
            "risky",
            "at risk",
            "likely late",
        ]
    ):
        results["delivery_risk"] = (
            delivery_risk_summary_tool(
                top_n=10,
            )
        )

    # Forecast / future performance
    if any(
        term in query
        for term in [
            "forecast",
            "predict revenue",
            "future revenue",
            "next month",
        ]
    ):
        # Current selected forecasting approach is
        # the validated naive baseline.
        results["monthly_history"] = (
            monthly_performance_tool()
        )

        results["forecast_method"] = {
            "selected_model": "naive_baseline",
            "holdout_mape": 4.94,
            "note": (
                "The naive baseline outperformed "
                "Holt exponential smoothing on "
                "temporal holdout validation."
            ),
        }

    # General risk baseline
    if not results:
        results["delivery_anomalies"] = (
            anomaly_detection_tool(
                metric="late_rate",
                higher_is_bad=True,
            )
        )

    return {
        "agent": "risk",
        "query": user_query,
        "results": results,
    }