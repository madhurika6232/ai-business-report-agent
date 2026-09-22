from pathlib import Path

import pandas as pd
import pytest

from src.ml.forecasting import (
    build_forecast_dataset,
    add_naive_forecast,
    naive_holdout_forecast,
    exponential_smoothing_forecast,
)

from src.ml.evaluation import (
    calculate_forecast_metrics,
    compare_forecast_models,
)


DATA_DIR = Path("data/processed")


@pytest.fixture(scope="module")
def orders():
    return pd.read_csv(
        DATA_DIR / "orders_enriched.csv"
    )


@pytest.fixture(scope="module")
def forecast_data(orders):
    return build_forecast_dataset(orders)


def test_forecast_dataset(forecast_data):
    assert len(forecast_data) == 20

    assert forecast_data["revenue"].notna().all()
    assert forecast_data["orders"].notna().all()

    assert (
        forecast_data["revenue"] >= 0
    ).all()


def test_naive_forecast(forecast_data):
    result = add_naive_forecast(
        forecast_data,
        target="revenue",
    )

    assert len(result) == 20
    assert result["forecast"].isna().sum() == 1

    assert result.iloc[1]["forecast"] == pytest.approx(
        result.iloc[0]["revenue"]
    )


def test_forecast_metrics():
    actual = [100, 120, 140]
    predicted = [90, 125, 150]

    metrics = calculate_forecast_metrics(
        actual,
        predicted,
    )

    assert metrics["mae"] >= 0
    assert metrics["rmse"] >= 0
    assert metrics["mape"] >= 0


def test_holdout_model_comparison(forecast_data):
    train = forecast_data.iloc[:-5].copy()
    test = forecast_data.iloc[-5:].copy()

    naive_predictions = naive_holdout_forecast(
        train,
        test,
    )

    naive_metrics = calculate_forecast_metrics(
        test["revenue"],
        naive_predictions,
    )

    holt_predictions = exponential_smoothing_forecast(
        train,
        periods=len(test),
    )

    holt_metrics = calculate_forecast_metrics(
        test["revenue"],
        holt_predictions,
    )

    comparison = compare_forecast_models(
        naive_metrics,
        holt_metrics,
    )

    assert naive_metrics["mape"] == pytest.approx(
        4.94,
        abs=0.01,
    )

    assert holt_metrics["mape"] == pytest.approx(
        27.41,
        abs=0.01,
    )

    assert comparison["winner"] == "baseline"

    assert (
        comparison["candidate_improvement_pct"] < 0
    )


def test_invalid_forecast_target(forecast_data):
    with pytest.raises(ValueError):
        add_naive_forecast(
            forecast_data,
            target="fake_target",
        )


def test_invalid_forecast_period(forecast_data):
    train = forecast_data.iloc[:-5]

    with pytest.raises(ValueError):
        exponential_smoothing_forecast(
            train,
            periods=0,
        )