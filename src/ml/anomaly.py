"""
Anomaly Detection

Business goal:
Detect unusual changes in marketplace performance that may
require investigation.

Metrics monitored:
- Revenue
- Order volume
- Late-delivery rate
- Average review score
- Negative-review rate

Success criteria:
- Detect meaningful deviations from historical behavior.
- Produce an interpretable anomaly score/severity.
- Avoid excessive false alerts.
"""

import pandas as pd


def build_anomaly_dataset(
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """Build monthly marketplace metrics for anomaly detection."""

    df = orders.copy()

    df["order_month"] = pd.to_datetime(
        df["order_month"]
    )

    df["is_negative_review"] = (
        df["review_score"] <= 2
    )

    monthly = (
        df.groupby("order_month")
        .agg(
            revenue=("order_revenue", "sum"),
            orders=("order_id", "nunique"),
            avg_review_score=("review_score", "mean"),
            negative_reviews=("is_negative_review", "sum"),
        )
        .reset_index()
        .sort_values("order_month")
    )

    monthly["negative_review_rate"] = (
        monthly["negative_reviews"]
        / monthly["orders"]
        * 100
    )

    # Delivery metrics require known delivery outcomes.
    delivery = df[
        df["is_late"].notna()
    ].copy()

    # CSV may load boolean values as strings.
    if delivery["is_late"].dtype != bool:
        delivery["is_late"] = (
            delivery["is_late"]
            .astype(str)
            .str.lower()
            .map({
                "true": True,
                "false": False,
            })
        )

    delivery_monthly = (
        delivery.groupby("order_month")
        .agg(
            evaluated_deliveries=("order_id", "nunique"),
            late_orders=("is_late", "sum"),
        )
        .reset_index()
    )

    delivery_monthly["late_rate"] = (
        delivery_monthly["late_orders"]
        / delivery_monthly["evaluated_deliveries"]
        * 100
    )

    monthly = monthly.merge(
        delivery_monthly[
            [
                "order_month",
                "evaluated_deliveries",
                "late_orders",
                "late_rate",
            ]
        ],
        on="order_month",
        how="left",
    )

    return monthly

def detect_metric_anomalies(
    data: pd.DataFrame,
    metric: str,
    window: int = 6,
    threshold: float = 2.0,
) -> pd.DataFrame:
    """Detect unusual metric values using historical rolling Z-scores."""

    if metric not in data.columns:
        raise ValueError(
            f"Metric '{metric}' does not exist."
        )

    df = data[
        ["order_month", metric]
    ].copy()

    # Historical baseline only — exclude current month.
    df["rolling_mean"] = (
        df[metric]
        .shift(1)
        .rolling(window=window, min_periods=3)
        .mean()
    )

    df["rolling_std"] = (
        df[metric]
        .shift(1)
        .rolling(window=window, min_periods=3)
        .std()
    )

    df["z_score"] = (
        (df[metric] - df["rolling_mean"])
        / df["rolling_std"]
    )

    df["is_anomaly"] = (
        df["z_score"].abs() >= threshold
    )

    return df

def classify_anomalies(
    anomalies: pd.DataFrame,
    higher_is_bad: bool,
) -> pd.DataFrame:
    """Add anomaly direction, business impact, and severity."""

    df = anomalies.copy()

    # Direction
    df["direction"] = "normal"
    df.loc[df["z_score"] > 0, "direction"] = "increase"
    df.loc[df["z_score"] < 0, "direction"] = "decrease"

    # Business impact
    df["impact"] = "normal"

    if higher_is_bad:
        df.loc[
            df["is_anomaly"] & (df["z_score"] > 0),
            "impact"
        ] = "negative"

        df.loc[
            df["is_anomaly"] & (df["z_score"] < 0),
            "impact"
        ] = "positive"

    else:
        df.loc[
            df["is_anomaly"] & (df["z_score"] < 0),
            "impact"
        ] = "negative"

        df.loc[
            df["is_anomaly"] & (df["z_score"] > 0),
            "impact"
        ] = "positive"

    # Severity
    df["severity"] = "normal"

    df.loc[
        df["z_score"].abs() >= 2,
        "severity"
    ] = "warning"

    df.loc[
        df["z_score"].abs() >= 3,
        "severity"
    ] = "critical"

    return df