from src.tools.business_tools import (
    business_summary_tool,
    monthly_performance_tool,
    category_performance_tool,
    state_performance_tool,
)

from src.tools.operations_tools import (
    delivery_summary_tool,
    delivery_trend_tool,
    high_risk_sellers_tool,
    cancellation_metrics_tool,
    freight_metrics_tool,
)

from src.tools.customer_tools import (
    review_summary_tool,
    review_trend_tool,
    delivery_review_impact_tool,
    delay_severity_impact_tool,
)


TOOL_REGISTRY = {
    # Business
    "business_summary": business_summary_tool,
    "monthly_performance": monthly_performance_tool,
    "category_performance": category_performance_tool,
    "state_performance": state_performance_tool,

    # Operations
    "delivery_summary": delivery_summary_tool,
    "delivery_trend": delivery_trend_tool,
    "high_risk_sellers": high_risk_sellers_tool,
    "cancellation_metrics": cancellation_metrics_tool,
    "freight_metrics": freight_metrics_tool,

    # Customer
    "review_summary": review_summary_tool,
    "review_trend": review_trend_tool,
    "delivery_review_impact": delivery_review_impact_tool,
    "delay_severity_impact": delay_severity_impact_tool,
}


TOOL_DESCRIPTIONS = {
    "business_summary":
        "Core revenue, order, AOV, item, and customer KPIs.",

    "monthly_performance":
        "Monthly revenue, order volume, AOV, and revenue growth.",

    "category_performance":
        "Top product categories ranked by revenue.",

    "state_performance":
        "Customer-state performance ranked by revenue.",

    "delivery_summary":
        "Overall delivery time and late-delivery KPIs.",

    "delivery_trend":
        "Monthly delivery performance and late-delivery trends.",

    "high_risk_sellers":
        "Sellers with unusually high late-delivery rates.",

    "cancellation_metrics":
        "Order cancellation volume and cancellation rate.",

    "freight_metrics":
        "Freight cost and freight-to-revenue metrics.",

    "review_summary":
        "Overall customer review and satisfaction KPIs.",

    "review_trend":
        "Monthly customer satisfaction and negative-review trends.",

    "delivery_review_impact":
        "Comparison of customer satisfaction for on-time versus late deliveries.",

    "delay_severity_impact":
        "Customer satisfaction across different delivery-delay severity levels.",
}