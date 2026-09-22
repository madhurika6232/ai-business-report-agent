from pathlib import Path

import pandas as pd

from src.analytics.operations import (
    get_delivery_summary,
    get_delivery_trend,
    get_high_risk_sellers,
    get_cancellation_metrics,
    get_freight_metrics,
)
from src.analytics.validation import filter_orders


DATA_DIR = Path("data/processed")


def _load_orders() -> pd.DataFrame:
    """Load processed order data."""

    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


def _load_sellers() -> pd.DataFrame:
    """Load processed seller metrics."""

    return pd.read_csv(
        DATA_DIR / "seller_metrics.csv"
    )


def delivery_summary_tool(
    start_date: str | None = None,
    end_date: str | None = None,
    customer_state: str | None = None,
    category: str | None = None,
) -> dict:
    """Return delivery KPIs for the requested filters."""

    orders = _load_orders()

    filtered = filter_orders(
        orders,
        start_date=start_date,
        end_date=end_date,
        customer_state=customer_state,
        category=category,
    )

    return get_delivery_summary(filtered)


def delivery_trend_tool(
    start_date: str | None = None,
    end_date: str | None = None,
    customer_state: str | None = None,
    category: str | None = None,
) -> list[dict]:
    """Return monthly delivery performance."""

    orders = _load_orders()

    filtered = filter_orders(
        orders,
        start_date=start_date,
        end_date=end_date,
        customer_state=customer_state,
        category=category,
    )

    result = get_delivery_trend(filtered)

    result["order_month"] = (
        result["order_month"]
        .dt.strftime("%Y-%m")
    )

    return result.to_dict(
        orient="records"
    )


def high_risk_sellers_tool(
    min_orders: int = 30,
    top_n: int = 10,
) -> list[dict]:
    """Return sellers with the highest late-delivery rates."""

    sellers = _load_sellers()

    result = get_high_risk_sellers(
        sellers,
        min_orders=min_orders,
        top_n=top_n,
    )

    records = result.to_dict(
        orient="records"
    )

    # Replace any NaN values for JSON compatibility.
    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None

    return records


def cancellation_metrics_tool(
    start_date: str | None = None,
    end_date: str | None = None,
    customer_state: str | None = None,
    category: str | None = None,
) -> dict:
    """Return order cancellation KPIs."""

    orders = _load_orders()

    filtered = filter_orders(
        orders,
        start_date=start_date,
        end_date=end_date,
        customer_state=customer_state,
        category=category,
    )

    return get_cancellation_metrics(filtered)


def freight_metrics_tool(
    start_date: str | None = None,
    end_date: str | None = None,
    customer_state: str | None = None,
    category: str | None = None,
) -> dict:
    """Return freight-cost KPIs."""

    orders = _load_orders()

    filtered = filter_orders(
        orders,
        start_date=start_date,
        end_date=end_date,
        customer_state=customer_state,
        category=category,
    )

    return get_freight_metrics(filtered)