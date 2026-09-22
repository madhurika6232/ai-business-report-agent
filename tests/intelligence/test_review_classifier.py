import pytest
from pydantic import ValidationError

from src.intelligence.schemas import (
    ReviewClassification,
)

from src.intelligence.review_classifier import (
    classify_review_safe,
)


def test_valid_review_classification():
    result = ReviewClassification(
        sentiment="negative",
        primary_issue="delivery_delay",
        secondary_issue=None,
        severity="high",
        confidence="high",
        summary="Customer reports a delivery delay.",
    )

    assert result.sentiment == "negative"
    assert result.primary_issue == "delivery_delay"
    assert result.severity == "high"


def test_invalid_issue_rejected():
    with pytest.raises(
        ValidationError
    ):
        ReviewClassification(
            sentiment="negative",
            primary_issue="fake_issue",
            severity="high",
            confidence="high",
            summary="Test classification.",
        )


def test_invalid_sentiment_rejected():
    with pytest.raises(
        ValidationError
    ):
        ReviewClassification(
            sentiment="angry",
            primary_issue="other",
            severity="high",
            confidence="high",
            summary="Test classification.",
        )


def test_empty_summary_rejected():
    with pytest.raises(
        ValidationError
    ):
        ReviewClassification(
            sentiment="negative",
            primary_issue="other",
            severity="low",
            confidence="low",
            summary="",
        )


def test_invalid_retry_count():
    with pytest.raises(
        ValueError,
        match="max_attempts must be greater than 0",
    ):
        classify_review_safe(
            "Test review",
            max_attempts=0,
        )