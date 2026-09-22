from pathlib import Path

import pandas as pd
import pytest

from src.intelligence.review_preprocessing import (
    prepare_review_dataset,
)


DATA_DIR = Path("data/processed")


@pytest.fixture(scope="module")
def orders():
    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


def test_prepare_review_dataset(orders):
    result = prepare_review_dataset(
        orders
    )

    assert len(result) == 40497

    assert (
        result["order_id"].nunique()
        == 40497
    )

    assert (
        result["review_comment_message"]
        .notna()
        .all()
    )

    assert (
        result["review_comment_message"]
        .str.len()
        .gt(0)
        .all()
    )


def test_review_dataset_columns(orders):
    result = prepare_review_dataset(
        orders
    )

    required = {
        "order_id",
        "order_month",
        "review_score",
        "review_comment_message",
        "product_categories",
        "is_late",
        "delay_days",
        "customer_state",
    }

    assert required.issubset(
        result.columns
    )


def test_missing_required_columns():
    bad_data = pd.DataFrame({
        "order_id": ["test"]
    })

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        prepare_review_dataset(
            bad_data
        )