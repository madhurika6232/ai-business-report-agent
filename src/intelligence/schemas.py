from typing import Literal
from pydantic import BaseModel, Field


ReviewSentiment = Literal[
    "positive",
    "neutral",
    "negative",
]

ReviewIssue = Literal[
    "delivery_delay",
    "non_delivery",
    "damaged_product",
    "wrong_product",
    "missing_item",
    "product_quality",
    "seller_service",
    "customer_service",
    "billing_payment",
    "expectation_mismatch",
    "positive_feedback",
    "other",
]

ReviewSeverity = Literal[
    "low",
    "medium",
    "high",
]

ReviewConfidence = Literal[
    "low",
    "medium",
    "high",
]


class ReviewClassification(BaseModel):
    """Structured classification produced for one customer review."""

    sentiment: ReviewSentiment

    primary_issue: ReviewIssue

    secondary_issue: ReviewIssue | None = None

    severity: ReviewSeverity

    confidence: ReviewConfidence

    summary: str = Field(
        min_length=1,
        max_length=200,
    )