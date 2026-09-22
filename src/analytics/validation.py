import pandas as pd

def validate_required_columns(
    df: pd.DataFrame,
    required_columns: list[str],
    dataset_name: str = "dataset",
) -> None:
    """Ensure a dataframe contains the required columns."""

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"{dataset_name} is missing required columns: "
            f"{', '.join(missing)}"
        )


def validate_date_range(
    start_date: str | None,
    end_date: str | None,
) -> None:
    """Validate an optional date range."""

    if start_date and end_date:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)

        if start > end:
            raise ValueError(
                "start_date cannot be after end_date."
            )


def filter_orders(
    orders: pd.DataFrame,
    start_date: str | None = None,
    end_date: str | None = None,
    customer_state: str | None = None,
    category: str | None = None,
) -> pd.DataFrame:
    """Filter orders using common business dimensions."""

    validate_required_columns(
        orders,
        [
            "order_id",
            "order_purchase_timestamp",
            "customer_state",
            "product_categories",
        ],
        dataset_name="orders",
    )

    validate_date_range(
        start_date,
        end_date,
    )

    df = orders.copy()

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"]
    )

    if start_date:
        df = df[
            df["order_purchase_timestamp"]
            >= pd.to_datetime(start_date)
        ]

    if end_date:
        df = df[
            df["order_purchase_timestamp"]
            <= pd.to_datetime(end_date)
        ]

    if customer_state:
        df = df[
            df["customer_state"].str.upper()
            == customer_state.upper()
        ]

    if category:
        df = df[
            df["product_categories"]
            .fillna("")
            .str.contains(
                category,
                case=False,
                regex=False,
            )
        ]

    return df.copy()