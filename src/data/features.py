import pandas as pd
def add_order_features(orders: pd.DataFrame) -> pd.DataFrame:
    """Create operational features at the order level."""

    df = orders.copy()

    df["order_month"] = (
        df["order_purchase_timestamp"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    df["is_canceled"] = df["order_status"] == "canceled"

    df["delivery_days"] = (
        df["order_delivered_customer_date"]
        - df["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    df["delay_days"] = (
        df["order_delivered_customer_date"]
        - df["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    df["is_late"] = (
        df["order_delivered_customer_date"]
        > df["order_estimated_delivery_date"]
    ).astype("boolean")

    # Delivery status is unknown when no actual delivery date exists.
    df.loc[
        df["order_delivered_customer_date"].isna(),
        "is_late"
    ] = pd.NA

    return df

def add_order_financials(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> pd.DataFrame:
    """Add revenue, freight, and item-count features to orders."""

    order_financials = (
        order_items
        .groupby("order_id")
        .agg(
            order_revenue=("price", "sum"),
            freight_value=("freight_value", "sum"),
            item_count=("order_item_id", "count"),
        )
        .reset_index()
    )

    return orders.merge(
        order_financials,
        on="order_id",
        how="left",
    )

def add_customer_features(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
) -> pd.DataFrame:
    """Add customer identity and location features."""

    customer_info = customers[
        [
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "customer_state",
        ]
    ].copy()

    return orders.merge(
        customer_info,
        on="customer_id",
        how="left",
    )

def add_review_features(
    orders: pd.DataFrame,
    reviews: pd.DataFrame,
) -> pd.DataFrame:
    """Add customer review features to orders."""

    review_info = reviews[
        [
            "order_id",
            "review_score",
            "review_comment_message",
        ]
    ].copy()

    review_info["is_negative_review"] = (
        review_info["review_score"] <= 2
    )

    review_info["has_review_comment"] = (
        review_info["review_comment_message"].notna()
    )

    return orders.merge(
        review_info,
        on="order_id",
        how="left",
    )

def add_category_features(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
    category_translation: pd.DataFrame,
) -> pd.DataFrame:
    """Add product-category information while preserving one row per order."""

    order_categories = (
        order_items[["order_id", "product_id"]]
        .merge(
            products[["product_id", "product_category_name"]],
            on="product_id",
            how="left",
        )
        .merge(
            category_translation,
            on="product_category_name",
            how="left",
        )
    )

    order_categories["product_category_name_english"] = (
        order_categories["product_category_name_english"]
        .fillna("unknown")
    )

    category_info = (
        order_categories
        .groupby("order_id")
        .agg(
            product_categories=(
                "product_category_name_english",
                lambda x: ", ".join(sorted(set(x))),
            ),
            category_count=(
                "product_category_name_english",
                "nunique",
            ),
        )
        .reset_index()
    )

    return orders.merge(
        category_info,
        on="order_id",
        how="left",
    )

def add_seller_features(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> pd.DataFrame:
    """Add seller information while preserving one row per order."""

    seller_info = (
        order_items
        .groupby("order_id")
        .agg(
            seller_ids=(
                "seller_id",
                lambda x: ", ".join(sorted(set(x))),
            ),
            seller_count=(
                "seller_id",
                "nunique",
            ),
        )
        .reset_index()
    )

    return orders.merge(
        seller_info,
        on="order_id",
        how="left",
    )

def build_seller_metrics(
    orders_enriched: pd.DataFrame,
    order_items: pd.DataFrame,
    sellers: pd.DataFrame,
) -> pd.DataFrame:
    """Build one-row-per-seller performance metrics."""

    seller_data = order_items[
        ["order_id", "seller_id", "price", "freight_value"]
    ].merge(
        orders_enriched[
            ["order_id", "is_late", "delivery_days", "review_score"]
        ],
        on="order_id",
        how="inner",
    )

    seller_metrics = (
        seller_data
        .groupby("seller_id")
        .agg(
            orders=("order_id", "nunique"),
            revenue=("price", "sum"),
            freight_value=("freight_value", "sum"),
            avg_delivery_days=("delivery_days", "mean"),
            avg_review_score=("review_score", "mean"),
        )
        .reset_index()
    )

    # One row per seller + order prevents multi-item orders
    # from inflating the number of late orders.
    seller_order_delivery = (
        seller_data[
            ["seller_id", "order_id", "is_late"]
        ]
        .dropna(subset=["is_late"])
        .drop_duplicates(
            subset=["seller_id", "order_id"]
        )
    )

    late_metrics = (
        seller_order_delivery
        .groupby("seller_id")
        .agg(
            evaluated_deliveries=("order_id", "nunique"),
            late_orders=("is_late", "sum"),
        )
        .reset_index()
    )

    late_metrics["late_rate"] = (
        late_metrics["late_orders"]
        / late_metrics["evaluated_deliveries"]
        * 100
    )

    seller_metrics = seller_metrics.merge(
        late_metrics,
        on="seller_id",
        how="left",
    )

    seller_metrics = seller_metrics.merge(
        sellers[
            ["seller_id", "seller_city", "seller_state"]
        ],
        on="seller_id",
        how="left",
    )

    return seller_metrics

def build_category_metrics(
    orders_enriched: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
    category_translation: pd.DataFrame,
) -> pd.DataFrame:
    """Build one-row-per-category performance metrics."""

    category_data = (
        order_items[
            ["order_id", "product_id", "price", "freight_value"]
        ]
        .merge(
            products[
                ["product_id", "product_category_name"]
            ],
            on="product_id",
            how="left",
        )
        .merge(
            category_translation,
            on="product_category_name",
            how="left",
        )
        .merge(
            orders_enriched[
                ["order_id", "is_late", "review_score"]
            ],
            on="order_id",
            how="inner",
        )
    )

    category_data["product_category_name_english"] = (
        category_data["product_category_name_english"]
        .fillna("unknown")
    )

    category_metrics = (
        category_data
        .groupby("product_category_name_english")
        .agg(
            orders=("order_id", "nunique"),
            items_sold=("product_id", "count"),
            revenue=("price", "sum"),
            freight_value=("freight_value", "sum"),
            avg_review_score=("review_score", "mean"),
        )
        .reset_index()
    )

    # One row per category + order prevents multi-item orders
    # from inflating late-order counts.
    category_order_delivery = (
        category_data[
            [
                "product_category_name_english",
                "order_id",
                "is_late",
            ]
        ]
        .dropna(subset=["is_late"])
        .drop_duplicates(
            subset=[
                "product_category_name_english",
                "order_id",
            ]
        )
    )

    late_metrics = (
        category_order_delivery
        .groupby("product_category_name_english")
        .agg(
            evaluated_deliveries=("order_id", "nunique"),
            late_orders=("is_late", "sum"),
        )
        .reset_index()
    )

    late_metrics["late_rate"] = (
        late_metrics["late_orders"]
        / late_metrics["evaluated_deliveries"]
        * 100
    )

    return category_metrics.merge(
        late_metrics,
        on="product_category_name_english",
        how="left",
    )