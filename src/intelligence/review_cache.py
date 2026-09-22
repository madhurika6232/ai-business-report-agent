from pathlib import Path

import pandas as pd


CACHE_COLUMNS = [
    "order_id",
    "review_comment_message",
    "sentiment",
    "primary_issue",
    "secondary_issue",
    "severity",
    "confidence",
    "summary",
    "classification_status",
    "error",
]


def load_review_cache(
    cache_path: Path,
) -> pd.DataFrame:
    """Load existing review classifications."""

    if not cache_path.exists():
        return pd.DataFrame(
            columns=CACHE_COLUMNS
        )

    return pd.read_csv(cache_path)


def save_review_cache(
    records: list[dict],
    cache_path: Path,
) -> None:
    """Save review classifications to the cache."""

    cache_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    new_data = pd.DataFrame(records)

    if cache_path.exists():
        existing = pd.read_csv(
            cache_path
        )

        combined = pd.concat(
            [existing, new_data],
            ignore_index=True,
        )

    else:
        combined = new_data

    # Keep the latest classification per order.
    combined = combined.drop_duplicates(
        subset="order_id",
        keep="last",
    )

    combined.to_csv(
        cache_path,
        index=False,
    )


def get_uncached_reviews(
    reviews: pd.DataFrame,
    cache: pd.DataFrame,
) -> pd.DataFrame:
    """Return reviews that have not already been classified."""

    if cache.empty:
        return reviews.copy()

    cached_orders = set(
        cache["order_id"]
        .dropna()
        .astype(str)
    )

    return reviews[
        ~reviews["order_id"]
        .astype(str)
        .isin(cached_orders)
    ].copy()