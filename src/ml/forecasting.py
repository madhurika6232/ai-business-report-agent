"""
Revenue Forecasting

Business goal:
Forecast near-term marketplace revenue to support planning.

Success criteria:
- Beat a naive forecasting baseline.
- Evaluate using time-based validation.
- Report MAE, RMSE, and MAPE.
- Communicate forecast uncertainty.
"""

import pandas as pd


def build_forecast_dataset(
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """Build monthly revenue and order-volume time series."""

    df = orders.copy()

    df["order_month"] = pd.to_datetime(
        df["order_month"]
    )

    monthly = (
        df.groupby("order_month")
        .agg(
            revenue=("order_revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values("order_month")
    )

    return monthly

def add_naive_forecast(
    data: pd.DataFrame,
    target: str = "revenue",
) -> pd.DataFrame:
    """
    Create a naive one-step forecast.

    Prediction for each month equals the actual
    value from the previous month.
    """

    if target not in data.columns:
        raise ValueError(
            f"Target '{target}' does not exist."
        )

    df = data.copy()

    df["forecast"] = (
        df[target].shift(1)
    )

    return df

from statsmodels.tsa.holtwinters import ExponentialSmoothing


def exponential_smoothing_forecast(
    train: pd.DataFrame,
    periods: int,
    target: str = "revenue",
) -> list[float]:
    """Forecast future values using Holt's trend method."""

    if target not in train.columns:
        raise ValueError(
            f"Target '{target}' does not exist."
        )

    if periods <= 0:
        raise ValueError(
            "periods must be greater than 0."
        )

    model = ExponentialSmoothing(
        train[target],
        trend="add",
        seasonal=None,
        initialization_method="estimated",
    )

    fitted_model = model.fit(
        optimized=True
    )

    forecast = fitted_model.forecast(
        periods
    )

    return [
        float(value)
        for value in forecast
    ]


def naive_holdout_forecast(
    train: pd.DataFrame,
    test: pd.DataFrame,
    target: str = "revenue",
) -> list[float]:
    """Generate rolling naive forecasts for a holdout period."""

    if target not in train.columns or target not in test.columns:
        raise ValueError(
            f"Target '{target}' does not exist."
        )

    predictions = []

    previous_value = train.iloc[-1][target]

    for actual_value in test[target]:
        predictions.append(float(previous_value))
        previous_value = actual_value

    return predictions