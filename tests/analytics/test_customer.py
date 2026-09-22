from pathlib import Path

import pandas as pd
import pytest

from src.analytics.customer import (
    get_review_summary,
    get_review_trend,
    get_delivery_review_impact,
    get_delay_severity_impact,
)


DATA_DIR = Path("data/processed")


@pytest.fixture(scope="module")
def orders():
    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


def test_review_summary(orders):
    result = get_review_summary(orders)

    assert result["total_reviews"] == 98330
    assert result["negative_reviews"] == 14383
    assert result["written_comments"] == 40524

    assert result["avg_review_score"] == pytest.approx(
        4.09,
        abs=0.01,
    )

    assert result["negative_review_rate"] == pytest.approx(
        14.63,
        abs=0.01,
    )

    assert result["positive_review_rate"] == pytest.approx(
        77.12,
        abs=0.01,
    )


def test_review_trend(orders):
    result = get_review_trend(orders)

    assert len(result) == 20

    assert result["avg_review_score"].between(
        1,
        5,
    ).all()

    assert result["negative_review_rate"].between(
        0,
        100,
    ).all()

    worst_month = result.loc[
        result["avg_review_score"].idxmin()
    ]

    assert worst_month[
        "order_month"
    ].strftime("%Y-%m") == "2018-03"

    assert worst_month["avg_review_score"] == pytest.approx(
        3.75,
        abs=0.01,
    )

    assert worst_month["negative_review_rate"] == pytest.approx(
        22.80,
        abs=0.01,
    )


def test_delivery_review_impact(orders):
    result = get_delivery_review_impact(orders)

    assert len(result) == 2

    on_time = result[
        result["delivery_status"] == "On time"
    ].iloc[0]

    late = result[
        result["delivery_status"] == "Late"
    ].iloc[0]

    assert on_time["avg_review_score"] == pytest.approx(
        4.29,
        abs=0.01,
    )

    assert late["avg_review_score"] == pytest.approx(
        2.57,
        abs=0.01,
    )

    assert on_time["negative_review_rate"] == pytest.approx(
        9.20,
        abs=0.01,
    )

    assert late["negative_review_rate"] == pytest.approx(
        54.04,
        abs=0.01,
    )

    assert (
        on_time["avg_review_score"]
        > late["avg_review_score"]
    )


def test_delay_severity_impact(orders):
    result = get_delay_severity_impact(orders)

    assert len(result) == 5

    assert result["avg_review_score"].between(
        1,
        5,
    ).all()

    assert result["negative_review_rate"].between(
        0,
        100,
    ).all()

    on_time = result[
        result["delay_bucket"] == "On time"
    ].iloc[0]

    severe = result[
        result["delay_bucket"] == "15+ days late"
    ].iloc[0]

    assert on_time["avg_review_score"] > severe[
        "avg_review_score"
    ]