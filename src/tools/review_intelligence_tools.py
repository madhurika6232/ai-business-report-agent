from pathlib import Path

import pandas as pd

from src.intelligence.review_insights import (
    get_complaint_themes,
    get_negative_complaint_themes,
    build_operational_evidence,
    get_delivery_complaint_evidence,
    generate_grounded_review_insight,
)


DATA_DIR = Path("data/processed")

CLASSIFICATION_PATH = (
    DATA_DIR / "review_sample_classifications.csv"
)

ORDERS_PATH = (
    DATA_DIR / "orders_enriched.csv"
)


def _load_classifications() -> pd.DataFrame:
    """Load cached Groq review classifications."""

    if not CLASSIFICATION_PATH.exists():
        raise FileNotFoundError(
            "Review classifications have not been generated."
        )

    return pd.read_csv(
        CLASSIFICATION_PATH
    )


def _load_orders() -> pd.DataFrame:
    """Load processed order data."""

    return pd.read_csv(
        ORDERS_PATH
    )


def complaint_themes_tool(
    negative_only: bool = True,
) -> list[dict]:
    """Return customer-review issue themes."""

    classifications = _load_classifications()

    if negative_only:
        result = get_negative_complaint_themes(
            classifications
        )
    else:
        result = get_complaint_themes(
            classifications
        )

    return result.to_dict(
        orient="records"
    )


def delivery_complaint_evidence_tool() -> dict:
    """
    Compare customer-reported delivery complaints
    with structured delivery evidence.
    """

    classifications = _load_classifications()
    orders = _load_orders()

    evidence = build_operational_evidence(
        classifications,
        orders,
    )

    return get_delivery_complaint_evidence(
        evidence
    )


def grounded_customer_insight_tool() -> str:
    """
    Generate an evidence-grounded customer-experience
    insight using cached review classifications and
    structured operational data.
    """

    classifications = _load_classifications()
    orders = _load_orders()

    themes = get_negative_complaint_themes(
        classifications
    )

    evidence = build_operational_evidence(
        classifications,
        orders,
    )

    delivery_evidence = (
        get_delivery_complaint_evidence(
            evidence
        )
    )

    return generate_grounded_review_insight(
        themes,
        delivery_evidence,
    )