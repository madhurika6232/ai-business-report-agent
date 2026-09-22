from pathlib import Path

import pandas as pd
import pytest

from src.analytics.validation import (
    filter_orders,
    validate_required_columns,
    validate_date_range,
)


DATA_DIR = Path("data/processed")


@pytest.fixture(scope="module")
def orders():
    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


def test_filter_by_state(orders):
    result = filter_orders(
        orders,
        customer_state="SP",
    )

    assert len(result) > 0
    assert result["customer_state"].eq("SP").all()


def test_filter_by_category(orders):
    result = filter_orders(
        orders,
        category="furniture_decor",
    )

    assert result["order_id"].nunique() == 6397


def test_combined_filters(orders):
    result = filter_orders(
        orders,
        start_date="2018-01-01",
        end_date="2018-03-31 23:59:59",
        customer_state="SP",
        category="furniture_decor",
    )

    assert result["order_id"].nunique() == 515
    assert result["customer_state"].eq("SP").all()


def test_missing_required_column():
    df = pd.DataFrame({
        "order_id": ["A"]
    })

    with pytest.raises(
        ValueError,
        match="missing required columns",
    ):
        validate_required_columns(
            df,
            ["order_id", "customer_state"],
            "test_data",
        )


def test_invalid_date_range():
    with pytest.raises(
        ValueError,
        match="start_date cannot be after end_date",
    ):
        validate_date_range(
            "2018-05-01",
            "2018-01-01",
        )


def test_valid_date_range():
    validate_date_range(
        "2018-01-01",
        "2018-05-01",
    )