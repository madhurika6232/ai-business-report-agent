from pathlib import Path

import pandas as pd

from src.ml.anomaly import (
    build_anomaly_dataset,
    detect_metric_anomalies,
    classify_anomalies,
)

from src.ml.delivery_risk import (
    MODEL_FEATURES,
    add_historical_seller_features,
    build_delivery_risk_dataset,
    classify_risk_level,
)

from src.ml.model_io import load_model


DATA_DIR = Path("data/processed")
MODEL_PATH = Path("models/delivery_risk_model.joblib")


def _load_orders() -> pd.DataFrame:
    """Load processed order data."""

    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


def anomaly_detection_tool(
    metric: str = "late_rate",
    window: int = 6,
    threshold: float = 2.0,
    higher_is_bad: bool = True,
) -> list[dict]:
    """Detect unusual monthly marketplace behavior."""

    orders = _load_orders()

    data = build_anomaly_dataset(
        orders
    )

    detected = detect_metric_anomalies(
        data,
        metric=metric,
        window=window,
        threshold=threshold,
    )

    classified = classify_anomalies(
        detected,
        higher_is_bad=higher_is_bad,
    )

    result = classified[
        classified["is_anomaly"]
    ].copy()

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


def delivery_risk_summary_tool(
    top_n: int = 10,
) -> list[dict]:
    """
    Return orders with the highest predicted
    late-delivery risk.

    This is a risk-screening tool, not a guarantee
    that an order will arrive late.
    """

    if top_n <= 0:
        raise ValueError(
            "top_n must be greater than 0."
        )

    orders = _load_orders()

    risk_data = build_delivery_risk_dataset(
        orders
    )

    risk_data = add_historical_seller_features(
        risk_data,
        orders,
    )

    model = load_model(
        MODEL_PATH
    )

    probabilities = model.predict_proba(
        risk_data[MODEL_FEATURES]
    )[:, 1]

    result = risk_data[
        [
            "order_id",
            "order_purchase_timestamp",
            "customer_state",
            "order_revenue",
        ]
    ].copy()

    result["late_risk_probability"] = (
        probabilities
    )

    result["risk_level"] = (
        result["late_risk_probability"]
        .apply(classify_risk_level)
    )

    result = (
        result
        .sort_values(
            "late_risk_probability",
            ascending=False,
        )
        .head(top_n)
        .copy()
    )

    result["order_purchase_timestamp"] = (
        pd.to_datetime(
            result["order_purchase_timestamp"]
        )
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )

    return result.to_dict(
        orient="records"
    )