from pathlib import Path

from src.data.loader import load_raw_data
from src.data.cleaner import clean_orders, clean_reviews
from src.data.features import (
    add_order_features,
    add_order_financials,
    add_customer_features,
    add_review_features,
    add_category_features,
    add_seller_features,
    build_seller_metrics,
    build_category_metrics,
)


def build_data_pipeline(
    raw_dir: Path,
    processed_dir: Path,
) -> None:
    """Build and save all processed RetailOps datasets."""

    # Load
    datasets = load_raw_data(raw_dir)

    # Clean
    orders_clean = clean_orders(datasets["orders"])
    reviews_clean = clean_reviews(datasets["reviews"])

    # Build enriched order dataset
    orders_enriched = add_order_features(orders_clean)

    orders_enriched = add_order_financials(
        orders_enriched,
        datasets["order_items"],
    )

    orders_enriched = add_customer_features(
        orders_enriched,
        datasets["customers"],
    )

    orders_enriched = add_review_features(
        orders_enriched,
        reviews_clean,
    )

    orders_enriched = add_category_features(
        orders_enriched,
        datasets["order_items"],
        datasets["products"],
        datasets["category_translation"],
    )

    orders_enriched = add_seller_features(
        orders_enriched,
        datasets["order_items"],
    )

    # Build aggregated datasets
    seller_metrics = build_seller_metrics(
        orders_enriched,
        datasets["order_items"],
        datasets["sellers"],
    )

    category_metrics = build_category_metrics(
        orders_enriched,
        datasets["order_items"],
        datasets["products"],
        datasets["category_translation"],
    )

    # Create output directory
    processed_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save
    orders_enriched.to_csv(
        processed_dir / "orders_enriched.csv",
        index=False,
    )

    seller_metrics.to_csv(
        processed_dir / "seller_metrics.csv",
        index=False,
    )

    category_metrics.to_csv(
        processed_dir / "category_metrics.csv",
        index=False,
    )

    print("Data pipeline completed successfully.")
    print(f"Orders: {len(orders_enriched):,}")
    print(f"Sellers: {len(seller_metrics):,}")
    print(f"Categories: {len(category_metrics):,}")