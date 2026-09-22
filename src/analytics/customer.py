import pandas as pd


def get_review_summary(orders: pd.DataFrame) -> dict:
    """Calculate customer satisfaction KPIs."""

    reviewed = orders[
        orders["review_score"].notna()
    ].copy()

    total_reviews = len(reviewed)

    negative_reviews = (
        reviewed["review_score"] <= 2
    ).sum()

    positive_reviews = (
        reviewed["review_score"] >= 4
    ).sum()

    written_comments = (
        reviewed["review_comment_message"]
        .notna()
        .sum()
    )

    return {
        "total_reviews": int(total_reviews),
        "avg_review_score": round(
            float(reviewed["review_score"].mean()),
            2,
        ),
        "negative_reviews": int(negative_reviews),
        "negative_review_rate": round(
            float(negative_reviews / total_reviews * 100),
            2,
        ) if total_reviews > 0 else 0,
        "positive_review_rate": round(
            float(positive_reviews / total_reviews * 100),
            2,
        ) if total_reviews > 0 else 0,
        "written_comments": int(written_comments),
    }

def get_review_trend(orders: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly customer satisfaction trends."""

    reviewed = orders[
        orders["review_score"].notna()
    ].copy()

    reviewed["order_month"] = pd.to_datetime(
        reviewed["order_month"]
    )

    reviewed["is_negative"] = (
        reviewed["review_score"] <= 2
    )

    monthly = (
        reviewed
        .groupby("order_month")
        .agg(
            reviews=("order_id", "nunique"),
            avg_review_score=("review_score", "mean"),
            negative_reviews=("is_negative", "sum"),
        )
        .reset_index()
        .sort_values("order_month")
    )

    monthly["negative_review_rate"] = (
        monthly["negative_reviews"]
        / monthly["reviews"]
        * 100
    )

    return monthly

def get_delivery_review_impact(
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """Compare customer satisfaction for on-time vs late deliveries."""

    df = orders[
        orders["review_score"].notna()
        & orders["is_late"].notna()
    ].copy()

    # CSV loading may represent boolean values differently.
    if df["is_late"].dtype != bool:
        df["is_late"] = (
            df["is_late"]
            .astype(str)
            .str.lower()
            .map({"true": True, "false": False})
        )

    df["is_negative_review"] = (
        df["review_score"] <= 2
    )

    result = (
        df.groupby("is_late")
        .agg(
            orders=("order_id", "nunique"),
            avg_review_score=("review_score", "mean"),
            negative_reviews=("is_negative_review", "sum"),
        )
        .reset_index()
    )

    result["negative_review_rate"] = (
        result["negative_reviews"]
        / result["orders"]
        * 100
    )

    result["delivery_status"] = result["is_late"].map({
        False: "On time",
        True: "Late",
    })

    return result[
        [
            "delivery_status",
            "orders",
            "avg_review_score",
            "negative_reviews",
            "negative_review_rate",
        ]
    ]

def get_delay_severity_impact(
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """Measure customer satisfaction across delivery-delay severity."""

    df = orders[
        orders["review_score"].notna()
        & orders["delay_days"].notna()
    ].copy()

    df["delay_bucket"] = pd.cut(
        df["delay_days"],
        bins=[
            -float("inf"),
            0,
            3,
            7,
            14,
            float("inf"),
        ],
        labels=[
            "On time",
            "1-3 days late",
            "4-7 days late",
            "8-14 days late",
            "15+ days late",
        ],
    )

    df["is_negative_review"] = (
        df["review_score"] <= 2
    )

    result = (
        df.groupby(
            "delay_bucket",
            observed=True,
        )
        .agg(
            orders=("order_id", "nunique"),
            avg_review_score=("review_score", "mean"),
            negative_reviews=("is_negative_review", "sum"),
        )
        .reset_index()
    )

    result["negative_review_rate"] = (
        result["negative_reviews"]
        / result["orders"]
        * 100
    )

    return result