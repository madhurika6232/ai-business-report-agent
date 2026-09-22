from pathlib import Path

import pandas as pd
import pytest

from src.analytics.operations import (
    get_delivery_summary,
    get_delivery_trend,
    get_high_risk_sellers,
    get_cancellation_metrics,
    get_freight_metrics,
)


DATA_DIR = Path("data/processed")


@pytest.fixture(scope="module")
def orders():
    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


@pytest.fixture(scope="module")
def sellers():
    return pd.read_csv(
        DATA_DIR / "seller_metrics.csv"
    )


def test_delivery_summary(orders):
    result = get_delivery_summary(orders)

    assert result["delivered_orders"] == 96204
    assert result["evaluated_deliveries"] == 96204
    assert result["late_orders"] == 7823

    assert result["late_rate"] == pytest.approx(
        8.13,
        abs=0.01,
    )

    assert result["avg_delivery_days"] == pytest.approx(
        12.54,
        abs=0.01,
    )


def test_delivery_trend(orders):
    result = get_delivery_trend(orders)

    assert len(result) == 20

    assert result["late_rate"].between(
        0,
        100,
    ).all()

    assert (
        result["avg_delivery_days"] >= 0
    ).all()

    worst_month = result.loc[
        result["late_rate"].idxmax()
    ]

    assert worst_month[
        "order_month"
    ].strftime("%Y-%m") == "2018-03"

    assert worst_month["late_rate"] == pytest.approx(
        21.36,
        abs=0.01,
    )


def test_high_risk_sellers(sellers):
    result = get_high_risk_sellers(
        sellers,
        min_orders=30,
        top_n=10,
    )

    assert len(result) == 10

    assert (
        result["orders"] >= 30
    ).all()

    assert result["late_rate"].between(
        0,
        100,
    ).all()

    assert result.iloc[0]["late_rate"] == pytest.approx(
        34.88,
        abs=0.01,
    )


def test_cancellation_metrics(orders):
    result = get_cancellation_metrics(orders)

    assert result["total_orders"] == 99092
    assert result["canceled_orders"] == 580

    assert result["cancellation_rate"] == pytest.approx(
        0.59,
        abs=0.01,
    )


def test_freight_metrics(orders):
    result = get_freight_metrics(orders)

    assert result["total_freight"] == pytest.approx(
        2244490.79,
        abs=0.01,
    )

    assert result["avg_freight_per_order"] == pytest.approx(
        22.82,
        abs=0.01,
    )

    assert result["freight_to_revenue_pct"] == pytest.approx(
        16.57,
        abs=0.01,
    )


def test_high_risk_sellers_invalid_min_orders(sellers):
    with pytest.raises(ValueError):
        get_high_risk_sellers(
            sellers,
            min_orders=0,
        )


def test_high_risk_sellers_invalid_top_n(sellers):
    with pytest.raises(ValueError):
        get_high_risk_sellers(
            sellers,
            top_n=0,
        )