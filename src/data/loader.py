from pathlib import Path

import pandas as pd


def load_raw_data(data_dir: Path) -> dict[str, pd.DataFrame]:
    """Load the raw Olist datasets."""

    datasets = {
        "orders": pd.read_csv(data_dir / "olist_orders_dataset.csv"),
        "order_items": pd.read_csv(data_dir / "olist_order_items_dataset.csv"),
        "customers": pd.read_csv(data_dir / "olist_customers_dataset.csv"),
        "products": pd.read_csv(data_dir / "olist_products_dataset.csv"),
        "sellers": pd.read_csv(data_dir / "olist_sellers_dataset.csv"),
        "payments": pd.read_csv(data_dir / "olist_order_payments_dataset.csv"),
        "reviews": pd.read_csv(data_dir / "olist_order_reviews_dataset.csv"),
        "category_translation": pd.read_csv(
            data_dir / "product_category_name_translation.csv"
        ),
    }

    return datasets