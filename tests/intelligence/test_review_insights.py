from pathlib import Path

import pandas as pd
import pytest

from src.intelligence.review_cache import (
    load_review_cache,
    save_review_cache,
    get_uncached_reviews,
)

from src.intelligence.review_insights import (
    get_complaint_themes,
    get_negative_complaint_themes,
    build_operational_evidence,
    get_delivery_complaint_evidence,
)


DATA_DIR = Path("data/processed")


@pytest.fixture(scope="module")
def classifications():
    return pd.read_csv(
        DATA_DIR / "review_sample_classifications.csv"
    )


@pytest.fixture(scope="module")
def orders():
    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


def test_complaint_themes(classifications):
    result = get_complaint_themes(
        classifications
    )

    assert len(result) > 0

    assert result["percentage"].sum() == pytest.approx(
        100.0,
        abs=0.01,
    )


def test_negative_complaint_themes(classifications):
    result = get_negative_complaint_themes(
        classifications
    )

    assert len(result) > 0

    assert result["percentage"].sum() == pytest.approx(
        100.0,
        abs=0.01,
    )

    assert result.iloc[0]["primary_issue"] == "non_delivery"


def test_operational_evidence(
    classifications,
    orders,
):
    result = build_operational_evidence(
        classifications,
        orders,
    )

    assert len(result) == 200

    assert "is_late_normalized" in result.columns


def test_delivery_complaint_evidence(
    classifications,
    orders,
):
    evidence = build_operational_evidence(
        classifications,
        orders,
    )

    result = get_delivery_complaint_evidence(
        evidence
    )

    assert result["delivery_related_complaints"] == 23
    assert result["delivery_delay_complaints"] == 10
    assert result["non_delivery_complaints"] == 13
    assert result["confirmed_late_deliveries"] == 4

    assert result["delay_confirmation_rate"] == pytest.approx(
        40.0,
        abs=0.01,
    )


def test_review_cache(tmp_path):
    cache_path = (
        tmp_path / "review_cache.csv"
    )

    records = [
        {
            "order_id": "A",
            "review_comment_message": "Produto atrasado",
            "sentiment": "negative",
            "primary_issue": "delivery_delay",
            "secondary_issue": None,
            "severity": "high",
            "confidence": "high",
            "summary": "Late product.",
            "classification_status": "success",
            "error": None,
        }
    ]

    save_review_cache(
        records,
        cache_path,
    )

    cache = load_review_cache(
        cache_path
    )

    assert len(cache) == 1

    reviews = pd.DataFrame([
        {
            "order_id": "A",
            "review_comment_message": "Produto atrasado",
        },
        {
            "order_id": "B",
            "review_comment_message": "Produto quebrado",
        },
    ])

    uncached = get_uncached_reviews(
        reviews,
        cache,
    )

    assert len(uncached) == 1
    assert uncached.iloc[0]["order_id"] == "B"