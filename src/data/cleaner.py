import pandas as pd


ORDER_DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

REVIEW_DATE_COLUMNS = [
    "review_creation_date",
    "review_answer_timestamp",
]


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """Clean orders and restrict data to the reliable analysis period."""

    df = orders.copy()

    # Convert order timestamps
    for column in ORDER_DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column])

    # Use the reliable analysis period identified during EDA
    df = df[
        (df["order_purchase_timestamp"] >= "2017-01-01")
        & (df["order_purchase_timestamp"] < "2018-09-01")
    ].copy()

    return df


def clean_reviews(reviews: pd.DataFrame) -> pd.DataFrame:
    """Clean reviews and retain one review per order."""

    df = reviews.copy()

    # Convert review timestamps
    for column in REVIEW_DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column])

    # Some orders have multiple reviews.
    # Keep the most recently created review.
    df = (
        df.sort_values("review_creation_date")
        .drop_duplicates(subset="order_id", keep="last")
        .copy()
    )

    return df


def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    """Prepare product data for downstream processing."""

    df = products.copy()

    df["product_category_name"] = (
        df["product_category_name"]
        .fillna("unknown")
    )

    return df