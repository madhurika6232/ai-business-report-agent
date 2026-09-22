import pandas as pd


def prepare_review_dataset(
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """Prepare written customer reviews for review intelligence."""

    required_columns = [
        "order_id",
        "order_month",
        "review_score",
        "review_comment_message",
        "product_categories",
        "is_late",
        "delay_days",
        "customer_state",
    ]

    missing = [
        column
        for column in required_columns
        if column not in orders.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )

    reviews = orders[
        required_columns
    ].copy()

    # Keep only actual written comments.
    reviews = reviews[
        reviews["review_comment_message"].notna()
    ].copy()

    # Normalize whitespace without altering meaning.
    reviews["review_comment_message"] = (
        reviews["review_comment_message"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Remove empty comments.
    reviews = reviews[
        reviews["review_comment_message"].str.len() > 0
    ].copy()

    reviews["order_month"] = pd.to_datetime(
        reviews["order_month"]
    )

    return reviews.reset_index(drop=True)