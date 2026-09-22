from pathlib import Path

import pandas as pd
import pytest

from src.ml.anomaly import (
    build_anomaly_dataset,
    detect_metric_anomalies,
    classify_anomalies,
)


DATA_DIR = Path("data/processed")


@pytest.fixture(scope="module")
def orders():
    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


@pytest.fixture(scope="module")
def anomaly_data(orders):
    return build_anomaly_dataset(orders)


def test_anomaly_dataset(anomaly_data):
    assert len(anomaly_data) == 20

    assert anomaly_data["revenue"].notna().all()

    assert anomaly_data["late_rate"].between(
        0,
        100,
    ).all()

    assert anomaly_data["avg_review_score"].between(
        1,
        5,
    ).all()


def test_late_delivery_anomalies(anomaly_data):
    result = detect_metric_anomalies(
        anomaly_data,
        metric="late_rate",
        window=6,
        threshold=2.0,
    )

    assert result["is_anomaly"].sum() == 4

    anomaly_months = set(
        result.loc[
            result["is_anomaly"],
            "order_month",
        ].dt.strftime("%Y-%m")
    )

    assert "2017-11" in anomaly_months
    assert "2018-02" in anomaly_months
    assert "2018-03" in anomaly_months


def test_anomaly_classification(anomaly_data):
    detected = detect_metric_anomalies(
        anomaly_data,
        metric="late_rate",
        window=6,
        threshold=2.0,
    )

    result = classify_anomalies(
        detected,
        higher_is_bad=True,
    )

    november = result[
        result["order_month"]
        == pd.Timestamp("2017-11-01")
    ].iloc[0]

    assert bool(november["is_anomaly"]) is True
    assert november["direction"] == "increase"
    assert november["impact"] == "negative"
    assert november["severity"] == "critical"


def test_review_anomaly_direction(anomaly_data):
    detected = detect_metric_anomalies(
        anomaly_data,
        metric="avg_review_score",
        window=6,
        threshold=2.0,
    )

    result = classify_anomalies(
        detected,
        higher_is_bad=False,
    )

    november = result[
        result["order_month"]
        == pd.Timestamp("2017-11-01")
    ].iloc[0]

    assert november["impact"] == "negative"


def test_invalid_metric(anomaly_data):
    with pytest.raises(
        ValueError,
        match="does not exist",
    ):
        detect_metric_anomalies(
            anomaly_data,
            metric="fake_metric",
        )