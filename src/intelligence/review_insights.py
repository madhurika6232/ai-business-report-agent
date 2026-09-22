import pandas as pd


def get_complaint_themes(
    classifications: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize issue themes from successfully classified reviews."""

    successful = classifications[
        classifications["classification_status"] == "success"
    ].copy()

    if successful.empty:
        return pd.DataFrame(
            columns=[
                "primary_issue",
                "reviews",
                "percentage",
            ]
        )

    themes = (
        successful
        .groupby("primary_issue")
        .size()
        .reset_index(name="reviews")
    )

    themes["percentage"] = (
        themes["reviews"]
        / themes["reviews"].sum()
        * 100
    )

    return (
        themes
        .sort_values(
            "reviews",
            ascending=False,
        )
        .reset_index(drop=True)
    )

def get_negative_complaint_themes(
    classifications: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize complaint themes among negative reviews."""

    negative = classifications[
        (classifications["classification_status"] == "success")
        & (classifications["sentiment"] == "negative")
    ].copy()

    if negative.empty:
        return pd.DataFrame(
            columns=[
                "primary_issue",
                "reviews",
                "percentage",
            ]
        )

    themes = (
        negative
        .groupby("primary_issue")
        .size()
        .reset_index(name="reviews")
    )

    themes["percentage"] = (
        themes["reviews"]
        / themes["reviews"].sum()
        * 100
    )

    return (
        themes
        .sort_values(
            "reviews",
            ascending=False,
        )
        .reset_index(drop=True)
    )

def build_operational_evidence(
    classifications: pd.DataFrame,
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """Connect classified review issues to structured operational data."""

    successful = classifications[
        classifications["classification_status"] == "success"
    ].copy()

    evidence = successful.merge(
        orders[
            [
                "order_id",
                "review_score",
                "is_late",
                "delay_days",
                "order_status",
                "product_categories",
            ]
        ],
        on="order_id",
        how="left",
    )

    # Normalize boolean values loaded from CSV.
    evidence["is_late_normalized"] = (
        evidence["is_late"]
        .astype(str)
        .str.lower()
        .map({
            "true": True,
            "false": False,
        })
    )

    return evidence

def get_delivery_complaint_evidence(
    evidence: pd.DataFrame,
) -> dict:
    """Measure structured delivery evidence for delivery-related complaints."""

    delivery_issues = evidence[
        evidence["primary_issue"].isin(
            [
                "delivery_delay",
                "non_delivery",
            ]
        )
    ].copy()

    delay_complaints = delivery_issues[
        delivery_issues["primary_issue"]
        == "delivery_delay"
    ]

    non_delivery_complaints = delivery_issues[
        delivery_issues["primary_issue"]
        == "non_delivery"
    ]

    known_delivery = delay_complaints[
        delay_complaints[
            "is_late_normalized"
        ].notna()
    ]

    confirmed_late = (
        known_delivery[
            "is_late_normalized"
        ].eq(True).sum()
    )

    confirmation_rate = (
        confirmed_late / len(known_delivery) * 100
        if len(known_delivery) > 0
        else 0
    )

    return {
        "delivery_related_complaints": int(
            len(delivery_issues)
        ),
        "delivery_delay_complaints": int(
            len(delay_complaints)
        ),
        "non_delivery_complaints": int(
            len(non_delivery_complaints)
        ),
        "delay_complaints_with_known_delivery": int(
            len(known_delivery)
        ),
        "confirmed_late_deliveries": int(
            confirmed_late
        ),
        "delay_confirmation_rate": round(
            float(confirmation_rate),
            2,
        ),
    }

import json

from src.intelligence.groq_client import (
    DEFAULT_MODEL,
    get_groq_client,
)

def generate_grounded_review_insight(
    themes: pd.DataFrame,
    delivery_evidence: dict,
) -> str:
    """Generate a concise insight using only supplied evidence."""

    client = get_groq_client()

    evidence = {
        "negative_complaint_themes": themes.to_dict(
            orient="records"
        ),
        "delivery_evidence": delivery_evidence,
    }

    prompt = f"""
You are analyzing a SAMPLE of customer reviews from an e-commerce marketplace.

Use ONLY the evidence provided below.

Evidence:
{json.dumps(evidence, ensure_ascii=False)}

STRICT RULES:

1. All complaint-theme percentages refer only to NEGATIVE REVIEWS
   in the analyzed sample. Never describe them as percentages of
   all reviews or all customers.

2. "delivery_delay" is a customer-reported complaint category.

3. "confirmed_late_deliveries" means the structured order data shows
   delivery occurred after the marketplace's estimated delivery date.

4. If a delivery-delay complaint is not confirmed by structured data,
   do NOT call the customer wrong, mistaken, misleading, or inaccurate.

5. A disagreement may occur because customer perception of slow delivery
   is different from the marketplace's promised delivery window.

6. Do not invent explanations such as carrier problems, seller problems,
   communication failures, or tracking problems unless supplied in evidence.

7. Do not claim causation.

8. Do not generalize this sample to the entire marketplace.

9. Clearly distinguish:
   - customer-reported evidence
   - structured operational evidence

Write a concise business insight in English containing:

- Main complaint themes among negative reviews in this sample
- What structured delivery evidence supports
- Important uncertainty or disagreement
- One investigation recommendation supported by the evidence

Keep the response under 180 words.
"""

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an evidence-grounded retail analytics assistant. "
                    "Never introduce facts that are absent from the supplied evidence."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content.strip()