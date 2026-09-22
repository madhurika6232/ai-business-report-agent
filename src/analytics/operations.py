import pandas as pd


def get_delivery_summary(orders: pd.DataFrame) -> dict:
    """Calculate marketplace delivery performance KPIs."""

    delivered = orders[
        orders["delivery_days"].notna()
    ].copy()

    evaluated = delivered[
        delivered["is_late"].notna()
    ].copy()

    total_delivered = len(delivered)
    evaluated_deliveries = len(evaluated)

    late_orders = (
        evaluated["is_late"]
        .astype(bool)
        .sum()
    )

    late_rate = (
        late_orders / evaluated_deliveries * 100
        if evaluated_deliveries > 0
        else 0
    )

    return {
        "delivered_orders": int(total_delivered),
        "evaluated_deliveries": int(evaluated_deliveries),
        "late_orders": int(late_orders),
        "late_rate": round(float(late_rate), 2),
        "avg_delivery_days": round(
            float(delivered["delivery_days"].mean()),
            2,
        ),
        "avg_delay_days": round(
            float(delivered["delay_days"].mean()),
            2,
        ),
    }

def get_delivery_trend(orders: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly delivery performance."""

    df = orders[
        orders["delivery_days"].notna()
        & orders["is_late"].notna()
    ].copy()

    df["order_month"] = pd.to_datetime(df["order_month"])

    monthly = (
        df.groupby("order_month")
        .agg(
            delivered_orders=("order_id", "nunique"),
            late_orders=("is_late", "sum"),
            avg_delivery_days=("delivery_days", "mean"),
        )
        .reset_index()
        .sort_values("order_month")
    )

    monthly["late_rate"] = (
        monthly["late_orders"]
        / monthly["delivered_orders"]
        * 100
    )

    return monthly

def get_high_risk_sellers(
    sellers: pd.DataFrame,
    min_orders: int = 30,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return sellers with the highest late-delivery rates."""

    if min_orders <= 0:
        raise ValueError("min_orders must be greater than 0.")

    if top_n <= 0:
        raise ValueError("top_n must be greater than 0.")

    eligible = sellers[
        sellers["orders"] >= min_orders
    ].copy()

    return (
        eligible
        .sort_values(
            ["late_rate", "orders"],
            ascending=[False, False],
        )
        .head(top_n)
        .reset_index(drop=True)
    )

def get_cancellation_metrics(orders: pd.DataFrame) -> dict:
    """Calculate marketplace order cancellation metrics."""

    total_orders = orders["order_id"].nunique()

    canceled = orders[
        orders["order_status"] == "canceled"
    ]

    canceled_orders = canceled["order_id"].nunique()

    cancellation_rate = (
        canceled_orders / total_orders * 100
        if total_orders > 0
        else 0
    )

    return {
        "total_orders": int(total_orders),
        "canceled_orders": int(canceled_orders),
        "cancellation_rate": round(
            float(cancellation_rate),
            2,
        ),
    }

def get_freight_metrics(orders: pd.DataFrame) -> dict:
    """Calculate marketplace freight-cost metrics."""

    valid = orders[
        orders["order_revenue"].notna()
        & orders["freight_value"].notna()
    ].copy()

    total_freight = valid["freight_value"].sum()
    total_revenue = valid["order_revenue"].sum()

    avg_freight_per_order = (
        total_freight / len(valid)
        if len(valid) > 0
        else 0
    )

    freight_to_revenue_pct = (
        total_freight / total_revenue * 100
        if total_revenue > 0
        else 0
    )

    return {
        "total_freight": round(float(total_freight), 2),
        "avg_freight_per_order": round(
            float(avg_freight_per_order),
            2,
        ),
        "freight_to_revenue_pct": round(
            float(freight_to_revenue_pct),
            2,
        ),
    }