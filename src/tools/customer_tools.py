from pathlib import Path

import pandas as pd

from src.analytics.customer import (
    get_review_summary,
    get_review_trend,
    get_delivery_review_impact,
    get_delay_severity_impact,
)
from src.analytics.validation import filter_orders


DATA_DIR = Path("data/processed")


def _load_orders() -> pd.DataFrame:
    """Load processed order data."""

    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


def review_summary_tool(
    start_date: str | None = None,
    end_date: str | None = None,
    customer_state: str | None = None,
    category: str | None = None,
) -> dict:
    """Return customer satisfaction KPIs."""

    orders = _load_orders()

    filtered = filter_orders(
        orders,
        start_date=start_date,
        end_date=end_date,
        customer_state=customer_state,
        category=category,
    )

    return get_review_summary(filtered)


def review_trend_tool(
    start_date: str | None = None,
    end_date: str | None = None,
    customer_state: str | None = None,
    category: str | None = None,
) -> list[dict]:
    """Return monthly customer satisfaction trends."""

    orders = _load_orders()

    filtered = filter_orders(
        orders,
        start_date=start_date,
        end_date=end_date,
        customer_state=customer_state,
        category=category,
    )

    result = get_review_trend(filtered)

    result["order_month"] = (
        result["order_month"]
        .dt.strftime("%Y-%m")
    )

    records = result.to_dict(
        orient="records"
    )

    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None

    return records


def delivery_review_impact_tool(
    start_date: str | None = None,
    end_date: str | None = None,
    customer_state: str | None = None,
    category: str | None = None,
) -> list[dict]:
    """Compare customer satisfaction for on-time and late deliveries."""

    orders = _load_orders()

    filtered = filter_orders(
        orders,
        start_date=start_date,
        end_date=end_date,
        customer_state=customer_state,
        category=category,
    )

    result = get_delivery_review_impact(
        filtered
    )

    return result.to_dict(
        orient="records"
    )


def delay_severity_impact_tool(
    start_date: str | None = None,
    end_date: str | None = None,
    customer_state: str | None = None,
    category: str | None = None,
) -> list[dict]:
    """Return satisfaction metrics by delivery-delay severity."""

    orders = _load_orders()

    filtered = filter_orders(
        orders,
        start_date=start_date,
        end_date=end_date,
        customer_state=customer_state,
        category=category,
    )

    result = get_delay_severity_impact(
        filtered
    )

    # Convert categorical values into ordinary strings.
    result["delay_bucket"] = (
        result["delay_bucket"].astype(str)
    )

    return result.to_dict(
        orient="records"
    )