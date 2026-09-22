from src.agents.business_agent import (
    run_business_agent,
)
from src.agents.operations_agent import (
    run_operations_agent,
)
from src.agents.customer_agent import (
    run_customer_agent,
)
from src.agents.risk_agent import (
    run_risk_agent,
)


# ============================================================
# BUSINESS AGENT
# ============================================================

def test_business_agent_summary():
    result = run_business_agent(
        "How is the business performing?"
    )

    assert result["agent"] == "business"

    assert (
        "business_summary"
        in result["results"]
    )

    summary = result["results"][
        "business_summary"
    ]

    assert summary["total_orders"] == 99092
    assert summary["total_revenue"] > 0


def test_business_agent_category():
    result = run_business_agent(
        "Which product categories generate the most revenue?"
    )

    assert (
        "category_performance"
        in result["results"]
    )


# ============================================================
# OPERATIONS AGENT
# ============================================================

def test_operations_agent_sellers():
    result = run_operations_agent(
        "Which sellers have the worst delivery performance?"
    )

    assert result["agent"] == "operations"

    assert (
        "delivery_summary"
        in result["results"]
    )

    assert (
        "high_risk_sellers"
        in result["results"]
    )


def test_operations_agent_cancellations():
    result = run_operations_agent(
        "What is our cancellation rate?"
    )

    assert (
        "cancellation_metrics"
        in result["results"]
    )


# ============================================================
# CUSTOMER AGENT
# ============================================================

def test_customer_agent_complaints():
    result = run_customer_agent(
        "What are customers complaining about?"
    )

    assert result["agent"] == "customer"

    assert (
        "complaint_themes"
        in result["results"]
    )


def test_customer_agent_delivery_impact():
    result = run_customer_agent(
        "How does late delivery affect customer satisfaction?"
    )

    assert (
        "delivery_review_impact"
        in result["results"]
    )

    assert (
        "delay_severity_impact"
        in result["results"]
    )


# ============================================================
# RISK AGENT
# ============================================================

def test_risk_agent_anomalies():
    result = run_risk_agent(
        "Were there unusual delivery anomalies?"
    )

    assert result["agent"] == "risk"

    assert (
        "delivery_anomalies"
        in result["results"]
    )


def test_risk_agent_delivery_risk():
    result = run_risk_agent(
        "Which orders have the highest delivery risk?"
    )

    assert (
        "delivery_risk"
        in result["results"]
    )


def test_risk_agent_forecast():
    result = run_risk_agent(
        "What method should we use to forecast future revenue?"
    )

    assert (
        "forecast_method"
        in result["results"]
    )

    assert (
        result["results"]
        ["forecast_method"]
        ["selected_model"]
        == "naive_baseline"
    )