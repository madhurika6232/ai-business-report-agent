from pathlib import Path

import pandas as pd
import pytest

from src.analytics.business import (
    get_business_summary,
    get_monthly_performance,
    get_category_performance,
    get_state_performance,
)


DATA_DIR = Path("data/processed")


@pytest.fixture(scope="module")
def orders():
    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


@pytest.fixture(scope="module")
def categories():
    return pd.read_csv(
        DATA_DIR / "category_metrics.csv"
    )


def test_business_summary(orders):
    summary = get_business_summary(orders)

    assert summary["total_orders"] == 99092
    assert summary["unique_customers"] == 95774
    assert summary["total_items"] == 112279

    assert summary["total_revenue"] == pytest.approx(
        13541712.78,
        abs=0.01,
    )

    assert summary["average_order_value"] == pytest.approx(
        136.66,
        abs=0.01,
    )


def test_monthly_performance(orders):
    monthly = get_monthly_performance(orders)

    assert len(monthly) == 20

    assert monthly["revenue"].sum() == pytest.approx(
        13541712.78,
        abs=0.01,
    )

    assert monthly["orders"].sum() == 99092

    peak_month = monthly.loc[
        monthly["revenue"].idxmax()
    ]

    assert peak_month["order_month"].strftime(
        "%Y-%m"
    ) == "2017-11"


def test_category_performance(categories):
    result = get_category_performance(
        categories,
        top_n=10,
    )

    assert len(result) == 10

    assert (
        result.iloc[0]["product_category_name_english"]
        == "health_beauty"
    )

    assert result.iloc[0]["revenue"] == pytest.approx(
        1253993.86,
        abs=0.01,
    )

    assert result["revenue_share_pct"].between(
        0,
        100,
    ).all()


def test_state_performance(orders):
    result = get_state_performance(
        orders,
        top_n=10,
    )

    assert len(result) == 10
    assert result.iloc[0]["customer_state"] == "SP"

    assert result.iloc[0]["revenue"] == pytest.approx(
        5188099.23,
        abs=0.01,
    )

    assert result["revenue_share_pct"].between(
        0,
        100,
    ).all()


def test_category_invalid_top_n(categories):
    with pytest.raises(ValueError):
        get_category_performance(
            categories,
            top_n=0,
        )


def test_state_invalid_top_n(orders):
    with pytest.raises(ValueError):
        get_state_performance(
            orders,
            top_n=0,
        )