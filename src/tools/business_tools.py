from pathlib import Path

import pandas as pd

from src.analytics.business import (
    get_business_summary,
    get_monthly_performance,
    get_category_performance,
    get_state_performance,
)
from src.analytics.validation import filter_orders


DATA_DIR = Path("data/processed")


def _load_orders() -> pd.DataFrame:
    """Load the processed order dataset."""

    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


def _load_categories() -> pd.DataFrame:
    """Load the processed category dataset."""

    return pd.read_csv(
        DATA_DIR / "category_metrics.csv"
    )


def business_summary_tool(
    start_date: str | None = None,
    end_date: str | None = None,
    customer_state: str | None = None,
    category: str | None = None,
) -> dict:
    """
    Return core business KPIs for the requested filters.

    Use this tool for questions about overall revenue,
    orders, average order value, items, or customers.
    """

    orders = _load_orders()

    filtered = filter_orders(
        orders,
        start_date=start_date,
        end_date=end_date,
        customer_state=customer_state,
        category=category,
    )

    return get_business_summary(filtered)


def monthly_performance_tool(
    start_date: str | None = None,
    end_date: str | None = None,
    customer_state: str | None = None,
    category: str | None = None,
) -> list[dict]:
    """
    Return monthly revenue, orders, AOV, and growth.

    Use this tool for trend and month-over-month
    performance questions.
    """

    orders = _load_orders()

    filtered = filter_orders(
        orders,
        start_date=start_date,
        end_date=end_date,
        customer_state=customer_state,
        category=category,
    )

    result = get_monthly_performance(filtered)

    # Convert dates into JSON-friendly strings
    result["order_month"] = (
        result["order_month"]
        .dt.strftime("%Y-%m")
    )

    # Convert DataFrame into records
    records = result.to_dict(
        orient="records"
    )

    # Replace NaN with None for JSON compatibility
    for record in records:
        if pd.isna(record["revenue_growth_pct"]):
            record["revenue_growth_pct"] = None

    return records


def category_performance_tool(
    top_n: int = 10,
) -> list[dict]:
    """
    Return top product categories ranked by revenue.

    Use this tool for category-performance questions.
    """

    categories = _load_categories()

    result = get_category_performance(
        categories,
        top_n=top_n,
    )

    return result.to_dict(
        orient="records"
    )


def state_performance_tool(
    top_n: int = 10,
) -> list[dict]:
    """
    Return top customer states ranked by revenue.

    Use this tool for geographic-performance questions.
    """

    orders = _load_orders()

    result = get_state_performance(
        orders,
        top_n=top_n,
    )

    return result.to_dict(
        orient="records"
    )