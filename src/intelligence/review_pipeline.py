from pathlib import Path

import pandas as pd

from src.intelligence.review_preprocessing import (
    prepare_review_dataset,
)
from src.intelligence.review_classifier import (
    classify_reviews_batch,
)
from src.intelligence.review_cache import (
    load_review_cache,
    save_review_cache,
    get_uncached_reviews,
)


def process_reviews(
    orders: pd.DataFrame,
    cache_path: Path,
    limit: int | None = None,
    max_attempts: int = 2,
) -> pd.DataFrame:
    """
    Prepare, classify, and cache customer reviews.

    Only reviews not already present in the cache
    are sent to Groq.
    """

    reviews = prepare_review_dataset(
        orders
    )

    cache = load_review_cache(
        cache_path
    )

    uncached = get_uncached_reviews(
        reviews,
        cache,
    )

    if limit is not None:
        if limit <= 0:
            raise ValueError(
                "limit must be greater than 0."
            )

        uncached = uncached.head(
            limit
        )

    if not uncached.empty:

        review_records = uncached[
            [
                "order_id",
                "review_comment_message",
            ]
        ].to_dict(
            orient="records"
        )

        classifications = classify_reviews_batch(
            review_records,
            max_attempts=max_attempts,
        )

        save_review_cache(
            classifications,
            cache_path,
        )

    return load_review_cache(
        cache_path
    )