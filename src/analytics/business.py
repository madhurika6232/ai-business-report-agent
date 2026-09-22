import pandas as pd


def get_business_summary(orders: pd.DataFrame) -> dict:
    """Calculate core marketplace business KPIs."""

    total_revenue = orders["order_revenue"].sum()
    total_orders = orders["order_id"].nunique()

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    total_items = orders["item_count"].sum()

    unique_customers = (
        orders["customer_unique_id"].nunique()
    )

    return {
        "total_revenue": round(float(total_revenue), 2),
        "total_orders": int(total_orders),
        "average_order_value": round(float(average_order_value), 2),
        "total_items": int(total_items),
        "unique_customers": int(unique_customers),
    }

def get_monthly_performance(orders: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly revenue, orders, AOV, and revenue growth."""

    df = orders.copy()

    df["order_month"] = pd.to_datetime(df["order_month"])

    monthly = (
        df.groupby("order_month")
        .agg(
            revenue=("order_revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values("order_month")
    )

    monthly["aov"] = (
        monthly["revenue"] / monthly["orders"]
    )

    monthly["revenue_growth_pct"] = (
        monthly["revenue"].pct_change() * 100
    )

    return monthly

def get_category_performance(
    categories: pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return top product categories ranked by revenue."""

    if top_n <= 0:
        raise ValueError("top_n must be greater than 0.")

    result = (
        categories
        .sort_values("revenue", ascending=False)
        .head(top_n)
        .copy()
    )

    result["revenue_share_pct"] = (
        result["revenue"]
        / categories["revenue"].sum()
        * 100
    )

    return result.reset_index(drop=True)


def get_state_performance(
    orders: pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """Calculate business performance by customer state."""

    if top_n <= 0:
        raise ValueError("top_n must be greater than 0.")

    state_performance = (
        orders
        .groupby("customer_state")
        .agg(
            revenue=("order_revenue", "sum"),
            orders=("order_id", "nunique"),
            customers=("customer_unique_id", "nunique"),
        )
        .reset_index()
    )

    state_performance["aov"] = (
        state_performance["revenue"]
        / state_performance["orders"]
    )

    total_revenue = state_performance["revenue"].sum()

    state_performance["revenue_share_pct"] = (
        state_performance["revenue"]
        / total_revenue
        * 100
    )

    return (
        state_performance
        .sort_values("revenue", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )